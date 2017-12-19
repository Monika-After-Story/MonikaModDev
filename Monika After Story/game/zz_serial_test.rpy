# TEmporary module for serialization testing
#

default persistent.begin_test = True
default persistent.serial_objs = None

init -1 python in data_points:
    eventlabels = [
        "test1",
        "test2",
        "test3",
        "test4"
    ]

    prompts = [
        "prompt1",
        "prompt2",
        "prompt3",
        "prompt4"
    ]

    labels = [
        "label1",
        "label2",
        "label3",
        "label4"
    ]

    categorys = [
        ("string101", "string102", "string103"),
        ("string201",),
        ("string301", "string302"),
        ("string401", "string402", "string403", "string404")
    ]

    m_categorys = [
        ((True,("string101","string401")), ("test1", "test4")),
        ((False,("string301", "string302")), ("test3",)),
        (None, ("test1","test2","test3","test4")),
        ((True,list()),("test1","test2","test3","test4"))
    ]

    unlockeds = [
        True,
        False,
        False,
        True
    ]

    m_unlockeds = [
        (True,("test1","test4")),
        (False,("test2","test3")),
        (None, ("test1","test2","test3","test4"))
    ]

    randoms = [
        False,
        True,
        False,
        True
    ]

    m_randoms = [
        (True, ("test2", "test4")),
        (False, ("test1", "test3")),
        (None, ("test1","test2","test3","test4"))
    ]

    pools = [
        True,
        True,
        False,
        True
    ]
    
    m_pools = [
        (True, ("test1","test2","test4")),
        (False, ("test3",)),
        (None, ("test1","test2","test3","test4"))
    ]

    conditionals = [
        "expr1",
        "expr2",
        "expr3",
        "expr4 == exrp3"
    ]

    actions = [
        "queue",
        "random",
        "push",
        None
    ]

    m_actions = [
        (("queue","random"),("test1","test2")),
        (("push",),("test3",)),
        (None, ("test1","test2","test3","test4"))
    ]

    from datetime import datetime

    start_dates = [
        datetime(1995,10,31),
        datetime(2000,1,2,10,10,10),
        datetime(1970,12,22),
        None
    ]

    end_dates = [
        None,
        datetime(2001,9,11),
        datetime(2004,4,20),
        datetime(2020,12,12,12,12)
    ]

    ud1 = None
    ud2 = datetime(2001,10,10)
    ud3 = datetime(1990,10,10)
    ud4 = datetime(2010,10,10)


    unlock_dates = [ud1, ud2, ud3, ud4]

    s_unlock_dates = [ud3, ud2, ud4]
    sn_unlock_dates = [ud3, ud2, ud4, ud1]


init python:
    import store.data_points as dpts

    if persistent.begin_test:
        persistent.serial_objs = dict()
        for i in range(0,4):
            persistent.serial_objs[dpts.eventlabels[i]] = Event(
                dpts.eventlabels[i],
                dpts.prompts[i],
                dpts.labels[i],
                dpts.categorys[i],
                dpts.unlockeds[i],
                dpts.randoms[i],
                dpts.pools[i],
                dpts.conditionals[i],
                dpts.actions[i],
                dpts.start_dates[i],
                dpts.end_dates[i],
                dpts.unlock_dates[i]
            )
        persistent.begin_test = False


    # test function 2
    def findIndex(k):
        for i in range(0,4):
            if k == dpts.eventlabels[i]:
                return i
        return -1

    # tfunc 3
    def testCase(name, found, expec):
        return ("[" + str(found == expec) + "]-" + name + "-> F: " 
            + str(found) + " E: " + str(expec) + "\n")

    # test fun for collections
    def testCaseColl(name, found, expec):
        from collections import Counter
        return ("[" + str(Counter(found) == Counter(expec)) + "]-" + name +
            "-> F: " + str(found) + " E: " + str(expec) + "\n")

    # test function
    # returns a string of the results
    def testSerial():
        results = ""
        for dex in range(0,4):
            v = persistent.serial_objs[dpts.eventlabels[dex]]
            results += "item:\n"
            results += testCase("eventlabels", v.eventlabel, dpts.eventlabels[dex])
            results += testCase("prompt", v.prompt, dpts.prompts[dex])
            results += testCase("label", v.label, dpts.labels[dex])
            results += testCase("category", v.category, dpts.categorys[dex])
            results += testCase("unlocked", v.unlocked, dpts.unlockeds[dex])
            results += testCase("random", v.random, dpts.randoms[dex])
            results += testCase("pool", v.pool, dpts.pools[dex])
            results += testCase("cond", v.conditional, dpts.conditionals[dex])
            results += testCase("action", v._action, dpts.actions[dex])
            results += testCase("start_date", v.start_date, dpts.start_dates[dex])
            results += testCase("end_date", v.end_date, dpts.end_dates[dex])
            results += testCase("unlock_date", v.unlock_date, dpts.unlock_dates[dex])
            results += "\n"
        return results

    # test sorting
    # returns a string of the results
    def testSort():

        # sorting, no NONe
        sorted_keys = Event.getSortedKeys(persistent.serial_objs)
        results = "SORTING, NO NONE:\n\n"
        dex = 0
        for k in sorted_keys:
            results += testCase(
                k, 
                persistent.serial_objs[k].unlock_date,
                dpts.s_unlock_dates[dex]
            )
            dex += 1

        # sorting,  with None
        sorted_keys = Event.getSortedKeys(
            persistent.serial_objs,
            include_none=True
        )
        results += "\n\nSORTING, WITH NONE:\n\n"
        dex = 0
        for k in sorted_keys:
            results += testCase(
                k,
                persistent.serial_objs[k].unlock_date,
                dpts.sn_unlock_dates[dex]
            )
            dex += 1

        results += "\n"
        return results

    # test filtering
    # returns a string of results
    def testFilter():

        results = ""
        ev_list = persistent.serial_objs

        # lets start with category
        results += "FILTER CATEGORY:\n\n"
        for i,o in dpts.m_categorys:
            filt_ev = Event.filterEvents(
                persistent.serial_objs,full_copy=True,category=i
            ).keys()
            results += testCaseColl("category",filt_ev,o)

        results += "\nFILTER UNLOCKS:\n\n"
        for i,o in dpts.m_unlockeds:
            filt_ev = Event.filterEvents(
                persistent.serial_objs,unlocked=i
            ).keys()
            results += testCaseColl("unlocked",filt_ev,o)

        results += "\nFILTER RANDOMS:\n\n"
        for i,o in dpts.m_randoms:
            filt_ev = Event.filterEvents(
                persistent.serial_objs,random=i
            ).keys()
            results += testCaseColl("random",filt_ev,o)

        results += "\nFILTER POOLS:\n\n"
        for i,o in dpts.m_pools:
            filt_ev = Event.filterEvents(
                persistent.serial_objs,pool=i
            ).keys()
            results += testCaseColl("pool",filt_ev,o)

        results += "\nFILTER actions\n\n"
        for i,o in dpts.m_actions:
            filt_ev = Event.filterEvents(
                persistent.serial_objs,action=i
            ).keys()
            results += testCaseColl("action", filt_ev, o)

        results += "\nCUSTOM FILTER:\n\n"
        filt_ev = Event.filterEvents(
            persistent.serial_objs,
            category=(True, ("string101","string302","string404")),
            unlocked=True,
            random=False,
            pool=True,
            action=("queue",)
        ).keys()
        results += testCaseColl("custom", filt_ev, ("test1",))

        return results
