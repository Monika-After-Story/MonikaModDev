## This file contains options that can be changed to customize your game.
##
## Lines beginning with two '#' marks are comments, and you shouldn't uncomment
## them. Lines beginning with a single '#' mark are commented-out code, and you
## may want to uncomment them when appropriate.


## Basics ######################################################################
python early:
    ## A human-readable name of the game. This is used to set the default window
    ## title, and shows up in the interface and error reports.
    ##
    ## The _() surrounding the string marks it as eligible for translation.
    renpy.config.name = "Monika After Story"

    ## The version of the game.
    renpy.config.version = "0.12.3"

    #Triple space suffix to avoid potential issues with same names in window title
    config.window_title = "Monika After Story   "

    ## Save directory ##############################################################
    ##
    ## Controls the platform-specific place Ren'Py will place the save files for
    ## this game. The save files will be placed in:
    ##
    ## Windows: %APPDATA\RenPy\<config.save_directory>
    ##
    ## Macintosh: $HOME/Library/RenPy/<config.save_directory>
    ##
    ## Linux: $HOME/.renpy/<config.save_directory>
    ##
    ## This generally should not be changed, and if it is, should always be a
    ## literal string, not an expression.

    renpy.config.save_directory = "Monika After Story"

init -1200 python:
## Sounds and music ############################################################

## These three variables control which mixers are shown to the player by
## default. Setting one of these to False will hide the appropriate mixer.

    renpy.config.has_sound = True
    renpy.config.has_music = True
    renpy.config.has_voice = False


## To allow the user to play a test sound on the sound or voice channel,
## uncomment a line below and use it to set a sample sound to play.

#     renpy.config.sample_sound = "sample-sound.ogg"
#     renpy.config.sample_voice = "sample-voice.ogg"


## Transitions #################################################################
##
## These variables set transitions that are used when certain events occur. Each
## variable should be set to a transition, or None to indicate that no
## transition should be used.

## Entering or exiting the game menu.

    renpy.config.enter_transition = Dissolve(.2)
    renpy.config.exit_transition = Dissolve(.2)


## A transition that is used after a game has been loaded.

    renpy.config.after_load_transition = None


## Used when entering the main menu after the game has ended.

    renpy.config.end_game_transition = Dissolve(.5)


## A variable to set the transition used when the game starts does not exist.
## Instead, use a with statement after showing the initial scene.


## Window management ###########################################################
##
## This controls when the dialogue window is displayed. If "show", it is always
## displayed. If "hide", it is only displayed when dialogue is present. If
## "auto", the window is hidden before scene statements and shown again once
## dialogue is displayed.
##
## After the game has started, this can be changed with the "window show",
## "window hide", and "window auto" statements.

    renpy.config.window = "auto"


## Icon
## ########################################################################'

## The icon displayed on the taskbar or dock.

    renpy.config.window_icon = "gui/window_icon.png"

## Custom configs ##############################################################

    renpy.config.allow_skipping = True
    renpy.config.has_autosave = False
    renpy.config.autosave_on_quit = False
    renpy.config.autosave_slots = 0
    renpy.config.layers = ["master", "transient", "minigames", "screens", "overlay", "front"]
    renpy.config.image_cache_size = 64
    renpy.config.debug_image_cache = config.developer
    renpy.config.predict_statements = 5
    renpy.config.rollback_enabled = config.developer
    renpy.config.menu_clear_layers = ["front"]
    renpy.config.gl_test_image = "white"

################START: INIT TIME CONFIGS

## Uncomment the following line to set an audio file that will be played while
## the player is at the main menu. This file will continue playing into the
## game, until it is stopped or another file is played.

define config.main_menu_music = audio.t1
## Transitions used to show and hide the dialogue window

define config.window_show_transition = dissolve_textbox
define config.window_hide_transition = dissolve_textbox
