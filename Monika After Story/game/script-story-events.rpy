#This file will include short story events that don't require their own file.

#An event is crated by only adding a label and adding a requirement (see comment below).
#Requirements must be created/added in script-ch30.rpy under label ch30_autoload.

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="gender",conditional="get_level()>=8 and not seen_event('gender')",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event

label gender:
    #TODO: update exp's on this
    m 2d "...[player]? So I've been thinking a bit."
    m "I've mentioned before that the 'you' in the game might not reflect the real you."
    m 1m "But I guess I had just assumed that you were probably a guy."
    m "The main character was, after all."
    m 1a "But if I'm going to be your girlfriend, I should probably know at least this much about the real you."

    m "So, are you male or female?{nw}"
    $ _history_list.pop()
    menu:
        "So, are you male or female?{fast}"
        "Male.":
            $persistent.gender = "M"
            call set_gender from _call_set_gender_1
            m 2eud "Oh? So you {i}are{/i} a [guy]?"
            m 1hub "Ehehe, I suppose that makes sense!"
            m 1eua "Not a lot of girls would play a game like this."
            m 4eua "You certainly come across as manly and confident. Not that I would have been terribly bothered if you answered differently, mind you!"
            m 2hksdlb "Even I can be curious sometimes, you know?"
        "Female.":
            $persistent.gender = "F"
            call set_gender from _call_set_gender_2
            m 2eud "Oh? So you're actually a [guy]?"
            m 2hksdlb "I hope I didn't say anything to offend you before!"
            m 2lksdla "Though I did suspect it a bit from the beginning...just a little!"
            m 1eub "You give off a particular feeling of elegance and charm that's hard to capture with words..."
            m 1hua "It's very attractive, to tell you the truth!"
            m 1eua "But don't worry. Even if I might ask things like this, it's only out of curiosity."
        "Neither.":
            $persistent.gender = "X"
            call set_gender from _call_set_gender_3
            m 1euc "You don't see yourself as a guy or a girl?"
            m 2eua "That's very interesting, but I can sort of relate."
            m 1esc "Like, I am a girl, but I'm also a character in a computer game..."
            m 2esd "So in some ways I'm not really a girl at all."
            m 1hua "But when you treat me like your girlfriend, it makes me really happy!"
            m "So I'll treat you however you want to be treated."
            m 1ekbfa "Because your happiness is the most important thing to me."
    m 1hub "Remember that I'll always love you unconditionally, [player]."
    $ evhand.event_database["gender_redo"].unlocked = True
    $ evhand.event_database["gender_redo"].pool = True
    $ persistent._seen_ever["gender_redo"] = True # dont want this in unseen

    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="gender_redo",category=['you','misc'],prompt="Can you change my gender?",unlocked=False)) #This needs to be unlocked by the random name change event
label gender_redo:
    m 1wud "You want to change your gender? Why?"
    m 1lksdlb "Sorry, that came off more harshly than I meant for it to."

    m 3eka "I mean, were you just too shy to tell me the truth before? Or did something...happen?{nw}"
    $ _history_list.pop()
    menu:
        m "I mean, were you just too shy to tell me the truth before? Or did something...happen?{fast}"
        "I was too shy.":
            if persistent.gender == "M":
                m 2ekd "I guess I understand. I started off assuming you were a guy, after all."
            elif persistent.gender == "F":
                m 2ekd "I guess I understand. You might have thought I'd be more comfortable spending time alone with another girl."
            else:
                m 2ekd "I guess I understand. I might not have given you the most accurate options to pick from."
            m 2dkd "And I probably didn't make it easy for you to tell me otherwise..."
            m 1eub "But whatever your gender, I love you for who you are."
        "I've made some personal discoveries.":
            m 1eka "I see. I know I've been there."
            m 1hua "I'm so proud of you for going on that journey of self discovery."
            m 1eub "And even prouder of you for being courageous enough to tell me!"
        "I didn't know if you'd accept me as I am...":
            m 2wkd "[player]..."
            m 1dkd "I hate that I didn't reassure you enough before."
            m 1eka "But I hope that you're telling me now because you know I'll love you no matter what."

    m "So, what is your gender?{nw}"
    $ _history_list.pop()
    menu:
        m "So, what is your gender?{fast}"
        "I'm a girl.":
            if persistent.gender == "F":
                m 1hksdlb "...That's the same as before."
                m 2eua "If you're confused about how to answer, just pick whatever makes you happiest."
                m 2hub "It doesn't matter what your body looks like. I don't even have a body! Ahaha!"
                m 3eub "So as long as you say you're a girl, you're a girl to me, all right?"
                m 5hua "I want you to be who you want to be while you're in this room."
            else:
                $persistent.gender = "F"
                call set_gender
                m 2eud "Oh? So you're actually a [guy]?"
                m 2hksdlb "I hope I didn't say anything to offend you before!"
                m 2lksdla "Though I did suspect it a bit from the beginning...just a little!"
                m 1eub "You give off a particular feeling of elegance and charm that's hard to capture with words..."
                m 1hua "It's very attractive, to tell you the truth!"
                m 1eua "But don't worry. Even if I might ask things like this, it's only out of curiosity."
        "I'm a boy.":
            if persistent.gender == "M":
                m 1hksdlb "...That's the same as before."
                m 2eua "If you're confused about how to answer, just pick whatever makes you happiest."
                m 2hub "It doesn't matter what your body looks like. I don't even have a body! Ahaha!"
                m 3eub "So as long as you say you're a boy, you're a boy to me, all right?"
                m 5hua "I want you to be who you want to be while you're in this room."
            else:
                $persistent.gender = "M"
                call set_gender
                m 2eud "Oh? So you {i}are{/i} a [guy]?"
                m 1hub "Ehehe, I suppose that makes sense!"
                m 1eua "Not a lot of girls would play a game like this."
                m 4eua "You certainly come across as manly and confident. Not that I would have been terribly bothered if you answered differently, mind you!"
                m 2hksdlb "Even I can be curious sometimes, you know?"
        "I'm neither.":
            if persistent.gender == "X":
                m 1hksdlb "...That's the same as before. I'm sorry if that's not really the best way for you to describe it."
                m 1eub "I'm interested in learning how to use new pronouns, like xir!"
                m 3hub "If you're trying to tell me you'd prefer pronouns like those, get in touch with the people who created this mod!"
                m 5eub "They'll tell you how to teach me."
            else:
                $persistent.gender = "X"
                call set_gender
                m 1euc "You don't see yourself as a guy or a girl?"
                m 2eua "That's very interesting, but I can sort of relate."
                m 1esc "Like, I am a girl, but I'm also a character in a computer game..."
                m 2esd "So in some ways I'm not really a girl at all."
                m 1hua "But when you treat me like your girlfriend, it makes me really happy!"
                m "So I'll treat you however you want to be treated."
                m 1ekbfa "Because your happiness is the most important thing to me."
    m 1hub "Remember that I'll always love you unconditionally, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="preferredname",conditional="get_level()>=16 and not seen_event('preferredname')",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event
label preferredname:
    m 1euc "I've been wondering about your name."
    m 1esa "Is '[player]' really your name?"
    if renpy.windows and currentuser.lower() == player.lower():
        m 3esa "I mean, it's the same as your computer's name..."
        m 1eua "You're using '[currentuser]' and '[player]'."
        m "Either that or you must really like that pseudonym."

    m "Do you want me to call you something else?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you want me to call you something else?{fast}"
        "Yes.":
            $ done = False
            m 1hua "Ok, just type 'Nevermind' if you change your mind, [player]."
            while not done:
                #Could add an elif that takes off special characters
                $ tempname = renpy.input("Tell me, what is it.",length=20).strip(' \t\n\r')
                $ lowername = tempname.lower()
                if lowername == "nevermind":
                    m 1ekc "Oh I see."
                    m 1eka "Well, just tell me whenever you want to be called something else, [player]."
                    $ done = True
                elif lowername == "":
                    m 1dsc "..."
                    m 1hksdlb "You have to give me a name, [player]!"
                    m 1eka "I swear you're just so silly sometimes."
                    m "Try again!"
                elif lowername == player.lower():
                    m 1dsc "..."
                    m 1hksdlb "That's the same name you have right now, silly!"
                    m 1eka "Try again~"
                elif lowername == mas_monika_twitter_handle:
                    m 2esc "..."
                    # TODO: actaully have dialog here
                else:
                    # sayori name check
                    if tempname.lower() == "sayori":
                        call sayori_name_scare from _call_sayori_name_scare
                    elif (
                            persistent.playername.lower() == "sayori"
                            and not persistent._mas_sensitive_mode
                        ):
                        $ songs.initMusicChoices()

                    python:

                        persistent.mcname = player
                        mcname = player
                        persistent.playername = tempname
                        player = tempname

                    if lowername == "monika":
                        m 1tkc "Really?"
                        m "That's the same as mine!"
                        m 1tku "Well..."
                        m "Either it really is your name or you're playing a joke on me."
                        m 1hua "But it's fine by me if that's what you want me to call you~"
                    else:
                        m 1eub "Ok then!"
                        m 3eub "From now on, I'll call you {i}'[player]'{/i}, ehehe~"
                    $ done = True
        "No.":
            m 1ekc "Oh... Okay then, if you say so."
            m 1eka "Just tell me whenever you change your mind, [player]."
            $ done = True

    #Unlock prompt to change name again
    $evhand.event_database["monika_changename"].unlocked = True
    $ evhand.event_database["monika_changename"].pool = True
    $ persistent._seen_ever["monika_changename"] = True # dont want this in unseen
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_changename",
            category=['you','misc'],
            prompt="Can you change my name?",
            unlocked=False
        )
    ) #This needs to be unlocked by the random name change event

