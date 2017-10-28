# Module that handles updates between versions
# Assumes:
#   persistent.monika_random_topics
#   updates.topics
#   updates.version_updates
#   persistent._seen_ever
#   persistent.version_number
#   topics.monika_topics

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
        # mainly force regneration of topics
        persistent.monika_random_built = False
        # clearing this to prevent crash
        persistent.monika_topic = None

# create some functions
init python:

    def removeTopicID(topicID):
        #
        # Removes one topic from both the _seen_ever variable and persistent
        # topics list (if it exists in either var) (persistent is also 
        # checked for existence)
        #
        # IN:
        #   @param topicID - the topicID to remove
        #
        # ASSUMES:
        #   persistent._seen_ever
        #   persistent.monika_random_topics (checks for exisitence)

        if renpy.seen_label(topicID):
            persistent._seen_ever.pop(topicID)

        if (persistent.monika_random_topics is not None and
            topicID in persistent.monika_random_topics):
            persistent.monika_random_topics.remove(topicID)

    def addNewTopicIDs():
        # 
        # Using some (not so) clever algorithm, adds new TopicIDs
        # that havent been seen to the persistent random topics list
        # by comparing persistent.monika_random_topics and
        # a newly generated topics.monika_topics list
        #
        # ASSUMES:
        #   persistent.monika_random_topics
        #   topics.monika_topics has been generated and filled
        #   version number has changed
        #
        # SIDE EFFECTS:
        #   topics.monika_topics is cleared
        #   persistent.monika_random_topics is extended

        new_topics = list()

        for topic in topics.monika_topics:
            # seen label check is first because assume longtime player
            if (not renpy.seen_label(topic) and
                topic not in persistent.monika_random_topics):
                new_topics.append(topic)

        # finally extend the persisents
        persistent.monika_random_topics.extend(new_topics)

        # and clear the topics
        topics.monika_topics[:] = []


    def adjustTopicIDs(oldList, changedIDs):
        #
        # Changes topic IDs in the oldLists
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
        
        for index in range(0,len(oldList)):
            if oldList[index] in changedIDs:
                newItem = changedIDs[oldList[index]]
                if newItem is None:
                    oldList.pop(index)
                else:
                    oldList[index] = newItem

        # now for a complicated alg that changes keys in _seen_ever
        # except its not that complicated lol

        for oldTopic in changedIDs:
            if oldTopic in persistent._seen_ever:
                persistent._seen_ever.pop(oldTopic)
                if changedIDs[oldTopic] is not None:
                    persistent._seen_ever[changedIDs[oldTopic]] = True


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
        #   updates.topics
    
        if version_number in updates.topics:
            changedIDs = updates.topics[version_number]
        
            if changedIDs is not None:
                adjustTopicIDs(
                    persistent.monika_random_topics,
                    changedIDs
                )


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
            renpy.call_in_new_context(
                updates.version_updates[startVers]
            )
            startVers = updates.version_updates[startVers]

        # adding new topics happens here because of logic issues
        addNewTopicIDs()


# this needs to run post script-topics
init 10 python:

    # okay do we have a verison number?
    if persistent.version_number is None:
        # here comes the logic train
        if no_topics_list:
            # we are in version 0.2.2 (the horror!)
            updateGameFrom("v022")
            
        elif (renpy.seen_label("monika_ribbon") or
                "monika_ribbon" in persistent.monika_random_topics):
            print("v033")
            # we are in version 0.3.3

        elif found_monika_ani: 
            # we are in version 0.3.2
            updateGameFrom("v032")

        elif (renpy.seen_label("monika_monika") or
                "monika_monika" in persistent.monika_random_topics):
            # we are in version 0.3.1
            updateGameFrom("v031")

        else:
            # we are in version 0.3.0
            updateGameFrom("v030")

        # set the version now
        persistent.version_number = config.version
    elif persistent.version_number != config.version:
        # parse this version number into something we can use
        vvvv_version = "v"+"".join(persistent.version_number.split("."))
        # so update!
        updateGameFrom(vvvv_version)
        # set the new version
        persistent.version_number = config.version


# UPDATE SCRIPTS ==============================================================
# use these to handle conflicting changes or special cases
# make sure the label is of the format v### and matches a version number
# defined in updates_topics.rpy.
#
# also, always make sure the script ends with a call to updateTopicIDs(),
# passing in the version number of that script
#
# NOTE: the labels here mean we are updating TO this version

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
        # the following labels are special cases because of conflicts
        removeTopicID("monika_piano")
        removeTopicID("monika_college")

        # update!
        updateTopicIDs("v030")
    return
