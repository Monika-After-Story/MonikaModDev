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
            self.msg = msg
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

init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_hitired",
        is_m2p=False,
        prompt="How many apples grow on a tree?",
        is_dad=True
    ))
label joke_hitired:
    m 1q "Ah, [player] please give me a second"
    m "I don't know why but I haven't been feeling that good today."
    m 2p "I'll try to guess your joke in a second."
    menu:
        m "Yet for now I'm tired, that's all."
        "Hi tired, I'm [player]!":
            m 4g "..."
            m "Did you just seriously tell me that?"
            m 2d "I really can't believe it."
            m "You just played on me the ultimate dad joke."
            m 2k"Gosh, [player]!"
            m 3e "You should know that your joke qualifies as a dad joke completely."
            m "There's only one reason it does!"
            m 3j "Your joke became apparent."
            m "..."
            m 1l "Ahaha, that should make up for your joke!"
    return

init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_cantopener",
        is_m2p=False,
        prompt="What do you call a broken can opener?"
    ))

label joke_cantopener:
    menu:
        "A can't opener!":
            m 1g "I... I didn't think it was possible to think up such a terrible joke."
            m 3c "[player], you do understand how the concept of humor works, right?"
            m 3l "You should get a bro{i}kan{/i} opener! Ehehe~" 
            m "That's the proper way to do it."
            m 3b "If your joke doesn't stand out then it might get lost in a {i}can{/i}yon of bad jokes."
    return
    
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_camouflagetraining",
        is_m2p=False,
        prompt="At evening roll call, the sergeant-major headed right towards a young soldier."
    ))
    
label joke_camouflagetraining:
    menu:
        "The sergeant-major growled at the young soldier, 'I didn’t see you at camouflage training this morning!'":
            menu:
                "The soldier replied: 'Thank you very much, sir.'":
                    m 1l "Ahaha, quite funny [player]."
                    m 3e "Although I believe there're better kinds of camouflage."
                    m "Like for example, how does a cow become invisible?"
                    m 1j "Through camooflage!"
                    m 2p "Gosh, I just can't find a better pun for camouflage."
    return
    
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_muffledexhausted",
        is_m2p=False,
        prompt="Last night I had a dream I was a muffler."
    ))
    
label joke_muffledexhausted:
    menu:
        "I woke up exhausted.":
            m "Ah in that case you should try to dream of being a bicycle!"
            m "Although you might sleep badly since you would be two tired."
            m "In that case {i}wheel{/i} see a better solution."
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
    menu:
        "The first guy wishes for a way off the island, the second guy wishes for the same as the first guy...":
            menu:
                "Finally, the third guy says: 'I'm lonely. I wish my friends were back here.'":
                    m 4p "The first and second guys must be feeling sad."
                    m 3b"I hope the third guy was shore of his sailection on that wish."
                    m "At least we could call it a seantimental reunion!"
                    m "From now on it might seem like seaparation is impossible."
                    m 2l "After all, they'll have to sea each other for a long time."
    return

    
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_sodapressing",
        is_m2p=False,
        prompt="Why did the can-crusher quit his job?"
    ))
    
label joke_sodapressing:
    menu:
        "Because it was soda-pressing!":
            m 2k "Ahaha, I see."
            m 1a "That joke is pretty bad, I just think you should can it!"
            m 3j "{i}So daring{/i} to tell such a bad pun to me! Ehehe~"
            return
            

init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_haircut",
        is_m2p=False,
        prompt="Did you ever get a haircut?"
    ))
    
label joke_haircut:
    m 3e "Ah, you're wrong there!"
    m 4j "I didn't get a haircut, I got several cut!  Ehehe~"
    m "Sorry, I simply saw the chance to answer back."
    return
    
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_pooldeepends",
        is_m2p=False,
        prompt="Are pools safe for diving?"
    ))
    
label joke_pooldeepends:
    menu:
        "It deep ends!":
            m 4j "Honestly [player], I think you could pool off something better!"
            m 4l"Put some more effort into it next time! Ehehe~"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_atomtrustissues",
        is_m2p=False,
        prompt="You shouldn't trust atoms!"
    ))
    
