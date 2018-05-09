# Module for Monika story telling
#
# Stories will get unlocked one at by session
# The unlocking logic has been added to script-ch30
# The topic that triggers the Story menu is monika_short_stories
# Topic is unlocked at the beginning of the game and is not
# random


# dict of tples containing the stories event data
default persistent._mas_story_database = dict()


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
            (mas_stories.story_database[k].prompt, k, not seen_event(k), False)
            for k in mas_stories.story_database
            if mas_stories.story_database[k].unlocked
        ]

        # also sort this list
        stories_menu_items.sort()

        # final quit item
        final_item = (mas_stories.STORY_RETURN, False, False, False, 20)

    # if we have only one story
    if len(stories_menu_items) == 1:

        # we jump to it, since doing pushEvent looks weird
        $ renpy.jump(stories_menu_items[0][1])
        #return

    m 1b "Sure thing!"
    m "What story would you like to hear?"

    # move Monika to the left
    show monika at t21

    # call scrollable pane
    call screen mas_gen_scrollable_menu(stories_menu_items, mas_stories.STORY_AREA, mas_stories.STORY_XALIGN, final_item=final_item)

    # return value? then push
    if _return:
        $ pushEvent(_return)

    # move her back to center
    show monika at t11
    return

# Stories start here

label mas_story_begin:
    python:
        story_begin_quips = [
            "Alright let's start the story.",
            "Ready to hear that story?",
            "Ready for story time?",
            "Let's begin~",
            "Let's begin then~"
        ]
        story_begin_quip=renpy.random.choice(story_begin_quips)
    m 3b "[story_begin_quip]"
    m 3dfc "Ahem."
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_tyrant",
        prompt="The cat and the cock",unlocked=True),eventdb=store.mas_stories.story_database)

