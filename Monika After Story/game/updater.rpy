# enabling unstable mode
default persistent._mas_unstable_mode = False
define mas_updater.regular = "http://updates.monikaafterstory.com/updates.json"
define mas_updater.unstable = "http://unstable.monikaafterstory.com/updates.json"

#This file goes through the actions for updating Monika After story
label update_now:
    $import time #this instance of time can stay
    python:
        last_updated=0
        for url in persistent._update_last_checked:
            last_updated = persistent._update_last_checked[url]

    #Make sure the update folder is where it should be
    if not updater.can_update():
        python:
            try: renpy.file(config.basedir + "/update/current.json")
            except:
                try: os.rename(config.basedir + "/game/update", config.basedir + "/update")
                except: pass

    default check_wait = 21600
    if time.time()-last_updated > check_wait and updater.can_update():
        if persistent._mas_unstable_mode:
            # use unstabel stuff
            $ update_link = mas_updater.unstable
        else:
            # use regular updates
            $ update_link = mas_updater.regular

        $timeout = False
        $latest_version = updater.UpdateVersion(update_link, check_interval=0)
        call screen update_check(Return(True),Return(False))

        if _return:
            $ persistent.closed_self = True # we take updates as self closed
            $updater.update(update_link, restart=True)
    return
