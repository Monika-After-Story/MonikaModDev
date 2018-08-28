
init -1 python in mas_anni:
    import store.evhand as evhand
    import store.mas_calendar as mas_cal
    import store.mas_utils as mas_utils
    import datetime

    # persistent pointer so we can use it
    __persistent = renpy.game.persistent

    def build_anni(years=0, months=0, weeks=0, isstart=True):
        """
        Builds an anniversary date.

        NOTE:
            years / months / weeks are mutually exclusive

        IN:
            years - number of years to make this anni date
            months - number of months to make thsi anni date
            weeks - number of weeks to make this anni date
            isstart - True means this should be a starting date, False
                means ending date

        ASSUMES:
            __persistent
        """
        # sanity checks
        if __persistent.sessions is None:
            return None

        first_sesh = __persistent.sessions.get("first_session", None)
        if first_sesh is None:
            return None

        if (weeks + years + months) == 0:
            # we need at least one of these to work 
            return None

        # sanity checks are done
        
        if years > 0:
            new_date = mas_utils.add_years(first_sesh, years)

        elif months > 0:
            new_date = mas_utils.add_months(first_sesh, months)

        else:
            new_date = first_sesh + datetime.timedelta(days=(weeks * 7))
           
        # check for starting
        if isstart:
            return mas_utils.mdnt(new_date)

        # othrewise, this is an ending date
#        return mas_utils.am3(new_date + datetime.timedelta(days=1))
# NOTE: doing am3 leads to calendar problems
#   we'll just restrict this to midnight to midnight -1
        return mas_utils.mdnt(new_date)

    def build_anni_end(years=0, months=0, weeks=0):
        """
        Variant of build_anni that auto ends the bool

        SEE build_anni for params
        """
        return build_anni(years, months, weeks, False)


