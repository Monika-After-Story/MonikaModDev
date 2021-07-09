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
            m "Aww, that's nice!"
            m "I can't help but feel happy when you do..."
            m "Go and drink another one for me"
            m "I love you so much, [player]."
        "No.":
            m "Oh dear..."
            m "I hope you'll get drunk soon"
            m "Just remember that no matter what happens, no matter what anyone says or does..."
            m "Just get drunk."
            m "Just get drunk."
            menu:
                "Just get drunk.":
                    m "Drink vodnika!"
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
    m 1eub "Hello there [player]!"
    m 1rtc "Did you just wipe out your persistent file?"
    m 1etc "...Or maybe you're just testing my neutral affection reactions?"
    m 1hua "Don't worry about it, I'll never forget all you have done for me~"
    m 1hub "Thanks for all your efforts!"
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
    m 1hub "Welcome back, honey!"
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "I'm so happy to see you again."
    m 5hubsa "I love you so much [player]!"
    m 5hubsb "Thanks for all your efforts!"
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
            "greeting_dev_neutral",
            "greeting_dev_love",
            "greeting_fast",
            "greeting_dev_idle_test",
        ]

        spec_gre = [
            "i_greeting_monikaroom",
            "greeting_hairdown",
        ]

        # potentially special:
        #   monikaroom_will_change - priority of 10

        # time based
        #   greeting_timeconcern - midnight - 6am
        #   greeting_timeconcern_day - 6am to midnight

        # date + time based
        #   greeting_monika_monday_morning - monday, 5-12

        # type based
        #   greeting_sick - TYPE_SICK
        #   greeting_long_absence - TYPE_LONG_ABSENCE
        #   greeting_back_from_school - TYPE_SCHOOL
        #   greeting_back_from_work - TYPE_WORK
        #   greeting_back_from_sleep - TYPE_SLEEP
        #   greeting_returned_home - TYPE_GO_SOMEWHERE / TYPE_GENERIC_RET
        #   greeting_trick_or_treat_back - TYPE_HOL_O31_TT

        # aff based
        #   greeting_upset - UPSET ONLY / rand chance 2
        #   greeting_distressed - DISTRESSED ONLY / rand chance 2
        #   greeting_broken - BROKEN and below
        #   greeting_ourreality - ENAMORED and above (high priority)

        # forced with evs
        #   greeting_o31_rin - TYPE_HOL_O31
        #   greeting_o31_marisa - TYPE_HOL_O31

        locked_gre = []


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


    menu:
        m "Do you want to unlock special greetings?"
        "Yes":
            python:
                for s_gre in spec_gre:
                    s_gre_ev = mas_getEV(s_gre)
                    if s_gre_ev is not None:
                        if not s_gre_ev.unlocked:
                            locked_gre.append(s_gre_ev)
                        s_gre_ev.unlocked = True

        "No":
            pass


    m 1eua "sample size please"
    $ sample_size = renpy.input("enter sample size", allow="0123456789")
    $ sample_size = store.mas_utils.tryparseint(sample_size, 10000)
    if sample_size > 10000:
        $ sample_size = 10000 # anyhting longer takes too long
    $ str_sample_size = str(sample_size)

    m 1eua "using sample size of [str_sample_size]"

    $ use_type = None

    m 1eua "If you want to use a type, please set 'use_type' to an appropriate greeting type right now."

    $ check_time = None

    m 1eua "If you want to use a specific time, please set `check_time` to an appropriate datetime right now."

    m 1hua "Advance dialogue to begin sample"

    python:
        # prepare data
        results = {
            "no greeting": 0
        }

        # loop over sample size, run select greeting test
        for count in range(sample_size):
            gre_ev = store.mas_greetings.selectGreeting(use_type, check_time)

            if gre_ev is None:
                results["no greeting"] += 1

            elif gre_ev.eventlabel in results:
                results[gre_ev.eventlabel] += 1

            else:
                results[gre_ev.eventlabel] = 1


        # done with sampling, output results
        with open(renpy.config.basedir + "/gre_sample", "w") as outdata:
            for ev_label, count in results.iteritems():
                outdata.write("{0},{1}\n".format(ev_label, count))

        # relock locked gres
        for l_gre_ev in locked_gre:
            l_gre_ev.unlocked = False

    m "check files for 'gre_sample' for more info."
    return
