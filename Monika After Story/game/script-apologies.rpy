#Create an apology db for storing our times
#Stores the event label as a key, its corresponding data is a tuple where:
#   [0] -> timedelta defined by: current total playtime + apology_active_expiry time
#   [1] -> datetime.date defined by the date the apology was added + apology_overall_expiry time
default persistent._mas_apology_time_db = {}

#Create a generic apology db. We'll want to know how many times the player has apologized for mas_apology_reason
#Allows us the ability to apply diminishing returns on affection for repeated use of the same apology
#This db here simply stores the integer corresponding to apology reason as a key,
#corresponding int value is the amt of times it was used
default persistent._mas_apology_reason_use_db = {}

init -10 python in mas_apology:
    apology_db = {}
    # Event database for apologies


init python:
    def mas_checkApologies():
        #Let's not do extra work
        if len(persistent._mas_apology_time_db) == 0:
            return

        #Calculate the current total playtime to compare...
        current_total_playtime = persistent.sessions['total_playtime'] + mas_getSessionLength()

        _today = datetime.date.today()
        #Iter thru the stuffs in the apology time tb
        for ev_label in persistent._mas_apology_time_db.keys():
            if current_total_playtime >= persistent._mas_apology_time_db[ev_label][0] or _today >= persistent._mas_apology_time_db[ev_label][1]:
                #Pop the ev_label from the time db and lock the event label. You just lost your chance
                store.mas_lockEVL(ev_label,'APL')
                persistent._mas_apology_time_db.pop(ev_label)

        return


init 5 python:
   addEvent(
       Event(
           persistent.event_database,
           eventlabel='monika_playerapologizes',
           prompt="I want to apologize...",
           category=['you'],
           pool=True,
           unlocked=True
        )
    )

label monika_playerapologizes:

    #Firstly, let's check if there's an apology reason for the prompt
    #NOTE: When adding more apology reasons, add a reason the player would say sorry for here (corresponding to the same #as the apology reason)
    $ player_apology_reasons = {
        0: "something else.", #since we shouldn't actually be able to get this, we use this as our fallback
        1: "saying I wanted to break up.",
        2: "joking about having another girlfriend.",
        3: "calling you a murderer.",
        4: "closing the game on you.",
        5: "entering your room without knocking.",
        6: "missing Christmas.",
        7: "forgetting your birthday.",
        8: "not spending time with you on your birthday.",
        9: "the game crashing.",
        10: "the game crashing.", #easiest way to handle this w/o overrides
        11: "not listening to your speech.",
        12: "calling you evil."
    }

    #Set the prompt for this...
    if len(persistent._mas_apology_time_db) > 0:
        #If there's a non-generic apology reason pending we use "for something else."
        $ mas_getEV('mas_apology_generic').prompt = "...for " + player_apology_reasons.get(mas_apology_reason,player_apology_reasons[0])
    else:
        #Otherwise, we use "for something." if reason isn't 0
        if mas_apology_reason == 0:
            $ mas_getEV('mas_apology_generic').prompt = "...for something."
        else:
            #We set this to an apology reason if it's valid
            $ mas_getEV('mas_apology_generic').prompt = "...for " + player_apology_reasons.get(mas_apology_reason,"something.")

    #Then we delete this since we're not going to need it again until we come back here, where it's created again.
    #No need to store excess memory
    $ del player_apology_reasons

    #Now we run through our apology db and find what's unlocked
    python:
        apologylist = [
            (ev.prompt, ev.eventlabel, False, False)
            for ev_label, ev in store.mas_apology.apology_db.iteritems()
            if ev.unlocked and (ev.prompt != "...for something." and ev.prompt != "...for something else.")
        ]

        #Now we add the generic if there's no prompt attached
        generic_ev = mas_getEV('mas_apology_generic')

        if generic_ev.prompt == "...for something." or generic_ev.prompt == "...for something else.":
            apologylist.append((generic_ev.prompt, generic_ev.eventlabel, False, False))

        #The back button
        return_prompt_back = ("Nevermind.", False, False, False, 20)

    #Display our scrollable
    show monika at t21
    call screen mas_gen_scrollable_menu(apologylist,(evhand.UNSE_X, evhand.UNSE_Y, evhand.UNSE_W, 500), evhand.UNSE_XALIGN, return_prompt_back)

    #Make sure we don't lose this value
    $ apology =_return

    #Handle backing out
    if not apology:
        if mas_apology_reason is not None or len(persistent._mas_apology_time_db) > 0:
            show monika at t11
            if mas_isMoniAff(higher=True):
                m 1ekd "[player], if you're feeling guilty about what happened..."
                m 1eka "You don't have to be afraid of apologizing, we all make mistakes after all."
                m 3eka "We just have to accept what happened, learn from our mistakes, and move on, together. Okay?"
            elif mas_isMoniNormal(higher=True):
                m 1eka "[player]..."
                m "If you want to apologize, go ahead. It'd mean a lot to me if you did."
            elif mas_isMoniUpset():
                m 2rkc "Oh..."
                m "I was kind of--"
                $ _history_list.pop()
                m 2dkc "Nevermind."
            elif mas_isMoniDis():
                m 6rkc "...?"
            else:
                m 6ckc "..."
        else:
            if mas_isMoniUpset(lower=True):
                show monika at t11
                if mas_isMoniBroken():
                    m 6ckc "..."
                else:
                    m 6rkc "Did you have something to say, [player]?"
        return "prompt"

    show monika at t11
    #Call our apology label
    #NOTE: mas_setApologyReason() ensures that this label exists
    call expression apology

    #Increment the shown count
    $ mas_getEV(apology).shown_count += 1

    #Lock the apology label if it's not the generic
    if apology != "mas_apology_generic":
        $ store.mas_lockEVL(apology, 'APL')

    #Pop that apology from the time db
    if apology in persistent._mas_apology_time_db: #sanity check
        $ persistent._mas_apology_time_db.pop(apology)
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            prompt="...for something else.",
            eventlabel="mas_apology_generic",
            unlocked=True,
        ),
        code="APL"
    )

