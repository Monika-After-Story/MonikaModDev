init -1000:
    # NOTE: For historical reasons we keep strings here instead of tuples
    default persistent._mas_submod_version_data = {}
    default persistent._mas_submod_settings = {}

init 10 python in mas_submod_utils:
    #Run updates if need be
    _Submod._run_submods_update_hooks()

init -999 python in mas_submod_utils:
    # Init submods
    _init_and_load_submods()

init -1000 python in mas_submod_utils:
    import bisect
    import glob
    import re
    import os
    import json
    import sys
    import subprocess
    import dataclasses
    import time
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

    # String must start with an alpha/underscore character, and can contain only alphanumerics and underscores
    LABEL_SAFE_NAME = re.compile(r'^[a-zA-Z_][ 0-9a-zA-Z_]*$')

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


    class _BaseUpdateProvider(python_object):
        __slots__ = ("_submod", "_settings")

        def __init__(self, submod: "_Submod", settings: dict[str, Any]) -> None:
            self._submod = submod
            self._settings = settings

        def get_latest_version(self) -> tuple[int, ...]:
            """
            Returns the latest available version for the submod

            OUT:
                version tuple
            """
            raise NotImplementedError()

        def has_update(self) -> bool:
            """
            Checks if there's an update available

            OUT:
                True if there's an update
                False otherwise
            """
            raise NotImplementedError()

        def update(self) -> bool:
            """
            Updates the submod if there's an update available

            OUT:
                True if successfully updated
                False otherwise
            """
            raise NotImplementedError()

    class _GitUpdateProvider(_BaseUpdateProvider):
        """
        Updater utilising git
        """
        __slots__ = (
            "_latest_version",
            "_last_update_check",
            "_has_updated",
        )

        class _GitOutput(typing.NamedTuple):
            return_code: int
            output: str

        # In seconds
        UPDATE_CHECK_INTERVAL = 3600 * 6

        def __init__(self, submod: "_Submod", settings: dict[str, Any]) -> None:
            super().__init__(submod, settings)
            self._latest_version = None  # type: tuple[int, ...] | None
            self._last_update_check = 0
            self._has_updated = False

        def _reset(self) -> None:
            self._latest_version = None
            self._last_update_check = 0
            self._has_updated = False

        @property
        def _name(self) -> str:
            return self._submod.name

        @property
        def _current_version(self) -> tuple[int, ...]:
            return self._submod.version

        @property
        def _current_version_str(self) -> str:
            return self._submod.version_str

        @property
        def _remote_url(self) -> str:
            return self._settings["url"]

        @property
        def _repo_path(self) -> str:
            return self._submod.abs_directory

        @classmethod
        def _get_git_binaries(cls) -> str:
            """
            Returns name of the executable for git

            OUT:
                str
            """
            match _Platform.get_current_os():
                case _Platform.windows:
                    return "bin/windows/cmd/git.exe"
                case _Platform.linux:
                    return "bin/linux/git"
                case _Platform.mac:
                    # TODO: Somehow build git for mac?
                    raise NotImplementedError("git updater doesn't support mac os")
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
        def _exec_git(cls, command: str, *options: list[str], cwd: str | None = None, timeout: int | None = 10) -> "_GitUpdateProvider._GitOutput":
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

        def _fetch_latest_version(self) -> "tuple[int, ...] | None":
            """
            Fetches tags from the remote and returns the latest version
            """
            if not self._is_within_repo():
                submod_log.warning(f"submod '{self._name}' doesn't appear to be within a git repository, we will attempt to fix this")
                if not self._init(self._remote_url, self._current_version_str):
                    submod_log.error(f"failed to init repository for submod '{self._name}'")
                    return None
                submod_log.info(f"successfully inited repository for submod '{self._name}'")

            all_versions = []  # type: list[tuple[int, ...]]
            for tag in self._get_tags():
                # Check for both None and empty tags
                if ver := _safe_parse_version(tag):
                    # TODO: log bad tags?
                    all_versions.append(ver)

            if not all_versions:
                submod_log.error(f"failed to fetch latest version for submod '{self._name}', no valid tags found")
                return None

            return _sort_versions(all_versions)[-1]

        def _update_latest_version(self, now: float | None = None) -> None:
            """
            Checks and updates the latest version

            IN:
                now - current time in seconds, by default uses system time
            """
            if now is None:
                now = time.time()
            if self._latest_version is None or (now - self._last_update_check) > self.UPDATE_CHECK_INTERVAL:
                self._latest_version = self._fetch_latest_version()
                self._last_update_check = now

        def get_latest_version(self) -> tuple[int, ...]:
            self._update_latest_version()
            if self._latest_version is None:
                # This is bad, fallback
                return ()

            return self._latest_version

        def has_update(self) -> bool:
            return not self._has_updated and mas_utils.compare_versions(self._current_version, self.get_latest_version()) < 0

        def update(self) -> bool:
            if not self.has_update():
                return False

            if not self._checkout(_dump_version(self._latest_version)):
                submod_log.error(f"failed to update submod '{self._name}'")
                return False

            self._has_updated = True
            submod_log.info(f"updated submod '{self._name}' {self._current_version_str} >>> {_dump_version(self._latest_version)}")
            return True


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

            # TODO: use match or smth?
            if self.provider is _UpdateProviders.git:
                url = self.settings.get("url", None)
                if url is None:
                    raise ValueError("Submod updater url wasn't provided in settings")
                if not url:
                    raise ValueError("Submod updater url setting is empty")

            else:
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
        def _is_str_label_safe(value: str) -> None:
            return re.match(LABEL_SAFE_NAME, value) is not None

        def validate_author(self) -> None:
            if not isinstance(self.author, str):
                raise ValueError("Submod author name must be a str")
            if not self._is_str_label_safe(self.author):
                raise ValueError(f"Submod author name '{self.author}' contains unsafe characters")

        def validate_name(self) -> None:
            if not isinstance(self.name, str):
                raise ValueError("Submod name must be a str")
            if not self._is_str_label_safe(self.name):
                raise ValueError(f"Submod name '{self.name}' contains unsafe characters")

        def validate_version(self) -> None:
            # TODO: regex check version r'^[0-9]+(\.[0-9]+)*$'
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
                if not self._is_str_label_safe(item):
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
            with open(header_path) as header_file:
                header_json = json.load(header_file)

        except Exception as e:
            submod_log.error(
                f"Failed to load submod from {_fmt_path(header_path)}:\n    Failed to read header",
                exc_info=True
            )
            return None

        if not header_json:
            submod_log.error(
                f"Failed to load submod from {_fmt_path(header_path)}:\n    Empty header"
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
            submod_log.error(f"Failed to load submod from {_fmt_path(header_path)}: {e}")
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

            if header.updater.provider is _UpdateProviders.git:
                updater = _GitUpdateProvider(submod, header.updater.settings)

            else:
                raise RuntimeError("unreachable code")

            submod.updater = updater

        except SubmodError as e:
            submod_log.error(
                f"Failed to load submod at: {_fmt_path(header_path)}:\n    {e}",
            )

        except Exception as e:
            submod_log.critical(
                f"Critical error while validating submod at: {_fmt_path(header_path)}",
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
            disabled_txt = " (disabled)"
            empty_txt = ""
            submod_log.info(
                "INSTALLED SUBMODS:\n{}".format(
                    ",\n".join(
                        f"    '{submod.name}' v{submod.version_str}{disabled_txt if not submod.is_enabled else empty_txt}"
                        for submod in _Submod._iter_submods()
                    )
                )
            )

    def _init_and_load_submods() -> None:
        """
        Loads submods
        """
        # Init submods
        _init_submods()
        # Verify we can run all the submods
        _Submod._remove_os_incompatible_submods()
        # Verify installed dependencies
        _Submod._remove_unmet_dependency_submods()
        # Log
        _log_inited_submods()
        # Finally load submods
        _Submod._load_submods()


    class SubmodError(Exception):
        def __init__(self, msg: str):
            self.msg = msg

        def __str__(self):
            return self.msg


    class _SubmodSettings():
        """
        Static class for managing submod settings
        """
        _SETTING_IS_SUBMOD_ENABLED = "is_enabled"

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
        def _get_setting(cls, submod: "_Submod", key: str, default):
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
            return cls._get_setting(submod, cls._SETTING_IS_SUBMOD_ENABLED, True)

        @classmethod
        def enable_submod(cls, submod: "_Submod"):
            cls._set_setting(submod, cls._SETTING_IS_SUBMOD_ENABLED, True)

        @classmethod
        def disable_submod(cls, submod: "_Submod"):
            cls._set_setting(submod, cls._SETTING_IS_SUBMOD_ENABLED, False)

        @classmethod
        def toggle_submod(cls, submod: "_Submod") -> bool:
            if cls.is_submod_enabled(submod):
                cls.disable_submod(submod)
                return False

            cls.enable_submod(submod)
            return True


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
            "_is_loading_failure",
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
            updater: "_BaseUpdateProvider | None",
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
                    f"Submod '{name}' has been installed twice. Please, uninstall the duplicate.",
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
            self._is_loading_failure = False

            self._submod_map[name] = self

        @property
        def abs_directory(self) -> str:
            return os.path.join(config.gamedir, self.directory)

        @property
        def version_str(self) -> str:
            return _dump_version(self.version)

        @property
        def is_loading_failure(self) -> bool:
            return self._is_loading_failure

        @property
        def is_enabled(self) -> bool:
            return not self.is_loading_failure and _SubmodSettings.is_submod_enabled(self)

        def _mark_broken(self) -> None:
            """
            Marks submod as invalid and disables its loading so the user can safely boot up the game next time
            """
            self._is_loading_failure = True
            _SubmodSettings.disable_submod(self)

        def fmt_author_str(self) -> str:
            """
            Returns human-readable prettified string containing the author and coauthors
            """
            if not self.coauthors:
                return self.author

            if len(self.coauthors) == 1:
                return f"{self.author} {self.AND_STR} {self.coauthors[0]}"

            return f"{self.author}, {', '.join(self.coauthors[:-1])} {self.AND_STR} {self.coauthors[-1]}"

        def __repr__(self) -> str:
            return f"<{type(self).__qualname__}('{self.name}' v{self.version_str} by {self.author})>"

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
                    f"Exception while running submod '{self.name}' on-install hook '{func_fullname}'",
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
                    f"Exception while running submod '{self.name}' hook '{func_fullname}' on first install",
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
                        f"Exception while running submod '{self.name}' hook '{func_fullname}' for version '{_dump_version(ver)}'",
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
            # TODO: sort submods in total order, first update the submods that other submods depend on
            #Iter thru all submods we've got stored
            for submod in cls._iter_submods():
                if submod._has_just_installed_for_first_time():
                    submod._run_first_time_install_hook()
                elif submod._should_run_update_hooks():
                    submod._run_update_hooks(persistent._mas_submod_version_data[submod.name])

                # Always adjust the value to reflect the correct version
                persistent._mas_submod_version_data[submod.name] = submod.version_str

        def _check_dependencies(self):
            """
            Checks to see if the dependencies for this submod are met

            RAISES:
                SubmodError - on dependency check fail
            """
            for dependency_name, minmax_version_tuple in self.dependencies.items():
                dependency_submod = self._get_submod(dependency_name)

                if dependency_submod is None:
                    raise SubmodError(
                        f"Dependency '{dependency_name}' is not installed and is required"
                    )

                if not dependency_submod.is_enabled:
                    raise SubmodError(
                        f"Dependency '{dependency_name}' is disabled and cannot be loaded"
                    )

                #Now we need to split our minmax
                minimum_version, maximum_version = minmax_version_tuple

                #First, check the minimum version. If we get -1, we're out of date
                if (
                    minimum_version
                    and dependency_submod._compare_versions(_parse_version(minimum_version)) < 0
                ):
                    raise SubmodError(
                        "Dependency '{}' is out of date. Version '{}' is required. Installed version is '{}'".format(
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
                        "Dependency '{}' is incompatible. Version '{}' is compatible. Installed version is '{}'".format(
                            dependency_submod.name,
                            maximum_version,
                            dependency_submod.version_str
                        )
                    )

        @classmethod
        def _remove_unmet_dependency_submods(cls):
            """
            Checks to see if all the submods dependencies are met
            """
            # Can't use an iterator here, we're modifying the map
            for submod in cls._get_submods():
                try:
                    submod._check_dependencies()

                # Technically there should only be SubmodError
                # but let's make it extra safe and instead catch broad Exception
                except Exception as e:
                    if isinstance(e, SubmodError):
                        submod_log.error(
                            f"Dependency check failed for submod '{submod.name}':\n    {e}"
                        )
                    else:
                        submod_log.critical(
                            f"Critical error while validating dependencies for submod '{submod.name}'",
                            exc_info=True
                        )
                    submod._mark_broken()

        def _check_os_compatibility(self):
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
                    f"Submod '{self.name}' does not support current operating system."
                )

        @classmethod
        def _remove_os_incompatible_submods(cls):
            """
            Removes submods that do not support user OS
            """
            for submod in cls._get_submods():
                try:
                    submod._check_os_compatibility()

                except SubmodError as e:
                    submod_log.error(
                        f"OS check for submod '{submod.name}' failed:\n    {e}"
                    )
                    submod._mark_broken()

        def _load(self):
            """
            NOTE: SHOULD NEVER BE CALLED DIRECTLY

            Loads modules of this submod

            RAISES:
                SubmodError - on module failure
            """
            if not self.is_enabled:
                return

            for mod_name in self.modules:
                full_mod_name = f"{self.directory}/{mod_name}"
                try:
                    renpy.include_module(full_mod_name)

                except BaseException as e:
                    # We can't abort loading at this point,
                    # and ignoring doesn't sit right with me
                    # it can cause more issues down the pipeline
                    msg = f"Critical error while loading module '{mod_name}' for submod '{self.name}': {e!r}"
                    submod_log.critical(msg)
                    # Disable broken submod so the user can boot the game next time
                    self._mark_broken()
                    raise SubmodError(msg) from e

        @classmethod
        def _load_submods(cls):
            """
            NOTE: SHOULD NEVER BE CALLED DIRECTLY

            Loads modules for every submod
            """
            # TODO: sort submods in total order, first load the dependencies
            submods = cls._get_submods()
            submods.sort(key=lambda s: s.name)

            for submod in submods:
                submod._load()

        @classmethod
        def has_any_submods(cls) -> bool:
            """
            Checks if any submods were loaded

            OUT:
                bool
            """
            return bool(cls._submod_map)

        @classmethod
        def _has_submod(cls, name: str) -> bool:
            """
            Checks if a submod exists

            IN:
                name - submod name

            OUT:
                True if exists
                False otherwise
            """
            return name in cls._submod_map

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
        def _iter_submods(cls) -> "Iterator[_Submod]":
            """
            Returns an iterator over the submods

            OUT:
                iterator of Submod objects
            """
            return iter(cls._submod_map.values())

        @classmethod
        def _get_submods(cls) -> "list[_Submod]":
            """
            Returns a list of all the submods

            OUT:
                list of Submod objects
            """
            return list(cls._submod_map.values())


    ### Common submod functions

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
init -999 python in mas_submod_utils:
    import inspect
    import store

    from store import mas_utils

    #Store the current label for use elsewhere
    current_label = None
    #Last label
    last_label = None

    #Dict of all function plugins
    function_plugins = dict()

    #Default priority
    DEF_PRIORITY = 0

    PRIORITY_SORT_KEY = lambda x: x[1][2]

    #START: Decorator Function
    def functionplugin(_label, _args=None, auto_error_handling=True, priority=0):
        """
        Decorator function to register a plugin

        The same as registerFunction. See its doc for parameter details
        """
        # TODO: functools.wraps
        def wrap(_function):
            registerFunction(
                _label,
                _function,
                _args,
                auto_error_handling,
                priority
            )
            return _function
        return wrap

    #START: Internal functions
    def getAndRunFunctions(key=None):
        """
        Gets and runs functions within the key provided

        IN:
            key - Key to retrieve and run functions from
        """
        global function_plugins

        #If the key isn't provided, we assume it from the caller
        if not key:
            key = inspect.stack()[1][3]

        func_dict = function_plugins.get(key)

        if not func_dict:
            return

        #Firstly, let's get our sorted list
        # TODO: use insort instead of sorting every time we run things
        sorted_plugins = __prioritySort(key)
        for _action, data_tuple in sorted_plugins:
            if data_tuple[1]:
                try:
                    store.__run(_action, __getArgs(key, _action))
                except Exception as ex:
                    store.mas_utils.mas_log.error("function {0} failed because {1}".format(_action.__name__, ex))

            else:
                store.__run(_action, __getArgs(key, _action))

    def registerFunction(key, _function, args=None, auto_error_handling=True, priority=DEF_PRIORITY):
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
            _function - function to register
            auto_error_handling - whether or function plugins should ignore errors in functions
                (Set this to False for functions which call or jump)
            priority - Order priority to run functions
                (Like init levels, the lower the number, the earlier it runs)

        OUT:
            boolean:
                - True if the function was registered successfully
                - False otherwise
        """
        global function_plugins

        #Verify that the function is callable
        if not callable(_function):
            store.mas_utils.mas_log.error("{0} is not callable".format(_function.__name__))
            return False

        # TODO: remove args entirely in r8
        if args is None:
            args = ()

        else:
            mas_utils.report_deprecation(
                "parameter 'args' in 'registerFunction'",
                use_instead="functools.partial",
                use_instead_msg_fmt="Wrap your callable in '{use_instead}' to provide it args/kwargs."
            )
            #Too many args
            if len(args) > len(inspect.getargspec(_function).args):
                store.mas_utils.mas_log.error("Too many args provided for function {0}".format(_function.__name__))
                return False

        #Check for overrides
        key = __getOverrideLabel(key)

        #Create the key if we need to
        if key not in function_plugins:
            function_plugins[key] = dict()

        #If we just created a key, then there won't be any existing values so we elif
        elif _function in function_plugins[key]:
            return False

        function_plugins[key][_function] = (args, auto_error_handling, priority)
        return True

    def __getArgs(key, _function):
        """
        TODO: remove this with r8
        Gets args for the given function at the given key

        IN:
            key - key to retrieve the function from
            _function - function to retrieve args from

        OUT:
            list of args if the function is present
            If function is not present, None is returned
        """
        global function_plugins

        try:
            return function_plugins[key][_function][0]

        except KeyError:
            # Unknown key/function
            # We do not handle index error as that shouldn't be possible
            # and means there's a bug in the system
            return None

    @mas_utils.deprecated(
        use_instead="functools.partial",
        use_instead_msg_fmt="Wrap your callable in '{use_instead}' to provide it args/kwargs."
    )
    def getArgs(key, _function):
        """
        Gets args for the given function at the given key

        IN:
            key - key to retrieve the function from
            _function - function to retrieve args from

        OUT:
            list of args if the function is present
            If function is not present, None is returned
        """
        return __getArgs(key, _function)

    @mas_utils.deprecated(
        use_instead="functools.partial",
        use_instead_msg_fmt="Wrap your callable in '{use_instead}' to provide it args/kwargs."
    )
    def setArgs(key, _function, args=None):
        """
        Sets args for the given function at the key

        IN:
            key - key that the function's function dict is stored in
            _function - function to set the args

        OUT:
            boolean:
                - True if args were set successfully
                - False if not
        """
        global function_plugins

        func_dict = function_plugins.get(key)

        #Key doesn't exist
        if not func_dict:
            return False

        #Function not in dict
        if _function not in func_dict:
            return False

        if args is None:
            args = ()

        #Too many args provided
        elif len(args) > len(inspect.getargspec(_function).args):
            store.mas_utils.mas_log.error("Too many args provided for function {0}".format(_function.__name__))
            return False

        #Otherwise we can set
        old_values = func_dict[_function]
        func_dict[_function] = (args, old_values[1], old_values[2])
        return True

    def unregisterFunction(key, _function):
        """
        Unregisters a function from the function_plugins dict

        IN:
            key - key the function we want to unregister is in
            _function - function we want to unregister

        OUT:
            boolean:
                - True if function was unregistered successfully
                - False otherwise
        """
        global function_plugins

        func_dict = function_plugins.get(key)

        #Key doesn't exist
        if not func_dict:
            return False

        #Function not in plugins dict
        elif _function not in func_dict:
            return False

        #Otherwise we can pop
        function_plugins[key].pop(_function)
        return True

    def __prioritySort(_label):
        """
        Sorts function plugins based on the priority order system

        IN:
            _label - label to sort functions by priority for

        OUT:
            sorted list of (_function, data_tuple) tuples

        NOTE: This assumes that the label exists in the function_plugins dict
        """
        global function_plugins

        #First, we need to convert the functions into a list of tuples
        func_list = [
            (_function, data_tuple)
            for _function, data_tuple in function_plugins[_label].items()
        ]

        return sorted(func_list, key=PRIORITY_SORT_KEY)

    def __getOverrideLabel(_label):
        """
        Gets the override label for the given label (will follow the chain if overrides are overridden)

        IN:
            _label - label to get the override label for

        OUT:
            string representing the last label in the override chain or _label if there are no overrides
        """
        while renpy.config.label_overrides.get(_label) is not None:
            _label = renpy.config.label_overrides[_label]
        return _label

#Global run area
init -990 python:
    def __run(_function, args):
        """
        Private function to run a function in the global store
        """
        return _function(*args)

#Label callback to get last label and run function plugins from the label
init 999 python:
    def label_callback(name, abnormal):
        """
        Function to run plugin functions and store the last label
        """
        #First, update the last label to what was current
        store.mas_submod_utils.last_label = store.mas_submod_utils.current_label
        #Now we can update the current
        store.mas_submod_utils.current_label = name
        #Run functions
        store.mas_submod_utils.getAndRunFunctions(name)

        #Let's also check if the current label is an override label, if so, we'll then mark the base label as seen
        base_label = _OVERRIDE_LABEL_TO_BASE_LABEL_MAP.get(name)
        if base_label is not None:
            persistent._seen_ever[base_label] = True

    config.label_callback = label_callback

    @store.mas_submod_utils.functionplugin("ch30_reset", priority=-999)
    def __build_override_label_to_base_label_map():
        """
        Populates a lookup dict for all label overrides which are in effect
        """
        #Let's loop here to update our label overrides map
        for overridden_label, label_override in config.label_overrides.items():
            _OVERRIDE_LABEL_TO_BASE_LABEL_MAP[label_override] = overridden_label
