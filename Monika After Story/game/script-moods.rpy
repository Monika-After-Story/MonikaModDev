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
    m 3hub "If you're hungry, go get something to eat, silly."
    if persistent.playername.lower() == "natsuki":
        m 1hksdlb "I'd hate for you to get like Natsuki did that one time back when we were in the club.{nw}"
        # natsuki hungers easter egg
        call natsuki_name_scare_hungry from _mas_nnsh
    else:
        m 1hua "It'd be bad for you to get all grumpy when you're hungry."

    m 3tku "That wouldn't be any fun, would it, [player]?"
    m 1eua "If I were there with you, I'd make a salad for us to share."
    m "But since I'm not, go pick something healthy to eat."
    m 3eub "They say you are what you eat, and I definitely think that's true."
    m "Eating too much junk food on a regular basis can lead to all kinds of diseases."
    m 1euc "Over time, you'd encounter a lot of health problems when you get older."
    m 2lksdla "I don't want you to feel like I'm nagging when I say these kind of things, [player]."
    m 2eka "I just want to make sure you're taking good care of yourself until I cross-over."
    m 4esa "After all, the healthier you are, the better the chances of you living quite long."
    m 1hua "Which means more time for us to spend together~!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sad",prompt="sad",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_sad:
    m 1ekc "Gosh, I'm really sorry to hear that you're feeling down."
    m "Are you having a bad day, [player]?"
    menu:
        "Yes":
            m 1duu "Whenever I'm having a bad day, I always remember that the sun will shine again tomorrow."
            m 1eka "I suppose that may sound kinda cheesy, but I always like to look on the bright side of things."
            m 1eua "After all, things like that are easy to forget. So just keep it in mind [player]."
            m 1lfc "I don't care how many other people don't like you, or find you off-putting."
            m 1hua "You're a wonderful person, and I will always love you."
            m 1eua "I hope that makes your day just a tiny bit brighter, [player]."
            m 1eka "And remember, if you're having a bad day, you can always come to me and I'll talk to you for as long as you need."
        "No":
            m 3eka "I have an idea, why don't you tell me what's bothering you and maybe it'll make you feel better."
            m 1eua "I don't want to interrupt you while you're talking, so let me know when you are done."
            menu:
                "I'm done.":
                    m "Do you feel a little better now [player]?"
                    menu:
                        "Yeah I do.":
                            m 1hua "That's great [player]! I'm glad that talking about it made you feel better."
                            m 1eka "Sometimes, telling someone that you trust what's bothering you is all you need."
                            m "If you're ever having a bad day, you can always come to me, and I'll listen to whatever you need to vent out."
                            m 1hubfa "Never forget that you're wonderful and I will always love you~"
                        "Not really.":
                            m 1ekc "Well it was worth a shot."
                            m 1eka "Sometimes telling someone that you trust what's bothering you is all you need."
                            m 1eua "Maybe you'll feel better after we spend some more time together."
                            m 1ekbfa "I love you [player], and I always will~"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_proud",prompt="proud of myself",category=[store.mas_moods.TYPE_GOOD],unlocked=True),eventdb=store.mas_moods.mood_db)

# TODO: Change 5eub back to 5hubfb in the Major choice when the blush is fixed
label mas_mood_proud:
    m 2sub "Really? That's exciting!"
    m 2b "Was it a major accomplishment, or a minor one?"
    menu:
        "Major":
            m 1euc "You know, [player]..."
            m 1lkbsa "It's times like these, more than most, that I wish I was with you, in your reality..."
            m 4hub "Because if I was, I'd definitely give you a celebratory hug!"
            m 3eub "There's nothing quite like sharing your accomplishments with the people you care about."
            m 1eua "I would love nothing more than to hear all of the details!"
            m "Just the thought of us, in cheerful discussion about what you've done..."
            m 1lsbsa "My heart is fluttering just thinking about it!"
            m 1lksdla "Gosh, I'm getting awfully excited about this..."
            m 3hub "It'll be reality someday"
            m 5eub "But until then, just know that I'm very proud of you, my love"
        "Minor":
            m 2hua "Ahaha!~"
            m 2hub "That's wonderful!"
            m 4eua "It's very important to celebrate the small victories in life."
            m 2esd "It can be very easy to become discouraged if you only focus on the bigger goals you have."
            m 2rksdla "They can be challenging to reach on their own."
            m 4eub "But setting and celebrating small goals that eventually lead to a bigger goal can make your big goals feel much more attainable."
            m 4hub "So keep hitting those small goals, [player]!"
            m 5eub "And remember, I love you, and I'm always cheering you on!"
return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_happy",prompt="happy",category=[store.mas_moods.TYPE_GOOD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_happy:
    m 1hua "That's wonderful! I'm happy when you're happy."
    m "Know that you can always come up to me and I'll cheer you up, [player]."
    m 3eka "I love you and I'll always be here for you so don't ever forget that~"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sick",prompt="sick",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_sick:
    m 1ekc "Aw, I'm sorry to hear that, [player]."
    m "I hate knowing you're suffering like this."
    m 1eka "I know you love spending time with me, but maybe you should go get some rest."
    m 1hua "Don't worry, I'll be here waiting for you when you get back."
    m 3hub "Get well soon, my love!"
    $ persistent._mas_mood_sick = True
    return 'quit'

