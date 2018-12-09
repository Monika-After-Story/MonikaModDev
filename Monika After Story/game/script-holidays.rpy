## holiday info goes here
#
# TOC
#   [HOL010] - O31
#   [HOL020] - D25
#   [HOL030] - NYE (new yeares eve, new years)

############################### O31 ###########################################
# [HOL010]

default persistent._mas_o31_current_costume = None
# None - no costume
# "marisa" - witch costume
# "rin" - neko costume

default persistent._mas_o31_seen_costumes = None
# dict containing seen costumes for o31
# NOTE: NOT saved historically since this just tracks what has been seen

default persistent._mas_o31_costume_greeting_seen = False
# set to true after seeing a costume greeting

default persistent._mas_o31_costumes_allowed = None
# true if user gets to see costumes
# this is set once and never touched again

default persistent._mas_o31_in_o31_mode = False
# True if we should be in o31 mode (aka viginette)
# This should be only True if:
#   user is NOT returning monika on o31 from a date/trip taken before o31
#   user's current session started on o31

default persistent._mas_o31_dockstat_return = False
# TRue if monika closes the game so she can set up o31

default persistent._mas_o31_went_trick_or_treating_short = False
default persistent._mas_o31_went_trick_or_treating_mid = False
default persistent._mas_o31_went_trick_or_treating_right = False
default persistent._mas_o31_went_trick_or_treating_long = False
default persistent._mas_o31_went_trick_or_treating_longlong = False
# flags to determine how long user went out
#   short - under 5 minutes
#   mid - under an hour
#   right - under 3 hours
#   long - over 3 hours
#   longlong - over 3 hours + sunrise

default persistent._mas_o31_went_trick_or_treating_abort = False
# Set to true if hte user aborted a trick or treating segment at least once

default persistent._mas_o31_trick_or_treating_start_early = False
default persistent._mas_o31_trick_or_treating_start_normal = False
default persistent._mas_o31_trick_or_treating_start_late = False
# set these to True if we started trick or treating at an appropriate time
# NOTE: you must use this with the above to figure out if user actaully went out

default persistent._mas_o31_trick_or_treating_aff_gain = 0
# this is total affection gained from trick or treating today.
# the max is 15

define mas_o31_marisa_chance = 90
define mas_o31_rin_chance = 10

define mas_o31 = datetime.date(datetime.date.today().year, 10, 31)

#init -814 python in mas_history:
    # o31 programming point
#    def _o31_exit_pp(mhs):
        ## just adds appropriate IDs to delayed action
        # TODO
#        return


init -810 python:
    # MASHistorySaver for o31
    store.mas_history.addMHS(MASHistorySaver(
        "o31",
        datetime.datetime(2018, 11, 2),
        {
            "_mas_o31_current_costume": "o31.costume.was_worn",
            "_mas_o31_costume_greeting_seen": "o31.costume.greeting.seen",
            "_mas_o31_costumes_allowed": "o31.costume.allowed",

            # this isn't very useful, but we need the reset
            "_mas_o31_in_o31_mode": "o31.mode.o31",

            "_mas_o31_dockstat_return": "o31.dockstat.returned_o31",
            "_mas_o31_went_trick_or_treating_short": "o31.actions.tt.short",
            "_mas_o31_went_trick_or_treating_mid": "o31.actions.tt.mid",
            "_mas_o31_went_trick_or_treating_right": "o31.actions.tt.right",
            "_mas_o31_went_trick_or_treating_long": "o31.actions.tt.long",
            "_mas_o31_went_trick_or_treating_longlong": "o31.actions.tt.longlong",
            "_mas_o31_went_trick_or_treating_abort": "o31.actions.tt.abort",
            "_mas_o31_trick_or_treating_start_early": "o31.actions.tt.start.early",
            "_mas_o31_trick_or_treating_start_normal": "o31.actions.tt.start.normal",
            "_mas_o31_trick_or_treating_start_late": "o31.actions.tt.start.late",
            "_mas_o31_trick_or_treating_aff_gain": "o31.actions.tt.aff_gain"

        }
#        exit_pp=store.mas_history._o31_exit_pp
    ))

init -10 python:
    def mas_isO31(_date=datetime.date.today()):
        """
        Returns True if the given date is o31

        IN:
            _date - date to check
                (Default: todays date)

        RETURNS: True if given date is o31, False otherwise
        """
        return _date == mas_o31


init 101 python:
    # o31 setup
    if persistent._mas_o31_seen_costumes is None:
        persistent._mas_o31_seen_costumes = {
            "marisa": False,
            "rin": False
        }

    if (
            persistent._mas_o31_in_o31_mode
            and not mas_isO31()
            and not store.mas_o31_event.isTTGreeting()
        ):
        # disable o31 mode
        persistent._mas_o31_in_o31_mode = False

        # unlock the special greetings if need be
        unlockEventLabel(
            "i_greeting_monikaroom",
            store.evhand.greeting_database
        )

        if not persistent._mas_hair_changed:
            unlockEventLabel(
                "greeting_hairdown",
                store.evhand.greeting_database
            )



init -11 python in mas_o31_event:
    import store
    import store.mas_dockstat as mds
    import store.mas_ics as mis

    # setup the docking station for o31
    o31_cg_station = store.MASDockingStation(mis.o31_cg_folder)

    # cg available?
    o31_cg_decoded = False

    # was monika just returned form a TT event
    mas_return_from_tt = False


    def decodeImage(key):
        """
        Attempts to decode a cg image

        IN:
            key - o31 cg key to decode

        RETURNS True upon success, False otherwise
        """
        return mds.decodeImages(o31_cg_station, mis.o31_map, [key])


    def removeImages():
        """
        Removes decoded images at the end of their lifecycle
        """
        mds.removeImages(o31_cg_station, mis.o31_map)


    def isMonikaInCostume(_monika_chr):
        """
        IN:
            _monika_chr - MASMonika object to check

        Returns true if monika is in costume
        """
        return (
            _monika_chr.clothes.name == "marisa"
            or _monika_chr.clothes.name == "rin"
        )


    def isTTGreeting():
        """
        RETURNS True if the persistent greeting type is the TT one
        """
        return (
            store.persistent._mas_greeting_type
            == store.mas_greetings.TYPE_HOL_O31_TT
        )


