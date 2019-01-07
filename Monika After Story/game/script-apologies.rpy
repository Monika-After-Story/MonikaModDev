#Create an apology db for storing our times
default persistent._mas_apology_time_db = {}
#going to need this post ev_handler init

init 20 python:
    def mas_checkApologies():
        #Let's not do extra work
        if persistent._mas_apology_time_db == {}:
            return

        #Calculate the current total playtime to compare...
        current_total_playtime = persistent.sessions['total_playtime'] + (datetime.datetime.now() - persistent.sessions['current_session_start'])

        #Iter thru the stuffs in the apology time tb
        for ev, td in persistent._mas_apology_time_db.items():
            if current_total_playtime >= td:
                #Pop the ev_label from the time db and lock the event label. You just lost your chance
                lockEventLabel(ev)
                del persistent._mas_apology_time_db[ev]

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
    #Run through our apology db and find what's unlocked
    python:
        apologylist = [(mas_getEV(ev).prompt,ev,False,False) for ev in persistent.apology_database if mas_getEV(ev).unlocked]

        #The back button
        return_prompt_back = ("Nevermind", False, False, False, 20)

        #renpy.say(m, "What are you apologizing for?", interact=False)

    #Display our scrollable
    show monika at t21
    call screen mas_gen_scrollable_menu(apologylist,(evhand.UNSE_X, evhand.UNSE_Y, evhand.UNSE_W, 500), evhand.UNSE_XALIGN, return_prompt_back)
    show monika at t11

    #Handle backing out
    if not _return:
        if mas_apology_reason is not None or persistent._mas_apology_time_db != {}:
            m 2rkc "Oh..."
        else:
            m 1eka "I'm not sure what you wanted to apologize for, but I'm sure that it was nothing."
        return


    #Call our apology label
    call _return

    #Lock the apology label again
    $ lockEventLabel(_return)
    #Pop that apology from the timedb
    if _return in persistent._mas_apology_time_db: #sanity check
        $ persistent._mas_apology_time_db.pop(_return)
    return

init 5 python:
    addEvent(
        Event(
            persistent.apology_database,
            prompt="...for something else.",
            eventlabel="mas_apology_generic",
            unlocked=True,
        )
    )

label mas_apology_generic:
    # if there's no reason to apologize
    if mas_apology_reason is None:
        m 1ekd "Did something happen?"
        m 2ekc "I see no reason for you to be sorry."
        m 1dsc "..."
        m 1eub "Anyway, thank you for the apology."
        m 1eua "Whatever it is, I know you're doing your best to make things right."
        m 1hub "That's why I love you, [player]!"
    # She knows why you are apologizing for
    elif mas_apology_reason:
        $ mas_gainAffection(modifier=0.2) # recover a bit of affection
        m 1eka "Thank you for apologizing for [mas_apology_reason]"
        m "I accept your apology, [player]. It means a lot to me."
    # She knows there's a reason for your apology but won't comment on it
    else:
        $ mas_gainAffection(modifier=0.1) # recover a bit of affection
        m 2tkd "What you did wasn't funny, [player]."
        m 2dkd "Please be more considerate about my feelings in the future."

    #Reset the apology reason
    $ mas_setApologyReason(None)
    return

init 5 python:
    addEvent(
        Event(
            persistent.apology_database,
            eventlabel="mas_apology_bad_nickname",
            prompt="...calling you a bad name",
            unlocked=False
        )
    )

label mas_apology_bad_nickname:
        if mas_getEV('mas_apology_bad_nickname').shown_count == 0:
            $ mas_gainAffection(modifier=0.2) # recover a bit of affection
            m 1eka "Thank you for apologizing for the name you tried to give me."
            m 2ekd "That really hurt, [player]..."
            m 2dsc "I accept your apology, but please don't do that again. Okay?"
            $ mas_unlockEventLabel("monika_affection_nickname")

        elif mas_getEV('mas_apology_bad_nickname').shown_count == 1:
            $ mas_gainAffection(modifier=0.1) # recover less affection
            m 2dsc "I can't believe you did that {i}again{/i}."
            m 2dkd "Even after I gave you a second chance."
            m 2tkc "I'm disappointed in you, [player]."
            m 2tfc "Don't ever do that again."
            $ mas_unlockEventLabel("monika_affection_nickname")

        elif mas_getEV('mas_apology_bad_nickname').shown_count == 2:
            #No recovery here. You asked for it.
            m 2wfc "[player]!"
            m 2wfd "I can't believe you."
            m 2dfc "I trusted you to give me a good nickname to make me more unique, but you just threw it back in my face..."
            m "I guess I couldn't trust you for this."
            m ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"
            m 2rfc "I'd accept your apology, [player], but I don't think you even mean it."
            #No unlock of nickname topic either.
        return
