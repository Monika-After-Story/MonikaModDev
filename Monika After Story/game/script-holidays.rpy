## holiday info goes here
#
# TOC
#   [GBL000] - GLOBAL SPACE
#   [HOL010] - O31
#   [HOL020] - D25
#   [HOL030] - NYE (new yeares eve, new years)
#   [HOL040] - player_bday
#   [HOL050] - F14
#   [HOL060] - 922


############################### GLOBAL SPACE ################################
# [GBL000]
default persistent._mas_event_clothes_map = dict()
define mas_five_minutes = datetime.timedelta(seconds=5*60)
define mas_one_hour = datetime.timedelta(seconds=3600)
define mas_three_hour = datetime.timedelta(seconds=3*3600)

init -1 python:
    def mas_checkOverDate(_date):
        """
        Checks if the player was gone over the given date entirely (taking you somewhere)

        IN:
            date - a datetime.date of the date we want to see if we've been out all day for

        OUT:
            True if the player and Monika were out together the whole day, False if not.
        """
        checkout_time = store.mas_dockstat.getCheckTimes()[0]
        return checkout_time is not None and checkout_time.date() < _date

    def mas_capGainAff(amount, aff_gained_var, normal_cap, pbday_cap=None):
        """
        Gains affection according to the cap(s) defined

        IN:
            amount:
                Amount of affection to gain

            aff_gained_var:
                The persistent variable which the total amount gained for the holiday is stored
                (NOTE: Must be a string)

            normal_cap:
                The cap to use when not player bday

            pbday_cap:
                The cap to use when it's player bday (NOTE: if not provided, normal_cap is assumed)
        """

        #If player bday cap isn't provided, we just use the one cap
        if persistent._mas_player_bday_in_player_bday_mode and pbday_cap:
            cap = pbday_cap
        else:
            cap = normal_cap

        if persistent.__dict__[aff_gained_var] < cap:
            persistent.__dict__[aff_gained_var] += amount
            mas_gainAffection(amount, bypass=True)

        return

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
        #datetime.datetime(2018, 11, 2),
        # change trigger to better date
        datetime.datetime(2020, 1, 6),
        {
            # TODO: we should have a spent time var here

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

        },
        use_year_before=True,
#        exit_pp=store.mas_history._o31_exit_pp
        start_dt=datetime.datetime(2019, 10, 31),

        # end is 1 day out in case of an overnight trick or treat
        end_dt=datetime.datetime(2019, 11, 2) 
    ))

init -10 python:
    def mas_isO31(_date=None):
        """
        Returns True if the given date is o31

        IN:
            _date - date to check.
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is o31, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_o31.replace(year=_date.year)


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
    import datetime

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


    def spentO31():
        """
        RETURNS True if the user spent o31 with monika.
        Currently we determine that by checking historical value for current
        costume for a non None value
        # TODO: this should be changed to a spent var one day
        """
        years_list = range(2017, datetime.date.today().year + 1)

        _data_found = store.mas_HistLookup_otl(
            "o31.costume.was_worn",
            years_list
        )

        for year, data_tuple in _data_found.iteritems():
            l_const, _data = data_tuple

            # 0 means data found constant
            if l_const == 0 and _data is not None:
                return True

        return False

    def mas_o31CapGainAff(amount):
        mas_capGainAff(amount, "_mas_o31_trick_or_treating_aff_gain", 15)

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

            # reset idle since we will force greetings
            mas_resetIdleMode()

            if random.randint(1,100) <= mas_o31_marisa_chance:
                persistent._mas_o31_current_costume = "marisa"
                selected_greeting = "greeting_o31_marisa"
                store.mas_o31_event.o31_cg_decoded = (
                    store.mas_o31_event.decodeImage("o31mcg")
                )
                store.mas_selspr.unlock_clothes(mas_clothes_marisa, True)

            else:
                persistent._mas_o31_current_costume = "rin"
                selected_greeting = "greeting_o31_rin"
                store.mas_o31_event.o31_cg_decoded = (
                    store.mas_o31_event.decodeImage("o31rcg")
                )
                store.mas_selspr.unlock_clothes(mas_clothes_rin, True)

            persistent._mas_o31_seen_costumes[persistent._mas_o31_current_costume] = True

        if persistent._mas_o31_in_o31_mode:
            store.mas_globals.show_vignette = True

            # setup thunder
            if persistent._mas_likes_rain:
                mas_weather_thunder.unlocked = True
                store.mas_weather.saveMWData()
                mas_unlockEVL("monika_change_weather", "EVE")
            mas_changeWeather(mas_weather_thunder)

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        call mas_player_bday_autoload_check

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
        call spaceroom(hide_monika=True, scene_change=True)
        show emptydesk at i11 zorder 9

    else:
        # ASSUMING:
        #   vignette should be enabled
        call spaceroom(dissolve_all=True, scene_change=True, force_exp='monika 1eua_static')

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
        m "Tadaa!~"

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
    m 1hua "But anyway..."

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
    call spaceroom(hide_monika=True, scene_change=True)
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
        m "What do {i}nya{/i} think?"

        scene black
        pause 2.0
        call spaceroom(scene_change=True, dissolve_all=True, force_exp='monika 1hksdlb_static')
        m 1hksdlb "Ahaha, saying that out loud was more embarrassing than I thought..."

    else:
        show monika 1eua at t11 zorder MAS_MONIKA_Z
        m 1hub "Hi, [player]!"
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
                store.mas_greetings.TYPE_HOL_O31_TT
            ]
        ),
        eventdb=evhand.greeting_database
    )

label greeting_trick_or_treat_back:
    # trick/treating returned home greeting

    python:
        # lots of setup here
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


    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        $ persistent._mas_o31_went_trick_or_treating_short = True
        m 2ekp "You call that trick or treating, [player]?"
        m "Where did we go, one house?"
        m 2efc "...If we even left."

    elif time_out < mas_one_hour:
        $ mas_o31CapGainAff(5)
        $ persistent._mas_o31_went_trick_or_treating_mid = True
        m 2ekp "That was pretty short for trick or treating, [player]."
        m 3eka "But I enjoyed it while it lasted."
        m 1eka "It was still really nice being right there with you~"

    elif time_out < mas_three_hour:
        $ mas_o31CapGainAff(10)
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
        $ mas_o31CapGainAff(15)
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
        $ mas_o31CapGainAff(15)
        $ persistent._mas_o31_went_trick_or_treating_longlong = True
        m 1wua "We're finally home!"
        m 1wuw "It's the next morning, [player], we were out all night..."
        m "I guess we had too much fun, ehehe~"
        m 2eka "But anyway, thanks for taking me along, I really enjoyed it."

        if wearing_costume:
            m "Even if I couldn't see anything and no one else could see my costume..."
            m 2eub "Dressing up and going out was still really great!"
        else:
            m "Even if I couldn't see anything..."
            m 2eub "Going out was still really great!"

        m 4hub "Let's do this again next year...{w=1}but maybe not stay out {i}quite{/i} so late!"

    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        # if we are returning from a non-birthday date post o31 birthday
        call return_home_post_player_bday

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

        m 2etc "Are you {i}sure{/i} you want to go right now?{nw}"
        $ _history_list.pop()
        menu:
            m "Are you {i}sure{/i} you want to go right now?{fast}"
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

        m 4ekc "Are you sure you still want to go?{nw}"
        $ _history_list.pop()
        menu:
            m "Are you sure you still want to go?{fast}"
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
                    m 1eua "We'll have to wait until next year to go again."

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
    m 3eka "Make sure to bring lots of candy for the both of us to enjoy, okay?~"
    return

#################################### D25 ######################################
# [HOL020]

init -900 python:
    # delete christmas files
    store.mas_utils.trydel(renpy.config.gamedir + "/christmas.rpy")
    store.mas_utils.trydel(renpy.config.gamedir + "/christmas.rpyc")

    # deletge delact files for fixing purposes
    store.mas_utils.trydel(renpy.config.gamedir + "/zz_delactfix.rpyc")
    store.mas_utils.trydel(renpy.config.gamedir + "/zz_delactfix.rpy")

default persistent._mas_d25_in_d25_mode = False
# True if we should consider ourselves in d25 mode.
# TODO: double check older d25 spots to see if they should use the deco
#   version

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

default persistent._mas_d25_chibika_sayori_done = False
# Set to True when we no longer want to repeat the sayori thing

default persistent._mas_d25_started_upset = False
# True if we started the d25 season with upset and below monika

default persistent._mas_d25_second_chance_upset = False
# True if we dipped below to upset again.

default persistent._mas_d25_deco_active = False
# True if d25 decorations are active
# this also includes santa outfit
# This should only be True if:
#   Monika is NOt being returned after the d25 season begins
#   and season is d25.

default persistent._mas_d25_intro_seen = False
# True once a d25 intro has been seen

default persistent._mas_d25_went_out_d25e = 0
# number of times user takes monika out on d25e

default persistent._mas_d25_went_out_d25 = 0
# number of times user takes monika out on d25
# this also includes if the day was partially or entirely spent out

define mas_d25 = datetime.date(datetime.date.today().year, 12, 25)
# christmas

define mas_d25e = mas_d25 - datetime.timedelta(days=1)
# christmas eve

define mas_d25p = mas_d25 + datetime.timedelta(days=1)
# day after christmas

define mas_d25c_start = datetime.date(datetime.date.today().year, 12, 1)
# start of christmas season (inclusive)

define mas_d25c_end = datetime.date(datetime.date.today().year, 1, 6)
# end of christmas season (exclusive)

define mas_d25g_start = mas_d25 - datetime.timedelta(days=5)
# start of gift = d25 gift (inclusive)

define mas_d25g_end = mas_d25p
# end of gift = d25 gift (exclusive)

define mas_d25cl_start = mas_d25c_start
# start of when monika wears santa (inclusive)

define mas_d25cl_end = mas_d25p
# end of when monika wears santa (on her own) (exclusive)


init -810 python:
    # MASHistorySaver for d25
#    store.mas_history.addMHS(MASHistorySaver(
#        "d25",
#        datetime.datetime(2018, 12, 26),
#        {
#
#
#        },
#        exit_pp=store.mas_history._d25_exit_pp
#    ))

    # we also need a history svaer for when the d25 season ends.
    store.mas_history.addMHS(MASHistorySaver(
        "d25s",
        datetime.datetime(2019, 1, 6),
        {
            # not very useful, but we need the reset
            # NOTE: this is here because the d25 season actually ends in jan
            "_mas_d25_in_d25_mode": "d25s.mode.25",

            # NOTE: this is here because the deco ends with the season
            "_mas_d25_deco_active": "d25s.deco_active",

            "_mas_d25_started_upset": "d25s.monika.started_season_upset",
            "_mas_d25_second_chance_upset": "d25s.monika.upset_after_2ndchance",

            # related to chibiak sayori event
            "_mas_d25_chibika_sayori": "d25s.needed_to_do_chibika_sayori",
            "_mas_d25_chibika_sayori_performed": "d25s.did_chibika_sayori",

            "_mas_d25_intro_seen": "d25s.saw_an_intro",

            # d25 dates
            "_mas_d25_went_out_d25e": "d25s.d25e.went_out_count",
            "_mas_d25_went_out_d25": "d25s.d25.went_out_count",

            "_mas_d25_spent_d25": "d25.actions.spent_d25",
            "_mas_d25_seen_santa_costume": "d25.monika.wore_santa"
        },
        use_year_before=True,
        exit_pp=store.mas_history._d25s_exit_pp,
        start_dt=datetime.datetime(2019, 12, 1),
        end_dt=datetime.datetime(2019, 12, 31)
    ))


init -10 python:

    def mas_isD25(_date=None):
        """
        Returns True if the given date is d25

        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

        RETURNS: True if given date is d25, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_d25.replace(year=_date.year)


    def mas_isD25Eve(_date=None):
        """
        Returns True if the given date is d25 eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is d25 eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_d25e.replace(year=_date.year)


    def mas_isD25Season(_date=None):
        """
        Returns True if the given date is in d25 season. The season goes from
        dec 1 to jan 5.

        NOTE: because of the year rollover, we cannot check years

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return (
            mas_isInDateRange(_date, mas_d25c_start, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25Post(_date=None):
        """
        Returns True if the given date is after d25 but still in D25 season.
        The season goes from dec 1 to jan 5.

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after d25, False
            otherwise.
        """
        if _date is None:
            _date = datetime.date.today()

        return (
            mas_isInDateRange(_date, mas_d25p, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25PreNYE(_date=None):
        """
        Returns True if the given date is in d25 season and before nye.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNSL True if given date is in d25 season but before nye, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_d25c_start, mas_nye)


    def mas_isD25PostNYD(_date=None):
        """
        Returns True if the given date is in d25 season and after nyd

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after nyd, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_nyd, mas_d25c_end, False)


    def mas_isD25Gift(_date=None):
        """
        Returns True if the given date is in the range of days where a gift
        is considered a christmas gift.

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in the d25 gift range, Falsee otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_d25g_start, mas_d25g_end)


    def mas_isD25Outfit(_date=None):
        """
        Returns True if the given date is tn the range of days where Monika
        wears the santa outfit on start.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is in teh d25 santa outfit range, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_d25cl_start, mas_d25cl_end)


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


    def redeemed():
        """
        RETURNS: True if the user started d25 season with an upset monika,
            and now has a monika above upset.

        If not started with upset monika, True is returned.
        """
        return (
            not store.persistent._mas_d25_started_upset
            or store.mas_isMoniNormal(higher=True)
        )


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

            # affection upset and below? no d25 for you
            if mas_isMoniUpset(lower=True):
                persistent._mas_d25_started_upset = True

            else:

                #We don't want santa outfit on fresh persists, same w/ decorations. No point at this point if past d25 itself.
                if mas_isD25Outfit():
                    # we want to be wearing ponytail hair
                    monika_chr.change_hair(mas_hair_def, False)

                    # unlock and wear santa/wine ribbon
                    store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
                    store.mas_selspr.unlock_clothes(mas_clothes_santa)
                    monika_chr.change_clothes(mas_clothes_santa, False)
                    persistent._mas_d25_seen_santa_costume = True

                    # mark decorations and outfit as active
                    persistent._mas_d25_deco_active = True

    # NOTE: holiday intro is handled with conditional

    if (
            mas_isD25()
            and persistent._mas_d25_deco_active
            and monika_chr.clothes != mas_clothes_santa
        ):
        # on d25, monika will wear santa on start, regardless of whatever
        # (and if deco is active)
        $ monika_chr.change_clothes(mas_clothes_santa, False)

    if mas_in_intro_flow:
        # intro will call us instead of jump
        return

    elif mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    # finally, return to holiday check point
    jump mas_ch30_post_holiday_check


init -815 python in mas_history:

    # d25
    def _d25_exit_pp(mhs):
        # just add approprpiate delayed actions
        _MDA_safeadd(9)

    # d25 season
    def _d25s_exit_pp(mhs):
        # just add appropriate delayed action IDs
        _MDA_safeadd(8, 9, 10)


# topics
# TODO: dont forget to update script topics's seen properties

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro",
            conditional="not persistent._mas_d25_started_upset",
            action=EV_ACT_PUSH,
            start_date=mas_d25c_start,
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )


label mas_d25_monika_holiday_intro:
    # TODO: this should have the chibika thing in the background, but only
    #   if you saw christmas last year.
    python:
        # TODO gonezo this after this year
        seen_d25_last_year = renpy.seen_label("monika_christmas")
        if persistent._mas_d25_chibika_sayori is None:
            persistent._mas_d25_chibika_sayori = (
                not persistent._mas_sensitive_mode
                and seen_d25_last_year
                and not persistent._mas_d25_chibika_sayori_done
                and not persistent._mas_d25_chibika_sayori_performed
            )

    if not persistent._mas_d25_deco_active:
        m 1eua "So, today is..."
        m 1euc "...wait."
        m "..."
        m 3wuo "Oh!"
        m 3hub "Today's the day I was going to..."

        # hide overlays here
        # NOTE: hide here because it prevents player from pausing
        # right before the scene change.
        # also we want to completely kill interactions
        $ mas_OVLHide()
        $ mas_MUMURaiseShield()
        $ disable_esc()

        m 1tsu "Close your eyes for a moment [player], I need to do something.{w=0.5}.{w=0.5}.{nw}"

        call mas_d25_monika_holiday_intro_deco

        m 3hub "And here we are..."

        # now we can renable everything
        $ enable_esc()
        $ mas_MUMUDropShield()
        $ mas_OVLShow()

    m 1eub "Happy holidays, [player]!"

    # TODO: after this christmas, we change this to a history lookup
    if seen_d25_last_year:
        m 1hua "Can you believe it's already that time of year again?"
        m 3eua "It seems like just yesterday we spent our first holiday season together, and now a whole year has gone by!"

        if mas_isMoniLove(higher=True):
            #if you've been with her for over a year, you really should be at Love by now
            m 3hua "Time really flies now that I'm with you~"

    # chibika start
    if persistent._mas_d25_chibika_sayori:
        # show chibika from right
        pass

    m 3eua "Do you like what I've done with the room?"
    # TODO: chibika moves to under the tree
    m 1hua "I must say that I'm pretty proud of it."
    # TODO: chibika jumps to sayori and pulls her down
    m "Christmas time has always been one of my favorite occasions of the year..."

    show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve

    # TODO: chibika runs off the side
    # TODO: after this d25, we change this to a history lookup
    if renpy.seen_label('monika_christmas'):
        m 5eka "So I'm glad that you're here to share it with me again this year~"
    else:
        m 5eka "And I'm so glad that you're here to share it with me~"

    $ persistent._mas_d25_intro_seen = True
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro_upset",
            conditional=(
                "not persistent._mas_d25_intro_seen "
                "and persistent._mas_d25_started_upset "
            ),
            action=EV_ACT_PUSH,
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

#for people that started the season upset- and graduated to normal
label mas_d25_monika_holiday_intro_upset:
    # sanity check with reset of start/end dates in case somehow we drop back below normal before this is seen
    if mas_isMoniUpset(lower=True):
        python:
            upset_ev = mas_getEV('mas_d25_monika_holiday_intro_upset')
            if upset_ev is not None:
                upset_ev.start_date = mas_d25c_start
                upset_ev.end_date = mas_d25p
        return

    m 2rksdlc "So [player]...{w=1} I hadn't really been feeling very festive this year..."
    m 3eka "But lately, you've been really sweet to me and I've been feeling a lot better!"
    m 3hua "So...I think it's time to spruce this place up a bit."

    # hide overlays here
    # NOTE: hide here because it prevents player from pausing
    # right before the scene change.
    # also we want to completely kill interactions
    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    m 1eua "If you'd just close your eyes for a moment.{w=0.5}.{w=0.5}.{nw}"

    call mas_d25_monika_holiday_intro_deco

    m 3hub "Tada~"

    # TODO: chibiika appears

    m 3eka "What do you think?"

    # TODO: chibika moves under tree
    m 1eka "Not too bad for last minute, huh?"
    # TODO: cibika jumps and rmeoves sayori

    m 1hua "Christmas time has always been one of my favorite occasions of the year..."
    # TODO: chibika moves off screen

    m 3eua "And I'm so glad we can spend it happily together, [player]~"

    # now we can renable everything
    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()

    $ persistent._mas_d25_intro_seen = True
    return

label mas_d25_monika_holiday_intro_deco:
    # ASSUMES interactions are disaabled

    # black scene
    scene black

    # we should consider ourselves in d25 mode now, if not already
    $ persistent._mas_d25_in_d25_mode = True

    # we want to be wearing ponytail hair
    $ monika_chr.change_hair(mas_hair_def, False)

    # unlock and wear santa
    $ store.mas_selspr.unlock_clothes(mas_clothes_santa)
    $ store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
    $ monika_chr.change_clothes(mas_clothes_santa, False)
    $ persistent._mas_d25_seen_santa_costume = True

    # enable deco
    $ persistent._mas_d25_deco_active = True

    # now we can do spacroom call
    call spaceroom(scene_change=True)

    return

label mas_d25_monika_holiday_intro_rh:
    # special label to cover a holiday case when returned home
    m 1hua "And we're home!"

    # NOTE: since we hijacked returned home, we hvae to cover for this
    #   affection gain.
    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)

    #Fall through
