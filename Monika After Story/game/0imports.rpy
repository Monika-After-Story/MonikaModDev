# mas can import paradigm.

init -1500 python in mas_can_import:
    # set importables

    certifi = MASImport_certifi()
    ssl = MASImport_ssl()

    # run checks

    check_imports()


init -1505 python in mas_can_import:
    import os
    import platform
    import datetime
    import threading

    import store
    from store.mas_threading import MASAsyncWrapper

    # initialize known imports.

    class MASImport_certifi(MASImport):
        """
        certifi import

        This also can do cert updating:
            1. call `start_cert_update` to begin the cert update.
                - this will return the promise, but you can also use
                    the following cert update functions to check the status
                    if you don't want to keep the promise.
            2. call `check_cert_update` to determine if the update is still
                running or is completed.
                - once the update is completed, all appropriate vars will be
                    set automatically.
            3. call `get_cert_update` to get the returned value from the 
                cert update promise.
            4. call `reset_cert_update` to cleanup the cert updater thread.
                this must be called before doing another cert update.

        Auto (startup) cert updating happens once every 6 months. 
        """

        def __init__(self):
            """
            Constructor
            """
            super(MASImport_certifi, self).__init__("certifi")

            self.__cert_available = False
            self.__cert_update_promise = MASAsyncWrapper(self._update_cert)

            self.__cert_available_lock = threading.Lock()
            self.__cert_available_cond = threading.Condition(
                self.__cert_available_lock
            )

        @property
        def cert_available(self):
            """
            True if cert is available.
            """
            return self.__th_get_cert_avail()

        def import_try(self):
            """
            Also checks if a cert is available.
            """
            import certifi
            certifi.set_parent_dir(renpy.config.gamedir)
            self.__th_set_cert_avail(certifi.has_cert())

            # start the cert update - this will be checked later.
            self.start_cert_update()

            return True

        def import_except(self, err):
            # kill the update thread and mark unavailble cert
            # updater thread probably failed so we just wont bother with it.
            self.__th_set_cert_avail(False)

        def load(self):
            try:
                super(MASImport_certifi, self).load()
            except AttributeError as e:
                self.__th_set_cert_avail(False)

        def start_cert_update(self, force=False):
            """
            Starts the cert update process. 

            NOTE: will NOT start the process if the updater is currently
                running. The promise is still returned though.

            IN:
                force - True to force the cert to update now.

            RETURNS: the cert update promise
            """
            if not self.__cert_update_promise.ready:
                return self.__cert_update_promise

            # update force arg
            self.__cert_update_promise._th_kwargs = {"force": force}

            # begin update
            self.__cert_update_promise.start()
            return self.__cert_update_promise

        def check_cert_update(self):
            """
            checks the status of the cert update.

            RETURNS: True if the cert update is done, False if not
            """
            return self.__cert_update_promise.done()

        def get_cert_update(self):
            """
            Gets the result from the cert update.

            RETURNS: certifi RV value of the check_update function, or None if
                the check_update function could not run. THIS WILL ALSO RETURN
                NONE IF THE CERT UPDATE IS NOT FINISHED.
                Use `check_cert_update` to check that the update is done
                before calling this.
            """
            return self.__cert_update_promise.get()

        def reset_cert_update(self):
            """
            Resets the cert update thread. This may fail if the cert update is
            not done yet.
            """
            self.__cert_update_promise.end()

        def is_cert_update_running(self):
            """
            Determines if the cert update is running.

            RETURNS: True if the cert update is running.
            """
            return not self.check_cert_update()

        def ch30_day_cert_update(self):
            """
            Call this during ch30_day to handle cert update checks
            """
            if not self.__cert_update_promise.ready:

                if self.is_cert_update_running():
                    # cert thread not done - assume thread is running and will
                    # finish later
                    return 

                # reset cert update so we can start the thread
                self.reset_cert_update()

            self.start_cert_update()

        def _update_cert(self, force=False):
            """
            Updates the cert and sets appropriate vars.

            Certs will only be updated if the last cert update was at least
            6 months ago.

            IN:
                force - True to force the cert to update right now

            RETURNS: certifi RV value of the check_update function, or None if
                the check_update function could not run.
            """
            last_update = store.persistent._mas_last_cert_update
            if last_update is None:
                last_update = datetime.datetime.utcnow()

            rv = None

            if self.enabled:
                if (
                        force
                        or (
                            datetime.datetime.utcnow() - last_update
                        ) > datetime.timedelta(days=180)
                ):
                    import certifi

                    rv, response = certifi.check_update()
                    if rv in (certifi.RV_SUCCESS, certifi.RV_NO_UPDATE):
                        self.__th_set_cert_avail(certifi.has_cert())

                    store.persistent._mas_last_cert_update = last_update

            return rv

        def __th_get_cert_avail(self):
            """
            thread-safe get cert available - for internal use only

            RETURNS: cert_available value
            """
            self.__cert_available_cond.acquire()
            cert_avail = self.__cert_available
            self.__cert_available_cond.release()

            return cert_avail

        def __th_set_cert_avail(self, value):
            """
            Thread-safe set cert available - for internal use only

            IN:
                value - value to set to cert_available
            """
            self.__cert_available_cond.acquire()
            self.__cert_available = value
            self.__cert_available_cond.release()


    class MASImport_ssl(MASImport):
        """
        SSL Import
        """

        def __init__(self):
            """
            Constructor
            """
            super(MASImport_ssl, self).__init__("ssl", set_sys=True)

        def import_try(self):
            """
            Also adjusts httplib.

            this is a hack.
            """
            import sys

            ssl_pkg = "python-packages/ssl"
            bit64 = "x86_64"
            bit32 = "i686"
            new_ssl = None

            if platform.system() == "Windows":
                sys.path.append(os.path.normcase(os.path.join(
                    renpy.config.gamedir,
                    ssl_pkg,
                    "windows/32/",
                )))

                import win32_ssl
                new_ssl = win32_ssl

            elif platform.system() == "Linux":

                if platform.machine() == bit64:
                    sys.path.append(os.path.normcase(os.path.join(
                        renpy.config.gamedir,
                        ssl_pkg,
                        "linux/64/",
                    )))

                    import linux64_ssl
                    new_ssl = linux64_ssl

                elif platform.machine() == bit32:
                    sys.path.append(os.path.normcase(os.path.join(
                        renpy.config.gamedir,
                        ssl_pkg,
                        "linux/32/",
                    )))

                    import linux32_ssl
                    new_ssl = linux32_ssl

            elif platform.system() == "Darwin" and platform.machine() == bit64:
                sys.path.append(os.path.normcase(os.path.join(
                    renpy.config.gamedir,
                    ssl_pkg,
                    "mac/64/",
                )))

                import mac64_ssl
                new_ssl = mac64_ssl

            if new_ssl is None:
                return False

            # overwrties httplib's ssl ref so later HTTPS will work.
            self._set_sys_module(new_ssl)
            import httplib
            httplib.ssl = new_ssl
            return True


