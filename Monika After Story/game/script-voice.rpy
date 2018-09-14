#This park is responsible for voice recognition using Google API for now
#Probably need reaction of Monica when she hear you first time and either we can hump to topic
#or create new replays depended on player key words
#Also someone need to change all Monika dialouge cus I can't write.

default global_path = config.basedir 

init -1 python:
    import sys
    base_path = config.basedir  # directory of the current module file, where all the FLAC bundled binaries are stored
    base_path += "\\game\\python-packages\\speech_recognition"
    sys.path.append(base_path)
    try:
        import _portaudio
    except ImportError:
        raise Exception('Fail importing _portaudio')
    import speech_recognition as sr
    sr.path_to_game_dir = config.basedir

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_hear_voice',
                                                            prompt="I want to tell you something",
                                                            label=None,
                                                            category=['misc'],
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
                        player_input_text = r.recognize_google(audio)
                    except Exception:
                        renpy.jump("can_hear_but_cant_recognise")
                player_input_text = player_input_text.lower()
                player_input_text = player_input_text.replace("monica", "monika")
        "No.":
            m "Maybe next time"
            return

#Here we can write logic to catch key words which than would jump into correct topics or do other stuff
#currently it check if what player said is contain in prompt of event. Probably need be other way around or add key words to event which we will catch in player text
    python:
        if player_input_text is not None:
            import store.evhand as evhand
            unlocked_events = Event.filterEvents(evhand.event_database, unlocked=True)
            for key in unlocked_events:
                temp = unlocked_events[key].prompt
                temp = temp.lower()
                if player_input_text in temp:
                    renpy.jump(unlocked_events[key].eventlabel)
            renpy.jump("what_player_said")

label cant_hear:
    m 1eua "[player], I thought you wanted to tell me something"
    m 1eua "But I didn't hear anything"
    return   

label can_hear_but_cant_recognise:
    m 1eua "I heard what you said [player]"
    m 1eua "However I couldn't understand it"
    return      
            
label what_player_said:
    m 1hub "[player], did you just say %(player_input_text)s?"
    m 1hub "I am not really sure how should I react to that"
    return   