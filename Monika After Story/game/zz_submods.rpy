init -1000:
    default persistent._mas_submod_version_data = dict()
    default persistent._mas_submod_settings = dict()

init 10 python in mas_submod_utils:
    #Run updates if need be
    _Submod._checkUpdates()

init -999 python in mas_submod_utils:
    # Init submods
    _load_submods()

init -1000 python in mas_submod_utils:
    import glob
    import re
    import os
    import json
    import sys
    from urllib.parse import urlparse
    from typing import (
        Literal,
        Optional
    )
    from collections.abc import Iterator

    import pydantic
    from pydantic import conlist as constrained_list, constr as constrained_str

    import store
    from store import (
        config,
        persistent,
        mas_utils,
        mas_logging,
        _mas_loader
    )


    submod_log = mas_logging.init_log("submod_log")

    # NOTE: ALWAYS UPDATE VERSION IF YOU CHANGE HEADER FORMAT
    HEADER_VERSION = 1

    HEADER_GLOB = "**/header.json"
    SUBMODS_DIR = "Submods"

    # String must start with an alpha/underscore character, and can contain only alphanumerics and underscores
    LABEL_SAFE_NAME = re.compile(r'^[a-zA-Z_][ 0-9a-zA-Z_]*$')


    class _SubmodSchema(pydantic.BaseModel):
        """
        Schema for validating submod json
        """
        # NOTE: JSON specific:
        header_version: int
        # NOTE: Submod specific:
        author: constrained_str(regex=LABEL_SAFE_NAME)
        name: constrained_str(regex=LABEL_SAFE_NAME)
        version: str
        directory: str # NOTE: this isn't part of the json, will be added dynamically during loading
        modules: tuple[str, ...]
        description: str = ""
        dependencies: dict[str, tuple[str, str]] = {}# pydantic handles mut args
        settings_pane: str = ""
        version_updates: dict[str, str] = {}# pydantic handles mut args
        coauthors: constrained_list(constrained_str(regex=LABEL_SAFE_NAME)) = []
        repository: str = ""
        priority: pydantic.conint(ge=-999, le=999) = 0

        @pydantic.validator("header_version")
        def validate_header_version(cls, value):
            if value <= 0:
                raise ValueError(
                    f"Submod header version {value} is invalid"
                )
            if value < HEADER_VERSION:
                raise ValueError(
                    f"Submod header version {value} is outdated (expected {HEADER_VERSION})"
                )
            if value > HEADER_VERSION:
                raise ValueError(
                    f"Submod header version {value} is unknown (expected {HEADER_VERSION})"
                )

            return value

        @pydantic.validator("version")
        def validate_version(cls, value):
            if not _is_valid_version(value):
                raise ValueError(f"Submod version number '{value}' is invalid")

            return value

        @pydantic.validator("modules")
        def validate_modules(cls, value, values):
            if not value:
                raise ValueError("Submod must define modules.")

            # IMPORTANT: Sort in alpha
            value = tuple(sorted(value))

            submod_dir = values.get("directory", None)
            if (
                submod_dir is not None
                and not _mas_loader.do_modules_exist(*(f"{submod_dir}/{m}" for m in value))
            ):
                raise ValueError(
                    "One or more submod modules are missing: {}".format(
                        ", ".join(map(lambda s: f"'{s}'", value))
                    )
                )

            return value

        @pydantic.validator("dependencies")
        def validate_dependencies(cls, value):
            for k, v in value.items():
                if len(v) != 2:
                    raise ValueError(f"Dependency '{k}' has invalid version tuple {v} (expected 2 items)")

                for i in v:
                    if not _is_valid_version(i):
                        raise ValueError(f"Dependency '{k}' has invalid version '{i}'")

            return value

        @pydantic.validator("version_updates")
        def validate_version_updates(cls, value, values):
            if value:
                try:
                    update_label = _generate_update_label(values["author"], values["name"], values["version"])

                except KeyError:
                    # This means that one of the other fields has failed, so we can't parse this one either
                    pass

                else:
                    author_name, _, version = update_label.rpartition("v")

                    for item in value.items():
                        for i in item:
                            i_author_name, _, i_version = i.rpartition("v")
                            if i_author_name != author_name or not _is_valid_version(i_version):
                                raise ValueError(f"Update label '{i}' is of invalid format")

            return value

        @pydantic.validator("repository")
        def validate_repository(cls, value, values):
            if value:
                if (name := values.get("name", None)):
                    url = urlparse(value)
                    if url.scheme != "https":
                        submod_log.warning(f"Submod '{name}' doesn't use https scheme in its repository link")

                    # After what github has done, not going to promote it
                    # if url.netloc != "github.com":
                    #     submod_log.warning(f"Submod '{name}' uses unknown repository hosting. Consider switching to GitHub.com")
                    # elif (
                    #     url.path.count("/") != 2
                    #     or url.params
                    #     or url.query
                    #     or url.fragmnent
                    # ):
                    #     # Only for github
                    #     submod_log.warning(f"Submod '{name}' seems to have invalid link to the repository.")

            return value

    def _parse_version(version: str) -> tuple[int, ...]:
        """
        Parses a string version number to list format.

        IN:
            version - version string to parse

        OUT:
            tuple - representing the parsed version number

        NOTE: Does not handle errors as to get here, formats must be correct regardless
        """
        return tuple(map(int, version.split('.')))

    def _is_valid_version(version: str) -> bool:
        """
        Checks if the given version string has valid format

        IN:
            version - version string to test

        OUT:
            boolean
        """
        try:
            _parse_version(version)
        except ValueError:
            return False

        return True

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

    def _read_submod_header(header_path: str) -> dict|None:
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

    def _process_submod_header(raw_header: dict, header_path: str) -> dict|None:
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
            model = _SubmodSchema(**raw_header)

        except pydantic.ValidationError as e:
            errors = e.errors()
            base_msg = (
                f"Failed to load submod from {_fmt_path(header_path)}:\n"
                f"    {len(errors)} error(s) occured:\n"
            )
            err_msg = "\n".join(
                (
                    "        field '{}': {}".format(
                        report["loc"][0],
                        report["msg"]
                    )
                    for report in errors
                )
            )
            submod_log.error(base_msg + err_msg)
            return None

        header = model.dict()
        # Pop from the dict sinse it's not used in the constructor
        header.pop("header_version")

        return header

    def _init_submod(header_path: str):
        """
        Reads a submod json header at the given path,
        validates and and tries to init the submod

        IN:
            header_path - str, abs path to the submod header
        """
        if not (raw_header := _read_submod_header(header_path)):
            return

        if not (header := _process_submod_header(raw_header, header_path)):
            return

        try:
            submod_obj = _Submod(**header)

        except SubmodError as e:
            submod_log.error(
                f"Failed to load submod at: {_fmt_path(header_path)}:\n    {e}"
            )

        except Exception as e:
            submod_log.critical(
                f"Critical error while validating submod at: {_fmt_path(header_path)}",
                exc_info=True
            )

    def _init_submods():
        """
        Scans and inits submods
        """
        search_path = os.path.join(config.gamedir, SUBMODS_DIR, HEADER_GLOB)
        for fn in glob.iglob(search_path, recursive=True):
            _init_submod(fn)

    def _log_inited_submods():
        if _Submod.hasSubmods():
            submod_log.info(
                "INITED SUBMODS:\n{}".format(
                    ",\n".join(
                        f"    '{submod.name}' v{submod.version}"
                        for submod in _Submod._iterSubmods()
                    )
                )
            )

    def _include_module(name: str):
        """
        Loads the module at the given path

        IN:
            name - str, name of the module

        RAISES:
            IncludeModuleError
        """
        _mas_loader.include_module(name)

    def _load_submods():
        """
        Loads submods
        """
        # Init submods
        _init_submods()
        # Verify installed dependencies
        _Submod._checkDependencies()
        # Log
        _log_inited_submods()
        # Finally load submods
        _Submod._loadSubmods()


    class SubmodError(Exception):
        def __init__(self, msg: str):
            self.msg = msg

        def __str__(self):
            return self.msg

    class _SubmodSettings():
        """
        Static class for managing submod settings
        """
        SETTING_IS_SUBMOD_ENABLED = "is_enabled"

        @classmethod
        def _create_setting(cls, submod: _Submod, key: str, default) -> bool:
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
        def _get_setting(cls, submod: _Submod, key: str, default):
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
        def _set_setting(cls, submod: _Submod, key: str, value) -> None:
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
        def is_submod_enabled(cls, submod: _Submod) -> bool:
            return cls._get_setting(submod, cls.SETTING_IS_SUBMOD_ENABLED, True)

        @classmethod
        def enable_submod(cls, submod: _Submod):
            cls._set_setting(submod, cls.SETTING_IS_SUBMOD_ENABLED, True)

        @classmethod
        def disable_submod(cls, submod: _Submod):
            cls._set_setting(submod, cls.SETTING_IS_SUBMOD_ENABLED, True)

        @classmethod
        def toggle_submod(cls, submod: _Submod) -> bool:
            if cls.is_submod_enabled(submod):
                cls.disable_submod(submod)
                return False

            cls.enable_submod(submod)
            return True


    class _Submod(object):
        """
        Submod class

        PROPERTIES:
            author - submod author
            name - submod name
            version - version of the submod installed
            directory - relative submod directory
            modules - submod modules
            description - submod description
            dependencies - dependencies required for the submod
            settings_pane - string referring to the screen used for the submod's settings
            version_updates - update labels
            coauthors - submod co-authors
            repository - submod repository
            priority - loading priority
        """
        #The fallback version string, used in case we don't have valid data
        FB_VERS_STR = "0.0.0"

        _submod_map = dict()

        def __init__(
            self,
            *,
            author: str,
            name: str,
            version: str,
            directory: str,
            modules: tuple[str, ...],
            description: str,
            dependencies: dict[str, tuple[str, str]],
            settings_pane: str,
            version_updates: dict[str, str],
            coauthors: tuple[str, ...],
            repository: str,
            priority: int,
        ):
            """
            Submod object constructor

            IN:
                author - str, author name.

                name - str, submod name

                version - str, version number in format SPECIFICALLY like so: `1.2.3`
                    (You can add more or less numbers as need be, but splits MUST be made using periods)

                directory - str, the relative path to the submod directory

                modules - list of modules of this submod

                description - a short description for the submod

                dependencies - dictionary in the following structure: {"name": ("minimum_version", "maximum_version")}
                    corresponding to the needed submod name and version required
                    NOTE: versions must be passed in the same way as the version property is done

                settings_pane - str, representing the screen for this submod's settings

                version_updates - dict of the format {"old_version_update_label_name": "new_version_update_label_name"}
                    NOTE: submods MUST use the format <author>_<name>_v<version> for update labels relating to their submods
                    NOTE: capital letters will be forced to lower and spaces will be replaced with underscores
                    NOTE: Update labels MUST accept a version parameter, defaulted to the version of the label
                    For example:
                        author name: MonikaAfterStory,
                        submod name: Example Submod
                        submod vers: 1.2.3

                    becomes:
                        label monikaafterstory_example_submod_v1_2_3(version="v1_2_3")

                coauthors - tuple of co-authors of this submod

                repository - link to the submod repository

                priority - submod loading priority. Must be within -999 and 999

            RAISES:
                SubmodError
            """
            #First make sure this name us unique
            if name in self._submod_map:
                raise SubmodError(
                    f"Submod '{name}' has been installed twice. Please, uninstall the duplicate."
                )

            #With verification done, let's make the object
            self._author = author
            self._name = name
            self._version = version
            self._directory = directory
            self._modules = modules
            self._description = description
            self._dependencies = dependencies
            self._settings_pane = settings_pane
            self._version_updates = version_updates
            self._coauthors = coauthors
            self._repository = repository
            self._priority = priority

            #Now we add these to our maps
            self._submod_map[name] = self

        @property
        def author(self):
            return self._author

        @property
        def name(self):
            return self._name

        @property
        def version(self):
            return self._version

        @property
        def directory(self):
            return self._directory

        @property
        def modules(self):
            return self._modules

        @property
        def description(self):
            return self._description

        @property
        def dependencies(self):
            return self._dependencies

        @property
        def settings_pane(self):
            return self._settings_pane

        @property
        def version_updates(self):
            return self._version_updates

        @property
        def coauthors(self):
            return self._coauthors

        @property
        def repository(self):
            return self._repository

        @property
        def priority(self):
            return self._priority

        def __repr__(self) -> str:
            """
            Representation of this object
            """
            return f"<Submod: ('{self.name}' v{self.version} by {self.author})>"

        def getVersionNumberList(self) -> list[int]:
            """
            Gets the version number as a list of integers

            OUT:
                List of integers representing the version number
            """
            return list(_parse_version(self.version))

        def _hasUpdated(self) -> bool:
            """
            Checks if this submod instance was updated (version number has incremented)

            OUT:
                boolean:
                    - True if the version number has incremented from the persistent one
                    - False otherwise
            """
            old_vers = persistent._mas_submod_version_data.get(self.name, None)

            #If we don't have an old vers, we're installing for the first time and aren't updating at all
            if old_vers is None:
                return False

            try:
                old_vers = list(_parse_version(old_vers))

            #Persist data was bad, we'll replace it with something safe and return False as we need not check more
            except Exception:
                submod_log.error(
                    (
                        "Unexpected exception occured while parsing version data "
                        f"for submod '{self.name}'\n    Data: '{old_vers}'"
                    ),
                    exc_info=True
                )
                persistent._mas_submod_version_data[self.name] = self.FB_VERS_STR
                return False

            return self._checkVersions(old_vers) > 0

        def _updateFrom(self, version: str):
            """
            Updates the submod, starting at the given start version

            IN:
                version - the version number in the parsed format ('author_name_v#_#_#')
            """
            while version in self.version_updates:
                updateTo = self.version_updates[version]

                # we should only call update labels that we have
                if renpy.has_label(updateTo) and not renpy.seen_label(updateTo):
                    renpy.call_in_new_context(updateTo, updateTo)
                version = self.version_updates[version]

        def _checkVersions(self, comparative_vers: list[int]) -> Literal[-1, 0, 1]:
            """
            Generic version checker for submods

            IN:
                comparative_vers - the version we're comparing to (or need the current version to be at or greater than) as a list

            OUT:
                integer:
                    - (-1) if the current version number is less than the comparitive version
                    - 0 if the current version is the same as the comparitive version
                    - 1 if the current version is greater than the comparitive version
            """
            return mas_utils.compareVersionLists(
                self.getVersionNumberList(),
                comparative_vers
            )

        @classmethod
        def _checkUpdates(cls):
            """
            Checks if submods have updated and sets the appropriate update scripts for them to run
            """
            #Iter thru all submods we've got stored
            for submod in cls._iterSubmods():
                #If it has updated, we need to call their update scripts and adjust the version data value
                if submod._hasUpdated():
                    submod._updateFrom(
                        "{0}_{1}_v{2}".format(
                            submod.author,
                            submod.name,
                            persistent._mas_submod_version_data.get(submod.name, cls.FB_VERS_STR).replace('.', '_')
                        ).lower().replace(' ', '_')
                    )

                #Even if this hasn't updated, we should adjust its value to reflect the correct version
                persistent._mas_submod_version_data[submod.name] = submod.version

        @classmethod
        def _checkDependencies(cls):
            """
            Checks to see if all the submods dependencies are met
            """
            for submod in cls._getSubmods():
                try:
                    submod.__checkDependencies()

                # Technically there should only be SubmodError
                # but let's make it extra safe and instead catch broad Exception
                except Exception as e:
                    if isinstance(e, SubmodError):
                        submod_log.error(
                            f"Dependency check failed for submod '{submod.name}':\n    {e}"
                        )
                    else:
                        submod_log.critical(
                            f"Critical error while validating dependencies for submod '{submod.name}':\n    {e}"
                        )
                    # If we're here, we failed for any reason
                    # Let's remove this submod as it cannot be loaded
                    cls._submod_map.pop(submod.name, None)

                else:
                    # No error means we passed
                    #NOTE: We check for things having updated later so all update scripts get called together
                    if submod.name not in persistent._mas_submod_version_data:
                        persistent._mas_submod_version_data[submod.name] = submod.version
                    continue

        def __checkDependencies(self):
            """
            Checks to see if the dependencies for this submod are met

            RAISES:
                SubmodError - on dependency check fail
            """
            for dependency_name, minmax_version_tuple in self.dependencies.items():
                dependency_submod = self._getSubmod(dependency_name)

                if dependency_submod is not None:
                    #Now we need to split our minmax
                    minimum_version, maximum_version = minmax_version_tuple

                    #First, check the minimum version. If we get -1, we're out of date
                    if (
                        minimum_version
                        and dependency_submod._checkVersions(_parse_version(minimum_version)) < 0
                    ):
                        raise SubmodError(
                            "Dependency '{}' is out of date. Version '{}' is required. Installed version is '{}'".format(
                                dependency_submod.name, minimum_version, dependency_submod.version
                            )
                        )

                    #If we have a maximum version, we should check if we're above it.
                    #If we get 1, this is incompatible and we should crash to avoid other ones
                    elif (
                        maximum_version
                        and dependency_submod._checkVersions(_parse_version(maximum_version)) > 0
                    ):
                        raise SubmodError(
                            "Dependency '{}' is incompatible. Version '{}' is compatible. Installed version is '{}'".format(
                                dependency_submod.name, maximum_version, dependency_submod.version
                            )
                        )

                #Submod wasn't installed at all
                else:
                    raise SubmodError(
                        f"Dependency '{dependency_name}' is not installed and is required"
                    )

        @classmethod
        def _loadSubmods(cls):
            """
            SHOULD NEVER BE CALLED DIRECTLY

            Loads modules for every submod
            """
            submods = cls._getSubmods()
            submods.sort(key=lambda s: s.priority)

            for submod in submods:
                submod.__load()

        def __load(self):
            """
            SHOULD NEVER BE CALLED DIRECTLY

            Loads modules of this submod and adds local py-packs
                to the global scope to be importable

            RAISES:
                SubmodError - on module failure
            """
            pypacks = os.path.join(
                config.gamedir, self.directory, "python-packages"
            )
            # TODO: Not sure if we should dynamically expand path like this?
            if os.path.exists(pypacks):
                # renpy.loader.add_python_directory(pypacks)
                sys.path.append(pypacks)

            for mod_name in self.modules:
                full_mod_name = f"{self.directory}/{mod_name}"
                try:
                    _include_module(full_mod_name)

                except Exception as e:
                    # We can't abort loading at this point,
                    # and ignoring doesn't sit right with me
                    # it can cause more issues down the pipeline
                    msg = f"Critical error while loading module '{mod_name}' for submod '{self.name}': {e}"
                    submod_log.critical(msg)
                    raise SubmodError(msg) from e

        @classmethod
        def hasSubmods(cls) -> bool:
            """
            Checks if any submods were loaded

            OUT:
                bool
            """
            return bool(cls._submod_map)

        @classmethod
        def _getSubmod(cls, name: str) -> _Submod|None:
            """
            Gets the submod with the name provided

            IN:
                name - name of the submod to get

            OUT:
                Submod object representing the submod by name if installed and registered
                None if not found
            """
            return cls._submod_map.get(name, None)

        @classmethod
        def _iterSubmods(cls) -> Iterator[_Submod]:
            """
            Returns an iterator over the submods

            OUT:
                iterator of Submod objects
            """
            return iter(cls._submod_map.values())

        @classmethod
        def _getSubmods(cls) -> list[_Submod]:
            """
            Returns a list of the submods

            OUT:
                list of Submod objects
            """
            return list(cls._submod_map.values())


    #END: Submod class
    def isSubmodInstalled(name: str, version: str|None = None) -> bool:
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
        submod = _Submod._getSubmod(name)

        if submod is None:
            return False

        if version:
            return submod._checkVersions(version) >= 0

        return True

    def getSubmodDirectory(name: str) -> str|None:
        """
        Returns a submod directory relative to the game folder

        IN:
            name - str, name of the submod

        OUT:
            str - relative path to the submod
            None - no submod with the given name was found
        """
        if (submod := _Submod._getSubmod(name)) is None:
            return None

        return submod.directory


