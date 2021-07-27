###
# The current chess points list:
# 1. Openings for novelty.
# 2. Principle - 'usually so'
# 3. Openings for beginners
# 4. Have fun in chess
# 5. Tennison Gambit: Intercontinental Ballistic Missile Variation
###
define CHESSPOINT_NUMBER = 5

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

label monika_chesslesson_points_1:#Openings for novelty
    m 1eub "You know, there are many openings in chess."
    m 1eud "But no matter what opening, there is always one condition."
    m 1euc "That is, after the opening is finished, neither player is in a obvious disadvantage or advantage."
    m 1etd "After all, the opening is made by both players."
    m "If this opening is bad for one player, why would that player want to play this opening?"
    m 2eub "The purpose of learning the opening, more importantly, is to let you know all kinds of opening ideas, so that you can quickly guess the opponent's train of thought, save time."
    m 2eud "But the more we play, the more we start to feel one thing."
    m 2ruc "That is, the opening is really boring at times."
    m 2eud "For example, one of the most popular openings in the world is the Sicilian Defense."
    m 2esd "For those grandmasters, they probably have played over a thousand of Sicilian Defense openings."
    m 2esc "You don't even need to be a grandmaster to quickly get the feeling that the opening is a little boring."
    m 3eub "Fortunately, there's a lot of variation in chess openings. So you'll soon find another opening that you like, and you'll get a fresh start for a long time."
    m 2eka "What I want to say is, if one day you start to feel that your opening is so repetitive..."
    m 2ekb "I can always tell you about the other openings."
    m 2esb "I know a lot of openings."
    m 2esa "From the most popular to the least popular, I've dabbled in everything."
    m "Learning a new start for the sake of freshness is not uncommon, and it is often beneficial. It will give you a new way of thinking."
    m 2etblu "Not to mention, to be able to teach my beloved person is a kind of enjoyment in itself~"
    m 1hublu "That's kind of a romantic way to spend eternity right? Ehehe~"
    return

label monika_chesslesson_points_2:#Principle - 'usually so'
    m 1eub "We often talk about the word \"principle\" in chess."
    m 1eud "Every time we say a principle, we usually follow it with this condition: {i}Usually so{/i}."
    m 1ruc "It's normal to feel a little annoyed when you hear this a lot."
    m 1etc "After all, when you apply this principle, you will find that there are many situations where it works, but there are also situations where following the principle can put you at a disadvantage."
    m 1ttc "And then you remember that condition at the end:{w=0.2} \"usually\"."
    m 1ekd "And you start to get really annoyed, wondering, {i}\"what's usally and what's not\"{/i}?"
    m 1esc "If that's true of you, then I need to point out a point that many people miss."
    m 1esd "The goal of those principles is, and always is, to allow the less skilled player to react to a situation in a way that is not at least a big blunder."
    m 2esd "They are never meant for all horizontal segments."
    m 4esd "With these principles, at the very least, those who do not know anything about chess can find a little fun."
    m 4esc "Think back.{w=0.3} They work well in the first a few games, right?"
    m 4etc "But as you play more games, you start to see that sometimes they don't work."
    m 2eub "Then you mustn't let it bother you. Because it means your level has improved."
    m 2eua "You see, as you get better at it, you start looking for a better match, and against a better opponent, it's almost impossible to beat them with principles only."
    m 2esa "That's why they're starting to stop working."
    m 2esb "This is also the first frustrating part of learning chess."
    m 2etd "The way to get out of this phase is simply to keep playing chess, and contemplate for what the condition \"usually\" does not include."
    m 4eua "But remember, just being more isn't going to work. You have to analyze every game."
    m 2rsb "Of course, you can also ask others for help..."
    m 5ksbsu "...Like a cute, talented and beautiful girlfriend~"
    m 1hsblu "Ehehe~"
    return