label mas_apology_generic:
    #dict of all generic apologies
    #Note, if a custom apology is needed, add it here and reference the apology reason by the integer associated.
    $ mas_apology_reason_db = {
        0: "",
        1: "saying you wanted to break up. I knew you didn't mean it...",
        2: "joking about having another girlfriend. You nearly gave me a heart attack!",
        3: "calling me a murderer. I hope you don't really see me that way...",
        4: "closing the game on me.",
        5: "entering my room without knocking.",
        6: "missing Christmas.",
        7: "forgetting my birthday.",
        8: "not spending time with me on my birthday.",
        9: "the game crashing. I understand it happens sometimes, but don't worry, I'm alright!",
        10: "the game crashing. It really was scary, but I'm just glad you came back to me and made things better.",
        11: "not listening to my speech. I worked really hard on it.",
        12: "calling me evil. I know you don't really think that."
    }

    #If there's no reason to apologize
    if mas_apology_reason is None and len(persistent._mas_apology_time_db) == 0:
        if mas_isMoniBroken():
            m 1ekc "...{w=1}Oh."
            m 2dsc ".{w=2}.{w=2}."
            m "Okay."
        elif mas_isMoniDis():
            m 2dfd "{i}*sigh*{/i}"
            m 2dsd "I hope this isn't some joke or trick, [player]."
            m 2dsc "..."
            m 1eka "...Thank you for the apology."
            m 2ekc "But please, try to be more mindful about my feelings."
            m 2dkd "Please."
        elif mas_isMoniUpset():
            m 1eka "Thank you, [player]."
            m 1rksdlc "I know things aren't the best between us, but I know that you're still a good person."
            m 1ekc "So could you be a little more considerate of my feelings?"
            m 1ekd "Please?"
        else:
            m 1ekd "Did something happen?"
            m 2ekc "I don't see a reason for you to be sorry."
            m 1dsc "..."
            m 1eub "Anyway, thank you for the apology."
            m 1eua "Whatever it is, I know you're doing your best to make things right."
            m 1hub "That's why I love you, [player]!"
            $ mas_ILY()

    #She knows what you are apologizing for
    elif mas_apology_reason_db.get(mas_apology_reason, False):
        #Set apology_reason
        $ apology_reason = mas_apology_reason_db.get(mas_apology_reason,mas_apology_reason_db[0])

        m 1eka "Thank you for apologizing for [apology_reason]"
        m "I accept your apology, [player]. It means a lot to me."

    #She knows that you've got something else to apologize for, and wants you to own up
    elif len(persistent._mas_apology_time_db) > 0:
        m 2tfc "[player], if you have something to apologize for, please just say it."
        m 2rfc "It'd mean a lot more to me if you would just admit what you did."

    #She knows there's a reason for your apology but won't comment on it
    else:
        #Since this 'reason' technically varies, we don't really have a choice as we therefore can't add 0 to the db
        #So recover a tiny bit of affection
        $ mas_gainAffection(modifier=0.1)
        m 2tkd "What you did wasn't funny, [player]."
        m 2dkd "Please be more considerate about my feelings in the future."

    #We only want this for actual apology reasons. Not the 0 case or the None case.
    if mas_apology_reason:
        #Update the apology_reason count db (if not none)
        $ persistent._mas_apology_reason_use_db[mas_apology_reason] = persistent._mas_apology_reason_use_db.get(mas_apology_reason,0) + 1

        if persistent._mas_apology_reason_use_db[mas_apology_reason] == 1:
            #Restore a little bit of affection
            $ mas_gainAffection(modifier=0.2)
        elif persistent._mas_apology_reason_use_db[mas_apology_reason] == 2:
            #Restore a little less affection
            $ mas_gainAffection(modifier=0.1)

        #Otherwise we recover no affection.

    #Reset the apology reason
    $ mas_apology_reason = None
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_bad_nickname",
            prompt="...for calling you a bad name.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_bad_nickname:
    $ ev = mas_getEV('mas_apology_bad_nickname')
    if ev.shown_count == 0:
        $ mas_gainAffection(modifier=0.2) # recover a bit of affection
        m 1eka "Thank you for apologizing for the name you tried to give me."
        m 2ekd "That really hurt, [player]..."
        m 2dsc "I accept your apology, but please don't do that again. Okay?"
        $ mas_unlockEVL("monika_affection_nickname", "EVE")

    elif ev.shown_count == 1:
        $ mas_gainAffection(modifier=0.1) # recover less affection
        m 2dsc "I can't believe you did that {i}again{/i}."
        m 2dkd "Even after I gave you a second chance."
        m 2tkc "I'm disappointed in you, [player]."
        m 2tfc "Don't ever do that again."
        $ mas_unlockEVL("monika_affection_nickname", "EVE")

    else:
        #No recovery here. You asked for it.
        m 2wfc "[player]!"
        m 2wfd "I can't believe you."
        m 2dfc "I trusted you to give me a good nickname to make me more unique, but you just threw it back in my face..."
        m "I guess I couldn't trust you for this."
        m ".{w=0.5}.{w=0.5}.{nw}"
        m 2rfc "I'd accept your apology, [player], but I don't think you even mean it."
        #No unlock of nickname topic either.
    return