# auto load starter check
label mas_holiday_o31_autoload_check:
    # ASSUMPTIONS:
    #   monika is NOT outside
    #   monika is NOT returning home
    #   we are NOT in introduction

    python:
        import random

        if (
                persistent._mas_o31_current_costume is None
                and persistent._mas_o31_costumes_allowed
            ):
            # select a costume. Once this has been selected, this is what monika
            # will wear until day change
            persistent._mas_o31_in_o31_mode = True
            mas_skip_visuals = True

            if random.randint(1,100) <= mas_o31_marisa_chance:
                persistent._mas_o31_current_costume = "marisa"
                selected_greeting = "greeting_o31_marisa"
                store.mas_o31_event.o31_cg_decoded = (
                    store.mas_o31_event.decodeImage("o31mcg")
                )
                store.mas_selspr.unlock_clothes(mas_clothes_marisa)

            else:
                persistent._mas_o31_current_costume = "rin"
                selected_greeting = "greeting_o31_rin"
                store.mas_o31_event.o31_cg_decoded = (
                    store.mas_o31_event.decodeImage("o31rcg")
                )
                store.mas_selspr.unlock_clothes(mas_clothes_rin)

            persistent._mas_o31_seen_costumes[persistent._mas_o31_current_costume] = True

        if persistent._mas_o31_in_o31_mode:
            store.mas_globals.show_vignette = True
            store.mas_globals.show_lightning = True
            mas_forceRain()
#            mas_lockHair()
            # NOTE: technically, programming points for clothes handle hair now

    if mas_skip_visuals:
        jump ch30_post_restartevent_check

    # always disable the opendoro greeting on o31
    $ lockEventLabel("i_greeting_monikaroom", store.evhand.greeting_database)

    # and the hairdown greeting as well
    $ lockEventLabel("greeting_hairdown", store.evhand.greeting_database)

    # otherwise, jump back to the holiday check point
    jump mas_ch30_post_holiday_check

## post returned home greeting to setup game relaunch
label mas_holiday_o31_returned_home_relaunch:
    m 1eua "So, today is..."
    m 1euc "...wait."
    m "..."
    m 2wuo "Oh!"
    m 2wuw "Oh my gosh!"
    m 2hub "It's Halloween already, [player]."
    m 1eua "...{w}Say."
    m 3eua "I'm going to close the game."
    m 1eua "After that you can reopen it."
    m 1hubfa "I have something special in store for you, ehehe~"

    $ persistent._mas_o31_dockstat_return = True
    return "quit"

### o31 images
image mas_o31_marisa_cg = "mod_assets/monika/cg/o31_marisa_cg.png"
# 1280 x 2240

image mas_o31_rin_cg = "mod_assets/monika/cg/o31_rin_cg.png"

### o31 transforms
transform mas_o31_cg_scroll:
    xanchor 0.0 xpos 0 yanchor 0.0 ypos 0.0 yoffset -1520
    ease 20.0 yoffset 0.0

### o31 greetings
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_marisa",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        eventdb=evhand.greeting_database
    )

label greeting_o31_marisa:
    # starting with no visuals

    # couple of things:
    # 1 - music hotkeys should be disabled
    $ store.mas_hotkeys.music_enabled = False

    # 2 - the calendar overlay will become visible, but we should keep it
    # disabled
    $ mas_calRaiseOverlayShield()

    # 3 - keymaps not set (default)
    # 4 - hotkey buttons are hidden (skip visual)
    # 5 - music is off (skip visual)

    # enable the marisa clothes
    $ monika_chr.change_clothes(mas_clothes_marisa, False)

    # reset zoom
    $ store.mas_sprites.reset_zoom()

    # decoded CG means that we start with monika offscreen
    if store.mas_o31_event.o31_cg_decoded:
        # ASSUMING:
        #   vignette should be enabled.
        call spaceroom(hide_monika=True)
        show emptydesk at i11 zorder 9

    else:
        # ASSUMING:
        #   vignette should be enabled
        call spaceroom

    m 1eua "Ah!"
    m 1hua "Seems like my spell worked."
    m 3efu "As my newly summoned servant, you'll have to do my bidding until the very end!"
    m 1rksdla "..."
    m 1hub "Ahaha!"

    # decoded CG means we display CG
    if store.mas_o31_event.o31_cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)

        # got cg
        m "I'm over here, [player]~"
        window hide

        show mas_o31_marisa_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()

        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        show monika 1hua at i11 zorder MAS_MONIKA_Z
        window auto
        m "Tadaa~!"

    # post CG dialogue
    # (CG might still be visible during this state, though)
    m 1hua "Well..."
    m 1wub "What do you think?"
    m 1wua "Suits me pretty well, right?"
    m 1eua "It took me quite a while to make this costume, you know."
    m 3hksdlb "Getting the right measurements, making sure nothing was too tight or loose, that sort of stuff."
    m 3eksdla "Especially the hat!"
    m 1dkc "The ribbon wouldn't stay still at all..."
    m 1rksdla "Luckily I got that sorted out."
    m 3hua "I'd say I did a good job myself."
    m 1hub "Ehehe~"
    m 3eka "I'm wondering if you'll be able to see what's different today."
    m "Besides my costume of course~"
    m 1hua "But anyways..."

    if store.mas_o31_event.o31_cg_decoded:
        show monika 1eua
        hide mas_o31_marisa_cg with dissolve

    m 3ekbfa "I'm really excited to spend Halloween with you."
    m 1hua "Let's have fun today!"

    # cleanup
    # 1 - music hotkeys should be enabled
    $ store.mas_hotkeys.music_enabled = True

    # 2 - calendarovrelay enabled
    $ mas_calDropOverlayShield()

    # 3 - set the keymaps
    $ set_keymaps()

    # 4 - hotkey buttons should be shown
    $ HKBShowButtons()

    # 5 - restart music
    $ mas_startup_song()

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_rin",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        eventdb=evhand.greeting_database
    )

