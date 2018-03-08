
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

init python:

   #Used to adjust the good and bad experience factors that are used to adjust affection levels.
    def _mas_updateAffectionExp():
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

    #Used to increment affection whenever something positive happens.
    def _mas_gainAffection(amount = 1):
        persistent._mas_affection["affection"] += amount
        
        _mas_updateAffectionExp()
        _mas_updateAffectionTitle() 
   
    #Used to subtract affection whenever something negative happens.
    def _mas_loseAffection(amount = -1):
        persistent._mas_affection["affection"] += amount
        
        _mas_updateAffectionExp()
        _mas_updateAffectionTitle()

    #Sets up the function to check and dynamically change the monika_current_affection variable.
    def _mas_updateAffectionTitle():
        global monika_current_affection
        global monika_current_affection_group
        
        #Defines an easy current affection statement to refer to so points aren't relied upon.
        if persistent._mas_affection["affection"] <= -100: 
            monika_current_affection = "heartbroken"

        elif persistent._mas_affection["affection"] >= -99 and persistent._mas_affection["affection"] <= -50:
            monika_current_affection = "distressed"

        elif persistent._mas_affection["affection"] >= -49 and persistent._mas_affection["affection"] <= -30 :
            monika_current_affection = "upset"

        elif persistent._mas_affection["affection"] >= -29 and persistent._mas_affection["affection"] <= 29:
            monika_current_affection = "normal"

        elif persistent._mas_affection["affection"] >= 30 and persistent._mas_affection["affection"] <= 49:
            monika_current_affection = "happy"

        elif persistent._mas_affection["affection"] >= 50 and persistent._mas_affection["affection"] <= 99:
            monika_current_affection = "enamored"

        elif persistent._mas_affection["affection"] >= 100:
            monika_current_affection = "lovestruck"

        else: 
            monika_current_affection = "confused"

        if persistent._mas_affection["affection"] <= -30:
            monika_current_affection_group = "sad"

        elif persistent._mas_affection["affection"] >=30:
            monika_current_affection_group = "happy"

        else:
            monika_current_affection_group = "normal"

    _mas_updateAffectionExp()

#Easy functions to add and subtract points, designed to make it easier to sadden her so player has to work harder to keep her happy.
    #Check function is added to make sure monika_current_affection is always appropriate to the points counter.
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


label monika_affection_check:
    m 1c "How do I feel? That came out of nowhere, [player]..."
    m 3h "In a single word I would say I am [monika_current_affection]."
    m 3c "But if I were pressed further I would say I'm feeling..."
    if monika_current_affection == "heartbroken":
        m 1q "Like you shattered my heart..."
        m 1f "Did I do something wrong?"
  
    elif monika_current_affection == "distressed":
        m 1r "Like my situation is hopeless..."
        m 1f "I really thought we could make it work..."

    elif monika_current_affection == "upset":
        m 1f "Like you want me to be unhappy..."
        m 1g "It's not always going to be like this, is it?"

    elif monika_current_affection == "normal":
        m 1a "...completely average right now."

    elif monika_current_affection == "happy":
        m 1e "Like you really do want to please me."
        m 1k "I hope I'm making you as happy as you make me."

    elif monika_current_affection == "enamored":
        m 1b "Like I'm luckiest girl in the world!"
        m 1j "No one else could make me feel so complete!"

    elif monika_current_affection == "lovestruck":
        m 1k "So overwhelming full of love! I really truly do love you [player]!"
        m 1k "I want nothing more than you, forever and ever!"

#############
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
