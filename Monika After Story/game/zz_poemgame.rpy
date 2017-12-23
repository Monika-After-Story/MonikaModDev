# Module that contains a modified version of the poem minigame so we can use
# it seamlessly in topics
# prefixed with zz becaues we dependent on script-poemgame.rpy

# copied from script-poemgame

# INIT block for poem stuff
init -4 python:
#   import random

    # the PoemWord class (now with monika)
    #
    # NOTE: We could potentially just inherit the exisiting PoemWord, but
    # doing so means we need to init this file AFTER script-poemgame. That
    # would be disastrous for all script-topics that want to use Poem stuff
    #
    # ATTRIBUTES:
    #   word - the word this PoemWord represents (string)
    #   sPoint - the amount of poitns this gives sayori (int)
    #   nPoint - the amount of points this gives natsuki (int)
    #   yPoint - the amount of points this gives yuri (int)
    #   mPoint - the amount of points this gives monika (int)
    #   glitch - True means this a glitch word, false if not
    #
    class MASPoemWord():
        def __init__(self, word, sPoint, nPoint, yPoint, mPoint, glitch=False):
            self.word = word
            self.sPoint = sPoint
            self.nPoint = nPoint
            self.yPoint = yPoint
            self.mPoint = mPoint
            self.glitch = glitch

    
    # poemword list class. Allows us to dynamically create Poemwords for 
    # the poem minigame
    #
    # ATTIRBUTES:
    #   wordlist - list of PoemWords this contains
    #   wordfile - name/path of file this list is generated from. If None, this
    #       list was not generated from a file.
    #
    class MASPoemWordList:
        def __init__(self, wordfile=None):
            #
            # Contrusctor for PoemWord list
            #
            # If a wordfile is passed in, the file will be read
            self.wordlist = list()
            self.wordfile = wordfile

            if wordfile:
                self.readInFile(wordfile)


        def readInFile(self, wordfile):
            # copied from poemgame (with adjustments)
            #
            # Reads in a file into the wordlist
            #
            # NOTE: On the poemwords file
            #   The file must consist of the following format:
            #       word,#1,#2,#3,#4
            #   WHERE:
            #       word - the word we want in the poem
            #       #1 - the points this word gives to sayori
            #       #2 - the points this word gives to natsuki
            #       #3 - the points this word gives to yuri
            #       #4 - the points this word gives to monika
            #   (LINES that strat with # are ignored)
            #
            # IN:
            #   wordfile - the filename/path of the file to read words
            with renpy.file(wordfile) as words:
                for line in words:
        
                    line = line.strip()

                    if line == '' or line[0] == '#': continue

                    x = line.split(',')
                    self.wordlist.append(
                        MASPoemWord(
                            x[0], 
                            float(x[1]), 
                            float(x[2]), 
                            float(x[3]),
                            float(x[4])
                        )
                    )           

    # Sticker Time and position class
    #
    # the values here control the offsetting posititions and time for random
    # hopping. 
    # NOTE: all the attributes change overtime, so we're not going to use this
    #   class anymore
    #
    # ATTR:
    #   time - time the sitcker will wait and not do anything
    #   pos - starting position of the sticker
    #   offset - amount of offset to move the sticker
    #   zoom - amount of zoom to give to the sticker
    #
#    class MASStickerTimePos:
#        def __init__(self, time=None, pos=None, offset=None, zoom=None):
#
#            if time:
#                self.time = time
#            else:
#                self.time = renpy.random.random() * 4 + 4
#
#            if pos:
#                self.pos = pos
#            else:
#                self.pos = renpy.random.randint(-1,1)
#
#            if offset:
#                self.offset = offset
#            else:
#                self.offset = 0
#
#            if zoom:
#                self.zoom = zoom
#            else:
#                self.zoom = 1
#
    # creating the default stickers:
#    class MASStickerSayori(MASStickerTimePos):
#        def __init__(self):
#            MASStickerTimePos.__init__(self)
#
#    class MASStickerNatsuki(MASStickerTimePos):
#        def __init__(self):
#            MASStickerTimePos.__init__(self)
#
#    class MASStickerYuri(MASStickerTimePos):
#        def __init__(self):
#            MASStickerTimePos.__init__(self)
#
#    class MASStickerMonika(MASStickerTimePos):
#        def __init__(self):
#            MASStickerTimePos.__init__(self)

# EXCEPTIONS ------------------------------------------------------------------
    
    # Exception that occurs when Stock Mode is run and monika_
    class OnlyMonikaStockFlowException(Exception):
        def __init__(self):
            self.msg = ("Cannot launch poem game in STOCK_MODE when " +
                "only_monika is True or only_monika_glitch is True")
        def __str__(self):
            return self.msg

