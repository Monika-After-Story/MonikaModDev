
from typing import Dict

import renpy as Renpy

_imports: Dict[str, 'MASImport'] = {}
# key: module name
# value: MASImport object


def check_imports(renpy: Renpy):
    """
    checks import availability

    :param renpy: renpy object for import usage
    """
    for module_name in _imports:
        _imports[module_name].load(renpy)


class MASImport():
    """
    Wrapper around import checks for MAS-based imports.
    All conditional imports should extend this class and implement all
    required functions.
    Use this before actually running a third-party import.
    All functionality that relies on third-party imports should be capable
    of being turned off.
    """
    _IMPORT_ERR = "Failed to import `{0}`: {1}"

    def __init__(self, module_name: str, set_sys: bool = False):
        """
        Constructor

        :param module_name: module being imported
        :param set_sys: pass True to allow this to overwrite the sys modules.
            This should only be used in cases wher eyou need to override a system module.
            (Default: False)
        """

        self.__module_name = module_name
        self.__set_sys = set_sys
        self.__enabled = False
        self.mas_log = None

        # add to imports dict
        # crashes if already exists
        if module_name in _imports:
            raise Exception(
                "duplicate import object - {0}".format(module_name)
            )

        _imports[self.__module_name] = self

    def _set_log(self, log):
        """
        set the mas log (temp use only)
        :param log: log to set mas log to
        """
        self.mas_log = log

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
        self.mas_log.error(self._IMPORT_ERR.format(
            self.module_name,
            "" if exp is None else repr(exp)
        ))

    def import_try(self, renpy: Renpy = None):
        """
        DERIVED CLASSES MUST IMPLEMENT THIS

        This should check if the import should be enabled.
        For more info, see `load`.

        :param renpy: renpy object for usage by derived classes
        :returns: True if the import should be enabled, False otherwise.
        """
        raise NotImplementedError

    def import_except(self, err, renpy: Renpy = None):
        """
        Runs if an ImportError is encountered. The import will always
        be disabled and an import error is logged after this runs.

        If you need to run additional behavior or set other vars on a
        failed import, override this function.

        For more info, see `load`.

        :param err: the exception that was raised
        :param renpy: renpy object for usage by derived classes
        """
        pass

    def load(self, renpy: Renpy = None):
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

        :param renpy: renpy object for usage by dervied classes
        """
        try:
            self.__enabled = self.import_try(renpy=renpy)

        except (ImportError, AttributeError, NameError) as e:
            self.__enabled = False
            self.log_import_error(e)
            self.import_except(e, renpy=renpy)

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