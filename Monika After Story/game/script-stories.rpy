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
default mas_full_scares = False


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
    STORY_RETURN = "I changed my mind."
    story_database = dict()

    def _unlock_everything():
        stories = renpy.store.Event.filterEvents(
            renpy.store.mas_stories.story_database,
            unlocked=False
        )
        for _, story in stories.iteritems():
            story.unlocked = True



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
            m 1ekc "Sorry [player]. That's the only story I can tell you right now."
            m 3hksdlb "Don't worry! I'll think of a story to tell you next time"
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
            "Let's begin, then~"
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
    #TODO persistent music spoop for o31
    stop music fadeout 1.0
    pause 1.0
    $ mas_temp_m_flag = morning_flag
    $ store.mas_sprites.reset_zoom()
    call spaceroom(start_bg="monika_gloomy_room")
    $ morning_flag = True
    play music "mod_assets/bgm/happy_story_telling.ogg" loop
    play background audio.rain fadein 1.0 loop
    if not mas_isO31():
        show vignette zorder 70
#    $ songs.current_track = songs.FP_NO_SONG
#    $ songs.selected_track = songs.FP_NO_SONG

    $ HKBHideButtons()
    $ mas_RaiseShield_core()
    #$ store.songs.enabled = False
    python:
        story_begin_quips = [
            "Alright let's start the story.",
            "Ready to hear the story?",
            "Ready for story time?",
            "Let's begin~",
            "Let's begin, then~"
        ]
        story_begin_quip=renpy.random.choice(story_begin_quips)
    m 3eua "[story_begin_quip]"
    m 1duu "Ahem."
    return

label mas_scary_story_cleanup:
    python:
        story_end_quips = [
            "Scared, [player]?",
            "Did I scare you, [player]?",
            "How was it?",
            "Well?"
        ]
        story_end_quip=renpy.substitute(renpy.random.choice(story_end_quips))

    m 3eua "[story_end_quip]"
    if not mas_temp_r_flag:
        stop background fadeout 1.0
    show monika 1dsc
    $ scene_change = True
    $ mas_is_raining = mas_temp_r_flag
    pause 1.0
    hide monika_gloomy_room
    $ morning_flag = mas_temp_m_flag
    if not mas_isO31():
        hide vignette
    call spaceroom