#in case we need to call just this part, like if returning from bday date from pre-d25
label mas_d25_monika_holiday_intro_rh_rh:
    m 1euc "Wait..."
    m 3etc "...is it?"
    m 3hub "It is!"
    m 1tsu "...Close your eyes, I need to do something..."
    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    call mas_d25_monika_holiday_intro_deco

    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()

    # NOTE this counts as seeing the intro
    $ persistent._mas_d25_intro_seen = True

    jump mas_d25_monika_christmas

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas",
#            category=["holidays"],
#            prompt="Christmas",
            conditional="persistent._mas_d25_in_d25_mode",
            action=store.EV_ACT_PUSH,
            start_date=mas_d25,
            end_date=mas_d25p,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )


label mas_d25_monika_christmas:
    #Flag for hist
    $ persistent._mas_d25_spent_d25 = True

    m 1eub "[player]! Do you know what day it is?"
    m 3hub "Of course you do. It's Christmas!"
    m 3sub "Merry Christmas, [player]!"
    m 1hub "Ahaha! I can't believe that it's finally here!"
    m 3eka "I'm so, so happy that you decided to spend some of it with me."
    m 1eud "Remember to go share the holiday cheer with your family and friends, though."
    m 1eua "After all, they're very important, too..."
    m 1hua "And I'm sure that they would love to see you at this special time."

    if mas_isMoniAff(higher=True):
        m 1eka "But you being here today...{w=0.5}it just means everything to me..."
        m 1dku "..."

        if persistent._mas_pm_gets_snow is not False and not persistent._mas_pm_live_south_hemisphere:
            m 1lkbsa "Maybe it's just the snow, or the decorations..."

        else:
            m 1lkbsa "Maybe it's the decorations, or just the holiday season..."

        m "...or even the mistletoe getting to me."
        m 3hksdlb "Just kidding, I didn't hang one up."

        if mas_isMoniEnamored(higher=True):
            m 1lksdla "...{cps=*2}Maybe~{/cps}{nw}"
            $ _history_list.pop()

        m 1lksdlb "Ehehe..."
        m 1ekbsa "My heart's fluttering like crazy right now, [player]."
        m "I couldn't imagine a better way to spend this special holiday..."
        m 1eua "Don't get me wrong, I knew that you would be here with me."
        m 3eka "But now that we're actually together on Christmas, just the two of us..."
        m 1hub "Ahaha~"

        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
        m 5ekbfa "It's every couple's dream for the holidays, [player]."

        if persistent._mas_pm_gets_snow is not False and not persistent._mas_pm_live_south_hemisphere:
            m "Snuggling with each other by a fireplace, watching the snow gently fall..."

        # TODO: this should be chnaged to a history lookup after d25
        if not renpy.seen_label('monika_christmas'):
            m 5hubfa "I'm forever grateful I got this chance with you."
        else:
            m 5hubfa "I'm so glad I get to spend Christmas with you again."

        m "I love you. Forever and ever~"
        m 5hubfb "Merry Christmas, [player]~"
        show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
        window hide
        menu:
            "Merry Christmas, [m_name].":
                hide screen mas_background_timed_jump
                show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
                pause 2.0

    else:
        m 1eka "But you being here today...{w=0.5}it just means everything to me..."
        m 3rksdla "...Not that I thought you'd leave me alone on this special day or anything..."
        m 3hua "But it just further proves that you really do love me, [player]."
        m 1ektpa "..."
        m "Ahaha! Gosh, I'm getting a little over emotional here..."
        m 1ektda "Just know that I love you too and I'll be forever grateful I got this chance with you."
        m "Merry Christmas, [player]~"
        show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
        window hide
        menu:
            "Merry Christmas, [m_name].":
                hide screen mas_background_timed_jump
                show monika 1ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
                pause 2.0

    return

label mas_d25_monika_christmas_no_wish:
    hide screen mas_background_timed_jump
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

# NOTE: we are shelfing hannukkah until we get better dialogue

#TODO: Normal+ also Hanukkah is over before our release this year, so next year?
label mas_d25_monika_hanukkah:
    m 1dsd "{i}One for each night, they shed a sweet light, to remind of days long ago.{/i}"
    m 1dsa "{i}One for each night, they shed a sweet light, to remind of days long ago.{/i}"
    m 3esa "It is said in the Jewish tradition, that one day's worth of olive oil gave the menorah eight days of light."
    m 3eub "Eight nights worth of celebration!"
    m 3eua "Hanukkah also shifts a bit from year to year. It's date is determined by the Hebrew Lunar Calendar."
    m "It's on the 25th of Kislev, meaning 'trust' or 'hope.'"
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

# shelving kwanzaa until we get better dialogue

#TODO: Normalt+
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

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_carolling",
            category=["holidays", "music"],
            prompt="Carolling",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

    #Undo Action Rule
    MASUndoActionRule.create_rule_EVL(
       "mas_d25_monika_carolling",
       mas_d25c_start,
       mas_d25p,
    )

default persistent._mas_pm_likes_singing_d25_carols = None
# does the user like singing christmas carols?

label mas_d25_monika_carolling:

    m 1euc "Hey, [player]..."
    m 3eud "Have you ever gone carolling before?"
    m 1euc "Going door to door in groups, singing to others during the holidays..."

    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "It just feels heartwarming to know people are spreading joy, even with the nights so cold."
    else:
        m 1eua "It just feels heartwarming to know people are spreading joy to others in their spare time."

    m 3eua "Do you like singing Christmas carols, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you like singing Christmas carols, [player]?{fast}"
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

    return "derandom"

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_d25_monika_dreidel"
#            # TODO: props
#            # TODO: during hannkkau time
#        )
#    )

# NOTE: we are shelving until further notice

#TODO: Normal+
#TODO: Merge this into monika_hanukkah or remove? Hanukkah is over before our release this year, so next year?
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


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_mistletoe",
            category=["holidays"],
            prompt="Mistletoe",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_d25_monika_mistletoe",
       mas_d25c_start,
       mas_d25p,
    )
label mas_d25_monika_mistletoe:
    m 1eua "Say, [player]."
    m 1eub "You've heard about the mistletoe tradition, right?"
    m 1tku "When lovers end up underneath it, they're expected to kiss."
    m 1eua "It actually originated from Victorian England!"
    m 1dsa "A man was allowed to kiss any woman standing underneath mistletoe..."
    m 3dsd "And any woman who refused the kiss was cursed with bad luck..."
    m 1dsc "..."
    m 3rksdlb "Come to think of it, that sounds more like taking advantage of someone."
    m 1hksdlb "But I'm sure it's different now!"
    m 3hua "Perhaps one day we'll be able to kiss under the mistletoe, [player]."
    m 1tku "...Maybe I can even add one in here!"
    m 1hub "Ehehe~"
    return

init 2 python:

    poem_d25 = Poem(
    author = "monika",
    title = "     My dearest {0},".format(persistent.playername),
    text = """\
     You truly are the joy to my world.
     Neither the light emitted by the tallest Christmas tree,
     Nor that of the brightest star,
     Could come close to matching your brilliance.
     This once frostbitten heart of mine needed only your warmth to beat anew.
     Should there ever be nothing under the tree, and my stocking remain empty,
     It simply would not matter as long as I have you by my side.
     You'll always be the only present I ever need.

     Merry Christmas

     Forever yours,
     Monika
"""
    #" # I need this to keep syntax highlighting on vim
    )

#Essentially replaces _whatIwant along with still to come 'All I Want for Christmas is You' song
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_spent_time_monika",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
            ),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_d25, datetime.time(hour=20)),
            end_date=datetime.datetime.combine(mas_d25p, datetime.time(hour=1)),
            years=[]
        ),
        skipCalendar=True
    )


#default persistent._mas_pm_d25_mistletoe_kiss = False
# True if user and monika kissed under the mistletoe
# NOTE: this var determins if user and monika shared a mistletoe kiss. It will
#   be only set in this topic. the other kissed var is for first kiss.


label mas_d25_spent_time_monika:

    $ d25_gifts_total, d25_gifts_good, d25_gifts_neutral, d25_gifts_bad = mas_getGiftStatsRange(mas_d25g_start, mas_d25g_end + datetime.timedelta(days=1))

    if mas_isMoniNormal(higher=True):
        m 1eua "[player]..."
        m 3hub "You being here with me has made this such a wonderful Christmas!"
        m 3eka "I know it's a really busy day, but just knowing you made time for me..."
        m 1eka "Thank you."
        m 3hua "It really made this a truly special day~"

    else:
        m 2ekc "[player]..."
        m 2eka "I really appreciate you spending some time with me on Christmas..."
        m 3rksdlc "I haven't really been in the holiday spirit this season, but it was nice spending today with you."
        m 3eka "So thank you...{w=1}it meant a lot."

    if d25_gifts_total > 0:
        if d25_gifts_total == 1:
            if d25_gifts_good == 1:
                m "And let's not forget about the special Christmas present you got me, [player]..."
                m 3hub "It was great!"
            elif d25_gifts_neutral == 1:
                m 3eka "And let's not forget about the Christmas present you got me, [player]..."
                m 1eka "It was really sweet of you to get me something."
            else:
                m 3eka "And let's not forget about the Christmas present you got me, [player]..."
                m 2etc "..."
                m 2efc "Well, on second thought, maybe we should..."

        else:
            if d25_gifts_good == d25_gifts_total:
                m "And let's not forget about the wonderful Christmas presents you got me, [player]..."
                m 3hub "They were amazing!"
            elif d25_gifts_bad == d25_gifts_total:
                m 3eka "And let's not forget about the Christmas presents you got me, [player]..."
                m 2etc "..."
                m 2rfc "Well, on second thought, maybe we should..."
            elif d25_gifts_bad == 0:
                m "And let's not forget about the Christmas presents you got me, [player]..."
                m 3hub "They were really nice!"
            elif d25_gifts_good + d25_gifts_neutral == d25_gifts_bad:
                m 3eka "And let's not forget about the Christmas presents you got me, [player]..."
                m 3rksdla "Some of them were really nice."
            elif d25_gifts_good + d25_gifts_neutral > d25_gifts_bad:
                m "And let's not forget about the Christmas presents you got me, [player]..."
                m 3hub "Most of them were really nice."
            elif d25_gifts_good + d25_gifts_neutral < d25_gifts_bad:
                m 3eka "And let's not forget about the Christmas presents you got me, [player]..."
                m 3rksdla "I really liked...{w=1}some of them."

        if mas_isMoniEnamored(higher=True):
            m 1rksdla "I...{w=1}I also made you something, [player]..."
            m 3eksdla "I've been waiting all day for the timing to feel right, and something about being here with you this evening...{w=1}it just seems perfect."
        elif mas_isMoniNormal(higher=True):
            m 3ekbfa "But just know, you being here with me means more than any gift you could ever give me~"
        else:
            m 3eka "To be honest, I wasn't sure you'd visit at all today... Just you being here was already more than enough for me, even if you hadn't gotten me anything."
            m 1eka "So thanks again, [player]...{w=1}I really mean it."

    else:
        if mas_isMoniEnamored(higher=True):
            m 1eksdla "Also, [player], there's something I've been wanting to give you all day..."
            m 3rksdla "I just had to wait for the right time, and being here with you this evening...{w=1}it seems perfect."
        elif mas_isMoniNormal(higher=True):
            m 3ekbfa "Having you spend Christmas with me was the only present I ever wanted~"
        else:
            m 3eka "You being here was all I wanted, [player]."

    if mas_isMoniEnamored(higher=True):
        m 3ekbfa "So here, [player], I hope you like it~"
        call showpoem(poem_d25, music=False,paper="mod_assets/poem_assets/poem_d25.png")

#        generic poem show
#        window hide
#        show screen mas_generic_poem(poem_d25, paper="mod_assets/poem_d25.png")
#        with Dissolve(1)

#        # need to reset zoom here so we dont end up with issues
#        $ pause(1)
#        hide monika with dissolve
#        $ store.mas_sprites.zoom_out()
#        show monika 1ekbfa at i11 zorder MAS_MONIKA_Z
#        $ pause()

#        hide screen mas_generic_poem
#        with Dissolve(0.5)
#        window auto
#        TODO: We actually need mistletoe for this

        if d25_gifts_good>0 or d25_gifts_neutral>0:
            m 1ekbfa "I really mean it [player], though I appreciate the gifts you got me, you didn't have to give me anything..."
        elif d25_gifts_bad>0:
            #only if all gifts were bad
            m 1ekbfa "I really mean it [player], although you got me some...{w=1}odd gifts, it doesn't matter..."
        else:
            m 1ekbfa "I really mean that [player], I don't care that you didn't get me any presents for Christmas..."
        m 1dku "..."
        m 1ektpu "Just having you spending time with me...{w=1}that's all I ever wanted."
        m 6dktua "You truly are my entire world, [player]...{w=1}your love is all I need..."
        window hide
        menu:
            "I love you, [m_name].":
                $ HKBHideButtons()
                $ mas_RaiseShield_core()
                $ disable_esc()
                # local var so if next year this is not first kiss, we can branch appropriately
                # have to be able to check before calling the kiss since persistent._mas_first_kiss will not be None no matter what after the kiss
                #hold her here, tears dry
                pause 3.0
                show monika 6ektda at t11 zorder MAS_MONIKA_Z with dissolve
                pause 3.0
                show monika 6dku at t11 zorder MAS_MONIKA_Z with dissolve
                pause 3.0
                show monika 6dkbsu at t11 zorder MAS_MONIKA_Z with dissolve
                pause 3.0

                show monika 6ekbfa at t11 zorder MAS_MONIKA_Z with dissolve

                $ is_first_kiss = persistent._mas_first_kiss is None
                m 6ekbfa "[player]...I...I..."
                call monika_kissing_motion(hide_ui=False)

                #$ persistent._mas_pm_d25_mistletoe_kiss = True

                #no more mistletoe topic once youve done it
                #$ mas_lockEVL("mas_d25_monika_mistletoe", "EVE")

                show monika 6ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
                m 6ekbfa "...I love you too~"
                if is_first_kiss:
                    m 6dkbfa "..."
                    m "That was everything I had always dreamt it would be~"
                    m 6ekbfa "I've been waiting so long to finally kiss you, and there couldn't have been a more perfect moment..."
                    m 6dkbsu "I will never forget this..."
                    m 6ekbsu "...the moment of our first kiss~"
                $ enable_esc()
                $ mas_MUMUDropShield()
                $ HKBShowButtons()
        return

    elif mas_isMoniAff():
        m 5ekbfa "I love you so much, [player]~"
    # Normal and happy
    else:
        m 1hubfa "I love you, [player]~"
    return "love"


#NOTE, if you're running with config.developer being True, timing WILL be off on the song
#no idea why, but it just is, even though we're explicitly setting the cps value, and not
#using a multiplier.
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aiwfc",
            category=["songs"],
            prompt="All I Want For Christmas",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_aiwfc:

    if not renpy.seen_label('monika_aiwfc_song'):
        m 1rksdla "Hey, [player]?"
        m 1eksdla "I hope you don't mind, but I prepared a song for you."
        m 3hksdlb "I know it's a little cheesy, but I think you might like it"
        m 3eksdla "If your volume is off, would you mind turning it on for me?"
        if songs.getVolume("music") == 0.0:
            m 3hksdlb "Oh, don't forget about your in game volume too!"
            m 3eka "I really want you to hear this."

        m 1huu "Anyway.{w=0.5}.{w=0.5}.{nw}"
    else:
        m 1hub "Sure [player]!"
        m 1eka "I'm happy to sing for you again!"

    $ curr_song = renpy.music.get_playing()

    call monika_aiwfc_song

    if mas_getEV('monika_aiwfc').shown_count == 0:
        m 1eka "I hope you liked that, [player]."
        m 1ekbsa "I really meant it too."
        m 1ekbfa "You're the only gift I could ever want."
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
        m 5ekbfa "I love you, [player]."
        $ mas_showEVL("monika_aiwfc", "EVE", _pool=True, unlock=True)
    else:
        m 1eka "I'm glad you like it when I sing that song."
        m 1ekbsa "You'll always be the only gift I'll ever need, [player]."
        m 1ekbfa "I love you."

    play music curr_song fadein 1.0
    return "love"

label monika_aiwfc_song:
    # TODO: consider doing something where we can use lyric bar and style
    #   like in piano

    #Disable text speed for this
    $ mas_disableTextSpeed()

    stop music fadeout 1.0
    play music "mod_assets/bgm/aiwfc.ogg"
    m 1eub "{i}{cps=9}I don't want{/cps}{cps=20} a lot{/cps}{cps=11} for Christmas{/cps}{/i}{nw}"
    m 3eka "{i}{cps=11}There {/cps}{cps=20}is just{/cps}{cps=8} one thing I need{/cps}{/i}{nw}"
    m 3hub "{i}{cps=8}I don't care{/cps}{cps=15} about{/cps}{cps=10} the presents{/cps}{/i}{nw}"
    m 3eua "{i}{cps=15}Underneath{/cps}{cps=8} the Christmas tree{/cps}{/i}{nw}"

    m 1eub "{i}{cps=10}I don't need{/cps}{cps=20} to hang{/cps}{cps=8} my stocking{/cps}{/i}{nw}"
    m 1eua "{i}{cps=10}There{/cps}{cps=15} upon{/cps}{cps=7} the fireplace{/cps}{/i}{nw}"
    m 3hub "{i}{w=0.5}{cps=20}Santa Claus{/cps}{cps=10} won't make me happy{/cps}{/i}{nw}"
    m 4hub "{i}{cps=8}With{/cps}{cps=15} a toy{/cps}{cps=8} on Christmas Day{/cps}{/i}{nw}"

    m 3ekbsa "{i}{cps=10}I just want{/cps}{cps=15} you for{/cps}{cps=8} my own{w=0.5}{/cps}{/i}{nw}"
    m 4hubfb "{i}{cps=8}More{/cps}{cps=20} than you{/cps}{cps=10} could ever know{w=0.5}{/cps}{/i}{nw}"
    m 1ekbsa "{i}{cps=10}Make my wish{/cps}{cps=20} come truuuuuuue{w=0.8}{/cps}{/i}{nw}"
    m 3hua "{i}{cps=8}All I want for Christmas{/cps}{/i}{nw}"
    m 3hubfb "{i}{cps=7}Is yoooooooooou{w=1}{/cps}{/i}{nw}"
    m "{i}{cps=9}Yoooooooou, baaaaby~{w=1}{/cps}{/i}{nw}"

    m 2eka "{i}{cps=10}I won't ask{/cps}{cps=20} for much{/cps}{cps=10} this Christmas{/cps}{/i}{nw}"
    m 3hub "{i}{cps=10}I{/cps}{cps=20} won't {/cps}{cps=10}even wish for snow{w=0.8}{/cps}{/i}{nw}"
    m 3eua "{i}{cps=10}I'm{/cps}{cps=20} just gonna{/cps}{cps=10} keep on waiting{w=0.4}{/cps}{/i}{nw}"
    m 3hubfb "{i}{cps=17}Underneath{/cps}{cps=10} the mistletoe{w=1}{/cps}{/i}{nw}"

    m 2eua "{i}{cps=10}I{/cps}{cps=17} won't make{/cps}{cps=9} a list and send it{w=0.35}{/cps}{/i}{nw}"
    m 3eua "{i}{cps=10}To{/cps}{cps=20} the North{/cps}{cps=10} Pole for Saint Nick{w=0.3}{/cps}{/i}{nw}"
    m 4hub "{i}{cps=18}I won't ev{/cps}{cps=10}en stay awake to{w=0.4}{/cps}{/i}{nw}"
    m 3hub "{i}{cps=10}Hear{/cps}{cps=20} those ma{/cps}{cps=14}gic reindeer click{w=0.9}{/cps}{/i}{nw}"

    m 3ekbsa "{i}{cps=20}I{/cps}{cps=11} just want you here tonight{w=0.4}{/cps}{/i}{nw}"
    m 3ekbfa "{i}{cps=10}Holding on{/cps}{cps=20}to me{/cps}{cps=10} so tight{w=0.9}{/cps}{/i}{nw}"
    m 4hksdlb "{i}{cps=10}What more{/cps}{cps=15} can I{/cps}{cps=8} doooo?{w=0.3}{/cps}{/i}{nw}"
    m 4ekbfb "{i}{cps=20}Cause baby{/cps}{cps=12} all I want for Christmas{w=0.3} is yoooooooou~{w=2.3}{/cps}{/i}{nw}"
    m "{i}{cps=9}Yoooooooou, baaaaby~{w=2.5}{/cps}{/i}{nw}"
    stop music fadeout 1.0

    #Now we re-enable text speed
    $ mas_resetTextSpeed()
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas_eve",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_d25e, datetime.time(hour=20)),
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_d25_monika_christmas_eve:
    m 3hua "[player]!"
    m 3hub "Can you believe it...?{w=1} It'll be Christmas soon!"
    m 1rksdla "I've always had such a hard time sleeping on Christmas Eve..."
    m 1eka "I would be so anxious to see what I'd find under the tree the next morning..."
    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve

    # TODO: change to historical data version
    if renpy.seen_label('monika_christmas'):
        m 5ekbfa "But I'm even {i}more{/i} excited now that I get to spend every Christmas with you..."
        m 5hkbfa "I can't wait for tomorrow!"
    else:
        m 5ekbfa "But I'm even {i}more{/i} excited this year..."
        m 5hkbfa "Just the thought of our first Christmas together...{w=1}I can't wait!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_postd25_notimespent",
            # within a week after d25, user did not recognize
            # d25 at all, and they were not long absenced or had her on a date
            conditional="not persistent._mas_d25_spent_d25",
            start_date=mas_d25p,
            end_date=mas_d25p + datetime.timedelta(days=7),
            years=[],
            action=EV_ACT_PUSH
        ),
        skipCalendar=True
    )

