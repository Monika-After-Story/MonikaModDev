python early in _mas_loader:
    import os
    import glob
    from itertools import chain
    from heapq import merge as heapq_merge
    from collections.abc import Iterator

    import store
    from renpy.game import script as renpy_script


    __LOADABLE_DATA = frozenset((
        "images.rpa",
        "audio.rpa",
        "fonts.rpa",
        "scripts.rpa",
    ))

    __GLOB_PATTERN_0 = "**/*.rp[aey]*"
    __GLOB_PATTERN_1 = "**/*_ren.py"

    __RENPY_EXTS = frozenset((
        "rpa",
        "rpe",
        "rpy",
        "rpyc",
        "py",
    ))

    __SPURIOUS_FILES_EXT = ".invalid"


    class IncludeModuleError(Exception):
        """
        Custom exception used by include_module
        """
        def __init__(self, msg: str):
            self.msg = msg

        def __str__(self):
            return self.msg


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

            if rel_fn in __LOADABLE_DATA:
                continue

            ext = os.path.splitext(fn)[1]

            if ext and ext[1:] in __RENPY_EXTS:
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

    def _disable_unrecognised_scripts():
        """
        Iterates over unrecognised scripts and disables them
        so they won't be loaded next time

        RAISES:
            RuntimeError - in case we failed an OS call
        """
        for fn in _get_unrecognised_scripts():
            try:
                os.rename(fn, "{}{}".format(fn, __SPURIOUS_FILES_EXT))

            except OSError as e:
                raise RuntimeError(
                    f"Unrecognised script at '{fn}'\nPlease remove the script manually"
                ) from e

    def _unload_unrecognised_scripts():
        """
        Iterates over unrecognised scripts and unloads them
        """
        # NOTE: renpy scripts are now in common_script_files
        scripts = renpy_script.script_files

        for i in range(len(scripts)-1, -1, -1):
            name, path = scripts[i]

            if path is not None:
                # Means it's not packed in an archive
                scripts.pop(i)

    def __handle_scripts():
        if not store._mas_root.is_dbug_enabled():
            _unload_unrecognised_scripts()
            _disable_unrecognised_scripts()


python early in _mas_root:
    import os
    from dotenv import load_dotenv
    import store

    __ENV_FILE = f"{renpy.config.basedir}/.env"
    load_dotenv(dotenv_path=__ENV_FILE, verbose=True)

    __ENV_KEY = "I_AM_RESPONSIBLE_FOR_ALL_ISSUES_AND_WILLING_TO_VOID_MY_WARRANTY_AND_SUPPORT"
    __DBUG_ENV_VALUE = "Yes, I will regret this! Enable DBUG!"
    __CNSL_ENV_VALUE = "Yes, I will regret this! Enable CNSL!"

    __BUILD_KEY = "CI_BUILD"

    def __get_env_var(key: str) -> "str | None":
        """
        Gets value of an env variable
        """
        return os.environ.get(key, None)

    def is_dbug_enabled() -> bool:
        """
        Checks if dbug is enabled
        """
        return __get_env_var(__ENV_KEY) == __DBUG_ENV_VALUE

    def __is_cnsl_enabled() -> bool:
        """
        Checks if cnsl is enabled
        """
        return __get_env_var(__ENV_KEY) == __CNSL_ENV_VALUE

    def __mark_dbug():
        store.persistent._mas_pm_used_dbug = True

    def __dbug_enabled_callback():
        """
        Callback on dm enabling
        """
        renpy.config.developer = True
        renpy.config.early_developer = True
        renpy.config.console = True
        __mark_dbug()

    def __dbug_disabled_callback():
        """
        Callback on dm disabling
        """
        renpy.config.developer = False
        renpy.config.early_developer = False
        if __is_cnsl_enabled():
            renpy.config.console = True
            __mark_dbug()

        else:
            renpy.config.console = False

    def handle_dbug() -> bool:
        if is_dbug_enabled():
            __dbug_enabled_callback()
            return True

        __dbug_disabled_callback()
        return False

    def in_ci_build() -> bool:
        """
        :return: True if building in CI
        """
        return bool(__get_env_var(__BUILD_KEY))


python early in _mas_loader:
    __handle_scripts()

init -999 python in _mas_root:
    # This has to be run during init,
    # and perhaps no earlier than -999
    handle_dbug()
