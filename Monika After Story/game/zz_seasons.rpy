## seasonal module.
# contains season functions and seasonal programming points.

define mas_spring_equinox = datetime.date(datetime.date.today().year,3,21)
define mas_summer_solstice = datetime.date(datetime.date.today().year,6,21)
define mas_fall_equinox = datetime.date(datetime.date.today().year,9,23)
define mas_winter_solstice = datetime.date(datetime.date.today().year,12,21)

init -1 python:

    def mas_isSpring(_date=datetime.date.today()):
        """
        Checks if given date is during spring
        iff none passed in, then we assume today

        Note: If persistent._mas_pm_live_north_hemisphere is none, we assume northern hemi

        RETURNS:
            boolean showing whether or not it's spring right now
        """
        _date = _date.replace(datetime.date.today().year)

        if persistent._mas_pm_live_south_hemisphere:
            return mas_fall_equinox <= _date < mas_winter_solstice
        else:
            return mas_spring_equinox <= _date < mas_summer_solstice

    def mas_isSummer(_date=datetime.date.today()):
        """
        Checks if given date is during summer
        iff none passed in, then we assume today

        Note: If persistent._mas_pm_live_north_hemisphere is none, we assume northern hemi

        RETURNS:
            boolean showing whether or not it's summer right now
        """
        _date = _date.replace(datetime.date.today().year)

        if persistent._mas_pm_live_south_hemisphere:
            return mas_winter_solstice <= _date or _date < mas_spring_equinox
        else:
            return mas_summer_solstice <= _date < mas_fall_equinox

    def mas_isFall(_date=datetime.date.today()):
        """
        Checks if given date is during fall
        iff none passed in, then we assume today

        Note: If persistent._mas_pm_live_north_hemisphere is none, we assume northern hemi

        RETURNS:
            boolean showing whether or not it's fall right now
        """
        _date = _date.replace(datetime.date.today().year)

        if persistent._mas_pm_live_south_hemisphere:
            return mas_spring_equinox <= _date < mas_summer_solstice
        else:
            return mas_fall_equinox <= _date < mas_winter_solstice

    def mas_isWinter(_date=datetime.date.today()):
        """
        Checks if given date is during winter
        iff none passed in, then we assume today

        Note: If persistent._mas_pm_live_north_hemisphere is none, we assume northern hemi

        RETURNS:
            boolean showing whether or not it's winter right now
        """
        _date = _date.replace(datetime.date.today().year)

        if persistent._mas_pm_live_south_hemisphere:
            return mas_summer_solstice <= _date < mas_fall_equinox
        else:
            return mas_winter_solstice <= _date or _date < mas_spring_equinox


init 10 python in mas_seasons:
    import store
    # NOTE: all functions here are guaranteed to run at 900, and runtime.


    def _pp_spring():
        """
        Programming point for spring
        """
        mas_getEv('monika_snow').random = False
        mas_getEv('monika_sledding').random = False
        mas_getEv('monika_snowcanvas').random = False
        mas_getEv('monika_cozy').random = False
        mas_getEv('monika_winter').random = False
        mas_getEv('monika_winter_dangers').random = False
        return


    def _pp_summer():
        """
        Programming point for summer
        """
        pass


    def _pp_fall():
        """
        Programming point for fall
        """
        pass


    def _pp_winter():
        """
        Programming point for winter
        """
        mas_getEv('monika_sledding').random = True
        mas_getEv('monika_snowcanvas').random = True
        mas_getEv('monika_cozy').random = True
        mas_getEv('monika_winter').random = True
        mas_getEv('monika_winter_dangers').random = True
        if not persistent._seen_ever["monika_snow"]:
            mas_getEv('monika_snow').random = True
        return


init 900 python:
    # run the init-time seasonal check
    mas_seasonalCheck()
        
    