label joke_atomtrustissues:
    menu:
        "They make up everything.":
            m 2j "You should just get {i}a tome{/i}of jokes."
            m "It might be useful but then again, it's made out of atoms!"
            m 2k "Ahaha, I'm made out of atoms too so are you."
            m 4p "Gosh, you have created a gigantic contradiction!."
            return

init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_hamdiscrimination",
        is_m2p=False,
        prompt="A ham sandwich walks into a bar."
    ))
    
label joke_hamdiscrimination:
    menu:
        "The bartender says ‘Sorry we don’t serve food here!’.":
            m 1b "That's a really tough way to {i}hammer{/i} his point."
            m 3b "I personally believe this discrimination was hamful."
            m 4j "Would the bartender serve food if the ham was instead a {i}hamster{/i}?"
            return
            

init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_mineistheanswer",
        is_m2p=False,
        prompt="A cop stops a miner for speeding on the highway."
    ))
    
label joke_mineistheanswer:
    menu:
        "The cop asks the miner; 'Whose car is this? Where are you headed? What do you do?'":
            menu:
                "The miner replies; 'Mine.'":
                    m 2b "It seems like you've hit rock bottom with this joke."
                    m 3a "I just have a cobble of rock puns."
                    m  "Not every pun can be a gem."
                    m 4k "Some just fall under the pressure."
                    m "You've to avoid taking these puns for granite."
                    return
                
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_beaverdamn",
        is_m2p=False,
        prompt="I just watched a show about beavers."
    ))
    
label joke_beaverdamn:
    menu:
        "It was the best damn thing ever.":
            m 4j "You wood need some better beaver puns for next time!"
            m 4l "Beavery careful with the puns you say! Ehehe~"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_themuggedcoffee",
        is_m2p=False,
        prompt="Why did the coffee file a police report?"
    ))

label joke_themuggedcoffee:
    menu:
        "It was mugged!":
            m 3b "I see, I wonder if the coffee procaffeinated filing that report."
            m "Getting mugged must be a bitter thing to happen to you."
            m 2j "I hope the coffee has bean okay after all this!"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_tearablepaper",
        is_m2p=False,
        prompt="Wanna hear a joke about paper?"
    ))

label joke_tearablepaper:
    menu:
        "Nevermind, it's just tearable!":
            m 4a "Your joke's quite flimsy."
            m 1b "If it was a bit better then we could make it pay-per view!"
            m 1l "Although for now all I can say is that it's far away from being a paperfect joke."
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_groundbreakingshovel",
        is_m2p=False,
        prompt="I think quite highly of the shovel."
    ))
    
label joke_groundbreakingshovel:
    menu:
        "It was after all, a ground breaking invention.":
            m 1a "You really shoveled that joke out."
            m 1k "It's a hole other joke compared to what one might expect. Ehehe~"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_igloosit",
        is_m2p=False,
        prompt="How does a penguin build it's house?"
    ))
            
label joke_igloosit:
    menu:
        "Igloos it together!":
            m 2e "I think that house would fall down under harsh weather, you snow?"
            m "I hope that penguin doesn't get excited over his new house and ends up giving the cold shoulder to other penguins!"
            m 3b "If somebody's in trouble then he should offer his alp!"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_irrelephant",
        is_m2p=False,
        prompt="What do you call an elephant that doesn't matter?"
    ))
    
label joke_irrelephant:
    menu:
        "An irrelephant!":
            m 4b "I assume coming up with that one was a tough tusk."
            m 1k "Making bad jokes like this is quite a big deal! Ehehe~"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_nutsdiet",
        is_m2p=False,
        prompt="I thought about going on an all-almond diet."
    ))
    
label joke_nutsdiet:
    menu:
        "But that's just nuts!":
            m 2k "Ahaha, you really went nuts with that joke."
            m 4j "If we're doing food jokes then you should watch out."
            m "There's a cereal killer around."
            m 1k "The police says 'Lettuce know if you see him.'"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_kidnappingatschool",
        is_m2p=False,
        prompt="Did you hear about the kidnapping at one school?"
    ))
    
label joke_kidnappingatschool:
    menu:
        "It's fine, he woke up.":
            m 3k "Ahaha, impressive."
            m 2p "Hope he could get a bed to nap on."
            m 1b "Otherwise he wouldn't get a beddy good sleep!"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_resistingarest",
        is_m2p=False,
        prompt="If a child refuses to sleep during night time."
    ))
    
