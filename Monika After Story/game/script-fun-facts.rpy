#Persistent event database for fun facts
default persistent._mas_fun_facts_database = dict()

init -10 python in mas_fun_facts:
    #The fun facts db
    fun_fact_db = {}

    def getUnseenFactsEVL():
        """
        Gets all unseen (locked) fun facts as eventlabels

        OUT:
            List of all unseen fun fact eventlabels
        """
        return [
            fun_fact_evl
            for fun_fact_evl, ev in fun_fact_db.iteritems()
            if not ev.unlocked
        ]

    def getAllFactsEVL():
        """
        Gets all fun facts regardless of unlocked as eventlabels

        OUT:
            List of all fun fact eventlabels
        """
        return fun_fact_db.keys()


#Whether or not the last fun fact seen was a good fact
default persistent._mas_funfactfun = True

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fun_facts_open",
            category=['misc'],
            prompt="Can you tell me a fun fact?",
            pool=True
        )
    )

label monika_fun_facts_open:
    if mas_getEV('monika_fun_facts_open').shown_count == 0:
        m 1eua "Say [player], would you like to hear a fun fact?"
        m 1eub "I've been looking some up to try and teach both of us something new."
        m 3hub "They say you learn something new every day, this way I'm making sure we actually do."
        m 1rksdla "I found most of these online, so I can't say they're {i}definitely{/i} true..."

    else:
        m 1eua "Up for another fun fact, [player]?"
        if persistent._mas_funfactfun:
            m 3hua "That last one was pretty interesting after all!"
        else:
            m 2rksdlb "I know the last one wasn't great...but I'm sure this next one will be better."
    m 2dsc "Now, let's see.{w=0.5}.{w=0.5}.{nw}"

    python:
        unseen_fact_evls = mas_fun_facts.getUnseenFactsEVL()
        if len(unseen_fact_evls) > 0:
            fact_evl_list = unseen_fact_evls
        else:
            fact_evl_list = mas_fun_facts.getAllFactsEVL()

        #Now we push and unlock the fact
        fun_fact_evl = renpy.random.choice(fact_evl_list)
        mas_unlockEVL(fun_fact_evl, "FFF")
        pushEvent(fun_fact_evl)
    return

#Most labels end here
label mas_fun_facts_end:
    m 3hub "I hope you enjoyed another session of 'Learning with Monika!'"
    $ persistent._mas_funfactfun = True
    return

label mas_bad_facts_end:
    m 1rkc "That fact wasn't very good..."
    m 4dkc "I'll try better next time, [player]."
    $ persistent._mas_funfactfun = False
    return


#START: Good facts
init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_librocubiculartist",
        ),
        code="FFF"
    )

label mas_fun_fact_librocubiculartist:
    m 1eub "Did you know there's a word to describe somebody that likes to read in bed?"
    m 3eub "It's 'librocubiculartist.' It looks difficult to pronounce at first glance."
    m 3rksdld "It's a real shame some words just never get used in general."
    m 3eud "But if you say that word, most people wouldn't really know what you're talking about."
    m 3euc "You'd probably have to explain what it means, but that kind of defeats the point of using the word."
    m 2rkc "If only people read more and improved their vocabulary!"
    m 2hksdlb "...Ehehe, sorry [player]. I didn't mean to get so bothered~"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_menu_currency",
        ),
        code="FFF"
    )

label mas_fun_fact_menu_currency:
    m 3euc "Supposedly, a lot of restaurants purposefully leave out any sign of currency on their menus."
    m 3eud "This is done to psychologically manipulate people into spending more money than they need to."
    m 2euc "It works because a currency sign, such as a dollar, is used to represent a cost."
    m "By removing it, you remove the association of that cost and only think about the food of your choosing."
    m 4rksdld "The practice seems understandable. They're still a business, after all."
    m 2dsc "No matter how good the food is in a restaurant, they'll be shutting down quick if they're beaten by their competition."
    m 3hksdlb "Oh well, what can you do?"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_love_you",
        ),
        code="FFF"
    )