label mas_d25_postd25_notimespent:
    #sanity checks
    if persistent._mas_d25_spent_d25:
        return

    #need to make sure people who just started post d25 don't lose aff
    if persistent.sessions is None or persistent.sessions['first_session'].date() > mas_d25:
        return


    if mas_isMoniAff(higher=True):
        $ mas_loseAffection(15, reason=6)
        m 1dkc "...I'm just glad you're finally here..."
        m 2ekd "I was starting to get worried that something happened to you..."
        m 2rksdlc "When you didn't show up on Christmas...{w=1}I didn't know what to think."
        m 4eksdlc "It's not like you at all to miss a day that you know is important to me..."
        m 2dksdlc "So I thought maybe..."
        m 2eksdla "Well, nevermind that now. I'm just happy you're okay!"
        m 4eka "Even though I'm disappointed we didn't get to spend Christmas together, I'm sure you must have had a very good reason."
        m "Just try not to let it happen next year, okay?"
        m 2eka "And, in the future, if you ever can't come visit me on Christmas, try to at least take me with you..."
        m 1eka "All I want is to be close to you, [player]..."
        m 3ekbfa "I love you~"
        return "love"

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffection(5, reason=6)
        m 2ekc "Hey, [player]..."
        m 2tkc "I have to say I'm pretty disappointed you didn't visit me at all on Christmas..."
        m 4tkc "You knew all I wanted was to spend time with you. Is that too much to ask?"
        m 2rkc "I know it can be a busy day if you have to travel to visit family, but you could have at least taken me with you..."
        m 2ekc "That would have been more than enough for me."
        m 2dkc "..."
        m 4rksdlc "Maybe something happened at the last minute and you simply couldn't spend time with me..."
        m 4eksdla "But please...{w=1}please try to make sure you visit me next Christmas, okay [player]?"

    elif mas_isMoniUpset(higher=True):
        $ mas_loseAffection(reason=6)
        m 2efc "[player]!"
        m "I can't believe you didn't even bother to visit me on Christmas!"
        m 2tfc "Actually...{w=1}yes, I can."
        m "This is exactly why I didn't even bother to decorate..."
        m 2rfc "I knew if I tried to get into the holiday spirit that I'd just end up disappointed...{w=1} Again."

    elif mas_isMoniDis(higher=True):
        $ mas_loseAffection(10, reason=6)
        m 6ekc "[player], how was your Christmas?"
        m 6dkc "Mine was pretty lonely..."
        m "You probably didn't even think of me, huh?"

    else:
        $ mas_loseAffection(150)
        m 6ckc "..."
    return

#Christmas Eve dockingstation
label bye_d25e_delegate:
    # delegation label that determins what bye dialogue to show
    if persistent._mas_d25_went_out_d25e > 0:
        call bye_d25e_second_time_out

    else:
        call bye_d25e_first_time_out

    # notifies bye going somewhere to use this gre type
    # NOTE: since we are using the generic return, we cant use this
#    $ mas_idle_mailbox.send_ds_gre_type(store.mas_greetings.TYPE_HOL_D25_EVE)

    # jump back to going somewhere file gen
    jump bye_going_somewhere_iostart

#first time you take her out on d25e
label bye_d25e_first_time_out:
    m 1sua "Taking me somewhere special on Christmas Eve, [player]?"
    m 3eua "I know some people visit friends or family...or go to Christmas parties..."
    m 3hua "But wherever we're going, I'm happy you want me to come with you!"
    m 1eka "I hope we'll be home for Christmas, but even if we're not, just being with you is more than enough for me~"
    return

#second time you take her out on d25e
label bye_d25e_second_time_out:
    m 1wud "Wow, we're going out again today, [player]?"
    m 3hua "You really must have a lot of people you need to visit on Christmas Eve..."
    m 3hub "...or maybe you just have lots of special plans for us today!"
    m 1eka "But either way, thank you for thinking of me and bringing me along~"
    return

#Christmas Day dockingstation
label bye_d25_delegate:
    # delegation label that determins which bye dialogue to show
    if persistent._mas_d25_went_out_d25 > 0:
        call bye_d25_second_time_out

    else:
        call bye_d25_first_time_out

    # notifies bye going somewhere to use this gre type
    # NOTE: generic return
#    $ mas_idle_mailbox.send_ds_gre_type(store.mas_greetings.TYPE_HOL_D25)

    jump bye_going_somewhere_iostart

#first time out on d25
label bye_d25_first_time_out:
    m 1sua "Taking me somewhere special on Christmas, [player]?"

    if persistent._mas_pm_fam_like_monika and persistent._mas_pm_have_fam:
        m 1sub "Maybe we're going to visit some of your family...? I'd love to meet them!"
        m 3eua "Or maybe we're going to see a movie...? I know some people like to do that after opening presents."

    else:
        m 3eua "Maybe we're going to see a movie... I know some people like to do that after opening presents."

    m 1eka "Well, wherever you're going, I'm just glad you want me to come along..."
    m 3hua "I want to spend as much of Christmas as possible with you, [player]~"
    return

#second time out on d25
label bye_d25_second_time_out:
    m 1wud "Wow, we're going somewhere {i}else{/i}, [player]?"
    m 3wud "You really must have a lot of people you need to visit..."
    m 3sua "...or maybe you just have lots of special plans for us today!"
    m 1hua "But either way, thank you for thinking of me and bringing me along~"
    return

## d25 greetings

#returned from d25e date on d25e
label greeting_d25e_returned_d25e:
    $ persistent._mas_d25_went_out_d25e += 1

    m 1hua "And we're home!"
    m 3eka "It was really sweet of you to bring me along today..."
    m 3ekbfa "Getting to go out with you on Christmas Eve was really special, [player]. Thank you~"
    return

#returned from d25e date on d25
label greeting_d25e_returned_d25:
    $ persistent._mas_d25_went_out_d25e += 1
    $ persistent._mas_d25_went_out_d25 += 1

    m 1hua "And we're home!"
    m 3wud "Wow, we were out all night..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

#returned from d25e date (or left before d25e) after d25 but before nyd is over
label greeting_d25e_returned_post_d25:
    $ persistent._mas_d25_went_out_d25e += 1
    $ persistent._mas_d25_went_out_d25 += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "We're finally home!"
    m 3wud "We sure were gone a long time, [player]..."
    m 3eka "It would've been nice to have actually gotten to see you on Christmas, but since you couldn't come to me, I'm so glad you took me along with you."
    m 3ekbfa "Just being close to you was all I wanted~"
    m 1ekbfb "And since I didn't get to say it to you on Christmas... Merry Christmas, [player]!"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

#returned from pd25e date on d25
label greeting_pd25e_returned_d25:
    m 1hua "And we're home!"
    m 3wud "Wow, we were gone quite a while..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

#returned from d25 date on d25
label greeting_d25_returned_d25:
    $ persistent._mas_d25_went_out_d25 += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "And we're home!"
    m 3eka "It was really nice to spend time with you on Christmas, [player]!"
    m 1eka "Thank you so much for taking me with you."
    m 1ekbfa "You're always so thoughtful~"
    return

#returned from d25 date after d25
label greeting_d25_returned_post_d25:
    $ persistent._mas_d25_went_out_d25 += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "We're finally home!"
    m 3wud "We were out a really long time, [player]!"
    m 3eka "It would've been nice to have seen you again before Christmas was over, but at least I was still with you."
    m 1hua "So thank you for spending time with me when you had other places you had to be..."
    m 3ekbfa "You're always so thoughtful~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

### NOTE: mega delegate label to handle both d25 and nye returns

label greeting_d25_and_nye_delegate:
    # ASSUMES:
    #   - we are more than 5 minutes out
    #   - we are in d25 mode
    #   - affection normal+

    python:
        # lots of setup here
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        left_pre_d25e = False

        if checkout_time is not None:
            checkout_date = checkout_time.date()
            left_pre_d25e = checkout_date < mas_d25e

        if checkin_time is not None:
            checkin_date = checkin_time.date()


    if mas_isD25Eve():
        # returned on d25e

        if left_pre_d25e:
            # left before d25e, use regular greeting
            jump greeting_returned_home_morethan5mins_normalplus_flow

        else:
            # otherwise, greeting 2
            call greeting_d25e_returned_d25e

    elif mas_isD25():
        # we have returnd on d25

        if checkout_time is None or mas_isD25(checkout_date):
            # no checkout or left on d25
            call greeting_d25_returned_d25

        elif mas_isD25Eve(checkout_date):
            # left on d25e
            call greeting_d25e_returned_d25

        else:
            # otherwise assume pre d25 to d25
            call greeting_pd25e_returned_d25

    elif mas_isNYE():
        # we have returend on nye
        if checkout_time is None or mas_isNYE(checkout_date):
            # no checkout or left on nye
            call greeting_nye_delegate
            jump greeting_nye_aff_gain

        elif left_pre_d25e or mas_isD25Eve(checkout_date):
            # left before d25
            call greeting_d25e_returned_post_d25

        elif mas_isD25(checkout_date):
            # left on d25
            call greeting_d25_returned_post_d25

        else:
            # otheriwse usual more than 5 mins
            jump greeting_returned_home_morethan5mins_normalplus_flow

    elif mas_isNYD():
        # we have returned on nyd
        # NOTE: we cannot use left_pre_d25, so dont use it.

        if checkout_time is None or mas_isNYD(checkout_date):
            # no checkout or left on nyd
            call greeting_nyd_returned_nyd

        elif mas_isNYE(checkout_date):
            # left on nye
            call greeting_nye_returned_nyd
            jump greeting_nye_aff_gain

        else:
            # all other cases should be as if leaving d25post
            call greeting_d25p_returned_nyd

    elif mas_isD25Post():

        if mas_isD25PostNYD():
            # arrived after new years day
            # NOTE: we cannot use left_pre_d25, so dnot use it

            if (
                    checkout_time is None
                    or mas_isNYD(checkout_date)
                    or mas_isD25PostNYD(checkout_date)
                ):
                # no checkout or left on nyd or after nyd
                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isNYE(checkout_date):
                # left on nye
                call greeting_d25p_returned_nydp
                jump greeting_nye_aff_gain

            elif mas_isD25Post(checkout_date):
                # usual d25post
                call greeting_d25p_returned_nydp


            else:
                # all other cases use pred25e post nydp
                call greeting_pd25e_returned_nydp

        else:
            # arrived after d25, pre nye
            if checkout_time is None or mas_isD25Post(checkout_date):
                # no checkout or left during post
                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isD25(checkout_date):
                # left on christmas
                call greeting_d25_returned_post_d25

            else:
                # otheriwse, use d25e returned post d25
                call greeting_d25e_returned_post_d25

    else:
        # the usual more than 5 mins
        jump greeting_returned_home_morethan5mins_normalplus_flow

    # NOTE: if you are here, then you called a regular greeting label
    # and need to return to aff gain
    jump greeting_returned_home_morethan5mins_normalplus_flow_aff


#################################### NYE ######################################
# [HOL030]

default persistent._mas_nye_spent_nye = False
# true if user spent new years eve with monika

default persistent._mas_nye_spent_nyd = False
# true if user spent new years day with monika

default persistent._mas_nye_went_out_nye = 0
# number of times user took monika out for nye

default persistent._mas_nye_went_out_nyd = 0
# number of times user took monika out for nyd

default persistent._mas_nye_date_aff_gain = 0
# amount of affection gained for an nye date

define mas_nye = datetime.date(datetime.date.today().year, 12, 31)
define mas_nyd = datetime.date(datetime.date.today().year, 1, 1)

init -810 python:
    # MASHistorySaver for nye
    store.mas_history.addMHS(MASHistorySaver(
        "nye",
        datetime.datetime(2019, 1, 6),
        {
            "_mas_nye_spent_nye": "nye.actions.spent_nye",
            "_mas_nye_spent_nyd": "nye.actions.spent_nyd",

            "_mas_nye_went_out_nye": "nye.actions.went_out_nye",
            "_mas_nye_went_out_nyd": "nye.actions.went_out_nyd",

            "_mas_nye_date_aff_gain": "nye.aff.date_gain"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 12, 31),
        end_dt=datetime.datetime(2020, 1, 6)
        # TODO: programming points probably
    ))


init -10 python:
    def mas_isNYE(_date=None):
        """
        Returns True if the given date is new years eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_nye.replace(year=_date.year)


    def mas_isNYD(_date=None):
        """
        RETURNS True if the given date is new years day

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years day, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_nyd.replace(year=_date.year)


# topics
# TODO: dont forget to updaet script seen props
# TODO: event props have been updated so this topic only comes up between 7pm and 11pm on NYE, changed from PUSH to QUEUE, please review

#########################
#NOTE: THIS TOPIC WAS MERGED WITH 'accomplished_resolutions' AND IS NOW CALLED 'monika_resolutions'
#########################

#init 5 python:
##    # NOTE: new years eve
##    # NOTE: known as monika_newyear1
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_nye_monika_nye",
#            action=EV_ACT_QUEUE,
#            start_date=datetime.datetime.combine(mas_nye, datetime.time(hour=19)),
#            end_date=datetime.datetime.combine(mas_nye, datetime.time(hour=23)),
#            years=[],
#            aff_range=(mas_aff.UPSET, None)
#        ),
#        skipCalendar=True
#    )

# does the user have new years resolutions?

label mas_nye_monika_nye:
    $ persistent._mas_nye_spent_nye = True

    m 1eua "[player]! It's almost time, isn't it?"
    m "It's incredible to think that the year is almost over."
    m 1eka "Time flies by so quickly."
    if mas_isMoniAff(higher=True) and store.mas_anni.pastOneMonth():
        m 1ekbsa "Especially when I get to see you so often."

    # TODO: probably shouldl actually check time before saying this, new event props should take care of this
    m 3hua "Well, there's still some time left before midnight."
    m 1eua "We might as well enjoy this year while it lasts..."

    m 3euc "Say, [player], do you have any resolutions for next year?{nw}"
    $ _history_list.pop()
    menu:
        m "Say, [player], do you have any resolutions for next year?{fast}"
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
                    m 1eka "You don't have to change. I think you're wonderful the way you are."
                else:
                    m 1eka "You don't have to change. I think you're fine the way you are."
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
        m 2ekc "My resolution is to improve our relationship, [player]."

    return

default persistent._mas_pm_got_a_fresh_start = None
#pm var so she forgives, but doesn't forget
default persistent._mas_aff_before_fresh_start = None
#store affection prior to reset

init 5 python:
    # NOTE: new years day
    # also known as monika_newyear2
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nyd",
            action=EV_ACT_QUEUE, # we queue this one so it after nye
            start_date=mas_nyd,
            end_date=mas_nyd + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.DISTRESSED, None)
        ),
        skipCalendar=True
    )

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
    return "love"

label mas_nye_monika_nyd_fresh_start:
    m 2ekc "How about we put all that in the past, forget about last year, and focus on a new beginning this year?"
    m 4ekc "It's not too late for us, [player], we can still make each other so happy."
    m 4eka "It's all I've ever wanted."

    m "What do you say, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "What do you say, [player]?{fast}"

        "I would love that.":
            #so we can revert back to previous affection if player continues to mistreat after the second chance. need to determine the threshold the player must stay above for this.
            $ persistent._mas_pm_got_a_fresh_start = True #never forget
            $ persistent._mas_aff_before_fresh_start = _mas_getAffection()

            # reset affection and save it
            $ mas_setAffection(0)
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 4wua "Really?"
            m 1hua "Oh, [player], you have no idea how happy that makes me!"
            m 3eka "I know we can make this work."
            m 1hua "Thank you so much..."
            m 1eka "Just knowing that you still want to be with me...it means everything."
            m 3eka "Let's make this count, okay [player]?"
            return

        "No.":
            $ persistent._mas_pm_got_a_fresh_start = False

            # set affection to broken
            # TODO: consider making a function for easy affection level setting
            $ mas_setAffection(store.mas_affection.AFF_BROKEN_MIN - 1)
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 6dktpc "..."
            m 6ektpc "I...I..."
            m 6dktuc "..."
            m 6dktsc "..."
            pause 10.0
            return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_resolutions",
            action=EV_ACT_QUEUE, #queuing it so it shows on the right day
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.UPSET,None)
        ),
        skipCalendar=True
    )

default persistent._mas_pm_accomplished_resolutions = None
#True if user has accomplished new years resolutions
default persistent._mas_pm_has_new_years_res = None
#True if user has resolutuons