label joke_resistingarest:
    menu:
        "Are they guilty of resisting a rest?":
            m 2b "I doubt the police could catch him in that case."
            m 2l "The child always sleeps away just when they're about to get him."
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_stepahead",
        is_m2p=False,
        prompt="I leave my right shoe inside my car."
    ))
    
label joke_stepahead:
    menu:
        "You could say I'm a step ahead!":
            m 4a "I believe you went a step too far with this joke."
            m "You should take baby steps first."
            m 1j "After all, a joke is not a cake walk."
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_leastspokenlanguage",
        is_m2p=False,
        prompt="What's the least spoken language in the world?"
    ))
    
label joke_leastspokenlanguage:
    menu:
        "Sign language.":
            m 1b "I should've seen that one coming."
            m 4k "The signs were pretty clear! Ehehe~"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_octover",
        is_m2p=False,
        prompt="What do you say when november starts?"
    ))
    
label joke_octover:
    menu:
        "Octover!":
            m 2j "I hope you {i}may{/i} come up with something better."
            m 2k "{i}March{/i} onwards until you can come up with something else! Ehehe~"
            return
                    
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_leekinginformation",
        is_m2p=False,
        prompt="Why did the vegetable go to jail?"
    ))
        
label joke_leekinginformation:
    menu:
        "Because he was leeking information.":
            m 3n "That joke was as salad as rock!"
            m 2j "I herb that one a while ago. Ehehe~"
            return

init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_timidpebble",
        is_m2p=False,
        prompt="What did the timid pebble wish for?"
    ))
    
label joke_timidpebble:
    menu:
        "It wished it could be a little bolder.":
            m 1a "That jokes was crystal clear."
            m 4k "I liked how concrete it was! Ehehe~"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_chickenslide",
        is_m2p=False,
        prompt="Why did the chicken cross the playground?"
    ))
    
label joke_chickenslide:
    menu:
        "To get to the other slide.":
            m 4b "I see the chicken decided to swing to that side!"
            m 1l "Ahaha, sorry [player], I just can't think of any other pun."
            return

init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_nicejester",
        is_m2p=False,
        prompt="Yesterday a clown held the door open for me."
    ))
    
label joke_nicejester:
    menu:
        "I thought it was a nice jester!":
            m 2a"It could have been a nice jester yet it must have felt funny."
            m 4b "After all, clowns have a funny bone."
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_caketiers",
        is_m2p=False,
        prompt="It was an emotional wedding."
    ))
    
label joke_caketiers:
    menu:
        "Even the cake was in tiers!":
            m 3b "Bake in my day cakes were smaller!"
            m "I suppose the cake having tiers was half-baked."
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_housewearadress",
        is_m2p=False,
        prompt="What does a house wear?"
    ))
    
label joke_housewearadress:
    menu:
        "A dress":
            m 1b "I roofly saw that one coming."
            m 1l "If the house had more stuff, that would be grate."
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_aimisgettingbetter",
        is_m2p=False,
        prompt="My ex-wife still misses me."
    ))
    
label joke_aimisgettingbetter:
    menu:
        "But her aim's steadily improving.":
            m 2n "I can only say one thing about your joke."
            m 4k "It's a {i}daimond{/i}!"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_daywellspent",
        is_m2p=False,
        prompt="If you spent your day in a well."
    ))
    
label joke_daywellspent:
    menu:
        "Would it be a day well-spent?":
            m 1a "Oh well, you don't always win."
            m 4k "Sometimes you just can't see well! Ehehe~"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_massconfusion",
        is_m2p=False,
        prompt="If America changed from pounds to kilograms."
    ))
    
label joke_massconfusion:
    menu:
        "It would be a mass confusion.":
            m 1a "If the metric system was changed too then it would be a feetiful situation."
            m 1b "Of course it would cause chaos too."
            m 3j "We shouldn't get into meters like these."
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_justchilling",
        is_m2p=False,
        prompt="What do snowmen do in their free time?"
    ))
    
label joke_justchilling:
    menu:
        "Just chilling!":
            m 1b "At least that's a good joke for breaking the ice."
            m "At frost glance it seems a lot worse."
            m 4j "It can clearly sled somebody to the wrong conclusion!"
            return
            
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_trainderailer",
        is_m2p=False,
        prompt="A boss yelled at a driver the other day."
    ))
    
