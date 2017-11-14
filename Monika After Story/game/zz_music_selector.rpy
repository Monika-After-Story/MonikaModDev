# Module that handles the music selection screen
# we start with zz to ensure this loads LAST
#

# music inits first, so the screen can be made well
init -1 python in songs:

    # defaults
    current_track = "bgm/m1.ogg"
    selected_track = current_track
    menu_open = False

    # SONGS:
    # if you want to add a song, add it to this list as a tuple, where:
    # [0] -> Title of song
    # [1] -> Path to song
    music_choices = list()
    music_choices.append(("Just Monika","bgm/m1.ogg"))
    music_choices.append(("Your Reality","bgm/credits.ogg"))
    music_choices.append(("I Still Love You","bgm/monika-end.ogg"))
    music_choices.append(("Okay, Everyone! (Monika)","<loop 4.444>bgm/5_monika.ogg"))
    music_choices.append(("Surprise!","<loop 36.782>bgm/d.ogg"))


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

screen music_menu():
    modal True

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
