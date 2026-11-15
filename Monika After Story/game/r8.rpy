
# pre-r8 r8 code

default persistent._mas_r8_testing_enabled = False
# is r8 testing enabled. controls updater source URL

default persistent._mas_r8_testing_confirmed = False
# true if Monika has confirmed with player to leave r8 testing enabled

default persistent._mas_r8_need_to_confirm_mode = False
# true if player just enabled r8 testing and we need to confirm 

default persistent._mas_r8_checkbox_touched = False
# true if player has touched the r8 checkbox

default persistent._mas_pm_tested_r8 = False
# true if the user has tested r8 (aka they are running r8 build)
#   NOTE: expected to be inaccurate if r6 restored

default persistent._mas_pm_enabled_r8_testing = False
# true if player ever enabled r8 testing and confimred with Monika

default persistent._mas_pm_touched_r8_testing = False
# true if player touched the r8 checkbox at all

init 50 python in mas_r8_testing:
    import renpy

    def _onclick_r8_checkbox():
        """
        Called when the r8 checkbox is toggled in some way.
        this is AFTER the testing mode is enabled/disabled
        """
        if renpy.persistent._mas_r8_testing_enabled:
            # r8 checkbox enabled

            # TODO:
            #   1 - set need_to_confirm to True
            #   2 - push EV to confirm r8 testing

            pass
            
        else:
            # r8 checkbox disabled

            # TODO:
            #   1 - clear EV for confirming (if was pushed)
            #   2 - need_to_confirm to False

            pass


init 5 python:
    # NOTE: this should never be unlocked unless the user clicks the R8 checbox
    #   and goes through this event at least once.
    addEvent(Event(
        persistent.event_database,
        eventlabel="mas_r8_testing",
        category=["mod"],
        prompt="Can we talk about updating to Renpy 8?"
    ))

label mas_r8_testing:

    # TODO:
    # Case 1: user clicks checkbox for first time
    # Case 2: user asks Monika with intention to disable r8 (pre update)
    # Case 3: user asks monika if R8 update available
    # Case 4: user asks monika general question about R8
    # Case 5: user enables checkbox for subsequent time/or 
    #       after having confirmed before
    # Case 6: (FUTURE) user has questions about R8 update AFTER having
    #       installed test build


    return 

