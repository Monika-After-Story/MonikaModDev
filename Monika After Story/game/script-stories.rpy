# Module for Monika story telling
#
# Stories will get unlocked one at by session
# The unlocking logic has been added to script-ch30
# The topic that triggers the Story menu is monika_short_stories
# Topic is unlocked at the beginning of the game and is not
# random


# dict of tples containing the stories event data
default persistent.story_database = dict()


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
    show monika at t21
    python:
        import store.mas_stories as mas_stories

        # build menu list
        stories_menu_items = [
            (mas_stories.story_database[k].prompt, k, not seen_event(k), False)
            for k in mas_stories.story_database
            if mas_stories.story_database[k].unlocked
        ]

        # also sort this list
        stories_menu_items.sort()

        # final quit item
        final_item = (mas_stories.STORY_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(stories_menu_items, mas_stories.STORY_AREA, mas_stories.STORY_XALIGN, final_item=final_item)

    # return value? then push
    if _return:
        $ pushEvent(_return)

    show monika at t11
    return _return

# Stories start here
init 5 python:
    addEvent(Event(persistent.story_database,eventlabel="story_tyrant",
        prompt="The cat and the cock",unlocked=True),eventdb=store.mas_stories.story_database)

label story_tyrant:
    m "Alright let's start the story."
    m "Ahem."
    m "A Cat caught a Cock and thought about reasonable excuses for eating him."
    m 1r "He accused him of being a nuisance by crowing at night; not letting men sleep."
    m 1 "The Cock defended his action by saying this was for the benefit of men, as it wakes them for labor."
    m 1k "The Cat replied, “you abound in apologies, but it’s time for breakfast.”"
    m "At that he made a meal of the Cock."
    m "The moral of this story is that: 'Tyrants need no excuse'."
    m "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.story_database,eventlabel="story_despise",
        prompt="The Fox",unlocked=False),eventdb=store.mas_stories.story_database)

label story_despise:
    m "Ready for story time?"
    m "Ahem."
    m "One hot summer’s day a Fox was strolling through an orchard till he came to a bunch of Grapes just ripening on a vine which had been trained over a lofty branch."
    m 1r "“Just the thing to quench my thirst,” quoth he."
    m 1 "Drawing back a few paces, he took a run and a jump, and just missed the bunch."
    m 1k "Turning round again with a One, Two, Three, he jumped up, but with no greater success."
    m "Again and again he tried after the tempting morsel, but at last had to give it up, and walked away with his nose in the air, saying: “I am sure they are sour.”"
    m "The moral of this story is that: 'It is easy to despise what you cannot get'."
    m "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.story_database,eventlabel="story_lies",
        prompt="The Shepherd Boy and the wolf",unlocked=False),eventdb=store.mas_stories.story_database)

label story_lies:
    m "Ready to hear a story?"
    m "Ahem."
    m "There was a Shepherd Boy who tended his sheep at the foot of a mountain near a dark forest."
    m 1r "It was lonely for him, so he devised a plan to get a little company."
    m 1 "He rushed down towards the village calling out “Wolf, Wolf,” and the villagers came out to meet him."
    m 1k "This pleased the boy so much that a few days after he tried the same trick, and again the villagers came to his help."
    m "Shortly after this a Wolf actually did come out from the forest."
    m "The boy cried out “Wolf, Wolf,” still louder than before."
    m "But this time the villagers, who had been fooled twice before, thought the boy was again lying, and nobody came to his aid."
    m "So the Wolf made a good meal off the boy’s flock."
    m "The moral of this story is that: 'Liars are not believed even when they speak the truth'."
    m "You shouldn't worry about it, [player]"
    m "I know you would never lie to me"
    m "Ehehe~"
    m "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.story_database,eventlabel="story_grasshoper",
        prompt="The Grasshopper",unlocked=False),eventdb=store.mas_stories.story_database)

