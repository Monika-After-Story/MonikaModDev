# Module that handles updates between versions
# Assumes:
#   persistent.monika_random_topics


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
                newItem = changedIDs[oldList[index]]
                if newItem is None:
                    oldList.pop(index)
                else:
                    oldList[index] = newItem


    def updateTopicIDs(version_number):
        #
        # Updates topic IDS between versions by performing
        # a two step process: adjust exisitng IDS to match
        # the new IDS, then add newIDs to the persistent
        # randomtopics
        #
        # IN:
        #   @param version_number - the version number we are
        #       updating to
        #
        # ASSUMES:
        #   persistent.monika_random_topics
        
        changedIDs,newIDs = updates.topics[version_number]
        
        if changedIDs is not None:
            adjustTopicIDs(
                persistent.monika_random_topics,
                changedIDs
            )

        if newIDs is not None:
            persistent.monika_random_topics.extend(newIDs)

    def updateGameFrom(startVers):
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

    # okay do we have a verison number?
    if persistent.version_number is None:
        # here comes the logic train
        if persistent.monika_random_topics is None:
            # we are in version 0.2.2 (the horror!)
            # TODO
            print("v022")
            
        elif updates.topics["v033"][1][0] in persistent.monika_random_topics:
            print("v033")
            # we are in version 0.3.3
            # TODO mgiht have something to do here

        elif persistent.monika_anniversary is not None:
            # we are in version 0.3.2
            updateGameFrom("v032")

        elif (set(updates.topics["v031"][1]).isdisjoint(persistent.monika_random_topics) and
                "monika_whispers" not in persistent.monika_random_topics):
            # we are in version 0.3.0
            updateGameFrom("v030")

        else:
            # we are in version 0.3.1
            updateGameFrom("v031")

    elif persistent.version_number != config.version:
        # parse this version number into something we can use
        vvvv_version = "v"+"".join(persistent.version_number.split("."))
        # so update!
        updateGameFrom(vvvv_version)
        # set the new version
        persistent.version_number = config.version


# testing update script
label v100:
    # imaginary super version
    python:
        # update!
        updateTopicIDs("v100")
    
    return        

# actual update scripts
# 0.3.3
label v033:
    python:
        # add additional update code here

        # update!
        updateTopicIDs("v033")

    return

# 0.3.2
label v032:
    python:

        # update!
        updateTopicIDs("v032")

    return

# 0.3.1
label v031:
    python:
        # update!
        updateTopicIDs("v031")

    return

# 0.3.0
label v030:
    python:
        print("nothing")
        # TODO



