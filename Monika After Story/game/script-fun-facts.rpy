#Persistent event database for fun facts
default persistent._mas_fun_facts_database = dict()

init -10 python in mas_fun_facts:
    #The fun facts db
    fun_fact_db = {}

    TYPE_GOOD = "good"
    TYPE_BAD = "bad"


#Whether or not the last fun fact seen was a good fact
default persistent._mas_funfactfun = True

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fun_facts_open",
            category=['misc'],
            prompt="Fun facts",
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
    m 2dsc "Now, let's see..."

    python:
        #Determines if it is a bad fact, 10% chance.
        if renpy.random.randint(1,100) <= 10:
            list_facts = [
                eventlabel
                for eventlabel, event in store.mas_fun_facts.fun_fact_db.iteritems()
                if store.mas_fun_facts.TYPE_BAD in event.category
            ]

        else:
            list_facts = [
                eventlabel
                for eventlabel, event in store.mas_fun_facts.fun_fact_db.iteritems()
                if store.mas_fun_facts.TYPE_GOOD in event.category
            ]

        #Now we push the fact
        pushEvent(renpy.random.choice(list_facts))
    return

#Most labels end here
label mas_fun_facts_end:
    m 1hub "I hope you enjoyed another session of 'Learning with Monika!'"
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
            eventlabel="mas_fun_facts_1",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_1:
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
            eventlabel="mas_fun_facts_2",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_2:
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
            eventlabel="mas_fun_facts_3",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_3:
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
            eventlabel="mas_fun_facts_4",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_4:
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
            eventlabel="mas_fun_facts_5",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_5:
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
            eventlabel="mas_fun_facts_6",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_6:
    if persistent.game_unlocks['chess']:
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

    elif not persistent.game_unlocks['chess'] and persistent_seen_ever["unlock_chess"]:
        m 1dsc "Chess..."
        m 2dfc "..."
        m 2rfd "You can forget about this fact since you're a cheater, [player]."
        m "Not to mention you never apologized."
        m 2lfc "...Hmph."
        #No end for this path
        return

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
            eventlabel="mas_fun_facts_7",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_7:
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
            eventlabel="mas_fun_facts_8",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_8:
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
            eventlabel="mas_fun_facts_9",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_9:
    m 1dsc "Ah, this one..."
    m 1ekd "It's a little disheartening, [player]..."
    m 1ekc "Did you know that Vincent Van Gogh's last words were '{i}La tristesse durera toujours?{/i}'"
    m 1eud "If you translate it, it means '{i}The sadness will last forever.{/i}'"
    m 1rkc "..."
    m 2ekc "It's really sad to know that someone so renowned would say something so dark with his last breath."
    m 2ekd "I don't think it's true, however. No matter how bad things can get and how deep the sadness can go..."
    m 2dkc "There will come a time where it'll no longer be there."
    m 2rkc "...Or at least noticeable."
    m 4eka "If you're ever sad, you know you can talk to me, right?"
    m 5hub "I will always accept and take on any burdens that you shoulder, my love~"
    #No end for this fact
    $ persistent._mas_funfactfun = True
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_facts_10",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_10:
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
            eventlabel="mas_fun_facts_11",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_11:
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
            eventlabel="mas_fun_facts_12",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_12:
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
            eventlabel="mas_fun_facts_13",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_13:
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
            eventlabel="mas_fun_facts_14",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_14:
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
            eventlabel="mas_fun_facts_15",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_15:
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
            eventlabel="mas_fun_facts_16",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_16:
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
            eventlabel="mas_fun_facts_17",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_17:
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
            eventlabel="mas_fun_facts_18",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_18:
    m 1hua "Ready for an interesting one, [player]?"
    m 3eua "The brain is a fickle thing..."
    m 3eub "Its way of composing and archiving information is very unique."
    m "Naturally it differs from person to person but but reading slowly like we're taught is usually less effective than going at at a faster pace."
    m 1tku "Our brains process information very rapidly and loves predictability in in our language."
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
            eventlabel="mas_fun_facts_19",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_19:
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
            eventlabel="mas_fun_facts_20",
            category=[store.mas_fun_facts.TYPE_GOOD],
        ),
        code="FFF"
    )

label mas_fun_facts_20:
    m 1hua "Now this is a wholesome one..."
    m 1eua "Currently, we have the lowest crime rates, maternity death, infant mortality and illiteracy ever in human history."
    m 3eub "Life expectancy, average income, and standards of living is the highest for most of the global population too!"
    m 3eka "This tells me that it can always get better. It really does show that despite all the bad things, the good times will always come afterwards."
    m 1hua "There really is {i}hope{/i}..."
    #Call the end
    call mas_fun_facts_end
    return


#START: Bad facts
init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_bad_facts_1",
            category=[store.mas_fun_facts.TYPE_BAD],
        ),
        code="FFF"
    )

label mas_bad_facts_1:
    m 1eub "Did you know th--"
    m 1wud "..."
    m 2efw "T-this isn't a true fact at all!"
    m 2dfc "'Humans only use 10 percent of their brain.'"
    m 2lfd "Ugh, such nonsense."
    m 4tfc "People don't really believe this, do they?"
    #Call the end
    call mas_bad_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_bad_facts_2",
            category=[store.mas_fun_facts.TYPE_BAD],
        ),
        code="FFF"
    )

label mas_bad_facts_2:
    m 2ekc "Hm? This doesn't sound right..."
    m 2tkd "It says here that different areas of the tongue taste different flavors."
    m 2tfd "One area for bitter tastes, another for sweet..."
    m 2dfd "{i}*sigh*{/i}{w} For the love of--"
    m 2rfd "--only children would believe this."
    #Call the end
    call mas_bad_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_bad_facts_3",
            category=[store.mas_fun_facts.TYPE_BAD],
        ),
        code="FFF"
    )

label mas_bad_facts_3:
    m 2dsc "{i}*inhale*{/i}"
    m 2dsd "{i}*exhale*{/i}"
    m 2esc "'Vaccines cause autism...'"
    m "Just wow."
    m "That's not even funny, and if they're serious, it's long since been disproven."
    m 2dsc "I really don't like these kinds of hoaxes. They {i}really{/i} cause a lot of harm for a mere joke."
    m 2lksdlc "I hope no one actually believes this..."
    #Call the end
    call mas_bad_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_bad_facts_4",
            category=[store.mas_fun_facts.TYPE_BAD],
        ),
        code="FFF"
    )

label mas_bad_facts_4:
    m 2dkc "...Oh."
    m 2rkc "I'm not even sure it's worth telling you this one, [player]."
    m 2dkc "It says here that moss only grows on the north side of trees, but I know that it's only a myth."
    m 2ekd "A very popular one too!"
    m 4eud "You see, moss grows wherever there is shady and damp conditions. Back then, people thought that since the sun comes from a certain direction, it means there'll be moss there too."
    m 2efd "But relying on that kind of logic is dangerous!"
    m 2efc "It ignores the very idea that forests already have many things, especially trees, that create the ideal conditions for it to grow in."
    m "Plus even if it wasn't like that, the trick would only work in the Northern hemisphere."
    m 2wfc "Anyone within the Southern hemisphere would have it growing facing south."
    m 2dfc "..."
    m 2dfd "[player], if you ever go out into a place where you might need to rely on such a cheap trick, please bring a compass."
    m 2dkc "I would hate for something to happen to you, especially because of false information like this..."
    #Call the end
    call mas_bad_facts_end
    return
