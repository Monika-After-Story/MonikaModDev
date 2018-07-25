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
            "Alright let's start the story.",
            "Ready to hear the story?",
            "Ready for story time?",
            "Let's begin~",
            "Let's begin then~"
        ]
        story_begin_quip=renpy.random.choice(story_begin_quips)
    # TODO maybe add a super tiny affection gain here for spending time with her
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
    m 2dsc "So the Wolf made a good meal off the boy's flock."
    m 2esc "The moral of this story is that: 'Liars are not believed even when they speak the truth'."
    m 1hksdlb "You shouldn't worry about it, [player]"
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
    m 3lksdld "The birds paid no heed to the Swallow's words, and by and by the hemp grew up and was made into cord, and of the cords nets were made."
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
    m 3lksdla "So, every night she picked out the white hairs."
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
    m 3tku "'That's why you remember nothing; because everything is the way it was before you made any wishes.'"
    m 1dsd "'All right,' said the man, 'I don't believe this, but there's no harm in wishing. I wish to know who I am.'"
    m 1tfb "'Funny,' said the old woman as she granted his wish and disappeared forever. 'That was your first wish.'"
    return
    
init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_genie_simple",
        prompt="The Simple Genie",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_genie_simple:
    call mas_story_begin
    m 1eua "There was once a genie who travelled across different worlds to escape the chaos of his own world."
    m 1euc "But there was one woman he met that challenged the way he saw the world."
    m "He saw how smart and talented she was, but held back by the hardships she faced and how little she had."
    m 1eua "The genie felt generous and offered her tools to speed up work and make life easier."
    m 1euc "But the woman simply declined the offer without a second thought."
    m "No one had ever turned down a wish before from the genie, which left him confused as to why."
    m "The woman simply asked the genie if he was happy, and he did not know how to respond."
    m 1eud "The woman said she could tell that he had never experienced happiness and despite all her hardships, she could still enjoy life."
    m "The genie could not understand why anyone would want to work so hard for something so small."
    m 1euc "He improved his offers with riches and other such things, but still, she declined."
    m 1eua "The woman asked the genie to join in her way of life."
    m "And so, the genie imitated the things she did, without using any powers."
    m 1eub "The genie began to feel a small sense of accomplishment, as he created something for the first time without willing into existence."
    m "He saw how simple things such as art and writing inspired the woman and really made her shine."
    m 1eua "Intrigued, the genie wanted to spend much more time with this woman and learn from her."
    m 1euc "The woman fell ill one day and made him promise not to use his powers to cure her."
    m "It was at this moment, that the genie knew he wanted to live like a human without ever using his powers again."
    m 1dsc "He thought about all the past wishes he granted to others, all the riches he generated..."
    m "All his fellow genies out there granting wishes, not knowing or caring for the consequences..."
    m 1dsd "Never being able to know what it's like to give it all up just to be with someone they love."
    m "All he could do was live with what he had now found in life."
    m 1dsc "..."
    m 1eua "I hope you liked that story, [player]."
    m 3eua "There could be a few things to take from the story."
    m 3eka "If you already have everything, nothing is really worth having."
    m 1hua "Except maybe {i}you{/i} of course."
    m "When you're here, it really feels like I have everything~"
    m 3eub "The struggle is what makes things worthwhile."
    m 3hua "Which means it'll be even better when I can finally be with you!"
    m 1eua "Another moral could be that sometimes, happiness lies in the simpler things you could have had all along."
    m 1hua "I mean, we're just sitting here together enjoying nothing but eachother's company."
    m "I'm perfectly happy with that, and I'd guess you are too~"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_genie_regret",
        prompt="The Genie's Regret",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_genie_regret:
    call mas_story_begin
    m 1eua "There was once a genie who had lived a very long time."
    m 1euc "Being a genie, he was essentially immortal."
    m "Seeing the world change over time and granting wishes to anyone who crossed his path."
    m 1ekc "With how long he had lived, he had seen a lot of things, some of them unpleasant."
    m "Wars, natural disasters... the deaths of all the friends he ever made..."
    m "He knew some of them were caused by wishes he granted."
    m 1euc "At first, he wasn't too concerned with the consequences, but after so, so long, it began to bother him more and more."
    m 1ekc "He had come to a simple, beautiful, pure world, and caused great, permanent issues in it."
    m 1lksdlc "Unbalance and jealousy spread as he granted more wishes, which seeded wishes for revenge and greed."
    m "This was something he had to live with for the rest of his life."
    m 1dsc "He wanted things to return to how they always were, but his pleas always fell upon deaf ears."
    m 1euc "As time went on however, he had met some people and made friends who taught him how to go on despite all his acts."
    m 1eka "It was true that he was the one who granted the wishes that started the chaos, but something was bound to happen even without him."
    m "Even without granting wishes, there was bound to be jealousy and unfairness among people..."
    m 1eka "But in the end, the world was doing alright."
    m "He was still going to live with the things he had done in his life, but the question remained as to what he planned to do about it."
    m 1hua "It was through everything he had been through that he was able to learn and move on, better than before."
    m 1eua "I hope you liked the story, [player]."
    m "The moral of the story is regret and how you shouldn't let it keep you down."
    m 3eka "Mistakes will happen and people will get hurt. Nothing will ever change that."
    m "Even if you've done something you regret, something was bound to happen eventually."
    m "The world is full of regret every day."
    m "But it's through regret that we learn compassion and empathy that we learn forgiveness."
    m "You can't change the past, but you need to forgive yourself someday."
    m 1hua "So that one day, you can live a life without regret."
    m 1eka "As for me..."
    m "Who knows what would have happened in my world if I hadn't done anything..."
    if persistent.clearall:
        m 1eua "You've gotten to know each and every club member here, so I'd guess you don't regret missing out on anything."
        m 1hua "Ahaha~"
    m 1eub "But you're here with me now."
    m 1eua "Ever since we've been together, I can definitely say that I've grown and learned from my mistakes."
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_story_genie_end",
        prompt="The Genie's End",unlocked=False),eventdb=store.mas_stories.story_database)