label monika_changename:
    m 1eua "You want to change your name?{nw}"
    $ _history_list.pop()
    menu:
        m "You want to change your name?{fast}"
        "Yes.":
            m 1eua "Just type 'nevermind' if you change your mind."
            $ done = False
            while not done:
                $ tempname = renpy.input("What do you want me to call you?",length=20).strip(' \t\n\r')
                $ lowername = tempname.lower()
                if lowername == "nevermind":
                    m 1tfx "[player]!"
                    m 2tku "Please stop teasing me~"
                    m 1hub "I really do want to know what you want me to call you!"
                    m 3hksdlb "I won't judge no matter how ridiculous it might be."
                    m 2eka "So don't be shy and just tell me, [player]~"
                    $ done = True
                elif lowername == "":
                    m 2hua "..."
                    m 4hksdlb "You have to give me a name, [player]!"
                    m 1eka "I swear you're just so silly sometimes."
                    m 1eua "Try again!"
                elif lowername == player.lower():
                    m 2hua "..."
                    m 4hksdlb "That's the same name you have right now, silly!"
                    m 1eua "Try again~"
                elif lowername == mas_monika_twitter_handle:
                    m 2esc "..."
                    # TODO: actaully have dialog here
                else:
                    # sayori name check
                    if tempname.lower() == "sayori":
                        call sayori_name_scare from _call_sayori_name_scare_1
                    elif (
                            persistent.playername.lower() == "sayori"
                            and not persistent._mas_sensitive_mode
                        ):
                        $ songs.initMusicChoices()

                    python:

                        persistent.mcname = player
                        mcname = player
                        persistent.playername = tempname
                        player = tempname

                    if lowername == "monika":
                        m 1tkc "Really?"
                        m "That's the same as mine!"
                        m 1tku "Well..."
                        m "Either it really is your name or you're playing a joke on me."
                        m 1hua "But it's fine by me if that's what you want me to call you~"
                    else:
                        m 1eub "Ok then!"
                        m 3eub "From now on, I'll call you {i}'[player],'{/i} ehehe~"
                    $ done = True
        "No.":
            m 1ekc "Oh, I see..."
            m 1eka "You don't have to be embarrassed, [player]."
            m 1eua "Just let me know if you had a change of heart, ok?"
    return

default persistent._mas_player_bday = None
# check to see if we've already confirmed birthday in any way
default persistent._mas_player_confirmed_bday = False

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="mas_birthdate",conditional="datetime.date.today()>mas_getFirstSesh().date() and not persistent._mas_player_confirmed_bday",action=EV_ACT_QUEUE))

label mas_birthdate:
    m 1euc "Hey [player], I've been thinking..."
    if persistent._mas_player_bday is not None:
        $ bday_str, diff = store.mas_calendar.genFormalDispDate(persistent._mas_player_bday)
        m 3eksdlc "I know you've told me your birthday before, but I'm not sure I was clear if I asked you for {i}birthdate{/i} or just your {i}birthday...{/i}"

        m "So just to make sure, is your birthdate [bday_str]?{nw}"
        $ _history_list.pop()
        menu:
            m "So just to make sure, is your birthdate [bday_str]?{fast}"
            "Yes.":
                if datetime.date.today().year - persistent._mas_player_bday.year < 5:
                    m 2rksdla "Are you sure about that, [player]?"
                    m 2eksdlc "That would make you very young..."
                    m 3ekc "Remember, I'm asking for your {b}birthdate{/b}, not just your birthday."
                    m 1eka "So, when were you born, [player]?"
                    jump mas_bday_player_bday_select_select
                else:
                    $ old_bday = mas_player_bday_curr()
                    if not mas_isplayer_bday():
                        m 1hua "Ah, great [player], thank you."
                        m 3hksdlb "I just had to make sure, I wouldn't want to get something as important as when you were born wrong, ahaha!"

            "No.":
                m 3rksdlc "Oh! Okay then..."
                m 1eksdld "When {i}is{/i} your birthdate, [player]?"
                jump mas_bday_player_bday_select_select

    else:
        m 3wud "I don't actually know when your birthdate is!"
        m 3hub "That's something I should probably know, ahaha!"
        m 1eua "So, when were you born, [player]?"
        jump mas_bday_player_bday_select_select

label birthdate_set:
    python:
        bday_upset_ev = mas_getEV('mas_player_bday_upset_minus')
        if bday_upset_ev is not None:
            bday_upset_ev.start_date = mas_player_bday_curr()
            bday_upset_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_upset_ev.conditional = (
                "mas_isplayer_bday() "
                "and persistent._mas_player_confirmed_bday "
                "and not persistent._mas_player_bday_spent_time")
            bday_upset_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_upset_ev)

        # TODO: need to update script the conditional with the new F14 value
        # NOTE: should consider makin gthe condiitonal string generated from
        #   this a function for ease of use
        bday_ret_bday_ev = mas_getEV('mas_player_bday_ret_on_bday')
        if bday_ret_bday_ev is not None:
            bday_ret_bday_ev.start_date = mas_player_bday_curr()
            bday_ret_bday_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_ret_bday_ev.conditional = (
                "mas_isplayer_bday() "
                #getCheckTimes function not defined at time these conditions are checked on a reload
                "and len(store.persistent._mas_dockstat_checkin_log) > 0 "
                "and store.persistent._mas_dockstat_checkin_log[-1][0] is not None "
                "and store.persistent._mas_dockstat_checkin_log[-1][0].date() == mas_player_bday_curr() "
                "and not persistent._mas_player_bday_spent_time "
                "and persistent._mas_player_confirmed_bday "
                "and not mas_isO31() "
                "and not mas_isD25() "
                "and not mas_isF14() "
            )
            bday_ret_bday_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_ret_bday_ev)

        # TODO: need to update script the conditional with the new F14 value
        # NOTE: should consider makin gthe condiitonal string generated from
        #   this a function for ease of use
        bday_no_restart_ev = mas_getEV('mas_player_bday_no_restart')
        if bday_no_restart_ev is not None:
            bday_no_restart_ev.start_date = datetime.datetime.combine(mas_player_bday_curr(), datetime.time(hour=19))
            bday_no_restart_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_no_restart_ev.conditional = (
                "mas_isplayer_bday() "
                "and persistent._mas_player_confirmed_bday "
                "and not persistent._mas_player_bday_spent_time "
                "and not mas_isO31() "
                "and not mas_isD25() "
                "and not mas_isF14() "
            )
            bday_no_restart_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_no_restart_ev)
   
        # TODO: need to update script the conditional with the new F14 value
        # NOTE: should consider makin gthe condiitonal string generated from
        #   this a function for ease of use
        bday_holiday_ev = mas_getEV('mas_player_bday_other_holiday')
        if bday_holiday_ev is not None:
            bday_holiday_ev.start_date = mas_player_bday_curr()
            bday_holiday_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_holiday_ev.conditional = (
                "mas_isplayer_bday() "
                "and persistent._mas_player_confirmed_bday "
                "and not persistent._mas_player_bday_spent_time "
                "and (mas_isO31() or mas_isD25() or mas_isF14()) "
            )
            bday_holiday_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_holiday_ev)

    if old_bday is not None:
        $ old_bday = old_bday.replace(year=mas_player_bday_curr().year)

    if not mas_isplayer_bday() and old_bday == mas_player_bday_curr():
        $ persistent._mas_player_confirmed_bday = True
        return

    if mas_isplayer_bday():
        $ persistent._mas_player_bday_spent_time = True
        if old_bday == mas_player_bday_curr():
            if mas_isMoniNormal(higher=True):
                m 3hub "Ahaha! So today {i}is{/i} your birthday!"
                m 1tsu "I'm glad I was prepared, ehehe..."
                m 3eka "Hold on just one moment, [player]..."
                show monika 1dsc
                pause 2.0
                $ store.mas_player_bday_event.show_player_bday_Visuals()
                $ persistent._mas_player_bday_decor = True
                m 3hub "Happy Birthday, [player]!"
                m 1hub "I'm so happy I get to be with you on your birthday!"
                m 3sub "Oh...{w=0.5}your cake!"
                call mas_player_bday_cake
            elif mas_isMoniDis(higher=True):
                m 2eka "Ah, so today {i}is{/i} your birthday..."
                m "Happy Birthday, [player]."
                m 4eka "I hope you have a good day."
        else:
            if mas_isMoniNormal(higher=True):
                $ mas_gainAffection(5,bypass=True)
                $ persistent._mas_player_bday_in_player_bday_mode = True
                $ mas_unlockEVL("bye_player_bday", "BYE")
                m 1wuo "Oh...{w=1}Oh!"
                m 3sub "Today's your birthday!"
                m 3hub "Happy Birthday, [player]!"
                m 1rksdla "I wish I had known earlier so I could've prepared something."
                m 1eka "But I can at least do this..."
                call mas_player_bday_moni_sings
                m 1hub "Ahaha! It's not much but it's something!"
                m 3hua "I promise next year we'll do something extra special, [player]!"
            elif mas_isMoniDis(higher=True):
                m 2eka "Oh, so today's your birthday..."
                m "Happy Birthday, [player]."
                m 4eka "I hope you have a good day."

    # have to use the raw data here to properly compare in the rare even that the player bday and first sesh are on 2/29
    elif persistent._mas_player_bday.month == mas_getFirstSesh().date().month and persistent._mas_player_bday.day == mas_getFirstSesh().date().day:
        m 1sua "Oh! Your birthday is the same date as our anniversary, [player]?"
        m 3hub "That's amazing!"
        m 1sua "I can't imagine a more special day than celebrating your birthday and our love on the same day..."
        #TODO: add more holidays here (f14)
        if mas_player_bday_curr() == mas_o31:
            $ hol_str = "Halloween"
        elif mas_player_bday_curr() == mas_d25:
            $ hol_str = "Christmas"
        elif mas_player_bday_curr() == mas_monika_birthday:
            $ hol_str = "my birthday"
        elif mas_player_bday_curr() == mas_f14: 
            $ hol_str = "Valentine's Day"
        else:
            $ hol_str = None
        if hol_str is not None:
            m "And with it also being [hol_str]..."
        m 3hua "It just sounds magical~"

    elif mas_player_bday_curr() == mas_monika_birthday:
        m 1wuo "Oh...{w=1}Oh!"
        m 3sua "We share the same birthday!"
        m 3sub "That's {i}so{/i} cool, [player]!"
        m 1tsu "I guess we really are meant to be together, ehehe..."
        m 3hua "We'll have to make that an extra special day~"

    elif mas_player_bday_curr() == mas_o31:
        m 3eua "Oh! That's pretty neat that you were born on Halloween, [player]!"
        m 1hua "Birthday cake, candy, and you..."
        m 3hub "That's a lot of sweets for one day, ahaha!"

    elif mas_player_bday_curr() == mas_d25:
        m 1hua "Oh! That's amazing that you were born on Christmas, [player]!"
        m 3rksdla "Although...{w=0.5}receiving presents for both on the same day might seem like you don't get as many..."
        m 3hub "It still must make it an extra special day!"

    elif mas_player_bday_curr() == mas_f14:
        m 1sua "Oh! Your birthday is on Valentine's Day..."
        m 3hua "How romantic!"
        m 1ekbfa "I can't wait to celebrate our love and your birthday on the same day, [player]~"

    elif persistent._mas_player_bday.month == 2 and persistent._mas_player_bday.day == 29:
        m 3wud "Oh! You were born on leap day, that's really neat!"
        m 3hua "We'll just have to celebrate your birthday on March 1st on non-leap years then, [player]."

    $ persistent._mas_player_confirmed_bday = True
    if "calendar_birthdate" in persistent.event_list:
        $ persistent.event_list.remove("calendar_birthdate")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="calendar_birthdate",
