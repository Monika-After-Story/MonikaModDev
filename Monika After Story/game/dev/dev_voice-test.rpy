init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_monika_voice_recognition_check",
            category=["dev"],
            prompt="Voice recognition CHECK",
            pool=True,
            unlocked=True
        )
    )

label dev_monika_voice_recognition_check:
    $ mas_RaiseShield_dlg()
    m 1esa  "I will perform tests for voice recognition [player]..."
    m 4esa  "Let's start with checking all the nessesary liberies "
    python:
        error_message = None
        try:
            import _portaudio
        except ImportError as e:
            error_message = e
            renpy.jump("no_found_portaudio")
        try:
            import speech_recognition as sr
            sr.path_to_game_dir = base_path + "/game/python-packages/speech_recognition"
            r = sr.Recognizer()
        except ImportError as e:
            error_message = e
            renpy.jump("no_found_portaudio")
            
    m 1esa "Everything seems to works fine for now, [player]"
    m "Let's continue with checking if you have any microphone is set up correctly."
    python:
        try:
            mic = sr.Microphone()
        except Exception as e:
            error_message = e
            renpy.jump("No_inpu_device") 

    m 1esa "So far so good"
    m  "Time to check if I can hear and understand you."
    m "Which feature would you like to test?"
    menu:
        "GOOGLE API":
            m 1eua "Okay, let's test Pocketsphinx than"
            m  "[player] you can start talking after this box but please keep it to one sentance for now. I am still learning how to do it after all"
            python:
                with sr.Microphone() as source:
                    try:
                        audio = r.listen(source)
                    except WaitTimeoutError as e:
                        error_message = e
                        renpy.jump("no_input")
                try:
                    player_input_text = r.recognize_google(audio)
                except Exception as e:
                    error_message = e
                    renpy.jump("cant_recognise")
                player_input_text = player_input_text.lower()
                player_input_text = player_input_text.replace("monica", "monika")
                topic = return_topic_test(player_input_text)
        "Pocketsphinx":
            m 1eua "Okay, let's test Pocketsphinx than"
            m  "[player] you can start talking after this box but please keep it to one sentance for now. I am still learning how to do it after all"
            python:
                with sr.Microphone() as source:
                    try:
                        audio = r.listen(source)
                    except WaitTimeoutError as e:
                        error_message = e
                        renpy.jump("no_input")
                try:
                    player_input_text = r.recognize_sphinx(audio)
                except Exception as e:
                    error_message = e
                    renpy.jump("cant_recognise")
                player_input_text = player_input_text.lower()
                player_input_text = player_input_text.replace("monica", "monika")
                topic = return_topic_test(player_input_text)
    m 1hub "[player], I heard that you said %(player_input_text)s. And I think best fitting topic would be %(topic)s. Am I correct?"
    menu:
        "Yes.":
            m 1hub "Everything works correctly than. I am really glad I can hear your voice [player] !"
            $ mas_DropShield_dlg()
            return
        "No.":
            m 1eua "I am sorry. I try my best. Maybe next time I would hear you better"
            $ mas_DropShield_dlg()
            return
            
label no_input:
    m 1eua "[player], I couldn't hear anything"
    m  "Is your mic work correctly?"
    m "Perhaps it would be good idea to check the voice.log file"
    python:
        file = open(base_path+"/log/voice.log", 'w')
        file.write("Error message: " + str(error_message))
        file.close()
        mas_DropShield_dlg()
    return   

label cant_recognise:
    m 1eua "I heard what you said [player]"
    m  "However I couldn't understand it"
    m "Perhaps it would be good idea to check the voice.log file"
    python:
        file = open(base_path+"/log/voice.log", 'w')
        file.write("Error message: " + str(error_message))
        file.close()
        mas_DropShield_dlg()
    return      
             
label no_found_portaudio:
    m 1eua  "[player], I can't seem to find portaudio libery"
    m "Be a sweetheart and check if you have it installed <3"
    m "Perhaps it would be good idea to check the voice.log file"
    python:
        file = open(base_path+"/log/voice.log", 'w')
        file.write("Error message: " + str(error_message))
        file.close()
        mas_DropShield_dlg()
    return
    
label no_found_speech_recognition:
    m 1eua  "I couldn't found speech_recognition libery. It shouldn't ever happen. Are you 100% sure you copy all the nessesary file to a game folder [player]?"
    m "or are you playing pranks on me?"
    m "Perhaps it would be good idea to check the voice.log file"
    python:
        file = open(base_path+"/log/voice.log", 'w')
        file.write("Error message: " + str(error_message))
        file.close()
        mas_DropShield_dlg()
    return
    
       
