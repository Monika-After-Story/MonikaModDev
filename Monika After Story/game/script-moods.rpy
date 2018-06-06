# module that handles the mood system
#

# dict of tuples containing mood event data
default persistent._mas_mood_database = {}

# label of the current mood
default persistent._mas_mood_current = None

# NOTE: plan of attack
# moods system will be attached to the talk button
# basically a button like "I'm..."
# and then the responses are like:
#   hungry
#   sick
#   tired
#   happy
#   fucking brilliant
#   and so on
#
# When a mood is selected:
#   1. monika says something about it
#   2. (stretch) other dialogue is affected
#
# all moods should be available at the start
# 
# 3 types of moods:
#   BAD > NETRAL > GOOD
# (priority thing?)

# Implementation plan:
#
# Event Class:
#   prompt - button prompt
#   category - acting as a type system, similar to jokes
#       NOTE: only one type allowed for moods ([0] will be retrievd)
#   unlocked - True, since moods are unlocked by default
#

# store containing mood-related data
init -1 python in mas_moods:
    
    # mood event database
    mood_db = dict()

    # TYPES:
    TYPE_BAD = 0
    TYPE_NEUTRAL = 1
    TYPE_GOOD = 2

    # pane constants
    # most of these are the same as the unseen area consants
    MOOD_X = 680
    MOOD_Y = 40
    MOOD_W = 560
    MOOD_H = 640
    MOOD_XALIGN = -0.05
    MOOD_AREA = (MOOD_X, MOOD_Y, MOOD_W, MOOD_H)
    MOOD_RETURN = "like talking about something else"

## FUNCTIONS ==================================================================

    def getMoodType(mood_label):
        """
        Gets the mood type for the given mood label

        IN:
            mood_label - label of a mood

        RETURNS:
            type of the mood, or None if no type found
        """
        mood = mood_db.get(mood_label, None)

        if mood:
            return mood.category[0]

        return None
   