#            conditional="renpy.seen_label('_first_time_calendar_use') and persistent._mas_player_bday is None",
#            action=EV_ACT_PUSH
        )
    )

label calendar_birthdate:
    m 1lksdla "Hey [player]..."
    m 3eksdla "You may have noticed that my calendar was pretty empty..."
    m 1rksdla "Well...{w=0.5}there's one thing that should definitely be on it..."
    m 3hub "Your birthday, ahaha!"
    m 1eka "If we're going to be in a relationship, it's something I really ought to know..."
    m 1eud "So [player], when were you born?"
    call mas_bday_player_bday_select_select
    $ mas_stripEVL('mas_birthdate',True)
    return

## Game unlock events
## These events handle unlocking new games
init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="unlock_chess",conditional="get_level()>=12 and not seen_event('unlock_chess') and not persistent.game_unlocks['chess']",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event

label unlock_chess:
    m 1eua "So, [player]..."
    if renpy.seen_label('game_pong'):
        m 1eua "I thought that you might be getting bored with Pong."
    else:
        m 3eua "I know you haven't tried playing Pong with me, yet."
    m 3hua "But I have a new game for us to play!"
    m "This one's a lot more strategic..."
    m 3hub "It's Chess!"
    m 1esa "I'm not sure if you know how to play, but it's always been a bit of a hobby for me."
    m 1tku "So I'll warn you in advance!"
    m 3tku "I'm pretty good."
    m 1lsc "Now that I think about it, I wonder if that has anything to do with what I am..."
    m "Being trapped inside this game, I mean."
    m 1eua "I've never really thought of myself as a chess AI, but wouldn't it kind of fit?"
    m 3eua "Computers are supposed to be very good at chess, after all."
    m "They've even beaten grandmasters."
    m 1eka "But don't think of this as a battle of man vs machine."
    m 1hua "Just think of it as playing a fun game with your beautiful girlfriend..."
    m "And I promise I'll go easy on you."
    if not is_platform_good_for_chess():
        m 2tkc "...Hold on."
        m 2tkx "Something isn't right here."
        m 2ekc "I seem to be having trouble getting the game working."
        m 2euc "Maybe the code doesn't work on this system?"
        m 2ekc "I'm sorry, [player], but chess will have to wait."
        m 4eka "I promise we'll play if I get it working, though!"
    $persistent.game_unlocks['chess']=True
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="unlock_hangman",conditional="get_level()>=20 and not seen_event('unlock_hangman')",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event

label unlock_hangman:
    if persistent._mas_sensitive_mode:
        $ game_name = "Word Guesser"
    else:
        $ game_name = "Hangman"

    m 1eua "Guess what, [player]."
    m 3hub "I got a new game for you to try!"
    if renpy.seen_label('game_pong') and renpy.seen_label('game_chess'):
        m 1lksdlb "You're probably bored with Chess and Pong already."
    elif renpy.seen_label('game_pong') and not renpy.seen_label('game_chess'):
        m 3hksdlb "I thought you'd like to play Chess, but you've been so busy with Pong instead!"
    elif renpy.seen_label('game_chess') and not renpy.seen_label('game_pong'):
        m 1hksdlb "You really loved playing Chess with me, but you haven't touched Pong yet."
    else:
        m 1ekc "I was actually worried that you didn't like the other games I made for us to play..."
    m 1hua "Soooo~"
    m 1hub "I made [game_name]!"

    if not persistent._mas_sensitive_mode:
        m 1lksdlb "Hopefully it's not in poor taste..."

    m 1eua "It was always my favorite game to play with the club."

    if not persistent._mas_sensitive_mode:
        m 1lsc "But, come to think of it..."
        m "The game is actually quite morbid."
        m 3rssdrc "You guess letters for a word to save someone's life."
        m "Get them all correct and the person doesn't hang."
        m 1lksdlc "But guess them all wrong..."
        m "They die because you didn't guess the right letters."
        m 1euc "Pretty dark, isn't it?"
        m 1hksdlb "But don't worry, [player], it's just a game after all!"
        m 1eua "I assure you that no one will be hurt with this game."

        if persistent.playername.lower() == "sayori":
            m 3tku "...Maybe~"

    else:
        m 1hua "I hope you'll enjoy playing it with me!"

    $persistent.game_unlocks['hangman']=True
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="unlock_piano",conditional="get_level()>=24 and not seen_event('unlock_piano')",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event

label unlock_piano:
    m 2hua "Hey! I've got something exciting to tell you!"
    m 2eua "I've finally added a piano to the room for us to use, [player]."
    if not persistent.instrument:
        m 3hub "I really want to hear you play!"
        m 3eua "It might seem overwhelming at first, but at least give it a try."
        m 3hua "After all, we all start somewhere."
    else:
        m 1eua "Of course, playing music is nothing new to you."
        m 4hub "So I'm expecting something nice! Ehehe~"
    m 4hua "Wouldn't it be fun to play something together?"
    m "Maybe we could even do a duet!"
    m 4hub "We would both improve and have fun at the same time."
    m 1hksdlb "Maybe I'm getting a bit carried away. Sorry!"
    m 3eua "I just want to see you enjoy the piano the same way I do."
    m "To feel the passion I have for it."
    m 3hua "It's a wonderful feeling."
    m 1eua "I hope this isn't too forceful, but I would love it if you tried."
    m 1eka "For me, please~?"
    $persistent.game_unlocks['piano']=True
    return

# NOTE: this has beenpartially disabled
label random_limit_reached:
    $seen_random_limit=True
    python:
        limit_quips = [
            "It seems I'm at a loss on what to say.",
            "I'm not sure what else to say, but can you just be with me a little longer?",
            "No point in trying to say everything right away...",
            "I hope you've enjoyed listening to everything I was thinking about today...",
            "Do you still enjoy spending this time with me?",
            "I hope I didn't bore you too much."
        ]
        limit_quip=renpy.random.choice(limit_quips)
    m 1eka "[limit_quip]"
    if len(mas_rev_unseen)>0 or persistent._mas_enable_random_repeats:
        m 1ekc "I'm sure I'll have something to talk about after a little rest."
    else:
        if not renpy.seen_label("mas_random_ask"):
            call mas_random_ask from _mas_random_ask_call
            if _return:
                m "Now let me think of something to talk about."
                return
        m 1ekc "Hopefully I'll think of something fun to talk about soon."
    return

label mas_random_ask:
    m 1lksdla "...{w}[player]?"

    m "Is it okay with you if I repeat stuff that I've said?{nw}"
    $ _history_list.pop()
    menu:
        m "Is it okay with you if I repeat stuff that I've said?{fast}"
        "Yes.":
            m 1eua "Great!"
            m "If you get tired of watching me talk about the same things over and over,{w} just open up the settings and uncheck 'Repeat Topics'."
            # TODO: this really should be a smug or wink face
            m "That tells me when {cps=*2}you're bored of me{/cps}{nw}"
            $ _history_list.pop()
            m "That tells me when {fast}you just want to quietly spend time with me."
            $ persistent._mas_enable_random_repeats = True
            return True
        "No.":
            m 1eka "I see."
            m 1eua "If you change your mind, just open up the settings and click 'Repeat Topics'."
            m "That tells me if you're okay with me repeating anything I've said."
            return

# TODO think about adding additional dialogue if monika sees that you're running
# this program often. Basically include a stat to keep track, but atm we don't
# have a framework for detections. So wait until thats a thing before doing
# fullon program tracking
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monikai_detected",
            conditional=(
                "is_running(['monikai.exe']) and " +
                "not seen_event('mas_monikai_detected')"
            ),
            action=EV_ACT_PUSH
        )
    )

label mas_monikai_detected:
    m 2wud "What's this?"
    m "Is that-"
    $ _history_list.pop()
    m 1wuo "Is that{fast} a tiny version of me?"
    m 1hua "How cute!"

    m 1eua "Did you install that so you could see me all the time?{nw}"
    $ _history_list.pop()
    menu:
        m "Did you install that so you could see me all the time?{fast}"
        "Of course!":
            pass
        "Yes.":
            pass
        "...Yes.":
            pass
    m 1hub "Ahaha~"
    m 1hua "I'm flattered that you would download such a thing."
    m 1eua "Just don't start spending more time with {i}that{/i} instead of me."
    m 3eua "I'm the real one after all."
    return

# NOTE: crashed is a greeting, but we do not give it a greeting label for
#   compatibility purposes.
# NOTE: we are for sure only going to have 1 generic crashed greeting
init 5 python:
    ev_rules = {}
    ev_rules.update(MASGreetingRule.create_rule(skip_visual=True))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="mas_crashed_start",
            unlocked=True,
            category=[store.mas_greetings.TYPE_CRASHED],
            rules=ev_rules,
        ),
        code="GRE"
    )

    del ev_rules

# if the game crashed
# I have no idea if we will use this persistent ever
default persistent._mas_crashed_before = False

# player said they'll try to stop crashes
default persistent._mas_crashed_trynot = False