# FUNCTIONS -------------------------------------------------------------------

    from store.mas_poemgame_consts import ODDS_SPACE
    from store.mas_poemgame_consts import ODDS_OTHER

    def glitchWord(word, odds_space=ODDS_SPACE, odds_other=ODDS_OTHER):
        #
        # Glitches the given word by replacing characters with spaces or
        # other chars
        #
        # IN:
        #   word - the word to glitch
        #   odds_space - the odds that a space will replace a character
        #       Use an int here. Odds are calculated like (1 out of x)
        #       (Default: ODDS_SPACE) - Defined in mas_poemgame_consts
        #   odds_other - the odds that a random unicode character will replace
        #       a character. Use an int here. Odds are calculated the same as
        #       odds_space.
        #       (Default: ODDS_OTHER) - Defined in mas_poemgame_consts
        s = list(word)
        for k in range(len(word)):
            if random.randint(1, odds_space) == 1:
                s[k] = ' '
            elif random.randint(1, odds_other) == 1:
                s[k] = random.choice(nonunicode)
        return "".join(s)

# poemgame related cosntants
init -10 python in mas_poemgame_consts:
    
    # girl names
    SAYORI = "sayori"
    NATSUKI = "natsuki"
    YURI = "yuri"
    MONIKA = "monika"

    # these are the thresholds for liking / disliking a poem
    # NOTE: do we need these?
    POEM_DISLIKE_THRESHOLD = 29
    POEM_LIKE_THRESHOLD = 45

    # default filename for poemwords
    POEM_FILE = "poemwords.txt"

    # flow constants
    DISPLAY_MODE = 0
    STOCK_MODE = 1
    MONIKA_MODE = 2

    # glitch words odds
    ODDS_SPACE = 5
    ODDS_OTHER = 5

    # glitch word scare odds
    ODDS_SCARE = 400

    # BAA ssound odds
    ODDS_BAA = 10

    # glitch soudn odds
    ODDS_GLTICH_SOUND = 3

    # yuri odds
    ODDS_YURI_SCARY = 100

    # eyes odds
    ODDS_EYES = 5

# store to handle sticker generation
 # init -2 python in mas_poemgamestickers:
#    import store.mas_poemgame_consts as mas_pg_consts

    # functions
#    def generateStickers():
        #
        # NOTE: not needed for now
        # Generates a dict of stickers you can use with the poem game.
        # This is so we dont overwrite the defaults
        #
        # RETURNS:
        #   A dict of the following format:
        #       "sayori": MASStickerSayori object
        #       "natsuki": MASStickerNatsuki object
        #       "yuri": MASStickerYuri object
        #       "monika": MASStickerMonika object
#        sticker_pos_time = {
#            mas_pg_consts.SAYORI: MASStickerSayori(),
#            mas_pg_consts.NATSUKI: MASStickerNatsuki(),
#            mas_pg_consts.YURI: MASStickerYuri(),
#            mas_pg_consts.MONIKA: MASStickerMonika()
#        }
#        return sticker_pos_time

# store to handle mas_poemgame functions
init -2 python in mas_poemgame_fun:
    import store.mas_poemgame_consts as mas_pgc
    
    # functions
    def getPointValue(condition, point):
        #
        # Returns the point value if the given condition is true, otherwise
        # returns 0
        #
        # IN:
        #   condition - the condition to evaluate
        #   point - the point value to return
        #
        # RETURNS: the point value if condition is True, 0 otherwise

        if condition:
            return point

        return 0

    def getWinner(word, sayori, natsuki, yuri, monika, mas=False):
        #
        # Checks the given PoemWord (or MASPoemWord) and returns the winner
        # The value returned is a constant in mas_poemgame_consts
        #
        # IN:
        #   word - the PoemWord (or MASPoemWord) to check
        #   sayori - True means sayori is visible, False means she is not
        #   natsuki - True means natsuki is visible, False means she is not
        #   yuri - True means yuri is visible, False means she is not
        #   monika - True means monika is visible, False means she is not
        #   mas - True means we are checking a MASPoemWord, False means a
        #       regular PoemWord
        #       (Default: False)
        #
        # RETURNS: The girl with the highest score, as a constnat defined in
        #   mas_poemgame_consts

        # build a list of point values
        girl_points = list()

        # we want monika to be in there first, because she has tiebreaker
        # rules
        if mas:
            girl_points.append(
                (mas_pgc.MONIKA, getPointValue(monika, word.mPoint))
            )

        # add the rest of the girls
        girl_points.append(
            (mas_pgc.SAYORI, getPointValue(sayori, word.sPoint))
        )
        girl_points.append(
            (mas_pgc.NATSUKI, getPointValue(natsuki, word.nPoint))
        )
        girl_points.append(
            (mas_pgc.YURI, getPointValue(yuri, word.yPoint))
        )

        # now get the largest from this list
        largest = 0
        largestValue = girl_points[largest][1]
        for index in range(1,len(girl_points)):
            if girl_points[index][1] > largestValue:
                largestValue = girl_points[index][1]
                largest = index

        # return our result
        return girl_points[largest][0]

    def validateFlow(flow):
        #
        # Validates the given flow if it is appropriate for the poemgame
        #
        # IN:
        #   flow - flow to validate
        #
        # RETURNS:
        #   True if flow is valid, false if not
        return (
            flow == mas_pgc.DISPLAY_MODE 
            or flow == mas_pgc.STOCK_MODE
            or flow == mas_pgc.MONIKA_MODE
        )


