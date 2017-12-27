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
default persistent.dark_jokes_told = 0

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
        "joke_moonrestaurant",
        is_m2p=False,
        prompt="Did you hear about the restaurant on the moon?"
    ))
    
label joke_moonrestaurant:
    menu:
        "It has great service but there's no atmosphere.":
            m 3l "Ahaha, maybe a better atmosphere would make this restaurant {i}out of this world{/i}!"
            m 2a"Some candles, plants and oxygen would make the place great."
            m "Hope you didn't {i}planet{/i}!"
            m 1j "Gosh, I should stop for now!"
            m "I'll tell you any bad jokes you want other time ehehe~"
    return

init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_scarecrowaward",
        is_m2p=False,
        prompt="Why did the scarecrow win an award?",
        is_dad=True
    ))

label joke_scarecrowaward:
    menu:
        "He was outstanding in his field.":
            m 4f "Ah, you can't be serious."
            m 2b "You've to consider that farming jokes are quite corny ehehe~"
    return

init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_fencegraveyard",
        is_m2p=False,
        prompt="A curious child asks his dad 'Why do they build a fence around a graveyard?'",
        is_dad=True
    ))
label joke_fencegraveyard:
    menu:
        "The dad quickly replies with 'Because people are dying to get in there!'":
            m 3b "Some people do get in like the writer who was sentenced to death!"
            m "Yet just skeletons can't get in since they have nobody to enter with."
            m 2f "It's a bit discriminative if you ask me."
            m 2j "We could call it a grave mistake."
            m 2k "Ahaha, I'm sorry [player], I didn't mean to bore you to death with those puns."
    return
    
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_knocknobel",
        is_m2p=False,
        prompt="Did you hear about the guy who invented knock knock jokes?"
    ))

label joke_knocknobel:
    menu:
        "Turns out he won the nobel prize.":
            m 3e "Well, I hope he could handle the pressure."
            m 2b "It's after all an unbellievable situation."
            m "I am glad he wasn't doormant in the middle of the awards."
            m 1l "Hope you do love my bad puns [player]! Ehehe~"
    return

init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_mushroomfungai",
        is_m2p=False,
        prompt="A mushroom walks into a bar."
    ))
    
label joke_mushroomfungai:
    menu:
        "The bartender says, 'Hey, get out of here! We don’t serve mushrooms here'":
            menu:
                "The mushroom says, 'Why not? I’m a fungi!'":
                    m 2b "Poor mushroom, maybe he wasn't allowed in cause there wasn't {i}mushroom{/i}!"
                    m 3p "I don't know that many mushroom jokes."
                    m 3n "Maybe I should just try to make other puns just for you ehehe~"
    return



#=============================================================================#
# MONIKA 2 PLAYER JOKES
#=============================================================================#

init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_bakercollege",
        is_m2p=True
    ))

label m_joke_bakercollege:
    m "What did the baker say when he had to go through college?"
    m 2b "Piece of cake!"
    m 3o "I wonder if Natsuki would have said the same thing."
    m 2l "Maybe she would loaf it! Ehehe~"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_gluehistory",
        is_m2p=True
    ))

label m_joke_gluehistory:
    m "I’ve been reading a book on the history of glue."
    m 2b "I just can’t seem to put it down."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_knifetoknowyou",
        is_m2p=True
    ))
    
label m_joke_knifetoknowyou:
    m "What did the serial murderer tell their victim?"
    m 2b "It was knife knowing you."
    m 1p "Now that I think about it, this joke reminds me of Yuri."
    m 4b "I believe she would have laughed at that joke for a knifeti- I mean, a lifetime!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_natsukishelf",
        is_m2p=True
    ))

label m_joke_natsukishelf:
    m "I would have felt horrible if Natsuki had been hurt by those falling books."
    m 2l "I'd only have my shelf to blame."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_undercoverbook",
        is_m2p=True
    ))

label m_joke_undercoverbook:
    m "Why did the book join the police?"
    m 2j "He wanted to go undercover."
    return