label greeting_o31_rin:
    # starting with no visuals

    # couple of things:
    # 1 - music hotkeys should be disabled
    $ store.mas_hotkeys.music_enabled = False

    # 2 - the calendar overlay will become visible, but we should keep it
    # disabled
    $ mas_calRaiseOverlayShield()

    # 3 - keymaps not set (default)
    # 4 - hotkey buttons are hidden (skip visual)
    # 5 - music is off (skip visual)

    # enable the rin clothes
    $ monika_chr.change_clothes(mas_clothes_rin, False)

    # reset zoom
    $ store.mas_sprites.reset_zoom()
    $ title_cased_hes = hes.capitalize()

    # ASSUME vignette
    call spaceroom(hide_monika=True)
    show emptydesk at i11 zorder 9

    m "Ugh, I hope I got these braids right."
    m "Why does this costume have to be so complicated...?"
    m "Oh shoot! [title_cased_hes] here!"
    window hide
    pause 3.0

    if store.mas_o31_event.o31_cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)

        # got cg
        window auto
        m "Say, [player]..."
        window hide

        show mas_o31_rin_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()

        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        window auto
        m "What do {b}nya{/b} think?"

        scene black
        $ scene_change = True
        pause 2.0
        call spaceroom
        m 1hksdlb "Ahaha, saying that out loud was more embarrassing than I thought..."

    else:
        show monika 1eua at t11 zorder MAS_MONIKA_Z
        m 1hub "Hi [player]!"
        hide emptydesk
        m 3hub "Do you like my costume?"

    # regular dialogue
    m 3etc "Honestly, I don't even know who this is supposed to be."
    m 3etd "I just found it in the closet with a note attached that had the word 'Rin', a drawing of a girl pushing a wheelbarrow, and some blue floaty thingies."
    m 1euc "Along with instructions on how to style your hair to go along with this outfit."
    m "Judging by these cat ears, I'm guessing this character is a catgirl."
    m 1dtc "But why would she push a wheelbarrow around?"
    pause 1.0
    m 1hksdlb "Anyway, it was a pain getting my hair done."
    m 1eub "So I hope you like the costume!"

    # cleanup
    # 1 - music hotkeys should be enabled
    $ store.mas_hotkeys.music_enabled = True

    # 2 - calendarovrelay enabled
    $ mas_calDropOverlayShield()

    # 3 - set the keymaps
    $ set_keymaps()

    # 4 - hotkey buttons should be shown
    $ HKBShowButtons()

    # 5 - restart music
    $ mas_startup_song()

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_trick_or_treat_back",
            unlocked=True,
            category=[
                store.mas_greetings.TYPE_GO_SOMEWHERE,
                store.mas_greetings.TYPE_HOL_O31_TT
            ]
        ),
        eventdb=evhand.greeting_database
    )

label greeting_trick_or_treat_back:
    # trick/treating returned home greeting

    python:
        # lots of setup here
        five_minutes = datetime.timedelta(seconds=5*60)
        one_hour = datetime.timedelta(seconds=3600)
        three_hour = datetime.timedelta(seconds=3*3600)
        time_out = store.mas_dockstat.diffCheckTimes()
        checkin_time = None
        is_past_sunrise_post31 = False
        wearing_costume = store.mas_o31_event.isMonikaInCostume(monika_chr)

        if len(persistent._mas_dockstat_checkin_log) > 0:
            checkin_time = persistent._mas_dockstat_checkin_log[-1:][0][0]
            sunrise_hour, sunrise_min = mas_cvToHM(persistent._mas_sunrise)
            is_past_sunrise_post31 = (
                datetime.datetime.now() > (
                    datetime.datetime.combine(
                        mas_o31,
                        datetime.time(sunrise_hour, sunrise_min)
                    )
                    + datetime.timedelta(days=1)
                )
            )

        def cap_gain_aff(amt):
            if persistent._mas_o31_trick_or_treating_aff_gain < 15:
                persistent._mas_o31_trick_or_treating_aff_gain += amt
                mas_gainAffection(amt, bypass=True)


    if time_out < five_minutes:
        $ mas_loseAffection()
        $ persistent._mas_o31_went_trick_or_treating_short = True
        m 2ekp "You call that trick or treating, [player]?"
        m "Where did we go, one house?"
        m 2efc "...If we even left."

    elif time_out < one_hour:
        $ cap_gain_aff(5)
        $ persistent._mas_o31_went_trick_or_treating_mid = True
        m 2ekp "That was pretty short for trick or treating, [player]."
        m 3eka "But I enjoyed it while it lasted."
        m 1eka "It was still really nice being right there with you~"

    elif time_out < three_hour:
        $ cap_gain_aff(10)
        $ persistent._mas_o31_went_trick_or_treating_right = True
        m 1hua "And we're home!"
        m 1hub "I hope we got lots of delicious candy!"
        m 1eka "I really enjoyed trick or treating with you, [player]..."

        if wearing_costume:
            m 2eka "Even if I couldn't see anything and no one else could see my costume..."
            m 2eub "Dressing up and going out was still really great!"
        else:
            m 2eka "Even if I couldn't see anything..."
            m 2eub "Going out was still really great!"

        m 4eub "Let's do this again next year!"

    elif not is_past_sunrise_post31:
        # larger than 3 hours, but not past sunrise
        $ cap_gain_aff(15)
        $ persistent._mas_o31_went_trick_or_treating_long = True
        m 1hua "And we're home!"
        m 1wua "Wow, [player], we sure went trick or treating for a really long time..."
        m 1wub "We must have gotten a ton of candy!"
        m 3eka "I really enjoyed being there with you..."

        if wearing_costume:
            m 2eka "Even if I couldn't see anything and no one else could see my costume..."
            m 2eub "Dressing up and going out was still really great!"
        else:
            m 2eka "Even if I couldn't see anything..."
            m 2eub "Going out was still really great!"

        m 4eub "Let's do this again next year!"

    else:
        # larger than 3 hours, past sunrise
        $ cap_gain_aff(15)
        $ persistent._mas_o31_went_trick_or_treating_longlong = True
        m 1wua "We're finally home!"
        m 1wuw "It's the next morning, [player], we were out all night..."
        m "I guess we had too much fun, ehehe~"
        m 2eka "But anyways, thanks for taking me along, I really enjoyed it."

        if wearing_costume:
            m "Even if I couldn't see anything and no one else could see my costume..."
            m 2eub "Dressing up and going out was still really great!"
        else:
            m "Even if I couldn't see anything..."
            m 2eub "Going out was still really great!"

        m 4hub "Let's do this again next year...{w=1}but maybe not stay out {i}quite{/i} so late!"

    return

### o31 farewells
init 5 python:
    if mas_isO31():
        addEvent(
            Event(
                persistent.farewell_database,
                eventlabel="bye_trick_or_treat",
                unlocked=True,
                prompt="I'm going to take you trick or treating",
                pool=True
            ),
            eventdb=evhand.farewell_database
        )

