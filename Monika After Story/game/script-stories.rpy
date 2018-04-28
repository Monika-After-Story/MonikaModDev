
# store containing mood-related data
init -1 python in mas_stories:

    # pane constants
    # most of these are the same as the unseen area consants
    STORY_X = 680
    STORY_Y = 40
    STORY_W = 560
    STORY_H = 640
    STORY_XALIGN = -0.05
    STORY_AREA = (MOOD_X, MOOD_Y, MOOD_W, MOOD_H)
    STORY_RETURN = "I changed my mind"


# entry point for stories flow
label mas_stories_start:
    python:
        import store.evhand as evhand
        import store.mas_stories as mas_stories

        # build menu list
        stories_menu_items = [
            (evhand.story_database[k].prompt, k, False, False)
            for k in evhand.story_database
            if evhand.story_database[k].unlocked
        ]

        # also sort this list
        stories_menu_items.sort()

        # final quit item
        final_item = (mas_moods.STORY_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(mood_menu_items, mas_stories.STORY_AREA, mas_stories.STORY_XALIGN, final_item=final_item)

    # return value? then push
    if _return:
        $ pushEvent(_return)

    return _return

# Stories start here
init 5 python:
    addEvent(Event(persistent.story_database,eventlabel="story_tyrant",
        prompt="The cat and the cock",unlocked=True),eventdb=evhand.story_database)

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
        prompt="The cat and the cock",unlocked=True),eventdb=evhand.story_database)

label story_despise:
    m "Ready for story time?."
    m "Ahem."
    m "One hot summer’s day a Fox was strolling through an orchard till he came to a bunch of Grapes just ripening on a vine which had been trained over a lofty branch."
    m 1r "“Just the thing to quench my thirst,” quoth he."
    m 1 "Drawing back a few paces, he took a run and a jump, and just missed the bunch."
    m 1k "Turning round again with a One, Two, Three, he jumped up, but with no greater success."
    m "Again and again he tried after the tempting morsel, but at last had to give it up, and walked away with his nose in the air, saying: “I am sure they are sour.”"
    m "The moral of this story is that: 'It is easy to despise what you cannot get'."
    m "I hope you enjoyed this little story, [player]~"
    return