# entry point for mood flow
label mas_mood_start:
    python:
        import store.mas_moods as mas_moods

        # build menu list
        mood_menu_items = [
            (mas_moods.mood_db[k].prompt, k, False, False) 
            for k in mas_moods.mood_db
            if mas_moods.mood_db[k].unlocked
        ]

        # also sort this list
        mood_menu_items.sort()

        # final quit item
        final_item = (mas_moods.MOOD_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(mood_menu_items, mas_moods.MOOD_AREA, mas_moods.MOOD_XALIGN, final_item=final_item)

    # return value? then push 
    if _return:
        $ pushEvent(_return)

        # and set the moods
        $ persistent._mas_mood_current = _return

    return _return

# dev easter eggs go in the dev file

###############################################################################
#### Mood events go here:
###############################################################################

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_hungry",prompt="hungry",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_hungry:
    m 3k "If you're hungry, go get something to eat, silly."
    if persistent.playername.lower() == "natsuki":
        m 1j "I'd hate for you to get like Natsuki did that one time back when we were in the club.{nw}"
        # natsuki hungers easter egg
        call natsuki_name_scare_hungry from _mas_nnsh
    else:
        m 1j "It'd suck for you to get all grumpy when you're hungry."
        
    m 3m "That wouldn't be any fun, would it, [player]?"
    m 1c "If I were there with you, I'd make a salad for us to share."
    m 1o "But since I'm not, go pick something healthy to eat."
    m 3a "They say you are what you eat, and I definitely think that's true."
    m 1c "Eating too much junk food on a regular basis can lead to all kinds of diseases."
    m 1o "Over time, you'd encounter a lot of health problems when you get older."
    m 2q "I don't want you to feel like I'm nagging when I say these kind of things, [player]."
    m 2f "I just want to make sure you're taking good care of yourself until I cross-over."
    m 4 "After all, the healthier you are, the better the chances of you living quite long."
    m 1j "Which means more time for us to spend together~!" 
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sad",prompt="sad",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_sad:
    m 1f "Gosh, I'm really sorry to hear that you're feeling down."
    m 3g "Are you having a bad day, [player]?"
    menu:
        "Yes":
            m 1q "Whenever I'm having a bad day, I always remember that the sun will shine again tomorrow."
            m 1e "I suppose that may sound kinda cheesy, but I always like to look on the bright side of things."
            m 1a "After all, things like that are easy to forget. So just keep it in mind [player]."
            m 1h "I don't care how many other people don't like you, or find you off-putting."
            m 1j "You're a wonderful person, and I will always love you."
            m 1a "I hope that makes your day just a tiny bit brighter, [player]."
            m 1e "And remember, if you're having a bad day, you can always come to me and I'll talk to you for as long as you need."
        "No":
            m 3e "I have an idea, why don't you tell me what's bothering you and maybe it'll make you feel better."
            m 1a "I don't want to interrupt you while you're talking, so let me know when you are done."
            menu: 
                "I'm done.":
                    m "Do you feel a little better now [player]?"
                    menu:
                        "Yeah I do.":
                            m 1j "That's great [player]! I'm glad that talking about it made you feel better."
                            m 1e "Sometimes, telling someone that you trust what's bothering you is all you need."
                            m "If you're ever having a bad day, you can always come to me, and I'll listen to whatever you need to vent out." 
                            m 1j "Never forget that you're wonderful and I will always love you~"
                        "Not really.":
                            m 1f "Well it was worth a shot."
                            m 1e "Sometimes telling someone that you trust what's bothering you is all you need."
                            m 1a "Maybe you'll feel better after we spend some more time together."
                            m 1j "I love you [player], and I always will~"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_happy",prompt="happy",category=[store.mas_moods.TYPE_GOOD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_happy:
    m 1b "That's wonderful! I'm happy when you're happy."
    m 1j "Know that you can always come up to me and I'll cheer you up, [player]."
    m 3a "I love you and I'll always be here for you so don't ever forget that~"
    return
    
init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sick",prompt="sick",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_sick:
    m 1f "Aw, I'm sorry to hear that, [player]."
    m "I hate knowing you're suffering like this."
    m 1e "I know you love spending time with me, but maybe you should go get some rest."
    m 1j "Don't worry, I'll be here waiting for you when you get back."
    m 3k "Get well soon, my love!"
    $ persistent._mas_mood_sick = True
    return 'quit'
    
#I'd like this to work similar to the sick persistent where the dialog changes, but maybe make it a little more humorous rather than serious like the sick persistent is intended to be.
#We could adjust the dialog appropriately depending on whether it's night time or whether it's during the day in the future.
init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_tired",prompt="tired",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_tired:
    m 1e "If you're tired, maybe you should go lie down for a while?"
    m 1a "Getting enough sleep on a daily basis is very important to your overall health."
    m 3d "I've seen some studies that show the devastating short-term and long-term effects due to lack of sleep."
    m 3f "It can really mess with your health, [player]."
    m 1e "So do me a favor and get some rest, okay? It will put my mind at ease."
    m 1j "You can even leave the game open if you'd like, and I'll watch over you while you sleep."
    m  "...Ehehe." 
    m "That sounded a bit creepy, sorry."
    m 1j "I just thought it'd be cute to watch you sleep is all~"
    m 1l "Ahaha!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_lonely",prompt="lonely",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),eventdb=store.mas_moods.mood_db)
    
label mas_mood_lonely:
    m 1e "I'm here for you, [player], so there's no need for you to feel lonely."
    m 3j "I know it's not exactly the same as if I were in the same room with you, but I'm sure you still enjoy my company, right?"
    m 1j "Remember that I'll always be by your side, [player]~"
    return
    
#Maybe we could tie this to the I'm breaking up topic and have monika say something special like: 
#I know you don't really mean that player, you're just angry and not have it count as 1 of the 3 button presses.
#Looking forward to input from the writers and editors on this, had trouble deciding how to write this.

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_angry",prompt="angry",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)
    