label mas_fun_fact_love_you:
    m 1dkc "Hmm, I'm not sure if I should tell you {i}this{/i} fact."
    m 1ekc "It's not for the faint of heart after all."
    m 1rkc "The thing is..."
    m 1dkc "..."
    m 3hub "...I love you, [player]!"
    m 1rksdlb "Ehehe, sorry, I just couldn't help myself."
    m 1hksdlb "I'll have a real fact next time, don't you worry~"
    #No end for this fact since it ends itself
    $ persistent._mas_funfactfun = True
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_morpheus",
        ),
        code="FFF"
    )

label mas_fun_fact_morpheus:
    m 3wub "Oh! A language based fact. I always like these."
    m 1eua "The word 'morphine' is based on the greek god Morpheus."
    m 1euc "Morpheus was the greek god of dreams so to have a word based on him makes sense."
    m 3ekc "But then again...wasn't his father Hypnos the god of sleep?"
    m 2dsc "Morphine {i}does{/i} let a person dream, but it's really about making someone fall asleep."
    m 4ekc "...So wouldn't it make more sense to name it after Hypnos then?"
    m 4rksdlb "Too little, too late I guess."
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_otter_hand_holding",
        ),
        code="FFF"
    )

label mas_fun_fact_otter_hand_holding:
    m 1eka "Aww, this one is really sweet."
    m 3ekb "Did you know that sea otters hold hands when they sleep to stop themselves drifting away from one another?"
    m 1hub "It's practical for them to do, but there's something really cute about it!"
    m 1eka "Sometimes I imagine myself in their position..."
    m 3hksdlb "Oh, not being a sea otter, but holding the hand of the one I love while I sleep."
    m 1rksdlb "Aha, it really does make me jealous of them."
    m 1hub "We'll get there one day though, love~"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_chess",
        ),
        code="FFF"
    )

label mas_fun_fact_chess:
    #Chess is unlocked
    if mas_isGameUnlocked("chess"):
        m 1eua "Now this is a fun fact!"
        m 3eub "There was a man named Claude Shannon who calculated the maximum amount of possible moves in chess."
        m "That number is called the 'Shannon number' and states that the amount of chess games possible is 10^120."
        m 1eua "It's often compared to the number of atoms in the observable universe which is 10^80."
        m 3hksdlb "Kind of crazy to think that there could be more chess games than atoms, isn't it?"
        m 1eua "We could play until the end of our days and it wouldn't come even close to a fraction of what is possible."
        m 3eud "Speaking of which, [player]..."
        m 1hua "Do you want to play a game of chess with me? I might even go easy on you, Ehehe~"
        #Call the good end for this path
        call mas_fun_facts_end
        return

    #Chess was unlocked, but locked due to cheating
    elif not mas_isGameUnlocked("chess") and renpy.seen_label("mas_unlock_chess"):
        m 1dsc "Chess..."
        m 2dfc "..."
        m 2rfd "You can forget about this fact since you're a cheater, [player]."
        m "Not to mention you never apologized."
        m 2lfc "...Hmph."
        #No end for this path
        return

    #We haven't unlocked chess yet
    else:
        m 1euc "Oh, not this one."
        m 3hksdlb "Not yet, at least."
        #Call the end
        call mas_bad_facts_end
        return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_struck_by_lightning",
        ),
        code="FFF"
    )

label mas_fun_fact_struck_by_lightning:
    m 2dkc "Hmm, this one sounds a bit misleading to me..."
    m 3ekc "'Men are six times more likely to be struck by lightning than women.'"
    m 3ekd "It's...rather silly, in my opinion."
    m 1eud "If men are more likely to be struck by lightning, then it's probably the landscape and circumstances of their work that make them more prone to being hit."
    m 1euc "Men traditionally have always worked more dangerous and elevated jobs so it's no surprise that it's going to happen to them often."
    m 1esc "Yet the way this fact is worded makes it sound like that just by being a man, it's more likely to happen, which is ridiculous."
    m 1rksdla "Maybe if it was phrased better, people wouldn't be so misinformed about them."
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_honey",
        ),
        code="FFF"
    )

