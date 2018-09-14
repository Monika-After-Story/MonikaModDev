# FileReactions framework.
# not too different from events

default persistent._mas_filereacts_failed_map = dict()

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

    def addReaction(ev_label, fname_list, _action=store.EV_ACT_QUEUE):
        """
        Adds a reaction to the file reactions database.

        IN:
            ev_label - label of this event
            fname_list - list of filenames to react to (lowercase please)
            _action - the EV_ACT to do
                (Default: EV_ACT_QUEUE)
        """
        # lowercase the list in case
        fname_list = sorted([x.lower() for x in fname_list])

        # build new Event object
        ev = store.Event(
            store.persistent.event_database,
            ev_label,
            category=fname_list,
            action=_action
        )

        # add it to the db and map
        filereact_db[ev_label] = ev
        filereact_map[fname_list] = ev


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
            gifts_found.append(c_gift_name)
            found_map[c_gift_name] = _gift

        # then sort the list
        gifts_found.sort()
            
        # now we are ready to check for reactions
        # first we check for all file reacts:
        all_reaction = filereact_map.get(gifts_found, None)

        if all_reaction is not None:
            return [all_reaction.eventlabel]

        # otherwise, we need to do this more carefully
        found_reacts = list()
        for index in range(len(gifts_round)-1, -1, -1):
            _gift = gifts_round[index]
            reaction = filereact_map.get(_gift, None)

            if _gift is not None:
                # remove from the list and add to found
                gifts_found.pop()
                found_reacts.append(reaction.eventlabel)
                found_reacts.append(gift_connectors.quip()[1])

        # add in the generic gift reactions
        if len(gifts_round) > 0:
            for _gift in gifts_found:
                found_reacts.append("mas_reaction_gift_generic")
                found_reacts.append(gift_connectors.quip()[1])

        # gotta remove the extra
        found_reacts.pop()

        # now return the list
        return found_reacts


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

        file_to_delete = _map.get(_filename, None):
        if file_to_delete is None:
            return

        if store.mas_docking_station.destroyPackage(file_to_delete):
            # file has been deleted (or is gone). pop and go
            _map.pop(file_to_delete)
            return

        # otherwise add to the failed map
        store.persistent._mas_filereacts_failed_map[_filename] = file_to_delete


    def delete_file(_filename):
        """
        Deletes a file off the found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete
                one randomly
        """
        _core_delete(_filename, foundreact_map)


    def th_delete_file(_filename):
        """
        Deletes a file off the threaded found_react map
        """
        _core_delete(_filename, th_foundreact_map)


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


### CONNECTORS [RCT000]

# none here!

## Gift CONNECTORS [RCT10]

init 5 python:
    store.mas_reactions.gift_connectors.addLabelQuip(
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
    return
