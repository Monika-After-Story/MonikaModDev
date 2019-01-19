# This file is meant to store any special effects.
# These can be some images or transforms.

image yuri dragon2:
    parallel:
        "yuri/dragon1.png"
        0.01
        "yuri/dragon2.png"
        0.01
        repeat

image blood splatter1:
    size (1, 1)
    truecenter
    Blood("blood_particle",dripTime=0.5, burstSize=150, burstSpeedX=400.0, burstSpeedY=400.0, numSquirts=15, squirtPower=400, squirtTime=2.0).sm


image k_rects_eyes1:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (580, 270)
    size (20, 25)
    8.0

image k_rects_eyes2:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (652, 264)
    size (20, 25)
    8.0

image natsuki mas_ghost:
    "natsuki ghost2"
    parallel:
        easeout 0.25 zoom 4.5 yoffset 1200
    parallel:
        ease 0.025 xoffset -20
        ease 0.025 xoffset 20
        repeat
    0.25

image mujina:
    "mod_assets/other/mujina.png"
    zoom 1.25
    parallel:
        easeout 0.5 zoom 4.5 yoffset 1200
    0.5

image mas_lightning:
    "mod_assets/other/thunder.png"
    alpha 1.0

    choice:
        block:
            0.05
            alpha 0.0
            0.05
            alpha 1.0
            repeat 3

    choice:
        block:
            0.05
            alpha 0.0
            0.05
            alpha 1.0
            repeat 2

    choice:
        0.05

    parallel:
        easeout 2.8 alpha 0.0
    3.0
    Null()

image mas_lightning_s_bg = LiveComposite(
    (1280, 720),
    (0, 0), "mod_assets/other/thunder.png",
    (30, 200), "mod_assets/other/tree_sil.png"
)

image mas_lightning_s:
    "mas_lightning_s_bg"
    alpha 1.0

    block:
        0.05
        alpha 0.0
        0.05
        alpha 1.0
        repeat 2

    0.05
    alpha 0.0
    0.05
    "mod_assets/other/thunder.png"
    alpha 1.0

    parallel:
        easeout 2.8 alpha 0.0
    3.0
    Null()

transform k_scare:
    tinstant(640)
    ease 1.0 zoom 2.0

transform otei_appear(a=0.70,time=1.0):
    i11
    alpha 0.0
    linear time alpha a

transform fade_in(time=1.0):
    alpha 0.0
    ease time alpha 1.0

init python:
    def zoom_smoothly(trans, st, at):
        if trans.y < _mas_current_kiss_y:
            trans.y = 50
        if trans.zoom < _mas_current_kiss_zoom:
            trans.zoom = 50
        return 0

# kissing animation transform
transform mas_kissing(_zoom, _y,time=2.0):
    i11
    xcenter 640 yoffset 700 yanchor 1.0
    linear time ypos _y zoom _zoom

transform mas_back_from_kissing(time, y):
    linear time xcenter 640 yoffset (y) zoom 0.80


default persistent._mas_first_kiss = None
# contains datetime of users's first kiss with monika
# NOTE: need to add this to calendar

# mas_kissing_motion_base label
# Used to do the kiss motion, it takes care of setting persistent._mas_first_kiss
#
# IN:
#     transition - time in seconds used to transition to the actual kiss and then
#         used for going back to the inital state
#         (Default: 4.0)
#     duration -  time in seconds that the screen stays black
#         (Default: 3.0)
#     hide_ui - boolean indicating if we shoudl hide the ui
#         (Default: True)
#     initial_exp - string indicating the expression Monika will have at the beginning
#         of the animation
#         (Default: 6dubfd)
#     mid_exp - string indicating the expression Monika will have at the middle
#         of the animation, when moving back to the original postion
#         (Default: 6tkbfu)
#     final_exp - string indicating the expression Monika will have at the end
#         of the animation, when she's done getting back to the original position
#         (Default: 6tkbfu)
#     fade_duration - time in seconds spent fading the screen into black
#         (Default: 1.0)
label monika_kissing_motion(transition=4.0, duration=2.0, hide_ui=True,
        initial_exp="6dubfd", mid_exp="6tkbfu", final_exp="6ekbfa", fade_duration=1.0):
    # Note: the hardcoded constants work to give the focus on lips
    # effect these were calculated based on max/min values of the zoom

    if persistent._mas_first_kiss is None:
        $ persistent._mas_first_kiss = datetime.datetime.now()

    window hide
    if hide_ui:
        # hide everything
        $ HKBHideButtons()
        $ mas_RaiseShield_core()
    # reset position to i11
    show monika at i11
    # do the appropriate calculations
    $ _mas_kiss_zoom = 4.9 / mas_sprites.value_zoom
    $ _mas_kiss_y = 2060 - ( 1700  * (mas_sprites.value_zoom - 1.1))
    $ _mas_kiss_y2 = -1320 + (1700 * (mas_sprites.value_zoom - 1.1))
    # 380 #correct value for max
    # start the kiss animation
    $ renpy.show("monika {}".format(initial_exp), [mas_kissing(_mas_kiss_zoom,int(_mas_kiss_y),transition)])
    # show monika 6dubfd at mas_kissing(_mas_kiss_zoom,int(_mas_kiss_y),transition)
    # wait until we're done with the animation
    $ renpy.pause(transition)
    # show black scene
    show black zorder 100 at fade_in(fade_duration)
    # wait half the time to play the sound effect
    $ renpy.pause(duration/2)
    play sound "mod_assets/sounds/effects/kissing.ogg"
    window auto
    "chu~{fast}{w=1}{nw}"
    window hide
    $ renpy.pause(duration/2)
    # hide the black scene
    hide black
    # trasition back which is the best time for non slow back off
    $ renpy.show("monika {}".format(mid_exp),[mas_back_from_kissing(transition,_mas_kiss_y2)])
    pause transition
    $ renpy.show("monika {}".format(final_exp),[i11()])
    show monika with dissolve
    if hide_ui:
        if store.mas_globals.dlg_workflow:
            $ mas_MUMUDropShield()
        else:
            $ mas_DropShield_core()
        $ HKBShowButtons()
    window auto
    return

label monika_kissing_motion_short:
    call monika_kissing_motion(duration=0.5, initial_exp="6hua", fade_duration=0.5)
    return