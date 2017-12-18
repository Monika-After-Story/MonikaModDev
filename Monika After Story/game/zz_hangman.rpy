# Module that does hangman man
#

# IMAGES-----------
image hm_head = "mod_assets/hangman/hm_head.png"
image hm_leftarm = "mod_assets/hangman/hm_leftarm.png"
image hm_rightarm = "mod_assets/hangman/hm_rightarm.png"
image hm_leftleg = "mod_assets/hangman/hm_leftleg.png"
image hm_rightleg = "mod_assets/hangman/hm_rightleg.png"
image hm_torso = "mod_assets/hangman/hm_torso.png"

init -1 python:
    
    # defining a class to contain a hangman letter
    #
    # PROPERTIES:
    #   letter - the letter this letter represents
    #   xpos - the xposition of this letter
    #   ypos - the y position of this letter
    #   visible - True means show the letter, False will show a blank (_)
    class MASHangmanLetter():
        def __init__(self, letter, xpos, ypos):
            self.letter = letter
            self.xpos = xpos
            self.ypos = ypos
            self.visible = False

init -1 python in hangman:
    # preprocessing
    # get poemwords as hangman words
    hm_words = list()

    # we need a copy of the full wordlist
    all_hm_words = list()

# post processing
init 10 python:
    from store.hangman import hm_words, all_hm_words
    with renpy.file("poemwords.txt") as words:
        for line in wordfile:

            line = line.strip()

            if len(line) != 0 and line[0] != "#":
                hm_words.append(line.split(",")[0])
    all_hm_words = list(hm_words)

# entry point for the hangman game
label hangman_game_start:
    $ from store.hangman import hm_words, all_hm_words
    m "You want to play Hangman? Okay!"

# looping location for the hangman game
label hangman_game_loop:
    m "I'll think of a word"
    pause 2
   
    python:
        # refill the list if empty
        if len(hm_words) == 0:
            hm_words = list(all_hm_wordS)

        # randomly pick word
        word = renpy.random.choice(hm_words)
        
        # turn the word into hangmang letters
        hm_letters = list()
#       for letter in word:
#           hm_letters.append(
        

    m "Alright, I've got one"

 #  python:
        
