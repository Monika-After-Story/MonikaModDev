# Module that does hangman man
#

# hangman stuff only
define hm_ltrs_only = "abcdefghijklmnopqrstuvwxyz?!"

# IMAGES-----------
# hangman
image hm_6 = "mod_assets/hangman/hm_6.png"
image hm_5 = "mod_assets/hangman/hm_5.png"
image hm_4 = "mod_assets/hangman/hm_4.png"
image hm_3 = "mod_assets/hangman/hm_3.png"
image hm_2 = "mod_assets/hangman/hm_2.png"
image hm_1 = "mod_assets/hangman/hm_1.png"
image hm_0 = "mod_assets/hangman/hm_0.png"
image hm_s1 = "mod_assets/hangman/hm_s1.png"
image hm_s2 = "mod_assets/hangman/hm_s2.png"

# frame
image hm_frame = "mod_assets/hangman/hm_frame.png"

# TRANSFORMS
transform hangman_board:
    xanchor 0 yanchor 0 xpos 675 ypos 100 alpha 0.7

transform hangman_missed_label:
    xanchor 0 yanchor 0 xpos 680 ypos 105

transform hangman_missed_chars:
    xanchor 0 yanchor 0 xpos 780 ypos 105

transform hangman_display_word:
    xcenter 975 yanchor 0 ypos 475

transform hangman_hangman:
    xanchor 0 yanchor 0 xpos 880 ypos 125

# we want monika on a kind of offset to the left
transform hangman_monika(z=0.80):
    tcommon(330,z=z)

transform hangman_monika_i(z=0.80):
    tinstant(330,z=z)

# styles for words
style hangman_text:
    yalign 0.5
    font "gui/font/Halogen.ttf"
    size 30
    color "#000"
    outlines []
    kerning 10.0

#init -1 python:

    # defining a class to contain a hangman letter
    #
    # NOTE: we might not need this (OR might). Keep for reference
    #
    # PROPERTIES:
    #   letter - the letter this letter represents
    #   xpos - the xposition of this letter
    #   ypos - the y position of this letter
    #   visible - True means show the letter, False will show a blank (_)
#    class MASHangmanLetter():
#        def __init__(self, letter, xpos, ypos):
#            self.letter = letter
#            self.xpos = xpos
#            self.ypos = ypos
#            self.visible = False

init -1 python in hangman:
    # preprocessing
    # get poemwords as hangman words
    hm_words = list()

    # we need a copy of the full wordlist
    all_hm_words = list()

    # CONSTANTS
    # spacing between rendered letters
    LETTER_SPACE = 10.0

    # word properties
    WORD_FONT = "gui/font/Halogen.ttf"
    WORD_SIZE = 30
    WORD_OUTLINE = []
    WORD_COLOR = "#fff"
    WORD_COLOR_GET = "#CC6699"
    WORD_COLOR_MISS = "#000"

    # hangman visual stuff
    HM_IMG_NAME = "hm_"

    # hint
    HM_HINT = "{0} would like this word the most."

# post processing
init 10 python:
    
    # setting up wordlist
    from store.hangman import hm_words, all_hm_words
    from copy import deepcopy

    # for now, lets use full_wordlist defined in poemgame
    # this is a list of PoemWord objects
    for word in full_wordlist:
        
        winner = ""

        # figure out who likes this word the most
        if word.sPoint > word.nPoint and word.sPoint > word.yPoint:
            winner = "Sayori" # sayori

        elif word.nPoint > word.yPoint:
            winner = "Natsuki" # natsuki

        else:
            winner = "Yuri" # yuri

        hm_words.append((word.word, winner))

    all_hm_words = deepcopy(hm_words)

#   NOTE: this is in case we decide to change wordlist
#    with renpy.file("poemwords.txt") as words:
#        for line in words:
#
#            line = line.strip()
#
#            if len(line) != 0 and line[0] != "#":
#
#                # word, sPt, nPt, yPt
#                hm_words.append(line.split(",")[0]) 
#    all_hm_words = list(hm_words)

    # setting up image names



# entry point for the hangman game
label game_hangman:
    $ import store.hangman as hmg
    $ from copy import deepcopy
    m 2b "You want to play hangman? Okay!"
    # setup positions
    show monika at hangman_monika
    show hm_frame at hangman_board zorder 5

    python:
        # setup constant displayabels
        missed_label = Text(
            "Missed:", 
            font=hmg.WORD_FONT,
            color=hmg.WORD_COLOR,
            size=hmg.WORD_SIZE,
            outlines=hmg.WORD_OUTLINE
        )

    # show missed label 
    show text missed_label zorder 10 as hmg_mis_label at hangman_missed_label
    
    # FALL THROUGH TO NEXT LABEL

# looping location for the hangman game
label hangman_game_loop:
    m 1a "I'll think of a word..."
    pause 0.7
   
    python:
        # refill the list if empty
        if len(hmg.hm_words) == 0:
            hmg.hm_words = deepcopy(hmg.all_hm_wordS)

        # randomly pick word
        word = renpy.random.choice(hmg.hm_words)
        hmg.hm_words.remove(word)

        # setup display word and hint
        display_word = list("_" * len(word[0]))
        hm_hint = hmg.HM_HINT.format(word[1])

        # we dont need PoemWord anymore
        word = word[0]
      
        # turn the word into hangman letters
        # NOTE: might not need this (or might). keep for reference
