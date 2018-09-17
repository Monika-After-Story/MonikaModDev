# FileReactions framework.
# not too different from events

default persistent._mas_filereacts_failed_map = dict()
default persistent._mas_filereacts_just_reacted = False

init 800 python:
    if len(persistent._mas_filereacts_failed_map) > 0:
        store.mas_filereacts.delete_all(persistent._mas_filereacts_failed_map)

init -1 python in mas_filereacts:
    import store
    import store.mas_utils as mas_utils
    import datetime
    import random

    # file react database
    filereact_db = dict()

    # file reaction filename mapping
    # key: filename or list of filenames
    # value: Event
    filereact_map = dict()

    # currently found files react map
    # NOTE: highly volitatle. Expect this to change often
    # key: lowercase filename, without extension
    # value: on disk filename
    foundreact_map = dict()

    # spare foundreact map, designed for threaded use
    # same keys/values as foundreact_map
    th_foundreact_map = dict()

    # connector quips
    connectors = None
    gift_connectors = None

    def addReaction(ev_label, fname, _action=store.EV_ACT_QUEUE):
        """
        Adds a reaction to the file reactions database.

        IN:
            ev_label - label of this event
            fname - filename to react to
            _action - the EV_ACT to do
                (Default: EV_ACT_QUEUE)
        """
        # lowercase the list in case
        if fname is not None:
            fname = fname.lower()


        # build new Event object
        ev = store.Event(
            store.persistent.event_database,
            ev_label,
            category=fname,
            action=_action
        )

        # add it to the db and map
        filereact_db[ev_label] = ev
        filereact_map[fname] = ev


    def _initConnectorQuips():
        """
        Initializes the connector quips
        """
        global connectors, gift_connectors

        # the connector is a MASQipList
        connectors = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_connectors = store.MASQuipList(allow_glitch=False, allow_line=False)


    def react_to_gifts(found_map, connect=True):
        """
        call this function when you want to check files for reacting to gifts.

        IN:
            found_map - dict to use to insert found items.
                NOTE: this function does NOT empty this dict.
            connect - True will add connectors in between each reaction label
                (Default: True)

        RETURNS:
            list of event labels in the order they should be shown
        """
        GIFT_EXT = ".gift"
        raw_gifts = store.mas_docking_station.getPackageList(GIFT_EXT)

        if len(raw_gifts) == 0:
            return []

        # otherwise we found some potential gifts
        gifts_found = list()
        # now lets lowercase this list whie also buliding a map of files
        for _gift in raw_gifts:
            gift_name, ext, garbage = _gift.partition(GIFT_EXT)
            c_gift_name = gift_name.lower()
            if c_gift_name not in store.persistent._mas_filereacts_failed_map:
                gifts_found.append(c_gift_name)
                found_map[c_gift_name] = _gift

        # then sort the list
        gifts_found.sort()

        # now we are ready to check for reactions
        # first we check for all file reacts:
        #all_reaction = filereact_map.get(gifts_found, None)

        #if all_reaction is not None:
        #    return [all_reaction.eventlabel]

        # otherwise, we need to do this more carefully
        found_reacts = list()
        for index in range(len(gifts_found)-1, -1, -1):
            _gift = gifts_found[index]
            reaction = filereact_map.get(_gift, None)

            if _gift is not None:
                # remove from the list and add to found
                gifts_found.pop()
                found_reacts.append(reaction.eventlabel)
                found_reacts.append(gift_connectors.quip()[1])

        # add in the generic gift reactions
        generic_reacts = list()
        if len(gifts_found) > 0:
            for _gift in gifts_found:
                generic_reacts.append("mas_reaction_gift_generic")
                generic_reacts.append(gift_connectors.quip()[1])
        generic_reacts.extend(found_reacts)

        # gotta remove the extra
        if len(generic_reacts) > 0:
            generic_reacts.pop()
            generic_reacts.insert(0, "mas_reaction_end")

        # now return the list
        return generic_reacts


    def _core_delete(_filename, _map):
        """
        Core deletion file function.

        IN:
            _filename - name of file to delete, if None, we delete one randomly
            _map - the map to use when deleting file.
        """
        if len(_map) == 0:
            return

        # otherwise check for random deletion
        if _filename is None:
            _filename = random.choice(_map.keys())

        file_to_delete = _map.get(_filename, None)
        if file_to_delete is None:
            return

        if store.mas_docking_station.destroyPackage(file_to_delete):
            # file has been deleted (or is gone). pop and go
            _map.pop(_filename)
            return

        # otherwise add to the failed map
        store.persistent._mas_filereacts_failed_map[_filename] = file_to_delete


    def _core_delete_list(_filename_list, _map):
        """
        Core deletion filename list function

        IN:
            _filename - list of filenames to delete.
            _map - the map to use when deleting files
        """
        for _fn in _filename_list:
            _core_delete(_fn, _map)


    def delete_file(_filename):
        """
        Deletes a file off the found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete
                one randomly
        """
        _core_delete(_filename, foundreact_map)


    def delete_files(_filename_list):
        """
        Deletes multiple files off the found_react map

        IN:
            _filename_list - list of filenames to delete.
        """
        for _fn in _filename_list:
            delete_file(_fn)


    def th_delete_file(_filename):
        """
        Deletes a file off the threaded found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete one
                randomly
        """
        _core_delete(_filename, th_foundreact_map)


    def th_delete_files(_filename_list):
        """
        Deletes multiple files off the threaded foundreact map

        IN:
            _filename_list - list of ilenames to delete
        """
        for _fn in _filename_list:
            th_delete_file(_fn)


    def delete_all(_map):
        """
        Attempts to delete all files in the given map.
        Removes files in that map if they dont exist no more

        IN:
            _map - map to delete all
        """
        _map_keys = _map.keys()
        for _key in _map_keys:
            _core_delete(_key, _map)


    _initConnectorQuips()

