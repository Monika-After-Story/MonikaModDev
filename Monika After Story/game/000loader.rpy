python early in _mas_loader:
    import os
    import glob
    import sys
    from itertools import chain
    from heapq import merge as heapq_merge
    from importlib.util import (
        spec_from_file_location,
        module_from_spec
    )
    from collections.abc import Iterator
    from types import ModuleType

    import store
    from renpy.game import script as renpy_script


    __EXCEPTIONS = frozenset((
        "images.rpa",
        "audio.rpa",
        "fonts.rpa",
        "scripts.rpa"
    ))

    __GLOB_PATTERN_0 = "**/*.rp[aey]*"
    __GLOB_PATTERN_1 = "**/*_ren.py"

    __RS_EXTS = frozenset((
        "rpa",
        "rpe",
        "rpy",
        "rpyc",
        "py"
    ))

    __DISB_EXT = ".disabled"


    class IncludeModuleError(Exception):
        """
        Custom exception used by include_module
        """
        def __init__(self, msg: str):
            self.msg = msg

        def __str__(self):
            return self.msg


    def _sanitise_path(path: str) -> str:
        """
        Fixes filepaths on Windows OS

        IN:
            path - the path to fix

        """
        return path.replace("\\", "/")

    def _get_unrecognised_scripts() -> Iterator[str]:
        """
        Returns an iterator over found unrecognised scripts
        """
        gamedir = renpy.config.gamedir
        file_names = chain(
            glob.iglob(os.path.join(gamedir, __GLOB_PATTERN_0), recursive=True),
            glob.iglob(os.path.join(gamedir, __GLOB_PATTERN_1), recursive=True)
        )

        for fn in file_names:
            rel_fn = fn.partition(gamedir)[-1]
            if rel_fn.startswith("\\") or rel_fn.startswith("/"):
                rel_fn = rel_fn[1:]

            if rel_fn in __EXCEPTIONS:
                continue

            ext = os.path.splitext(fn)[1]

            if ext and ext[1:] in __RS_EXTS:
                yield fn

    def do_modules_exist(*modules: str, is_any: bool = False) -> bool:
        """
        Checks if all or any of the modules were defined
        NOTE: This doesn't validate if the modules are
            loadable or valid at all

        IN:
            *modules - str, the modules to find
            is_any - bool, check if any given module exists
                instead of all
                (Default: False)

        OUT:
            bool
        """
        modules = set(modules)

        for n, p in renpy_script.module_files:
            if n in modules:
                modules.remove(n)
                if is_any or not modules:
                    return True

        return False

    def include_module(name: str):
        """
        Fine, I'll do it myself (c)
        Includes a module to load down the init pipeline

        IN:
            name - str, name of the moduleto include

        RAISES:
            IncludeModuleError - in case we failed to include the module for any reason
        """
        if not renpy.is_init_phase():
            raise IncludeModuleError("Can't include module when init phase is over")

        try:
            if not (module_initcode := renpy_script.load_module(name)):
                # Loaded, but the module is empty, can quit here
                return

        except Exception as e:
            raise IncludeModuleError(f"Failed to include module: {e}") from e

        # We may not insert elements at or prior the current id!
        current_id = renpy.game.initcode_ast_id

        if module_initcode[0][0] < renpy_script.initcode[current_id][0]:
            raise IncludeModuleError(
                f"Module '{name}' contains nodes with priority lower than the node that loads it"
            )

        merge_id = current_id + 1
        current_tail = renpy_script.initcode[merge_id:]
        # Since script initcode and module initcode are both sorted,
        # we can use heap to merge them
        new_tail = heapq_merge(current_tail, module_initcode, key=lambda i: i[0])

        renpy_script.initcode[merge_id:] = list(new_tail)

    def _disable_unrecognised_scripts():
        """
        Iterates over unrecognised scripts and disables them
        so they won't be loaded next time

        RAISES:
            RuntimeError - in case we failed an OS call
        """
        for fn in _get_unrecognised_scripts():
            try:
                os.rename(fn, "{}{}".format(fn, __DISB_EXT))

            except OSError as e:
                raise RuntimeError(
                    f"Unrecognised script at '{fn}'\nPlease remove the script manually"
                ) from e

    def _unload_unrecognised_scripts():
        """
        Iterates over unrecognised scripts and unloads them
        """
        scripts = renpy_script.script_files

        for i in range(len(scripts)-1, -1, -1):
            name, path = scripts[i]

            if (
                path is None# Means packed
                or path.endswith("/renpy/common")# renpy specific
            ):
                continue

            scripts.pop(i)

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

    def handle_scripts():
        if not store._mas_root.is_dm_enabled():
            _unload_unrecognised_scripts()
            _disable_unrecognised_scripts()


python early in _mas_root:
    import os
    from dotenv import load_dotenv
    import store

    __ENV_FILE = f"{renpy.config.basedir}/.env"
    load_dotenv(dotenv_path=__ENV_FILE, verbose=True)

    __ENV_KEY = "I_AM_RESPONSIBLE_FOR_ALL_ISSUES_AND_WILLING_TO_VOID_MY_WARRANTY_AND_SUPPORT"
    __DM_ENV_VALUE = "Yes, I will regret this! Enable DM!"
    __CNSL_ENV_VALUE = "Yes, I will regret this! Enable CNSL!"


    def __get_env_var(key: str) -> str|None:
        """
        Gets value of an env variable
        """
        return os.environ.get(key, None)

    def is_dm_enabled() -> bool:
        """
        Checks if dm is enabled
        """
        return __get_env_var(__ENV_KEY) == __DM_ENV_VALUE

    def _is_cnsl_enabled() -> bool:
        """
        Checks if cnsl is enabled
        """
        return __get_env_var(__ENV_KEY) == __CNSL_ENV_VALUE

    def __mark_dm():
        store.persistent._mas_pm_used_dm = True

    def __dm_enabled_cb():
        """
        Callback on dm enabling
        """
        renpy.config.developer = True
        renpy.config.early_developer = True
        renpy.config.console = True
        __mark_dm()

    def __dm_disabled_cb():
        """
        Callback on dm disabling
        """
        renpy.config.developer = False
        renpy.config.early_developer = False
        if _is_cnsl_enabled():
            renpy.config.console = True
            __mark_dm()

        else:
            renpy.config.console = False

    def handle_dm() -> bool:
        if is_dm_enabled():
            __dm_enabled_cb()
            return True

        __dm_disabled_cb()
        return False


python early:
    _mas_loader.handle_scripts()

init -999 python:
    # This has to be run during init,
    # and perhaps no earlier than -999
    _mas_root.handle_dm()
