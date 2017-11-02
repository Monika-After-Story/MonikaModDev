##This is an example scene
##It teaches you about making mods, and is also a code example itself!

#Each section needs a label, this is how we will call the scene in or parts of the script
label example_chapter:
    stop music fadeout 2.0
    
    #This set's up the scene with a background and music
    scene bg club_day
    with dissolve_scene_full
    play music t3
    
    # Most of the story will be told using "Say" statements
    # They take the form of a short nickname, follow by their statement in quotes.    
    m "...[player]?"
    
    #You will also want to show characters of other images
    show monika 1 at t11 zorder 2
    m "Ah! What a nice surprise!"

    #Character images are their name followed by a number and letters
    #The trailing letter is generally the facial expression
    show monika 1b at t11 zorder 2
    m "Welcome to the club!"
    m "The Modification Club."
    
    #The number is the pose
    show monika 3 at t11 zorder 2
    m " I started this club after I had some difficulties changing code in Doki Doki Literature Club."
    
    
    m "It turns out that bad coding can really hurt people."
    m "That's why I wanted to make this club to teach people how to mod responsibly!"
    
    m "First, you need the right template."
    m "This template you're looking at right now!"
    $ config.developer = "auto"
    if config.developer:
        m "Looks like you're ahead of me on that one."
        m "Way to take the initiative!"
    else:
        m "You can find the source for it online at https://github.com/therationalpi/DDLCModTemplate"
        m "If you haven't already, of course."
        
    m "Then you need to add files from DDLC."
    m "You'll want to put those in the /game folder of the template."
    if config.developer:
        m "Again, that's something you already know."
        m "Please let me know if I'm boring you!"
    else:
        m "Kind of like what you did to make this demo work!"
    
    m "Finally, you're going to want to download the Ren'Py SDK."
    m "That's at https://www.renpy.org/latest.html"
    if config.developer:
        m "I promise I'll get to the good stuff now."
    else:
        m "You'll be using that to write and test your scripts."
        
    m "So now that you have everything, it's time to get started!"
    m "Start by opening up your /game folder"
    m "You'll notice there aren't a lot of files in there."
    m "Most of the data we'll be using is coming from DDLC."
    m "Including all of the user interface and system coding."
    m "All you need to bring are the stories you want to tell!"
    m "Of course, if you really want to dig deep and change how the game works..."
    m "That's possible too."
    
    m "That reminds me..."
    m "I haven't asked about you or the game you want to make."
    m "How silly of me, Ahaha~!"
    
    default knows_python=False
    default knows_renpy=False
    menu:
        m "How experienced are you with coding?"
        "I'm an experienced coder":
            $experience_level = 2
            m "Really? That's very impressive!"
            m "I'm new to this, myself, so maybe I'll end up learning more from you, instead!"
        "I've coded before":
            $experience_level = 1
            m "That's good."
            m "Building a mod for DDLC should feel very natural, then!"
        "New to coding":
            $experience_level = 0
            m "Really? This should be fun then!"
            m "I'm pretty new to this myself..."
            m "So it's a little a weird for me to be someone's teacher."
            m "But I'll try my best!"
            
    if experience_level > 0:
        m "Since you've coded before, you might like to know that mods are built in renpy."
        m "It's a very popular platform for making visual novels."
        menu:
            m "Have you used Renpy before?"
            "Yes.":
                $knows_renpy = True
                m "Sounds like you're ahead of the game, then."
            "No.":
                m "Well, don't worry about that."
                m "Renpy is actually very easy once you get used to it."
        
        m "For more advanced coding, python might be necessary."
        m "Renpy is actually built with Python..."
        m "So the sky's the limit for modding if you know how to use it!"
        menu:
            m "Are you familiar with python?"
            "Yes.":
                $knows_python = True
                if not knows_renpy:
                    m "That might help you pick up renpy a little quicker, then."
                    m "But there are some things that makes Renpy's python a bit different."
                    m "I'll try to call them out when they come up."
                else:
                    m "Sounds like you're in great shape for this!"
                    m "You have all the skills you need to make whatever you want."
                    m "I'm excited to see what you come up with."
            "No.":
                if not knows_renpy:
                    m "Well, any coding experience will help a lot."
                    m "Python is made to be an easy language to pick up, after all."
                else:
                    m "Don't sell yourself short, [player]."
                    m "I'm sure you picked up a few tricks from Renpy already."
                    m "But I'll be sure to share a few I've picked up with you, too."            
                
    m "Now, about the mod you want to make."
    m "How difficult of a project is it going to be?"
    m "Is it mostly going to be standard scripts with a few choices and special effects..."
    m "...or will you be creating lots of new systems to really change the game?"
    menu:
        m "Will this be a basic or advanced project?"
        "Basic.":
            $advanced = False
            m "Starting off with something simple?"
            m "I think that's a good way to go."
            m "Making a simple script is a lot like writing a play."
            m "But the actors are us characters, and we'll always do just what you direct from us..."
            m "..for better or worse."
        "Advanced.":
            $advanced = True
            m "Trying for something a little more complicated?"
            m "Well, I'll try to share all the tools I have with you."
            m "Hopefully you'll find what you need to make your perfect game!"
    
    return