### BEGIN POEMGAME CALLS ======================================================
#
# Since the configurable poemgame call (mas_poem_minigame) is insanely 
# complex, I've added special wrapper labels that take of care the 3 major
# poemgame configurations: (Act 1, Act 2, Act 3)
#
# These wrappers are slightly configurable, but the overall flow of them
# is locked to what they were in stock game.
#
# NOTE: READ THE DOCUMENTATION. There's a ton of options here and whatever
#   you want to do is probably adjustable via a param. 
#
# NOTE: If you don't like passing in 2000 keyword arguments, learn a little
#   more python and call the label using the renpy/python equivalent and
#   **kwargs
#
# NOTE: If you find some issues with this/configurabilty that is missing and
#   you have a good reason it should be added, please contact me, ThePotatoGuy.
#   You can find me on the Monika After Story discord. Or email me via the
#   email I have on github.
#

# ACT 1 ------------------
# silghty configrable poemgame call using mostly ACT 1 params.
# 
# IN:
# NOTE: SEE mas_poem_minigame documentation for full descriptions of the params
#   gather_words - (Default: False)
#   music_filename - (Default: audio.t4 - the default poem game audio)
#   only_winner - (Default: False)
#   poem_wordlist - (Default: None)
#   sel_sound - (Default: gui.activate_sound)
#   show_monika - (Default: False)
#   show_natsuki - (Default: True)
#   show_poemhelp - (Default: True)
#   show_sayori - (Default: True)
#   show_yuri - (Default: True)
#   total_words - (Default: 20)
#
# OUT:
#   See mas_poem_minigame -> STOCK_MODE documentation
#
label mas_poem_minigame_actone(gather_words=False,music_filename=audio.t4,
        only_winner=False,poem_wordlist=None,sel_sound=gui.activate_sound,
        show_monika=False,show_natsuki=True,show_poemhelp=True,
        show_sayori=True,show_yuri=True,total_words=20):
    $ from store.mas_poemgame_consts import STOCK_MODE
    call mas_poem_minigame(STOCK_MODE,music_filename=music_filename,show_monika=show_monika,show_natsuki=show_natsuki,show_sayori=show_sayori,show_yuri=show_yuri,show_poemhelp=show_poemhelp,total_words=total_words,poem_wordlist=poem_wordlist,only_winner=only_winner,gather_words=gather_words,sel_sound=sel_sound) from _call_poem_minigame_actone
    return _return

