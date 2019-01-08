define mas_player_bday_curr = store.mas_utils.add_years(persistent._mas_player_bday,datetime.date.today().year-persistent._mas_player_bday.year)

init -10 python:
    def mas_isplayer_bday(_date=None):
        if _date is None:
            _date = datetime.date.today()

        return _date == store.mas_utils.add_years(persistent._mas_player_bday,_date.year-persistent._mas_player_bday.year)
        
default persistent._mas_player_bday_in_player_bday_mode = False
label mas_player_bday_autoload_check:
    if not persistent._mas_player_bday_in_player_bday_mode:
        $ mas_skip_visuals = True
        $ selected_greeting = "i_greeting_monikaroom"
        $ persistent.closed_self = True
        jump ch30_post_restartevent_check
    else:
        jump mas_ch30_post_holiday_check
    return

default persistent._mas_opened_door_bday = False

label mas_player_bday_opendoor:
    $ persistent._mas_opened_door_bday = True
    $ scene_change = True
    call spaceroom(hide_monika=True)
    $ mas_disable_quit()
    m 2wud "[player]!"
    m 2tfc "You didn't knock!"
    m 2tfd "I was just going to start setting up your birthday party, but I didn't have time before you came in!"
    m 2dkc "..."
    m 2ekd "Well, I guess the surprise is ruined now, but let me finish up anyway..."
    show monika 1dsc
    pause 2.0
    $ renpy.show("mas_bday_banners", zorder=7)
    $ renpy.show("mas_bday_balloons", zorder=8)
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    m 4hub "Happy birthday, [player]!"
    m 2rksdla "I just wished you had knocked first."
    m 4hksdlb "Oh...your cake!"
    window hide
    show monika 6dsc
    pause 1.0
    $ renpy.show("mas_bday_cake", zorder=store.MAS_MONIKA_Z+1)
    pause 1.0
    jump monikaroom_greeting_cleanup

label mas_player_bday_knock_no_listen:
    menu:
        m "Who is it?"

        "It's me.":
            $ mas_disable_quit()
            m "Oh! Can you wait just a moment please?"
            pause 5.0
            m "Alright, come on in, [player]..."
            jump mas_player_bday_surprise

label mas_player_bday_surprise:
    $ scene_change = True
    call spaceroom(hide_monika=False)
    show monika 1hub at t11
    $ renpy.show("mas_bday_banners", zorder=7)
    $ renpy.show("mas_bday_balloons", zorder=8)
    m 4hub "Surprise!"
    m 4sub "Ahaha! Happy Birthday, [player]!"
    menu:
        m "Did I surprise you?"
        "Yes":
            m 1hub "Yay!"
            m 3hua "I always love pulling off a good surprise!"
            m 1tsu "I wish I could've seen the look on your face, ehehe."

        "No":
            m 2lfp "Hmph. Well that's okay."
            m 2tsu "You're probably just saying that because you don't want to admit I caught you off guard..."
            if renpy.seen_label("monikaroom_greeting_ear_narration") and renpy.seen_label("mas_player_bday_listen"):
                m 2tsb "...or maybe you were listening through the door again..."
            elif renpy.seen_label("mas_player_bday_listen"):
                m 2tsb"{cps=2}...or maybe you were eavesdropping on me.{/cps}{nw}"
                $ _history_list.pop()
            m 2hua "Ehehe."
    m 3wub "Oh! {w=0.5}I also made you a cake, [player]!"
    window hide
    show monika 6dsc
    pause 1.0
    $ renpy.show("mas_bday_cake", zorder=store.MAS_MONIKA_Z+1)
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup

label mas_player_bday_listen:
    m "...I'll just put this here..."
    m "...hmm that looks pretty good, but something's missing..."
    m "Oh! {w=0.5}Of course!"
    m "There! {w=0.5}Perfect!"
    window hide
    jump monikaroom_greeting_choice

label mas_player_bday_knock_listened:
    window hide
    pause 5.0
    menu:
        "Open the door":
            $ mas_disable_quit()
            jump mas_player_bday_surprise

