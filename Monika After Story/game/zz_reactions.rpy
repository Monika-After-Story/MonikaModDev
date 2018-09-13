# FileReactions framework.
# not too different from events

init -1 python in mas_filereacts:
    import store
    import datetime
    
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

    def addReaction(ev_label, fname_list, _action):
        """
        Adds a reaction to the file reactions database.

        IN:
            ev_label - label of this event
            fname_list - list of filenames to react to (lowercase please)
            _action - the EV_ACT to do
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
        global connectors

        # the connector is a MASQipList
        connectors = store.MASQuipList(allow_glitch=False, allow_line=False)

        # add label connectors here
        _conn_labels = [] 
        for _connector in _conn_labels:
            connectors.addLabelQuip(_connector)


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
        # TODO

    _initConnectorQuips()

