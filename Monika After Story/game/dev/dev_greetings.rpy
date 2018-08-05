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
        eventdb=evhand.greeting_database,
        skipCalendar=True
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

init 5 python:
    rules = dict()
    rules.update(MASAffectionRule.create_rule(min=None,max=-20))
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_dev_no_hate",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.greeting_database
    )
    del rules


label greeting_dev_no_hate:
    m "Oh, hello [player]!"
    m "Don't worry, I know you're just testing my negative affection reactions"
    m "I know you actually love me a lot."
    m "Thanks for all your efforts!"
    return

init 5 python:
    rules = dict()
    rules.update(MASAffectionRule.create_rule(min=-14,max=14))
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_dev_neutral",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.greeting_database
    )
    del rules

label greeting_dev_neutral:
    m "Hello there [player]!"
    m 1l "Did you just wiped out the persistent file?"
    m 1l "or maybe you're just testing my neutral affection reactions?"
    m "Don't worry about it, I'll never forget all you have done for me~"
    m 1k "Thanks for all your efforts!"
    return

init 5 python:
    rules = dict()
    rules.update(MASAffectionRule.create_rule(min=20,max=None))
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_dev_love",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.greeting_database
    )
    del rules

label greeting_dev_love:
    m 1b "Welcome back, honey!"
    m 5a "I'm so happy to see you again."
    m 5a "I love you so much [player]!"
    m 5a "Thanks for all your efforts!"
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
