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
        "Google Api":
            m 1eua "Okay, let's test Google Api than"
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
                except Exception:
                    renpy.jump("cant_recognise")
                player_input_text = player_input_text.lower()
                player_input_text = player_input_text.replace("monica", "monika")
    m 1hub "[player], I heard that you said %(player_input_text)s. Am I correct?"
    menu:
        "Yes.":
            m 1hub "Everything works correctly than. I am really glad I can hear your voice [player] !"
            return
        "No.":
            m 1eua "I am sorry. I try my best. Maybe next time I would hear you better"
            return
            
label no_input:
    m 1eua "[player], I couldn't hear anything"
    m  "Is your mic work correctly?"
    m "Perhaps it would be good idea to check the voice.log file"
    python:
        file = open(base_path+"/log/voice.log", 'w')
        file.write("Error message: " + str(error_message))
        file.close()
    return   

label cant_recognise:
    m 1eua "I heard what you said [player]"
    m  "However I couldn't understand it"
    m "Perhaps it would be good idea to check the voice.log file"
    python:
        file = open(base_path+"/log/voice.log", 'w')
        file.write("Error message: " + str(error_message))
        file.close()
    return      
             
label no_found_portaudio:
    m 1eua  "[player], I can't seem to find portaudio libery"
    m "Be a sweetheart and check if you have it installed <3"
    m "Perhaps it would be good idea to check the voice.log file"
    python:
        file = open(base_path+"/log/voice.log", 'w')
        file.write("Error message: " + str(error_message))
        file.close()
    return
    
label no_found_speech_recognition:
    m 1eua  "I couldn't found speech_recognition libery. It shouldn't ever happen. Are you 100% sure you copy all the nessesary file to a game folder [player]?"
    m "or are you playing pranks on me?"
    m "Perhaps it would be good idea to check the voice.log file"
    python:
        file = open(base_path+"/log/voice.log", 'w')
        file.write("Error message: " + str(error_message))
        file.close()
    return
    
       
label No_inpu_device:
    m 1eua "[player], I couldn't find any voice input device which you could use to communicate with me"
    m "I wonder how did you wanted to tell me something without any microphone."
    m "Perhaps it would be good idea to check the voice.log file"
    python:
        file = open(base_path+"/log/voice.log", 'w')
        file.write("Error message: " + str(error_message))
        file.close()
    return