init python:
    import sys
    sys.path.extend((renpy.config.gamedir + '\\python-packages\\win32', renpy.config.gamedir +'\\python-packages\\win32\\Lib'))
    import balloontip
    tip = balloontip.WindowsBalloonTip()

label display_notif(title, body):
    $ tip.showWindow(title,body)
    return

#Need to keep testing timing
label monika_loveyou:
    call display_notif("Monika", "I just wanted to tell you...")
    pause 15.0
    call display_notif("Monika", "I love you!")
    return