python early in _mas_loader:
    import os
    import glob
    from collections.abc import Iterator

    import store


    __EXCEPTIONS = frozenset((
        "images.rpa",
        "audio.rpa",
        "fonts.rpa",
        "scripts.rpa"
    ))

    __GLOB_PATTERN = "**/*.rp[aey]*"

    __RS_EXTS = frozenset((
        "rpa",
        "rpe",
        "rpy",
        "rpyc"
    ))

    __DISB_EXT = ".disabled"


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
        pattern = os.path.join(gamedir, __GLOB_PATTERN)
        file_names = glob.iglob(pattern, recursive=True)

        for fn in file_names:
            rel_fn = fn.partition(gamedir)[-1]
            if rel_fn.startswith("\\") or rel_fn.startswith("/"):
                rel_fn = rel_fn[1:]

            if rel_fn in __EXCEPTIONS:
                continue

            ext = os.path.splitext(fn)[1]

            if ext and ext[1:] in __RS_EXTS:
                yield fn

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
        scripts = renpy.game.script.script_files

        for i in range(len(scripts)-1, -1, -1):
            name, path = scripts[i]

            if (
                path is None# Means packed
                or path.endswith("/renpy/common")# renpy specific
            ):
                continue

            scripts.pop(i)

    def handle_scripts():
        if not store._mas_root.is_dm_enabled():
            _unload_unrecognised_scripts()
            _disable_unrecognised_scripts()


python early in _mas_root:
    import os

    import store


    __ENV_KEY = "I_AM_RESPONSIBLE_FOR_ALL_ISSUES_AND_WILLING_TO_VOID_MY_WARRANTY_AND_SUPPORT_OR_SACRIFICE_CHILDREN"
    __DM_ENV_VALUE = "Yes, I will regret this! Enable DM!"
    __CNSL_ENV_VALUE = "Yes, I will regret this! Enable CNSL!"


    def __get_env_var(key: str) -> str|None:
        """
        Gets value  of an env variable
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

    def __set_dev_pm_var():
        store.persistent._mas_pm_used_dm = True

    def __dm_enabled_cb():
        """
        Callback on dm enabling
        """
        renpy.config.developer = True
        renpy.config.console = True
        __set_dev_pm_var()

    def __dm_disabled_cb():
        """
        Callback on dm disabling
        """
        renpy.config.developer = False
        if _is_cnsl_enabled():
            renpy.config.console = True
            __set_dev_pm_var()

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
