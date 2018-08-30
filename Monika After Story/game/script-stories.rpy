# Module for Monika story telling
#
# Stories will get unlocked one at by session
# The unlocking logic has been added to script-ch30
# The topic that triggers the Story menu is monika_short_stories
# Topic is unlocked at the beginning of the game and is not
# random


# dict of tples containing the stories event data
default persistent._mas_story_database = dict()
default mas_can_unlock_story = False


# store containing stories-related things
init -1 python in mas_stories:

    # pane constants
    STORY_X = 680
    STORY_Y = 40
    STORY_W = 450
    STORY_H = 640
    STORY_XALIGN = -0.05
    STORY_AREA = (STORY_X, STORY_Y, STORY_W, STORY_H)
    STORY_RETURN = "I changed my mind"
    story_database = dict()


# entry point for stories flow
label mas_stories_start:

    python:
        import store.mas_stories as mas_stories

        # build menu list
        stories_menu_items = [
            (mas_stories.story_database[k].prompt, k, False, False)
            for k in mas_stories.story_database
            if mas_stories.story_database[k].unlocked and seen_event(k)
        ]

        # sanity check for first timers
        if not stories_menu_items:
            stories_menu_items = [
                (mas_stories.story_database[k].prompt, k, False, False)
                for k in mas_stories.story_database
                if mas_stories.story_database[k].unlocked
            ]

            # set the mas_can_unlock_story flag to False since it
            # shouldn't unlock anything at this time
            mas_can_unlock_story = False

        # check if we have a story available to be unlocked and we can unlock it
        if len(stories_menu_items) < len(mas_stories.story_database) and mas_can_unlock_story:

            # Add to the menu the new story option
            stories_menu_items.append(("A new story", "mas_story_unlock_random", True, False))

        # also sort this list
        stories_menu_items.sort()

        # final quit item
        final_item = (mas_stories.STORY_RETURN, False, False, False, 20)

    # if we have only one story
    if len(stories_menu_items) == 1:

        # get the event label
        $ story = stories_menu_items[0][1]

        # check if we have seen it already
        if seen_event(story):
            m 1ekc "Sorry [player], that's the only story I can tell you right now"
            m 1lksdlb "I'll think of a story to tell you next time"
            return

        # increment event's shown count and update last seen
        $ mas_stories.story_database[story].shown_count += 1
        $ mas_stories.story_database[story].last_seen = datetime.datetime.now()

        # and we jump to it, since doing pushEvent looks weird
        $ renpy.jump(story)

    m 1hua "Sure thing!"
    m 1eua "What story would you like to hear?"

    # move Monika to the left
    show monika at t21

    # call scrollable pane
    call screen mas_gen_scrollable_menu(stories_menu_items, mas_stories.STORY_AREA, mas_stories.STORY_XALIGN, final_item=final_item)

    # return value?
    if _return:

        # NOTE: call_next_event now properly records shown_count and last_seen
        #check if it's an actual story
#        if _return in mas_stories.story_database:

            # track show_count stats
#            $ mas_stories.story_database[_return].shown_count += 1
#            $ mas_stories.story_database[_return].last_seen = datetime.datetime.now()

        # then push
        $ pushEvent(_return)

    # move her back to center
    show monika at t11
    return

# Stories start here
label mas_story_begin:
    python:
        story_begin_quips = [
            "Alright, let's start the story.",
            "Ready to hear the story?",
            "Ready for story time?",
            "Let's begin~",
            "Let's begin then~"
        ]
        story_begin_quip=renpy.random.choice(story_begin_quips)
    $ mas_gainAffection(modifier=0.2)
    m 3eua "[story_begin_quip]"
    m 1duu "Ahem."
    return

label mas_story_unlock_random:

    python:

        # reset flag so we don't unlock another one
        mas_can_unlock_story = False

        # get locked stories
        stories = renpy.store.Event.filterEvents(
            renpy.store.mas_stories.story_database,
            unlocked=False
        )

        if len(stories) == 0:

            # in case the player left the game mid unlocking
            stories = renpy.store.Event.filterEvents(
                renpy.store.mas_stories.story_database,
                unlocked=True,
                seen=False
            )

            if len(stories) == 0:

                # There should be no way to get to this point but just in case
                # let's fail 'nicely'
                stories = renpy.store.Event.filterEvents(
                    renpy.store.mas_stories.story_database,
                    unlocked=True
                )


        # select one story randomly
        story = stories[renpy.random.choice(stories.keys())]

        # unlock the story
        story.unlocked = True

        # increment event's shown count and update last seen
        story.shown_count += 1
        story.last_seen = datetime.datetime.now()

        # using renpy.jump again cause again trasition looks like she's stuck
        renpy.jump(story.eventlabel)


    return


init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_tyrant",
        prompt="The Cat and the Cock",unlocked=True),eventdb=store.mas_stories.story_database)

