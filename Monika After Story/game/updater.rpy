#This file goes through the actions for updating Monika After story
label update_now:
    $import time
    python:
        last_updated=0
        for url in persistent._update_last_checked:
            last_updated = persistent._update_last_checked[url]
    if time.time()-last_updated > 21600 and updater.can_update():
        $timeout = False
        $latest_version = updater.UpdateVersion('http://s3.us-east-2.amazonaws.com/monikaafterstory/updates.json')
        call screen update_check(Return(True),Return(False))

        if _return:
            $updater.update('http://s3.us-east-2.amazonaws.com/monikaafterstory/updates.json')
    return