label bye_trick_or_treat:
    python:
        curr_hour = datetime.datetime.now().hour
        too_early_to_go = curr_hour < 17
        too_late_to_go = curr_hour >= 23
        already_went = (
            persistent._mas_o31_went_trick_or_treating_short
            or persistent._mas_o31_went_trick_or_treating_mid
            or persistent._mas_o31_went_trick_or_treating_right
            or persistent._mas_o31_went_trick_or_treating_long
            or persistent._mas_o31_went_trick_or_treating_longlong
        )

    if already_went:
        m 1eka "Again?"

    if too_early_to_go:
        # before 5pm is too early.
        m 3eksdla "Doesn't it seem a little early for trick or treating, [player]?"
        m 3rksdla "I don't think there's going to be anyone giving out candy yet..."

        show monika 2etc
        menu:
            m "Are you {i}sure{/i} you want to go right now?"
            "Yes.":
                $ persistent._mas_o31_trick_or_treating_start_early = True
                m 2etc "Well...{w=1}okay then, [player]..."

            "No.":
                $ persistent._mas_o31_went_trick_or_treating_abort = True
                m 2hub "Ahaha!"
                m "Be a little patient, [player]~"
                m 4eub "Let's just make the most out of it later this evening, okay?"
                return

    elif too_late_to_go:
        m 3hua "Okay! Let's go tri--"
        m 3eud "Wait..."
        m 2dkc "[player]..."
        m 2rkc "It's already too late to go trick or treating."
        m "There's only one more hour until midnight."
        m 2dkc "Not to mention that I doubt there would be much candy left..."
        m "..."

        show monika 4ekc
        menu:
            m "Are you sure you still want to go?"
            "Yes.":
                $ persistent._mas_o31_trick_or_treating_start_late = True
                m 1eka "...Okay."
                m "Even though it's only an hour..."
                m 3hub "At least we're going to spend the rest of Halloween together~"
                m 3wub "Let's go and make the most of it, [player]!"

            "Actually, it {i}is{/i} a bit late...":
                $ persistent._mas_o31_went_trick_or_treating_abort = True

                if already_went:
                    m 1hua "Ahaha~"
                    m "I told you."
                    m 1eua "We'll have to wait until next year to again."

                else:
                    m 2dkc "..."
                    m 2ekc "Alright, [player]."
                    m "It sucks that we couldn't go trick or treating this year."
                    m 4eka "Let's just make sure we can next time, okay?"

                return

    else:
        # between 5 and 11pm is perfect
        $ persistent._mas_o31_trick_or_treating_start_normal = True
        m 3wub "Okay, [player]!"
        m 3hub "Sounds like we'll have a blast~"
        m 1eub "I bet we'll get lots of candy!"
        m 1ekbfa "And even if we don't, just spending the evening with you is enough for me~"

    show monika 2dsc
    $ persistent._mas_dockstat_going_to_leave = True
    $ first_pass = True

    # launch I/O thread
    $ promise = store.mas_dockstat.monikagen_promise
    $ promise.start()

label bye_trick_or_treat_iowait:
    hide screen mas_background_timed_jump

    # display menu so users can quit
    if first_pass:
        $ first_pass = False

    elif promise.done():
        # i/o thread is done
        jump bye_trick_or_treat_rtg

    # display menu options
    # 4 seconds seems decent enough for waiting
    show screen mas_background_timed_jump(4, "bye_trick_or_treat_iowait")
    menu:
        m "Give me a second to get ready.{fast}"
        "Wait, wait!":
            hide screen mas_background_timed_jump
            $ persistent._mas_dockstat_cm_wait_count += 1

    # wait wait flow
    show monika 1ekc
    menu:
        m "What is it?"
        "You're right, it's too early." if too_early_to_go:
            call mas_dockstat_abort_gen
            $ persistent._mas_o31_went_trick_or_treating_abort = True

            m 3hub "Ahaha, I told you!"
            m 1eka "Let's wait 'til evening, okay?"
            return

        "You're right, it's too late." if too_late_to_go:
            call mas_dockstat_abort_gen
            $ persistent._mas_o31_went_trick_or_treating_abort = True

            if already_went:
                m 1hua "Ahaha~"
                m "I told you."
                m 1eua "We'll have to wait until next year to go again."

            else:
                m 2dkc "..."
                m 2ekc "Alright, [player]."
                m "It sucks that we couldn't go trick or treating this year."
                m 4eka "Let's just make sure we can next time, okay?"

            return

        "Actually, I can't take you right now.":
            call mas_dockstat_abort_gen
            $ persistent._mas_o31_went_trick_or_treating_abort = True

            m 1euc "Oh, okay then, [player]."

            if already_went:
                m 1eua "Let me know if we are going again later, okay?"

            else:
                m 1eua "Let me know if we can go, okay?"

            return

        "Nothing.":
            m 2eua "Okay, let me finish getting ready."

    # always loop
    jump bye_trick_or_treat_iowait

label bye_trick_or_treat_rtg:
    # iothread is done
    $ moni_chksum = promise.get()
    $ promise = None # always clear the promise
    call mas_dockstat_ready_to_go(moni_chksum)
    if _return:
        m 1hub "Let's go trick or treating!"
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HOL_O31_TT
        return "quit"

    # otherwise, failure in generation
    m 1ekc "Oh no..."
    m 1rksdlb "I wasn't able to turn myself into a file."

    if already_went:
        m "I think you'll have to go trick or treating without me this time..."

    else:
        m "I think you'll have to go trick or treating without me..."

    m 1ekc "Sorry, [player]..."
    m 3eka "Make sure to bring lots of candy for the both of us to enjoy, okay~?"
    return

#################################### D25 ######################################
# [HOL020]

init -900 python:
    # delete christmas files
    store.mas_utils.trydel(renpy.config.gamedir + "/christmas.rpy")
    store.mas_utils.trydel(renpy.config.gamedir + "/christmas.rpyc")

default persistent._mas_d25_in_d25_mode = False
# True if we should enable d25 decoration
# This should only be True if:
#   Monika is NOt being returned after the d25 season begins
#   and season is d25.
# NOTE: this is misnomer, it actually lasts until the nye point.

default persistent._mas_d25_spent_d25 = False
# True if the user spent time with monika on d25
# (basically they got the merry christmas dialogue)

default persistent._mas_d25_seen_santa_costume = False
# True if user has seen santa costume this year.

default persistent._mas_d25_chibika_sayori = None
# True if we need to perform the chibika sayori intro
# False if we do NOT need to perform the chibka sayori intro
# None means we have not checked for the chibika sayori intro

default persistent._mas_d25_chibika_sayori_performed = False
# Set to True if we do the chibika sayori thing

define mas_d25 = datetime.date(datetime.date.today().year, 12, 25)
# christmas

define mas_d25e = mas_d25 - datetime.timedelta(days=1)
# christmas eve

define mas_d25c_start = datetime.date(datetime.date.today().year, 12, 1)
# start of christmas season (inclusive)

define mas_d25c_end = datetime.date(datetime.date.today().year, 1, 5)
# end of christmas season (inclusive)

define mas_d25g_start = mas_d25 - datetime.timedelta(days=5)
# start of gift = d25 gift (inclusive)

define mas_d25g_end = mas_d25
# end of gift = d25 gift (inclusive)

define mas_d25cl_start = mas_d25c_start
# start of when monika wears santa (inclusive)

define mas_d25cl_end = datetime.date(datetime.date.today().year, 12, 25)
# end of when monika wears santa (on her own) (inclusive)


