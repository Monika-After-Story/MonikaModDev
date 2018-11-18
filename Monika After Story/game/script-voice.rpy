#This park is responsible for voice recognition using Google API for now
#Probably need reaction of Monica when she hear you first time and either we can hump to topic
#or create new replays depended on player key words
#Also someone need to change all Monika dialouge cus I can't write.

default global_path = config.basedir 
default disable_voice_option = None

init -1 python:
    import sys
    base_path = config.basedir  # directory of the current module file, where all the FLAC bundled binaries are stored
    sys.path.append(base_path + "/game/python-packages/speech_recognition")
    sys.path.append(base_path + "/game/python-packages/sphinxbase")
    sys.path.append(base_path + "/game/python-packages/pocketsphinx")
    disable_voice_option = False
    try:
        import _portaudio
        import speech_recognition as sr
        sr.path_to_game_dir = base_path + "/game/python-packages/speech_recognition"
    except ImportError:
        disable_voice_option = True #pass #raise Exception('Fail importing _portaudio')


init 5 python:
    if disable_voice_option == False:
        addEvent(Event(persistent.event_database,eventlabel='monika_hear_voice',
                                                                prompt="Monika, listen to me",
                                                                label=None,
                                                                category=['voice'],
                                                                random=False,
                                                                unlocked=False,
                                                                pool=False,
                                                                conditional=None,
                                                                action=None,
                                                                start_date=None,
                                                                end_date=None,
                                                                unlock_date=None
                                                                ))

label monika_hear_voice:
    $ mas_RaiseShield_dlg()
    m 1eua "[player], would you like to tell me something?"
    menu:
        "Yes.":
            m 1hub "It might lag game a little for time when I will try to hear your gently voice"
            m 1eua "I'm all ears but please keep it to one sentance for now. I am still learning how to do it after all"
            python:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    try:
                        audio = r.listen(source)
                    except WaitTimeoutError:
                        renpy.jump("cant_hear")
                    try:
                        player_input_text = r.recognize_sphinx(audio)
                        #player_input_text = r.recognize_google(audio)
                    except Exception:
                        renpy.jump("can_hear_but_cant_recognise")
                player_input_text = player_input_text.lower()
                player_input_text = player_input_text.replace("monica", "monika")
                renpy.jump(return_topic(player_input_text))
                
        "No.":
            m "Maybe next time"
            $ mas_DropShield_dlg()
            return

#Here we can write logic to catch key words which than would jump into correct topics or do other stuff
init -1 python:
    def return_topic(player_input_text):
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
            elif "bye" in player_input_text or "goodbye" in player_input_text or ("good" in player_input_text and "night" in player_input_text):
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
                                    counterFitNumber += float(keyWord[1])
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
                return "no_topic_found" 
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
            if "piano" in player_input_text:
                if not renpy.seen_label("mas_piano_start"):
                    grant_xp(xp.NEW_GAME)
                return "mas_piano_start"
                
                
label cant_hear:
    m 1eua "[player], I thought you wanted to tell me something"
    m 1eua "But I didn't hear anything"
    return   

label can_hear_but_cant_recognise:
    m 1eua "I heard what you said [player]"
    m 1eua "However I couldn't understand it"
    return      
            
label no_topic_found:
    m 1hub "[player], did you just say %(player_input_text)s?"
    m 1hub "I am not really sure how should I react to that"
    return   

#/////////////////////////////////ALWAYS LISTEN OPTION//////////////////////////////////////////////////////
#Spawning knew thread which will listen mic input all the time. Causing some issues for now, ewsspecially when you use both this and ask option. Both option add event so Monika repeat it.    
#init 5 python:
#    addEvent(Event(persistent.event_database,eventlabel='monika_listen',
#                                                            prompt="Monika listen to me",
#                                                            label=None,
#                                                            category=['voice'],
#                                                            random=False,
#                                                            unlocked=False,
#                                                            pool=False,
#                                                            conditional=None,
#                                                            action=None,
#                                                            start_date=None,
#                                                            end_date=None,
#                                                            unlock_date=None
#                                                            ))

label monika_listen:
    m 1eua "[player], would you like me to listen to you all the time?"
    menu:
        "Yes.":
            m "Okay"
            python:
                r = sr.Recognizer()
                mic = sr.Microphone()
                Monika_is_listening = True
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                stop_listening = r.listen_in_background(mic, callback)
            return
        "No.":
            m "Okay"
            python:
                Monika_is_listening = False
                if stop_listening is not None:
                    stop_listening(wait_for_stop=False)
            return

init -1 python:
    def callback(recognizer, audio):
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            #player_voice = recognizer.recognize_google(audio)
            player_voice = recognizer.recognize_sphinx(audio)
            temp = return_topic(player_voice)
            if temp != "No_topic_found":
                pushEvent(temp)
            
        except sr.UnknownValueError as e:
            pass
        except sr.RequestError as e:
            pass       