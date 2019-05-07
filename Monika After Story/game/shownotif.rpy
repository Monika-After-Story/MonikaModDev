init python:
    import sys
    sys.path.extend((renpy.config.gamedir + '\\python-packages\\win32', renpy.config.gamedir +'\\python-packages\\win32\\Lib'))
    import balloontip
    tip = balloontip.WindowsBalloonTip()

label display_notif(title, body):
    $ tip.showWindow(title,body)
    return