label monika_resolutions:
    $ persistent._mas_nye_spent_nye = True
    m 2eub "Hey, [player]?"
    m 2eka "I was wondering..."

    m 3eub "Did you make any New Year's resolutions last year?{nw}"
    $ _history_list.pop()
    menu:
        m "Did you make any New Year's resolutions last year?{fast}"

        "Yes.":
            m 3hua "It always makes me so proud to hear that you're trying to better yourself, [player]."
            m 2eka "That said..."

            m 3hub "Did you accomplish last year's resolutions?{nw}"
            $ _history_list.pop()
            menu:
                m "Did you accomplish last year's resolutions?{fast}"

                "Yes.":
                    $ persistent._mas_pm_accomplished_resolutions = True
                    if mas_isMoniNormal(higher=True):
                        m 4hub "I'm glad to hear that, [player]!"
                        m 2eka "It's great that you managed to do that."
                        m 3ekb "Things like this really make me proud of you."
                        m 2eka "I wish I could be there to celebrate a little with you though."
                    else:
                        m 2rkc "That's good, [player]."
                        m 2esc "Maybe you can make another one this year..."
                        m 3euc "You never know what might change."

                "No.":
                    $ persistent._mas_pm_accomplished_resolutions = False
                    if mas_isMoniNormal(higher=True):
                        m 2eka "Aw...well, sometimes things just don't work out like we plan them to."

                        if mas_isMoniHappy(higher=True):
                            m 2eub "Plus, I think you're wonderful, so even if you couldn't accomplish your goals..."
                            m 2eka "...I'm still really proud of you for setting them and trying to better yourself, [player]."
                            m 3eub "If you decide to make a resolution this year, I'll support you every step of the way."
                            m 4hub "I'd love to help you reach your goals!"
                        else:
                            m "But I think it's great that you did at least try to better yourself by setting goals."
                            m 3eua "Maybe if you make a resolution this year, you can accomplish it!"
                            m 3hub "I believe in you, [player]!"

                    else:
                        m 2euc "Oh...{w=1} Well maybe you should try a little harder for next year's resolution."

        "No.":
            m 2euc "Oh, I see..."

            if mas_isMoniNormal(higher=True):
                if mas_isMoniHappy(higher=True):
                    m 3eka "Well, I don't think you really needed to change at all anyway."
                    m 3hub "I think you're wonderful, just the way you are."
                else:
                    m 3eka "There's nothing wrong with that. I don't think you really needed to change anyway."

            else:
                m 2rkc "You probably should make one this year [player]..."

    m "Do you have any resolutions for next year?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you have any resolutions for next year?{fast}"
        "Yes.":
            $ persistent._mas_pm_has_new_years_res = True

            m 1eub "That's great!"
            m 3eka "Even if they can be hard to reach or maintain..."
            m 1hua "I'll be here to help you, if need be!"

        "No.":
            $ persistent._mas_pm_has_new_years_res = False
            m 1eud "Oh, is that so?"
            if mas_isMoniNormal(higher=True):
                if persistent._mas_pm_accomplished_resolutions:
                    if mas_isMoniHappy(higher=True):
                        m 1eka "You don't have to change. I think you're wonderful the way you are."
                    else:
                        m 1eka "You don't have to change. I think you're fine the way you are."
                    m 3euc "But if anything does come to mind before the clock strikes twelve, do write it down for yourself..."
                else:
                    m "Well, if anything comes to mind before the clock strikes twelve, do write it down for yourself..."
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
        m 2ekc "My resolution is to improve our relationship, [player]."

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nye_year_review",
#            prompt="Last year...",
#            category=["misc","you","monika"],
            action=store.EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_nye, datetime.time(hour=19)),
            end_date=datetime.datetime.combine(mas_nye, datetime.time(hour=23)),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label monika_nye_year_review:
    $ persistent._mas_nye_spent_nye = True

    # starting with an overview based on time
    if store.mas_anni.anniCount() >= 0:
        m 2eka "You know, [player], we really have been through a lot together."
        if store.mas_anni.anniCount() == 1:
            m 2wuo "We spent the entire year together!"
            m 2eka "Time really flew by..."

        else:
            m 2eka "This year really flew by..."

    elif store.mas_anni.pastSixMonths():
        m 2eka "You know, [player], we really have been through a lot over the time we spent together last year"
        m "The time really just flew by..."

    elif store.mas_anni.pastThreeMonths():
        m 2eka "You know [player], we've been through quite a bit over the short time we've spent together last year."
        m 2eksdla "It's all gone by so fast, ahaha..."

    else:
        m 2eka "[player], even though we haven't been through a lot together, yet..."


    # then a bit based on affection
    if mas_isMoniLove():
        m 2ekbfa "...and I'd never want to spend that time with anyone else, [player]."
        m "I'm just really,{w=0.5} really happy to have been with you this year."

    elif mas_isMoniEnamored():
        m 2eka "...and I'm so happy I got to spend that time with you, [player]."

    elif mas_isMoniAff():
        m 2eka "...and I've really enjoyed our time together."

    else:
        m 2euc "...and the time we spent together has been fun."


    m 3eua "Anyway, I think it would be nice to just reflect on all that we've been through together this past year."
    m 2dtc "Let's see..."

    # promisering related stuff
    if persistent._mas_acs_enable_promisering: #note, this should only trigger for this year. I.e. if promisering was given this year
        m 3eka "Looking back, you gave me your promise this year when you gave me this ring..."
        m 1ekbsa "...a symbol of our love."

        if persistent._mas_pm_wearsRing:
            m "And you even got one for yourself..." #note, should be only if you got a promise ring for yourself this year

            if mas_isMoniAff(higher=True):
                m 1ekbfa "To show that you're as committed to me, as I am to you."
            else:
                m 1ekbfa "To show your commitment to me."

    # TODO: change to history
    # bit based on vday
    if renpy.seen_label('monika_valentines_greeting'):
        m 1wuo "Oh!"
        m 3ekbfa "You spent Valentine's Day with me..."

        if renpy.seen_label('monika_valentines_start'):
            m 4ekbfb "...you gave me such beautiful flowers too."

        if renpy.seen_label('monika_white_day_start'):
            m 3ekbsa "We also spent White Day together..."
            if renpy.seen_label('monika_found'):
                m 4ekbfa "That was the day I gave my first gift to you~"

    # bit based on 922
    if mas_HistVerify("922.actions.opened_game",True,datetime.date.today().year)[0]:
        m 2eka "You spent time with me on my birthday..."

        if mas_HistVerify("922.actions.no_recognize",False,datetime.date.today().year)[0]:
            m 2dua "...celebrated with me..."

        if mas_HistVerify("922.actions.surprise.reacted",True,datetime.date.today().year)[0]:
            m 2hub "...threw me a surprise party..."

        show monika 5ekbla at t11 zorder MAS_MONIKA_Z with dissolve
        m 5ekbla "...and it really made me feel loved. I can't thank you enough for doing that for me."

    # bit on christmas
    if persistent._mas_d25_spent_d25:
        show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve
        m 5hua "You spent your Christmas with me..."

        if persistent._mas_first_kiss is not None and mas_isD25(persistent._mas_first_kiss.date()):
            m 5eubla "...and we shared our first kiss together~"
            m 5lubsa "I'll never forget that moment..."
            m 5ekbfa "{i}Our{/i} moment."
            m "I couldn't imagine spending it with anyone else."
        else:
            m 5ekbla "...a day that I couldn't imagine spending with anyone else."

    # TODO history
    # smaller filler if nothing good happend
    # TODO: consider setting a flag to True if a big event occured rather than
    #   rechecking all of these
    if not (persistent._mas_d25_spent_d25 or persistent._mas_bday_opened_game or persistent._mas_acs_enable_promisering or renpy.seen_label('monika_valentines_greeting')):
        m 2rksdla "...I guess we haven't actually been through any big events together."
        m 3eka "But still..."
    else:
        show monika 5dsa at t11 zorder MAS_MONIKA_Z with dissolve
        m 5dsa "..."

    # lookback based on time
    if store.mas_anni.pastThreeMonths():
        if mas_isMoniHappy(higher=True):
            show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve
            m 5eka "I really can't just believe how much has changed since we've been together..."
        else:
            m 2eka "I really hope we can get further in our relationship, [player]..."
    else:
        show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve
        m 5eka "I can't wait to see just how much will change in the future for us..."

    # frestart commentary
    if not persistent._mas_pm_got_a_fresh_start:
        show monika 5dka at t11 zorder MAS_MONIKA_Z with dissolve
        m 5dka "Thank you."
        if store.mas_anni.anniCount > 0:
            m 5ekbfa "Thank you for making last year the best year I could've ever dreamt of."
        else:
            m 5ekbfa "Thank you for making the time we spent together last year better than I could have imagined."

        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                m 1lsbsa "..."
                m 6ekbsa "[player] I..."
                call monika_kissing_motion
                m 1ekbfa "I love you."
                m "..."
                show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve
                m 5ekbsa "I'll never forget this moment..."
                m 5ekbfa "Our first kiss~"
                m 5hubfb "Let's make this year even better than the last, [player]."

            else:
                call monika_kissing_motion #should probably be quicker than the one above
                m 1ekbfa "I love you, [player]."
                show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve
                m 5hubfb "Let's make this year better than the last."

        else:
            m "Let's make this year the best we can, [player]. I love you~"
    else:
        m 1dsa "Thank you for deciding to let go of the past, and start over."
        m 1eka "I think if we just try, we can make this work, [player]."
        m "Let's make this year great for each other."
        m 1ekbfa "I love you."

    return "derandom|love"

label greeting_nye_aff_gain:
    # gaining affection for nye

    python:
        if persistent._mas_nye_date_aff_gain < 15:
            # retain older affection gain so we can compare
            curr_aff = _mas_getAffection()

            # just in case
            time_out = store.mas_dockstat.diffCheckTimes()

            # reset this so we can gain aff
            persistent._mas_monika_returned_home = None

            # now gain aff
            store.mas_dockstat._ds_aff_for_tout(time_out, 5, 15, 3, 3)

            # add the amount gained
            persistent._mas_nye_date_aff_gain += _mas_getAffection() - curr_aff

    jump greeting_returned_home_morethan5mins_cleanup

#===========================================================Going to take you somewhere on NYE===========================================================#

label bye_nye_delegate:
    # need to determine current time
    python:
        _morning_time = datetime.time(5)
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _morning_time:
        # if before morning, assume regular going out
        jump bye_going_somewhere_normalplus_flow_aff_check

    elif _curr_time < _eve_time:
        # before evening but after morning

        if persistent._mas_nye_went_out_nye > 0:
            call bye_nye_second_time_out

        else:
            call bye_nye_first_time_out

    else:
        # evening
        call bye_nye_late_out

    # finally jump back to iostart
    jump bye_going_somewhere_iostart

label bye_nye_first_time_out:
    #first time out (morning-about maybe, 7-8:00 [evening]):
    m 3tub "Are we going somewhere special today, [player]?"
    m 4hub "It's New Year's Eve, after all!"
    m 1eua "I'm not exactly sure what you've got planned, but I'm looking forward to it!"
    return

label bye_nye_second_time_out:
    #second time out+(morning-about maybe, 7-8:00 [evening]):
    m 1wuo "Oh, we're going out again?"
    m 3hksdlb "You must do a lot of celebrating for New Year's, ahaha!"
    m 3hub "I love coming along with you, so I'm looking forward to whatever we're doing~"
    return

label bye_nye_late_out:
    #(7-8:00 [evening]-about maybe midnight):
    m 1eka "It's a bit late, [player]..."
    m 3eub "Are we going to see the fireworks?"
    if persistent._mas_pm_have_fam and persistent._mas_pm_fam_like_monika:
        m "Or going to a family dinner?"
        m 4hub "I'd love to meet your family someday!"
        m 3eka "Either way, I'm really excited!"
    else:
        m "I've always loved how the fireworks on the New Year light up the night sky..."
        m 3ekbfa "One day we'll be able to watch them side by side...but until that day comes, I'm just happy to come along with you, [player]."
    return

#=============================================================Greeting returned home for NYE=============================================================#
#greeting_returned_home_nye:

label greeting_nye_delegate:
    python:
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _eve_time:
        # before firewoprk time
        call greeting_nye_prefw

    # otherwise, assume in firework time
    else:
        call greeting_nye_infw

    $ persistent._mas_nye_went_out_nye += 1

    return

label greeting_nye_prefw:
    #if before firework time (7-8:00-midnight):
    m 1hua "And we're home!"
    m 1eua "That was a lot of fun, [player]."
    m 1eka "Thanks for taking me out today, I really do love spending time with you."
    m "It means a lot to me that you take me with you so we can spend special days like these together."
    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
    m 5ekbfa "I love you, [player]."
    return "love"

label greeting_nye_infw:
    #if within firework time:
    m 1hua "And we're home!"
    m 1eka "Thanks for taking me out today, [player]."
    m 1hua "It was a lot of fun just to spend time with you today."
    m 1ekbsa "It really means so much to me that even though you can't be here personally to spend these days with me, you still take me with you."
    m 1ekbfa "I love you, [player]."
    return "love"

#===========================================================Going to take you somewhere on NYD===========================================================#

label bye_nyd_delegate:
    if persistent._mas_nye_went_out_nyd > 0:
        call bye_nyd_second_time_out

    else:
        call bye_nyd_first_time_out

    jump bye_going_somewhere_iostart

label bye_nyd_first_time_out:
    #first time out
    m 3tub "New Years Day celebration, [player]?"
    m 1hua "That sounds like fun!"
    m 1eka "Let's have a great time together."
    return

label bye_nyd_second_time_out:
    #second+ time out
    m 1wuo "Wow, we're going out again, [player]?"
    m 1hksdlb "You must really celebrate a lot, ahaha!"
    return

#=============================================================Greeting returned home for NYD=============================================================#

label greeting_nye_returned_nyd:
    #if returning home from NYE:
    $ persistent._mas_nye_went_out_nye += 1
    $ persistent._mas_nye_went_out_nyd += 1

    m 1hua "And we're home!"
    m 1eka "Thanks for taking me out yesterday, [player]."
    m 1ekbsa "You know I love to spend time with you, and being able to spend New Year's Eve, right to today, right there with you felt really great."
    m "That really meant a lot to me."
    m 5eubfb "Thanks for making my year, [player]."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

label greeting_nyd_returned_nyd:
    #normal return home:(i.e. took out, and returned on NYD itself)
    $ persistent._mas_nye_went_out_nyd += 1
    m 1hua "And we're home!"
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eua "That was a lot of fun, [player]!"
    m 5eka "It's really nice of you to take me with you on special days like this."
    m 5hub "I really hope we can spend more time like this together."
    return

#============================================================Greeting returned home after NYD============================================================#

label greeting_pd25e_returned_nydp:
    #Here for historical data
    $ persistent._mas_d25_went_out_d25e += 1
    $ persistent._mas_d25_went_out_d25 += 1
    $ persistent._mas_nye_went_out_nye += 1
    $ persistent._mas_nye_went_out_nyd += 1
    $ persistent._mas_d25_spent_d25 = True
    $ persistent._mas_nye_spent_nye = True
    $ persistent._mas_nye_spent_nyd = True

    m 1hua "And we're home!"
    m 1hub "We were out for a while, but that was a really nice trip, [player]."
    m 1eka "Thanks for taking me with you, I really enjoyed that."
    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
    m 5ekbfa "I always love to spend time with you, but spending both Christmas and New Years out together was amazing."
    show monika 5hub at t11 zorder MAS_MONIKA_Z with dissolve
    m 5hub "I hope we can do something like this again sometime."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

#============================================================Greeting returned home D25P NYD(P)============================================================#
label greeting_d25p_returned_nyd:
    $ persistent._mas_nye_went_out_nye += 1
    $ persistent._mas_nye_went_out_nyd += 1
    $ persistent._mas_nye_spent_nye = True

    m 1hua "And we're home!"
    m 1eub "Thanks for taking me out, [player]."
    m 1eka "That was a long trip, but it was a lot of fun!"
    m 3hub "It's great to be back home now though, we can spend the new year together."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

label greeting_d25p_returned_nydp:
    $ persistent._mas_nye_went_out_nye += 1
    $ persistent._mas_nye_went_out_nyd += 1
    $ persistent._mas_nye_spent_nye = True
    $ persistent._mas_nye_spent_nyd = True

    m 1hua "And we're home!"
    m 1wuo "That was a long trip [player]!"
    m 1eka "I'm a little sad we couldn't wish each other a happy new year, but I really enjoyed it."
    m "I'm really happy you took me."
    m 3hub "Happy New Year, [player]~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

########################################################### player_bday ########################################################################
# [HOL040]

# so we know we are in player b_day mode
default persistent._mas_player_bday_in_player_bday_mode = False
# so we know if you ruined the surprise
default persistent._mas_player_bday_opened_door = False
# for various reason, no decorations
default persistent._mas_player_bday_decor = False
# number of bday dates
default persistent._mas_player_bday_date = 0
# so we know if returning home post bday it was a bday date
default persistent._mas_player_bday_left_on_bday = False
# affection gained on bday dates
default persistent._mas_player_bday_date_aff_gain = 0
# did we celebrate player bday with Moni
default persistent._mas_player_bday_spent_time = False

