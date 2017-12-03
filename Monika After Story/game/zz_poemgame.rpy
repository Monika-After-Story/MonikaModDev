# Module that contains a modified version of the poem minigame so we can use
# it seamlessly in topics
#

# copied from script-poemgame

# INIT block for poem stuff
init python:
#   import random

    # the PoemWord class.
    # TODO: should we add monika points? hmmmm
    class PoemWord:
        def __init__(self, word, sPoint, nPoint, yPoint, glitch=False):
            self.word = word
            self.sPoint = sPoint
            self.nPoint = nPoint
            self.yPoint = yPoint
            self.glitch = glitch


    # these are the thresholds for liking / disliking a poem
    # NOTE: do we need these?
    POEM_DISLIKE_THRESHOLD = 29
    POEM_LIKE_THRESHOLD = 45

    # generating the word list
    full_wordlist = []
    with renpy.file('poemwords.txt') as wordfile:
        for line in wordfile:

            line = line.strip()

            if line == '' or line[0] == '#': continue


            x = line.split(',')
            full_wordlist.append(PoemWord(x[0], float(x[1]), float(x[2]), float(x[3])))



# To complete stop music, set both music params to None
#
# IN:
#   music_obj - music to play during the mini game (music object, NOT FILENAME)
#       Takes priority over music_filename. Set to None to use music_filename.
#       (default: t4, which is the regular poem minigame song)
#   music_filename - filename of the music to play. Set music to None to use
#       this param. 
#       NOTE: NO checks are made for the existence of this file. Please no
#       bully.
#       (Default: None)
#   show_monika - True will display monika and her related actions. False will
#       not. 
#       (Default: True)
#   show_natsuki - True will display natsuki and her related actions. False 
#       will not.
#       (Default: False)
#   show_sayori - True will display sayori and her related actions. False will
#       not.
#       (Default: False)
#   show_yuri - True will display yuri and her related actions. False will not.
#       (Default: False)
#   glitch_nb - True will use the glitched notebook. False will use regular
#       one.
#       (Default: False)
#   show_poemhelp - True will display the poem help screen. False will not
#       (Default: False)
#   total_words - Number of words that can be picked this game
#       (Default: 20)
label zz_poem_minigame (music_obj=t4,music_filename=None,show_monika=True,
        show_natsuki=False,show_sayori=False,show_yuri=False,glitch_nb=False,
        show_poemhelp=False,total_words=20):

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
        play_song(music_filename)

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

        # makes the poem game go into glitch mode
        poemgame_glitch = False

        # plays the baa sound (which is a glitch thing i think)
        played_baa = False

        # current word progress
        progress = 1

        # total number of selections
        numWords = total_words

        # point totals for the girls
        # TODO: adding monika? this depends on what we want the poem game to
        # do
        sPointTotal = 0
        nPointTotal = 0
        yPointTotal = 0
        
        # the list of words.
        wordlist = list(full_wordlist)

        sayoriTime = renpy.random.random() * 4 + 4
        natsukiTime = renpy.random.random() * 4 + 4
        yuriTime = renpy.random.random() * 4 + 4
        sayoriPos = renpy.random.randint(-1,1)
        natsukiPos = renpy.random.randint(-1,1)
        yuriPos = renpy.random.randint(-1,1)
        sayoriOffset = 0
        natsukiOffset = 0
        yuriOffset = 0
        sayoriZoom = 1
        natsukiZoom = 1
        yuriZoom = 1





        while True:
            ystart = 160
            if persistent.playthrough == 2 and chapter == 2:
                pstring = ""
                for i in range(progress):
                    pstring += "1"
            else:
                pstring = str(progress)
            ui.text(pstring + "/" + str(numWords), style="poemgame_text", xpos=810, ypos=80, color='#000')
            for j in range(2):
                if j == 0: x = 440
                else: x = 680
                ui.vbox()
                for i in range(5):
                    if persistent.playthrough == 3:
                        s = list("Monika")
                        for k in range(6):
                            if random.randint(0, 4) == 0:
                                s[k] = ' '
                            elif random.randint(0, 4) == 0:
                                s[k] = random.choice(nonunicode)
                        word = PoemWord("".join(s), 0, 0, 0, False)
                    elif persistent.playthrough == 2 and not poemgame_glitch and chapter >= 1 and progress < numWords and random.randint(0, 400) == 0:
                        word = PoemWord(glitchtext(80), 0, 0, 0, True)
                    else:
                        word = random.choice(wordlist)
                        wordlist.remove(word)
                    ui.textbutton(word.word, clicked=ui.returns(word), text_style="poemgame_text", xpos=x, ypos=i * 56 + ystart)
                ui.close()
            
            t = ui.interact()
            if not poemgame_glitch:
                if t.glitch:
                    poemgame_glitch = True
                    renpy.music.play(audio.t4g)
                    renpy.scene()
                    renpy.show("white")
                    renpy.show("y_sticker glitch", at_list=[sticker_glitch])
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
                r = random.randint(0, 10)
                if r == 0 and not played_baa:
                    renpy.play("gui/sfx/baa.ogg")
                    played_baa = True
                elif r <= 5: renpy.play(gui.activate_sound_glitch)
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
