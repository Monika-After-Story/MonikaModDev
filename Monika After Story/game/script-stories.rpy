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
default mas_can_unlock_scary_story = False


# store containing stories-related things
init -1 python in mas_stories:

    # TYPES:
    TYPE_SCARY = 0

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
label mas_stories_start(scary=False):

    python:
        import store.mas_stories as mas_stories

        if scary:
            stories = renpy.store.Event.filterEvents(
                mas_stories.story_database,
                category=(True,[mas_stories.TYPE_SCARY])
            )
        else:
            stories = renpy.store.Event.filterEvents(
                mas_stories.story_database,
                excl_cat=list()
            )

        # build menu list
        stories_menu_items = [
            (mas_stories.story_database[k].prompt, k, False, False)
            for k in stories
            if mas_stories.story_database[k].unlocked and seen_event(k)
        ]

        # sanity check for first timers
        if not stories_menu_items:
            stories_menu_items = [
                (mas_stories.story_database[k].prompt, k, False, False)
                for k in stories
                if mas_stories.story_database[k].unlocked
            ]

            # set the mas_can_unlock_story flag to False since it
            # shouldn't unlock anything at this time
            if scary:
                mas_can_unlock_scary_story = False
            else:
                mas_can_unlock_story = False

        # check if we have a story available to be unlocked and we can unlock it
        if len(stories_menu_items) < len(stories) and ((not scary and mas_can_unlock_story)
                or (scary and mas_can_unlock_scary_story)):

            # Add to the menu the new story option
            if scary:
                return_label = "mas_scary_story_unlock_random"
            else:
                return_label = "mas_story_unlock_random"

            stories_menu_items.append(("A new story", return_label, True, False))

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
   call mas_story_unlock_random_cat()
   return

label mas_scary_story_unlock_random:
   call mas_story_unlock_random_cat(scary=True)
   return

