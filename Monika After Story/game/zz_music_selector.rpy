# Module that handles the music selection screen
# we start with zz to ensure this loads LAST
#
# NOTE: We added support for custom music.
# To add custom music to your game:
# 1. Ensure that the custom music is of "ogg" file format (with the extension)
# 2. Add a directory "custom_bgm" in your DDLC/ directory.
# 3. Drop your oggs into that directory.
# 4. Start the game

# music inits first, so the screen can be made well
init -1 python in songs:

    # MUSICAL CONSTANTS
    # SONG NAMES
    PIANO_COVER = "Your Reality (Piano Cover)"
    JUST_MONIKA = "Just Monika"
    YOURE_REAL = "Your Reality"
    STILL_LOVE = "I Still Love You"
    MY_FEELS = "My Feelings"
    MY_CONF = "My Confession"
    OKAY_EV_MON = "Okay, Everyone! (Monika)"
    DDLC_MT_80 = "Doki Doki Theme (80s ver.)"
    SAYO_NARA = "Surprise!"
    PLAYWITHME_VAR6 = "Play With Me (Variant 6)"
    KAZOO_COVER = "Your Reality (Kazoo Cover)"
    YR_EUROBEAT = "Your Reality (Eurobeat ver.)"
    NO_SONG = "No Music"

    # SONG FILEPATHS
    FP_PIANO_COVER = "mod_assets/bgm/runereality.ogg"
    FP_JUST_MONIKA = "bgm/m1.ogg"
    FP_YOURE_REAL = "bgm/credits.ogg"
    FP_STILL_LOVE = "bgm/monika-end.ogg"
    FP_MY_FEELS = "<loop 3.172>bgm/9.ogg" 
    FP_MY_CONF =  "<loop 5.861>bgm/10.ogg" 
    FP_OKAY_EV_MON = "<loop 4.444>bgm/5_monika.ogg"
    FP_DDLC_MT_80 = (
        "<loop 17.451 to 119.999>mod_assets/bgm/ddlc_maintheme_80s.ogg"
    )
    FP_SAYO_NARA = "<loop 36.782>bgm/d.ogg"
    FP_PLAYWITHME_VAR6 = "<loop 43.572>bgm/6s.ogg"
    FP_KAZOO_COVER = "mod_assets/bgm/kazoo.ogg"
    FP_YR_EUROBEAT = "<loop 1.414>mod_assets/bgm/eurobeatreality.ogg"
    FP_NO_SONG = None


    # functions
    def adjustVolume(channel="music",up=True):
        #
        # Adjusts the volume of the given channel by the volume bump value
        #
        # IN:
        #   channel - the channel to adjust volume
        #       (DEFAULT: music)
        #   up - True means increase volume, False means decrease
        #       (DEFAULT: True)
        direct = 1
        if not up:
            direct = -1

        # volume checks
        new_vol = getVolume(channel)+(direct*vol_bump)
        if new_vol < 0.0:
            new_vol = 0.0
        elif new_vol > 1.0:
            new_vol = 1.0

        renpy.music.set_volume(new_vol, channel=channel)

    def getVolume(channel):
        #
        # Gets the volume of the given audio channel
        #
        # IN:
        #   channel - the audio channel to get the volume for
        #
        # RETURNS:
        #   The volume of the given audio channel (as a double/float)
        return renpy.audio.audio.get_channel(channel).context.secondary_volume

    def getPlayingMusicName():
        #
        # Gets the name of the currently playing song.
        #
        # IN:
        #   channel - the audio channel to get the playing file
        #
        # RETURNS:
        #   The name of the currently playing song, as defined here in
        #   music_choices, Or None if nothing is currently playing
        #
        # ASSUMES:
        #   music_choices (songs store)
        curr_filename = renpy.music.get_playing()

        # check for brackets (so we can confine the check to filename only)
        if curr_filename:
            bracket_endex = curr_filename.find(">")

            if bracket_endex >= 0:
                curr_filename = curr_filename[bracket_endex:]

            # go through music choices and find the match
            for name,song in music_choices:

                # bracket check
                if song: # None check
                    bracket_endex = song.find(">")

                    if bracket_endex >= 0:
                        check_song = song[bracket_endex:]
                    else:
                        check_song = song
                else:
                    check_song = song

                if curr_filename == check_song:
                    return name
        return None

    def initMusicChoices(sayori=False):
        #
        # Sets up the music choices list
        #
        # IN:
        #   sayori - True if the player name is sayori, which means only
        #       allow Surprise in the player

        global music_choices
        global music_pages
        music_choices = list()
        # SONGS:
        # if you want to add a song, add it to this list as a tuple, where:
        # [0] -> Title of song
        # [1] -> Path to song
        if not sayori:
            music_choices.append((JUST_MONIKA, FP_JUST_MONIKA))
            music_choices.append((YOURE_REAL, FP_YOURE_REAL))

            # Shoutout to Rune0n for this wonderful piano cover!
            music_choices.append((PIANO_COVER, FP_PIANO_COVER))

            # Shoutout to TheAloofPotato for this wonderful eurobeat version!
            music_choices.append((YR_EUROBEAT, FP_YR_EUROBEAT))

            music_choices.append((KAZOO_COVER, FP_KAZOO_COVER))
            music_choices.append((STILL_LOVE, FP_STILL_LOVE))
            music_choices.append((MY_FEELS, FP_MY_FEELS))
            music_choices.append((MY_CONF, FP_MY_CONF))
            music_choices.append((OKAY_EV_MON, FP_OKAY_EV_MON))
            music_choices.append((PLAYWITHME_VAR6, FP_PLAYWITHME_VAR6))

            # BIG SHOUTOUT to HalHarrison for this lovely track!
            music_choices.append((DDLC_MT_80, FP_DDLC_MT_80))

        # sayori only allows this
        music_choices.append((SAYO_NARA, FP_SAYO_NARA))

        # grab custom music
        __scanCustomBGM(music_choices)

        # separte the music choices into pages
        music_pages = __paginate(music_choices)


    def __paginate(music_list):
        """
        Paginates the music list and returns a dict of the pages.

        IN:
            music_list - list of music choice tuples (see initMusicChoices)

        RETURNS:
            dict of music choices, paginated nicely:
            [0]: first page of music
            [1]: next page of music
            ...
            [n]: last page of music
        """
        pages_dict = dict()
        page = 0
        leftovers = music_list
        while len(leftovers) > 0:
            music_page, leftovers = __genPage(leftovers)
            pages_dict[page] = music_page
            page += 1

        return pages_dict

        
    def __genPage(music_list):
        """
        Generates the a page of music choices

        IN:
            music_list - list of music choice tuples (see initMusicChoices)

        RETURNS:
            tuple of the following format:
                [0] - page of the music choices
                [1] - reamining items in the music_list
        """
        return (music_list[:PAGE_LIMIT], music_list[PAGE_LIMIT:])


    def __scanCustomBGM(music_list):
        """
        Scans the custom music directory for custom musics and adds them to
        the given music_list.

        IN/OUT:
            music_list - list of music tuples to append to
        """
        # TODO: make song names / other tags configurable
        import os
        ogg_ext = ".ogg"

        # No custom directory? abort
        if not os.access(custom_music_dir, os.F_OK):
            return

        # get the oggs
        found_files = os.listdir(custom_music_dir)
        found_oggs = [
            ogg_file
            for ogg_file in found_files
            if (
                ogg_file.endswith(ogg_ext) 
                and os.access(custom_music_dir + ogg_file, os.R_OK)
            )
        ]

        if len(found_oggs) == 0:
            # no custom oggs found, please move on
            return

        # otherwise, we got some oggs to add
        for ogg_file in found_oggs:
            music_list.append((
                cleanGUIText(ogg_file[:-(len(ogg_ext))]),
                custom_music_reldir + ogg_file
            ))


    def cleanGUIText(unclean):
        """
        Cleans the given text so its applicable for gui usage

        IN:
            unclean - unclean text

        RETURNS:
            cleaned text
        """
        # bad text to be removed:
        bad_text = ("{", "}", "[", "]")

        # NOTE: for bad text, we just replace with empty
        cleaned_text = unclean
        for bt_el in bad_text:
            cleaned_text = cleaned_text.replace(bt_el, "")

        return cleaned_text


    def isInMusicList(filepath):
        """
        Checks if the a song with the given filepath is in the music choices
        list

        IN:
            filepath - filepath of song to check

        RETURNS:
            True if filepath is in the music_choices list, False otherwise
        """
        for name,fpath in music_choices:
            if filepath == fpath:
                return True

        return False


    # defaults
