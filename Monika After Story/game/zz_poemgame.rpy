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
    # TODO: full description
    #
    # ATTR:
    #   time - TODO   
    #   pos - TODO
    #   offset - TODO
    #   zoom - TODO
    #
    class MASStickerTimePos:
        def __init__(self, time=None, pos=None, offset=None, zoom=None):

            if time:
                self.time = time
            else:
                self.time = renpy.random.random() * 4 + 4

            if pos:
                self.pos = pos
            else:
                self.pos = renpy.random.randint(-1,1)

            if offset:
                self.offset = offset
            else:
                self.offset = 0

            if zoom:
                self.zoom = zoom
            else:
                self.zoom = 1

    # creating the default stickers:
    class MASStickerSayori(MASStickerTimePos):
        def __init__(self):
            MASStickerTimePos.__init__(self)

    class MASStickerNatsuki(MASStickerTimePos):
        def __init__(self):
            MASStickerTimePos.__init__(self)

    class MASStickerYuri(MASStickerTimePos):
        def __init__(self):
            MASStickerTimePos.__init__(self)

    class MASStickerMonika(MASStickerTimePos):
        def __init__(self):
            MASStickerTimePos.__init__(self)

# EXCEPTIONS ------------------------------------------------------------------
    
    # Exception that occurs when Stock Mode is run and monika_
    class OnlyMonikaStockFlowException(Exception):
        def __init__(self):
            self.msg = ("Cannot launch poem game in STOCK_MODE when " +
                "only_monika is True or only_monika_glitch is True")
        def __str__(self):
            return self.msg

# FUNCTIONS -------------------------------------------------------------------

    from mas_poemgame_constants import ODDS_SPACE
    from mas_poemgame_constants import ODDS_OTHER

    def glitchWord(word, odds_space=ODDS_SPACE, odds_other=ODDS_OTHER):
        #
        # Glitches the given word by replacing characters with spaces or
        # other chars
        #
        # IN:
        #   word - the word to glitch
        #   odds_space - the odds that a space will replace a character
        #       Use an int here. Odds are calculated like (1 out of x)
        #       (Default: ODDS_SPACE) - Defined in mas_poemgame_constants
        #   odds_other - the odds that a random unicode character will replace
        #       a character. Use an int here. Odds are calculated the same as
        #       odds_space.
        #       (Default: ODDS_OTHER) - Defined in mas_poemgame_constants
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

# store to handle sticker generation
init -2 python in mas_poemgamestickers:
    import store.mas_poemgame_consts as mas_pg_consts

    # functions
    def generateStickers():
        #
        # Generates a dict of stickers you can use with the poem game.
        # This is so we dont overwrite the defaults
        #
        # RETURNS:
        #   A dict of the following format:
        #       "sayori": MASStickerSayori object
        #       "natsuki": MASStickerNatsuki object
        #       "yuri": MASStickerYuri object
        #       "monika": MASStickerMonika object
        sticker_pos_time = {
            mas_pg_consts.SAYORI: MASStickerSayori(),
            mas_pg_consts.NATSUKI: MASStickerNatsuki(),
            mas_pg_consts.YURI: MASStickerYuri(),
            mas_pg_consts.MONIKA: MASStickerMonika()
        }
        return sticker_pos_time

# store to handle poem-related validations
init -2 python in mas_poemgame_val:
    import store.mas_poemgame_consts as mas_pg_consts
    
    # functions
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
            flow == mas_pg_consts.DISPLAY_MODE 
            or flow == mas_pg_consts.STOCK_MODE
            or flow == mas_pg_consts.MONIKA_MODE
        )


