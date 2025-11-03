## This file is for overriding specific declarations from DDLC
## Use this if you want to change a few variables, but don't want
## to replace entire script files that are otherwise fine.

## Normal overrides
## These overrides happen after any of the normal init blocks in scripts.
## Use these to change variables on screens, effects, and the like.
init 10 python:
    pass

## Early overrides
## These overrides happen before the normal init blocks in scripts.
## Use this in the rare event that you need to overwrite some variable
## before it's called in another init block.
## You likely won't use this.
init -10 python:
    pass

## Super early overrides
## You'll need a block like this for creator defined screen language
## Don't use this unless you know you need it
python early in mas_overrides:
    import threading

    import renpy
    import renpy.savelocation as savelocation


    def verify_data_override(data, signatures, check_verifying=True):
        """
        Verify the data in a save token.

        Originally, this function is used to check against a checksum to verify the persistent should be loaded
        But because we want to allow anyone be able to migrate and transfer their data, we will just return True
        """
        return True

    renpy.savetoken.verify_data = verify_data_override


    def savelocation_init_override():
        """
        Run **SOME** of the stuff savelocation.init runs

        basically we trying to keep saves in the AppData/equivalent folder
        to make backups/restoring easier.

        The only difference here is that this skips over game savedirs and
        'extra' save dirs (so just omissions)
        """
        savelocation.quit()
        savelocation.quit_scan_thread = False

        location = savelocation.MultiLocation()

        # 1. User savedir.
        location.add(savelocation.FileLocation(renpy.config.savedir))

        # 2. Game-local savedir.
        # if (not renpy.mobile) and (not renpy.macapp):
        #     path = os.path.join(renpy.config.gamedir, "saves")
        #     location_add(path)

        # 3. Extra savedirs.
        # for i in renpy.config.extra_savedirs:
        #     location_add(i)

        location.scan()

        renpy.loadsave.location = location

        if not renpy.emscripten:
            savelocation.scan_thread = threading.Thread(target=savelocation.run_scan_thread)
            savelocation.scan_thread.start()

    savelocation.init = savelocation_init_override

init -999 python:
    # With our override we should always have only one save location
    # If there's more, we better just crash than let some data mismatch
    if len(renpy.loadsave.location.locations) > 1:
        raise RuntimeError("multiple savelocations detected, exiting")