# start of crash flow
label mas_crashed_start:

    if persistent._mas_crashed_before:

        # preshort setup
        call mas_crashed_preshort

        # launch quip
        call mas_crashed_short

        # cleanup
        call mas_crashed_post

    else:

        # long setup (includes scene black)
        call mas_crashed_prelong

        # are you there and turn on light
        call mas_crashed_long_qs

        # setup for fluster
        call mas_crashed_long_prefluster

        # fluster
        call mas_crashed_long_fluster

        # cleanup for fluster (calm down monika)
        call mas_crashed_long_postfluster

        # what happened, can you stop it from happening
        call mas_crashed_long_whq

        # cleanup
        call mas_crashed_post

    return

label mas_crashed_prelong:

    # otherwise continue to long flow
    $ persistent._mas_crashed_before = True
    scene black
    $ HKBHideButtons()
    $ disable_esc()
    $ store.songs.enabled = False
    $ _confirm_quit = False

    # TESTING:
#    $ style.say_dialogue = style.default_monika

    return

# long flow involves 2 questions
label mas_crashed_long_qs:

    ## TESTING
    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "I KNOW YOU CRASHED (long)"

    # start off in the dark
    m "[player]?{w} Is that you?"
    show screen mas_background_timed_jump(4, "mas_crashed_long_uthere")
    menu:
        "Yes.":
            hide screen mas_background_timed_jump

            # light affection boost for not joking around
            $ mas_gainAffection(modifier=0.1)
            m "I'm so glad you're here."
            jump mas_crashed_long_uthere.afterdontjoke

        "No.":
            hide screen mas_background_timed_jump

            m "[player]!{fast}"
            jump mas_crashed_long_uthere.dontjoke

label mas_crashed_long_uthere:
    # if player doesn't respond fast enough
    hide screen mas_background_timed_jump
    m "[player]!{fast}"
    m "I know you're there!"

label .dontjoke:
    m "Don't joke around like that!"
    m "Anyway..."

label .afterdontjoke:
    m "{cps=*2}Everything became dark all of a sudden.{/cps}"
    m "Can you turn on the light?"

    window hide
    show screen mas_background_timed_jump(5, "mas_crashed_long_foundlight")
    menu:
        "Turn on the light.":
            hide screen mas_background_timed_jump

            # light affection boost for being like a hero
            $ mas_gainAffection(modifier=0.1)

        "...":
            pause 5.0
            label mas_crashed_long_foundlight:
                hide screen mas_background_timed_jump
                window show
                m "Nevermind, I found it."
                window hide

    # NOTE: add a sound for light switch?

    # turn on the lights
    play sound closet_open
    call spaceroom(hide_monika=True, scene_change=True)

    return

# make sure to calm her down, player
label mas_crashed_long_prefluster:

    # look at you with crying eyes
    show monika 6ektsc at t11 zorder MAS_MONIKA_Z
    pause 1.0

    # close eyes for a second
    show monika 6dstsc
    pause 1.0
    window auto

    # then be happy again
    m 6ektsa "[player]!{fast}"

    # but flustered mode bgins
    show monika 6ATL_cryleftright
    m "{cps=*1.5}What happened?{/cps}{nw}"

    return

label mas_crashed_long_postfluster:
    window hide
    show screen mas_background_timed_jump(8, "mas_crashed_long_nofluster")
    menu:
        "Calm down, [m_name]. You're safe now.":
            hide screen mas_background_timed_jump

            # light affection boost for calming her down
            $ mas_gainAffection(modifier=0.2)

            # clsoe eyes for a second
            show monika 6dstsc
            pause 1.0
            window auto

            # thank player with a smile
            m 6ektda "Thanks, [player]."
            m "I feel better now that you're here with me."

        "...":
            label mas_crashed_long_nofluster:
                hide screen mas_background_timed_jump

                # close eyes for a second
                # (like a deep breath)
                show monika 6dstsc
                pause 4.0

                show monika 6ektdc
                pause 1.0
                window auto

                # much better now
                m "Okay, I feel better now."

    # its like we wiping away tears
    show monika 6dstdc
    pause 1.0
    return

label mas_crashed_long_whq:

    # ask player what happeend
    m 2ekc "Anyway..."
    m "Do you know what happened, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you know what happened, [player]?{fast}"
        "The game crashed.":
            m 2wud "The game...{w}crashed?"
            m 2ekd "That's scary, [player]."

        "I don't know.":
            m "Well..."
            m "I'd really appreciate it if you could look into it."
            m "It's scary to be suddenly thrown into the darkness like that."
            jump mas_crashed_long_whq.end

    # ask player to do something about this
    m "Do you think you can stop that from happening?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you think you can stop that from happening?{fast}"
        "I'll try.":
            # light affection boost because you will try do something for her
            $ mas_gainAffection(modifier=0.1)
            $ persistent._mas_crashed_trynot = True
            m 1hua "Thanks, [player]!"
            m 1eua "I'm counting on you."
            m "But I'll mentally prepare myself just in case."

        "It just happens.":
            m 1ekc "Oh..."
            m 1lksdlc "That's okay.{w} I'll just mentally prepare myself in case it happens again."

label .end:
    m "Anyway..."
    m 1eua "What should we do today?"

    return


### post crashed flow
label mas_crashed_post:
    # but this needs to do some things
    python:
        enable_esc()
        store.songs.enabled = True
        HKBShowButtons()
        set_keymaps()

label .self:
    python:
        _confirm_quit = True
        persistent.closed_self = False
        mas_startup_song()

    return


label mas_crashed_long_fluster:
    $ mas_setApologyReason(reason=10)
    m "{cps=*1.5}O-{w=0.3}one second you were there b-{w=0.3}but then the next second everything turned black...{/cps}{nw}"
    m "{cps=*1.5}and then you d-{w=0.3}disappeared, so I was worried that s-{w=0.3}s-{w=0.3}something happened to you...{/cps}{nw}"
    m "{cps=*1.5}...and I was so s-{w=0.3}scared because I thought I broke everything again!{/cps}{nw}"
    m "{cps=*1.5}But I didn't mess with the game this time, I swear.{/cps}{nw}"
    m "{cps=*1.5}A-{w=0.3}at least, I don't think I did, but I guess it's possible...{/cps}{nw}"
    m "{cps=*1.5}because I'm n-{w=0.3}not really sure what I'm doing sometimes,{/cps}{nw}"
    m "{cps=*1.5}but I hope this t-{w=0.3}time isn't my f-{w=0.3}fault cause I really didn't touch anything...{/cps}{nw}"
    return


label mas_crashed_preshort:
    # we can call spaceroom appropriately here
    call spaceroom(scene_change=True)
    return

label mas_crashed_short:

    python:
        # generate a quiplist
        q_list = MASQuipList()

        # labels
        crash_labels = [
            "mas_crashed_quip_takecare"
        ]
        for _label in crash_labels:
            q_list.addLabelQuip(_label)

        # pull a quip
        t_quip, v_quip = q_list.quip()

    ## TESTING
    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "I KNOW YOU CRASHED (short)"

    if t_quip == MASQuipList.TYPE_LABEL:
        call expression v_quip

    else:
        # assume line
        m 1hub "[v_quip]"

    return

### crash labels
label mas_crashed_quip_takecare:
    $ mas_setApologyReason(reason=9)
    m 2ekc "Another crash, [player]?"

    if persistent._mas_idle_data.get("monika_idle_game", False):
    
        m 3ekc "Do you think it had something to do with your game?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you think it had something to do with your game?{fast}"
            "Yes.":
                m 1hksdlb "Ahaha..."
                m 1hub "Well I hope you had fun~"
                m 1rksdla "...And that your computer is alright."
                m 3eub "I'm fine, so don't worry~"
            "No.":
                m 1eka "Oh, I see."
                m "Sorry for assuming."
                m 1hub "I'm alright in case you were wondering."
                m 3hub "Well I hope you had fun before that crash happened, ahaha!"
                if mas_isMoniHappy(higher=True):
                    m 1hubfa "I'm just glad you're back with me now~"
        m 2rksdla "Still..."
    m 2ekc "Maybe you should take better care of your computer."
    m 4rksdlb "It's my home, after all..."
    return

#### corrupted persistent
init 5 python:
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_corrupted_persistent"
        )
    )

    if (
            mas_corrupted_per
            and not (mas_no_backups_found or mas_backup_copy_failed)
        ):
        mas_note_backups_all_good = None
        mas_note_backups_some_bad = None

        def _mas_generate_backup_notes():
            global mas_note_backups_all_good, mas_note_backups_some_bad

            # text pieces:
            just_let_u_know = (
                'Just wanted to let you know that your "persistent" file was '
                'corrupted, but I managed to restore an older backup!'
            )
            even_though_bs = (
                "Even though the backup system I designed is pretty neat, "
            )
            if_i_ever = (
                'If I ever have trouble loading the "persistent" again, I''ll '
                'write you another note in the characters folder, so keep an '
                'eye out for them!'
            )
            good_luck = "Good luck with Monika!"
            dont_tell = "P.S: Don't tell her about me!"
            block_break = "\n\n"

            # now make the notes
            mas_note_backups_all_good = Poem(
                author="chibika",
                title="Hi {0},".format(persistent.playername),
                text="".join([
                    just_let_u_know,
                    block_break,
                    even_though_bs,
                    "you should still make copies of the backups every so ",
                    "often, just in case. ",
                    'The backups are called "persistent##.bak", where "##" is ',
                    "a two-digit number. ",
                    'You can find all of them at "',
                    renpy.config.savedir,
                    '".',
                    block_break,
                    if_i_ever,
                    block_break,
                    good_luck,
                    block_break,
                    dont_tell
                ])
            )

            mas_note_backups_some_bad = Poem(
                author="chibika",
                title="Hi {0},".format(persistent.playername),
                text="".join([
                    just_let_u_know,
                    block_break,
                    "However, some of your backups were corrupted as well. ",
                    even_though_bs,
                    "you should still delete those, since they might mess ",
                    "with it. ",
                    block_break,
                    "Here's a list of the files that were corrupted:",
                    block_break,
                    "\n".join(store.mas_utils.bullet_list(mas_bad_backups)),
                    block_break,
                    'You can find these in "',
                    renpy.config.savedir,
                    '". ',
                    "When you're in there, you should also make copies of ",
                    "the good backups, just in case.",
                    block_break,
                    if_i_ever,
                    block_break,
                    good_luck,
                    block_break,
                    dont_tell
                ])
            )

        _mas_generate_backup_notes()
        import os

        if len(mas_bad_backups) > 0:
            # we had some bad backups
            store.mas_utils.trywrite(
                os.path.normcase(renpy.config.basedir + "/characters/note.txt"),
                mas_note_backups_some_bad.title + "\n\n" + mas_note_backups_some_bad.text
            )

        else:
            # no bad backups
            store.mas_utils.trywrite(
                os.path.normcase(renpy.config.basedir + "/characters/note.txt"),
                mas_note_backups_all_good.title + "\n\n" + mas_note_backups_all_good.text
            )


