init -1002:
    # NOTE: For historical reasons we keep strings here instead of tuples
    default persistent._mas_submod_version_data = {}
    default persistent._mas_submod_settings = {}
    default persistent._mas_submod_install_history = set()
    default persistent._mas_submod_last_update_check = {}


init -1000 python in mas_submod_utils:
    # Init submods
    _init_and_load_submods()

init -990 python in mas_submod_utils:
    # Runs hooks at -995, the creators should have defined their hooks by now
    _Submod._run_submods_install_hooks()

init 10 python in mas_submod_utils:
    # Run updates if need be
    _Submod._run_submods_update_hooks()

# Cache this, we're not adding/removing submods after the initial load, this helps us keep 60 fps in the submods screen
define 10 mas_submod_utils.ALPHA_SORTED_SUBMODS = store.mas_submod_utils._Submod._get_alpha_sorted_submods()


init -1001 python in mas_submod_utils:
    import bisect
    import glob
    import re
    import random
    import os
    import json
    import sys
    import subprocess
    import dataclasses
    import datetime
    import time
    import threading
    import functools
    import typing

    from urllib.parse import urlparse
    from typing import (
        Any,
        Literal,
        Optional,
        Self,
    )
    from collections.abc import (
        Callable,
        Iterator,
        Iterable,
        Sequence,
    )
    from enum import Enum

    import store
    from store import (
        config,
        persistent,
        mas_utils,
        mas_logging,
        _mas_loader,
    )


    submod_log = mas_logging.init_log("submod_log")

    # NOTE: ALWAYS UPDATE VERSION IF YOU CHANGE HEADER FORMAT
    HEADER_VERSION = 1

    HEADER_GLOB = "**/header.json"
    SUBMODS_DIR = "Submods"

    # A string that can be used as a stable identifier
    RE_SAFE_NAME = re.compile(r"^[^\W\d][ \w\d]*[\w\d]$")


    class _Platform(str, Enum):
        """
        Enum for representing OS platforms that are supported by MAS
        """
        unknown = ""
        windows = "windows"
        linux = "linux"
        mac = "mac"

        @classmethod
        def get_current_os(cls) -> Self:
            if renpy.windows:
                return cls.windows

            elif renpy.linux:
                return cls.linux

            elif renpy.macintosh:
                return cls.mac

            return cls.unknown


    class _UpdateProviders(str, Enum):
        """
        Enum represents supported update providers
        """
        git = "git"


    class NonBlockingLock(python_object):
        """
        Allows to use locks without blocking the thread and utilise the with statement

        Example:
        ```python
        lock = NonBlockingLock(threading.Lock())
        with lock as has_grabbed:
            if not has_grabbed:
                # Lock is busy
                return
            # Lock is ours
            work_with_shared_state()
        ```
        """
        __slots__ = ("lock",)

        def __init__(self, lock) -> None:
            self.lock = lock

        def __enter__(self) -> bool:
            return self.lock.acquire(blocking=False)

        def __exit__(self, exc_type, exc_value, traceback) -> bool:
            self.lock.release()
            return False


    class Updater(python_object):
        __slots__ = (
            "submod",
            "provider",
            "_lock",
            "_latest_version",
            "_has_updated",
            "_is_idle",
        )

        UPDATE_CHECK_INTERVAL = datetime.timedelta(hours=0.5).total_seconds()

        def __init__(self, submod: "_Submod", provider: "_BaseUpdateProvider") -> None:
            self.submod = submod
            self.provider = provider
            self._lock = NonBlockingLock(threading.RLock())
            self._latest_version: tuple[int, ...] = ()
            self._has_updated = False
            self._is_idle = True

        @property
        def name(self) -> str:
            return self.submod.name

        @property
        def _last_update_check(self) -> float:
            return persistent._mas_submod_last_update_check.get(self.name, 1506038400.0)

        @_last_update_check.setter
        def _last_update_check(self, value: float) -> None:
            persistent._mas_submod_last_update_check[self.name] = value

        @property
        def current_version(self) -> tuple[int, ...]:
            return self.submod.version

        @property
        def current_version_str(self) -> str:
            return self.submod.version_str

        @property
        def latest_version(self) -> tuple[int, ...]:
            return self._latest_version

        @property
        def latest_version_str(self) -> tuple[int, ...]:
            return _dump_version(self._latest_version)

        def __repr__(self) -> str:
            return (
                f"<{type(self).__qualname__}(submod='{self.name}', provider='{type(self.provider).__qualname__}', "
                f"latest={self.latest_version_str}, last_check={datetime.datetime.fromtimestamp(self._last_update_check)}, "
                f"updated={self._has_updated}, idle={self._is_idle})>"
            )

        def _reset(self) -> None:
            with self._lock as has_grabbed:
                if not has_grabbed:
                    return
                self._latest_version = ()
                self._last_update_check = 1506038400.0
                self._has_updated = False

        def is_idle(self) -> bool:
            """
            Returns current status of the updater

            OUT:
                True if the updater is idling
                False if we're updating/fetching/etc
            """
            with self._lock as has_grabbed:
                if not has_grabbed:
                    return False

                return self._is_idle

        def can_check_for_updates(self, now: float | None = None) -> bool:
            """
            Checks if enough time has passed since last update check

            IN:
                now - current timestamp, if None we fetch time here

            OUT:
                True we should check for update
                False we shouldn't to avoid overloading
            """
            if now is None:
                now = time.time()
            return (now - self._last_update_check) > self.UPDATE_CHECK_INTERVAL

        def check_for_updates(self, now: float | None = None) -> None:
            """
            Fetchest latest available version for the submod

            OUT:
                version tuple or None if failed to fetch
            """
            with self._lock as has_grabbed:
                if not has_grabbed or not self._is_idle:
                    return

                self._is_idle = False
                try:
                    if now is None:
                        now = time.time()

                    if not self.can_check_for_updates(now):
                        return

                    self._latest_version = self.provider.fetch_latest_version()
                    self._last_update_check = now

                finally:
                    self._is_idle = True

        def has_update(self) -> bool:
            """
            Returns latest known status of update availability, does not check for update itself

            OUT:
                True if there's an update
                False otherwise
            """
            return (
                not self._has_updated
                and mas_utils.compare_versions(self.current_version, self.latest_version) < 0
            )

        def update(self) -> bool:
            """
            Updates the submod if there's an update available

            OUT:
                True if successfully updated
                False otherwise
            """
            with self._lock as has_grabbed:
                if not has_grabbed or not self._is_idle:
                    # Already updating
                    return False

                self._is_idle = False
                try:
                    self.check_for_updates()

                    if not self.has_update():
                        return False

                    if not self.provider.update(self.latest_version):
                        submod_log.error(f"failed to update submod '{self.name}'")
                        return False

                    self._has_updated = True
                    submod_log.info(f"updated submod '{self.name}' v{self.current_version_str} >>> v{_dump_version(self.latest_version)}")
                    return True

                finally:
                    self._is_idle = True

    class _BaseUpdateProvider(python_object):
        __slots__ = ()

        def fetch_latest_version(self) -> "tuple[int, ...] | None":
            raise NotImplementedError()

        def update(self, version: tuple[int, ...]) -> bool:
            raise NotImplementedError()

    class _GitUpdateProvider(_BaseUpdateProvider):
        __slots__ = ("_remote_url", "_repo_path")

        class _GitOutput(typing.NamedTuple):
            return_code: int
            output: str

        def __init__(self, remote_url: str, repo_path: str) -> None:
            self._remote_url = remote_url
            self._repo_path = repo_path

        @classmethod
        def _get_git_binaries(cls) -> str:
            """
            Returns name of the executable for git

            OUT:
                str
            """
            match _Platform.get_current_os():
                case _Platform.windows:
                    return "bin/git/windows/cmd/git.exe"
                case _Platform.linux:
                    return "bin/git/linux/git"
                case _Platform.mac:
                    # TODO: Somehow build git for mac?
                    # return "bin/git/mac/git"
                    # raise NotImplementedError("git updater doesn't support mac os")
                    return "bin/git/mac/git"
                case _:
                    raise NotImplementedError("git updater couldn't detect current os")

        @staticmethod
        def _safe_decode(data: bytes) -> str:
            """
            Decodes bytes into a unicode string, if impossible, return bytes string

            OUT:
                str
            """
            try:
                return data.decode(encoding="utf-8")
            except UnicodeDecodeError:
                submod_log.error(f"failed to decode git process output '{data!r}'", exc_info=True)
                return str(data)

        @classmethod
        def _exec_git(cls, command: str, *options: list[str], cwd: str | None = None, timeout: int | None = 30) -> "_GitUpdateProvider._GitOutput":
            """
            Runs git with the given arguments

            IN:
                command - git command to run
                *options -  command options to use
                cwd - the directory to execute from, by default uses wherever MAS is
                timeout - timeout for the process, None disables timeout

            OUT:
                tuple of status code and output
            """
            executable = os.path.join(config.gamedir, cls._get_git_binaries())
            args = [executable, command, *options]

            creationflags = 0
            if _Platform.get_current_os() is _Platform.windows:
                creationflags |= subprocess.CREATE_NO_WINDOW

            try:
                result = subprocess.run(
                    args,
                    # Explicitly declare pipes
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    # Avoid creating a window on windows
                    creationflags=creationflags,
                    # chdir
                    cwd=cwd,
                    timeout=timeout,
                    # Avoid potential injections
                    shell=False,
                )

            except OSError:
                submod_log.error("system failed to spawn a git process", exc_info=True)
                return cls._GitOutput(-64, "")

            except subprocess.TimeoutExpired:
                submod_log.error(f"timeout {timeout}s occured while waiting for the git process")
                return cls._GitOutput(-128, "")

            except Exception:
                submod_log.error(f"unexpected error while spawning a git process, args were: {args}", exc_info=True)
                return cls._GitOutput(-256, "")

            if result.returncode != 0:
                stderr_out = cls._safe_decode(result.stderr.strip())
                submod_log.error(f"git returned a non-zero status code {result.returncode}, output was: '{stderr_out}'")
                return cls._GitOutput(result.returncode, stderr_out)

            return cls._GitOutput(0, cls._safe_decode(result.stdout.strip()))

        def _is_within_repo(self) -> bool:
            """
            Checks if we're within a git repository
            """
            if not os.path.isdir(os.path.join(self._repo_path, ".git")):
                return False

            result = self._exec_git("rev-parse", "--is-inside-work-tree", cwd=self._repo_path)
            return result.return_code == 0 and result.output == "true"

        def _fetch(self) -> bool:
            """
            Fetches the remote

            OUT:
                True if success
                False otherwise
            """
            result = self._exec_git("fetch", "--prune", "--prune-tags", "--tags", cwd=self._repo_path)
            return result.return_code == 0

        def _get_tags(self) -> list[str]:
            """
            Retrieves all tags from the remote

            OUT:
                list of tags
            """
            if not self._fetch():
                return []
            result = self._exec_git("tag", "--list", cwd=self._repo_path)
            if result.return_code != 0:
                return []
            return result.output.split("\n")

        def _checkout(self, index: str) -> bool:
            """
            Checkouts to the given commit/tag/branch

            OUT:
                True if checout was successful
                False otherwise
            """
            if not self._fetch():
                return False
            result = self._exec_git("checkout", "--force", "--detach", index, cwd=self._repo_path)
            return result.return_code == 0

        def _init(self, url: str, index: str) -> bool:
            """
            Sets up a repository

            OUT:
                True if success
                False otherwise
            """
            result = self._exec_git("init", "--initial-branch=master", ".", cwd=self._repo_path)
            if result.return_code != 0:
                return False
            result = self._exec_git("remote", "add", "origin", self._remote_url, cwd=self._repo_path)
            if result.return_code != 0:
                return False

            return self._checkout(index)

        def _clone(self, url: str, index: str) -> None:
            """
            Clones a repo at the given tag from the given url

            IN:
                url - repository url
                index - git object to checkout

            OUT:
                True if checout was successful
                False otherwise
            """
            result = self._exec_git("clone", "--branch", index, "--depth", "1", url, self._repo_path)
            return result.return_code == 0

        def _ensure_within_repo(self) -> bool:
            """
            Checks if the submod is within a git repository, if not, attempts to create it

            OUT:
                True if we're within a repo and can proceed
                False if we're not within a repo
            """
            if self._is_within_repo():
                return True

            submod_log.warning(f"'{self._repo_path}' doesn't appear to be a git repository, we will attempt to fix this")
            if not self._init(self._remote_url, self.current_version_str):
                submod_log.error(f"failed to init repository at '{self._repo_path}'")
                return False

            submod_log.info(f"successfully inited repository at '{self._repo_path}'")
            return True

        def fetch_latest_version(self) -> "tuple[int, ...] | None":
            if not self._ensure_within_repo():
                return None

            all_versions: list[tuple[int, ...]] = []
            for tag in self._get_tags():
                # Check for both None and empty tags
                if ver := _safe_parse_version(tag):
                    # TODO: log bad tags?
                    all_versions.append(ver)

            if not all_versions:
                submod_log.error(f"failed to fetch latest version in '{self._repo_path}', no valid tags found")
                return None

            return _sort_versions(all_versions)[-1]

        def update(self, version: tuple[int, ...]) -> bool:
            return self._checkout(_dump_version(version))


    @dataclasses.dataclass(init=True, repr=True, eq=False, slots=True)
    class _UpdaterSchema(python_object):
        """
        Subschema for validating updater field of submod
        """
        # Name of the provider to use for updates
        provider: _UpdateProviders
        # Settings of the provider, can be different depending on the provider
        settings: dict[str, Any]

        def __post_init__(self):
            self.validate_provider()
            self.validate_settings()

        def validate_provider(self) -> None:
            if not isinstance(self.provider, str):
                raise TypeError("Submod updater provider must be a str")

            if self.provider not in _UpdateProviders.__members__:
                raise ValueError(f"Submod updater uses unknown provider '{self.provider}'")

            self.provider = _UpdateProviders(self.provider)

        def validate_settings(self) -> None:
            if not isinstance(self.settings, (dict, python_dict)):
                raise TypeError("Submod updater settings must be a dict")

            if not self.settings:
                raise ValueError("Submod updater settings are empty")

            match self.provider:
                case _UpdateProviders.git:
                    url = self.settings.get("url", None)
                    if url is None:
                        raise ValueError("Submod updater url wasn't provided in settings")
                    if not url:
                        raise ValueError("Submod updater url setting is empty")

                case _:
                    raise NotImplementedError(f"updater provider {self.provider} is not supported")

        @classmethod
        def from_json(cls, data: dict[str, Any]) -> Self:
            return cls(**data)

    @dataclasses.dataclass(init=True, repr=True, eq=False, slots=True)
    class _SubmodSchema(python_object):
        """
        Schema for validating submod json headers
        If there's an incompatible change between header version,
        we can handle it's here
        """
        ### NOTE: JSON specific:
        header_version: int
        ### NOTE: Submod specific:
        # Name of the submod author
        author: str
        # Name of the submod. Must be unique
        name: str
        # A version number following the semantic versioning format (https://semver.org/)
        version: str
        # Submod dir, NOTE: this isn't part of the json, will be added dynamically during loading
        directory: str
        # List of modules of this submod. Must be non-empty, all modules must exist, forwardslashes must be used instead of backslashes,
        # paths must also not start with a slash, nor end in one, likewise it must not end in .rpy* or a slash
        modules: list[str]
        # A short description for the submod. Does not support interpolation?
        description: str = dataclasses.field(default="")
        updater: "_UpdaterSchema | None" = None
        # Dictionary in the following structure: {'name': ('minimum_version', 'maximum_version')}
        # corresponding to the needed submod name and version required
        # NOTE: versions must be passed in the same way as the version property is done
        dependencies: "dict[str, tuple[str | None, str | None]]" = dataclasses.field(default_factory=dict)
        # String referring to the screen used for the submod's settings
        settings_pane: str = dataclasses.field(default="")
        # List of co-authors who helped work on this submod
        coauthors: list[str] = dataclasses.field(default_factory=list)
        # Set of OS that are supported by the submod
        os_whitelist: frozenset[_Platform] = dataclasses.field(default=frozenset())
        # Set of OS that the submod does not support
        os_blacklist: frozenset[_Platform] = dataclasses.field(default=frozenset())

        def __post_init__(self):
            self.validate_header_version()
            self.validate_author()
            self.validate_name()
            self.validate_version()
            self.validate_modules()
            self.validate_description()
            self.validate_updater()
            self.validate_dependencies()
            self.validate_settings_pane()
            self.validate_coauthors()
            self.validate_os_whitelist()
            self.validate_os_blacklist()

        @classmethod
        def from_json(cls, data: dict[str, Any]) -> Self:
            return cls(**data)

        def validate_header_version(self) -> None:
            if not isinstance(self.header_version, int):
                raise ValueError("Submod header version must be int")
            if self.header_version <= 0:
                raise ValueError(f"Submod header version '{self.header_version}' is invalid")
            if self.header_version < HEADER_VERSION:
                raise ValueError(
                    f"Submod header version '{self.header_version}' is outdated (expected {HEADER_VERSION})",
                )
            if self.header_version > HEADER_VERSION:
                raise ValueError(
                    f"Submod header version '{self.header_version}' is unknown (expected {HEADER_VERSION})",
                )

        @staticmethod
        def _is_str_safe(value: str) -> None:
            return re.match(RE_SAFE_NAME, value) is not None

        def validate_author(self) -> None:
            if not isinstance(self.author, str):
                raise ValueError("Submod author name must be a str")
            if not self._is_str_safe(self.author):
                raise ValueError(f"Submod author name '{self.author}' contains unsafe characters")

        def validate_name(self) -> None:
            if not isinstance(self.name, str):
                raise ValueError("Submod name must be a str")
            if not self._is_str_safe(self.name):
                raise ValueError(f"Submod name '{self.name}' contains unsafe characters")
            self.name = self.name.strip()

        def validate_version(self) -> None:
            if not _is_valid_version(self.version):
                raise ValueError(f"Submod version number '{self.version}' is invalid")

        def validate_modules(self) -> None:
            if not isinstance(self.modules, (list, python_list)):
                raise ValueError(f"Submod modules must be a list of strings")

            if not self.modules:
                raise ValueError("Submod must define at least one module")

            for m in self.modules:
                if (
                    not isinstance(m, str)
                    or re.match(r'^(?!.*\\)(?!\/)(?!.*\.rpy.*$).*[^\/]$', m) is None
                ):
                    raise ValueError(f"Submod module '{m}' is invalid")

            # IMPORTANT: Sort in alpha order
            modules = tuple(sorted(self.modules))

            if not _mas_loader.do_modules_exist(*(f"{self.directory}/{m}" for m in modules)):
                raise ValueError(
                    "One or more submod modules are missing: {}".format(
                        ", ".join(map(lambda s: f"'{s}'", modules))
                    )
                )

        def validate_description(self) -> None:
            if not isinstance(self.description, str):
                raise ValueError("Submod description must be a str")

        def validate_updater(self) -> None:
            if self.updater is None:
                submod_log.warning(f"submod '{self.name}' has no updater defined and won't be able to update")
                return

            if not isinstance(self.updater, (dict, python_dict)):
                raise TypeError("Submod updater must be a dict")

            self.updater = _UpdaterSchema.from_json(self.updater)

        def validate_dependencies(self) -> None:
            if not isinstance(self.dependencies, (dict, python_dict)):
                raise ValueError("Submod dependencies must be a dict")

            for k, v in self.dependencies.items():
                if not isinstance(v, (list, python_list)) or len(v) != 2:
                    raise ValueError(f"Dependency '{k}' has invalid version tuple '{v}'")

                for i in v:
                    if i is not None and not _is_valid_version(i):
                        raise ValueError(f"Dependency '{k}' has invalid version '{i}'")

        def validate_settings_pane(self) -> None:
            if not isinstance(self.settings_pane, str):
                raise ValueError("Submod settings_pane must be a str")

        def validate_coauthors(self) -> None:
            if not isinstance(self.coauthors, (list, python_list)):
                raise ValueError("Submod coauthors must be a list of strings")

            for item in self.coauthors:
                if not isinstance(item, str):
                    raise ValueError("Submod coauthors items must be strings")
                if not self._is_str_safe(item):
                    raise ValueError(f"Submod coauthor '{item}' contains unsafe characters")

        def validate_os_whitelist(self) -> None:
            if not isinstance(self.os_whitelist, (frozenset, list, python_list)):
                raise ValueError("Submod os_whitelist must be a list of strings")

            for item in self.os_whitelist:
                if not isinstance(item, str):
                    raise ValueError("Submod os_whitelist items must be strings")

                if item.lower() not in _Platform.__members__:
                    raise ValueError(f"Submod os_whitelist item '{item}' is unknown")

            self.os_whitelist = frozenset(_Platform(v.lower()) for v in self.os_whitelist)

        def validate_os_blacklist(self) -> None:
            if not isinstance(self.os_blacklist, (frozenset, list, python_list)):
                raise ValueError("Submod os_blacklist must be a list of strings")

            for item in self.os_blacklist:
                if not isinstance(item, str):
                    raise ValueError("Submod os_blacklist items must be strings")

                if item.lower() not in _Platform.__members__:
                    raise ValueError(f"Submod os_blacklist item '{item}' is unknown")

            self.os_blacklist = frozenset(_Platform(v.lower()) for v in self.os_blacklist)

            if (common := (self.os_whitelist & self.os_blacklist)):
                raise ValueError(
                    f"Submod has common values in os_whitelist and os_blacklist which is an error: {', '.join(common)}"
                )


    def _parse_version(version: str) -> tuple[int, ...]:
        """
        Parses a string version number to list format.

        NOTE: Does not handle errors

        IN:
            version - version string to parse

        OUT:
            tuple - representing the parsed version number
        """
        return tuple(map(int, version.split('.')))

    def _safe_parse_version(version: str) -> tuple[int, ...] | None:
        """
        Parses a string version number to list format.

        IN:
            version - version string to parse

        OUT:
            tuple - representing the parsed version number
            None if version is invalid
        """
        try:
            return tuple(map(int, version.split(".")))
        except ValueError:
            return None

    def _is_valid_version(version: str) -> bool:
        """
        Checks if the given version string has valid format

        IN:
            version - version string to test

        OUT:
            boolean
        """
        return _safe_parse_version(version) is not None

    def _dump_version(version: tuple[int, ...]) -> str:
        """
        Dumps a version tuple back into a str

        IN:
            version - version tuple

        OUT:
            str
        """
        return ".".join(map(str, version))

    def _sort_versions(versions: Sequence[tuple[int, ...]]) -> list[tuple[int, ...]]:
        """
        Takes a sequence of versions and returns a sorted list of those versions

        IN:
            versions - list of version tuples

        OUT:
            list of version tuples where at index 0 is the oldest and at index -1 is the latest
        """
        return sorted(versions, key=functools.cmp_to_key(mas_utils.compare_versions))

    class _ComparableVersionWrapper(python_object):
        """
        See implementation of functools.cmp_to_key
        this is used for bisect as a workaround its limitations
        """
        __slots__ = ("version",)
        def __init__(self, version):
            self.version = version
        def __lt__(self, other):
            return mas_utils.compare_versions(self.version, other.version) < 0
        def __gt__(self, other):
            return mas_utils.compare_versions(self.version, other.version) > 0
        def __eq__(self, other):
            return mas_utils.compare_versions(self.version, other.version) == 0
        def __le__(self, other):
            return mas_utils.compare_versions(self.version, other.version) <= 0
        def __ge__(self, other):
            return mas_utils.compare_versions(self.version, other.version) >= 0
        __hash__ = None

    def _sort_by_version():
        """
        This is functools.cmp_to_key for the poor
        """
        return _ComparableVersionWrapper

    def _generate_update_label(author: str, name: str, version: str) -> str:
        """
        Creates an update label name from submod info

        For example:
            author name: MonikaAfterStory,
            submod name: Example Submod
            submod vers: 1.2.3

        becomes:
            label monikaafterstory_example_submod_v1_2_3
        """
        fmt_author = lambda s: s.lower().replace(" ", "_")

        author = fmt_author(author)
        name = fmt_author(name)
        version = version.replace(".", "_")

        return f"{author}_{name}_v{version}"


    def _fmt_path(header_path: str) -> str:
        """
        Formats path to the submod header to be pretty printer
        """
        return f"'{os.path.dirname(header_path)}'"

    def _read_submod_header(header_path: str) -> "dict | None":
        """
        Tries to read a submod header at the given path

        IN:
            header_path - str, abs path to the submod header

        OUT:
            dict - raw json data
            None - if failed to read the json
        """
        header_json = None
        try:
            with renpy.open_file(header_path.split("/game/")[1], encoding="utf-8") as header_file:
                header_json = json.load(header_file)

        except Exception as e:
            submod_log.error(
                f"failed to load submod from {_fmt_path(header_path)}:\n    Failed to read header",
                exc_info=True
            )
            return None

        if not header_json:
            submod_log.error(
                f"failed to load submod from {_fmt_path(header_path)}:\n    Empty header"
            )
            return None

        return header_json

    def _parse_submod_header(raw_header: dict, header_path: str) -> "_SubmodSchema | None":
        """
        This does extra processing on header, validation, and setting default values

        IN:
            raw_header - dict, the parsed submod json
            path - str, abs path to the submod header

        OUT:
            _SubmodSchema - if successfully parsed
            None - if failed
        """
        # Dynamically add submod dir
        submod_dir = os.path.relpath(
            os.path.dirname(header_path),
            start=config.gamedir
        ).replace("\\", "/")
        raw_header["directory"] = submod_dir

        try:
            return _SubmodSchema.from_json(raw_header)

        except Exception as e:
            submod_log.error(f"failed to load submod from {_fmt_path(header_path)}: {e}")
            return None

    def _try_init_submod(header_path: str) -> None:
        """
        Reads a submod json header at the given path,
        validates and and tries to init the submod

        IN:
            header_path - str, abs path to the submod header
        """
        if not (raw_header := _read_submod_header(header_path)):
            return

        if not (header := _parse_submod_header(raw_header, header_path)):
            return

        try:
            submod = _Submod(
                author=header.author,
                name=header.name,
                version=_parse_version(header.version),
                directory=header.directory,
                modules=header.modules,
                description=header.description,
                # Gets set later
                updater=None,
                dependencies=header.dependencies,
                settings_pane=header.settings_pane,
                coauthors=header.coauthors,
                os_whitelist=header.os_whitelist,
                os_blacklist=header.os_blacklist,
            )
            if header.updater is None:
                return

            match header.updater.provider:
                case _UpdateProviders.git:
                    provider = _GitUpdateProvider(header.updater.settings["url"], submod.abs_directory)

                case _:
                    raise RuntimeError("unreachable code")

            submod.updater = Updater(submod, provider)

        except SubmodError as e:
            submod_log.error(
                f"failed to load submod at: {_fmt_path(header_path)}:\n    {e}",
            )

        except Exception as e:
            submod_log.critical(
                f"critical error while validating submod at: {_fmt_path(header_path)}",
                exc_info=True,
            )

    def _init_submods() -> None:
        """
        Scans and inits submods
        """
        search_path = os.path.join(config.gamedir, SUBMODS_DIR, HEADER_GLOB)
        for fn in glob.iglob(search_path, recursive=True):
            _try_init_submod(fn)

    def _log_inited_submods() -> None:
        if _Submod.has_any_submods():
            disabled_txt = " (inactive)"
            empty_txt = ""
            submod_log.info(
                "INSTALLED SUBMODS:\n{}".format(
                    ",\n".join(
                        f"    '{submod.name}' v{submod.version_str}{disabled_txt if not submod.is_active else empty_txt}"
                        for submod in _Submod._get_alpha_sorted_submods()
                    )
                )
            )

    def _init_and_load_submods() -> None:
        """
        Finds and loads submods
        """
        _init_submods()
        # Verify topological order is possible
        _Submod._disable_circular_dependency_submods()
        # Verify we can run all the submods
        _Submod._disable_os_incompatible_submods()
        # Verify the dependencies are met
        _Submod._disable_unmet_dependency_submods()
        _log_inited_submods()
        _Submod._load_submods()


    class SubmodError(Exception):
        def __init__(self, msg: str) -> None:
            self.msg = msg

        def __str__(self) -> str:
            return self.msg

    class DependencyCycleError(SubmodError):
        def __init__(self, submod: "_Submod") -> None:
            super().__init__("cycle: ")
            self.chain = []
            self.add(submod)

        def add(self, submod: "_Submod") -> None:
            self.chain.append(submod)

        def __str__(self) -> str:
            return super().__str__() + " < ".join(f"'{s.name} v{s.version_str}'" for s in self.chain)


    class _SubmodSettings():
        """
        Static class for managing submod settings
        """
        _SETTING_IS_SUBMOD_ENABLED = "is_submod_enabled"
        _SETTING_IS_AUTO_UPDATE_CHECK_ENABLED = "is_auto_update_check_enabled"

        @classmethod
        def _create_setting(cls, submod: "_Submod", key: str, default) -> bool:
            """
            Defines a submod setting (including intermediate keys) with
            the given default value

            IN:
                submod - the submod object
                key - the setting unique key
                default - the default value of the setting

            OUT:
                bool - True if created, False if not
            """
            if persistent._mas_submod_settings is None:
                persistent._mas_submod_settings = {}

            setings = persistent._mas_submod_settings

            if submod.name not in setings:
                setings[submod.name] = {}

            if key not in setings[submod.name]:
                setings[submod.name][key] = default
                return True

            return False

        @classmethod
        def _get_setting(cls, submod: "_Submod", key: str, default: Any) -> Any:
            """
            Returns a setting for a submod

            IN:
                submod - the submod object
                key - the setting unique key
                default - the default value of the setting (if doesn't exist)

            OUT:
                setting value
            """
            try:
                return persistent._mas_submod_settings[submod.name][key]

            except KeyError:
                cls._create_setting(submod, key, default)
                return default

        @classmethod
        def _set_setting(cls, submod: "_Submod", key: str, value) -> None:
            """
            Sets a setting for a submod

            IN:
                submod - the submod object
                key - the setting unique key
                value - the setting value
            """
            try:
                persistent._mas_submod_settings[submod.name][key] = value

            except KeyError:
                cls._create_setting(submod, key, value)

        @classmethod
        def is_submod_enabled(cls, submod: "_Submod") -> bool:
            return cls._get_setting(submod, cls._SETTING_IS_SUBMOD_ENABLED, False)

        @classmethod
        def enable_submod(cls, submod: "_Submod") -> None:
            cls._set_setting(submod, cls._SETTING_IS_SUBMOD_ENABLED, True)

        @classmethod
        def disable_submod(cls, submod: "_Submod") -> None:
            cls._set_setting(submod, cls._SETTING_IS_SUBMOD_ENABLED, False)

        @classmethod
        def toggle_submod(cls, submod: "_Submod") -> None:
            if cls.is_submod_enabled(submod):
                cls.disable_submod(submod)
            else:
                cls.enable_submod(submod)

        @classmethod
        def is_auto_update_check_enabled(cls, submod: "_Submod") -> bool:
            return cls._get_setting(submod, cls._SETTING_IS_AUTO_UPDATE_CHECK_ENABLED, True)

        @classmethod
        def enable_auto_update_check(cls, submod: "_Submod") -> None:
            cls._set_setting(submod, cls._SETTING_IS_AUTO_UPDATE_CHECK_ENABLED, True)

        @classmethod
        def disable_auto_update_check(cls, submod: "_Submod") -> None:
            cls._set_setting(submod, cls._SETTING_IS_AUTO_UPDATE_CHECK_ENABLED, False)

        @classmethod
        def toggle_auto_update_check(cls, submod: "_Submod") -> None:
            if cls.is_auto_update_check_enabled(submod):
                cls.disable_auto_update_check(submod)
            else:
                cls.enable_auto_update_check(submod)


    class _Submod(python_object):
        """
        Submod class
        """
        __slots__ = (
            "author",
            "name",
            "version",
            "directory",
            "modules",
            "description",
            "updater",
            "dependencies",
            "settings_pane",
            "coauthors",
            "os_whitelist",
            "os_blacklist",
            "_failed_to_load",
        )

        # The string is used to join author and coauthors strings together, moved here so submods can translate it
        AND_STR = _("and")

        # SubmodName: Submod
        _submod_map: "dict[str, _Submod]" = {}
        # SubmodName: (Version: Function)
        _submod_update_hooks: "dict[str, dict[str, Callable[[SubmodUpdateInfo], None]]]" = {}
        # SubmodName: Function
        _submod_first_install_hooks: "dict[str, Callable[[], None]]" = {}
        # SubmodName: Function
        _submod_install_hooks: "dict[str, Callable[[], None]]" = {}

        def __init__(
            self,
            author: str,
            name: str,
            version: tuple[int, ...],
            directory: str,
            modules: list[str],
            description: str,
            updater: "Updater | None",
            dependencies: "dict[str, tuple[str | None, str | None]]",
            settings_pane: str,
            coauthors: list[str],
            os_whitelist: frozenset[_Platform],
            os_blacklist: frozenset[_Platform],
        ):
            """
            Submod object constructor

            RAISES:
                SubmodError
            """
            if name in self._submod_map:
                raise SubmodError(
                    f"submod '{name}' has been installed twice. Please, uninstall the duplicate.",
                )

            self.author = author
            self.name = name
            self.version = version
            self.directory = directory
            self.modules = modules
            self.description = description
            self.updater = updater
            self.dependencies = dependencies
            self.settings_pane = settings_pane
            self.coauthors = coauthors
            self.os_whitelist = os_whitelist
            self.os_blacklist = os_blacklist

            # If for whatever reason this submod doesn't work, mark it as such
            self._failed_to_load = False

            self._submod_map[name] = self

        # @staticmethod
        # def convert_name_to_id(name: str) -> str:
        #     return re.sub(r"[  ]+", " ", name.lower()).replace(" ", "_")

        # @property
        # def id(self) -> str:
        #     return self.convert_name_to_id(self.name)

        @property
        def abs_directory(self) -> str:
            return os.path.join(config.gamedir, self.directory)

        @property
        def version_str(self) -> str:
            return _dump_version(self.version)

        @property
        def failed_to_load(self) -> bool:
            return self._failed_to_load

        @property
        def is_active(self) -> bool:
            return not self.failed_to_load and self.is_enabled

        @property
        def is_enabled(self) -> bool:
            return _SubmodSettings.is_submod_enabled(self)

        @property
        def is_auto_update_check_enabled(self) -> bool:
            return _SubmodSettings.is_auto_update_check_enabled(self)

        def _mark_broken(self) -> None:
            """
            Marks submod as invalid and disables its loading so the user can safely boot up the game next time
            """
            self._failed_to_load = True
            _SubmodSettings.disable_submod(self)

        def fmt_author_str(self) -> str:
            """
            Returns a human-readable prettified string containing the author and coauthors
            """
            if not self.coauthors:
                return self.author

            if len(self.coauthors) == 1:
                return f"{self.author} {self.AND_STR} {self.coauthors[0]}"

            return f"{self.author}, {', '.join(self.coauthors[:-1])} {self.AND_STR} {self.coauthors[-1]}"

        def __repr__(self) -> str:
            return f"<{type(self).__qualname__}('{self.name}' v{self.version_str} by {self.author})>"

        @classmethod
        def has_any_submods(cls) -> bool:
            """
            Checks if any submods were loaded

            OUT:
                bool
            """
            return bool(cls._submod_map)

        @classmethod
        def _get_submod(cls, name: str) -> "_Submod | None":
            """
            Gets the submod with the name provided

            IN:
                name - name of the submod to get

            OUT:
                Submod object if the submod is installed and registered
                None if not found
            """
            return cls._submod_map.get(name, None)

        @classmethod
        def _get_alpha_sorted_submods(cls) -> "list[_Submod]":
            """
            Returns a list of all the submods sorted alphabetically by name
            NOTE: this is intended to be used for UI/display only

            OUT:
                list of Submod objects
            """
            return sorted(cls._submod_map.values(), key=lambda x: x.name)

        @classmethod
        def _get_topologically_sorted_submods(cls, only_active: bool) -> "list[_Submod]":
            """
            Topologically sorts the submods from dependencies to dependents
            NOTE: load order of independent submods is not declared, not stable,
                and no guarantees are made
            NOTE: this doesn't account of missing dependencies, versions mismatches, or anything of sorts,
                it just sorts and returns the submods, everything else is done in other methods

            IN:
                only_active - whether to only sort and return enabled submods

            OUT:
                list of sorted submod objects
            """
            out: "list[_Submod]" = []
            finished: "set[str]" = set()
            processing: "set[str]" = set()
            unvisited: "set[_Submod]" = set(
                submod
                for submod in cls._submod_map.values()
                if submod.is_active or not only_active
            )

            def visit(submod: "_Submod") -> None:
                if submod.name in finished:
                    return
                if submod.name in processing:
                    raise DependencyCycleError(submod)

                processing.add(submod.name)

                for dependency_name in submod.dependencies.keys():
                    dependency = cls._get_submod(dependency_name)
                    # If the dependency is missing, we don't care about it here
                    # If it's disabled, then it depends on the provided flag
                    if dependency is None or (not dependency.is_active and only_active):
                        continue

                    try:
                        visit(dependency)

                    except DependencyCycleError as e:
                        e.add(submod)
                        raise

                unvisited.discard(submod.name)
                processing.remove(submod.name)
                finished.add(submod.name)
                out.append(submod)

            while unvisited:
                submod = unvisited.pop()
                visit(submod)

            return out

        def has_update_hook_for(self, version: tuple[int, ...]) -> bool:
            """
            Checks if an update hook has been registered for the given version

            IN:
                version - update version

            OUT:
                True if there's a hook
                False otherwise
            """
            return self.name in self._submod_update_hooks and version in self._submod_update_hooks[self.name]

        def register_update_hook(self, version: tuple[int, ...], func: "Callable[[SubmodUpdateInfo], None]") -> None:
            """
            Registers a function to run on an update

            IN:
                version - update version
                func - the function to call on update
            """
            if self.name not in self._submod_update_hooks:
                self._submod_update_hooks[self.name] = {}
            if version not in self._submod_update_hooks[self.name]:
                self._submod_update_hooks[self.name][version] = func

        def has_first_install_hook(self) -> bool:
            """
            Checks if a first-time-install hook has been registered for this submod

            OUT:
                True if there's a hook
                False otherwise
            """
            return self.name in self._submod_first_install_hooks

        def register_first_install_hook(self, func: Callable[[], None]) -> None:
            """
            Registers a function to run on first install

            IN:
                func - the function to call on first install
            """
            if self.name not in self._submod_first_install_hooks:
                self._submod_first_install_hooks[self.name] = func

        def has_install_hook(self) -> bool:
            """
            Checks if an install hook has been registered for this submod

            OUT:
                True if there's a hook
                False otherwise
            """
            return self.name in self._submod_install_hooks

        def register_install_hook(self, func: Callable[[], None]) -> None:
            """
            Registers a function to run on successful install

            IN:
                func - the function to call on first install
            """
            if self.name not in self._submod_install_hooks:
                self._submod_install_hooks[self.name] = func

        def _run_install_hook(self) -> None:
            """
            Runs on-install hook for the submod
            """
            if not self.is_active:
                return

            hook = self._submod_install_hooks.get(self.name, None)
            if hook is None:
                return

            try:
                hook()

            # Catch base exc to handle as many cases as possible
            except BaseException as e:
                func_mod = getattr(hook, "__module__", "")
                func_name = getattr(hook, "__qualname__", hook.__name__)
                func_fullname = ".".join((func_mod, func_name))
                submod_log.error(
                    f"exception while running submod '{self.name}' on-install hook '{func_fullname}'",
                    exc_info=True,
            )

            else:
                submod_log.info(f"successfully executed on-install hook for submod '{self.name}'")

        def _compare_versions(self, comparative_vers: tuple[int, ...]) -> Literal[-1, 0, 1]:
            """
            Generic version checker for submods

            IN:
                comparative_vers - the version we're comparing to (or need the current version to be at or greater than)

            OUT:
                integer:
                    - (-1) if the current version number is less than the comparitive version
                    - 0 if the current version is the same as the comparitive version
                    - 1 if the current version is greater than the comparitive version
            """
            return mas_utils.compare_versions(
                self.version,
                comparative_vers
            )

        def _has_just_installed_for_first_time(self) -> bool:
            """
            Checks if this submod has just been installed for the first time

            OUT:
                bool
            """
            return self.name not in persistent._mas_submod_version_data

        def _run_first_time_install_hook(self) -> None:
            """
            Runs first-time-install hook for the submod
            """
            if not self.is_active:
                return

            hook = self._submod_first_install_hooks.get(self.name, None)
            if hook is None:
                return

            try:
                hook()

            # Catch base exc to handle as many cases as possible
            except BaseException as e:
                func_mod = getattr(hook, "__module__", "")
                func_name = getattr(hook, "__qualname__", hook.__name__)
                func_fullname = ".".join((func_mod, func_name))
                submod_log.error(
                    f"exception while running submod '{self.name}' hook '{func_fullname}' on first install",
                    exc_info=True,
            )

            else:
                submod_log.info(f"successfully executed first-install hook for submod '{self.name}'")

            # Set version to avoid executing this again
            persistent._mas_submod_version_data[self.name] = self.version_str

        def _should_run_update_hooks(self) -> bool:
            """
            Checks if this submod instance has been be updated (its version number has incremented since last load)
            and whether we should call its update hooks

            OUT:
                True if the version number has incremented from the persistent one
                False otherwise
            """
            old_version_str = persistent._mas_submod_version_data.get(self.name, None)
            #If we don't have an old vers, we're installing for the first time and aren't updating at all
            if old_version_str is None:
                return False

            old_version_tuple = _safe_parse_version(old_version_str)
            #Persist data was bad, return False
            if old_version_tuple is None:
                submod_log.error(
                    (
                        "unexpected exception occured while parsing version data "
                        f"for submod '{self.name}', update hooks will NOT be called. Version data: '{old_version_str!r}'"
                    ),
                )
                return False

            cmp_result = self._compare_versions(old_version_tuple)
            if cmp_result < 0:
                submod_log.warning(
                    (
                        f"submod '{self.name}' appears to have been downgraded from '{old_version_str}' to "
                        f"'{self.version_str}'. THIS COULD UNPREDICTABLY CORRUPT SAVES"
                    ),
                )
            # If current submod version is higher than the last known, then the submod has been updated
            return cmp_result > 0

        def _run_update_hooks(self, last_update_version: str) -> None:
            """
            Runs update hooks for the submod, starting after the given version

            IN:
                last_update_version - the version of the last installed update in string format like "1.2.3"

            ASSUMES:
                last_update_version is valid version
            """
            if not self.is_active:
                return

            # Get all version + hooks for this submod
            versions_to_hooks = self._submod_update_hooks.get(self.name, None)
            if not versions_to_hooks:
                return

            # Sort versions from oldest to newest
            update_versions = _sort_versions(versions_to_hooks.keys())
            # Find the next update version we need to run
            next_update_index = bisect.bisect_right(
                update_versions,
                # NOTE: bisect doesn't call the key function for the search value,
                # for some usecases it makes sense, and for others you can call the key function yourself.
                # Sadly in our case due to how functools.cmp_to_key works,
                # we can't do that, so we use our own implementation with a workaround
                _ComparableVersionWrapper(_parse_version(last_update_version)),
                # TODO: Consider caching if submods ever get *a lot* of updates (maybe above 1k?)
                key=_ComparableVersionWrapper,
            )
            if next_update_index >= len(update_versions):
                # If index is out of bounds, it means we don't have an update hook registered for the update
                return

            for idx in range(next_update_index, len(update_versions)):
                ver = update_versions[idx]
                if self._compare_versions(ver) < 0:
                    # If the version from the update hooks is somehow higher than the currently installed,
                    # we stop runing hooks. This shouldn't happen because we're checking for this in the decorator, but just in case
                    submod_log.error(f"submod '{self.name}' has update hook for version '{_dump_version(ver)}', but submod version is lower '{self.version_str}'")
                    return

                hook = versions_to_hooks[ver]
                try:
                    hook(SubmodUpdateInfo(last_update_version, _dump_version(ver), self.version_str))

                # Catch base exc to handle as many cases as possible
                except BaseException as e:
                    func_mod = getattr(hook, "__module__", "")
                    func_name = getattr(hook, "__qualname__", hook.__name__)
                    func_fullname = ".".join((func_mod, func_name))
                    submod_log.error(
                        f"exception while running submod '{self.name}' hook '{func_fullname}' for version '{_dump_version(ver)}'",
                        exc_info=True,
                )
                else:
                    submod_log.info(f"successfully executed update hook '{_dump_version(ver)}' for submod '{self.name}'")

                # We ran the hook for this version, bump version in persistent to avoid running the same hook again
                # This is just in case of a crash or power outage mid-update
                persistent._mas_submod_version_data[self.name] = _dump_version(ver)

        @classmethod
        def _run_submods_update_hooks(cls) -> None:
            """
            Checks if submods have updated and runs the appropriate update hooks for them
            """
            for submod in cls._get_topologically_sorted_submods(only_active=True):
                if submod._has_just_installed_for_first_time():
                    submod._run_first_time_install_hook()
                elif submod._should_run_update_hooks():
                    submod._run_update_hooks(persistent._mas_submod_version_data[submod.name])

                # Always adjust the value to reflect the correct version
                persistent._mas_submod_version_data[submod.name] = submod.version_str

        def _check_dependencies(self) -> None:
            """
            Checks to see if the dependencies for this submod are met

            RAISES:
                SubmodError - on dependency check fail
            """
            for dependency_name, minmax_version_tuple in self.dependencies.items():
                dependency_submod = self._get_submod(dependency_name)

                if dependency_submod is None:
                    raise SubmodError(
                        f"dependency '{dependency_name}' is not installed and is required"
                    )

                if not dependency_submod.is_active:
                    raise SubmodError(
                        f"dependency '{dependency_name}' is disabled or cannot be loaded"
                    )

                #Now we need to split our minmax
                minimum_version, maximum_version = minmax_version_tuple

                #First, check the minimum version. If we get -1, we're out of date
                if (
                    minimum_version
                    and dependency_submod._compare_versions(_parse_version(minimum_version)) < 0
                ):
                    raise SubmodError(
                        "dependency '{}' is out of date. Version '{}' is required. Installed version is '{}'".format(
                            dependency_submod.name,
                            minimum_version,
                            dependency_submod.version_str
                        )
                    )

                #If we have a maximum version, we should check if we're above it.
                #If we get 1, this is incompatible and we should crash to avoid other ones
                elif (
                    maximum_version
                    and dependency_submod._compare_versions(_parse_version(maximum_version)) > 0
                ):
                    raise SubmodError(
                        "dependency '{}' is incompatible. Version '{}' is compatible. Installed version is '{}'".format(
                            dependency_submod.name,
                            maximum_version,
                            dependency_submod.version_str
                        )
                    )

        @classmethod
        def _disable_unmet_dependency_submods(cls) -> None:
            """
            Disables the submods that are missing dependencies
            """
            for submod in cls._get_topologically_sorted_submods(only_active=True):
                try:
                    submod._check_dependencies()

                # Technically there should only be SubmodError
                # but let's make it extra safe and instead catch broad Exception
                except Exception as e:
                    if isinstance(e, SubmodError):
                        submod_log.error(
                            f"dependency check failed for submod '{submod.name}':\n    {e}"
                        )
                    else:
                        submod_log.critical(
                            f"critical error while validating dependencies for submod '{submod.name}'",
                            exc_info=True
                        )
                    submod._mark_broken()

        def _check_os_compatibility(self) -> None:
            """
            Checks if this submod supports user OS

            RAISES:
                SubmodError - on OS check fail
            """
            current_os = _Platform.get_current_os()

            if (
                not current_os
                or (self.os_whitelist and current_os not in self.os_whitelist)
                or (self.os_blacklist and current_os in self.os_blacklist)
            ):
                raise SubmodError(
                    f"submod '{self.name}' does not support current operating system."
                )

        @classmethod
        def _disable_os_incompatible_submods(cls) -> None:
            """
            Disables the submods that do not support user OS
            """
            for submod in cls._get_topologically_sorted_submods(only_active=True):
                try:
                    submod._check_os_compatibility()

                except SubmodError as e:
                    submod_log.error(
                        f"OS check for submod '{submod.name}' failed:\n    {e}"
                    )
                    submod._mark_broken()

        @classmethod
        def _disable_circular_dependency_submods(cls) -> None:
            """
            Disables the submods that cause cyclic dependency, for example:
                submod A depends on itself
                submod A depends on submod B while submod B depends on submod A
            """
            while True:
                try:
                    cls._get_topologically_sorted_submods(only_active=True)

                except DependencyCycleError as e:
                    submod_log.error(
                        f"circular dependencies detected:\n    {e}"
                    )
                    submod_log.info(f"we will attempt to disable bad actor submods and load again")
                    for submod in e.chain:
                        submod._mark_broken()

                else:
                    # No circular dependencies, we can continue load process
                    break

        def _load(self) -> None:
            """
            NOTE: SHOULD NEVER BE CALLED DIRECTLY

            Loads modules of this submod

            RAISES:
                SubmodError - on module failure
            """
            if not self.is_active:
                return

            for mod_name in self.modules:
                full_mod_name = f"{self.directory}/{mod_name}"
                try:
                    renpy.include_module(full_mod_name)

                except BaseException as e:
                    # We can't abort loading at this point,
                    # and ignoring doesn't sit right with me
                    # it can cause more issues down the pipeline
                    msg = f"critical error while loading module '{mod_name}' for submod '{self.name}': {e!r}"
                    submod_log.critical(msg)
                    # Disable broken submod so the user can boot the game next time
                    self._mark_broken()
                    raise SubmodError(msg) from e

        @classmethod
        def _load_submods(cls) -> None:
            """
            NOTE: SHOULD NEVER BE CALLED DIRECTLY

            Loads modules for every submod
            """
            for submod in cls._get_topologically_sorted_submods(only_active=True):
                submod._load()

        @classmethod
        def _run_submods_install_hooks(cls) -> None:
            """
            NOTE: MUST BE USED IN A NODE AFTER _load_submods AS EARLY AS POSSIBLE

            Runs installation hooks for the new submods that weren't found in the last session,
            this includes submods that were installed for the first time and reinstalled submods
            """
            previous_install_history = frozenset(persistent._mas_submod_install_history)
            new_install_history = set()

            for submod in cls._get_topologically_sorted_submods(only_active=True):
                if submod.name not in previous_install_history:
                    submod._run_install_hook()
                new_install_history.add(submod.name)

            persistent._mas_submod_install_history = new_install_history

        def is_updatable(self) -> bool:
            """
            Checks if this submod has an updater and the submod is enabled

            OUT:
                bool
            """
            return self.updater is not None and _SubmodSettings.is_submod_enabled(self)

        def can_check_for_update(self) -> bool:
            """
            Checks if we can fetch new updates

            OUT:
                bool
            """
            return self.is_updatable() and self.updater.is_idle() and self.updater.can_check_for_updates()

        def can_update(self) -> bool:
            """
            Checks if we can update the submod

            OUT:
                bool
            """
            return self.is_updatable() and self.updater.is_idle() and self.updater.has_update()

        def check_for_updates_in_background(self) -> None:
            """
            Checks for new update for the submod in a thread
            """
            if not self.can_check_for_update():
                return

            def worker() -> None:
                try:
                    self.updater.check_for_updates()
                except BaseException:
                    submod_log.error(f"failed to check for update for '{self.name}'", exc_info=True)

            thread = threading.Thread(target=worker, name=f"submod '{self.name}' update checker")
            thread.daemon = True
            thread.start()

        def install_update_in_background(self) -> None:
            """
            Installs new update for the submod in a thread
            """
            if not self.can_update():
                return

            def worker() -> None:
                try:
                    self.updater.update()
                except BaseException:
                    submod_log.error(f"failed to install update for '{self.name}'", exc_info=True)

            thread = threading.Thread(target=worker, name=f"submod '{self.name}' update installer")
            thread.daemon = True
            thread.start()

        @classmethod
        def notify_about_submods_updates_in_background(cls) -> None:
            """
            Checks for new updates and shows a notification in a thread

            ASSUMES: we're in runtime
            """
            def worker() -> None:
                try:
                    update_lines = []
                    for submod in cls._get_alpha_sorted_submods():
                        # NOTE: We don't check for updates submods that the user has disabled
                        # However we allow updating submods that are marked as broken - for example to install a fix
                        if submod.is_auto_update_check_enabled and submod.can_check_for_update():
                            submod.updater.check_for_updates()
                            if submod.can_update():
                                new_version_str = _dump_version(submod.updater.latest_version)
                                update_lines.append(_(f"Submod '{submod.name}' has an update to v{new_version_str}"))

                    if not update_lines:
                        return

                    if store.mas_isMoniAff(higher=True):
                        if store.mas_isA01():
                            chance = 10.0
                        else:
                            chance = 365.0
                        with_chibi = random.random() < 1.0/chance
                    else:
                        with_chibi = False
                    _display_submod_update_notify(update_lines, with_chibi)

                except BaseException:
                    submod_log.error("failed to check and notify for updates", exc_info=True)

            thread = threading.Thread(target=worker, name="submods update notifier")
            thread.daemon = True
            thread.start()


    ### Common submod functions

    def _display_submod_update_notify(messages: Iterable[str], with_chibi: bool = False) -> None:
        if not messages:
            return
        renpy.hide_screen("mas_submod_update_notify", immediately=True)
        renpy.show_screen("mas_submod_update_notify", messages=messages, with_chibi=with_chibi)
        if with_chibi:
            renpy.music.play(
                ("<silence 6.0>", "mod_assets/sounds/effects/metal-pipe-falling.mp3"),
                loop=False,
                relative_volume=min(max(len(messages) / 4.0, 0.1), 3.0),
                channel="sound",
            )
            renpy.music.pump()
        renpy.restart_interaction()


    class SubmodUpdateInfo(python_object):
        """
        This gets passed as the first argument to update hooks, it holds
        information about the submod and applied update which might be useful
        in update scripts
        """
        __slots__ = ("from_version", "to_version", "current_version")

        def __init__(self, from_version: str, to_version: str, current_version: str):
            """
            Constructor

            IN:
                from_version - the previously installed submod version
                    NOTE: this might NOT be equal to the version that came before 'to_version'
                        in case the user updates through multiple versions
                to_version - the version of the update
                current_version - the version of the currently installed submod
                    NOTE: this might NOT be equal to 'to_version' in case the user
                        updates through multiple versions
            """
            self.from_version = from_version
            self.to_version = to_version
            self.current_version = current_version

        def __repr__(self) -> str:
            from_version = self.from_version
            to_version = self.to_version
            current_version = self.current_version
            return f"<{type(self).__qualname__}({from_version=}, {to_version=}, {current_version=})>"

    def on_submod_update(name: str, version: str) -> Callable[[Callable[[SubmodUpdateInfo], None]], Callable[[SubmodUpdateInfo], None]]:
        """
        Decorator to register a function to run when a submod named 'name' updates
        to version 'version' or higher

        Usage:
            ```py
            @mas_submod_utils.on_submod_update("Example", "0.1.0")
            def on_update_0_1_0(update: mas_submod_utils.SubmodUpdateInfo) -> None:
                ...
            ```

        IN:
            name - submod name
            version - the version to update to

        OUT:
            returns the original function
        """
        def decorator(func: Callable[[SubmodUpdateInfo], None]) -> Callable[[SubmodUpdateInfo], None]:
            submod = _Submod._get_submod(name)
            if submod is None:
                submod_log.error(f"trying to add an update hook for the submod '{name}' that doesn't exist")
                return func

            version_tuple = _safe_parse_version(version)
            if version_tuple is None:
                submod_log.error(f"update hook for the submod '{name}' has invalid version '{version}'")
                return func

            if submod._compare_versions(version_tuple) < 0:
                submod_log.error(
                    (
                        f"trying to add an update hook '{version}' for the submod '{name}', "
                        f"but current submod version is '{submod.version_str}' (lower than the update hook)"
                    ),
                )
                return func

            if submod.has_update_hook_for(version_tuple):
                submod_log.error(f"can't register an update hook for submod '{name}' for version '{version}', a hook has already been added")
                return func

            submod.register_update_hook(version_tuple, func)

            return func

        return decorator

    def on_submod_first_install(name: str) -> Callable[[Callable[[], None]], Callable[[], None]]:
        """
        Decorator to register a function to run when the user first time installs
        the given submod

        Usage:
            ```py
            @mas_submod_utils.on_submod_first_install("Example")
            def on_first_install() -> None:
                ...
            ```

        IN:
            name - submod name

        OUT:
            returns the original function
        """
        def decorator(func: Callable[[], None]) -> Callable[[], None]:
            submod = _Submod._get_submod(name)
            if submod is None:
                submod_log.error(f"trying to add an installation hook to the submod '{name}' that doesn't exist")
                return func

            if submod.has_first_install_hook():
                submod_log.error(f"can't add an installation hook to the submod '{name}', a hook has already been added")
                return func

            submod.register_first_install_hook(func)

            return func

        return decorator

    def on_submod_install(name: str) -> Callable[[Callable[[], None]], Callable[[], None]]:
        """
        Decorator to register a function to run on submod installation

        Usage:
            ```py
            @mas_submod_utils.on_submod_install("Example")
            def submod_setup() -> None:
                ...
            ```

        IN:
            name - submod name

        OUT:
            returns the original function
        """
        def decorator(func: Callable[[], None]) -> Callable[[], None]:
            submod = _Submod._get_submod(name)
            if submod is None:
                submod_log.error(f"trying to add an installation hook to the submod '{name}' that doesn't exist")
                return func

            if submod.has_install_hook():
                submod_log.error(f"can't add an installation hook to the submod '{name}', a hook has already been added")
                return func

            submod.register_install_hook(func)

            return func

        return decorator

    def is_submod_installed(name: str, version: "str | None" = None) -> bool:
        """
        Checks if a submod with `name` is installed

        IN:
            name - name of the submod to check for
            version - if a specific version (or greater) is installed
            (NOTE: if None, this is ignored. Default: None)

        OUT:
            boolean:
                - True if submod with name is installed
                - False otherwise
        """
        submod = _Submod._get_submod(name)

        if submod is None:
            return False

        if version:
            return submod._compare_versions(_parse_version(version)) >= 0

        return True

    @mas_utils.deprecated(use_instead="is_submod_installed")
    def isSubmodInstalled(*args, **kwargs):
        return isSubmodInstalled(*args, **kwargs)

    def get_submod_directory(name: str) -> "str | None":
        """
        Returns a submod directory relative to the game folder

        IN:
            name - str, name of the submod

        OUT:
            str - relative path to the submod
            None - no submod with the given name was found
        """
        if (submod := _Submod._get_submod(name)) is None:
            return None

        return submod.directory


