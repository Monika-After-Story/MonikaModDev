
# pre-r8 r8 code

default persistent._mas_r8_testing_enabled = False
# is r8 testing enabled. controls updater source URL

default persistent._mas_r8_testing_confirmed = False
# true if Monika has confirmed with player to leave r8 testing enabled

default persistent._mas_r8_need_to_confirm_testing = False
# true if player just enabled r8 testing and we need to confirm 

default persistent._mas_pm_tested_r8 = False
# true if the user has tested r8 (aka they are running r8 build)
#   NOTE: expected to be inaccurate if r6 restored

default persistent._mas_pm_enabled_r8_testing = False
# true if player ever enabled r8 testing and confimred with Monika

default persistent._mas_pm_touched_r8_testing = False
# true if player touched the r8 checkbox at all

init 49 python in mas_r8_testing_ctx:

    r8_checkbox_touched = False
    # set when the r8 checkbox has been touched

init 50 python in mas_r8_testing:
    import store
    import store.mas_r8_testing_ctx as ctx
    from store import MASEventList, mas_rmallEVL, persistent

    def _onclick_r8_checkbox():
        """
        Called when the r8 checkbox is toggled in some way.
        this is AFTER the testing mode is enabled/disabled
        """
        ctx.r8_checkbox_touched = True
        persistent._mas_pm_touched_r8_testing = True

        # only confirm with user if they just enabled r8 testnig and 
        # they arent already confirmed for r8 testing
        persistent._mas_r8_need_to_confirm_testing = (
            persistent._mas_r8_testing_enabled and not persistent._mas_r8_testing_confirmed
        )


    def _on_mas_game_menu_end(scope):
        """
        Called when the game menu is closed
        """
        # NOTE: this is here to avoid having to reset midloopeval skip
        if persistent._mas_r8_need_to_confirm_testing:
            # should immediately talk to the player about this
            MASEventList.push("mas_r8_testing", skipeval=True, notify=True)

        elif ctx.r8_checkbox_touched and not persistent._mas_r8_testing_enabled:
            # user touched the checkbox, but testing is not enabled, assume they dont want to test anymore
            persistent._mas_r8_testing_confirmed = False

        # clear checkbox touch status
        ctx.r8_checkbox_touched = False


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

    m 1eua "TODO: wow r8"

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