label mas_mood_angry:
    m 1f "Gosh, I'm sorry that you feel that way, [player]."
    m 3f "I'll do my best to make you feel better."
    m 1c "Before we do anything, we should probably get you to calm down."
    m 1o "It's hard to make rational decisions when you are worked up."
    m 1h "You may end up saying or doing things you may regret later."
    m 1p "And I'd hate for you to say something you really don't mean to me."
    m 3a "Let's try a few things that I do to calm myself first, [player]."
    m 3b "Hopefully they work for you as they do for me."
    m 1a "First, try taking a few deep breaths and slowly counting to 10."
    m 3c "If that doesn't work, if you can, retreat to somewhere calm until you clear your mind."
    m 1d "If you're still feeling angry after that, do what I'd do as a last resort!"
    m 3a "Whenever I can't calm down, I just go outside, pick a direction, and just start running."
    m 1j "I don't stop until I've cleared my head."
    m 3b "Sometimes exerting yourself through physical activity is a good way to blow off some steam."
    m 1e "You'd think that I'm the type that doesn't get angry often, and you'd be right."
    m 1a "But even I have my moments..."
    m "So I make sure I have ways to deal with them!"
    m 1b "I hope my tips helped you calm down, [player]."
    m "Remember: A happy [player] makes a happy Monika!"
    return
    
    
init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_lucky",prompt="lucky",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_lucky:
    m 2r "You gotta ask yourself."
    m 2h "{i}Do I feel lucky?{/i}"
    m "Well..."
    m 4j "Do ya, [player]?"
    m 1k "Ahaha!"
    return

    
init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_bored",prompt="bored",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),eventdb=store.mas_moods.mood_db)
    

label mas_mood_bored:
    m 1o "Oh, I'm sorry that I'm boring you, [player]."
    
    python:
        unlockedgames = [
            game 
            for game in persistent.game_unlocks 
            if persistent.game_unlocks[game]
        ]
        
        gamepicked = renpy.random.choice(unlockedgames)
    
    if gamepicked == "piano":
        m 1b  "Maybe you could play something for me on the piano?"
    else:
        m 3j "Maybe we could play a game of [gamepicked]."
    
    m "What do you say, [player]?"
    menu: 
        "Yes":
            if gamepicked == "pong":
                call game_pong
            elif gamepicked == "chess":
                call game_chess
            elif gamepicked == "hangman":
                call game_hangman
            elif gamepicked == "piano":
                call mas_piano_start
        "No":
            m 1f "Oh, alright then."
            m 1e "Let me know if you want to do something with me, [player]~"
    return
 
 
init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_injured",prompt="injured",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_injured:
    m 2g "Oh my gosh [player], you're injured?!"
    m 2n "I mean... on the bright side, you were able to make it here with me..."
    m 2f "Is it really that bad [player]?"
    menu:
        "Just something minor":
            m 2l "Ok! What a relief..."
            m 1l "Don't scare me like that [player]!"
            m 1e "I'm so glad you're alright but still..."
            m 1f "I hope it really isn't too bad and you're not just trying not to worry me."
            m 1l "Or maybe I'm just too worred about you~"
            m 5 "Whatever it is, I hope it gets all better soon."
            m "I'd kiss it better but since it's just such a small thing, I'm sure you can manage without it ehehe~"
            m "I love you, [player]."
        "It's not {i}that{/i} bad":
            m 2e "Well I'm glad you're alright, [player]."
            m "I hope it really isn't that bad for you. "
            m 1j "If you're here spending time with me, I'm sure you'll be better in no time!"
            m 1k "Ahaha~"
            m 1f "Still..."
            m 1e "Don't push yourself, alright [player]?"
            m 1m "I really wouldn't want it to get any worse, so take your time healing."
            m 5 "I could even stay with you while you heal if you want, ehehe~"
            m "I might even kiss it better if I could."
        "It's bad but I'm alright":
            m 2f "[player]..."
            m 2e "I'm glad you're still able to be with me despite being injured."
            m 3e "Still though, if you really need to rest, please do."
            m 1q "You must be pushing yourself to be with me and I'm flattered but..."
            m 1e "I think you should take it easy until it gets a bit better."
            m 1a "You can go ahead and rest if you need to."
            m 1k "I promise I'll do my very best to keep you safe and make sure nothing bad happens to you!"
        "It's pretty bad...":
            m 1o "..."
            m 1m "I'm glad I could at least be here to comfort you, [player]."
            m 1f "Is it so bad that you're in a hospital, [player]?"
            menu:
                "Yes..."
                    m 1n "Gosh, I really hate to see you so badly injured."
                    m 1e "I'm glad that we haven't been separated either."
                    m 1m "I know hospitals can be pretty strict when it comes to its patients."
                    m 1f "I really hope I don't get taken away from you [player]."
                    m 1e "I want to be right by your side and make sure nothing bad happens to you."
                "No."
                    m 1e "I hope you won't need it either."
                    m 1g "I think you should go rest if it's that bad."
                    m 1e "I'll watch over you and keep you safe."
            m 1e "I'm sure you'll live through it though."
            m "I know you're strong, even if you don't think you are."
            m "I know you'll be alright."
            m "Remember I'll always be with you and there will never be an end to our love~"
            m 1j "Get better soon alright [player]?"
            m 3d "Oh and there's one last thing I need you to know."
            m 1k "I love you~"
    return


