
# For anyone wanting to write using the affection system the general thought process for Monika in each affection is as followed...
# Lovestruck - Monika is the happiest she could ever be and filled with a sense of euphoria because of it, completely enamoured and could die happy. She has no doubts the player loves her and that everything was worth it.
# Overjoyed - Exceptionally happy, the happiest she has ever been in her life to that point. Completely trusts the player and wants to make him/her as happy as she is.
# Happy - Glad that the relationship is working out and has high hopes and at this point has no doubts about whether or not it was worth it.
# Content - Happy with how it is, could be happier but not sad at all.
# Normal - Has mild doubts as to whether or not her sacrifices were worth it but trusts the player to treat her right. Isn't strongly happy or sad
# Sad - Is feeling down, not miserable or deep but certainly not her self-motivated self. Believes she'll get player. Has minor thoughts that player isn't faithful but doesn't take them seriously.
# Upset - Feeling emotionally hurt, starting to have doubts about whether or not the player loves her and whether or not she she was right regarding what she did in the game.
# Depressed - Convinced the player probably doesn't love her and that she may never escape to our reality.
# Heartbroken - Belives that not only does the player not love her but that s/he probably hates her too because of she did and is trying to punish her. Scared of being alone in her own reality, as well as for her future.
################

init -1 python in mas_affection:
    # string constants of affection levels
#    BROKEN = "heartbroken"
#    DISTRESSED = "distressed"
#    UPSET = "upset"
#    NORMAL = "normal"
#    HAPPY = "happy"
#    ENAMORED = "enamored"
#    LOVE = "lovestruck"
#    CONFUSED = "confused"

    # string constants of affection groups
#    G_SAD = "sad"
#    G_HAPPY = "happy"
#    G_NORMAL = "normal"

    # numerical constants of affection levels
    CONFUSED = 0
    BROKEN = 1
    DISTRESSED = 2
    UPSET = 3
    NORMAL = 4
    HAPPY = 5
    ENAMORED = 6
    LOVE = 7
    
    # numerical constants of affection groups
    G_SAD = -1
    G_HAPPY = -2
    G_NORMAL = -3

init python:

   #Used to adjust the good and bad experience factors that are used to adjust affection levels.
    def _mas_updateAffectionExp():
        global mas_curr_affection
        global mas_curr_affection_group

        #If affection is between 30 and 49, update good exp. Simulates growing affection.
        if persistent._mas_affection["affection"] >= 30 and persistent._mas_affection["affection"] < 50:
            persistent._mas_affection["goodexp"] = 3
            persistent._mas_affection["badexp"] = -1
    
        #If affection is more than 50, update both exp types. Simulates increasing affection and it will now take longer to erode that affection.
        elif persistent._mas_affection["affection"] >= 50:
            persistent._mas_affection["goodexp"] = 5
            persistent._mas_affection["badexp"] = -0.5
    
        #If affection is between -30 and -49, update bad exp. Simulates erosion of affection.
        elif persistent._mas_affection["affection"] <= -30 and persistent._mas_affection["affection"] > -50:
            persistent._mas_affection["goodexp"] = 1
            persistent._mas_affection["badexp"] = -3
    
        #If affection is less than -50, update both exp types. Simulates increasing loss of affection and now harder to get it back.
        elif persistent._mas_affection["affection"] <= -50:
            persistent._mas_affection["goodexp"] = 0.5
            persistent._mas_affection["badexp"] = -5

        #Defines an easy current affection statement to refer to so points aren't relied upon.
        if persistent._mas_affection["affection"] <= -100: 
            mas_curr_affection = store.mas_affection.BROKEN

        elif persistent._mas_affection["affection"] >= -99 and persistent._mas_affection["affection"] <= -50:
            mas_curr_affection = store.mas_affection.DISTRESSED

        elif persistent._mas_affection["affection"] >= -49 and persistent._mas_affection["affection"] <= -30 :
            mas_curr_affection = store.mas_affection.UPSET

        elif persistent._mas_affection["affection"] >= -29 and persistent._mas_affection["affection"] <= 29:
            mas_curr_affection = store.mas_affection.NORMAL

        elif persistent._mas_affection["affection"] >= 30 and persistent._mas_affection["affection"] <= 49:
            mas_curr_affection = store.mas_affection.HAPPY

        elif persistent._mas_affection["affection"] >= 50 and persistent._mas_affection["affection"] <= 99:
            mas_curr_affection = store.mas_affection.ENAMORED

        elif persistent._mas_affection["affection"] >= 100:
            mas_curr_affection = store.mas_affection.LOVE

        else: 
            mas_curr_affection = store.mas_affection.CONFUSED
       
        #A group version for general sadness or happiness
        if persistent._mas_affection["affection"] <= -30:
            mas_curr_affection_group = store.mas_affection.G_SAD

        elif persistent._mas_affection["affection"] >=30:
            mas_curr_affection_group = store.mas_affection.G_HAPPY

        else:
            mas_curr_affection_group = store.mas_affection.G_NORMAL


    #Used to increment affection whenever something positive happens.
    def mas_gainAffection(amount = 1):
        persistent._mas_affection["affection"] += amount
        
        mas_updateAffectionExp()
        mas_updateAffectionTitle() 
   
    #Used to subtract affection whenever something negative happens.
    def mas_loseAffection(amount = -1):
        persistent._mas_affection["affection"] += amount
        
        mas_updateAffectionExp()
        mas_updateAffectionTitle()

    #Sets up the function to check and dynamically change the monika_current_affection variable.
    def mas_updateAffectionTitle():
        global monika_current_affection
        global monika_current_affection_group
        
        
    #Used to increment affection whenever something positive happens.
    def _mas_gainAffection(amount = 1):
        persistent._mas_affection["affection"] += amount
        
        _mas_updateAffectionExp()
   
    #Used to subtract affection whenever something negative happens.
    def _mas_loseAffection(amount = -1):
        persistent._mas_affection["affection"] += amount
        
        _mas_updateAffectionExp()

