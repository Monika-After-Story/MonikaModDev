init 10 python:
    import time
    global mas_afk_already
    global mas_afk_time
    global mas_afk_duration
    mas_afk_already = False
    # How much time in seconds should pass, before it's considered that player is afk.
    mas_afk_duration = 600
    mas_afk_time = time.time() + mas_afk_duration
    config.overlay_screens.append("dev_detection")
    class MASInactivity(renpy.Displayable):
        
        import pygame

        def __init__(self):
            super(MASInactivity, self).__init__()

        def event(self, ev, x, y, st):
            global mas_afk_time
            global mas_afk_already
            global mas_afk_duration
            # Constant checking for player activity - mouse movement, keystrokes and mouse button clicks
            if ev.type == pygame.MOUSEMOTION:
                mas_afk_time = time.time() + mas_afk_duration
            if ev.type == pygame.KEYDOWN:
                mas_afk_time = time.time() + mas_afk_duration
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mas_afk_time = time.time() + mas_afk_duration
            if mas_afk_time < time.time() and not mas_afk_already:
                mas_afk_already = True
                # Checking if event can be restarted (added greetings and byes in event-handler.rpy for only afk check)
                if not mas_isRstBlk(persistent.current_monikatopic):
                    pushEvent(persistent.current_monikatopic)
                    pushEvent('continue_event')
                    persistent.current_monikatopic = 0
                    #if can be restarted jump to afk dialogue.
                    renpy.jump("dev_inactivity_detection")
                else:
                #if can't be restarted simply call afk dialogue.
                    renpy.call("dev_inactivity_detection")
            renpy.redraw(self, 0)

        def render(self, width, height, st, at):
            return renpy.Render(0, 0)

screen dev_detection():
    add MASInactivity()


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_inactivity_detection",
            category=["dev"],
            prompt="INACTIVITY DETECTION (ACTUALLY NO NEED TO PRESS THAT)",
            pool=True,
            unlocked=True
        )
    )

label dev_inactivity_detection:
#TODO: I'm terrible at making dialogues, can someone please check if this is actually alright?
    m "Are you still there?"
    m "You are back, [player]!"
    $ global mas_afk_already
    $ mas_afk_already = False
    return

return