# Monika's Python Tip of the Day (PTOD)
# 
# I probably will be adding many of these, so For the sake of organization
# this is kept separate from script-topics.
#
# NOTE: these are considered pool type events, similar to writing tips
#
# And to keep the theme, these are 0-indexed
#
# META: Python things to talk about:
#   0 - what is python?
#   1 - types 
#   2 - Variables and assignment
#   3 - If statement / elif and else
#   4 - while loop
#   5 - for loop
#   6 - functions
#   7 - functions continiued?
#   8 - classes (might be too much)
#   9 - modules (might be too much) / importing?
#   10 - lists
#   11 - dict
#   12 - tuples
#   13 - py2 vs py3
#   

## We can assume evhand is already imported

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
    # I dont know that much about programming
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

    # python is a programming lanauge created in X
    # its an interpreted language, which means it does not need to be compiled
    # before being executed. this makes it easier and faster to make quick 
    # adjustments to code on the fly.
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
    # The versions of RenPy that runs this game uses Python2, so I'll 
    # mainly teach you python2
    # but i'll mention py3 at times when it's appropriate.
    # 
    #  That's my lesson for today!
    # Thanks for listening
    return 

###############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip002",
            category=["python tips"],
            prompt="Types",
            conditional="seen_event('monika_ptod_tip001')",
            action=EV_ACT_POOL
        )
    )

label monika_ptod_tip002:
    # In 
    return