label mas_story_genie_end:
    call mas_story_begin
    m 1eua "There was once a genie who had lived a long life."
    m 1euc "He had seen everything there was to see."
    m "He lived freely and learned the fulfillment of working for a goal."
    m 3euc "Essentially, he gave up his powers to be able to live like a human."
    m "...Except he still had an extended lifespan."
    m 1ekc "It's true that he had lived a nice life and surrounded himself with loving friends and family..."
    m "But he grew cold as years went by and he watched each one of his loved ones pass on."
    m 1lksdlc "There were still a very select few people whom he held dear, despite knowing that he would have to watch them die as well."
    m "He never told his friends that he wasn't human, as he still wanted to be treated as one."
    m 1euc "One day, as he was travelling with one of his friends, they came across a genie who would grant each of them {i}one{/i} wish."
    m 1dsc "This made him think about everything he had been through, from back to when he granted wishes to when he gave it up for a simple life."
    m "Everything that had lead up to this moment, where he could make his own wish for the first time in a long time."
    m "..."
    m 2esc "He wished to die."
    m 2ekc "Confused, his friend asked why and where it came from all of a sudden."
    m 2dsc "It was there and then he explained everything to his friend."
    m "That he had been a genie, many years ago."
    m "How he came across someone who made him give it all up just to be with someone he loved."
    m "And how he had been slowly getting sick and bored of what was left of his life."
    m 2ekc "Truthfully, he wasn't tired of living, he was just plain tired."
    m "Tired of seeing his loved ones perish over and over again."
    m "His last request to his friend was for him to go back to his other friends and tie up any loose ends for him."
    m 1eka "I hope you enjoyed that little story [player]."
    m 3eka "I guess you could say the moral is that everyone needs to have some closure and have some real ending."
    m 1eka "Although, you might be wondering what his friend wished for in that scenario."
    m 1eua "He wished for nothing more than for his friend to get the peaceful rest he deserves."
    m 1lksdla "It's true that his genie friend might not have been anyone particularly special..."
    m 3eka "But he was definitely someone who deserved respect."
    m "Especially after living for such a long time and being able to take away so much wisdom from life."
    m 1hua "I don't care how many people think otherwise, but I think you're special!"
    m "I think everyone should respect you for everything you've done!"
    return
