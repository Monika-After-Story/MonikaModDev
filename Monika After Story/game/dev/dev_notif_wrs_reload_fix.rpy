#NOTE: This is done because the wndclass can't be registered twice
#and we need to clear notifs to reload
init 999 python:
    try:
        import store
        import win32gui
        def mas_prepForReload():
            store.mas_clearNotifs()
            win32gui.UnregisterClass(tip.classAtom, tip.hinst)
    except:
        pass