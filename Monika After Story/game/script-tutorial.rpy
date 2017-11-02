label script_tutorial:

    m "Alright, now that I know more about you and your project..."
    m "The real tutorial can begin."
    m "And don't worry if you want to change your choices.."
    m "You can replay this tutorial at any time, if you want me to go more in depth or take things down a level."
    
    m "Okay, let's go back to the /game folder you opened earlier for a closer look."
    m "There are a few files in there already."
    m "Which would you like to learn about first?"
    menu:
        "splash.rpy":
            m "That seems like a good place to start."
            m "It's the first thing the player will see, after all." 
            call .splash_lesson from _call_splash_lesson
        "script.rpy":
            m "That's a good place to start."
            m "The file is pretty short, and it acts like an overview of your story!"
            call .script_lesson from _call_script_lesson
        "options.rpy":
            m "Are you the sort that likes to explore their options before a big decision?"
            m "I'm kind of like that too, sometimes."
            call .options_lesson from _call_options_lesson
        "script-example.rpy":
            m "Diving right into the thick of things, are we?"
            if experience_level == 0:
                m "That's actually a good choice for someone without a coding background."
                m "These basic scripts are less like code, and more like writing a regular story."
            elif not knows_renpy:
                m "This is probably where you'll have the most to learn."
                m "Normal scripts are almost entirely renpy commands."
                m "But you'll get the hang of it!"
            elif not advanced:
                m "This is where you'll do the bulk of your writing."
                m "So it's probably best to start learning it early."
            else:
                m "Actually, you won't have to do a lot of heavy coding in these basic scripts."
                m "But that doesn't mean they aren't important!"
            call .example_lesson from _call_example_lesson
    return
    
label .splash_lesson:
    m "The splash screen is that little thing that happens before the main menu comes up."
    m "It usually where the developer puts their logo, and any messages."
    return
            
label .script_lesson:
    m "The script file has the start label, which is called whenever the player hits the 'New Game' button."
    m "And you will probably send them back here between chapters."
    m "It's like the backbone of your story!"
    return
    
label .options_lesson:
    m "The options file let's you customize your project."
    m "While you probably won't need to change most of the settings in here."
    m "There are a few you should definitely change before you release your mod."
    return
    
label .example_lesson:
    m "The example script should look very familiar already."
    m "It's the little introduction we just finished!"
    return