#Dict holding seen poems and amount of times seen
#poem_id:shown_count
default persistent._mas_poems_seen = dict()

init python in mas_poems:
    import store
    poem_map = dict()

    poem_sort_key = lambda x:x.category
    poem_menu_sort_key = lambda x:x[1].category

    paper_cat_map = {
        "f14": "mod_assets/poem_assets/poem_vday.jpg",
        "d25": "mod_assets/poem_assets/poem_d25.png",
        "ff": "mod_assets/poem_assets/poem_finalfarewell.png"
    }

    author_font_map = {
        "monika": "monika_text",
        "chibika": "chibika_note_text"
    }

    #If we've got pbday, let's also add this here.
    if store.persistent._mas_player_bday is not None:
        paper_cat_map["pbday"] = "mod_assets/poem_assets/poem_pbday_" + str(store.persistent._mas_player_bday.month) + ".png"

    def hasUnlockedPoems():
        """
        Checks if we have any poems that we've unlocked.
        """
        return len(store.persistent._mas_poems_seen) > 0

init 11 python in mas_poems:
    import store

    def getPoemsByCategory(category, unseen=False):
        """
        Returns a list of poems by the category provided

        IN:
            category:
                category to search for

            unseen:
                whether or not we only want unseen poems

        OUT:
            A list of poems based on the specifications above
        """

        #If we only want unseen, do this
        if unseen:
            return [
                poem
                for poem in poem_map.itervalues()
                if not poem.is_seen() and poem.category == category
            ]

        #Otherwise we just get all
        return [
            poem
            for poem in poem_map.itervalues()
            if poem.category == category
        ]

    def getSeenPoems():
        """
        Returns a list of all seen poems ordered by category
        """
        return sorted([
            poem
            for poem in poem_map.itervalues()
            if poem.is_seen()
        ], key=poem_sort_key)

    def getUnseenPoems():
        """
        Returns a list of all unseen poems ordered by category
        """
        return sorted([
            poem
            for poem in poem_map.itervalues()
            if not poem.is_seen()
        ], key=poem_sort_key)

    def getPoem(poem_id):
        """
        Gets a poem by id

        IN:
            poem_id - poem id of the poem to get

        OUT:
            MASPoem if there's a poem with the id
            None if no poem with the id exists
        """
        return poem_map.get(poem_id, None)

    def getSeenPoemsMenu():
        """
        Gets a list of seen poems in scrollable menu format (ordered by category)

        OUT:
            A list of seen poems in the format for a mas gen scrollable menu
        """
        return sorted([
            (poem.prompt, poem, False, False)
            for poem in poem_map.itervalues()
            if poem.is_seen()
        ], key=poem_menu_sort_key)

    def getRandomPoem(category,unseen=True):
        """
        Gets a random poem from the specified category
        IN:
            category:
                category to search for

            unseen:
                whether or not we only want unseen poems
                defaults to True

        OUT:
            A random poem
        """
        unseen_poem_amt = len(getPoemsByCategory(category, unseen=True))
        total_poem_amt = len(getPoemsByCategory(category, unseen=False))
        sel_poem_len = total_poem_amt-1

        if unseen:
            if unseen_poem_amt > 0:
                sel_poem_len = unseen_poem_amt-1
            else:
                unseen = False
        poem_num = renpy.random.randint(0, sel_poem_len)

        return getPoemsByCategory(category, unseen=unseen)[poem_num]

init 10 python:
    #Used ex_props:
    # KEY : VALUE
    # sad : ignored - Whether or not we should use sad dialogue pre-poem show/post poem show in the show poem topic
    class MASPoem:
        def __init__(
            self,
            poem_id,
            category,
            prompt,
            paper=None,
            title="",
            text="",
            author="monika",
            ex_props=None
        ):
            """
            MASPoem constructor

            Similar to the Poem class from DDLC, but excludes the yuri variables and adds a poem id property.


            poem_id:
                identifier for the poem.
                (NOTE: Must be unique)

            category:
                category for the poem is under (So we can get poems by category)

            prompt:
                prompt for this poem (So it can be viewed by a scrollable menu)

            paper:
                paper to use for this poem. If None, assumes from the paper category map
                    (Default: None)

            title:
                poem title (supports renpy substitution)
                    (Default: '')

            text:
                poem contents (supports renpy substitution)
                    (Default: '')

            author:
                poem author
                (Default: monika)

            ex_props:
                extra tags for the poem (used for dialogue flow based on it)
                If None, an empty dict is assumed
                    (Default: None)
            """
            if poem_id in store.mas_poems.poem_map:
                raise Exception ("poem_id {0} already exists in the poem map.".format(poem_id))

            self.poem_id=poem_id
            self.category=category
            self.prompt=prompt
            self.paper=paper
            self.title=title
            self.text=text
            self.author=author
            self.ex_props = dict() if ex_props is None else ex_props

            #And add this to map
            store.mas_poems.poem_map[poem_id] = self

        def is_seen(self):
            """
            Checks if the poem is seen

            OUT:
                boolean:
                    - True if poem was seen before
                    - False otherwise
            """
            return self.poem_id in store.persistent._mas_poems_seen

        def get_shown_count(self):
            """
            Gets the shown count of the poem

            OUT:
                integer:
                    - The amount of times this poem was seen
            """
            return store.persistent._mas_poems_seen.get(self.poem_id, 0)