# THE BIG ONE ------------
# completely configurable poemgame call.
# NOTE: well, almost configurable
# NOTE: disables skipping 
# NOTE: spaceroom is replaced. You will need to call spaceroom after this
#
# IN:
#   (REQUIRED)
#   flow - what are we trying to do with this minigame. This changes the
#       returned values: 
#
#       (these are from mas_poemgame_consts)
#       DISPLAY_MODE - glitch/display mode.
#           If gather_words is True:
#               Returns list of words selected
#           else:
#               Nothing
#
#       STOCK_MODE - stock minigame mode. 
#           If only_winner is True:
#               Returns only the winner and points as Tuple:
#                   [0] -> name of winner (defined in mas_poemgame_consts)
#                   [1] -> pts they won
#               If gather_words is True:
#                   [2] -> list of words selected
#           else:
#               Returns the point totals for each character in a dict of the 
#               following format: (keys are defined in mas_poemgame_consts)
#                   "sayori": <pts>
#                   "natsuki": <pts>
#                   "yuri": <pts>
#                   "monika": <pts>
#               If gather _words is True:
#                   "words": list of words selected
#
#       MONIKA_MODE - poemgame as it was in Act 3. Slightly configurable
#           If gather_words is True:
#               Returns list of words selected
#           else:
#               Nothing
#
#       TODO: add more flows? when we need them ofc
#
#       NOTE: If the given flow is none of the above, DISPLAY_MODE is assumed
#
#   (CONFIGURATION OPTIONS): (ORDER DOES NOT MATCH INPUT PARAMS)
#
#   gather_words - True will include a list of the selected words in the 
#       return, False will not
#       NOTE: The types of objects in this list may be different:
#           If we are in monika_mode, then this will be a list of 
#               MASPoemWord objects
#           If poem_wordlist is not given, then this will be a list of
#               PoemWord objects
#           If poem_wordlist is given, then this will be a list of 
#               MASPoemWord Objects
#       NOTE: The returned objects are deepcopied
#       (Default: False)
#
#   glitch_baa - Tuple of the following format:
#           [0] -> True means do the baa glitch, false means no
#               (If None, default True)
#           [1] -> odds that the baa glitch occurs (1 out of x)
#               (If None, default 10)
#           [2] -> True means play the baa glitch more than once, False means
#               only once
#               (If None, default False)
#       If the tuple is None (or is not of length 2), the default values are
#       used.
#       NOTE: Only is active if glitch_wordscare is used.
#       (Default: None)
#
#   glitch_nb - True will use the glitched notebook. False will use regular
#       one.
#       (Default: False)   
#
#   glitch_words - Tuple of the following format:
#           [0] -> True means display gltich words, false means no
#               (If None, default False)
#           [1] -> odds that a space appears instead of a letter (1 out of x)
#               (If None, default is in glitchWord())
#           [2] -> odds that a nonunicode appears instead of a letter (1 out 
#               of x)
#               (If None, default is in glitchWord())
#       If the tuple is None (or is not of length 3), the default values are
#       used. (SEE glitchWord())
#       NOTE: This effect is purely visible. If you want the glitchable words
#       that cause the scare, use glitch_wordscare
#       (Default: None)
#
#   glitch_wordscare - Tuple of the following format:
#           [0] -> True means display glitch words that cause the scare
#               (If None, default False)
#           [1] -> odds that one of these glitch words will appear (1 out of x)
#               (If None, default is 400)
#       If the tuple is None (or is not of length 2), the default values are
#       used.
#       NOTE: This is the glitch that causes a scare. If you want purely
#       visisble glitch words, use glitch_words
#       (Default: None)
#
#   glitch_wordscare_sound - Tuple of the following format:
#           [0] -> True means play the glitch sound if a glictch word was
#               clicked, False will not
#               (If None, default True)
#           [1] -> odds that a glitch sound will play (1 out of x)
#               NOTE: these odds are applied after glitch_baa, if that is True
#               (If None, default 3)
#       If the tuple is None (or is not of length 2), the deafult vlaues are
#       used.
#       NOTE: Only active if glitch_wordscare is used.
#       (Default: None)
#
#   hop_monika - True means monika will hop when a word is selected in monika
#       mode. False will not
#       NOTE: Only applies to Monika mode hopping
#       (Default: False)
#
#   music_filename - filename of the music to play. Set music to None to use
#       this param. 
#       NOTE: NO checks are made for the existence of this file. Please no
#       bully.
#       (Default: audio.t4 - the defualt poem game audio)
#
#   one_counter - True will apply the glitch that made the poem counter 
#       display 1 over and over again instead of the approriate number. False
#       will do regular counting
#       (Default: False)
#
#   only_winner - True will the return value of STOCK_MODE the following tuple:
#           [0] -> name of winning girl (defined in mas_poemgame_consts)
#           [1] -> the amount of points this girl received
#       False will return what is described above in flow.
#       (Default: False)
#
#   poem_wordlist - MASPoemWordList of the poemwords to use this game.
#       If None, the default full_wordlist defined in script-poemgame is used.
#       NOTE: If this is None, show_monika is IGNORED. This is to ensure
#       compatibility with the stock PoemWord class
#
#   sel_sound - Filename of the sound to play when a word is selected
#       (Default: gui.activate_sound)
#
#   show_eyes - Tuple of the following format:
#           [0] -> True displays the eyes glitch, False does not
#               (Default: False)
#           [1] -> odds that the eyes glitch appears (1 out of x)
#               (Default: 5)
#       If Tuple is None (or not of length 2), the default values are used
#       (Default: None)
#
#   show_monika - True will display monika and her related actions. False will
#       not. 
#       (Default: True)
#
#   show_natsuki - True will display natsuki and her related actions. False 
#       will not.
#       (Default: False)
#
#   show_poemhelp - True will display the poem help screen. False will not
#       (Default: False)
#
#   show_sayori - True will display sayori and her related actions. False will
#       not.
#       (Default: False)
#
#   show_yuri - True will display yuri and her related actions. False will not.
#       (Default: False)
#
#   show_yuri_cut - True will display a cut yuri instead of regular yuri,
#       False will not.
#       NOTE: show_yuri must be true for this to work
#       NOTE: show_yuri_scary takes precendence over this
#       (Defualt: False)
#
#   show_yuri_scary - Tuple of the following format:
#           [0] -> True will show the scary yuri sticker, False will not
#               (If none, Default False)
#           [1] -> odds that the scary yuri sticker should show up (1 out of x)
#               (If None, Default 100)
#           [2] -> True means show the sticker more than once, False means
#               only once
#               (If None, Default Flase)
#       If the tuple is None (or not of length 3), the default values are used
#       NOTE: If this set to show all the time, it takes precendence over 
#           show_yuri_cut
#       NOTE: Only active if show_yuri is True
#       (Default: None)
#
#   total_words - Number of words that can be picked this game
#       (Default: 20)
#
#   (DISPLAY_MODE OPTIONS)
#   gather_words
#   glitch_baa
#   glitch_nb
#   glitch_words
#   glitch_wordscare
#   glitch_wordscare_sound
#   music_filename
#   one_counter
#   poem_wordlist
#   sel_sound
#   show_eyes
#   show_monika
#   show_natsuki
#   show_poemhelp
#   show_sayori
#   show_yuri
#   show_yuri_cut
#   show_yuri_scary
#   total_words
#
#   (STOCK_MODE OPTIONS)
#   gather_words
#   glitch_baa
#   glitch_nb
#   glitch_words
#   glitch_wordscare
#   glitch_wordscare_sound
#   music_filename
#   one_counter
#   only_winner
#   poem_wordlist
#   sel_sound
#   show_eyes
#   show_monika
#   show_natsuki
#   show_poemhelp
#   show_sayori
#   show_yuri
#   show_yuri_cut
#   show_yuri_scary
#   total_words
#
#   (MONIKA_MODE OPTIONS)
#   gather_words
#   glitch_baa
#   glitch_nb
#   glitch_words
#   glitch_wordscare
#   glitch_wordscare_sound
#   hop_monika
#   music_filename
#   one_counter
#   sel_sound
#   show_eyes
#   show_poemhelp
#   total_words
#
# OUT:
#   DISPLAY_MODE:
#       If gather_words is True:
#           Returns of list of words selected
#       else:
#           None
#
#   STOCK_MODE:
#       If only_winner is True:
#           Returns only the winner and points as Tuple:
#               [0] -> name of winner (defined in mas_poemgame_consts)
#               [1] -> pts they won
#           If gather_words is True:
#               [2] -> list of words selected
#       else:
#           Returns the point toals for each character in a dict of the
#           following format: (keys are defined in mas_poemgame_consts)
#               "sayori": <pts>
#               "natsuki": <pts>
#               "yuri": <pts>
#               "monika": <pts>
#           If gather_words is True:
#               "words": list of words selected
#
#   MONIKA_MODE:
#       If gather_words is True:
#           Returns list of words selected
#       else:
#           None
#
label mas_poem_minigame (flow,music_filename=audio.t4,show_monika=True,
        show_natsuki=False,show_sayori=False,show_yuri=False,glitch_nb=False,
        show_poemhelp=False,total_words=20,poem_wordlist=None,
        one_counter=False,only_monika=False,glitch_words=None,
        glitch_wordscare=None,only_winner=False,glitch_baa=None,
        gather_words=False,sel_sound=gui.activate_sound,hop_monika=False,
        show_yuri_cut=False,show_yuri_scary=None,show_eyes=None):

