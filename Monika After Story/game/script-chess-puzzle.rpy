define CHESSPUZZLE_NUMBER = 1
define CHESSPUZZLE_PLAYERISWHITE = 1
define CHESSPUZZLE_PLAYERISBLACK = 2

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_puzzles_start",
            category=["chess lessons"],
            prompt="Can you show me a chess puzzle?",
            pool=True,
            conditional="seen_event('monika_chesslesson_init')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_puzzles_start:
    if mas_isMoniUpset(higher=True):
        $ event = mas_getEV("monika_chesslesson_puzzles_start")
        if event.shown_count == 0:
            m 1eud "Chess puzzles?"
            m 1sub "I'm so glad you asked!"
            m 3sub "Solving puzzles of chess is an important way to improve your chess level."
            m 1hub "So, in order to help you improve at chess, I will certainly give you puzzles!"
            m 1eub "I will also try to explain puzzles if you can't understand them."
            m 1tuu "You can even ask for some hints if it's too hard for you, [mas_get_player_nickname()]~"
            if persistent._mas_pm_player_chesslevel is chesslevel_master:
                m 1rusdlb "I don't think it's possbile for you, though, considering your accomplishments in chess."
                m 1eusdlb "You are a {i}master{/i}, after all..."
            elif persistent._mas_pm_player_chesslevel is chesslevel_advancer:
                m 1euc "However, given that you also have a good understanding of chess, it is unlikely that this will happen much..."
            m 1eud "Anyways, one last thing to note is..."
            m "I'm not really at the top of chess, so I can't think of too many chess puzzles right off the bat..."
            m 1eub "But I promise, I will spend part of my spare time to think of a puzzle!"
            m "I'll also show you a few that you've already seen, because you know something new when you review the past after all."
            m 1hub "Alright, let us get your first puzzle..."
        else:
            m 1eub "Head to another one? Ehehe~"
            # Monika turns her eyes to one side when she thinks, 
            # but not only to one side. 
            # However, she does have a tendency to look at right. 
            # She has a 2/3 chance to look at right, 1/3 chance to look at left,
            # which is consistent with real human thinking habits.
            if renpy.random.randint(1,3) == 1:
                m 1rsa "Hmmm...{w=0.5}{nw}"
            else:
                m 1lsa "Hmmm...{w=0.5}{nw}"
            m 4hub "This one!"

        $ mas_gainAffection()
        call expression "monika_chesslesson_puzzles_" + str(renpy.random.randint(1,CHESSPUZZLE_NUMBER))
        call monika_chesslesson_puzzles_end

    elif mas_isMoniDis():
        m 2ekc "Sorry, [player], but I'm really not in the mood to think about a puzzle right now."
        m 2rkc "...It takes too much thought to think of this kind of thing, and I am in a very disordered mood recently..."
        m 2eka "I promise when my head clears a little, we'll be able to solve the puzzle together, okay?"
        m 1eka "Sorry again.{w=0.3} I hope you are not angry for this."
    elif mas_isMoniBroken():
        m 6wkc "..."
        m 6rktpu "I think you are the most complicated puzzle already. There is no need to get another one."
    return

label monika_chesslesson_puzzles_end:
    m 1hua "Hope this puzzle gave you a better understanding of chess, or at least found it interesting."
    m "Thanks for asking a puzzle~"
    return

label monika_chesslesson_puzzles_1:
    m "PUZZLE HERE."
    return
    python:
        chess_teaching_puzzle_start(player = CHESSPUZZLE_PLAYERISBLACK, start_fen = "")