# To complete stop music, set both music params to None
#
# IN:
#   (REQUIRED)
#   flow - what are we trying to do with this minigame. This changes the
#       returned values: 
#
#       (these are from mas_poemgame_constants)
#       DISPLAY_MODE - glitch/display mode. Nothing is returned. 
#
#       STOCK_MODE - stock minigame mode. 
#           If only_winner is True:
#               Returns only the winner and points as Tuple:
#                   [0] -> name of winner (defined in mas_poemgame_constants)
#                   [1] -> pts they won
#           else:
#               Returns the point totals for each character in a dict of the 
#               following format: (keys are defined in mas_poemgame_constants)
#                   "sayori": <pts>
#                   "natsuki": <pts>
#                   "yuri": <pts>
#                   "monika": <pts>
#
#       MONIKA_MODE - poemgame as it was in Act 3. Slightly configurable
#           Nothing is returned.
#
#       TODO: add more flows? when we need them ofc
#
#       NOTE: If the given flow is none of the above, DISPLAY_MODE is assumed
#
#   (CONFIGURATION OPTIONS): (ORDER DOES NOT MATCH INPUT PARAMS)
#
#   glitch_baa - Tuple of the following format:
#           [0] -> True means do the baa glitch, false means no
#               (If None, default True)
#           [1] -> odds that the baa glitch occurs (1 out of x)
#               (If None, default 10)
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
#           [0] -> name of winning girl (defined in mas_poemgame_constants)
#           [1] -> the amount of points this girl received
#       False will return what is described above in flow.
#       (Default: False)
#
#   poem_wordlist - MASPoemWordList of the poemwords to use this game.
#       If None, the default full_wordlist defined in script-poemgame is used.
#       NOTE: If this is None, show_monika is IGNORED. This is to ensure
#       compatibility with the stock PoemWord class
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
#   sticker_pt - a dict of the format described in the generateStickers 
#       function above. If a show_x arg is False, their key:value in this dict
#       will be ignored.
#       If none, the default one from generateStickers is used
#       (Default: None)
#
#   total_words - Number of words that can be picked this game
#       (Default: 20)
#       (Default: None)
#
#   (DISPLAY_MODE OPTIONS)
#   glitch_baa
#   glitch_nb
#   glitch_words
#   glitch_wordscare
#   glitch_wordscare_sound
#   music_filename
#   one_counter
#   poem_wordlist
#   show_monika
#   show_natsuki
#   show_poemhelp
#   show_sayori
#   show_yuri
#   sticker_pt
#   total_words
#
#   (STOCK_MODE OPTIONS)
#   glitch_baa
#   glitch_nb
#   glitch_words
#   glitch_wordscare
#   glitch_wordscare_sound
#   music_filename
#   one_counter
#   only_winner
#   poem_wordlist
#   show_monika
#   show_natsuki
#   show_poemhelp
#   show_sayori
#   show_yuri
#   sticker_pt
#   total_words
#
#   (MONIKA_MODE OPTIONS)
#   glitch_baa
#   glitch_nb
#   glitch_words
#   glitch_wordscare
#   glitch_wordscare_sound
#   music_filename
#   one_counter
#   show_poemhelp
#   sticker_pt
#   total_words
#
label mas_poem_minigame (flow,music_filename=audio.t4,show_monika=True,
        show_natsuki=False,show_sayori=False,show_yuri=False,glitch_nb=False,
        show_poemhelp=False,total_words=20,poem_wordlist=None,sticker_pt=None,
        one_counter=False,only_monika=False,glitch_words=None,
        glitch_wordscare=None,only_winner=False,glitch_baa=None

    $ import store.mas_poemgamestickers as mas_stickers
    $ import store.mas_poemgame_val as mas_validator
    $ import store.mas_poemgame_constants as mas_pg_consts

    # flow validation
    if not mas_validator.validateFlow(flow):
        $ flow = mas_pg_consts.DISPLAY_MODE
    
    # flow bools so we dont have == all the time
    $ in_display_mode = flow == mas_pg_consts.DISPLAY_MODE
    $ in_stock_mode = flow == mas_pg_consts.STOCK_MODE
    $ in_monika_mode = flow == mas_pg_consts.MONIKA_MODE

    # arg processing
    python:
        
        # glitch word processing
        # not None, is length 3, and first item is True
        if (glitch_words is not None
            and len(glitch_words) >= 3 
            and glitch_words[0]):

            if not glitch_words[1]: # None
                glitch_words[1] = mas_pg_consts.ODDS_SPACE
            if not glitch_words[2]: # None
                glitch_words[2] = mas_pg_Consts.ODDS_OTHER

        else: # None, or length < 3, or first item is False
            glitch_words = None

        # glitch word scare processing
        # not None, is length 2, and first item is True
        if (glitch_wordscare is not None
            and len(glitch_wordscare) >= 2 
            and gltich_wordscare[0]):

            if not glitch_wordscare[1]: # None
                glitch_wordscare[1] = mas_pg_consts.ODDS_SCARE

            # stuff glitchword scare handles
            # makes the poem game go into glitch mode (white display)
            poemgame_glitch = False

            # baa checking
            if (glitch_baa is None or (
                len(glitch_baa) >= 2
                and glitch_baa[0])):

                # plays the baa sound which is a glitch sound
                played_baa = False

                if not glitch_baa[1]: # None
                    glitch_baa[1] = mas_pg_consts.ODDS_BAA

            else: # length < 2, or first item is False
                glitch_baa = None

            # glitch_wordscare_sound checking
            if (glitch_wordscare_sound is None or (
                len(glitch_wordscare_sound) >= 2
                and glitch_wordscare_sound[0])):

                if not glitch_wordscare_sound[1]: # None
                    glitch_wordscare_sound[1] = mas_pg_consts.ODDS_GLTICH_SOUND

            else: # length < 2, or first item is False
                glitch_wordscare_sound = None

        else: # None, or length < 2, or first item is False
            glitch_wordscare = None


    # TODO: do we need to paramterize this?
    stop music fadeout 2.0

    # glitch the notebook?
    if glitch_nb:
        scene bg notebook-glitch
    else:
        scene bg notebook

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
            show y_sticker at sticker_midright
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
    if transition:
        with dissolve_scene_full

    # for reference:
    # play music ghostmenu

    # music playing
    if music_obj: # music object is not None
        play music music_obj
    elif music_filename:
        # calling a function from script-ch30
        $ play_song(music_filename)

    # else no music lol

    # lots of skip removal
    $ config.skipping = False
    $ config.allow_skipping = False
    $ allow_skipping = False
    
    # poem help screen
    if show_poemhelp:
        call screen dialog("It's time to write a poem!\n\nPick words you think your favorite club member\nwill like. Something good might happen with\nwhoever likes your poem the most!", ok_action=Return())

    # okay here begins the main flow
    python:

        # current word progress
        progress = 1

        # total number of selections
        numWords = total_words

        # point totals for the girls
        if in_stock_mode:
            points = {
                mas_pg_consts.SAYORI: 0,
                mas_pg_consts.NATSUKI: 0,
                mas_pg_consts.YURI: 0,
                mas_pg_consts.MONIKA: 0
            }
        
        # the list of words
        if not in_monika_mode:
            if poem_wordlist:
                wordlist = list(poem_wordlist.wordlist)
            else:
                pw_list = MASPoemWordList(mas_pg_consts.POEM_FILE)
                wordlist = list(pw_list.wordlist)

        # the following handles the positioning and time between a sticker
        if sticker_pt:
            sticker_pos_time = sticker_pt
        else:
            sticker_pos_time = mas_stickers.generateStickers()

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
                            and random.randint(1,glitch_wordscare[1]) == 1):
                            
                            word = MASPoemWord(glitchtext(7), 0, 0, 0, 0, True)

                        # are we displaying a glitched Monika
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
                        word = random.choice(wordlist)
                        wordlist.remove(word)

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

            if glitch_wordscare and not poemgame_glitch:
                if t.glitch:
                    poemgame_glitch = True
                    renpy.music.play(audio.t4g)
                    renpy.scene()
                    renpy.show("white")
                    renpy.show("y_sticker glitch", at_list=[sticker_glitch])
            elif poemgame_glitch:
                if (not glitch_baa 
                    and not played_baa
                    and random.randint(1, glitch_baa[1]) == 1):
                    renpy.play("gui/sfx/baa.ogg")
                    played_baa = True
                elif (not glitch_wordscare_sound
                    and random.randint(1, glitch_wordscare_sound[1]) == 1):
                    renpy.play(gui.activate_sound_glitch)

           else:

                elif persistent.playthrough != 3:
                    renpy.play(gui.activate_sound)
                    if persistent.playthrough == 0:
                        if t.sPoint >= 3:
                            renpy.show("s_sticker hop")
                        if t.nPoint >= 3:
                            renpy.show("n_sticker hop")
                        if t.yPoint >= 3:
                            renpy.show("y_sticker hop")
                    else:
                        if persistent.playthrough == 2 and chapter == 2 and random.randint(0,10) == 0: renpy.show("m_sticker hop")
                        elif t.nPoint > t.yPoint: renpy.show("n_sticker hop")
                        elif persistent.playthrough == 2 and not persistent.seen_sticker and random.randint(0,100) == 0:
                            renpy.show("y_sticker hopg")
                            persistent.seen_sticker = True
                        elif persistent.playthrough == 2 and chapter == 2: renpy.show("y_sticker_cut hop")
                        else: renpy.show("y_sticker hop")
            else:
                           sPointTotal += t.sPoint
            nPointTotal += t.nPoint
            yPointTotal += t.yPoint
            progress += 1
            if progress > numWords:
                break

        if persistent.playthrough == 0:
            
            if chapter == 1:
                exec(ch1_choice[0] + "PointTotal += 5")
            
            unsorted_pointlist = {"sayori": sPointTotal, "natsuki": nPointTotal, "yuri": yPointTotal}
            pointlist = sorted(unsorted_pointlist, key=unsorted_pointlist.get)
            
            
            poemwinner[chapter] = pointlist[2]
        else:
            if nPointTotal > yPointTotal: poemwinner[chapter] = "natsuki"
            else: poemwinner[chapter] = "yuri"


        exec(poemwinner[chapter][0] + "_appeal += 1")


        if sPointTotal < POEM_DISLIKE_THRESHOLD: s_poemappeal[chapter] = -1
        elif sPointTotal > POEM_LIKE_THRESHOLD: s_poemappeal[chapter] = 1
        if nPointTotal < POEM_DISLIKE_THRESHOLD: n_poemappeal[chapter] = -1
        elif nPointTotal > POEM_LIKE_THRESHOLD: n_poemappeal[chapter] = 1
        if yPointTotal < POEM_DISLIKE_THRESHOLD: y_poemappeal[chapter] = -1
        elif yPointTotal > POEM_LIKE_THRESHOLD: y_poemappeal[chapter] = 1


        exec(poemwinner[chapter][0] + "_poemappeal[chapter] = 1")

    if persistent.playthrough == 2 and persistent.seen_eyes == None and renpy.random.randint(0,5) == 0:
        $ seen_eyes_this_chapter = True
        $ quick_menu = False
        play sound "sfx/eyes.ogg"
        $ persistent.seen_eyes = True
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
    $ config.allow_skipping = True
    $ allow_skipping = True
    stop music fadeout 2.0
    hide screen quick_menu
    show black as fadeout:
        alpha 0
        linear 1.0 alpha 1.0
    pause 1.0
    return

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
