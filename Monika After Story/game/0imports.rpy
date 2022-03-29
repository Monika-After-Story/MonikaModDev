# mas can import paradigm.

init -1500 python in mas_can_import:
    # run checks

    check_imports()

    # set importables

    certifi = imports["certifi"]
    ssl = imports["ssl"]


init -1505 python in mas_can_import:
    import os
    import platform
    import datetime

    import store

    # initialize known imports.

    class MASImport_certifi(MASImport):
        """
        certifi import
        """

        def __init__(self):
            """
            Constructor
            """
            super(MASImport_certifi, self).__init__("certifi")

            self._cert_available = False

        @property
        def cert_available():
            """
            True if cert is available.
            """
            return self._cert_available

        def import_try(self):
            """
            Also checks if a cert is available.
            """
            import certifi
            self._cert_available = certifi.has_cert()
            self.update_cert()
            return True

        def import_except(self):
            self._cert_available = False

        def load(self):
            try:
                super(MASImport_certifi, self).load()
            except AttributeError as e:
                self._cert_available = False

        def update_cert(self, force=False):
            """
            See mas_utils.update_cert
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

                    rv, response = certifi.check_update(renpy.config.gamedir)
                    if rv in (certifi.RV_SUCCESS, certifi.RV_NO_UPDATE):
                        self._cert_available = certifi.has_cert()

                    store.persistent._mas_last_cert_update = last_update

            return rv


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
    import store.mas_logging as mas_loggging

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
            mas_log = mas_logging.init_log("mas_log")
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

        def import_except(self):
            """
            Runs if an ImportError is encountered. The import will always
            be disabled and an import error is logged after this runs.

            If you need to run additional behavior or set other vars on a 
            failed import, override this function.

            For more info, see `load`.
            """
            pass

        def load(self):
            """
            Loads the import and checks that it works. This is called 
            sometime before init level -1000.

            This will call `import_try` and mark the this import as enabled if
            appropriate.

            If an ImportError is triggered, disable this import, log an 
            import error, and call `import_except.

            If any other errors occur, the import will be disabled and
            an import error will be logged, but the error will percolate up.
            If you wish to catch those errors, override this function and wrap
            a try-except block around the base call.
            """
            try:
                self.__enabled = self.import_try():

            except ImportError as e:
                self.__enabled = False
                self.log_import_error(e)
                self.import_except():

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
