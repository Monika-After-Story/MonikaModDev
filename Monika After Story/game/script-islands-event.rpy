# Monika's ???? Event
# deserves it's own file because of how much dialogue these have

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_islands",
            category=['monika','misc'],
            prompt="Can you show me the floating islands?",
            pool=True
        )
    )

label mas_monika_islands:
    m 1eub "I'll let you admire the scenery for now."
    m 1hub "Hope you like it!"
    $ mas_RaiseShield_core()
    $ mas_OVLHide()
    $ disable_esc()
    $ _mas_island_dialogue = False
    show screen mas_show_islands()
    return

label mas_monika_upsidedownisland:
    if _mas_island_dialogue:
        return
    $ _mas_island_dialogue = True
    m "Oh, that."
    m "I guess you're wondering why that island is upside down, right?"
    m "Well...I was about to fix it until I took another good look at it."
    m "It looks surreal, doesn't it?"
    m "I just feel like there's something special about it."
    m "It's just… mesmerizing."
    $ _mas_island_dialogue = False
    return

label mas_monika_glitchedmess:
    if _mas_island_dialogue:
        return
    $ _mas_island_dialogue = True
    m "Oh, that."
    m "It's something I'm currently working on."
    m "It's still a huge mess, thought. I'm still trying to figure out how to be good at it."
    m "In due time, I'm sure I'll get better at coding!"
    m "Practice makes perfect after all, right?"
    $ _mas_island_dialogue = False
    return

label mas_monika_sky:
    if _mas_island_dialogue:
        return
    $ _mas_island_dialogue = True
    python:
        if morning_flag:
            _mas_sky_events = ["mas_monika_day1","mas_monika_day2",
            "mas_monika_day3"]
        else:
            _mas_sky_events = ["mas_monika_night1","mas_monika_night2"]

        _mas_sky_events.append("mas_monika_daynight1")

        renpy.call(renpy.random.choice(_mas_sky_events))

    $ _mas_island_dialogue = False
    return

label mas_monika_day1:
    m "It's a nice day today."
    m "This weather would be good for a little book reading under the Cherry Blossom tree right, [player]?"
    m "Lying under the shade while reading my favorite book."
    m "Along with a snack and your favorite drink on the side."
    m "Ahh, that'd be really nice to do~"
    return

label mas_monika_day2:
    m "The weather looks nice."
    m "This would definitely be the best time to have a picnic."
    m "We even have a great view to accompany it with!"
    m "Wouldn't it be nice?"
    m "Eating under the Cherry Blossom tree."
    m "Adoring the scenery around us."
    m "Enjoying ourselves with each other's company."
    m "Ahh, that'd be fantastic~"
    return

label mas_monika_day3:
    m "It's pretty peaceful outside."
    m "I wouldn't mind lazing around the grass right now."
    m "Or your head resting on my lap..."
    m "Ah!"
    m "Uh..."
    m "Ahaha!"
    m "N-nevermind!"
    m "Just forget what I said..."
    return

label mas_monika_night1:
    m "You're probably wondering what happend to that orange comet that occassionaly passes by."
    m "Don't worry, I've dealt with it."
    m "I wouldn't want you to get hurt~"
    return

label mas_monika_night2:
    m "Have you ever gone stargazing, [player]?"
    m "Taking some time out of your evening to look at the night sky and to just stare at the beauty of the sky above..."
    m "It's surprisingly relaxing, you know?"
    m "I’ve found that it can really relieve stress and clear your head..."
    m "And seeing all kinds of constellations in the sky just fills your mind with wonder."
    m "Of course, it really makes you realize just how small we are in the universe."
    m "Ahaha..."
    return

label mas_monika_daynight1:
    m "Maybe I should add more shrubs and trees."
    m "Make the islands more prettier you know?"
    m "I just have to find the right flowers and foliage to go with it."
    m "Or maybe each island should have its own set of plants so that everything will be different and have variety."
    m "I'm getting excited thinking about it~"
    return

label mas_back_to_spaceroom:
    if _mas_island_dialogue:
        return
    $ _mas_island_dialogue = True
    menu:
        "Would you like to return, [player]?"
        "Yes":
            hide screen mas_show_islands
            $ mas_DropShield_core()
            $ mas_OVLShow()
            $ enable_esc()
            m 1eua "I hope you liked it, [player]~"
        "No":
            m "Alright, please continue looking around~"
    $ _mas_island_dialogue = False
    return

screen mas_show_islands():
    imagemap:
        if morning_flag:
            ground "mod_assets/location/special/without_frame.png"
        else:
            ground "mod_assets/location/special/night_without_frame.png"

        #alpha False
        # This is so that everything transparent is invisible to the cursor.
        hotspot (11, 13, 314, 270) action Function(renpy.call, "mas_monika_upsidedownisland") # Function(renpy.call_in_new_context(mas_monika_upsidedownisland)) #island upside down
        hotspot (403, 7, 868, 158) action Function(renpy.call, "mas_monika_sky") # Function(renpy.call_in_new_context(mas_monika_sky)) # sky
        hotspot (699, 337, 170, 163) action Function(renpy.call, "mas_monika_glitchedmess") # Function(renpy.call_in_new_context(mas_monika_glitchedmess)) # glitched house
        hotspot (1, 606, 300, 100) action Function(renpy.call, "mas_back_to_spaceroom") # Function(renpy.call_in_new_context(mas_back_to_spaceroom))
