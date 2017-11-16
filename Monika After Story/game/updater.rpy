#This file goes through the actions for updating Monika After story
label update_now:
    $updater.update('http://s3.us-east-2.amazonaws.com/monikaafterstory/updates.json')
    return