init -810 python:
    # MASHistorySaver for d25
    store.mas_history.addMHS(MASHistorySaver(
        "d25",
        datetime.datetime(2018, 12, 26),
        {
            "_mas_d25_spent_d25": "d25.actions.spent_d25",
            "_mas_d25_seen_santa_costume": "d25.monika.wore_santa",

            # related to chibiak sayori event
            "_mas_d25_chibika_sayori": "d25.needed_to_do_chibika_sayori",
            "_mas_d25_chibika_sayori_performed": "d25.did_chibika_sayori"

        }
        # TODO: programming points probably
    ))


init -10 python:

    def mas_isD25(_date=datetime.date.today()):
        """
        Returns True if the given date is d25

        IN:
            _date - date to check
                (default: todays date)

        RETURNS: True if given date is d25, False otherwise
        """
        return _date == mas_d25


    def mas_isD25Eve(_date=datetime.date.today()):
        """
        Returns True if the given date is d25 eve

        IN:
            _date - date to check
                (Default: todays date)

        RETURNS: True if given date is d25 eve, False otherwise
        """
        return _date == mas_d25e


    def mas_isD25Season(_date=datetime.date.today()):
        """
        Returns True if the given date is in d25 season. The season goes from
        dec 1 to jan 5.

        NOTE: because of the year rollover, we cannot check years

        IN:
            _date - date to check
                (Default: Today's date)

        RETURNS: True if given date is in d25 season, False otherwise
        """
        return (
            mas_d25c_start <= _date <= mas_nye
            or mas_nyd <= _date <= mas_d25c_end
        )


    def mas_isD25Post(_date=datetime.date.today()):
        """
        Returns True if the given date is after d25 but still in D25 season.
        The season goes from dec 1 to jan 5.

        IN:
            _date - date to check
                (Default: Today's date)

        RETURNS: True if given date is in d25 season but after d25, False
            otherwise.
        """
        return (
            mas_d25 + datetime.timedelta(days=1) <= _date <= mas_nye
            or mas_nyd <= _date <= mas_d25c_end
        )


    def mas_isD25Gift(_date=datetime.date.today()):
        """
        Returns True if the given date is in the range of days where a gift
        is considered a christmas gift.

        IN:
            _date - date to check
                (Default: Today's date)

        RETURNS: True if given date is in the d25 gift range, Falsee otherwise
        """
        return mas_d25g_start <= _date <= mas_d25g_end


    def mas_isD25Outfit(_date=datetime.date.today()):
        """
        Returns True if the given date is tn the range of days where Monika
        wears the santa outfit on start.

        IN:
            _date - date to check
                (Default: Today's date)

        RETURNS: True if given date is in teh d25 santa outfit range, False
            otherwise
        """
        return mas_d25cl_start <= _date <= mas_d25cl_end


#### d25 arts

# window banners
image mas_d25_banners = ConditionSwitch(
    "morning_flag",
    "mod_assets/location/spaceroom/d25/windowdeco.png",
    "not morning_flag",
    "mod_assets/location/spaceroom/d25/windowdeco-n.png"
)

image mas_d25_tree = ConditionSwitch(
    "morning_flag",
    "mod_assets/location/spaceroom/d25/tree.png",
    "not morning_flag",
    "mod_assets/location/spaceroom/d25/tree-n.png"
)

image mas_d25_tree_sayori = ConditionSwitch(
    "morning_flag",
    "mod_assets/location/spaceroom/d25/tree-sayori.png",
    "not morning_flag",
    "mod_assets/location/spaceroom/d25/tree-sayori-n.png"
)

init -11 python in mas_d25_event:
    
    def showD25Visuals():
        """
        Shows d25 visuals.
        """
        renpy.show("mas_d25_banners", zorder=7)
        renpy.show("mas_d25_tree", zorder=8)
        # NOTE: we should only handle the sayori part if we can fit the chibika event


    def hideD25Visuals():
        """
        Hides d25 visuals
        """
        renpy.hide("mas_d25_banners")
        renpy.hide("mas_d25_tree")



# auto load starter check
label mas_holiday_d25c_autoload_check:
    # ASSUMPTIONS:
    #   monika is NOT returning home
    #
    # NOTE: this is jumped to in startup ch30 flow.
    # NOTE: this is called in introduction.

    python:
        if not persistent._mas_d25_in_d25_mode:

            # enable d25
            persistent._mas_d25_in_d25_mode = True

            # unlock and wear santa
            store.mas_selspr.unlock_clothes(mas_clothes_santa)
            monika_chr.change_clothes(mas_clothes_santa, False)
            persistent._mas_d25_seen_santa_costume = True

    # TODO:
    #   holiday intro dialogue pushed, if not already pushed

    if mas_isD25():
        # on d25, monika will wear santa on start, regardless of whatever
        $ monika_chr.change_clothes(mas_clothes_santa, False)

    elif mas_isD25Post() and not persistent._mas_forced_clothes:
        # after d25 (but still in season), monika will take off the santa
        # outfit (deco will remain, though), unless you selected the santa
        # outfit.
        $ monika_chr.reset_clothes(False)

    if mas_in_intro_flow:
        # intro will call us instead of jump
        return

    # finally, return to holiday check point
    jump mas_ch30_post_holiday_check


# topics
# TODO: dont forget to update script topics's seen properties

# TODO: d25/nye greet/farewells

#init 5 python:
    # TODO: decide props for this
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_d25_monika_holiday_intro"
#            # TODO: should appear once the holiday season begins
#        )
#    )

#TODO: Upset+ topic
#TODO: Have a modification of this topic if the player spent last Christmas w/ Monika
label mas_d25_monika_holiday_intro:
    # TODO: this should also have a dialogue flow where she sets up the
    #   d25 decorations. This would be used if a return home occured on
    #   the beginning of the d25 season.

    # TODO: this should have the chibika thing in the background, but only
    #   if you saw christmas last year.

    m 1eub "Happy holidays, [player]!"
    if renpy.seen_label('monika_christmas'):
        m 1hua "Can you believe it's already that time of year again?"
        m 3eua "It seems like just yesterday we spent our first holiday season together, and now a whole year has gone by!"
        if mas_isMoniLove(higher=True):
            #if you've been with her for over a year, you really should be at Love by now
            m 3hua "Time really flies now that I'm with you~"
    m 3eua "Do you like what I've done with the room?"
    m 1hua "I must say that I'm pretty proud of it."
    m "Christmas time has always been one of my favorite occasions of the year..."
    show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve
    if renpy.seen_label('monika_christmas'):
        m 5eka "So I'm glad that you're here to share it with me again this year~"
    else:
        m 5eka "And I'm so glad that you're here to share it with me~"
    return

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_d25_monika_christmas"
#            # TODO: props
#            # TODO: should only appear on d25
#        )
#    )