label mas_story_tyrant:
    call mas_story_begin
    m 1eua "A Cat caught a Cock and thought about reasonable excuses for eating him."
    m "He accused him of being a nuisance by crowing at night; not letting men sleep."
    m 3eud "The Cock defended his action by saying this was for the benefit of men, as it wakes them for labor."
    m 1tfb "The Cat replied, 'you abound in apologies, but it's time for breakfast.'"
    m 1hksdrb "At that he made a meal of the Cock."
    m 3eua "The moral of this story is that: 'Tyrants need no excuse'."
    m 1hua "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_despise",
        prompt="The Fox",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_despise:
    call mas_story_begin
    m 1eud "One hot summer's day, a Fox was strolling through an orchard till he came to a bunch of grapes just ripening on a vine which had been trained over a lofty branch."
    m 1tfu "'Just the thing to quench my thirst,' said the Fox."
    m 1eua "Drawing back a few paces, he took a run and a jump, and just missed the bunch."
    m 3eub "Turning round again with a one,{w=1.0} two,{w=1.0} three,{w=1.0} he jumped up, but with no greater success."
    m 3tkc "Again and again he tried after the tempting morsel, but at last had to give it up, and walked away with his nose in the air, saying: 'I am sure they are sour.'"
    m 1hksdrb "The moral of this story is that: 'It is easy to despise what you cannot get'."
    m 1eua "I hope you liked it, [player]~"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_lies",
        prompt="The Shepherd Boy and the Wolf",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_lies:
    call mas_story_begin
    m 1euc "There was a Shepherd Boy who tended his sheep at the foot of a mountain near a dark forest."
    m 1lsc "It was lonely for him, so he devised a plan to get a little company."
    m 4hfw "He rushed down towards the village calling out 'Wolf! Wolf!' and the villagers came out to meet him."
    m 1hksdrb "This pleased the boy so much that a few days after he tried the same trick, and again the villagers came to his help."
    m 3wud "Shortly after, a Wolf actually did come out from the forest."
    m 1ekc "The boy cried out 'Wolf, Wolf!' still louder than before."
    m 4efd "But this time the villagers, who had been fooled twice before, thought the boy was again lying, and nobody came to his aid."
    m 2dsc "So the Wolf made a good meal of the boy's flock."
    m 2esc "The moral of this story is that: 'Liars are not believed even when they speak the truth'."
    m 1hksdlb "You shouldn't worry about it, [player]..."
    m 3hua "You'd never lie to me, right?"
    m 1hub "Ehehe~"
    m 1eua "I hope you enjoyed the story, [player]!"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_grasshoper",
        prompt="The Grasshopper",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_grasshoper:
    call mas_story_begin
    m 1eua "One summer's day, a Grasshopper was hopping about, chirping and singing to its heart's content."
    m "An Ant passed by, bearing an ear of corn he was taking to the nest."
    m 3eud "'Why not come and chat with me,' said the Grasshopper, 'instead of toiling in that way?'"
    m 1efc "'I am helping to lay up food for the winter,' said the Ant, 'and recommend you do the same.'"
    m 1hfb "'Why bother about winter?' said the Grasshopper; 'we have plenty of food now!'"
    m 3eua "The Ant went on its way."
    m 1dsc "When winter came, the Grasshopper had no food and found itself dying of hunger, while it saw the ants distributing corn and grain from the stores they had collected in the summer."
    m 3hua "The moral of this story is that: 'There's a time for work and a time for play'."
    m 1dubsu "But there's always a time to spend with your cute girlfriend~"
    m 1hub "Ehehe, I love you so much, [player]!"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_wind_sun",
        prompt="The Wind and the Sun",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_wind_sun:
    call mas_story_begin
    m 1dsc "The Wind and the Sun were disputing which was the strongest."
    m 1euc "Suddenly they saw a traveller coming down the road, and the Sun said: 'I see a way to decide our dispute.'"
    m 3efd "'Whichever of us can cause that traveller to take off his cloak shall be regarded as the strongest. You begin.'"
    m 3euc "So the Sun retired behind a cloud, and the Wind began to blow as hard as it could upon the traveller."
    m 1ekc "But the harder he blew the more closely did the traveller wrap his cloak around him, till at last the Wind had to give up in despair."
    m 1euc "Then the Sun came out and shone in all his glory upon the traveller, who soon found it too hot to walk with his cloak on."
    m 3hua "The moral of this story is that: 'Gentleness and kind persuasion win where force and bluster fail.'"
    m 1hub "Hope you had fun, [player]."
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_seeds",
        prompt="The seeds",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_seeds:
    call mas_story_begin
    m 1euc "It happened that a Countryman was sowing some hemp seeds in a field where a Swallow and some other birds were hopping about picking up their food."
    m 1tfd "'Beware of that man,' quote the Swallow."
    m 3eud "'Why, what is he doing?' asked the others."
    m 1tkd "'That is hemp seed he is sowing; be careful to pick up every one of the seeds, or else you will repent it.' The Swallow replied."
    m 3rksdld "The birds paid no heed to the Swallow's words, and by and by the hemp grew up and was made into cord, and of the cords nets were made."
    m 1euc "Many birds that had despised the Swallow's advice were caught in nets made out of that very hemp."
    m 3hfu "'What did I tell you?' said the Swallow."
    m 3hua "The moral of this story is: 'Destroy the seeds of evil before they grow up to be your ruin.'"
    m 1lksdlc "..."
    m 2dsc "I wish I could've followed that moral."
    m 2lksdlc "You wouldn't had to go through what you saw."
    m 4hksdlb "Anyway, I hope you liked the story, [player]!"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_gray_hair",
        prompt="The gray hair",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_gray_hair:
    call mas_story_begin
    m 1eua "In the old days, a middle-aged Man had one wife that was old and one that was young; each loved him and desired nothing more than to earn his affection."
    m 1euc "The Man's hair was turning grey, which the young Wife did not like, as it made him look too old."
    m 3rksdla "So, every night she picked out the white hairs."
    m 3euc "But, the elder Wife did not like to be mistaken for his mother."
    m 1eud "So, every morning she picked out as many of the black hairs as she could."
    m 3hksdlb "The Man soon found himself entirely bald."
    m 1hua "The moral of this story is that: 'Yield to all and you will soon have nothing to yield'."
    m 1hub "So before you give everything, make sure you still have some for yourself!"
    m 1lksdla "...Not that being bald is bad, [player]."
    m 1hksdlb "Ehehe, I love you~!"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_fisherman",
        prompt="The fisherman",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_fisherman:
    call mas_story_begin
    m 1euc "A poor Fisherman, who lived on the fish he caught, had bad luck one day and caught nothing but a very small fry."
    m 1eud "The Fisherman was about to put it in his basket when the little Fish spoke."
    m 3ekd "'Please spare me, Mr. Fisherman! I am so small it is not worth while to carry me home. When I am bigger, I shall make you a much better meal!'"
    m 1eud "But the Fisherman quickly put the fish into his basket."
    m 3tfu "'How foolish I should be,' he said, 'to throw you back. However small you may be, you are better than nothing at all.'"
    m 3esa "The moral of this story is that: 'A small gain is worth more than a large promise'."
    m 1hub "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_ravel",
    prompt="Old man's three wishes",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_ravel:
    call mas_story_begin
    m 3euc "Once, an elderly man was sitting alone on a dark path."
    m 1euc "He had forgotten both where he was traveling to, and who he was."
    m "Suddenly, he looked up to see an elderly woman before him."
    m 1tfu "She grinned toothlessly and with a cackle, spoke: 'Now your *third* wish. What will it be?'"
    m 3eud "'Third wish?' The man was baffled. 'How can it be a third wish if I haven't had a first and second wish?'"
    m 1tfd "'You've had two wishes already,' the hag said, 'but your second wish was for me to return everything to the way it was before you had made your first wish.'"
    m 3tku "'That's why you remember nothing: because everything is the way it was before you made any wishes.'"
    m 1dsd "'All right,' said the man, 'I don't believe this, but there's no harm in wishing. I wish to know who I am.'"
    m 1tfb "'Funny,' said the old woman as she granted his wish and disappeared forever. 'That was your first wish.'"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_immortal_love",
        prompt="Love Never Ends",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_immortal_love:
    call mas_story_begin
    m 3eua "There was a married couple who lived happily together for many years."
    m "Every Valentine's Day, the husband would have a beautiful bouquet of flowers sent to his wife."
    m 1eka "Each of these bouquets came with a note with a few simple words written on it."
    m 3dsc "{i}My love for you only grows.{/i}"
    m 1eud "After some time, the husband passed away."
    m 1eka "The wife, saddened by her loss, believed she would spend her next Valentine's Day alone and in mourning."
    m 1dsc "..."
    m 2euc "However,{w} on her first Valentine's Day without her husband, she still received a bouquet from him."
    m 2efd "Heartbroken and angry, she complained to the florist that there was a mistake."
    m 2euc "The florist explained that there was no mistake."
    m "The husband had ordered many bouquets in advance to ensure that his beloved wife would continue to receive flowers long after his death."
    m "Speechless and stunned, the wife read the note attached to the bouquet."
    m "{i}My love for you is eternal.{/i}"
    
    m 1dubsu "Ahh..."
    m 1eua "Wasn't that a touching story, [player]?"
    m 1hua "I thought it was really romantic."
    m 1lksdlb "But I don't want to think of either of us dying."
    m 1eua "At least the ending was very heartwarming."
    m 1hua "Thanks for listening~"
    return