label monika_chesslesson_points_3:#Openings to beginners
    m 2eud "You know, there are many openings. But not all of them are suitable for beginners."
    m 2euc "Like \"Alekhine's Defense\", this {i}not-so-popular{/i} opening line of thought is incomprehensible to many people."
    if mas_seenLabels("monika_chesslesson_points_1"):
        m 2eud "As far as this opening is concerned, I may put in a word."
        m 4eud "Do you remember how I told you that many people learn a new opening for the sake of freshness?"
        m 1eua "Alekhine's Defense is such an opening."
    else:
        m 1eua "Alekhine's Defense is an opening invented for the sake of novelty."
    m 1eub "Its inventor, Alekhine, tired of repetitive routines, responded the pawn with a shocking knight move."
    m 1husdlb "I didn't learn much about it because it was designed mainly for freshness and it was proven that the defender was at a slight disadvantage so it was not a {i}that{/i} good opening."
    m 1husdla "So if you're interested, you can look it up yourself. Since I haven't studied it, I won't talk about it."
    m 1eua "Now, let's get back to business."
    m 1eub "For beginners, I particularly recommend a few openings. They're great for beginners."
    m 3eub "The first one would be {i}Italian Game{/i}."
    m 3duc "Hold on...{w=0.3}{nw}"
    show monika at t21
    python:
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
    m 2lub "The one in front of your eyes now is the Italian Game."
    if seen_event("monika_chesslesson_italian_game"):
        m 2eub "Remember? I told you about this opening."
    else:
        m 2eub "I haven't told you about this opening before, but I've put it on my to-do list."
        m 2eua "You might consider finding out how to play this opening yourself, or wait for my lesson."
    m 4eua "It's a opening that relatively peaceful, less intense, and make beginners not that easy to lose."
    m 4esa "It is also a good start for beginners to understand what castle is."
    m 1eub "As for the second one, it would be French Defense."
    m 1duc "Hold on again...{w=0.3}{nw}"
    python:
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPP2PPP/RNBQKBNR w KQkq d6 0 3")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
    m 1lub "This one is the French Defense."
    if seen_event("monika_chesslesson_french_defense"):
        $ word = ",{w=0.2} too." if seen_event(monika_chesslesson_italian_game) == False else "."
        m 1eua "I know I haven't taught you this opening[word]"
        m 1hua "But I added it to my list[word]"
        m "So you may wait for my lesson to introduce it."
    m 3hua "In short, the French Defense was an opening that really focused on the word \"defense\"."
    m 1eub "The defensive side, which is the black side, creates a chain of pawns that looks plain, but is actually very strong."
    m 1esb "I recommend it for the same reason as Italian Game, beginners can at least have some fun without losing quickly when playing this opening."
    m 1rtd "However, the French Defense is more closed than the Italian Game, which is somewhat offensive. That's worth noting."
    m 1etd "As for the third one, I'd like to talk about Ruy Lopez, which is also called as Spanish Opening."
    m "This opening is not in my teaching list yet, but this one is actually a pretty typical opening."
    m 1duc "Just give me one second...{w=0.3}{nw}"
    python:
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
    m 2lua "Alright.{w=0.2}{nw}"
    extend 2eub " At first glance, this opening might look a lot like the Italian Game."
    m 2eua "This is also reasonable. After all, there is only one change of position compared to the Italian Game, that's the bishop's position."
    m 2eud "But it was this small change that made a big difference."
    m 2rtd "In Italian Game, the bishop's role is to control the center, but in this case, it's directly attacking the black knights."
    m 1etd "If Franch Defense was a more conservative opening than Italian Game, then this was a more intense one."
    m 1eub "If a beginner wants to see what an attack feels like, try this."
    m 1eua "The last thing I'd like to mention in passing is the Sicilian Defense."
    m 1eub "There are a lot of people who recommend this for new players."
    m 1etd "But I personally think that it's not a good opening for beginner."
    m 1duc "Let me show the Sicilian Defense here...{w=0.2}{nw}"
    python:
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
    m 1etd "Okay, here it is."
    if seen_event("monika_chesslesson_sicilian_defense"):
        m 1etc "You've heard me talk about it, so you should know why I don't think it's suitable for beginners."
    else:
        m 1etc "I haven't taught you this one yet, so let me tell you why I don't think it's suitable for beginners."
    m 1rtd "It's just too intense. Despite the word \"defense\" in its name, it often engages in fierce fighting."
    m 1etd "If the beginner don't know how to play it correctly, beginners will only lose very quickly and may be overwhelmed and lose confidence."
    m 2rtc "But think about it another way..."
    extend 2ltc " This kind of intense opening can also make beginners quickly realize their own shortcomings. So I'm not sure if it's suitable."
    m 2htsdla "After all, I could only say that I was good at chess among amateurs.{w=0.2} I was nowhere near as good as a real grandmaster."
    m 2htsdlb "Anyway, um...{w=0.2}{nw}"
    extend 2eub " The above suggestions are only applicable to most people. Maybe something else would suit you, this is also possible."
    m 1eua "As long as you want to play chess, I'm always here."
    m 1hua "So don't worry about having no one to play with!"
    $ chess_teaching_disp.hide()
    show monika at t11
    return