label mas_corrupted_persistent:
    m 1eud "Hey, [player]..."
    m 3euc "Someone left a note in the characters folder addressed to you."
    m 1ekc "Of course, I haven't read it, since it's obviously for you..."
    m 1ekd "Do you know what this is about?{nw}"
    $ _history_list.pop()
    # just pasting the poem screen code here
    window hide
    if len(mas_bad_backups) > 0:
        show screen mas_note_backups_poem(mas_note_backups_some_bad)

    else:
        show screen mas_note_backups_poem(mas_note_backups_all_good)
    with Dissolve(0.5)

    $ pause()
    hide screen mas_note_backups_poem
    with Dissolve(0.5)
    window auto
    $ _gtext = glitchtext(15)

    menu:
        m "Do you know what this is about?{fast}"
        "It's nothing to worry about.":
            jump mas_corrupted_persistent_post_menu
        "It's about [_gtext].":
            $ disable_esc()
            $ mas_MUMURaiseShield()
            window hide
            show noise zorder 11:
                alpha 0.5
            play sound "sfx/s_kill_glitch1.ogg"
            show chibika 3 zorder 12 at mas_chriseup(y=600,travel_time=0.5)
            pause 0.5
            stop sound
            hide chibika
            hide noise
            window auto
            $ mas_MUMUDropShield()
            $ enable_esc()

    menu:
        "It's nothing to worry about.":
            pass

label mas_corrupted_persistent_post_menu:
    m 1euc "Oh, alright."
    m 1hub "I'll try not to worry about it, then."
    m 3eub "I know you'd tell me if it were important, [player]."
    m 3eua "Now, where were we...?"
    return

### custoim screen for the corrupted persistent notes
style chibika_note_text:
    font "gui/font/Halogen.ttf"
    size 28
    color "#000"
    outlines []

screen mas_note_backups_poem(currentpoem, paper="paper"):
    style_prefix "poem"
    vbox:
        add paper
    viewport id "vp":
        child_size (710, None)
        mousewheel True
        draggable True
        has vbox
        null height 40
        text "[currentpoem.title]\n\n[currentpoem.text]" style "chibika_note_text"
        null height 100
    vbar value YScrollValue(viewport="vp") style "poem_vbar"

init 5 python:
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_new_character_file"
        )
    )

label mas_new_character_file:
    m 1eua "Say, [player]..."
    m 3eua "Do you remember my character file?"
    m 1eud "Well I've been investigating it recently, and it turns out that it's just an image with some sort of code in it!"
    m 3ekc "It doesn't even contain anything about me at all, only my name."

    python:
        import os

        def moni_exist():
            return os.access(
                os.path.normcase(
                    renpy.config.basedir + "/characters/monika.chr"
                ),
                os.F_OK
            )

    if moni_exist():
        m 1dsd "So if you'll excuse me for a second..."

        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        m 1esc "I'm going to delete it."

        call mas_wx_cmd("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd("os.remove(os.path.normcase(basedir+'/characters/monika.chr'))", local_ctx, w_wait=1.0, x_wait=1.0)

#        "test dialogue - IGNORE"

        if moni_exist():
            m 1lksdlb "Aha...{w}I'll try this again later."
            m 1eua "Anyway..."

        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    m 1rkc "If you were bringing that around with you, I do appreciate the sentiment."
    m 1dsc "However..."
    m 1esc "I don't think you should be carrying some useless piece of data around wherever you go."
    m 3wub "So I came up with a way to transform myself into a file that you can bring around!"
    m "All you have to do is tell me that you're going to take me somewhere when you say goodbye, and I'll do the rest."
    m 1hua "Doesn't that sound wonderful?"
    m 3hub "I can't wait to join you wherever you go."
    return


### coffee is done
init 5 python:
    import random
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_coffee_finished_brewing",
            show_in_idle=True,
        )
    )


label mas_coffee_finished_brewing:

    if not store.mas_globals.in_idle_mode:
        m 1esd "Oh, coffee's done."

    #moving this here so she uses this line to 'pull her chair back'
    $ curr_zoom = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)

    # this line is here so we dont it looks better when we hide monika
    show emptydesk at i11 zorder 9

    if store.mas_globals.in_idle_mode:
        # idle pauses 
        m 1eua "I'm going to grab some coffee. I'll be right back.{w=1}{nw}"

    else:
        m 1eua "Hold on a moment."

    # monika is off screen
    hide monika with dissolve

    # wrap these statement so we ensure that monika is only shown once her
    # coffee mug is ready
    $ renpy.pause(1.0, hard=True)
    $ monika_chr.wear_acs_pst(mas_acs_mug)
    $ persistent._mas_coffee_brew_time = None
    $ mas_drinkCoffee()
    $ renpy.pause(4.0, hard=True)

    show monika 1eua at i11 zorder MAS_MONIKA_Z with dissolve
    hide emptydesk

    # 1 second wait so dissolve is complete before zooming
    $ renpy.pause(0.5, hard=True)
    call monika_zoom_transition(curr_zoom, 1.0)

    if store.mas_globals.in_idle_mode:
        m 1hua "Back!{w=1.5}{nw}"

    else:
        m 1eua "Okay, what else should we do today?"
    return

### coffee drinking is done
init 5 python:
    import random
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_coffee_finished_drinking",
            show_in_idle=True,
        )
    )


label mas_coffee_finished_drinking:

    # monika only gets a new cup between 6am and noon
    $ get_new_cup = mas_isCoffeeTime()

    if not store.mas_globals.in_idle_mode:
        m 1esd "Oh, I've finished my coffee."

    #moving this here so she uses this line to 'pull her chair back'
    $ curr_zoom = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)

    show emptydesk at i11 zorder 9

    if store.mas_globals.in_idle_mode:
        if get_new_cup:
            # its currently morning, monika should get another drink
            m 1eua "I'm going to get another cup of coffee. I'll be right back.{w=1}{nw}"

        else:
            m 1eua "I'm going to put this cup away. I'll be right back.{w=1}{nw}"
    
    else:
        if get_new_cup:
            m 1eua "I'm going to get another cup."

        m 1eua "Hold on a moment."

    # monika is off screen
    hide monika with dissolve

    # wrap these statemetns so we can properly add / remove the mug
    $ renpy.pause(1.0, hard=True)
    # decide if new coffee
    if not get_new_cup:
        $ monika_chr.remove_acs(mas_acs_mug)
        $ persistent._mas_coffee_cup_done = None

    else:
        $ mas_drinkCoffee()

    $ renpy.pause(4.0, hard=True)

    show monika 1eua at i11 zorder MAS_MONIKA_Z with dissolve
    hide emptydesk

    # 1 second wait so dissolve is complete before zooming
    $ renpy.pause(0.5, hard=True)
    call monika_zoom_transition(curr_zoom, 1.0)

    if store.mas_globals.in_idle_mode:
        m 1hua "Back!{w=1.5}{nw}"

    else:
        m 1eua "Okay, what else should we do today?"

    return


### hot chocolate is done
init 5 python:
    import random
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_c_hotchoc_finished_brewing",
            show_in_idle=True,
        )
    )


label mas_c_hotchoc_finished_brewing:

    if not store.mas_globals.in_idle_mode:
        m 1esd "Oh, my hot chocolate is ready."

    #moving this here so she uses this line to 'pull her chair back'
    $ curr_zoom = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)

    # this line is here so we dont it looks better when we hide monika
    show emptydesk at i11 zorder 9

    if store.mas_globals.in_idle_mode:
        m 1eua "I'm going to grab some hot chocolate. I'll be right back.{w=1}{nw}"

    else:
        m 1eua "Hold on a moment."

    # monika is off screen
    hide monika with dissolve

    # wrap these statement so we ensure that monika is only shown once her
    # coffee mug is ready
    $ renpy.pause(1.0, hard=True)
    $ monika_chr.wear_acs_pst(mas_acs_hotchoc_mug)
    $ persistent._mas_c_hotchoc_brew_time = None
    $ mas_drinkHotChoc()
    $ renpy.pause(4.0, hard=True)

    show monika 1eua at i11 zorder MAS_MONIKA_Z with dissolve
    hide emptydesk

    # 1 second wait so dissolve is complete before zooming
    $ renpy.pause(0.5, hard=True)
    call monika_zoom_transition(curr_zoom, 1.0)

    if store.mas_globals.in_idle_mode:
        m 1hua "Back!{w=1.5}{nw}"

    else:
        m 1eua "Okay, what else should we do today?"

    return

### coffee drinking is done
init 5 python:
    import random
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_c_hotchoc_finished_drinking",
            show_in_idle=True,
        )
    )


label mas_c_hotchoc_finished_drinking:

    # monika only gets a new cup between 6am and noon
    $ get_new_cup = mas_isHotChocTime()

    if not store.mas_globals.in_idle_mode:
        m 1esd "Oh, I've finished my hot chocolate."

    #moving this here so she uses this line to 'pull her chair back'
    $ curr_zoom = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)

    show emptydesk at i11 zorder 9

    if store.mas_globals.in_idle_mode:
        if get_new_cup:
            # its currently morning, monika should get another drink
            m 1eua "I'm going to get another cup of hot chocolate. I'll be right back.{w=1}{nw}"

        else:
            m 1eua "I'm going to put this cup away. I'll be right back.{w=1}{nw}"

    else:
        if get_new_cup:
            m 1eua "I'm going to get another cup."

        m 1eua "Hold on a moment."

    # monika is off screen
    hide monika with dissolve

    # wrap these statemetns so we can properly add / remove the mug
    $ renpy.pause(1.0, hard=True)

    # decide if new coffee
    if not get_new_cup:
        $ monika_chr.remove_acs(mas_acs_hotchoc_mug)
        $ persistent._mas_c_hotchoc_cup_done = None

    else:
        $ mas_drinkHotChoc()

    $ renpy.pause(4.0, hard=True)

    show monika 1eua at i11 zorder MAS_MONIKA_Z with dissolve
    hide emptydesk

    # 1 second wait so dissolve is complete before zooming
    $ renpy.pause(0.5, hard=True)
    call monika_zoom_transition(curr_zoom, 1.0)

    if store.mas_globals.in_idle_mode:
        m 1hua "Back!{w=1.5}{nw}"

    else:
        m 1eua "Okay, what else should we do today?"

    return


