# Module that handles updates between versions
# Assumes:
#   updates.topics
#   updates.version_updates
#   persistent._seen_ever
#   persistent.version_number

# preeverything stuff
init -10 python:
    found_monika_ani = persistent.monika_anniversary is not None
    no_topics_list = persistent.monika_random_topics is None

# uncomment these lines if you need to compare pre-update topics to
# updated topics (have dev = True)
#    import copy
#    old_list = copy.deepcopy(persistent.monika_random_topics)


# pre script-topics (which is runlevel 5)
init 4 python:
    # check version change
    # this also handles if version number is None
    if persistent.version_number != config.version:
        # clearing this to prevent crash
        persistent.monika_topic = None

# create some functions
init python:

    def removeTopicID(topicID):
        #
        # Removes one topic from the _seen_ever variable
        # topics list (if it exists in either var) (persistent is also
        # checked for existence)
        #
        # IN:
        #   @param topicID - the topicID to remove
        #
        # ASSUMES:
        #   persistent._seen_ever

        if renpy.seen_label(topicID):
            persistent._seen_ever.pop(topicID)


    def adjustTopicIDs(changedIDs,updating_persistent=persistent):
        #
        # Changes labels in persistent._seen_ever
        # to new IDs in the changedIDs dict
        #
        # IN:
        #   @param oldList - the list of old Ids to change
        #   @param changedIDs - dict of changed ids:
        #       key -> old ID
        #       value -> new ID
        #
        # ASSUMES:
        #   persistent._seen_ever

        # now for a complicated alg that changes keys in _seen_ever
        # except its not that complicated lol

        for oldTopic in changedIDs:
            if updating_persistent._seen_ever.pop(oldTopic,False):
                updating_persistent._seen_ever[changedIDs[oldTopic]] = True

        return updating_persistent



    def updateTopicIDs(version_number,updating_persistent=persistent):
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
        #   persistent._seen_ever
        #   updates.topics
        if version_number in updates.topics:
            changedIDs = updates.topics[version_number]


            if changedIDs is not None:
                updating_persistent = adjustTopicIDs(
                    changedIDs, updating_persistent
                )

        return updating_persistent


    def updateGameFrom(startVers):
        #
        # Updates the game, starting at the given start version
        #
        # IN:
        #   @param startVers - the version number in the parsed
        #       format ("v#####")
        #
        # ASSUMES:
        #   updates.version_updates

        while startVers in updates.version_updates:

            updateTo = updates.version_updates[startVers]

            # we should only call update labels that we have
            if renpy.has_label(updateTo):
                renpy.call_in_new_context(updateTo, updateTo)
            startVers = updates.version_updates[startVers]




# this needs to run post script-topics
init 10 python:

    # okay do we have a version number?
    if persistent.version_number is None:
        # here comes the logic train
        if no_topics_list:
            # we are in version 0.2.2 (the horror!)
            updateGameFrom("v0_2_2")

        elif (renpy.seen_label("monika_ribbon") or
                "monika_ribbon" in persistent.monika_random_topics):
            # we are in version 0.3.3
            updateGameFrom("v0_3_3")

        elif found_monika_ani:
            # we are in version 0.3.2
            updateGameFrom("v0_3_2")

        elif (renpy.seen_label("monika_monika") or
                "monika_monika" in persistent.monika_random_topics):
            # we are in version 0.3.1
            updateGameFrom("v0_3_1")

        else:
            # we are in version 0.3.0
            updateGameFrom("v0_3_0")

        # set the version now
        persistent.version_number = config.version

        # and clear update data
        clearUpdateStructs()

    elif persistent.version_number != config.version:
        # parse this version number into something we can use
        vvvv_version = "v"+"_".join(persistent.version_number.split("."))
        # so update!
        updateGameFrom(vvvv_version)

        # set the new version
        persistent.version_number = config.version

        # and clear update data
        clearUpdateStructs()


# UPDATE SCRIPTS ==============================================================
# use these to handle conflicting changes or special cases
# make sure the label is of the format v### and matches a version number
# defined in updates_topics.rpy.
#
# also, always make sure the script ends with a call to updateTopicIDs(),
# passing in the version number of that script
#
# NOTE: the labels here mean we are updating TO this version

# all generic (only updateTopicID calls) go here
label vgenericupdate(version="v0_2_2"):
label v0_6_1(version=version): # 0.6.1
label v0_5_1(version=version): # 0.5.1
label v0_3_3(version=version): # 0.3.3
label v0_3_2(version=version): # 0.3.2
label v0_3_1(version=version): # 0.3.1
    python:
        # update !
        persistent = updateTopicIDs(version)

    return

# non generic updates go here

# 0.7.0
label v0_7_0(version="v0_7_0"):
    python:
        # check for christmas existence and delete!
        import os
        try: os.remove(config.basedir + "/game/christmas.rpyc")
        except: pass

        # update !
        persistent = updateTopicIDs(version)

        temp_event_list = persistent.event_list
        # now properly set all seen events as unlocked
        import store.evhand as evhand
        for k in evhand.event_database:
            event = evhand.event_database[k]
            if (renpy.seen_label(event.eventlabel)
                and (event.pool
                    or event.random
                    or event.action == EV_ACT_POOL
                    or event.action == EV_ACT_RANDOM
                )):
                event.unlocked = True
                event.conditional = None

                #Grant some XP so existing players don't start at square 1
                grant_xp(xp.NEW_EVENT)

        #Clear the "Add prompt" events that this adds to the stack
        persistent.event_list = temp_event_list

        #Unlock chess if they've already played it
        if seen_event('game_chess'):
            persistent.game_unlocks['chess']=True

        #Unlock the name change topic if the name change topic has been seen
        if seen_event('preferredname'):
            evhand.event_database["monika_changename"].unlocked = True

    return

# 0.4.0
label v0_4_0(version="v0_4_0"):
    python:
        # persistent topics are dunzo
        persistent.monika_random_topics = None

        # update!
        # uncomment if we actually have changes
        #persistent = updateTopicIDs("v040")
    return

# 0.3.0
label v0_3_0(version="v0_3_0"):
    python:
        # the following labels are special cases because of conflicts
        removeTopicID("monika_piano")
        removeTopicID("monika_college")

        # update!
        persistent = updateTopicIDs(version)
    return
