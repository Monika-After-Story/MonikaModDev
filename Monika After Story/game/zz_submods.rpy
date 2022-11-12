init -999:
    default persistent._mas_submod_version_data = dict()

init 10 python in mas_submod_utils:
    #Run updates if need be
    Submod._checkUpdates()

init -999 python in mas_submod_utils:
    # Init submods
    _load_submods()

init -1000 python in mas_submod_utils:
    import glob
    import re
    import os
    import json
    # import sys
    # import traceback
    from urllib.parse import urlparse
    from typing import Literal
    # from collections.abc import Iterator

    import store
    from store import (
        config,
        persistent,
        mas_utils,
        mas_logging
    )


    submod_log = mas_logging.init_log("submod_log")

    # NOTE: ALWAYS UPDATE VERSION IF YOU CHANGE HEADER FORMAT
    HEADER_VERSION = 1
    HEADER_GLOB = "**/header.json"
    SUBMOD_DIR = "Submods"


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
            header data - dict|None
        """
        header_json = None
        try:
            with open(header_path) as header_file:
                header_json = json.load(header_file)

        except Exception as e:
            submod_log.error(
                f"Found submod header, but couldn't read it: {_fmt_path(header_path)}",
                exc_info=True
            )
            return None

        if not header_json:
            submod_log.error(
                f"Found submod header, but it's empty: {_fmt_path(header_path)}"
            )
            return None

        return header_json

    def _process_submod_header(header_json: dict, header_path: str) -> bool:
        """
        This does extra processing on header, like setting default values
        if optional parameters not present

        IN:
            header_json - dict, the parsed submod json
            path - str, abs path to the submod header

        OUT:
            boolean - True if successfully, False otherwise
        """
        # NOTE: pop from the dict sinse it's not used in the submod constructor
        v = header_json.pop("header_version", None)
        if v is None:
            submod_log.error(
                f"Submod is missing required 'header_version' field: {_fmt_path(header_path)}"
            )
            return False

        # NOTE: for now we just don't load outdated headers,
        # but we could try to process old headers in the future
        if v < HEADER_VERSION:
            submod_log.error(
                f"Submod has outdated header version (expected {HEADER_VERSION}, got {v}): {_fmt_path(header_path)}"
            )
            return False

        # header_json.setdefault("description", "")
        # header_json.setdefault("dependencies", None)
        # header_json.setdefault("settings_pane", "")
        # header_json.setdefault("version_updates", None)
        # header_json.setdefault("coauthors", ())
        # header_json.setdefault("repository", "")
        # header_json.setdefault("priority", 0)

        return True

    def _init_submod(header_path: str):
        """
        Reads a submod json header at the given path,
        validates and and tries to init the submod

        IN:
            header_path - str, abs path to the submod header
        """
        if not (header_json := _read_submod_header(header_path)):
            return

        if not _process_submod_header(header_json, header_path):
            return

        try:
            submod_dir = os.path.relpath(
                os.path.dirname(header_path),
                start=config.gamedir
            ).replace("\\", "/")
            submod_obj = Submod(directory=submod_dir, **header_json)

        except (SubmodError, TypeError) as e:# TypeError is for extra/invalid args
            submod_log.error(
                f"Failed to load submod at: {_fmt_path(header_path)}\n    {e}"
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
        search_path = os.path.join(config.gamedir, SUBMOD_DIR, HEADER_GLOB)
        for fn in glob.iglob(search_path, recursive=True):
            _init_submod(fn)

    def _log_inited_submods():
        if Submod.hasSubmods():
            submod_log.info(
                "INSTALLED SUBMODS:\n{}".format(
                    ",\n".join(
                        f"    '{submod.name}' v{submod.version}"
                        for submod in Submod._getSubmods()
                    )
                )
            )

    def _load_module(name: str):
        """
        Loads the module at the given path

        IN:
            name - str, name of the module

        RAISES:
            Can raise any kind of error due to renpy not using proper typing
            use with care
        """
        renpy.load_module(name)

    def _load_submods():
        """
        Loads submods
        """
        # Init submods
        _init_submods()
        # Log
        _log_inited_submods()
        # Verify installed dependencies
        Submod._runDependencyCheck()
        # Finally load submods
        Submod._runLoadingLogic()


    class SubmodError(Exception):
        def __init__(self, msg: str):
            self.msg = msg

        def __str__(self):
            return self.msg

    class Submod(object):
        """
        Submod class

        PROPERTIES:
            author - submod author
            name - submod name
            version - version of the submod installed
            description - submod description
            dependencies - dependencies required for the submod
            settings_pane - string referring to the screen used for the submod's settings
            version_updates - update labels
        """
        #The fallback version string, used in case we don't have valid data
        FB_VERS_STR = "0.0.0"

        #Regular expression representing a valid author and name
        AN_REGEXP = re.compile(r'^[a-zA-Z_\u00a0-\ufffd][ 0-9a-zA-Z_\u00a0-\ufffd]*$')

        _submod_map = dict()

        def __init__(
            self,
            author: str,
            name: str,
            version: str,
            directory: str,
            modules: tuple[str, ...],
            description: str = "",
            dependencies: dict[str, tuple[str, str]]|None = None,
            settings_pane: str = "",
            version_updates: dict[str, str]|None = None,
            coauthors: tuple[str, ...] = (),
            repository: str = "",
            priority: int = 0,
        ):
            """
            Submod object constructor

            IN:
                author - string, author name.

                name - submod name

                version - version number in format SPECIFICALLY like so: `1.2.3`
                    (You can add more or less as need be, but splits MUST be made using periods)

                directory - str, the relative path to the submod directory

                modules - list of modules of this submod

                description - a short description for the submod
                    (Default: "")

                dependencies - dictionary in the following structure: {"name": ("minimum_version", "maximum_version")}
                corresponding to the needed submod name and version required
                NOTE: versions must be passed in the same way as the version property is done
                    (Default: empty dict)

                settings_pane - a string representing the screen for this submod's settings
                    (Default: None)

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
                    (Default: empty tuple)

                repository - link to the submod repository
                    (Default: "")

                priority - submod loading priority. Must be within -999 and 999
                    (Default: 0)
            """
            #First make sure this name us unique
            if name in self._submod_map:
                raise SubmodError(f"A submod with name '{name}' has been installed twice. Please, uninstall the duplicate.")

            #Now we verify that the version number is something proper
            if not self._isValidVersion(version):
                raise SubmodError(f"Invalid version number '{version}' for submod '{name}'")

            #Make sure author and name are proper label names
            if not self.AN_REGEXP.match(name):
                raise SubmodError(f"Submod name '{name}' is invalid")

            if not self.AN_REGEXP.match(author):
                raise SubmodError(f"Invalid author '{author}' for submod '{name}'")

            # A submod without any modules doesn't make sense
            if not modules:
                raise SubmodError(f"Submod '{name}' was defined without any modules.")
            for m in modules:
                if not isinstance(m, str):
                    raise SubmodError(f"Invalid module '{m}' for submod '{name}'")

            if not isinstance(description, str):
                raise SubmodError(f"Invalid description '{description}' for submod '{name}'")

            if dependencies is not None:
                if not isinstance(dependencies, (dict, python_dict)):
                    raise SubmodError(f"Invalid 'dependencies' field for submod '{name}'")

                for k, v in dependencies.items():
                    if not isinstance(k, str):
                        raise SubmodError(f"Invalid key '{k}' in the 'dependencies' field for submod '{name}'")

                    if not isinstance(v, (tuple, list, python_list)):
                        raise SubmodError(f"Invalid value type for key '{k}' in the 'dependencies' field for submod '{name}'")

                    if len(v) != 2:
                        raise SubmodError(f"Invalid value for key '{k}' in the 'dependencies' field for submod '{name}'")

                    for i in v:
                        if not self._isValidVersion(i):
                            raise SubmodError(f"Invalid value for key '{k}' in the 'dependencies' field for submod '{name}'")

            else:
                dependencies = {}

            if not isinstance(settings_pane, str):
                raise SubmodError(f"Invalid settings pane '{settings_pane}' for the submod '{name}'")

            if version_updates is not None:
                for k, v in version_updates.items():
                    if not isinstance(k, str):
                        raise SubmodError(f"Invalid key '{k}' in the 'version_updates' field for the submod '{name}'")

                    if not isinstance(v, str):
                        raise SubmodError(f"Invalid value for key '{k}' in the 'version_updates' field for the submod '{name}'")

            else:
                version_updates = {}

            for ca in coauthors:
                if not Submod.AN_REGEXP.match(ca):
                    raise SubmodError(f"Invalid co-author '{ca}' for the submod '{name}'")

            if repository:
                url = urlparse(repository)
                if url.scheme != "https":
                    submod_log.warning(f"Submod '{name}' doesn't use https scheme in its repository link")
                if url.netloc != "github.com":
                    submod_log.warning(f"Submod '{name}' uses unknown repository hosting. Consider switching to GitHub.com")
                elif (
                    url.path.count("/") != 2
                    or url.params
                    or url.query
                    or url.fragmnent
                ):
                    # Only for github
                    submod_log.warning(f"Submod '{name}' seems to have invalid link to the repository.")

            if not isinstance(priority, int) or not (-999 <= priority <= 999):
                raise SubmodError(f"Invalid priority '{priority}' for the submod '{name}'")

            #With verification done, let's make the object
            self.author = author
            self.name = name
            self.version = version
            self.directory = directory
            self.modules = tuple(sorted(modules))
            self.description = description
            self.dependencies = dependencies
            self.settings_pane = settings_pane
            self.version_updates = version_updates
            self.coauthors = tuple(coauthors)
            self.repository = repository
            self.priority = priority

            #Now we add these to our maps
            self._submod_map[name] = self

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
            return list(self._parseVersions(self.version))

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
            if not old_vers:
                return False

            try:
                old_vers = list(self._parseVersions(old_vers))

            #Persist data was bad, we'll replace it with something safe and return False as we need not check more
            except Exception:
                submod_log.error(
                    (
                        "Unexpected exception occured while parsing version data "
                        f"for submod '{self.name}'\n    Data: '{old_vers}'"
                    ),
                    exc_info=True
                )
                persistent._mas_submod_version_data[self.name] = Submod.FB_VERS_STR
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
            for submod in cls._getSubmods():
                #If it has updated, we need to call their update scripts and adjust the version data value
                if submod._hasUpdated():
                    submod._updateFrom(
                        "{0}_{1}_v{2}".format(
                            submod.author,
                            submod.name,
                            persistent._mas_submod_version_data.get(submod.name, Submod.FB_VERS_STR).replace('.', '_')
                        ).lower().replace(' ', '_')
                    )

                #Even if this hasn't updated, we should adjust its value to reflect the correct version
                persistent._mas_submod_version_data[submod.name] = submod.version

        @staticmethod
        def _parseVersions(version: str) -> tuple[int, ...]:
            """
            Parses a string version number to list format.

            IN:
                version - version string to parse

            OUT:
                tuple - representing the parsed version number

            NOTE: Does not handle errors as to get here, formats must be correct regardless
            """
            return tuple(map(int, version.split('.')))

        @classmethod
        def _isValidVersion(cls, version: str) -> bool:
            """
            Checks if the given version string has valid format

            IN:
                version - version string to test

            OUT:
                boolean
            """
            try:
                cls._parseVersions(version)
            except ValueError:
                return False

            return True

        @classmethod
        def _runDependencyCheck(cls):
            """
            Checks to see if all the submods dependencies are met
            """
            for submod in cls._getSubmods():
                try:
                    submod._checkDependencies()

                except SubmodError as e:
                    submod_log.error(e)

                except Exception as e:
                    submod_log.critical(
                        f"Dependency check failed for submod '{submod.name}'",
                        exc_info=True
                    )

                else:
                    # No error means we passed
                    #NOTE: We check for things having updated later so all update scripts get called together
                    if submod.name not in persistent._mas_submod_version_data:
                        persistent._mas_submod_version_data[submod.name] = submod.version
                    continue

                # If we're here, we failed for any reason
                # Let's remove this submod as it cannot be loaded
                cls._submod_map.pop(submod.name, None)

        def _checkDependencies(self):
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
                        and dependency_submod._checkVersions(self._parseVersions(minimum_version)) < 0
                    ):
                        raise SubmodError(
                            "Submod '{}' is out of date. Version '{}' is required for '{}'. Installed version is '{}'".format(
                                dependency_submod.name, minimum_version, self.name, dependency_submod.version
                            )
                        )

                    #If we have a maximum version, we should check if we're above it.
                    #If we get 1, this is incompatible and we should crash to avoid other ones
                    elif (
                        maximum_version
                        and dependency_submod._checkVersions(self._parseVersions(maximum_version)) > 0
                    ):
                        raise SubmodError(
                            "Submod '{}' is incompatible with '{}'. Version '{}' is compatible. Installed version is '{}'".format(
                                dependency_submod.name, self.name, maximum_version, dependency_submod.version
                            )
                        )

                #Submod wasn't installed at all
                else:
                    raise SubmodError(
                        "Submod '{}' is not installed and is required for '{}'".format(
                            dependency_name, self.name
                        )
                    )

        @classmethod
        def _runLoadingLogic(cls):
            """
            Loads modules for every submod
            """
            for submod in cls._getSubmods():
                submod._loadModules()

        def _loadModules(self):
            """
            Loads modules of this submod, should never be called directly

            RAISES:
                SubmodError - on module failure
            """
            for mod_name in self.modules:
                full_mod_name = f"{self.directory}/{mod_name}"
                try:
                    _load_module(full_mod_name)

                except Exception as e:
                    # We can't abort loading at this point
                    # but ignoring doesn't sit right with me
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
        def _getSubmod(cls, name: str) -> Submod|None:
            """
            Gets the submod with the name provided

            IN:
                name - name of the submod to get

            OUT:
                Submod object representing the submod by name if installed and registered
                None if not found
            """
            return cls._submod_map.get(name)

        @classmethod
        def _getSubmods(cls) -> list[Submod]:
            """
            Returns all the submods

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
        submod = Submod._getSubmod(name)

        if submod and version:
            return submod._checkVersions(version) >= 0
        return bool(submod)

    def getSubmodDirectory(name: str) -> str|None:
        """
        Returns a submod directory relative to the game folder

        IN:
            name - str, name of the submod

        OUT:
            str - relative path to the submod
            None - no submod with the given name was found
        """
        if (submod := Submod._getSubmod(name)) is None:
            return None

        return submod.directory


#START: Function Plugins
init -980 python in mas_submod_utils:
    import inspect
    import store

    #Store the current label for use elsewhere
    current_label = None
    #Last label
    last_label = None

    #Dict of all function plugins
    function_plugins = dict()

    #Default priority
    DEF_PRIORITY = 0

    #Priority for jumps and calls
    JUMP_CALL_PRIORITY = 999

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
