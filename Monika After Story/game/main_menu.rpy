screen main_menu():

    # This ensures that any other menu screen is replaced.
    tag menu

    style_prefix "main_menu"

    add "menu_bg"
    #Removed adding other char imgs to avoid red text error
    frame:
        pass

## The use statement includes another screen inside this one. The actual
## contents of the main menu are in the navigation screen.
    use navigation

    add "menu_particles"
    add "menu_particles"
    add "menu_particles"
    add "menu_logo"
    #Removed adding other char imgs to avoid red text error
    add "menu_particles"
    add "menu_art_m"
    add "menu_fade"

    if gui.show_name:

        vbox:
            text "[config.name!t]":
                style "main_menu_title"

            text "v. [config.version]":
                style "main_menu_version"


    key "K_ESCAPE" action Quit(confirm=False)

style main_menu_version is main_menu_text:
    color "#000000"
    size 16
    outlines []

style main_menu_version_dark is main_menu_text:
    color mas_ui.dark_button_text_idle_color
    size 16
    outlines []

style main_menu_frame is empty:
    xsize 310
    yfill True
    background "menu_nav"

style main_menu_frame_dark is empty:
    xsize 310
    yfill True
    background "menu_nav"

style main_menu_vbox is vbox:
    xalign 1.0
    xoffset -20
    xmaximum 800
    yalign 1.0
    yoffset -20

style main_menu_text is gui_text:
    xalign 1.0
    layout "subtitle"
    text_align 1.0
    color gui.accent_color

style main_menu_title is main_menu_text:
    size gui.title_text_size
