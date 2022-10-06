# NOTE: we do not store keys in persistent.
#   this is for safety reasons since persistents may be shared online for
#   troubleshooting purposes.


screen mas_update_cert(screen_data):

    # cert update screen

    modal True
    zorder 200
    style_prefix "hkb"

    add mas_getTimeFile("gui/overlay/confirm.png")

    timer 1.0 repeat True action Function(screen_data.loop)

    frame:
        xfill True
        yfill True


        text screen_data.main_text:
            xalign 0.5
            yalign 0.5

        hbox:
            xalign 0.5
            yalign 0.6

            spacing 50

            if screen_data.show_retry:
                textbutton _("Retry"):
                    action Function(screen_data.action_retry)

            if screen_data.show_ok:
                textbutton _("Ok"):
                    action [Function(screen_data.action_ok), Hide("mas_update_cert")]

            if screen_data.show_cancel:
                textbutton _("Cancel"):
                    action [Function(screen_data.action_cancel), Hide("mas_update_cert")]


init -750 python in mas_api_keys:

    import store.mas_layout as mas_layout
    import store.mas_can_import as mas_can_import


    class MASUpdateCertScreenData(mas_layout.MASScreenData):
        """
        screen data for the mas_update_cert screen
        """

        def __init__(self):
            super(MASUpdateCertScreenData, self).__init__("mas_update_cert")

            self._main_text = ""
            self._show_retry = False
            self._show_ok = False
            self._show_cancel = False
            self._rv_value = None # should be set to RV value from certifi
            self._loop_counter = 0 # debugging
            self._updating = False

        @property
        def main_text(self):
            """
            Primary text to show in screen describing current state
            """
            return self._main_text

        @property
        def show_cancel(self):
            """
            True if the cancel button be shown
            """
            return self._show_cancel

        @property
        def show_ok(self):
            """
            True if the ok button should be shown
            """
            return self._show_ok

        @property
        def show_retry(self):
            """
            True if the retry button should be shown
            """
            return self._show_retry

        def loop(self):
            """
            Main loop should just do update promise checking.
            Assumes Cert update promise was started.
            """
            if not mas_can_import.certifi():
                return

            if not self._updating:
                return

            self._loop_counter += 1

            if mas_can_import.certifi.check_cert_update():
                self._updating = False

                # cert update is done
                self._rv_value = mas_can_import.certifi.get_cert_update()

                import certifi

                if self._rv_value == certifi.RV_SUCCESS:
                    self._set_state_updated()

                elif self._rv_value == certifi.RV_NO_UPDATE:
                    self._set_state_no_update()

                else:
                    self._set_state_error()

            else:
                # cert update in progress
                self._set_state_checking_update()

            renpy.restart_interaction()

        def start(self):
            """
            Call this before showing the update cert screen. This will
            run initializations and stuff.
            """
            self._set_state_checking_update()
            self._updating = True
            if mas_can_import.certifi.is_cert_update_running():
                # if the update is running, assume it might complete here.
                return

            # otherwise, reset and run the updater
            mas_can_import.certifi.reset_cert_update()
            mas_can_import.certifi.start_cert_update(force=True)

        def action_cancel(self):
            """
            Called when the cancel button is clicked.
            """
            # NOTE: threads cannot be killed. All we can do is just leave it
            # running.
            pass

        def action_ok(self):
            """
            Called when the ok button is clicked
            """
            self.action_cancel()

        def action_retry(self):
            """
            Called when the retry button is clicked
            """
            self.start()

        def _hide_all_buttons(self):
            """
            Hides all buttons
            """
            self._show_cancel = False
            self._show_ok = False
            self._show_retry = False

        def _set_buttons_ok(self):
            """
            Sets button flags for ok available
            """
            self._hide_all_buttons()
            self._show_ok = True

        def _set_buttons_retrycancel(self):
            """
            Sets button flags for retrycancel available
            """
            self._hide_all_buttons()
            self._show_cancel = True
            self._show_retry = True

        def _set_state_checking_update(self):
            """
            Sets text and button flags for when an update is in progress.
            This includes checking for an update.
            """
            self._main_text = "Updating cert{0} (This can take a while)".format(
                "." * (self._loop_counter % 4)
            )
            self._hide_all_buttons()
            self._show_cancel = True

        def _set_state_error(self):
            """
            Sets text and button flags for when update failed
            """
            if mas_can_import.certifi():
                import certifi

                if self._rv_value == certifi.RV_ERR_CERT_WRITE:
                    self._main_text = (
                        "ERROR: failed to write cert to disk. Try again later "
                        "or manually update the cert."
                    )
                    self._set_buttons_retrycancel()

                elif self._rv_value == certifi.RV_ERR_BAD_SSL_LIB:
                    self._main_text = (
                        "ERROR: SSL is not available. Cannot update cert"
                    )
                    self._set_buttons_ok()

                else:
                    self._main_text = (
                        "ERROR: failed to update cert. Try again later or "
                        "manually update the cert."
                    )
                    self._set_buttons_retrycancel()

            else:
                self._main_text = (
                    "ERROR: certifi not available. Cannot update cert"
                )
                self._set_buttons_ok()

        def _set_state_no_update(self):
            """
            Sets text and button flags for when no update is found
            """
            self._main_text = "Cert already up to date!"
            self._hide_all_buttons()
            self._show_ok = True
            self._show_retry = False

        def _set_state_updated(self):
            """
            Sets text and button flags for whe cert was updated
            """
            self._main_text = "Cert updated!"
            self._set_buttons_ok()


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

    FILEPATH_KEYS = os.path.normcase(renpy.config.savedir + "/api_keys.json")

    MAX_KEY_SIZE_DISP = 39

    # error messages
    ERR_ON_CHG_CRASH = "crash when running on_change for feature {0} - {1}"
    ERR_ON_CHG_CRASH_MSG = "on-change crash  - see logs"
    ERR_ON_CHG_TYPE = "invalid return value from on_change for feature {0} - {1}"
    ERR_ON_CHG_TYPE_MSG = "invalid value from on-change - see logs"
    ERR_ON_CHG_TYPE_NOT_TUPLE = "expected tuple, got {0}"
    ERR_ON_CHG_TYPE_BAD_TUP_SIZE = "expected tuple of at least size 2, got one of size {0}"
    ERR_ON_CHG_TYPE_BAD_ERR_MSG = "invalid type for value at index 1 in return value: expected str, got {0}"


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


    def has_features():
        """
        Do we have API-key based features?

        RETURNS: True if we have api key based features
        """
        return len(registered_api_keys) > 0


    def clean_key(dirty_key):
        """
        Cleans an aPI key

        IN:
            dirty_key - key to clean

        RETURNS: cleaned key
        """
        return dirty_key.replace("\n", "").replace("\r", "")


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

            # guarded on change execution
            try:
                rv = on_change(api_key)

            except Exception as e:
                mas_utils.mas_log.error(
                    ERR_ON_CHG_CRASH.format(feature, repr(e))
                )

                return False, ERR_ON_CHG_CRASH_MSG

            # type check
            try:
                if not isinstance(rv, tuple):
                    raise TypeError(ERR_ON_CHG_TYPE_NOT_TUPLE.format(type(rv).__name__))

                if len(rv) < 2:
                    raise TypeError(ERR_ON_CHG_TYPE_BAD_TUP_SIZE.format(len(rv)))

                # only check error message if on_change is returning false
                # TODO: py3: unicode doesn't exist. On migration, simply check for str
                if not rv[0] and not isinstance(rv[1], (str, unicode)):
                    raise TypeError(ERR_ON_CHG_TYPE_BAD_ERR_MSG.format(type(rv[1]).__name__))

                return rv

            except TypeError as e:
                mas_utils.mas_log.error(
                    ERR_ON_CHG_TYPE.format(feature, str(e)) # str used since msg says type error
                )
                return False, ERR_ON_CHG_TYPE_MSG

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

        # clear newlines
        new_key = clean_key(new_key)

        # on change
        onchange_rv = _run_on_change(feature, new_key)
        key_valid = onchange_rv[0]
        err_msg = onchange_rv[1]

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


    def screen_update_cert():
        """
        Called when the update cert button is used on the api key screen
        """
        if not store.mas_can_import.certifi():
            # no certifi enabled - the button shouldn't be visislbe
            return

        screen_data = MASUpdateCertScreenData()
        screen_data.start()

        store.renpy.show_screen("mas_update_cert", screen_data)


    def load_keys():
        """
        Loads API keys from config file
        """
        try:
            if not os.access(FILEPATH_KEYS, os.F_OK | os.R_OK | os.W_OK):
                return
        except:
            return

        try:
            with open(FILEPATH_KEYS, "r") as keys:
                loaded_keys = json.load(keys)

                # clear newlines
                for feat in loaded_keys:
                    loaded_keys[feat] = clean_key(loaded_keys[feat])

                api_keys.clear()
                api_keys.update(loaded_keys)

        except Exception as e:
            mas_utils.mas_log.warning(
                "problem loading api key json {0} from {1}".format(
                    repr(e),
                    FILEPATH_KEYS
                )
            )


    def save_keys():
        """
        Saves API keys to disk
        """
        if len(api_keys) < 1:
            return

        try:
            with open(FILEPATH_KEYS, "w") as keys:
                json.dump(api_keys, keys, indent=4)

        except Exception as e:
            mas_utils.mas_log.warning(
                "problem saving api key json {0} in {1}".format(
                    repr(e),
                    FILEPATH_KEYS
                )
            )


    # load keys on start
    load_keys()
