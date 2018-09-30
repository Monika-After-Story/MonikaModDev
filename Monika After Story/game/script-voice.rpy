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
                                                                prompt="I want to tell you something",
                                                                label=None,
                                                                category=['voice'],
                                                                random=False,
                                                                unlocked=True,
                                                                pool=False,
                                                                conditional=None,
                                                                action=None,
                                                                start_date=None,
                                                                end_date=None,
                                                                unlock_date=None
                                                                ))

label monika_hear_voice:
    m 1eua "[player], would you like to tell me something?"
    menu:
        "Yes.":
            m 1hub "It might lag game a little for time when i will try to hear your gently voice but don't worry about it"
            m 1eua "I\'m all ears but please keep it to one sentance for now. I am still learning how to do it after all"
            python:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    try:
                        audio = r.listen(source)
                    except WaitTimeoutError:
                        renpy.jump("cant_hear")
                    try:
                        #player_input_text = r.recognize_google(audio)
                        player_input_text = r.recognize_sphinx(audio)
                    except Exception:
                        renpy.jump("can_hear_but_cant_recognise")
                player_input_text = player_input_text.lower()
                player_input_text = player_input_text.replace("monica", "monika")
                renpy.jump(return_topic(player_input_text))
                
        "No.":
            m "Maybe next time"
            return

#Here we can write logic to catch key words which than would jump into correct topics or do other stuff
#currently it check if what player said is contain in prompt of event. Probably need be other way around or add key words to event which we will catch in player text
init -1 python:
    def return_topic(player_input_text):
        mas_DropShield_dlg()
        if player_input_text is not None:
            import store.evhand as evhand
            lowWeightWordList = ["monika", "i", "and", "or", "a", "an", "love", "why", "me", "of", "to", "is", "was", "for", "in", "be", "me", "the", "do", "does", "did", "you", "your", "have", "has", "too", "like", "can", "could", "how", "what", "where", "when", "will", "tell", "told",  "being", " ", "" ]
            unlocked_events = Event.filterEvents(evhand.event_database, unlocked=True)
            if "love you" in player_input_text or "love monika" in player_input_text:
                return "monika_love"
            mostFitTopic = ""
            currentMaxFitNumber = 0
            for key in unlocked_events:
                counterFitNumber = 0
                temp = unlocked_events[key].prompt
                temp = temp.lower()
                temp = temp.split(" ")
                for keyWord in temp:
                    #Delete special characters like ? ! ' in kew word
                    keyWord = ''.join(e for e in keyWord if e.isalnum())
                    #Check the weight value of the words
                    weight = 1
                    for word in lowWeightWordList:
                        if keyWord == word:
                            weight = 0
                    if weight == 1:
                        if keyWord in player_input_text:
                            counterFitNumber += weight
                if currentMaxFitNumber < counterFitNumber:
                    mostFitTopic = unlocked_events[key].eventlabel
                    currentMaxFitNumber = counterFitNumber
            file = open(base_path+"/log/what_Monika_heard.log", 'w')
            file.write("This is player input - " + player_input_text + " / Most fitting topic based on player input: " + mostFitTopic)
            file.close()
            if mostFitTopic == "":
                return "No_topic_found" 
            else:
                return mostFitTopic
                
label cant_hear:
    m 1eua "[player], I thought you wanted to tell me something"
    m 1eua "But I didn't hear anything"
    return   

label can_hear_but_cant_recognise:
    m 1eua "I heard what you said [player]"
    m 1eua "However I couldn't understand it"
    return      
            
label No_topic_found:
    m 1hub "[player], did you just say %(player_input_text)s?"
    m 1hub "I am not really sure how should I react to that"
    return   

#/////////////////////////////////ALWAYS LISTEN OPTION//////////////////////////////////////////////////////
    
init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_listen',
                                                            prompt="Monika listen to me",
                                                            label=None,
                                                            category=['voice'],
                                                            random=False,
                                                            unlocked=True,
                                                            pool=False,
                                                            conditional=None,
                                                            action=None,
                                                            start_date=None,
                                                            end_date=None,
                                                            unlock_date=None
                                                            ))

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
    import _portaudio
    import speech_recognition as sr
    def callback(recognizer, audio):
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            player_voice = recognizer.recognize_google(audio)
            temp = return_topic(player_voice)
            if temp != "No_topic_found":
                pushEvent(temp)
            
        except sr.UnknownValueError as e:
            pass
        except sr.RequestError as e:
            pass    