label mas_fun_fact_honey:
    m 1eub "Ah, this is a nice easy one."
    m 3eub "Did you know that honey never spoils?"
    m 3eua "Honey can crystallize, though. Some people may see this as spoiling but it's still completely edible and fine!"
    m "The reason why this happens is because honey is mostly made of sugar and only a bit of water, making it solid over time."
    m 1euc "Most of the honey that you see in groceries doesn't crystallize as fast as real honey would because it's been pasteurized in the process of making it."
    m 1eud "...Which removes the stuff that makes the honey go solid quickly."
    m 3eub "But wouldn't it be nice to eat crystallized honey too?"
    m 3hub "It'd be like candy when you bite into it!"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_vincent_van_gone",
        ),
        code="FFF"
    )

label mas_fun_fact_vincent_van_gone:
    m 1dsc "Ah, this one..."
    m 1ekd "It's a little disheartening, [player]..."
    m 1ekc "Did you know that Vincent Van Gogh's last words were '{i}La tristesse durera toujours{/i}'?"
    m 1eud "If you translate it, it means '{i}The sadness will last forever.{/i}'"
    m 1rkc "..."
    m 2ekc "It's really sad to know that someone so renowned would say something so dark with his last breath."
    m 2ekd "I don't think it's true, however. No matter how bad things can get and how deep the sadness can go..."
    m 2dkc "There will come a time where it'll no longer be there."
    m 2rkc "...Or at least be noticeable."
    m 4eka "If you're ever sad, you know you can talk to me, right?"
    m 5hub "I will always accept and take on any burdens that you shoulder, my love~"
    #No end for this fact
    $ persistent._mas_funfactfun = True
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_king_snakes",
        ),
        code="FFF"
    )

label mas_fun_fact_king_snakes:
    m 1dsc "Hmm..."
    m 3eub "Did you know that if a snake has the word 'king' in its name, it devours other snakes?"
    m 1euc "I always wondered why a king cobra would be named how it is but never really thought more into it."
    m 1tfu "Does that mean if I eat you up, would I become Queen Monika?"
    m 1hksdlb "Ahaha, I'm just kidding, [player]."
    m 1hub "Sorry for being a little weird~"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_strength",
        ),
        code="FFF"
    )

label mas_fun_fact_strength:
    m 1hub "This fact might motivate you a bit!"
    m 3eub "The longest word in English that only contains a single vowel is 'strength'."
    m 1eua "It's funny how out of every word in the language, it's such a meaningful word that had that little detail."
    m 1hua "Little details like this really make language so fascinating to me!"
    m 3eua "Do you want to know what comes to mind when I think of the word 'strength'?"
    m 1hua "You!"
    m 1hub "Because you are the source of my strength, ehehe~"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_reindeer_eyes",
        ),
        code="FFF"
    )

label mas_fun_fact_reindeer_eyes:
    m 3eua "Ready for this one?"
    m "A reindeer's eyes changes color depending on the season. They're gold in summer and blue in winter."
    m 1rksdlb "It's a really strange phenomenon, though I don't know why..."
    m "There's probably a good scientific reason to it."
    m 3hksdlb "Maybe you can look up this one yourself?"
    m 5eua "It'd be fun to have you teach me this time~"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_bananas",
        ),
        code="FFF"
    )

label mas_fun_fact_bananas:
    m 1eub "Oh, I'd say this fact is healthy!"
    m 3eua "Did you know that when a banana grows, it curves to face the sun?"
    m 1hua "It's a process called negative geotropism."
    m 3hub "Don't you think that's pretty neat?"
    m 1hua "..."
    m 1rksdla "Umm..."
    m 3rksdlb "I guess I don't really have much else to say on it, ahaha..."
    m 1lksdlc "..."
    m 3hub "D-Did you also know that bananas aren't actually fruits but berries?"
    m 3eub "Or that the original bananas were large, green and full of hard seeds?"
    m 1eka "How about the fact that they're slightly radioactive?"
    m 1rksdla  "..."
    m 1rksdlb "...I'm just rambling on about bananas now."
    m 1rksdlc "Ummm..."
    m 1dsc "Let's just move on..."
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_pens",
        ),
        code="FFF"
    )

