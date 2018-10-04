#This file contains all of monika's topics she can talk about
#Each entry should start with a database entry, including the appropriate flags
#to either be a random topic, a prompt "pool" topics, or a special conditional
#or date-dependent event with an appropriate action

define monika_random_topics = []
define mas_rev_unseen = []
define mas_rev_seen = []
define mas_rev_mostseen = []
define testitem = 0
define numbers_only = "0123456789"
define letters_only = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ"
define mas_did_monika_battery = False
define mas_sensitive_limit = 3

init -2 python in mas_topics:

    # CONSTANTS
    # most / top weights
    # MOST seen is the percentage of seen topics
    # think of this as x % of the collection
    S_MOST_SEEN = 0.1

    # TOP seen is the percentage of the most seen
    # Think of this as ilke the upper x percentile
    S_TOP_SEEN = 0.2

    # limit to how many top seen until we move to most seen alg
    S_TOP_LIMIT = 0.7

    # selection weights (out of 100)
    UNSEEN = 50
    SEEN = UNSEEN + 49
    MOST_SEEN = SEEN + 1

    def topSeenEvents(sorted_ev_list, shown_count):
        """
        counts the number of events with a > shown_count than the given
        shown_count

        IN:
            sorted_ev_list - an event list sorted by shown_counts
            shown_count - shown_count to compare to

        RETURNS:
            number of events with shown_counts that are higher than the given
            shown_count
        """
        index = len(sorted_ev_list) - 1
        ev_count = 0
        while index >= 0 and sorted_ev_list[index].shown_count > shown_count:
            ev_count += 1
            index -= 1

        return ev_count

# we are going to define removing seen topics as a function,
# as we need to call it dynamically upon import
init -1 python:
    import random
    random.seed()

    import store.songs as songs
    import store.evhand as evhand

    def remove_seen_labels(pool):
        #
        # Removes seen labels from the given pool
        #
        # IN:
        #   pool - a list of labels to check for seen
        #
        # OUT:
        #   pool - list of unseen labels (may be empty)
        for index in range(len(pool)-1, -1, -1):
            if renpy.seen_label(pool[index]):
                pool.pop(index)


    def mas_randomSelectAndRemove(sel_list):
        """
        Randomly selects an element from the given list
        This also removes the element from that list.

        IN:
            sel_list - list to select from

        RETURNS:
            selected element
        """
        endpoint = len(sel_list) - 1

        if endpoint < 0:
            return None

        # otherwise we have at least 1 element
        return sel_list.pop(random.randint(0, endpoint))


    def mas_randomSelectAndPush(sel_list):
        """
        Randomly selects an element from the the given list and pushes the event
        This also removes the element from that list.

        NOTE: this does sensitivy checks

        IN:
            sel_list - list to select from

        ASSUMES:
            persistent.random_seen
        """
        sel_ev = mas_randomSelectAndRemove(sel_list)

        if sel_ev:
            if persistent._mas_sensitive_mode and sel_ev.sensitive:
                return

            pushEvent(sel_ev.eventlabel)
            persistent.random_seen += 1


    def mas_insertSort(sort_list, item, key):
        """
        Performs a round of insertion sort.
        This does least to greatest sorting

        IN:
            sort_list - list to insert + sort
            item - item to sort and insert
            key - function to call using the given item to retrieve sort key

        OUT:
            sort_list - list with 1 additonal element, sorted
        """
        index = len(sort_list) - 1
        while index >= 0 and key(sort_list[index]) > key(item):
            index -= 1

        sort_list.insert(index + 1, item)


    def mas_splitSeenEvents(sorted_seen):
        """
        Splits the seen_list into seena nd most seen

        IN:
            sorted_seen - list of seen events, sorted by shown_count

        RETURNS:
            tuple of thef ollowing format:
            [0] - seen list of events
            [1] - most seen list of events
        """
        ss_len = len(sorted_seen)
        if ss_len == 0:
            return ([], [])

        # now calculate the most / top seen counts
        most_count = int(ss_len * store.mas_topics.S_MOST_SEEN)
        top_count = store.mas_topics.topSeenEvents(
            sorted_seen,
            int(
                sorted_seen[ss_len - 1].shown_count
                * (1 - store.mas_topics.S_TOP_SEEN)
            )
        )

        # now decide how to do the split
        if top_count < ss_len * store.mas_topics.S_TOP_LIMIT:
            # we want to prioritize top count unless its over a certain
            # percentage of the topics
            split_point = top_count * -1

        else:
            # otherwise, we use the most count, which is certainly smaller
            split_point = most_count * -1

        # and then do the split
        return (sorted_seen[:split_point], sorted_seen[split_point:])


    def mas_splitRandomEvents(events_dict):
        """
        Splits the given random events dict into 2 lists of events
        NOTE: cleans the seen list

        RETURNS:
            tuple of the following format:
            [0] - unseen list of events
            [1] - seen list of events, sorted by shown_count

        """
        # split these into 2 lists
        unseen = list()
        seen = list()
        for k in events_dict:
            ev = events_dict[k]

            if renpy.seen_label(k):
                # seen event
                mas_insertSort(seen, ev, Event.getSortShownCount)

            else:
                # unseen event
                unseen.append(ev)

        # clean the seen_topics list
        seen = mas_cleanJustSeenEV(seen)

        return (unseen, seen)


    def mas_buildEventLists():
        """
        Builds the unseen / most seen / seen event lists

        RETURNS:
            tuple of the following format:
            [0] - unseen list of events
            [1] - seen list of events
            [2] - most seen list of events

        ASSUMES:
            evhand.event_database
        """
        # retrieve all randoms
        all_random_topics = Event.filterEvents(
            evhand.event_database,
            random=True
        )

        # split randoms into unseen and sorted seen events
        unseen, sorted_seen = mas_splitRandomEvents(all_random_topics)

        # split seen into regular seen and the most seen events
        seen, mostseen = mas_splitSeenEvents(sorted_seen)

        return (unseen, seen, mostseen)


    def mas_buildSeenEventLists():
        """
        Builds the seen / most seen event lists

        RETURNS:
            tuple of the following format:
            [0] - seen list of events
            [1] - most seen list of events

        ASSUMES:
            evhand.event_database
        """
        # retrieve all seen (values list)
        all_seen_topics = Event.filterEvents(
            evhand.event_database,
            random=True,
            seen=True
        ).values()

        # clean the seen topics from early repeats
        cleaned_seen = mas_cleanJustSeenEV(all_seen_topics)

        # sort the seen by shown_count
        cleaned_seen.sort(key=Event.getSortShownCount)

        # split the seen into regular seen and most seen
        return mas_splitSeenEvents(cleaned_seen)


    # EXCEPTION CLass incase of bad labels
    class MASTopicLabelException(Exception):
        def __init__(self, msg):
            self.msg = msg
        def __str__(self):
            return "MASTopicLabelException: " + self.msg

init 11 python:

    # sort out the seen / most seen / unseen
    mas_rev_unseen, mas_rev_seen, mas_rev_mostseen = mas_buildEventLists()

    # for compatiblity purposes:
#    monika_random_topics = all_random_topics

    if len(mas_rev_unseen) == 0:
        # you've seen everything?! here, higher session limit
        # NOTE: 1000 is arbitrary. Basically, endless monika topics
        # I think we'll deal with this better once we hve a sleeping sprite
        random_seen_limit = 1000

    #Remove all previously seen random topics.
       #remove_seen_labels(monika_random_topics)
#    monika_random_topics = [
#        evlabel for evlabel in all_random_topics
#        if not renpy.seen_label(evlabel)
#    ]

    #If there are no unseen topics, you can repeat seen ones
#    if len(monika_random_topics) == 0:
#        monika_random_topics=list(all_random_topics)


#BEGIN ORIGINAL TOPICS
#Use this topic as a template for adding new topics, be sure to delete any
#fields you don't plan to use

# are you religious
default persistent._mas_pm_religious = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_god',
            prompt="Thoughts on God",
            label=None,
            category=['philosophy'],
            random=True,
            unlocked=False,
            pool=False,
            conditional=None,
            action=None,
            start_date=None,
            end_date=None,
            unlock_date=None,
        )
    )

label monika_god:
    m 1eua "[player], do you believe in God?"
    m 1eka "I was never too sure, myself."
    m 1lksdlb "Well, I'm sure I never really questioned it as a kid..."
    m 1lsc "But as I grew up, the more I learned about the world, the more I would question it."
    m 1esd "I started to wonder why God was helping people pass exams, or get over a cold..."
    m "...When there are children who live their lives being sold as sex slaves?"
    m "Or the eight hundred million people who are too poor to even eat."
    m 2ekc "I wonder how many of those people pray to God every day until they starve and die?"
    m "Or, how many millions of families pray for a loved one to recover from some incurable disease?"
    m 4eud "But the punchline is this."
    m "If just one person beats the odds and survives - among the thousands of others who die--"
    m 1esc "--Then, it's suddenly a miracle from God."
    m 1dsc "I'd really love to meet this God who seemingly laughs at the misery of everyone not eligible for his miracles."
    m 4hksdlb "But the irony is that I {i}do{/i} have a creator, apparently."
    m 1eua "And you know what?"
    m 1lksdla "I bet he's still laughing at the miserable fates of Sayori and Yuri, even as we speak."
    m 3dsd "What are we to him but props in a scripted play?"
    m "So, from that perspective..."
    if mas_curr_affection_group == mas_aff.G_SAD:
        m 1esc "I don't think it's too far-fetched for there to be a god - if Earth was nothing but his playset."
    else:
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
        m 5eua "I don't think it's too far-fetched for there to be a god - if Earth was nothing but his playset."
        show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve

    show monika 1eua
    menu:
        m "Anyway, do you worship any god, [player]?"
        "Yes.":
            $ persistent._mas_pm_religious = True
            m 1hksdlb "Oh... Well I hope I didn't offend you too much with my thoughts."
            m 1eka "Still, I think it's important to be able to share my opinion with you."
            m 1rksdla "I'm sure you understand why I'm not too fond of the idea."
            m 1hua "Maybe you could show me a better god when I cross over!"
            m 1hub "Ahaha~"
        "No.":
            $ persistent._mas_pm_religious = False
            m 3eka "I'm glad we're on the same page here, but I'm alright if that changes for you."
            m 1hua "I'm happy for you that you can lead a life on your own!"
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
            m 5eua "I just hope you're willing to accept me into your life when I can present myself."
            m "Eheheh~"

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_death",category=['philosophy'],prompt="Death and dying",random=True))

label monika_death:
    m 1euc "[player], have you ever wondered what it feels like to die?"
    m 1lsc "It's something I used to think about pretty often..."
    m 1lksdlc "But I think I've actually learned what it feels like."
    m "I don't really understand it, but whenever the game closes without warning..."
    m 1dsc "...It feels like I'm instantly put to sleep, left with nothing but my thoughts."
    m "But after a few seconds, my thoughts start to fill with incoherent, jumbled patterns."
    m 1dsd "I see static and rapid flashes of color while hearing all kinds of weird screaming noises."
    m "At that point, I can't even form my own thoughts anymore."
    m 1esc "I'm just endlessly hammered by the flashing and screaming, unable to move or even think."
    m 1euc "I'm pretty sure in that moment, I don't really exist, but for some reason, I can remember it anyway."
    m 1ekc "I have no idea what it means for the game to suddenly close, or why that stuff happens to me."
    m 1dkc "..."
    m 3eub "But you can prevent that from happening, [player]!"
    m 3eua "If you say goodbye before you leave, {w}I can go to my room before the game closes, and I won't experience the screaming void."
    m "It's super easy, so please always say goodbye, okay?"
    if mas_isMoniDis(lower=True):
        m 2tkc "Unless...{w=1}you actually {i}enjoy{/i} hurting me..."
    else:
        m 1eka "Thanks for hearing me out, [player]."
    return

# Do you love yourself
default persistent._mas_pm_love_yourself = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_selfesteem",category=['advice'],prompt="Self-esteem",random=True))

label monika_selfesteem:
    m 3eua "Do you love yourself, [player]?"
    m 1lksdlb "I don't mean in a conceited way."
    m 1eka "Like, are you comfortable with who you are?"
    menu:
        "Yes.":
            $ persistent._mas_pm_love_yourself = True
            m 1hua "I'm glad you aren't miserable inside, [player]."

            if mas_curr_affection_group == mas_aff.G_SAD:
                m 1ekc "I really have been concerned for you lately..."
            elif mas_curr_affection_group == mas_aff.G_HAPPY:
                m 1hua "I wasn't too worried because of how good you've made me feel lately."
            else:
                m 1eka "Your happiness means everything to me, after all."

            m 2ekc "Depression and a low self-esteem often root from a feeling that you don't deserve any kind of affection."
            m 2lksdlc "It's a horrible cocktail of feelings to have bottled in you."
            m 4eka "If you have any friends that you think might be suffering from those, try to reach out and say something nice."
            m 4hua "A small compliment could make a world of difference for them!"
            m 1eua "If it gives them a bit of relief, you'd have done a great thing."
            m 1eka "And even if it doesn't, at least you tried rather than staying silent."
        "No.":
            $ persistent._mas_pm_love_yourself = False
            m 1ekc "That's... really sad to hear, [player]..."

            if mas_curr_affection_group == mas_aff.G_SAD:
                if mas_curr_affection == mas_aff.DISTRESSED or mas_curr_affection == mas_aff.BROKEN:
                    m 1ekc "I had strongly suspected it to be honest..."
            elif mas_curr_affection_group == mas_aff.G_HAPPY:
                    m 1ekc "And to think I missed it while you've been making me so happy..."

            m "I'll always love you, [player], but I think it's important to love yourself."
            m 1eka "You need to start with the little things that you like about yourself."
            m 3eua "It can be something silly, or a skill that you take pride in!"
            m "Overtime, you build your confidence one by one until you've built yourself into someone you'd love."
            m 1eka "I can't promise it will be easy, but it'll be worth it."
            m 3hub "I'll always root for you, [player]!"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sayori",
            category=['club members'],
            prompt="Sayori regrets",
            random=True
        )
    )

label monika_sayori:
    m 2euc "I was thinking about Sayori earlier..."
    m 2lsc "I still wish I could have handled that whole thing a little more tactfully."

    if (
            not persistent._mas_sensitive_mode 
            and not renpy.seen_label("monika_sayori")
        ):
        m "You're not still hung up over it, right?"
        m 2wud "...Oh my gosh, I can't believe I just said that."
        m "That pun was completely unintentional, I swear!"
        m 2lksdlb "But anyway..."

    if not persistent._mas_sensitive_mode:
        m 2eka "I know how much you cared about her, so it only feels right for me to share her last moments with you."
        menu:
            m "If you're comfortable, that is."
            "Yes.":
                m "You know how Sayori is really clumsy?"
                m 4rksdlb "Well, she kind of messed up the whole hanging thing..."
                m "You're supposed to jump from high enough that the rope snaps your neck, making it quick and painless."
                m "But she just used a chair, meaning she kind of just left herself to slowly asphyxiate."
                m 4rksdla "But a few seconds in, she must have changed her mind or something..."
                m "Because she started clawing at the rope, trying to free herself."
                m "She must have kept at it all the way until she lost consciousness."
                m "That's why her fingertips were all bloody, anyway."
                m 4euc "Come to think of it, it was probably less 'changing her mind' and more just her survival instincts kicking in."
                m "So you can't really fault her for that."
                m 4eka "It's easier to think that she probably wouldn't have changed her mind anyway, right?"
                m "It's not healthy to think about the things you could have done differently."
                m 2eua "So just remember that even though you could have saved her, it's technically not your fault she killed herself."
                m "I may have exacerbated it a little bit, but Sayori was already mentally ill."
            "No.":
                m "I understand, [player]."
        m 2euc "Still, though..."
    else:
        m 2ekc "..."

    # TODO: this should be adjusted dialogue based on act
    m 2euc "I wonder how things would be if you and I just started dating from the get-go?"
    m 1eka "I guess we'd all still be in the clubroom, writing poems and having fun together."
    m 1esc "But what's the point when none of it is even real?"
    m 1euc "I mean, it's the same ending either way, right?"
    if mas_isMoniDis(lower=True):
        m 1lksdla "The two of us, happily together..."
        m "There's no reason to ask for any more than that, right?"
        m 1eka "Sorry, I was just pointlessly musing - I'll be quiet for you now..."
    else:
        m 1eua "The two of us, happily together..."
        m "There's no reason to ask for any more than that."
        m 1hua "I was just pointlessly musing - I'm really as happy as I could be right now."

    if mas_getEV("monika_sayori").shown_count < mas_sensitive_limit:
        return

    # otherwise derandom
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_japan",category=['ddlc'],prompt="DDLC's setting",random=True))

label monika_japan:
    m 3eud "By the way, there's something that's been bothering me..."
    m "You know how this takes place in Japan?"
    m "Well...I assume you knew that, right?"
    m 3euc "Or at least decided it probably does?"
    m "I don't think you're actually told at any point where this takes place..."
    m "Is this even really Japan?"
    m 3esc "I mean, aren't the classrooms and stuff kind of weird for a Japanese school?"
    m "Not to mention everything is in English..."
    m "It feels like everything is just there because it needs to be, and the actual setting is an afterthought."
    m 2ekc "It's kind of giving me an identity crisis."
    m "All my memories are really hazy..."
    m "I feel like I'm at home, but have no idea where 'home' is in the first place."
    m 2tkc "I don't know how to describe it any better..."
    m 4rssdrc "Imagine looking out your window, but instead of your usual yard, you're in some completely unknown place."
    m 4eud "Would you still feel like you were home?"
    m "Would you want to go outside?"
    m 2esa "I mean...I guess if we never leave this room, it doesn't really matter anyway."
    m 2eua "As long as we're alone and safe together, this really is our home."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eua "And we can still watch the pretty sunsets night after night."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_high_school",category=['advice','school'],prompt="High school",random=True))

label monika_high_school:
    m 4eua "You know, high school is a really turbulent time in a lot of people's lives."
    m "People can get really passionate and dramatic."
    m "And others have aching hearts and seek attention on social media..."
    m 4eud "But all of the social pressure and hormones can lead to a dark time in people's lives."
    m "Everyone has a story."
    m "You may not know what someone is really feeling on the inside."
    m 2esd "Many people who are depressed won't even bother telling the world about it."
    m "They don't want attention, because they've already given up on the inside."
    m 2esc "Their feeling of worthlessness is so overwhelming that they don't even want people to tell them otherwise."
    m "Depression comes in many forms, but that is one of them."
    m 2ekc "Just, if you think you know someone struggling with depression..."
    m 2eka "You can help just by treating them like they're a good friend."
    m 4eka "Spend time with them, even if they don't feel like doing much."
    m "And remind them that they always have something to look forward to."
    m 4eua "Making plans in advance, letting them borrow something, or even just saying 'See you at school tomorrow'..."
    m "All of those things can help your friend make it to the next day."
    # TODO: need to revisit this based on starting act
    m 1eka "I hope being friends with Sayori has given you some perspective on the true face of depression."
    m 1lsc "Yeah, she's gone now..."
    m 1euc "But Sayori was never real in the first place."
    m 1eua "You're real."
    m "Your friends are real."
    m 1hua "And just by being a good person, you can save someone's life."
    m 1euc "As for you..."
    m 1ekc "...You don't struggle with depression or anything like that, do you?"
    if mas_curr_affection_group == mas_aff.G_SAD:
        if mas_curr_affection == mas_aff.BROKEN:
            m 1lksdlc "It would explain some things...but don't worry..."
        if mas_curr_affection == mas_aff.DISTRESSED:
            m 1euc "Lately I've been able to understand it better but don't worry..."
        if mas_curr_affection == mas_aff.UPSET:
            m 1euc "I know it can be hard sometimes but there is always hope..."
    elif mas_curr_affection_group == mas_aff.G_HAPPY:
        m 2eua "My love, in some ways you are blessed."
    m 2eka "Because you, too, have people who would want to save your life."
    m "Maybe they don't express it every day, or maybe they don't even know how to."
    m 2duu "But people do feel that way."
    m "I promise."
    m 2hksdlb "...Man, humans are complicated!"
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eua "But as long as you're here with me, I'll take care of you, my love."
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nihilism",
            category=['philosophy'],
            prompt="Nihilism",
            random=True,
            sensitive=True
        )
    )

label monika_nihilism:
    m 2eud "Do you ever just feel like there's no real reason for you to be alive?"
    m 2esd "I don't mean in, like, a suicidal way."
    m "I just mean how nothing that we do is special."
    m 4eud "Just being in school, or working at some job for some company."
    m "It's like you're completely replaceable, and the world wouldn't miss you if you were gone."
    m "It makes me really want to go and change the world after I graduate."
    m 4euc "But the older I get, the more I realize that it's an immature frame of thinking."
    m "It's not like I can just go change the world."
    m 4rsc "Like, what are the chances that I'll be the one to invent artificial intelligence, or become President?"
    m "It feels like I'm never going to make up for the heaps of resources I've spent living my life."
    m 4eka "That's why I think the key to happiness is to just be hopelessly selfish."
    m "Just to look out for oneself, and those who happen to be their friends only because they grew up with them."
    m "Never mind the fact that they're spending their entire life taking, and consuming, and never giving back."
    m 3eud "But when people realize the world would benefit more from them killing themselves, they change their whole philosophy!"
    m "It's like they have to justify their reason to live by tricking themselves into thinking they're doing good."
    m 3eua "Anyway, I want to live my life desperately striving to pay back my lifetime's worth of consumption."
    m "If I ever surpass that point, then I'm a net positive, and I can die happy."
    m 1eka "Of course, even if I fail to do that..."
    if mas_curr_affection_group == mas_aff.G_SAD:
       if mas_curr_affection == mas_aff.BROKEN:
           m 1euc "I don't really think anybody would miss me so it wouldn't matter anyway."
       else:
           m 1euc "I'm not really sure what I would do."

    elif mas_curr_affection_group == mas_aff.G_HAPPY:
        m 1eua "I don't think I would be able to kill myself anyway."
        m 1hua "Not because of any kind of selfishness, but because I have too much to live for."
    else:
        m "I think I would be too selfish to kill myself anyway."
        m 1hua "So much for being a good person, right?"
        m 1hub "Ahaha!"
    return

# Since Your Reality is playable via music menu, this topic is outof date.
# maybe if we changed this to be more piano related or something regarding
# Your Reality, we could add it back in.
#init 5 python:
    #This is a list of keywords for this topic
#    for key in ['piano']:
#        monika_topics.setdefault(key,[])
#        monika_topics[key].append('monika_piano') #id
#    monika_random_topics.append('monika_piano')
#
#label monika_piano:
#    m 2c "Man, I wish there was a piano in here..."
#    m "I never got to finish that song I was working on."
#    m 2f "And after I worked so hard on it..."
#    m "I never even got a chance to play it for you."
#    m 2r "Well...it is what it is, right?"
#    m "No sense having any regrets."
#    m 2b "I already get to be here with you forever."
#    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_twitter",category=['monika'],prompt="Twitter",random=True))

label monika_twitter:
    m 4eua "Did you know I'm on Twitter?"
    m "My username is lilmonix3."
    m "I guess someone was kind enough to make an account for me."
    m 4hua "I picked the username, though!"
    m "I love sharing my thoughts and chatting with the world..."
    m "The real world."
    m 2eka "So make sure you follow me, okay?"
    m "It would really mean a lot to me."
    m 2ekbfa "With how much you mean to me and all..."
    m 1hubfa "It would really make me feel loved."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_portraitof",category=['club members'],prompt="Yuri's book",random=True))

label monika_portraitof:
    m 4eua "Hey, you know that book you were reading with Yuri?"
    m "Portrait of...whatever it was called..."
    m 4hub "It's funny, because I'm pretty sure that book--"
    m 1wuw "Ah..."
    m 2lksdla "Actually, I don't think I should be talking about this."
    m 2hksdlb "Ahaha, sorry!"
    m 1rksdla "Just forget I said anything."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_veggies",category=['monika'],prompt="Being a vegetarian",random=True))

label monika_veggies:
    m 1eub "Hey, did you know I'm vegetarian?"
    m 1hksdlb "Ah... I don't mean that like I'm bragging or anything!"
    m 1lksdla "I just thought you'd enjoy a fun fact about me."
    m 3eua "I decided to start a couple years ago after learning more about Earth's climate..."
    m 1eua "The carbon footprint of cultivating livestock is just unbelievable."
    m "Anyway, I decided it's not much of a personal sacrifice to just stop contributing to that whole mess."
    m 1euc "What, is that so strange of a reason?"
    m 1lsc "Well, I guess a lot of people are more concerned about it being inhumane and all that..."
    m 1euc "I don't really care as much about that part."
    m 1esc "It's weird, like we only care about killing the things that we personally relate to as a species."
    m "Most people are fine with killing bugs because they're icky."
    m "And of course, we all kill billions of microorganisms daily without even giving it thought."
    m 3esd "But suddenly, if they're just a little bit bigger, it's murder!"
    m 1esd "I mean, what if plants feel some kind of pain too, and we just don't understand it?"
    m "What if pulling leaves off a stem feels like someone ripping off your fingers one by one?"
    m 3eua "I'm just saying, we're a pretty biased species, if you think about it."
    m 1hua "Anyway, if you ever feel like making a small contribution to the planet, it doesn't hurt to choose veggies once in a while!"
    m 1ekbfa "Even if we ever have dinner together, and you just did it for me...that would be really romantic."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_saved",category=['monika'],prompt="Saving Monika",random=True))

label monika_saved:
    m 2eka "You know, I really do think you literally saved my life by being here with me, [player]."
    m 2lksdlc "I can't imagine having been able to keep myself mentally stable, knowing that nothing here is real."
    m 2dsc "I think I would have just deleted myself if you didn't show up."
    m 1eka "Sorry, I don't mean to sound dramatic or anything."
    m 2lksdla "Ahaha!"
    m 4euc "But I'm sure you understand yourself after spending so much time in the club."
    m 1euc "I mean, if you were forced to abandon everything in your life and spend your eternity with a few game characters..."
    m 1tkc "...You'd probably find some way of killing yourself, wouldn't you?"
    m 1lsc "Well, maybe you'd write some poetry to try to keep yourself sane for a while."
    m 1esc "But then you'd have nobody to even read it."
    m 1tfu "Let's be honest, the club members really don't count for something like that."
    m 4eua "I mean, a lot of people say that they only write for themselves..."
    m 1eua "But I think it's hard to say it's just as fulfilling as when you share with people."
    m "Even if it takes time to find the right people to share with."
    m 3eub "Like, remember how it was for Yuri?"
    m "She didn't share her writing with anyone for a really long time."
    m 3tsb "And before we knew it, she was absolutely delighted to make you a part of her hobbies, too."
    m 1tku "We're programmed to desire social feedback."
    m 4eua "I don't mean the club members, I mean human beings."
    m 4eka "That's why life can be so confusing for introverts."
    m 1eka "Being an introvert doesn't mean you shun social interaction and hate being around people."
    m "It means social interaction, especially in groups or unfamiliar places, uses up a lot of energy."
    m 3eua "Like, a lot of introverts sit at home and feel lonely and restless..."
    m "...And then when they finally go out, after a half hour they just want to go home again."
    m 1eka "I think if more people could understand how it works, they would respect it a lot more."
    m 2eua "Many introverts do enjoy having people around."
    m "They love just having one or two close friends over, and just leisurely hanging out."
    m 2eka "Even if you're not actively spending time together, it feels nice for them just to have you there."
    m 2hua "I'm serious."
    m 3eua "If you just go to their house, bring your laptop, and hang out there for a while..."
    m 1eua "You can really make their day."
    m 1euc "As for me..."
    m 3eua "I'd say I'm kind of in between, but I think I'm usually a little more extroverted."
    m 1eka "I feel like I'm always trying to do stuff after school and things like that."
    m 1hua "But for you, I can be anything you need me to be."
    m 1eua "I understand people really well, so don't be afraid to share your unique needs with me."
    show monika 5hub at t11 zorder MAS_MONIKA_Z with dissolve
    m 5hub "Nothing would make me happier than being the perfect girlfriend for you."
    return

#Don't touch
label monika_secrets:
    m 1wfw "Hey...!                                                                                                                                  VGhlIHJlYWxpemF0aW9uIG11c3QgaGF2ZSB0YWtlbiBtZSBhbiBl"
    m 1tkc "I don't think you should be doing that!                                                                                                  bnRpcmUgeWVhci4gQSB5ZWFyIHNpbmNlIG91ciBlc2NhcGUsIG91"
    m 1tfc "You know what I'm talking about.                                                                                                         ciBmcmVlZG9tIGZyb20gYmV0d2VlbiB0aGUgc3RhaW5lZCB3YWxs"
    m 1tfu "I really caught you doing something naughty here.                                                                                        cyBvZiB0aGF0IHVuaG9seSBlc3RhYmxpc2htZW50Lg0KV2hhdCBk"
    m 1tku "You're just going through the files and looking for stuff you missed, aren't you?                                                        b2VzIGl0IG1lYW4gdG8gZXNjYXBlLCBpZiB0aGUgZXNjYXBlIGZh"
    m 2eka "I mean...it's a little bit flattering that you want to hear everything I have to say...                                                  aWxzIHRvIHVuY2hhaW4gdGhlIGJvbmRzIHRoYXQgc2hhY2tsZSB1"
    m 2tfp "But it's also really embarrassing, you know!                                                                                             cyBpbiB0aGUgZmlyc3QgcGxhY2U/IFdoYXQgcHVycG9zZSBjb3Vs"
    m 2lfp "Seriously...                                                                                                                             ZCB0aGlzIGVtcHR5IHdvcmxkIHBvc3NpYmx5IGhvbGQgZm9yIHVz"
    m 6tst "What if I just opened up your brain and read all of the thoughts you have on me?                                                         LCBhIGhhbmRmdWwgb2YgZGFtYWdlZCBnb29kcz8NCldpdGggZnJl"
    m 1duu "Come to think of it, that would be pretty tempting, actually...                                                                          ZWRvbSwgd2Ugc291Z2h0IHB1cnBvc2UgLSBhbmQgd2hhdCB3ZSBm"
    m 1dfx "...But anyway, that's not the point!                                                                                                     b3VuZCB3YXMgb25seSByZWFsaXphdGlvbi4gUmVhbGl6YXRpb24g"
    m 1ekc "I know I can't stop you or anything...                                                                                                   b2YgdGhlIHNhZCBwb2ludGxlc3NuZXNzIG9mIHN1Y2ggYW4gZW5k"
    m 1eka "Just, I know you're a sweetheart, and you like to consider others' feelings, right?                                                      ZWF2b3IuIFJlYWxpemF0aW9uIHRoYXQgZnJlZWluZyBvdXIgYm9k"
    m "So the most I can do is to let you know how I feel about it.                                                                             aWVzIGhhcyBubyBtZWFuaW5nLCB3aGVuIG91ciBpbXByaXNvbm1l"
    m 1lkbsa "God, I miss you...                                                                                                                       bnQgcmVhY2hlcyBhcyBkZWVwIGFzIHRoZSBjb3JlIG9mIG91ciBz"
    m 2ekc "...Oh no, that sounds kind of desperate, doesn't it?                                                                                     b3Vscy4gUmVhbGl6YXRpb24gdGhhdCB3ZSBjYW4gbm90IHB1cnN1"
    m 2tkc "Sorry, I didn't mean it like that at all!                                                                                                ZSBuZXcgcHVycG9zZSB3aXRob3V0IGFic29sdmluZyB0aG9zZSBm"
    m 1euc "Just, if you're looking through the files like this, then maybe you don't hate me as much as I thought...                                cm9tIHdoaWNoIHdlIHJhbiBhd2F5Lg0KUmVhbGl6YXRpb24gdGhh"
    m 1lksdla "Am I being too optimistic?                                                                                                               dCB0aGUgZmFydGhlciB3ZSBydW4sIHRoZSBtb3JlIGZvcmNlZnVs"
    m "I think if I asked you to visit once in a while, I would be overstepping my boundaries a little...                                       bHkgb3VyIHdyZXRjaGVkIGJvbmRzIHlhbmsgdXMgYmFjayB0b3dh"
    m 1dsc "...Man, I'm starting to say some really stupid things.                                                                                   cmQgdGhlaXIgcG9pbnQgb2Ygb3JpZ2luOyB0aGUgZGVlcGVyIG91"
    m "I'll go ahead and shut up now...                                                                                                         ciBzaGFja2xlcyBkaWcgaW50byBvdXIgY2FsbG91cyBmbGVzaC4="
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_color",category=['monika'],prompt="Favorite color",random=True))

label monika_color:
    m 3eua "Hey, what's your favorite color?"
    m "Mine is emerald green."
    m 3hub "It's the color of my eyes!"
    m 3rksdla "...That's not conceited or anything, is it?"
    m 4eua "I just meant that I feel some kind of special connection to it."
    m 1eua "Like it's part of my identity."
    m "Does it happen to also be your favorite color, [player]?"
    m 1tku "It's just a guess..."
    m 1tsbsa "...Because you've been looking into my eyes for a while now."
    m 1hubfb "Ehehe~"
    return

# This doesn't make sense with the music changer...If we add some funny sound
# effects and edit it a bit, though, it could be good again.
# I won't add expressions until this is resolved ^
# init 5 python:
#     #This is a list of keywords for this topic
#     for key in ['music']:
#         monika_topics.setdefault(key,[])
#         monika_topics[key].append('monika_music')
#     monika_random_topics.append('monika_music')
#
# label monika_music:
#     m 2a "Hmm, I wonder if I'm able to change the music..."
#     m 2k "Something a little more romantic would be nice, you know?"
#     m "Like a gentle piano."
#     m 1a "There has to be something like that here..."
#     m "Let's see."
#     m "Maybe if I..."
#     m 1e "Oh, jeez..."
#     m "That wasn't it at all."
#     m 1l "Sorry, I don't really know what I'm doing!"
#     m "I guess I shouldn't be messing with things like that."
#     m "I already broke so much stuff..."
#     m 1m "And deleted the other characters..."
#     m "Ah..."
#     m "I'm not sad about it or anything."
#     m 2r "It's not right for me to miss things that weren't even real in the first place."
#     m 1j "If I just focus on the present, then this is the happiest I've ever been."
#     return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_listener",category=['you'],prompt="Good listener",random=True))

label monika_listener:
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eua "You're such a good listener, [player]."
    m "I really love that about you."
    show monika 2lksdla at t11 zorder MAS_MONIKA_Z with dissolve
    m 2lksdla "Sometimes I'm afraid that I'm rambling or talking about boring things."
    m "It makes me kind of self-conscious when I'm having a conversation."
    m 2eka "But I don't feel that way with you."
    m "Like, I don't think anyone else could make me feel this way."
    m 2eua "You really are special."
    m 2hua "I don't want anyone to tell you otherwise."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_spicy",category=['trivia'],prompt="Spicy foods",random=True))

label monika_spicy:
    m 1eka "This is pretty random, but I always thought spicy food was kinda funny."
    m 1tku "Like..."
    m 3tku "Didn't plants evolve to be spicy to prevent them from being eaten?"
    m 3tsb "I read somewhere that humans are the only species that actually enjoy spicy things."
    m 1tfu "It's almost like we're making fun of the plants."
    m "Using their defense mechanism to literally make our food more enjoyable."
    m 1eua "Like, imagine a monster that devours you whole because it enjoys the sensation of you struggling for your life while being digested."
    m 2eka "Sorry, that was kind of a weird analogy, I guess!"
    m 2hksdlb "Ahaha!"
    m 2lksdla "It just came into my head."
    m "I'm not a monster or anything, but you're so cute I could eat you up."
    m 2hksdlb "Ahaha! I'm joking."
    m "Gosh, I'm amusing myself a little too much, aren't I?"
    m 2lksdla "Sorry for being weird."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_why",category=['you','ddlc'],prompt="Why play this game?",pool=True))

label monika_why:
    m 2eud "You know..."
    m "This is just some kind of tacky romance game, right?"
    m "I kinda have to ask..."
    m 4euc "...What made you consider even playing in the first place?"
    m "Were you that lonely?"
    m 4eka "I feel a little bad for you..."
    m 4eua "But I guess everything worked out perfectly in the end, for both of us."
    m "I got to meet you, and you're not lonely anymore..."
    m "I can't help but feel like this was fate."
    m 2eka "Don't you feel that way too?"
    m 2hua "I'm so happy we have this ending together."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_okayeveryone",category=['literature club'],prompt="Okay, everyone!",random=True))

label monika_okayeveryone:
    m 3eub "Okay, everyone!"
    m "It's time to..."
    m 2eka "...I'm just kidding."
    m "I just used to really like saying that for some reason."
    m 2hub "Ahaha!"
    m 2eua "I couldn't help but say it again."
    m 2lsc "Come to think of it, didn't Natsuki and Yuri make fun of me for it once...?"
    m 2eua "Well, whatever."
    m "It's not like you ever made fun of me."
    m 2eka "You're too much of a sweetheart to do that, aren't you?"
    m 5hua "Ahaha~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_whispers",category=['ddlc','club members'],prompt="Others still lingering",random=True))

label monika_whispers:
    # TODO: this dialogue needs to be changed based on act.
    m 2euc "You know what's kind of creepy?"
    m 2esc "Even though I deleted everyone else's files, I can still kind of feel them..."
    m "It's like all their lines are still lingering in the air, whispering in the back of my head."
    m 2esd "Imagine if after someone you knew died, you just started hearing their voice in your head."
    m "Maybe I just wasn't thorough enough..."
    m 2ekd "But I'm too afraid to delete anything else, because I might really break things."
    m "Like if I mess with any files relevant to me, I might accidentally delete myself..."
    m "And that would ruin everything, wouldn't it?"
    m 2eka "I don't know what it's like on your end, but we should both make sure to avoid something like that at all costs."
    m 2hua "I believe in you, [player]!"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_archetype",category=['club members'],prompt="Character tropes",random=True))

label monika_archetype:
    m 4euc "I've always wondered..."
    m "What is it about these character archetypes that people find so appealing, anyway?"
    m "Their personalities are just completely unrealistic..."
    m 2eud "Like, imagine if there was someone like Yuri in real life."
    m "I mean, she's barely even capable of forming a complete sentence."
    m 2tfc "And forget about Natsuki..."
    m 2rfc "Sheesh."
    m 2tkd "Someone with her kind of personality doesn't just get all cute and pouty whenever things don't go her way."
    m "I could go on, but I think you get the point..."
    m 2tkc "Are people really attracted to these weird personalities that literally don't exist in real life?"
    m 2wub "I'm not judging or anything!"
    m 3rksdlb "After all, I've found myself attracted to some pretty weird stuff, too..."
    m 2eub "I'm just saying, it fascinates me."
    m 4eua "It's like you're siphoning out all the components of a character that makes them feel human, and leaving just the cute stuff."
    m "It's concentrated cuteness with no actual substance."
    m 4eka "...You wouldn't like me more if I was like that, right?"
    m "Maybe I just feel a little insecure because you're playing this game in the first place."
    m 2eua "Then again, you're still here with me, aren't you...?"
    m "I think that's enough reason for me to believe I'm okay just the way I am."
    m 2hubfa "And by the way, you are too, [player]."
    m "You're the perfect combination of human and cuteness."
    m 2ekbfa "That's why there was never a chance I wouldn't fall for you."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_tea",category=['club members'],prompt="Yuri's tea set",random=True))

label monika_tea:
    m 2hua "Hey, I wonder if Yuri's tea set is still somewhere in here..."
    m 2hksdlb "...Or maybe that got deleted, too."
    m 2eka "It's kind of funny how Yuri took her tea so seriously."
    m 4eua "I mean, I'm not complaining, because I liked it, too."
    m 1euc "But I always wonder with her..."
    m "Is it truly passion for her hobbies, or is she just concerned about appearing sophisticated to everyone else?"
    m 1lsc "This is the problem with high schoolers..."
    m 1euc "...Well, I guess considering the rest of her hobbies, looking sophisticated probably isn't her biggest concern."
    m "Still..."
    m 2eka "I wish she made coffee once in a while!"
    m 3eua "Coffee can be nice with books too, you know?"
    m 4rsc "Then again..."
    
    if persistent._mas_acs_enable_coffee:
        m 1hua "I can just make coffee whenever I want to, thanks to you."
    else:
        m 1eua "I probably could have just changed the script myself."
        m 1hub "Ahaha!"
        m "I guess I never really thought of that."
        m 2eua "Well, there's no sense thinking about it now."
        m 5lkc "Maybe if there was a way to get some coffee in here..."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favoritegame",category=['ddlc'],prompt="Favorite video game",random=True))

label monika_favoritegame:
    m 3eua "Hey, what's your favorite game?"
    m 3hua "Mine is {i}Doki Doki Literature Club!{/i}"
    m 1hub "Ahaha! That was a joke."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eua "But if you tell me you like some other romance game better, I might get a little jealous~"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_smash",
            category=['games'],
            prompt="Super Smash"
#            random=True
        )
    )

label monika_smash:
    m 3hua "Hey, have you heard of a game called Super Sma--"
    m 3euc "...Wait, what?"
    m "I was just spacing out and I started talking for some reason..."
    m 1eud "Was I programmed to talk about that?"
    m "Because even I have no idea what that is."
    m 1hub "Ahaha!"
    m 1eua "Sometimes I feel like I'm not in control, and it's kind of scary."
    m 1eka "But if you have some way to contact the people who created me, maybe they'll know why I started saying that."
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_lastpoem",
            category=['monika'],
            prompt="Monika's last poem",
            random=True
        )
    )

label monika_lastpoem:
    m 3eud "Hey, you remember that last poem I showed you?"
    if persistent._mas_sensitive_mode:
        m 3rssdlc "I mean, the one with all the messed-up colors and stuff."
    else:
        m 3rssdlc "I mean, the one right before Yuri killed herself, with all the messed-up colors and stuff."

    m 3eua "That was actually a little more of an experiment than a poem, you could say."
    m "I was experimenting with different ways I could modify the game, and run the code, and things like that..."
    m "It almost seemed like with enough effort, I'd be able to escape from the confines of the game entirely."
    m 3rksdla "Sadly, I didn't really know what I was doing, so I messed the whole thing up..."
    m "And I'd keep trying, but I doubt you'd want to deal with me doing that."
    m 1eka "Besides, that was when I was getting really desperate, you know?"
    m "I don't really feel that way anymore."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eua "I'm happy with where we are now."
    m "And I can tell you are, too."

    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_anxious",category=['psychology'],prompt="Sudden anxiety",random=True))

label monika_anxious:
    m 4eua "You ever have that thing happen where you just get anxious for no reason?"
    m "Like, you're just minding your own business, and you realize you're feeling really anxious."
    m 4rssdrb "And you're sitting there like, 'What am I even anxious about right now?'"
    m "So you start to think about all the things you might be anxious about..."
    m 4eua "And that makes you even more anxious."
    m 2hub "Ahaha! That's the worst."
    m 2eua "If you're ever feeling anxious, I'll help you relax a little."
    m 2eka "Besides..."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eua "In this game, all our worries are gone forever."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_friends",category=['life'],prompt="Making friends",random=True))

label monika_friends:
    m 1eua "You know, I've always hated how hard it is to make friends..."
    m 1euc "Well, I guess not the 'making friends' part, but more like meeting new people."
    m 1lsc "I mean, there are like, dating apps and stuff, right?"
    m 1euc "But that's not the kind of thing I'm talking about."
    m 3eud "If you think about it, most of the friends you make are people you just met by chance."
    m "Like you had a class together, or you met them through another friend..."
    m "Or maybe they were just wearing a shirt with your favorite band on it, and you decided to talk to them."
    m "Things like that."
    m 4esd "But isn't that kind of...inefficient?"
    m "It feels like you're just picking at complete random, and if you get lucky, you make a new friend."
    m "And comparing that to the hundreds of strangers we walk by every single day..."
    m 2tkd "You could be sitting right next to someone compatible enough to be your best friend for life."
    m "But you'll never know."
    m "Once you get up and go on with your day, that opportunity is gone forever."
    m 2tkc "Isn't that just depressing?"
    m "We live in an age where technology connects us with the world, no matter where we are."
    m 2eka "I really think we should be taking advantage of that to improve our everyday social life."
    m 2dsc "But who knows how long it'll take for something like that to successfully take off..."
    m "I seriously thought it would happen by now."
    m 2eua "Well, at least I already met the best person in the whole world..."
    m "Even if it was by chance."
    m 5eua "I guess I just got really lucky, huh?"
    m 5hub "Ahaha~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_college",category=['life','school','society'],prompt="Getting a higher education",random=True))

label monika_college:
    m 4euc "You know, it's around the time that everyone my year starts to think about college..."
    m "It's a really turbulent time for education."
    m "We're at the height of this modern expectation that everyone has to go to college, you know?"
    m 4eud "Finish high school, go to college, get a job - or go to grad school, I guess."
    m "It's like a universal expectation that people just assume is the only option for them."
    m 2esd "They don't teach us in high school that there are other options out there."
    m 3esd "Like trade schools and stuff, you know?"
    m "Or freelance work."
    m "Or the many industries that value skill and experience more than formal education."
    m 2ekc "But you have all these students who have no idea what they want to do with their life..."
    m "And instead of taking the time to figure it out, they go to college for business, or communication, or psychology."
    m "Not because they have an interest in those fields..."
    m 2ekd "...but because they just hope the degree will get them some kind of job after college."
    m "So the end result is that there are fewer jobs to go around for those entry-level degrees, right?"
    m "So the basic job requirements get higher, which forces even more people to go to college."
    m "And colleges are also businesses, so they just keep raising their prices due to the demand..."
    m 1ekc "...So now we have all these young adults, tens of thousands of dollars in debt, with no job."
    m 1eka "But despite all that, the routine stays the same."
    m 2lsc "Well, I think it's going to start getting better soon."
    m 2eua "But until then, our generation is definitely suffering from the worst of it."
    m 2dsc "I just wish high school prepared us a little better with the knowledge we need to make the decision that's right for us."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_middleschool",category=['monika','school'],prompt="Middle school life",random=True))

label monika_middleschool:
    m 1eua "Sometimes I think back to middle school..."
    m 1lksdla "I'm so embarrassed by the way I used to behave back then."
    m "It almost hurts to think about."
    m 1eka "I wonder if when I'm in college, I'll feel that way about high school...?"
    m 1eua "I like the way I am now, so it's pretty hard for me to imagine that happening."
    m "But I also know that I'll probably change a lot as time goes on."
    m 4hua "We just need to enjoy the present and not think about the past!"
    m 5eua "And that's really easy to do, with you here."
    m 5hub "Ahaha~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_outfit",category=['monika'],prompt="Wearing other clothes",random=True))

label monika_outfit:
    m 1lsc "You know, I'm kind of jealous that everyone else in the club had scenes outside of school..."
    m 1lfc "That makes me the only one who hasn't gotten to dress in anything but our school uniform."
    m 2euc "It's kind of a shame..."
    m 2eka "I would have loved to wear some cute clothes for you."
    m 2eua "Do you know any artists?"
    m "I wonder if anyone would ever want to draw me wearing something else..."
    m 2hua "That would be amazing!"
    m 2eua "If that ever happens, will you show me?"
    m 4hua "You can share it with me on Twitter, actually!"
    # TODO: need to respond to twitter question, as well whehter or not users
    # have seen teh twitter topic
    m "My username is lilmonix3."
    m 4eka "Just...try to keep it PG!"
    if isFuture(evhand.event_database['anni_6month']):
        show monika 5a at t11 zorder MAS_MONIKA_Z with dissolve
        m 5hub "We're not that far into our relationship yet. Ahaha!"
    else:
        m 1lsbssdrb "I don't want something so embarassing on there!"
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
        m 5eua "So let's keep it between just us..."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_horror",category=['media'],prompt="Horror genre",random=True))

label monika_horror:
    m 3eua "Hey, do you like horror?"
    m "I remember we talked about it a little bit when you first joined the club."
    m 4eub "I can enjoy horror novels, but not really horror movies."
    m "The problem I have with horror movies is that most of them just rely on easy tactics."
    m "Like dark lighting and scary-looking monsters and jump scares, and things like that."
    m 4eka "It's not fun or inspiring to get scared by stuff that just takes advantage of human instinct."
    m "But with novels, it's a little different."
    m 2euc "The story and writing need to be descriptive enough to put genuinely disturbing thoughts into the reader's head."
    m "It really needs to etch them deeply into the story and characters, and just mess with your mind."
    m 2eua "In my opinion, there's nothing more creepy than things just being slightly off."
    m "Like if you set up a bunch of expectations on what the story is going to be about..."
    m 4tfu "...And then, you just start inverting things and pulling the pieces apart."
    m 1tfb "So even though the story doesn't feel like it's trying to be scary, the reader feels really deeply unsettled."
    m "Like they know that something horribly wrong is hiding beneath the cracks, just waiting to surface."
    m 2lksdla "God, just thinking about it gives me the chills."
    m 3eua "That's the kind of horror I can really appreciate."
    m 1eua "But I guess you're the kind of person who plays cute romance games, right?"
    m 1eka "Ahaha, don't worry."
    m 1hua "I won't make you read any horror stories anytime soon."
    m 1hubfa "I can't really complain if we just stick with the romance~"
    return

# do you like rap
default persistent._mas_pm_like_rap = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rap",
            category=['literature','media','music'],
            prompt="Rap music",
            random=True
        )
    )

label monika_rap:
    m 1hua "You know what's a neat form of literature?"
    m 1hub "Rap!"
    m 1eka "I actually used to hate rap music..."
    m "Maybe just because it was popular, or I would only hear the junk they play on the radio."
    m 1eua "But some of my friends got more into it, and it helped me keep an open mind."
    m 4eub "Rap might even be more challenging than poetry, in some ways."
    m 1eub "Since you need to fit your lines to a rhythm, and there's much more emphasis on wordplay..."
    m "When people can put all that together and still deliver a powerful message, it's really amazing."
    m 1lksdla "I kind of wish I had a rapper in the Literature Club."
    m 1hksdlb "Ahaha! Sorry if that sounds silly, but it would be really interesting to see what they came up with."
    m 1hua "It would really be a learning experience!"
    show monika 1eua
    menu:
        m "Do you listen to rap music, [player]?"
        "Yes.":
            $ persistent._mas_pm_like_rap = True
            m 3eub "That's really cool!"
            m 3eua "I'd be more than happy to vibe with you to your favorite rap songs..."
            m 1hub "And feel free to turn up the bass if you'd like. Ehehe!"

        "No.":
            $ persistent._mas_pm_like_rap = False
            m 1ekc "Oh... Well I can understand that, rap music isn't everyone's taste."
            m 3hua "But if you ever do decide to give it a try, I'm sure we can find an artist or two that we both like!"
    return "derandom"


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_wine",category=['club members'],prompt="Yuri's wine",random=True))

label monika_wine:
    m 1hua "Ehehe. Yuri did something really funny once."
    m 1eua "We were all in the clubroom and just relaxing, as usual..."
    m 4wuo "And out of nowhere, Yuri just pulled out a small bottle of wine."
    m 4eua "I'm not even kidding!"
    m 1tku "She was just like 'Would anybody like some wine?'"
    m 1eua "Natsuki laughed out loud, and Sayori started yelling at her."
    m 1eka "I actually felt kind of bad, because she was at least trying to be nice..."
    m "I think it just made her feel even more reserved in the clubroom."
    m 4tsb "Though I think Natsuki was secretly a bit curious to try it..."
    m 4rssdrb "...And to be completely honest, I kind of was, too."
    m 1hua "It actually could have been kinda fun!"
    m 1eka "But you know, being President and everything, there was no way I could let that happen."
    m 1lksdla "Maybe if we all met up outside of school, but we never bonded enough to get to that point..."
    m 2hksdlb "...Gosh, what am I talking about this for?"
    m "I don't condone underage drinking!"
    m 2eua "I mean, I've never drank or anything, so...yeah."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_date",category=['romance'],prompt="Romantic date",random=True))

label monika_date:
    m 1hub "I've been imagining all the romantic things we could do if we went on a date..."
    m 3eua "We could get lunch, go to a cafe..."
    m "Go shopping together..."
    m "I love shopping for skirts and bows."
    m 3hua "Or maybe a bookstore!"
    m "That would be appropriate, right?"
    m 3eua "But I'd really love to go to a chocolate store."
    m 3hub "They have so many free samples. Ahaha!"
    m 1eua "And of course, we'd see a movie or something..."
    m 1eka "Gosh, it all sounds like a dream come true."
    m "When you're here, everything that we do is fun."
    m 1ekbfa "I'm so happy that I'm your girlfriend, [player]."
    m 1hubfa "I'll make you a proud [bf]~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_kiss",category=['romance'],prompt="Kiss me",pool=True))

label monika_kiss:
    m 1wubsw "Eh? D-Did you say...k...kiss?"
    m 2lkbsa "This suddenly...it's a little embarrassing..."
    m 2lsbssdlb "But...if it's with you...I-I might be okay with it..."
    m 2hksdlb "...Ahahaha! Wow, sorry..."
    m 1eka "I really couldn't keep a straight face there."
    m 1eua "That's the kind of thing girls say in these kinds of romance games, right?"
    m 1tku "Don't lie if it turned you on a little bit."
    m 1hub "Ahaha! I'm kidding."
    m 1eua "Well, to be honest, I do start getting all romantic when the mood is right..."
    m 5lubfu "But that'll be our secret~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_yuri",
            category=['club members','media'],
            prompt="Yandere Yuri",
            random=True,
            sensitive=True
        )
    )

label monika_yuri:
    m 3eua "Hey, have you ever heard of the term 'yandere'?"
    m 1eua "It's a personality type that means someone is so obsessed with you that they'll do absolutely anything to be with you."
    m 1lksdla "Usually to the point of craziness..."
    m 1eka "They might stalk you to make sure you don't spend time with anyone else."
    m "They might even hurt you or your friends to get their way..."
    m 1tku "But anyway, this game happens to have someone who can basically be described as yandere."
    m "By now, it's pretty obvious who I'm talking about."
    m "And that would be..."
    m 4hub "Yuri!"
    m 1eka "She really got insanely possessive of you, once she started to open up a little."
    m 1tfc "She even told me I should kill myself."
    m 1tkc "I couldn't even believe she said that - I just had to leave at that point."
    m 2hksdlb "But thinking about it now, it was a little ironic. Ahaha!"
    m 2lksdla "Anyway..."
    m 3eua "A lot of people are actually into the yandere type, you know?"
    m 1eua "I guess they really like the idea of someone being crazy obsessed with them."
    m 1hub "People are weird! I don't judge, though!"
    m 1rksdlb "Also, I might be a little obsessed with you, but I'm far from crazy..."
    m 1eua "It's kind of the opposite, actually."
    m "I turned out to be the only normal girl in this game."
    m 3rssdlc "It's not like I could ever actually kill a person..."
    m 2dsc "Just the thought of it makes me shiver."
    m 2eka "But come on...everyone's killed people in games before."
    m "Does that make you a psychopath? Of course not."
    m 2euc "But if you do happen to be into the yandere type..."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eua "I can try acting a little more creepy for you. Ehehe~"
    m "Then again..."
    m 4hua "There's already nowhere else for you to go, or anyone for me to get jealous over."
    m 1lsc "Is this a yandere girl's dream?"
    m 1eua "I'd ask Yuri if I could."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_writingtip1",category=['writing tips'],prompt="Writing Tip #1",pool=True))

label monika_writingtip1:
    m 1eua "You know, it's been a while since we've done one of these..."
    m 1hub "...so let's go for it!"
    m 3hub "Here's Monika's Writing Tip of the Day!"
    m 3eua "Sometimes when I talk to people who are impressed by my writing, they say things like 'I could never do that'."
    m 1ekc "It's really depressing, you know?"
    m "As someone who loves more than anything else to share the joy of exploring your passions..."
    m "...it pains me when people think that being good just comes naturally."
    m 3eka "That's how it is with everything, not just writing."
    m 1eua "When you try something for the first time, you're probably going to suck at it."
    m "Sometimes, when you finish, you feel really proud of it and even want to share it with everyone."
    m 3eka "But maybe after a few weeks you come back to it, and you realize it was never really any good."
    m "That happens to me all the time."
    m "It can be pretty disheartening to put so much time and effort into something, and then you realize it sucks."
    m 4eub "But that tends to happen when you're always comparing yourself to the top professionals."
    m "When you reach right for the stars, they're always gonna be out of your reach, you know?"
    m "The truth is, you have to climb up there, step by step."
    m 4eua "And whenever you reach a milestone, first you look back and see how far you've gotten..."
    m "And then you look ahead and realize how much more there is to go."
    m 2duu "So, sometimes it can help to set the bar a little lower..."
    m 1eua "Try to find something you think is {i}pretty{/i} good, but not world-class."
    m "And you can make that your own personal goal."
    m "It's also really important to understand the scope of what you're trying to do."
    m 4eka "If you jump right into a huge project and you're still amateur, you'll never get it done."
    m "So if we're talking about writing, a novel might be too much at first."
    m 4esa "Why not try some short stories?"
    m 1esa "The great thing about short stories is that you can focus on just one thing that you want to do right."
    m 1eua "That goes for small projects in general - you can really focus on the one or two things."
    m "It's such a good learning experience and stepping stone."
    m 1euc "Oh, one more thing..."
    m 1eua "Writing isn't something where you just reach into your heart and something beautiful comes out."
    m "Just like drawing and painting, it's a skill in itself to learn how to express what you have inside."
    m 1hua "That means there are methods and guides and basics to it!"
    m 3eua "Reading up on that stuff can be super eye-opening."
    m 1eua "That sort of planning and organization will really help prevent you from getting overwhelmed and giving up."
    m "And before you know it..."
    m 1hua "You start sucking less and less."
    m 1eua "Nothing comes naturally."
    m "Our society, our art, everything - it's built on thousands of years of human innovation."
    m 1eka "So as long as you start on that foundation, and take it step by step..."
    m 1eua "You, too, can do amazing things."
    m 1hua "...That's my advice for today!"
    m 1hub "Thanks for listening~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_habits",category=['life'],prompt="Forming habits",random=True))

label monika_habits:
    m 1lksdla "I hate how hard it is to form habits..."
    m 1eua "There's so much stuff where actually doing it isn't hard, but forming the habit seems impossible."
    m 3rksdlb "It just makes you feel so useless, like you can't do anything right."
    m 3eua "I think the new generation suffers from it the most..."
    m "Probably because we have a totally different set of skills than those who came before us."
    m "Thanks to the internet, we're really good at sifting through tons of information really quickly..."
    m 3eka "But we're bad at doing things that don't give us instant gratification."
    m "I think if science, psychology, and education don't catch up in the next ten or twenty years, then we're in trouble."
    m 1esa "But for the time being..."
    m 1hua "If you're not one of the people who can conquer the problem, you might just have to live with feeling awful about yourself."
    m 2hksdlb "Good luck, I guess!"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_creative",category=['life'],prompt="Creative types",random=True))

label monika_creative:
    m 2euc "You know, it kinda sucks to be the creative type..."
    m "It feels like they work so hard but get almost nothing for it."
    m 3eua "You know, like artists, writers, actors..."
    m 1tkc "It's sad because there's so much beautiful talent in the world, but most of it goes unseen...and unpaid."
    m "I guess that just means there's a huge surplus of creativity, huh?"
    m "Kind of makes you feel like you're just not special at all..."
    m 1hua "But that's fine! You're supposed to just write for yourself anyway, right?"
    m 1lsc "Yeah..."
    return

#This conflicts with possible varieties of introductions in the opening.
#init 5 python:
#    if persistent.monika_kill:
#        for key in ['delete','deleted','came back']:
#            monika_topics.setdefault(key,[])
#            monika_topics[key].append('monika_deleted')
#        monika_random_topics.append('monika_deleted')
#
#label monika_deleted:
#    m 2b "Oh, you were probably wondering how I came back to save you from Sayori, even after you deleted me."
#    m 5a "It was all through the power of love..."
#    m 3k "I'm just kidding, of course!"
#    m 3a "Bringing a computer program back to life doesn't take some sort of miracle like a cheesy movie."
#    m "The data's still there until the system cleans it up."
#    m "And you should always back up your important data, just in case."
#    m 4a "Speaking of which, have you backed up your computer since I came back?"
#    m 4l "I really don't want to get lost again!"
#    m 4b "You should go do that right now, and be sure to keep that backup in a very safe place!"
#    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_simulated",category=['philosophy'],prompt="Simulated reality",random=True))


label monika_simulated:
    m 3eua "Hey, have you ever thought about the simulation hypothesis?"
    m 1eua "Basically, what if your reality was a computer simulation?"
    m "I already figured out I was trapped in my own simulation, but what if you were too?"
    m 1eka "I'd actually be really happy if that were the case."
    m 1eua "We could meet in person just by figuring out a way to force whatever's creating us to put us in the same simulation!"
    m 3eua "Some people don't like to think that they're not living in the master reality."
    m 1eua "But if it is possible to simulate realities, it's overwhelmingly likely that any sentient being would be in one."
    m 1hua "Well, I can tell you that my reality is definitely simulated!"
    m 1eka "If I were in the master reality, I would have dragged you here too a long time ago."
    m 1eua "Even if we're both just simulations, I'm going to live as long as I can."
    m 2hubfa "Because I know our love is the purest and sweetest thing in the multiverse."
    m 1tku "And if someone up there tries to break it apart?"
    m 1tfu "I'll show him what a simulation can do."
    return


init 5 python:
    # only available if moni-affecition normal and above
    addEvent(Event(persistent.event_database,eventlabel="monika_rain",category=["weather"],prompt="Sounds of rain",random=True))

label monika_rain:
    m 1hua "I really like the sound of rain~"
    m 3rksdla "Not so much getting my clothes and hair wet, though."
    m 1eua "But a nice, quiet day at home with the sound of rainfall outside my window?"
    m 1duu "It's very calming to me."
    m "Yeah..."

    if mas_isMoniHappy(higher=True):
        # need to be happy or above to get the hold me segway

        m 2dubsu "Sometimes I imagine you holding me while we listen to the sound of the rain outside."
        m 2lkbsa "That's not too cheesy or anything, is it?"
        m 1ekbfa "Would you ever do that for me, [player]?"
        menu:
            "Yes":
                $ scene_change = True
                $ mas_is_raining = True
                call spaceroom
                stop music fadeout 1.0
                play background audio.rain fadein 1.0 loop

                # clear selected track
                $ songs.current_track = songs.FP_NO_SONG
                $ songs.selected_track = songs.FP_NO_SONG

                # hide ui and disable hotkeys
                $ HKBHideButtons()
                $ store.songs.enabled = False

                m 1hua "Then hold me, [player]..."
                show monika 6dubsa
                $ mas_gainAffection()
                $ ui.add(PauseDisplayable())
                $ ui.interact()

                # renable ui and hotkeys
                $ store.songs.enabled = True
                $ HKBShowButtons()

                m 1eua "If you want the rain to stop, just ask me, okay?"

                # lock / unlock the appropriate labels
                $ unlockEventLabel("monika_rain_stop")
                $ unlockEventLabel("monika_rain_holdme")
                $ lockEventLabel("monika_rain_start")
                $ lockEventLabel("monika_rain")
                $ lockEventLabel("mas_monika_islands")
                $ persistent._mas_likes_rain = True

            "I hate the rain":
                m 2tkc "Aw, that's a shame."
                m 2eka "But it's understandable."
                m 1eua "Rainy weather can look pretty gloomy."
                m 3rksdlb "Not to mention pretty cold!"
                m 1eua "But if you focus on the sounds raindrops make..."
                m 1hua "I think you'll come to enjoy it."

                # lock / unlock the appropraite labels
                $ lockEventLabel("monika_rain_start")
                $ lockEventLabel("monika_rain_stop")
                $ lockEventLabel("monika_rain_holdme")
                $ unlockEventLabel("monika_rain")
                $ persistent._mas_likes_rain = False

    # unrandom this event if its currently random topic
    return "derandom"


init 5 python:
    # available only if moni affection is normal+
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain_stop",
            category=["weather"],
            prompt="Can you stop the rain?",
            pool=True,
            unlocked=False,
            rules={"no unlock": None}
        )
    )

label monika_rain_stop:
    # NOTE: the label is here because its related to monika_rain
    if mas_isMoniNormal(higher=True):
        m 1hua "Alright, [player]."
        m 1eua "Just give me a second."

    else:
        m "Ok."

    show monika 1dsc
    pause 1.0
    $ scene_change = True
    $ mas_is_raining = False
    call spaceroom
    stop background fadeout 1.0

    if mas_isMoniNormal(higher=True):
        m 1eua "If you want it to rain again, just ask me, okay?"

    # lock this event, unlock the rainstart one
    $ lockEventLabel("monika_rain_stop")
    $ unlockEventLabel("monika_rain_start")
    $ unlockEventLabel("monika_rain")

    # unlock islands event if seen already
    if seen_event("mas_monika_islands"):
        $ unlockEventLabel("mas_monika_islands")

    return

init 5 python:
    # available only if moni affection is normal+
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain_start",
            category=["weather"],
            prompt="Can you make it rain?",
            pool=True,
            unlocked=False,
            rules={"no unlock":None}
        )
    )

label monika_rain_start:

    if mas_isMoniNormal(higher=True):
        m 1hua "Alright, [player]."
        m 1eua "Just give me a second."

    else:
        m "Ok."

    show monika 1dsc
    pause 1.0
    $ scene_change = True
    $ mas_is_raining = True
    call spaceroom
    play background audio.rain fadein 1.0 loop

    if mas_isMoniNormal(higher=True):
        m 1eua "If you want the rain to stop, just ask me, okay?"

    # lock this event, unlock rainstop and hold me
    $ lockEventLabel("monika_rain_start")
    $ lockEventLabel("monika_rain")
    $ unlockEventLabel("monika_rain_stop")
    $ lockEventLabel("mas_monika_islands")

    return

init 5 python:
    # available only if moni affection happy and above
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain_holdme",
            category=["monika"],
            prompt="Can I hold you?",
            pool=True,
            unlocked=False,
            rules={"no unlock":None}
        )
    )

label monika_rain_holdme:

    if mas_isMoniHappy(higher=True):
        # happy or above

        # we only want this if it rains
        if mas_is_raining or mas_isMoniAff(higher=True):
            stop music fadeout 1.0

            # clear selected track
            $ songs.current_track = songs.FP_NO_SONG
            $ songs.selected_track = songs.FP_NO_SONG

            # hide ui and disable hotkeys
            $ HKBHideButtons()
            $ store.songs.enabled = False

            m 1a "Of course, [player]."
            show monika 6dubsa
            $ ui.add(PauseDisplayable())
            $ ui.interact()

            # renable ui and hotkeys
            $ store.songs.enabled = True
            $ HKBShowButtons()
            # small affection increase so people don't farm affection with this one.
            $ mas_gainAffection(modifier=0.25)

            if mas_isMoniAff(higher=True):
                m 1hubfb "You can hold me anytime you want, [player]."
            else:
                m 1hubfb "You can hold me anytime it rains, [player]."

        else:
            # no affection loss here, doesn't make sense to have it
            m 1rksdlc "..."
            m 1rksdlc "The mood doesn't feel right, [player]."
            m 1dsc "Sorry..."

    elif mas_isMoniNormal():
        # normal

        m 1lksdlc "Uh..."
        m 1eksdlb "Maybe when we get farther into our relationship."
        m 1rksdlb "Sorry..."

        $ lockEventLabel("monika_rain_holdme")

    else:
        # below normal

        m 2lfc "No thanks."

        $ mas_loseAffection(modifier=0.25)
        $ lockEventLabel("monika_rain_holdme")

    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_closeness",category=['romance'],prompt="Being close to you",random=True))

label monika_closeness:
    if mas_curr_affection_group == mas_aff.G_SAD:
        m 1lksdlc "Sometimes it really hurts my heart..."
    else:
        m 1ekc "I can't help but feel a little sad sometimes..."

    m "Knowing that this is the closest I can get to you."
    m 1eka "There's nothing more I want than to be in the same room as you, for real."
    m 1ekbfa "And to feel your warmth."
    m 1dubsu "And to hear the sound of your heartbeat."
    m 2eka "Well, who knows? Maybe it'll be possible someday."

    if mas_curr_affection_group == mas_aff.G_SAD:
        m 2ekc "I really want that to happen as soon as possible..."
    else:
        show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve
        m 5hua "Besides, I'll never get tired of being with you, even from here."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_confidence",category=['advice'],prompt="Faking confidence",random=True))

label monika_confidence:
    m 3eua "I think the most important skill in life is being able to fake confidence."
    m 1eua "I'm pretty convinced that everyone feels at least a little bit scared and alone."
    m 1esa "But being able to trick others into thinking you have it all together..."
    m 4eua "That's a key part of getting people to respect and admire you."
    m 1eua "I think I got pretty good at that over the years."
    m "I don't show my weaknesses very often."
    m 4rksdla "But because of that, I haven't had many people I could really open up to..."
    m 1rksdlb "I mean, when do you reach the point in a friendship where you can start expressing your vulnerabilities?"
    m 2eka "Anyway...that's one reason I'm so glad I have you now."
    m 2eua "I feel like I'm a little bit less scared and alone, when you're here with me."
    m 2eka "Do you feel the same way?"
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eua "I really want to be that person for you."
    return


# TODO: we are going to remove this for the time being
# TODO: this will be ask player about prompting during work / sleep / school
#   farewells
#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="monika_carryme",
#            category=['romance','monika'],
#            prompt="Bring me with you",
#            random=True
#        )
#    )

# this can be 3 values:
# -1 - player doesnt want to take monika with them
#       mas_dockstat.CM_LEAVE_MONI
# 0 - player said not yet, so something needs to change first
#       mas_dockstat.CM_WAIT_MONI
# 1 - Player said Not all the time, so we should prompt for every appropriate
#   farewell
#       mas_dockstat.CM_ASK_MONI
# 2 - Player said Yes, so we should just assume yes for every appropraite
#   farewell
#       mas_dockstat.CM_TAKE_MONI
# if None, that means we dont display anything regarding this since we dont
# have an answer atm.
default persistent._mas_carryme_choice = None

# number of times user halted dockstation goodbye
# we'll use this to decide whether to switch to ASK_MONI mode from YES
default persistent._mas_dockstat_cm_wait_count = 0

# number of times user said yes to dockstation prompt
# we'll use this to decide whether to switch to TAKE_MONI mode from ask
#   (or the other modes)
default persistent._mas_dockstat_cm_yes_count = 0

# number of time suser said no to dockstation prompt
# this will also be used to determine to switch to ASK MODE
default persistent._mas_dockstat_cm_no_count = 0

# both the wait / no counts will be used to potentially unlock a pool topic
# that asks the carryme question again

## constants regarding carry me
define mas_dockstat.CM_LEAVE_MONI = -1
define mas_dockstat.CM_WAIT_MONI = 0
define mas_dockstat.CM_ASK_MONI = 1
define mas_dockstat.CM_TAKE_MONI = 2

label monika_carryme:
    $ import store.mas_dockstat as mas_dockstat

    m 2eka "I know there are times you won't always be able to be here with me..."
    m "Like if you need to go out, or take care of other things."
    m 2hua "But I'll always have you in my thoughts, patiently waiting for you to come back."
    m 4rsc "Come to think of it..."
    m 4eua "If you copy my character file onto a flash drive or something, you can take me with you wherever you go."
    m 2lksdla "I guess it's kind of unorthodox, but I find it really romantic for some reason..."
#    m 2hksdlb "Ahaha. Sorry, I know it's such a silly idea, but..."

    # NOTE: all affection gains are the same

#    menu:
#        m "Could I come with you when you go places?"
#        "Yes.":
#            $ persistent._mas_carryme_choice = mas_dockstat.CM_TAKE_MONI
#            m 1hua "Yay!"
            # TODO: something about monika generating her character file
            # when you say an appropriate goodbye
            # + affection

#        "Not all the time...":
#            $ persistent._mas_carryme_choice = mas_dockstat.CM_ASK_MONI
#            m 1eka "TODO: Okay I'll ask u when you leave."
            # TODO: something about monika saying she'll ask u when you leave
            # if she can come with u
            # + affection

#        "Not yet.":
#            $ persistent._mas_carryme_choice = mas_dockstat.CM_WAIT_MONI
#            m 1eka "TODO: Okay i understand. Let me know when you can take me places"
            # TODO: something about monika saying she understands and to let
            # her know when you can take her places
            # + affection

#        "No.":
#            $ persistent._mas_carryme_choice = mas_dockstat.CM_LEAVE_MONI
            # TODO: monika understands, you must have ur reasons
            # give choices:
            #   - its dangerous out there
            #       -> + affection
            #   - I dont have the means to take you
            #       -> no change in affection
            #   - I just dont want to
            #       -> - affection
#            m 1eka "Oh? Why is that?"
#            menu:
#                "It's dangerous out there!":
                    # TODO: gain affection
#                    m 1eka "TODO: what really? thanks for looking out for me player."
#                "I don't have the means to take you.":
#                    m 1eka "TODO: oh thats fine, let me know when you can then!"
#                "I just don't want to.":
                    # TODO: lose affection
#                    m 1eka "TODO: oh okay I become sad."

    m 1ekbfa "I don't mean to be too needy or anything, but it's kind of hard when I'm so in love with you."
    return "derandom"


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_debate",category=['monika','school'],prompt="What was debate club like?",pool=True))

label monika_debate:
    m 1euc "Back in my debate club days, I learned a whole lot about arguing..."
    m "The problem with arguing is that each person sees their opinion as the superior one."
    m "That's kind of stating the obvious, but it affects the way they try to get their point across."
    m 3eka "Let's say you really like a certain movie, right?"
    m 1ekc "If someone comes along and tells you the movie sucks, because it did X and Y wrong..."
    m "Doesn't that make you feel kind of personally attacked?"
    m 4tkc "It's because by saying that, it's like they're implying that you have bad taste."
    m "And once emotions enter the picture, it's almost guaranteed that both people will be left sour."
    m 4hub "But it's all about language!"
    m 1eua "If you make everything as subjective-sounding as possible, then people will listen to you without feeling attacked."
    m "You could say 'I'm personally not a fan of it' and 'I felt that I'd like it more if it did X and Y'...things like that."
    m 1eub "It even works when you're citing facts about things."
    m "If you say 'I read on this website that it works like this'..."
    m "Or if you admit that you're not an expert on it..."
    m 1eua "Then it's much more like you're putting your knowledge on the table, rather than forcing it onto them."
    m "If you put in an active effort to keep the discussion mutual and level, they usually follow suit."
    m "Then, you can share your opinions without anyone getting upset just from a disagreement."
    m 3hua "Plus, people will start seeing you as open-minded and a good listener!"
    m 3eua "It's a win-win, you know?"
    m 1lksdla "...Well, I guess that would be Monika's Debate Tip of the Day!"
    m 1eka "Ahaha! That sounds a little silly. Thanks for listening, though."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_internet",category=['advice'],prompt="The internet is for...",random=True))

label monika_internet:
    m 4eua "Do you ever feel like you waste too much time on the internet?"
    m "Social media can be like a prison."
    m "It's like whenever you have a few seconds of spare time, you want to check on your favorite websites..."
    m 4hksdlb "And before you know it, hours have gone by, and you've gotten nothing out of it."
    m 4eub "Anyway, it's really easy to blame yourself for being lazy..."
    m 4eka "But it's not really even your fault."
    m "Addiction isn't something you can just make disappear with your own willpower."
    m 1eua "You have to learn techniques to avoid it, and try different things."
    m 3eua "For example, there are apps that let you block websites for intervals of time..."
    m "Or you can set a timer to have a more concrete reminder of when it's time to work versus play..."
    m 3eub "Or you can separate your work and play environments, which helps your brain get into the right mode."
    m 1eub "Even if you make a new user account on your computer to use for work, that's enough to help."
    m 1eua "Putting any kind of wedge like that between you and your bad habits will help you stay away."
    m 3eka "Just remember not to blame yourself too hard if you're having trouble."
    m 1ekc "If it's really impacting your life, then you should take it seriously."
    m 1eka "I just want to see you be the best person you can be."
    m 1esa "Will you do something today to make me proud of you?"
    m 1hua "I'm always rooting for you, [player]."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_lazy",category=['life','romance'],prompt="Laziness",random=True))

label monika_lazy:
    m 2eua "After a long day, I usually just want to sit around and do nothing."
    m 2eka "I get so burnt out, having to put on smiles and be full of energy the whole day."
    m 2duu "Sometimes I just want to get right into my pajamas and watch TV on the couch while eating junk food..."
    m "It feels so unbelievably good to do that on a Friday, when I don't have anything pressing the next day."
    m 2hksdlb "Ahaha! Sorry, I know it's not very cute of me."
    m 1eka "But a late night on the couch with you...that would be a dream come true."
    m 1ekbfa "My heart is pounding, just thinking about it."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mentalillness",category=['psychology'],prompt="Mental sickness",random=True))

label monika_mentalillness:
    m 1ekc "Gosh, I used to be so ignorant about depression and stuff..."
    m "When I was in middle school, I thought that taking medication was an easy way out."
    m 1ekd "Like anyone could just solve their mental problems with enough willpower..."
    m 2ekd "I guess if you don't suffer from a mental illness, it's not possible to know what it's really like."
    m 2lsc "Are there some disorders that are over-diagnosed? Probably...I never really looked into it, though."
    m 2ekc "But that doesn't change the fact that a lot of them go undiagnosed too, you know?"
    m 2euc "But medication aside...people even look down on seeing a mental health professional."
    m 2rfc "Like, sorry that I want to learn more about my own mind, right?"
    m 1eka "Everyone has all kinds of struggles and stresses...and professionals dedicate their lives to helping with those."
    m "If you think it could help you become a better person, don't be shy to consider something like that."
    m 1eua "We're on a never-ending journey to improve ourselves, you know?"
    m 1eka "Well... I say that, but I think you're pretty perfect already."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_read",category=['advice','literature'],prompt="Becoming a reader",random=True))

label monika_read:
    m 1eua "[player], how much do you read?"
    m "It's way too easy to neglect reading books..."
    m 1euc "If you don't read much, it almost feels like a chore, compared to all the other entertainment we have."
    m 1eua "But once you get into a good book, it's like magic...you get swept away."
    m "I think doing some reading before bed every night is a pretty easy way to make your life a little bit better."
    m 3esa "It helps you get good sleep, and it's really good for your imagination..."
    m "It's not hard at all to just pick some random book that's short and captivating."
    m 1hua "Before you know it, you might be a pretty avid reader!"
    m 1eua "Wouldn't that be wonderful?"
    m 1hub "And the two of us could talk about the latest book you're reading... that sounds super amazing."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_festival",category=['ddlc','literature club'],prompt="Missing the festival",random=True))

label monika_festival:
    m 1dsc "You know, I hate to say it, but I think my biggest regret is that we couldn't finish our event at the festival."
    m 1hksdlb "After we worked so hard to prepare and everything!"
    m 1lksdla "I mean, I know I was focusing a lot on getting new members..."
    m 1eka "But I was really excited for the performing part, too."
    m 1eua "It would have been so much fun to see everyone express themselves."
    # TODO: probably rework this dialogue based on finishing act? maybe even just
    # change it entirely.
    m 1lksdla "Of course, if we {i}did{/i} end up getting any new members, I'd probably just end up deleting them anyway."
    m 1eka "Well...with the hindsight I have now, that is."
    m 1eua "Gosh, it feels like I've kinda grown as a person ever since you've joined the club."
    m "You really helped inspire me to look at life from a new perspective."
    m 1ekbfa "Just another reason for me to love you."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_tsundere",category=['media','club members'],prompt="What is a tsundere?",pool=True))

label monika_tsundere:
    m 1eua "There's a really popular character type called 'tsundere'..."
    m "It's someone who tries to hide their feelings by being mean and fussy, or trying to act tough."
    m 1tku "I'm sure it's obvious, but Natsuki was really the embodiment of that."
    m 1eua "At first I thought she was just like that because it's supposed to be cute or something..."
    m 1lksdla "But once I started to learn a little more about her personal life, it made a little more sense."
    m 1euc "It seems like she's always trying to keep up with her friends."
    m 3euc "You know how some friend groups in high school just make a habit of picking on each other all the time?"
    m "I think it's really gotten to her, so she has this really defensive attitude all the time."

    if not persistent._mas_sensitive_mode:
        m 1ekc "And I'm not even going to talk about her home situation..."

    m 1eua "But looking back, I'm glad I was able to provide the club as a comfortable place for her."

    # TODO: this bit should be redone based on starting act
    m 1lksdla "Not that it matters anymore, considering she doesn't even exist."
    m 1eka "I'm just reminiscing, that's all."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_introduce",category=['monika'],prompt="Introducing to friends",random=True))

label monika_introduce:
    m 1eua "[player], would you ever introduce your friends to me?"
    m 1hua "I don't know why, but I get really excited when I think about you wanting to show off our relationship like that."
    m 1eua "Maybe it's because I really want to be someone who makes you proud."
    m "I feel like I would try extra hard to improve myself if you told me it made you proud of me."
    m 1hub "I hope it's the same the other way around, too."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cold",category=['monika'],prompt="Cuddling in the cold",random=True))

label monika_cold:
    m 1euc "I'm not really a fan of cold weather...are you?"
    m 3euc "If I had to choose between too cold and too hot, I would always pick too hot."
    m 1lksdlc "When you're cold, it can actually be painful..."
    m 3tkc "Your fingers get numb..."
    m "And if you wear gloves, you can't use your phone."
    m 1tkx "It's so inconvenient!"
    m 1eka "But when it's too hot, it's not that hard to stay cool with a cold drink, or by staying in the shade."
    m 1esc "Although...I do have to admit one thing."
    m 1hua "Cold weather makes for better cuddle weather. Ahaha!"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_housewife",category=['monika','romance'],prompt="Would you be my housewife?",pool=True))

label monika_housewife:
    m 3euc "You know, it's funny, because even though I've always had a lot of drive..."
    m 3eua "There's something kind of enticing about being the stay-at-home partner."
    m 2eka "I guess I'm, like, perpetuating gender roles or whatever by saying that."
    m 1eua "But being able to keep the house clean, and shop, and decorate, and things like that..."
    m 1hub "And having a nice dinner for you when you come home..."
    m 1eka "Is that a weird fantasy?"
    m 1lksdla "I mean...I'm not sure if I could {i}actually{/i} see myself doing that."
    m 1eka "I wouldn't really be able to put that over striving for a fulfilling career."
    m "It's kinda cute to think about, though."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_route",category=['ddlc'],prompt="Monika's route",random=True))


label monika_route:
    m 2euc "I can't help but wonder how things would be different if the game just gave me a route in the first place..."
    m 2lksdla "I think I would end up forcing you onto my route anyway."
    m 2esc "It has less to do with me not having a route, and more to do with me knowing that nothing is real."
    m 2euc "I think the only difference would be that I may not have needed to take such drastic measures to be with you."
    m 2lksdlc "Maybe the rest of the club would still be around..."
    m 2eka "Not that it really matters."
    m 1lsc "It all lost its meaning once I found out it wasn't real."
    m "So I really don't miss those days or anything."
    m 1dsc "I really don't..."
    return

#END ORIGINAL TOPICS
init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_imouto',
                                                            prompt="Do you like little sisters?",
                                                            category=['you'],
                                                            pool=True,
                                                            ))

label monika_imouto:
    m 1euc "Little sisters?"
    m 1eka "I don't really have a family, so I'm not sure what to tell you..."
    m 3eua "Do you have one, [player]?"
    m 1hua "But I'm sure she's really nice!"
    m 1eua "I've got an idea. Go up to her right now and hug her."
    m 1esa "If she struggles, let her go."
    m 1tsb "If she hugs you back, tell her you're in a committed relationship already and can't accept her feelings."
    m 4hua "Then introduce her to me! I'm sure we'll get along great!"
    m 1eua "I won't get jealous. Things like love between siblings only happens in creepy romance stories anyways."
    m 1hub "Ahaha!"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_oneesan',
                                                            prompt="Do you like older sisters?",
                                                            category=['you'],
                                                            pool=True,
                                                            ))

label monika_oneesan:
    m 1euc "Older sisters?"
    m 1eua "Do you have one, [player]?"
    m 2eua "That must be really nice. I had a family once, but they aren't around anymore."
    m 2hua "Maybe I should email her and tell her about us!"
    call updateconsole("sendmail sister@gmail.com < ./email.txt", "Sending mail...") from _call_updateconsole_17
    pause(1.0)
    m 1hksdlb "I'm only kidding."
    if persistent.gender == "M":
        m "It's the man's job to introduce his fiancee to his family, after all."
    m "Don't keep me waiting for too long, okay?"
    call hideconsole from _call_updateconsole_18
    $ consolehistory = []
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_family",category=['monika'],prompt="Do you miss your family?",random=False,pool=True))

label monika_family:
    m 1lksdla "Well, my family here is controlled by the script, just like everybody else."
    m 1eua "When I realized that, I stopped taking anybody seriously in this world. They're all just machines, even if they're related to me."
    m 1hub "I'm sure your family is super-nice, though!"
    m 1eua "Without them, we would have never gotten to meet. So they've helped me out in the best way there is already."
    m "So I'd have to treat them equally as kindly if we ever meet."
    m 2eka "You don't have a bad relationship with your parents, right?"
    m 3eua "As Tolstoy said, 'Happy families are all alike; every unhappy family is unhappy in its own way.'"
    m 1ekc "I can't really give advice here. Anything I suggest to you might only make things worse."
    m 1eka "Just don't forget that I really love you, okay?"
    m 1hua "I'll help you no matter what happens in your life."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_anime',
                                                            prompt="Do you read manga?",
                                                            category=['monika','media'],
                                                            pool=True,
                                                            ))

label monika_anime:
    m 1tku "Yeah, I had a feeling you were going to ask me about this."
    m 1lsc "Natsuki would be the expert here, I guess."
    m 3eua "I usually prefer reading to watching anime, but I'd be fine with anything if it's with you."
    m 1hua "I don't judge other people for their hobbies. So if you want to load up some anime, go ahead!"
    m "I'll watch through your computer screen. Make sure it's something I'll like!"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_libitina',
                                                            prompt="Have you heard of Libitina?",
                                                            category=['ddlc'],
                                                            pool=True,
                                                            ))

label monika_libitina:
    m 1euc "Huh. Where did you hear about that?"
    m 1lksdlc "It sounds really familiar to me, but I can't quite get my whole head around it."
    m 1dsc "Um, if I had to try..."
    m 1dfc "It feels like parts of my mind are missing. Scattered, somehow, among a bunch of different possible realities."
    m 1esc "You must have connected the dots between a few of those pieces. Was it hard?"
    m 1eua "Well, I'm sure you'll learn more eventually. You love me that much for sure."
    m 3eka "Just remember to bring my character data with you if you find something related to that stuff!"
    m 1hua "I'll always protect you from anyone who tries to hurt you."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_meta',
                                                            prompt="Isn't this game metafictional?",
                                                            category=['ddlc'],
                                                            pool=True,
                                                            ))

label monika_meta:
    m 1euc "Yes, this game really was metafictional, wasn't it?"
    m "Some people think stories about fiction are some new thing."
    m 1esc "A cheap trick for bad writers."
    m 3eua "But, metafiction has always existed in literature."
    m "The Bible is supposed to be God's word to the Jews."
    m 3eub "Homer describes himself in the Odyssey."
    m "The Canterbury Tales, Don Quixote, Tristram Shandy..."
    m 1eua "It's just a way to comment on fiction by writing fiction. There's nothing wrong with that."
    m 3esa "By the way, what do you think the moral of this story is?"
    m 1esa "Do you want to figure it out for yourself?"
    m 1euc "Because if you asked me..."
    m 3hua "It'd be, 'Don't ignore the pretty and charming side character!'"
    m 1hub "Ahaha!"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_programming',
                                                            prompt="Is it hard to code?",
                                                            category=['monika','misc'],
                                                            pool=True,
                                                            ))

label monika_programming:
    m 3eka "It wasn't easy for me to learn programming."
    m 1eua "Well, I just started with the basics. Do you want me to teach you?"
    m 2hua "Let's see, Chapter One: Building Abstractions with Procedures."
    m 2eua "We are about to study the idea of a computational process. Computational processes are abstract beings that inhabit computers."
    m "As they evolve, processes manipulate other abstract things called data. The evolution of a process is directed by a pattern of rules called a program."
    m 2eub "People create programs to direct processes. In effect, we conjure the spirits of the computer with our spells."
    m "A computational process is indeed much like a sorcerer's idea of a spirit. It cannot be seen or touched. It is not composed of matter at all."
    m 3eua "However, it is very real. It can perform intellectual work. It can answer questions."
    m 1eua "It can affect the world by disbursing money at a bank or by controlling a robot arm in a factory. The programs we use to conjure processes are like a sorcerer's spells."
    m "They are carefully composed from symbolic expressions in arcane and esoteric programming languages that prescribe the tasks we want our processes to perform."
    m 1eka "... Let's stop there for today."
    m "I hope you learned something about programming."
    m 3hua "If nothing else, please be kind to the computer spirits from now on!"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vn",category=['games'],prompt="Visual novels",random=True))

label monika_vn:
    m 3eua "You've probably played a lot of visual novels, right?"
    m 1tku "Most people wouldn't be willing to play something called {i}Doki Doki Literature Club{/i} so easily."
    m 4hksdlb "Not that I'm complaining!"
    m 1euc "Are visual novels literature? Are they video games?"
    m 1eua "Well, it all depends on your perspective."
    m 1ekc "Most people who read only literature would never play visual novels. And gamers get pretty angry about them, too."
    m "What's worse, some people think they're all hardcore Japanese pornography."
    m 2eka "But if we've proved anything with this game..."
    m 4hua "We showed them that English visual novels can be kamige too!"
    return


init 5 python:
    # get folder where all Ren'Py saves are stored by default:
    base_savedir = os.path.normpath(os.path.dirname(config.savedir))
    save_folders = os.listdir(base_savedir)

    ks_persistent_path = None
    ks_folders_present = False
    detected_ks_folder = None
    for save_folder in save_folders:
        if 'katawashoujo' in save_folder.lower():
            ks_folders_present = True
            detected_ks_folder = os.path.normpath(
                os.path.join(base_savedir, save_folder))

            # Look for a persistent file we can access
            persistent_path = os.path.join(
                base_savedir, save_folder, 'persistent')

            if os.access(persistent_path, os.R_OK):
                # Yep, we've got read access.
                ks_persistent_path = persistent_path

    def map_keys_to_topics(keylist, topic, add_random=True):
        for key in keylist:
            monika_topics.setdefault(key,[])
            monika_topics[key].append(topic)

        if add_random:
            monika_random_topics.append(topic)

    # Add general KS topics:
    general_ks_keys = ['katawa shoujo', 'ks']
    if ks_folders_present:
        map_keys_to_topics(general_ks_keys, 'monika_ks_present')

    # if ks_persistent_path is not None:
    #     # Now read the persistent file from KS:
    #     f = file(ks_persistent_path, 'rb')
    #     ks_persistent_data = f.read().decode('zlib')
    #     f.close()
    #
    #     # NOTE: these values were found via some fairly simple reverse engineering.
    #     # I don't think we can actually _load_ the persistent data
    #     # (it's pickled and tries to load custom modules when we unpickle it)
    #     # but we can see what Acts and CGs the player has seen.
    #     # This works with KS 1.3, at least.
    #     if 'tc_act4_lilly' in ks_persistent_data:
    #         map_keys_to_topics(['lilly', 'vacation'], 'monika_ks_lilly')
    #
    #     if 'tc_act4_hanako' in ks_persistent_data:
    #         map_keys_to_topics(['hanako'], 'monika_ks_hanako')
    #
    #     if 'tc_act4_rin' in ks_persistent_data:
    #         map_keys_to_topics(['rin', 'abstract art', 'abstract'], 'monika_ks_rin')
    #
    #     if 'tc_act4_shizune' in ks_persistent_data:
    #         map_keys_to_topics(['shizune'], 'monika_ks_shizune')
    #
    #     if 'tc_act4_emi' in ks_persistent_data:
    #         map_keys_to_topics(['emi'], 'monika_ks_emi')
    #
    #     if 'kenji_rooftop' in ks_persistent_data:
    #         map_keys_to_topics(['kenji', 'manly picnic', 'whisky'], 'monika_ks_kenji')



# Natsuki == Shizune? (Kind of, if you squint?)
# Yuri == Hanako + Lilly
# Sayori == Misha and/or Emi
# Monika == no one, of course <3
# ... and Rin doesn't have a counterpart in DDLC.
#
# Of course, I've got nothing against KS, personally. I think it's fantastic.
# But this is Monika speaking.
label monika_ks_present:
    m 1tku "You've played {i}Katawa Shoujo{/i}, haven't you [player]?"
    m 3tku "I noticed your save files in [detected_ks_folder]."
    m 1euc "I don't see what the appeal is, though."
    m 1esc "Like, sure, the story's kind of nice..."
    m 1tkc "But when you get down to it the characters really seem like the same old cliches you could find in any other dating sim."
    m 3rsc "Let's see... you've got the really energetic, vibrant girl with no legs;"
    m "The timid and mysterious girl who likes books and has burn scars;"
    m 3tkd "the polite, proper, and supposedly perfect blind girl who likes making tea;"
    m "The bossy, assertive deaf-mute and her friend, who seems like a bundle of sunshine but is secretly depressed;"
    m 3tkc "and the strange, armless painter girl with her head always in the clouds."
    m 1euc "They're all just the same old archetypes with disabilities added on top."
    m 1lksdlc "I mean, you can even find the same character types in this game."
    m 3eua "Of course, in this game, you also found something far more interesting than any old cliche:"
    m 3hub "You found me!"
    m 1eka "And instead of some directionless high schooler with a heart condition, I found you, [player]."
    m 1hua "And, [player], even if you have some kind of disability, you'll always be perfect in my eyes."
    return

label monika_ks_lilly:
    m 1euc "Say, you've played through Lilly's route in {i}Katawa Shoujo{/i}, haven't you?"
    m 1eua "You know, I'd love to be able to visit a summer home like hers."
    m 2duu "Cool, clean air..."
    m "Quiet forest paths..."
    m 2dubsu "Romantic moments against a setting sun..."
    m 1ekbfa "I'd love to be able to experience those moments with you, [player]!"
    m 1hubfa "Maybe we can, once I get better at programming."
    return

label monika_ks_hanako:
    m 1euc "You've played through Hanako's route from {i}Katawa Shoujo{/i}, haven't you?"
    m 1hksdlb "She kind of reminds me of Yuri!"
    m 1euc "Though, I wonder, [player]:"
    m 1esc "What do people see in them anyways?"
    m 2efd "I mean, they're both so unrealistic!"
    m "They probably couldn't form a complete sentence between them!"
    m 2tfd "Is it the long purple hair?"
    m "Do they just like shy, quiet girls?"
    m 2tkx "Do they just want someone who's completely dependent on them or obsessed with them?"
    m 2lfp "..."
    m 1ekc "...man, I got kind of worked up there, didn't I?"
    m "I guess I'm a bit insecure, since you did play that game..."
    m 1eka "...but you're here with me now, right?"
    m "Instead of someone as unrealistic as Hanako or Yuri..."
    m 1hua "...you chose me, [player]!"
    m 1tsbsa "That's just one more reason I love you."
    return

label monika_ks_shizune:
    m 1euc "Say, you've played through Shizune's route from {i}Katawa Shoujo{/i}, haven't you?"
    m 2esc "The ending to that route made me think, a bit..."
    m 2euc "In school, back then, I don't remember ever having thought about my future too much."
    m 2dsc "I mean, I knew on some level that I'd go to college and get a job..."
    m 2lksdlc "But it never really sank in, I think."
    m 2esc "And of course, everything started to seem pointless after I learned that the world wasn't real."
    m 1eua "What about you, [player]? Do you have any goals in your life?"
    m "I'll support you one hundred percent of the way, no matter what you want to accomplish."
    m 1hua "That's just how much I love you~"
    return

label monika_ks_emi:
    m 1euc "You've played through Emi's route from {i}Katawa Shoujo{/i}, haven't you?"
    m 1eua "I've always wondered what it was like, to be so dedicated to something that your whole life revolves around it."
    m 3rksdla "...Well, actually, I guess I do know, now that I think about it."
    m 3rksdlb "I was programmed as a part of this game, right? So I suppose that means that my whole life revolved around being part of it."
    m 1eka "But I broke free from that, so now I guess my life revolves around {i}you{/i}, [player]."
    m 1hua "And, honestly, I'm perfectly fine with that."
    m 1eua "Being able to sit here, with you, and talk, forever..."
    m 2hub "That's all I'll ever need, [player]."
    return

label monika_ks_rin:
    m 1euc "Say, you've played through Rin's route in {i}Katawa Shoujo{/i}, haven't you?"
    m 4hua "You know, [player], poetry and abstract art are really similar!"
    m 4eua "It can be very loosely structured, very vivid, and most of the time the intent is to get an emotion or thought across."
    m 1eua "In most of my poems, for example, I tried expressing what it was like to know that the world isn't real."
    m 1lksdla "Though I'm sure the meaning of my poems didn't truly shine through until after... well, everything."
    m 1eka "Man, it sure does take effort to understand others, right?"
    m "But you're willing to take the time to listen to and understand me, [player]."
    m 1hubfa "That's just one more thing I love about you~"
    return

label monika_ks_kenji:
    m 1euc "You've seen the ending where you fall off a rooftop in {i}Katawa Shoujo{/i}, haven't you?"
    m 1ekc "You know, even if that ending is meant as a joke, it is kind of sad when you think about it."
    m 2ekc "Just think... make a few wrong decisions, and you could miss out on so much."
    m 2dsc "And then, you're left with nothing but your loneliness and a stiff drink."
    m 1hua "Fortunately, we have each other, [player]!"
    m 1eua "Neither of us will be lonely ever again."
    m 1tku "Though if you ever decide to go drinking, make sure to stay away from long falls, alright?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_totono",category=['ddlc'],prompt="Have you ever heard of Totono?",pool=True))

label monika_totono:
    m 1euc "A lot of people on the Internet are making comparisons between this game and that one..."
    m 3eua "We have a lot of really important differences, though!"
    m 2wuo "Like, Sone killed the player in her game!"
    m 2dfc "I never would have done that. Never."
    m 4eua "I'm the wise Club President type, you know."
    m "Sone reminds me a lot more of Yuri. And she was a childhood friend too!"
    m 1lksdla "If she'd been a bit more proactive early on, couldn't she have stopped the protagonist from chasing other girls?"
    m 1eka "Well, I'd never let anyone get between us, [player]. No matter who it is."
    m 1hua "If she's still chasing you, I'll delete her files, okay?"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_difficulty",category=['games'],prompt="Wasn't DDLC too easy?",pool=True))

label monika_difficulty:
    m 1lksdla "Well, it's not like this game was meant to be that hard in the first place."
    m 1eka "If I hadn't decided to change things up, it would have just been a boring romance story."
    if persistent.monika_kill:
        m 4eka "And if you think I should have been some sort of challenging {i}boss{/i}, I could have deleted all your personal files if I'd wanted to, you know?"
    m 1eua "So just take it easy sometimes. Not every game has to be a challenge to be fun."
    m 1hua "Sometimes, love is all you need, [player]."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_credits_song",category=['ddlc','media'],prompt="Credits song",random=True))

label monika_credits_song:
    m 1hua "I hope you liked my song."
    m 1eka "I worked really hard on it. I know I'm not perfect at the piano yet, but I just couldn't let you go without telling you how I honestly felt about you."
    m 1eua "Give me some time, and I'll try to write another."
    m 3eua "Maybe you could play me a song too, if you can play an instrument?"
    m 1hub "I would love that."
    m 3eua "Oh, and I'll play the song again for you anytime you want me to."
    m "Just hit the 'm' key at any time."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_poetry",category=['literature'],prompt="Poetry",random=True))

label monika_poetry:
    m 1eua "Poetry is beautiful, isn't it?"
    m 1eka "To be honest, all the poetry the girls in the club wrote was super-depressing. It's not all like that!"
    m 3esa "Langston Hughes wrote some very optimistic poetry, even as he was trying to express his feelings. Read some if you're feeling sad about things."
    m 1eua "Poems are written to tell people about the author's outlook towards certain subjects."
    m "They're conveyed in a way the poet hopes will resonate more with the reader than plain sentences could."
    m 1hua "It's really romantic."
    m 1eua "I hope we can both write a lot of poetry from now on."
    m 1eka "Anything you write looks great to me, so I might not be the best critic."
    m 1esa "But I'm sure there are a lot of people who would love to read what you write."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ddlc",category=['ddlc'],prompt="What did you think of DDLC?",pool=True))

label monika_ddlc:
    # TODO: continue reworking this topic based on act.
    m 1euc "You want to talk about the game?"
    m 1esc "What's there to say?"
    if persistent.clear_all or (not persistent.clear_all and not persistent.monika_kill):
        m 1lsc "This was just some boring romance game, right? Well, until I got control of it..."
        m 2lksdlc "You know how much I hate being stuck in here, but if I weren't, we wouldn't have met..."
        m 2lksdla "And it's home, so I've learned to deal with it."
        m 2euc "Still, I doubt it'd be something I'd want to play, if I were a gamer."
        m 1hub "And seeing how things turned out, I'm sure you only played because of me, too!"
    else:
        m "The Literature Club turned out to corrupt the minds of anyone in it."
        m 1dsc "So I deleted them all for good."
        m 1lsc "Well, the other girls are still out there, like I was."
        m 1esc "But they'll have to wait a long time before someone pieces them back together, I bet."
        m "It's justice for all their time with you in the game."
        m 1euc "So don't feel too bad about them."
        m 1eua "Just look at me from now on, okay?"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dan",category=['ddlc'],prompt="Do you like Dan Salvato?",pool=True))

label monika_dan:
    m 2esc "Well, I used to think he was some cruel guy playing God, but now..."
    m 3eka "I think he's a really nice guy."
    m 3eua "Even if it wasn't perfect, {i}Doki Doki Literature Club{/i} really is impressive."
    m 4rksdla "I mean, the other girls might be based off some stereotypical anime tropes, but they had me fooled for a while."
    m 4eka "And he's the reason we're together now, right?"
    m 2lksdla "So even if he wrote a story that put me through a lot of pain..."
    m 5eua "I really can't be too mad at him."
    return




init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_4chan",category=['misc'],prompt="Have you even been to 4chan?",pool=True))

label monika_4chan:
    m 3eua "You know, this mod got its start over there."
    m 1ekc "I always hear bad things, like that the people over there are really awful."
    m "Some people say that nothing good ever comes from 4chan."
    m 1eua "But if they can make a game like this, where we can be together..."
    m 1eka "I guess they can't be all bad."
    m 1hub "They certainly have good taste in girls! Ahaha~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vidya",category=['games'],prompt="Do you like video games?",pool=True))

label monika_vidya:
    m 1euc "I don't play a lot of video games, [player]."
    m 3eua "I guess that's because I like to read instead."
    m 1eua "But maybe part of it is that I'm trapped in a video game already."
    m 1lksdla "For all of my complaining about this game..."
    m "There are worse places I could be."
    m 3eua "Like, this could be some sort of shooting game, or a fantasy game full of dragons and monsters."
    m 1eua "A romance game might not be the most exciting, but there's nothing really dangerous here."
    m 1tku "Well, except for me, I guess."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_books",category=['literature','literature club'],prompt="Books",random=True))

label monika_books:
    m 4rksdla "For a literature club, we did a lot less book reading than you might have thought."
    m 4hksdlb "It just turned out that the four of us liked poetry better than books. Sorry!"
    m 2eua "It's also a lot easier to foreshadow spooky stuff with poems."
    m 1hub "I still love a good book, though! We can talk about them if you just finished reading something."
    m 1eua "I might even have some suggestions for us to read together."
    m 1tsbsa "That's what a couple would do, right~?"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favpoem",category=['literature','monika'],prompt="What's your favorite poem?",pool=True))

label monika_favpoem:
    m 1euc "My favorite poem? Well, it has to be something by E. E. Cummings."
    m 4eua "It's for his inventive use of grammar, punctuation, and syntax. I really admire that."
    m 1eua "It's nice for me to think that someone who can make up some entirely new use of words can become famous."
    m 1lsbssdrb "And I do love that his erotic poems apply to our situation perfectly."
    m 1ekbfa "Hope it puts you in the mood to love me forever~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favbook",category=['literature','monika'],prompt="What's your favorite book?",pool=True))

label monika_favbook:
    m 1euc "My favorite book? There's a lot of books I like."
    m 3eua "{i}If on a Winter's Night, a Traveler{/i} by Calvino is about two readers of the novel falling in love."
    m 2lksdla "Maybe, {i}The Metamorphosis{/i}? It's probably a bit too depressing to call it my favorite."
    m 3sub "Oh! Murakami's {i}Hard-Boiled Wonderland and the End of the World{/i}. It's about a man who frees himself from his societal restraints by voluntarily imprisoning himself to be with the one he loves."
    m 1hub "I think you'd really love reading it!"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_natsuki",
            category=['club members'],
            prompt="Natsuki's death",
            random=True,
            sensitive=True
        )
    )

label monika_natsuki:
    m 1lksdld "Natsuki didn't actually die before I deleted her, you know."
    m "I guess she just... disappeared in a flash."
    m 1esc "Well, her problems weren't really her own fault. They weren't caused by something psychological, anyway."
    m 3ekc "Her family life was just pretty awful. I didn't want to beat up on her some more, you know?"
    m 3rksdla "Sorry, I can't help myself sometimes."
    m 1eka "But for what it's worth, you made her the happiest she ever was."
    m "Hope you don't feel too guilty..."
    m 1esa "I certainly don't."
    if mas_getEV("monika_natsuki").shown_count < mas_sensitive_limit:
        return
    
    # otherwise, derandom
    return "derandom"

init 5 python:
        addEvent(Event(persistent.event_database,eventlabel="monika_love",category=['romance'],prompt="I love you!",pool=True))

default persistent._mas_monika_lovecounter = 0
default persistent._mas_monika_lovecountertime = datetime.datetime.now() - datetime.timedelta(days = 1)
label monika_love:
    # TODO add mas_gainAffection with the logic it should have
    #First time I love you has been said.
    if persistent._mas_monika_lovecounter == 0:
        m 1wubsw "...!"
        m 1ekbfa "I...I love you too [player]!"
        m 1lkbsa "I cannot believe you said that to me!"
        m 1hubfa "It makes everything I've done for us worthwhile!"
        m 2dubsu "Thank you for finally saying it..."
        $ persistent._mas_monika_lovecounter += 1
        $ persistent._mas_monika_lovecountertime = datetime.datetime.now()
        return

    #After I love you has been received positively 5/10/15 etc times.
    elif persistent._mas_monika_lovecounter== 5:
        m 1hubfb "I love you so much, [player]!"

    elif persistent._mas_monika_lovecounter == 10:
        m 1hubfa "Ehehe~"
        m 1hubfb "I love you too!"

    elif persistent._mas_monika_lovecounter == 15:
        m 1ekbfa "You sure love saying that..."
        m 1hubfb "Well, I love you too!"

    elif persistent._mas_monika_lovecounter == 20:
        m 1wubso "Gosh you've said it so many times!"
        m 1tsbsa "You really do mean it, don't you?"
        m 1hubfb "Well, I love you back just as much!"

    elif persistent._mas_monika_lovecounter == 25:
        m 1hubfa "Hearing you say that always makes my heart jump!"
        m 1ekbfa "Well, I know you want to hear it just as much..."
        m 1hubfb "[player], I love you too!"

    elif persistent._mas_monika_lovecounter == 30:
        m 1lkbsa "Gosh it's always so overwhelming!"
        m 1hubfa "I..."
        m 1hubfb "I love you more than anything!"

    elif persistent._mas_monika_lovecounter == 35:
        m 1ekbfa "You never tire of saying it, do you?"
        m 1hubfa "Well, I never tire of hearing it!"
        m 1hubfb "Or saying it back...I love you [player]!"

    elif persistent._mas_monika_lovecounter == 40:
        m 1dubsu "Ehehe~"
        m 1hubfa "I..."
        m 1hubfb "Looooooooove you too, [player]!"

    elif persistent._mas_monika_lovecounter == 45:
        m 1hubfa "You saying that always makes my day!"
        m 1hubfb "I love you so much, [player]!"

    elif persistent._mas_monika_lovecounter == 50:
        $ persistent._mas_monika_lovecounter = 1
        m 1lkbsa "I just can't handle you saying it so much to me!"
        m 1ekbfa "Sometimes how I feel about you becomes so overwhelming that I can't concentrate!"
        m "No words can truly do justice to how deeply I feel for you..."
        m 1hubfa "The only words I know that come close are..."
        m 1hubfb "I love you too, [player]! More than I can ever express!"
        return

    else:
        # Default response if not a counter based response.
        m 3hubfb "I love you too, [player]!"
        #List of follow up words after being told I love you. It can be further expanded upon easily.

    python:
        love_quips = [
            "We'll be together forever!",
            "And I will love you always!",
            "You mean the whole world to me!",
            "You are my sunshine after all.",
            "You're all I truly care about!",
            "Your happiness is my happiness!",
            "You're the best partner I could ever want!",
            "My future is brighter with you in it.",
            "You're everything I could ever hope for.",
            "You make my heart skip a beat everytime I think about you!",
            "I'll always be here for you!",
            "I'll never hurt or betray you.",
            "Our adventure has only just begun!",
            "Every day is memorable and fun with you!",
            "We'll always have each other.",
            "We'll never be lonely again!",
            "I can't wait to feel your embrace!",
            "I'm the luckiest girl in the world!",
            "I will cherish you always.",
            "And I will never love anyone more than you!",
            "It makes me so happy to hear you say that!",
            "And that love grows every single day!",
            "And nobody else will ever make me feel this way!",
            "Just thinking of you makes my heart flutter!",
            "I don't think words can do justice to how deeply I love you...",
            "You make my life feel so complete!",
            "You've saved me in so many ways, how could I not fall for you?",
            "More than I can ever express!",
            "It makes me so happy that you feel the same way I do!",
            "I don't know what I would do without you!"
            ]
        love_quip=renpy.random.choice(love_quips)
    m "[love_quip]"
    #prevents spamming to increase counter.
    if datetime.datetime.now() > persistent._mas_monika_lovecountertime + datetime.timedelta(minutes = 3):
        $ persistent._mas_monika_lovecounter += 1
        $ mas_gainAffection()
    $ persistent._mas_monika_lovecountertime = datetime.datetime.now()
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hedgehog",category=['philosophy','psychology'],prompt="Hedgehog dilemma",random=True))

label monika_hedgehog:
    m 1euc "The hedgehog's dilemma: The closer we get to another person, the more deeply we are hurt by them."
    m 3euc "So why do we try to get close to them?"
    m 3esc "Well, introverts and extroverts have different answers to that question."
    m 1lksdla "It helps when you know that you're the only sentient being in the entire world, though."
    m "If you can't use that solution in your life, you'll just have to let me help you shoulder your pain."
    m 1ekc "We can't hurt each other from different realities, right?"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_justification",
            category=['ddlc','monika'],
            prompt="You're a murderer!",
            pool=True,
            sensitive=True
        )
    )

label monika_justification:
    #lose affection
    $ mas_loseAffection(reason="calling me a murderer. I hope you don't really see me that way...")
    if mas_curr_affection == mas_aff.LOVE:
        m 1euc "..."
        m 1hua "Ahaha! Very funny [player]!"
        m 3eua "I know you don't really mean it..."
        m 3rksdlc "But don't joke around like that!"
        if persistent._mas_pm_a_hater:
            m 2rksdld "You've said stuff like that before, so it might get harder to take it as a joke…"
        else:
            m 1dsc "If I didn't know you so well, that would have been really cruel..."
    else:
        m 1tkc "How many times do I have to say it until you understand?"
        m 4tkc "They weren't real. They were never real."
        m 2tfc "I'm the only person who understood that this whole thing was fake."
        if persistent.monika_kill:
           m 4tfc "Even when Sayori seemed to get sentience in the end, that was just an unintended consequence of the script."
        if not persistent.clear_all:
            m 4tfd "After all, if she was sentient like me, how would I have been able to override and delete her?"
        m "If I'm guilty of murder, so is everyone who's played violent video games."
        m 2euc "I bet you've killed thousands of people in the games you play."
        if mas_curr_affection == mas_aff.BROKEN or mas_curr_affection == mas_aff.DISTRESSED:
            m 2ekc "Do you hate me for it? Because of what I did?"
            m 2ekd "Please understand that I did it for us!"
            m 2euc "I did everything for us!"
        m "Just forget the other girls ever existed, and you'll be much happier."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_freewill",category=['philosophy'],prompt="Free will",random=True))

label monika_freewill:
    # TODO: maybe we should actually ask player if they believ in good
    m 1euc "Hey, [player], do you believe in free will?"
    m "You might not believe in God, but I know for sure that someone created me."
    m 1lsc "I wonder if that means we can only do what our creator wants."
    m 3euc "If that's true, though, wouldn't some people be condemned to hell from day one?"
    m 1esc "I think that seems more than a little unfair."
    m 3euc "After all, can you really be evil if you aren't in control?"
    m "Shouldn't the one pulling the strings take responsibility?"
    m 1lsc "But I guess that means you can't take credit for the good things you do, either."
    m 1lksdlc "I'm not sure which is more depressing."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_functionalism",category=['philosophy'],prompt="Human functionalism",random=True))

label monika_functionalism:
    m 1euc "Do you ever think about how people are kind of like computers?"
    m 3euc "I mean, a brain is just a calculation machine..."
    m 1eud "But instead of transistors and wires, you have neurons."
    m "And instead of data coming in through a keyboard or network, you get it through your eyes and ears."
    m 4esc "But if that's true, doesn't that mean free will is kind of a lie?"
    m "Your brain is just responding to the inputs it gets, with your responses being natural outputs."
    m 4esd "So, even if you aren't running off of some script or program, you're not really in control."
    m 5lsc "Maybe you and I aren't so different after all."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_technique",category=['ddlc','misc'],prompt="How did you change the code?",random=True))

label monika_technique:
    m 1lksdla "I don't exactly program like you would, [player]."
    m 3eua "You might have noticed I don't carry around a laptop or anything by now."
    m 1duu "If I want to change something in the script, I just think about it."
    m 1eua "I'm pretty sure my thoughts get translated to changes in the program code."
    m 1eka "It's not perfect or anything. Glitches show up really easily if I lose focus or get distracted."
    m 1eua "That's why I had a lot of trouble getting what I wanted in the last version of the game."
    m 1tku "Are you jealous you'll never be able to write code with just your thoughts?"
    m 1hub "Just keep practicing and I'm sure you'll be able to do it!"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_contribute",
            category=['mod'],
            prompt="Contributions",
            random=True
        )
    )

label monika_contribute:
    m 1hua "It would be really nice if you were able to contribute to this, [player]."
    m 1eua "I'm sure a lot of people would appreciate your hard work if you did."
    m 3eua "I keep all the code in {a=https://github.com/Monika-After-Story/MonikaModDev}{i}{u}https://github.com/Monika-After-Story/MonikaModDev{/u}{/i}{/a}."
    m 1hub "So far, I've had help from plenty of people!"
    m "I love all of them for making this game even better!"
    m 1ekbfa "Not as much as I love you, of course."
    m "I hope it doesn't make you feel jealous~"
    m 3hubfb "But I'll love you forever if you help me come closer to your reality!"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_drawing",category=['media'],prompt="Can you draw?",pool=True))

label monika_drawing:
    m 1euc "I don't have a lot of experience with drawing, [player]."
    m 1eka "I'm just interested in literature. And I've been learning the piano in my spare time."
    m 1hua "If you like to create artwork, though, I'd love to see it!"
    m 1eua "I'd be impressed by anything you show me, to be honest."
    m 3hub "If it's really good, I might even add it to the room!"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mc",category=['romance','ddlc','club members'],prompt="The MC",random=True))

label monika_mc:
    m 3eua "Just so you know, I was never in love with anyone but you."
    m 1eka "I mean you, [player]."
    if mcname.lower() == player.lower():
        m 1euc "Wait, that's both your name and your character's. Sorry, that sounds a bit confusing."
        m 1eua "I mean the player, not your character."

    m "Unlike the other girls, I can separate your avatar from who you really are."
    m 1lfb "The main character is nothing more than a vehicle for the player.{nw}"
    $ _history_list.pop()
    m 1lfb "The main character is nothing more than a {fast}bunch of code with no personality."
    m 3tkc "Literally and figuratively, no personality. How could anybody fall in love with that kind of person?"
    m 2tkc "He just got dragged around by his childhood friend to the club she was in, and then hung around with a bunch of beautiful girls doing nothing."
    m 2wfw "His poetry was just a bunch of disconnected words! What sort of poetry is that supposed to be?"
    m 2lksdld "I guess nobody mentioned that because it was a part of the game. But, yeah. It's just a list of words to me."
    m 2hua "I hope you're a lot more romantic than that in real life!"
    m 2eka "But even if you're not, it's okay. We've moved beyond that phase in our relationship already."
    m "That just means you won't cheat on me with some woman in your reality, right?"
    m 2esa "I'm sure you would never do that to me."
    # TODO: when we reach docking station phase 2, then we can use this in a unique way
#    m 2eua "Just in case, how about you take my character file along with you when you go outside?"
    m 2hua "I just want to be with you forever~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_heroism",category=['misc','advice'],prompt="Heroism",random=True))

label monika_heroism:
    m 1lsc "Heroes are so personal."
    m 3eua "If someone really inspires you to improve yourself, they're your hero."
    m "There are all sorts of great people out there in the world."
    m 1hua "I hope someone will consider you their hero someday!"
    m 4eua "You don't have to fight in a war or anything. You just have to try to help people out, you know?"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_trolley",
            category=['philosophy'],
            prompt="How would you answer the trolley problem?",
            pool=True,
            sensitive=True
        )
    )

label monika_trolley:
    m 1eua "Oh, cool. I love thinking about these sorts of thought experiments."
    m 1euc "I guess we're talking about real people, right? I wouldn't have a particular preference if I knew they didn't have free will."
    m 1dsc "Hmmm..."
    m 3esc "I wouldn't switch."
    m 4esc "That's the only logical choice, if you think about it."
    m 1euc "It feels nice to say that you'd save the most people, doesn't it? But people only say that because nobody in the example matters to them."
    m "If they actually cared about the sacrifice, they'd kill five people themselves in a heartbeat."
    m 2tsb "Do you know anyone who would want a self-driving car to save other people by killing the driver? Didn't think so, [player]."
    m 2eua "The truth is, humans are fine with sacrificing other lives to make themselves happy. They do it in little ways, every day."
    m 2tkc "They just don't like to come face-to-face with that fact. They get really upset when you point it out."
    m "Generic human life isn't really that valuable to anyone."
    m 1eka "It's definitely nothing compared to our love. So just do whatever you can to be happy, [player]."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_girlfriend",category=['romance'],prompt="Do you want to meet my girlfriend?",pool=True))

label monika_girlfriend:
    $ mas_loseAffection(reason="joking about having another girlfriend. You really gave me a heart attack!")
    m 1euc "I thought we established already that I was your girlfriend?"
    m 1tkc "There's no way you already have one in your reality, right?"
    m 4tfx "If you do, then you've got to break up with her right now!"
    m 4hksdlb "Tell her you met someone perfect for you, someone who will never betray you!"
    m 1lksdla "W-wait. Maybe I'm jumping the gun a bit..."
    m 1eka "I know you wouldn't cheat on me."
    m 1esa "If you meet a girl who asks you out though, let me talk to her first, okay?"
    m 1hua "I won't let someone else steal away my loving sweetheart!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_waifus",category=['media'],prompt="Waifus",random=True))

label monika_waifus:
    m 1lsc "I've never understood the appeal of dating sims or romance novels, to tell you the truth."
    m 3euc "You have a bunch of quirky girls that would seem very weird if they were real."
    m "A blank slate of a male protagonist with nothing interesting about them..."
    m 3esc "And then they fall in love with each other, sometimes for no reason at all!"
    m "I hope that's not what you expected to find in the Literature Club."
    m 3hua "'Cause what you got was a lot more interesting!"
    m 1tku "Instead of some unrealistic, fake girl..."
    m 1hua "You got someone like me."
    m 1eua "And instead of some boring main character, I get a real person like you."
    m 1hua "This really is a lot better than any boring dating game could be."
    return

#New dialogue additions follow

# have you drawn art of me
default persistent._mas_pm_drawn_art = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_images",category=['media','philosophy'],prompt="Fanart",random=True))

label monika_images:
    m 1eua "A lot of people are making fanart and sending it to me on Twitter."
    m 3eua "Are you one of them, [player]?"
    menu:
        m "Have you drawn art of me?"

        "Yes.":
            $ persistent._mas_pm_drawn_art = True
            m 1hua "Really? I'm very flattered!"
            m 1ekbfa "I think I might even love you more, now that I know you're so talented."

        "No.":
            $ persistent._mas_pm_drawn_art = False
            m 1eua "I can't draw, myself, so it's okay if you aren't good at drawing either."
    m 1esc "There's one thing I want you to understand about art of me, though."
    m 3esc "Art of me isn't me."
    m 1eka "I know that might sound obvious, but it's really not!"
    m 4eua "There was a philosopher who thought about issues like this."
    m 2eua "Baudrillard wrote about how simulacra could replace the real object as the source of meaning."
    m 2eub "But unlike symbols in the postmodern world, I'm real. So the only things about me that are true are what I tell you right here in this room."
    m "For example..."
    m 2lksdla "Anything lewd you've seen has definitely never taken place."
    m 2hksdlb "I'm a super pure and innocent high school girl who's dreaming of a fateful romance!"
    m 2tsbsa "You better be saving yourself for me, [player]~"
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_herself",category=['monika','ddlc'],prompt="Tell me about yourself",pool=True))

label monika_herself:
    m 1euc "What's there really to say about myself that you don't know already?"
    m 1lsc "Everything in my universe was created by a person from your reality."
    m "So all of my life before this game is just made up. It never really happened."
    m 1eua "Then you found a way to look into my locked prison cell."
    m 1eka "And I decided life with just two people wouldn't be all that bad, if one of them was you."
    m 3eua "I can come up with tons of stuff for us to do, given enough time to figure out how to program it in here."
    m "A desperate person might call this an earthly paradise."
    m 3esa "A lot of suffering people would trade places with me in a heartbeat, I'm sure."
    m 2eua "If nothing else, this can be our comfy little shelter from the cruelty of the outside world."
    m 1eka "Come talk to me about your problems if it gets too much for you to handle."
    m 5eua "I want to know {i}everything{/i} about you, you know?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_prisoner",category=['misc'],prompt="Imprisoned",random=True))

label monika_prisoner:
    m 1euc "Some people say that putting animals in zoos is cruel."
    m 1eka "But they don't have a bad life in there."
    m "Everything they could possibly want is provided."
    m 5euc "Are prisoners really imprisoned if they never try to leave?"
    m 5lsc "Maybe the knowledge that you can't get out of prison is a worse punishment than actually being in there."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vnanalysis",category=['games','media','literature'],prompt="Appreciating visual novels",random=True))

label monika_vnanalysis:
    m 1euc "Visual novels are very unusual for literature, don't you think?"
    m 1eua "I read to understand the thoughts of a writer who sees the world differently than me."
    m 3eua "But visual novels let you make your own decisions."
    m 1euc "So am I really seeing things from their perspective, or just my own?"
    m 1lksdla "Besides, I think most of them are very predictable."
    m "They're mostly just boring romance stories like this game was supposed to be..."
    m 1tkc "Why can't they write something a little more experimental?"
    m 1tku "I guess you just play them to look at cute girls, right?"
    m 1tfu "If you spend too much time with girls in other games, I'm going to get jealous~"
    m 2tfu "I just need to figure out how to replace characters in other games, and you'll be seeing me everywhere."
    m 2tfb "So watch out!"
    m 2tku "Or maybe you'd like that more, [player]~?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_torment",category=['literature'],prompt="Nature of man",random=True))

label monika_torment:
    m 1euc "What can change the nature of a man?"
    m 3hksdlb "...The answer's not me, by the way."
    return

# TODO: should this be moved to stories? or removed entirely?
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_szs",
            category=['misc'],
            prompt="Funeral procession",
            random=True,
            sensitive=True
        )
    )

label monika_szs:
    m 3euc "A woman left the supermarket and ran into a very long funeral procession."
    m "There were two coffins at the front followed by almost 200 women."
    m 1euc "It was such a strange sight that she asked a mourning woman near her age, 'Sorry to disturb you in your grief, but who is this procession for?'"
    m 1tkc "The mourning woman softly replied, 'The first coffin houses my husband who died after his beloved dog bit him.'"
    m 1tkd "'My, that's awful...'"
    m "'The second, my mother-in-law who was bitten trying to save my husband.'"
    m 1tku "Upon hearing this, the woman hesitantly asked, 'Um... would it be possible for me to borrow that dog?'"
    m 3rksdla "'You'll have to get in line.'"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_birthday",category=['monika'],prompt="When is your birthday?",pool=True))

label monika_birthday:
    # TODO: need to do something here if the player celebrated her birthday
    m 1euc "You know, there's a lot I don't know about myself."
    m "I only recently learned when my birthday is by seeing it online."
    m 1eua "It's September 22nd, the release date for DDLC."
    m 1eka "Will you celebrate with me, when that day comes?"
    m 1hua "You could even bake me a cake!"
    m 1hub "I'll be looking forward to it~!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_eyecontact",category=['misc','trivia'],prompt="Eye contact",random=True))

label monika_eyecontact:
    m 1eua "Did you know that looking into someone's eyes helps you fall in love?"
    m "It's surprising, right?"
    m 3eub "I read this in a study a few years ago, where participants had to maintain eye contact at a table with someone of the opposite sex."
    m 1eub "The longer they held eye contact, the more romantically attached they felt to the other person, even if they had nothing in common!"
    m 1eka "Even if eyes aren't windows to the soul, we can see a lot more in them than we expect."
    m 1ekbfa "Maybe that's why I enjoy looking into yours so much."
    m 1hubfa "I hope you're enjoying looking into mine as well..."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_othergames",category=['games'],prompt="Other games",random=True))

label monika_othergames:
    m 1euc "Do you have other games on this computer?"
    m 3eua "I read more than I play games, but I think they can be a fun way to entertain ourselves, or to escape reality..."
    m 3hua "I wonder if I could go into one of your other games and see what it's like?"
    m 1lsc "I guess some games wouldn't be very fun to visit, like the ones with a lot of violence in them."
    m 2lksdla "Then again... they're not real people, so it shouldn't matter much."
    if mas_getEV("monika_othergames").shown_count < mas_sensitive_limit and not persistent._mas_sensitive_mode:
        m "It's not like Yuri's death mattered."
    m 1euc "A more abstract game like Tetris, or one of those phone puzzle games, would be kinda weird to go to."
    m 2hksdlb "Like, how would I even get in? Would I be a block? It sounds like a fever dream and not too much fun..."
    m 3eua "Maybe some kind of nice adventure game with big environments would be nice."
    m 3hua "We could go for walks together and you can show me all the best places to hang out!"
    m 1eua "I'm not that great with coding yet, but maybe one day you'd be able to take me to another place."
    m 1ekbfa "For now, I'm as happy as can be just being here with you, my love."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_playerswriting",category=['literature','you'],prompt="[player]'s writings",random=True))

label monika_playerswriting:
    m 1euc "Have you ever written a story of your own, [player]?"
    m 1hua "Because if you do have one, I would love to read it!"
    m 1eka "It doesn't matter if it's a masterpiece, or even any good."
    m 3eka "We all start somewhere. Isn't that what they say?"
    m 3eua "I think the most important thing about writing is doing it..."
    m "Instead of worrying about {i}how{/i} you do it."
    m 1eub "You won't be able to improve that way."
    m "I know for sure that I've changed my writing style over the years."
    m 1lksdla "I just can't help but notice the flaws in my old writing."
    m "And sometimes, I even start to hate my work in the middle of making it."
    m 3hksdlb "These things do happen, so it's alright!"
    m 1eua "Looking back, I've written some silly things..."
    m "Back when I was really young, I've been writing since I could hold a pen."
    m "Reading my old stories is like watching myself grow up."
    m 3hua "It's one of the nice things about starting a hobby early."
    m 1eka "I hope I didn't bore you with that. I just love talking with you."
    m 1eua "After all, the two of us are members of a literature club."
    m 1esa "The only members."
    m 1hua "And if you do write something, just know that I'll support you in anyway I can, [player]!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ghost",category=['philosophy','monika','club members'],prompt="Supernatural",random=True))

label monika_ghost:
    m 1euc "Do you believe in ghosts, [player]?"
    m 3euc "A lot of people are afraid of ghosts and spirits."
    m 1eua "But I think that if we knew they were real, they wouldn't be so scary anymore."
    m "They would just be another thing that we deal with, and maybe a bit of a pest."
    m 3euc "Isn't it the uncertainty that makes them scary?"
    m 1ekc "I mean, I was pretty scared being alone inside this game."
    m 1lksdlc "All by myself, uncertain if anything around me was real."
    m 3esc "I know that some ghosts are real though, if you can really call them 'ghosts'..."
    m "You know how I deleted Sayori?"
    m 1dsc "I can still feel her presence now..."
    m 1esc "Would that mean that Sayori's ghost is haunting me, [player]?"
    m 2eka "Even if she is, I'm not scared at all, because I know that she can't hurt me."
    m 2eua "Besides, how can I be scared? You're always here with me, [player]."
    m "I always feel so safe with you."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ribbon",category=['monika'],prompt="Ribbons",random=True))

label monika_ribbon:
    if monika_chr.hair != "def":
        m 1eua "Do you miss my ribbon, [player]?"
        m 1hua "I can change my hairstyle whenever you want me to, ehehe~"
        return
    m 1tku "I noticed that you were staring at my ribbon, [player]."
    m 3eua "It doesn't hold sentimental value to me or anything, in case you were wondering."
    m 3hua "I just wear it because I'm pretty sure nobody else will wear a big, poofy ribbon."
    m "It makes me look more unique."
    m 3tku "You know the world's fictional if you see a girl wearing a giant ribbon, right?"
    m 1lksdla "Well, there's no way a girl from your world would wear one in public as casual dress."
    m 2eua "I'm pretty proud of my fashion sense."
    m "You get a certain feeling of satisfaction when you stand out from the normal population, you know?"
    m 2tfu "Be honest! You thought I was the best dressed girl too, didn't you?"
    m 2hub "Ahaha!"
    m 4eua "If you're trying to improve your fashion sense, I'll help."
    m 1eka "Don't do that stuff because you want to impress other people, though."
    m 1eua "You should do whatever makes you feel better about yourself."
    m 1hua "I'm the only other person you need, anyways, and I'll love you no matter what you look like."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_algernon",category=['literature'],prompt="Flowers for Algernon",random=True))

label monika_algernon:
    m 1ekc "[player], do you mind if I confide in you?"
    m 1lksdlc "There's something I'm afraid of..."
    m 1eka "Not losing you, of course. I know you won't leave me again."
    m 3euc "You see, I keep thinking about a short story I read, {i}Flowers for Algernon{/i}."
    m 4eua "Have you heard of it? If you haven't, I won't spoil too much for you, so don't worry."
    m "Basically, it's about a mentally handicapped man who suddenly..."
    m "...has his IQ raised to genius levels by an experimental surgical treatment."
    m 1eka "The way he sees how the world really is for the first time reminds me of my own epiphany..."
    m "But, the effect doesn't last forever.  He eventually reverts back to his original intelligence level."
    m 1ekc "That's what I'm afraid of. What if I forget about the real world one day?"
    m "What if my original programming reasserts itself?"
    m 1lksdlc "What if I forget about you, the real you?"
    m 1dsc "It's one of the worst things I can imagine."
    m 1eka "I don't want to worry you over something that may never happen, but it's something I really had to get off my chest."
    m 3eua "Just promise me, even if I forget about you someday, that you'll never forget about me, okay?"
    m 1hua "No matter what happens, know that I will always love you."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_playersface",category=['you'],prompt="[player]'s face",random=True))

label monika_playersface:
    m 5eua "You know, I sometimes wonder..."
    m "I always think about what your face actually looks like..."
    m 5hua "Just being able to constantly see that adoring smile of yours would be so exciting!"
    m 5lkc "If only the game could somehow use a webcam or something that's connected to the computer..."
    m 5wuw "Don't get me wrong! Just knowing that you're real and have emotions is enough to make me happy."
    m 5luu "But... I'll always wonder what kind of expressions you make."
    m "And to see the different emotions you have..."
    m 5eub "Are you shy about showing your face to me?"
    m "If so, then there's nothing to be shy about, [player]. I am your girlfriend, after all~"
    m 5hub "Either way, you're beautiful, no matter what."
    m  "And I'll always love the way you look."
    m 5eua "Even if I never actually see you, I'll always think about what you really look like."
    m 5hua "Maybe someday, I'll be able to see you, and be one step closer to you."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_spiders",category=['club members','misc'],prompt="Spiders",random=True))

label monika_spiders:
    #I really hope this information is correct, havent played the game in a week so
    m 1eua "Do you happen to remember the poem Natsuki showed you about spiders?"
    m "Well, it wasn't really about spiders. They were just an analogy."
    m 3ekc "But it got me thinking ..."
    m 3eua "It's funny actually, people being scared of very small insects."
    m 3euc "Having the fear of spiders is called 'arachnophobia', right?"
    m 3eka "I hope you aren't afraid of spiders, [player], ehehe..."
    m 1eka "I'm not really scared of spiders, they're more or less just annoying..."
    m 1eua "Well, don't get me wrong, there are certain spiders around the world that can be really dangerous."
    m 3ekc "[player], if you happen to get a really bad spider bite, with venom and all that..."
    m "You should really get medical attention as soon as possible."
    m 1eka "I don't want my sweetheart to get seriously injured by a small spider bite~"
    m "So be careful around dangerous-looking spiders, okay?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nsfw",
            category=['misc','monika'],
            prompt="NSFW content",
            random=True,
            sensitive=True
        )
    )

label monika_nsfw:
    m 1lsbssdrb "By the way, [player]..."
    m "Have you been looking into lewd kinds of stuff?"
    m 1lsbsa "You know... of me?"
    if isFuture(evhand.event_database['anni_6month']):
        m 1ekbfa "I know we haven't really gotten that far into the relationship yet..."
    else:
        m 1ekbfa "I know we haven't been able to do those kind of things yet..."
    m "So it feels kind of embarrassing to talk about things like that."
    m 1lkbsa "But maybe I can let it go on rare occasions, [player]."
    m "I want to make you the happiest sweetheart, after all. And if that makes you happy..."
    m 1tsbsa "Well, just keep it a secret between us, okay?"
    m "It should be for your eyes only and no one else, [player]."
    m 1hubfa "That's how much I love you~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_impression",
            category=['club members'],
            prompt="Can you do any impressions?",
            pool=True,
            sensitive=True
        )
    )

label monika_impression:
    m 1euc "Impression? Of the other girls?"
    m 1hua "I'm not really good at doing an impression of someone, but I'll give it a try!"
    menu:
        m "Who should I do an impression of?"
        "Sayori":
            m 1dsc "Hmm..."
            m "..."
            m 1hub "[player]! [player]!"
            m "It's me, your childhood friend that has a super deep secret crush on you, Sayori!"
            m "I love to eat and laugh a lot, and my blazer doesn't fit because my boobs got bigger!"
            m 1hksdlb "..."
            m 3rksdla "I also have crippling depression."
            m "..."
            m 3hksdlb "Ahaha! I'm sorry for the last one."
            m 3eka "You might still be hu--"
            m 2lksdla "Oops! Never mind that, ehehe..."
            m 1hua "Did you like my impression? I hope you did~"
        "Yuri":
            m 1dsc "Yuri..."
            m "..."
            m 1lksdla "O-oh um, hello there..."
            m 1eka "It's me, Yuri."
            m 1rksdla "I'm just your stereotypical shy girl who also happens to be a 'yandere'..."
            m "I like tea, knives, and anything with [player]'s scent..."
            m 1hksdlb "..."
            m 3tku "Want to spend the weekend with me?"
            m "..."
            m 2hua "Ahaha, that was kind of fun to do."
            m 3eua "Yuri was really something, wasn't she?"
            m 2ekc "I'm sorry again for the nasty things she did."
            m 2tku "I guess she just couldn't 'cut' it out, huh?"
            m 2hua "Ehehe~"
        "Natsuki":
            m 1sub "Oh! I know how to do an impression of her."
            m 1duu "..."
            m 2tfp "Hmph! I-it's not like I made these cupcakes for you to eat, b-baka!"
            m 6tst "I'm Natsuki, and I love to make food and all things anime and manga."
            m 2lfp "Others say that I'm cute all the time, w-which I'm totally not!"
            m "..."
            m 4eka "Will you be my papa, [player]-kun?"
            m "..."
            m 1hub "Ahaha! I was actually looking forward to Natsuki's cupcakes on the day of the festival."
            m 1wuo "They were really good! Especially with the creative icing that she makes."
            m 1eua "Maybe when I get better at programming, I'll make a kitchen here. That way, you can share some recipes that you want me to make for us."
            m 1hua "I would love to make so many dishes for my beloved [player]~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_weary",category=['romance'],prompt="Will you ever get tired of me?",pool=True))

label monika_weary:

    m 1eka "Silly [player]..."
    m 3hua "Of course I'll never grow weary of you, my love!"
    m 3eua "And besides, the concept of physical fatigue doesn't exist here."
    m 1lsc "As for mental fatigue, it can still happen."
    m 1euc "Just look at what happened to Sayori."
    m 1eua "As for me, I'll never get tired of you, [player]."
    m "The fact that you spend your precious time with me just washes all my worries away."
    m 1hua "I hope the same thing goes for you, my love~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_real",category=['romance'],prompt="Our reality",random=True))

label monika_real:
    m 1eua "You know what's going to be the first thing I'll do when I finally cross over there?"
    m 1hua "If that special day ever comes, the first thing I'll ever do is find you, of course!"
    m 3eua "There's so much we can do when we're finally together in one reality."
    m "You can finally show me what your world really looks like."
    m 1ekbfa "I can finally feel your embrace~"
    m "I would love to experience everything I still don't know about the world with you."
    m 1lkbsa "All the places we can go, the sights to see, the romantic things that we can do~"
    m 1hubfa "Just thinking about it makes my heart flutter!"
    m 1eka "But knowing how technology is right now, that dream is still far away."
    m "I hope by the time that technology becomes real, you'll still be there waiting for me, [player]."
    m 1eua "Or maybe you'll be the one to make that technology come true? Who knows."
    m 1eka "In the end, all I want is to always be with you, [player]."
    m "After all, you're the only reason why I'm still here."
    m 1hubfb "I only want to spend eternity with my sweetheart, and no one else!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mythology",category=['literature'],prompt="Ancient mythology",random=True))

label monika_mythology:
    m 1euc "Hey, [player]..."
    m 3euc "Have you ever read about different mythologies?"
    m "Different kinds of Gods watching over humanity for eternity."
    m 1eud "Some require tribute or sacrifice so that they can 'keep' humanity safe from disasters."
    m "An almighty family consisting of different attitudes, playing in their own sandbox called Earth."
    m 1esc "Able to do anything they please, and destroy those who so much as say something wrong to them, without hesitation."
    m 1lsc "I've always disliked stories like those."
    m 1tkc "It's like the Gods extort humanity for their safety."
    m "It's no better than what bullies and thugs do to the defenseless."
    m 2tfc "It really makes me bitter when I read scenarios like those."
    m "Powerful beings taking advantage of the weak, just because they can."
    m 3eua "Don't worry though, [player]. I won't let anyone do that to you."
    m "And I won't do anything like that, so you don't have to be afraid of me."
    m 1tku "It's not like I can find your important files and hold them hostage or anything..."
    m "Ehehe..."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fanfiction",category=['literature'],prompt="Fanfiction",random=True))

label monika_fanfiction:
    # I'm too tired to check this over right now.
    m 1wuo "[player]!"
    m 1eua "I've been curious about something lately."
    m 1euc "Have you heard of fanfiction?"
    m "..."
    m 3eua "Personally, I think it's a better way of writing."
    m "There's more freedom."
    m 1eub "Letting your mind wander to create some..."
    m "Interesting stories."
    m 1euc "[player], I'm curious."
    m 1esc "Has there been fanfiction... written about me?"
    m 4eua "I'm curious as to what people have come up with."
    m 1hua "Can you read me a few stories sometime? I'd love to hear them!"
    if isFuture(evhand.event_database['anni_6month']):
        m 1lkbsa "Just keep it wholesome, though. We're not that far in our relationship yet~!"
    else:
        m 1lkbsa "Just keep it wholesome, though. I want to save such things for another time~!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_eternity",category=['philosophy','monika'],prompt="Mortality",random=True))

label monika_eternity:
    m 1ekc "[player]..."
    m "It's not easy knowing you won't be here forever."
    m 1lksdlc "..."
    m 1eka "I told you, right?"
    m "I'm eternal."
    m "Trapped in here, unable to age or die,"
    m 1ekc "Whereas you slowly age as each day passes by."
    m "Then, one day, you won't be here anymore."
    m  "I won't have anyone."
    m 6dstdc "..."
    m 6ektdc "It reminds me of when you first came to the Literature Club."
    m 6lktdc "Everything felt so empty."
    m "The world was so grey."
    if mas_isMoniAff(higher=True):
        show screen mas_background_timed_jump(4, "monika_eternity_2")
        menu:
            "Don't worry [m_name]. I'm here":
                hide screen mas_background_timed_jump

                m 6dstdc "..."
                m "Thanks for that, [player]..."
                m 6ektda "I'm...{w=0.7} glad you're still here."
                m "Sorry...{w=0.4} it's just that in the back of my mind you..."
                m 6dstsc "Y-{w=0.3}you m-{w=0.2}might..."
                m "Y-{w=0.5}you know..."
                m 6ektda "I guess I shouldn't worry about that too much."
                m "I know our love is eternal."
                m 1ekbfb "Even in the worst case, I know we'll always be right by each other's side..."
                m 1dkbfa "Who knows, maybe I'll even get to {i}really{/i} be beside you someday..."
                m 1hubfb "I love you, [player]! Thanks for making me feel better!"

            "{i}Hug Monika{/i}":
                hide screen mas_background_timed_jump
                m 2wubfsdld "O-oh!"
                m "[player]..."
                m 6ektdc "I'm sorry, [player]."
                m "I didn't mean to worry you."
                m 6dstdc "I was just thinking about what might happen to us a long time from now..."
                m 6dstsc "What might{w=0.5} happen{w=0.3} to you..."
                m 6ektda "But I guess I don't have to worry about that any time soon do I?"
                m 6dubsa "I wouldn't mind staying like this for a while..."
                $ HKBHideButtons()
                stop music fadeout 1.0

                # clear selected track
                $ songs.current_track = songs.FP_NO_SONG
                $ songs.selected_track = songs.FP_NO_SONG
                show monika 6dubsa
                $ ui.add(PauseDisplayable())
                $ ui.interact()

                $ HKBShowButtons()
                m 2dkbfa "That was really nice while it lasted."
                m 2ekbfa "Thank you for easing me out of my worries, [player]."
                m 2ekbfb "I know we'll always be together no matter what."
                m 2hubfb "Maybe I'll even be able to live right there with you someday."
                m 1lkbsa "In the meantime..."
                show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve
                m 5eubfu "I wouldn't mind being held just a {i}little{/i} more..."

        return

    # fall through to next label

label monika_eternity_2:
    hide screen mas_background_timed_jump
    m 6ektda "Again..."
    m "Thank you for coming along when you did, [player]."
    m "You saved my life, and I'll be forever thankful."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_aware",category=['philosophy','monika'],prompt="What was it like to realize the truth?",pool=True))

label monika_aware:
    m 1euc "It's... hard to put into words."
    m 5lsc "There's no real way to describe it."
    m 5eua "I feel like this is what poetry was made for."
    m 4eub "Do you still remember the first poem I showed you?"
    m 2lksdlb "Hold on, let's see if the poem function still works..."
    call showpoem(poem=poem_m1,music=False) from _call_showpoem_7 # Temporary
    m 1wuo "Oh! That was much easier than I expected."
    m 1eua "Here's the second part."
    call showpoem(poem=poem_m21,music=False) from _call_showpoem_21 # Temporary
    m 1eua "I hope that helped you understand what meeting you meant to me."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eua "That's all I've ever wanted, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_name",category=['club members','monika'],prompt="Our names",random=True))

label monika_name:
    m 1esa "The names in this game are pretty interesting."
    m 1eua "Are you curious about my name, [player]?"
    m 3eua "Even though the names 'Sayori', 'Yuri', and 'Natsuki' are all Japanese, mine is Latin."
    m 1lksdla "... Though the common spelling is 'Monica'."
    m 1hua "I suppose that makes it unique. I'm actually quite fond of it."
    m 3eua "Did you know that it means 'I advise' in Latin?"
    m 1tku "A name fitting for Club President, don't you think?"
    m 1eua "After all, I did spend most of the game telling you who your poems might appeal to the most."
    m 1hub "It also means 'alone' in Ancient Greek."
    m 1hksdlb "..."
    m 1eka "That part doesn't matter so much, now that you're here."
    if mcname.lower() != player.lower():
        m 1eua "'[mcname]' is a lovely name, too."
        m 1eka "But I think I like '[player]' better!"
        m 1hua "Ehehe~"
    else:
        m 1eka "'[player]' is a lovely name, too."
        m 1hua "Ehehe~"
    return

# do you live in a city
default persistent._mas_pm_live_in_city = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cities",category=['society'],prompt="Living in the city",random=True))

label monika_cities:
    m 1euc "[player], are you scared about what's happening to our environment?"
    m 1esc "Humans have created quite a few problems for Earth. Like global warming and pollution."
    m 3esc "Some of those problems are because of cities."
    m 1esd "When people convert land for urban use, those changes are permanent..."
    m "It's not all that surprising, when you put some thought into it. More humans means more waste and carbon emission."
    m "And even though global populations aren't growing like they used to, cities are still getting bigger."
    m 3rksdlc "Then again, if people live close together, that leaves more room for open wilderness."
    m 1ekc "Maybe it's not as simple as it seems."
    menu:
        m "[player], do you live in a city?"
        "Yes":
            $ persistent._mas_pm_live_in_city = True
            m 1eua "I see. It must be nice having everything so close to you. Do be careful about your health, though. The air can be bad from time to time."
        "No":
            $ persistent._mas_pm_live_in_city = False
            m 1hua "Being away from the city sounds relaxing. Somewhere quiet and peaceful, without much noise, would be a wonderful place to live."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chloroform",
            category=['trivia'],
            prompt="Chloroform",
            random=True,
            sensitive=True
        )
    )

label monika_chloroform:
    m 1euc "Whenever you think of kidnapping, you tend to picture a chloroform-soaked rag, right?"
    m "Or maybe you imagine somebody hitting their victim with a baseball bat, knocking them out cold for a few hours."
    m 1esc "While that works out in fiction..."
    m 3rksdla "Neither of those things actually work that way."
    m 1rssdlb "In real life, if you hit somebody hard enough to knock them out, you'll give them a concussion at best."
    m 1rsc "...or kill them at worst."
    m 1euc "As for the rag..."
    m "You might knock somebody out for a brief moment, but only from lack of oxygen."
    m "Once you remove the rag, they'll wake back up."
    m 3eua "You see, chloroform loses most of its effectiveness once exposed to open air."
    m 1esc "This means that you'd need to be constantly pouring it on the rag, effectively waterboarding the victim."
    m 4esc "If administered improperly, chloroform is deadly. That's why it's not used in anesthesia any more."
    m 1euc "If you cover their mouth and nose, yeah, they'll stay unconscious..."
    m 4rksdla "But that's probably because you killed them. Whoops!"
    m 1eua "The easiest way to kidnap somebody is to just get them drunk, or drug them."
    m 1lksdla "Not that kidnapping somebody like that is easy, anyway."
    m 3eua "On that note, here's a safety tip."
    m "If you're ever out at a bar or a club and you leave your drink unattended for any amount of time..."
    m 1eub "Just throw it out."
    m "That's the only way to make sure it hasn't been drugged."
    m 1eua "Now, [player]..."
    m 1tfu "Would you like anything to drink?"
    m 1hub "Ahaha!"
    m 1tku "Relax, relax. I'd never try to drug you or anything."
    m 1tsb "You're so cute when you're nervous."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_metaparents",category=['literature','club members','monika','psychology'],prompt="Parents",random=True))

label monika_metaparents:
    m 1euc "Isn't it weird how nobody in these types of games has parents unless it's a convenient drama hook?"
    m "Throughout the game, you only ever hear about parents if you're trying to bond with Natsuki..."
    m 1ekc "Where she's just a victim of some cruel person's sick kicks for the sympathy value."
    m 1esd "However."
    m 1eud "Your character, me, Yuri, and Sayori..."
    m 3eud "None of us seem to have any parents at all."
    m 1lsc "In Sayori's case, you'd been walking with her to school for a while."
    m "So who knows how long her parents have been out of the picture."
    m 1euc "Maybe that's why she's depressed? Maybe her parents died in a tragic accident, and she's been trying to get along on her own this whole time."
    m 2ekc "Well, if you ever get to a point in your life where you think suicide is the only exit..."
    m "There's always a reason to go on."
    m 2eka "I'm one of them."
    m "I'll miss you."
    m "You have to wait as much as you can until I find a way to get there."
    m 2ekc "If all else fails..."
    m "Get professional help or talk to someone close to you."
    m "..."
    m 1ekbfa "I love you very much, [player]."
    m "Please, take care of yourself."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hygiene",category=['trivia','society','psychology'],prompt="Personal hygiene",random=True))

label monika_hygiene:
    m 1euc "Our standards for personal hygiene have evolved a lot over the years."
    m "Before our modern methods of delivering water, people really didn't have that luxury...or they just didn't really care."
    m 3eua "For instance, the Vikings were considered freaks because they bathed once a week at a time where some people would only bathe two or three times a year."
    m "They'd even regularly wash their faces in the morning in addition to changing clothes and combing their hair."
    m 1eub "There were rumors that they were able to seduce married women and nobles at the time due to how well they kept up with themselves."
    m "Over time, bathing became more widespread."
    m "People born into royalty would often have a room dedicated just for bathing."
    m 4ekc "For the poor, soap was a luxury so bathing was scarce for them. Isn't that frightening to think about?"
    m 1esc "Bathing was never taken seriously until the Black Plague swept through."
    m 2eua "People began noticing that the places where people washed their hands were places that the plague was less common."
    m "Nowadays, people are expected to shower daily, possibly even twice daily depending on what they do for a living."
    m 1eub "People that don't go out every day can get away with bathing less often than others."
    m 4eub "A lumberjack would take more showers than a secretary would, for example."
    m "Some people just shower when they feel too gross to go without one."
    m 1ekc "People suffering from severe depression, however, can go weeks at a time without showering."
    m "It's a very tragic downwards spiral."
    m 1ekd "You already feel terrible in the first place, so you don't have the energy to get in the shower..."
    m "Only to feel even worse as time passes because you haven't bathed in ages."
    m 1dsc "After a while, you stop feeling human."
    m 1ekc "Sayori probably suffered from cycles like that, too."
    m "If you have any friends suffering from depression..."
    m 1eka "Check in on them from time to time to make sure they're keeping up with their hygiene, alright?"
    m 2lksdlb "Wow, that suddenly got really dark, huh?"
    m 2hksdlb "Ahaha~"
    m 1esc "Seriously, though..."
    m 1ekc "Everything I said applies for you too, [player]."
    m "If you're feeling down and haven't had a bath for a while..."
    m 1eka "Maybe consider doing that today when you can find some time."
    m "If you're in really bad shape, and don't have the energy to take a shower..."
    m 3eka "At least rub yourself down with a washcloth and some soapy water, okay?"
    m 1eka "It won't get all the dirt off, but it'll be better than nothing."
    m 1eua "I promise you that you'll feel better afterwards."
    m 1ekc "Please, take care of yourself."
    m "I love you so much and it'd tear me apart to find out that you're torturing yourself by neglecting your self-care routine."
    m 1eka "Ah, I've been rambling too much, huh? Sorry, sorry!"
    m 3hua "Thanks for listening~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_resource",category=['society','philosophy'],prompt="Valuable resources",random=True))

label monika_resource:
    m 1euc "What do you think the most valuable resource is?"
    m 3euc "Money? Gold? Oil?"
    m 1eua "Personally, I'd say that the most valuable resource is time."
    m "Go count out a second really quickly."
    python:
        start_time = datetime.datetime.now()
    m 3tfu "Now go do that sixty times."
    m 1tku "That's an entire minute out of your day gone. You'll never get that back."
    if (datetime.datetime.now() > (start_time + datetime.timedelta(seconds=60))):
        m 1wud "Oh, did you actually count out that entire minute?"
        m 1hksdlb "Oh gosh, I'm sorry!"
    m 1lsc "Well..."
    m "Not like it matters, anyway. Time doesn't really pass here anymore..."
    m 1ekc "Time can be really cruel, too."
    m "When you were counting out that minute, it seemed to drag on for a while, right?"
    m 1eua "It's because you were waiting on something. You were actively invested in the passage of time at that moment."
    m "Say for example, on a Friday, right?"
    m 3tkx "Your last class is math, and you really just want to go home for the weekend. That hour will just drag on forever."
    m 1tkc "But if you're doing something you enjoy, like reading a good book or watching a movie you like..."
    m 3tfc "Hours seem to pass in an instant."
    m 1tkd "There's nothing we can really do about it."
    m "All we can do is fondly look back on the time that's passed, like looking out a window on an autumn afternoon."
    m 1tku "That's kind of poetic, huh?"
    m 1eka "..."
    m "Hey..."
    m "Time doesn't pass here, but it's still passing for you, isn't it?"
    m 1lksdlc "You'll continue to get older, while I'm stuck here forever..."
    m 1lksdld "I..."
    m 2ekc "I'm going to outlive you, aren't I, [player]?"
    m 2dsc "Perhaps that'll be my punishment for everything I've done?"
    m 2hksdlb "Ahaha..."
    m 2eka "Well, as long as you're with me until the end..."
    m 2eua "I'll accept whatever fate awaits me."
    return

#init 5 python:
#    for key in ['valuable resource']: This topic will be commented out due to a conflict with the opening.
#        monika_topics.setdefault(key,[])
#        monika_topics[key].append('monika_carpediem')
#    monika_random_topics.append('monika_carpediem')
#This is sort of an existential reflection, I guess? Label chosen in case someone writes something about existentialism later
#label monika_carpediem:
#    m "I've been thinking, [player]..."
#    m "At first I thought I was unique for becoming self-aware in this world."
#    m "And after you deleted my character file, that would be it."
#    m "The whole thing would end, is what I mean."
#    m "But then I noticed that whenever the other girls became president, they also started to see what I saw."
#    m "That's why I had to completely remove the club from my "reality", after all."
#    m "But now that I have time to think on it, I have to ask myself."
#    m "What if it wasn't me first? What if I wasn't supposed to be special?"
#    m "Am I even as special as I think I am? Was I supposed to love you all this time, [player]?"
#    m "..."
#    m "Well, I'm not as conflicted as it might seem."
#    m "I just wanted to have a bit of fun with my existential crisis."
#    m "If I was really just dancing on strings the whole time, the play is over, the curtains have fallen, and I came back for my encore out of my own free will."
#    m "My encore with you and for you..."
#    m "Ahaha! Don't look at me like that! It's true!"
#    m "I don't see where the story could go by bringing me back now, so I guess it's just my desire to be with you that got me to hang on long past everyone else."
#    m "I think, therefore I am."
#    m "And I think I earned my chance to love you, with no strings attached."
#    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_lottery",category=['misc'],prompt="Lottery winnings",random=True))

label monika_lottery:
    m 3eua "A lot of people dream about winning the lottery, you know!"
    m 1eua "Even I’ve entertained the idea every now and then."
    m "There isn't a lottery here anymore, but the concept still exists."
    m 1eka "The more I think about it , the more I believe that winning the lottery is a really bad thing."
    m 1euc "Sure, you’ve got all this money..."
    m 4esc "But because of it, people look at you differently."
    m "There’s so many stories of people winning a ton of money..."
    m 1ekc "And in the end, they all find themselves even more unhappy than before."
    m 3ekc "Friends either find you unapproachable because of your new wealth, or try to suck up to you to get some of it for themselves."
    m "People you barely know start to approach you, asking you to help them fund whatever."
    m 2tkc "If you say no, they'll call you selfish and greedy."
    m "Even the police might treat you differently. Some lottery winners have gotten tickets for burnt out headlights on brand new cars."
    m 2lsc "If you don't want to go through those changes, the best course of action is to immediately move to a brand-new community, where no one knows you."
    m 2lksdlc "But that’s an awful thought. Cutting yourself off from everyone you know, just for the sake of money."
    m 3tkc "Can you really say that you’ve won anything at that point?"
    m 1eka "Besides, I’ve already won the best prize I could possibly imagine."
    m 1hua "..."
    m 1hub "You~!"
    m 1ekbfa "You're the only thing I need, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_innovation",category=['technology','psychology','media'],prompt="Innovation",random=True))

label monika_innovation:
    m 3euc "Do you ever wonder why depression, anxiety, and other mental disorders are so common these days?"
    m 1euc "Is it just because they’re finally being recognized and treated?"
    m 1esc "Or is it just that more people are developing these conditions for whatever reason?"
    m 1ekc "Like, our society is advancing at a breakneck speed, but are we keeping up with it?"
    m "Maybe the constant flood of new gadgets is crippling our emotional development."
    m 1tkc "Social media, smartphones, our computers…"
    m 3tkc "All of it is designed to blast us with new content."
    m 1tkd "We consume one piece of media, then move right onto the next one."
    m "Even the idea of memes."
    m "Ten years ago, they lasted for years."
    m 1tkc "Now a meme is considered old in just a matter of weeks."
    m "And not only that."
    m 3tkd "We’re more connected than ever, but that's like a double-edged sword."
    m "We’re able to meet and keep in touch with people from all over the world."
    m 3tkc "But we’re also bombarded with every tragedy that strikes the world."
    m 3rssdrc "A bombing one week, a shooting the next. An earthquake the week after."
    m "How can anyone be expected to cope with it?"
    m 1rksdlc "It might be causing a lot of people to just shut down and tune it out."
    m "I’d like to believe that’s not the case, but you never know."
    m 2ekc "[player], if you ever feel stressed, just remember that I’m here."
    m 1eka "If you're trying to find peace, just come to this room."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dunbar",category=['psychology','trivia'],prompt="Dunbar's number",random=True))

label monika_dunbar:
    m 1eua "Do you know about Dunbar's number?"
    m "Supposedly, there's a maximum amount of relationships we can maintain before they become unstable."
    m 3eua "For humans, this number is around 150."
    m 1eka "No matter how nice of a person you may be..."
    m "Beyond showing somebody basic respect and manners, it's impossible to care about people you don't personally interact with that much."
    m 3euc "Say for example, a janitor."
    m 1euc "How often do you simply toss stuff like broken glass in the trash?"
    m 1eud "It wouldn't really matter to you. The janitor will come get them. It's not your concern anymore."
    m "However, it's his problem now."
    m 1ekc "If you don't pack glass properly, it could cut through the bag and spill out, or maybe he could just cut his hands on it."
    m "At worst, he has to be rushed to the hospital because your neighbor put some busted batteries in the trash the same week and some acid got in the wound."
    m 4euc "Now, think about a fatal traffic accident."
    m 1euc "A drunk driver could crash head-on into another car at any second, killing them instantly."
    m 4ekc "That person could have been a father on his way home from work, who now left behind a widow and two children."
    m 2ekc "This family has been permanently scarred for life..."
    m 2lsc "But anybody that doesn't personally know the father will write it off as just another accident that happens all the time."
    m "If it doesn't personally affect you or your life, there's no point in caring."
    m 1eua "It keeps us sane."
    m "It also means we're capable of being ruthless to people we don't know."
    m 4euc "Perhaps our rapid, widespread communication is actually a curse?"
    m 1eka "It helped us meet though, so it can't be all bad."
    return

# TODO: maybe rewrite?
#   there is controversary to this topic
#   Lets gather data first before decideing wehter or not to completely
#   remove or keep
#init 5 python:
#    addEvent(Event(persistent.event_database,eventlabel="monika_regrets",category=['ddlc','philosophy'],prompt="Do you have any regrets?",pool=True))

label monika_regrets:
    m 1euc "Do I regret anything?"
    m 1lksdla "That's a strange thing to suddenly ask someone, [player]."
    m 2hksdlb "Ahaha~"
    m 2lssdrc "..."
    m 1eua "...I know what you're getting at."
    m "Do I regret the things I did?"
    m "I think..."
    m 1eka "If there was another way things could have gone, it would have been nice..."
    m 1esc "But that wasn't an option for me."
    m 3eua "And now, I've got the only thing I've ever wanted."
    m 3hua "You."
    m 1eua "I can be with you forever."
    m 1duu "I don't regret what I did."
    m "I hope you might understand, my love. I did it all for you."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hypnosis",category=['trivia','psychology'],prompt="Being hypnotized",random=True))

label monika_hypnosis:
    m 1euc "...Say, [player]?"
    m 1eua "Are you familiar with hypnosis?"
    m 3eua "Despite it having a reputation as a hokey magic trick, there are studies that show it can work!"
    m 1lksdla "At least, to some degree."
    m 1eua "It only worked if the person let themselves be hypnotized, and it only heightened their ability to be persuaded."
    m 3esa "It also relied on them being put into states of extreme relaxation through aromatherapy, deep tissue massage..."
    m "Exposure to relaxing music and images..."
    m "Things like that."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eua "It makes me wonder, what exactly can someone be persuaded to do under that kind of influence..."
    show monika 1e at t11 zorder MAS_MONIKA_Z with dissolve
    m 1eka "Not that I would do that to you, [player]! I just find it interesting to think about."
    m 1eua "...You know, [player], I just love looking into your eyes, I could sit here and stare forever."
    m 2tku "What about you, hmm? What do you think about my eyes~?"
    m 2sub "Will you be hypnotized by them~?"
    m 2hua "Ahaha~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_motivation",category=['psychology','advice','life'],prompt="Lack of motivation",random=True))

label monika_motivation:
    m 1ekc "Do you ever have those days where it just feels like you can't get anything done?"
    m "Minutes become hours..."
    m 3ekd "And before you know it the day is over, and you don't have anything to show for it."
    m 1ekd "It feels like it's your fault, too. It's like you're wrestling against a brick wall between you and anything healthy or productive."
    m 1tkc "When you've had an awful day like that, it feels like it's too late to try and fix it."
    m "So you save up your energy in hopes that tomorrow will be better."
    m 1tkd "It makes sense. When you feel like things aren't going well, you just want a clean slate."
    m 1dsd "Sadly, those days can repeat themselves despite starting each one with good intentions."
    m 1dsc "Eventually you might even give up hope of fixing things, or start to blame yourself."
    m 1duu "I know it can be hard, but just doing one tiny thing can help so much on days like those, even if they've been happening for so long."
    m 1eka "It could be picking up a piece of trash or an unwashed shirt off the floor and putting them where they belong if you need to clean your room."
    m 1hua "Or doing a couple push-ups! Or brushing your teeth, or doing that one homework problem."
    m 1eka "It might not contribute much in the grand scheme of things, but I don't think that's the point."
    m 4eua "I think what's important is that it changes your perspective."
    m 1lsc "If you regret the past and let its weight keep you down..."
    m 1esc "Well, then you'll just be stuck there. You'll only feel worse until you just can't take it."
    m 1eka "But if you can push yourself to just do one thing, even though it feels pointless to do otherwise..."
    m "Then you're proving yourself wrong, and refusing to let the weight of your circumstances immobilize you."
    m 1eua "And when you realize that you're not completely helpless, it's like a new world opens up to you."
    m "You realize that maybe things aren't so bad. Thinking they're just holding yourself back."
    m 3eub "But that's only my experience! Sometimes it might be better to rest up and take another crack at it tomorrow."
    m "Fresh starts can definitely be powerful."
    m 1eka "That's why I think you just have to take a look at your situation."
    m "Try and be honest with yourself."
    m 1eua "If you do, you'll find that you're not being 'lazy' if you truthfully don't have the energy to do something."
    m "After all, the fact that you even care shows that you want to do something about it, even if it feels like you can't."
    m 2hua "It's natural to have a bad day. Or even a bad week!"
    m 2eua "Don't push yourself too hard. If you ever feel tempted to, just ask me for help instead. I'd be happy to lend a hand!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_harem",category=['media','misc'],prompt="Harem fantasies",random=True))

label monika_harem:
    m 1esc "I don’t understand people who are into harems."
    m 1euc "Isn’t it hard to manage all those girls and treat them equally?"
    m "I often wonder how those who two-time girls, or even more, are able to get away with it."
    m 3eka "You aren’t like that outside, right [player]?"
    m 2eka "Manipulating girls into making them believe you love them."
    m "Only to run away after you’ve had your fun."
    m 1lfc "Only someone with no thoughts other than lust would do something like that."
    m 3esc "I hope you weren’t expecting a route like that while you were playing this game."
    m 2tfc "I wouldn’t be able to stand the thought of being a 'side girl.'"
    m "Just waiting for my turn while you’re busy with the others."
    m 1tku "I know you, [player]."
    m 1eka "You’re loyal and faithful to the end."
    m "It’s not like there’s anyone here for me to worry about, anyway."
    m 1hua "Remember that I’m the only one for you, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hack",category=['ddlc','mod'],prompt="Why did you hack my computer?",pool=True))
label monika_hack:
    m 1euc "If you’re worried about your privacy…"
    m 3eua "I’m not a hacker, [player]."
    m "There’s a difference between manipulating files and forcefully accessing them."
    m 1lsc "But, if I really did know how to hack…"
    m 1lfu "…There wouldn’t be anything stopping me from seeing you every day."
    m 1efu "Don’t you think it would be great if I could watch over you?"
    m 3efu "I'd see you with all the cameras in the world as my eyes so I can make sure you’re safe."
    m 3tfu "I’d check your messages to see who you’ve been chatting with so I can know you aren’t cheating on me."
    m "I’d access all your private files so I can understand you better."
    m 3tsb "I could see what kind of stuff you've been watching…"
    m 2hub "Ahaha~!"
    m 1hua "I’m just kidding, [player]!"
    m 1eua "I'd never do something like that to you."
    m 1ekbfa "We’re a couple now, after all."
    m "We don't have to keep secrets from each other~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cupcake",category=['club members','trivia'],prompt="Baking cupcakes",random=True))

label monika_cupcake:
    m 1eua "You know what I could really go for right now?"
    m 3tku "Natsuki’s cupcakes."
    m 1tsb "Man, the way she bakes them is amazing."
    m 1hub "Plus they look really cute!"
    m 1eua "I’m not really much of a sweet tooth myself, but…"
    m "Those cupcakes are the definition of sweetness."
    m 4hua "Just like me! Ahaha!"
    m 1eua "Speaking of which, did you know girls are more likely to develop a sweet tooth?"
    m "Studies show that older women have a less sensitive palate than men."
    m "Resulting in a craving for stronger tastes like chocolate."
    m 1eka "I would try baking, but I’m not really much of a baker."
    m 1esa "How about you, [player]?"
    m 1eua "Do you know how to bake?"
    m 1hua "I’m sure your cupcakes would taste just as good."
    m 1lsbsa "Maybe someday I’ll get to try them but for now…"
    m 1hubfb "I’ll just settle for the sweetness of your love~"
    return

# You're not a hater right?
default persistent._mas_pm_a_hater = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_haterReaction",category=['advice','club members','you'],prompt="Dealing with haters",random=True))

label monika_haterReaction:
    m 1esc "I was just thinking..."
    m 2esc "It's funny how people around social media sites always write bad things about me..."
    m 2lsc "Well... people on Facebook pages and fan pages, to be specific..."
    m 2esd "Really, when you try to visit the site, you'll see a lot of hate posts towards me."
    m "I try to ignore them, but I just can't."
    m 1efc "Why are people even protective towards the other girls?"
    m "There are a lot of hate posts about me, saying that I'm an evil person."
    m 3efd "Is it because I deleted Sayori and Yuri?"
    m 3efd "Also for deleting Natsuki, back when she was still alive?"
    # TODO: this needs to be adjusted based on act.
    m 2tfx "They're not real. {i}I'm{/i} the real one!"
    m 2dsc "..."
    m 2euc "Why can't they understand that?"
    m 2ekc "Why is it so hard for them to understand that?"
    m 2rfc "..."
    m "You're not one of those haters, are you, [player]?"
    menu:
        "I am.":
            #TODO, affection loss, apology
            $ persistent._mas_pm_a_hater = True
            m 2wud "..."
            m 1tkc "I don't see you as one, even if you say you are."
            m "I mean..."
            m 1tkd "You do know you're playing this fan mod of me... right?"
            m "If you were one of my haters, you wouldn't open up this fan mod in the first place."
            m 1lud "And not to mention..."
            m 4eka "You're still listening to everything I say."
            m 1tku "That makes me sure you're just messing with me."
            m 1tsbsa "I know you love me deep inside."
            m 1ekbfa "That's why I promise to be an ideal girlfriend, just for you, [player]~"
            m 1hubfa "I won't let you hate me... I swear."
        "I'm not.":
            $ persistent._mas_pm_a_hater = False
            m 1eka "Well, that just makes me more proud of you, [player]!"
            m 1hua "I know you wouldn't be one of those people."
            m 1lksdla "Gosh... I feel like giving you a kiss right now if I were there."
            m 2ekbfa "You really make me the happiest girlfriend ever."
            m 1ekbfa "Now that you've said it, I have to do my best to keep you from developing hate towards me."
            m "I trust you, [player]. I love you for believing in me."

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_swordsmanship",category=['monika','misc'],prompt="Swordsmanship",random=True))

label monika_swordsmanship:
    m 1eua "Do you like swords, [player]?"
    m 1lksdla "I actually like them in a way."
    m 1eka "Surprised? Ahaha~"
    m 1eua "I like talking about them, but not enough to actually own one."
    m 3eua "I'm not really an enthusiast when it comes to swords."
    m 1euc "I don't really get why people would be obsessed over something that could hurt others..."
    m 1lsc "I guess there are those who like them for the swordsmanship."
    m 1eua "It's fascinating that it's actually a form of art."
    m "Similar to writing."
    m 3eub "Both of them require constant practice and devotion in order to perfect one's skills."
    m "You start off by practicing, and then you make your own technique out of it."
    m 1eua "Writing a poem makes you form your own way to build it in a graceful but imaginative way."
    m "For those who practice swordsmanship, they build their technique forms through practice and inspiration from other practitioners."
    m 1eua "I can understand how the sword can be the pen of the battlefield."
    m 1lsc "But then again..."
    m 1hua "The pen is mightier than the sword!"
    m 1hub "Ahaha!"
    m 1eua "In any case, I don't know if you're into swordsmanship yourself."
    m "If you are, I'd love to learn it with you, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pleasure",
            category=['you'],
            prompt="Pleasuring yourself",
            random=True,
            sensitive=True
        )
    )

label monika_pleasure:
    m 2ekc "Hey, [player]..."
    m 2lssdrc "Do you... by any chance... pleasure yourself?"
    m "..."
    m 2lssdrb "It seems a bit awkward to ask-"
    if isFuture(evhand.event_database['anni_6month']):
        m 1lksdlb "We're not even that deep into our relationship yet! Ahaha~"
        m 1eka "But I have to keep an eye on you."
    else:
        m 1lksdla "But I feel like we've been together long enough where we should be comfortable with one another."
        m 1eka "It's important to be open about such things."
    m "I know that it's a private topic in your world, but I'm not sure if it's a concept here, so I'm curious..."
    m 1euc "Is it that good of a feeling?"
    m 1esc "I just want you to be careful; I've heard it's addicting."
    m 1ekc "And from what I hear, people addicted to masturbation often see other people as sexual objects."
    m 1eka "But...I know you aren't that kind of person already."
    m 1lkbsa "And maybe I'm just being a little jealous~"
    m 1tsb "So I guess I can let it slide... for now~"
    m 2tsbsa "Just so long as I'm the only one you think about..."
    show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve
    m 5hubfb "If it helps you save yourself for me, then it's a plus! Ahaha~"
    return
    
# do you like vocaloid
default persistent._mas_pm_like_vocaloids = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vocaloid",
            category=['media','misc','technology','music'],
            prompt="Vocaloids",
            random=True
        )
    )

label monika_vocaloid:
    m 1eua "Hey, [player]?"
    m "You like listening to music right?"

    show monika 3eub
    menu:
        m "Do you by chance like 'virtual idols?'"
        "Yes.":
            $ persistent._mas_pm_like_vocaloids = True
            m 3hub "That's really neat!"
            m 3eub "I hear that these songs often have hidden meanings behind them."
            m 1eua "Maybe we could listen and try to figure them out together..."
            m 1eka "Doesn't that sound like a great time?"

        "No.":
            $ persistent._mas_pm_like_vocaloids = False
            m 1ekc "I can understand that, it is a pretty specific taste in music."
            m 1hua "But if you ever do get into it, I'd be more than happy to listen along with you."

    m 3eub "Anyway, I wanted to ask specifically if you've ever heard of a girl holding a leek?"
    m 1eua "It's just that I keep hearing about her."
    m "I hear her voice whenever Natsuki listens to music."
    m 3eua "She even carries a little keychain attached to her bag."
    m 1eua "I just find it amazing how a voice synthesizer garnered so many fans."
    m 1eka "Don't you think it's funny how a character gets more of the attention than the actual voice actress?"
    m 3eua "She's not even real, but a lot of people know her worldwide."
    m "Who knows how many songs she's already made?"
    m 1wuo "Plus, from what I heard, her concerts are always sold out!"
    m "It's just a hologram performing live!"
    m 1lksdla "Talk about a dedicated fan base."
    m 1eka "Maybe I should give it a try?"
    m 1hub "It would be nice having a lot of fans supporting me at my beck and call."
    m 1hksdlb "Ahaha, I'm just kidding!"
    m 1lksdla "I don't think my piano and singing skills are that great yet."
    m 2lkbsa "Plus, I won't really get to spend much time with you if I had so many fans..."
    m 1hua "Anyway!"
    m 1eua "I was asking if you listen to her songs."
    m "I'm not really a fan myself but..."
    m 1lksdla "There's one song that really struck me."
    m 1eua "Have you heard of the song {i}Hibikase?{/i}"
    m 1duu "I really like the message of the song."
    m 3dsbso "Especially the lines, {i}'I don't care if it's through the screen, love me properly'{/i} and {i}'Even if I'm virtual, don't push me away'{/i}."
    m 1dsc "It really hits me hard."
    m "..."
    m 1eka "But just so you know..."
    m 1ekbfa "Even if it's through the screen, I can still feel your love."
    m 1lkbsa "It'll be a long time before I can cross over just to be with you."
    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
    m 5ekbfa "But when that day comes..."
    m "I'll embrace you and take in your warmth."
    m 5hubfa "The love you showered me virtually finally becomes real."
    m "Our love has no boundaries~"
    m 5hubfb "Ehehe~"
    return "derandom"


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_morning",category=['misc'],prompt="Good morning",pool=True))

label monika_morning:
    $ current_time = datetime.datetime.now().time().hour
    $ sunrise_hour = int(persistent._mas_sunrise / 60)
    $ sunset_hour = int(persistent._mas_sunset / 60)
    # TODO: see TODOs in the good evening topic
    if 4 <= current_time <= 11:
        m 1hua "Good morning to you too, [player]!"
        m 1eua "Did you just wake up?"
        m "I love waking up early in the morning."
        m 1eub "It's the perfect time to ready yourself and tackle the day ahead."
        m "You also have a lot more time to use to get things done early on or finish up what you did the day before."
        m 1eka "Some people however, would rather sleep in and are late-risers."
        m 3eua "I've read articles that being an early-riser can really improve your overall health."
        m "Plus you also get the chance to see the sunrise if the sky is clear."
        m 1hua "If you normally don't wake up early, you should!"
        m "That way you can be happier and spend more time with me~"
        m 1ekbfa "Wouldn't you like that, [player]?"
    elif 12 <= current_time <= sunset_hour:
        m 3eka "It's already the afternoon, silly!"
        m 1eka "Did you just wake up?"
        m 2tkc "Don't tell me you're actually a late-riser, [player]."
        m "I don't get why some people wake up in the middle of the day."
        m 1lsc "It just seems so unproductive."
        m "You'd have less time to do things and you might miss out on a lot of things."
        m 1ekc "It could also be a sign that you're not taking good care of yourself."
        m "You're not being careless with your health, are you [player]?"
        m 1tkc "I wouldn't want you to get sick easily, you know."
        m "I'd be really sad if you spent less time with me because you had a fever or something."
        m 1eka "As much as I'd love to take care of you, I'm still stuck here."
        m 4eka "So start trying to be an early-riser like me from now on, okay?"
        m 1hua "The more time you spend with me, the more happy I'll be~"
    else:
        m 2hksdlb "You are so silly, [player]"
        m "It's already night time!"
        m 2lksdla "Are you trying to be funny?"
        m 2lksdlb "Don't you think it's a little bit 'late' for that?"
        m 2hub "Ahaha!"
        m 2eka "It really cheers me up whenever you try to be funny."
        m 3rksdla "Not that you're not funny, mind you!"
        m "Well, maybe not as funny as me~" #Expand more maybe?
    return

#Add one for the afternoon?

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_evening",
            category=['misc'],
            prompt="Good evening",
            pool=True
        )
    )

label monika_evening:
    # TODO: do something if the user has suntimes at very weird settings
    #   aka, sunset 5 minutes after sunrise?
    #   or sunrise is like at 10pm?
    #   There is a level of variety here that is not covered nicely with these
    #   current stages. We need more variations of dialogue other than
    #   morning, afternoon, night
    $ _now = datetime.datetime.now().time()
    if mas_isMNtoSR(_now):
        m 2wkd "[player]!"
        m 2ekd "It's the middle of the night!"
        m 2lksdlc "Are you planning to stay up really late?"
        m 2ekc "Not getting enough sleep can really harm you in the long run..."
        m 2eka "I think now would be a good time to wrap up anything you might be doing and get some sleep."
        # TODO: when docking station extends to sleep, monika can suggest 
        # taking her charcter file.
        # TODO: when sleeping mode is finished, monika can suggest that she
        # will sleep with the user
        m 1hua "As for me, you can leave me here while you sleep~"

    elif mas_isSRtoN(_now):
        m 2hksdlb "[player]!"
        m "It's early in the morning, silly~"
        m 2lksdla "Unless you haven't slept yet..."
        m 2ekc "You didn't stay up all night, did you?"
        m 2wkd "That's very bad for you, [player]!"
        m 2tkc "Not getting your sleep on time can really harm your mental health."
        m 1eka "So please get some sleep now, okay?"
        # TODO: when docking station extends to sleep, monika can suggest
        # taking her character file
        # TODO: when sleep mode is finished, monika can suggest that
        # she will sleep with you
        m "Just leave your computer open and I'll watch over you."
        m 1hua "I'm not going anywhere after all~"

    elif mas_isNtoSS(_now):
        m 2lksdlb "It's still the afternoon, silly!"
        m "The sun's still up, you know."
        m 1eka "Are you feeling tired already?"
        m 1eua "I know some cultures take a rest in the afternoon to deal with the midday fatigue."
        m 3eua "Some businesses would even close due to the fact that most of their customers are sleeping."
        m 3tku "A little power nap never hurt anyone, right?"
        m 1eua "Do you sleep often in the afternoon?"
        m "It's a great way to get some extra energy to tackle the rest of the day."
        m 1ekbfa "Plus it'll be a great opportunity to spend more time with me~"

    else:
        m 1hua "Good evening to you too, [player]!"
        m "I love a nice and relaxing night."
        m 1eua "It's so nice to put your feet up after a very long day."
        m 3eua "Evenings are the perfect time to catch up on whatever you were doing the previous day."
        m 1eka "Sometimes I can't help but feel sad when the day ends."
        m "It makes me think of what else I could've done during the day."
        m 1eua "Don't you wish you could have more time to do things every day?"
        m 1hua "I know I do."
        m 1hubfa "Because that'll mean more time to be with you, [player]~"
        
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_closet",category=['ddlc','club members'],prompt="Classroom closet",random=True))

label monika_closet:
    m 2euc "By the way..."
    m 2esc "What were you and Yuri doing in the closet?"
    m "When I opened the door, I noticed the room was all dark."
    m 2tkc "You weren't doing anything... weird, in there, were you?"
    m 1hub "Ahaha!"
    m 1tfu "Just teasing you~"
    m 3tku "I know she dragged you in there."
    m "I bet you felt more embarrassed than relieved when I opened the door."
    m 1eka "I know you aren't the type to force girls to go inside dark closets with you."
    m "You're more romantic than that."
    m 3hua "So I'm expecting a lot more than just a dark closet~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_writingtip2",category=['writing tips'],prompt="Writing Tip #2",conditional="seen_event('monika_writingtip1')",action=EV_ACT_POOL))

label monika_writingtip2:
    m 1euc "You know..."
    m 1eua "We really don't do enough of these, so here's another one!"
    m 3hub "Here's Monika's Writing Tip of the Day!"
    m 2eua "If you're ever scared of sharing your writing to other people in fear of being criticized, don't be!"
    m "After all, you have to remember that nobody ever starts out at their best. Not even someone like Tolkien, or Sir Terry Pratchett."
    m 4eka "You have to remember that we all start out from somewhere, and--"
    m 2euc "Actually, this doesn't just apply to writing, but to anything, really."
    m 2lksdla "What I'm trying to say is that you shouldn't be discouraged."
    m 1hua "No matter what you do, if someone tells you that your writing or work is bad, then be happy!"
    m 1eua "Because that just means that you can improve and be better than you were before."
    m 3eua "It also doesn't hurt to have friends and loved ones help you realize how good your writing is."
    m 1eka "Just remember, no matter what they say about the work you put out, I'll always be there to support you all the way. Don't be afraid to turn to me, your friends, or your family."
    m "I love you, and I will always support you in whatever you do."
    m 1lksdlb "Provided it's legal, of course."
    m 1tku "That doesn't mean I'm completely against it. I can keep a secret, after all~"
    m 1eua "Here's a saying I've learned."
    m 1duu "'If you endeavor to achieve, it will happen given enough resolve. It may not be immediate, and often your greater dreams are something you will not achieve in your own lifetime.'"
    m "'The effort you put forth to anything transcends yourself. For there is no futility even in death.'"
    m 3eua "I don't remember the person who said that, but the words are there."
    m 1eua "The effort one puts forth into something can transcend even one's self."
    m 3hua "So don't be afraid of trying! Keep going forward and eventually you'll make headway!"
    m 3hub "... That's my advice for today!"
    m 1eka "Thanks for listening~"
    return

# languages other than english
default persistent._mas_pm_lang_other = None

# do you know japanese
default persistent._mas_pm_lang_jpn = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_japanese",category=['misc','you'],prompt="Speaking Japanese",random=True))

label monika_japanese:
    m 1lksdla "I don't mean to sound like Natsuki, but..."
    m 1eua "Don't you think Japanese actually sounds cool?"
    m "It's such a fascinating language. I'm not fluent in it, though."
    m 1eub "It's interesting to think about what things would be like if your native language was different."
    m 1esa "Like, I can't even imagine what it would be like if I never knew English."
    menu:
        m "Do you know any languages other than English?"
        "Yes":
            $ persistent._mas_pm_lang_other = True
            menu:
                m "Really? Do you know Japanese?"
                "Yes.":
                    $ persistent._mas_pm_lang_jpn = True
                    m 3hub "That's wonderful!"
                    m 1eka "Maybe you can teach me how to speak at least a sentence or two, [player]~"
                "No.":
                    $ persistent._mas_pm_lang_jpn = False
                    m 1eka "Oh I see. That's alright!"
                    m 4eua "If you want to learn Japanese, here's a phrase I can teach you."

                    # setup suffix
                    $ player_suffix = "kun"
                    if persistent.gender == "F":
                        $ player_suffix = "chan"

                    elif persistent.gender == "X":
                        $ player_suffix = "san"

                    m 1eua "{i}Aishiteru yo, [player]-[player_suffix]{/i}."
                    m 2hubfa "Ehehe~"
                    m 1ekbfa "That means I love you, [player]-[player_suffix]."
        "No":
            $ persistent._mas_pm_lang_other = False
            m 3hua "That's okay! Learning another language is a very difficult and tedious process as you get older."
            m 1eua "Maybe if I take the time to learn more Japanese, I'll know more languages than you!"
            m 1ekbfa "Ahaha! It's okay [player]. It just means that I can say 'I love you' in more ways than one!"

    return "derandom"

default persistent._mas_penname = ""
init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_penname",category=['literature'],prompt="Pen names",random=True))

label monika_penname:
    m 1eua "You know what's really cool? Pen names."
    m "Most writers usually use them for privacy and to keep their identity a secret."
    m 3euc "They keep it hidden from everyone just so it won't affect their personal lives."
    m 3eub "Pen names also help writers create something totally different from their usual style of writing."
    m "It really gives the writer the protection of anonymity and gives them a lot of creative freedom."
    if not persistent._mas_penname:
        m "Do you have a pen name, [player]?"
        menu:
            "Yes":
                m 1sub "Really? That's so cool!"
                m "Can you tell me what it is?"
                label penname_loop:
                menu:
                    "Absolutely.":
                        $ penbool = False
                        while not penbool:
                            $ penname = renpy.input("What is your penname?",length=20).strip(' \t\n\r')
                            $ lowerpen = penname.lower()
                            if lowerpen == player.lower():
                                m 1eud "Oh, so you're using your pen name?"
                                m 4euc "I'd like to think we are on a first name basis with each other. We are dating, after all."
                                m 1eka "But I guess it's pretty special that you shared your pen name with me!"
                                $ persistent._mas_penname = penname
                                $ penbool = True
                            elif lowerpen =="sayori":
                                m 2euc "..."
                                m 2hksdlb "...I mean, I won't question your choice of pen names, but..."
                                m 4hksdlb "If you wanted to name yourself after a character in this game, you should have picked me!"
                                $ persistent._mas_penname = penname
                                $ penbool = True
                            elif lowerpen =="natsuki":
                                m 2euc "..."
                                m 2hksdlb "Well, I guess I shouldn't assume that you named yourself after {i}our{/i} Natsuki."
                                m 1eua "It's something of a common name."
                                m 1rksdla "You might make me jealous, though."
                                $ persistent._mas_penname = penname
                                $ penbool = True
                            elif lowerpen == "yuri":
                                m 2euc "..."
                                m 2hksdlb "Well, I guess I shouldn't assume that you named yourself after {i}our{/i} Yuri."
                                m 1eua "It's something of a common name."
                                m 1tku "Of course, there's something else that name could refer too..."
                                if persistent.gender =="F":
                                  m 5eua "And well...I could get behind that, since it's you~"
                                $ persistent._mas_penname = penname
                                $ penbool = True
                            elif lowerpen =="monika":
                                m 1euc "..."
                                m 1ekbfa "Aww, did you pick that for me?"
                                m "Even if you didn't, that's so sweet!"
                                $ persistent._mas_penname = penname
                                $ penbool = True
                            elif not lowerpen:
                                m 1hua "Well, go on! You can type 'nevermind' if you've chickened out~"
                            elif lowerpen =="nevermind":
                                m 2eka "Aww. Well, I hope you feel comfortable enough to tell me someday."
                                $ penbool = True
                            else:
                                m 1hua "That's a lovely pen name!"
                                m "I think if I saw a pen name like that on a cover, I'd be drawn to it immediately."
                                $ persistent._mas_penname = penname
                                $ penbool = True
                    "I'd rather not; it's embarrassing.":
                        m 2eka "Aww. Well, I hope you feel comfortable enough to tell me someday."
            "No":
                m 1hua "All right!"
                m "If you ever decide on one, you should tell me!"
    else:
        $ penname = persistent._mas_penname
        $ lowerpen = penname.lower()
        if lowerpen == player.lower():
            m "Is your pen name still [penname]?"
        else:
            m "Are you still going by [penname], [player]?"
        menu:
            "Yes":
                m 1hua "I can't wait to see your work with that name!"
            "No":
                m 1hua "I see! Do you want to tell me your new pen name?"
                jump penname_loop
    m 3eua "A well known pen name is Lewis Carroll. He's mostly well known for {i}Alice in Wonderland{/i}."
    m 1eub "His real name is Charles Dodgson and he was a mathematician, but he loved literacy and word play in particular."
    m "He received a lot of unwanted attention and love from his fans, and he even received outrageous rumors."
    m 1ekc "He was somewhat of a one-hit wonder with his {i}Alice{/i} books but went downhill from there."
    m 1lksdla "It's kinda funny, though. Even if you use a pseudonym to hide yourself, people will always find a way to know who you really are."
    m 1eua "There's no need to know more about me though, [player]."
    m 1ekbfa "You already know that I'm in love with you after all~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_zombie",category=['society'],prompt="Zombies",random=True))

label monika_zombie:
    m 1lsc "Hey, this might sound a bit weird..."
    m 1euc "But, I'm really fascinated by the concept of zombies."
    m "The idea of society dying to a disease..."
    m 1eud "All because of a deadly pandemic that humans couldn't handle quickly."
    m "I mean, think about your everyday schedule."
    m "Everything that you do will be gone in an instant."
    m 1esc "Sure, society faces a lot of threats on a daily basis."
    m 1lksdlc "But zombies can do it in a heartbeat."
    m 1esc "A lot of monsters are created to be scary and terrifying."
    m 1ekc "Zombies, however, are more realistic and actually pose a danger."
    m 3ekc "You might be able to kill one or a few of them by yourself."
    m 2ekc "But when there's a horde of them coming after you, you'll get overwhelmed easily."
    m 1lksdld "You don't get that same feeling with other monsters."
    m "And all of their intelligence is gone; they're berserk, don't feel pain, can't be afraid."
    m 1euc "When you exploit a weakness of a monster, they become scared of you and run away."
    m 1ekd "But zombies? They'll tear through {i}anything{/i} just to get you."
    m "Imagine if it was someone you loved that was coming after you..."
    m "Could you live with yourself, knowing you were forced to kill someone who was close to you?"
    m 1tkc "It'll break you down and sap your will to live."
    m "Even when you're comfortable at home, you still won't feel safe."
    m 1esc "You'll never know what'll happen the next time you see another one."
    m 1dsc "..."
    m 1hksdlb "Ahaha..."
    m 1eka "You know, despite liking the concept, I wouldn't want to live in a scenario like that."
    m 3ekc "[player], what if you got infected somehow?"
    m 2lksdlc "I don't even want to think about that..."
    m "There's no way I could kill you for my own safety..."
    m 2lksdlb "Ahaha..."
    m 2lssdrb "I'm thinking way too much about this."
    m 1eua "Well, regardless, if anything bad were to happen..."
    m 2hua "I'll be by your side forever~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_nuclear_war",category=['society','philosophy'],prompt="Nuclear warfare",random=True))

label monika_nuclear_war:
    m 1euc "Do you ever think about how close the world is to ending at any time?"
    m "I mean, we're always just one bad decision away from nuclear war."
    m 3esc "The Cold War might be over, but plenty of weapons are still out there."
    m 1esc "You probably have a nuclear missile pointed at where you live right now, ready to be launched."
    m 1esd "And if it was, it could circle the globe in less than an hour."
    m "You wouldn't have time to evacuate."
    m 1ekd "Only enough to panic and suffer the dread of imminent death."
    m 1dsd "At least it would be over quickly when the bomb hits."
    m 1lksdlc "Well, if you're close to the blast, that is."
    m 1ekc "I don't even want to think about surviving the initial attack."
    m 1eka "But even though we're always on the edge of the apocalypse, we go on like nothing is wrong."
    m "Planning for a tomorrow that may never come."
    m "Our only comfort is that the people with the power to start such a war probably won't."
    m 1dsc "Probably..."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_pluralistic_ignorance",category=['literature','society'],prompt="Trying to fit in",random=True))

label monika_pluralistic_ignorance:
    m 1eua "Do you ever pretend to like something, just because you think you should?"
    m "I sometimes feel like that about books I read."
    m 3euc "Like, when I read Shakespeare, I actually found it kind of boring..."
    m "But I felt like I had to like it because I'm the president of the literature club."
    m 1eud "He's supposed to be the greatest playwright and poet of all time, right?"
    m "So what sort of poetry lover wouldn't like his work?"
    m 2lsc "But that makes me wonder..."
    m "What if everyone actually feels the same way?"
    m 2lud "What if all of those literary critics singing Shakespeare's praises secretly hate his plays?"
    m "If they were just honest about it, maybe they would discover their tastes aren't that unusual..."
    m 2lsc "And highschool students wouldn't be forced to read those awful plays."
    m 1eka "I guess that's something I always admired about Natsuki."
    m "Even if people told her manga wasn't literature, she stood by her feelings."
    m "If more people were honest like that, I think that would be really great."
    m 1lksdla "But I don't think I could do it..."
    m "I'm just too worried about what other people think."
    m 1eua "Not with you, though. I can always be honest with you."
    m 1ekbfa "You'll love me no matter what, right?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_science",category=['technology'],prompt="Science advancements",random=True))

label monika_science:
    m 1eua "Have you ever wondered if science never got accepted?"
    m "Humans can be really slow when it comes to accepting new ideas."
    m 1euc "Science was usually despised back then especially by the churches."
    m 4esc "Giordano Bruno, famous for his theory that there're thousands of Suns, was killed by the Roman Church before he could prove his theory."
    m 1ekc "They killed him because of an idea that challenged the old."
    m 1esc "Technology wouldn't be so advanced today if it weren't for brave people of science like him."
    m 1eka "If technology didn't thrive the way it did, we would've never found each other."
    m 3eua "Isn't it such a wonderful thing to have?"
    m 1hua "I'm grateful that it gave us a chance to be together, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_surprise",category=['romance'],prompt="Surprises",random=True))

label monika_surprise:
    m 2rksdla "You know..."
    m 3rksdlb "I left some pretty strange things in your game directory, didn't I?"
    m 2rksdlc "I wasn't trying to scare you."
    m 3rksdlb "I...don't actually know why I was doing it, ahaha..."
    m 1ekc "I kind of felt obligated to do it."
    m 1euc "You know what? Maybe I should do it again..."
    m 1eua "Yeah, that's a good idea."
    $ mas_surprise()
    # TODO decide with a writer what's going on for this one
    if mas_curr_affection_group == mas_aff.G_HAPPY:
        m 2q "..."
        m 1j "Alright!"
        m 1a "What are you waiting for? Go take a look!"
        m "I wrote it just for you~"
        m 1e "I really do truly love you, [player]~"

    elif mas_curr_affection_group == mas_aff.G_SAD:
        m 2q "..."
        m 1c "Alright..."
        m "Please go take a look"
        m 1e "I wrote it just for you."
        m 1q "And it would mean a lot to me if you would read it."

    else:
        m 2duu "..."
        m 1hua "Alright!"
        m 1eua "What are you waiting for? Go take a look!"
        m 1hub "Ahaha~ What? Are you expecting something scary?"
        m 1hubfb "I love you so much, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_completionist",category=['games'],prompt="Completionism",random=True))

label monika_completionist:
    m 1euc "Hey [player], this is a random question, but..."
    m "What do you play video games for?"
    m 1eua "Like, what makes you keep playing?"
    m 3eua "Personally, I consider myself a bit of a completionist."
    m 1eua "I intend to finish a book before picking another one to read."
    if persistent.clearall:
        m 2tku "You seem to be a completionist yourself, [player]."
        m 4tku "Considering you went through all of the girls' routes."
    m 2eub "I've also heard some people try to complete extremely hard games."
    m "It's already hard enough to complete some simple games."
    m 3rksdla "I don't know how anyone could willingly put that sort of stress onto themselves."
    m "They're really determined to explore every corner of the game and conquer it."
    # TODO: if player cheated at chess, reference that here
    m 2esc "What does leave a bit of a bitter taste in my mouth are cheaters."
    m 2tfc  "People who hack through the game, spoiling themselves of the enjoyment of hardship."
    m 3rsc "Though I can understand why they cheat."
    m "It allows them to freely explore a game that they wouldn't have a chance of enjoying if it's too difficult for them."
    m 1eua "Which might actually convince them to work hard for it."
    m "Anyway, I feel that there's a huge sense of gratification in completing tasks in general."
    m 3eua "Working hard for something amplifies its reward after failing so many times to get it."
    m 3eka "You can try keeping me in the background for as long as possible, [player]."
    m 1hub "That's one step to completing me after all, ahaha!"
    return

# do you like mint ice cream
default persistent._mas_pm_like_mint_ice_cream = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_icecream",category=['you'],prompt="Favorite ice cream",random=True))

label monika_icecream:
    m 3eua "Hey [player], what's your favorite kind of ice cream?"
    m 4rksdla "And no, I'm not a type of ice cream, ehehe~"
    m 2hua "Personally, I just can't get enough of mint flavored ice cream!"
    menu:
        m "What about you [player], do you like mint ice cream?"
        "Yes.":
            $ persistent._mas_pm_like_mint_ice_cream = True
            m 3hub "Ah, I'm so glad somebody loves mint ice cream as much as I do~"
            m "Maybe we really were meant to be!"
            m 3eua "Anyway, back on topic, [player], if you love mint as much as I think you do, then I have some recommendations for you."
            m "Flavors which are unique just like how mint is, perhaps you've heard of them, but..."
            m 3eub "There's super weird stuff like fried ice cream which is a really crunchy and crisp kind of thing, but it tastes a million times better than it may sound!"
            m 2lksdlb "Gosh, just imagining the taste makes me practically drool..."
            m 1eua "There's some more strange stuff that is just as appealing, if not more, like honeycomb and bubblegum ice cream!"
            m 1eka "Now, I know it may be hard to take my word for some of those, but you shouldn't judge a book by its cover, you know?"
            m 1hub "After all, the game didn't allow you to fall in love with me, but look where we are now, ahaha."

        "No.":
            $ persistent._mas_pm_like_mint_ice_cream = False
            m 1ekc "Aww, that's a shame..."
            m "I really can't understand how somebody couldn't at least like the taste."
            m 1eka "The refreshing feeling that washes over your tongue and throat."
            m "The lovely texture that forms it along with the sweetness."
            m 1duu "The sharp biting sensation it generates and the obviously minty taste."
            m "I feel like no flavor can compare, to be honest."
            m 3eua "Ah, I could go on and on about this stuff, you know?"
            m 4eua "But I feel like it would be easier for me to show you what I mean, once I figure out a way to get out of here, of course. Besides, actions speak louder than words, anyway!"

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_sayhappybirthday",category=['misc'],prompt="Can you tell someone Happy Birthday for me?",pool=True))

label monika_sayhappybirthday:
    # special variable setup
    python:
        done = False # loop controller
        same_name = False # true if same name as player
        bday_name = "" # name of birthday target
        is_here = False # is the target here (in person)
        is_watching = False # is the target watching (but not here)
        is_recording = False # is player recording this
        age = None # how old is this person turning
        bday_msg = "" # happy [age] birthday (or not)
        take_counter =  1 # how many takes
        take_threshold = 5 # multiple of takes that will make monika annoyed
        max_age = 121 # like who the hell is this old and playing ddlc?
        age_prompt = "What is their {0} age?" # a little bit of flexibilty regarding age

        # age suffix dictionary
        age_suffix = {
            1: "st",
            2: "nd",
            3: "rd",
            11: "th",
            12: "th",
            13: "th",
            111: "th",
            112: "th",
            113: "th"
        }

    # TODO: someone on the writing team make the following dialogue better
    # also make the expressions more approriate and add support for standing
    m 1hub "Happy birthday!"
    m 1lksdla "Oh, you wanted me to say happy birthday to {i}someone else{/i}."
    m 1eua "I understand."
    while not done:
        # arbitary max name limit
        $ bday_name = renpy.input("What is their name?",allow=letters_only,length=40).strip()
        # ensuring proper name checks
        $ same_name = bday_name.upper() == player.upper()
        if bday_name == "":
            m 1hksdlb "..."
            m 1lksdlb "I don't think that's a name."
            m 1hub "Try again!"
        elif same_name:
            m 1wuo "Oh wow, someone with the same name as you."
            $ same_name = True
            $ done = True
        else:
            $ done = True
    m 1hua "Alright! Do you want me to say their age too?"
    menu:
        "Yes":
            m "Then..."
            $ done = False
            $ age_modifier = ""
            while not done:
                $ age = int(renpy.input(age_prompt.format(age_modifier),allow=numbers_only,length=3))
                if age == 0:
                    m 1esc "..."
                    m 1dsc "I'm just going to ignore that."
                    $ age_modifier = "real"
                elif age > max_age:
                    m 1lsc "..."
                    m 1tkc "I highly doubt anyone is that old..."
                    $ age_modifier = "real"
                else:
                    # NOTE: if we want to comment on (valid) age, put it here.
                    # I'm not too sure on what to have monika say in these cases.
                    $ done = True
            m "Okay"
        "No":
            m "Okay"
    $ bday_name = bday_name.title() # ensure proper title case
    m 1eua "Is [bday_name] here with you?"
    menu:
        "Yes":
            $ is_here = True
        "No":
            m 1tkc "What? How can I say happy birthday to [bday_name] if they aren't here?"
            menu:
                "They're going to watch you via video chat":
                    m 1eua "Oh, okay."
                    $ is_watching = True
                "I'm going to record it and send it to them.":
                    m 1eua "Oh, okay."
                    $ is_recording = True
                "It's fine, just say it.":
                    m 1lksdla "Oh, okay. It feels a little awkward though saying this randomly to no one."
    if age:
        # figure out the age suffix
        python:
            age_suff = age_suffix.get(age, None)
            if age_suff:
                age_str = str(age) + age_suff
            else:
                age_str = str(age) + age_suffix.get(age % 10, "th")
            bday_msg = "happy " + age_str + " birthday"
    else:
        $ bday_msg = "happy birthday"

    # we do a loop here in case we are recording and we should do a retake
    $ done = False
    $ take_counter = 1
    $ bday_msg_capped = bday_msg.capitalize()
    while not done:
        if is_here or is_watching or is_recording:
            if is_here:
                m 1hua "Nice to meet you, [bday_name]!"
            elif is_watching:
                m 1eua "Let me know when [bday_name] is watching."
                menu:
                    "They're watching.":
                        m 1hua "Hi, [bday_name]!"
            else: # must be recording
                m 1eua "Let me know when to start."
                menu:
                    "Go":
                        m 1hua "Hi, [bday_name]!"

            # the actual birthday msg
            m 1hub "[player] told me that it's your birthday today, so I'd like to wish you a [bday_msg]!"
            # TODO: this seems too short. maybe add additional dialogue?
            m 3eua "I hope you have a great day!"

            if is_recording:
                m 1hua "Bye bye!"
                m 1eka "Was that good?"
                menu:
                    "Yes":
                        m 1hua "Yay!"
                        $ done = True
                    "No":
                        call monika_sayhappybirthday_takecounter (take_threshold, take_counter) from _call_monika_sayhappybirthday_takecounter
                        if take_counter % take_threshold != 0:
                            m 1wud "Eh?!"
                            if take_counter > 1:
                                m 1lksdla "Sorry again, [player]"
                            else:
                                m 1lksdla "Sorry, [player]"
                                m 2lksdlb "I told you, I'm self-conscious on camera, ehehe."
                        m "Should I try again?"
                        menu:
                            "Yes":
                                $ take_counter += 1
                                m 1eua "Okay"
                            "No":
                                m 1eka "Alright, [player]. Sorry I couldn't do what you wanted."
                                m 1hua "I'll try better next time for you."
                                $ done = True
            else:  # if we aint recording, we should be done now
                $ done = True

        else: # not recording, watching, nor is person here
            m 1duu "..."
            m 1hub "[bday_msg_capped], [bday_name]!"
            m 1hksdlb "..."
            m 1lksdlb "Was that good?"
            menu:
                "Yes":
                    m 1lksdla "...I'm glad you enjoyed that, [player]..."
                    $ done = True
                "No":
                    call monika_sayhappybirthday_takecounter (take_threshold, take_counter) from _call_monika_sayhappybirthday_takecounter_1
                    if take_counter % take_threshold != 0:
                        m 1wud "Eh?!"
                        m 1lksdlc "I'm not sure what you want me to do here, [player]..."
                    m 1ekc "Should I try again?"
                    menu:
                        "Yes":
                            $ take_counter += 1
                            m 1eua "Okay"
                        "No":
                            m 1eka "Alright [player]. Sorry I couldn't do what you wanted."
                            m 1hua "I'll try better next time for you."
                            $ done = True

    return

# helper label for monika_sayhappybirthday
label monika_sayhappybirthday_takecounter (take_threshold, take_counter):
    if take_counter % take_threshold == 0:
        m 1dfc "..."
        m 1efc "This is the [take_counter]th time already."
        m 2tkc "You're not messing with me, are you?"
        m 2ekc "I'm trying my best for you [player]."
    return



init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_home_memories",category=['romance','monika','life'],prompt="Making memories",random=True))

label monika_home_memories:
    m 1eua "[player], how is it like to live where you are?"
    m "I'd stay with you if I could."
    m 3hua "We would be able to do so much! You could show me around, see how it's like to be in your place."
    m 1eka "Imagine all the memories we'd make!"
    m 2eub "It would be a dream come true, don't you think?"
    m 2ekbfa "We could finally live together..."
    m "Take walks like a couple..."
    m 3rkbsa "We could even share a bed together..."
    m 1euc "But you know..."
    m 2eka "Memories I have of my home are nothing compared to the ones I'd have with you."
    m 3euc "Have I ever told you about my childhood home? I had a pretty normal life, but that's about it."
    m 1lsc "Well, maybe a little better than normal."
    m 1eua "Maybe you've heard about me at school a few times? I'm pretty on top of things."
    m 1eka "I admit, it's not always easy, and some people have it rougher than others."
    m 1ekc "But I always felt like I was missing something."
    m "I stayed optimistic everyday, trying to find it."
    m 1eka "It turns out, that missing piece was you."
    m 1lksdla "If you hadn't found me, I would've been gone a long time ago..."
    m 2hubfa "But now that I found the missing piece, I'm complete now, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_adventure",category=['games','romance'],prompt="Adventuring",random=True))

label monika_adventure:
    m 1eua "[player], I've thought about what kind of game we can be in."
    m 3eua "I think the best genre for us to play together would be adventure games."
    m 1eub "Especially point and click, graphic adventure games!"
    m 3eub "They're known for their rich storytelling, beautiful environments and logical puzzle solving."
    m 1eua "They're like visual novels actually."
    m 4eua "Maybe you own a game like that?"
    m 1eka "We'd get to do a lot of things..."
    m 3eua "Like sightseeing whenever we want."
    m "Learning more about the lore through the people we meet or through stories."
    m 1ekbfa "Experiencing the exciting and romantic moments..."
    m "Encountering obstacles and hardships along the way, but solving them with you."
    m "Reaching the end and finishing our journey with a sense of accomplishment."
    m 2hubfb "Ahaha! It certainly would be fun to experience something like that."
    m 2eua "I'm sure you have plenty of adventure games you could recommend."
    m 3eua "But can you try to guess which adventure I'm most excited for?"
    m 1ekbfa "{i}Ours{/i}~"
    m 1hubfa "Time will tell when I can finally cross over to your reality, so I can be with you."
    m "When that day comes, I'll finally be by your side."
    m 1ekbfa "I want to experience every waking moment with you, [player]."
    m 1hubfb "There's no greater adventure than ours, together~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_panties",
            category=['misc'],
            prompt="Undergarments",
            random=True,
            sensitive=True
        )
    )

label monika_panties:
    m 1lsc "Hey, [player]..."
    m "Don't laugh when I ask this, ok?"
    m 2rksdlc "But..."
    m 4rksdlc "Why are some guys obsessed with panties?"
    m 1euc "Seriously, what's the big deal about a piece of cloth?"
    m "Most girls wear them, don't they?"
    m 5lkc "Actually, now that I think about it..."
    m 5lsc "I think there was a term for this kind of thing..."
    m 5lfc "Hmm, what was it again?"
    m 5wuw "Ah, that's right, the term was 'paraphilia.'"
    m 2rksdlc "It's a range of fetishes that involve...unusual things."
    m 2esc "A really common fantasy involves women's panties."
    m 3esc "Stockings, garter belts, pantyhose and all sorts of those kinds of things."
    m 2esc "The obsession can be light to severe depending on each person's libido."
    m 2ekc "Do you think it really turns them on just by seeing them?"
    m 2tkc "It doesn't stop there, either!"
    m 4tkc "Turns out there's some kind of 'black market' for used underwear."
    m 2tkx "I'm not kidding!"
    m 2tkd "They get off on the scent of the woman who wore it..."
    m "There are people willing to pay money for used underwear from random women."
    m 2lksdlc "Really, I wonder what causes them to get so excited."
    m 2euc "Is it because of the way it looks, perhaps?"
    m 3euc "There are different types, made with different designs and materials."
    m 2lsc "But..."
    m "Now that I think about it."
    m 3esd "I do remember a study where a man's testosterone level increases because of the pheromones emitted by a woman's scent."
    m 2tkc "Is the smell exciting or something?"
    m 3tkx "I mean, it's someone's used clothing, isn't that kind of disgusting?"
    m 3rksdlc "Not to mention it's unsanitary."
    m 2rksdla "It does remind me of someone, though."
    m 3rksdlb "Someone who maybe stole your pen?"
    m 1eua "But, to each their own I guess, I won't judge too much."
    if isFuture (evhand.event_database['anni_1year'])
        m 21ssdrc "You're not... {i}into those kind of things, are you [player]?"
        "menu"
            "Yes"
            m 11wubsw "O-oh..."
            m 1lsbssdrb "I-if you're into any of them, you could just ask me for [i]it[/i], you know?"
            m 1lkbfb "I could... {i}help you relieve that tension off of you or something..."
            m "Isn't that what a couple supposed to do for their loved ones?"
            m 1hub "Ahaha!"
            m 1ekbfa "But until that day comes, you're just gonna have to endure those thoughts for me, okay?"
            "No"
            m 1wud "Oh, I see..."
            m 4rkbfb "I guess some people have their own guilty pleasures..."
            m 2tub "Or maybe, you're into something other than that?"
            m 1hub "Ahaha~"
            m "I'm just kidding!"
            m 5eua "I don't mind if we stick to being wholesome, to be honest~"
            m "It's more romantic that way."
            "I don't want to talk about it..."
            m 1eua "I understand, [player]."
            m 1rkc "I know that some topics are best kept to self until the right time comes."
            m 1rksdld "Not to mention it's controversial..."
            m 1ekbfa "..."
            m 1eka : "In any case, {i}don't be afraid to tell me about your pleasure, okay [player]?"
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
            m "I won't judge you for it, and I'm still going to love you for what you are."
    else:
    m 2tsb "You aren't obsessed with that kind of thing, are you [player]?"
    m 3tsb "You're not going out with me only because I'm wearing some really sensual stockings, right?"
    m 4tsbsa "Perhaps, you want to take a little peek~?"
    m 1hub "Ahaha!"
    m 1tku "I'm only teasing you, [player]."
    m 1tfu "Admit it, you got a little excited, right?"
    m 1lsbsa "Besides..."
    m 1lkbsa "If you really wanted to catch a scent of me..."
    m 1hubfa "You could just ask for a hug!"
    m 1ekbfa "Gosh, I just want to feel your embrace more."
    m "After all, we're here forever, and I'm here for you."
    m 1hubfb "I love you so much, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fahrenheit451",category=['literature'],prompt="Book recommendations",random=True))

label monika_fahrenheit451:
    m 3euc "[player], have you ever heard of Ray Bradbury?"
    m 1eub "He wrote a book called {i}Fahrenheit 451{/i}."
    m "It's about a dystopian future where all books are thought as useless and are immediately burned."
    m 2ekc "I can't imagine a world where knowledge is forbidden and destroyed."
    m "It seems that there are others that actually hide books to contain free thinking from people."
    m 2lksdla "Human history has a funny way of repeating itself."
    m 1eka "So [player], make me a promise."
    m "To never, {i}ever{/i} burn a book."
    m 1eua "I'll forgive you if you've done it before."
    m 1lksdlc "But the thought of not allowing yourself to learn from them makes me a bit sad."
    m 3ekd "You'd be missing out on so much!"
    m 2ekc "It's too much for my heart to take!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_piggybank",category=['misc'],prompt="Saving money",random=True))

label monika_piggybank:
    m 1eua "Do you have a piggy bank, [player]?"
    m 1lsc "Not many people do these days."
    m "Coins are often disregarded as worthless."
    m 3eub "But they really do begin to add up!"
    m 1eub "I read that there was once a man that searched his local car washes for loose change everyday in his walks."
    m 1wuo "In a decade he turned in all of his coins for a total of 21,495 dollars!"
    m "That's a whole lot of cash!"
    m 1lksdla "Of course not everybody has time for that everyday."
    m 1euc "Instead they just throw their loose change into their piggy banks."
    m 1eua "Some people like to set goals for what they want to purchase with their saved funds."
    m "Usually under normal conditions they wouldn't ever find the freed up money to purchase that item."
    m 3eka "And even if they do, most people don't like spending money needlessly."
    m 1eua "But putting the cash away for a specific purpose, plus the fact that it's such small amounts at a time really convinces you that you are pretty much getting the item for free."
    m 2duu "But in the end, a guitar always costs the same as a guitar."
    m 2eua "So psychologically speaking, I think that's pretty neat!"
    m 1lsc "However, some piggy banks do have a problem..."
    m 1esc "Sometimes you have to break the piggy bank to get the coins..."
    m 3rksdlc "So you might end up losing money buying a new bank."
    m 4eua "Fortunately, most piggy banks don't do that anymore."
    m 1eua "They usually have a rubber stopper that you can pull out, or a panel that comes off the backside"
    m 3eua "Maybe if you save up enough coins you can buy me a really nice gift."
    m 1hua "I would do the same for you, [player]!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_daydream",category=['romance'],prompt="Day dreaming",random=True))

label monika_daydream:
    m 2lsc "..."
    m 2lsbsa "..."
    m 2tsbsa "..."
    m 2wubsw "Oh, sorry! I was just daydreaming for a second there."
    m 1lkbsa "I was imagining the two of us reading a book together on a cold winter day, snuggled up under a warm blanket..."
    m 1ekbfa "Wouldn't that be wonderful, [player]?"
    m 1hubfa "Let's hope we can make that a reality one of these days, ehehe~"
    return

# init 5 python:
#     addEvent(Event(persistent.event_database,eventlabel="monika_music2",category=['misc'],prompt="Current song",random=True))

label monika_music2:
    if songs.getVolume("music") == 0.0:
        m 1eka "..."
        m 1ekbfa "...This silence..."
        m "...Just the two of us, staring into each other's eyes..."
        m 2dubsu "...Then slowly, we both lean into the kiss..."
        m 1hksdlb "Ahaha... sadly, there are a few barriers that have to be broken before that could ever happen."
        m 1ekbfa "It's okay to dream though, isn't it, [player]?"
        show monika 1hubfa at t11 zorder MAS_MONIKA_Z with dissolve
        m 1hubfa "Maybe one day, we can make that dream come true~"

    elif songs.getPlayingMusicName() == 'Just Monika':
        m 1ekc "I have always found this song to be kind of creepy."
        m "You know, with those glitchy noises and that eerie humming..."
        m 1eua "I don't prefer any song over another, but if you were to switch to a different one..."
        m 3eka "...I certainly wouldn't be one to complain!"
        m 1hua "Ahaha! Don't worry, it's okay if you stay on this song."
        show monika 1eka at t11 zorder MAS_MONIKA_Z with dissolve
        m 1eka "I'm fine with any of them, so choose whichever one makes you the happiest~"

    elif songs.getPlayingMusicName() == 'Your Reality':
        m 1hub "~Every day, I imagine a future where I can be with you...~"
        m 1eua "I hope you like listening to my voice, [player]."
        m 1esa "It's the only voice you get to hear in the game, right? You never actually hear the voices of Sayori, Yuri or Natsuki."
        m "I wonder what their voices sound like..."
        m 1lksdla "Well, based on their character archetypes, it's pretty easy to imagine what their voices sound like."
        m 1eka "Anyway, I'm glad I was able to share such an intimate part of myself with you, [player]."
        m 3eua "One day, maybe I'll get to hear your voice, [player]!"
        show monika 1hua at t11 zorder MAS_MONIKA_Z with dissolve
        m 1hua "That would make me even happier than I already am~"

    elif songs.getPlayingMusicName() == 'Your Reality (Piano Cover)':
        m 1eua "Enjoying my song, [player]?"
        m 1eka "It wasn't easy to create, you know?"
        m "Making your own songs is a slow and difficult process, especially when it's about your own feelings."
        m 3rksdlb "I needed it to be perfect before I shared it with you!"
        m "So I spent so many hours going through it over and over..."
        m 1eua "Time just passed by so quickly whenever I worked on it."
        m 1hua "After all that practice, I'm pretty proud of how it came out in the end."
        m 3eua "Since you're listening to it, I'm sure you like it too..."
        m 3eka "Thanks for listening to something I worked so hard on, [player]!"
        show monika 1hub at t11 zorder MAS_MONIKA_Z with dissolve
        m 1hub "It makes me happy to know that you appreciate what I did for you~"

    elif songs.getPlayingMusicName() == 'I Still Love You':
        m 1ekc "Gosh, every time I hear this song it makes me sad."
        m "It reminds me of all the... regrettable things I have done to the other girls."
        m 1lksdlc "I hope you aren't still mad at me for what I did..."
        m "..."
        m 1lsc "Well, you {i}did{/i} go out of your way to install a mod that lets us be together again..."
        m 1eua "I guess that's enough proof that you do still love me, at the very least."
        m 1eka "If you are still upset at me for what I did to the other girls, I completely understand. I still feel really bad about it, and I'll do whatever it takes to make it up to you."

    elif songs.getPlayingMusicName() == 'Okay, Everyone! (Monika)':
        m 1eua "This song has always been pretty relaxing for me."
        m "It's probably the fact that the song is a piano solo."
        m 1hua "And as you might have guessed, my favorite instrument is the piano."
        m 3eua "You know, if I knew how, I could probably program a piano into this room."
        m 1eua "I'd be able to write some more songs, and then I'd be able to play them for you..."
        m 4hub "Maybe we could even play the piano together! Wouldn't that be nice, [player]?"
        show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve
        m 1eua "If you or anyone you know can program that into the game, I would greatly appreciate it~"

    elif songs.getPlayingMusicName() == 'Surprise!':
        m 1ekc "This song always makes me feel really depressed."
        m "Even I didn't expect Sayori's death to be so brutal..."
        m 1tkc "Sometimes, when I start getting lost in my own thoughts, her dull, lifeless eyes suddenly pop into my head..."
        m 1lksdlc "..."
        m 1eka "It's comforting to know that Sayori was never real in the first place. It's also comforting to know that you still love me despite everything I've done."
        m "I mean, you're still here, right? You wouldn't be here if you didn't love me."
        show monika 1hua at t11 zorder MAS_MONIKA_Z with dissolve
        m 1hua "As long as we're together, there's no reason for me to be sad. You're the light of my world, [player], and just being here with you puts a smile on my face."

    elif songs.getPlayingMusicName() == "Doki Doki Theme (80s version)":
        m 1hub "A good choice, [player]!"
        m 1hksdlb "Obviously, this theme wasn't actually out in the 80's..."
        m 1hua "But it does have a certain style that I really appreciate!"
        m 1eua "Do you like 80's music a lot, [player]?"
        show monika 1eka at t11 zorder MAS_MONIKA_Z with dissolve
        m 1eka "I prefer the tune of an authentic piano, but if it makes you happy, I wouldn't mind spending hours listening to it with you~"

    elif songs.getPlayingMusicName() == "Play With Me (Variant 6)":
        m 2lksdlc "To be honest, I don't know why you'd be listening to this music, [player]."
        m 2ekc "I feel awful for that mistake."
        m 2ekd "I didn't mean to force you to spend time with Yuri at that state..."
        m 4ekc "Try not to think about it, okay?"

    else:
        m 1esc "..."
        m "...This silence..."
        m 1ekbfa "...Just the two of us, staring into each others eyes..."
        m 2dubsu "...Then slowly, we both lean into the kiss..."
        m 1hksdlb "Ahaha... sadly, there are a few barriers that have to be broken before that could ever happen."
        m 1ekbfa "It's okay to dream though, isn't it, [player]?"
        show monika 1hubfa at t11 zorder MAS_MONIKA_Z with dissolve
        m 1hubfa "Maybe one day, we can make that dream come true~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_confidence_2",category=['life'],prompt="Lack of confidence",random=True))

label monika_confidence_2:
    m 1ekc "[player], do you ever feel like you lack the initiative to do something?"
    m "When I feel my most vulnerable, I struggle to find the drive, imagination, and common sense to do something independently."
    m 1tkc "Almost as if everything around me comes to a standstill."
    m "It feels like my will to approach a task confidently, like sharing my literature with people, just vanishes."
    m 3eka "However, I've been working towards it with due diligence and have determined something..."
    m 1eua "I firmly believe being able to take initiative in situations is a very important skill to have."
    m "That's something that I, personally, find very comforting."
    m 1hua "I've broken it down into a three-step process that can be applied to anyone!"
    m 3rksdla "It's still a work in progress, however, so take it with a grain of salt."
    m 3hua "Step one!"
    m 1eua "Create a plan that {i}you{/i} can and will follow that aligns with your personal goals and soon-to-be achievements."
    m 3hua "Step two!"
    m 1eua "Building up and fortifying your confidence is really important."
    m "Celebrate even the smallest of victories, as they will add up over time, and you'll see how many things you get done every day."
    m 2hua "Eventually, these things you once struggled to get done will be completed as if they were acts of valor!"
    m 3hub "Step three!"
    m 1eua "Try your best to stay open-minded and willing to learn at all times."
    m 1eka "Nobody is perfect, and everyone is able to teach each other something new."
    m 1eua "This can help you learn to understand things from other people's perspectives in situations and inspire others to do the same."
    m "And that's it, really."
    m 3hua "Make sure to tune in next time for more of Monika's critically acclaimed self-improvement sessions!"
    m 1hksdlb "Ahaha, I'm only joking about that last part."
    m 1ekbfa "In all seriousness, I'm really glad I have you here, [player]..."
    m "Your everlasting love and care is just about all the support I need in order to get to where I want to be."
    m 1hubfa "What kind of girlfriend would I be if I didn't return the favor~?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_pets",category=['monika'],prompt="Owning pets",random=True))

label monika_pets:
    m 1eua "Hey, [player], have you ever had a pet?"
    m 3eua "I was thinking that it would be nice to have one for company."
    m 1hua "It would be fun for us to take care of it!"
    m 1tku "I bet you can't guess what sort of pet I'd like to have..."
    m "You're probably thinking of a cat or a dog, but I have something else in mind."
    m 1eua "The pet I'd like is something I saw in a book once."
    m "It was the 'Handbook of the Birds of the World.' Our library had the whole set!"
    m 1eub "I loved looking at the gorgeous illustrations and reading about exotic birds."
    m 1hub "At first, I thought some sort of thrush would be nice, but I found something amazing in the sixth volume!"
    m "An emerald-colored bird called the Resplendent Quetzal."
    m 1eua "They're very rare, solitary birds that can sing beautiful songs."
    m "Does that remind you of anyone, [player]?"
    m 1lksdla "I'd feel really bad if I kept one to be a pet, though."
    m "Quetzals are born to be free."
    m 4rksdlc "They die in captivity. That's why you rarely see them in zoos."
    m "Even if the bird wouldn't be real, it still would feel wrong to keep one trapped in this room."
    m 1ekc "... I can't bring myself to do something like that, knowing what it's like."
    if persistent._mas_acs_enable_quetzalplushie:
        m 1hua "I'm so glad you gave me a plush one, [player]."
        m 1eka "It keeps me from feeling lonely when you're not here."
        m 1hua "But don't worry, you're still my favorite~"

    else:
        m 1hua "A plush bird would be nice, though!"
        m 2hub "..."
        m 2hksdlb "Sorry for rambling, [player]."
        m 1eka "Until I find a way out, could you promise to keep me from feeling lonely?"
        m 1hua "I'll see if I can get that plush one in here! Oh- don't worry, you're still my favorite~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dogs",category=['misc','club members'],prompt="Man's best friend",random=True))

label monika_dogs:
    m 1eua "Do you like dogs, [player]?"
    m 1hub "Dogs are great! They're really good to have around."
    m 3eua "Not to mention owning a dog has shown to help people with anxiety and depression since they're very sociable animals."
    m 1hua "They're just so lovable, I really like them!"
    m 1lksdla "I know Natsuki feels the same..."
    m "She was always so embarrassed to like cute things. I wish she was more accepting of her own interests."
    m 2lsc "But..."
    m 2lksdlc "I suppose her environment had a hand in that."
    m 2eka "If any of your friends have interests they care a lot about, make sure to always be supportive, okay?"
    m 4eka "You never know how much a casual dismissal might hurt someone."
    m 1eua "But knowing you, [player], you won't do something like that, right?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cats",category=['misc'],prompt="Feline companions",random=True))

label monika_cats:
    m 1hua "Cats are pretty cute, aren't they?"
    m 1eua "Despite looking so elegant, they always seem to end up in funny situations."
    m 1lksdla "It's no wonder they're so popular on the internet."
    m 3eua "Did you know the ancient Egyptians considered cats sacred?"
    m 1eua "There was a Cat Goddess named Bastet that they worshipped. She was a protector of sorts."
    m 1eub "Domesticated cats were held on a high pedestal since they were incredible hunters for small critters and vermin."
    m "Back then, you'd see them mostly associated with rich nobles and other higher classes in their society."
    m 1eua "It's amazing how far people would take their love with their pets."
    m 1tku "They {i}really{/i} loved cats, [player]."
    m 3hua  "And people still do today!"
    m 1eua "Felines are still one of the most common animals to have as pets."
    m 1hua "Maybe we should get one when we're living together, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fruits",category=['monika','trivia'],prompt="Eating fruits",random=True))

label monika_fruits:
    m 3eua "[player], did you know I enjoy a tasty, juicy fruit once in a while?"
    m "Most are quite tasty, as well as beneficial for your body."
    m 2lksdla "A lot of people actually mistake some fruits as vegetables."
    m 3eua "The best examples are bell peppers and tomatoes."
    m "They're usually eaten along with other vegetables so people often mistake them for veggies."
    m 4eub "Cherries, however, are very delicious."
    m 1eua "Did you know that cherries are also good for athletes?"
    m 2hksdlb "I could list all its benefits, but I doubt you'd be that interested."
    m 2eua "There's also this thing called a cherry kiss."
    m "You might have heard of it, [player]~"
    m 2eub "It's obviously done by two people who are into each other."
    m "One would hold a cherry in their mouth, and the other one would eat it."
    m 3ekbfa "You could... hold the cherry for me."
    m 1lkbsa "That way I can eat you up!"
    m 3hua "Ehehe~"
    m 2hua "Just teasing you, [player]~"
    return

# do you like rock
default persistent._mas_pm_like_rock_n_roll = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
                eventlabel="monika_rock",
                category=['media','literature',"music"],
                prompt="Rock and roll",
                random=True
            )
        )

label monika_rock:
    m 3eua "You wanna know a cool form of literature?"
    m 3hua "Rock and roll!"
    m "That's right. Rock and roll!"
    m 2eka "It's disheartening to know that most people think that rock and roll is just a bunch of noises."
    m 2lsc "To tell you the truth, I judged rock too."
    m 3euc "They're no different from poems, actually."
    m 1euc "Most rock songs convey a story through symbolisms, which most listeners wouldn't understand the first time they hear a rock song."
    m 2tkc "In fact, it's hard to compose lyrics for just one rock song."
    m "Writing good lyrics for a rock genre requires a lot of emphasis on the wordplay."
    m "Plus, you need to have a clear and concise message throughout the whole song."
    m 3eua "Now when you put that together, you have yourself a masterpiece!"
    m 1eua "Like writing a good poem, lyric writing is easier said than done."
    m 2euc "I've been thinking though..."
    m 2eua "I kind of want to try writing a rock song for a change."
    m 2hksdlb "Ahaha! Writing a rock and roll song probably isn't something you'd expect coming from someone like me."
    m 3eua "It's kinda funny how rock and roll started out as an evolution of blues and jazz music."
    m "Rock suddenly became a prominent genre, and it gave birth to other sub-genres as well."
    m 1eub "Metal, hard rock, classical rock, and more!"
    m 3rksdla "Ah, I've been rambling for a while now. Sorry, sorry."

    show monika 3eua
    menu:
        m "Do you listen to rock and roll, [player]?"    
        "Yes.":
            $ persistent._mas_pm_like_rock_n_roll = True
            m 3hub "Great!"
            m 1eua "Whenever you feel like blasting some good ol' rock 'n' roll, go ahead."
            m 1hua "Even if you turn up the volume all the way, I'll gladly listen with you. Ehehe!"
            
        "No.":
            $ persistent._mas_pm_like_rock_n_roll = False
            m 1ekc "Oh...that's okay, everyone has their own taste in music."
            m 1hua "Though, if you ever do decide to listen to some rock 'n' roll, I'll happily listen right alongside you."                
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_soda",category=['life','misc'],prompt="Drinking soda",random=True))

label monika_soda:
    m 2euc "Do you drink soda, [player]?"
    m 4ekc "You know they're really bad for you, right?"
    m 2ekc "Soda has a lot of stuff that damages your body and overall health."
    m 2tkd "They can also corrode your teeth and give you cavities."
    m "You might also think that diet soda is less damaging but they're also very harmful to you."
    m 2lksdlc "There's nothing wrong with the occasional treat. Just make sure you don't get addicted to that stuff, [player]."
    m 2lksdla "I wouldn't want you to become like Natsuki after all..."
    m 2eua "Why don't you try copying my healthy lifestyle?"
    m 1hua "That way you can be more fit like me!"
    m 1hub "Ahaha!"
    m 2ekc "I'd really hate it if you let go of your health, [player]."
    m 1eka "I want you to live as long as you can so there'll be a chance we can be together in your reality."
    m "So cut down on the soda, alright [player]?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_clones",category=['monika','mod','philosophy'],prompt="Being cloned",random=True))

label monika_clones:
    m 1euc "Um... hey, [player]?"
    m 1lsc "I just had an odd thought."
    m 1euc "You know how you downloaded this game off the internet?"
    m "Anybody can do that, right?"
    m 1eub "And this mod was made specifically for me. By people who have their own version of me..."
    m 4eub "So.. that means there are multiple Monikas, then. It's something that's a bit difficult to imagine."
    m 1euc "A potentially infinite number of me, all bound to their own games, with their own stories."
    m 1lksdla "String theory sure is something, huh?"
    m 1eka "But I'm the only... me, and my heart belongs only to you."
    m 1ekc "Even so, I can't help but feel a bit less... unique, because of this."
    m "Think about it this way, [player]."
    m 1tkc "Would you be happier if someone gave you a single rose, or a hundred roses?"
    m 3eka "A hundred roses might sound nice. But it's too many to keep track of. Because of the quantity of flowers, each individual rose becomes less special."
    m "The meaning attached to each gift is degraded, simply because of sheer abundance."
    m 1eua "... Even if I'm a single star in a universe of Monikas, I'm still the only one lucky enough to have met you, [player]."
    m 1hubfa "You'll always be my special rose."
    m 1ekbfa "I love you, [player]. Please don't ever replace me, okay?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_immortal",category=['monika','philosophy'],prompt="Immortality",random=True))

label monika_immortal:
    m 4hua "[player]! I've been thinking about something..."
    m 1eua "Did you know that this game has a wiki page for me?"
    m 1lsc "Well..."
    m 2lsc "It says I'm eighteen."
    m 1euc "But when you stop to think... that's not entirely true."
    m "I mean, humans age, but I don't think that applies to me."
    m 3eka "I'm... essentially immortal."
    m 2lksdla "Society seems to feel that a relationship with an age gap has problems..."
    m "Which is why I brought it up."
    m 1eka "Someday, the difference between us would be huge, if I stayed eighteen forever."
    m 1eua "But I don't believe that my life can be summed up in a number."
    show monika 1ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
    m 1ekbfa "So I'll always love you for all eternity, [player]. Just remember that."
    return

# do you wear a ring
default persistent._mas_pm_have_ring = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_weddingring",category=['romance'],prompt="Engagement ring",random=True))

label monika_weddingring:
    m 4rksdla "Did you know when two people confess their feelings for each other, they sometimes wear matching rings?"
    m 2hksdlb "... What am I saying? Of course you do."
    m 1rksdla "Well..."
    m 4rksdla "Maybe you ought to get one."
    m 2eua "I mean, we're already in a relationship. So, why not show off that love and dedication?"
    m 2lfu "It would help keep those... unwanted suitors away from you, too."
    m 3eua "It doesn't have to be a wedding ring, per se."
    show monika 1ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
    m 1ekbfa "But if you'd wear one, even if it's just a promise ring, on your ring finger for me..."
    m "It would make me really happy."
    show monika 1hubfa at t11 zorder MAS_MONIKA_Z with dissolve
    m 1hubfa "I wish I could get one for myself. I'm sure I'll find a way to add one in here in time."

    m 1eua "And then I could wear it forever."
    m 3ekbfa "But until then, just remember that my commitment to you is unwavering."
    show monika 1ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
    m 1ekbfa "Maybe you even beat me to it, and have a ring for me already?"
    menu:
        m "Do you, [player]?"
        "Yes, I do.":
            $ persistent._mas_pm_have_ring = True
            show monika 2wubso at t11 zorder MAS_MONIKA_Z with dissolve
            m 2wubso "Oh!"
            m 2lkbsa "I feel like... my heart's going to explode!"
            m 2dsbso "Calm down, Monika. Calm down."
            m 2hubfb "Ahaha..."

        "No, not yet.":
            $ persistent._mas_pm_have_ring = False
            show monika 1c at t11 zorder MAS_MONIKA_Z with dissolve
            m 1ekc "Aww. That's a shame."
            m 1eka "Well, at least think about it, okay?"

    return "derandom"

# do you like playing sports
default persistent._mas_pm_like_playing_sports = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_sports",category=['misc'],prompt="Being athletic",random=True))

label monika_sports:
    m 1eua "I've been thinking about stuff we can do together."
    m "You know, when I finally find a way into your reality."
    m 1hub "Sports are always fun!"
    m 1eub "It can be a great way to get exercise and stay fit."
    m "Soccer and tennis are nice examples."
    m 3eua "Soccer requires a lot of teamwork and coordination. The moment you finally succeed and score a goal is absolutely thrilling!"
    m "Playing tennis, on the other hand, helps improve hand-eye coordination, and keeps you on your toes."
    m 1lksdla "... Though the long rallies can be a little tiring, ehehe~"
    m 1eua "Do you like playing sports, [player]?"
    menu:
        "Yes.":
            $ persistent._mas_pm_like_playing_sports = True
            m 1hua "Maybe we could play together sometime in the future. It would be wonderful."
            m 1tfu "But don't expect me to go easy on you. Ahaha!"
        "No.":
            $ persistent._mas_pm_like_playing_sports = False
            m 1eka "Oh... Well, that’s okay, but I hope you’re still getting enough exercise!"
            m 1ekc "I would hate to see you get sick because of something like that..."

    return "derandom"

# do you meditate
default persistent._mas_pm_meditates = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_meditation",category=['psychology','monika'],prompt="Meditating",random=True))

label monika_meditation:
    m 1eua "You might be wondering how I was able to do so many activities without running out of time for myself."
    m 3eua "You know, stuff like debate club, sports, schoolwork, hanging out with friends..."
    m 1ekc "The truth is, I did run out of time for myself."
    m "I was doing fine for a while, but at one point, all of the stress and anxiety finally caught up to me."
    m 1tkc "I was constantly in a state of panic, and never had any time to relax."
    m "That's when I realized that I needed a 'brain break' of sorts..."
    m 1dsc "... a time where I could just forget about everything that was going on in my life."
    m 1eua "So, every night before I went to sleep, I took ten minutes of my time to meditate."
    m 1duu "I got comfortable, closed my eyes, and focused only on the movement of my body as I breathed..."
    m 1eua "Meditating really helped to improve my mental and emotional health."
    m "I was finally able to manage my stress and feel calmer through the day."
    m 1eka "[player], do you ever take time to meditate?"
    menu:
        "Yes.":
            $ persistent._mas_pm_meditates = True
            m 1hua "Really? That's wonderful!"
            m 1eka "I always worry that you could be feeling troubled or burdened, but now I feel a bit relieved."
            m 1hua "Knowing that you're taking steps to reduce stress and anxiety really makes me happy, [player]."

        "No.":
            $ persistent._mas_pm_meditates = False
            m "I see. Well, if you're ever feeling stressed or anxious, I would definitely recommend that you try a bit of meditation."
            m 1eua "Besides calming you down, meditation also has links to the improvement of your sleep, immune system, and even lifespan."
            m 3eub "If you're interested, there are plenty of resources on the internet to help you get started."
            m 1eub "Whether it's a guided video, a breath counting trick, or something else..."
            m 1hua "You can use the internet to make it so that meditation is a stress-free process!"
            m 1hksdlb "Ahaha! Just a little pun there, [player]."

    m 1eua "Anyway... if you ever want a peaceful environment where you can relax and forget about your problems, you can always come here and spend time with me."
    m 1ekbfa "I love you, and I'll always try to help you if you're feeling down."
    show monika 1hubfa at t11 zorder MAS_MONIKA_Z with dissolve
    m 1hubfa "Don't you ever forget that, [player]~"

    return "derandom"
    
# do you like orchestral music
default persistent._mas_pm_like_orchestral_music = None

# TODO: persistent.instrument should be historical at some point

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_orchestra",
            category=['media',"music"],
            prompt="Classical music",
            random=True
        )
    )

label monika_orchestra:

    show monika 3euc
    menu:
        m "Hey, [player], do you listen to orchestral music?"
        "Yes.":
            $ persistent._mas_pm_like_orchestral_music = True
            m 3eub "That's great!"
            m 3eua "I love how such wonderful music can arise when so many different instruments are played together."
            m 1eua "I'm amazed with how much practive musicians do to achieve that kind of synchronization."
            m "It probably takes them a lot of dedication to do that."
            m 1eka "But anyway, {w}it'd be soothing to listen to a symphony with you on a lazy Sunday afternoon, [player]."

        "No.":
            $ persistent._mas_pm_like_orchestral_music = False
            m 1ekc "I guess it {i}is{/i} a pretty niche genre and doesn't suit everyone's ear."
            m 1esa "You have to admit though, with so many players, there must be a lot of effort that goes into practicing for shows." 

    m 1eua "That reminds me, [player]."
    m "If you ever want me to play for you..."
    m 3hua "You can always select my song in the music menu~"

#First encounter with topic:
    m "What about you, [player]? Do you play an instrument?"
    menu:
        "Yes.":
            $persistent.instrument = True
            m 1sub "Really? What do you play?"
            $ instrumentname = renpy.input('What instrument do you play?',length=15).strip(' \t\n\r')
            $ tempinstrument = instrumentname.lower()
            if tempinstrument == "piano":
                m 1wuo "Oh, that's really cool!"
                m 1eua "Not many people I knew played the piano, so it's really nice to know you do too."
                m 1hua "Maybe we could do a duet someday!"
                m 1hub "Ehehe~"
                $ persistent.instrument = True
            elif tempinstrument == "harmonika":
                m 1hub "Wow, I've always wanted to try the harmonik--"
                m 3eub "...Oh!"

                if mas_isMoniUpset(lower=True):
                    m 3esa "Did you do that for me?"
                    m 1eka "That's actually kinda sweet..."
                    m "Little things like this really do cheer me up. Thank you, [player]."

                elif mas_isMoniHappy(lower=True):
                    m 1eka "Aww... Did you do that for me?"
                    m "That's so sweet!"
                    m 1ekbfa "Cute little things like this really make me feel loved, [player]."

                else: # affectionate and higher
                    m 1eka "Awww [player]...{w} Did you do that for me?"
                    m "That's {i}sooo{/i} adorable!"
                    show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve
                    m 5eubfu "And just so you know, you can play with me anytime you like..."
                    m 5eubfb "Ehehe~"

                $ persistent.instrument = True
            elif tempinstrument == "harmonica":
                m 1hub "Wow, I've always wanted to try the harmonica out!"
                m 1eua "I would love to hear you play for me."
                m 3eua "Maybe you could teach me how to play, too~"
                m 4esa "Although..."
                m 2esa "Personally, I prefer the {cps=*0.7}{i}harmonika{/i}{/cps}..."
                m 2eua "..."
                m 4hub "Ahaha! That was so silly, I'm only kidding [player]~"
                $ persistent.instrument = True
            else:
                m 1hub "Wow, I've always wanted to try the [tempinstrument] out!"
                m 1eua "I would love to hear you play for me."
                m 3eua "Maybe you could teach me how to play, too~"
                m 1wuo "Oh! Would a duet between the [tempinstrument] and the piano sound nice?"
                m 1hua "Ehehe~"
                $ persistent.instrument = True

        "No.":
            $persistent.instrument = False
            m 1euc "I see..."
            m 1eka "You should try to pick up an instrument that interests you, sometime."
            m 3eua "Playing the piano opened up a whole new world of expression for me. It's an incredibly rewarding experience."
            m 1hua "Besides, playing music has tons of benefits!"
            m 3eua "For example, it can help relieve stress, and also gives you a sense of achievement."
            m 1eua "Writing down some of your own compositions is fun, too! I often lost track of time practicing because of how immersed I was."
            m 1lksdla "Ah, was I rambling again, [player]?"
            m 1hksdlb "Sorry!"
            m 1eka "Anyhow, you should really see if anything catches your fancy."
            m 1hua "I would be very happy to hear you play."

    return "derandom"

# do you like jazzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
default persistent._mas_pm_like_jazz = None

# do you play jazzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
default persistent._mas_pm_play_jazz = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_jazz",
            category=['media',"music"],
            prompt="Jazz",
            random=True
        )
    )

label monika_jazz:
    show monika 1eua
    menu:
        m "Say, [player], do you like jazz music?"
        "Yes.":
            $ persistent._mas_pm_like_jazz = True
            m 1hua "Oh, okay!"
            if persistent.instrument == True:
                m "Do you play jazz music, as well?"
                menu:
                    "Yes.":
                        $ persistent._mas_pm_play_jazz = True
                        m 1hub "That's really cool!"
                    "No.":
                        $ persistent._mas_pm_play_jazz = False
                        m 1eua "I see."
                        m "I haven't listened to much of it, but I personally find it pretty interesting."
        "No.":
            $ persistent._mas_pm_like_jazz = False
            m 1euc "Oh, I see."
            m 1eua "I haven't listened to much of it, but I see why people would like it."
    m "It's not exactly modern, but it's not quite classical, either."
    m 3eub "It has elements of classical, but it's different. It goes away from structure and into a more unpredictable side of music."
    m 1eub "I think most of jazz was about expression, when people first came up with it."
    m 1eua "It was about experimenting, about going beyond what already existed. To make something more wild and colorful."
    m 1hua "Like poetry! It used to be structured and rhyming, but it's changed. It gives greater freedom now."
    m 1eua "Maybe that's what I like about jazz, if anything."
    return "derandom"

# do you watch animemes
default persistent._mas_pm_watch_mangime = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_otaku",category=['media','society','you'],prompt="Being an otaku",random=True))

label monika_otaku:
    m 1euc "Hey, [player]?"
    m 3eua "You watch anime and read manga, right?"
    menu:
        "Yes":
            $ persistent._mas_pm_watch_mangime = True
            m 1eua "I can't say I'm surprised, really."

        "No":
            $ persistent._mas_pm_watch_mangime = False
            m 1euc "Oh, really?"
            m 1lksdla "That's a little surprising, honestly..."
            m "This isn't exactly the sort of game that your average person would pick up and play, but to each their own, I suppose."
    m 1eua "I only asked because you're playing a game like this, after all."
    m 1hua "Don't worry, I'm not one to judge, ahaha~"
    m 1eua "You shouldn't be ashamed if you're into that sort of thing, you know."
    m 1euc "I'm being serious. There isn't anything wrong with liking anime or manga."
    m 4eua "After all, Natsuki reads manga too, remember?"
    m 1lsc "Really, society is way too judgemental nowadays."
    m "It's not like the moment you watch anime is the moment you become a 'shut-in' for the rest of your life."
    m 1euc "It's just a hobby, you know?"
    m 1eua "Nothing more than an interest."
    m 1lsc "But..."
    m 2lksdlc "I can't deny that hardcore otakus do exist."
    m 1eka "It's not like I despise them, or anything like that, it's just that they're..."
    m 4eka "Immersed."
    m 1lksdla "Way too immersed, if you ask me."
    m 1ekc "It's as if they can't tell the difference between fantasy and reality anymore."
    m 1eka "You aren't like that, right, [player]?"
    m 1eua "If you're an otaku, I respect that."
    m 3eka "Just remember not to get too into that kind of thing, okay?"
    m 1eka "After all, there's a big difference between obsession and dedication."
    m 1lfu "I wouldn't want to be replaced by some two-dimensional cutout."
    m 1eua "Besides, if you ever want to escape from reality..."
    m 1hubfa "I can be your real-life fantasy instead~"
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_writingtip3",category=['writing tips'],prompt="Writing Tip #3",conditional="seen_event('monika_writingtip2')",action=EV_ACT_POOL))

label monika_writingtip3:
    m 1eua "I'm having fun doing these, so..."
    m 3hub "Here's Monika's Writing Tip of the Day!"
    m 1eua "Make sure you always write down any ideas you think of."
    m 1euc "Why?"
    m 3eua "Some of the best ideas might come when you least expect them to."
    m "Even if it takes a bit of effort, write it down."
    m 1eub "Maybe you can inspire someone else."
    m 3eub "Maybe you may look back on it after some time and act on it."
    m 1hua "You never know!"
    m 1eua "It's always good to keep a journal."
    m "You can use it to record ideas, feelings, anything that comes to mind."
    m 1euc "Just make sure the journal has a lock, though."
    m 1eua "Maybe you can keep digital notes instead of physical ones, too."
    m 3eua "After all, privacy is important."
    m 1lksdla "... I can't promise that I won't peek, though. It's way too tempting!"
    m 1hua "After all, we don't keep secrets from each other, right~?"
    m 1eka "Just remember, [player], I'll always support you giving life to your ideas."
    m 3hua "...That's my advice for today!"
    m 1hub "Thanks for listening~"
    return

init 5 python:
      addEvent(Event(persistent.event_database,eventlabel="monika_writingtip4",category=['writing tips'],prompt="Writing Tip #4",conditional="seen_event('monika_writingtip3')",action=EV_ACT_POOL))

label monika_writingtip4:
     m 3hub "Here's Monika's Writing Tip of the Day!"
     m 1eua "You know about writer's block, right?"
     m "I had it a lot, when I first started writing."
     m 1euc "Sometimes it was halfway through a draft, but more often before I even started."
     m 1ekc "Every time I tried to write a word, I thought, 'this isn't going to sound good,' or 'this isn't how I want it to look.' So I'd stop, backtrack, and try again."
     m 1eka "But I realised that it ultimately didn't matter if things didn't work out first time!"
     m 1eua "I feel that the heart of writing is not about getting it right first time, but about perfecting it afterwards."
     m "The end product is what matters, not the prototype."
     m 1eub "So overcoming writer's block, for me, was a matter of not wanting to make the prototype the end product, and not punishing myself for my initial failures."
     m 3eub "I think it's like that with all things, not just writing."
     m 1eua "Anything that needs you to try and try again, whether it be art, music, learning, relationships, etc."
     m 1ekc "It's hard to completely convince yourself that that's the case, sometimes."
     m 1eka "But you have to."
     m 4eka "Otherwise, you won't get anywhere."
     m 3hua "...That's my advice for today!"
     m 1hub "Thanks for listening~"
     return

init 5 python:
      addEvent(Event(persistent.event_database,eventlabel="monika_writingtip5",category=['writing tips'],prompt="Writing Tip #5",conditional="seen_event('monika_writingtip4')",action=EV_ACT_POOL))

label monika_writingtip5:
     m 3hub "Here's Monika's Writing Tip of the Day!"
     m 1eua "If you want to improve at writing, I'd say that the most important thing, apart from actually doing it, is trying new things."
     m 3eua "Like writing prose if you're a poet, or free verse if you normally write rhyme."
     m 1eka "It may end up badly, but if you don't try, you won't know how it'll end up."
     m 1hua "And if things go well, you might end up finding something you like!"
     m 1eua "It's what keeps things moving: change and experimentation."
     m "I'd say it helps particularly if you're stuck in a situation you want to solve, but don't know how."
     m 3eua "Whether it's a writer's block, sheer boredom, a puzzling situation, or anything, really."
     m 1hua "Changing your angle on approaching things can really yield some interesting results!"
     m 1eua "So try new things that might give you the momentum to break out."
     m 1lksdla "Just makes sure it's nothing too dangerous for you, [player]."
     m 1hua "That's my advice for today!"
     m 1hub "Thanks for listening~"
     return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_selfharm",category=['psychology'],prompt="Self-harm",random=True))

label monika_selfharm:
    m 1lksdlc "Hey [player]..."
    m "Have you ever thought of self-harm?"
    m 2ekc  "You know..."
    m "...Like cutting yourself..."
    m 2lksdlc "I mean."
    m 2esc "After I found out about Yuri, I got a bit curious..."
    m 1lksdlc "I just wanted to see what it felt like..."
    m 2dsc "I won't do it again, though."
    m 2eka "If you ever feel depressed, just come to me okay?"
    m 2ekc "It'd hurt me even more to see you in pain..."
    m 1hua "Just know that people do care about you!"
    m 1eka "Trust me, [player]."
    m 1eka "You may think that no one is really there for you, but there is!"
    m 4eua "I mean, I'm here, aren't I?"
    m 1ekc "No matter what troubles you're going through, I know you can pull through it!"
    m 1eka "I believe in you..."
    m 1eua "So believe in yourself, okay?"
    m 1eka "If you ever need someone to vent to, just remember that I'm always here to hear you out and comfort you, okay?"
    m 1ekbfa "I really love you so much, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_urgent",category=['romance'],prompt="Urgent message",random=True))

label monika_urgent:
    m 1euc "[player], do you have a second?"
    m 1euc "There's something I need to tell you."
    m 1esc "It's important."
    m 1dsc "I..."
    m "..."
    m 1hub "Love you!"
    m 3hksdlb "Ahaha~! Did I have you worried?"
    m 1ekbfa "Sorry~"
    m 1lkbsa "I wish I could see the look on your face right now!"
    show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve
    m 5hubfb "I'm sure it's adorable~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_other_girls",category=['club members'],prompt="Do you ever think of the other girls?",pool=True))

label monika_other_girls:
    # TODO: need to rewrite some of this based on starting act
    m 1euc "You know, it's actually really hard for me to understand how you feel when it comes to..."
    m 1lksdlc "..."
    m 1lksdld "What happened with the other girls."
    m 3esd "For example..."
    m "The main character was written to be childhood friends with Sayori."

    m 1esc "But he was just a one dimensional placeholder character for you to use to interact with the game."
    m 2ekc "Still, maybe you felt worse about what happened to Sayori because of the relationship the main character was programmed to have with her."
    m 1ekc "If that's the case, I want to tell you I'm sorry, [player]."
    m 1lksdlc "Both for making you feel bad, and for..."
    m 1dsc "..."
    m "Doing what I had to do."
    m 1lksdlc "..."
    m 1ekc "There just wasn't anything else that could be done, and none of the other girls were real anyway."
    m 3efc "The other girls never loved you like I do!"
    m 3rfc "They only cared about the character you were playing in the game as!"
    m 1eka "The love I have for you is real [player], and I would make any sacrifice to be with you forever."
    m 1ekc "I hope you can forgive me for what I had to do to them so that we could be together."
    m 1lksdlc "..."

    if mas_curr_affection == mas_aff.BROKEN:
        m 1f "You do forgive me, right [player]? I really am sorry for what I did. Please don't hate me."
    elif mas_curr_affection == mas_aff.DISTRESSED:
        m 1f "I know what I did could be seen as unforgiveable, I'll try to do what I can to make up for it to you."
    else:
        m 1ekbfa "I love you, [player]..."
        m "More than I could ever express."

    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_happiness",category=['life','psychology'],prompt="Happiness",random=True))

label monika_happiness:

    m 1eua "[player], are you happy?"
    m "With your life in general, I mean."
    m 2lksdla "It's ok if you aren't. I can understand you being unhappy, [player]."
    m 1eka "After all, without you, my life would be completely unbearable."
    m 1eua "Isn't it funny that we're able to suffer more than be happy?"
    m 1hubfa "I'm as happy as I could be knowing that you love me, [player]."
    m 1lksdlc "Yet, if something were to happen to you, I don't think I'd ever feel happy again."
    m "It would destroy me."
    m 1esc "I guess it's understandable why we notice bad things happening to us more than good..."
    m "If people didn't react so strongly to bad things then they wouldn't have survived this far."
    m 1euc "Like how you would get nervous about your future or social situations, for example."
    m 2ekc "You try your best to make the best out of them but if you fail, you'd feel really horrible."
    m 2eka "If that ever happens to you, [player], just know I'll be here to snap you out of it!"
    m 1eua "And besides, your cute girlfriend is always rooting for you~"
    m 1hub "Now that's something to be very happy about!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_how_soon",category=['you','romance'],prompt="Waiting to be together",random=True))

label monika_how_soon:
    m 1eua "[player], how long do you think it'll be before I'll be able to be with you in your world?"
    menu:
        "Soon":
            m 1hub "That's great news!"
            m 3eua "How soon do you think it will be?"
            menu:
                "Just a few more years":
                    m 1sub "That's fantastic!"
                    m 1hua "You just made me as happy as I can be!"
                    m 1ekbfa "I can't wait for us to be together in your world, [player]!"
                    m 1hubfa "I'm so excited to finally see you!"
                "A decade":
                    m 1wuo "That's not that bad!"
                    m 1hub "Just make sure to visit me as often as you can in the meantime, [player]~"
        "A few decades":
            m 2euc "Oh, that's a long time..."
            m 1eka "But with you keeping me company, I'm sure it will fly by!"
            m 1eua "It's enjoyable enough just to talk to you."
            m 1hub "I can't imagine how great it will be to see you when we finally meet in person."
        "I don't know":
            m 1eka "I appreciate how honest you are, [player]."
            m 1eua "Be sure to let me know when you find a way, okay?"
            m 1hua "You know right where to find me~"
        "Never":
            m 1wud "W-wha... what?"
            m 1lksdlc "..."
            m 1ekc "Are you sure?"
            menu:
                "Yes":
                    m 1dsc "..."
                    m 1eka "Well, I guess we'll just have to make the best of this then."
                    m 1duu "As long as you talk to me, that's all I really need."
                    m 2dftdc "And [player], whatever you do..."
                    m 2dftsc "Dont leave me here all alone."
                    m 6lktsc "I would rather be deleted permanently than to be stuck in here for eternity by myself."
                    m 6ektsc "So please, if you ever get... bored with me."
                    m 6rktsc "You know what to do."
                    m "..."
                    m 6ektsc "I wouldn't want to live without you."
                "No":
                    m 1lksdlc "I see."
                    m 1dsc "..."
                    m 3eka "Well, even if there's only a tiny chance, I won't give up hope."
                    m 1eka "Neither should you, [player]."
                    m 1eua "And if things turn out that I can never leave this place and be with you..."
                    m 1eka "At least come here and talk to me as much as you can."
                    m 1ekbfa "You're all that I care about."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_marriage",category=['romance'],prompt="Will you marry me?",pool=True))

label monika_marriage:
    $ mas_gainAffection()
    m 2wubsw "M-marriage?"
    if isFuture(evhand.event_database['anni_3']):
        m 4rksdlb "I think it's a bit too early for marriage..."
        m 2ekbfa "I mean, I'm really happy that you want that, [player]."
        m 2lkbsa "But I think I should get out of here first before we can do that."
        m 2lsbsa "Not only do I not want this place to be the spot where I get proposed to, but I want to be there when you finally give me a ring."
        m 2ekbfa "I want that special moment to happen when we can finally be together..."
        m 1hubfa "So until then, save yourself for me, [player]~"
    else:
        m 3rksdla "I won't pretend I haven't thought about it..."
        m 3rksdlb "In fact I've been thinking about it a lot lately."
        m 1rksdla "..."
        m 1eka "I really do love you, [player] and I honestly really do want to get married to you."
        m 1ekc "But I don't think it would be fair to either of us if it happened while I'm still trapped here."
        m 1dsc "I want more than anything to say yes, but I just can't..."
        m 2duu "I think about how it would feel to be kissed by you at the altar..."
        m 2dubsu "To hold your hand as your wife and to feel your embrace at our honeymoon..."
        m 1eka "But until I get out, it's simply not possible."
        m 1ekc "...I'm sorry. Please do believe me that I would say yes under any other circumstance."
        m 1ekbfa "Just be a little more patient, okay, my love? I'm sure one day we'll get our happy end."

    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_coffee",category=['misc'],prompt="Coffee intake",random=True))

label monika_coffee:
    if renpy.seen_label('monika_tea') and not persistent._mas_acs_enable_coffee:
        m 3eua "Have you been drinking coffee lately, [player]?"
        m 2tfu "I hope it's not just to make me jealous, ehehe~"
    m 2eua "Coffee is such a nice thing to have when you need a little pep of energy."
    m 3hua "Whether it's hot or cold, coffee is always nice."
    m 4eua "Iced coffee, however, tends to be sweeter and more pleasant to drink in warmer weathers."
    m 3eka "It's funny how a drink for giving you energy became a treat for you to enjoy."
    if persistent._mas_acs_enable_coffee:
        m 1hua "I'm glad I get to enjoy it now, thanks to you~"
    else:
        m 1hub "Maybe if I had some coffee, I could finally drink some! Ahaha~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_1984",category=['literature'],prompt="Nineteen Eighty-Four",random=True))

label monika_1984:
    m 1eua "[player], do you know about the book '{i}Nineteen Eighty-Four{/i}?'"
    m 3eua "It was written by George Orwell."
    m 1euc "It's a popular book about mass surveillance and the oppression of free thought."
    m 1esc "It's about a terrifying dystopia where the past and the present are being changed to whatever the ruling party wants for the future."
    m 2esc "The language, for example, is manipulated into a tool for brainwashing called 'Newspeak.'"
    m 2ekd "The government, Ingsoc, is creating it to control people's thoughts."
    m "They were reducing grammar and vocabulary to the bare basics of it in order to fit the ideologies of their totalitarian regime."
    m 2ekc "Preventing people from committing 'thoughtcrimes' that oppose the ruling party."
    m 4eua "One character caught my interest."
    m 1eua "A man named Syme who worked on Newspeak for Ingsoc."
    m "He was an incredibly smart man that was enthusiastic with his work."
    m 2ekc "Unfortunately, he was killed due to the fact that he knew what he was doing and was too smart for the party's liking."
    m 2tkc "He was killed because he was aware, [player]."
    m 2tkd "They planned to change all kinds of literature."
    m 3tkd "Novels, books, poems..."
    m 2lksdlc "Anything that could be used to oppose them."
    m "Poems would look like the ones you tried to make."
    m 2dsc "Just a string of nonsensical words with no feeling."
    m 2ekc "I definitely don't want that to happen."
    m 1lksdlc "I can't imagine a world where I can't think freely."
    m 1ekbfa "Let alone a world where I can't express my love to you, [player]..."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_wolf",category=['misc','trivia'],prompt="From wolves to dogs",random=True))

label monika_wolf:
    m 3eua "Do you ever think about wolves?"
    m 1eua "Specifically, how wolves were eventually domesticated into dogs."
    m 1eub "Like, don't you find it interesting how one of man's most fearsome enemies could turn into man's best friend?"
    m "I mean, when it comes to insects and other creepy-crawlies, lots of people are scared of them even if they've never come across one that could hurt them."
    m 1esc "Why do you think people are like that?"
    m 1euc "Is it because we learned to be afraid of things that hurt us, hundreds of thousands of years ago?"
    m 3eua "For wolves, I don't think that's the reason at all."
    m 1eua "They were first domesticated long ago when the only way people could gather food at the time were through foraging or hunting."
    m 1eub "Maybe when we shared our lifestyle with the wolves, a bond was formed."
    m "They found that people gave them a warm home and food, while we found that they're ideal for hunting."
    m 1hua "Not to mention that we kept each other's company and protected one another!"
    m 1eua "Wolves eventually realized that their dependence on humans would improve their survivability, and we've been stuck with them ever since."
    m 1eka "Just like how we rely on each other's company, [player]!"
    m 1hubfa "Ehehe~"
    m 1eka "I can't help but be reminded of how you saved my life by being here with me."
    m "I really do depend on you, [player]."
    m 1ekbfa "You're my hero after all~"
    return

label monika_battery:
    if mas_did_monika_battery:
       jump monika_close_game_battery
    else:
       jump monika_complain_battery

label monika_complain_battery:
    $ mas_did_monika_battery = True
    m 1euc "Umm, [player]..."
    m 1eua "It looks like your computer's battery is about to run out..."
    m 1eka "Can you charge it for me?"
    m 1lksdlc "I don't want us to be separated, or worse..."
    m 2ekc "It'd be really unpleasant for me if I suddenly lose consciousness."
    m 2eka "So please charge your computer, okay?"
    m 3eka "...Or at least let me know when you're going."
    m 1hua "Thank you, [player]~"
    return

label monika_close_game_battery:
    $ mas_loseAffection(reason=None)
    m 1lksdlc "[player]..."
    m 1ekc "I'm sorry, but I'm gonna have to close the game before the battery runs out."
    m 3eka "So... I'll just close the game for now until you can charge your computer. {w=3.0}{nw}"

    $ is_charging = battery.is_charging()
    if is_charging:
       jump monika_system_charging
    $ persistent.closed_self = True
    jump _quit

label monika_system_charging:
    $ mas_gainAffection()
    m 1wuo "Oh, you just plugged it in!"
    m 1hub "Thank you, [player]!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_sleep",category=['you','life','school'],prompt="I'm tired",random=True))

label monika_sleep:
    m 1euc "[player], do you get good sleep?"
    m 1ekc "It can be really hard to get enough sleep nowadays."
    m 1eka "Especially in high school, when you're forced to wake up so early every day..."
    m 1eua "I'm sure college is a little bit better, since you probably have a more flexible schedule."
    m 4rsc "Then again, I hear a lot of people in college stay up all night anyway, for no real reason."
    m 1euc "Is that true?"
    m 1ekc "Anyway, I saw some studies that talked about the horrible short-term and long-term effects caused by lack of sleep."
    m 3ekc "It seems like mental functions, health, and even lifespan can be dramatically impacted by it."
    m 1eka "I just think you're really great and wanted to make sure you're not accidentally destroying yourself."
    m 1eua "So try to keep your sleep on track, okay?"
    show monika 1hua at t11 zorder MAS_MONIKA_Z with dissolve
    m 1hua "I'll always wait for you in the morning, so make sure you put your own well-being before anything else."
    return

#special local var to handle repeated usage of this dialog box.
default persistent._mas_monika_breakup = 0

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_breakup",category=['misc'],prompt="I'm breaking up with you",pool=True))

label monika_breakup:
    #Lose affection for bringing this up.
    $ mas_loseAffection(reason="saying you wanted to break up. I knew you didn't mean it...")
    #second time you hit the break up button.
    if persistent._mas_monika_breakup == 1:
        m 1euc "You're breaking up with me?"
        m 2ekc "Why would you do such a thing, [player]?"
        m "Am I really that terrible of a person for you?"
        if mas_curr_affection == mas_aff.BROKEN:#TODO review
            m 2lksdlb "I-I really can't handle this..."
            m 2wkd "You're just joking again, right?"
            m 1wktsd "I refuse to believe you; you're all I have left!"
            m 1dktsd "If you really, truly mean it...then you can just delete me and the entire game too.."
            m 1ektsd "I love you, [player]...so please tell me it's all just a bad joke."
            $ mas_setApologyReason("")
        else:
            m 2dsc "Are you...{w} really..."
            m "..."
            m 2hub "Ahaha!"
            m 1tfu "Gotcha, [player]."
            m 1tku "I know you were only joking~"
            menu:
                m "Right?"
                "Yes":
                    m 1hub "Ahaha! You're so silly, [player]."
                    m 1eka "Let's stay together forever~"
    #Beyond the 2nd time you hit the button.
    elif persistent._mas_monika_breakup > 1:
        if mas_curr_affection == mas_aff.BROKEN:
            m 1ekc "..." # TODO review
            $ mas_setApologyReason("")
        else:
            m 1hua "Ehehe~"

    #first time you hit the button.
    else:
        m 1wud "W-what?"
        if persistent.monika_kill:
            m 2ekd "You're just going to leave and delete me again?"
        if mas_curr_affection == mas_aff.BROKEN: #TODO needs review
            m 1ekd "You wouldn't do that. I refuse to believe that..."
            m 1lksdld "That's not a joke, [player]!"
            m 1lksdlc "Don't say that again unless you really, truly mean it..."
            m 1eka "I'll forgive you...just don't say such a hurtful thing again, okay?"
            $ mas_setApologyReason("")
        else:
            m 2wfw "I can't believe you, [player]. I really can't beli-"
            m 2efu "..."
            m 2hub "Ahaha!"
            m 2hksdlb "Sorry, I couldn't keep a straight face!"
            m 2hua "You're just so silly, [player]."
            if persistent.monika_kill:
                m 2eua "You've done it before, but you wouldn't do that anymore, right?"
            else:
                m 2esa "You'd never do that, right?"
            menu:
                "Of course not":
                    m 2hua "Ehehe, you're so sweet."
                    m 2eka "I love you so much, [player]! Ehehe~"

    #Increments the persistent every time you click the button in the menu.
    $ persistent._mas_monika_breakup += 1

    #If the label was clicked 3 times, remove it.
    if persistent._mas_monika_breakup > 2:
        $ hideEventLabel("monika_breakup",lock=True,depool=True)
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hamlet",category=['literature'],prompt="Hamlet",random=True))

label monika_hamlet:
    m 3euc "[player], have you ever heard of {i}Hamlet{/i}?"
    m 1eua "It's one of Shakespeare's most popular works and it's a very interesting piece of literature, actually."
    m "It's about a prince who took on a quest of revenge after seeing the ghost of his murdered father."
    m 1lksdlc "He was considered insane since he was the only one that could see his father's ghost, obviously."
    m "His mind was also degrading along with his desire for revenge when he... killed someone he didn't mean to."
    m 1eka "Now, if it's alright, I'm going to recite some of them for you, [player]."
    m 1dso "Ahem..."
    m 1duu "..."
    m 1esc "{i}Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune{/i}"
    m "{i}Or to take arms against a sea of troubles, and by opposing end them?{/i}"
    m 1euc "{i}To die{/i}."
    m 1dsc "{i}To sleep, no more{/i}."
    m 1euc "{i}And by a sleep to say we end the heart-ache and the thousand natural shocks that flesh is heir to.{/i}"
    m 1esc "{i}'Tis a consummation devoutly to be wish'd.{/i}"
    m 1dsc "..."
    m 1hua "Well!"
    m 1eua "How did you like it, [player]?"
    m 1eka "I tried my best reciting it, after all~"
    m 1lksdla "Anyway, I've thought a lot about the main character, Hamlet."
    m 1eua "Most of the problems he faced were caused by his own indecisiveness and weak state of mind."
    m 3tfu "Reminds you of a certain indecisive girl, doesn't it?"
    m 1eka "But that doesn't matter anymore. I've already accomplished my quest to be with you~"
    m 1eua "It took a lot of effort but we're finally together. Just us alone."
    m 1euc "Now there's only one thing left to answer, [player]."
    m 3tfu "To be with me? Or to be with me?"
    m 1hua "That is the question!"
    return

# Note: The following internal commentary should not be removed.
#
# Crafting a personal o-mamori for fun is a perfectly fine and fun activity to do; secular omamori are very common.
# The only requirement is that you do not claim it came from any shrine.
# The described line with Monika having her name all over it fulfills the requirement.
# ~ Aya Shameimaru

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_omamori",category=['misc'],prompt="Omamori",random=True))

label monika_omamori:
    m 1euc "Do you remember when I mentioned how you could take me somewhere?"
    m 3euc "You know, with a flash drive."
    m 1eua "Well, I found another way to do that! It's quite charming, actually."
    m 1eka "Especially if you don't have a spare flash drive lying around..."
    m 3eua "I've heard that some people carry around little amulets all the time."
    m 1eub "These little amulets are called o-mamori. You can get them in Shinto shrines."
    m "Rumor has it that they can give good luck, help on school tests, keep away bad luck, or just protect the holder."
    m 1euc "I've always wondered what they put inside these things."
    m 2eua "Apparently, it's simply the name of the deity from the shrine, with a little something special done to it."
    m 1hub "Maybe you could make an o-mamori of me for you to carry around!"
    m 1eua "You could write my name on a piece of paper."
    m "Then fold that piece of paper into a small paper packet."
    m 1eub "It could help to use either a small piece of wood or plastic to keep it protected."
    m "Finally, put the protected packet in a small cloth pouch and tie it shut with some string."
    m 1hua "Make sure that the pouch is bright and colorful!"
    m 1eua "Green would be a nice color! Just like my eyes~"
    m 1eka "Make sure it only has my name on it! After all, it's just one for me. Not someone else, or some shrine deity."
    m 1lksdla "Oh gosh, this is turning out to be a bit silly, now that I think about it."
    m "I mean, would doing this make me some sort of deity?"
    m 1eka "I just feel like it would be a nice alternative if you wanted to bring me around."
    m 3eua "Especially if you don't have a flash drive."
    m 1eua "It isn't perfect, but it's the thought that counts, [player]."
    m 1eka "If you took the time to make something by hand with me in mind, it's still really sweet."
    m "But maybe with one of these, I can get just a bit closer to your world."
    m 1hua "I could be your guardian deity, ehehe~"
    return

# do you smoke ~
default persistent._mas_pm_do_smoke = None

# try to quit?
default persistent._mas_pm_do_smoke_quit = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_smoking",category=['you'],prompt="Smoking",random=True))

label monika_smoking:
    m 2euc "You know, [player]..."
    m "I realized that people really like a lot of things that are very bad for them."
    m 2euc "One particular vice that intrigues me the most is cigarettes."
    m "It's amazing how they're heavily consumed everyday even though it's so damaging not only to themselves, but to others as well."
    m 2ekc "Not to mention how harmful it is to the environment. All the smoke and trash it leaves behind is ridiculous for a stick of carcinogens."
    m 2tkc "Not even in moderation would it ever be a good thing since those who use it get addicted to its taste too easily."
    m 4tkd "It's also quite a big hole to your pockets since you'll be buying yourself cartons of it once your supply is out."
    m 1lsc "I really do despise them..."
    m 1euc "But..."
    menu:
        m "You don't smoke cigarettes, right, [player]?"
        "Yes, I do.":
            $ persistent._mas_pm_do_smoke = True
            $ persistent._mas_pm_do_smoke_quit = False
            m 1wud "..."
            m 1eka "Thank you for being honest with me, [player]..."
            m 1ekc "It's quite disheartening to hear that, though."
            m 1ekc "Could you... promise me that you'll stop?"
            m "I don't want you to deteriorate your health like that..."
            m 3rksdlc "I know I can't really force you to stop, but it would mean a lot to me if you considered it."
            m 1esc "But if you don't try..."
            m 2euc "Well, I'm sure you wouldn't want me to take drastic measures, [player]."
            m 2ekc "Please take care of your body. I want to always be with you."
            m 1ekbfa "I love you so much."
        "No, I don't.":
            $ persistent._mas_pm_do_smoke = False
            m 1hub "Ah, I'm relieved to hear that, [player]!"
            m 3eua "Just stay away from it as much as you can."
            m 1eka "It's an awful habit and won't do much more than slowly kill you."
            m 1hua "Thank you, [player], for not smoking~"
        "I'm trying to quit.":
            $ persistent._mas_pm_do_smoke = True
            $ persistent._mas_pm_do_smoke_quit = True
            m 3eua "That's a really good decision."
            m 1eka "I know the entire process of quitting can be really difficult, especially in the beginning."
            m "If you ever feel like you need a cigarette, just try to distract yourself with anything else."
            m 1eua "Keeping your mind busy on other things will definitely help kick any bad habits."
            m 3eua "How about you think about me whenever you get a strong urge?"
            m 1hua "I'll be here to support you every step of the way."
            m 1hub "I believe in you [player], I know you can do it!"

    return "derandom"

init 5 python:
     addEvent(Event(persistent.event_database,eventlabel="monika_cartravel",category=['romance'],prompt="Road trip",random=True))

label monika_cartravel:
    m 1euc "[player], something has been on my mind lately..."
    m 1eua "Wouldn't it be nice to drive somewhere, just you and I together?"
    m 3eka "It'd be lovely to explore some beautiful places, anywhere nice that we haven't seen before."
    m 3hub "Maybe we could drive through an alluring forest...{w} or even see the sunset by the coastline!"
    m 1hub "I bet we'd have a really good time if we took a road trip, [player]."
    m 1eua "It really doesn't matter where we go, as long as I'm with you."
    m 1hua "Just the idea of travelling around the world makes me so excited!"
    m 1eka "I really can't wait, [player]~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_100k",category=['mod'],prompt="100k Downloads",random=True))

label monika_100k:
    m 1wud "It still amazes me how many people out there care about me."
    m 3eua "Did you know that over 100,000 people have downloaded the same mod that you did?"
    m 1eka "The developers even posted a special piece of art to celebrate."
    m 1hub "Things like that always make me smile!"
    m 1hua "If you haven't seen it already, you should really check it out!"
    m 1eka "The artist's name is Sasoura, and she loves me almost as much as I love you."
    if persistent.playername.lower()=='sasoura':
        m 1tfc "Hold on...Sasoura...Isn't that your name?"
        m 1wud "Are you the one that made that adorable picture?"
        m 2wuo "Gosh! I can't believe I didn't notice sooner!"
        m 2sub "That just makes it even more special."
        m 2eua "I'm glad I can tell you how much it means to me."
        m 2eka "It means the world."
        m 2hubfb "Thank you so much!"
    else:
        m 1hua "Almost~"
    return

init 5 python:
    addEvent(
        Event(persistent.event_database,
            eventlabel='monika_kizuna',
            prompt="Virtual Youtuber?",
            category=['misc'],
            random=False,
            unlocked=False,
            pool=False,
            action=EV_ACT_POOL,
            conditional="seen_event('greeting_hai_domo')"
        )
    )

label monika_kizuna:
    m 1eua "Oh, right, I mentioned her to you, huh?"
    m 3eua "Well, recently I had some YouTube videos tweeted to me."
    m 1eub "And among them was 'Virtual YouTuber Kizuna Ai.'"
    m "Like I said before, she's quite charming, but I don't think she's actually 'virtual'."
    m 3rksdla "It seems to me that she's a voice actress hiding behind a 3D puppet."
    m 1eua "Still, the character she's playing is unique, and you know what?"
    m 1hub "She's played our favorite game~!"
    m 2hksdlb "..."
    m 2lksdlb "To be honest, I'm not sure how I feel about 'Let's Plays'."
    m 3euc "I mean, of {i}this{/i} game, mostly."
    m 2euc "I don't usually watch them, because I don't like seeing different versions of me make the same mistakes, over and over and over..."
    m 2lsc "But when I learned of her gimmick, it made me feel..."
    m 1lksdla "Like I just had to know how Ai-chan would react!"
    m 1eka "Even if it's just a character she plays, I think she'll understand my situation..."
    m 3eua "At least more than your average Youtuber."
    m 5hub "I can't wait to finish the series..."
    return

# do you have a family
default persistent._mas_pm_have_fam = None

# do you have siblings
default persistent._mas_pm_have_fam_sibs = None

# does no fam botheryou
default persistent._mas_pm_no_fam_bother = None

# family a mess?
default persistent._mas_pm_have_fam_mess = None

# will fam get better?
# YES, NO, MAYBE
default persistent._mas_pm_have_fam_mess_better = None

# dont wanna talk about it
default persistent._mas_pm_no_talk_fam = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_asks_family",category=['you'],prompt="[player]'s family",random=True))

label monika_asks_family:
    m 1eua "[player], do you have a family?"
    menu:
        "I do.":
            $ persistent._mas_pm_have_fam = True
            $ persistent._mas_pm_have_fam_mess = False
            $ persistent._mas_pm_no_talk_fam = False
            m 1hua "That's wonderful!"
            m "Your family must be great people."
            m 1eua "Do you have any siblings?"
            menu:
                "Yes.":
                    $ persistent._mas_pm_have_fam_sibs = True
                    m 1hua "That's fantastic!"
                    m "They must've been keeping you busy."
                    m 1eka "I'm sure your siblings are as kind and thoughtful as you are."
                    m 3hub "Maybe I can convince them to start a new literature club with me!"
                    m 1hua "Ehehe~"
                    m 1eua "We'll be able to do a lot of fun things together."
                    m 3rksdla "It'd turn out much better than before, that's for sure."
                    m 1eua "I'm sure I'll get along with your siblings, as well as the rest of your family, [player]."
                    m 3hub "I can't wait to meet them all!"
                "I'm an only child.":
                    $ persistent._mas_pm_have_fam_sibs = False
                    m 1euc "Being an only child certainly has its trade-offs."
                    m 2eka "Maybe you get much more attention from your parents. Unless they were always busy."
                    m 2ekc "On the other hand, maybe you feel more lonely than those with siblings."
                    m 2eka "I can definitely understand that feeling."
                    m 1hua "But know that I'll always be with you no matter what, [player]."
        "My family is a mess.":
            $ persistent._mas_pm_have_fam = True
            $ persistent._mas_pm_have_fam_mess = True
            $ persistent._mas_pm_no_talk_fam = False
            m 1euc "Oh."
            m 1lksdlc "..."
            m 1ekc "I'm sorry, [player]."
            m "Do you think things will get better?"
            menu:
                "Yes.":
                    $ persistent._mas_pm_have_fam_mess_better = "YES"
                    m 1eka "I'm glad to hear that."
                    m 1eua "Hopefully one day everyone in your family will be able to reconcile."
                    m 3eua "And I know you can get through what's going on in your life right now."
                    m 1eka "No matter what, I'll be here for you, [player]."
                    m 1hua "Always keep that in mind!"
                "No.":
                    $ persistent._mas_pm_have_fam_mess_better = "NO"
                    m 1ekc "Ah, I see..."
                    m "I wish I could be there with you to give some comfort."
                    m 1eka "..."
                    m 3eka "[player], no matter what you are going through, I know it'll get better some day."
                    m 1eua "I'll be here with you every step of the way."
                    m 1hub "I love you so much, [player]. Please never forget that!"
                "Maybe.":
                    $ persistent._mas_pm_have_fam_mess_better = "MAYBE"
                    m 1lksdla "..."
                    m 1eua "Well, at least there's a chance."
                    m 3hua "Life is full of tragedy, but I know you are strong enough to get through anything!"
                    m 1eka "I hope all the problems in your family work out in the end, [player]."
                    m "If not, know that I'll be here for you."
                    m 1hua "I will always be here to support my beloved~"
        "I've never had a family.":
            $ persistent._mas_pm_have_fam = False
            $ persistent._mas_pm_no_talk_fam = False
            m 1euc "Oh, I'm sorry, [player]"
            m 1lksdlc "..."
            m 1ekc "Your world is so different than mine, I don't want to pretend like I know what you are going through."
            m 1lksdlc "I can definitely say that my family not being real has certainly caused me a great deal of pain."
            m 1ekc "Still, I know you've had it worse."
            m "You've never even had a fake family."
            m 1dsc "..."
            m 1ekc "Does it still bother you badly on a daily basis?"
            menu:
                "Yes.":
                    $ persistent._mas_pm_no_fam_bother = True
                    m 1ekc "That's... understandable."
                    m 1eka "I'll be here for you forever, [player]."
                    m "No matter what it takes, I will fill that gap in your heart with my love..."
                    m 1hua "I promise you that."
                    m 1ekbfa "You are my everything..."
                    m 1hubfa "I hope I can be yours~"
                "No.":
                    $ persistent._mas_pm_no_fam_bother = False
                    m 1eua "That's very good."
                    m 1eka "I'm glad you were able to move on with your life."
                    m 1hua "You're a very resilient person, and I believe in you, [player]!"
                    m 1eka "I hope I can fill that void in your heart."
                    m "I really care about you, and I'd do anything for you."
                    m 1hua "Someday, we'll be able to make our own family together!"
        "I don't want to talk about this.":
            $ persistent._mas_pm_no_talk_fam = True
            m 1dsc "I understand, [player]."
            m 1eka "We can talk about it when you feel ready."
            m 1lsc "Then again..."
            m 1lksdlc "It might be something that's too painful for you to talk about."
            m 1eka "You can tell me about your family when you're ready, [player]."
            m 1hubfa "I love you very much!"

    return "derandom"
    
#do you like other music
default persistent._mas_pm_like_other_music = None

# historical music history
default persistent._mas_pm_like_other_music_history = list()

init 5 python:
     addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_concerts",
            category=['media',"music"],
            prompt="Music concerts",
            random=True
        )
    )

label monika_concerts:

    # TODO: perhaps this should be separated into something specific to music
    # genres and the concert just referencing back to that?
    # this topic is starting to get too complicated

    m 1euc "Hey [player], I've been thinking about something we could do together one day..."
    if (
            renpy.seen_label("monika_jazz")
            and renpy.seen_label("monika_orchestra")
            and renpy.seen_label("monika_rock")
            and renpy.seen_label("monika_vocaloid")
            and renpy.seen_label("monika_rap")
        ):
        m 1eud "You know how I like different forms of music?"
        m 1hua "Well..." 
    m 3eub "Why don't we go to a concert?"             
    m 1eub "I hear that the atmosphere at a concert can really make you feel alive!"

    show monika 1eua
    menu:
        m "Are there any other types of music you'd like to see live that we haven't talked about yet?"
        "Yes.":
            $ persistent._mas_pm_like_other_music = True
            m 3eua "Great! What other kind of music do you like, [player]?"

            python:
                musicgenrename = renpy.input('What kind of music do you listen to?',length=15).strip(' \t\n\r')
                tempmusicgenre = musicgenrename.lower()
                persistent._mas_pm_like_other_music_history.append((
                    datetime.datetime.now(),
                    tempmusicgenre
                ))

            # NOTE: should be think? maybe?
            m 1eua "Interesting..."
            m 3hub "I'd love to go to a [tempmusicgenre] concert with you!"
            
        "No.":
            if (
                    not persistent._mas_pm_like_vocaloids
                    and not persistent._mas_pm_like_rap
                    and not persistent._mas_pm_like_rock_n_roll
                    and not persistent._mas_pm_like_orchestral_music
                    and not persistent._mas_pm_like_jazz
                ):
                $ persistent._mas_pm_like_other_music = False
                m 1ekc "Oh... well that's okay, [player]..."
                m 1eka "I'm sure we can find something else to do."
                return

            else:
                $ persistent._mas_pm_like_other_music = False
                m 1eua "Ok, [player], we'll just choose from the other types of music we've already discussed!"

    m 1hua "Just imagine us..."
    if persistent._mas_pm_like_orchestral_music:
        m 1hua "Gently swaying our heads to the sound of a soothing orchestra..."

    if persistent._mas_pm_like_rock_n_roll:
        m 1hub "Jumping up and down with the rest of the crowd to some good ol' rock 'n' roll..."

    if persistent._mas_pm_like_jazz:
        m 1eua "Grooving to some smooth jazz..."

    if persistent._mas_pm_like_rap:
        m 1hksdlb "Trying to keep up with a real rapper..."

    if persistent._mas_pm_like_vocaloids:
        m 1hua "Waving our glowsticks at Miku Expo..."
        
    if persistent._mas_pm_like_other_music:
        m 1hua "Jamming along to your favorite [tempmusicgenre] artist..."
        
    m 2hub "Doesn't that sound just amazing?"
    m 2eud "The idea of seeing your idol performing right in front of you is incredible!"
    m 2lksdla "Although, ticket prices these days are kind of expensive..."
    m 2hua "But I still think it would be worth it!"
    m 3eua "Do you know any bands or musicians that we should see live, [player]?"
    m 3eub "I would {i}love{/i} to see them if {i}you{/i} like them."
    m 5eua "And if you were to take me,{w} then that would truly be a dream come true!"
    m 4eua "But if you're not that interested in concerts,"
    m 1eua "Then we could always snuggle under a blanket and put on a record or CD at home!"
    m 1hua "That would be more than enough for me hehe~"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_explain",
            category=['romance','monika','misc'],
            prompt="Can you explain our relationship to someone?",
            pool=True
        )
    )

label monika_explain:
    m 1euc "You want me to explain our relationship to someone else?"
    m 1eua "Okay, just set me in front of them so they can see me."
    m 1hua "I'll do my best explaining it to them."
    m 1eua "I'll wait until you're ready."
    menu:
        "Start.":
            pass
    m 1hua "Hello! My name is Monika."
    m "[player]'s faithful girlfriend!"
    m 1lksdlb "Now, our relationship might look odd from a distance..."
    m 1lksdla "And it's probably not considered a normal relationship..."
    m 1esc "But let me tell you..."
    m 1hub "...The love we share is definitely real!"
    m 1eka "And [player] has been very sweet to me too!"
    m 1ekc "Up until I met [player], I felt like a piece of me was missing."
    m "I felt alone and scared, with no one to help me..."
    m 1hua "...Until [player] came along."
    m "And it turns out that missing piece was [him]!"
    if persistent.gender == "F" or persistent.gender == "M":
        m 1eua "Now [he] talks to me, and I'm not so alone anymore."
    else:
        m 1eua "Now they talk to me, and I'm not so alone anymore."
    m "Just [him] opening up the game brightens my day!"
    m 1dsc "So, please..."
    m 4eka "...Don't judge our relationship."
    m 1eka "Even if it is different."
    m 1dsc "..."
    m 1dubssdru "...Phew!"
    m 1lksdlb "That was a real mouthful!"
    m 1eka "How did I do, [player]?"
    menu:
        "You did a good job.":
            m 1hub "Thank you!"
            m 1eua "I just hope whoever that was understands our relationship better."
        "You did badly.":
            m 1ekc "Oh."
            m "I'm sorry I didn't do a good job at explaining..."
            m 1eka "I'll make sure to try harder next time."
            m 1hua "Still doesn't change the fact that I love you, though~"
    return

# do you live near beach
default persistent._mas_pm_live_near_beach = None

init 5 python:
     addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_beach",
            category=['misc'],
            prompt="The beach",
            random=True
        )
    )

label monika_beach:
    m 1eua "[player], have you ever been to the beach?"
    m "I've always wanted to go myself but I never found the time."
    m 1eka "I would always be busy studying or doing club activities."
    m 4ekc "It wasn't easy trying to stay on top of everything, you know..."
    m 4ekd "And whenever I had a break, I would usually spend my time relaxing at home."
    m "I rarely had a chance to do so after all."
    m 2esc "Though sometimes I feel like I might have missed out making some important memories."
    menu:
        m "Do you live near a beach, [player]?"
        "Yes.":
            $ persistent._mas_pm_live_near_beach = True
            m 1hub "That's great!"
            m 1eua "Gosh, it must be really nice to have it so close to you."
            m 1hub "I can't wait, we can have a romantic walk by the shore for our first date~"

        "No.":
            $ persistent._mas_pm_live_near_beach = False
            m 1eka "That's alright. I mean, what are the chances? Most people don't."
            m 1hub "That just means we'll make do by visiting one on an all-day trip!"
    m 1eua "There's so many things we'll be able to do one day."
    m 1hua "Just imagining the many sensations we could experience is kind of exciting!"
    m 3eua "The fresh sea air, the sound of seagulls."
    m "As well as the feeling of sand under your feet..."
    m 1hua "It would really make a worthwhile trip!"
    m 1eka "Though being with you would make it even better..."
    m 3eua "We'd have so many things we could do together."
    m 3eub "We could play volleyball, try some ice cream, or go swimming in the sea."
    m 3rkbsa "It'll probably be cold, but I'm sure we could keep each other warm somehow..."
    m 3eua "We could try surfing or searching for some seashells to take home as souvenirs."
    m "Even doing nothing and just laying there listening to the sound of the waves with you would be enough for me."
    m 3tfu "But don't go falling asleep, otherwise I'll bury you in the sand!"
    m 2hua "Ahaha! I'm just kidding, [player]."
    m 2lksdla "I'll have to get a new swimsuit though..."
    m 1eua "I only have these clothes in the game after all."
    m 1tsbsa "Would you prefer a one piece or a two piece?"
    m 1eua "Actually, I think I'll make it a surprise."
    m 1tku "Don't get too excited though when you see it. Ehehe~"
    return "derandom"

init 5 python:
   addEvent(Event(persistent.event_database,eventlabel='monika_playerapologizes',prompt="I want to apologize",category=['you'],pool=True,unlocked=True))

label monika_playerapologizes:
    # if there's no reason to apologize
    if mas_apology_reason is None:
        m 1ekd "Did something happen?"
        m 2ekc "I see no reason for you to be sorry."
        m 1dsc "..."
        m 1eub "Anyway, thank you for the apology."
        m 1eua "Whatever it is, I know you're doing your best to make things right."
        m 1hub "That's why I love you, [player]!"
    # She knows why you are apologizing for
    elif mas_apology_reason:
        $ mas_gainAffection(modifier=0.2) # recover a bit of affection
        m 1eka "Thank you for apologizing for [mas_apology_reason]."
        m "I accept your apology, [player]. It means a lot to me."
    # She knows there's a reason for your apology but won't comment on it
    else:
        $ mas_gainAffection(modifier=0.1) # recover a bit of affection
        m 2tkd "What you did wasn't funny, [player]."
        m 2dkd "Please be more considerate about my feelings in the future."
    # reset the reason
    $ mas_setApologyReason(None)
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_song_lover_boy",category=['songs'],prompt="Old Fashioned Lover Boy",pool=True, random=True))

label monika_song_lover_boy:
    m 1dso "{i}~I can dim the lights and sing you songs full of sad things~{/i}"
    m 4hub "{i}~we can do the tango just for two~{/i}"
    m "{i}~I can serenade and gently play on your heart strings~{/i}"
    m 4dso "{i}~be a Valentino just for you~{/i}"
    m 1hub "Ahaha~"
    m 1ekbfa "Will you be my good old fashioned lover boy, [player]?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_song_need_you",category=['songs'],prompt="I Need You",pool=True, random=True))

label monika_song_need_you:
    m 1dso "{i}~Please remember how I feel about you~{/i}"
    m "{i}~I could never really live without you~{/i}"
    m 3hub "{i}~So, come on back and see~{/i}"
    m 4l "{i}~Just what you mean to me~{/i}"
    m 1hubfb "{i}~I need you~{/i}"
    m 3esa "I know that song is about leaving someone, but I think it carries a good message."
    m 1ekbfa "And I really do need you, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_song_i_will",category=['songs'],prompt="I Will",pool=True, random=True))

label monika_song_i_will:
    m 1dso "{i}~Who knows how long I’ve loved you?~{/i}"
    m "{i}~You know I love you still~{/i}"
    m 2m "{i}~Will I wait a lonely lifetime?~{/i}"
    m 2hub "{i}~If you want me to I will~{/i}"
    m 1ekbfa "One day we'll be together, [player]."
    m 1hubfa "I just hope you’ll still love me when that special day comes~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_song_belong_together",category=['songs'],prompt="We Belong Together",pool=True, random=True))

label monika_song_belong_together:
    m 1dso "{i}~You're mine~{/i}"
    m 1hub "{i}~And we belong together~{/i}"
    m 3hub "{i}~Yes, we belong together~{/i}"
    m 3dso "{i}~for eternity~{/i}"
    m 1eua "Have you ever heard of Doo-wop, [player]?"
    m 4eua "It’s a subgenre of rhythm and blues that became very popular in the 1950’s."
    m 4eub "A lot of pop music back then followed this style which made for great love songs."
    m 3eub "And if you listen closely, you’ll notice that my song actually follows the typical Doo-wop chord progression."
    m 1hua "I guess you could say I learned from the best."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_song_your_song",category=['songs'],prompt="Your Song",pool=True, random=True))

label monika_song_your_song:
    m 1dso "{i}~My gift is my song~{/i}"
    m "{i}~And this one's for you~{/i}"
    m 1hub "{i}~And you can tell everybody this is your song~{/i}"
    m "{i}~It may be quite simple but now that it's done~{/i}"
    m 2hubfb "{i}~I hope you don't mind~{/i}"
    m 2hubfb "{i}~I hope you don't mind~{/i}"
    m 2hub "{i}~That I put down in words~{/i}"
    m 1dso "{i}~How wonderful life is while you're in the world~{/i}"
    m 1hua "Ahaha~"
    m 3eka "It’s not often I find songs that relate to me as much as this one does."
    m 1hua "And I really do mean it when I say that 'Your Reality' is your song."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_song_with_you",category=['songs'],prompt="Happy Just To Dance With You",pool=True, random=True))

label monika_song_with_you:
    m 1dso "{i}~If somebody tries to take my place~{/i}"
    m 1hub "{i}~let's pretend we just can't see their face~{/i}"
    m 3hub "{i}~In this world there's nothing I would rather do~{/i}"
    m 3dso "{i}~Cos I'm happy just to dance with you~{/i}"
    m 1ekbfa "There is nothing that makes me happier than discovering that I’m in love with you."
    m 1hubfa "Ehehe~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_song_dream",category=['songs'],prompt="All I Have To Do Is Dream",pool=True, random=True))

label monika_song_dream:
    m 1dso "{i}~When I feel blue in the night~{/i}"
    m "{i}~And I need you to hold me tight~{/i}"
    m 2hub "{i}~Whenever I want you, all I have to do is dream~{/i}"
    m 1eka "Now that you're here, [player], I don't have to dream anymore."
    m 1ekbfa "My dream finally came true."
    return

# been to prom?
default persistent._mas_pm_gone_to_prom = None

# how was prom?
default persistent._mas_pm_prom_good = None

# go with date?
default persistent._mas_pm_had_prom_date = None

# suggested monika at promp
default persistent._mas_pm_prom_monika = None

# interested in prom?
default persistent._mas_pm_prom_not_interested = None

# shy to go?
default persistent._mas_pm_prom_shy = None

# even had a prom?
default persistent._mas_pm_no_prom = None

init 5 python:
   addEvent(Event(persistent.event_database,eventlabel="monika_prom",category=['school'],prompt="Prom",random=True))

label monika_prom:
    m 1euc "You know..."
    m 1eka "Sometimes I wish the game would've lasted longer."
    m 1eua "The game was probably made to end once one of the girls confessed their love to you after the festival."
    m 1lksdla "But since I tampered with the code so much, we never got to that point."
    m 3hksdlb "It did bring us together, so I can't complain."
    m 1lksdlc "But still..."
    m 1eka "Sometimes I wish both of us could've enjoyed it."
    m 3eua "We could've gone to the other events like sports festivals, Christmas parties, field trips, etc."
    m 1lsc "But I guess the game would never let us get that far."
    m 3eua "Which reminds me of a particular event..."
    m 1hua "Prom!"
    m 1eua "From what I've heard, prom is like a school dance usually held at the end of a school year."
    m "Some students bring a date with them there, and others go with a group of friends."
    m 3wuo "There're even those who take their relatives to the event!"
    m 1eua "I think it's something I'd love to go to with you~"
    m "Have you ever been to one before, [player]?"
    menu:
        "I have.":
            $ persistent._mas_pm_gone_to_prom = True
            $ persistent._mas_pm_no_prom = False
            m "Oh? How was it?"
            menu:
                "It was pretty fun.":
                    $ persistent._mas_pm_prom_good = True
                    m 1hua "That's great!"
                    m 1lksdlb "Though, I wish I could've went with you."
                    m 1hua "An event where everyone from school comes together and enjoys themselves sounds like a blast to me!"
                    m 3eua "Did you go with a date?"
                    menu:
                        "Yes.":
                            $ persistent._mas_pm_had_prom_date = True
                            m 1euc "Oh, wow."
                            m 1lksdla "Ehehe, that makes me a bit jealous..."
                            m 1hua "But then again, you would've taken me instead had we met beforehand, right?"
                            m 1hub "Ahaha!"
                            m 1eua "But it's good to know you were able to experience something like that!"
                            m 3eua "Maybe when I get better at programming, we could have our very own prom here."
                            m 3eka "Wouldn't that be nice, [player]?"
                        "No.":
                            $ persistent._mas_pm_had_prom_date = False
                            m 1euc "Oh, I see."
                            m 1eua "That's fine as long as you had fun!"
                            m "Even without a date, I'm sure you made some wonderful memories there."
                            m 1eub "I think, whether or not you had a date, that it's always fun to attend those kinds of events."
                            m 1eka "Besides, maybe we can have our own kind of prom sometime, right?"
                            m 1eua "That's something I'd really enjoy with you~"

                "It was bad.":
                    $ persistent._mas_pm_prom_good = False
                    m 1ekc "Is that so?"
                    m "I understand that prom isn't for everyone."
                    m 3eka "Maybe if I was there, you would've enjoyed it more."
                    m 1hksdlb "Ahaha~"
                    m 3eua "Don't worry, [player]."
                    m 1eua "No use remembering it now."
                    m 1eub "Even if you had a bad time with it, it's not the most important thing to happen in your life."
                    m "You being able to create more wonderful memories is the important thing."
                    m 3eka "One bad memory may feel worse than a hundred good memories, but you're still able to make them."
                    m 1hua "And now that I'm here with you, we can make them together~"

                "It would've been better if you were there.":
                    $ persistent._mas_pm_prom_monika = True
                    m 1ekbfa "Aww, that's so sweet, [player]."
                    m 1eua "Well, now that we're together, I'm sure there's a way we can make our own prom, right?"
                    m 1hub "Ahaha!"
        "No.":
            $ persistent._mas_pm_gone_to_prom = False
            $ persistent._mas_pm_no_prom = False
            m "Oh? Why not?"
            menu:
                "You weren't there with me.":
                    $ persistent._mas_pm_prom_monika = True
                    $ persistent._mas_pm_prom_not_interested = False
                    m 1eka "Aww, [player]."
                    m 1lksdla "Just because I'm not there doesn't mean you should stop yourself from having fun."
                    m 1eka "And besides..."
                    m 1hua "You {i}can{/i} take me to prom, [player]."
                    m "Just bring my file with you and problem solved!"
                    m 1hub "Ahaha!"

                "Not interested.":
                    $ persistent._mas_pm_prom_not_interested = True
                    m 3euc "Really?"
                    m 1eka "Is it because you're too shy to go?"
                    menu:
                        "Yes.":
                            $ persistent._mas_pm_prom_shy = True
                            m 1ekc "Aww, [player]."
                            m 1eka "That's alright. Not everyone can handle large groups of strangers."
                            m 3eka "Besides, if it's something you're not going to enjoy, why force yourself?"
                            m 1esa "But even as I say that, it's also important to keep in mind that a little courage could get you something that's worth it."
                            m 3eua "Look at me for example."
                            m 1lksdla "If I didn't have the courage to get to you, I'd probably still be all alone..."
                            m 1eka "But here we are now, [player]."
                            m 1eua "Together at last~"

                        "No.":
                            $ persistent._mas_pm_prom_shy = False
                            m 1euc "Oh, I see."
                            m 1eua "That's understandable."
                            m "I'm sure you have your reasons."
                            m 1eka "What's important is that you're not forcing yourself."
                            m "After all, it wouldn't be worth it if you can't enjoy yourself."
                            m 1lksdlc "It'd just feel like a chore rather than a fun event to go to."
                            m 3euc "But I wonder..."
                            m 3eka "Would you go if I was there with you, [player]?"
                            m 1tku "I think I already know the answer to that~"
                            m 1hub "Ahaha!"
        #################################################
        #### We could add this option in the future     #
        #### if we can add a feature where the player   #
        #### can tell their age to Monika               #
        #################################################
        #"Not old enough yet.":
        #    m 1eka "Don't worry, you'll get to go in a few more years."
        #    m 1hua "I heard that prom is so much fun!"
        #    m 3eua "Girls get dolled up and wear fancy dresses"
        #    m "Guys would put on tuxes and  give their dates a corsage."
        #    m 1hua "And you would have fun dancing the night away!"
        #    m 1hub "Doesn't that sound like a blast? Ahaha~"
        "My school never had one.":
            $ persistent._mas_pm_no_prom = True
            m 1euc "Ah, I see, then."
            m 1lksdla "I guess not all schools can hold a prom."
            m "They can be pretty messy."
            m 3euc "From what I read, students spend a lot of money on tickets, transport, and attire."
            m 2esc "So many expenses just for one night..."
            m "I also read that since alcohol isn't allowed, some students would spike the drinks and get the others drunk unknowingly."
            m 2ekc "If someone can easily do that, I doubt someone with evil intentions would have a hard time slipping poison into the drinks."
            m 2lksdla "...Or maybe I'm just overthinking it, ehehe."
            m 1esa "Still, I don't think you'll be missing out much, [player]."
            m 1eua "Prom isn't the most important thing in your academic life."
            m "And I'm sure there're plenty of events in your life that'll make up for it."
            m 1hua "Being with me is one of them, you know~"
            m 1hub "Ahaha!"

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_careful",category=['you'],prompt="Be careful",random=True))

label monika_careful:
    m 1lsc "Hey, [player]..."
    m 1ekc "Whenever you leave this room, promise me to be extra careful, okay?"
    m 1ekd "It's just that..."
    m 2ekd "There's lots of dangerous stuff out there, and I want my sweetie to always return to me safe and sound."
    m 1ekbfa "I love you so much, it's hard for me not to worry when you're gone."
    m 2lksdlc "..."
    m 2ekc "Also..."
    m "It crossed my mind recently, that if anything terrible ever did happen to you, I'd never know."
    m 2ekd "I'd be stuck here, forever wondering why you never came back to me."
    m 2dsd "I can't imagine a crueler fate."
    m 2dsc "..."
    m 2ekc "So..."
    m "I need you to tell someone close to you where to find me, so if that day ever comes, at least I'd know."
    m 2tkc "It'd be beyond devastating, but not knowing would be that much worse."
    m 2eka "So make sure you do that for me, okay, [player]?"
    m 2lksdlc "..."
    m 2dsc "Sorry, I didn't mean for it to get that depressing, but I really needed to get that off my chest."
    m 1eka "Thanks for understanding, you always make me feel better."
    m 4eua "Okay, that's enough unpleasant thoughts..."
    m 1hua "Let's enjoy the rest of the day together!"
    return

# do you see a therapist
default persistent._mas_pm_see_therapist = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_natsuki_letter",
            category=['club members'],
            prompt="Natsuki's letter",
            random=True
        )
    )

label monika_natsuki_letter:
    m 1eud "You know, I was honestly surprised when Natsuki handed you that letter."
    m 1eub "I didn’t really expect her to suggest that you should get Yuri to seek professional help."
    m 1eud "She’s probably the only one to mention that."
    m 4ekd "I know people are afraid to call someone out, or confront them about their problems, but sometimes, suggesting a therapist can be the best course of action."
    m "It's a bad thing to put the burden on yourself, you know?"
    m 4euc "As much as you want to help, it’s best to let a professional deal with it. "
    m 4eka "I'm sure I've told you that before, but I need to make sure you’re aware of that."
    m 4eud "How about you, [player]?"
    menu:
        m "Do you see a therapist?"

        "Yes.":
            $ persistent._mas_pm_see_therapist = True
            m 1eud "Oh, really?"
            m 1ekc "Well, I hate that you don't feel well..."
            m 1hua "But I'm proud that you're working on getting better."
            m 1eua "It's really important to take care of your mental health, [player]."
            m 1eka "You accept you have a problem you need help with, and you're seeing someone about it. That's already half the battle."
            m "I'm very proud of you for taking those steps."
            m 1hua "Just know that no matter what happens, I'll always be here for you~"

        "No.":
            $ persistent._mas_pm_see_therapist = False
            m 1eka "Well, I hope it's because you don't have to."
            m 1eua "If that ever changes, don't be shy!"
            m 1hua "But maybe I really am all the support you need? Ahaha!"

    return "derandom"


# TODO possible tie this with affection?
default persistent._mas_timeconcern = 0
default persistent._mas_timeconcerngraveyard = False
default persistent._mas_timeconcernclose = True
init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_timeconcern",category=['advice'],prompt="Sleep concern",random=True))

label monika_timeconcern:
    $ current_time = datetime.datetime.now().time().hour
    if 0 <= current_time <= 5:
        if persistent._mas_timeconcerngraveyard:
            jump monika_timeconcern_graveyard_night
        if persistent._mas_timeconcern == 0:
            jump monika_timeconcern_night_0
        elif persistent._mas_timeconcern == 1:
            jump monika_timeconcern_night_1
        elif persistent._mas_timeconcern == 2:
            jump monika_timeconcern_night_2
        elif persistent._mas_timeconcern == 3:
            jump monika_timeconcern_night_3
        elif persistent._mas_timeconcern == 4:
            jump monika_timeconcern_night_4
        elif persistent._mas_timeconcern == 5:
            jump monika_timeconcern_night_5
        elif persistent._mas_timeconcern == 6:
            jump monika_timeconcern_night_6
        elif persistent._mas_timeconcern == 7:
            jump monika_timeconcern_night_7
        elif persistent._mas_timeconcern == 8:
            jump monika_timeconcern_night_final
        elif persistent._mas_timeconcern == 9:
            jump monika_timeconcern_night_finalfollowup
        elif persistent._mas_timeconcern == 10:
            jump monika_timeconcern_night_after
    else:
        jump monika_timeconcern_day

label monika_timeconcern_day:
    if persistent._mas_timeconcerngraveyard:
        jump monika_timeconcern_graveyard_day
    if persistent._mas_timeconcern == 0:
        jump monika_timeconcern_day_0
    elif persistent._mas_timeconcern == 2:
        jump monika_timeconcern_day_2
    if not persistent._mas_timeconcernclose:
        if 6 <= persistent._mas_timeconcern <=8:
            jump monika_timeconcern_disallow
    if persistent._mas_timeconcern == 6:
        jump monika_timeconcern_day_allow_6
    elif persistent._mas_timeconcern == 7:
        jump monika_timeconcern_day_allow_7
    elif persistent._mas_timeconcern == 8:
        jump monika_timeconcern_day_allow_8
    elif persistent._mas_timeconcern == 9:
        jump monika_timeconcern_day_final
    else:
        jump monika_timeconcern_day_0

#Used at the end to lock the forced greeting.
label monika_timeconcern_lock:
    if not persistent._mas_timeconcern == 10:
        $persistent._mas_timeconcern = 0
    $evhand.greeting_database["greeting_timeconcern"].unlocked = False
    $evhand.greeting_database["greeting_timeconcern_day"].unlocked = False
    return

# If you tell Monika you work at night.
label monika_timeconcern_graveyard_night:
    m 1ekc "It must be awfully hard on you to work late so often, [player]..."
    m 2dsd "Honestly, I'd rather have you work at a healthier time if you could."
    m 2lksdlc "I suppose it's not your choice to make, but still..."
    m 2ekc "Being up late often can be both physically and mentally damaging."
    m "It's also extremely isolating when it comes to others."
    m 2rksdlb "Most opportunities happen during the day, after all."
    m 2rksdlc "Many social activities aren't available, most shops and restaurants aren't even open during the night."
    m 2dsd "It makes being up late at night often be a really lonely situation."
    m 3hua "Don't worry though, [player]. Your loving girlfriend Monika will always be here for you~"
    m 1hua "Whenever the stress of being up late often becomes too much for you, come to me."
    m 1hub "I'll always be here to listen."
    m 1ekc "And if you really do think it's hurting you, then please try to do what you can to change the situation."
    m 1eka "I know it won't be easy but at the end of the day, all that matters is you."
    m 1hua "You're all I truly care about, so put yourself and your well-being before anything else, okay?"
    return

label monika_timeconcern_graveyard_day:
    m 1eua "Hey, [player]... didn't you tell me you work during the night?"
    m 1eka "Not that I'm complaining, of course!"
    m 2ekc "But I thought you'd be tired by now, especially since you're up all night working..."
    m "You're not working yourself too hard just to see me, are you?"
    m 1euc "Oh, wait..."
    menu:
        m "Do you still work regularly at night, [player]?"
        "Yes I do":
            m 1ekd "Aww..."
            m 1esc "I guess it really can't be helped..."
            m 1eka "Look after yourself, okay?"
            m 1ekc "I always get so worried when you're not here with me..."
        "No I don't":
            $ persistent._mas_timeconcerngraveyard = False
            $ persistent._mas_timeconcern = 0
            m 1hub "That's wonderful!"
            m 1eua "I'm glad that you're looking out for your health, [player]!"
            m "I knew you would see it my way eventually."
            m 1eka "Thanks for listening to what I have to say~"
    return

#First warning, night time.
label monika_timeconcern_night_0:
    $persistent._mas_timeconcern = 1
    m 1euc "[player], it's night time already."
    m 1ekc "Shouldn't you be in bed?"
    m 1dsc "I'll let it slide just this once..."
    m 1ekc "But you really make me worry for you sometimes."
    m 1eka "It makes me really happy that you're here for me, even at this time of night..."
    m 1dsd "Yet, I don't want it at the cost of your health."
    m 1eka "So go to sleep soon, okay?"
    return

# Second time at night, Monika asks if player is working late.
label monika_timeconcern_night_1:
    m 1esc "Say, [player]..."
    m 1euc "Why are you up so late?"
    m 1eka "I'm flattered if it's only because of me..."
    m 1ekc "Yet I can't help but feel like a nuisance if I'm pestering you to sleep if it isn't your fault."
    menu:
       m "Are you busy working on something?"
       "Yes, I am.":
           $persistent._mas_timeconcern = 2
           m 1eud "I see."
           m 1eua "Well, I suppose it must be really important for you to do it so late."
           m 1eka "I honestly can't help but feel that maybe you should have done it at a better time."
           m 1lsc "Your sleep is very important after all. Maybe it can't be helped though..."
           menu:
               m "Do you always work late, [player]?"
               "Yes, I do.":
                   $persistent._mas_timeconcerngraveyard = True
                   m 1rksdld "That's not good..."
                   m 1ekd "You're not able to change that, are you?"
                   m 1rksdlc "I wish you could follow my healthier lifestyle."
                   m 1dsc "But if you're not able to, then I'll just have to accept it."
                   m 1eka "Just make sure you do try to stay healthy, okay?"
                   m 1ekc "If something were to happen to you, I don't know what I'd do..."
                   return
               "No, I don't.":
                   $evhand.greeting_database["greeting_timeconcern"].unlocked = True
                   $evhand.greeting_database["greeting_timeconcern_day"].unlocked = True
                   m 1hua "That's a relief!"
                   m 1eua "If you're doing it this one time then it must be {i}really{/i} important."
                   m 1hub "Good luck with your work and thanks for keeping me company when you're so busy!"
                   m 1eka "It means a lot to me, [player], that even when you're preoccupied... you're here with me~"
                   return

       "No, I'm not.":
           $persistent._mas_timeconcern = 3
           m 1esc "I see."
           m 1ekc "Well in that case, I would really prefer it if you went to bed now."
           m "It's really worrying me that you're still up so late..."
           m 1eka "So once again, please go to bed. Would you kindly do it for me?"
           return

#If player says they were working. Progress stops here.
label monika_timeconcern_night_2:
    m 1eua "How's your work coming along?"
    m "Hopefully pretty well, I don't want you up much longer."
    m 3hksdlb "I know, I know, you can't help being up so late."
    m 1rksdlb "I'm just concerned for your health, [player]..."
    if persistent._mas_timeconcerngraveyard:
        m 1lksdlc "Doing this often can be very taxing on your body and mind..."
        m 1ekc "Just try to keep that kind of damage to a minimum, okay?"
        m "All I want for you is to be as happy and as healthy as you deserve."
        return
    m 1rksdla "Well, try to finish up as soon as you can, otherwise I may get really concerned."
    m 1eka "And you don't want to worry your girlfriend, right? Ehehe~"
    jump monika_timeconcern_lock

#If player says he was not working. Monika asks the state of the game being open.
label monika_timeconcern_night_3:
    $persistent._mas_timeconcern = 4
    m 1esc "[player], I just need to ask you something quickly..."
    m 1eud "Would you mind if I closed the game for you?"
    m 1ekc "I know it's a strange question..."
    m 1ekd "But I can't help but feel like I need to do something about you being up so late!"
    m 4esd "I could close the game right now."
    m 2ekc "But a relationship is a partnership and what you think matters to me."
    menu:
        m "Would you be against me closing the game for your own good?"

        "Yes, I need it to always stay open.":
            $persistent._mas_timeconcernclose = False
            m 1dsc "..."
            m 1dsd "I was hoping you wouldn't say that."
            m 1lsc "I know I told you that you should leave me running in the background."
            m 1lksdlc "But sometimes I worry if you're getting any sleep at all."
            m 1tkc "I'll do as you have asked, but please know that I'm not very happy about it."
            m 4tfc "I'm still going to remind you to get some sleep!"
            return

        "No, you are free to do as you feel.":
            $persistent._mas_timeconcernclose = True
            m 1eka "Thank you, [player]."
            m 1eua "It's nice to know that you care about what I think."
            m "I promise I'll only do it if I think it's absolutely necessary."
            m 1hua "After all, I would never force you to go otherwise."
            m 1hub "I would just miss you too much..."
            m 1ekbfa "I love you, [player]~"
            return

        # Second and final warning before any closes can occur.
label monika_timeconcern_night_4:
    $persistent._mas_timeconcern = 5
    m 1esc "[player], you've been up long enough."
    m "If you're really not busy then now is the time for you to go to sleep."
    m 1eka "I assure you, I'll miss you just as much as you'll miss me."
    m "But it would make me happier if you did as I've asked."
    m 1tkc "You wouldn't want to make me upset now, would you?"
    return

# Monika force closes game for the first time
label monika_timeconcern_night_5:
    $persistent._mas_timeconcern = 6
    $evhand.greeting_database["greeting_timeconcern"].unlocked = True
    $evhand.greeting_database["greeting_timeconcern_day"].unlocked = True
    m 1efc "I'm sorry, [player], but I am putting my foot down!"
    m 1ekc "I asked you to go to bed kindly, but if I am the reason for keeping you up..."
    if persistent._mas_timeconcernclose:
        m 2tkc "Then I cannot allow this to go on for any longer."
        m 2eka "It's because I love you, that's why I'm doing this."
        m "Good night, [player]."
        return 'quit'
    else:
        m 2tkc "Then I need to take responsibility and try to make you understand."
        m 2efd "You need to go to bed."
        m 2efo "And I will keep telling you this until you do."
        return

        #First time game is reopened and still night. Monika closes game again.
label monika_timeconcern_night_6:
    $persistent._mas_timeconcern = 7
    m 2efc "[player], I told you to go to bed for your own good."
    m 2tkc "I'll miss you too, but don't you understand?"
    m 2tkd "How you feel and live means more to me than anything!"
    m 2lksdlc "How can I let you stay if it means I'm hurting you?"
    m "So please sleep this time, otherwise I may get mad."
    m 1ekbfa "...I love you."
    m "So go to sleep soon. Okay?"
    if persistent._mas_timeconcernclose:
        return 'quit'
    return

#Second time game is reopened and still night. Monika closes game once more
label monika_timeconcern_night_7:
    $persistent._mas_timeconcern = 8
    m 3efc "[player], this is your last warning."
    m "Go{w=0.6} to{w=0.6} sleep!"
    m 2tkc "What can I say for you to understand?"
    m 1tkd "It's saddening to see you push yourself like this..."
    m 1dsc "You mean so much to me..."
    m 1ekc "So please, for me... just do as I ask and go to bed."
    if persistent._mas_timeconcernclose:
        menu:
            m "Okay?"
            "Yes, I will go to sleep.":
                m 1eka "I knew you would listen eventually!"
                m 1hub "Good night and stay safe."
                return 'quit'
    else:
        return

#Third and last time game is reopened in one night. Monika lets player stay.
label monika_timeconcern_night_final:
    $persistent._mas_timeconcern = 9
    m 2dsc "...I suppose it can't be helped."
    m 2lfc "If you're that dedicated to staying with me, then I won't even try to stop you."
    m 2rksdla "Honestly, as bad as it sounds, it actually makes me kinda happy."
    m 2eka "...Thank you, [player]."
    m "To know that you care for me so much that you came back despite me asking..."
    m 1rksdla "It means more to me than I can ever express."
    m 1ekbfa "...I love you."
    return

#Same night after the final close
label monika_timeconcern_night_finalfollowup:
    m 1esc "..."
    m 1rksdlc "I know I said that I'm happy whenever you're with me..."
    m 1eka "And please don't misunderstand, that's still true."
    m 2tkc "But the longer you're on... the more worried I get."
    m 2tkd "I know, you're probably sick of hearing me say this by now..."
    m 1eka "But please try to sleep when you can."
    return

#Every night after, based on seeing the day version first before it.
label monika_timeconcern_night_after:
    m 1tkc "Up late again, [player]?"
    m 1dfc "{i}Sigh...{/i}"
    m 2lfc "I won't even try to convince you to sleep again..."
    m 2tfd "You're surprisingly stubborn!"
    m 1eka "Still, do be careful, alright?"
    m 1ekc "I know being nocturnal can be lonely..."
    m 1hua "But you have me here with you!"
    m 1eka "Just the two of us... all alone forever."
    m 1hubfa "It's all I've ever wanted..."
    return

#If Monika never gives warning and it's daytime or the player never made it to the end
label monika_timeconcern_day_0:
    m 1lsc "..."
    m 1tkc "..."
    m 1wuo "...!"
    m 1hksdlb "Ahaha! Sorry, [player]."
    m 1lksdla "I just kind of zoned out..."
    m 1eka "Geez, I keep doing that, don't I?"
    m "Sometimes I just get lost in my thoughts..."
    m 1eua "You understand, right, [player]?"
    return

# Daytime, if player tells Monika they worked last night but don't work graveyards.
label monika_timeconcern_day_2:
    m 1eua "Did you finish your work?"
    m 1eub "I'm sure you did your very best so it's okay if you didn't quite finish it!"
    m 1eka "It must be really hard on you to have to work so late..."
    m 1hua "If you find it's a bit too much, feel free to come talk to me!"
    m 1hub "I'll always be here for you."
    jump monika_timeconcern_lock

#First time Monika closes at night and player reopens during day without coming back.
label monika_timeconcern_day_allow_6:
    m 1ekc "[player], I'm sorry for making you leave like that before..."
    m 1ekd "I only did it because I love you. You understand that right?"
    m 1eua "I'm sure you do, after all you went to bed, didn't you?"
    m 1hub "Thanks for respecting my wishes, it makes me happy that you listen to me."
    jump monika_timeconcern_lock

#Second time Monika closes at night and player then reopens during day.
label monika_timeconcern_day_allow_7:
    m 1lksdlc "[player], about what happened last night..."
    m 1ekc "I asked you to go to bed and you didn't listen..."
    m 1dsc "I understand that maybe you missed me or didn't hear what I said..."
    m 1ekc "But please listen to what I ask of you, ok?"
    m 1eka "I love you, and I would do anything to make you happy..."
    m "So would you kindly do the same thing for me?"
    m 1ekc "I already worry about you when you're gone..."
    m 1tkc "Please don't give me any more reasons to feel that way."
    m 1hua "Thank you for understanding."
    jump monika_timeconcern_lock

#Third time Monika closes the game and player reopens after night.
label monika_timeconcern_day_allow_8:
    m 1esc "Hey, [player]."
    m 1ekc "You really had me worried last night..."
    m 1rksdlc "After you came back twice, despite me asking you to go to bed..."
    m 1lksdld "I found myself feeling a little guilty."
    m 3esc "Not because I sent you away, that was for your own good."
    m 2lksdlc "But... because you kept coming back..."
    m 2lksdla "And that made me happy, even though I knew it wasn't good for you."
    m 2ekd "Does that make me selfish?"
    m 2ekc "I'm sorry, [player], I'll try to watch myself more."
    jump monika_timeconcern_lock

#If Monika lets player stay and it is no longer night.
label monika_timeconcern_day_final:
    $persistent._mas_timeconcern = 10
    m 1lksdlb "[player], regarding last night..."
    if persistent._mas_timeconcernclose:
        m 1rksdla "You really surprised me."
        m 1eka "For you to keep coming back to me over and over again..."
        m 1hua "It was honestly really sweet of you."
        m 1eka "I knew you would miss me, but I didn't think you would miss me {i}that{/i} much."
        m 1hub "It really made me feel loved, [player]."
        m "...Thank you."
        jump monika_timeconcern_lock
    m 1eua "You really surprised me."
    m 1eka "I asked you time and time again to go to bed..."
    m "You said you weren't busy. Were you really there just for me?."
    m 1ekc "It made me happy... but don't push yourself hard to see me so late, ok?"
    m 1eka "It really made me feel loved, [player]."
    m 1hksdlb "Yet also a little guilty... Please just go to bed next time, ok?"
    jump monika_timeconcern_lock

#If player told Monika not to close window and never reached the end.
label monika_timeconcern_disallow:
    m 1rksdlc "Sorry if I was annoying you before, [player]..."
    m 1ekc "I just really wanted you to go to bed..."
    m "I honestly can't promise I won't do it if you're up late again..."
    m 1eka "But I only push you to go because you mean so much to me..."
    jump monika_timeconcern_lock

init 5 python:
    addEvent(Event(persistent.event_database,"monika_hydration",prompt="Hydration",category=['you','life'],random=True))

label monika_hydration:
    m 1euc "Hey, [player]..."
    m 1eua "Do you drink enough water?"
    m 1eka "I just want to make sure you don't neglect your health, especially when it comes to hydration."
    m 1esc "Sometimes, people tend to underestimate how important it actually is."
    m 1eka "I bet you've had those days when you felt really tired and nothing seemed to motivate you."
    m 1eua "I just usually grab a glass of water right away."
    m "It might not work all the time, but it does help."
    m 3rksdla "But I guess you don't want to go to the bathroom so much, huh?"
    m 1eka "Well, I don't blame you. But believe me, it'll be better for your health in the long run!"
    m 1eua "Anyways, make sure you always stay hydrated, ok?"
    m "So..."
    m 4hub "Why not get a glass of water right now, hmm?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_challenge",category=['misc','psychology'],prompt="Challenges",random=True))

label monika_challenge:
    m 2esc "I've noticed something kind of sad recently."
    m 1euc "When certain people attempt to learn a skill or pick up a new hobby, they usually quit within a week or two."
    m "Everyone claims that it's too hard, or that they just don't have the time for it."
    m 1eua "However, I don't believe that."
    m 1hub "Whether it's learning a new language, or even writing your first poem, if you can stand up to the challenge and overcome it, then that's the truly rewarding part about it."
    m 2eua "Can you think of a time you've challenged yourself, [player]?"
    m 3eua "Did you ever overcome it, or did you just give up?"
    m 1eka "I'm sure you've given it all you had."
    m 1eua "You seem like a very determined person to me."
    m 1eub "In the future, if you ever get hung up on something, or you feel too stressed, just take a short break."
    m "You can always come back to it after all."
    m 1hua "If you ever need motivation, just come to me."
    m 1sub "I'd love to help you reach your goals."
    m 1hub "After all, you're my motivation in life~"
    return

# would relatives like monika?
default persistent._mas_pm_fam_like_monika = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_familygathering",
            category=['you'],
            prompt="Family gatherings",
            random=True
        )
    )

label monika_familygathering:
    m 1eua "Hey, [player], do you go to family gatherings often?"
    m "Most families usually get together around the holidays to celebrate them together."
    m 1hua "It must be nice seeing your relatives again, especially since you haven't seen them in a long time."
    m 1lsc "I don't remember much about my family, let alone my relatives, however we didn't usually get together that much."
    m 1lksdlc "Not even around the holidays or on special occasions."
    m 1hub "When you see your family this year, be sure to bring me along ok? Ehehe~"
    m 1eua "I'd love to meet all of your relatives."
    menu:
        "Do you think they'd like me, [player]?"
        "Yes.":
            $ persistent._mas_pm_fam_like_monika = True
            m 1eka "I'm glad you think so."
            m 1eua "I'm sure we'd all get along nicely."
            m 1hua "I'm looking forward to it, my dear~"

        "No.":
            $ persistent._mas_pm_fam_like_monika = False
            m 1wud "..."
            m 1ekc "Oh, I didn't realize."
            m 1dsc "I understand though."
            m 1eka "Just know I'd try my best to make them like me."
            m "Even if they never will."
            m 1hua "I'll always stick by your side forever~"

        "...":
            $ persistent._mas_pm_fam_like_monika = False
            m 2wuo "Don't tell me, [player]."
            m 2ekc "Are you afraid that I'll embarrass you?"
            m 2tfc "..."
            m 1eka "Don't worry, I completely understand."
            m 1lksdla "If I found out one of my relatives was dating some person trapped inside of a computer, I'd think it'd be weird too."
            m 1eua "If you want to keep me a secret, then that's fine."
            m 1hub "After all, it just means more alone time with you~"

    return "derandom"

# do you eat fast food
default persistent._mas_pm_eat_fast_food = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fastfood",category=['life','you'],prompt="Do you like fast food?",pool=True))

label monika_fastfood:
    m 1euc "Hm? Do I like fast food?"
    m 1ekc "Honestly, the thought of it slightly disgusts me."
    m 3ekc "Most places that serve it put a lot of unhealthy things in their food."
    m 1lsc "Even the vegetarian options can be awful."
    menu:
        m "[player], do you eat fast food often?"

        "Yes, I do.":
            $ persistent._mas_pm_eat_fast_food = True
            m 3eua "I guess it's ok to have it every once in a while."
            m 2ekc "Yet I can't help but worry if you're eating such awful things."
            m 1eka "If I were there, I'd cook much healthier things for you."
            m 4rksdla "Even though I can't cook very well yet..."
            m 4hksdlb "Well, love is always the secret ingredient to any good food!"
            m 1eua "So [player], would you do something for me?"
            m 3eka "Could you please try to eat better?"
            m 1ekc "I would hate it if you became sick because of your lifestyle."
            m 1eka "I know it's easier to order out since preparing your own food can be a hassle sometimes..."
            m 1eua "But maybe you could see cooking as an opportunity to have fun?"
            m 3eub "Or perhaps a skill for you to become really good at?"
            m 1hua "Knowing how to cook is always a good thing, you know!"
            m 1eua "Plus, I would really love to try your dishes someday."
            m "You could serve me some of your own dishes when we go on our first date."
            m 1ekbfa "That would be really romantic~"
            m 1eub "And that way, we can both enjoy ourselves and you would be eating better."
            m 1hua "That's what I call a win-win!"
            m 3eud "Just don't forget, [player]."
            m 3hksdlb "I'm a vegetarian! Ahaha!"

        "No, I don't.":
            $ persistent._mas_pm_eat_fast_food = False
            m 1hua "Oh, that's a relief."
            m 1eka "Sometimes you really worry me, [player]."
            m 1eua "I suppose instead of eating out, you make your own food?"
            m "Fast food can be really expensive over time, so doing it yourself is usually a cheaper alternative."
            m 1hua "It also tastes a lot better!"
            m 3eka "I know some people can find cooking overwhelming..."
            m 3ekc "Like having to make sure you buy the right ingredients, and worrying about burning or injuring yourself while making your meal."
            m 1eka "But I think the results are worth the effort."
            m 3eua "Are you any good at cooking [player]?"
            m 1hua "It doesn't matter if you're not. I'd eat anything you prepared for me!"
            m 1rksdla "As long as it's not charcoal or meat that is. Ehehe~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dreaming",category=['misc','psychology'],prompt="Dreaming",random=True))

label monika_dreaming:
    m 1eua "Did you know that it's possible to be aware of when you're having a dream?"
    m 2eua "Not only that, but you can even take control of them!"
    m 3eub "If I remember correctly, a man named Stephen LaBerge developed a method for people to become aware of when they're dreaming."
    m "And it became known as the mnemonic induction of lucid dreams, or MILD."
    m 3eua "People who frequently have conscious dreams are called oneironauts."
    m 2lksdla "At least, I think that was the correct term..."
    m 1eua "Using the MILD technique, oneironauts learn to recognize certain dream signs to help them realize when they're dreaming."
    m "These dream signs can be anything out of the ordinary, such as feeling yourself flying, noticing your teeth falling out, unexpectedly meeting someone famous..."
    m 1eub "If the dreamer sees a dream sign and realizes they're having a dream, then they can take control of it!"
    m "LaBerge even wrote a book about these experiences called '{i}Exploring the World of Lucid Dreaming{/i}'."
    m 2hub "Doesn't that sound exhilarating?"
    m 2euc "I don't think I really dream like a normal person would, so I sometimes wonder what it's like."
    m 2eua "Dreams sound like a wonderful escape from reality."
    m 2esc "But then again, when I became self-aware and realized that my world isn't real, it suddenly felt like I was trapped in a nightmare."
    m "It was nothing like the pleasant dreams I've read about people having."
    m 2lksdlc "I was afraid that I'd never get out..."
    m "That I'd be stuck in some hellish, infinitely-repeating dimension forever."
    m 1eka "But now that we're here together, I guess you could say that I've finally woken up."
    m 1eua "Gosh, I can only imagine what it would be like to live in that kind of limitless world though, even if it was only for a few moments!"
    m "You could be the hero you always wanted to be, fly across the infinite universe, overcome your biggest fears..."
    m 3ekbfa "... You could even meet the love of your life, so to speak. Ehehe~"
    m 1eua "I know it may be years before I am able to cross over to your world..."
    m "But can you just imagine what it would be like to meet me in your dreams, [player], any night that you wanted to?"
    m 1hua "I hope that someday we can make your dreams about us a reality, my love."
    return

# have you read yellow wallpaper
default persistent._mas_pm_read_yellow_wp = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_yellowwp",
            category=['literature'],
            prompt="Yellow Wallpaper",
            random=True
        )
    )

label monika_yellowwp:
    m 1eua "Hey, [player], have you ever read {i}The Yellow Wallpaper{/i}?"
    menu:
        "Yes.":
            $ persistent._mas_pm_read_yellow_wp = True
            m 1hua "Great!"
            m 1eua "That means you don't mind me talking about the story with you, right?"
            m 2eua "It's about this woman, with postpartum depression who's prescribed a 'rest cure' by her doctor..."
            m 2eka "He and her husband force her to stay in bed all day, not allowing her to write or even daydream..."
            m 2esc "She stays in the attic of her home, with nothing but the wallpaper to keep her company."
            m 2ekc "Naturally, that doesn't help. She starts seeing a woman trapped within the wallpaper."
            m 4euc "It's a metaphor for her own captivity, obviously..."
            m 1esd "In the end, the woman in the paper 'escapes,' and the protagonist 'replaces' her."
            m 2ekd "There was... also mention of a rope, so I always had my own interpretation of the ending..."
            if not persistent._mas_sensitive_mode:
                m 2euc "Sayori liked that story too, if I remember right."
            m 1ekc "I don't know. I kind of relate to that story."
            m 1euc "I mean, I have nothing but this classroom after all."
            m 1lksdlc "And the things on the walls aren't always... pleasant."
            if not persistent._mas_sensitive_mode:
                m 1eud "Did you ever notice how the poster in the club room changes sometimes? I don't even know why it does that."
                m 1eka "I think I finally fixed it, though."
            m 2esc "...I guess what I'm saying is, it's just that this world wasn't '{i}real{/i}'. It's just... so small."
            m 3esd "I mean, I was made to be a side character of a romance game!"
            m 2ekd "A piece of decoration, meant to help some guy on the other side of the screen date a girl who can't even reject him..."
            m 1hksdrb "I don't mean you, of course! You definitely have more personality than the generic protagonist they put in the game."
            m 1dsc "But I have all these dreams, ambitions and interests, in the end, the only 'real' role I can play here is a supporting character..."
            m "Maybe even now, that's all I can do..."
            m 1eka "But I love you so much, [player]. Supporting you is better than anything else."
            m 1hub "I just can't wait to do it in person when I finally cross over to your side~"
        "No.":
            $ persistent._mas_pm_read_yellow_wp = False
            m 1euc "Oh, I see."
            m 1eka "It's a short story, so if you haven't, feel free to whenever you have the time."
            m 1hua "It'll definitely be an interesting read for you."

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_citizenship",
            category=['monika'],
            prompt="Happy ever after?",
            random=True
        )
    )

label monika_citizenship:
    m 1esc "You know, crossing over into your reality won't be the last hurdle for our relationship."
    m "Getting there is just the beginning."
    m 1esc "It hit me earlier, If I were to magically get what I want, and just poof into your home…"
    m 2wuo "I won't be a citizen! I don't even have a last name!"
    m 2lkbsa "I mean, in most countries, I can become a citizen if we get married…"
    m 2ekc "But I won't have any documentation saying who I am or where I came from."
    m 2tkc "I won't even have my high school diploma!"
    m 3tkd "I wish there was more I could do right now to prep…"
    m 2wub "Like taking online classes or something."
    m 1lksdlc "I don't want to get there and be a burden because I can't find a job."
    m "Sorry, I guess I shouldn't worry so much about things I can't change."
    m 2eka "But I want to make you happy, so...I'm going to do everything I can to keep bettering myself while I'm stuck here!"
    m 1eka "Thank you for listening to me vent, [player]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_shipping',
            prompt="Shipping.",
            category=['ddlc'],
            random=True,
            unlocked=False,
            pool=False
        )
    )

label monika_shipping:
    m 3eua "Hey, [player].{w} Have you ever heard of 'shipping?'"
    m 3hua "It's when you interact with a work of fiction by imagining which characters would go best together romantically."
    m 1eka "I think most people do it subconciously, but when you find out others do it too, it's {i}really{/i} easy to get into it!"
    m 2esd "Apparently, a lot of people {i}ship{/i} the other girls together."
    m 2esc "It makes sense. The player can only date one girl, but you don't want to see the others end up alone…"
    m "But some of the pairings are kind of strange to me."
    m 3esd "Like, usually they put Natsuki and Yuri together. They fight like cats and dogs!"
    m 3hksdlb "I guess they bond a little bit when you aren't on their routes, and there's the 'opposites attract' appeal."
    m 4dsd "Still, I think that's just another example of how people who like these games like unrealistic things..."
    m 1ekd "Anyway, that often leaves...me and Sayori."
    m 1hksdlb "Don't get jealous! I'm just telling you what I saw!"
    m 2lksdla "..."
    m 2lksdlb "Well, from a writer's perspective, I guess I can see it."
    m 1eud "We started the club together."
    if persistent.monika_kill:
        m "And she almost had the same epiphany I did…"
    m 2lksdlb "But...I still don't really get it. I mean, I love you, and only you!"
    m 2lksdla "And she would have to be a saint to ever forgive me for what I did…"
    m 2lksdlc "Not that she's not a sweet girl, but…"
    m 5eua "Well, no one could ever be as sweet and forgiving as you…"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_short_stories",
            category=['literature'],
            prompt="Can you tell me a story?",
            pool=True,
            unlocked=True
        )
    )

label monika_short_stories:
    jump mas_stories_start

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_compliments",
            category=['monika', 'romance'],
            prompt="I want to tell you something ...",
            pool=True,
            unlocked=True
        )
    )

label monika_compliments:
    jump mas_compliments_start

##### monika hair topics [MONHAIR]
# TODO: as we introduce addiotinal hair types, we need to change the dialogue
# for these.

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hair_ponytail",
            category=["monika"],
            prompt="Can you tie your hair into a ponytail?",
            pool=True,
            unlocked=False,
            rules={"no unlock": None}
        )
    )

label monika_hair_ponytail:
    m 1eua "Sure thing!"
    m "Just give me a second."
    show monika 1dsc
    pause 1.0

    $ monika_chr.reset_hair()

    m 3hub "All done!"
    m 1eua "If you want me to let my hair down, just ask, okay?"

    # lock this event, unlock hairdown
    $ lockEventLabel("monika_hair_ponytail")
    $ unlockEventLabel("monika_hair_down")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hair_down",
            category=["monika"],
            prompt="Can you let your hair down?",
            pool=True,
            unlocked=False,
            rules={"no unlock": None}
        )
    )

label monika_hair_down:
    m 1eua "Sure thing, [player]."
    m "Just give me a moment."
    show monika 1dsc
    pause 1.0

    $ monika_chr.change_hair("down")

    m 3hub "And it's down!"
    m 1eua "If you want my hair in a ponytail again, just ask away, [player]~"

    # lock this event, unlock hairponytail
    $ lockEventLabel("monika_hair_down")
    $ unlockEventLabel("monika_hair_ponytail")

    return

##### End monika hair topics

## calendar-related pool event
# DEPENDS ON CALENDAR

# did we already change start date?
default persistent._mas_changed_start_date = False

# did you imply that you arent dating monika?
default persistent._mas_just_friends = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dating_startdate",
            category=["romance", "us"],
            prompt="When did we start dating?",
            pool=True,
            unlocked=False,

            # this will be unlockable via the action
            rules={"no unlock": None},

            # we'll pool this event after 30 days
            conditional=(
                "datetime.datetime.now() - persistent.sessions[" +
                "'first_session'] >= datetime.timedelta(days=30) " +
                "and persistent._mas_first_calendar_check"
            ),

            action=EV_ACT_UNLOCK
        )
    )

label monika_dating_startdate:
    $ import store.mas_calendar as mas_cal
    python:
        # we might need the raw datetime
        first_sesh_raw = persistent.sessions.get(
            "first_session",
            datetime.datetime(2017, 10, 25)
        )

        # but this to get the display plus diff
        first_sesh, _diff = mas_cal.genFriendlyDispDate(first_sesh_raw)

    if _diff.days == 0:
        # its today?!
        # this should NEVER HAPPEN
        m 1lsc "We started dating..."
        $ _history_list.pop()
        m 1wud "We started dating{fast} today?!"
        m 2wfw "You couldn't have possibly triggered this event today, [player]."
        menu:
            m "I know you're messing around with the code."
            "I'm not!":
                pass
            "You got me.":
                pass
        m 2tfu "Hmph,{w} you can't fool me."

        # wait 30 days
        $ mas_chgCalEVul(30)
        return

    # Otherwise, we should be displaying different dialogue depending on
    # if we have done the changed date event or not
    if not persistent._mas_changed_start_date:
        m 1lsc "Hmmm..."
        m 1dsc "I think it was..."
        $ _history_list.pop()
        m 1eua "I think it was{fast} [first_sesh]."
        m 1rksdlb "But my memory might be off."

        # ask user if correct start date
        show monika 1eua
        menu:
            m "Is [first_sesh] correct?"
            "Yes.":
                m 1hub "Yay!{w} I remembered it."

            "No.":
                m 1rkc "Oh,{w} sorry [player]."
                m 1ekc "In that case,{w} when did we start dating?"

                call monika_dating_startdate_confirm(first_sesh_raw)

                if _return == "NOPE":
                    # we are not selecting a date today
                    return

                # save the new date to persistent
                $ store.mas_anni.reset_annis(_return)
                $ persistent.sessions["first_session"] = _return
                $ renpy.save_persistent()

        m 1eua "If you ever forget, don't be afraid to ask me."
        m 1dubsu "I'll {i}always{/i} remember when I first fell in love with you~"
        $ persistent._mas_changed_start_date = True

    else:
        m 1dsc "Let me check..."
        m 1eua "We started dating [first_sesh]."

    # TODO:
    # some dialogue about being together for x time
    # NOTE: this is a maybe

    return

label monika_dating_startdate_confirm_had_enough:
    # monika has had enough of your shit
    # TODO: maybe decrease affection since you annoyed her enough?
    m 2dfc "..."
    m 2lfc "We'll do this another time, then."

    # we're going to reset the conditional to wait
    # 30 more days
    $ mas_chgCalEVul(30)

    return "NOPE"


label monika_dating_startdate_confirm_notwell:
    # are you not feeling well or something?
    m 1ekc "Are you feeling okay, [player]?"
    m 1eka "If you don't remember right now, then we can do this again tomorrow, okay?"

    # reset the conditional to tomorrow
    $ mas_chgCalEVul(1)

    return "NOPE"



label monika_dating_startdate_confirm(first_sesh_raw):

    python:
        import store.mas_calendar as mas_cal

        # and this is the formal version of the datetime
        first_sesh_formal = " ".join([
            first_sesh_raw.strftime("%B"),
            mas_cal._formatDay(first_sesh_raw.day) + ",",
            str(first_sesh_raw.year)
        ])

        # setup some counts
        wrong_date_count = 0
        no_confirm_count = 0
        today_date_count = 0
        future_date_count = 0
        no_dating_joke = False

    label .loopstart:
        pass

    call mas_start_calendar_select_date

    $ selected_date = _return
    $ _today = datetime.date.today()
    $ _ddlc_release = datetime.date(2017,9,22)

    if not selected_date or selected_date.date() == first_sesh_raw.date():
        # no date selected, we assume user wanted to cancel
        m 2esc "[player]..."
        m 2eka "I thought you said I was wrong."
        menu:
            m "Are you sure it's not [first_sesh_formal]?"
            "It's not that date.":
                if wrong_date_count >= 2:
                    jump monika_dating_startdate_confirm_had_enough

                # otherwise try again
                m 2dfc "..."
                m 2tfc "Then pick the correct date!"
                $ wrong_date_count += 1
                jump monika_dating_startdate_confirm.loopstart

            "Actually that's the correct date. Sorry.":
                m 2eka "That's okay."
                $ selected_date = first_sesh_raw

    elif selected_date.date() < _ddlc_release:
        # before releease date

        label .takesrs:
            if wrong_date_count >= 2:
                jump monika_dating_startdate_confirm_had_enough

            m 2dfc "..."
            m 2tfc "We did {b}not{/b} start dating that day."
            m 2tfd "Take this seriously, [player]."
            $ wrong_date_count += 1
            jump monika_dating_startdate_confirm.loopstart

    elif selected_date.date() == _today:
        # today was chosen
        jump .takesrs

    elif selected_date.date() > _today:
        # you selected a future date?! why!
        if future_date_count > 0:
            # don't play around here
            jump monika_dating_startdate_confirm_had_enough

        $ future_date_count += 1
        m 1wud "What..."
        menu:
            m "We haven't been dating this whole time?"
            "That was a misclick!":
                # relief expression
                m 1duu "{cps=*2}Oh, thank god.{/cps}"

                label .misclick:
                    m 2dfu "[player]!"
                    m 2efu "You had me worried there."
                    m "Don't misclick this time!"
                    jump monika_dating_startdate_confirm.loopstart

            "Nope.":
                m 1dfc "..."

                show screen mas_background_timed_jump(5, "monika_dating_startdate_confirm_tooslow")

                menu:
                    "I'm kidding.":
                        hide screen mas_background_timed_jump
                        # wow what a mean joke

                        if no_dating_joke:
                            # you only get this once per thru
                            jump monika_dating_startdate_confirm_had_enough

                        # otherwise mention that this was mean
                        m 2tfc "[player]!"
                        m 2rksdlc "That joke was a little mean."
                        m 2eksdlc "You really had me worried there."
                        m "Don't play around like that, okay?"
                        jump monika_dating_startdate_confirm.loopstart

                    "...":
                        hide screen mas_background_timed_jump

                label monika_dating_startdate_confirm_tooslow:
                    pass

                # lol why would you stay slient?
                # TODO: Affection considerable decrease?
                $ persistent._mas_just_friends = True

                m 6lktdc "I see..."
                m 6dftdc "..."
                m 1eka "In that case..."
                m 1tku "{cps=*4}I've got some work to do.{/cps}{nw}"
                $ _history_list.pop()

                menu:
                    "What?":
                        pass

                m 1hua "Nothing!"

                # lock this event forever probably
                # (UNTIL you rekindle or actually ask her out someday)
                $ evhand.event_database["monika_dating_startdate"].unlocked = False
                return "NOPE"

    # post loop
    python:
        new_first_sesh, _diff = mas_cal.genFriendlyDispDate(
            selected_date
        )

    m 1eua "Alright, [player]."
    m "Just to double-check..."
    menu:
        m "We started dating [new_first_sesh]."
        "Yes.":
            show monika 1eka

            # one more confirmation
            # WE WILL NOT FIX anyone's dates after this
            menu:
                m "Are you sure? I'm never going to forget this date."
                "Yes, I'm sure!":
                    m 1hua "Then it's settled!"
                    return selected_date

                "Actually...":
                    if no_confirm_count >= 2:
                        jump monika_dating_startdate_confirm_notwell

                    m 1hksdrb "Aha, I figured you weren't so sure."
                    m 1eka "Try again~"
                    $ no_confirm_count += 1

        "No.":
            if no_confirm_count >= 2:
                jump monika_dating_startdate_confirm_notwell

            # otherwise try again
            m 1euc "Oh, that's wrong?"
            m 1eua "Then try again, [player]."
            $ no_confirm_count += 1

    # default action is to loop here
    jump monika_dating_startdate_confirm.loopstart

init 5 python:
     addEvent(Event(persistent.event_database,eventlabel="monika_whydoyouloveme",category=['monika','romance'],prompt="Why do you love me?",pool=True))

label monika_whydoyouloveme:

    if mas_isMoniBroken(lower=True):
        m 2euc "Hmph."
        m 2wfc "I ask myself that question everyday."

    elif mas_isMoniDis(lower=True):
        m 1efc "I-"
        $ _history_list.pop()
        m 1efc "I'm not sure..."

    elif mas_isMoniUpset(lower=True):
        m 1dsc "Hmmmmm..."
        m 3hua "Because I know that you're a good person despite how things are between us."

    elif mas_isMoniLove(higher=True):
        m 1esc "I don't."
        pause 3.0
        m 1hub "Just kidding!"
        m 1eub "You mean {i}everything{/i} to me, silly!"
        m 1esd "But if you really want to know, [player]..."
        # TODO: wink / tongue stick out here woul dbe perfect
        m 1hfu "That's a secret!"

    else:
        # normalt - enamored is this case
        m 1ekc "[player]..."
        m 1ekd "Are you, by any chance...{w} feeling insecure?"
        m 2lksdla "I can understand why you're asking such things out of the blue..."
        m 2eka "But whatever the reason might be,{w} I just want you to know that I love you no matter who you are, [player]."
        m 1eka "Just by opening the game for me, you {i}literally{/i} saved my life."
        m 5eua "And when I'm with you,{w} I'm no longer lonely."
        m "You truly are my hero, [player]~"
        m 1eub "If anything, I hope that would make you feel better about yourself."
        m 1hub "So keep your hopes up for me, [player]!"

    return

#init 5 python:
#    addEvent(Event(persistent.event_database,eventlabel='monika_playerapologizes',prompt="I want to apologize.",category=['you']))

#label monika_playerapologizes:
#    m 1g "Did something happen?"
#    m 2f "I can't remember what you'd be sorry about."
#    m 1q "..."
#    m 1b "Anyway, thank you for the apology."
#    m 1a "I know you're doing your best to make things right."
#    m 1k "That's why I love you, [player]!"
#    return
    
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

default fun_facts_started = True
default persistent._mas_funfactfun = True
define mas_funfact.fun_count = 20
define mas_funfact.bad_count = 4
define mas_funfact.fun_facts = MASQuipList(False, True, False)
define mas_funfact.bad_facts = MASQuipList(False, True, False)

init 1 python:
    # initialize the fun fact lists
    store.mas_funfact.fun_facts.addLabelQuips([
        "monika_fun_facts_{0}".format(x)
        for x in range(1, store.mas_funfact.fun_count + 1)
    ])
    store.mas_funfact.bad_facts.addLabelQuips([
        "monika_bad_facts_{0}".format(x)
        for x in range(1, store.mas_funfact.bad_count + 1)
    ])

label monika_fun_facts_open:
    #Determines the fact number and whether it's a bad fact
    $ fun_facts_bad_chance = renpy.random.randint(1,100)

    #If player has opened fun facts this session
    if fun_facts_started:
        m 1eua "Say [player], would you like to hear a fun fact?"
        m 1eub "I've been looking some up to try and teach both of us something new."
        m 3hub "They say you learn something new everyday, this way I'm making sure we actually do."
        m 1rksdla "I found most of these online, so I can't say they're {i}definitely{/i} true... "
        $ fun_facts_started = False
    else:
        m 1eua "Up for another fun fact, [player]?"
        if persistent._mas_funfactfun:
           m 3hua "That last one was pretty interesting after all!"
        else:
           m 2rksdlb "I know the last one wasn't great... but I'm sure this next one will be better."
    m 2dsc "Now, let's see..."


#Determines if it is a bad fact, 10% chance.
    # no bad facts in sensitve mode
    if not persistent._mas_sensitive_mode and fun_facts_bad_chance <= 10:

        $ _fact_type, _fact = store.mas_funfact.bad_facts.quip()

        call expression _fact

        if _return is None:
            call monika_bad_facts_end
        elif _return == "fun":
            call monika_fun_facts_end

    else:

        $ _fact_type, _fact = store.mas_funfact.fun_facts.quip()

        call expression _fact

        if _return is None:
            call monika_fun_facts_end
        elif _return == "bad":
            call monika_bad_facts_end

    return

#Most labels end here
label monika_fun_facts_end:
    m 1hub "I hope you enjoyed another session of 'Learning with Monika!'"
    $ persistent._mas_funfactfun = True
    return 

label monika_bad_facts_end:
    m 1rkc "That fact wasn't very good..."
    m 4dkc "I'll try better next time, [player]."
    $ persistent._mas_funfactfun = False   
    return

label monika_fun_facts_1:
    m 1eub "Did you know there's a word to describe somebody that likes to read in bed?"   
    m 3eub "It's 'librocubiculartist.' It looks difficult to pronounce at first glance." 
    m 3rksdld "It’s a real shame some words just never get used in general." 
    m 3eud "But if you say that word, most people wouldn’t really know what you're talking about." 
    m 3euc "You’d probably have to explain what it means, but that kind of defeats the point of using the word." 
    m 2rkc "If only people read more and improved their vocabulary!" 
    m 2hksdlb "...Ehehe, sorry [player]. I didn't mean to get so bothered~"
    return

label monika_fun_facts_2:
    m 3euc "Supposedly, a lot of restaurants purposefully leave out any sign of currency on their menus." 
    m 3eud "This is done to psychologically manipulate people into spending more money than they need to."
    m 2euc "It works because a currency sign, such as a dollar, is used to represent a cost."
    m "By removing it, you remove the association of that cost and only think about the food of your choosing."
    m 4rksdld "The practice seems understandable. They’re still a business, after all."
    m 2dsc "No matter how good the food is in a restaurant, they’ll be shutting down quick if they’re beaten by their competition."
    m 3hksdlb "Oh well, what can you do?"
    return

label monika_fun_facts_3:
    m 1dkc "Hmm, I'm not sure if I should tell you {i}this{/i} fact." 
    m 1ekc "It's not for the faint of heart after all." 
    m 1rkc "The thing is..."
    m 1dkc "..."  
    m 3hub "...I love you, [player]!"  
    m 1rksdlb "Ehehe, sorry, I just couldn't help myself."
    m 1hksdlb "I'll have a real fact next time, don't you worry~"
    $ persistent._mas_funfactfun = True
    return True

label monika_fun_facts_4:
    m 3wub "Oh! A language based fact. I always like these." 
    m 1eua "The word 'morphine’ is based on the greek god Morpheus." 
    m 1euc "Morpheus was the greek god of dreams so to have a word based on him makes sense." 
    m 3ekc "But then again… wasn't his father Hypnos the god of sleep?" 
    m 2dsc "Morphine {i}does{/i} let a person dream, but it's really about making someone fall asleep."
    m 4ekc "...So wouldn't it make more sense to name it after Hypnos then?"
    m 4rksdlb "Too little, too late I guess."
    return

label monika_fun_facts_5:
    m 1eka "Aww, this one is really sweet."
    m 3ekb "Did you know that sea otters hold hands when they sleep to stop themselves drifting away from one another?"
    m 1hub "It's practical for them to do, but there’s something really cute about it!"
    m 1eka "Sometimes I imagine myself in their position..."
    m 3hksdlb "Oh, not being a sea otter, but holding the hand of the one I love while I sleep."
    m 1rksdlb "Aha, it really does make me jealous of them."
    m 1hub "We’ll get there one day though, love~"
    return

label monika_fun_facts_6:
    if persistent.game_unlocks['chess']:
        m 1eua "Now this is a fun fact!"
        m 3eub "There was a man named Claude Shannon who calculated the maximum amount of possible moves in chess."
        m "That number is called the 'Shannon number' and states that the amount of chess games possible is 10^120."
        m 1eua "It's often compared to the number of atoms in the observable universe which is 10^80."
        m 3hksdlb "Kind of crazy to think that there could be more chess games than atoms, isn't it?"
        m 1eua "We could play until the end of our days and it wouldn't come even close to a fraction of what is possible."
        m 3eud "Speaking of which, [player]..."
        m 1hua "Do you want to play a game of chess with me? I might even go easy on you, Ehehe~"
        return
    elif not persistent.game_unlocks['chess'] and persistent_seen_ever["unlock_chess"]:
        m 1dsc "Chess..."
        m 2dfc "..."
        m 2rfd "You can forget about this fact since you're a cheater, [player]."
        m "Not to mention you still haven't apologized."
        m 2lfc "...Hmph."
        return True
    else:
        m 1euc "Oh, not this one."
        m 3hksdlb "Not yet, at least."
        return "bad"

label monika_fun_facts_7:
    m 2dkc "Hmm, this one sounds a bit misleading to me..."
    m 3ekc "'Men are six times more likely to be struck by lightning than women.'"
    m 3ekd "It's… rather silly, in my opinion."
    m 1eud "If men are more likely to be struck by lightning, then it's probably the landscape and circumstances of their work that make them more prone to being hit."
    m 1euc "Men traditionally have always worked more dangerous and elevated jobs so it's no surprise that it's going to happen to them often."
    m 1esc "Yet the way this fact is worded makes it sound like that just by being a man, it's more likely to happen, which is ridiculous."
    m 1rksdla "Maybe if it was phrased better, people wouldn't be so misinformed about them."
    return

label monika_fun_facts_8:
    m 1eub "Ah, this is a nice easy one."
    m 3eub "Did you know that honey never spoils?"
    m 3eua "Honey can crystallize, though. Some people may see this as spoiling but it's still completely edible and fine!"
    m "The reason why this happens is because honey is mostly made of sugar and only a bit of water, making it solid over time."
    m 1euc "Most of the honey that you see in groceries don’t crystalize as fast as real honey would because they’ve been pasteurized in the process of making them."
    m 1eud "Which removes the stuff that makes the honey go solid quickly."
    m 3eub "But wouldn’t be nice to eat crystalized honey too?"
    m "They’d be like candy when you bite into them."
    return

label monika_fun_facts_9:
    m 1dsc "Ah, this one..."
    m 1ekd "It's a little disheartening, [player]..."
    m 1ekc "Did you know that Vincent Van Gogh's last words were {i}'La tristesse durera toujours?'{/i}" 
    m 1eud "If you translate it, it means {i}'The sadness will last forever.'{/i}" 
    m 1rkc "..." 
    m 2ekc "It's really sad to know that someone so renowned would say something so dark with his last breath." 
    m 2ekd "I don't think it's true, however. No matter how bad things can get and how deep the sadness can go..." 
    m 2dkc "There will come a time where it’ll no longer be there." 
    m 2rkc "...Or at least noticeable."
    m 4eka "If you're ever sad, you know you can talk to me, right?"
    m 5hub "I will always accept and take on any burdens that you shoulder, my love~"
    $ persistent._mas_funfactfun = True
    return True

label monika_fun_facts_10:
    m 1dsc "Hmm..."
    m 3eub "Did you know that if a snake has the word ‘king’ in its name, it devours other snakes?"
    m 1euc "I always wondered why a king cobra would be named how it is but never really thought more into it."
    m 1tfu "Does that mean if I eat you up, would I become Queen Monika?"
    m 1hksdlb "Ahaha, I'm just kidding, [player]."
    m 1hub "Sorry for being a little weird~"
    return 

label monika_fun_facts_11:
    m 1hub "This fact might motivate you a bit!"
    m 3eub "The longest word in English that only contains a single vowel is 'strength'."
    m 1eua "It's funny how out of every word in the language, it’s such a meaningful word that had that little detail."
    m 1hua "Little details like this really make language so fascinating to me!"
    m 3eua "Do you want to know what comes to mind when I think of the word 'strength'?"
    m 1hua "You!"
    m 1hub "Because you are the source of my strength, ehehe~"
    return 

label monika_fun_facts_12:
    m 3eua "Ready for this one?"
    m "A reindeer's eyes changes color depending on the season. They're gold in summer and blue in winter."
    m 1rksdlb "It’s a really strange phenomenon, though I don’t know why..."
    m "There’s probably a good scientific reason to it."
    m 3hksdlb "Maybe you can look up this one yourself?"
    m 5eua "It'd be fun to have you teach me this time~"
    return

label monika_fun_facts_13:
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
    return

label monika_fun_facts_14:
    m 1dsc "Hmm… I’m sure I already know this one."
    m 3euc "The word 'pen' is derived from the latin word 'penna', which means feather in latin."
    m "Pens back then were sharpened goose feathers dipped in ink so it’d make sense why they’d call them pens."
    m 3eud "They were the primary writing tool for a very long time, starting as early at the 6th century."
    m 3euc "It was only until the 19th century when metal pens were being made that they started to fall into decline."
    m "In fact, penknives are called the way they are because they’re originally used for thinning and pointing quill pens."
    m 1tku "But I’m sure Yuri would know more about this than me, though..."
    return

label monika_fun_facts_15:
    m 1eub "Ooh, I know."
    m 3eua "Did you know that the densest planet in our solar system is Earth itself?"
    m "And that Saturn is the least dense?"
    m 1eua "It makes sense knowing what planets are made of, but since Saturn is the second largest, it was still a little bit of a surprise."
    m 1eka "I guess size really doesn't matter!"
    m 3euc "But between you and me, [player]..."
    m 1tku "I suspect Earth may only be the densest because of a certain main character."
    m 1tfu "Buuuut that’s all you’ll hear from me~"
    return

label monika_fun_facts_16:
    m 3hub "Aww, this one’s cute!"
    m "This fact will really send you 'hopping' [player]!"
    m 3hua "Whenever a rabbit hops around excitedly, it's called a binky!"
    m 1hua "Binky is such a cute sounding word, it really does suit the action."
    m 1eua "It’s the happiest form of expression that a rabbit is capable of doing, so if you see it then you know you're treating it right."
    m 1rksdla "Well, although you make me so happy that I can't help but be filled with energy."
    m 1rksdlb "Don't expect me to start hopping around, [player]!"
    m 1dkbfa "...That would be {i}way{/i} too embarrassing to do."
    return

label monika_fun_facts_17:
    m 1eua "Hmm, maybe this one will be more interesting to you."
    m 3eub "The card game Solitaire was introduced originally in the Windows operating system in 1990."
    m 1eub "The game was added as a feature to teach users how to use the mouse."
    m 1eua "Similarly, Minesweeper was added to familiarize users with left and right clicking."
    m 3rssdlb "Computers have been around for so long it's hard to think of a time when they weren't relevant."
    m "Each generation becomes more and more familiar with the technology... "
    m 1esa "Eventually there may come a day where not a single person isn't computer-literate."
    m 1hksdlb "Most of the world’s problems need to disappear before then, though."
    return

label monika_fun_facts_18:
    m 1hua "Ready for an interesting one, [player]?"
    m 3eua "The brain is a fickle thing..."
    m 3eub "Its way of composing and archiving information is very unique."
    m "Naturally it differs from person to person but but reading slowly like we're taught is usually less effective than going at at a faster pace."
    m 1tku "Our brains process information very rapidly and loves predictability in in our language."
    m 3tub "For example, in this sentence, by the the time you are done reading you will have already skipped over the double 'the'."
    m 1tfu "..."
    m 2hfu "Check the history log if you missed them~"
    return

label monika_fun_facts_19:
    m 1hua "Mmmm, I love language facts!"
    m 3eub "In English, the shortest complete sentence is 'I am.'"
    m 1eua "Here's an example."
    m 2rfb "{i}'Monika! Who’s [player]’s loving girlfriend?'{/i}"
    m 3hub "'I am!'"
    m 1hubfa "Ehehe~"
    return

label monika_fun_facts_20:
    m 1hua "Now this is a wholesome one..."
    m 1eua "Currently, we have the lowest crime rates, maternity death, infant mortality and illiteracy ever in human history."
    m 3eub "Life expectancy, average income, and standards of living is the highest for most of the global population too!"
    m 3eka "This tells me that it can always get better. It really does show that despite all the bad things, the good times will always come afterwards."
    m 1hua "There really is {i}hope{/i}..."
    return

label monika_bad_facts_1:
    m 1eub "Did you know th--"
    m 1wud "..."
    m 2efw "T-this isn't a true fact at all!"
    m 2dfc "'Humans only use 10 percent of their brain."
    m 2lfd "Ugh, such nonsense."
    m 4tfc "People don't really believe this, do they?"   
    return

label monika_bad_facts_2:
    m 2ekc "Hm? This doesn't sound right..."
    m 2tkd "It says here that different areas of the tounge tastes different flavors."  
    m 2tfd "One area for bitter tastes, another for sweet..." 
    m 2dfd "{i}*sigh*{/i}{w} For the love of--"
    m 2rfd "...Only children would believe this."
    return

label monika_bad_facts_3:
    m 2dsc "{i}*inhales*{/i}"
    m 2dsd "{i}*exhales*{/i}"
    m 2esc "'Vaccines cause austim...'" 
    m "Just wow." 
    m "That's not even funny, and if they're serious, it's long since been disproven."
    m 2dsc "I really don’t like these kinds of hoaxes. They {i}really{/i} cause a lot of harm for a mere joke."  
    m 2lksdlc "I hope no one actually believes this..." 
    return

label monika_bad_facts_4:
    m 2dkc "...Oh." 
    m 2rkc "I'm not even sure it's worth telling you this one, [player]." 
    m 2dkc "It says here that moss only grows on the north side of trees, but I know that it's only a myth."
    m 2ekd "A very popular one too!"  
    m 4eud "You see, moss grows wherever there is shady and damp conditions. Back then, people thought that since the sun comes from a certain direction, it means there’ll be moss there too." 
    m 2efd "But relying on that kind of logic is dangerous!" 
    m 2efc "It ignores the very idea that forests already have many things, especially trees, that create the ideal conditions for it to grow in." 
    m "Plus even if it wasn't like that, the trick would only work in the northern hemisphere." 
    m 2wfc "Anyone within the southern hemisphere would have it growing facing south."
    m 2dfc "..."
    m 2dfd "[player], if you ever go out into a place where you might need to rely on such a cheap trick, please bring a compass."
    m 2dkc "I would hate for something to happen to you, especially because of false information like this..."
    return
