init -999:
    default persistent._mas_submod_version_data = dict()

init 10 python:
    #Run updates if need be
    store.mas_submod_utils.Submod._checkUpdates()

init -989 python:
    #Run dependency checks
    store.mas_submod_utils.Submod._checkDependencies()

init -990 python in mas_ui:
    import store
    has_submod_settings = len([
        submod
        for submod in store.mas_submod_utils.submod_map.values()
        if submod.settings_pane is not None
    ]) > 0

init -991 python in mas_submod_utils:
    import store
    import sys
    import traceback

    persistent = store.persistent

    submod_map = dict()

    class SubmodError(Exception):
        def __init__(self, _msg):
            self.msg = _msg
        def __str__(self):
            return self.msg

    class Submod:
        """
        Submod class

        PROPERTIES:
            author - submod author
            name - submod name
            description - submod description
            version - version of the submod installed
            dependencies - dependencies required for the submod
            settings_pane - string referring to the screen used for the submod's settings
            version_updates - update labels
        """
        #The fallback version string, used in case we don't have valid data
        FB_VERS_STR = "0.0.0"

        def __init__(
            self,
            author,
            name,
            description,
            version,
            dependencies={},
            settings_pane=None,
            version_updates={}
        ):
            """
            Submod object constructor

            IN:
                author - string, author name.

                name - submod name

                description - a short description for the submod

                version - version number in format SPECIFICALLY like so: `1.2.3`
                    (You can add more or less as need be, but splits MUST be made using periods)

                dependencies - dictionary in the following structure: {"name": ("minimum_version", "maximum_version")}
                corresponding to the needed submod name and version required
                NOTE: versions must be passed in the same way as the version property is done
                    (Default: empty dict)

                settings_pane - a string representing the screen for this submod's settings

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
            """
            #First make sure this name us unique
            if name in submod_map:
                store.mas_utils.writelog("[SUBMOD ERROR]: A submod with name '{0}' already exists. Ignoring.\n".format(name))
                return

            #Now we verify that the version number is something proper
            try:
                map(int, version.split('.'))
            except:
                raise SubmodError("Version number '{0}' is invalid.".format(version))

            #With verification done, let's make the object
            self.author = author
            self.name = name
            self.description = description if description is not None else ""
            self.version = version
            self.dependencies = dependencies
            self.settings_pane = settings_pane
            self.version_updates = version_updates

            #Now we add these to our maps
            submod_map[name] = self

            #NOTE: We check for things having updated later so all update scripts get called together
            if name not in persistent._mas_submod_version_data:
                persistent._mas_submod_version_data[name] = version

        def getVersionNumberList(self):
            """
            Gets the version number as a list of integers

            OUT:
                List of integers representing the version number
            """
            return map(int, self.version.split('.'))

        def hasUpdated(self):
            """
            Checks if this submod instance was updated (version number has incremented)

            OUT:
                boolean:
                    - True if the version number has incremented from the persistent one
                    - False otherwise
            """
            old_vers = persistent._mas_submod_version_data.get(self.name)

            #If we don't have an old vers, we're installing for the first time and aren't updating at all
            if not old_vers:
                return False

            try:
                old_vers = map(int, old_vers.split('.'))

            #Persist data was bad, we'll replace it with something safe and return False as we need not check more
            except:
                persistent._mas_submod_version_data[self.name] = Submod.FB_VERS_STR
                return False

            return self.checkVersions(old_vers) == 1

        def updateFrom(self, version):
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

        def checkVersions(self, comparative_vers):
            """
            Generic version checker for submods

            IN:
                curr_vers - current installed version of the submod as a list
                comparative_vers - the version we're comparing to (or need the current version to be at or greater than) as a list

            OUT:
                integer:
                    - (-1) if the current version number is less than the comparitive version
                    - 0 if the current version is the same as the comparitive version
                    - 1 if the current version is greater than the comparitive version
            """
            return store.mas_utils.compareVersionLists(
                self.getVersionNumberList(),
                comparative_vers
            )

        @staticmethod
        def _checkUpdates():
            """
            Checks if submods have updated and sets the appropriate update scripts for them to run
            """
            #Iter thru all submods we've got stored
            for submod in submod_map.itervalues():
                #If it has updated, we need to call their update scripts and adjust the version data value
                if submod.hasUpdated():
                    submod.updateFrom(
                        "{0}_{1}_v{2}".format(
                            submod.author,
                            submod.name,
                            persistent._mas_submod_version_data.get(submod.name, Submod.FB_VERS_STR).replace('.', '_')
                        ).lower().replace(' ', '_')
                    )

                #Even if this hasn't updated, we should adjust its value to reflect the correct version
                persistent._mas_submod_version_data[submod.name] = submod.version

        @staticmethod
        def _checkDependencies():
            """
            Checks to see if the dependencies for this submod are met
            """
            def parseVersions(version):
                """
                Parses a string version number to list format.

                IN:
                    version - version string to parse

                OUT:
                    list() - representing the parsed version number

                NOTE: Does not handle errors as to get here, formats must be correct regardless
                """
                return map(int, version.split('.'))

            for submod in submod_map.itervalues():
                for dependency, minmax_version_tuple in submod.dependencies.iteritems():
                    dependency_submod = Submod._getSubmod(dependency)

                    if dependency_submod is not None:
                        #Now we need to split our minmax
                        minimum_version, maximum_version = minmax_version_tuple

                        #First, check the minimum version. If we get -1, we're out of date
                        if (
                            minimum_version
                            and dependency_submod.checkVersions(parseVersions(minimum_version)) < 0
                        ):
                            raise SubmodError(
                                "Submod '{0}' is out of date. Version {1} required for {2}. Installed version is {3}".format(
                                    dependency_submod.name, minimum_version, submod.name, dependency_submod.version
                                )
                            )

                        #If we have a maximum version, we should check if we're above it.
                        #If we get 1, this is incompatible and we should crash to avoid other ones
                        elif (
                            maximum_version
                            and dependency_submod.checkVersions(parseVersions(maximum_version)) > 0
                        ):
                            raise SubmodError(
                                "Version '{0}' of '{1}' is installed and is incompatible with {2}.\nVersion {3} is compatible.".format(
                                    dependency_submod.version, dependency_submod.name, submod.name, maximum_version
                                )
                            )

                    #Submod wasn't installed at all
                    else:
                        raise SubmodError(
                            "Submod '{0}' is not installed and is required for {1}.".format(
                                dependency, submod.name
                            )
                        )

        @staticmethod
        def _getSubmod(name):
            """
            Gets the submod with the name provided

            IN:
                name - name of the submod to get

            OUT:
                Submod object representing the submod by name if installed and registered
                None if not found
            """
            return submod_map.get(name)

    #END: Submod class
    def isSubmodInstalled(name, version=None):
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
            return submod.checkVersions(version) >= 0
        return bool(submod)