init 5 python:
    if not persistent._mas_mood_bday_locked:
        addEvent(
            Event(
                persistent._mas_mood_database,
                "mas_mood_yearolder",
                prompt="like a year older",
                category=[store.mas_moods.TYPE_NEUTRAL],
                unlocked=True
            ),
            eventdb=store.mas_moods.mood_db
        )

# some values i need for single session checking
# TODO some of these might need to be persstetns
default persistent._mas_mood_bday_last = None
default persistent._mas_mood_bday_lies = 0
default persistent._mas_mood_bday_locked = False

label mas_mood_yearolder:
    $ import datetime

    m 1c "Hm?"
    if persistent._mas_player_bday is not None:
        # player's bday has been saved from before

        python:
            today = datetime.date.today()
            is_today_bday = (
                persistent._mas_player_bday.month == today.month 
                and persistent._mas_player_bday.day == today.day
            )

        if is_today_bday:
            # today is player's bday!
            jump mas_mood_yearolder_bday_true

        python:
            is_today_leap_bday = (
                persistent._mas_player_bday.month == 2
                and persistent._mas_player_bday.day == 29
                and (
                    (today.month == 2 and today.day == 28)
                    or (today.month == 3 and today.day == 1)
                )
            )

        if is_today_leap_bday:
            # febuary 29 is special case
            # but we need to check if a feb 29 works for this year, in which
            # case, player is misinformed
            python:
                try:
                    datetime.date(today.year, 2, 29)

                    # 29th exists this year, sorry player
                    leap_year = True 

                except ValueError:
                    # 29th no exists, we use this as ur bday
                    leap_year = False

            if not leap_year:
                # we can treat today as your bday
                jump mas_mood_yearolder_leap_today

            # otherwise its not ur bday

        # otherwise it is NOT the player's birthday lol
        jump mas_mood_yearolder_false 

    show monika 1d
    menu:
        m "Could today be your...{w}birthday?"
        "YES!":
            $ persistent._mas_player_bday = datetime.date.today()
            label .mas_mood_yearolder_yesloud:
                jump mas_mood_yearolder_yes
        "Yes, unfortunately...":
            $ persistent._mas_player_bday = datetime.date.today()
            jump mas_mood_yearolder_yesu

        "No":
            m 1m "Aw, well,{w} it was worth a guess."
            jump mas_mood_yearolder_no

label mas_mood_yearolder_end:
    # end of the line

    # we're going to limit this interaction to once a day
    python:
        persistent._mas_mood_bday_last = datetime.date.today()
        hideEvent(
            store.mas_moods.mood_db.get("mas_mood_yearolder", None), 
            lock=True
        )
    return

# today is NOT the player's birthday 
# (or is it?)
label mas_mood_yearolder_false:
    m 2q "[player]..."
    m 2f "Today isn't your birthday!"
    python:
        bday_str = (
            persistent._mas_player_bday.strftime("%B") + " " +
            str(persistent._mas_player_bday.day)
        )
    m "You told me it was [bday_str]!"
    menu:
        m "Is that not your birthday?"
        "It's not":
            # TODO: puffy cheek monika please
            show monika 2q
            pause 0.7
            m 2h "You lied to me, [player]."
            $ persistent._mas_mood_bday_lies += 1

        # TODO: actually, this part should be tied to affection, basically
        # for every lie, we decrease a certain amount