#TODO: Upset+ topic
label mas_d25_monika_christmas:
    $ persistent._mas_d25_spent_d25 = True

    m 1eub "[player]! Do you know what day it is?"
    m 3hub "Of course you do. It's Christmas!"
    m 3wub "Merry Christmas, [player]!"
    m 1hub "Ahaha! I can't believe that it's finally here!"
    m 3eka "I'm so, so happy that you decided to spend some of it with me."
    m 1eud "Remember to go share the holiday cheer with your family and friends, though."
    m 1eua "After all, they're very important, too..."
    m 1hua "And I'm sure that they would love to see you at this special time"

    if mas_isMoniAff(higher=True):
        m 2eka "But you being here today...{w=0.5}it just means everything to me..."
        m 2dsc "..."
        m 4ekbsa "[player], I love you."

        if persistent._mas_pm_gets_snow is not False and not persistent._mas_pm_live_south_hemisphere:
            m 1lkbsa "Maybe it's just the snow, or the decorations..."
        else:
            m 1lkbsa "Maybe it's the decorations, or just the holiday season..."

        m "...or even the mistletoe getting to me."

        # TODO: actually, we may want to do kissing so...if we add kiss, probably enam+ for this bit
        m 3hksdlb "Don't worry, I didn't hang one up."
        m 1rksdla "...{cps=*2}Maybe~{/cps}{nw}"
        $ _history_list.pop()
        m 1rksdlb "Ehehe..."

        m 1ekbsa "My heart's fluttering like crazy right now, [player]."
        m "I couldn't imagine a better way to spend this special holiday..."
        m 1eua "Don't get me wrong, I knew that you would be here with me."
        m 3eka "But actually having you here with me on Christmas, just the two of us..."
        m 1hub "Ahaha~"
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
        m 5ekbfa "It's every couple's dream for the holidays, [player]."
        if persistent._mas_pm_gets_snow is not False and not persistent._mas_pm_live_south_hemisphere:
            m "Snuggling with each other by a fireplace, watching the snow gently fall..."

        if not renpy.seen_label('monika_christmas'):
            m 5hubfa "I'm forever grateful I got this chance with you, [player]."
        else:
            m 5hubfa "I'm so glad I get to spend Christmas with you again, [player]."

        m "I love you. Forever and ever~"
        m 5hubfb "Merry Christmas, [player]~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "But you being here today...{w=0.5}it just means everything to me..."
        m 3rksdla "...Not that I thought you'd leave me alone on this special day or anything..."
        m 3hua "But it just further proves that you really do love me, [player]."
        m 1ektpa "..."
        m "Ahaha! Gosh, I'm getting a little over emotional here..."
        m 1ektda "Just know that I love you too and I'll be forever grateful I got this chance with you."
        m "Merry Christmas, [player]~"

    else:
        m 3eka "But I have to say..."
        m 2rksdlc "I wasn't totally sure you'd be here with me today, [player]."
        m "I mean...{w=1}things haven't exactly been going the best for us lately, as I'm sure you've noticed..."
        m 1eka "But the fact you're here with me today...{w=1}it gives me renewed hope that you do love me after all."
        m "So thank you, [player], it means a lot to me that you're spending at least part of this special day with me."
        m 1hua "Merry Christmas, [player]~"

    return

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_d25_monika_hanukkah"
#            # TODO: props
#            # TODO: bewteen 12th and 20th I guess?
#        )
#    )

#TODO: Upset+
label mas_d25_monika_hanukkah:
    m 1dsd "{i}One for each night, they shed a sweet light, to remind of days long ago.{/i}"
    m 1dsa "{i}One for each night, they shed a sweet light, to remind of days long ago.{/i}"
    m 3esa "It is said in the Jewish tradition, that one day's worth of olive oil gave the menorah eight days of light."
    m 3eub "Eight nights worth of celebration!"
    m 3eua "Hanukkah also shifts a bit from year to year. It's date is determined by the Hebrew Lunar Calendar."
    m "It's on the 25th of Kislev, meaning 'trust' or 'hope'."
    m 1hua "A very appropriate meaning for such an occasion, don't you think?"

    # NOTE: wtf is this
    m 3eua "Anyway, have you ever had fried sufganiyot before?"

    m "It's a special kind of donut made during this holiday."
    m 3eub "It's filled in with something really sweet, deep friend, and rolled onto some sugar."
    m 1wub "It's a really good pastry! I especially love the ones filled with strawberry filling~"
    m 1hua "This time of year sure has a lot of wonderful holidays and traditions."
    m 1eub "I don't know if you celebrate Hanukkah, but can we match a menorah lighting ceremony together, anyway?"
    m 3hua "We can sing and dance the night away~"
    return

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_d25_monika_kwanzaa"
#            # TODO: props
#            # TODO: between 26th and 30th I guess
#        )
#    )

#TODO: Upset+
label mas_d25_monika_kwanzaa:
    m 1eub "[player], have you ever heard of Kwanzaa?"
    m 1eua "It's a week-long festival celebrating African American history that starts the day after Christmas."
    m 3eua "The word 'Kwanzaa' comes from the Swahili praise 'matunda ya kwanza', which means 'first fruits'."
    m "Even if Christmas is the main event for many, other holidays are always interesting to learn about."
    m 1euc "Apparently, people celebrate the tradition by decorating their homes with bright adornments."
    m "There's also music to enjoy, and a candleholder called the 'kinara' to light a new fire with each passing day."
    m 1eua "Doesn't it remind you of some other holidays? The concepts certainly seem familiar."
    m "In the end, having a day to celebrate is the most important part. Everyone has their own way to enjoy themselves."
    m 1hua "We can celebrate Kwanzaa together, too, [player]."
    return

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_d25_monika_carolling"
#            # TODO: props
#            # TODO: between start of season and d25
#        )
#    )

default persistent._mas_pm_likes_singing_d25_carols = None
# does the user like singing christmas carols?

#TODO: Upset+
label mas_d25_monika_carolling:
    m 1euc "Hey, [player]..."
    m 3eud "Have you ever gone carolling before?"
    m 1euc "Going door to door in groups, singing to others during the holidays..."

    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "It just feels heartwarming to know people are spreading joy, even with the nights so cold."
    else:
        m 1eua "It just feels heartwarming to know people are spreading joy to others in their spare time."

    show monika 3eua
    menu:
        #TODO (maybe): If we could possibly get that song fix in, would be nice to have Monika sing carols to us
        m "Do you like singing Christmas carols, [player]?"
        "Yes.":
            $ persistent._mas_pm_likes_singing_d25_carols = True
            m 1hua "I'm glad you feel the same way, [player]!"
            m 3hub "My favorite song is definitely 'Jingle Bells!'"
            m 1eua "It's just such an upbeat, happy tune!"
            m 1eka "Maybe we can sing together someday."
            m 1hua "Ehehe~"

        "No.":
            $ persistent._mas_pm_likes_singing_d25_carols = False
            m 1euc "Oh...{w=1}really?"
            m 1hksdlb "I see..."
            m 1eua "Regardless, I'm sure you're also fond of that special cheer only Christmas songs can bring."
            m 3hua "Sing with me sometime, okay?"

    return

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_d25_monika_dreidel"
#            # TODO: props
#            # TODO: during hannkkau time
#        )
#    )