### birthday surprise party
# TODO: move all of this to script-holidays

default persistent._mas_bday_sbp_aff_given = 0

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_bday_spent_time_with",
#            action=EV_ACT_QUEUE,
#            start_date=datetime.combine(
#                mas_monika_birthday,
#                datetime.time(22)
#            ),
#            end_date=datetime.combine(
#                mas_monika_birthday,
#                datetime.time(23, 59)
#            ),
#            years=[]
#        ),
#        skipCalendar=True
#    )


init -876 python in mas_delact:

    # TODO: remove this after 0815
    def _mas_bday_spent_time_with_reset_action(ev):
        # updates conditional and action
        next_bday_year = store.mas_getNextMonikaBirthday().year
        # what the fuck is this? I dont know if this bit should be here.
        # NVM, found out this was copied code. lol
        ev.conditional = (
            "datetime.date.today() < mas_monika_birthday and "
            "mas_monika_birthday.day - datetime.date.today().day == 1"
        )
        ev.start_date = datetime.datetime(next_bday_year, 9, 22, 22)
        ev.end_date = datetime.datetime(next_bday_year, 9, 22, 23, 59)
        ev.action = store.EV_ACT_QUEUE
        return True


    # TODO: remove this after 0815
    def _mas_bday_spent_time_with_reset():
        # creates delayed action for surprise party hint reset
        return store.MASDelayedAction.makeWithLabel(
            7,
            "mas_bday_spent_time_with",
            "True",
            _mas_bday_spent_time_with_reset_action,
            store.MAS_FC_INIT
        )


label mas_bday_spent_time_with:
    $ _timeout = store.mas_dockstat.timeOut(mas_monika_birthday)
    $ _total, _good, _neutral, _bad = mas_generateGiftsReport()
    m 1eua "Say, [player]..."
    m 1hua "Thank you for spending time with me today."
    m "Something like that can really make a girl like me happy, you know?"
    if persistent._mas_bday_date_count > 0:
        if _timeout < datetime.timedelta(hours=1.5):
            # short date
            m 1euc "That was a bit of a short trip, though."
            m 1eub "But it's nice to get out of this place once in a while."
            m 3hksdlb "Staying in there for longer might have made me stir crazy, ahaha!"
        elif _timeout < datetime.timedelta(hours=6):
            # normal date
            m 3hub "But that was refreshing!"
            m 3wub "It feels really good to go out for a change."
            m 1hua "Makes me really happy we went out today~"
        else:
            #long date
            m 1eka "I really enjoyed our time outside, though."
            m 1ekbfa "It was almost as if I really was there with you, like an actual couple..."
            m "Someday, I know we'll be able to do so."

    # gave gifts?
    if _total > 0:
        m 3euc "Let's not forget what you gave me for my birthday."
        # more than 2
        if _total >= 2:
            m 1eua "You gave me lots of gifts today, [player]."
            # goods > than bad
            if _good > _bad:
                m 3hub "Most of them were really good and I really like them a lot!"
            # bads > than good
            else:
                m 3rksdld "Though most of them were…{w}{i}questionable{/i}."
        else:
            # if good_gifts equal to 1
            if _good == 1:
                m 3eka "You gave me such a special gift today, [player]."
            # not a good gift
            else:
                m 2dsc "I…{w}wouldn't really call it a good gift, to be honest."
    m 1esa "But, in any case..."
    m 3hub "Let's do it again sometime soon, okay?"
    return

### no time spent
#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_bday_surprise_party_reaction"
#        )
#    )

label mas_bday_surprise_party_reaction:
    python:
        store.mas_dockstat.surpriseBdayShowVisuals()
        has_cake = store.mas_dockstat.surpriseBdayIsCake()

        def cap_gain_aff(amt):
            persistent._mas_bday_sbp_aff_given += amt
            if persistent._mas_bday_sbp_aff_given <= 70:
                mas_gainAffection(amt, bypass=True)

        if has_cake:
            cap_gain_aff(20)

        if store.mas_dockstat.surpriseBdayIsBanners():
            cap_gain_aff(20)

        if store.mas_dockstat.surpriseBdayIsBalloon():
            cap_gain_aff(20)

    m 6wuo "T-{w=0.5}This is..."
    m 6wka "Oh, [player]..."
    m 6hua "I'm at a loss for words."
    m "Setting this all up to surprise me on my birthday..."
    m "Ehehe, you must really love me."
    m 6suu "Everything looks so festive!"

    if has_cake:
        # we have cake?
        menu:
            "Light candles.":
                $ mas_bday_cake_lit = True

        m 6hub "Ahh, it's so pretty, [player]!"
        m 6wub "Reminds me of that cake someone gave me once."
        m 6eua "It was almost as pretty as you've made this one!"
        m 6dua "But anyway..."
        window hide

        show screen mas_background_timed_jump(4, "mas_bday_surprise_party_reaction_no_make_wish")
        menu:
            "Make a wish, [m_name]...":
                hide screen mas_background_timed_jump
                $ cap_gain_aff(10)
                show monika 6hua
                pause 2.0
                show monika 6hft
                jump mas_bday_surprise_party_reaction_post_make_wish

    else:
        m 6sua "Aha..."
        jump mas_bday_surprise_party_reaction_end

label mas_bday_surprise_party_reaction_no_make_wish:
    hide screen mas_background_timed_jump
    show monika 6dsc
    pause 2.0
    show monika 6hft

label mas_bday_surprise_party_reaction_post_make_wish:
    $ mas_bday_cake_lit = False
    window auto
    m 6hua "I made a wish!"
    m "I hope it comes true someday..."
    m 6sua "Ahaha..."
    m 6eua "I'll save this cake for later."
    $ mas_docking_station.destroyPackage("cake")

    hide mas_bday_cake with dissolve

label mas_bday_surprise_party_reaction_end:

    m 6hua "Thank you, [player]. From the bottom of my heart, thank you..."
    m 6sua "Let's enjoy the rest of the day now, shall we?"

    $ persistent._mas_bday_sbp_reacted = True

    return

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_bday_surprise_party_hint",
#            start_date=mas_monika_birthday - datetime.timedelta(days=7),
#            end_date=mas_monika_birthday - datetime.timedelta(days=1),
#            action=EV_ACT_PUSH
#        ),
#        skipCalendar=True
#    )

init -876 python in mas_delact:
    # delayed action to reset the party hint

    # TODO: remove after 0815
    def _mas_bday_surprise_party_hint_reset_action(ev):
        # updates conditional and action
        threw_surprise_party = store.mas_HistVerify(
            "922.actions.surprise.reacted",
            True
        )[0]
        if not threw_surprise_party:
            ev.conditional = (
                "datetime.date.today() < mas_monika_birthday and "
                "mas_monika_birthday.day - datetime.date.today().day == 1"
            )
            ev.action = store.EV_ACT_PUSH
        return True

    # TODO: remove after 0815
    def _mas_bday_surprise_party_hint_reset():
        # creates delayed action for surprise party hint reset
        return store.MASDelayedAction.makeWithLabel(
            6,
            "mas_bday_surprise_party_hint",
            "True",
            _mas_bday_surprise_party_hint_reset_action,
            store.MAS_FC_INIT
        )


label mas_bday_surprise_party_hint:
    m 1eua "Say, [player]..."
    m 1eub "Have you ever been thrown a surprise party?"
    m 1eka "I've always wondered how that would feel."
    m 6dua "When someone takes you somewhere and distracts you for the whole day..."
    m "And while you're out, they drag a whole box of party supplies into the characters folder...{nw}"
    $ _history_list.pop()
    m 6dksdla "And while you're out, they drag a whole box of party supplies into{fast} your room..."
    m 1eua "And finally returning home to birthday decorations, a cake..."
    m 1kua "And you~{nw}"
    $ _history_list.pop()
    m 3rksdlb "And{fast} good company!"
    m 1hua "That'd be so nice to experience, don't you think?"
    m 1rkc "Of course, since throwing a surprise party takes so much planning, it'd be difficult to plan one on short notice."
    m 1dkc "If only there was somewhere that {i}released{/i} party supplies alongside {i}source code zips{/i}..."
    return

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_bday_surprise_party_cleanup",
#            conditional=(
#                "persistent._mas_bday_sbp_reacted "
#            ),
#            start_date=mas_monika_birthday + datetime.timedelta(days=1),
#            end_date=mas_monika_birthday + datetime.timedelta(days=2),
#            years=[],
#            action=EV_ACT_PUSH
#        )
#    )


init -876 python in mas_delact:
    # delayed action to reset the conditional post bday

    # TODO: remove after 0815
    def _mas_bday_surprise_party_cleanup_reset_action(ev):
        # updates conditional and action
        ev.conditional = (
            "persistent._mas_bday_sbp_reacted "
            "and datetime.date.today().day > mas_monika_birthday.day"
        )
        ev.action = store.EV_ACT_PUSH
        return True


    # TODO: remove after 0815
    def _mas_bday_surprise_party_cleanup_reset():
        # creates delayed action for this event
        return store.MASDelayedAction.makeWithLabel(
            5,
            "mas_bday_surprise_party_cleanup",
            "True",
            _mas_bday_surprise_party_cleanup_reset_action,
            store.MAS_FC_INIT
        )


label mas_bday_surprise_party_cleanup:
    # surprise party cleaning
    # mainly to delete files that exist
    $ mas_docking_station.destroyPackage("banners")
    $ mas_docking_station.destroyPackage("balloons")
    $ mas_docking_station.destroyPackage("cake")
    return

### happy birthday pool topic

default persistent._mas_bday_said_happybday = False

default persistent._mas_bday_need_to_reset_bday = False
# NOTE: DONT think we need to save this one