label mas_fun_fact_pens:
    m 1dsc "Hmm...I'm sure I already know this one."
    m 3euc "The word 'pen' is derived from the latin word 'penna', which means feather in latin."
    m "Pens back then were sharpened goose feathers dipped in ink so it'd make sense why they'd call them pens."
    m 3eud "They were the primary writing tool for a very long time, starting as early at the 6th century."
    m 3euc "It was only until the 19th century when metal pens were being made that they started to fall into decline."
    m "In fact, penknives are called the way they are because they're originally used for thinning and pointing quill pens."
    m 1tku "But I'm sure Yuri would know more about this than me, though..."
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_density",
        ),
        code="FFF"
    )

label mas_fun_fact_density:
    m 1eub "Ooh, I know."
    m 3eua "Did you know that the densest planet in our solar system is Earth itself?"
    m "And that Saturn is the least dense?"
    m 1eua "It makes sense knowing what planets are made of, but since Saturn is the second largest, it was still a little bit of a surprise."
    m 1eka "I guess size really doesn't matter!"
    m 3euc "But between you and me, [player]..."
    m 1tku "I suspect Earth may only be the densest because of a certain main character."
    m 1tfu "Buuuut that's all you'll hear from me~"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_binky",
        ),
        code="FFF"
    )

label mas_fun_fact_binky:
    m 3hub "Aww, this one's cute!"
    m "This fact will really send you 'hopping' [player]!"
    m 3hua "Whenever a rabbit hops around excitedly, it's called a binky!"
    m 1hua "Binky is such a cute sounding word, it really does suit the action."
    m 1eua "It's the happiest form of expression that a rabbit is capable of doing, so if you see it then you know you're treating it right."
    m 1rksdla "Well, although you make me so happy that I can't help but be filled with energy."
    m 1rksdlb "Don't expect me to start hopping around, [player]!"
    m 1dkbfa "...That would be {i}way{/i} too embarrassing to do."
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_windows_games",
        ),
        code="FFF"
    )

label mas_fun_fact_windows_games:
    m 1eua "Hmm, maybe this one will be more interesting to you."
    m 3eub "The card game Solitaire was introduced originally in the Windows operating system in 1990."
    m 1eub "The game was added as a feature to teach users how to use the mouse."
    m 1eua "Similarly, Minesweeper was added to familiarize users with left and right clicking."
    m 3rssdlb "Computers have been around for so long it's hard to think of a time when they weren't relevant."
    m "Each generation becomes more and more familiar with the technology..."
    m 1esa "Eventually there may come a day where not a single person isn't computer-literate."
    m 1hksdlb "Most of the world's problems need to disappear before then, though."
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_mental_word_processing",
        ),
        code="FFF"
    )

label mas_fun_fact_mental_word_processing:
    m 1hua "Ready for an interesting one, [player]?"
    m 3eua "The brain is a fickle thing..."
    m 3eub "Its way of composing and archiving information is very unique."
    m "Naturally it differs from person to person but but reading slowly like we're taught is usually less effective than going at at a faster pace."
    m 1tku "Our brains process information very rapidly and love predictability in in our language."
    m 3tub "For example, in this sentence, by the the time you are done reading you will have already skipped over the double 'the.'"
    m 1tfu "..."
    m 2hfu "Check the history log if you missed them~"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_I_am",
        ),
        code="FFF"
    )

label mas_fun_fact_I_am:
    m 1hua "Mmmm, I love language facts!"
    m 3eub "In English, the shortest complete sentence is 'I am.'"
    m 1eua "Here's an example."
    m 2rfb "'{i}Monika! Who's [player]'s loving girlfriend?{/i}'"
    m 3hub "'I am!'"
    m 1hubfa "Ehehe~"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_low_rates",
        ),
        code="FFF"
    )