label mas_player_bday_opendoor_listened:
    $ persistent._mas_opened_door_bday = True
    $ renpy.show("mas_bday_banners", zorder=7)
    $ renpy.show("mas_bday_balloons", zorder=8)
    $ mas_disable_quit()
    m "[player]!"
    m "You didn't knock!"
    m "I was setting up your birthday party, but I didn't have time before you came in to get ready to surprise you!"
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    m 4hub "Happy birthday, [player]!"
    m 2rksdla "I just wished you had knocked first."
    m 2hksdlb "Oh...your cake!"
    window hide
    show monika 6dsc
    pause 1.0
    $ renpy.show("mas_bday_cake", zorder=store.MAS_MONIKA_Z+1)
    jump monikaroom_greeting_cleanup


label mas_player_bday_cake:
    $ persistent._mas_player_bday_in_player_bday_mode = True
    m 6eua "Let me just light the candles for you..."
    window hide
    show monika 6dsc
    pause 1.0
    $ mas_bday_cake_lit = True
    pause 1.0
    m 6sua "Isn't it pretty, [player]?"
    m 6eksdla "Now I know you can't exactly blow the candles out yourself, so I'll do it for you..."
    m 6eua "You should still make a wish though, it just might come true someday..."
    menu:
        m "Let me know when you're ready."
        "I'm ready.":
            show monika 6hua
            m "Okay [player], make a wish!"
            window hide
            pause 1.0
            show monika 6hft
            pause 0.1
            $ mas_bday_cake_lit = False
            pause 1.0
    m 6hua "Ehehe..."
    m 6eka "I know it's your birthday, but I made a wish too, [player]..."
    m 6ekbsa "And you know what? {w=0.5}I bet we both wished for the same thing~"
    m 6hkbsu "..."
    m 6rksdla "Oh gosh, I guess you can't really eat this cake either, huh [player]?"
    m 6eksdla "This is all rather silly, isn't it?"
    m 6hksdlb "I think I'll just save this for later. It seems kind of rude for me to eat {i}your{/i} birthday cake in front of you, ahaha!"
    hide mas_bday_cake with dissolve
    m 6dkbsu "..."
    m 4ekbfa "I...I also made a card for you, [player]. I hope you like it..."
    $ p_bday_month = mas_player_bday_curr.month
    call showpoem(poem_pbday, music=False,paper="mod_assets/poem_pbday_[p_bday_month].png")
    show monika 5hkbfa at t11 zorder MAS_MONIKA_Z with dissolve
    m 5hkbfa "I love you so much [player], let's have a great day~"
    return

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
    m 3rksdla "Well [player], I was hoping to do something a little more fun, but you've been so sweet and haven't left all day long, so..."
    show monika 1dsc
    pause 2.0
    $ renpy.show("mas_bday_banners", zorder=7)
    $ renpy.show("mas_bday_balloons", zorder=8)
    m 3hub "Happy birthday, [player]!"
    m 1eka "I really wanted to surprise you today, but it's getting late and I just couldn't wait any longer."
    m 3eksdlc "Gosh, I just hope you weren't starting to think I forgot your birthday. I'm really sorry if you did..."
    m 1rksdla "I guess I probably shouldn't have waited so long, ehehe."
    m 1hua "Oh! I made you a cake!"
    window hide
    show monika 6dsc
    pause 1.0
    $ renpy.show("mas_bday_cake", zorder=store.MAS_MONIKA_Z+1)
    pause 1.0
    call mas_player_bday_cake
    return

init 2 python:

    poem_pbday = Poem(
    author = "monika",
    title = " My dearest {0},".format(persistent.playername),
    text = """\
 To the one I love,
 The one I trust,
 The one I can't live without.
 I hope your day is as special as you make everyday for me.
 Thank you so much for being you. 

 Happy Birthday, sweetheart

 Forever yours,
 Monika
"""
    #" # I need this to keep syntax highlighting on vim
    )

