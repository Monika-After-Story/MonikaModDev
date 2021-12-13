# NOTE: we do not store keys in persistent. 
#   this is for safety reasons since persistents may be shared online for
#   troubleshooting purposes.

init -979 python:


    def mas_getAPIKey(feature):
        """
        gets the API key for a feature

        IN:
            feature - the string name of the feature to lookup.

        RETURNS: the api key, as a string. Will be null string if no key found
        """
        return store.mas_api_keys.api_keys.get(feature, "")


    def mas_hasAPIKey(feature):
        """
        Checks if a feature has an API key

        IN:
            feature - string name of the feature to check

        RETURNS: true if the feature has an API key, false otherwise
        """
        return bool(mas_getAPIKey(feature))


    def mas_registerAPIKey(feature, display_name, on_change=None):
        """
        Registers a feature that accepts an API key.
        Features are NOT registered if they already exist.

        Can run a function when the api key is changed. This function should
        return a tuple:
            [0] - True if the key is valid, False if not
            [1] - optional error message to show
        The return value is primarily for setting a key. If no return value
        is provided, the key is assumed valid.
        The API key is passed in as the first param. The key will be a null
        string if the key is being cleared.

        IN:
            feature - the string name of the feature to lookup
            display_name - the display name the feature should use on screen
            on_change - function to run when the API key is changed.

        RETURNS: True if the feature was added, False if not.
        """
        if store.mas_api_keys.feature_registered(feature):
            # feature already registered
            return False

        store.mas_api_keys.register_feature(
            feature,
            (display_name, on_change)
        )
        return True


init -980 python in mas_api_keys:
    import json
    import os
    import pygame
    import store
    import store.mas_utils as mas_utils

    registered_api_keys = {}
    # mapping of available features to the feature display name
    #   key: unique feature name
    #   value: tuple containnig:
    #   [0] - feature display name
    #   [1] - code to run on change

    api_keys = {}
    # current actual API keys that are set
    # key: unique feature name
    # value: API key


    FILEPATH_KEYS = os.path.normcase(
        os.path.join(renpy.config.gamedir, "mod_assets/api_keys.json")
    )

    MAX_KEY_SIZE_DISP = 39


    def feature_registered(feature):
        """
        Checks if a feature is registered for API keys

        IN:
            feature - feature to check (string)

        RETURNS: True if the feature is registered for API keys
        """
        return feature in registered_api_keys


    def register_feature(feature, data):
        """
        Registers a feature for API key usage

        IN:
            feature - name of the feature
            data - data to associate with the feature
        """
        registered_api_keys[feature] = data


    def features_for_display():
        """
        Returns list of the features for display

        RETURNS: list of the features as tuples, sorted for display:
            [0] - the display name of the feature
            [1] - the on_change function to run
        """
        feats = []
        for feature in registered_api_keys:
            key = store.mas_getAPIKey(feature)

            # reduce length to avoid going past screen edge
            if len(key) > MAX_KEY_SIZE_DISP:
                key = key[:MAX_KEY_SIZE_DISP - 3] + "..."

            feats.append((
                registered_api_keys[feature][0],
                feature,
                key,
            ))

        return sorted(feats)


    def _run_on_change(feature, api_key):
        """
        Runs on change for a feature with api key

        IN:
            feature - feature to run on change for
            api_key - api key to run on change with

        RETURNS: tuple of the following format:
            [0] - True if valid key, False if not
            [1] - error message to show
        """
        on_change = registered_api_keys[feature][1]
        if on_change is not None:
            try:
                rv = on_change(api_key)

                if not isinstance(rv, tuple) or len(rv) < 2:
                    return True, ""

                return rv

            except Exception as e:
                mas_utils.mas_log.error(
                    "crash when running on_change for feature {0} - {1}".format(
                        feature,
                        repr(e)
                    )
                )

                return False, "on-change crash - see logs"

        return True, ""


    def screen_clear(feature):
        """
        Called when the clear button is used on the api key screen

        IN:
            feature - the feature whose key is being cleared
        """
        if not feature_registered(feature) or not store.mas_hasAPIKey(feature):
            return

        # clear key
        api_keys.pop(feature)
        save_keys()

        # on change
        _run_on_change(feature, "")


    def screen_paste(feature):
        """
        Called when the paste button is used on the api key screen.

        IN:
            feature - the feature whose key is being pasted
        """
        if not feature_registered(feature):
            return

        # grab key 
        new_key = pygame.scrap.get(pygame.SCRAP_TEXT).strip()
        if not new_key:
            # null key is not counted
            return

        # on change
        key_valid, err_msg = _run_on_change(feature, new_key)

        if key_valid:
            # set key
            api_keys[feature] = new_key
            save_keys()

        else:
            # show message box
            store.renpy.show_screen(
                "dialog",
                message=err_msg,
                ok_action=store.Hide("dialog")
            )


    def load_keys():
        """
        Loads API keys from config file
        """
        try:
            with open(FILEPATH_KEYS, "r") as keys:
                loaded_keys = json.load(keys)
                api_keys.clear()
                api_keys.update(loaded_keys)

        except Exception as e:
            mas_utils.mas_log.warning(
                "problem loading api key json {0}".format(repr(e))
            )

    def save_keys():
        """
        Saves API keys to disk
        """
        try:
            with open(FILEPATH_KEYS, "w") as keys:
                json.dump(api_keys, keys)

        except Exception as e:
            mas_utils.mas_log.warning(
                "problem saving api key json {0}".format(repr(e))
            )


    # load keys on start
    load_keys()


init 999 python in mas_api_keys:
    import store

    # remove persistent api keys that were not registered
    # TODO - re-evaluate if good idea - this is kind of annoying tbh
#    for feature in store.persistent._mas_api_keys.keys():
#        if not feature_registered(feature):
#            store.persistent._mas_api_keys.pop(feature)