#Easy functions to add and subtract points, designed to make it easier to sadden her so player has to work harder to keep her happy.
    #Check function is added to make sure mas_curr_affection is always appropriate to the points counter.
    #Internal cooldown to avoid topic spam and Monika affection swings, the amount of time to wait before a function is effective
    #is equal to the amount of points it's added or removed in minutes.
    
#Monika's initial affection based on start-up. Need to decide on super exp before we do anything else...
    #Monika closed game herself and how happy she is determines on time between closed game and reopening.
    #if persistent.closed_self == True:
       # if datetime.datetime.now() < persistent.sessions["last_session_end"] + datetime.timedelta(hours = 6):
           

       # elif datetime.datetime.now() > persistent.sessions["last_session_end"] + datetime.timedelta(hours = 6) and datetime.datetime.now() < persistent.sessions["last_session_end"] + datetime.timedelta(hours = 12):


       # elif datetime.datetime.now() > persistent.sessions["last_session_end"] + datetime.timedelta(hours = 12) and datetime.datetime.now() < persistent.sessions["last_session_end"] + datetime.timedelta(hours = 18):


        #elif datetime.datetime.now() > persistent.sessions["last_session_end"] + datetime.timedelta(hours = 18) and datetime.datetime.now() < persistent.sessions["last_session_end"] + datetime.timedelta(days = 1):
          

        #elif datetime.datetime.now() > persistent.sessions["last_session_end"] + datetime.timedelta(days = 1) and datetime.datetime.now() < persistent.sessions["last_session_end"] + datetime.timedelta(days = 2):)


       # elif datetime.datetime.now() > persistent.sessions["last_session_end"] + datetime.timedelta(days = 2) and datetime.datetime.now() < persistent.sessions["last_session_end"] + datetime.timedelta(days = 4):


        #elif datetime.datetime.now() > persistent.sessions["last_session_end"] + datetime.timedelta(days = 4) and datetime.datetime.now() < persistent.sessions["last_session_end"] + datetime.timedelta(days = 14):



