define mas_player_bday_curr = store.mas_utils.add_years(persistent._mas_player_bday,datetime.date.today().year-persistent._mas_player_bday.year)

init -10 python:
    def mas_isplayer_bday(_date=None):
        if _date is None:
            _date = datetime.date.today()

        #return _date == store.mas_utils.add_years(persistent._mas_player_bday,_date.year-persistent._mas_player_bday.year)
        return _date == mas_player_bday_curr
        
default persistent._mas_player_bday_in_player_bday_mode = False
label mas_player_bday_autoload_check:
    if not persistent._mas_player_bday_in_player_bday_mode:
        $ persistent._mas_player_bday_in_player_bday_mode = True
        $ mas_skip_visuals = True
        $ selected_greeting = "i_greeting_monikaroom"
        jump ch30_post_restartevent_check
    else:
        jump mas_ch30_post_holiday_check
    return

default persistent._mas_seen_bday_surprise = False
default persistent._mas_opened_door_bday = False

label mas_player_bday_opendoor:
    $ persistent._mas_seen_bday_surprise = True
    $ persistent._mas_opened_door_bday = True
    $ scene_change = True
    call spaceroom(hide_monika=True)
    m 2wud "[player]!"
    m 2tfc "You didn't knock!"
    m 2tfd "I was just going to start setting up your birthday party, but I didn't have time before you came in!"
    m 2dkc "..."
    m 2ekd "Well, I guess the surprise is ruined now, but let me finish up anyway..."
    $ renpy.show("mas_bday_banners", zorder=7)
    $ renpy.show("mas_bday_balloons", zorder=8)
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    m 4hub "Happy birthday, [player]!"
    m 2rksdla "I just wished you had knocked first."
    m 4hksdlb "Oh...your cake!"
    $ renpy.show("mas_bday_cake", zorder=store.MAS_MONIKA_Z+1)
    jump monikaroom_greeting_cleanup

label mas_player_bday_knock_no_listen:
    menu:
        m "Who is it?"

        "It's me.":
            m "Oh! Can you wait just a moment please?"
            pause 5.0
            m "Alright, come on in, [player]..."
            jump mas_player_bday_surprise

label mas_player_bday_surprise:
    $ persistent._mas_seen_bday_surprise = True
    $ scene_change = True
    call spaceroom(hide_monika=False)
    show monika 1hub at t11
    $ renpy.show("mas_bday_cake", zorder=store.MAS_MONIKA_Z+1)
    $ renpy.show("mas_bday_banners", zorder=7)
    $ renpy.show("mas_bday_balloons", zorder=8)
    m 4hub "Surprise!"
    m 4sub "Ahaha! Happy Birthday, [player]!"
    jump monikaroom_greeting_cleanup

label mas_player_bday_listen:
    m "...I'll just put this here..."
    m "...hmm that looks pretty good, but something's missing..."
    m "Oh! Of course!"
    m "There! Perfect!"
    jump monikaroom_greeting_choice

label mas_player_bday_knock_listened:
    pause 5.0
    menu:
        "Open the door":
            jump mas_player_bday_surprise

label mas_player_bday_opendoor_listened:
    $ persistent._mas_seen_bday_surprise = True
    $ renpy.show("mas_bday_banners", zorder=7)
    $ renpy.show("mas_bday_balloons", zorder=8)
    m "[player]!"
    m "You didn't knock!"
    m "I was set up your birthday party, but I didn't have time before you came in to get ready to surprise you!"
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    m 4hub "Happy birthday, [player]!"
    m 2rksdla "I just wished you had knocked first."
    m 2hksdlb "Oh...your cake!"
    $ renpy.show("mas_bday_cake", zorder=store.MAS_MONIKA_Z+1)
    jump monikaroom_greeting_cleanup


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_no_restart",
            conditional=(
                "mas_isplayer_bday() "
                "and not persistent._mas_player_bday_in_player_bday_mode"
            ),
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_player_bday_curr, datetime.time(hour=19)),
            end_date=mas_player_bday_curr + datetime.timedelta(days=1),
            years=[]
        ),
        skipCalendar=True
    )

label mas_player_bday_no_restart:
    if persistent._mas_player_bday_in_player_bday_mode:
        m "error"
        return
    m "test"
    return



