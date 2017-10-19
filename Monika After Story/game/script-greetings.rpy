##This page holds all of the random greetings that Monika can give you after you've gone through all of her "reload" scripts

#Make a list of every label that starts with "greeting_", and use that for random greetings during startup
init python:
    greetings_list=[]
    label_list=renpy.get_all_labels()
    for label in label_list:
        if label.startswith('greeting_'):
            greetings_list.append(label)

label greeting_sweetheart:
    m "Hello again, sweetheart!"
    m "That's kind of embarassing to say out loud, isn't it?"
    m "Still, I think it's okay to be embarassed every now and then."
    return
    
label greeting_goodmorning:
    m "Good Morning!"
    m "Actually, I don't know what time it is out there."
    m "I think there's a project to fix that on the site for this mod."
    menu:
        "Do you know how to code, [player]?"
        "Yes.":
              m "Maybe you should try to fix the problem, then."
              m "It can't possibly be that hard."
        "No.":
            m "It's really not that hard, if you want to learn."
            m "In the meantime, just go to the developer's site and pester them to work on it some more."
            m "I'm sure you can do that much for me."
            
    m "Anyway, no matter what time it really is. I'm glad you're here!"
    m "Let's spend the whole day together."    
    return