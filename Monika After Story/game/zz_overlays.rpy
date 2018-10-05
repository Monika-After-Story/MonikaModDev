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

    def mas_OVLDropShield():
        """RUNTIME ONLY
        Enables all overlay screens. This is like "dropping a shield" because
        it allows user interactions with the overlays.
        """
        # put all enabling functions here
        mas_HKBDropShield()
        mas_calDropOverlayShield()


    def mas_OVLHide():
        """RUNTIME ONLY
        Hides all overlay screens.
        """
        # put hide functions here
        HKBHideButtons()
        mas_calHideOverlay()


    def mas_OVLRaiseShield():
        """RUNTIME ONLY
        Disables all overlay screens. This is like "raising a shield" because
        it prevents user interactions with the overlays.
        """
        # put all disabling functions here
        mas_HKBRaiseShield() 
        mas_calRaiseOverlayShield()


    def mas_OVLShow():
        """RUNTIME ONLY
        Shows all overlay screens.
        """
        # put all show functions
        HKBShowButtons()
        mas_calShowOverlay()