label monika_chesslesson_points_4:#Have fun in chess
    $ wins = persistent._mas_chess_stats["wins"]
    $ losses = persistent._mas_chess_stats["losses"]
    m 1eud "Do you know what's the most important thing in chess?"
    m 1esd "{i}Have fun{/i}."
    m 2eka "I'm serious."
    if losses < wins and losses > 30:#Probably a player struggling on chess.
        m 2ekb "Especially to you."
        m 2dud "I know you have lost many times here..."
        m 2eka "And I really hope you haven't lost your temper in the meantime."
    m 1eud "Always remember, chess is a game. And the goal of the game is, and always is, happiness."
    m 1duc "You may think that I am saying these words as casually..."
    m 1dkc "You might also think that from someone as pretty good in chess as I am, this would be an offhand remark."
    m 1eka "But I'm really serious."
    m 1esb "I'm human, too. I couldn't have been born knowing how to play chess."
    m 1duc "When I was learning chess myself, I used to get so angry that I just wanted to smash the board."
    m 1husdrb "...oh, you probably don't think it's something I would do, do you?"
    m 1esa "But I'm really just a normal human. I have my temper, too."
    m 3esd "During that period of time when I was losing and losing because I was playing chess against people who were better than me, I could hardly make any progress."
    m 2dsc "Because I'm just pissed off."
    m 2esc "It wasn't until a few months later that I suddenly understood."
    m 2esd "I was wrong. I suddenly remembered what's my first motivation to play chess."
    m 2ekd "Have fun."
    m 2esb "Just because I lose a lot of games doesn't mean I'm a bad person."
    m 2eka "This has been extremely difficult for me to realize because, as I told you, I have always tried to be perfect in all areas."
    m 1eka "You're such a wonderful person, and I'm sure you'll realize it someday."
    m 1dsc "And if you were ever mad that you lost to me...{w=0.2}"
    $ nickname = mas_get_player_nickname(exclude_names=["my love","love"])
    extend 1esd "Remember, I don't need my [nickname] to be talented at chess."
    m 1duu "My [nickname] cared for me and was willing to play chess with me, and that was all I needed."
    m 1esa "I'm not going to love you less because you're not good at chess."
    m 1ekbla "You will always be lovely in my eyes. It doesn't matter if you win or lose, you look cute."
    m 2dkbla "..."
    m 2ekbla "..."
    m 1hub "So, please, don't get too mad about the chess, okay?"
    return