init -1510 python in mas_can_import:
    import store.mas_logging as mas_logging
    import store.mas_utils as mas_utils

    # new data pattern
    import store.mas_can_import_data as Data


    class MASImport(object):
        """
        Wrapper around import checks for MAS-based imports.
        All conditional imports should extend this class and implement all 
        required functions.
        Use this before actually running a third-party import. 
        All functionality that relies on third-party imports should be capable
        of being turned off.
        """
        _IMPORT_ERR = "Failed to import `{0}`: {1}"

        def __init__(self, module_name, set_sys=False):
            """
            Constructor

            IN:
                module_name - the name of the module to import
                set_sys - pass True to allow this to overwrite the sys modules.
                    This should only be used in cases where you need to 
                    override a system (aka built-in) module.
                    (Default: False)
            """
            self.__module_name = module_name
            self.__set_sys = set_sys
            self.__enabled = False

            # add to imports dict
            # crashes if already exists
            if module_name in Data.imports:
                raise Exception(
                    "duplicate import object - {0}".format(module_name)
                )

            Data.imports[self.__module_name] = self

        def __call__(self):
            """
            Just returns if this is enabled or not
            """
            return self.enabled

        @property
        def enabled(self):
            """
            True if this import is enabled (can be imported)
            """
            return self.__enabled

        @property
        def module_name(self):
            """
            module name for this import
            """
            return self.__module_name

        @property
        def set_sys(self):
            """
            True if sys module can be overwritten by this.
            """
            return self.__set_sys

        def log_import_error(self, exp=None):
            """
            Logs import error message.

            IN:
                exp - current exception if available.
                    (Default: None)
            """
            mas_log = mas_utils.init_mas_log()
            mas_log.error(self._IMPORT_ERR.format(
                self.module_name,
                "" if exp is None else repr(exp)
            ))

        def import_try(self):
            """
            DERIVED CLASSES MUST IMPLEMENT THIS

            This should check if the import should be enabled.
            For more info, see `load`.

            RETURNS: True if the import should be enabled, False otherwise.
            """
            raise NotImplementedError

        def import_except(self, err):
            """
            Runs if an ImportError is encountered. The import will always
            be disabled and an import error is logged after this runs.

            If you need to run additional behavior or set other vars on a 
            failed import, override this function.

            For more info, see `load`.

            IN:
                err - the exception that was raised
            """
            pass

        def load(self):
            """
            Loads the import and checks that it works. This is called 
            sometime before init level -1000.

            This will call `import_try` and mark the this import as enabled if
            appropriate.

            If an ImportError/AttributeError/NameError is triggered,
            disable this import, log an import error, and call `import_except.

            If any other errors occur, the import will be disabled and
            an import error will be logged, but the error will percolate up.
            If you wish to catch those errors, override this function and wrap
            a try-except block around the base call.
            """
            try:
                self.__enabled = self.import_try()

            except (ImportError, AttributeError, NameError) as e:
                self.__enabled = False
                self.log_import_error(e)
                self.import_except(e)

            except Exception as e:
                self.__enabled = False
                self.log_import_error(e)
                raise e

        def _set_sys_module(self, module):
            """
            Sets the system module so this import can be used elsewhere.
            Not called by the load system - you must call this manually
            if desired.

            This is also guardrailed on construction so no injection.

            IN:
                module - the imported module
            """
            if self.set_sys:
                import sys
                sys.modules[self.module_name] = module


    def check_imports():
        """
        checks import availability
        """
        for module_name in Data.imports:
            Data.imports[module_name].load()


init -1511 python in mas_can_import_data:
    # data store

    imports = {}
    # key: module name
    # value: MASImport object
