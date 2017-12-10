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

    unlockeds = [
        True,
        False,
        False,
        True
    ]

    randoms = [
        False,
        True,
        False,
        True
    ]

    pools = [
        True,
        True,
        False,
        True
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
                dpts.end_dates[i]
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
            results += "\n"
        return results