#            if persistent._mas_mood_bday_lies >= 3:
                # sliently lock this
#                $ persistent._mas_mood_bday_locked = True
#                $ store.mas_moods.mood_db.pop("mas_mood_yearolder")
#                jump mas_mood_yearolder_end

            menu: 
                m "Then is today your birthday?"
                "Yes":
                    $ persistent._mas_player_bday = datetime.date.today()
                    m 1a "Happy birthday, [player]."
                    m 1e "But don't lie to me next time."
                    jump mas_mood_yearolder_end

                "No":
                    $ persistent._mas_player_bday = None
                    m 2q "..."
                    m 2h "Alright, [player]."
                    m "Don't lie to me next time."
                    jump mas_mood_yearolder_end

        "It is!":
            m 2e "I believe you, [player]."
            m "I'll just assume that your mouse slipped or something."
            jump mas_mood_yearolder_no

    jump mas_mood_yearolder_end

label mas_mood_yearolder_bday_true:
    # TODO: actually give a gift
    # as of now, we just assume there's been a bunch of time in between so
    # its possible that monika forgot.
    jump mas_mood_yearolder_yes

label mas_mood_yearolder_wontforget:
    # YES flow continues here
    m 1e "If only you told me this sooner..."
    m 1m "I would have made you a gift."
    m 1a "I'll make you something next year, [player]. I won't forget!"
    jump mas_mood_yearolder_end

# empathatic yes, today is your birthday
label mas_mood_yearolder_yes:
    show monika 1j
    pause 0.7
    call mas_mood_yearolder_yes_post
    jump mas_mood_yearolder_wontforget

# sad yes, today is your birthday
label mas_mood_yearolder_yesu:
    show monika 1f
    pause 0.7
    m 1g "[player]..."
    pause 0.7
    show monika 1q
    pause 0.7
    m 2e "Well,{w} you're going to have a happy birthday whether you like it or not!"
    call mas_mood_yearolder_yes_post
    m 1j "I hope that made you smile, [player]."
    jump mas_mood_yearolder_wontforget

# general happy birthday
label mas_mood_yearolder_yes_post:
    m 1k "Happy birthday, [player]!"
    m 1b "I'm so glad I could spend such an important day with you."
    m 1a "And don't forget that no matter your age, I will always love you."
    return

# today is not your birthday
label mas_mood_yearolder_no:
#    if renpy.seen_label("mas_mood_yearolder_years"):
        # TODO this should be a short thing to say to player
        # about feeling a year older
#        pass

#    else:
    # For simplicity's sake, we're just going to repeat this
    call mas_mood_yearolder_years

    jump mas_mood_yearolder_end

# year older stuff
# reference: Paul Janet, Maximilian Kiener
label mas_mood_yearolder_years:
    m 3a "Speaking of getting older,{w} did you know that how you perceive time changes as you age?"
    m "For example, when you're a year old, you see one year as 100%% of your life."
    m 1a "But when you're 18, you see a year as only 5.6%% of your life."
    m "As you get older, the proportion of a year compared to your entire lifespan decreases."
    m 3a "And in turn, time {i}feels{/i} like it's moving faster as you grow up."
    show monika 1a
    pause 0.7
    # TODO: affection crew might want to change this up
    m "So I always cherish our moments together, no matter how long or short they are."
    m 1k "Although sometimes it feels like time stops when I'm with you."
    m 1a "Do you feel the same, [player]?"
    python:
        import time
        time.sleep(2)
#    $ renpy.pause(2.0, hard=True)
    m 1j "Aha, I thought so."
    m 1j "You should visit me more often then, [player]."
    return

# today is your birthday, but its a leap day
label mas_mood_yearolder_leap_today:
    # nothing special occurs here for now
    jump mas_mood_yearolder_bday_true