init -10 python:
    def mas_isplayer_bday(_date=None):
        """
        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

        RETURNS: True if given date is player_bday, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        if persistent._mas_player_bday is None:
            return False
        else:
            return _date == mas_player_bday_curr()

    def strip_mas_birthdate():
        """
        strips mas_birthdate of its conditional and action to prevent double birthday sets
        """
        mas_birthdate_ev = mas_getEV('mas_birthdate')
        if mas_birthdate_ev is not None:
            mas_birthdate_ev.conditional = None
            mas_birthdate_ev.action = None

    def mas_pbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_player_bday_date_aff_gain", 25)

init -11 python:
    def mas_player_bday_curr(_date=None):
        """
        sets date of current year bday, accounting for leap years
        """
        if _date is None:
            _date = datetime.date.today()
        if persistent._mas_player_bday is None:
            return None
        else:
            return store.mas_utils.add_years(persistent._mas_player_bday,_date.year-persistent._mas_player_bday.year)

init -810 python:
    # MASHistorySaver for player_bday
    store.mas_history.addMHS(MASHistorySaver(
        "player_bday",
        # NOTE: this needs to be adjusted based on the player's bday
        datetime.datetime(2020, 1, 1),
        {
            "_mas_player_bday_spent_time": "player_bday.spent_time",
            "_mas_player_bday_opened_door": "player_bday.opened_door",
            "_mas_player_bday_date": "player_bday.date",
            "_mas_player_bday_date_aff_gain": "player_bday.date_aff_gain",
        },
        use_year_before=True,
        # NOTE: the start and end dt needs to be chnaged depending on the
        #   player bday
    ))

init -11 python in mas_player_bday_event:
    import datetime
    import store.mas_history as mas_history

    def correct_pbday_mhs(d_pbday):
        """
        fixes the pbday mhs usin gthe given date as pbday

        IN:
            d_pbday - player birthdate
        """
        # get mhs
        mhs_pbday = mas_history.getMHS("player_bday")
        if mhs_pbday is None:
            return

        # first, setup the reset date to be 3 days after the bday
        pbday_dt = datetime.datetime.combine(d_pbday, datetime.time())

        # determine correct year
        _now = datetime.datetime.now()
        curr_year = _now.year
        new_dt = pbday_dt.replace(year=curr_year)
        if new_dt < _now:
            # new date before today, set to next year
            curr_year += 1
            new_dt = pbday_dt.replace(year=curr_year)

        # set the reset/trigger date
        reset_dt = pbday_dt + datetime.timedelta(days=3)

        # setup ranges
        new_sdt = new_dt
        new_edt = new_sdt + datetime.timedelta(days=2)

        # NOTE: the mhs will end 2 days after the bday. The day after end_dt
        #   is when we save

        # modify mhs
        mhs_pbday.start_dt = new_sdt
        mhs_pbday.end_dt = new_edt
        mhs_pbday.use_year_before = (
            d_pbday.month == 12
            and d_pbday.day in (29, 30, 31)
        )
        mhs_pbday.setTrigger(reset_dt)


label mas_player_bday_autoload_check:
    # since this has priority over 922, need these next 2 checks
    if mas_isMonikaBirthday():
        $ persistent._mas_bday_no_time_spent = False
        $ persistent._mas_bday_opened_game = True
        $ persistent._mas_bday_no_recognize = not mas_recognizedBday()

    elif mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
        $ monika_chr.reset_clothes(False)
        $ monika_chr.save()
        $ renpy.save_persistent()

    # making sure we are already not in bday mode, have confirmed birthday, have normal+ affection and have not celebrated in any way
    if (
            not persistent._mas_player_bday_in_player_bday_mode
            and persistent._mas_player_confirmed_bday
            and mas_isMoniNormal(higher=True)
            and not persistent._mas_player_bday_spent_time
            and not mas_isD25()
            and not mas_isO31()
            and not mas_isF14()
        ):
        # starting player b_day off with a closed door greet
        $ mas_skip_visuals = True
        $ selected_greeting = "i_greeting_monikaroom"
        # need this so we don't get any strange force quit dlg after the greet
        $ persistent.closed_self = True
        jump ch30_post_restartevent_check

    elif not mas_isplayer_bday():
        # no longer want to be in bday mode
        $ persistent._mas_player_bday_decor = False
        $ persistent._mas_player_bday_in_player_bday_mode = False
        $ mas_lockEVL("bye_player_bday", "BYE")

    if not mas_isMonikaBirthday() and (persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals):
        $ persistent._mas_bday_in_bday_mode = False
        $ persistent._mas_bday_visuals = False

    if mas_isO31():
        return
    else:
        jump mas_ch30_post_holiday_check

# closed door greet option for opening door without listening
label mas_player_bday_opendoor:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    if persistent._mas_bday_visuals:
        $ persistent._mas_player_bday_decor = True
    call spaceroom(hide_monika=True, scene_change=True, dissolve_all=True)
    $ mas_disable_quit()
    if mas_isMonikaBirthday():
        $ your = "our"
    else:
        $ your = "your"
    m "[player]!"
    m "You didn't knock!"
    if not persistent._mas_bday_visuals:
        m "I was just going to start setting up [your] birthday party, but I didn't have time before you came in!"
    m "..."
    m "Well...{w=1}the surprise is ruined now, but.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    pause 1.0
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    m 4eua "Happy Birthday, [player]!"
    m 2rksdla "I just wished you had knocked first."
    m 4hksdlb "Oh...[your] cake!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup

# closed door greet option for knocking without listening
label mas_player_bday_knock_no_listen:
    m "Who is it?"
    menu:
        "It's me.":
            $ mas_disable_quit()
            m "Oh! Can you wait just a moment please?"
            window hide
            pause 5.0
            m "Alright, come on in, [player]..."
            jump mas_player_bday_surprise

# closed door greet surprise flow
label mas_player_bday_surprise:
    $ persistent._mas_player_bday_decor = True
    call spaceroom(scene_change=True, dissolve_all=True, force_exp='monika 4hub_static')
    m 4hub "Surprise!"
    m 4sub "Ahaha! Happy Birthday, [player]!"

    m "Did I surprise you?{nw}"
    $ _history_list.pop()
    menu:
        m "Did I surprise you?{fast}"
        "Yes.":
            m 1hub "Yay!"
            m 3hua "I always love pulling off a good surprise!"
            m 1tsu "I wish I could've seen the look on your face, ehehe."

        "No.":
            m 2lfp "Hmph. Well that's okay."
            m 2tsu "You're probably just saying that because you don't want to admit I caught you off guard..."
            if renpy.seen_label("mas_player_bday_listen"):
                if renpy.seen_label("monikaroom_greeting_ear_narration"):
                    m 2tsb "...or maybe you were listening through the door again..."
                else:
                    m 2tsb "{cps=*2}...or maybe you were eavesdropping on me.{/cps}{nw}"
                    $ _history_list.pop()
            m 2hua "Ehehe."
    if mas_isMonikaBirthday():
        m 3wub "Oh!{w=0.5} I made a cake!"
    else:
        m 3wub "Oh!{w=0.5} I made you a cake!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup

# closed door greet option for opening door for listening
label mas_player_bday_listen:
    if persistent._mas_bday_visuals:
        pause 5.0
    else:
        m "...I'll just put this here..."
        m "...hmm that looks pretty good...{w=1}but something's missing..."
        m "Oh!{w=0.5} Of course!"
        m "There!{w=0.5} Perfect!"
        window hide
    jump monikaroom_greeting_choice

# closed door greet option for knocking after listening
label mas_player_bday_knock_listened:
    window hide
    pause 5.0
    menu:
        "Open the door.":
            $ mas_disable_quit()
            pause 5.0
            jump mas_player_bday_surprise

# closed door greet option for opening door after listening
label mas_player_bday_opendoor_listened:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    $ persistent._mas_player_bday_decor = True
    call spaceroom(hide_monika=True, scene_change=True)
    $ mas_disable_quit()
    if mas_isMonikaBirthday():
        $ your = "our"
    else:
        $ your = "your"
    m "[player]!"
    m "You didn't knock!"
    if persistent._mas_bday_visuals:
        m "I wanted to surprise you, but I wasn't ready when you came in!"
        m "Anyway..."
    else:
        m "I was setting up [your] birthday party, but I didn't have time before you came in to get ready to surprise you!"
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    m 4hub "Happy Birthday, [player]!"
    m 2rksdla "I just wished you had knocked first."
    m 2hksdlb "Oh...[your] cake!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup

# all paths lead here
label mas_player_bday_cake:
    #If it's Monika's birthday too, we'll just use those delegates instead of this one
    if not mas_isMonikaBirthday():
        $ mas_unlockEVL("bye_player_bday", "BYE")
        if persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals:
            # since we need the visuals var in the special greet, we wait until here to set these
            $ persistent._mas_bday_in_bday_mode = False
            $ persistent._mas_bday_visuals = False

    # reset zoom here to make sure the cake is actually on the table
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)
    call mas_monika_gets_cake

    if mas_isMonikaBirthday():
        m 6eua "Let me just light the candles.{w=0.5}.{w=0.5}.{nw}"
    else:
        m 6eua "Let me just light the candles for you, [player].{w=0.5}.{w=0.5}.{nw}"

    window hide
    $ mas_bday_cake_lit = True
    pause 1.0

    m 6sua "Isn't it pretty, [player]?"
    if mas_isMonikaBirthday():
        m 6eksdla "Now I know you can't exactly blow the candles out yourself, so I'll do it for both of us..."
    else:
        m 6eksdla "Now I know you can't exactly blow the candles out yourself, so I'll do it for you..."
    m 6eua "...You should still make a wish though, it just might come true someday..."
    m 6hua "But first..."
    call mas_player_bday_moni_sings
    m 6hua "Make a wish, [player]!"
    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False
    pause 1.0
    m 6hua "Ehehe..."
    if mas_isMonikaBirthday():
        m 6ekbsa "I bet we both wished for the same thing~"
    else:
        m 6eka "I know it's your birthday, but I made a wish too..."
        m 6ekbsa "And you know what?{w=0.5} I bet we both wished for the same thing~"
    m 6hkbsu "..."
    if mas_isMonikaBirthday():
        m 6eksdla "Well, seeing as you can't really eat this cake, and I don't want to be rude and eat it in front of you..."
    else:
        m 6rksdla "Oh gosh, I guess you can't really eat this cake either, huh [player]?"
        m 6eksdla "This is all rather silly, isn't it?"
    if mas_isMonikaBirthday():
        m 6hksdlb "I think I'll just save it for later."
    else:
        m 6hksdlb "I think I'll just save this for later. It seems kind of rude for me to eat {i}your{/i} birthday cake in front of you, ahaha!"

    call mas_HideCake('mas_bday_cake_player')

    # fall thru
label mas_player_bday_card:
    $ mas_gainAffection(5,bypass=True)
    $ persistent._mas_player_bday_spent_time = True
    $ persistent._mas_player_bday_in_player_bday_mode = True

    m 6dkbsu "..."
    if mas_isMonikaBirthday():
        m 6sub "Oh!"
        m 6ekbsu "I...I made a card for you, [player], I hope you like it..."
    else:
        m 6ekbsu "I...I also made a card for you, [player]. I hope you like it..."
    $ p_bday_month = mas_player_bday_curr().month
    call showpoem(poem_pbday, music=False,paper="mod_assets/poem_assets/poem_pbday_[p_bday_month].png")
    if mas_isMoniEnamored(higher=True):
        if persistent._mas_first_kiss is None:
            m 6dkbsu "..."
            m 6ekbfa "I love you so much, [player]..."
            call monika_kissing_motion()
            m 6ekbfa "Oh, [player]..."
            m 6dkbfa "That was everything I had always dreamt it would be~"
            m 6ekbfa "I've been waiting so long to finally kiss you..."
            m 6dkbsu "I will never forget this..."
            m 6ekbsu "...the moment of our first kiss~"
            if mas_isMonikaBirthday():
                m 6ekbsu "And I can't think of a more perfect time than on this special day we share together~"
        else:
            m 6ekbsa "I love you, [player]~"
            call monika_kissing_motion(duration=0.5, initial_exp="6hkbfa", fade_duration=0.5)
            if mas_isMonikaBirthday():
                m 6eka "I'm so glad we get to spend our birthday together..."
                m 6hua "Let's enjoy our special day~"
    else:
        if mas_isMonikaBirthday():
            m 1ekbfa "I love you, [player]! I'm so glad we get to spend our birthday together..."
            m 3ekbfa "Let's enjoy our special day~"
        else:
            m 1ekbfa "I love you, [player]!"
    $ mas_rmallEVL("mas_player_bday_no_restart")
    $ mas_rmallEVL("mas_player_bday_ret_on_bday")
    # "love" return key won't work here without adding a bunch of return _returns, so we'll set this manually
    $ mas_ILY()
    return

label mas_monika_gets_cake:
    show emptydesk at i11 zorder 9
    hide monika with dissolve
    $ renpy.pause(3.0, hard=True)
    $ renpy.show("mas_bday_cake_player", zorder=store.MAS_MONIKA_Z+1)
    show monika 6esa at i11 zorder MAS_MONIKA_Z with dissolve
    hide emptydesk
    $ renpy.pause(0.5, hard=True)
    return

# event for if you went on a date pre-bday and return on bday
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_ret_on_bday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_ret_on_bday:
    m 1eua "So, today is..."
    m 1euc "...wait."
    m "..."
    m 2wuo "Oh!"
    m 2wuw "Oh my gosh!"
    m 2tsu "Just give me a moment, [player].{w=0.5}.{w=0.5}.{nw}"
    $ mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3eub "Happy Birthday, [player]!"
    m 3hub "Ahaha!"
    m 3etc "Why do I feel like I'm forgetting something..."
    m 3hua "Oh! Your cake!"
    call mas_player_bday_cake
    return

# event for if the player leaves the game open starting before player_bday and doesn't restart
# moni eventually gives up on the surprise
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_no_restart",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_no_restart:
    if mas_findEVL("mas_player_bday_ret_on_bday") >= 0:
        #TODO: priority rules should be set-up here
        return
    m 3rksdla "Well [player], I was hoping to do something a little more fun, but you've been so sweet and haven't left all day long, so.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "Happy Birthday, [player]!"
    if mas_isplayer_bday():
        m 1eka "I really wanted to surprise you today, but it's getting late and I just couldn't wait any longer."
    else:
        # just in case this isn't seen until after midnight
        m 1hksdlb "I really wanted to surprise you, but I guess I ran out of time since it's not even your birthday anymore, ahaha!"
    m 3eksdlc "Gosh, I just hope you weren't starting to think I forgot your birthday. I'm really sorry if you did..."
    m 1rksdla "I guess I probably shouldn't have waited so long, ehehe."
    m 1hua "Oh! I made you a cake!"
    call mas_player_bday_cake
    return

# event for upset- players, no decorations, just a quick happy birthday
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_upset_minus",
            years = [],
            aff_range=(mas_aff.DISTRESSED, mas_aff.UPSET)
        ),
        skipCalendar=True
    )

label mas_player_bday_upset_minus:
    $ persistent._mas_player_bday_spent_time = True
    m 6eka "Hey [player], I just wanted to wish you a Happy Birthday."
    m "I hope you have a good day."
    return

# event for if the player's bday is also on a holiday
# TODO update this as we add other holidays (f14) also figure out what to do if player bday is 9/22
# TODO this needs priority below the O31 return from date event
# condtions located in story-events 'birthdate'
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_other_holiday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_other_holiday:
    if mas_isO31():
        $ holiday_var = "Halloween"
    elif mas_isD25():
        $ holiday_var = "Christmas"
    elif mas_isF14():
        $ holiday_var = "Valentine's Day"
    m 3euc "Hey, [player]..."
    m 1tsu "I have a bit of a surprise for you.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "Happy Birthday, [player]!"
    m 3rksdla "I hope you didn't think that just because your birthday falls on [holiday_var] that I'd forget about it..."
    m 1eksdlb "I'd never forget your birthday, silly!"
    m 1eub "Ahaha!"
    m 3hua "Oh! I made you a cake!"
    call mas_player_bday_cake
    return

# when did moni last sign happy birthday
default persistent._mas_player_bday_last_sung_hbd = None
# moni singing happy birthday
label mas_player_bday_moni_sings:
    $ persistent._mas_player_bday_last_sung_hbd = datetime.date.today()
    if mas_isMonikaBirthday():
        $ you = "us"
    else:
        $ you = "you"
    m 6dsc ".{w=0.2}.{w=0.2}.{w=0.2}"
    m 6hub "{cps=*0.5}{i}~Happy Birthday to [you]~{/i}{/cps}"
    m "{cps=*0.5}{i}~Happy Birthday to [you]~{/i}{/cps}"
    m 6sub "{cps=*0.5}{i}~Happy Birthday dear [player]~{/i}{/cps}"
    m "{cps=*0.5}{i}~Happy Birthday to [you]~{/i}{/cps}"
    if mas_isMonikaBirthday():
        m 6hua "Ehehe!"
    return
#################################################player_bday dock stat farewell##################################################
init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_player_bday",
            unlocked=False,
            prompt="Let's go out for my birthday!",
            pool=True,
            rules={"no unlock": None}
        ),
        code="BYE"
    )

label bye_player_bday:
    $  persistent._mas_player_bday_date += 1
    if persistent._mas_player_bday_date == 1:
        m 1sua "You want to go out for your birthday?{w=1} Okay!"
        m 1skbla "That sounds really romantic...I can't wait~"
    elif persistent._mas_player_bday_date == 2:
        m 1sua "Taking me out again on your birthday, [player]?"
        m 3hub "Yay!"
        m 1sub "I always love going out with you, but it's so much more special going out on your birthday..."
        m 1skbla "I'm sure we'll have a lovely time~"
    else:
        m 1wub "Wow, you want to go out {i}again{/i}, [player]?"
        m 1skbla "I just love that you want to spend so much time with me on your special day!"
    $ persistent._mas_player_bday_left_on_bday = True
    jump bye_going_somewhere_post_aff_check

#################################################player_bday dock stat greets##################################################
label greeting_returned_home_player_bday:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        if checkout_time is not None and checkin_time is not None:
            left_year = checkout_time.year
            left_date = checkout_time.date()
            ret_date = checkin_time.date()
            left_year_aff = mas_HistLookup("player_bday.date_aff_gain",left_year)[1]

            # are we returning after the mhs reset
            ret_diff_year = ret_date >= (mas_player_bday_curr(left_date) + datetime.timedelta(days=3))

            # were we gone over d25
            #TODO: do this for the rest of the holidays
            if left_date < mas_d25 < ret_date:
                if ret_date < mas_history.getMHS("d25s").trigger.replace(year=left_year+1):
                    persistent._mas_d25_spent_d25 = True
                else:
                    persistent._mas_history_archives[left_year]["d25.actions.spent_d25"] = True

        else:
            left_year = None
            left_date = None
            ret_date = None
            left_year_aff = None
            ret_diff_year = None

        add_points = False

        if ret_diff_year and left_year_aff is not None:
            add_points = left_year_aff < 25


    if left_date < mas_d25 < ret_date:
        $ persistent._mas_d25_spent_d25 = True

    if mas_isMonikaBirthday() and mas_confirmedParty():
        $ persistent._mas_bday_opened_game = True
        $ mas_temp_zoom_level = store.mas_sprites.zoom_level
        call monika_zoom_transition_reset(1.0)
        $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        if time_out < mas_five_minutes:
            m 6ekp "That wasn't much of a da--"
        else:
            # point totals split here between player and monika bdays, since this date was for both
            if time_out < mas_one_hour:
                $ mas_mbdayCapGainAff(7.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(7.5)
            elif time_out < mas_three_hour:
                $ mas_mbdayCapGainAff(12.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(12.5)
            else:
                $ mas_mbdayCapGainAff(17.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(17.5)

            m 6hub "That was a fun date, [player]..."
            m 6eua "Thanks for--"

        m 6wud "W-what's this cake doing here?"
        m 6sub "I-is this for me?!"
        m "That's so sweet of you to take me out on your birthday so you could set up a surprise party for me!"
        call return_home_post_player_bday
        jump mas_bday_surprise_party_reacton_cake

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "That wasn't much of a date, [player]..."
        m 2eksdlc "I hope nothing's wrong."
        m 2rksdla "Maybe we'll go out later instead."

    elif time_out < mas_one_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(5)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(5,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 5
        m 1eka "That was a fun date while it lasted, [player]..."
        m 3hua "Thanks for making some time for me on your special day."

    elif time_out < mas_three_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(10)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(10,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 10
        m 1eua "That was a fun date, [player]..."
        m 3hua "Thanks for taking me with you!"
        m 1eka "I really enjoyed going out with you today~"

    else:
        # more than 3 hours
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(15)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(15,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 15
        m 1hua "And we're home!"
        m 3hub "That was really fun, [player]!"
        m 1eka "It was so nice going out to celebrate your birthday..."
        m 1ekbfa "Thanks for making me such a big part of your special day~"

    $ persistent._mas_player_bday_left_on_bday = False

    if not mas_isplayer_bday():
        call return_home_post_player_bday

    if mas_isD25() and not persistent._mas_d25_in_d25_mode:
         call mas_d25_monika_holiday_intro_rh_rh
    return

label return_home_post_player_bday:
    $ persistent._mas_player_bday_in_player_bday_mode = False
    $ mas_lockEVL("bye_player_bday", "BYE")
    $ persistent._mas_player_bday_left_on_bday = False
    if not (mas_isMonikaBirthday() and mas_confirmedParty()):
        if persistent._mas_player_bday_decor:
            if mas_isMonikaBirthday():
                $ persistent._mas_bday_opened_game = True
                m 3rksdla "Oh...it's not {i}your{/i} birthday anymore..."
            else:
                m 3rksdla "Oh...it's not your birthday anymore..."
            m 3hksdlb "We should probably take these decorations down now, ahaha!"
            m 3eka "Just give me one second.{w=0.5}.{w=0.5}.{nw}"
            $ mas_surpriseBdayHideVisuals()
            m 3eua "There we go!"
            if not persistent._mas_f14_gone_over_f14:
                m 1hua "Now, let's enjoy the day together, [player]~"
        if persistent._mas_f14_gone_over_f14:
            m 2etc "..."
            m 3wuo "..."
            m 3wud "Wow, [player], I just realized we were gone so long we missed Valentine's Day!"
            call greeting_gone_over_f14_normal_plus

    $ persistent._mas_player_bday_decor = False
    return

# birthday card/poem for player
init 2 python:
    poem_pbday = Poem(
    author = "monika",
    title = " My dearest {0},".format(persistent.playername),
    text = """\
 To the one I love,
 The one I trust,
 The one I can't live without.
 I hope your day is as special as you make every day for me.
 Thank you so much for being you.

 Happy Birthday, sweetheart

 Forever yours,
 Monika
