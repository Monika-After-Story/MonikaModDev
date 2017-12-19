# Module that does hangman man
#

# IMAGES-----------
# hangman
image hm_head = "mod_assets/hangman/hm_head.png"
image hm_leftarm = "mod_assets/hangman/hm_leftarm.png"
image hm_rightarm = "mod_assets/hangman/hm_rightarm.png"
image hm_leftleg = "mod_assets/hangman/hm_leftleg.png"
image hm_rightleg = "mod_assets/hangman/hm_rightleg.png"
image hm_torso = "mod_assets/hangman/hm_torso.png"

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
transform hangman_monika:
    tcommon(330)

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
    # starting point of the letter generation
#    WORD_XPOS_START = 760
#    WORD_YPOS_START = 210
#    WORD_XALIGN_START = 0.0
#    WORD_YALIGN_START = 0.0

    # spacing between rendered letters
    LETTER_SPACE = 10.0

    # word properties
    WORD_FONT = "gui/font/Halogen.ttf"
    WORD_SIZE = 30
    WORD_OUTLINE = []
    WORD_COLOR = "#fff"

    # other props
#    MISS_LABEL_XPOS_START = 190
#    MISS_LABEL_YPOS_START = -530
#    MISS_LETTERS_XPOS_START = 260
#    MISS_LETTERS_YPOS_START = -460
#    MISS_LABEL_XALIGN_START = 0.0
#    MISS_LABEL_YALIGN_START = 0.0
#    MISS_LETTERS_XALIGN_START = 0.0
#    MISS_LETTERS_YALIGN_START = 0.0

    # hangman visual stuff
    HM_IMG_NAME = "hm_"

    # hangman image properties
#    HM_IMG_XPOS = 0
#    HM_IMG_YPOS = 0
#    HM_IMG_ZORDER = 10

    # hangman AT list
#    HM_IMG_ATLIST = [
#        "hangman_hangman"
#    ]

    # hangman tag
#    HM_IMG_TAG = "hmg_hanging_man"

# post processing
init 10 python:
    
    # setting up wordlist
    from store.hangman import hm_words, all_hm_words
    with renpy.file("poemwords.txt") as words:
        for line in words:

            line = line.strip()

            if len(line) != 0 and line[0] != "#":
                hm_words.append(line.split(",")[0])
    all_hm_words = list(hm_words)

    # setting up image names
    renpy.image("hm_6","mod_assets/hangman/hm_6.png")
    renpy.image("hm_5","mod_assets/hangman/hm_5.png")
    renpy.image("hm_4","mod_assets/hangman/hm_4.png")
    renpy.image("hm_3","mod_assets/hangman/hm_3.png")
    renpy.image("hm_2","mod_assets/hangman/hm_2.png")
    renpy.image("hm_1","mod_assets/hangman/hm_1.png")
    renpy.image("hm_0","mod_assets/hangman/hm_0.png")


# entry point for the hangman game
label hangman_game_start:
    $ import store.hangman as hmg
    m 2b "You want to play Hangman? Okay!"
    # setup positions
    show monika at hangman_monika
    show hm_frame at hangman_board zorder 5

    python:
        # setup constant displayabels
        missed_label = Text(
            "Missed:", 
#            xpos=hmg.MISS_LABEL_XPOS_START,
#            ypos=hmg.MISS_LABEL_YPOS_START,
#            xalign=hmg.MISS_LABEL_XALIGN_START,
#            yalign=hmg.MISS_LABEL_YALIGN_START,
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
    m 1a "I'll think of a word"
    pause 0.7
   
    python:
        # refill the list if empty
        if len(hmg.hm_words) == 0:
            hmg.hm_words = list(hmg.all_hm_wordS)

        # randomly pick word
        #word = renpy.random.choice(hmg.hm_words)
        word = "uncontrollable"
        display_word = list("_" * len(word))
      
        # turn the word into hangman letters
        # NOTE: might not need this (or might). keep for reference
#       hm_letters = list()
#       for dex in range(0,len(word))
#           hm_letters.append(MASHangmanLetter(
#               word[dex],
#               hmg.WORD_XPOS_START + (hmg,LETTER_SPACE * dex),
#               hmg.WORD_YPOS_START
#           )
    
    m "Alright, I've got one"

    # main loop for hangman game
    $ done = False
    $ win = False
    $ chances = 6
    $ missed = ""
    $ avail_letters = list(l_letters_only)
    while not done:
        # create displayables
        python:
            display_text = Text(
                "".join(display_word), 
#                xpos=hmg.WORD_XPOS_START,
#                ypos=hmg.WORD_YPOS_START,
#                xalign=hmg.WORD_XALIGN_START,
#                yalign=hmg.WORD_YALIGN_START,
                font=hmg.WORD_FONT,
                color=hmg.WORD_COLOR,
                size=hmg.WORD_SIZE,
                outlines=hmg.WORD_OUTLINE,
                kerning=hmg.LETTER_SPACE
            )

            missed_text = Text(
                missed,
#                xpos=hmg.MISS_LETTERS_XPOS_START,
#                ypos=hmg.MISS_LETTERS_YPOS_START,
#                xalign=hmg.MISS_LETTERS_XALIGN_START,
#                yalign=hmg.MISS_LETTERS_YALIGN_START,
                font=hmg.WORD_FONT,
                color=hmg.WORD_COLOR,
                size=hmg.WORD_SIZE,
                outlines=hmg.WORD_OUTLINE,
                kerning=hmg.LETTER_SPACE
            )

        # show disables
        show text display_text zorder 10 as hmg_dis_text at hangman_display_word
        show text missed_text zorder 10 as hmg_mis_text at hangman_missed_chars
        $ hm_display = hmg.HM_IMG_NAME + str(chances)
        show expression hm_display zorder 10 as hmg_hanging_man at hangman_hangman

        if chances == 0:
            $ done = True
        elif "_" not in display_word:
            $ done = True
            $ win = True
        else:
            python:

                # input loop
                bad_input = True
                while bad_input:
                    guess = renpy.input(
                        "Guess a letter:",
                        allow="".join(avail_letters),
                        length=1
                    )

                    if len(guess) != 0:
                        bad_input = False
                
                # parse input
                if guess in word:
                    for index in range(0,len(word)):
                        if guess == word[index]:
                            display_word[index] = guess
                else:
                    chances -= 1
                    missed += guess
                    # TODO display hangman adjustment

                # remove letter from being entered agin
                avail_letters.remove(guess)

            # HIDE displayables
            hide text hmg_dis_text
            hide text hmg_mis_text
            hide hmg_hanging_man


    jump hangman_game_loop

# end of game flow
label hangman_game_end:
    m "Some factoids about hangmang"
    return
