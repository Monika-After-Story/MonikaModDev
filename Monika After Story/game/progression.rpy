# Module that defines functions for handling game progression and leveling up

init python:

    def grant_xp('experience'):
        #Check level before experience gain
        old_level = get_level()

        #Add XP
        persistent.playerxp += experience

        #Check new level
        new_level = get_level()

        #Do any actions you need to do based on level.
        for i in range(old_level,new_level):
            #Whenever you level up, unlock a prompt
            pushEvent('unlock_prompt')



    def get_level():
        import math

        xp = persistent.playerxp

        if xp <= 390:
            approx_level = (-1.0+sqrt(1+(8.0/5.0)*xp))/2.0
            level = floor(approx_level)
        else:
            level = 12 + floor((xp-390.0)/60.0)

        return level
