# Module that handles updates between versions
# Assumes:
#   persistent.monika_random_topics
#   persistent.monika_said_topics

# start by initalization version update dict
define updates.version_updates = {}

# this needs to run post script-topics
init 10 python:

    def adjustTopicIDs(oldList, changedIDs):
        #
        # Changes topic IDs in the persistent lists
        # to new IDs in the changedIDs dict
        #
        # IN:
        #   @param oldList - the list of old Ids to change
        #   @param changedIDs - dict of changed ids:
        #       key -> old ID
        #       value -> new ID
        
        for index in range(0,len(oldList)):
            if oldList[index] in changedIDs:
                oldList[index] = changedIDs[oldList[index]]


    def updateTopicIDs(changedIDs,newIDs):
        #
        # Updates topic IDS between versions by performing
        # a two step process: adjust exisitng IDS to match
        # the new IDS, then add newIDs to the persistent
        # randomtopics
        #
        # IN:
        #   @param changedIDs - dict of changed ids:
        #       key -> old ID
        #       value -> new ID
        #   @param newIDs - list of new ids
        #
        # ASSUMES:
        #   persistent.monika_random_topics
        
        
        if persistent.monika_random_topics:
            adjustTopicIDs(
                persistent.monika_random_topics,
                changedIDs
            )
            persistent.monika_random_topics.extend(newIDs)

    def updateGame(startVers):
        #
        # Updates the game, starting at the given start version
        #
        # IN:
        #   @param startVers - the version number in the parsed
        #       format ("v#####")
        
        while startVers in updates.version_updates:
            renpy.call_in_new_context(
                updates.version_updates[startVers]
            )
            startVers = updates.version_updates[startVers]

            
    # update this dict accordingly to every new version
    # k:old version number -> v:new version number
    updates.version_updates["v033"] = "v100"

    # okay do we have a verison number?
    if persistent.version_number is None:
        # in this case, we need to do some srs logic. save for later
        print("nthing")
    elif persistent.version_number != config.version:
        # parse this version number into something we can use
        vvvv_version = "v"+"".join(persistent.version_number.split("."))
        # so update!
        updateGame(vvvv_version)
        # set the new version
        persistent.version_number = config.version


# testing update script
label v100:
    # imaginary super version
    python:
        # whats our dict of changed ids?
        changedIDs = dict()
        changedIDs["monika_spiders"] = "notspiderslol"
        changedIDs["monika_playersface"] = "not playersface"

        # and new ids?
        newIDs = list()
        newIDs.append("this is new")
        newIDs.append("so is this")
        newIDs.append("this is also new")

        # update!
        updateTopicIDs(changedIDs,newIDs)
    
    return        