screen mas_submod_update_notify(messages, with_chibi=False):
    zorder 999

    timer 4 action Hide("mas_submod_update_notify")

    fixed:
        at (mas_submod_update_notify_appear_chibi_tfm if with_chibi else mas_submod_update_notify_appear_norm_tfm)

        vbox:
            box_reverse True

            if with_chibi:
                add "chibika 3":
                    at mas_submod_update_notify_chibi_hang

            frame:
                at transform:
                    alpha 0.9

                vbox:
                    for message in messages:
                        text "[message!tq]" style "notify_text"

transform mas_submod_update_notify_chibi_hang:
    animation
    anchor (80, 84)
    subpixel True
    transform_anchor True
    rotate_pad True

    xpos 0.4
    rotate -25.0
    block:
        warp _warper.ease_cubic 1.0 rotate -65.0
        warp _warper.ease_cubic 1.0 rotate -25.0
        repeat

transform mas_submod_update_notify_appear_norm_tfm:
    animation
    subpixel True

    on show:
        yanchor 1.0
        linear 1.0 yanchor 0.0
    on hide:
        linear 1.0 yanchor 1.0

transform mas_submod_update_notify_appear_chibi_tfm:
    animation
    subpixel True
    transform_anchor True
    rotate_pad True

    on show:
        yanchor 1.0
        warp _warper.easein_bounce 1.25 yanchor 0.125
        pause 0.1
        warp _warper.ease_quart 1.0 yanchor 0.0
    on hide:
        anchor (0.0, 0.0)
        warp _warper.easein_elastic 1.0 rotate 33.0
        warp _warper.easeout_expo 0.75:
            rotate 90.0
            ypos 1.0
            xpos 0.05


