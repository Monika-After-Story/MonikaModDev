#This file will include short story events that don't require their own file.

#An event is crated by only adding a label and adding a requirement (see comment below).
#Requirements must be created/added in script-ch30.rpy under label ch30_autoload.

label gender:
    m "...[currentuser]? So I've been thinking a bit."
    m "I've mentioned before that the 'you' in the game might not reflect the real you."
    m "But I guess I had just assumed that you were probably a guy."
    m "The main character was, after all."
    m "But if I'm going to be your girlfriend, I should probably know at least this much about the real you."
    menu:
        "So, are you male or female?"
        "Male.":
            $persistent.gender = "M"
            call set_gender
            m "Oh? So you {i}are{/i} a [guy]?"
            m "Ehehe, I suppose that makes sense!"
            m "Not a lot of girls would play a game like this."
            m "You certainly come across as manly and confident. Not that I would have been terribly bothered if you answered differently, mind you!"
            m "Even I can be curious sometimes, you know?"
        "Female.":
            $persistent.gender = "F"
            call set_gender
            m "Oh? So you're actually a [guy]?"
            m "I hope I didn't say anything to offend you before!"
            m "Though I did suspect it a bit from the beginning... just a little!"
            m "You give off a particular feeling of elegance and charm that's hard to capture with words..."
            m "It's very attractive, to tell you the truth!"
            m "But don't worry. Even if I might ask things like this, it's only out of curiosity."
        "Neither.":
            $persistent.gender = "X"
            call set_gender
            m "You don't see yourself as a guy or a girl?"
            m "That's very interesting, but I can sort of relate."
            m "Like, I am a girl, but I'm also a character in a computer game..."
            m "So in some ways I'm not really a girl at all."
            m "But when you treat me like your girlfriend, it makes me really happy!"
            m "So I'll treat you however you want to be treated."
            m "Because your happiness is the most important thing to me."

    m "Remember that I'll always love you unconditionally, [currentuser]."
