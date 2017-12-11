# Module that handles the music selection screen
# we start with zz to ensure this loads LAST
#

# music inits first, so the screen can be made well
init -1 python in songs:

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
        bracket_endex = curr_filename.find(">")
        if bracket_endex >= 0:
            curr_filename = curr_filename[bracket_endex:]

        if curr_filename:
            for name,song in music_choices:

                # bracket check
                bracket_endex = song.find(">")

                if bracket_endex >= 0:
                    check_song = song[bracket_endex:]
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
        music_choices = list()
        # SONGS:
        # if you want to add a song, add it to this list as a tuple, where:
        # [0] -> Title of song
        # [1] -> Path to song
        if not sayori:
            music_choices.append(("Just Monika","bgm/m1.ogg"))
            music_choices.append(("Your Reality","bgm/credits.ogg"))
            music_choices.append(("I Still Love You","bgm/monika-end.ogg"))
            music_choices.append(("Okay, Everyone! (Monika)","<loop 4.444>bgm/5_monika.ogg"))

        # sayori only allows this
        music_choices.append(("Surprise!",sayori_track))

        if not sayori:
            # leave this one last, so we can stopplaying stuff
            music_choices.append(("None", None))


    # defaults
    current_track = "bgm/m1.ogg"
    selected_track = current_track
    sayori_track = "<loop 36.782>bgm/d.ogg"
    menu_open = False
    enabled = True
    vol_bump = 0.1 # how much to increase volume by

    # contains the song list
    music_choices = list()

# some post screen init is setting volume to current settings
init 10 python in songs:

    # for muting
    music_volume = getVolume("music")

# non store post inint stuff
init 10 python:

    # ensure proper current track is set
    if persistent.playername.lower() == "sayori":
        store.songs.current_track = store.songs.sayori_track
        store.songs.selected_track = store.songs.sayori_track
    else:
        store.songs.current_track = persistent.current_track
        store.songs.selected_track = store.songs.current_track

    # song choice generation
    store.songs.initMusicChoices(
        sayori=persistent.playername.lower() == "sayori"
    )

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

style music_menu_outer_frame is game_menu_outer_frame
style music_menu_navigation_frame is game_menu_navigation_frame
style music_menu_content_frame is game_menu_content_frame
style music_menu_viewport is game_menu_viewport
style music_menu_side is game_menu_side
style music_menu_label is game_menu_label
style music_menu_label_text is game_menu_label_text

style music_menu_return_button is return_button

style music_menu_outer_frame:
    background "mod_assets/music_menu.png"

screen music_menu():
    modal True

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
        yalign 0.8
        spacing gui.navigation_spacing

        # wonderful loop so we can dynamically add songs
        $ import store.songs as songs
        for name,song in songs.music_choices:
            textbutton _(name) action [SetField(songs,"selected_track",song), Return()]

    textbutton _("Return"):
        style "music_menu_return_button"
        action Return()

    label "Music Menu"

# sets locks and calls hte appropriate screen
label display_music_menu:
    # set var so we can block multiple music menus
    python:
        import store.songs as songs
        songs.menu_open = True
        prev_dialogue = allow_dialogue
        allow_dialogue = False

    call screen music_menu

    $ songs.menu_open = False
    $ allow_dialogue = prev_dialogue
    return