label joke_trainderailer:
    menu:
        "He said 'You've got to be the worst train driver. How many trains did you derail last year?'":
            menu:
                "The driver said 'I don't know, I'ts hard to keep track!'":
                    m 1a "That driver should train his driving skills."
                    m 1b "He must have a loco-motive for doing that!"
                    m 4k "I feel like his life's going onto the wrong track. Ehehe~"
                    return
                    
init 5 python:
    p2m_jokes.append(MASJoke(
        "joke_wealldig",
        is_m2p=False,
        prompt="I dig, you dig, she dig, he dig, we dig..."
    ))
            
label joke_wealldig:
    menu:
        "...the poem may not be beatiful, but it's certainly very deep.":
            m 1a "That poem's the hole truth!"
            m 1j "Your next joke better not deep me dissapointed."
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
    m 1a "What did the baker say when he had to go through college?"
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
    m 2a"I’ve been reading a book on the history of glue."
    m 2b "I just can’t seem to put it down."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_knifetoknowyou",
        is_m2p=True
    ))
    
label m_joke_knifetoknowyou:
    m 2a "What did the serial murderer tell their victim?"
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
    m 3a "I would have felt horrible if Natsuki had been hurt by those falling books."
    m 2l "I'd only have my shelf to blame."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_undercoverbook",
        is_m2p=True
    ))

label m_joke_undercoverbook:
    m 1a "Why did the book join the police?"
    m 2j "He wanted to go undercover."
    return

init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_authlete",
        is_m2p=True
    ))
    
label m_joke_authlete:
    m 1a "What do you call a writer who completes a whole book in one day?"
    m 4e "You call him an authlete!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_stockholmbook",
        is_m2p=True
    ))
    
label m_joke_stockholmbook:
    m 1a "I just read a textbook about Stockholm Syndrome."
    m 2j"The first couple chapters were awful but by the end I loved it."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_sinkholebook",
        is_m2p=True
    ))
    
label m_joke_sinkholebook:
    m 1a "I had plans to begin reading a book about sinkholes."
    m 1b "Sadly my plans fell through."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_penciltobeornot",
        is_m2p=True
    ))

label m_joke_penciltobeornot:
    m 1b "Why did Shakespeare always write in pen?"
    m 3b "Pencils were confusing to him. 2B or not 2B?"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_booknovelideas",
        is_m2p=True
    ))
    
label m_joke_booknovelideas:
    m 2a "What do you say to a book that has good plans?"
    m 4l "You say he has some novel ideas!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_confidentbook",
        is_m2p=True
    ))
    
label m_joke_confidentbook:
    m 1a "What made the book so confident?"
    m 3b "He had everything covered!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_booklove",
        is_m2p=True
    ))
    
label m_joke_booklove:
    m 1a "How do you know when two books are in love?"
    m 4j "They're very font of each other."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_smartbookworm",
        is_m2p=True
    ))
    
label m_joke_smartbookworm:
    m 1a "Why couldn't they trick the bookworm?"
    m 2b "Because he could read between the lines."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_booknovelideas",
        is_m2p=True
    ))
    
label m_joke_bookednovelist:
    m 2a "Why was the novelist so busy?"
    m 2k "Because he was booked!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_soccernogoal",
        is_m2p=True
    ))
    
label m_joke_soccernogoal:
    m 1a "I've talked to people that quit soccer."
    m 4j "They tell me they lost their goal in life."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_stepupyourgamecompetition",
        is_m2p=True
    ))
    
label m_joke_stepupyourgamecompetition:
    m 1a "I was competing for a stair cimbling competition."
    m 3e "I had to step up my game to win."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_skiingdownhill",
        is_m2p=True
    ))
    
label m_joke_skiingdownhill:
    m 1a "It's been a long time since I last went skiing."
    m 2k "I believe my skills are going downhill."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_unbeatablewall",
        is_m2p=True
    ))
    
label m_joke_unbeatablewall:
    m 1a "The depressing thing about tennis is that no matter how good you get."
    m 4n "You'll never be as good as a wall."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_olympicprocrastination",
        is_m2p=True
    ))
    
label m_joke_olympicprocrastination:
    m 1a "If procrastination was an Olympic sport."
    m 3l "I would compete on it later! Ehehe~"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_pooldonation",
        is_m2p=True
    ))
    
