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
        $timeout = False
        $latest_version = updater.UpdateVersion('http://updates.monikaafterstory.com/updates.json',check_interval=0)
        call screen update_check(Return(True),Return(False))

        if _return:
            $updater.update('http://updates.monikaafterstory.com/updates.json',restart=True)
    return
