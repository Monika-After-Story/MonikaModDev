# Monika's Python Tip of the Day (PTOD)
#
# I probably will be adding many of these, so For the sake of organization
# this is kept separate from script-topics.
#
# NOTE: these are considered pool type events, similar to writing tips
# NOTE: these are also NOT literally once a day. There is a day in between
#   unlocking the next one, though
#
# And to keep the theme, these are 0-indexed
#
# META: Python things to talk about:
#   0 - what is python?
#   --- sugestion python compared to other languages/ how does it work
#   --- suggestion mention syntax and probably how to get python maybe separate each part
#   1 - types
#       - numbers and strings, Nones are together (002)
#     - comparisons (bools) (should be its own title
#   2 - Variables and assignment
#   3 - If statement / elif and else
#   4 - while loop
#   5 - for loop
#   6 - functions
#   7 - functions continiued?
#   8 - classes (might be too much) -- Definitely too much, we should probably stick to functional programming
#   9 - modules (might be too much) / importing? -- mention importing only, module making is too much
#   10 - lists
#   11 - dict
#   12 - tuples
#   13 - py2 vs py3
#   14 - String operations
#   15 - start talking about renpy
#
#
# Also what about Renpy?
#
# Another NOTE: We should try to make the topics of an adequate lenght otherwise
# we're just going to throw a lot of info that is going to be ignored or forgotten quickly
# I think splitting something in more than one topic may be a good idea
#
## We can assume evhand is already imported

init 4 python in mas_ptod:
    # to simplify unlocking, lets use a special function to unlock tips
    import datetime
    import store.evhand as evhand

    M_PTOD = "monika_ptod_tip{:0>3d}"

    def has_day_past(tip_num):
        """
        Checks if the tip with the given number has already been seen and
        a day has past since it was unlocked.
        NOTE: by day, we mean date has changd, not 24 hours

        IN:
            tip_num - number of the tip to check

        RETURNS:
            true if the tip has been seen and a day has past since it was
            unlocked, False otherwise
        """
        # as a special thing for devs
        if renpy.game.persistent._mas_dev_enable_ptods:
            return True

        tip_ev = evhand.event_database.get(
            M_PTOD.format(tip_num),
            None
        )

        if tip_ev is None:
            return False

        # otherwise, unlocked date is our key
        if tip_ev.unlock_date is None or tip_ev.shown_count == 0:
            return False

        # now check the actual day
        return (
            datetime.date.today() - tip_ev.unlock_date.date() 
            > datetime.timedelta(days=1)
        )


# The initial event is getting Monika to talk about python
# this must be hidden after it has been completed
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip000",
            category=["python tips"],
            prompt="Can you teach me about Python?",
            pool=True
        )
    )

label monika_ptod_tip000:
    # You want to learn about Python?
    # Aha yokatta
    # I dont know that much about programming, I'm still learning
    # but i will try my best
    # lets start with whaat python is

    # hide this label since we dont need it anymore
    $ hideEventLabel("monika_ptod_tip000", depool=True)
    jump monika_ptod_tip001

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip001",
            category=["python tips"],
            prompt="What is Python?"
        )
    )

label monika_ptod_tip001:
    # first enable this event
    $ evhand.event_database["monika_ptod_tip001"].pool = True

    # Python was created by Guido Van Rossum in the early 90s
    # -- the bit explaining that is interpreted is probably a bit too soon
    # -> Yeah, save this part for later. This seciton should be an overview of
    #   what python is used for, the fact that its a programming language,
    #   and the 2 main versions. also how it relates to MAS via RenPy
    # its an interpreted language, which means it does not need to be compiled
    # before being executed. this makes it easier and faster to make quick
    # adjustments to code on the fly.
    # --
    # Python is used in many places, including web apps, embedded stuff,
    # rasberry pi, x, y, z, and ofc, This game!
    # DDLC, in particular uses a game engine called RenPy, which is built off
    # of Python. If you learn python, you can learn how to mod this?
    #
    # One last thing, Thre are currently 2 main versions of python:
    # py2 and py3. These versions are **incompatible** with each other
    # because the changes added in py3 fixed many fundamental design flaws in
    # py2. Even though this caused a split in the python community, it's
    # generally agreed that both versions of the language have their own
    # strengths and weaknesses.
    #
    # [show this once]
    # The versions of RenPy that runs this game uses Python2, so I'll
    # mainly teach you python2
    # but i'll mention py3 at times when it's appropriate. -- for saying that she doesn't know much she seems rather confident here
    #
    # That's my lesson for today!
    # Thanks for listening
    # [end]
    return

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip002",
            category=["python tips"],
            prompt="Types",
            conditional="store.mas_ptod.has_day_past(1)",
            action=EV_ACT_POOL
        )
    )