init -999 python in mas_submod_utils:
    import os
    import sys

    from types import ModuleType
    from importlib.util import (
        spec_from_file_location,
        module_from_spec,
    )

    def import_from_path(name: str, path: str, *, is_global: bool = False) -> ModuleType:
        """
        Dynamically imports a module from the given relative path
        This is like Nodejs 'require'

        Example:
            my_module = import_from_path("my_module", "some/path/my_module.py")
            my_module.hello_world()

        IN:
            name - str, the name to import the mode as
            path - str, relative path to the module (relative to gamedir)
            is_global - bool, whether or not add the module to 'sys.modules'
                (Default: False)

        OUT:
            the module object

        RAISES:
            ModuleNotFoundError - if failed to find the module
        """
        path = os.path.join(renpy.config.gamedir, path)
        # If it's a dir, then it's a module, so we should find its __init__.py
        if os.path.isdir(path):
            path = os.path.join(path, "__init__.py")

        spec = spec_from_file_location(name, path)
        if spec is None:
            raise ModuleNotFoundError(f"Failed to dynamically import '{path}' as '{name}', not found")

        module = module_from_spec(spec)

        if is_global:
            sys.modules[name] = module

        spec.loader.exec_module(module)

        return module


#START: Function Plugins
init -1000 python in mas_submod_utils:
    import bisect
    import inspect
    import store
    import typing

    from store import mas_utils
    from collections.abc import Callable

    #Store the current label for use elsewhere
    current_label = None
    #Last label
    last_label = None

    #Dict of all function plugins
    function_plugins: "dict[str, list[_FPEntry]]" = {}

    #Default priority
    _FP_DEF_PRIORITY: int = 0

    PRIORITY_SORT_KEY = lambda x: x[1][2]

    class _FPEntry(typing.NamedTuple):
        callable_: Callable
        priority: int

        def __repr__(self) -> str:
            return (
                f"<FunctionPluginEntry({self.callable_.__qualname__}, "
                f"priority={self.priority})>"
            )

    #START: Decorator Function
    def functionplugin(key: str, *, priority: int = _FP_DEF_PRIORITY, auto_error_handling: bool = True) -> Callable:
        """
        Decorator function to register a plugin

        The same as register_plugin. See its doc for parameter details
        """
        def wrap(_function: Callable) -> Callable:
            register_plugin(
                key,
                _function,
                priority=priority,
            )
            return _function
        return wrap

    #START: Internal functions
    def register_plugin(key: str, callable_: Callable, *, priority: int = _FP_DEF_PRIORITY, auto_error_handling: bool = True) -> None:
        """
        Registers a function to the function_plugins dict

        NOTE: Does NOT allow overwriting of existing functions in the dict
        NOTE: Function must be callable
        NOTE: Functions run when a label matching the key for the function is:
            called, jumped, or fallen through to.
            Or if plugged into a function, when a function by the name of the key calls getAndRunFunctions
        NOTE: If you need to provide args/kwargs to the function,
            wrap it into functools.partial

        IN:
            key - key to add the function to.
                NOTE: The key is either a label, or a function name
                NOTE: Function names only work if the function contains a getAndRunFunctions call.
                    Without it, it does nothing.
            _funcallable_ction - function to register
            auto_error_handling - unused
            priority - Order priority to run functions
                (Like init levels, the lower the number, the earlier it runs)
        """
        global function_plugins

        # Check for overrides if the key is a label
        if renpy.has_label(key):
            key = _get_override_label(key)

        entry = _FPEntry(
            callable_=callable_,
            priority=priority,
        )

        if key not in function_plugins:
            function_plugins[key] = []

        bisect.insort_right(function_plugins[key], entry, key=lambda e: e.priority)

    @store.mas_utils.deprecated(use_instead="mas_submod_utils.register_plugin")
    def registerFunction(*args, **kwargs):
        register_plugin(*args, **kwargs)

    def unregister_plugin(key: str, callable_: Callable) -> bool:
        """
        Unregisters a function from the function_plugins dict

        IN:
            key - key the function we want to unregister is in
            callable_ - function we want to unregister

        OUT:
            boolean:
                - True if function was unregistered successfully
                - False otherwise
        """
        global function_plugins

        hooks = function_plugins.get(key, ())
        for i, entry in enumerate(hooks):
            if entry.callable_ == callable_:
                hooks.pop(i)
                if not hooks:
                    function_plugins.pop(key)
                return True

        return False

    @store.mas_utils.deprecated(use_instead="mas_submod_utils.unregister_plugin")
    def unregisterFunction(*args, **kwargs):
        unregister_plugin(*args, **kwargs)

    def execute_plugins(key: str | None = None) -> None:
        """
        Gets and runs functions within the key provided

        IN:
            key - Key to retrieve and run functions from
        """
        global function_plugins

        #If the key isn't provided, we assume it from the caller
        if not key:
            key = inspect.stack()[1][3]

        hooks = function_plugins.get(key, ())
        for entry in hooks:
            try:
                store.__run(entry.callable_)

            except (renpy.game.JumpException, renpy.game.CallException):
                # Allow advanced users to use renpy.call and renpy.jump
                # NOTE: this will prevent other plugins from executing and will terminate
                # the python block renpy is currently executing, this can easily lead to bugs
                raise

            except Exception as ex:
                store.mas_utils.mas_log.error(f"function plugin hook '{entry}' for key '{key}' failed: {ex}")

    @store.mas_utils.deprecated(use_instead="mas_submod_utils.execute_plugins")
    def getAndRunFunctions(*args, **kwargs):
        execute_plugins(*args, **kwargs)

    def _get_override_label(_label):
        """
        Gets the override label for the given label (will follow the chain if overrides are overridden)

        IN:
            _label - label to get the override label for

        OUT:
            string representing the last label in the override chain or _label if there are no overrides
        """
        while _label in renpy.config.label_overrides:
            _label = renpy.config.label_overrides[_label]
        return _label

#Global run area
init -990 python:
    def __run(_function, *args, **kwargs):
        """
        Private function to run a function in the global store
        """
        return _function(*args)

#Label callback to get last label and run function plugins from the label
init 999 python:
    def _mas_label_callback(name, abnormal):
        """
        Function to run plugin functions and store the last label
        """
        #First, update the last label to what was current
        store.mas_submod_utils.last_label = store.mas_submod_utils.current_label
        #Now we can update the current
        store.mas_submod_utils.current_label = name
        #Run functions
        store.mas_submod_utils.execute_plugins(name)

        #Let's also check if the current label is an override label, if so, we'll then mark the base label as seen
        base_label = _OVERRIDE_LABEL_TO_BASE_LABEL_MAP.get(name)
        if base_label is not None:
            persistent._seen_ever[base_label] = True

    config.label_callback = _mas_label_callback
