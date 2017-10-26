# Module that handles updates between versions
# Assumes:
#   persistent.monika_random_topics

#define teststore = None
#define teststore_t = None
define prev033 = False

# pre script-topics (which is runlevel 5)
init 4 python:
    # check version change
    # this also handles if version number is None
    if persistent.version_number != config.version:
        # mainly force regneration of topics
        persistent.monika_random_built = False

# create some functions
init python:

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
        #   updates.topics
        
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



# this needs to run post script-topics
init 10 python:

    # okay do we have a verison number?
    if persistent.version_number is None:
        # here comes the logic train
        if persistent.monika_random_topics is None:
            # we are in version 0.2.2 (the horror!)
            # TODO
            print("v022")
            
        elif renpy.has_label("monika_ribbon"):
            print("v033")
            # we are in version 0.3.3
            # TODO mgiht have something to do here

        elif persistent.monika_anniversary is not None:
            # we are in version 0.3.2
            updateGameFrom("v032")

        elif renpy.has_label("monika_monika"):
            # we are in version 0.3.1
            updateGameFrom("v031")

        else:
            # we are in version 0.3.0
            updateGameFrom("v030")

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
        addNewTopicIDs()
    
    return        

# actual update scripts
# 0.3.3
label v033:
    python:
        # add additional update code here

        # update!
        updateTopicIDs("v033")
        addNewTopicIDs()
    return

# 0.3.2
label v032:
    python:

        # update!
        updateTopicIDs("v032")
        addNewTopicIDs()
    return

# 0.3.1
label v031:
    python:
        # update!
        updateTopicIDs("v031")
        addNewTopicIDs()

    return

# 0.3.0
label v030:
    python:
        print("nothing")
        # TODO