label mas_fun_fact_low_rates:
    m 1hua "Now this is a wholesome one..."
    m 1eua "Currently, we have the lowest crime rates, maternity death, infant mortality and illiteracy ever in human history."
    m 3eub "Life expectancy, average income, and standards of living is the highest for most of the global population too!"
    m 3eka "This tells me that it can always get better. It really does show that despite all the bad things, the good times will always come afterwards."
    m 1hua "There really is {i}hope{/i}..."
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_desert",
        ),
        code="FFF"
    )

label mas_fun_fact_desert:
    m 3euc "Deserts have a pretty unique ecosystem..."
    m 3rksdla "However, they don't offer a lot of positive factors for humans."
    m 1eud "Temperatures can vary between extreme heat during the day and freezing cold at night. Their average rainfall is also pretty low, making living in one difficult."
    m 3eub "That's not to say they can't be beneficial to us though!"
    m 3eua "Their surface is a great spot for solar power generation and oil is commonly found beneath all that sand."
    m 3eub "Not to mention, their unique landscape makes them popular vacation spots!"
    m 1eua "So I guess while we can't live in them that easily, they're still better than they seem."

    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_photography",
        ),
        code="FFF"
    )

label mas_fun_fact_photography:
    m 1esa "Did you know that the first photograph was taken using a box with a hole in it as a camera?"
    m 1eua "Lenses weren't actually introduced until much later on."
    m 1euc "Early photography also relied on a series of special chemicals in a dark room to prepare the photos..."
    m 3eud "Developer, stop bath, and fixer chemicals were used just to prepare the paper the photos would be printed on...{w=0.3} {nw}"
    extend 1wuo "And that's only for black and white prints!"
    m 1hksdlb "Old photos were much harder to prepare compared to modern ones, don't you think?"

    #Call the end
    call mas_fun_facts_end
    return

#Stealing yearolder's bit for this since it makes sense as a fun fact
init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_getting_older",
        ),
        code="FFF"
    )

label mas_fun_fact_getting_older:
    m 3eua "Did you know that how you perceive time changes as you age?"
    m "For example, when you're a year old, you see one year as 100%% of your life."
    m 1euc "But when you're 18, you see a year as only 5.6%% of your life."
    m 3eud "As you get older, the proportion of a year compared to your entire lifespan decreases, and in turn, time {i}feels{/i} like it's moving faster as you grow up."
    m 1eka "So I'll always cherish our moments together, no matter how long or short they are."
    m 1lkbsa "Although sometimes it feels like time stops when I'm with you."
    m 1ekbfa "Do you feel the same, [player]?"
    python:
        import time
        time.sleep(5)

    m 1hubfa "Ahaha, I thought so!"

    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_dancing_plague",
        ),
        code="FFF"
    )

label mas_fun_fact_dancing_plague:
    m 3esa "Oh, this one's pretty weird..."
    m 1eua "Apparently, Europe has been afflicted by outbreaks of a 'dancing plague' in the past."
    m 3wud "People, {w=0.2}sometimes hundreds at once, {w=0.2}would involuntarily dance for days at a time, with some even dying from exhaustion!"
    m 3eksdla "They tried to treat it by having people play music alongside the dancers, but you can imagine that didn't work out so well."
    m 1euc "To this day, they're still unsure exactly what caused it."
    m 3rka "The whole thing seems kind of unbelievable to me...{w=0.2}{nw}"
    extend 3eud "but it has been independently documented and observed by multiple sources across centuries..."
    m 3hksdlb "Reality really is stranger than fiction, I guess!"
    m 1eksdlc "Gosh, I can't imagine dancing for days on end."
    m 1rsc "Though...{w=0.3}{nw}"
    extend 1eubla "I guess I wouldn't mind if it was with you."
    m 3tsu "...Just for a bit, ehehe~"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_pando_forest",
        ),
        code="FFF"
    )