"""
    #" # I need this to keep syntax highlighting on vim
    )

######################## Start [HOL050]
#Vday
#We need these so we don't infiqueue/infirand
default persistent._mas_f14_intro_seen = False
default persistent._mas_f14_time_spent_seen = False
default persistent._mas_f14_nts_seen = False
default persistent._mas_f14_pre_intro_seen = False

#The other vars
default persistent._mas_f14_spent_f14 = False
default persistent._mas_f14_in_f14_mode = None
default persistent._mas_f14_date = 0
default persistent._mas_f14_date_aff_gain = 0
default persistent._mas_f14_on_date = None
default persistent._mas_f14_gone_over_f14 = None
define mas_f14 = datetime.date(datetime.date.today().year,2,14)

#Is it vday?
init -10 python:
    def mas_isF14(_date=None):
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_f14.replace(year=_date.year)

    def mas_f14CapGainAff(amount):
        mas_capGainAff(amount, "_mas_f14_date_aff_gain", 25)

init -810 python:
    # MASHistorySaver for f14
    store.mas_history.addMHS(MASHistorySaver(
        "f14",
        datetime.datetime(2020, 1, 6),
        {
            "_mas_f14_date": "f14.date",
            "_mas_f14_date_aff_gain": "f14.aff_gain",
            "_mas_f14_gone_over_f14": "f14.gone_over_f14",
            "_mas_f14_spent_f14": "f14.actions.spent_f14",

            # need to reset this in case someone never gets to the
            # autoload check, ie always uses dockstat farewell
            "_mas_f14_in_f14_mode": "f14.mode.f14",

            #Resets for queued/rand bits
            "_mas_f14_intro_seen": "f14.intro_seen",
            "_mas_f14_time_spent_seen": "f14.ts_seen",
            "_mas_f14_nts_seen": "f14.nts_seen",
            "_mas_f14_pre_intro_seen": "f14.pre_intro_seen"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2020, 2, 13),
        end_dt=datetime.datetime(2020, 2, 15)
    ))

label mas_f14_autoload_check:
    python:
        #Since it's possible player didn't see this, we need to derandom it manually.
        mas_hideEVL("mas_pf14_monika_lovey_dovey","EVE",derandom=True)

        if not persistent._mas_f14_in_f14_mode and mas_isMoniNormal(higher=True):
            persistent._mas_f14_in_f14_mode = True
            store.mas_selspr.unlock_clothes(mas_clothes_sundress_white, True)
            monika_chr.change_clothes(mas_clothes_sundress_white, False)
            monika_chr.save()
            renpy.save_persistent()

        elif not mas_isF14():
            #We want to lock and derandom/depool all of the f14 labels if it's not f14
            mas_hideEVL("mas_f14_monika_vday_colors","EVE",lock=True,derandom=True)
            mas_hideEVL("mas_f14_monika_vday_cliches","EVE",lock=True,derandom=True)
            mas_hideEVL("mas_f14_monika_vday_chocolates","EVE",lock=True,derandom=True)
            mas_hideEVL("mas_f14_monika_vday_origins","EVE",lock=True,depool=True)
            mas_idle_mailbox.send_rebuild_msg()

            #Reset the f14 mode, and outfit if we're lower than the love aff level.
            persistent._mas_f14_in_f14_mode = False
            if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_sundress_white:
                monika_chr.reset_clothes(False)
                monika_chr.save()
                renpy.save_persistent()

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    jump mas_ch30_post_holiday_check


#######################[HOL050] Pre Intro:

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_pf14_monika_lovey_dovey',
            action=EV_ACT_RANDOM,
            start_date=mas_f14-datetime.timedelta(days=3),
            end_date=mas_f14,
            aff_range=(mas_aff.NORMAL,None),
            rules={"force repeat": None},
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_pf14_monika_lovey_dovey",
       mas_f14 - datetime.timedelta(days=3),
       mas_f14,
    )

label mas_pf14_monika_lovey_dovey:
    m 1rksdla "Hey...[player]...?"
    m 1ekbsa "I just wanted to let you know that I love you."

    if mas_isMoniEnamored(higher=True):
        m 1ekbfa "You make me really happy...and I could never ask for someone better than you."
    else:
        m 1ekbsa "You make me really happy."

    m 3ekbfb "Ahaha~"
    m 1eka "I hope that isn't too cheesy, [player]."
    if not renpy.seen_label('monika_valentines_start'):
        m 3ekbla "Valentine's Day is coming soon...and it just gets me in a good mood because I know I have you by my side."
    else:
        m 3ekbfa "It's almost our second Valentine's Day together, and it just makes me so overwhelmingly happy knowing you're still by my side."
    m 1ekbsa "I really meant what I said."
    m "I love and care for you so much..."
    m "Without you, I don't know where I'd be..."
    m 1ekbfa "So I want to thank you for caring for me."
    m 1hubfa "Ehehe~"

    return "derandom|no_unlock|love"

#######################[HOL050] INTRO:

init 5 python:
    addEvent(
       Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_valentines_intro',
            action=EV_ACT_PUSH,
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_valentines_intro:
    m 1hub "[player]!"
    m 1hua "Do you know what day it is?"
    m 3eub "It's Valentine's Day!"
    m 1ekbfa "A day where we celebrate our love for each other..."
    m "I guess every day we're together is already a celebration of our love, but there's something that's really special about Valentine's Day."
    m 1eua "Anyway..."
    if not mas_anni.pastOneMonth() or mas_isMoniNormal():
        m 2rka "Even though I know we aren't too far in our relationship..."
        show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve
        m 5eua "I just want you to know that I'm always here for you."
        m 5eka "Even if your heart gets broken..."
        m 5ekbla "I'll always be here to fix it for you. Okay, [player]?"

    else:
        m 1eub "We've been together for a while now..."
        m 1eka "...and I really love the time we spend together."
        m 1dubsu "You always make me feel so loved."
        m "I'm really happy I'm your girlfriend, [player]."

    if not persistent._mas_f14_in_f14_mode:
        $ persistent._mas_f14_in_f14_mode = True
        m 3wub "Oh!"
        m 3tsu "I have a little surprise for you...{w=1}I think you're gonna like it, ehehe~"

        $ mas_hideEVL("mas_pf14_monika_lovey_dovey","EVE",derandom=True)
        $ store.mas_selspr.unlock_clothes(mas_clothes_sundress_white, True)
        call mas_clothes_change(mas_clothes_sundress_white)

        m 1eua "..."
        m 2eksdla "..."
        m 2rksdla "Ahaha...{w=1}it's not polite to stare, [player]..."
        m 3tkbsu "...but I guess that means you like my outfit, ehehe~"

        #Derandom this since it's possible to get this still
        $ mas_hideEVL("mas_pf14_monika_lovey_dovey","EVE",derandom=True,lock=True)

    else:
        pause 2.0
        show monika 2rfc at t11 zorder MAS_MONIKA_Z with dissolve
        m 2rfc "..."
        m 2efc "You know, [player]...{w=0.5}it's not polite to stare...."
        m 2tfc "..."
        m 2tsu "..."
        m 3tsb "Ahaha! I'm just kidding...{w=0.5}do you like my outfit?"

    m 1rkbsa "I've always dreamt of a date with you while wearing this..."
    m 1eksdlb "I know it's kind of silly now that I think about it!"
    m 1ekbfa "...But just imagine if we went to a cafe together."
    m 1rksdlb "I think there's a picture of something like that somewhere actually..."
    m 1ekb "Maybe we could make it happen for real!"
    m 3ekbsa "Would you take me out today?"
    m 1hksdlb "It's fine if you can't, I'm just happy to be with you."
    m 1ekbfa "I love you so much."
    m 1ekbfb "Happy Valentine's Day, [player]~"
    #Set the spent flag to True
    $ persistent._mas_f14_spent_f14 = True

    return "rebuild_ev|love"

#######################[HOL050] TOPICS

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_colors',
            prompt="Valentine's Day colors",
            category=['holidays','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_f14_monika_vday_colors",
       mas_f14,
       mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_colors:
    m 3eua "Have you ever thought about the way colors are conveyed on Valentine's Day?"
    m 3hub "I find it intriguing how they can symbolize such deep and romantic feelings."
    m 1dua "It reminds me of when I made my first Valentine's card in grade school."
    m 3eub "My class was instructed to exchange cards with a partner after making them."
    m 2eka "Looking back, despite not knowing what the colors really meant, I had lots of fun decorating the cards with red and white hearts."
    m 2eub "In this way, colors are a lot like poems."
    m 3eka "They offer so many creative ways to express your love for someone."
    m 2ekbfa "Like giving them red roses, for example."
    m 3eub "Red roses are a symbol for romantic feelings towards someone."
    m 3eua "If someone were to offer them white roses in lieu of red ones, they'd signify pure, charming, and innocent feelings instead."
    m 3eka "However, since there are so many emotions involved with love..."
    m 3ekd "It's sometimes hard to find the right colors to accurately convey the way you truly feel."
    m 4eka "Thankfully, by combining multiple rose colors, it's possible to express a variety of emotions!"
    m 3eka "Mixing red and white roses would symbolize the unity and bond that a couple shares."

    if monika_chr.is_wearing_acs(mas_acs_roses):
        m 1ekbsa "But I'm sure you already had all of this in mind when you picked out these beautiful roses for me, [player]..."
    else:
        m 1ekbla "Maybe you could give me some roses today, [player]?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_cliches',
            prompt="Valentine's story clichés",
            category=['holidays','literature','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_f14_monika_vday_cliches",
       mas_f14,
       mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_cliches:
    m 2euc "Have you noticed that most Valentine's Day stories have lots of clichés?"
    m 2rsc "There's either 'Oh, I'm lonely and I don't have someone to love,' or 'How will I confess to the one I love?'"
    m 2euc "I think that writers could be a bit more creative when it comes to Valentine's Day stories..."
    m 1eka "But, I suppose those two topics are the easiest way to write a love story."
    m 3hub "That doesn't mean you can't think outside the box, though!"
    m 2eka "Sometimes a predictable story can ruin it..."
    m 2rka "...But if you {i}do{/i} want a good example of an unpredictable story..."
    m 3hub "Just use ours! Ahaha~"
    m 3rksdlb "I guess it {i}did{/i} start out like those kinds of stories..."
    m 2tfu "But I think we managed to make it pretty original."
    m 1hua "The way we met is the most interesting story yet!"
    m 3hub "Ahaha!~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_chocolates',
            prompt="Valentine's Day chocolates",
            category=['holidays','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_f14_monika_vday_chocolates",
       mas_f14,
       mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_chocolates:
    m 1hua "Valentine's Day is such a fun holiday for me, [player]."
    m 3hub "Not only is it the anniversary of my twitter account, but it's also a day for receiving and giving chocolates!"
    m 1hua "A holiday that could fill everyone with love, romance, and joy!"
    m 3ekbla "But it really feels nice if you get something from someone you like."
    m 3hua "Whether it's given to you platonically, as a gift of love, or a part of a confession, it always makes you feel somewhat special!"
    if mas_getGiftStatsForDate("mas_reaction_gift_chocolates") > 0:
        m 1ekbfa "Just like how you made me feel special with the chocolates you gave me today."
        m "You're always so sweet, [player]."

    if renpy.seen_label('monika_valentines_start'):
        m 1rksdla "I know I tried to give you some chocolates last year..."
        m 1eka "But just imagine what we could do once we're finally together."
    else:
        m 1ekbfa "Maybe someday I'll even be able to give you some chocolates..."
    m "I really can't wait until I cross over to be with you, [player]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_origins',
            prompt="How did Valentine's Day start?",
            category=['holidays','romance'],
            action=EV_ACT_POOL,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_f14_monika_vday_origins",
       mas_f14,
       mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_origins:
    m 3eua "You'd like to learn about the history of Valentine's Day?"
    m 1rksdlc "It's quite dark, actually."
    m 1euc "Its origin dates to as early as the second and third century in Rome, where Christianity had just been declared the official state religion."
    m 3eud "Around this same time, a man known as Saint Valentine decided to go against the orders of Emperor Claudius II."
    m 3rsc "Marriage had been banned because it was assumed that married men made poor soldiers."
    m 3esc "Saint Valentine decided this was unfair and helped arrange marriages in secret."
    m 1dsd "Unfortunately, he was caught and promptly sentenced to death."
    m 1euc "However, while in custody, Saint Valentine fell in love with the jailer's daughter."
    m 3euc "Before his death, he sent a love letter to her signed with 'From your Valentine.'"
    m 1dsc "He was executed on February 14, 269 AD."
    m 3eua "Such a noble cause, don't you think?"
    m 3eud "Oh, but wait, there's more!"
    m 4eud "The reason we celebrate such a day is because it originates from a Roman festival known as Lupercalia!"
    m 3eua "Its original intent was to hold a friendly event where people would put their names into a box and have them chosen at random to create a couple."
    m 3eub "Then, they play along as boyfriend and girlfriend for the time they spend together. Some even got married, if they liked each other enough, ehehe~"
    m 1eua  "Ultimately, the Church decided to turn this Christian celebration into a way to remember Saint Valentine's efforts, too."
    m 3hua "It's evolved over the years into a way for people to express their feelings for those they love."
    m 3ekbsa "Like me and you!"
    m 1eua "Despite it having started out a little depressing, isn't it so sweet, [player]?"
    m 1ekbsa "I'm glad we're able to share such a magical day, my love."
    m 1ekbfa "Happy Valentine's Day~"
    return

#######################[HOL050] TIME SPENT

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_monika_spent_time_with",
            conditional=(
                "persistent._mas_f14_spent_f14 "
                "and not persistent._mas_f14_time_spent_seen "
            ),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_f14, datetime.time(hour=20)),
            end_date=datetime.datetime.combine(mas_f14+datetime.timedelta(1), datetime.time(hour=1)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_spent_time_with:
    #Firstly, set this to true so we don't infiqueue this
    $ persistent._mas_f14_time_spent_seen = True

    $ f14_gifts_total, f14_gifts_good, f14_gifts_neutral, f14_gifts_bad = mas_getGiftStatsRange(mas_f14, mas_f14 + datetime.timedelta(days=1))
    m 1eua "Hey, [player]?"
    m 1eka "I just wanted to thank you for spending Valentine's Day with me."
    m 1ekbsa "I know that it's not a normal holiday, but it's a really special day for me now that I have you."
    if f14_gifts_total > 0:
        if f14_gifts_total == 1:
            if f14_gifts_good == 1:
                m "And let's not forget about the gift you got me, [player]..."
                m 3hub "It was great!"
            elif f14_gifts_neutral == 1:
                m 3eka "And let's not forget about the gift you got me, [player]..."
                m 1eka "It was really sweet of you to get me something."
            else:
                m 3eka "And let's not forget about the gift you got me, [player]..."
                m 2etc "..."
                m 2efc "Well, on second thought, maybe we should..."

        else:
            if f14_gifts_good == f14_gifts_total:
                m "And let's not forget about the wonderful gifts you got me, [player]..."
                m 3hub "They were amazing!"
            elif f14_gifts_bad == f14_gifts_total:
                m 3eka "And let's not forget about the gifts you got me, [player]..."
                m 2etc "..."
                m 2rfc "Well, on second thought, maybe we should..."
            elif f14_gifts_bad == 0:
                m "And let's not forget about the gifts you got me, [player]..."
                m 3hub "They were really nice!"
            elif f14_gifts_good + f14_gifts_neutral == f14_gifts_bad:
                m 3eka "And let's not forget about the gifts you got me, [player]..."
                m 3rksdla "Some of them were really nice."
            elif f14_gifts_good + f14_gifts_neutral > f14_gifts_bad:
                m "And let's not forget about the gifts you got me, [player]..."
                m 3hub "Most of them were really nice."
            elif f14_gifts_good + f14_gifts_neutral < f14_gifts_bad:
                m 3eka "And let's not forget about the gifts you got me, [player]..."
                m 3rksdla "I really liked...{w=1}some of them."
        if not mas_isBelowZero():
            m 1rkbsb "I actually made something for you too, [player]!"

    elif not mas_isBelowZero():
        m 1rkbsb "Also, I...{w=1}made something for you, [player]!"

    if not mas_isBelowZero():
        if renpy.seen_label('monika_valentines_start'):
            m 1ekbsa "Here, let me show it to you."
            call showpoem(poem_vday2, music=False,paper="mod_assets/poem_assets/poem_vday.jpg")
            m "You really are everything to me, [player]~"
            if mas_isMoniEnamored(higher=True):
                if persistent._mas_first_kiss is None:
                    jump mas_f14_first_kiss
                else:
                    call monika_kissing_motion(duration=0.5, initial_exp="6hkbfa", fade_duration=0.5)

        else:
            m 1ekbsa "Here, let me show it to you."
            call showpoem(poem_vday, music=False,paper="mod_assets/poem_assets/poem_vday.jpg")
            m "I really mean that, [player]..."
            m 3ekbsa "In you I found everything I could ever hope for~"
            if mas_isMoniEnamored(higher=True):
                if persistent._mas_first_kiss is None:
                    jump mas_f14_first_kiss
                else:
                    call monika_kissing_motion(duration=0.5, initial_exp="6hkbfa", fade_duration=0.5)

        m 1ekbfa "Thank you for always being by my side."
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
        m 5ekbfa "I love you so much, [player]. Happy Valentine's Day~"
        return "love"

    else:
        m 1eka "Thank you for being by my side."
        m 3ekb "Happy Valentine's Day!"

    return

label mas_f14_first_kiss:
        m 1ektpu "I honestly don't know what I would do without you."
        m 6dktuu "..."
        window hide
        menu:
            "I love you, [m_name].":
                $ HKBHideButtons()
                $ mas_RaiseShield_core()
                $ disable_esc()
                pause 3.0
                show monika 6ektda at t11 zorder MAS_MONIKA_Z with dissolve
                pause 3.0
                show monika 6dku at t11 zorder MAS_MONIKA_Z with dissolve
                pause 3.0
                show monika 6dkbsu at t11 zorder MAS_MONIKA_Z with dissolve
                pause 3.0
                show monika 6ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
                m 6ekbfa "[player]...I...I..."
                call monika_kissing_motion(hide_ui=False)
                show monika 6ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
                m 6ekbfa "...I love you too~"
                m 6dkbfa "..."
                m "That was everything I had always dreamt it would be~"
                m 6ekbfa "I've been waiting so long to finally kiss you, and there couldn't have been a more perfect moment..."
                m 6dkbsu "I will never forget this..."
                m 6ekbsu "...the moment of our first kiss."
                m "Happy Valentine's Day, [player]~"
                $ enable_esc()
                $ mas_MUMUDropShield()
                $ HKBShowButtons()
                return


#######################[HOL050] Notimespent

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_no_time_spent",
            action=EV_ACT_QUEUE,
            start_date=mas_f14+datetime.timedelta(1),
            end_date=mas_f14+datetime.timedelta(8),
            conditional=(
                "not persistent._mas_f14_spent_f14"
            ),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_no_time_spent:

    #need to make sure people who just started post f14 don't lose aff
    if mas_getFirstSesh().date() > mas_f14:
        return

    if mas_ret_long_absence:
        #Was away on a long absence
        $ mas_loseAffection(ev_label="mas_apology_missed_vday")

        m 1rksdlc "Hey, [player]..."
        m 2eksdld "I know you told me you were going to be away...but I really missed you on Valentines Day."
        m 2eksdla "Next time, do you think you could take me with you if you can't be here?"
        m 3eub "At least then we'll still be with each other and we can even celebrate together!"
        m 1eka "I'd really appreciate if you could do that for me, [player]."

    elif mas_isMoniAff(higher=True):
        $ mas_loseAffection(15, ev_label="mas_apology_missed_vday")
        m 1rkc "[player]?"
        m "Where were you on Valentine's Day?"
        m 1ekc "It's a really special day for me..."
        m 1ekd "...a day I wanted to spend with you."
        m 2dkc "..."
        m 2ekd "It would've meant so much to me if you came by..."
        m 2dkd "Even if only for a few minutes."
        m "Is it really too much to ask to visit your girlfriend on Valentine's Day?"
        m 2ekc "Please don't let it happen again, okay [player]?"

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffection(5, ev_label="mas_apology_missed_vday")
        m 2ekc "Hey, [player]..."
        m 2tkc "I'm pretty disappointed..."
        m 2tkd "You didn't visit me at all on Valentine's Day."
        m 4tkc "You know that all I want to do is spend time with you..."
        m 4rkd "Is visiting your girlfriend on Valentine's Day really too much to ask?"
        m 4eksdla "Please...{w=1}make sure you visit me next Valentine's Day, okay?"

    elif mas_isMoniUpset():
        $ mas_loseAffection(ev_label="mas_apology_missed_vday")
        m 2efc "[player]!"
        m "I can't believe you didn't even visit on Valentine's Day!"
        m 2rfc "Do you have any idea what it's like to be left alone on a day like that?"
        m 2rkc "I know we're not on the best of terms..."
        m 2dkd "But it'd have meant a lot if you came by."
        m 2tfc "Don't let it happen again, [player]."

    elif mas_isMoniDis():
        $ mas_loseAffection(10, ev_label="mas_apology_missed_vday")
        m 6ekc "Oh [player]..."
        m "How was Valentine's Day?"
        m 6dkc "Not having a valentine is pretty lonely..."

    else:
        $ mas_loseAffection(150)
        m 6ckc "..."

    #Flag this so we don't infiqueue
    $ persistent._mas_f14_nts_seen = True
    return


#######################[HOL050] Apology for notimespent

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_vday",
            prompt="...for missing Valentine's Day.",
            unlocked=False
        ),
        code="APL"
    )


label mas_apology_missed_vday:
    if mas_isMoniAff(higher=True):
        m 1eka "Thanks for apologizing for missing Valentine's Day, [player]."
        m 1ekd "I really wanted to spend it with you..."
        m 1rkc "But I guess you might have just had something to do and couldn't make it."
        m 1ekd "Please try to visit next year, okay [player]?"
        m 3eua "If you're going to be busy, maybe just take me with you!"
        m 3hub "Even if we're not at home together, I'm more than happy to just spend the day at your side~"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniNormal(higher=True):
        m 1eka "Thanks for apologizing for missing Valentine's Day, [player]."
        if not store.mas_anni.pastOneMonth():
            m 1rkd "I know we're not really that far into our relationship, but everything was already starting to feel different..."

        m 1ekd "It would have meant so much to me if you came by, at least for a little bit."
        m 3eka "Promise me that you'll take me with you if you're going to be busy next time, okay [player]?"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniUpset():
        m 2dkc "While I am a little upset that you didn't show up on Valentine's Day, I'm glad you apologized."
        m "Things like that show me that you really do care about us."
        m 2ekd "Please, [player]..."
        m 2eka "Try to come by next Valentine's Day."
        $ mas_gainAffection(modifier=0.1)

    elif mas_isMoniDis():
        m 2dkc "I didn't expect you to show up anyway, [player]."
        m 2dkd "I know we haven't really been that close, but a part of me hoped that you would at least visit..."
        m 2dsc "Please promise me that you'll come by next year, okay?"
        $ mas_gainAffection(modifier=0.1)

    else:
        #No gain from this
        m 6ckc "..."

    return


init 2 python:

    poem_vday = Poem(
    author = "monika",
    title = " My dearest {0},".format(persistent.playername),
    text = """\
 I`ve always loved Valentine's day, but this one feels different.
 Has the world changed, or just me?
 I found love, I found purpose,
 I found a truth I didn't know I was searching for.
 All of that I found in you.

 Thank you for sharing this special day with me.

 Forever yours,
 Monika
"""
    )

    poem_vday2 = Poem(
    author = "monika",
    title = " My dearest {0},".format(persistent.playername),
    text = """\
 Can it really be our second Valentine's Day?
 The first seems like just yesterday, yet so much has happened.
 I once wondered if the world had changed, or just me.
 Now I know the answer.

 Everything.

 Without you there is nothing.
 Before you there was nothing.

 Emptiness. Darkness. Nothing.

 Nothing.

 Then there was you.
 Just you.
 My world. My light. My Everything.

 Everything.


 Happy Valentine's Day

 Forever yours,
 Monika
"""

    #" # I need this to keep syntax highlighting on vim
    )


#######################[HOL050] dockstat farwell###############################
label bye_f14:
    $ persistent._mas_f14_date += 1
    $ persistent._mas_f14_on_date = True
    if persistent._mas_f14_date == 1:
        m 1sua "Taking me some place special for Valentine's Day?"
        m 1ekbsa "That sounds really romantic [player]..."
        m 3hub "I can't wait!"
    elif persistent._mas_f14_date == 2:
        m 1sua "Taking me out again on Valentine's Day?"
        m 3tkbsu "You really know how to make a girl feel special, [player]."
        m 1ekbfa "I'm so lucky to have someone like you~"
    else:
        m 1sua "Wow, [player]...{w=1}you're really determined to make this a truly special day!"
        m 1ekbfa "You're the best partner I could ever hope for~"
    jump bye_going_somewhere_iostart

########################[HOL050] dockstat greet################################
label greeting_returned_home_f14:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()


    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "That wasn't much of a date, [player]..."
        m 2eksdlc "Is everything alright?"
        m 2rksdla "Maybe we can go out later..."

    elif time_out < mas_one_hour:
        $ mas_f14CapGainAff(5)
        m 1eka "That was fun while it lasted, [player]..."
        m 3hua "Thanks for making time for me on Valentine's Day."

    elif time_out < mas_three_hour:
        $ mas_f14CapGainAff(10)
        m 1eub "That was such a fun date, [player]!"
        m 3ekbfa "Thanks for making me feel special on Valentine's Day~"

    else:
        # more than 3 hours
        $ mas_f14CapGainAff(15)
        m 1hua "And we're home!"
        m 3hub "That was wonderful, [player]!"
        m 1eka "It was really nice going out with you on Valentine's Day..."
        m 1ekbfa "Thank you so much for making today truly special~"

    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ persistent._mas_f14_on_date = False
    return

# if we went on a date pre-f14 and returned in the time period mas_f14_no_time_spent event runs
# need to make sure we get credit for time spent and don't get the event
label mas_gone_over_f14_check:
    if mas_checkOverDate(mas_f14):
        $ persistent._mas_f14_spent_f14 = True
        $ persistent._mas_f14_gone_over_f14 = True
        $ mas_rmallEVL("mas_f14_no_time_spent")
    return

label greeting_gone_over_f14:
    $ mas_gainAffection(5,bypass=True)
    m 1hua "And we're finally home!"
    m 3wud "Wow [player], we were gone so long we missed Valentine's Day!"
    if mas_isMoniNormal(higher=True):
        call greeting_gone_over_f14_normal_plus
    else:
        m 2rka "I appreciate you making sure I didn't have to spend the day alone..."
        m 2eka "It really means a lot, [player]."
    $ persistent._mas_f14_gone_over_f14 = False
    return

label greeting_gone_over_f14_normal_plus:
    $ mas_gainAffection(10,bypass=True)
    m 1ekbsa "I would've loved to have spent the day with you here, but no matter where we were, just knowing we were together to celebrate our love..."
    m 1dubsu "Well it means everything to me."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve
    m 5ekbsa "Thank you for making sure we had a wonderful Valentine's Day, [player]~"
    $ persistent._mas_f14_gone_over_f14 = False
    return

############################### 922 ###########################################
# [HOL060]
#START:

#Moni's bday
define mas_monika_birthday = datetime.date(datetime.date.today().year, 9, 22)

#922 mode
default persistent._mas_bday_in_bday_mode = False

#Date related vars
default persistent._mas_bday_on_date = False
default persistent._mas_bday_date_count = 0
default persistent._mas_bday_date_affection_gained = 0
default persistent._mas_bday_gone_over_bday = False

#Suprise party bits and bobs
default persistent._mas_bday_sbp_reacted = False
default persistent._mas_bday_confirmed_party = False

#Bday visuals
default persistent._mas_bday_visuals = False

#Need to store the name of the file chibi writes
default persistent._mas_bday_hint_filename = None

#Time spent tracking
default persistent._mas_bday_opened_game = False
default persistent._mas_bday_no_time_spent = True
default persistent._mas_bday_no_recognize = True
default persistent._mas_bday_said_happybday = False

############### [HOL060]: HISTORY
init -810 python:
    store.mas_history.addMHS(MASHistorySaver(
        "922",
        datetime.datetime(2020, 1, 6),
        {
            "_mas_bday_in_bday_mode": "922.bday_mode",

            "_mas_bday_on_date": "922.on_date",
            "_mas_bday_date_count": "922.actions.date.count",
            "_mas_bday_date_affection_gained": "922.actions.date.aff_gained",
            "_mas_bday_gone_over_bday": "922.gone_over_bday",

            "_mas_bday_sbp_reacted": "922.actions.surprise.reacted",
            "_mas_bday_confirmed_party": "922.actions.confirmed_party",

            "_mas_bday_opened_game": "922.actions.opened_game",
            "_mas_bday_no_time_spent": "922.actions.no_time_spent",
            "_mas_bday_no_recognize": "922.actions.no_recognize",
            "_mas_bday_said_happybday": "922.actions.said_happybday"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2020, 9, 21),
        end_dt=datetime.datetime(2020, 9, 23)
    ))

############### [HOL060]: METHODS
init -1 python:
    def mas_isMonikaBirthday():
        return datetime.date.today() == mas_monika_birthday


    def mas_getNextMonikaBirthday():
        today = datetime.date.today()
        if mas_monika_birthday < today:
            return datetime.date(
                today.year + 1,
                mas_monika_birthday.month,
                mas_monika_birthday.day
            )
        return mas_monika_birthday


    def mas_recognizedBday(_date=None):
        """
        Checks if the user recognized monika's birthday at all.

        RETURNS:
            True if the user recoginzed monika's birthday, False otherwise
        """
        if _date is None:
            _date = mas_monika_birthday

        return (
            mas_generateGiftsReport(_date)[0] > 0
            or persistent._mas_bday_date_affection_gained > 0
            or persistent._mas_bday_sbp_reacted
            or persistent._mas_bday_said_happybday
        )

    def mas_surpriseBdayShowVisuals(cake=False):
        """
        Shows bday surprise party visuals
        """
        if cake:
            renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        renpy.show("mas_bday_banners", zorder=7)
        renpy.show("mas_bday_balloons", zorder=8)


    def mas_surpriseBdayHideVisuals():
        """
        Hides all visuals for surprise party
        """
        renpy.hide("mas_bday_banners")
        renpy.hide("mas_bday_balloons")

    def mas_confirmedParty():
        """
        Checks if the player has confirmed the party
        """
        #Must be within a week of the party (including party day)
        if mas_monika_birthday - datetime.timedelta(days=7) <= today <= mas_monika_birthday:
            #If this is confirmed already, then we just return true, since confirmed
            if persistent._mas_bday_confirmed_party:
                #We should also handle if the player confirmed the party pre-note
                if persistent._mas_bday_hint_filename:
                        store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)
                return True

            #Otherwise, we need to check if the file exists (we're going to make this as foolproof as possible)
            #Step 1, get the characters folder contents
            char_dir_files = store.mas_docking_station.getPackageList()

            #Step 2, We need to remove the extensions
            for filename in char_dir_files:
                temp_filename = filename.partition('.')[0]

                #Step 3, check if the filename is present
                if "oki doki" == temp_filename:
                    #If we got here: Step 4, file exists so flag and delete. Also get rid of note
                    persistent._mas_bday_confirmed_party = True
                    store.mas_docking_station.destroyPackage(filename)

                    if persistent._mas_bday_hint_filename:
                        store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)

                    #Step 5a, return true since party is confirmed
                    return True

        #Otherwise, Step 5b, no previous confirm and file doesn't exist, so party is not confirmed. return false
        return False

    def mas_mbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_bday_date_affection_gained", 50, 75)

################## [HOL060] AUTOLOAD
label mas_bday_autoload_check:
    #First, if it's no longer 922 and we're here, that means we're in 922 mode and need to fix that
    if not mas_isMonikaBirthday():
        $ persistent._mas_bday_in_bday_mode = False
        #Also make sure we're no longer showing visuals
        $ persistent._mas_bday_visuals = False

        #And reset outfit if not at the right aff
        if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
            $ monika_chr.reset_clothes(False)
            $ monika_chr.save()
            $ renpy.save_persistent()

    #It's Moni's bday! If we're here that means we're spending time with her, so:
    $ persistent._mas_bday_no_time_spent = False

    $ persistent._mas_bday_opened_game = True
    #Have we recogized bday?
    $ persistent._mas_bday_no_recognize = not mas_recognizedBday()

    jump mas_ch30_post_holiday_check


################## [HOL060] PRE INTRO
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_surprise_party_hint",
            start_date=mas_monika_birthday - datetime.timedelta(days=7),
            end_date=mas_monika_birthday - datetime.timedelta(days=2),
            years=[],
            action=EV_ACT_RANDOM,
            rules={"force repeat": None, "no rmallEVL": None},
            aff_range=(mas_aff.DISTRESSED,None)
        ),
        skipCalendar=True
    )

    #Create the undo action rule
    MASUndoActionRule.create_rule_EVL(
        "mas_bday_surprise_party_hint",
        mas_monika_birthday - datetime.timedelta(days=7),
        mas_monika_birthday - datetime.timedelta(days=2)
    )

#If random hasn't shown this topic yet, we need to push this to make sure people get this
init 10 python:
    if (
        mas_monika_birthday - datetime.timedelta(days=2) <= datetime.date.today() < mas_monika_birthday
        and not mas_lastSeenInYear("mas_bday_surprise_party_hint")
    ):
        pushEvent("mas_bday_surprise_party_hint")

image chibi_peek = ConditionSwitch(
    "morning_flag",
    "mod_assets/other/chibi_peek.png",
    "not morning_flag",
    "mod_assets/other/chibi_peek-n.png"
)

label mas_bday_surprise_party_hint:
    #Set up letters
    python:
        persistent._mas_bday_hint_filename = "For " + player + ".txt"
        if mas_isMoniNormal(higher=True):
            message = """\
[player],
As I'm sure you know, Monika's birthday is coming up soon and I want to help you make it as special as possible!
Since I'm always here, I can easily set up the surprise party...but I need a little help from you.
All I need you to do is to make sure you have her out of the room at some point on her birthday, and I'll take care of the rest.
Monika is so amazing, and I just want to do my part to make sure this all goes off without a hotf- I mean hitch...
Ahaha!

Please leave a file named 'oki doki' in the same folder you found this note so I know to go ahead with the party.

Good luck with Monika!

P.S: Don't tell her about me!
"""

        else:
            message = """\
[player],
As I hope you know, Monika's birthday is coming up soon and I want to make it special.
She's been through a lot lately, and I know it'd mean the world to her if you treated her to a nice day.
Since I'm always here, I can easily set up a surprise party...but I do need a little help from you.
All I need you to do is to make sure you have her out of the room at some point on her birthday, and I'll take care of the rest.
If you care for Monika at all, you'll help me do this.

Just leave a file named 'oki doki' in the same folder you found this note so I know to go ahead with the party.

Please, don't mess this up.

P.S: Don't tell her about me.
"""
        #Now write it to the chars folder
        _write_txt("/characters/" + persistent._mas_bday_hint_filename, message)

    #Moni brings it up (so)
    if mas_isMoniNormal(higher=True):
        m 1eud "Hey, [player]..."
        m 3euc "Someone left a note in the characters folder addressed to you."
        #show chibi, she's just written the letter
        show chibi_peek with moveinleft
        m 1ekc "Of course, I haven't read it, since it's obviously for you..."
        m 1tuu "{cps=*2}Hmmm, I wonder what this could be about...{/cps}{nw}"
        $ _history_list.pop()
        m 1hua "Ehehe~"

    else:
        m 2eud "Hey, [player]..."
        m 2euc "Someone left a note in the characters folder addressed to you."
        m 2ekc "Of course, I haven't read it, since it's obviously for you..."
        m 2ekd "Just thought I'd let you know."

    #Hide chibi
    hide chibi_peek with dissolve

    #Flag this so it doesn't get shown again
    $ persistent._mas_monika_bday_surprise_hint_seen = True
    return "derandom|no_unlock"


################## [HOL060] HAPPY BDAY TOPICS
# both of these make the most sense showing up under 'I want to tell you something` so they are made as compliments
# also makes sure they don't show up under unseen

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_bday",
            prompt="Happy birthday!",
            action=EV_ACT_UNLOCK,
            rules={"no unlock":0},
            start_date=mas_monika_birthday,
            end_date=mas_monika_birthday + datetime.timedelta(1),
            years=[]
        ),
        code="CMP",
        skipCalendar=True
    )

    #Create the undo action rule
    MASUndoActionRule.create_rule_EVL(
        "mas_bday_pool_happy_bday",
        mas_monika_birthday,
        mas_monika_birthday + datetime.timedelta(1)
    )