#    $ import store.mas_poemgamestickers as mas_stickers
    $ import store.mas_poemgame_fun as mas_fun
    $ import store.mas_poemgame_consts as mas_pgc

    # flow validation
    if not mas_fun.validateFlow(flow):
        $ flow = mas_pgc.DISPLAY_MODE
    
    # flow bools so we dont have == all the time
    $ in_display_mode = flow == mas_pgc.DISPLAY_MODE
    $ in_stock_mode = flow == mas_pgc.STOCK_MODE
    $ in_monika_mode = flow == mas_pgc.MONIKA_MODE

    # arg processing
    python:
        
        # glitch word processing
        # not None, is length 3, and first item is True
        if (glitch_words is not None
            and len(glitch_words) >= 3 
            and glitch_words[0]):

            # SPACE odds
            glitch_words_alspace = False
            if not glitch_words[1]: # None
                glitch_words[1] = mas_pgc.ODDS_SPACE
            elif glitch_Words[1] == 1: # 1 out of 1 odds means always
                glitch_words_alspace = True

            # other char odds
            glitch_words_alother = False
            if not glitch_words[2]: # None
                glitch_words[2] = mas_pg_Consts.ODDS_OTHER
            elif glitch_words[2] == 1: # 1 out of 1 odds means always
                glitch_words_alother = True

        else: # None, or length < 3, or first item is False
            glitch_words = None

        # glitch word scare processing
        # not None, is length 2, and first item is True
        if (glitch_wordscare is not None
            and len(glitch_wordscare) >= 2 
            and gltich_wordscare[0]):

            # sound wordscare glitch odds
            glitch_wordscare_alscare = False
            if not glitch_wordscare[1]: # None
                glitch_wordscare[1] = mas_pgc.ODDS_SCARE
            elif glitch_wordscare[1] == 1: # 1 / 1 odds
                glitch_wordscare_alscare = True

            # baa checking
            if (glitch_baa is None or (
                len(glitch_baa) >= 3
                and glitch_baa[0])):

                # plays the baa sound which is a glitch sound
                played_baa = False

                glitch_baa_albaa = False
                if not glitch_baa[1]: # None
                    glitch_baa[1] = mas_pgc.ODDS_BAA
                if glitch_baa[2] is None: # None
                    glitch_baa[2] = False

                # baa odds check
                if glitch_baa[1] == 1:
                    glitch_baa_albaa = True

            else: # length < 2, or first item is False
                glitch_baa = None

            # glitch_wordscare_sound checking
            if (glitch_wordscare_sound is not None
                and len(glitch_wordscare_sound) >= 2
                and glitch_wordscare_sound[0]):

                glitch_wordscare_alsound = False
                if not glitch_wordscare_sound[1]: # None
                    glitch_wordscare_sound[1] = mas_pgc.ODDS_GLTICH_SOUND

                # sound odds check
                if glitch_wordscare_sound[1] == 1:
                    glitch_wordscare_alsound = True

            else: # length < 2, or first item is False
                glitch_wordscare_sound = None

        else: # None, or length < 2, or first item is False
            glitch_wordscare = None

        # gather words processing
        if gather_words:
            from copy import deepcopy
            selected_words = list()

        # scary yuri processing
        if show_yuri:
            if (
                show_yuri_scary is not None
                and len(show_yuri_scary) >= 3
                and show_yuri_scary[0]
            ):
    
                # seen yuri scary
                seen_yuri_scary = False

                show_yuri_alscary = False 
                if not show_yuri_scary[1]: # None
                    show_yuri_scary[1] = mas_pgc.ODDS_YURI_SCARY
                if show_yuri_scary[2] is None: # None
                    show_yuri_scary[2] = False

                # odds check
                if show_yuri_scary[1] == 1:
                    show_yuri_alscary = True

            else: # show yuri scary nope
                show_yuri_scary = None

        # show_yuri is False
        else:
            show_yuri_scary = None
            show_yuri_cut = False

        # eyes processing
        if (show_eyes 
                and len(show_eyes) >= 2
                and show_eyes[0]):

            if not show_eyes[1]: # None
                show_eyes[1] = mas_pgc.ODDS_EYES

        # no show eyes
        else:
            show_eyes = None
 
    # glitch the notebook?
    if glitch_nb:
        scene bg notebook-glitch
    else:
        scene bg notebook

    #

    # bottom quick menu. atm, we probably dont need this
    # show screen quick_menu
    
    # sticker positions. Our order is as followS:
    # sayori, natsuki, yuri, monika
    if in_monika_mode:
        show m_sticker at sticker_right
    else:
        if show_sayori:
            show s_sticker at sticker_left
        if show_natsuki:
            show n_sticker at sticker_midleft
        if show_yuri:
            if show_yuri_cut:
                show y_sticker_cut at sticker_midright
                $ yuristicker = "y_sticker_cut"
            else:
                show y_sticker at sticker_midright
                $ yuristicker = "y_sticker"
        if show_monika:
            show m_sticker at sticker_right

