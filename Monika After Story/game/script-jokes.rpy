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

# okay we actually need some persits
default persistent.allow_dark_jokes = False
default persistent.allow_dad_jokes = False
default persistent.jokes_available = 0

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

        @staticmethod
        def filterJoke(joke):
            #
            # Filters the given joke accoridng to persistent rule
            #
            # IN:
            #   joke - MASJoke object to filter
            #
            # RETURNS:
            #   True if the joke passes the filter, false otherwise
            #
            # ASSUMES:
            #   persistent.allow_dark_jokes
            #   persistent.allow_dad_jokes

            # sanity check
            if not joke:
                return False

            # let the filtering begin
            if not persistent.allow_dark_jokes and joke.is_dark:
                return False

            if not persistent.allow_dad_jokes and joke.is_dad:
                return False

            # pass filtering rules
            return True

    # list of jokes we tell monika
    # each elem is a MASJoke
    p2m_jokes = list()

    # list of jokes monika tells us
    # each elem is a MASJoke
    m2p_jokes = list()

    def removeSeenJokes(pool):
        #
        # Removes both jokes that we have already told monika and jokes that
        # monika has already told us from their appropriate structures
        #
        # IN:
        #   pool - list of MASJokes to remove jokes from
        #
        # OUT:
        #   pool - list of MASJokes with seen jokes removed

        for index in range(len(pool)-1, -1, -1):
            if renpy.seen_label(pool[index].jokelabel):
                pool.pop(index)

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
        #   n number of items, randomly selected, or len(pool) number of items
        #   if n < len(pool)
        
        if len(pool) < n:
            n = len(pool)

        # remove n number of items
        removed = list()
        for i in range(0,n):
            item = renpy.random.choice(pool)
            removed.append(item)
            pool.remove(item)
        return removed


    def filterPool(pool):
        #
        # Filters the given pool according to persistent rules. 
        # The returned list is a reference copy only
        #
        # IN:
        #   pool - the pool to filter. Assumed to be a list of MASJoke objects
        #
        # RETURNS:
        #   a list of MASJoke objects that have been filtered. These are
        #   reference opies.
        
        # sanity checks
        if not pool or len(pool) == 0:
            return list(pool)

        # lets apply filtering!!
        new_pool = list()

        for joke in pool:
            if MASJoke.filterJoke(joke):
                new_pool.append(joke)

        return new_pool

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
    all_p2m_jokes = deepcopy(p2m_jokes)

    # copy of the total monika 2 player jokes list
    all_m2p_jokes = deepcopy(m2p_jokes)

    # remove seen shit
    removeSeenJokes(p2m_jokes)
    removeSeenJokes(m2p_jokes)

    # empty lists mean we need to reset
    if len(p2m_jokes) == 0:
        p2m_jokes = deepcopy(all_p2m_jokes)

    if len(m2p_jokes) == 0:
        m2p_jokes = deepcopy(all_m2p_jokes)

    # FILTER jokes
    p2m_jokes = filterPool(p2m_jokes)
    m2p_jokes = filterPool(m2p_jokes)

    # fill up the daily jokes list
    # NOTE: since we are waiting on daily limiting, this is currently set
    # to only showcasing 3 jokes per launch.
    import store.mas_jokes_consts as mjc
    p2m_jokes_avail = mjc.OPTION_MAX  # number of player 2 monika jokes avail
    m2p_jokes_avail = mjc.OPTION_MAX  # number of monika 2 player jokes avail

    # TODO: integrate the daily portion of prompt-system with this to ensure
    # daily limit of jokes
    # number of jokes m and p exchange
    persistent.jokes_available = mjc.JOKE_DAILY_MAX 

    # length checks to ensure we dont go pull too many
    if len(p2m_jokes) < p2m_jokes_avail:
        p2m_jokes_avail = len(p2m_jokes)
    if len(m2p_jokes) < m2p_jokes_avail:
        m2p_jokes_avail = len(m2p_jokes)

    # now remove from the pool
    # the daily player 2 monika jokes dict
#    daily_p2m_jokes = randomlyRemoveFromDictPool(p2m_jokes, p2m_jokes_avail)
#    daily_p2m_jokes = randomlyRemoveFromDictPool(p2m_jokes, jokes_available)
    daily_p2m_jokes = randomlyRemoveFromListPool(p2m_jokes, p2m_jokes_avail)

    # the daily monika 2 player jokes list
    daily_m2p_jokes = randomlyRemoveFromListPool(m2p_jokes, m2p_jokes_avail)