label No_inpu_device:
    m 1eua "[player], I couldn't find any voice input device which you could use to communicate with me"
    m "I wonder how did you wanted to tell me something without any microphone."
    m "Perhaps it would be good idea to check the voice.log file"
    python:
        file = open(base_path+"/log/voice.log", 'w')
        file.write("Error message: " + str(error_message))
        file.close()
        mas_DropShield_dlg()
    return
    
    
#//////////////////////////////Finding right topic algorythm////////////////////////////////////
#Function that find most fitting topic base on the return of text from pocketsphyinx
init -1 python:
    def return_topic_test(player_input_text):
        unlocked_events = []
        #Check if we even have any text
        if player_input_text is not None:
            #Get all unluck events
            import store.evhand as evhand
            import store.mas_moods as mas_moods
            import store.mas_compliments as mas_compliments
            mostFitTopic = ""
            currentMaxFitNumber = 0
            #exclusive words for filtering right event 
            #We add all events to the array (as each events have separate database dicts)
            if "play" in player_input_text and ("chess" in player_input_text or "pong" in player_input_text or "hangman" in player_input_text or "piano" in player_input_text):
                return preprocessing_games()     
            elif "change" in player_input_text and "music" in player_input_text:  
                select_music()
                return "ch30_loop"  
            elif "feel" in player_input_text:
                unlocked_events.append(Event.filterEvents(mas_moods.mood_db, unlocked=True))
            elif "bye" in player_input_text or "goodbye" in player_input_text or "goodnight" in player_input_text:
                mostFitTopic = "random_farewell"
                unlocked_events.append(Event.filterEvents(evhand.farewell_database, unlocked=True, pool=True))
            else:
                unlocked_events.append(Event.filterEvents(evhand.event_database, unlocked=True))
                unlocked_events.append(Event.filterEvents(mas_compliments.compliment_database, unlocked=True))
            #Calculate fit for each unluck event in each dict.
            for event in unlocked_events:
                for key in event:
                    counterFitNumber = 0
                    temp = event[key].key_words
                    #Check event has any key_words
                    if temp != "":
                        temp = temp.lower()
                        temp = temp.split(" ")
                        #Check if the individual key words of topic is in the text from pocketsphyinx
                        for keyWord in temp:
                            keyWord = keyWord.split("_")
                            #If word is found add it's weight to the current topic weight
                            if len(keyWord) > 1:
                                if keyWord[0] in player_input_text:
                                    counterFitNumber += int(keyWord[1])
                    #Check if current topic weight is bigger than end Topic weight
                    if currentMaxFitNumber < counterFitNumber:
                        mostFitTopic = event[key].eventlabel
                        currentMaxFitNumber = counterFitNumber
            #Create and put to log what text from pocketsphyinx we got 
            file = open(base_path+"/log/what_Monika_heard.log", 'w')
            file.write("This is player input - " + player_input_text + " / Most fitting topic based on player input: " + mostFitTopic)
            file.close()
            #Return most fitting topic
            if mostFitTopic == "":
                return "No_topic_found_test" 
            else:
                return mostFitTopic

init -1 python:
    def preprocessing_games():  
        import datetime
        _hour = datetime.timedelta(hours=1)
        _now = datetime.datetime.now()

        # chess has timed disabling
        if persistent._mas_chess_timed_disable is not None:
            if _now - persistent._mas_chess_timed_disable >= _hour:
                chess_disabled = False
                persistent._mas_chess_timed_disable = None

            else:
                chess_disabled = True

        else:
            chess_disabled = False

        # single var for readibility
        chess_unlocked = (
            is_platform_good_for_chess()
            and persistent.game_unlocks["chess"]
            and not chess_disabled
        )

        # hangman text
        if persistent._mas_sensitive_mode:
            _hangman_text = "Word Guesser"
        else:
            _hangman_text = "Hangman"

        # decide the say dialogue
        play_menu_dlg = store.mas_affection.play_quip()[1]

        if persistent.game_unlocks['pong']:
            if "pong" in player_input_text:
                if not renpy.seen_label('game_pong'):
                    grant_xp(xp.NEW_GAME)
                return "game_pong"
        if chess_unlocked:
            if "chess" in player_input_text:
                if not renpy.seen_label('game_chess'):
                    grant_xp(xp.NEW_GAME)
                return "game_chess"
        if persistent.game_unlocks['hangman']:
            if "hangman" in player_input_text:
                if not renpy.seen_label("game_hangman"):
                    grant_xp(xp.NEW_GAME)
                return "game_hangman"
        if persistent.game_unlocks['piano']:
            if "Piano" in player_input_text:
                if not renpy.seen_label("mas_piano_start"):
                    grant_xp(xp.NEW_GAME)
                return "mas_piano_start"