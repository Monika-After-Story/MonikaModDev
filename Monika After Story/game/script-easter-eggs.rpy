# script stuff that is actually easter eggs

# yuri scare
label yuri_name_scare:
#    show yuri 3s zorder 2 at t11
    $ HKBHideButtons()
    $ disable_esc()
    scene black
    show yuri eyes zorder 2 at t11
    play music hb
    show layer master at heartbeat
    show dark zorder 200
    pause 4.0
    hide yuri
    hide dark
    show layer master
    stop music
    $ HKBShowButtons()
    $ enable_esc()
    return
