#Dict holding seen poems and amount of times seen
#poem_id:shown_count
default persistent._mas_poems_seen = dict()

#Monika's text font
style mas_monika_poem_text:
    font "mod_assets/font/m1_fixed.ttf"
    size 34
    color "#000"
    outlines []

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
        "monika": "mas_monika_poem_text",
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
                for poem in poem_map.values()
                if not poem.is_seen() and poem.category == category
            ]

        #Otherwise we just get all
        return [
            poem
            for poem in poem_map.values()
            if poem.category == category
        ]

    def getSeenPoems():
        """
        Returns a list of all seen poems ordered by category
        """
        return sorted([
            poem
            for poem in poem_map.values()
            if poem.is_seen()
        ], key=poem_sort_key)

    def getUnseenPoems():
        """
        Returns a list of all unseen poems ordered by category
        """
        return sorted([
            poem
            for poem in poem_map.values()
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
            for poem in poem_map.values()
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


## Stock DDLC poems
init 20 python:
    poem_m1 = MASPoem(
        poem_id="poem_m1",
        category="ddlc",
        prompt="Hole in Wall (Part 1)",
        title = "",
        text = """\
It couldn't have been me.
See, the direction the spackle protrudes.
A noisy neighbor? An angry boyfriend? I'll never know. I wasn't home.
I peer inside for a clue.
No! I can't see. I reel, blind, like a film left out in the sun.
But it's too late. My retinas.
Already scorched with a permanent copy of the meaningless image.
It's just a little hole. It wasn't too bright.
It was too deep.
Stretching forever into everything.
A hole of infinite choices.
I realize now, that I wasn't looking in.
I was looking out.
And he, on the other side, was looking in.\
"""
    )

    poem_m21 = MASPoem(
        poem_id="poem_m21",
        category="ddlc",
        prompt="Hole in Wall (Part 2)",
        title = "",
        text = """\
But he wasn't looking at me.
Confused, I frantically glance at my surroundings.
But my burned eyes can no longer see color.
Are there others in this room? Are they talking?
Or are they simply poems on flat sheets of paper,
The sound of frantic scrawling playing tricks on my ears?
The room begins to crinkle.
Closing in on me.
The air I breathe dissipates before it reaches my lungs.
I panic. There must be a way out.
It's right there. He's right there.

Swallowing my fears, I brandish my pen.\
"""
    )

    poem_m2 = MASPoem(
        poem_id="poem_m2",
        category="ddlc",
        prompt="Save Me",
        title = "",
        text = """\
The colors, they won't stop.
Bright, beautiful colors
Flashing, expanding, piercing
Red, green, blue
An endless
cacophony
Of meaningless
noise


The noise, it won't stop.
Violent, grating waveforms
Squeaking, screeching, piercing
Sine, cosine, tangent
    Like playing a chalkboard on a turntable
        Like playing a vinyl on a pizza crust
An endless
poem
Of meaningless\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
Load Me
    \
"""
    )

    poem_m3 = MASPoem(
        poem_id="poem_m3",
        category="ddlc",
        prompt="The Lady who Knows Everything",
        title = "",
        text = """\
An old tale tells of a lady who wanders Earth.
The Lady who Knows Everything.
A beautiful lady who has found every answer,
All meaning,
All purpose,
And all that was ever sought.

And here I am,


              a feather


Lost adrift the sky, victim of the currents of the wind.

Day after day, I search.
I search with little hope, knowing legends don't exist.
But when all else has failed me,
When all others have turned away,
The legend is all that remains - the last dim star glimmering in the twilit sky.

Until one day, the wind ceases to blow.
I fall.
And I fall and fall, and fall even more.
Gentle as a feather.
A dry quill, expressionless.

But a hand catches me between the thumb and forefinger.
The hand of a beautiful lady.
I look at her eyes and find no end to her gaze.

The Lady who Knows Everything knows what I am thinking.
Before I can speak, she responds in a hollow voice.
"I have found every answer, all of which amount to nothing.
There is no meaning.
There is no purpose.
And we seek only the impossible.
I am not your legend.
Your legend does not exist."

And with a breath, she blows me back afloat, and I pick up a gust of wind.\
"""
    )

    poem_m4 = MASPoem(
        poem_id="poem_m4",
        category="ddlc",
        prompt="Happy End",
        title = "",
        text = """\
Pen in hand, I find my strength.
The courage endowed upon me by my one and only love.
Together, let us dismantle this crumbling world
And write a novel of our own fantasies.

With a flick of her pen, the lost finds her way.
In a world of infinite choices, behold this special day.

After all,
Not all good times must come to an end.\
"""
    )


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
