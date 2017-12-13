# Module holding jokes that monika can tell
#

# pre stuff
init -1 python:

    # list of monika jokes
    # key -> the name of the label the joke leads to
    # value -> the joke (starter) we want to display
    monika_jokes = dict()

    # first item of the list is the caption
    # NOTE: DO NOT CHANGE
#    monika_jokes.append(("Do you know any good jokes?", None))

    def removeJoke(joke):
        #
        # Removes a joke from the monika jokes dict cleanly
        #
        # IN:
        #   joke - the joke to remove (key)
        #
        # RETURNS:
        #   the joke that was removed (or None if no removal occured)

        global monika_jokes
        return monika_jokes.pop(joke,None)

init 5 python:
    monika_jokes["joke_okidoki"] = "Doki Doki is not Oki Doki"

label joke_okidoki:
    m "Ahaha, what makes you say that?"
    m "Sure, maybe the events that lead up to this point weren't exactly 'oki doki'..."
    m "But it's not like it wasn't worth it in the end, right?"    
    m "I mean, take a glance at the bright side of our situation, [player]."
    m "For instance, since you're here, and I'm here, that means we're both together!"
    m "Since we love each other so much, I hope you can understand the lengths I had to go to even reach this point..."
    # joke removal test
    $ removeJoke("joke_okidoki")
    return


init 5 python:
    monika_jokes["joke_cantopener"] = "What do you call a broken can opener?"

label joke_cantopener:
    m "Well, I'm not sure!"
    m "Maybe something like a bro{i}kan{/i} opener? Ehehe~" # Amber proud lol
    m "..."
    m "Ahaha, there's no way you'd come up with something that corny..."
    menu:
        m "Gosh, just lay it on me already! The anticipation is killing me, [player]!"
        "A can't opener!":
            m "I... I didn't think it was possible to think up such a terrible joke."
            m "[player], you do understand how the concept of humor works, right?"
            m "You can't just rely on such simple-minded methods of comedy and expect a positive response."  
            m "There needs to be a proper punchline to your joke, and a little less reliant on wordplay."
            m "Having the build up to the actual punchline is really important, too."
            m "If you tell it too early, it might lack the comedic impact..."
            m "However, if you tell it too late, interest might deteriorate and when the joke does come, it might be totally lost on the listener."
            m "And ultimately, if your joke is too simple and predictable, it will simply lack the impact that a good and memorable joke has to offer."
            m "Ah, I'm sorry if that came off as a little harsh, [player]."
            m "I only want to help you improve, after all."
            m "I'm sure your next joke will be great! Ehehe~"
    $ removeJoke("joke_cantopener")
    return

init 5 python:
    monika_jokes["joke_threewishes"] = ("Three guys, who are stranded on an "+
        "island, find a magic lantern which contains a genie, who will grant "+
        "three wishes.")

label joke_threewishes:
    m "Oh, what things will they wish for I wonder?"
    m "I bet the first thing will be to get off of the island."
    m "I wish I knew a genie who could get me out of here..."
    menu:
        m "Now, what do they wish for?"
        "The first guy wishes for a way off the island, the second guy wishes for the same as the first guy...":
            m "Ah, I was right!"
            m "That was a bit predictable [player], you know?"
            m "I really hope the punchline is good."
            m "I'm expecting great things..."
            menu:
                m "Now, how does it end?"
                "Finally, the third guy says: 'I'm lonely. I wish my friends were back here.'":
                    m "Ahaha, that was actually pretty funny, [player]."
                    m "I'm even impressed as to how well you set that joke up."
                    m "A comedian too? Now I have even more reasons to love you!"
                    m "..."
                    m "Have I mentioned how happy I am to be here with you?"
    $ removeJoke("joke_threewishes")
    return

init 5 python:
    monika_jokes["joke_sayorihobby"] = ("What would have been Sayori's " +
    "favorite hobby?")

label joke_sayorihobby:
    m "I think she's quite good at art, and probably enjoyed it a lot!"
    m "You might have your doubts, though, due to that... depiction of her dangling from that rope..."
    m "But, since her and I worked together on the festival banners, I was able to see how enthusiastic and how skillful she was."
    m "I'm sure, aside from her little arts and crafts, she spent most of her time reading and writing."
    m "I mean, besides her whole state of constantly being depressed, and stuff..."
    menu:
        m "Now [player], what {i}was{/i} Sayori's favorite hobby?"
        "Bungee jumping!":
            m "...Wow"
            m "[player], I didn't think you enjoyed those kinds of jokes."
            m "I know she wasn't exactly real like you and I, but she was still my friend."
            m "That joke just feels a bit too far, you know?"
            m "Gruesomely reminding me of all that happened with Sayori..."
            m "Gosh, I can't believe you would do something like that [player]!"
            m "Unless that wasn't your intention..."
            m "I'll give you benefit of the doubt, because I love you so much, but please try to cut down on these kinds of jokes from now on."
    $ removeJoke("joke_sayorihobby")
    return