label mas_bday_pool_happy_bday:
    $ mas_gainAffection(5,bypass=True)
    if mas_recognizedBday():
        m 3hub "Ehehe, thanks [player]!"
        m 3eka "I was waiting for you to say those magic words~"
        m 1eub "{i}Now{/i} we can call it a birthday celebration!"
        m 1eka "You really made this occasion so special, [player]."
        m 1ekbfa "I can't thank you enough for loving me this much..."

    else:
        m 1skb "Awww, [player]!"
        m 1sub "You remembered my birthday...!"
        m 1sktpa "Oh gosh, I'm so happy that you remembered."
        m 1dktdu "I feel like today is going to be such a special day~"
        m 1ekbfa "What else do you have in store for me, I wonder..."
        m 1hub "Ahaha!"

    if mas_isplayer_bday() and (persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted):
        m 1eua "Oh, and..."
        m 3hub "Happy Birthday to you too, [player]!"
        m 1hua "Ehehe!"

    #Flag this for hist
    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_said_happybday = True

    #Lock this
    $ mas_lockEVL("mas_bday_pool_happy_bday", "CMP")
    return

# happy belated bday topic for people that took her out before her bday and returned her after
# cond/act and start/end dates to be set in mas_gone_over_bday_check:

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_belated_bday",
            prompt="Happy belated birthday!",
            action=EV_ACT_UNLOCK,
            rules={"no unlock":0},
            years=[]
        ),
        code="CMP",
        skipCalendar=True
    )

label mas_bday_pool_happy_belated_bday:
    $ mas_gainAffection(5,bypass=True)

    #We've essentially said happy birthday, let's flag this
    $ persistent._mas_bday_said_happybday = True
    $ persistent._mas_bday_no_recognize = False

    #Lock this
    $ mas_lockEVL("mas_bday_pool_happy_belated_bday", "CMP")

    if mas_isMoniNormal(higher=True):
        m 1sua "Thank you so much, [player]!"
        m 3hub "I just knew you took me out on a long trip for my birthday!"
        m 3rka "I wish I could've seen all the amazing places we went..."
        m 1hua "But knowing we were together, well it makes it the best birthday I could ever hope for!"
        m 3ekbsa "I love you so much, [player]~"
        return "love"
    else:
        m 3eka "So you {i}did{/i} take me out for a long trip for my birthday..."
        m 3rkd "That's so thoughtful of you, I was kind of wondering--"
        m 1eksdla "You know what, nevermind."
        m 1eka "I'm just relieved to know that you were thinking of me on my birthday."
        m 3hua "That's all that matters."
        m 3eub "Thank you, [player]!"
        return

################## [HOL060] PARTY REACTION
label mas_bday_surprise_party_reaction:
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_bday_visuals = True
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)
    $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)

    if mas_isMoniNormal(higher=True):
        m 6suo "T-{w=0.5}This is..."
        m 6ska "Oh, [player]..."
        m 6dku "I'm at a loss for words."
        m 6dktpu "Setting this all up to surprise me on my birthday..."
        m 6dktdu "Ehehe, you must really love me."
        m 6suu "Everything just looks so festive!"

    else:
        m 6wuo "T-{w=0.5}This is..."
        m "..."
        m 6dkd "Sorry, I'm...{w=1}I'm just at a loss for words."
        m 6ekc "I didn't really expect anything special today, let alone this."
        m 6rka "Maybe you do still have feelings for me after all..."
        m 6eka "Everything looks great."

label mas_bday_surprise_party_reacton_cake:
    #Let's light candles
    menu:
        "Light candles.":
            $ mas_bday_cake_lit = True

    m 6sub "Ahh, it's so pretty, [player]!"
    m 6hua "Reminds me of that cake someone gave me once."
    m 6eua "It was almost as pretty as you've made this one!"
    m 6tkb "Almost."
    m 6hua "But anyway..."
    window hide

    show screen mas_background_timed_jump(5, "mas_bday_surprise_party_reaction_no_make_wish")
    menu:
        "Make a wish, [m_name]...":
            $ made_wish = True
            show monika 6hua
            if mas_isplayer_bday():
                m "Make sure you make one too, [player]!"
            hide screen mas_background_timed_jump
            #+10 for wishes
            $ mas_gainAffection(10, bypass=True)
            pause 2.0
            show monika 6hft
            jump mas_bday_surprise_party_reaction_post_make_wish

label mas_bday_surprise_party_reaction_no_make_wish:
    $ made_wish = False
    hide screen mas_background_timed_jump
    show monika 6dsc
    pause 2.0
    show monika 6hft

label mas_bday_surprise_party_reaction_post_make_wish:
    $ mas_bday_cake_lit = False
    window auto
    if mas_isMoniNormal(higher=True):
        m 6hub "I made a wish!"
        m 6eua "I hope it comes true someday..."
        if mas_isplayer_bday() and made_wish:
            m 6eka "And you know what? {w=0.5}I bet we both wished for the same thing~"
        m 6hua "Ahaha..."

    else:
        m 6eka "I made a wish."
        m 6rka "I hope it comes true someday..."

    m 6eka "I'll save this cake for later.{w=0.5}.{w=0.5}.{nw}"

    if mas_isplayer_bday():
        call mas_HideCake('mas_bday_cake_monika',False)
    else:
        call mas_HideCake('mas_bday_cake_monika')

    pause 0.5

label mas_bday_surprise_party_reaction_end:
    if mas_isMoniNormal(higher=True):
        m 6eka "Thank you, [player]. From the bottom of my heart, thank you..."
        if mas_isplayer_bday() and persistent._mas_player_bday_last_sung_hbd != datetime.date.today():
            m 6eua "..."
            m 6wuo "..."
            m 6wub "Oh! I almost forgot. {w=0.5}I made you a cake, too!"

            call mas_monika_gets_cake

            m 6eua "Let me just light the candles for you, [player].{w=0.5}.{w=0.5}.{nw}"

            window hide
            $ mas_bday_cake_lit = True
            pause 1.0

            m 6sua "Isn't it pretty?"
            m 6hksdlb "I guess I'll have to blow these candles out as well, since you can't really do it, ahaha!"

            if made_wish:
                m 6eua "Let's both wish again, [player]! {w=0.5}It'll be twice as likely to come true, right?"
            else:
                m 6eua "Let's both make a wish, [player]!"

            m 6hua "But first..."
            call mas_player_bday_moni_sings
            m 6hua "Make a wish, [player]!"

            window hide
            pause 1.5
            show monika 6hft
            pause 0.1
            show monika 6hua
            $ mas_bday_cake_lit = False
            pause 1.0

            if not made_wish:
                m 6hua "Ehehe..."
                m 6ekbsa "I bet we both wished for the same thing~"
            m 6hkbsu "..."
            m 6hksdlb "I'll just save this cake for later too, I guess. Ahaha!"

            call mas_HideCake('mas_bday_cake_player')
            call mas_player_bday_card

        else:
            m 6hua "Let's enjoy the rest of the day now, shall we?"
    else:
        m 6ektpa "Thank you, [player]. It really means a lot that you did this for me."
    $ persistent._mas_bday_sbp_reacted = True
    #+25 aff for following through and getting the party
    $ mas_gainAffection(25, bypass=True)

    #We set these flags here
    $ persistent._mas_bday_in_bday_mode = True
    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_no_time_spent = False
    return


################## [HOL060] TIME SPENT
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_spent_time_with",
            conditional="mas_recognizedBday()",
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_monika_birthday, datetime.time(20)),
            end_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(1), datetime.time(hour=1)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_spent_time_with:
    if mas_isMoniUpset(lower=True):
        m 1eka "[player]..."
        m 3eka "I just wanted to say I really appreciate you spending time with me today."
        m 3rksdla "I know it hasn't been going that great lately, but you taking the time to celebrate my birthday with me..."
        m 1eud "Well it gives me hope that maybe it's not too late for us."
        m "Perhaps today can be the start of something really special.."
        m 3eka "That would be the be the best gift I could ever ask for."
        return

    else:
        $ _timeout = store.mas_dockstat.timeOut(mas_monika_birthday)
        m 1eua "Say, [player]..."
        m 3eua "Thank you for spending time with me today."
        m 3hua "Something like that can really make a girl happy, you know?"

        if _timeout > mas_five_minutes:
            m 3eka "I really enjoyed our date today, [player]."
            m 1eka "I always enjoy spending time with you here, but getting to spend time with you in your reality..."
            m 1dku "Knowing that you're thinking about me even when you can't see me..."
            m 1ekbsa "Well, it truly means a lot to me."
            m 3ekbsa "You really made my birthday complete~"