label monika_ptod_tip002:
    # [show this once]
    # In most programming languages, each piece of data that can be chnaged
    # or modified by a program has a _type_
    # associated with it. If some data should be treated as a number, then
    # it will have a numeric type. If some data should be treated as text,
    # then it will have a string type.
    # [end]
    #
    # Python has two separate types to represent numbers: _integers_ and _floats_.
    # Integers are used to represent whole numbers - Anything that isn't a
    # decimal.
    # -22, 0, -1234, 42 are all integers in python.
    # Floats are used to represent decimals:
    # 0.14, 9.3, -10.2 would all be floats in Python.
    #
    # Text in python is represented with string types. 
    # anything surrounded in single quotes (') or double quotes (") are strings.
    # For example, 'this is a string in single quotes'
    # And "this is a string in double quotes".
    # Strings can also be created with three double quotes ("""), but these
    # strings are treated specially in python. I'll talk about this another day.
    #
    # Python also has a special data type called a NoneType. This type 
    # represents the absence of any data. If you're familiar with with other
    # programming languages, this is akin to a null or undefined type.
    # The keyword None represents NoneTypes in python.
    #
    # [show this once]
    # Python uses other data types, but I think the types we've covered is
    # enough for today.
    # Thanks for listening!
    # [end]
    return

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip003", # may change order, you decide on this
            category=["python tips"],
            prompt="How does Python work?",
            conditional="store.mas_ptod.has_day_past(1)",
            action=EV_ACT_POOL
        )
    )

label monika_ptod_tip003:
    # Python is an interpreted language, which means it requires to be *interpreted*
    # by a thing called python interpreter
    # you can download that interpreter from  -- link to python 2
    # check if renpy.macintosh mention that the user already has it
    # TODO this is unfinished and I dislike how I've worded it so far
    #
    return

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip004",
            category=["python tips"],
            prompt="What does python code look like?",
            conditional="store.mas_ptod.has_day_past(1)",
            action=EV_ACT_POOL
        )
    )

label monika_ptod_tip004:
    # Oh well this may be a bit hard to explain here but I'll do my best for you [player]
    # The first thing you need to know is that any line starting with a # is going to
    # be ignored and you can write anything on that line
    # those lines are named comments, and you use them to explain what your code does
    # it's a good practice to comment your code so you don't forget later what it was supposed to do!
    # TODO unfinished and probably will split it in more than just one, also I know I should call it
    # python syntax but I'm making it non programmers friendly
    return

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip005",
            category=["python tips"],
            prompt="Comparisons and booleans",
#            conditional="store.mas_ptod.has_day_past(2)",
#   actually, this should probably unlock after we talk about variable 
#   assignment, since we can do an example like variable = a == b kind of thing
            action=EV_ACT_POOL
        )
    )

label monika_ptod_tip005:
    # [show this once]
    # So if you remember, a single = does assignment, the == does 
    # compariosns
    #
    # The boolean type represents True / False values. 
    return

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip006",
            category=["python tips"],
            prompt="Variables and Assignment",
            conditional="store.mas_ptod.has_day_past(2)",
            action=EV_ACT_POOL
        )
    )

label monika_ptod_tip006:
    # nothing here yet
    return