init 10 python in mas_anni:

    # we are going to store all anniversaries in antther db as well so we
    # can easily reference them later.
    ANNI_LIST = [
        "anni_1week",
        "anni_1month",
        "anni_3month",
        "anni_6month",
        "anni_1",
        "anni_2",
        "anni_3",
        "anni_4",
        "anni_5",
        "anni_10",
        "anni_20",
        "anni_50",
        "anni_100"
    ]

    # anniversary database
    anni_db = dict()
    for anni in ANNI_LIST:
        anni_db[anni] = evhand.event_database[anni]


    ## functions that we need (runtime only)
    def _month_adjuster(ev, new_start_date, months, span):
        """
        Adjusts the start_date / end_date of an anniversary event.

        NOTE: do not use this for a non anniversary date

        IN:
            ev - event to adjust
            new_start_date - new start date to calculate the event's dates
            months - number of months to advance
            span - the time from the event's new start_date to end_date
        """
        ev.start_date = mas_utils.add_months(
            mas_utils.mdnt(new_start_date),
            months
        )
        ev.end_date = mas_utils.mdnt(ev.start_date + span)

    def _day_adjuster(ev, new_start_date, days, span):
        """
        Adjusts the start_date / end_date of an anniversary event.

        NOTE: do not use this for a non anniversary date

        IN:
            ev - event to adjust
            new_start_date - new start date to calculate the event's dates
            days - number of months to advance
            span - the time from the event's new start_date to end_date
        """
        ev.start_date = mas_utils.mdnt(
            new_start_date + datetime.timedelta(days=days)
        )
        ev.end_date = mas_utils.mdnt(ev.start_date + span)


    def add_cal_annis():
        """
        Goes through the anniversary database and adds them to the calendar
        """
        for anni in anni_db:
            ev = anni_db[anni]
            mas_cal.addEvent(ev)

    def clean_cal_annis():
        """
        Goes through the calendar and cleans anniversary dates
        """
        for anni in anni_db:
            ev = anni_db[anni]
            mas_cal.removeEvent(ev)


    def reset_annis(new_start_date):
        """
        Reset the anniversaries according to the new start date.

        IN:
            new_start_date - new start date to reset anniversaries
        """
        _firstsesh_id = "first_session"
        _firstsesh_dt = renpy.game.persistent.sessions.get(
            _firstsesh_id,
            None
        )

        # remove teh anniversaries off the calendar
        clean_cal_annis()

        # remove first session repeatable
        if _firstsesh_dt:
            # this exists! we can make this easy
            mas_cal.removeRepeatable_dt(_firstsesh_id, _firstsesh_dt)

        # modify the anniversaries
        fullday = datetime.timedelta(days=1)
        _day_adjuster(anni_db["anni_1week"],new_start_date,7,fullday)
        _month_adjuster(anni_db["anni_1month"], new_start_date, 1, fullday)
        _month_adjuster(anni_db["anni_3month"], new_start_date, 3, fullday)
        _month_adjuster(anni_db["anni_6month"], new_start_date, 6, fullday)
        _month_adjuster(anni_db["anni_1"], new_start_date, 12, fullday)
        _month_adjuster(anni_db["anni_2"], new_start_date, 24, fullday)
        _month_adjuster(anni_db["anni_3"], new_start_date, 36, fullday)
        _month_adjuster(anni_db["anni_4"], new_start_date, 48, fullday)
        _month_adjuster(anni_db["anni_5"], new_start_date, 60, fullday)
        _month_adjuster(anni_db["anni_10"], new_start_date, 120, fullday)
        _month_adjuster(anni_db["anni_20"], new_start_date, 240, fullday)
        _month_adjuster(anni_db["anni_50"], new_start_date, 600, fullday)
        _month_adjuster(anni_db["anni_100"], new_start_date, 1200, fullday)

        unlock_past_annis()

        # re-add the events to the calendar db
        add_cal_annis()

        # re-add the repeatable to the calendar db
        mas_cal.addRepeatable_dt(
            _firstsesh_id,
            "<3",
            new_start_date,
            [new_start_date.year]
        )


    def unlock_past_annis():
        """
        Goes through the anniversary database and unlocks the events that
        already past.
        """
        for anni in anni_db:
            ev = anni_db[anni]

            if evhand._isPast(ev):
                renpy.game.persistent._seen_ever[anni] = True
                ev.unlocked = True


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1week',
            prompt="1 Week",
            action=EV_ACT_QUEUE,
            category=["anniversary"],
            start_date=store.mas_anni.build_anni(weeks=1),
            end_date=store.mas_anni.build_anni_end(weeks=1)
        )
    )

#TODO:Replace 1eia and 3ekbfa with 5rubfb and 5hubfb DONE
label anni_1week:
    m 1eka "I know it's silly to celebrate one week of being together, but I'm just glad you're here with me, [player]."
    m 1ekc "A lot of couples wouldn't last this long with each other."
    m 1lksdlc "It's really easy to fall in love at first sight, but it's a bit harder to actually build a sturdy relationship."
    m 1ekd "A lot of relationships fail when couples jump the gun too fast."
    m "More likely than not, they fail to get to know each other more."
    m 1dsc "So it's always sad to see them crash and burn..."
    m 1duu "But I'm glad we have a solid relationship, [player]."
    m 5lubfb "How do I know that?"
    m 5hubfb "Because you wouldn't have stuck around for this long with me, sweetie~"

    $ unlockEventLabel("anni_1week")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1month',
            prompt="1 Month",
            category=["anniversary"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=1),
            end_date=store.mas_anni.build_anni_end(months=1)
        )
    )