#START: Function Plugins
init -999 python in mas_submod_utils:
    import inspect
    import store
    from store._mas_loader import import_from_path as require

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
    def functionplugin(_label, _args=[], auto_error_handling=True, priority=0):
        """
        Decorator function to register a plugin

        The same as registerFunction. See its doc for parameter details
        """
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
        sorted_plugins = __prioritySort(key)
        for _action, data_tuple in sorted_plugins:
            if data_tuple[1]:
                try:
                    store.__run(_action, getArgs(key, _action))
                except Exception as ex:
                    store.mas_utils.mas_log.error("function {0} failed because {1}".format(_action.__name__, ex))

            else:
                store.__run(_action, getArgs(key, _action))

    def registerFunction(key, _function, args=[], auto_error_handling=True, priority=DEF_PRIORITY):
        """
        Registers a function to the function_plugins dict

        NOTE: Does NOT allow overwriting of existing functions in the dict
        NOTE: Function must be callable
        NOTE: Functions run when a label matching the key for the function is:
        called, jumped, or fallen through to.
        Or if plugged into a function, when a function by the name of the key calls getAndRunFunctions

        IN:
            key - key to add the function to.
                NOTE: The key is either a label, or a function name
                NOTE: Function names only work if the function contains a getAndRunFunctions call.
                    Without it, it does nothing.
            _function - function to register
            args - list of args (must be in order) to pass to the function
                (Default: [])
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

        #Too many args
        elif len(args) > len(inspect.getargspec(_function).args):
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
        global function_plugins

        func_dict = function_plugins.get(key)

        if not func_dict:
            return

        return func_dict.get(_function)[0]

    def setArgs(key, _function, args=[]):
        """
        Sets args for the given function at the key

        IN:
            key - key that the function's function dict is stored in
            _function - function to set the args
            args - list of args (must be in order) to pass to the function (Default: [])

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
        elif _function not in func_dict:
            return False

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