label m_joke_pooldonation:
    m 2a "One day a man knocked on my door."
    m 3a "He asked for a small donation for the local swimming pool."
    m 3j "So I gave him a glass of water!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_flippingoutgymnast",
        is_m2p=True
    ))
    
label m_joke_flippingoutgymnast:
    m 2a "What does a gymnast do when they're angry?"
    m 4b "They flip out!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_marathonforeducation",
        is_m2p=True
    ))
    
label m_joke_marathonforeducation:
    m 3a"Why does someone who runs marathons make a good student?"
    m 2j "Because education pays off in the long run!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_wetdribbled",
        is_m2p=True
    ))
    
label m_joke_wetdribbled:
    m 3a "How did the basketball court get wet?"
    m 4e "Players dribbled all over it!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_jographysubject",
        is_m2p=True
    ))
    
label m_joke_jographysubject:
    m 4a "What's a runner's favorite subject in school?"
    m 4k "Jog-graphy!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_changingrooms",
        is_m2p=True
    ))
    
label m_joke_changingrooms:
    m 2a "What part of a football ground's never the same?"
    m 2j "The changing rooms."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_volleyballserving",
        is_m2p=True
    ))
    
label m_joke_volleyballserving:
    m 2a "What can you serve but never eat?"
    m 3k "A volley ball!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_samepagebooks",
        is_m2p=True
    ))
    
label m_joke_samepagebooks:
    m 3a "What did one book say to the other one?"
    m 4b "I just wanted to see if we're on the same page!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_nowordsindictionary",
        is_m2p=True
    ))
    
label m_joke_nowordsindictionary:
    m 4a "A father gives his son a really cheap dictionary for his birthday."
    m 4k "The son couldn't find the words to thank him!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_favoriteauthornowriter",
        is_m2p=True
    ))
    
label m_joke_favoriteauthornowriter:
    m 2a "A teacher asks her student 'Who's your favorite author?'"
    m "The student replies 'George Washington!'"
    m 2b "The teacher quickly says 'But he never wrote any books.'"
    m "The student answers saying 'You got it!'."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_abigarithmeticproblem",
        is_m2p=True
    ))

label m_joke_abigarithmeticproblem:
    m 4a "What did one arithmetic book say to the other?"
    m 4j "I've got a big problem!"
    return

init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_ghosthomework",
        is_m2p=True
    ))
    
label m_joke_ghosthomework:
    m 3e "Where do young ghosts write their homework?"
    m 1k "Exorcise books!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_biggestliar",
        is_m2p=True
    ))
    
label m_joke_biggestliar:
    m 1a "Who's the biggest liar in a city?"
    m 3j "The lie-brarian."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_binarytypes",
        is_m2p=True
    ))
    
label m_joke_binarytypes:
    m 4a "There're 10 types of people on the world."
    m 4e "Those who understand binary and those who don't."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_mymosthatedsnake",
        is_m2p=True
    ))
    
label m_joke_mymosthatedsnake:
    m 1a "What's the snake I hate the most?"
    m 3b "Python!"
    return

init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_natski",
        is_m2p=True
    ))
    
label m_joke_natski:
    m 2a "Why did Natsuki skip the ski trip?"
    m 4l "She could natsuki!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_programmerwithoutarrays",
        is_m2p=True
    ))
    
label m_joke_programmerwithoutarrays:
    m 2a "Why did the programmer quit his job?"
    m 3b "He couldn't get arrays!"
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_renpie",
        is_m2p=True
    ))
    
label m_joke_renpie:
    m 4a "What's my favorite pie flavor?"
    m 4b "Renpy."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_moosician",
        is_m2p=True
    ))

label m_joke_moosician:
    m 1a "What do you call a cow that plays the piano?"
    m 1k "A moo-sician."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_lockedpiano",
        is_m2p=True
    ))
    
label m_joke_lockedpiano:
    m 3a "Why're pianos so hard to open?"
    m 3e "Because the keys are inside."
    return
    
init 5 python:
    m2p_jokes.append(MASJoke(
        "m_joke_debait",
        is_m2p=True
    ))
    
label m_joke_debait:
    m 1b "How do you catch a fish?"
    m 1k "Debait!"
    return