#    $ store.songs.enabled = True
    $ play_song(songs.current_track)
    m 1eua "I hope you liked it, [player]~"
    $ mas_DropShield_core()
    $ HKBShowButtons()
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_hunter",
    category=[store.mas_stories.TYPE_SCARY], prompt="The Hunter",unlocked=True),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_hunter:
    call mas_scary_story_setup
    m 3esa "One day, a hunter went out hunting for game in the forest."
    m 3esc "The forest was dense and dark all around him, so he struggled to hit his mark."
    m 1esd "He was soon approached by a salesman, who kept his face covered."
    m 3esd "The salesman offered seven magic bullets that would hit whatever target the owner wanted without fail."
    m "He would give the hunter these bullets on one condition."
    m "The hunter could use the first six bullets as he wished, but the last bullet's mark would be chosen by the salesman."
    m 1euc "The hunter agreed and quickly became famous in his town for bringing home kill after kill."
    m 3eud "It wasn't long before the hunter used up all six bullets."
    m 1esc "On his next hunt, the hunter saw a wild boar, the largest he had ever seen. It was too great of a prey to pass up on."
    m 1euc "He loaded the last bullet hoping to take down the beast..."
    m 1dsc "But when he fired, the bullet instead hit his beloved fiancée in the chest, killing her."
    m 3esc "The salesman then appeared to the hunter as he grieved his tragic loss, revealing that he was in fact the Devil."
    m 1esd "'I will give you a chance for redemption, hunter.' The salesman told him."
    m 4esb "'Remain ever faithful to your slain beloved for the remainder of your life, and you would be reunited with her after death.'"
    m 1eud "The hunter vowed to remain true to her for for as long as he lived..."
    m 1dsd "...{w}Or so he would."
    m 1dsc "Long after her demise, he fell in love with another woman and soon married her, forgetting his past love."
    m 1esc "It was until one year to the day after the fatal incident, as the hunter rode through the forest chasing some game, he came across the spot where he slayed his beloved."
    m 3wud "To his horror,{w=1.0} her corpse, which was buried elsewhere, was standing in the same spot she was slain."
    m "She approached the hunter, scorning him for being unfaithful and vowing revenge for slaying her."
    m "The hunter rode away in a panic."
    m 1euc "After a short way, he looked behind him to see if she was following him any longer."
    m 1wkd "To his horror, not only had he not further his distance, but she had gained on him significantly."
    m 3wkd "In his state of fear, he failed to avoid the branch that was ahead of him, promptly dismounting the hunter from his steed and down to the cold ground."
    m 4dsc "His attention wasn't on his horse however, as the creature loped away without him."
    show emptydesk at i11 zorder 9
    m 1esc "...It was instead on the figure that he promised to be with eternally in the afterlife."
    # 1 in 10
    if renpy.random.randint(1,10) == 1 or mas_full_scares or persistent._mas_pm_likes_spoops:
        hide monika
        play sound "sfx/giggle.ogg"
        show yuri dragon2 zorder 72 at malpha
        $ style.say_dialogue = style.edited
        y "{cps=*2}I'll get you too.{/cps}{nw}"
        hide yuri
        $ style.say_dialogue = style.default_monika
        show monika 1eua at i11 zorder MAS_MONIKA_Z
    hide emptydesk
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_kuchisake_onna",
    category=[store.mas_stories.TYPE_SCARY], prompt="Kuchisake-Onna",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_kuchisake_onna:
    call mas_scary_story_setup
    m 3eud "There once was a beautiful woman, whom was the wife of a samurai."
    m 3eub "She was as incredibly beautiful as she was vain, welcoming the attention of any man prepared to offer it to her."
    m 1tsu "And often, would ask men to appraise her appearance."
    m 1euc "The woman was prone to cheat on her husband multiple times and was soon found out about her affairs."
    m 1esc "When he confronted her, he was beyond infuriated as she was damaging their status as nobles, humiliating him."
    m 2dsc "He then brutally punished her by cutting her mouth from ear to ear, disfiguring her delicate beauty."
    m 4efd "'Who will think you as beautiful now?' were his salt to her horrifying wound."
    m 2dsd "Shortly after, the woman died."
    m "She couldn't live further after she was tarnished and treated like a freak by everyone around her."
    m 1esc "Her husband, denounced by his cruelty, committed seppuku shortly after."
    m 3eud "The woman, dying from such a fate, became a vengeful and malicious spirit."
    m "They say she now wanders around aimlessly at night, her face covered with a mask and a bladed weapon on her hands."
    m 1dsd "Anyone unlucky enough to come across her will hear her spine-chilling question..."
    m 1cua "{b}{i}Am I p r e t t y?{/i}{/b}"
    # 1 in 15
    if renpy.random.randint(1,15) == 1 or mas_full_scares or persistent._mas_pm_likes_spoops:
        hide monika
        show screen tear(20, 0.1, 0.1, 0, 40)
        play sound "sfx/s_kill_glitch1.ogg"
        show natsuki ghost2 zorder 73 at i11
        show k_rects_eyes1 zorder 74
        show k_rects_eyes2 zorder 74
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
                jump mas_scary_story_kuchisake_onna.clean
            "No":
                jump mas_scary_story_kuchisake_onna.no
    else:
        jump mas_scary_story_kuchisake_onna.end

label .no:
    hide screen mas_background_timed_jump
    "{b}{i}Is that, so?{w=1.0}{nw}{/i}{/b}"
    $ _history_list.pop()
    $ _history_list.pop()
    $ pause(1.0)
    hide natsuki
    play sound "sfx/run.ogg"
    show natsuki mas_ghost onlayer front at i11
    $ pause(0.25)
    hide natsuki mas_ghost onlayer front