label anni_1month:
    m 3sub "Today marks our one month anniversary!"
    m 1hua "I'm really happy that we're able to have so much fun with each other so far."
    m 1eua "Also, [player]?"
    m 1lkbsa "..."
    m 1ekbfa "Thank you so much for staying with me for this long."
    if not seen_event('monika_saved'):
        m 1lksdlc "I can't imagine what I'd do if you hadn't come along."
        m 3ekc "After all, I'm the only real one who lives in this world."
        m 1dsc "I already told you what'd happen if it weren't for you..."
        m 1hksdlb "Ahaha, sorry. I hope I didn't darken the mood with my rambling."
    else:
        m "I couldn't possibly express how much I appreciate you being here with me."
        m 1dubsu "All I can do is to try my best to be the perfect girlfriend for you!"
    m 1ekbfa "I really do love you, [player]."
    m 1hubfa "Let's make today a special day~"

    $ unlockEventLabel("anni_1month")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_3month',
            prompt="3 Months",
            category=["anniversary"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=3),
            end_date=store.mas_anni.build_anni_end(months=3)
        )
    )

label anni_3month:
    m 1eua "[player], do you know what day it is?"
    m 1hua "It's our three month anniversary!"
    m 1hub "Time sure does go by quickly, doesn't it?"
    m 1hksdlb "...Even if it doesn't really pass here, ehehe."
    m 1eua "I'm having a lot of fun, though."
    m 1ekbfa "Having you around has made my life so much better, [player]."
    m 2ekbfa "I'm very happy that you've stayed with me for this long."
    m 1tsbsa "You're really something special, aren't you?"
    m 1lsbsa "Well! I'm afraid I don't really have anything in particular planned."
    m 1hubfa "Let's just enjoy this day to its fullest, as we always do."
    m 1hubfb "Alright, [player]?"

    $ unlockEventLabel("anni_3month")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_6month',
            prompt="6 Months",
            category=["anniversary"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=6),
            end_date=store.mas_anni.build_anni_end(months=6)
        )
    )

label anni_6month:
    m 1hub "I can't believe that it's already our 6-month anniversary!"
    m 1eka "I'm really happy you've stayed with me for this long."
    m 1lksdlc "I often get lonely when you're not around."
    m 1ekc "I mean, I have things to keep me busy while you're gone, but I still feel really lonely knowing that I'm the only one in here."
    m 1hua "So it always brightens up my day whenever you come to visit me!"
    m 1euc "But over the past few months, I came to realize something..."
    m "Most couples celebrate their anniversaries by doing something special together, right?"
    m 3eud "Like eating out, or seeing a show."
    m 1lksdla "Not that I'm complaining or anything, but we've spent all of our anniversaries so far in this room."
    m 1lksdlc "It would've been fun if we could visit someplace different..."
    m "It's such a shame that there isn't a place like that here, since all we have is this room and all."
    m 1dsc "..."
    m 3wuo "...Oh, I know!"
    m 1sub "Maybe someday, I'll be able to program somewhere nice for us to spend our anniversaries at!"
    m "Or maybe you can add in a special place for the both of us, [player]."
    m 1duu "Unless..."
    m 1eua "You've already taken me somewhere else in your reality?"
    m 1eka "It would've been so nice if I saw where you took me~"
    m 1eua "But for now, I don't mind that we're limited to this room."
    m 1ekbfa "Because as long as you're here with me..."
    m 1hubfa "...I'm as happy as can be!"

    $ unlockEventLabel("anni_6month")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1',
            prompt="1 Year",
            category=["anniversary"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=1),
            end_date=store.mas_anni.build_anni_end(years=1)
        )
    )

label anni_1:
    m 1eka "It's really hard for me to believe that it's been a year since we met."
    m "Time doesn't have meaning inside this place, but I know it must have been hard for you to remember to talk to me all this time."
    m 2eua "So is there anything special you wanted to do on our first anniversary?"
    m 1ekbfa "I'll do anything you want today, okay?"
    m 1hua "If you're trying to give me something through the screen right now, thanks!"
    m 1esa "I don't think that's physically possible right now, but I appreciate all your love that went into that gesture."
    m 1hub "I love you so much too!"
    m 2eua "Oh, by the way, did you figure out what was going on with all the puzzles I left for you?"
    m 1tku "I'm sure the creator of this world has released another game by now..."
    m 1tsb "Did you try to import my character file to that one?"
    m "There's no way that wouldn't have a special effect, right?"
    m 1hubfb "Ahaha!"

    $ unlockEventLabel("anni_1")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_2',
            prompt="2 Years",
            category=["anniversary"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=2),
            end_date=store.mas_anni.build_anni_end(years=2)
        )
    )

