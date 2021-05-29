define CHESSPOINT_NUMBER = 1

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_points_start",
            category=["chess lessons"],
            prompt="Can you tell me a point of chess?",
            pool=True,
            conditional="seen_event('monika_chesslesson_init')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_points_start:
    $ event = mas_getEV("monika_chesslesson_points_start")
    if event.shown_count == 0:
        m 1eud "You want me to tell you a point about chess?"
        m 1euc "..."
        m 1sub "Wow, that's great!"
        m 3sub "I didn't think of before can use this way to teach you chess!"
        m 2hub "There are a lot of points in chess that are piecemeal, and it's not easy to introduce them systematically into lessons..."
        m 2hua "From now on I will tell you these fragmented knowledge in this way!"
        m 1eub "In the future, ask me as many times as you want, I will always randomly pick one from my chess knowledge to tell you, so that you can remember them easily."
        m 1hua "Now, let me think about what I should put that knowledge as your first..."
        m 1hub "Oh, this one should be fit!"
    else:
        m 1eub "Ready to learn more? Ehehe~"
        # Monika turns her eyes to one side when she thinks, 
        # but not only to one side. 
        # However, she does have a tendency to look at right. 
        # She has a 2/3 chance to look at right, 1/3 chance to look at left,
        # which is consistent with real human thinking habits.
        if renpy.random.randint(1,3) == 1:
            m 1rsa "Hmmm...{w=0.5}{nw}"
        else:
            m 1lsa "Hmmm...{w=0.5}{nw}"

    call expression "monika_chesslesson_points_" + str(renpy.random.randint(1,CHESSPOINT_NUMBER))
    call monika_chesslesson_points_end
    return

label monika_chesslesson_points_end:
    m 1hua "Thanks for listening~"
    return

label monika_chesslesson_points_1:
    m "CHESS POINT 1 HERE."
    m "END."
    return