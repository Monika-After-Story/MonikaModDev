# dev related greetings

# TODO Delete this *Insert Monika with a handgun*
# Seriously this is for testing only
init 5 python:
    rules = dict()
    rules.update(MASNumericalRepeatRule.create_rule(repeat=EV_NUM_RULE_YEAR))
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_st_patrick",
            start_date=datetime.datetime(2017, 3, 17),
            end_date=datetime.datetime(2017, 3, 18),
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.greeting_database
    )
    del rules

label greeting_st_patrick:
    m "Oh, hello [player]!"
    m "Happy St. Patrick day!"
    menu:
        m "Are you drunk yet?"
        "I'm drunk":
            m 1k "Aww, that's nice!"
            m 1b "I can't help but feel happy when you do..."
            m 1b "Go and drink another one for me"
            m "I love you so much, [player]."
        "No.":
            m 1g "Oh dear..."
            m "I hope you'll get drunk soon"
            m "Just remember that no matter what happens, no matter what anyone says or does..."
            m "Just get drunk."
            m "Just get drunk."
            menu:
                "Just get drunk.":
                    m 4j "Drink vodnika!"
    return

# Dev Fast greeting
init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(0,24)))
    rules.update({"monika wants this first":""})
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_fast",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.greeting_database
    )
    del rules

label greeting_fast:
    m "{fast}Hello!{nw}"
    return