#    FIRST_PAGE_LIMIT = 10
    PAGE_LIMIT = 10
    current_track = "bgm/m1.ogg"
    selected_track = current_track
    menu_open = False
    enabled = True
    vol_bump = 0.1 # how much to increase volume by

    # contains the song list
    music_choices = list()
    music_pages = dict() # song pages dict

    # custom music directory
    custom_music_dir = "custom_bgm"
    custom_music_reldir = "../" + custom_music_dir + "/"

# some post screen init is setting volume to current settings
init 10 python in songs:

    # for muting
    music_volume = getVolume("music")

# non store post inint stuff
init 10 python:

    # setupthe custom music directory
    store.songs.custom_music_dir = (
        config.basedir + "/" + store.songs.custom_music_dir + "/"
    ).replace("\\", "/")

    if persistent.playername.lower() == "sayori":
        # sayori specific

        # init choices
        store.songs.initMusicChoices(True)

        # setup start songs
        store.songs.current_track = store.songs.FP_SAYO_NARA
        store.songs.selected_track = store.songs.FP_SAYO_NARA
        persistent.current_track = store.songs.FP_SAYO_NARA

    else:
        # non sayori stuff

        # init choices
        store.songs.initMusicChoices(False)

        # double check track existence
        if not store.songs.isInMusicList(persistent.current_track):
            # non existence song becomes No Music
            persistent.current_track = None

        # setup start songs
        store.songs.current_track = persistent.current_track
        store.songs.selected_track = store.songs.current_track