label mas_fun_fact_pando_forest:
    m 1esa "Supposedly, in the state of Utah, there's a forest that's actually made up of a single tree."
    m 3eua "It's called the Pando forest, and for all of its 43 hectares, its trunks are connected by a single root system."
    m 3eub "Not to mention, each of its thousands of trunks are essentially clones of each other."
    m 1ruc "'A single organism that became an army of clones on its own, all connected to the same hivemind.'"
    m 1eua "I think it could make a good science fiction or horror short-story, [player]. What do you think?"
    m 3eub "Anyway,{w=0.2} I feel like this really changes the meaning of the phrase 'missing the forest for the trees'{w=0.1}{nw} "
    extend 3hub "ahaha!"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_immortal_jellyfish",
        ),
        code="FFF"
    )

label mas_fun_fact_immortal_jellyfish:
    m 3eub "Here's one!"
    m 1eua "Apparently, immortality has been achieved by one species of jellyfish."
    m 3eua "The aptly named immortal jellyfish has the ability to return to its polyp state once it has reproduced."
    m 1eub "...And it can keep doing this forever!{w=0.3} {nw}"
    extend 1rksdla "Unless of course it's eaten or infected by a disease."
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_arrhichion",
        ),
        code="FFF"
    )

label mas_fun_fact_arrhichion:
    m 3eua "Okay...{w=0.2}here's a historical one."
    m 1esa "An ancient Greek athlete was able to win his fighting match even though he'd already died."
    m 1eua "Reigning champion Arrhichion was fighting in a pankration match when his competitor started to choke him out using both his hands and legs."
    m 3eua "Instead of yielding, Arrhichion still aimed for the win by dislocating his opponent's toe."
    m 3ekd "His opponent quit from the pain, but when they went to announce Arrhichion as the victor they found him dead from suffocation."
    m 1rksdlc "Some people are really dedicated to their ideals to victory and to honour.{w=0.2} {nw}"
    extend 3eka "I think it's admirable, in a way."
    m 1etc "But I wonder...{w=0.2}if we could ask Arrhichion now if he thought it was worth it, what would he say?"
    #Call the end
    call mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_antarctica_brain",
        ),
        code="FFF"
    )

label mas_fun_fact_antarctica_brain:
    #Do some setup for the last line
    python:
        has_friends = persistent._mas_pm_has_friends is not None

        has_fam_to_talk = (
            persistent._mas_pm_have_fam
            and not persistent._mas_pm_have_fam_mess
            or (persistent._mas_pm_have_fam_mess and persistent._mas_pm_have_fam_mess_better in ["YES", "MAYBE"])
        )

        dlg_prefix = "But make sure you keep up with your "

        if has_fam_to_talk and has_friends:
            dlg_line = dlg_prefix + "family and friends too, okay?"

        elif has_fam_to_talk and not has_friends:
            dlg_line = dlg_prefix + "family too, okay?"

        elif has_friends and not has_fam_to_talk:
            dlg_line = dlg_prefix + "friends too, okay?"

        else:
            dlg_line = "Just be sure you find some people to talk to in your reality too, okay?"

    m 3eud "Apparently, spending a year in Antarctica can shrink one part of your brain by about 7 percent."
    m 3euc "It looks like it results in reduced memory capacity and spatial thinking ability."
    m 1ekc "The research indicates that it's due to social isolation, monotony of life, and the environment over there."
    m 1eud "I think this serves as a cautionary tale for us, [player]."
    m 3ekd "Even if you don't end up going to Antarctica, your brain can still get pretty messed up if you're isolated all the time, or stay cooped up in one room."
    m 3eka "I love being with you [player], and I hope we can keep talking like this long into the future. {w=0.2}[dlg_line]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_cloud_weight",
        ),
        code="FFF"
    )

label mas_fun_fact_cloud_weight:
    m 3eub "Did you know that the average cloud weighs 500 tonnes?"
    m 3eua "I have to admit, this one caught me by surprise, more so than some of the other facts."
    m 1hua "I mean, they just look {i}really{/i} light and fluffy.{w=0.3} {nw}"
    extend 1eua "It's hard to imagine that something so heavy can just float in the air like that."
    m 3eub "It kind of reminds me of the classic question...what's heavier, a kilogram of steel or a kilogram of feathers?"
    m 1tua "You most likely already know the answer to that though, right [player]? Ehehe~"
    #Call the end
    call mas_fun_facts_end
    return