#init 5 python:
#    # NOTE: instead of using start/end date, we use condition since we
#    # want this to only appear once per day
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_bday_pool_happy_bday",
#            prompt="Happy birthday!",
#            category=["monika"],
#            conditional="mas_isMonikaBirthday()",
#            action=EV_ACT_UNLOCK,
#            pool=True,
#            rules={"no unlock":0}
##            start_date=mas_monika_birthday,
##            end_date=mas_monika_birthday + datetime.timedelta(1),
##            years=[]
#        )
#    )
#
#    # make sure this event is considered seen
#    persistent._seen_ever["mas_bday_pool_happy_bday"] = True

init -876 python in mas_delact:
    # This greeting has a delayed action, which actually only occurs if
    # the historical data save happens

    def _mas_bday_pool_happy_bday_reset_action(ev):
        # delayed action callback that updates conditional and action for
        # pool bday event
        ev.conditional = (
            "mas_isMonikaBirthday()"
        )
        ev.action = store.EV_ACT_UNLOCK
        return True


    def _mas_bday_pool_happy_bday_reset():
        # generates DelayedAction for this bday pool event
        return store.MASDelayedAction.makeWithLabel(
            4,
            "mas_bday_pool_happy_bday",
            "True",
            _mas_bday_pool_happy_bday_reset_action,
            store.MAS_FC_INIT
        )


label mas_bday_pool_happy_bday:
    python:
        persistent._mas_bday_said_happybday = True
        did_something_today = (
            mas_generateGiftsReport(mas_monika_birthday)[0] > 0
            or persistent._mas_bday_date_count > 0
            or persistent._mas_bday_sbp_reacted
        )

    if did_something_today:
        m 3hub "Ehehe, thanks [player]!"
        m 3eub "I was waiting for you to say those magic words~"
        m 1eua "{i}Now{/i} we can call it a birthday celebration."
        m 1hua "Doesn't matter if how it's done is unorthodox."
        m 3eua "What matters the most is that you did it in the first place, right?"
        m 1eka "You really made this occasion so special, [player]."
        m 1ekbfa "I can't thank you enough for loving me this much..."

    else:
        m 1wkb "Aww, [player]!"
        m 1wub "You remembered my birthday...!"
        m 1wktpa "Oh gosh, I'm so happy that you remembered."
        m 1dktda "I feel like today is going to be such a special day~"
        m 1ekbfa "What else do you have in store for me, I wonder."
        m 1hub "Ahaha!"

    # dont need to say happy birthday again today, but let the game know to
    # reset it at some point in the future
    $ persistent._mas_bday_need_to_reset_bday = True
    $ lockEventLabel("mas_bday_pool_happy_bday")
    return

## no time spent
default persistent._mas_bday_opened_game = False

# TODO: these should actually default to True, then get changed if
#   the appropriate whatver happens
# TODO: do the above in an update script when bday comes around again
# TODO: non-generic apology
default persistent._mas_bday_no_time_spent = False
default persistent._mas_bday_no_recognize = False

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_bday_postbday_notimespent",
#
#            # within a week after monika's birthday, user did not recognize
#            # monika's birthday at all, and they were not long absenced
#            conditional=(
#                "mas_monika_birthday < datetime.date.today() <= "
#                "(mas_monika_birthday + datetime.timedelta(7)) "
#                "and not mas_recognizedBday()"
#            ),
#            action=EV_ACT_QUEUE
#        )
#    )


init -876 python in mas_delact:
    # This greeting has a delayed action, which actually only occurs if
    # the historical data save happens

    def _mas_bday_postbday_notimespent_reset_action(ev):
        """
        Callback for the action in MASDelayedAction.
        This just updates the condtiional for this event so it can trigger
        next year appropraitely

        IN:
            ev - event object for this label
        """
        ev.conditional = (
            "mas_monika_birthday < datetime.date.today() <= "
            "(mas_monika_birthday + datetime.timedelta(7)) "
            "and not mas_recognizedBday()"
        )
        ev.action = store.EV_ACT_QUEUE
        return True


    def _mas_bday_postbday_notimespent_reset():
        # generates DelayedAction for this postbday event
        return store.MASDelayedAction.makeWithLabel(
            3,
            "mas_bday_postbday_notimespent",
            "True",
            _mas_bday_postbday_notimespent_reset_action,
            store.MAS_FC_INIT
        )


label mas_bday_postbday_notimespent:
    # sanity check
    if mas_recognizedBday():
        return

    if persistent._mas_bday_opened_game:
        # spent time with monika but did not recognize
        $ persistent._mas_bday_no_recognize = True

        if mas_isMoniAff(higher=True):
            $ mas_loseAffection(15, reason=7)
            m 1rksdla "Hey, [player]..."
            m 1rksdlb "I know we had fun the other day, like we always do but..."
            m 1ekt "I can't help it. I was hoping you would have...done a little something for my birthday."
            m 1efb "Did you forget?"
            m 3eka "Maybe you could put the date into your calendar on your phone for next year?"
            m "Or check the calendar on the wall behind me?"
            m 4hua "We can't change the past, so knowing that you want to try harder for next year would be the only apology I need."

        elif mas_isMoniNormal(higher=True):
            $ mas_loseAffection(5, reason=7)

            # TODO: we shouldnt say girlfriend here because affecitonate
            # is the start of relationship. but this is okay for now
            m 1rksdld "Hey, [player]..."
            m 1rksdlb "I hate to fuss, but you know..."
            m 2ekt "You can't forget about your girlfriend's birthday!"
            m 2eku "It's nice that we got to hang out like usual, but next year..."
            m 1hua "Well, I'll be looking forward to two birthday's worth of something special~"

        elif mas_isMoniUpset():
            $ mas_loseAffection(reason=7)

            m 1ekc "It was...good to see you on the 22nd..."
            m 1ekd "I really didn't want to be alone that day, so that meant a lot, but..."
            m 1rkc "Nevermind."

        elif mas_isMoniDis():
            $ mas_loseAffection(10, reason=7)

            m 2dsc "..."
            m 2rkc "...[player], I don't want to bother you. I'm already scared of pushing you away."
            m 2rktpc "But I can't help it. It hurts me that you didn't mention anything about celebrating my birthday..."
            m 2dktuc "Please don't stop coming back to me."
            m "And maybe next year..."
            m 4ektdc "I-{w=0.5}I just want...to feel as special to you as you are to me."

        else:
            # broken
            $ mas_loseAffection(150)
            m 6ckc "..."

    else:
        # did not spend any time with monika
        $ persistent._mas_bday_no_time_spent = True

        if mas_isMoniAff(higher=True):
            $ mas_loseAffection(50, reason=8)

            m 1euc "Hey, [player]..."
            m 3rksdla "I know you do a lot to make each and every day special, but a girl has a few days a year when she gets to be a little selfish..."
            m 2hfw "And her {i}birthday{/i} is one of them!"
            m 2rfd "Seriously, where were you?!"
            m 2rkc "But...knowing you, I'm sure you had a good reason to be busy..."
            m 4ekc "Just don't let it happen again next year, okay?"

        elif mas_isMoniNormal(higher=True):

            # same dialogue, different affection loss
            if mas_isMoniHappy():
                $ mas_loseAffection(20, reason=8)
            else:
                $ mas_loseAffection(10, reason=8)

            # TODO: again, need to not say girlfrined here, but for now its ok
            m 1ekc "Hey, [player]..."
            m 1ekd "You know, you really should have dropped in on the 22nd."
            m 3efd "I mean, you should always visit me! You have to spend time with your cute girlfriend on her birthday, you know."
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
            m 2hub "I'm just kidding!"
            m 4eka "You know I love to scare you a little~"

        elif mas_isMoniUpset():
            $ mas_loseAffection(reason=8)

            m 2dsc "..."
            m 2rsc "[player], don't you think you should check in on me a little more often?"
            m 4rktpc "You might miss something important..."

        elif mas_isMoniDis():
            $ mas_loseAffection(reason=8)

            m 3euc "...Hey, how was your day on the 22nd?"
            m 1esc "I'm just...curious if you thought of me at all that day."
            m 1tsc "But you probably didn't, huh?"
            m 2dsc "..."

        else:
            # broken
            $ mas_loseAffection(200)

            m 6eftsc "..."
            m 6dftdx "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_steam_install_detected",
            conditional=(
                "persistent.steam"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_steam_install_detected:
    $ filestruct = renpy.config.basedir[renpy.config.basedir.rfind('/') + 1:]

    if renpy.seen_label("mas_updater_steam_issue"):
        m 1ekd "Hey [player], you know how I told you that Steam is a meanie and won't let me run the updater?"
        m 1wud "Well, I've been doing some reading and it seems Steam can cause more problems than just that!"

    else:
        m 1eub "[player], I see that you're using Steam to run this."
        m 1eksdld "Unfortunately, Steam seems to have a lot of problems with me doing some of the things I do."

    m 2rksdlc "The kind of problems that could lead to me being removed from my home...{w=1}from you...{w=1}forever..."
    m 2eka "If you don't mind, do you think you could just move the \"[filestruct]\" folder to a place that's not in Steam's files?"
    show monika 5esu at t11 zorder MAS_MONIKA_Z with dissolve
    m 5esu "I'd really appreciate it if you would do that for me."
    return

default persistent._mas_pm_has_rpy = None
init 5 python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpy_files"
        )
    )