# MUSIC MENU ##################################################################
# This is the music selection menu
###############################################################################

# here we are copying game_menu's layout

#style music_menu_outer_frame is empty
#style music_menu_navigation_frame is empty
#style music_menu_content_frame is empty
#style music_menu_viewport is gui_viewport
#style music_menu_side is gui_side
#style music_menu_scrollbar is gui_vscrollbar

#style music_menu_label is gui_label
#style music_menu_label_text is gui_label_text

#style music_menu_return_button is navigation_button
style music_menu_return_button_text is navigation_button_text
style music_menu_prev_button_text is navigation_button_text:
    min_width 135
    text_align 1.0

style music_menu_outer_frame is game_menu_outer_frame
style music_menu_navigation_frame is game_menu_navigation_frame
style music_menu_content_frame is game_menu_content_frame
style music_menu_viewport is game_menu_viewport
style music_menu_side is game_menu_side
style music_menu_label is game_menu_label
style music_menu_label_text is game_menu_label_text

style music_menu_return_button is return_button:
    xminimum 0
    xmaximum 200
    xfill False

style music_menu_prev_button is return_button:
    xminimum 0
    xmaximum 135
    xfill False

style music_menu_outer_frame:
    background "mod_assets/music_menu.png"

# Music menu 
#
# IN:
#   music_page - current page of music
#   page_num - current page number
#   more_pages - true if there are more pages left
#
screen music_menu(music_page, page_num=0, more_pages=False):
    modal True

    $ import store.songs as songs

    # allows the music menu to quit using hotkey
    key "noshift_M" action Return()
    key "noshift_m" action Return()

    zorder 200

    style_prefix "music_menu"

    frame:
        style "music_menu_outer_frame"

        hbox:

            frame:
                style "music_menu_navigation_frame"

            frame:
                style "music_menu_content_frame"

                transclude

        # this part copied from navigation menu
        vbox:
            style_prefix "navigation"

            xpos gui.navigation_xpos
    #        yalign 0.4
            spacing gui.navigation_spacing

            # wonderful loop so we can dynamically add songs
            for name,song in music_page:
                textbutton _(name) action Return(song)

    vbox:

        yalign 1.0

        hbox:

            # dynamic prevous text, so we can keep button size alignments
            if page_num > 0:
                textbutton _("<<<< Prev"):
                    style "music_menu_prev_button"
                    action Return(page_num - 1)

            else:
                textbutton _( " "):
                    style "music_menu_prev_button"
                    sensitive False

#                if more_pages:
#                    textbutton _(" | "):
#                        xsize 50
#                        text_font "gui/font/Halogen.ttf" 
#                        text_align 0.5
#                        sensitive False

            if more_pages:
                textbutton _("Next >>>>"):
                    style "music_menu_return_button"
                    action Return(page_num + 1)

        textbutton _(songs.NO_SONG): 
            style "music_menu_return_button"
            action Return(songs.NO_SONG)

        # logic to ensure Return works
        if songs.current_track is None:
            $ return_value = songs.NO_SONG
        else:
            $ return_value = songs.current_track

        textbutton _("Return"):
            style "music_menu_return_button"
            action Return(return_value)

    label "Music Menu"

# sets locks and calls hte appropriate screen
label display_music_menu:
    # set var so we can block multiple music menus
    python:
        import store.songs as songs
        songs.menu_open = True
        prev_dialogue = allow_dialogue
        allow_dialogue = False
        song_selected = False
        curr_page = 0

    # loop until we've selected a song
    while not song_selected:

        # setup pages
        $ music_page = songs.music_pages.get(curr_page, None)
            
        if music_page is None:
            # this should never happen. Immediately quit with None
            return songs.NO_SONG

        # otherwise, continue formatting args
        $ next_page = (curr_page + 1) in songs.music_pages

        call screen music_menu(music_page, page_num=curr_page, more_pages=next_page)

        # obtain result
        $ curr_page = _return
        $ song_selected = _return not in songs.music_pages

    $ songs.menu_open = False
    $ allow_dialogue = prev_dialogue
    return _return