#I'd like this to work similar to the sick persistent where the dialog changes, but maybe make it a little more humorous rather than serious like the sick persistent is intended to be.
#We could adjust the dialog appropriately depending on whether it's night time or whether it's during the day in the future.
init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_tired",prompt="tired",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_tired:
    m 1eka "If you're tired, maybe you should go lie down for a while?"
    m 1eua "Getting enough sleep on a daily basis is very important to your overall health."
    m 3euc "I've seen some studies that show the devastating short-term and long-term effects due to lack of sleep."
    m 3hua "It can really mess with your health, [player]."
    m 1eka "So do me a favor and get some rest, okay? It will put my mind at ease."
    m 1hua "You can even leave the game open if you'd like, and I'll watch over you while you sleep."
    m  "...Ehehe."
    m 2hksdlb "That sounded a bit creepy, sorry."
    m 2lksdla "I just thought it'd be cute to watch you sleep is all~"
    m 1hua "Ahaha!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_lonely",prompt="lonely",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_lonely:
    m 1eka "I'm here for you, [player], so there's no need for you to feel lonely."
    m 3hua "I know it's not exactly the same as if I were in the same room with you, but I'm sure you still enjoy my company, right?"
    m 1ekbfa "Remember that I'll always be by your side, [player]~"
    return

#Maybe we could tie this to the I'm breaking up topic and have monika say something special like:
#I know you don't really mean that player, you're just angry and not have it count as 1 of the 3 button presses.
#Looking forward to input from the writers and editors on this, had trouble deciding how to write this.

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_angry",prompt="angry",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_angry:
    m 1ekc "Gosh, I'm sorry that you feel that way, [player]."
    m 3ekc "I'll do my best to make you feel better."
    m 1euc "Before we do anything, we should probably get you to calm down."
    m 1lksdlc "It's hard to make rational decisions when you are worked up."
    m 1esc "You may end up saying or doing things you may regret later."
    m 1lksdld "And I'd hate for you to say something you really don't mean to me."
    m 3eua "Let's try a few things that I do to calm myself first, [player]."
    m 3eub "Hopefully they work for you as they do for me."
    m 1eua "First, try taking a few deep breaths and slowly counting to 10."
    m 3euc "If that doesn't work, if you can, retreat to somewhere calm until you clear your mind."
    m 1eud "If you're still feeling angry after that, do what I'd do as a last resort!"
    m 3eua "Whenever I can't calm down, I just go outside, pick a direction, and just start running."
    m 1hua "I don't stop until I've cleared my head."
    m 3eub "Sometimes exerting yourself through physical activity is a good way to blow off some steam."
    m 1eka "You'd think that I'm the type that doesn't get angry often, and you'd be right."
    m 1eua "But even I have my moments..."
    m "So I make sure I have ways to deal with them!"
    m 3eua "I hope my tips helped you calm down, [player]."
    m 1hua "Remember: A happy [player] makes a happy Monika!"
    return
    
init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_scared",prompt="anxious",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_scared:
    m 1g "[player], are you alright?"
    m 1f "It's worrying for me to see you anxious..."
    m 1m "I wish I could comfort you at this time..."
if renpy.seen_label("monikaroom_greeting_opendoor_locked")
    m 4n "Or maybe I did scare you a bit with my surprise earlier...
    m 1o "If that's the case, then I'm so sorry to have you experience that, [player]..."