label mas_story_tyrant:
    call mas_story_begin
    m 1i "A Cat caught a Cock and thought about reasonable excuses for eating him."
    m "He accused him of being a nuisance by crowing at night; not letting men sleep."
    m 1d "The Cock defended his action by saying this was for the benefit of men, as it wakes them for labor."
    m 1tfb "The Cat replied, “you abound in apologies, but it’s time for breakfast.”"
    m 1l "At that he made a meal of the Cock."
    m 4d "The moral of this story is that: 'Tyrants need no excuse'."
    m 1k "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_despise",
        prompt="The Fox",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_despise:
    call mas_story_begin
    m 1i "One hot summer’s day a Fox was strolling through an orchard till he came to a bunch of Grapes just ripening on a vine which had been trained over a lofty branch."
    m 1tfu "“Just the thing to quench my thirst,” quoth he."
    m 1i "Drawing back a few paces, he took a run and a jump, and just missed the bunch."
    m 1l "Turning round again with a One, Two, Three, he jumped up, but with no greater success."
    m 1tkx "Again and again he tried after the tempting morsel, but at last had to give it up, and walked away with his nose in the air, saying: “I am sure they are sour.”"
    m 3j "The moral of this story is that: 'It is easy to despise what you cannot get'."
    m 1k "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_lies",
        prompt="The Shepherd Boy and the wolf",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_lies:
    call mas_story_begin
    m 1d "There was a Shepherd Boy who tended his sheep at the foot of a mountain near a dark forest."
    m "It was lonely for him, so he devised a plan to get a little company."
    m 1hfw "He rushed down towards the village calling out “Wolf, Wolf,” and the villagers came out to meet him."
    m 1d "This pleased the boy so much that a few days after he tried the same trick, and again the villagers came to his help."
    m 1p "Shortly after this a Wolf actually did come out from the forest."
    m 1wfw "The boy cried out “Wolf, Wolf,” still louder than before."
    m 4efd "But this time the villagers, who had been fooled twice before, thought the boy was again lying, and nobody came to his aid."
    m 1q "So the Wolf made a good meal off the boy’s flock."
    m "The moral of this story is that: 'Liars are not believed even when they speak the truth'."
    m 1i "You shouldn't worry about it, [player]"
    m 1efb "I know you would never lie to me"
    m 1j "Ehehe~"
    m 1k "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_grasshoper",
        prompt="The Grasshopper",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_grasshoper:
    call mas_story_begin
    m 3 "One summer’s day a Grasshopper was hopping about, chirping and singing to its heart’s content."
    m 1 "An Ant passed by, bearing an ear of corn he was taking to the nest."
    m 1b "“Why not come and chat with me,” said the Grasshopper, “instead of toiling in that way?”"
    m 1efc "“I am helping to lay up food for the winter,” said the Ant, “and recommend you do the same.”"
    m 1tku "“Why bother about winter?” said the Grasshopper; “we have plenty of food now.”"
    m 1i "The Ant went on its way."
    m 1q "When winter came the Grasshopper had no food and found itself dying of hunger, while it saw the ants distributing corn and grain from the stores they had collected in the summer."
    m 3r "The moral of this story is that: 'There’s a time for work and a time for play'."
    m 1lkbsa "And there's also a time to spend with your cute girlfriend~"
    m 1ekbfa "I love you so much, [player]!"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_wind_sun",
        prompt="The Wind and the Sun",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_wind_sun:
    call mas_story_begin
    m 1 "The Wind and the Sun were disputing which was the strongest."
    m 1i "Suddenly they saw a traveller coming down the road, and the Sun said: “I see a way to decide our dispute.”"
    m "“Whichever of us can cause that traveller to take off his cloak shall be regarded as the strongest. You begin.”"
    m "So the Sun retired behind a cloud, and the Wind began to blow as hard as it could upon the traveller."
    m 1g"But the harder he blew the more closely did the traveller wrap his cloak round him, till at last the Wind had to give up in despair."
    m 1i "Then the Sun came out and shone in all his glory upon the traveller, who soon found it too hot to walk with his cloak on."
    m 3 "The moral of this story is that: 'Gentleness and kind persuasion win where force and bluster fail'."
    m 1k "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_seeds",
        prompt="The seeds",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_seeds:
    call mas_story_begin
    m 1 "It happened that a Countryman was sowing some hemp seeds in a field where a Swallow and some other birds were hopping about picking up their food."
    m 1tfd "“Beware of that man,” quoth the Swallow."
    m 1g "“Why, what is he doing?” said the others."
    m 1tfd "“That is hemp seed he is sowing; be careful to pick up every one of the seeds, or else you will repent it.” The Swallow replied."
    m 1r "The birds paid no heed to the Swallow’s words, and by and by the hemp grew up and was made into cord, and of the cords nets were made."
    m "Many birds that had despised the Swallow’s advice were caught in nets made out of that very hemp."
    m 3hfu "“What did I tell you?” said the Swallow."
    m 3i "The moral of this story is that: 'Destroy the seeds of evil before they grow up to be your ruin'."
    m 1k "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_gray_hair",
        prompt="The gray hair",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_gray_hair:
    call mas_story_begin
    m 1i "In the old days, a middle-aged Man had one wife that was old and one that was young; each loved him and desired nothing more than to earn his affection."
    m 1 "The Man’s hair was turning grey, which the young Wife did not like, as it made him look too old."
    m 1i "So, every night she picked out the white hairs."
    m 1g "But, the elder Wife did not like to be mistaken for his mother."
    m 1i "So, every morning she picked out as many of the black hairs as she could."
    m 1l "The Man soon found himself entirely bald."
    m 3i "The moral of this story is that: 'Yield to all and you will soon have nothing to yield'."
    m 1k "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_fisherman",
        prompt="The fisherman",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_fisherman:
    call mas_story_begin
    m 1d "A poor Fisherman, who lived on the fish he caught, had bad luck one day and caught nothing but a very small fry."
    m 1i "The Fisherman was about to put it in his basket when the little Fish said:"
    m 1wuo "“Please spare me, Mr. Fisherman! I am so small it is not worth while to carry me home. When I am bigger, I shall make you a much better meal.”"
    m 1i "But the Fisherman quickly put the fish into his basket."
    m 1tfu "“How foolish I should be,” he said, “to throw you back. However small you may be, you are better than nothing at all.”"
    m 3 "The moral of this story is that: 'A small gain is worth more than a large promise'."
    m 1k "I hope you enjoyed this little story, [player]~"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_ravel",
    prompt="Old man's three wishes",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_ravel:
    call mas_story_begin
    m 3 "Once, an elderly man was sitting alone on a dark path."
    m "He had forgotten both where he was traveling to, and who he was."
    m "Suddenly, he looked up to see an elderly woman before him."
    m "She grinned toothlessly and with a cackle, spoke: “Now your *third* wish. What will it be?”"
    m 3i "“Third wish?” The man was baffled. “How can it be a third wish if I haven't had a first and second wish?”"
    m "“You've had two wishes already,” the hag said, “but your second wish was for me to return everything to the way it was before you had made your first wish.”"
    m "“That's why you remember nothing; because everything is the way it was before you made any wishes.”"
    m "“All right,' said the man, “I don't believe this, but there's no harm in wishing. I wish to know who I am.”"
    m 1 "“Funny,” said the old woman as she granted his wish and disappeared forever. “That was your first wish.”"
    return
