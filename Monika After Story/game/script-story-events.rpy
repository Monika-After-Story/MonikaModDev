#This file will include story events (as it is in the name).

#An event is crated by only adding a label and adding a requirement (see comment below).
#Requirements must be created/added in script-ch30.rpy under label ch30_autoload.

label gender:
    m "...[currentuser]? So I've been thinking a bit."
    m "I've mentioned before that the "you" in the game might not reflect the real you."
    m "[currentuser], is your name a guy's name, or a girl's name?"
    menu:
        "Male":
            m "Oh?"
            m "Ehehe, I suppose that makes sense!"
            m "I never really thought much about this. Before I got to be alone with you, that is."
            m "You certainly come across as manly and confident. Not that I would have been terribly bothered if you answered differently, mind you!"
            m "Even I can be curious sometimes, you know?"
            m "Remember that I'll always love you unconditionally, [currentuser]."
            gender.persistent = "M"
        "Female":
            m "Oh?"
            m "Ehehe, I never really thought much about this. Before I got to be alone with you, that is!"
            m "I suspected it a bit from the beginning... just a little!"
            m "You give off a particular feeling of elegance and charm that's hard to capture with words..."
            m "It's very attractive, to tell you the truth!"
            m "But don't worry. Even if I might ask things like this, it's only out of curiosity."
            m "Remember that I'll always love you unconditionally, [currentuser]."
            gender.persistent = "F"