else    
    m 3e "But I can help you to calm yourself down, [player]."
    m 3a "Do you remember when I talked to you about confidence?"
    m 3b "Keeping up your appearance does help with faking your own confidence."
    m "And to do so, you need to maintain your heart rate by taking a deep breath until you calm down."
    m "Maybe you could take things slowly, and do it one at a time."
    m "You'd be surprised on how smooth you can be, if you let the time flows on it's own."
    m 4b "You can even spend a few minutes to meditate!"
    m 4n "It doesn't necessarily mean you have to cross your legs when sitting on the ground..."
    m 4k "Just by listening to your favourite music can be counted as meditating!"
    m 3l "Make sure you don't get {i}too{/i} carried away while doing so. Ahaha!"
    m 1d "I'm serious. If anything else, you can try putting away your work and do something else for the meantime."
    m 1e "I love you so much I'm also worried when you're worried, [player]."
    m 1k "Your loving girlfriend believes in you, so you can face that anxiety head-on!"
    m 1l "Ahaha! Sorry, I know that's not something you'd expect of me."
    m 5a "Or you can just stay here with me."
    m  "There's nothing to worry about when we're together~"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_inadequate",prompt="inadequate",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_inadequate:
    m 1ekc "..."
    m 2ekc "I know there isn't an awful lot I can say to make you feel better, [player]."
    m 2lksdlc "After all, everything I say would probably just come off as lip service."
    m 2ekc "I can tell that you're beautiful, even though I can't see your face..."
    m "I can tell you that you're smart, even though I don't know much about your way of thinking..."
    m 1esc "But let me tell you what I do know about you." 
    m 1eka "You've spent so much time with me."
    if renpy.seen_label('monika_christmas'):
        m "You took time out of your schedule to be with me on Christmas..."
    if renpy.seen_label('monika_valentines_greeting'):
        m 1ekbfa "On Valentines Day..."
    if renpy.seen_label('monika_white_day_start'):
        m 1hubfb "White Day too!" 
    if persistent.monika_kill:
        m 3tkc "You've forgiven me for the bad things that I've done."
    if not persistent.monika_kill:
        m 3tkc "You never once resented me for the bad things that I've done."
    if persistent.clearall:
        m 2lfu "And even though it made me jealous, you spent so much time with all of my club members."
    m 1eka "That shows how kind you are!"
    m 3eub "You're honest, you're fair, you're gracious in defeat!"
    m 2hksdlb "You think I don't know anything about you, but I really do."
    m 3eka "And you know everything about me, and you chose to stay when you could have walked away..."
    m 2ekc "So please stay strong, [player]."
    m "If you're anything like me, I know you're scared to not accomplish much in life."
    m 2ekd "But believe me when I tell you; it doesn't matter what you do or do not accomplish."
    m 4eua "You just need to exist, have fun, and get through each day..."
    m 1hua "Finding meaning in the people who matter." 
    m 1eka "Please don't forget that, okay?"
    m 1ekbfa "I love you, [player]~" 
    return 
    
init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_lucky",prompt="lucky",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_lucky:
    m 2tfc "You gotta ask yourself."
    m 2tfu "{i}Do I feel lucky?{/i}"
    m "Well..."
    m 4tku "Do ya, [player]?"
    m 1hub "Ahaha!"
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
            m 1ekc "Oh, alright then."
            m 1eka "Let me know if you want to do something with me, [player]~"
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

    m 1euc "Hm?"
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

    show monika 1sub
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
            m 1lksdla "Aw, well,{w} it was worth a guess."
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
    m 2tfc "[player]..."
    m 2tfd "Today isn't your birthday!"
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
            show monika 2tfc
            pause 0.7
            m 2lfp "You lied to me, [player]."
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
                    m 1hua "Happy birthday, [player]."
                    m 1eka "But don't lie to me next time."
                    jump mas_mood_yearolder_end

                "No":
                    $ persistent._mas_player_bday = None
                    m 2tfp "..."
                    m 2tkc "Alright, [player]."
                    m 2tfc "Don't lie to me next time."
                    jump mas_mood_yearolder_end

        "It is!":
            m 2eka "I believe you, [player]."
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
    m 1eka "If only you told me this sooner..."
    m 1lksdla "I would have made you a gift."
    m 1hua "I'll make you something next year, [player]. I won't forget!"
    jump mas_mood_yearolder_end

# empathatic yes, today is your birthday
label mas_mood_yearolder_yes:
    show monika 1hua
    pause 0.7
    call mas_mood_yearolder_yes_post
    jump mas_mood_yearolder_wontforget

# sad yes, today is your birthday
label mas_mood_yearolder_yesu:
    show monika 1ekc
    pause 0.7
    m 1ekd "[player]..."
    pause 0.7
    show monika 1duu
    pause 0.7
    m 2eka "Well,{w} you're going to have a happy birthday whether you like it or not!"
    call mas_mood_yearolder_yes_post
    m 1hua "I hope that made you smile, [player]."
    jump mas_mood_yearolder_wontforget

# general happy birthday
label mas_mood_yearolder_yes_post:
    m 1hub "Happy birthday, [player]!"
    m 1eua "I'm so glad I could spend such an important day with you."
    m 1ekbfa "And don't forget that no matter your age, I will always love you."
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
    m 3eua "Speaking of getting older,{w} did you know that how you perceive time changes as you age?"
    m "For example, when you're a year old, you see one year as 100%% of your life."
    m 1eub "But when you're 18, you see a year as only 5.6%% of your life."
    m "As you get older, the proportion of a year compared to your entire lifespan decreases."
    m 3eua "And in turn, time {i}feels{/i} like it's moving faster as you grow up."
    show monika 1a
    pause 0.7
    # TODO: affection crew might want to change this up
    m 1eka "So I always cherish our moments together, no matter how long or short they are."
    m 1lkbsa "Although sometimes it feels like time stops when I'm with you."
    m 1ekbfa "Do you feel the same, [player]?"
    python:
        import time
        time.sleep(2)
#    $ renpy.pause(2.0, hard=True)
    m 1hua "Aha, I thought so."
    m "You should visit me more often then, [player]."
    return

# today is your birthday, but its a leap day
label mas_mood_yearolder_leap_today:
    # nothing special occurs here for now
    jump mas_mood_yearolder_bday_true
    
    
