image console_bg:
    "#333"
    topleft
    alpha 0.75 size (480,180)

style console_text:
    font "gui/font/F25_Bank_Printer.ttf"
    color "#fff"
    size 18
    outlines []
    #slow_cps 20

style console_text_console is console_text:
    slow_cps 30

default consolehistory = []
image console_text = ParameterizedText(style="console_text_console", anchor=(0,0), xpos=30, ypos=10)
image console_history = ParameterizedText(style="console_text", anchor=(0,0), xpos=30, ypos=50)
image console_caret = Text(">", style="console_text", anchor=(0,0), xpos=5, ypos=10)

label updateconsole(text="", history=""):
    show console_bg zorder 100
    show console_caret zorder 100
    show console_text "_" as ctext zorder 100
    show console_text "[text]" as ctext zorder 100
    $ pause(len(text) / 30.0 + 0.5)
    hide ctext
    show console_text "_" as ctext zorder 100
    call updateconsolehistory(history)
    pause 0.5
    return

label updateconsole_clearall(text="", history=""):
    $ pause(len(text) / 30.0 + 0.5)
    pause 0.5
    return

label updateconsole_old(text="", history=""):
    $ starttime = datetime.datetime.now()
    $ textlength = len(text)
    $ textcount = 0
    show console_bg zorder 100
    show console_caret zorder 100
    show console_text "_" as ctext zorder 100
    label updateconsole_loop:
        $ currenttext = text[:textcount]
        call drawconsole(drawtext=currenttext)
        $ pause_duration = 0.08 - (datetime.datetime.now() - starttime).microseconds / 1000.0 / 1000.0
        $ starttime = datetime.datetime.now()
        if pause_duration > 0:
            $ renpy.pause(pause_duration / 2)
        $ textcount += 1
        if textcount <= textlength:
            jump updateconsole_loop
    
    pause 0.5
    hide ctext
    show console_text "_" as ctext zorder 100
    call updateconsolehistory(history)
    pause 0.5
    return

    label drawconsole(drawtext=""):
        #$ cursortext = "_".rjust(len(drawtext) + 1)
        show console_text "[drawtext]_" as ctext zorder 100
        #show console_text cursortext as ccursor zorder 100
        return

label updateconsolehistory(text=""):
    if text:
        python:
            consolehistory.insert(0, text)
            if len(consolehistory) > 5:
                del consolehistory[5:]
            consolehistorydisplay = '\n'.join(map(str, consolehistory))
        show console_history "[consolehistorydisplay]" as chistory zorder 100
    return

label hideconsole:
    hide console_bg
    hide console_caret
    #hide ccursor
    hide ctext
    hide chistory