#       hm_letters = list()
#       for dex in range(0,len(word))
#           hm_letters.append(MASHangmanLetter(
#               word[dex],
#               hmg.WORD_XPOS_START + (hmg,LETTER_SPACE * dex),
#               hmg.WORD_YPOS_START
#           )
    
    m "Alright, I've got one."
    m "[hm_hint]"
    # main loop for hangman game
    $ done = False
    $ win = False
    $ chances = 6
    $ missed = ""
    $ avail_letters = list(hm_ltrs_only)
    $ dt_color = hmg.WORD_COLOR
    while not done:
        # create displayables
        python:
            if chances == 0:
                dt_color = hmg.WORD_COLOR_MISS
            elif "_" not in display_word:
                dt_color = hmg.WORD_COLOR_GET

            display_text = Text(
                "".join(display_word), 
                font=hmg.WORD_FONT,
                color=dt_color,
                size=hmg.WORD_SIZE,
                outlines=hmg.WORD_OUTLINE,
                kerning=hmg.LETTER_SPACE
            )

            missed_text = Text(
                missed,
                font=hmg.WORD_FONT,
                color=hmg.WORD_COLOR,
                size=hmg.WORD_SIZE,
                outlines=hmg.WORD_OUTLINE,
                kerning=hmg.LETTER_SPACE
            )

        # show disables
        show text display_text zorder 10 as hmg_dis_text at hangman_display_word
        show text missed_text zorder 10 as hmg_mis_text at hangman_missed_chars

        # sayori easter egg
        if persistent.playername.lower() == "sayori" and chances == 0:

            # disable hotkeys, music and more
            $ disable_esc()
            $ store.songs.enabled = False
            $ store.hkb_button.enabled = False

            # setup glitch text
            $ hm_glitch_word = glitchtext(20) + "?"
            $ style.say_dialogue = style.edited

            # show hanging sayori
            show hm_s2 zorder 10 at hangman_hangman

            # hide monika and display glitch version
            hide monika 
            show monika_body_glitch1 as mbg zorder 3 at hangman_monika_i(z=1.0)

            # tear screen and glitch sound
            show screen tear(20, 0.1, 0.1, 0, 40)
            play sound "sfx/s_kill_glitch1.ogg"
            pause 0.2
            stop sound
            hide screen tear

            # display weird text
            m "{cps=*2}[hm_glitch_word]{/cps}{nw}"

            # tear screen and glitch sound
            show screen tear(20, 0.1, 0.1, 0, 40)
            play sound "sfx/s_kill_glitch1.ogg"
            pause 0.2
            stop sound
            hide screen tear

            # hide scary shit and return to normal
            hide mbg
            show monika 1 at hangman_monika_i
            hide hm_s2
            $ style.say_dialogue = style.normal
            $ store.songs.enabled = True
            $ store.hkb_button.enabled = True
            $ enable_esc()

        $ hm_display = hmg.HM_IMG_NAME + str(chances)

        show expression hm_display zorder 10 as hmg_hanging_man at hangman_hangman


        if chances == 0:
            $ done = True
            m 1j "Better luck next time~"
        elif "_" not in display_word:
            $ done = True
            $ win = True
        else:
            python:

                # input loop
                bad_input = True
                while bad_input:
                    guess = renpy.input(
                        "Guess a letter: (Type '?' to repeat the hint, " +
                        "'!' to give up)",
                        allow="".join(avail_letters),
                        length=1
                    )

                    if len(guess) != 0:
                        bad_input = False
                
            # parse input
            if guess == "?": # hint text
                m "[hm_hint]"
            elif guess == "!": # give up dialogue
                $ done = True
                hide hmg_hanging_man
                show hm_6 zorder 10 as hmg_hanging_man at hangman_hangman
                m 1n "[player]..."
                m "You should at least play to the end..."
                m 1f "Giving up so easily is a sign of poor resolve."
                if chances > 1:
                    m "I mean, you'd have to miss [chances] more letters to actually lose."
                else:
                    m "I mean, you'd have to miss [chances] more letter to actually lose."
                m 1e "Can you play to the end next time, [player]? For me?"
            else:
                python:
                    if guess in word:
                        for index in range(0,len(word)):
                            if guess == word[index]:
                                display_word[index] = guess
                    else:
                        chances -= 1
                        missed += guess
                        if chances == 0:
                            # show the word you lost
                            display_word = word

                    # remove letter from being entered agin
                    avail_letters.remove(guess)

                # HIDE displayables
                hide text hmg_dis_text
                hide text hmg_mis_text
                hide hmg_hanging_man

    # post loop
    if win:
        m 1j "Wow, you guessed the word correctly!"
        m "Good job, [player]!"
        $ grant_xp(xp.WIN_GAME)

    # try again?
    menu:
        m "Would you like to play again?"
        "Yes":
            jump hangman_game_loop
        "No":
            jump hangman_game_end

    # RETURN AT END 

# end of game flow
label hangman_game_end:
    # hide the stuff
    hide hmg_hanging_man
    hide hmg_mis_label
    hide hmg_dis_text
    hide hmg_mis_text
    hide hm_frame
    show monika at t32

    m 1d "Hangman is actually a pretty hard game."
    m "You need to have a good vocabulary to be able to guess different words."
    m 1j "The best way to improve that is to read more books!"
    m 1a "I'd be very happy if you did that for me, [player]."
    return
