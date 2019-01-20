# dev related greetings

# TODO Delete this *Insert Monika with a handgun*
# Seriously this is for testing only

init python:
    if persistent._mas_fastgreeting is None:
        persistent._mas_fastgreeting = config.developer

init 5 python:
    ev_rules = {}
    ev_rules.update(MASNumericalRepeatRule.create_rule(repeat=EV_NUM_RULE_YEAR))
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_st_patrick",
            start_date=datetime.datetime(2017, 3, 17),
            end_date=datetime.datetime(2017, 3, 18),
            unlocked=True,
            rules=ev_rules
        ),
        eventdb=evhand.greeting_database,
        skipCalendar=True
    )
    del ev_rules

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
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_dev_no_hate",
            unlocked=True,
            aff_range=(None, mas_aff.UPSET)
        ),
        eventdb=evhand.greeting_database
    )


label greeting_dev_no_hate:
    m "Oh, hello [player]!"
    m "Don't worry, I know you're just testing my negative affection reactions"
    m "I know you actually love me a lot."
    m "Thanks for all your efforts!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_dev_neutral",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, mas_aff.NORMAL)
        ),
        eventdb=evhand.greeting_database
    )

label greeting_dev_neutral:
    m "Hello there [player]!"
    m 1l "Did you just wiped out the persistent file?"
    m 1l "or maybe you're just testing my neutral affection reactions?"
    m "Don't worry about it, I'll never forget all you have done for me~"
    m 1k "Thanks for all your efforts!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_dev_love",
            unlocked=True,
            aff_range=(mas_aff.HAPPY, None)
        ),
        eventdb=evhand.greeting_database
    )

label greeting_dev_love:
    m 1b "Welcome back, honey!"
    m 5a "I'm so happy to see you again."
    m 5a "I love you so much [player]!"
    m 5a "Thanks for all your efforts!"
    return


# Dev Fast greeting
init 5 python:
    if persistent._mas_fastgreeting:
        ev_rules = {}
        ev_rules.update(MASPriorityRule.create_rule(-100))
        addEvent(
            Event(
                persistent.greeting_database,
                eventlabel="greeting_fast",
                unlocked=True,
                rules=ev_rules
            ),
            code="GRE"
        )

label greeting_fast:
    m "{fast}Hello!{nw}"
    return

# greeting testing label
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_gre_sampler",
            category=["dev"],
            prompt="SAMPLE GRE",
            pool=True,
            unlocked=True
        )
    )

label dev_gre_sampler:
    m 1eua "Let's sample greeting algs."
    m "Make sure to unlock special ones if you want"

    python:
        dev_gres = [
            "greeting_st_patrick",
            "greeting_dev_no_hate",
            "greeting_dev_netural",
            "greeting_dev_love",
            "greeting_fast",
        ]
        

    menu:
        m "do you want to include dev?"
        "Yes":
            pass
        "No":
            python:
                # remove dev items 
                for d_gre in dev_gres:
                    if d_gre in store.evhand.greeting_database:
                        store.evhand.greeting_database.pop(d_gre)


    m 1eua "sample size please"
    $ sample_size = renpy.input("enter sample size", allow="0123456789")
    $ sample_size = store.mas_utils.tryparseint(sample_size, 10000)
    $ str_sample_size = str(sample_size)

    m 1eua "using sample size of [str_sample_size]"

    python:
        # prepare data
        results = {}

        # loop over sample size, run select greeting test
        for count in range(sample_size):
            gre_ev = store.mas_greetings.selectGreeting()

            if gre_ev.eventlabel in results:
                results[gre_ev.eventlabel] += 1

            else:
                results[gre_ev.eventlabel] = 0


        # done with sampling, output results
        with open(renpy.config.basedir + "/gre_sample", "w") as outdata:
            for ev_label, count in results.iteritems():
                outdata.write("{0} | {1}\n".format(count, ev_label))


    m "check files for 'gre_sample' for more info."
    return