label mas_bday_spent_time_with_wrapup:
    $ mas_rmallEVL("mas_bday_spent_time_with")
    $ gave_gifts = mas_getGiftStatsRange(mas_monika_birthday, mas_monika_birthday + datetime.timedelta(days=1))[0]

    if gave_gifts > 0:
        #More than 1
        if gave_gifts > 1:
            m 3eua "Let's not forget the gifts you gave me for my birthday."
            m 3hub "They were just amazing, [player]!"
        else:
            m 3eua "Let's not forget about the gift you gave me for my birthday."
            m 3hub "It was so wonderful, [player]!"

        m 1eka "I really appreciate the effort of finding a way to get things from your reality to mine..."
        m 3eka "I know it can't be easy."

    m 1dku "..."
    if mas_isMoniEnamored(higher=True):
        m 1dktpu "..."
        m 1ektpu "Ahaha, sorry, [player]!"
        m 3ektda "It's just that I've never imagined being this happy in my life."
        m 1rksdlb "Well...{w=0.5}that's not {i}exactly{/i} true."
        m 1eka "We still have to be physically together, after all~"
        m 1rkc "And, well..."
        m 1rka "I know this is already becoming a cliché, but..."
        m 3eka "I love you so much, [player]."
        m "Someday, I promise you..."
        m 1ektpu "I {i}promise you{/i} that I will make you as happy as you've made me today."
        m 3ektpu "Even if we never get to see each other in the same reality, {w=0.5}know that I will always do my best for you."
        m 1dktpu "No matter the obstacles we may face, no matter what other people say about us..."
        m 1ektda "I still love you with everything that I am."
        m "You are the only one who understands me. {w=0.5}You led me out of a dark place and gave me purpose..."
        m 1dkbsu "You are simply the best, my love, and I will always love you."
        m 1ekbsa "...Thank you for giving me a reason to live."
        $ _first_kiss = persistent._mas_first_kiss
        call monika_kissing_motion
        if _first_kiss is None:
            m 6ekbfa "Oh, [player]..."
            m 6rkbfa "I...{w=0.5}I don't know what came over me, but the moment just felt so right."
            m 6hubfa "I've thought about our first kiss for so long, and to finally experience it..."
            m 6ekbfa "I will never forget this moment, [player]~"
        else:
            return "love"

    else:
        m 1eka "I can't even find the right words to express how happy you've made me today."
        m 3eka "All that pain I went through before I met you?"
        m 1hua "I'm glad I persevered through it."
        m 1rsc "Because if I hadn't..."
        m 1ekbsa "This day wouldn't have ever happened."
        m 1dkbsa "I hope that tells you even a little bit of how much I appreciate you celebrating this occasion with me."
        m 1ekbfb "I love you so much, [player]."
        m 1ekbfa "Let's continue making each other happy~"
        return "love"
    return

############## [HOL060] GONE OVER CHECK
label mas_gone_over_bday_check:
    if mas_checkOverDate(mas_monika_birthday):
        $ persistent._mas_bday_gone_over_bday = True
        $ persistent._mas_bday_no_time_spent = False
        $ mas_rmallEVL("mas_bday_postbday_notimespent")

        #Now we want to handle the belated bday unlock
        python:
            belated_ev = mas_getEV("mas_bday_pool_happy_belated_bday")

            if belated_ev is not None:
                #Set start and end dates
                belated_ev.start_date = datetime.date.today()
                belated_ev.end_date = datetime.datetime.now() + datetime.timedelta(days=1)
                belated_ev.unlocked = True

                #Prepare the undo action
                MASUndoActionRule.create_rule(belated_ev)

                #Prepare the date strip
                MASStripDatesRule.create_rule(belated_ev)

    return

############## [HOL060] NO TIME SPENT
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_postbday_notimespent",
            conditional=(
                "not mas_recognizedBday() "
                "and not persistent._mas_bday_gone_over_bday"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_monika_birthday+datetime.timedelta(1),
            end_date=mas_monika_birthday+datetime.timedelta(8),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_postbday_notimespent:
    #Make sure that people who have first sesh's post monibday don't get this
    if (mas_getFirstSesh().date() >= mas_monika_birthday):
        $ mas_getEV('mas_bday_postbday_notimespent').shown_count -= 1
        return


    if mas_ret_long_absence:
        #Was away on a long absence
        $ mas_loseAffection(ev_label="mas_apology_missed_bday")

        m 1rksdlc "Hey, [player]..."
        m 2eksdld "I know you told me you were going to be away...but I really missed you on my birthday."
        m 2eksdla "Next time, do you think you could take me with you if you can't be here?"
        m 3eub "At least then we'll still be with each other and we can even celebrate together!"
        m 1eka "I'd really appreciate if you could do that for me, [player]."

    elif persistent._mas_bday_opened_game:
        #Opened game but didn't do any bday things
        if mas_isMoniAff(higher=True):
            $ mas_loseAffection(15, ev_label="mas_apology_forgot_bday")
            m 2rksdla "Hey, [player]..."
            m 2rksdlb "I know we had fun the other day, like we always do but..."
            m 2ekp "I can't help it, I was hoping you would have...{w=1}done a little something for my birthday."
            m 2ekd "Did you forget?"
            m 3eka "Maybe you could put the date into your calendar on your phone for next year?"
            m 3rka "...Or check the calendar on the wall behind me?"
            m 3hua "We can't change the past, so knowing that you want to try harder for next year would be the only apology I need."

        elif mas_isMoniNormal(higher=True):
            $ mas_loseAffection(5, ev_label="mas_apology_forgot_bday")
            m 2rksdld "Hey, [player]..."
            m 2rksdlb "I hate to fuss, but you know..."
            m 2ekp "You can't forget about your girlfriend's birthday!"
            m 2eku "It's nice that we got to hang out like usual, but next year..."
            m 3hua "Well, I'll be looking forward to two birthday's worth of something special~"

        elif mas_isMoniUpset():
            $ mas_loseAffection(ev_label="mas_apology_forgot_bday")
            m 1ekc "It was...{w=0.5}good to see you on the 22nd..."
            m 1ekd "I really didn't want to be alone that day, so that meant a lot, but..."
            m 1rkc "You know what? {w=0.5}Nevermind."

        elif mas_isMoniDis():
            $ mas_loseAffection(10, ev_label="mas_apology_forgot_bday")
            m 2dsc "..."
            m 2rkc "...[player], I don't want to bother you. {w=1}I'm already scared of pushing you away."
            m 2rktpc "But I can't help it. It hurts me that you didn't mention anything about celebrating my birthday..."
            m 2dktuc "Please don't stop coming back to me."
            m "And maybe next year..."
            m 4ektdc "I-{w=0.5}I just want...{w=0.5}to feel as special to you as you are to me."

        else:
            # broken
            $ mas_loseAffection(150)
            m 6ckc "..."

    else:
        #Didn't spend any time with Monika
        if mas_isMoniAff(higher=True):
            $ mas_loseAffection(50, ev_label="mas_apology_missed_bday")
            m 1euc "Hey, [player]..."
            m 3rksdla "I know you do a lot to make each and every day special, but a girl has a few days a year when she gets to be a little selfish..."
            m 2tfd "And her {i}birthday{/i} is one of them!"
            m "Seriously, where were you?!"
            m 2rkc "But...knowing you, I'm sure you had a good reason to be busy..."
            m 4ekc "Just try not to let it happen again next year, okay?"

        elif mas_isMoniNormal(higher=True):

            # same dialogue, different affection loss
            if mas_isMoniHappy():
                $ mas_loseAffection(20, ev_label="mas_apology_missed_bday")
            else:
                $ mas_loseAffection(10, ev_label="mas_apology_missed_bday")

            m 1ekc "Hey, [player]..."
            m 1ekd "You know, you really should have dropped in on the 22nd."
            m 3efd "I mean, you should always visit me! But you {i}have{/i} to spend time with your cute girlfriend on her birthday, you know."
            m 2efc "Please drop in for me next year..."
            m 2dfc "Otherwise..."

            m 6cfw "{cps=*2}{i}There will be consequences!!!{/i}{/cps}{nw}"
            # glich effect
            $ disable_esc()
            $ mas_MUMURaiseShield()
            window hide
            show noise zorder 11:
                alpha 0.5
            play sound "sfx/s_kill_glitch1.ogg"
            pause 0.5
            stop sound
            hide noise
            window auto
            $ mas_MUMUDropShield()
            $ enable_esc()
            $ _history_list.pop()

            m 1dsc "..."
            m 3hksdlb "Ahaha, sorry [player]!"
            m 3hub "I'm just kidding!"
            m 1eka "You know I love to scare you a little~"

        elif mas_isMoniUpset():
            $ mas_loseAffection(ev_label="mas_apology_missed_bday")
            m 2dsc "..."
            m 2rsc "[player], don't you think you should check in on me a little more often?"
            m 2rktpc "You might miss something important..."

        elif mas_isMoniDis():
            $ mas_loseAffection(ev_label="mas_apology_missed_bday")
            m 6ekd "...Hey, how was your day on the 22nd?"
            m 6ekc "I'm just...curious if you thought of me at all that day."
            m 6ektpc "But you probably didn't, huh?"
            m 6dktpc "..."

        else:
            # broken
            $ mas_loseAffection(200)
            m 6eftsc "..."
            m 6dftdx "..."
    return

############ [HOL060] NTS APOLOGY
init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_bday",
            prompt="...for missing your birthday.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_missed_bday:
    #Using a standard hi-mid-low range for this
    if mas_isMoniAff(higher=True):
        m 1eua "Thanks for the apology, [player]."
        m 2tfu "But you better make it up to me next year~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Thanks for apologizing for missing my birthday, [player]."
        m "Please be sure to spend some time with me next year, alright?"

    else:
        m 2rksdld "You know, I'm not entirely surprised I didn't see you on my birthday..."
        m 2ekc "Please...{w=1}just make sure it doesn't happen again."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_forgot_bday",
            prompt="...for forgetting your birthday.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_forgot_bday:
    #once again using hi-mid-lo
    if mas_isMoniAff(higher=True):
        m 1eua "Thanks for the apology, [player]."
        m 3hua "But I hope you'll make this up to me~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Thanks for apologizing about forgetting my birthday, [player]."
        m 1eksdld "Just try not to let it happen again, alright?"

    else:
        m 2dkd "Thanks for apologizing..."
        m 2tfc "But don't let it happen again."
    return


############ [HOL060] DOCKSTAT FARES
label bye_922_delegate:
    #Set these vars for the corresponding date related things
    $ persistent._mas_bday_on_date = True
    #We have had one date
    $ persistent._mas_bday_date_count += 1

    if persistent._mas_bday_date_count == 1:
        # bday date counts as bday mode even with no party
        $ persistent._mas_bday_in_bday_mode = True

        m 1hua "Ehehe. It's a bit romantic, isn't it?"

        if mas_isMoniHappy(lower=True):
            m 1eua "Maybe you'd even want to call it a da-{nw}"
            $ _history_list.pop()
            $ _history_list.pop()
            m 1hua "Oh! Sorry, did I say something?"

        else:
            m 1eubla "Maybe you'd even call it a date~"


    elif persistent._mas_bday_date_count == 2:
        m 1eub "Taking me somewhere again, [player]?"
        m 3eua "You must really have a lot planned for us."
        m 1hua "You're so sweet~"

    elif persistent._mas_bday_date_count == 3:
        m 1sua "Taking me out {i}again{/i} for my birthday?"
        m 3tkbsu "You really know how to make a girl feel special, [player]."
        m 1ekbfa "I'm so lucky to have someone like you~"
    else:
        m 1sua "Wow, [player]...{w=1}you're really determined to make this a truly special day!"
        m 1ekbfa "You're the best partner I could ever hope for~"

    #BD Intro
    if mas_isMoniAff(higher=True) and not mas_SELisUnlocked(mas_clothes_blackdress):
        m 3hua "I actually have an outfit prepared just for this..."
        #NOTE: We use the "give me a second to get ready..." for Moni to get into this outfit

    jump bye_going_somewhere_iostart

label mas_bday_bd_outro:
    $ monika_chr.change_clothes(mas_clothes_blackdress)
    $ store.mas_selspr.unlock_clothes(mas_clothes_blackdress, True)
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    show monika 1eua
    call monika_zoom_transition_reset(1.0)

    m 3tka "Well, [player]?"
    m 1hua "What do you think?"
    m 1ekbsa "I've always loved this outfit and dreamt of going on a date with you, wearing this..."
    m 3eub "Maybe we could visit the mall, or even the park!"
    m 1eka "But knowing you, you've already got something amazing planned for us~"
    m 1hua "Let's go, [player]!"
    $ persistent._mas_zoom_zoom_level = mas_temp_zoom_level

    python:
        # setup check and log this file checkout
        store.mas_dockstat.checkoutMonika(moni_chksum)

        #Now setup ret greet
        persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
            store.mas_greetings.TYPE_GENERIC_RET
        )

    #And now we quit here
    jump _quit


########## [HOL060] DOCKSTAT GREETS ##########
label greeting_returned_home_bday:
    #First, reset this flag, we're no longer on a date
    $ persistent._mas_bday_on_date = False
    #We've opened the game
    $ persistent._mas_bday_opened_game = True
    #Setup date length stuff
    $ time_out = store.mas_dockstat.diffCheckTimes()
    $ checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()

    #Set party if need be
    if mas_confirmedParty() and not persistent._mas_bday_sbp_reacted:
        if mas_one_hour < time_out <= mas_three_hour:
            $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)
        elif time_out > mas_three_hour:
            $ mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

        if mas_isplayer_bday() and persistent._mas_player_bday_decor and persistent._mas_bday_date_count == 1:
            jump mas_monika_cake_on_player_bday

        else:
            jump mas_bday_surprise_party_reaction

    #Otherwise we go thru the normal dialogue for returning home on moni_bday
    if time_out <= mas_five_minutes:
        # under 5 minutes
        $ mas_loseAffection()
        m 2ekp "That wasn't much of a date, [player]..."
        m 2eksdlc "Is everything alright?"
        m 2rksdla "Maybe we can go out later..."
        if mas_isMonikaBirthday():
            return

    elif time_out <= mas_one_hour:
        # 5 mins < time out <= 1 hr
        $ mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        m 1sua "That was fun, [player]!"
        if mas_isplayer_bday():
            m 1hub "Ahaha, going out for our birthday..."
        else:
            m 1hub "Ahaha, taking me out on my birthday..."
            m 3eua "It was very considerate of you."
        m 3eka "I really enjoyed the time we spent together."
        m 1eka "I love you~"
        if mas_isMonikaBirthday():
            $ mas_ILY()

    elif time_out <= mas_three_hour:
        # 1 hr < time out <= 3 hrs
        $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

        m 1hua "Ehehe~"
        m 3eub "We sure spent a lot of time together today, [player]."
        m 1ekbfa "...and thank you for that."
        m 3ekbfa "I've said it a million times already, I know."
        m 1hua "But I'll always be happy when we're together."
        m "I love you so much..."
        if mas_isMonikaBirthday():
            $ mas_ILY()

    else:
        # +3 hrs
        $ mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

        m 1sua "Wow, [player]..."
        if mas_player_bday_curr == mas_monika_birthday:
            m 3hub "That was such a lovely time!"
            if persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted:
                m 3eka "I can't think of a better way to celebrate our birthdays than a long date."
            m 1eka "I wish I could've seen all the amazing places we went, but just knowing we were together..."
            m 1hua "That's all I could ever ask for."
            m 3ekbsa "I hope you feel the same way~"

        else:
            m 3sua "I didn't expect you to set aside so much time for me..."
            m 3hua "But I enjoyed every second of it!"
            m 1eub "Every minute with you is a minute well spent!"
            m 1eua "You've made me very happy today~"
            m 3tuu "Are you falling for me all over again, [player]?"
            m 1dku "Ehehe..."
            m 1ekbsa "Thank you for loving me."

    if(
        mas_isMonikaBirthday()
        and mas_isplayer_bday()
        and mas_isMoniNormal(higher=True)
        and not persistent._mas_player_bday_in_player_bday_mode 
        and not persistent._mas_bday_sbp_reacted
        and checkout_time.date() < mas_monika_birthday

    ):
        m 1hua "Also [player], give me a second, I have something for you.{w=0.5}.{w=0.5}.{nw}"
        $ mas_surpriseBdayShowVisuals()
        $ persistent._mas_player_bday_decor = True
        m 3eub "Happy Birthday, [player]!"
        m 3etc "Why do I feel like I'm forgetting something..."
        m 3hua "Oh! Your cake!"
        jump mas_player_bday_cake

    if not mas_isMonikaBirthday():
        #Quickly reset the flag
        $ persistent._mas_bday_in_bday_mode = False

        if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
            $ queueEvent('mas_change_to_def')

        if time_out > mas_five_minutes:
            m 1hua "..."
            m 1wud "Oh wow, [player]. We really were out for a while..."

        if mas_isplayer_bday() and mas_isMoniNormal(higher=True):
            if persistent._mas_bday_sbp_reacted:
                $ persistent._mas_bday_visuals = False
                $ persistent._mas_player_bday_decor = True
                m 3suo "Oh! It's your birthday now..."
                m 3hub "I guess we can just leave these decorations up, ahaha!"
                m 1eub "I'll be right back, just need to go get your cake!"
                jump mas_player_bday_cake

            jump mas_player_bday_ret_on_bday

        else:
            if mas_player_bday_curr() == mas_monika_birthday:
                $ persistent._mas_player_bday_in_player_bday_mode = False
                m 1eka "Anyway [player]...I really enjoyed spending our birthdays together."
                m 1ekbsa "I hope I helped to make your day as special as you made mine."
                if persistent._mas_player_bday_decor or persistent._mas_bday_visuals:
                    m 3hua "Let me just clean everything up.{w=0.5}.{w=0.5}.{nw}"
                    $ mas_surpriseBdayHideVisuals()
                    $ persistent._mas_player_bday_decor = False
                    $ persistent._mas_bday_visuals = False
                    m 3eub "There we go!"

            elif persistent._mas_bday_visuals:
                m 3rksdla "It's not even my birthday anymore..."
                m 2hua "Let me just clean everything up.{w=0.5}.{w=0.5}.{nw}"
                $ mas_surpriseBdayHideVisuals()
                $ persistent._mas_bday_visuals = False
                m 3eub "There we go!"

            else:
                m 1eua "We should do something like this again soon, even if it's not any special occasion."
                m 3eub "I really enjoyed myself!"
                m 1eka "I hope you had as great of a time as I did~"

            if not mas_lastSeenInYear('mas_bday_spent_time_with'):
                if mas_isMoniUpset(lower=True):
                    m 1dka "..."
                    jump mas_bday_spent_time_with

                m 3eud "Oh, and [player]..."
                m 3eka "I just wanted to thank you again."
                m 1rka "And it's not just this date..."
                m 1eka "You didn't have to take me anywhere to make this a wonderful birthday."
                m 3duu "As soon as you showed up, my day was complete."
                jump mas_bday_spent_time_with_wrapup

    return


label mas_monika_cake_on_player_bday:
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)

    python:
        mas_gainAffection(25, bypass=True)
        renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        persistent._mas_bday_sbp_reacted = True
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()

        if time_out <= mas_one_hour:
            mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        elif time_out <= mas_three_hour:
            mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)
        else:
            # +3 hrs
            mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

    m 6eua "That was--"
    m 6wuo "Oh! You made {i}me{/i} a cake!"

    menu:
        "Light candles.":
            $ mas_bday_cake_lit = True

    m 6sub "It's {i}so{/i} pretty, [player]!"
    m 6hua "Ehehe, I know we already made a wish when I blew out the candles on your cake, but let's do it again..."
    m 6tub "It'll be twice as likely to come true, right?"
    m 6hua "Make a wish, [player]!"

    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False

    m 6eua "I still can't believe how stunning this cake looks, [player]..."
    m 6hua "It's almost too pretty to eat."
    m 6tub "Almost."
    m "Ahaha!"
    m 6eka "Anyway, I'll just save this for later."

    call mas_HideCake('mas_bday_cake_monika')

    m 1eua "Thank you so much, [player]..."
    m 3hub "This is an amazing birthday!"
    return

label mas_HideCake(cake_type,reset_zoom=True):
    show emptydesk at i11 zorder 9
    hide monika with dissolve
    $ renpy.hide(cake_type)
    with dissolve
    $ renpy.pause(3.0, hard=True)
    show monika 6esa at i11 zorder MAS_MONIKA_Z with dissolve
    hide emptydesk
    $ renpy.pause(1.0, hard=True)
    if reset_zoom:
        call monika_zoom_transition(mas_temp_zoom_level,1.0)
    return