init python:
    import store.mas_filereacts as mas_filereacts

    def addReaction(ev_label, fname_list, _action=EV_ACT_QUEUE):
        """
        Globalied version of the addReaction function in the mas_filereacts
        store.

        Refer to that function for more information
        """
        mas_filereacts.addReaction(ev_label, fname_list, _action)


    def mas_checkReactions():
        """
        Checks for reactions, then pushes them
        """
        # only check if we didnt just react
        if persistent._mas_filereacts_just_reacted:
            return

        # otherwise check
        mas_filereacts.foundreact_map.clear()
        reacts = mas_filereacts.react_to_gifts(mas_filereacts.foundreact_map)
        if len(reacts) > 0:
            for _react in reacts:
                pushEvent(_react)
            persistent._mas_filereacts_just_reacted = True


### CONNECTORS [RCT000]

# none here!

## Gift CONNECTORS [RCT10]

init 5 python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector_test"
    )

label mas_reaction_gift_connector_test:
    m "this is a test of the connector system"
    return


### REACTIONS [RCT100]

init 5 python:
    addReaction("mas_reaction_generic", None)

label mas_reaction_generic:
    "This is a test"
    return

init 5 python:
    addReaction("mas_reaction_gift_generic", None)

label mas_reaction_gift_generic:
    m "this is a test of the generic gift reaction"
    $ store.mas_filereacts.delete_file(None)
    return

init 5 python:
    addReaction("mas_reaction_gift_test1", "test1")

label mas_reaction_gift_test1:
    m "Thank you for gift test 1!"

    $ gift_ev = mas_getEV("mas_reaction_gift_test1")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init 5 python:
    addReaction("mas_reaction_gift_test2", "test2")

label mas_reaction_gift_test2:
    m "Thank you for gift test 2!"

    $ gift_ev = mas_getEV("mas_reaction_gift_test2")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

## coffee vars
# NOTE: this is just for reference, check sprite-chart for inits
# persistent._mas_acs_enable_coffee
# persistent._mas_coffee_brewing

init 5 python:
    addReaction("mas_reaction_gift_coffee", "coffee")

label mas_reaction_gift_coffee:

    m 1euc "Hmm?"
    m 1euc "Oh,{w} is this coffee?"

    if persistent._mas_coffee_been_given:
        $ mas_gainAffection(bypass=True)
        m 1wuo "It's a flavor I've haven't had before, too."
        m 1hua "I can't wait to try it!"
        m "Thank you so much, [player]!"

    else:
        show emptydesk at i11 zorder 9
        $ mas_gainAffection(modifier=2, bypass=True)

        m 1hua "Now I can finally make some!"
        m "Thank you so much, [player]!"
        m "Why don't I go ahead and make a cup right now?"
        m 1eua "I'd like to share the first with you, after all."

        # monika is off screen
        hide monika with dissolve
        pause 2.0
        m "I know there's a coffee machine somewhere around here...{w=2}{nw}"
        m "Ah, there it is!{w=2}{nw}"
        pause 5.0
        m "And there we go!{w=2}{nw}"
        show monika 1eua at i11 zorder MAS_MONIKA_Z with dissolve
        hide emptydesk

        # monika back on screen
        m 1eua "I'll let that brew for a few minutes."
        $ mas_brewCoffee()
        $ persistent._mas_acs_enable_coffee = True
        $ persistent._mas_coffee_been_given = True

    $ gift_ev = mas_getEV("mas_reaction_gift_coffee")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init 5 python:
    addReaction("mas_reaction_quetzal_plush", "quetzalplushie")

label mas_reaction_quetzal_plush:
    if not persistent._mas_acs_enable_quetzalplushie:
        $ mas_gainAffection(modifier=2, bypass=True)
        m 1wud "Oh!"
        $ monika_chr.wear_acs_pst(mas_acs_quetzalplushie)
        $ persistent._mas_acs_enable_quetzalplushie = True
        m 1sub "It’s a quetzal!"
        m "Oh my gosh, thanks a lot, [player]!"
        m 1eua "I did mention that I’d like to have a quetzal as a pet..."
        m 1rud "But I would never force the poor thing to stay."
        m 1hua "And now you gave me the next closest thing!"
        m 1hub "This makes me so happy!"
        if mas_isMoniAff(higher=True):
            m 5esbfa "You always seem to know how to make me smile."

        m 1hsb "Thank you again, [player]~"
    else:
        $ 1rksdlb "You already gave me a quetzal plushie, [player]"
    $ gift_ev = mas_getEV("mas_reaction_quetzal_plush")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

# ending label for gift reactions, this just resets a thing
label mas_reaction_end:
    $ persistent._mas_filereacts_just_reacted = False
    return