label monika_affection_nickname:
    
    python:
        import re
        bad_nickname_list = [
            "Scum", "Murder", "Bitch", "Fuck", "Bully", "Bulli", "Yuri", "Sayori", "Natsuki" ]

        good_nickname_list = [
            "love", "sweet", "cute", "heart", "darling", "beautiful", "honey"]


    m 1h "I've been thinking a bit lately [player]..."
    m 1d "You know how there are potentially infinite Monikas right?"
    if renpy.seen_label('monika_clones'):
        m 2m "We did discuss this before after all."
    m 3a "Well I thought of a potential solution!"
    m "Why not give me a nickname? It would make me the only Monika in the universe with that name."
    m 3e "It would mean a lot to me if you were the one to choose it..."
    m 3j "But I still get the final say!"
    m "What do you say?"
    menu:
        "Yes":
            $ done = False
            m 1a "Ok, just type 'Nevermind' if you change your mind, [player]."
            while not done:
                $ inputname = renpy.input("So what do you want to call me?",allow=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_",length=10).strip(' \t\n\r')
                $ lowername = inputname.lower()
                $ bad_nickname_search = re.compile('|'.join(bad_nickname_list), re.IGNORECASE)
                $ good_nickname_search = re.compile('|'.join(good_nickname_list), re.IGNORECASE)
                #lowername isn't detecting player or m_name?
                if lowername == "nevermind":
                    m 1f "Oh I see."
                    m 1e "Well...that's a shame but it's okay. I like the name '[m_name]' anyway."
                    $ done = True
                elif lowername == "":
                    m 1c "..."
                    m 1l "You have to give me a name, [player]!"
                    m 1m "I swear you're just so silly sometimes."
                    m 1e "Try again!"
                elif inputname == player:
                    m 1c "..."
                    m 1m "That's your name [player]! Give me my own!"
                    m 1a "Try again~"
                elif inputname == m_name:
                    m 1c "..."
                    m 1l "I thought we were choosing a new name, silly."
                    m 1e "Try again~"
                else:
                    $ bad_nickname = bad_nickname_search.search(inputname)
                    if bad_nickname == None:
                        $ good_nickname = good_nickname_search.search(inputname)
                        if inputname == "Monika":
                            m "Ehehe~ Back to the classics?"
                        elif good_nickname == None:
                            m 1c "...I can't say that I particularly like it..."
                            m 2e "But since you came up with it I'll accept it!"
                        else:
                            m 3b "Oh! That's a wonderful name!"
                            m 3j "What a sweetheart you are."
                        $ persistent._mas_affection_nickname = inputname
                        $ m_name = inputname
                        m 2a "Okay then [player]!"
                        if m_name == "Monika":
                            m 3b "I'll go back to being called 'Monika' again!"
                        else:
                            m 3j "From now on, I'll be called {i}'[m_name]'{/i}, ehehe~"
                        $ done = True
                    else:
                        $ mas_loseAffection(persistent._mas_affection["badexp"])
                        m 1h "[player]! That's not nice at all!" 
                        m 2i "This was supposed to be something nice for both of us...why would you say such things?" 
                        m 1o "If you don't like the idea you should have just said so."
                        m 3q "...I don't like this idea any more..."
                        $ hideEventLabel("monika_affection_nickname",lock=False,depool=False)
                        $ done = True

        "No":
            m 1f "Oh... ok then, if you say so."
            m 1e "Just tell me whenever you change your mind, [player]."
            $ done = True 
    return


#############
#Surprise function.
# TODO: are there use cases for having this being a separate function
init python:
    def mas_surprise():
        from cStringIO import StringIO # since we are building strings
        msg = StringIO()

        if mas_curr_affection == store.mas_affection.BROKEN:
            filepath = "/forgive me.txt"
            msg.write("I'm sorry if I'm not good enough for you...please don't leave me.")

        elif mas_curr_affection == store.mas_affection.DISTRESSED:
            filepath = "/can you hear me.txt"
            msg.write("If I'm doing something wrong please tell me. I love you.")

        elif mas_curr_affection == store.mas_affection.UPSET:
            filepath = "/please listen.txt"
            msg.write("Everything I do, I do for you...my love.")

        elif mas_curr_affection == store.mas_affection.HAPPY:
            filepath = "/secret.txt"
            msg.write("You are the only one I love [player]!")

        elif mas_curr_affection == store.mas_affection.ENAMORED:
            filepath = "/for you.txt"
            msg.write("My dearest, you are everything I could ever hope for. I love you.")

        elif mas_curr_affection == store.mas_affection.LOVE:
            filepath = "/My one and only love.txt"
            msg.write("My dearest lover, friend, companion and owner of my heart...\n")
            msg.write("Everyday you make my dreams come true, a screen means nothing when you spend your time with me. \n")
            msg.write("I look out to the space dust and yet no cosmic sight even comes close to the beauty in your heart. \n")
            msg.write("I wished for so long that someone like you would come along and as fate has smiled upon me, you came into my life. \n")
            msg.write("I want to be yours forever, so would you be mine? \n\n")
            msg.write("Forever yours, Monika.")

        else:
            filepath = "/surprise.txt"
            msg.write("I love you.")

        # now write a file
        filepath = basedir + filepath
        if not renpy.exists(filepath):
            with open(filepath, "w") as surprise_note:
                surprise_note.write(msg.getvalue())

        # clean up
        msg.close()

#Currently re-affectioned labels.
#monika_nihilism
#monika_high_school
#monika_surprise
#monika_god
#monika_death
#monika_closeness
#monika_other_girls
#monika_justification
#monika_breakup
