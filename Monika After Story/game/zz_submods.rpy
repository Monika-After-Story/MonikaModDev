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
                raise SubmodError("A submod with name '{0}' already exists.\n".format(name))

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

            old_vers = map(int, old_vers.split('.'))
            curr_vers = self.getVersionNumberList()

            return Submod._checkVersions(curr_vers, old_vers, is_current=False)

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
                            submod.name.replace(' ', '_'),
                            persistent._mas_submod_version_data[submod.name].replace('.', '_')
                        ).lower()
                    )

                #Even if this hasn't updated, we should adjust its value to reflect the correct version
                persistent._mas_submod_version_data[submod.name] = submod.version

        @staticmethod
        def _checkDependencies():
            """
            Checks to see if the dependencies for this submod are met
            """
            for submod in submod_map.itervalues():
                for dependency, minmax_version_tuple in submod.dependencies.iteritems():
                    dependency_submod = Submod._getSubmod(dependency)

                    if dependency_submod is not None:
                        #Now we need to split our minmax
                        minimum_version, maximum_version = minmax_version_tuple

                        #First, check the minimum version
                        if (
                            minimum_version
                            and not Submod._checkVersions(dependency_submod.version, minimum_version)
                        ):
                            raise SubmodError(
                                "Submod '{0}' is out of date. Version {1} required.".format(
                                    dependency_submod.name, minimum_version
                                )
                            )

                        #If we have a maximum version, we should check if we're surpassing it
                        elif (
                            maximum_version
                            and Submod._checkVersions(dependency_submod.version, maximum_version, is_current=False)
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

        @staticmethod
        def _checkVersions(curr_vers, comparitive_vers, is_current=True):
            """
            Generic version checker for submods

            IN:
                curr_vers - current installed version of the submod as a list
                comparitive_vers - the version we're comparing to (or need the current version to be at or greater than) as a list
                is_current - True if it's okay for the comparitive version to be the same as the current. False otherwise.
                    (Default: True)

            OUT:
                boolean:
                    - True if the version number is greater than the comparitive version (or equal if is_current is True)
                    - False otherwise
            """
            #First, we check if the lists are the same. If so, we're the same version
            if comparitive_vers == curr_vers:
                if is_current:
                    return True
                return False

            #Otherwise, we need to do a bit of work
            #Firstly, we need to make the lengths of the two lists equal
            def fixVersionListLen(smaller_vers_list, larger_vers_list):
                """
                Adjusts the smaller version list to be the same length as the larger version list for easy comparison

                OUT:
                    adjusted version list

                NOTE: fills missing indeces with 0's
                """
                for missing_ind in range(len(larger_vers_list) - len(smaller_vers_list)):
                    smaller_vers_list.append(0)
                return smaller_vers_list

            if len(comparitive_vers) > len(curr_vers):
                curr_vers = fixVersionListLen(curr_vers, comparitive_vers)

            elif len(curr_vers) > len(comparitive_vers):
                comparitive_vers = fixVersionListLen(comparitive_vers, curr_vers)

            #Now we iterate and check the version numbers sequentially from left to right
            for index in range(len(curr_vers)):
                if curr_vers[index] > comparitive_vers[index]:
                    return True

            #If we never found something greater, then we didn't update, and we actually rolled back
            return False

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
            return Submod._checkVersions(submod.version, version)
        return bool(submod)