# in case we want to reference the older sticker positions:
#    else:
#        if persistent.playthrough == 0:
#            show s_sticker at sticker_left
#        show n_sticker at sticker_mid
#        if persistent.playthrough == 2 and chapter == 2:
#            show y_sticker_cut at sticker_right
#        else:
#            show y_sticker at sticker_right
#        if persistent.playthrough == 2 and chapter == 2:
#            show m_sticker at sticker_m_glitch

    # the scene transition
    # TODO: do we need to parameterize this?
#    if transition:
#        with dissolve_scene_full

    # for reference:
    # play music ghostmenu

    # TODO: do we need to paramterize this?
    stop music fadeout 2.0

    # music playing
    if music_filename:
        # calling a function from script-ch30
        $ play_song(music_filename)

    # else no music lol

    # lots of skip removal
#    $ config.skipping = False
#    $ config.allow_skipping = False
#    $ allow_skipping = False
    
    # poem help screen
    if show_poemhelp:
        call screen dialog("It's time to write a poem!\n\nPick words you think your favorite club member\nwill like. Something good might happen with\nwhoever likes your poem the most!", ok_action=Return())

    # okay here begins the main flow
    python:

        # stuff glitchword scare handles
        # makes the poem game go into glitch mode (white display)
        poemgame_glitch = False

        # current word progress
        progress = 1

        # total number of selections
        numWords = total_words

        # point totals for the girls
        if in_stock_mode:
            points = {
                mas_pgc.SAYORI: 0,
                mas_pgc.NATSUKI: 0,
                mas_pgc.YURI: 0,
                mas_pgc.MONIKA: 0
            }
        
        # the list of words
        if not in_monika_mode:
            from copy import deepcopy
            if poem_wordlist:
                wordlist = deepcopy(poem_wordlist.wordlist)
            else:
                #pw_list = MASPoemWordList(mas_pgc.POEM_FILE)
                #wordlist = list(pw_list.wordlist)
                show_monika = False
                wordlist = deepcopy(full_wordlist)

        # the following handles the positioning and time between a sticker