label .clean:
    show black zorder 100
    hide k_rects_eyes1
    hide k_rects_eyes2
    hide natsuki
    $ pause(1.5)
    hide black
    $ style.say_dialogue = style.default_monika
    show monika 1eua at i11 zorder MAS_MONIKA_Z

label .end:
    m 3eud "The fate she gives you depends on your answer, actually."
    m "Meeting her isn't always certain to seal your doom."
    m 3esc "However..."
    m "If you're not smart with how you deal with the question..."
    m 3tku "You might just end up like her."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_o_tei",
    category=[store.mas_stories.TYPE_SCARY], prompt="The tale of O-Tei",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_o_tei:
    call mas_scary_story_setup
    m 1eua "A long time ago, there lived a man named Kenji, who was studying to be a physician."
    m 3eub "He was engaged to a young woman named Tomoe and they were to be married after he finished his studies."
    m 1esd "Unfortunately, Tomoe contracted a serious illness before that could happen."
    m 2dsd "It wasn't long until she was bedridden, nearing the end of her life."
    m 2esd "Kenji knelt by her bedside, and she said to him, 'We have been promised to each other since childhood...'"
    m 4ekd "'Unfortunately with this frail body of mine, my time has come and I am going to die before I could become your wife.'"
    m 3ekd "'Please do not grieve when I go. I believe we shall meet again.'"
    m 3eud "He asked, 'How would I know of your return?'"
    m 2dsc "Unfortunately, she had succumbed before she could give him an answer."
    m "Kenji grieved deeply for the loss of his love, taken too soon from him."
    m 2esc "He never forgot about Tomoe as time moved on, but he was required to marry someone else and preserve the family name."
    m "He soon married another girl, but his heart stayed somewhere else."
    m 2esd "And as everything does in life, his family too had been taken by time and he was left all alone again."
    m 4eud "It was then that he decided to abandon his home and take a long journey to forget his troubles."
    m 1euc "He travelled all around the country, searching for a cure to his malaise."
    m "And then on one evening, he came across an inn and stopped there to rest."
    m "As he settled down in his room, a nakai opened the door to greet him."
    m 3eud "His heart leapt..."
    m 3wud "The girl that greeted him looked exactly like Tomoe."
    m "Everything he saw in her reminded him perfectly of his past love."
    # 1 in 9
    if renpy.random.randint(1,9) == 1 or mas_full_scares or persistent._mas_pm_likes_spoops:
        show yuri eyes zorder 73 at otei_appear(a=0.075,time=4.0)
        show yuri eyes_base zorder 72 at otei_appear(a=0.085,time=3.0)
        show yuripupils zorder 74 at otei_appear(a=0.095,time=5.0)
    m 1eud "Kenji then remembered the last words they exchanged before her departure."
    m "He flagged down the girl and told her, 'I'm sorry to be a bother, but you remind me so much of someone I knew long ago that it startled me at first.'"
    m "'If you don't mind me asking, what is your name?'"
    m 3wud "Immediately, in the unforgotten voice of his deceased beloved, the girl answered, 'My name is Tomoe, and you are Kenji, my promised husband.'"
    m 1wud "'I had died tragically before we could complete our marriage...'"
    m "'And now I have returned, Kenji, my husband-to-be.'"
    hide yuri
    hide yuripupils
    m 1dsc "The girl then collapsed to the floor, unconscious."
    m 1esa "Kenji held her to his arms, tears flowing from his face."
    m 1dsa "'...Welcome back, Tomoe...'"
    m 3esa "As she came to, she had no memory of what happened in the inn."
    m 1hua "Not long after, Kenji married her as soon as they could, and lived on happily for the rest of their lives."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_mujina",
    category=[store.mas_stories.TYPE_SCARY], prompt="Mujina",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_mujina:
    call mas_scary_story_setup
    m 1esc "One night at a late hour, an old merchant was walking down a road heading home after a long day of selling his wares."
    m 3esc "The road he travelled on led to a large hill that was very dark and secluded at night so many travelers tended to avoid the area."
    m "The man was tired, however, and decided to take the road anyways since it would get him home quicker."
    m "On the one side of the hill was an old moat that was quite deep."
    m 3eud "As he went along, he noticed a woman crouching by the moat, all alone and weeping bitterly."
    m "Although the man was exhausted, he feared the woman intended to throw herself into the water, so he stopped."
    m 3euc "She was petite and well-dressed, covering her face with one of the sleeves of her kimono facing away from him."
    m 3eud "The man said to her, 'Miss, please don't cry. What is the matter? If there is anything I can do to help you, I would be glad to do it.'"
    m "The woman kept crying, however, ignoring him."
    m 3ekd "'Miss, listen to me. This is no place for a lady at night. Please, let me help you.'"
    m 1euc "Slowly, the woman rose up, still sobbing."
    m 1dsc "The man laid his hand lightly on her shoulder..."
    m 4wud "When she abruptly turned her head to him, showing a blank face, void of all human features."
    m 4wuw "No eyes, mouth, or nose. Just an empty visage that stared back at him!"
    m "The merchant ran away as fast as he could, panicking from the haunting figure."
    m 1efc "He continued to run until he saw the light of a lantern and ran towards it."
    m 3euc "The lantern belonged to a travelling salesman that was walking along."
    m 1esc "The old man stopped in front of him, doubled over to catch his breath."
    m 3esc "The salesman asked why the man was running."
    m 4ekd "'A m-monster! There was a girl with no face by the moat!' the merchant cried."
    # 1 in 10
    if renpy.random.randint(1,10) == 1 or mas_full_scares or persistent._mas_pm_likes_spoops:
        $ style.say_dialogue = style.edited
        m 2tub "The salesman responded, 'Oh, you mean...{w=2} {b}like this?{/b}'{nw}"
        show mujina zorder 75 at otei_appear(a=1.0,time=0.25)
        play sound "sfx/glitch1.ogg"
        $ style.say_dialogue = style.default_monika
        $ pause(0.4)
        stop sound
        hide mujina
    else:
        m 2tub "The salesman responded 'Oh, you mean like this?'"
    m 4wud "The man looked up at the salesman and saw the same horrifying emptiness from the girl."
    m "Before the merchant could get away, the void let out a high pitch screech..."
    m 1dsc "...And then there was darkness."
    show black zorder 100
    $ pause(3.5)
    hide black
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_ubume",
    category=[store.mas_stories.TYPE_SCARY], prompt="The ubume",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_ubume:
    call mas_scary_story_setup
    m 3euc "One night at a late hour, a woman walked into a confectionery store to buy some candy right before the owner was about to head off to bed."
    m 1esc "The village was small, and the confectioner didn't recognize the woman, but didn't think much of it."
    m "He tiredly sold the woman the candy that she requested."
    m 1euc "The next night around the same time, the same woman walked into the shop to buy some more candy."
    m "She continued to visit the shop nightly, until the confectioner became curious about the woman and decided to follow her the next time she came in."
    m 1esd "The next night, the woman arrived at her usual time, purchased the candy that she always did, and went happily on her way."
    m 3wud "After she walked out the door, the confectioner looked into his money box and saw the coins that the woman had given to him turned into leaves from a tree."
    # 1 in 20
    if renpy.random.randint(1,20) == 1 or mas_full_scares or persistent._mas_pm_likes_spoops:
        play sound "sfx/giggle.ogg"
    m 1euc "He followed the woman to the outside of a nearby temple, where she simply vanished."
    m 1esc "The confectioner was shocked by this and decided to head back home."
    m 3eud "The next day, he went to the temple and told the monk there what he saw."
    m 1dsd "The priest told the confectioner that a young woman that was travelling through the village recently had suddenly died on the street."
    m "The monk felt compassion for the poor dead woman, as she had been in her last month of pregnancy."
    m 1esc "He had her buried in the cemetery behind the temple and gave her and her child safe passage to the afterlife."
    m 4eud "As the monk led the confectioner to the site of the grave, they both heard a baby crying from beneath the ground."
    m "Immediately, they fetched a couple of shovels and dug up the grave."
    m 1wuw "Much to their shock, they found a newborn baby boy sucking on a piece of candy."
    m "Candy that the confectioner had always sold to the woman."
    m 1dsd "They lifted the boy out of the grave and the monk would take him as his own to raise."
    m 1esc "And the woman's ghost was never seen ever again."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_womaninblack",
    category=[store.mas_stories.TYPE_SCARY], prompt="The woman in black",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_womaninblack:
    call mas_scary_story_setup
    m 3esd "One night, a colonel boarded a train on his way home."
    m 1esd "When he found a comfortable spot to sit, he fell asleep from the day's fatigue."
    m 3eud "A short time later, he awoke abruptly feeling stiff and uneasy."
    m "To his surprise, he noticed that there was now a woman sitting opposite of him."
    m "Her attire was entirely black, including a veil that obscured her face."
    m 1esc "She appeared to be looking down at something in her lap, although there wasn't anything there."
    m 3esd "The colonel was a friendly fellow and tried to make small talk with her."
    m 1dsd "To his dismay, she did not respond to his pleasantries."
    m 1esc "Suddenly, she began rocking back and forth and singing a soft lullaby."
    m "Before the colonel could inquire about it, the train screeched to a halt."
    m "A suitcase from the compartment above fell and hit him on the head, knocking him unconscious."
    show black zorder 100
    play sound "sfx/crack.ogg"
    $ pause(1.5)
    hide black
    m 3eud "When he came to, the woman was gone. The colonel questioned some of the other passengers, but none of them had seen her."
    m 3ekd "To boot, once the colonel had entered the compartment it was locked, as was customary, and no one had entered or left the compartment after he had entered."
    m 1esc "When he exited the train, a railway official that overheard him talked to the colonel about the woman he was asking about."
    m "According to the official, a woman and her husband were travelling on a train together."
    m 1dsd "The husband had his head too far out in one of the windows and was decapitated by a wire."
    m "His body then fell onto her lap, lifeless."
    m 3wud "When the train arrived at its stop, she was found holding the corpse and singing a lullaby to it."
    m "She never regained her sanity and died shortly after."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_resurrection_mary",
    category=[store.mas_stories.TYPE_SCARY], prompt="Resurrection Mary",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_resurrection_mary:
    call mas_scary_story_setup
    m 3eua "At a dancehall around Christmas time, a young man named Lewis was enjoying some time with his friends, when a young woman he hadn't seen before caught his attention."
    m 1eub "The girl was tall, blonde, blue-eyed, and very beautiful."
    m 1hub "She was wearing a fancy white dress, with white dancing shoes and a thin shawl."
    m 3esb "Lewis found the girl captivating. He decided to ask her to dance with him and she accepted his invitation."
    m 1eud "She was certainly beautiful, but Lewis felt there was something strange about her."
    m 3esd "As they danced, he tried to get to know her a little better, but all she would say about herself was that her name was Mary and that she was from the south side of town."
    m "Also, her skin was cool and clammy to the touch. At one point during the evening, he kissed Mary, and found her lips were as cool as her skin."
    m 1esb "The two spent much of the night together dancing. When the time came to leave, Lewis offered Mary a ride home and she again accepted the invitation."
    m 3esb "She directed him to drive down a certain road, and he obliged."
    m 3eud "As they were passing the gates of a cemetery, Mary asked Lewis to pull over."
    m 1eud "Although perplexed, Lewis stopped the car as she requested."
    m 3eud "She then opened the door, leaned in towards Lewis and whispered that she had to go and that he could not go with her."
    m 1euc "She got out of the car and walked towards the cemetery gate before disappearing."
    m "Lewis sat in the car for a long time bewildered by what had just happened."
    m 1esd "He never saw the beautiful woman ever again."
    # 1 in 20
    if renpy.random.randint(1,20) == 1 or mas_full_scares or persistent._mas_pm_likes_spoops:
        play sound "sfx/giggle.ogg"
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_corpse",
    category=[store.mas_stories.TYPE_SCARY], prompt="The resuscitated corpse",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_corpse:
    call mas_scary_story_setup
    m 1esa "There once was an old man that ran an old roadside inn. One evening, 4 men arrived and asked for a room."
    m 3eua "The old man replied that all of the rooms were taken, but he could find them a place to sleep if they weren't too particular."
    m 1esa "The men were exhausted and assured the man that any place would do."
    m 1eud "He led them to a room around back. Lying in the corner of the room was the corpse of a woman."
    m "He explained that his daughter-in-law had recently perished and she was awaiting burial."
    m 1eua "After the old man departed, 3 of the 4 men fell asleep. The last man couldn't fall asleep."
    m 1wuo "Suddenly, the man heard a creaking noise."
    if renpy.random.randint(1,2) == 1 or mas_full_scares or persistent._mas_pm_likes_spoops:
        play sound "sfx/crack.ogg"
    m 3wuo "He looked up and in the light of the lamp, he saw the woman rise, now bearing fangs and fingernails that looked like claws, advancing towards them."
    m "She bent down and bit each of the sleeping men. The fourth man, at the last second, pulled up a pillow in front of his neck."
    m 1eud "The woman bit the pillow and apparently not realizing she hadn't bit the last man, returned to her original resting spot."
    m 3eud "The man kicked his companions, but none of them moved. The man decided to take his chances and make a run for it."
    m 3wuo "As soon as his feet touched the ground, however, he heard another creak."
    if renpy.random.randint(1,2) == 1 or mas_full_scares or persistent._mas_pm_likes_spoops:
        play sound "sfx/crack.ogg"
    m "Realizing that the woman was again rising from her spot, he opened the door and ran as fast as he could."
    # need opinions on this one since it's for storytelling purposes
    show layer master at heartbeat2(1)
    show vignette as flicker zorder 72 at vignetteflicker(0)
    play sound hb loop
    m 3eud "After a short distance, he looked behind him and saw that the corpse was not far behind him."
    m 3wud "A chase ensued and as she caught up to him, he found himself standing under a tree."
    m "She charged towards him with her claw-like fingernails extended."
    m 4wud "At the last second, the man dodged and she struck the tree with great ferocity."
    m 3wud "Her fingernails were now deeply embedded in the tree."
    m 1wud "She wildly swung her freehand at the man as he lay on the ground, unable to reach him."
    m 1eud "The man, frightened and exhausted crawled a short distance away and then passed out."
    show layer master
    stop sound
    hide flicker
    show black zorder 100
    $ pause(2.5)
    hide black
    m 1esd "The next morning a passing police officer found the man and brought him back to consciousness."
    m "The man recounted what had happened. The officer, thinking the man was a drunkard, walked the man back to the inn."
    m 1eud "As they arrived, the inn was in a state of great commotion."
    m 3eud "The 3 travelers had been found dead in their beds."
    m "The body of the daughter-in-law was lying where she had been the night before, but now her clothes were soiled with blood and a piece of bark was found under her fingernail."
    m 3esd "After some questioning, the innkeeper finally admitted that the woman had died six months previously and he was trying to save enough money to give her a proper burial."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_jack_o_lantern",
    category=[store.mas_stories.TYPE_SCARY], prompt="Jack O Lantern",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_jack_o_lantern:
    call mas_scary_story_setup
    # chance of 1 in 4
    $ _mas_jack_scare = renpy.random.randint(1,4) == 1
    m 4esd "There was once a man named Jack. Jack was a miserable, old drunk who took pleasure in playing tricks on people."
    m 3esa "One night, Jack ran into the Devil and invited him to have a drink with him."
    m "After Jack had had his fill, he turned to the Devil and asked him to turn into a coin so he could pay for their drinks, as he didn't have the money to pay for them."
    m 1esa "Once the Devil did so, Jack pocketed the coin and walked out without paying."
    m "The Devil could not turn back to his original form because Jack had put it into his pocket next to a silver cross."
    m 3esa "Jack eventually freed the Devil, under the condition that he would not bother Jack for 1 year and that, should Jack die, he would not claim his soul."
    m "The next year, Jack ran into the Devil again. This time he tricked him into climbing into a tree to pick a piece of fruit."
    m 3esd "While he was in the tree, Jack surrounded it with white crosses so that the Devil could not come down."
    m "Once the Devil promised not to bother him again for another 10 years, Jack removed them. When Jack died, he went to Heaven."
    m 1eud "When he arrived, he was told he could not enter for how poorly a life he had lived on Earth."
    m 1eua "So, he went down to Hell, where the Devil kept his promise and would not allow Jack to enter."
    m 1eud "Jack became scared, for he had no place to go."
    m 1esd "Jack asked the Devil how he could leave, as there was no light."
    if _mas_jack_scare or mas_full_scares or persistent._mas_pm_likes_spoops:
        hide vignette
        show darkred zorder 82:
            alpha 0.85
    m 1eud "The Devil tossed Jack an ember from the flames of Hell to help Jack light his way."
    m "Jack pulled out a turnip he had with him, carved it out, and placed the ember inside of it."
    m 3eua "From that day onward, Jack roamed the earth without a resting place, lighting the way as he went with his Jack O'Lantern."
    if _mas_jack_scare or mas_full_scares or persistent._mas_pm_likes_spoops:
        hide darkred
        show vignette zorder 70
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_baobhan_sith",
    category=[store.mas_stories.TYPE_SCARY], prompt="Baobhan Sith",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_baobhan_sith:
    call mas_scary_story_setup
    m 1esa "There was once a young group of hunters, who stopped for the night in a small hunting lodge."
    m 3esb "As the men settled in, they built a fire, and began eating and drinking merrily, for it had been a good day."
    m 1tku "They said to themselves the only thing that they lacked was the company of some beautiful women by their sides."
    m 1tsb "Not too long after they said this, there came a knock at their door."
    m 3eub "There in the doorway stood four beautiful women."
    m "The women, having become lost in the wilderness, asked if they may join the men in their shelter for the night."
    m 1tku "The men, silently congratulating themselves on their good fortunes, invited the women in."
    m 1esa "After a while of enjoying each other's company, the women expressed a wish to dance."
    m 1tku "The men wasted no time coupling off with each of the maidens."
    m 1eub "As they are dancing, one of the men notices that the other couples are dancing rather erratically."
    m 1wuo "Then, to his horror, he realizes that the other men have blood pouring from their necks onto their shirts."
    m 3wuo "In a blind panic, the man abandoned his partner and bolted out the door, before he could share the fate of his friends."
    m 3wud "He ran into the forest and hid amongst the horses he and his friends had ridden during that day's hunt."
    m "The women, not far behind, closed in, but appeared unable to get past the horses to the man."
    m 1eud "So there he stood, weary eyed, among the animals all night long as the women circled around the horses, trying to find a way to get to him."
    m 1esa "Just before dawn, the women gave up and retreated back into the woods."
    m 1esd "Now alone, the man cautiously headed back towards the hunting lodge, hearing no sound from within."
    # chance of 1 in 14
    if renpy.random.randint(1,14) == 1 or mas_full_scares or persistent._mas_pm_likes_spoops:
        play sound "sfx/stab.ogg"
        show blood splatter1 as bl2 zorder 73:
            pos (50,95)
        show blood splatter1 as bl3 zorder 73:
            pos (170,695)
        show blood splatter1 as bl4 zorder 73:
            pos (150,395)
        show blood splatter1 as bl5 zorder 73:
            pos (950,505)
        show blood splatter1 as bl6 zorder 73:
            pos (700,795)
        show blood splatter1 as bl7 zorder 73:
            pos (1050,95)
        $ pause(1.5)
        stop sound
        hide bl2
        hide bl3
        hide bl4
        hide bl5
        hide bl6
        hide bl7
    m 3wuo "When he looked inside, he saw his three comrades dead on the floor, their skin almost translucent, as they lay in a pool of their own blood."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_serial_killer",
    category=[store.mas_stories.TYPE_SCARY], prompt="The serial killer",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_serial_killer:
    call mas_scary_story_setup
    m 3tub "A young couple parked their car next to a large willow tree at a cemetery one night for some undisturbed 'lovemaking.'"
    m 3euc "After a while, they were interrupted by a radio report that a notorious serial killer had escaped from a psychiatric hospital nearby."
    m "Worried about their safety, they decided to continue elsewhere."
    m 1esc "However...{w} The car wouldn't start at all."
    m 3esd "The young man got out of the car to look for help and told the girl to stay inside with the doors locked."
    m 3wud "A few moments later, she was startled when she heard an eerie scratching sound on the roof of the car."
    m 1eud "She thought to herself that it must've been a tree branch in the wind."
    m 1euc "After a long time had passed, a police car drove by and stopped but still no sight of her boyfriend."
    m 1eud "The police officer went to the car and instructed the girl to exit the vehicle and walk toward him and not look back."
    m "She did so slowly..."
    m 1ekc "The girl then noticed numerous other police cars arriving with their sirens blaring behind the first one to arrive."
    m 1dsd "Curiosity then got the better of her and she turned to look at the car..."
    m 4wfw "She saw her boyfriend upside down and hanging from the tree above their car with his neck slit wide open..."
    # chance of 1 in 8
    if renpy.random.randint(1,8) == 1 or mas_full_scares or persistent._mas_pm_likes_spoops:
        show y_sticker hopg zorder 74:
            pos(600,425)
            alpha 1.0
            linear 1.6 alpha 0
        play sound "<from 0.4 to 2.0 >sfx/eyes.ogg"
    m 1dfc "...And his broken and bloody fingernails on the roof."
    hide y_sticker
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_revenant",
    category=[store.mas_stories.TYPE_SCARY], prompt="The Revenant",unlocked=False),
    eventdb=store.mas_stories.story_database)