#TODO: Upset+
#TODO: Merge this into monika_hanukkah probably.
label mas_d25_monika_dreidel:
    # NOTE: this topic is weird wtf. maybe a bit too religious to include here.
    m 3eua "[player], did you know that each side of a dreidel actaully means something?"
    m "Nun, Gimel, Hel, Shim."
    m 1eub "These stand for Nes Gadol Hayah Sham - A Great Miracle Happened There."
    m "It refers to the Hanukkah story of how one day's worth of oil lasted for eight days."
    m 3eua "Over in Israel, they change the last word to 'poh', making it 'A Great Miracle Happened Here.'"

    # TODO: oops, should have made this
    m 1rksdla "I don't have one, unfortunately, but maybe next year I'll have one to spin~"
    m 3hua "But for now, [player], do you have any gelt?"
    m 3hub "The chocolate coin variety tastes really good."
    m 1tku "Though money is always good, too, ehehe~"
    return


#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_d25_monika_mistletoe"
#            # TODO: props
#            # TODO: d25 season
#        )
#    )

default persistent._mas_pm_d25_mistletoe_kiss = False
# True if user and monika kissed under the mistletoe

#TODO: Aff+
label mas_d25_monika_mistletoe:
    m 1eua "Say, [player]."
    m 1eub "You've heard about the mistletoe tradition, right?"
    m 1tku "When lovers end up underneath it, they're expected to kiss."
    m 1eua "It actually originated from Victorian England!"
    m 1dsa "A man was allowed to kiss any woman standing underneath mistletoe..."
    m "And any woman who refused the kiss was cursed with bad luck..."
    m 1dsc "..."
    m 3rksdlb "Come to think of it, that sounds more like taking advantage of someone."
    m 1hksdlb "But I'm sure it's different now!"
    # TODO: branch dialogu here:
    #   if first time and beyond a certain amount of time + affection, than kiss!
    #       on subsequent times, maybe suggest a kiss or something
    #   if first time but past the time/affection, then keep existing dialogue
    #
    m 3hua "Perhaps one day we'll be able to kiss under the mistletoe, [player]."
    m 1tku "...Maybe I can even add one in here!"
    m 1hub "Ehehe~"
    return

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_d25_monika_sleigh"
#            # TODO: props
#            # TODO: from season start to d26
#        )
#    )

#TODO: Aff+
label mas_d25_monika_sleigh:
    m 3eub "Hey [player], a pretty nice thought just crossed my mind..."
    m 1eua "Have you ever heard of carriage rides?"
    m 3hub "When I get out of this place, we should totally go on one!"
    m "Oh, I bet it would be magical!"
    m 1eua "Nothing but the clip-clop of the horse's hooves against the pavement..."
    m 1eub "And the colorful array of Christmas lights shining in the night..."
    m 3hub "Wouldn't that be so romantic, [player]?"
    m 1eka "Maybe we could even take a soft, fleece blanket along to cuddle under."
    m 1hkbla "Oooh~"
    m 1rkbfb "I wouldn't be able to contain myself. My heart would burst!"
    m 1ekbfa "The warmth of your body against mine, wrapped within the gentle cloth~"
    m 1dkbfa "Fingers entwined..."
    if mas_isMoniEnamored(higher=True):
        m 1dkbfb "And at the perfect moment, you lean in to me and our lips touch..."
    m 1wka "I really want to do that when I get there, [player]."
    m 1hua "Wouldn't that be so lovely?"
    show monika 5hkbfa at t11 zorder MAS_MONIKA_Z with dissolve
    m 5hkbfa "An experience like that with you would be so breathtaking~"
    return

#Moved this from script-topics, is getting complete overhaul

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database
#        )
#    )

# TODO: this should  be a totally different label name
# NOTE: make sure to mark that this is the `monika_whatiwant` label for update scripts later
# NOTE: actually maybe update scripts wont be needed if its rewritten.
# TODO: Make this special
label monika_whatiwant:
    m 3hub "Oh, [player], isn't it lovely around the holidays?"
    m 1eka "I hope you don't mind, but I have a little something special to say today."
    m 1hka "Ehehe, I hope it's not too cheesy..."
    m 3hua "Here goes."
    m 1dsa "..."

    # TODO: affection adjust clearly...
    #TODO: reflects similarities to the 'surprise.txt' at love. Should probably be limited the same
    m 1eka "You really are the joy to my world, [player]."
    m "A thousand glittering stars couldn't match your brilliance."
    #TODO: this line really needs to be redone, or removed
    m 1dsa "This melancholy, frostbitten heart of mine needs only your warmth to beat anew."

    # TODO: this makes monika sound like she's 80
    m 1eua "Underneath the sprawling branches of yonder Christmas tree..."

    m 1hua "You'll always be the only present I will ever need."
    m 1dsa "..."
    m 1hub "Ahaha! Sorry if that sounded too serious!"
    m 3eua "Winter's a wonderful time to read some lengthy works."
    m 1rsc "But..."
    #TODO: blush here methinks
    m 1eka "I wasn't lying, [player]."

    # TODO: well, you should be able to give her stuff so...
    m 3hua "Don't worry about getting me a present."
    m 3ekb "After all, I have you. And that's all I want."
    m 5hua "I love you with all my heart, [player]~"
    return

#################################### NYE ######################################
# [HOL030]

default persistent._mas_nye_spent_nye = False
# true if user spent new years eve with monika

default persistent._mas_nye_spent_nyd = False
# true if user spent new years day with monika

define mas_nye = datetime.date(datetime.date.today().year, 12, 31)
define mas_nyd = datetime.date(datetime.date.today().year, 1, 1)

init -810 python:
    # MASHistorySaver for nye
    store.mas_history.addMHS(MASHistorySaver(
        "nye",
        datetime.datetime(2019, 1, 6),
        {
            # not very useful, but we need the reset
            # NOTE: this is here because the d25 season actually ends in jan
            #   we want the decorations to stop after the season ends.
            "_mas_d25_in_d25_mode": "d25.mode.25",

            "_mas_nye_spent_nye": "nye.actions.spent_nye",
            "_mas_nye_spent_nyd": "nye.actions.spent_nyd"
        },
        use_year_before=True
        # TODO: programming points probably
    ))