label monika_chesslesson_points_5:#Tennison Gambit
    m 1wub "Oh!{w=0.2}{nw}"
    extend 1tsu " This one is a pretty useful one..."
    m 1ttu "It's a chess trap that hasn't been defeated for even once yet."
    m 1eud "There is an {i}unpopular{/i} opening variation called {i}Tennison Gambit: Intercontinental Ballistic Missile Variation{/i}."
    m 1euc "Although it is very unpopular, but so far, out of this opening situation has not lost a single game."
    m 1duc "Let us see...{w=0.5}{nw}"
    show monika at t21
    python:
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True)
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
    m 1eub "This is what it looks like at the beginning of each game."
    m 3eua "In Tennison Gambit, we chose to start by pushing the pawn in e2 to e4."
    python:
        chess_teaching_disp.queue_move("e2e4")
        chess_teaching_disp.handle_player_move()
    m 1eub "And if black responsed with this...{w=0.3}{nw}"
    python:
        chess_teaching_disp.queue_move("d7d5")
        chess_teaching_disp.handle_monika_move()
    extend 1ttu " then black is already losing. This is a fatal mistake. The game is already over."
    if seen_event("monika_chesslesson_scandinavian_defense"):
        m 1tsu "Yes, I know this is the Scandinavian Defense that I introduced to you."
        m 1esd "I know I told you that this is not a bad opening for either side. It is a reasonable opening."
        m 3tsb "But that only works when we ignore this invincible variation. I was afraid your mind could not accept such a shocking idea."
    else:
        m 1esd "The current situation, also known as the {i}Scandinavian Defense{/i}, is one of the popular openings."
        m 3tsb "But few people in the world realized that this opening could be transformed into a powerful one like this variation..."
    m 1eub "As I said, at this point, the opponent has essentially lost at this point."
    m 1eua "A mediocre white side player might choose to capture the opponent's pawn."
    m 1tfu "But we are not mediocre players.{w=0.3}{nw}"
    extend 1eub " In Tennison Gambit, we will move our knight and discard the pawn."
    python:
        chess_teaching_disp.queue_move("g1f3")
        chess_teaching_disp.handle_player_move()
        renpy.pause(1)
        chess_teaching_disp.queue_move("d5e4")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(1)
    m 1lud "The situation doesn't look good. We had already lost a pawn, and with the opponent's pawn threatening our knight, we seemed to have to spend another turn to get the knight safe."
    python:
        chess_teaching_disp.queue_move("f3g5")
        chess_teaching_disp.handle_player_move()
    m 3eub "But as we flee our knights here, we also attack our opponent's pawn."
    python:
        chess_teaching_disp.queue_move("g8f6")
        chess_teaching_disp.handle_monika_move()
    m 3hua "A very common choice for the opponent, of course, is to move their knight to protect the pawn."
    m 1lua "And then here, our second sacrifice is coming.{w=0.2}{nw}"
    python:
        chess_teaching_disp.queue_move("d2d3")
        chess_teaching_disp.handle_player_move()
    extend 1lub " We moved another pawn to an assailable square."
    m 3eub "The opponent, {i}naturally{/i}, was happy to take the pawn. So,{w=0.3}{nw}"
    python:
        chess_teaching_disp.queue_move("e4d3")
        chess_teaching_disp.handle_monika_move()
    extend 3lua " the opponent would play this move."
    python:
        chess_teaching_disp.queue_move("f1d3")
        chess_teaching_disp.handle_player_move()
    m 1eua "Then we can use the bishop to take the pawn.{w=0.3}{nw}"
    extend 1etd " As for the opponent? The opponent must have been very wary of our knight being so close to their rear,{w=0.2}{nw}"
    python:
        chess_teaching_disp.queue_move("h7h6")
        chess_teaching_disp.handle_monika_move()
    extend 1hua " so they used a pawn to attack our knight."
    m 1eub "Then we will make the third sacrifice.{w=0.3}{nw}"
    python:
        chess_teaching_disp.queue_move("g5f7")
        chess_teaching_disp.handle_player_move()
        chess_teaching_disp.request_highlight_common_format("d8",highlight_type_red)
        chess_teaching_disp.request_highlight_common_format("h8",highlight_type_red)
    extend 1lub " Since our knight attacked both the opponent's queen and the rook, obviously, the opponent had to take our knight."
    python:
        chess_teaching_disp.remove_highlight_all()
        chess_teaching_disp.queue_move("e8f7")
        chess_teaching_disp.handle_monika_move()
    m 1eud "The fourth and final sacrifice.{w=0.2} Let's move the bishop over.{w=0.3}{nw}"
    python:
        chess_teaching_disp.queue_move("d3g6")
        chess_teaching_disp.handle_player_move()
    extend 1hua " Apparently, you'd be a fool not to take such a gift. So the opponent will be happy to accept our sacrifice."
    python:
        chess_teaching_disp.queue_move("f7g6")
        chess_teaching_disp.handle_monika_move()
    m 1eua "Okay, now the king and queen were completely apart,{w=0.3}{nw}"
    python:
        chess_teaching_disp.request_highlight_file('d')
    extend 1wub " and there were no pieces between our queen and our opponent's queen! So it was clear what we were going to do."
    m 1hub "That would be to fire an RT-2PM2 Topol-M cold-launched three-stage solid-propellant silo ICBM at the opponent."
    m 1hua "For beginners, you can also choose to use anti-tank missiles instead."
    m ".{w=0.2}.{w=0.2}.{w=0.2}"
    m 1rusdlu "Puff!"
    m 1eusdlu "Okay, I can't hold that face anymore. This is actually a famous chess meme that I recently learnt."
    m 1eub "If you're interested, search for Tennison Gambit should be enough to find it."
    m 3eub "Although this is a meme, it does have something to learn from it."
    m 3husdlu "...{w=0.3}Ahaha, not the ICBM part of course, but the trap part in the front."
    m 3eub "So when I introduced this, I used several words like 'Obviously', 'Naturally'. In fact, these words themselves are irresponsible statements."
    m 1rtd "For example, the opponent didn't actually have to push the pawn to h6 square to attack our knight. A more common option is to move another knight to take control of the center."
    m 1eud "There are many leaks in this opening. As soon as your opponent doesn't take a move along that line of this idea, you're immediately at a huge disadvantage."
    m 1euc "I haven't really studied it, but I don't think any master player will fall into this trap."
    m 2husdrb "So the main reason I said it was 'invincible' earlier was because of the ICBM part, ahaha~"
    m 1esd "However, to be serious, think about it from another view, this opening also has its good idea."
    m 1esa "Like the idea of separating queen and king is a pretty good one."
    m 1eub "In addition, it is interesting to use this opening against players who are not very skilled."
    m 2husdrb "And, again, I'm not talking about ICBM part, ahaha~"
    $ chess_teaching_disp.hide()
    return