#    daily_m2p_jokes = randomlyRemoveFromListPool(m2p_jokes, jokes_available)

#=============================================================================#
# PLAYER 2 MONIKA JOKES
#=============================================================================#

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
        prompt="What would have been Sayori's favorite hobby?",
        is_dark=True
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


#=============================================================================#
# MONIKA 2 PLAYER JOKES
#=============================================================================#

init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_fencegraveyard",
        is_m2p=True,
        is_dad=True
    ))

label m_joke_fencegraveyard:
    m "A curious child asks his dad ‘Why do they build a fence around a graveyard?’"
    m "The dad quickly replies with ‘Because people are dying to get in there!’"
    m "..."
    m "It’s surprising how a lot of jokes are based on unexpected answers."
    m "Maybe that’s a bit ironic for me to be surprised ehehe~"
    m "Normally in jokes the characters won’t get a proper answer."
    m "They will either get a quite literal answer or an unexpected twist of the question."
    m "Maybe I should start giving you unexpected answers to any questions!"
    m "Just teasing you~"
return

init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_gotagig",
        is_m2p=True,
    ))

label m_joke_gotagig:
    m "Have you heard of the band ‘1023MB’?"
    m "They haven’t got a gig yet."
    m "..."
    m "Sorry if you didn’t get it~."
    m "This joke probably flew right over your head if you aren’t too big into computers."
    m "In a computer 1024 megabytes makes a gigabyte."
    m "So the joke is centered around the fact that they are 1mb away from having a ‘gig’."
    m "Anyways, you were technically advanced enough to install this mod."
    m "So I am sure you understood it! Right [player]? ehehe~"
return

init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_sodapressingjob",
        is_m2p=True,
    ))
label m_joke_sodapressingjob:
    m "Why did the can-crusher quit his job?"
    m "Because it was soda-pressing!"
    m "..."
    m "Gosh, I forgot how silly this joke sounded!"
    m "Well, it’s more of a play on words than anything else."
    m "It’s really interesting how much one can play with the varying sounds words can make."
    m "Word play is really interesting if you look it form a linguistic point of view."
    m "It’s pretty much combining words to make it sound like a different word!"
    m "Ah, I hope you’re fond of these type of jokes, just as I am fond of you [player]!"
return

init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_nextquestion",
        is_m2p=True,
    ))
label m_joke_nextquestion:
    m "It is close to the end of the school day, the teacher is finishing up their lesson."
    m "The teacher announces that whoever answers her next question, can go home."
    m "One boy throws his bag out the window."
    m "The teacher then asked: Who just threw that?!"
    m "The same boy who threw the bag then yells: I did! I’m going home now."
    m "..."
    m "This joke works quite well as it’s quite absurd, which actually adds to the humor of it."
    m "Normally nobody would take questions that literally."
    m "It surprises the reader just like it surprised me the first time I read it!"
return

init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_mine",
        is_m2p=True,
    ))
label m_joke_mine:
    m = "A cop stops a miner for speeding on the highway."
    m "The cop asks the miner; Whose car is this? Where are you headed? What do you do?"
    m "The miner replies: mine."
    m "..."
    m "Sorry, I know it’s not one of the best jokes out there, but it can bring a small giggle."
    m "I found it pretty funny myself the first time I heard it."
    m "I guess in the end it is more a bad joke than anything, right [player]? Ehehe~"
    m "I hope you still found it a bit funny in the end."
return

init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_camouflagetraining",
        is_m2p=True,
    ))
    
label m_joke_camouflagetraining:
    m "At evening roll call, the sergeant-major headed right towards a young soldier."
    m "The sergeant-major growled at the young soldier, I didn’t see you at camouflage training this morning!"
    m "The soldier replied: Thank you very much, sir."
    m "..."
    m "This joke can be funny the first time you hear it!"
    m "It establishes a where and when before giving a situation where you would expect the soldier to reply with something to justify his absence."
    m "You end up surprised as the soldier doesn’t justify it."
    m "I wonder if you would be able to see me if I wore camouflage clothes here? ehehe~"
return