#### mas_showpoem ####
#Handles showing poems and automatically incrementing the shown counts of MASPoems
#Can also show normal poems
#
#IN:
#   poem - poem to show
#   paper - paper to use
#       If None, and the poem is a MASPoem, it attempts to get paper by the category if the poem object itself does not have paper passed in
#       If nothing can be found, it defaults to paper.
#       Normal poems use the standard paper by default if None.
#       (Default: None)
#   background_action_label - label to handle background setup with (Default: None)
label mas_showpoem(poem=None, paper=None, background_action_label=None):
    #No poem? That's not right. Return
    if poem == None:
        return

    $ is_maspoem = isinstance(poem, MASPoem)
    if paper is None:
        if is_maspoem:
            $ paper = poem.paper if poem.paper is not None else mas_poems.paper_cat_map.get(poem.category, "paper")

        else:
            $ paper = "paper"

    #Play the page turn sound
    play sound page_turn

    window hide
    $ afm_pref = renpy.game.preferences.afm_enable
    $ renpy.game.preferences.afm_enable = False

    #Handle the poem screen we use
    show screen mas_generic_poem(poem, paper=paper, _styletext=mas_poems.author_font_map.get(poem.author, "monika_text"))

    with Dissolve(1)

    #If we have a bg_action_label, we execute what it needs to do
    if background_action_label and renpy.has_label(background_action_label):
        call expression background_action_label

    #Wait for user to progress the poem
    $ pause()

    #And hide it
    hide screen mas_generic_poem

    with Dissolve(.5)

    $ renpy.game.preferences.afm_enable = afm_pref
    window auto

    #Flag this poem as seen
    #We only want to increment showns of MASPoems, since only they have the poem_id attribute
    #NOTE: If the poem has no title, we can assume that this shouldn't be unlocked
    if is_maspoem and poem.prompt:
        if poem.poem_id in persistent._mas_poems_seen:
            $ persistent._mas_poems_seen[poem.poem_id] += 1
        else:
            $ persistent._mas_poems_seen[poem.poem_id] = 1
    return

#Poem accessor topic
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_showpoem",
            prompt="Can I read one of your poems again?",
            category=["literature"],
            pool=True,
            unlocked=True,
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None},
            aff_range=(mas_aff.ENAMORED,None)
        )
    )


label monika_showpoem:
    show monika 1eua at t21
    python:
        #We'll store the base DDLC poems here
        poems_list = [
            ("Hole in Wall (Part 1)", poem_m1, False, False),
            ("Hole in Wall (Part 2)", poem_m21, False, False),
            ("Save Me", poem_m2, False, False),
            ("The Lady Who Knows Everything", poem_m3, False, False),
            ("Happy End", poem_m4, False, False)
        ]

        ret_back = ("Nevermind", False, False, False, 20)
        #Extend the new poems
        poems_list.extend(mas_poems.getSeenPoemsMenu())

        renpy.say(m, "Which poem would you like to read?", interact=False)

    call screen mas_gen_scrollable_menu(poems_list, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ret_back)

    $ _poem = _return

    if not _poem:
        return "prompt"


    show monika at t11

    $ is_sad = isinstance(_poem, MASPoem) and "sad" in _poem.ex_props
    if is_sad:
        m 1rkc "Alright, [player]..."
        show monika 1esc

    else:
        m 3hua "Alright!"

    call mas_showpoem(_poem)

    if not is_sad:
        m 3eka "I hope you liked it, [player]."

    m 1eka "Would you like to read another poem?{nw}"
    $ _history_list.pop()
    menu:
        m "Would you like to read another poem?{fast}"

        "Yes.":
            jump monika_showpoem

        "No.":
            m 1eua "Alright, [player]."
    return