#        if sticker_pt:
#            sticker_pos_time = sticker_pt
#        else:
#            sticker_pos_time = mas_stickers.generateStickers()

        # as always, have loop controllers
        done = False
        while not done:
            ystart = 160

            # word counter setup
            if one_counter:
                pstring = ""
                for i in range(progress):
                    pstring += "1"
            else:
                pstring = str(progress)

            # word counter display
            ui.text(
                pstring + "/" + str(numWords), 
                style="poemgame_text", 
                xpos=810, 
                ypos=80, 
                color='#000'
            )

            # word display
            for j in range(2):  # columns
                if j == 0: x = 440
                else: x = 680
                ui.vbox()
                for i in range(5): # rows

                    # monika mode:
                    if in_monika_mode:

                        # are we displaying a word that causes glitch scare?
                        if (glitch_wordscare 
                            and (
                                glitch_wordscare_alscare or
                                random.randint(1,glitch_wordscare[1]) == 1
                            )):
                            
                            word = MASPoemWord(glitchtext(7), 0, 0, 0, 0, True)

                        # are we displaying a glitched Monika word
                        elif glitch_words:
                            word = MASPoemWord(
                                glitchWord(
                                    "Monika", glitch_words[1], glitch_words[2]
                                ),
                                0, 0, 0, 0, False
                            )

                        # regular Monika
                        else:
                            word = MASPoemWord("Monika", 0, 0, 0, 0, False)

                    # display or stock mode
                    else:

                        # pick a word yo
                        word = random.choice(wordlist)
                        wordlist.remove(word)

                        # wordscare mode
                        if (glitch_wordscare
                            and ( # again odds,
                                glitch_wordscare_alscare or
                                random.randint(1,glitch_wordscare[1]) == 1
                            )):

                            word.word = glitchtext(len(word.word))
                            word.glitch = True

                        # glitchy words (visual)
                        elif glitch_words:
                            word.word = glitchWord(
                                word.word, glitch_words[1], glitch_words[2]
                            )

                    # display the word as a textbutton
                    ui.textbutton(
                        word.word, 
                        clicked=ui.returns(word), 
                        text_style="poemgame_text", 
                        xpos=x, 
                        ypos=i * 56 + ystart
                    )

                # close this ui i guess
                ui.close()
            
            # wait for user to hit a word
            t = ui.interact()

            # get the word if we need to
            if gather_words:
                selected_words.append(deepcopy(t))

            # wordscare glitch
            if glitch_wordscare:

                # poemgame_glitch mode check
                if not poemgame_glitch:
                    # then check this word is a glitch word
                    if t.glitch:
                        poemgame_glitch = True
                        renpy.music.play(audio.t4g)
                        renpy.scene()
                        renpy.show("white")
                        renpy.show("y_sticker glitch", at_list=[sticker_glitch])

                # we've been glitched!
                elif poemgame_glitch:
                    if (not glitch_baa 
                        and (glitch_baa[2] or not played_baa)
                        and (
                            glitch_wordscare_albaa 
                            or random.randint(1, glitch_baa[1]) == 1
                        )):

                        renpy.play("gui/sfx/baa.ogg")
                        played_baa = True

                    elif (not glitch_wordscare_sound
                        and (
                            glitch_wordscare_alsound
                            or random.randint(
                                1, glitch_wordscare_sound[1]
                            ) == 1
                        )):

                        renpy.play(gui.activate_sound_glitch)
            
            # do sticker hopping!
            else:
                if sel_sound:
                    renpy.play(sel_sound)

                # check for mode
                if in_monika_mode and hop_monika:
                    # monika mode only has monika
                    renpy.show("m_sticker hop")
                else:
                    word_winner = mas_fun.getWinner(
                        t,
                        show_sayori,
                        show_natsuki,
                        show_yuri,
                        show_monika,
                        mas=poem_wordlist is not None
                    )

                    if show_monika and word_winner == mas_pgc.MONIKA:
                        renpy.show("m_sticker hop")
                    elif show_sayori and word_winner == mas_pgc.SAYORI:
                        renpy.show("s_sticker hop")
                    elif show_natsuki and word_winner == mas_pgc.NATSUKI:
                        renpy.show("n_sticker hop")
                    #elif show_yuri and word_winner == mas_pgc.YURI:
                    elif show_yuri:

                        if (show_yuri_scary and (
                                (
                                    show_yuri_scary[2] 
                                    or not seen_yuri_scary
                                )
                                and (
                                    show_yuri_alscary
                                    or random.randint(
                                        1, show_yuri_scary[1]
                                    ) == 1
                                ))):
                            renpy.show(yuristicker + " hopg")
                       
                        # either regular yuri or cut yuri
                        else:
                            renpy.show(yuristicker + " hop")

            # now time to calculate points (if needed)
            if in_stock_mode:
                if show_sayori:
                    points[mas_pgc.SAYORI] += t.sPoint
                if show_natsuki:
                    points[mas_pgc.NATSUKI] += t.nPoint
                if show_yuri:
                    points[mas_pgc.YURI] += t.yPoint
                if show_monika:
                    points[mas_pgc.MONIKA] += t.mPoint

            # progress check
            progress += 1
            if progress > numWords:
                done = False

        # if we only want the winner (and we in stock mode)
        results = None
        if in_stock_mode:
           
            # only winner mode means that we only wnat he winner
            if only_winner:

                # figure out the winner
                largest = ""
                largestVal = 0
                for girl,points in points.iteritems():
                    if points > largestVal:
                        largest = girl
                        largestVal = points
                
                # do we want the words we selected
                if gather_words:
                    results = (largest, largestVal, selected_words)
                else:
                    results = (largest, largestVal)

            else: # we want everyone ya know

                if gather_words:
                    results = points
                    results["words"] = selected_words

                else:
                    results = points

        # either display mode or monika mode
        else:
            if gather_words:
                results = selected_words

    # show eyes?
    if show_eyes and renpy.random.randint(0,show_eyes[1]) == 1:
        $ quick_menu = False
        play sound "sfx/eyes.ogg"
        stop music
        scene black with None
        show bg eyes_move
        pause 1.2
        hide bg eyes_move
        show bg eyes
        pause 0.5
        hide bg eyes
        show bg eyes_move
        pause 1.25
        hide bg eyes with None
        $ quick_menu = True

#    $ config.allow_skipping = True
#    $ allow_skipping = True

    # post cleanup
    stop music fadeout 2.0
    hide screen quick_menu
    show black as fadeout:
        alpha 0
        linear 1.0 alpha 1.0
    pause 1.0
    return results

###############################################################################
# graphical adjustments
###############################################################################

# left most sticker
transform sticker_left:
    xcenter 70 yalign 0.9 subpixel True

# mid left sticker
transform sticker_midleft:
    xcenter 160  yalign 0.9 subpixel True

# mid right sticker
transform sticker_midright:
    xcenter 250 yalign 0.9 subpixel True

# right sticker
transform sticker_right:
    xcenter 340 yalign 0.9 subpixel True

# we need a special scary yuri hop incase we want to remain cut
image y_sticker_cut hopg:
    "gui/poemgame/y_sticker_2g.png"
    xoffset yuriOffset xzoom yuriZoom
    sticker_hop
    xoffset 0 xzoom 1
    "y_sticker_cut"
