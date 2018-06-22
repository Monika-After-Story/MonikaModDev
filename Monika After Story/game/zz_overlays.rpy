# module for handling of overlay screens nicely
# NOTE: do not write screen overlays that need to be past 500 init level.
# this should be ran last to setup proper linkages
#
# NOTE: Contrary to the name of this file, overlays should NOT be written here.
#   Put your overlays in the appropriate file they belong in.
#   If they are global (aka not specific to a module), then fine, you can put
#   them in here.

init 501 python:
    # EVERYTHING HERE SHOULD ONLY BE USED AT RUNTIME

    def mas_dropShields(all_input=False):
        """RUNTIME ONLY
        Enables all overlay screens. This is like "dropping a shield" because
        it allows user interactions with the overlays.

        IN:
            all_input - True will enable all input. False will only enable
                overlays.
                NOTE: if all input was previously disabled, this arg is treated
                    as true.
        """
        if all_input or store.mas_overlays.INPUT_DISABLED:
            # enable mouse / keyboard interactions
            # TODO
            enable_esc()

        # put all enabling functions here
        mas_HKBDropShield()
        mas_calDropOverlayShield()

        # unshackle the input disable
        store.mas_overlays.INPUT_DISABLED = False


    def mas_hideOverlays():
        """RUNTIME ONLY
        Hides all overlay screens.
        """
        # put hide functions here
        HKBHideButtons()
        mas_calHideOverlay()


    def mas_raiseShields(all_input=False):
        """RUNTIME ONLY
        Disables all overlay screens. This is like "raising a shield" because
        it prevents user interactions with the overlays.

        IN:
            all_input - True will disable all input. False will only disable
                overlays
        """
        store.mas_overlays.INPUT_DISABLED = all_input
        if all_input:
            # disable mouse / keyhboard interactions
            # TODO
            disable_esc()

        # put all disabling functions here
        mas_HKBRaiseShield() 
        mas_calRaiseOverlayShield()


    def mas_showOverlays():
        """RUNTIME ONLY
        Shows all overlay screens.
        """
        # put all show functions
        HKBShowButtons()
        mas_calShowOverlay()


init 500 python in mas_overlays:
    # internalized functions
    INPUT_DISABLED = False # when true, that means all input was disabled


