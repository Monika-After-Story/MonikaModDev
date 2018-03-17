# dev related farewells

init 5 python:
    rules = dict()
    rules.update(MASNumericalRepeatRule.create_rule(repeat=EV_NUM_RULE_YEAR))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_st_patrick",
            start_date=datetime.datetime(2017, 3, 17, 5),
            end_date=datetime.datetime(2017, 3, 18, 5),
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_st_patrick:
    m 1c "Aww, leaving already?"
    m 1e "It's really sad whenever you have to go..."
    m 1b "Good luck with the hangover!"
    return 'quit'

init 5 python:
    ev = Event(persistent.farewell_database,eventlabel="bye_dev",unlocked=True)
    MASFarewellRule.create_rule(random_chance=5,ev=ev)
    addEvent(ev,eventdb=evhand.farewell_database)
    del ev

label bye_dev:
    m 1c "How's the new feature going, eh [player]?"
    m 1e "Or maybe you're just running some tests?"
    m 1k "Don't give up until everything works as expected!"
    return 'quit'

# This one exists so devs get an autoupdate once they pull these changes
init 5 python:
    ev = Event(persistent.farewell_database,eventlabel="bye_dev_temp",unlocked=True)
    addEvent(ev,eventdb=evhand.farewell_database)
    del ev

label bye_dev_temp:
    m 1c "Leaving now, eh [player]?"
    m 1e "We had some changes in the farewell system, I need to update something first ..."
    python:
        for k in evhand.farewell_database:
            # no need to do any special checks since all farewells were already available
            renpy.store.evhand.farewell_database[k].unlocked = True
    $ evhand.farewell_database["bye_dev_temp"].unlocked = False
    m 1k "All done, thanks for waiting [player]!"
    #Don't show this farewell again
    return 'quit'