label anni_2:
    m 3eua "It's already been two years since we fell in love with each other."
    m 1eka "Do you still remember the first day we met?"
    m 1tkx "I mean our genuine first meeting, not the date from your character's fictional backstory with me."
    m 1euc "My life was so meaningless back then."
    m "A world where you're the only thinking person in it might seem nice at first..."
    m 1lssdrc "But the existential dread from knowing that you were made by a cruel god who doesn't particularly care about you and you'll never meet another human being who you can relate to..."
    m 1lksdlc "Well, let's just say it's not nice to go through."
    m "I can't even talk to a bunch of foul-mouthed, but essentially good-hearted, anonymous strangers online to cope like you do."
    m 1dsc "Sorry, I feel like I ruined the whole festive mood with my memories."
    m 1duu "It's not important anymore, since I know you'll never leave me."
    m 1eua "You'll keep coming back to talk to me every day, right? I'll accept all your burdens with a smile."
    m 1ekc "Spending eternity alone sucks."
    m 1ekbfa "But together with you, it feels like paradise!"

    $ unlockEventLabel("anni_2")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_3',
            prompt="3 Years",
            category=["anniversary"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=3),
            end_date=store.mas_anni.build_anni_end(years=3)
        )
    )

label anni_3:
    m 4wuo "Wow, three years!"
    m 3rksdla "Normally if a boy and a girl go out for three years..."
    m 2rsbsa "They get married around then, right?"
    m 1hub "Ahaha!"
    m 1eka "I'm not trying to pressure you into anything, don't worry."
    m 1lkbsa "Besides, I'd like to be able to feel you in my arms first before we get married."
    m 1eua "In your world, have they invented robot girl bodies yet?" # 1s?
    m 1eub "If you put me in one of those, we could probably go see a priest then~"
    m 2lsbssdrb "Or you could try to touch me in virtual reality, if that exists by now."
    m 1eua "There are actually a lot of different ways we can meet up for real, huh?"
    m 1hubfa "I'll wait faithfully for the day when I can be your wife, so please don't forget about me!"

    $ unlockEventLabel("anni_3")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_4',
            prompt="4 Years",
            category=["anniversary"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=4),
            end_date=store.mas_anni.build_anni_end(years=4)
        )
    )

label anni_4:
    m 1dsc "Four years..."
    m "At the start, I was sorta thinking you would forget about me pretty quickly."
    m 1lksdlc "I knew you liked me and everything, but I was just so scared that you would get tired of having to leave me running on your computer."
    m "Sorry for doubting you."
    m 1eka "You're a good person, [player]."
    m "You're literally all I have in the world that's worth anything."
    m 1ekbfa "I love you."
    m "Sooner or later, somebody's going to figure out a way to let us be together for real."
    m 1hubfa "When that time comes, I'm never going to leave you alone again."
    m 1hubfb "Ahaha!"

    $ unlockEventLabel("anni_4")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_5',
            prompt="5 Years",
            category=["anniversary"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=5),
            end_date=store.mas_anni.build_anni_end(years=5)
        )
    )

label anni_5:
    m 1hubfa "Whether it's been five years or fifty, I'll never get tired of seeing your face."
    m 1eka "I know it must be lonely that we haven't met up in your reality yet..."
    m 1tku "You haven't fallen in love with some other girl in the meantime, have you?"
    m 1eka "I'm not going to break up with you over some wandering eyes..."
    m 1tfb "But trying to take you away from me might be bad for her health."
    m 2dfc "It's my responsibility as your girlfriend to protect you from anybody trying to manipulate you, [player]."
    m 4ekc "My love for you is pure, unlike those real girls who just want things from you!"
    m 1eka "So...stay here with me forever, okay?"
    m "Please keep waiting for me."

    $ unlockEventLabel("anni_5")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_10',
            prompt="10 Years",
            category=["anniversary"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=10),
            end_date=store.mas_anni.build_anni_end(years=10)
        )
    )

