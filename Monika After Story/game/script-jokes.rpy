# Module holding jokes that you can tell to monika
# as well as jokes monika tells to you
#
# TODO: add some way to do toggling of dark jokes
#   and differenetiating of dark jokes
#   
# NOTE: consider doing a tag system

# we need some persists
# dict of following format:
# "p2m": p2m_jokes dict
# "m2p": m2p_jokes list
# default persistent.monika_jokes = {}
# NOTE: If we are trying to make a label work for both monika and player, 
#   it requires some complexity added to the label, particularly two 
#   different paths. The label must have support for this.


# pre stuff
init -1 python:

    class MASJokeException(Exception):
        def __init__(self, msg):
            str.msg = msg
        def __str__(self):
            return "MASJokeError: " + self.msg

    # alright, im making this a class instead. its just easier to handle
    #
    # This class handles represntations of MASJokes and attributes
    #
    # PROPERTIES:
    #   jokelabel - the label this joke resides at (existence is checked,
    #       please only create this class post init level 5)
    #       NOTE: will raise a MASJokeException if the jokelabel doesnt exist
    #       (REQUIRED)
    #   is_m2p - True if this joke is one that monika can tell the player
    #       False means this joke is one the player tells monika
    #       NOTE: If false, Prompt is REQUIRED
    #       (Default: True)
    #   prompt - the prompt to show on the button for this joke
    #       NOTE: Only required if is_p2m is True.
    #       NOTE: Will raise a MASJokeException if None while is_m2p is False
    #   is_dark - True if this joke is a dark joke, False if not
    #       (Default: False)
    #   is_dad - True if this joke is a dad joke, False if not
    #       (Default: False)
    class MASJoke():
        def __init__(self, 
                jokelabel,
                is_m2p=True,
                prompt=None,
                is_dark=False,
                is_dad=False):

            # sanity checks
            if not jokelabel:
                raise MASJokeException("jokelabel cannot be None")
            if not renpy.has_label(jokelabel):
                raise MASJokeException("'"+jokelabel+"' does not exist")
            if not is_m2p and not prompt:
                raise MASJokeException("prompt cannot be None")

            self.jokelabel = jokelabel
            self.is_m2p = is_m2p
            self.prompt = prompt
            self.is_dark = is_dark
            self.is_dad = is_dad

    # list of jokes we tell monika
    # each elem is a MASJoke
    p2m_jokes = list()

    # list of jokes monika tells us
    # each elem is a MASJoke
    m2p_jokes = list()

    def removeSeenJokes():
        #
        # Removes both jokes that we have already told monika and jokes that
        # monika has already told us from their appropriate structures
        #
        # ASSUMES:
        #   p2m_jokes
        #   m2p_jokes

        # lets start with p2m
        global p2m_jokes
        for key in p2m_jokes:
            if renpy.seen_label(key):
                p2m_jokes.pop(key)

        # now for m2p
        global m2p_jokes
        for index in range(len(m2p_jokes)-1, -1, -1):
            if renpy.seen_label(m2p_jokes[index]):
                m2p_jokes.pop(index)

    def randomlyRemoveFromDictPool(pool, n):
        #
        # randomly returns n number of items from the given pool. The pool 
        # must be a dict. If there are less than n items in the pool, then the
        # pool is returned. Returned items are removed from the pool.
        #
        # IN:
        #   pool - dict that we want to retrieve from
        #   n - number of items to remove off the pool
        #
        # RETURNS:
        #   n number of items, randomly selected if n < len(pool), the pool
        #       itself otherwise
        
        if len(pool) <= n:
            return pool

        # remove n number of items
        keys = pool.keys()
        removed = dict()
        for i in range(0,n):
            sel_key = renpy.random.choice(keys)
            removed[sel_key] = pool.pop(sel_key)
        return removed

    def randomlyRemoveFromListPool(pool, n):
        #
        # randomly returns n number of items from teh given pool. The pool 
        # must be a list. If there are less than n items in the pool, then the 
        # pool is returned. Returned items are removed from teh pool.
        #
        # IN:
        #   pool - list that we want to retrieve from
        #   n - number of items to remove off the pool
        #
        # RETURNS:
        #   n number of items, randomly seelcted if n < len(pool), the pool
        #       itself otherwise
        
        if len(pool) <= n:
            return pool

        # remove n number of items
        removed = list()
        for i in range(0,n):
            item = renpy.random.choice(pool)
            removed.append(pool.remove(item))
        return removed

init -1 python in mas_jokes_consts:
    # only 3 choices at a time
    OPTION_MAX = 3

    # how many jokes can we say? 
    # per day?
    JOKE_DAILY_MAX = 3

# post stuff
init 10 python:
    from copy import deepcopy

    # copy of the total player 2 monika jokes dict
    all_p2m_jokes = dict(p2m_jokes)

    # copy of the total monika 2 player jokes list
    all_m2p_jokes = list(m2p_jokes)

    # remove seen shit
    removeSeenJokes()

    # empty lists mean we need to reset
    if len(p2m_jokes) == 0:
        p2m_jokes = dict(all_p2m_jokes)

    if len(m2p_jokes) == 0:
        m2p_jokes = list(all_m2p_jokes)

    # fill up the daily jokes list
    # NOTE: since we are waiting on daily limiting, this is currently set
    # to only showcasing 3 jokes per launch.
    import store.mas_jokes_consts as mjc:
    p2m_jokes_avail = mjc.OPTION_MAX  # number of player 2 monika jokes avail
    m2p_jokes_avail = mjc.OPTION_MAX  # number of monika 2 player jokes avail
    jokes_available = mjc.JOKE_DAILY_MAX # number of jokes m and p exchange

    # length checks to ensure we dont go pull too many
    if len(p2m_jokes) < p2m_jokes_avail:
        p2m_jokes_avail = len(p2m_jokes)
    if len(m2p_jokes) < m2p_jokes_avail:
        m2p_jokes_avail = len(m2p_jokes)

    # now remove from the pool
    # the daily player 2 monika jokes dict
    daily_p2m_jokes = randomlyRemoveFromDictPool(p2m_jokes, p2m_jokes_avail)
#    daily_p2m_jokes = randomlyRemoveFromDictPool(p2m_jokes, jokes_available)

    # the daily monika 2 player jokes list
    daily_m2p_jokes = randomlyRemoveFromListPool(m2p_jokes, m2p_jokes_avail)
#    daily_m2p_jokes = randomlyRemoveFromListPool(m2p_jokes, jokes_available)


init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_okidoki",
        is_m2p=False,
        prompt="Doki Doki is not Oki Doki"
    ))

label joke_okidoki:
    m "Ahaha, what makes you say that?"
    m "Sure, maybe the events that lead up to this point weren't exactly 'oki doki'..."
    m "But it's not like it wasn't worth it in the end, right?"    
    m "I mean, take a glance at the bright side of our situation, [player]."
    m "For instance, since you're here, and I'm here, that means we're both together!"
    m "Since we love each other so much, I hope you can understand the lengths I had to go to even reach this point..."
    return


init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_cantopener",
        is_m2p=False,
        prompt="What do you call a broken can opener?"
    ))

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
    return

init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_threewishes",
        is_m2p=False,
        prompt=("Three guys, who are stranded on an "+
        "island, find a magic lantern which contains a genie, who will grant "+
        "three wishes.")
    ))

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
    return

init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_sayorihobby",
        is_m2p=False,
        prompt="What would have been Sayori's favorite hobby?"
    ))

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
    return
