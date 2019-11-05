#Dict holding seen poems and amount of times seen
#poem_id:shown_count
default persistent._mas_poems_seen = dict()

init python in mas_poems:
    poem_map = dict()

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
        Returns a list of all seen poems
        """
        return [
            poem
            for poem in poem_map.itervalues()
            if poem.is_seen()
        ]

    def getUnseenPoems():
        """
        Returns a list of all unseen poems
        """
        return [
            poem
            for poem in poem_map.itervalues()
            if not poem.is_seen()
        ]

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
        Gets a list of seen poems in scrollable menu format

        OUT:
            A list of seen poems in the format for a mas gen scrollable menu
        """
        return [
            (poem.prompt, poem, False, False)
            for poem in poem_map.itervalues()
            if poem.is_seen()
        ]


init 10 python:
    class MASPoem:
        def __init__(
            self,
            poem_id,
            category,
            prompt,
            title="",
            text="",
            author="monika"
        ):
            """
            MASPoem constructor

            Similar to the Poem class from DDLC, but excludes the yuri variables and adds a poem id property.


            poem_id:
                identifier for the poem. (NOTE: Must be unique)

            category:
                category for the poem is under (So we can get poems by category)

            prompt:
                prompt for this poem (So it can be viewed by a scrollable menu)

            title:
                poem title (supports renpy substitution)

            text:
                poem contents

            author:
                poem author (Default: monika)
            """
            if poem_id in store.mas_poems.poem_map:
                raise Exception ("poem_id {0} already exists in the poem map.".format(poem_id))

            self.poem_id=poem_id
            self.category=category
            self.prompt=prompt
            self.title=renpy.substitute(title)
            self.text=text
            self.author=author

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
#   paper - paper to use (Default: "paper")
#   use_mas_poem_screen - whether or not to use the mas_generic_poem screen to display the poem (Default: False)
label mas_showpoem(poem=None, paper="paper", use_mas_poem_screen=False):
    #No poem? That's not right. Return
    if poem == None:
        return

    #Play the page turn sound
    play sound page_turn

    window hide
    $ renpy.game.preferences.afm_enable = False

    #Handle the poem screen we use
    if use_mas_poem_screen:
        show screen mas_generic_poem(poem, paper=paper)
    else:
        show screen poem(poem, paper=paper)

    with Dissolve(1)

    #Wait for user to progress the poem
    $ pause()

    #And hide it
    if use_mas_poem_screen:
        hide screen mas_generic_poem
    else:
        hide screen poem

    with Dissolve(.5)
    window auto

    #Flag this poem as seen
    #We only want to increment showns of MASPoems, since only they have the poem_id attribute
    if isinstance(poem, MASPoem):
        if poem.poem_id in persistent._mas_poems_seen:
            $ persistent._mas_poems_seen[poem.poem_id] += 1
        else:
            $ persistent._mas_poems_seen[poem.poem_id] = 1
    return