label mas_story_unlock_random_cat(scary=False):

    python:
        if scary:
            # reset flag so we don't unlock another one
            mas_can_unlock_scary_story = False

            # get locked stories
            stories = renpy.store.Event.filterEvents(
                renpy.store.mas_stories.story_database,
                unlocked=False,
                category=(True,[renpy.store.mas_stories.TYPE_SCARY])
            )

            if len(stories) == 0:

                # in case the player left the game mid unlocking
                stories = renpy.store.Event.filterEvents(
                    renpy.store.mas_stories.story_database,
                    unlocked=True,
                    seen=False,
                    category=(True,[renpy.store.mas_stories.TYPE_SCARY])
                )

                if len(stories) == 0:

                    # There should be no way to get to this point but just in case
                    # let's fail 'nicely'
                    stories = renpy.store.Event.filterEvents(
                        renpy.store.mas_stories.story_database,
                        unlocked=True,
                        category=(True,[renpy.store.mas_stories.TYPE_SCARY])
                    )
        else:
            # reset flag so we don't unlock another one
            mas_can_unlock_story = False

            # get locked stories
            stories = renpy.store.Event.filterEvents(
                renpy.store.mas_stories.story_database,
                unlocked=False,
                excl_cat=list()
            )

            if len(stories) == 0:

                # in case the player left the game mid unlocking
                stories = renpy.store.Event.filterEvents(
                    renpy.store.mas_stories.story_database,
                    unlocked=True,
                    seen=False,
                    excl_cat=list()
                )

                if len(stories) == 0:

                    # There should be no way to get to this point but just in case
                    # let's fail 'nicely'
                    stories = renpy.store.Event.filterEvents(
                        renpy.store.mas_stories.story_database,
                        unlocked=True,
                        excl_cat=list()
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
    m 2lksdlc "You wouldn't have had to go through what you saw."
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

# Scary stories start here
label mas_scary_story_setup:
    show monika 1dsc
    $ mas_temp_r_flag = mas_is_raining
    $ scene_change = True
    $ mas_is_raining = True
    pause 1.0
    $ mas_temp_m_flag = morning_flag
    call spaceroom(start_bg="monika_gloomy_room")
    $ morning_flag = True
    #stop music fadeout 1.0
    play background audio.rain fadein 1.0 loop
    show vignette zorder 13
#    $ songs.current_track = songs.FP_NO_SONG
#    $ songs.selected_track = songs.FP_NO_SONG

    $ HKBHideButtons()
    #$ store.songs.enabled = False
    python:
        story_begin_quips = [
            "Alright let's start the story.",
            "Ready to hear the story?",
            "Ready for story time?",
            "Let's begin~",
            "Let's begin then~"
        ]
        story_begin_quip=renpy.random.choice(story_begin_quips)
    m 3eua "[story_begin_quip]"
    m 1duu "Ahem."
    return

label mas_scary_story_cleanup:
    python:
        story_end_quips = [
            "Scared, " + player + "?",
            "Did I scare you, " + player + "?",
            "How was it?"
        ]
        story_end_quip=renpy.random.choice(story_end_quips)

    m 3eua "[story_end_quip]"
    if not mas_temp_r_flag:
        stop background fadeout 1.0
    show monika 1dsc
    $ scene_change = True
    $ mas_is_raining = mas_temp_r_flag
    pause 1.0
    hide monika_gloomy_room
    $ morning_flag = mas_temp_m_flag
    hide vignette
    call spaceroom
    $ store.songs.enabled = True
    $ HKBShowButtons()
    m 1esa "I hope you liked it, [player]~"
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_hunter",
    category=[store.mas_stories.TYPE_SCARY], prompt="The Hunter",unlocked=True),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_hunter:
    call mas_scary_story_setup
    m 3esa "One day, a hunter went out hunting for game out in the forest."
    m 3esc "The forest was dense and dark all around him and he struggled to hit his mark."
    m 1esd "He was soon approached by a salesman, who kept his face covered."
    m 3esd "The salesman offered seven magic bullets that would hit whatever target the owner wanted without fail."
    m "He would give the hunter these bullets on one condition."
    m "The hunter could use the first six bullets as he wished, but the last bullet’s mark would be chosen by the salesman."
    m 1esa "The hunter agreed and quickly became famous in his town for bringing home kill after kill without fail."
    m "It wasn’t long before the hunter used up all six bullets."
    m "On his next hunt, the hunter saw a wild boar and loaded the last bullet hoping to take down the beast."
    m "When he fired, he missed and the bullet instead hit his beloved fiancée in the chest, killing her."
    m "The salesman then suddenly appeared to the hunter while he was grieving his loss, revealing that he was in fact the devil."
    m "He gives the hunter a chance to redeem for his mistake."
    m "If the hunter remained faithful to his beloved who was slain for the remainder of his life, he would be reunited with her after death."
    m "The hunter vowed to remain true to his beloved and remained faithful for a time, but soon fell in love with another girl and married her."
    m "One year to the day after the fatal incident, as the hunter rode through the forest chasing some game, he comes across the spot where he slayed his beloved."
    m "To his horror,{w=1.0} her corpse, which was buried elsewhere, was standing in the same spot she was slain."
    m "She approached the hunter, scorning him for being unfaithful and vowing revenge for slaying her."
    m "The hunter rides away in a panic."
    m "After a short way, he looks behind him to see if she was following him any longer."
    m "To his horror, not only had he gained no distance, she had gained on him significantly."
    m "In his state of panic, he failed to see the branch that would strike a blow at his neck, freeing him from his horse and introducing him to the wet ground beneath him."
    m "His attention isn't on his horse however, as the creature lopes away without him."
    show emptydesk at i11 zorder 9
    m "It is instead on the figure that now looms above him as a former vision of the one he once loved."
    # Yuri dragon spoop TODO this is going to be 1 in 10 but for testing I won't add that as of now.
    # hide monika so it's just yuri
    hide monika
    play sound "sfx/giggle.ogg"
    show yuri dragon2 zorder 15 at malpha
    $ style.say_dialogue = style.edited
    y "{cps=*2}I'll get you too.{/cps}{nw}"
    hide yuri
    $ style.say_dialogue = style.normal
    show monika 1eua at i11 zorder MAS_MONIKA_Z
    # spoop ends
    m "The next morning, the villagers found the hunter dead at the edge of the forest."
    hide emptydesk
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_kuchisake_onna",
    category=[store.mas_stories.TYPE_SCARY], prompt="Kuchisake-Onna",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_kuchisake_onna:
    call mas_scary_story_setup
    m 3eua "There once was a beautiful woman, whom was the wife of a samurai."
    m 3eub "Not only was she very beautiful, but she was very vain, and welcomed the attention of any man prepared to offer it to her."
    m 1tsu "She would often ask men to rate her appearance."
    m 1esd "The woman ended up cheating on her husband and he quickly found out."
    m 1efd "When he confronted the woman about it, they got into an argument and the samurai ended up slitting her mouth from ear to ear, in the shape of a wide smile; asking her, ‘who will think you are beautiful, now?’."
    m 2dsd "Shortly after, the woman died."
    m "The samurai, full of regret for what he had done, committed seppuku shortly afterwards as well."
    m 3eud "The woman’s story doesn’t end here though, she came back as a vengeful spirit."
    m "They say she now wanders around aimlessly at night, her face covered with a surgical mask."
    m 1esa "When she comes across someone walking by themselves, she will suddenly pose the question, ‘am I pretty?’."
    # TODO 1 in 15 chance
    hide monika
    show screen tear(20, 0.1, 0.1, 0, 40)
    play sound "sfx/s_kill_glitch1.ogg"
    show natsuki ghost2 zorder 16 at i11
    show k_rects_eyes1 zorder 17
    show k_rects_eyes2 zorder 17
    $ pause(0.25)
    #play music t7g
    stop sound
    hide screen tear
    $ style.say_dialogue = style.edited
    show screen mas_background_timed_jump(5, "mas_scary_story_kuchisake_onna.no")
    menu:
        "am I pretty?"
        "Yes":
            hide screen mas_background_timed_jump
            jump mas_scary_story_kuchisake_onna.end
        "No":
            jump mas_scary_story_kuchisake_onna.no
    label .no:
        hide screen mas_background_timed_jump
        "is that, so?{w=1.0}{nw}"
        $ _history_list.pop()
        $ pause(1.0)
        hide natsuki
        play sound "sfx/run.ogg"
        show natsuki mas_ghost onlayer front at i11
        $ pause(0.25)
        hide natsuki mas_ghost onlayer front
    label .end:
        show black zorder 100
        hide k_rects_eyes1
        hide k_rects_eyes2
        hide natsuki
        $ pause(1.5)
        hide black
        $ style.say_dialogue = style.normal
        show monika 1eua at i11 zorder MAS_MONIKA_Z
    m 3eud "If the person doesn’t give her the answer she seeks, she will slay them where they stand with a large pair of scissors she has stashed away."
    m 3esa "So, when you are walking alone at night, make sure you have someone to walk with, lest you end up the next victim of this hostile spirit."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_o_tei",
    category=[store.mas_stories.TYPE_SCARY], prompt="The tale of O-Tei",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_o_tei:
    call mas_scary_story_setup
    m "A long time ago, there lived a man named Kenji, who was studying to be a physician."
    m "Kenji was engaged to a young woman named Tomoe and they were to be married after he finished his studies."
    m "Unfortunately, Tomoe contracted a serious illness before that could happen."
    m "She summoned her husband-to-be, as she lay on her deathbed."
    m "As he knelt by her bedside, she said to him, 'We have been promised to each other since childhood...'"
    m "'Unfortunately with this frail body of mine, my time has come and I am going to die before I could become your wife.'"
    m "'I want you to promise me that you will not grieve my loss, because I believe we shall meet again.'."
    m "Kenji answered earnestly that yes they would meet again in the afterlife."
    m "Tomoe replied 'No, I believe that we are destined to meet each other again in this world, only if you wish it to be so.'."
    m "Kenji replied tenderly, 'To see you again, my love, would be no less a joy than a duty, but if we were to meet again, how would I know that it is you?'."
    m "Tomoe replies, 'That I cannot answer, you will know when the time comes, remember these words of mine.'."
    m "And there she ceased to speak and expired."
    m "Kenji grieved deeply for the loss of his love."
    m "Years passed, Kenji never forgot Tomoe, but since he was the only son in his family, he was required to marry someone else and carry on the family name."
    m "Time was not kind to Kenji, however, he lost his parents, and shortly after, his wife and child died as well."
    m "One day, he decided to abandon his home and take a long journey to forget his troubles."
    m "Somewhere along his journey, he came across a mountain village."
    m "At the inn he decided to stay for the night, his heart nearly lept out of his chest."
    m "The girl that greeted him, reminded him so much of his former lover, that he had to pinch himself to ensure he wasn’t dreaming."
    m "As she came and went, her attitude and motion reminded him so much of her."
    show yuri eyes zorder 16 at otei_appear(a=0.075,time=4.0)
    show yuri eyes_base zorder 15 at otei_appear(a=0.085,time=3.0)
    show yuripupils zorder 17 at otei_appear(a=0.095,time=5.0)
    m "He remembered the last conversation that he and Tomoe had before she passed away."
    m "He flagged down the girl and said to her, 'I’m sorry to bother you, but you remind me so much of someone I knew long ago that it startled me at first.'."
    m "'If you don’t mind me asking, are you from around here and what is your name?'."
    m "Immediately, in the unforgotten voice of his deceased beloved, the girl answered: 'My name is Tomoe, and you are Kenji, my promised husband.`"
    m "`17 years ago, I died and you made a promise to marry me if I could come back to this world and now I stand before you.'."
    hide yuri
    hide yuripupils
    m "Then she fell unconscious and could not recall what she had said to him previously."
    m "A short time later Kenji married the girl and they lived a happy, long life together afterwards."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_mujina",
    category=[store.mas_stories.TYPE_SCARY], prompt="Mujina",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_mujina:
    call mas_scary_story_setup
    m "One night, at a late hour, an old merchant was walking down a road, heading home after a long day of selling his wares."
    m "The road he travelled on led to a large hill, that was very dark and secluded at night, and many travelers tended to avoid the area."
    m "The man was tired though, and decided to take the road anyways, because it would get him home quicker."
    m "On the one side of the hill was an old moat, that was quite deep."
    m "As he went along, he noticed a woman crouching by the moat, all alone, weeping bitterly."
    m "Although the man was exhausted, he feared the woman intended to throw herself into the water, so he stopped."
    m "The woman was petite and well-dressed, covering her face with one of the sleeves of her kimono facing away from him."
    m "The man said to her, ‘Miss, please don’t cry, tell me what is the matter? If there is anything I can do to help you, I would be glad to do it.’ The woman continued to weep."
    m "The man started again, ‘Miss, listen to me, this is no place for a lady at night. Please stop crying, tell me how I may help you!’."
    m "Slowly, the woman rose up, with her head still turned, continuing to sob."
    m "The man laid his hand lightly on her shoulder and said ‘Miss…’."
    m "At that moment, the woman turned around, dropping her sleeve, revealing a face with no features."
    m "No eyes, nose or mouth anywhere! {w}The man ran up the hill screaming. "
    m "He continued to run until in the distance he saw the light of a lantern and ran towards it."
    m "The lantern belonged to a travelling salesman that was walking along."
    m "The old man stopped in front of him, doubled over to catch his breath."
    m "The salesman asked why the man was running."
    m "After the old man caught his breath a little, he said to the salesman, ‘I saw a woman by the moat, she didn’t have a face!’."
    m "The salesman responded ‘Oh, you mean like this?’."
    m "The man looked up at the salesman only to be greeted again by the familiarly vague shape of a human face devoid of features."
    m "The old man let out a scream and then suddenly, the lantern went out."
    show black zorder 100
    play sound "sfx/glitch1.ogg"
    $ pause(1.5)
    stop sound
    hide black
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_ubume",
    category=[store.mas_stories.TYPE_SCARY], prompt="The ubume",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_ubume:
    call mas_scary_story_setup
    m "One night, at a late hour, a woman walked into a confectionery store to buy some candy, right before the owner was about to head off to bed."
    m "The village was small, and the confectioner didn’t recognize the woman, but didn’t think much of it, and sold the woman the candy that she requested."
    m "The next night, around the same time, the woman would walk into the shop to buy some more candy."
    m "After a few nights of this happening, the confectioner became curious about the woman and decided to follow her the next time she came in."
    m "The next night, the woman arrived at her normal time, purchased the candy that she always did and went happily along her way."
    m "After the woman walked out the door, the confectioner looked into his money box and saw the coins that the woman had given to him had turned into a leaf from a tree."
    # TODO 1 in 20
    play sound "sfx/giggle.ogg"
    m "He followed the woman to the outside of a nearby temple, where she simply vanished."
    m "The confectioner was shocked by this and decided to head back home."
    m "The next day, he went to the temple and told the monk there what he saw."
    m "The priest told the confectioner that a young woman that was travelling through the village recently had suddenly fallen dead in the street."
    m "The monk felt compassion for the poor dead woman, as she had been in her last month of pregnancy, and had her buried in the cemetery behind the temple."
    m "As the monk led the confectioner to the site of the grave, they both heard a baby crying."
    m "They quickly got some shovels, dug up the grave and raised the lid off of the coffin."
    m "Inside they found a newborn baby boy sucking on a piece of candy."
    m "The monk took the child out of the grave and raised him as his own."
    m "The woman’s ghost was never seen again after that."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_womaninblack",
    category=[store.mas_stories.TYPE_SCARY], prompt="The woman in black",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_womaninblack:
    call mas_scary_story_setup
    m "One night, a colonel boarded a train on his way home."
    m "The colonel was content because he was able to secure a compartment to himself and promptly fell asleep."
    m "A short time later, he awoke with a start, feeling stiff and uneasy."
    m "To his surprise, he noticed that there was now a woman sitting opposite of him."
    m "The woman's attire was entirely black, including a veil that obscured her face."
    m "The woman appeared to be looking down at something in her lap, although there wasn’t anything there."
    m "The colonel was a friendly fellow and tried to make small talk with the woman."
    m "To his dismay, the woman did not respond to his pleasantries."
    m "Suddenly, the woman started rocking back and forth and singing a soft lullaby."
    m "Before the colonel could inquire about it, the train suddenly screeched to a halt."
    m "A suitcase from the compartment above fell and hit him on the head, knocking him unconscious."
    show black zorder 100
    play sound "sfx/crack.ogg"
    $ pause(1.5)
    hide black
    m "When he came to, the woman was gone. The colonel questioned some of the train workers about the woman, but none of them had seen her."
    m "To boot, once the colonel had entered the compartment it was locked, as was customary, and no one had entered or left the compartment after he had entered."
    m "A few months later, the colonel was talking to a railway official that informed him that some time ago, a woman and her husband were travelling on a train together."
    m "The woman’s husband had his head too far out one of the windows and was decapitated by a wire."
    m "The headless body fell into her lap. When the train arrived at its stop, the woman was found holding the corpse and singing a lullaby to it."
    m "She never regained her sanity and died a few months later."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_resurrection_mary",
    category=[store.mas_stories.TYPE_SCARY], prompt="Resurrection Mary",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_resurrection_mary:
    call mas_scary_story_setup
    m "At a dancehall around Christmas time, a young man named Lewis was enjoying some time with his friends, when a young woman he hadn’t seen before caught his attention."
    m "The girl was tall, blond, blue-eyed and very beautiful."
    m "The woman was wearing a fancy white dress, with white dancing shoes and a thin shawl."
    m "Lewis found the girl captivating and decided to ask the woman to dance with him and she accepted his invitation."
    m "The woman was certainly beautiful, but Lewis felt there was something strange about her."
    m "As they danced, he tried to get to know her a little better, but all she would say about herself was that her name was Mary and that she was from the south side of town."
    m "Also, her skin was cool and clammy to the touch. At one point during the evening, he kissed Mary, and found her lips were as cool as her skin."
    m "The two spent much of the night together dancing. When the time came to leave, Lewis offered Mary a ride home and she again accepted the invitation."
    m "She directed him to drive down a certain road, and he obliged."
    m "As they were passing the gates of a cemetery, Mary asked Lewis to pull over."
    m "Although perplexed, Lewis stopped the car as she requested."
    m "She then opened the door, leaned in towards Lewis, whispered that she had to go and that he could not go with her."
    m "She then got out of the car and walked towards the cemetery gate before disappearing."
    m "Lewis sat in the car for a long time bewildered by what had just happened."
    m "He never saw the beautiful woman ever again."
    # TODO 1 in 20
    play sound "sfx/giggle.ogg"
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_corpse",
    category=[store.mas_stories.TYPE_SCARY], prompt="The resuscitated corpse",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_corpse:
    call mas_scary_story_setup
    m "There once was an old man that ran an old roadside inn. One evening, 4 men arrived and asked for a room."
    m "The old man replied that all of the rooms were taken, but he could find them a place to sleep if they weren’t too particular."
    m "The men were exhausted and assured the old man that any place would do."
    m "The old man led them to a room around back. Lying in the corner of the room was the corpse of a woman."
    m "The old man explained that his daughter-in-law had recently perished and she was awaiting burial."
    m "After the old man departed, 3 of the 4 men fell asleep. The last man couldn’t fall asleep."
    m "Suddenly, the man heard a creaking noise."
    # need opinion on this one since it's for storytelling purposes
    play sound "sfx/crack.ogg"
    m "He looked up and in the light of the lamp, he saw the woman rise, now bearing fangs and fingernails that looked like claws, advancing towards them."
    m "She bent down and bit each of the sleeping men. The fourth man, at the last second, pulled up a pillow in front of his neck."
    m "The woman bit the pillow and apparently not realizing she hadn’t bit the last man, returned to her original resting spot."
    m "The man kicked his companions, but none of them moved. The man decided to take his chances and make a run for it."
    m "As soon as his feet touched the ground, however, he heard another creak."
    m "Realizing that the woman was again rising from her spot, he opened the door and ran as fast as he could."
    # need opinions on this one since it's for storytelling purposes
    show layer master at heartbeat2(1)
    show vignette as flicker zorder 14 at vignetteflicker(0)
    m "After a short distance, he looked behind him and saw that the corpse was not far behind him."
    m "A chase ensued and as she caught up to him, he found himself standing under a tree."
    m "The woman charged towards him with her claw-like fingernails extended."
    m "At the last second, the man dodged and the woman struck the tree with great ferocity."
    m "Her fingernails were now deeply embedded in the tree."
    m "She wildly swung her freehand at the man as he lay on the ground, unable to reach him."
    m "The man, frightened and exhausted crawled a short distance away and then passed out."
    show layer master
    hide flicker
    show black zorder 100
    $ pause(2.5)
    hide black
    m "The next morning a passing police officer found the man and brought him back to consciousness."
    m "The man recounted what had happened. The officer, thinking the man was a drunkard, walked the man back to the inn."
    m "As they arrived, the inn was in a state of great commotion."
    m "The 3 travelers had been found dead in their beds."
    m "The body of the daughter-in-law was lying where she had been the night before, but now her clothes were soiled with blood and a piece of bark was found under her fingernail."
    m "After some questioning, the innkeeper finally admitted that the woman had died six months previously and he was trying to save enough money to give her a proper burial."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_jack_o_lantern",
    category=[store.mas_stories.TYPE_SCARY], prompt="Jack O Lantern",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_jack_o_lantern:
    call mas_scary_story_setup
    show darkred zorder 25:
        alpha 0
        linear 2.0 alpha 1.0
    m "There was once a man named Jack. Jack was a miserable, old drunk who took pleasure in playing tricks on people."
    m "One night, Jack ran into the Devil and invited him to have a drink with him."
    m "After Jack had had his fill, he turned to the Devil and asked him to turn into a coin so he could pay for their drinks, as he didn’t have the money to pay for them."
    m "Once the Devil did so, Jack pocketed the coin and walked out without paying."
    m "The Devil could not turn back to his original form because Jack had put it into his pocket next to a silver cross."
    m "Jack eventually freed the Devil, under the condition that he would not bother Jack for 1 year and that, should Jack die, he would not claim his soul. The next year, Jack ran into the Devil again."
    m "This time he tricked him into climbing into a tree to pick a piece of fruit."
    m "While he was in the tree, Jack surrounded it with white crosses so that the Devil could not come down."
    m "Once the Devil promised not to bother him again for another 10 years, Jack removed them. When Jack died, he went to Heaven."
    m "When he arrived, he was told he could not enter for how poorly a life he had lived on Earth."
    m "So, he went down to Hell, where the Devil kept his promise and would not allow Jack to enter."
    m "Jack became scared, for he had no place to go."
    m "Jack asked the Devil how he could leave, as there was no light."
    m "The Devil tossed Jack an ember from the flames of Hell to help Jack light his way."
    m "Jack pulled out a turnip he had with him and carved it out and placed the ember inside of it."
    m "From that day onward, Jack roamed the earth without a resting place, lighting the way as he went with his Jack O’Lantern."
    hide darkred
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_baobhan_sith",
    category=[store.mas_stories.TYPE_SCARY], prompt="Baobhan Sith",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_baobhan_sith:
    call mas_scary_story_setup
    m "There was once a young group of hunters, who stopped for the night in a small hunting lodge."
    m "As the men settled in, they built a fire, and began eating and drinking merrily, for it had been a good day."
    m "They said to themselves the only thing that they lacked was the company of some beautiful women by their sides."
    m "Not too long after they said this, there came a knock at their door."
    m "There in the doorway stood four beautiful women."
    m "The women, having become lost in the wilderness, asked if they may join the men in their shelter for the night."
    m "The men, silently congratulating themselves on their good fortunes, invited the women in."
    m "After a while of enjoying each other’s company, the women expressed a wish to dance."
    m "The men wasted no time coupling off with each of the maidens."
    m "As they are dancing, one of the men notices that the other couples are dancing rather erratically."
    m "Then, to his horror, he realizes that the other men have blood pouring from their necks onto their shirts."
    m "In a blind panic, the man abandoned his partner and bolted out the door, which he was fortunate enough to be close to, before he could share the fate of his friends."
    m "The man ran into the forest and ended up hiding amongst the horses he and his friends had ridden during that day’s hunt."
    m "The women, not far behind, closed in, but appeared unable to get past the horses to the man."
    m "So there the man stood, weary eyed, among the animals all night long as the women circled around the horses, trying to find a way to get to the man."
    m "Just before dawn, the women gave up and retreated back into the woods."
    m "Now alone, the man cautiously headed back towards the hunting lodge, hearing no sound from within."
    m "When he looked inside, he saw his three comrades dead on the floor, their skin almost translucent, as they lay in a pool of their own blood."
    play sound "sfx/stab.ogg"
    show blood splatter1 zorder 16:
        pos (570,195)
    show blood splatter1 as bl2 zorder 16:
        pos (50,95)
    show blood splatter1 as bl3 zorder 16:
        pos (370,695)
    show blood splatter1 as bl4 zorder 16:
        pos (150,295)
    show blood splatter1 as bl5 zorder 16:
        pos (950,505)
    show blood splatter1 as bl6 zorder 16:
        pos (700,795)
    show blood splatter1 as bl7 zorder 16:
        pos (1050,95)
    $ pause(1.5)
    stop sound
    hide blood
    hide bl2
    hide bl3
    hide bl4
    hide bl5
    hide bl6
    hide bl7
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_serial_killer",
    category=[store.mas_stories.TYPE_SCARY], prompt="The serial killer",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_serial_killer:
    call mas_scary_story_setup
    m "A young couple park at a cemetery one night for some undisturbed lovemaking."
    m "They are interrupted by a radio report that a mass murderer has escaped from a psychiatric hospital nearby and may be headed in their direction."
    m "They decide to leave, but the car won't start."
    m "The young man gets out of the car to go for help and instructs the girl to stay in the car with the doors locked."
    m "A few moments later, she hears a scratching sound on the roof of the car."
    play sound "sfx/mscare.ogg"
    m "She thinks to herself it must be a tree branch in the wind."
    m "Her date doesn't return and after some time passes, a police car drives by."
    m "An officer stops and gets out of the car."
    m "The police officer instructs the girl to get out of the car, walk towards him and not look back."
    m "She does as he instructs her to. Not too long after, more police cars arrive."
    m "Curiosity gets the better of the girl and she looks behind her."
    m "She is horrified to see the body of her boyfriend hanging head down from a tree, his throat slit from ear to ear."
    m "His fingernails scratching the car roof."
    call mas_scary_story_cleanup
    return
