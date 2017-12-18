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
    xcenter 975 ypos 100 alpha 0.7

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

init -1 python:
    
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
    WORD_XPOS_START = 760
    WORD_YPOS_START = 210

    # spacing between rendered letters
    LETTER_SPACE = 10.0

    # word properties
    WORD_FONT = "gui/font/Halogen.ttf"
    WORD_SIZE = 30
    WORD_OUTLINE = []
    WORD_COLOR = "#fff"

    # other props
    MISS_LABEL_XPOS_START = 190
    MISS_LABEL_YPOS_START = -530
    MISS_LETTERS_XPOS_START = 260
    MISS_LETTERS_YPOS_START = -460

# post processing
init 10 python:
    from store.hangman import hm_words, all_hm_words
    with renpy.file("poemwords.txt") as words:
        for line in words:

            line = line.strip()

            if len(line) != 0 and line[0] != "#":
                hm_words.append(line.split(",")[0])
    all_hm_words = list(hm_words)

# entry point for the hangman game
label hangman_game_start:
    $ import store.hangman as hmg
    m "You want to play Hangman? Okay!"
    # setup positions
    show monika at hangman_monika
    show hm_frame at hangman_board zorder 5

    python:
        # setup constant displayabels
        missed_label = Text(
            "Missed:", 
            xpos=hmg.MISS_LABEL_XPOS_START,
            ypos=hmg.MISS_LABEL_YPOS_START,
            font=hmg.WORD_FONT,
            color=hmg.WORD_COLOR,
            size=hmg.WORD_SIZE,
            outlines=hmg.WORD_OUTLINE
        )

    # show missed label 
    show text missed_label zorder 10 as mis_label
    
    # FALL THROUGH TO NEXT LABEL

# looping location for the hangman game
label hangman_game_loop:
    m "I'll think of a word"
    pause 1
   
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
                xpos=hmg.WORD_XPOS_START,
                ypos=hmg.WORD_YPOS_START,
                font=hmg.WORD_FONT,
                color=hmg.WORD_COLOR,
                size=hmg.WORD_SIZE,
                outlines=hmg.WORD_OUTLINE,
                kerning=hmg.LETTER_SPACE
            )

            missed_text = Text(
                missed,
                xpos=hmg.MISS_LETTERS_XPOS_START,
                ypos=hmg.MISS_LETTERS_YPOS_START,
                font=hmg.WORD_FONT,
                color=hmg.WORD_COLOR,
                size=hmg.WORD_SIZE,
                outlines=hmg.WORD_OUTLINE,
                kerning=hmg.LETTER_SPACE
            )

        show text display_text zorder 10 as dis_text
        show text missed_text zorder 10 as mis_text

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

            # HIDE all text for next round
            hide text dis_text
            hide text mis_text



    jump hangman_game_loop