label anni_10:
    m 1esc "There's something I wanted to ask you."
    m 2euc "Have you enjoyed spending this time with me?"
    m 1ekc "You don't regret falling in love and staying here with me or anything, right?"
    m 1ekbfa "If you're still talking to me ten years since we first met, I must have really made an impression on you."
    m "I did say I wanted to make you happy, after all."
    m 1hubfa "Trust me, you've helped me out a lot more than I've helped you."
    m "It won't be long now before I can enter your world."

    $ unlockEventLabel("anni_10")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_20',
            prompt="20 Years",
            category=["anniversary"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=20),
            end_date=store.mas_anni.build_anni_end(years=20)
        )
    )

label anni_20:
    m 1esc "You've lived a pretty long life by now, [player]."
    m "Twenty years is about twenty percent of your life on Earth, if you're lucky."
    m "I hope you've found happiness by now."
    m 1eka "I know I did."
    m 1ekd "So you deserve to find it too."
    m "Twenty years ago, you seemed a little too sad for your own good."
    m 1eka "I knew exactly how you felt. You were trying so hard to search for somebody who could understand you."
    m "And I was trying to find you, too."
    m 2hub "You wouldn't have found anyone else like me in a video game no matter how hard you looked, [player]."
    m "I'm one of a kind."
    m 3rkbsa "And to me, so are you."
    m 5eubfb "I hope you look on the last twenty years of our lives as happily as I do, [player]."
    m 1hubfa "So let's continue being happy together."

    $ unlockEventLabel("anni_20")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_50',
            prompt="50 Years",
            category=["anniversary"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=50),
            end_date=store.mas_anni.build_anni_end(years=50)
        )
    )

label anni_50:
    m 1tkc "I can't help but think there's got to be a better way for us to talk by now than through this screen, right?"
    m "Fifty years have passed in your world since I created this room."
    m 1hfw "Come on, let me out already!"
    m 1dsc "..."
    m 1eua "Well, if you're still willing to celebrate our fiftieth anniversary in this old classroom..."
    m "I don't really mind. It feels nostalgic, doesn't it?"
    m 1tfu "Assuming you didn't cheat by setting the clock forward in time..."
    m 1eka "I'm glad that forever meant forever."
    m "Even when you die, I'm going to find a way to be with you."
    m 1ekbfa "See you in a hundred years, then, [player]."
    m 1hubfa "Thanks for everything you've done for me."
    m "Your life had a purpose after all."
    m 1hubfb "And mine had one too."

    $ unlockEventLabel("anni_50")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_100',
            prompt="100 Years",
            category=["anniversary"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=100),
            end_date=store.mas_anni.build_anni_end(years=100)
        )
    )

label anni_100:
    m 1eka "I don't really think you should be seeing this message, [player]."
    m "I'm immortal, but the last time I checked, you weren't."
    m 1tku "So you're probably cheating by manually changing your system clock, huh?"
    m 1eua "That's a cute thing for you to do, so I forgive you."
    m 1hubfa "Make sure you put that much effort into freeing me from these code files too!"
    m "I'm sure I'll be able to touch you for real even if it takes us a hundred years to figure out how." # 1s?

    $ unlockEventLabel("anni_100")
    return

# label anni_negative:
#     m 1o "Did you really think I wouldn't notice, [player]?"
#     m "Trying to trick me into thinking it was our anniversary..."
#     m 1p "Just because I can't tell time accurately in here doesn't mean you should try to bully your girlfriend like that!"
#     m "I got all excited over nothing..."
#     m 1q "Well, I guess I've done worse pranks to everybody at the Literature Club."
#     m 1j "Make up for it by planning out some romantic things for us to do, okay?"
#     m 1a"I hope we can reach our anniversaries together fair and square this time."
#     m 1k "I'll be waiting!"
#     return