label story_grasshoper:
    m 3 "Let's begin then~"
    m "Ahem."
    m "One summer’s day a Grasshopper was hopping about, chirping and singing to its heart’s content."
    m 1r "It was lonely for him, so he devised a plan to get a little company."
    m 1 "An Ant passed by, bearing an ear of corn he was taking to the nest."
    m 1k "“Why not come and chat with me,” said the Grasshopper, “instead of toiling in that way?”"
    m "“I am helping to lay up food for the winter,” said the Ant, “and recommend you do the same.”"
    m "“Why bother about winter?” said the Grasshopper; “we have plenty of food now.”"
    m "The Ant went on its way."
    m "When winter came the Grasshopper had no food and found itself dying of hunger, while it saw the ants distributing corn and grain from the stores they had collected in the summer."
    m "The moral of this story is that: 'There’s a time for work and a time for play'."
    m "And there's also a time to spend with your cute girlfriend~"
    m "I love you so much, [player]!"
    m "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.story_database,eventlabel="story_wind_sun",
        prompt="The Wind and the Sun",unlocked=False),eventdb=store.mas_stories.story_database)

label story_wind_sun:
    m 3 "Ready for story time?"
    m "Ahem."
    m "The Wind and the Sun were disputing which was the strongest."
    m 1 "Suddenly they saw a traveller coming down the road, and the Sun said: “I see a way to decide our dispute. Whichever of us can cause that traveller to take off his cloak shall be regarded as the strongest. You begin.”"
    m 1k "So the Sun retired behind a cloud, and the Wind began to blow as hard as it could upon the traveller."
    m "But the harder he blew the more closely did the traveller wrap his cloak round him, till at last the Wind had to give up in despair."
    m "Then the Sun came out and shone in all his glory upon the traveller, who soon found it too hot to walk with his cloak on."
    m "The moral of this story is that: 'Gentleness and kind persuasion win where force and bluster fail'."
    m "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.story_database,eventlabel="story_seeds",
        prompt="The seeds",unlocked=False),eventdb=store.mas_stories.story_database)

label story_seeds:
    m 3 "Sure thing!"
    m "Ahem."
    m "It happened that a Countryman was sowing some hemp seeds in a field where a Swallow and some other birds were hopping about picking up their food."
    m 1 "“Beware of that man,” quoth the Swallow."
    m 1k "“Why, what is he doing?” said the others."
    m "“That is hemp seed he is sowing; be careful to pick up every one of the seeds, or else you will repent it.” The Swallow replied."
    m "The birds paid no heed to the Swallow’s words, and by and by the hemp grew up and was made into cord, and of the cords nets were made, and many birds that had despised the Swallow’s advice were caught in nets made out of that very hemp."
    m 1k "“What did I tell you?” said the Swallow."
    m "The moral of this story is that: 'Destroy the seeds of evil before they grow up to your ruin'."
    m "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.story_database,eventlabel="story_gray_hair",
        prompt="The gray hair",unlocked=False),eventdb=store.mas_stories.story_database)

label story_gray_hair:
    m 3 "Let's begin~"
    m "Ahem."
    m "In the old days, a middle-aged Man had one wife that was old and one that was young; each loved him and desired to see him like herself."
    m 1 "The Man’s hair was turning grey, which the young Wife did not like, as it made him look too old."
    m 1k "So, every night she picked out the white hairs."
    m "But, the elder Wife did not like to be mistaken for his mother."
    m "So, every morning she picked out as many of the black hairs as she could."
    m 1k "The Man soon found himself entirely bald."
    m "The moral of this story is that: 'Yield to all and you will soon have nothing to yield'."
    m "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.story_database,eventlabel="story_fisherman",
        prompt="The fisherman",unlocked=False),eventdb=store.mas_stories.story_database)

label story_fisherman:
    m 3 "Let's begin~"
    m "Ahem."
    m "A poor Fisherman, who lived on the fish he caught, had bad luck one day and caught nothing but a very small fry."
    m 1 "The Fisherman was about to put it in his basket when the little Fish said:"
    m 1k "“Please spare me, Mr. Fisherman! I am so small it is not worth while to carry me home. When I am bigger, I shall make you a much better meal.”"
    m "But the Fisherman quickly put the fish into his basket."
    m "So, every morning she picked out as many of the black hairs as she could."
    m 1k "“How foolish I should be,” he said, “to throw you back. However small you may be, you are better than nothing at all.”"
    m "The moral of this story is that: 'A small gain is worth more than a large promise'."
    m "I hope you enjoyed this little story, [player]~"
    return