label mas_scary_story_revenant:
    call mas_scary_story_setup
    m 4eua "There was once a man who married a woman."
    m 4ekd "He was a wealthy person who made his money through ill-gotten means."
    m 2eud "Shortly after their marriage, he started to hear rumors that his wife was being unfaithful to him."
    m 2esd "Anxious to ascertain the truth, the man told his wife he was going away on a business trip for a few days and left the house."
    m 2eud "Unbeknownst to his wife, the man snuck back into the house later in the evening with the aid of one of his servants."
    m "The man climbed up one of the beams overhanging in his bedchamber and laid in wait."
    m 4ekd "Shortly afterwards his wife entered with a man of the neighborhood, the two chatted for a while and then began to undress themselves."
    m 4eud "The man, at this time, clumsily fell to the ground not far from where the two were, unconscious."
    m "The adulterer grabbed his clothes and ran away, but the wife came over to her husband and gently patted his hair until he awoke."
    m "The man chastised his wife for her adultery and threatened punishment once he recovered from his fall."
    m 2dsc "The man, however, never recovered from his fall and died overnight. He was buried the next day."
    m 2esd "That night, the man's corpse rose up from his grave and began to wander the neighborhoods."
    m "As dawn broke, he would return to his grave."
    m 3esd "This continued night after night and people began locking their doors, fearing to go out to run any errands after the sun went down."
    m "Lest they run into the creature and be beaten black and blue."
    m 2dsd "Not long afterwards, the town became plagued by disease and there was no doubt in their minds that the corpse was to blame."
    m 2dsc "People started fleeing the town, lest they too should die by the disease."
    m 2esd "As the town was falling apart, a meeting was gathered and it was decided that the corpse should be dug up and disposed of."
    m "A group of people took spades and found the cemetery the man was buried in."
    m "They didn't have to dig long before they reached the man's corpse."
    m 4eud "Once he was fully disinterred, the villagers beat the carcass with their shovels and dragged the body out of town."
    m 3esd "There, they built a great fire and threw the body on the fire."
    m 3eub "The man's corpse let out a blood curdling scream and attempted to crawl out of the flames before finally succumbing to it."
    call mas_scary_story_cleanup
    return