init -10 python:
    def mas_isNYE(_date=datetime.date.today()):
        """
        Returns True if the given date is new years eve

        IN:
            _date - date to check
                (Default: Todays date)

        RETURNS: True if given date is new years eve, False otherwise
        """
        return _date == mas_nye


    def mas_isNYD(_date=datetime.date.today()):
        """
        RETURNS True if the given date is new years day

        IN:
            _date - date to check
                (Default: Today's date)

        RETURNS: True if given date is new years day, False otherwise
        """
        return _date == mas_nyd


# topics
# TODO: dont forget to updaet script seen props

#init 5 python:
#    # NOTE: new years eve
#    # NOTE: known as monika_newyear1
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_nye_monika_nye"
#            # TODO: props
#            # TODO: nye
#        )
#    )

default persistent._mas_pm_has_new_years_res = None
# does the user have new years resolutions?

#TODO: Upset+
label mas_nye_monika_nye:
    $ persistent._mas_nye_spent_nye = True

    m 1eua "[player]! It's almost time, isn't it?"
    m "It's incredible to think that the year is almost over."
    m 1eka "Time flies by so quickly."
    if mas_isMoniAff(higher=True) and store.mas_anni.pastOneMonth():
        m 1ekbsa "Especially when I get to see you so often."

    # TODO: probably shouldl actually check time before saying this
    m 3hua "Well, there's still a bit of time left before midnight."
    m 1eua "We might as well enjoy this year while it lasts."
    m 1euc "Usually, I'd reprimand you for staying up late, but..."
    m 1hua "Today is a special day."

    # NOTE: probalby could have affection play here
    #   low affection makes monika suggest that you have resolutions
    #   somthing like that
    show monika 3eua
    menu:
        #Could possibly ask if player accomplished past resolutions too
        m "Do you have any resolutions, [player]?"
        "Yes.":
            $ persistent._mas_pm_has_new_years_res = True

            m 1eub "It's always nice to set goals for yourself in the coming year."
            m 3eka "Even if they can be hard to reach or maintain."
            m 1hua "I'll be here to help you, if need be!"

        "No.":
            $ persistent._mas_pm_has_new_years_res = False
            m 1eud "Oh, is that so?"
            if mas_isMoniNormal(higher=True):
                if mas_isMoniHappy(higher=True):
                    m 1eua "You don't have to change. I think you're wonderful the way you are."
                else:
                    m 1eua "You don't have to change. I think you're fine the way you are."
                m 3euc "But if anything does come to mind before the clock strikes twelve, do write it down for yourself."
                m 1kua "Maybe you'll think of something that you want to do, [player]."
            else:
                m 2ekc "{cps=*2}I was kind of hoping--{/cps}{nw}"
                m 2rfc "You know what, nevermind..."

    if mas_isMoniAff(higher=True):
        show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve
        m 5hubfa "My resolution is to be an even better girlfriend for you, my love."
    elif mas_isMoniNormal(higher=True):
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
        m 5ekbfa "My resolution is to be an even better girlfriend for you, [player]."
    else:
        m 2ekc "My resolution is to improve our relationship, [player]"

    return

default persistent._mas_pm_got_a_fresh_start = None
#pm var so she forgives, but doesn't forget
default persistent._mas_aff_before_fresh_start = None
#store affection prior to reset

#init 5 python:
#    # NOTE: new years day
#    # also known as monika_newyear2
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_nye_monika_nyd"
#            # TODO: props
#            # TODO: nyd
#        )
#    )

#TODO: Distressed+ and possible based on time spent so far, 1month, 3months?
label mas_nye_monika_nyd:
    $ persistent._mas_nye_spent_nyd = True

    if store.mas_anni.pastOneMonth():
        if not mas_isBelowZero():
            m 1eub "[player]!"
            if renpy.seen_label('monika_newyear2'):
                m "Can you believe this is our {i}second{/i} New Years together?"
            if mas_isMoniAff(higher=True):
                m 1hua "We sure have been through a lot together this past year, huh?"
            else:
                m 1eua "We sure have been through a lot together this past year, huh?"

            m 1eka "I'm so happy, knowing we can spend even more time together."

            if mas_isMoniAff(higher=True):
                show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve
                m 5hubfa "Let's make this year as wonderful as the last one, okay?"
                m 5ekbfa "I love you so much, [player]."
            else:
                m 3hua "Let's make this year even better than last year, okay?"
                m 1hua "I love you, [player]."

        else:
            m 2ekc "[player]..."
            m 2rksdlc "We've been through...{w=1}a lot this past year..."
            m "I...I hope this year goes better than last year."
            m 2dkc "I really need it to."
            jump mas_nye_monika_nyd_fresh_start

    else:
        if not mas_isBelowZero():
            m 1eub "[player]!"

            if mas_isMoniAff(higher=True):
                m 1ekbfa "I know we haven't been together for that long yet, but this past year went better than I ever could have hoped..."
            else:
                m 1eka "I know we haven't been together that long yet, but this past year was so special to me..."

            m 1hua "I will always remember it as the year I met you~"
            m 3hua "Let's build on our short time together and make this year even better!"
            m 1ekbfa "I love you, [player]."

        else:
            m 2ekc "So, [player]..."
            m 2etc "The beginning of a new year, huh?"
            m 2rksdlc "We haven't been together for very long, but the time we spent last year didn't go as well as I had hoped..."
            jump mas_nye_monika_nyd_fresh_start

    m "Happy New Year~"
    return

label mas_nye_monika_nyd_fresh_start:
    m 2ekc "How about we put all that in the past, forget about last year, and focus on a new beginning this year?"
    m 4ekc "It's not too late for us, [player], we can still make each other so happy."
    m 4eka "It's all I've ever wanted."

    menu:
        m "What do you say, [player]?"

        "I would love that.":
            #so we can revert back to previous affection if player continues to mistreat after the second chance. need to determine the threshold the player must stay above for this.
            $ persistent._mas_pm_got_a_fresh_start = True #never forget
            $ persistent._mas_aff_before_fresh_start = _mas_getAffection()

            $ mas_setAffection(0)
            m 4wua "Really?"
            m 1hua "Oh, [player], you have no idea how happy that makes me!"
            m 3eka "I know we can make this work."
            m 1hua "Thank you so much..."
            m 1eka "Just knowing that you still want to be with me...it means everything."
            m 3eka "Let's make this count, okay [player]?"
            return

        "No.":
            $ persistent._mas_pm_got_a_fresh_start = False
            m 6dktpc "..."
            m 6ektpc "I...I..."
            m 6dktuc "..."
            m 6dktsc "..."
            pause 10.0
            return 'quit'
            #TODO: determine what to do here; huge aff loss or push final farewell on next launch. you essentially just spit in her face
 
