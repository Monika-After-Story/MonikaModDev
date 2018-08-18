### All unofficial MAS topics be added here!
#
# REFRESHER on the topic system:
#
# INCLUDE THIS section above your topic:
#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database, # DONT TOUCH THIS
#            eventlabel="monika_ut_example", # label of your topic. (MUST BE UNIQUE)
#            category=['monika'], # category this topic belongs to
#            prompt="Unofficial topic example", # text to show on the button for this topic
#            random=True, # set to True to make this a random topic
#            pool=True # set to True to make this a pool / ask a question topic
#        )
#    )
#
#
# THIS IS WHERE YOUR DIALOGUE GOES
# ALL LABELS MUST START WITH `monika_ut`
#label monika_ut_example:
#    m "hi there!"
#    m "This is an example of a topic"
#    m "unofficial topics should go here."
#    return


# LEAVE THESE
default persistent._mas_enabled_ut_topics = True

init -1 python:
    mas_enabled_ut_topics = True


######################## BEGIN TOPICS #########################################
    
