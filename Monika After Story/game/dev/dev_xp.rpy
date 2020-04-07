
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_xp_calc_test",
            category=["dev"],
            prompt="TEST XP CALC",
            pool=True,
            unlocked=True
        )
    )


label dev_xp_calc_test:

    $ numbers = "0123456789."

    m 1eua "test xp calculations here"

    $ xp_rate = renpy.input("enter desired xp / hour", allow=numbers)
    $ xp_rate = store.mas_utils.tryparsefloat(xp_rate, store.mas_xp.DEF_XP_RATE)

    $ duration = renpy.input("enter desired amt of hours to calc xp for", allow=numbers)
    $ duration = store.mas_utils.tryparsefloat(duration, 1)
    python:
        hours, hour_f = store.mas_utils.floatsplit(duration)
        duration_td = datetime.timedelta(seconds=hour_f*3600, hours=hours)
        end_time = datetime.datetime.now()
        start_time = end_time - duration_td

    $ hrx = renpy.input("enter number of hours we have already applied the current rate to", allow=numbers)
    $ hrx = store.mas_utils.tryparsefloat(hrx, 0.0)

    $ xp_gained, new_rate, new_hrx = store.mas_xp._calc(xp_rate, start_time, end_time, hrx)

    m 3eua "xp gained: [xp_gained]"
    m 3eua "new xp rate: [new_rate]"
    m 3eua "new daily hours: [new_hrx]"

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_xp_grant_test",
            category=["dev"],
            prompt="TEST XP GRANT",
            pool=True,
            unlocked=True
        )
    )

label dev_xp_grant_test:

    $ numbers = "0123456789."

    m 1eua "test xp grant calc here"

    $ xp = renpy.input("enter desired xp gained", allow=numbers)
    $ xp = store.mas_utils.tryparsefloat(xp, store.mas_xp.XP_LVL_RATE / 2)

    $ xptnl = renpy.input("entire xp to next level", allow=numbers)
    $ xptnl = store.mas_utils.tryparsefloat(xptnl, store.mas_xp.XP_LVL_RATE)

    $ lvl_gained, new_xptnl = store.mas_xp._grant(xp, xptnl)

    m 3eua "lvls gained: [lvl_gained]"
    m 3eua "new xp to next lvl: [new_xptnl]"

    return
