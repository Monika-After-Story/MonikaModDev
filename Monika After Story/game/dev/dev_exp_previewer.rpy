# special module that contains a screen dedicated to expression prevewing. 
# we really needed this lol.

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_exp_previewer",
            category=["dev"],
            prompt="EXP PREVIEW",
            pool=True,
            random=True,
            unlocked=True
        )
    )

label dev_exp_previewer:
    # call a screen
    m "TODO call a screen"
    return


init 1000 python:
    class MASExpPreviewer(renpy.Displayable):
        """
        we are about to go there
        """
        import pygame

        # CONSTANTS
        VIEW_WIDTH = 1280
        VIEW_HEIGHT = 720

        ROW_SPACING = 20
        BUTTON_WIDTH = 120
        BUTTON_HEIGHT = 35

        # 300 pixels from the top
        BUTTON_Y_START = 300

        def __init__(self):
            """
            Creates the Expression previewer displayable
            """
            super(renpy.Displayable, self).__init__()

            ### setup images
            # buttons:
            button_idle = Image("mod_assets/hkb_idle_background.png")
            button_hover = Image("mod_assets/hkb_hover_background.png")
            button_disabled = Image("mod_assets/hkb_disabled_background.png")

            # button text