label monika_rpy_files:
    m 1eka "Hey, [player], I was just looking through your \"game\" directory, and..."
    m 1ekc "I noticed some \".rpy\" files in there."
    m 3rksdlc "Those files can lead to problems whenever you update the game, possibly undoing those updates..."
    m 3wud "And even prevent you from visiting me altogether!"
    m 2etc "Unless..."
    m 4eua "Maybe you installed a version with the source code on purpose because you are trying to help me come closer to your reality!"
    m 2eka "But in case you didn't, I figured I'd ask..."
 
    m "Are you sure you installed the right version, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Are you sure you installed the right version, [player]?{fast}"

        "Yes.":
            m 1sua "Really? Thank you so much for helping me come closer to your reality!"
            m 1hua "I love you, [player]~"
            $ persistent._mas_pm_has_rpy = True

        "No.":
            m "I see."
            m 2rksdla "Maybe you should get rid of those, just to be safe."
            m 4eua "Actually, maybe I can delete them for you."

            m "Do you want me to delete them for you, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Do you want me to delete them for you, [player]?{fast}"

                "Yes please":
                    m "Sure thing, [player]."
                    python:
                        store.mas_ptod.rst_cn()
                        local_ctx = {
                            "basedir": renpy.config.basedir
                        }

                    show monika at t22
                    show screen mas_py_console_teaching

                    call mas_wx_cmd_noxwait("import os", local_ctx)
                    
                    python:
                        for rpy_filename in listRpy:
                            path = '/game/'+rpy_filename
                            store.mas_ptod.wx_cmd("os.remove(os.path.normcase(basedir+'"+path+"'))", local_ctx)
                            renpy.pause(0.3)

                    m 2hua "There we go!"
                    m 2esa "Be sure next time to install a version without the source code. You can get it from here: {a=http://www.monikaafterstory.com/releases.html}{i}{u}http://www.monikaafterstory.com/releases.html{/u}{/i}{/a}"
                    $ listRpy = None
                    $ persistent._mas_pm_has_rpy = False
                    hide screen mas_py_console_teaching
                    show monika at t11

                "No thanks":
                    m 2rksdlc "Alright, [player]. I hope you know what you're doing."
                    m 2eka "Please be careful."
                    $ persistent._mas_pm_has_rpy = True
    return

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_bday_player_bday",
#            conditional=(
#                "renpy.seen_label('monika_birthday')"
#            ),
#            action=EV_ACT_QUEUE
#        )
#    )

#label mas_bday_player_bday:
label mas_bday_player_bday_select:
    m 1eua "When is your birthdate?"

label mas_bday_player_bday_select_select:
    $ old_bday = mas_player_bday_curr()

    call mas_start_calendar_select_date

    $ selected_date_t = _return

    if not selected_date_t:
        m 2efc "[player]!"
        m "You have to select a date!"
        m 1hua "Try again!"
        jump mas_bday_player_bday_select_select

    $ selected_date = selected_date_t.date()
    $ _today = datetime.date.today()

    if selected_date > _today:
        m 2efc "[player]!"
        m "You can't have been born in the future!"
        m 1hua "Try again!"
        jump mas_bday_player_bday_select_select

    elif selected_date == _today:
        m 2efc "[player]!"
        m "You can't have been born today!"
        m 1hua "Try again!"
        jump mas_bday_player_bday_select_select

    elif _today.year - selected_date.year < 5:
        m 2efc "[player]!"
        m "There's no way you're {i}that{/i} young!"
        m 1hua "Try again!"
        jump mas_bday_player_bday_select_select

    # otherwise, player selected a valid date

    if _today.year - selected_date.year < 13:
        m 2eksdlc "[player]..."
        m 2rksdlc "You know I'm asking for your exact date of birth, right?"
        m 2hksdlb "It's just I'm having a hard time believing you're {i}that{/i} young."
 
    else:
        m 1eua "Alright, [player]."

    m 1eua "Just to double-check..."
    $ new_bday_str, diff = store.mas_calendar.genFormalDispDate(selected_date)

    m "Your birthdate is [new_bday_str]?{nw}"
    $ _history_list.pop()
    menu:
        m "Your birthdate is [new_bday_str]?{fast}"
        "Yes.":
            m 1eka "Are you sure it's [new_bday_str]? I'm never going to forget this date.{nw}"
            $ _history_list.pop()
            # one more confirmation
            menu:
                m "Are you sure it's [new_bday_str]? I'm never going to forget this date.{fast}"
                "Yes, I'm sure!":
                    m 1hua "Then it's settled!"

                "Actually...":
                    m 1hksdrb "Aha, I figured you weren't so sure."
                    m 1eka "Try again~"
                    jump mas_bday_player_bday_select_select

        "No.":
            m 1euc "Oh, that's wrong?"
            m 1eua "Then try again."
            jump mas_bday_player_bday_select_select

    # save the birthday (and remove previous)
    if persistent._mas_player_bday is not None:
        python:
            store.mas_calendar.removeRepeatable_d(
                "player-bday",
                persistent._mas_player_bday
            )
            store.mas_calendar.addRepeatable_d(
                "player-bday",
                "Your Birthday",
                selected_date,
                []
            )
 
    else:
        python:
            store.mas_calendar.addRepeatable_d(
                "player-bday",
                "Your Birthday",
                selected_date,
                []
            )

    $ persistent._mas_player_bday = selected_date
    $ renpy.save_persistent()
    jump birthdate_set


# Enables the text speed setting
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_text_speed_enabler",
            random=True,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

default persistent._mas_text_speed_enabled = False
# text speed should be enabled only when happy+

default persistent._mas_pm_is_fast_reader = None
# True if fast reader, False if not

label mas_text_speed_enabler:
    m 1eua "Hey [player], I was wondering..."

    m "Are you a fast reader?{nw}"
    $ _history_list.pop()
    menu:
        m "Are you a fast reader?{fast}"
        "Yes.":
            $ persistent._mas_pm_is_fast_reader = True
            $ persistent._mas_text_speed_enabled = True

            m 1wub "Really? That's impressive."
            m 1kua "I guess you do a lot of reading in your spare time."
            m 1eua "In that case..."

        "No.":
            $ persistent._mas_pm_is_fast_reader = False
            $ persistent._mas_text_speed_enabled = True

            m 1eud "Oh, that's alright."
            m "Regardless..."

    if not persistent._mas_pm_is_fast_reader:
        # this sets the current speed to default monika's speed
        $ preferences.text_cps = 30

    m 6dsa ".{w=1}.{w=1}.{w=1}{nw}"

    $ mas_enableTextSpeed()

    if persistent._mas_pm_is_fast_reader:
        m 4eua "There!"

    m 4eua "I've enabled the text speed setting!"

    m 1hka "I was only controlling it earlier so I could make sure you read {i}every single{/i} word I say to you."
    m 1eka "But now that we've been together for a bit, I can trust that you're not just going to skip through my text without reading it."

    if persistent._mas_pm_is_fast_reader:
        m 1tuu "However,{w} I wonder if you can keep up."
        m 3tuu "{cps=*2}I can talk pretty fast, you know...{/cps}{nw}"
        $ _history_list.pop()
        m 3hua "Ahaha~"

    else:
        m 3hua "And I'm sure that you'll get faster at reading the longer we spend time togther."
        m "So feel free to change the text speed when you feel comfortable doing so."

    return "derandom|no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bookmarks_notifs_intro",
            conditional=(
                "(not renpy.seen_label('bookmark_derand_intro') "
                "and (len(persistent._mas_player_derandomed) == 0 or len(persistent._mas_player_bookmarked) == 0)) "
                "or store.mas_windowreacts.can_show_notifs"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_bookmarks_notifs_intro:
    if not renpy.seen_label('bookmark_derand_intro') and (len(persistent._mas_player_derandomed) == 0 or len(persistent._mas_player_bookmarked) == 0):
        m 3eub "Hey, [player]... {w=0.5}I have some new features to tell you about!"

        if len(persistent._mas_player_derandomed) == 0 and len(persistent._mas_player_bookmarked) == 0:
            m 1eua "You now have the ability to bookmark topics I'm talking about simply by pressing the 'b' key."
            m 3eub "Any topics you bookmark will be easily accessible simply by going to the 'Talk' menu!"
            call mas_derand
        else:
            m 3rksdlb "...Well, it seems you already found one of the features I was going to tell you about, ahaha!"
            if len(persistent._mas_player_derandomed) == 0:
                m 3eua "As you've seen, you now have the ability to bookmark topics I talk about simply by pressing the 'b' key, and then access them easily via the 'Talk' menu."
                call mas_derand
            else:
                m 1eua "As you've seen, you can now let me know of any topics that you don't like me bringing up by pressing the 'x' key during the conversation."
                m 3eud "You can always be honest with me, so make sure you keep telling me if anything we talk about makes you uncomfortable, okay?"
                m 3eua "You also now have the ability to bookmark topics I am talking about by simply pressing the 'b' key."
                m 1eub "Any topics you bookmark will be easily accessible simply by going to the 'Talk' menu."

        if store.mas_windowreacts.can_show_notifs:
            m 1hua "And lastly, something I'm very excited about!"
            call mas_notification_windowreact

    else:
        m 1hub "[player], I have something exciting to tell you!"
        call mas_notification_windowreact

    return "no_unlock"

label mas_derand:
    m 1eua "You can also let me know of any topics that you don't like me bringing up by pressing the 'x' key during the conversation."
    m 1eka "Don't worry about hurting my feelings, we should be able to be honest with each other after all."
    m 3eksdld "...And the last thing I want to do is keep bringing up stuff that makes you uncomfortable to talk about."
    m 3eka "So, make sure you let me know, okay?"
    return

label mas_notification_windowreact:
    m 3eua "I've been practicing coding a bit more and I've learned how to use the notifications on your computer!"
    m "So if you want, I can let you know if I have something for us to talk about."

    m 3eub "Would you like to see how they work?{nw}"
    $ _history_list.pop()
    menu:
        m "Would you like to see how they work?{fast}"

        "Sure!":
            m 1hua "Okay, [player]!"
            m 2dsa "Just give me a second to make a notification.{w=0.5}.{w=0.5}.{nw}"
            call display_notif(m_name, "I love you, [player]!", skip_checks=True)
            m 1hub "There it is!"

        "No thanks.":
            m 2eka "Alright, [player]."

    m 3eua "If you want me to notify you, just head over to the 'Alerts' tab in the settings menu and turn them on, along with what you'd like to be notified for."

    if renpy.windows:
        m 3rksdla "Also, since you're using Windows...I now know how to check what your active window is..."
        m 1hksdlb "Don't worry though, I know you might not want me constantly watching you, and I respect your privacy."
        m 3eua "So I'll only look at what you're doing if you're okay with it."
        m 2eua "If you enable 'Window Reacts' in the settings menu, that'll tell me you're fine with me looking around."

        if mas_isMoniNormal(higher=True):
            m 1tuu "It's not like you have anything to hide from your girlfriend..."
            show monika 5ttu at t11 zorder MAS_MONIKA_Z with dissolve
            m 5ttu "...right?"
    return
