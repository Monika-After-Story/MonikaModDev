init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_mas_renderer",
            category=["dev"],
            prompt="SHOW RENDERER INFO",
            pool=True,
            unlocked=True
        )
    )
    
label dev_mas_renderer:
    python:
        renderer = mas_getRendererName() # string
        isSoftware = mas_isSoftwareRendering() # bool
        kwinRunning = is_running(['kwin_x11', 'kwin_wayland']) # bool
        
    m "Sure! RenPy is using the \"[renderer]\" renderer..."
    if isSoftware:
        m "...which means it's using software rendering. Ahaha... I feel bad for your CPU, [player]."
    else:
        m "...which means I'm not on software rendering mode! Yay!~"
        
    if renpy.linux:
        if kwinRunning:
            m "It also looks like you're using KWin."
        else:
            m "You're on Linux, but you don't appear to be using KWin."