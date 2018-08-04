# Initialise the DDMM SDK
init -10 python:
    import urllib2, json
    ddmm_rpc_url = "http://127.0.0.1:41420/"
    ddmm_online = False
    try:
        request = urllib2.Request(ddmm_rpc_url, json.dumps({"method": "ping"}))
        urllib2.urlopen(request).read()
        ddmm_online = True
    except:
        ddmm_online = False


# Register an achievement with Doki Doki Mod Manager
# id = the unique ID of the achievement, can be any string
# name = the user-facing name of the achievement
# description = the user-facing description of the achievement
label ddmm_register_achievement(id, name, description):
    python:
        if ddmm_online:
                request = urllib2.Request(ddmm_rpc_url, json.dumps({"method": "register achievement", "payload": {"id": id, "name": name, "description": description}}))
                urllib2.urlopen(request).read()
    return

# Earn an achievement
# id = the unique ID of the achievement
label ddmm_earn_achievement(id):
    python:
        if ddmm_online:
            request = urllib2.Request(ddmm_rpc_url, json.dumps({"method": "earn achievement", "payload": {"id": id}}))
            urllib2.urlopen(request).read()
    return

# Test SDK functions
label _ddmm_test:
    scene black
    "Online: [ddmm_online]"
    menu:
        "Pick one..."
        "Register Achievements":
            call ddmm_register_achievement("TEST_ACHIEVEMENT_1", "Just Monika", "Complete Monika's Route") from _call_ddmm_register_achievement
            call ddmm_register_achievement("TEST_ACHIEVEMENT_2", "Hanging Out", "Complete Sayori's Route") from _call_ddmm_register_achievement_1
            "Registered achievement."
        "Earn Achieve 1":
            call ddmm_earn_achievement("TEST_ACHIEVEMENT_1") from _call_ddmm_earn_achievement
            "Earned achievement."
        "Earn Achieve 2":
            call ddmm_earn_achievement("TEST_ACHIEVEMENT_2") from _call_ddmm_earn_achievement_1
            "Earned achievement."
        "Quit":
            pass
    return
