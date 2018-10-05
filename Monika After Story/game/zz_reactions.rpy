# FileReactions framework.
# not too different from events

default persistent._mas_filereacts_failed_map = dict()
# mapping of failed deleted file reacts

default persistent._mas_filereacts_just_reacted = False
# True if we just reacted to something

default persistent._mas_filereacts_reacted_map = dict()
# mapping of file reacts that we have already reacted to today

default persistent._mas_filereacts_stop_map = dict()
# mapping of file reacts that we should no longer react to ever again

default persistent._mas_filereacts_historic = dict()
# historic database used to track when and how many gifts Monika has received

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

    # good gifts list
    # TODO: note this would probably be better handled by a property
    # on the event
    good_gifts = ["mas_reaction_gift_coffee","mas_reaction_quetzal_plush",
        "mas_reaction_promisering", "mas_reaction_plush",
        "mas_reaction_bday_cake","mas_reaction_cupcake"]
    # bad gifts list
    # TODO: note this would probably be better handled by a property
    # on the event
    bad_gifts = ["mas_reaction_knife"]


    # connector quips
    connectors = None
    gift_connectors = None

    # starter quips
    starters = None
    gift_starters = None

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


    def _initStarterQuips():
        """
        Initializes the starter quips
        """
        global starters, gift_starters

        # the starter is a MASQuipList
        starters = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_starters = store.MASQuipList(allow_glitch=False, allow_line=False)


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
            if (
                    c_gift_name not in
                        store.persistent._mas_filereacts_failed_map
                    and c_gift_name not in
                        store.persistent._mas_filereacts_reacted_map
                    and c_gift_name not in
                        store.persistent._mas_filereacts_stop_map
                ):
                gifts_found.append(c_gift_name)
                found_map[c_gift_name] = _gift
                store.persistent._mas_filereacts_reacted_map[c_gift_name] = _gift

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

            if _gift is not None and reaction is not None:
                # remove from the list and add to found
                # TODO add to the persistent react map today
                gifts_found.pop()
                found_reacts.append(reaction.eventlabel)
                found_reacts.append(gift_connectors.quip()[1])

        # add in the generic gift reactions
        generic_reacts = list()
        if len(gifts_found) > 0:
            for _gift in gifts_found:
                generic_reacts.append("mas_reaction_gift_generic")
                generic_reacts.append(gift_connectors.quip()[1])
                # keep stats for today
                _register_received_gift("mas_reaction_gift_generic")


        generic_reacts.extend(found_reacts)

        # gotta remove the extra
        if len(generic_reacts) > 0:
            generic_reacts.pop()

            # add the ender
            generic_reacts.insert(0, "mas_reaction_end")

            # add the starter
            generic_reacts.append("mas_reaction_gift_starter_bday")
#            generic_reacts.append(gift_starters.quip()[1])

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


    def _register_received_gift(eventlabel):
        """
        Registers when player gave a gift successfully
        IN:
            eventlabel - the event label for the gift reaction

        """
        # check for stats dict for today
        today = datetime.date.today()
        if not today in store.persistent._mas_filereacts_historic:
            store.persistent._mas_filereacts_historic[today] = dict()

        # Add stats
        store.persistent._mas_filereacts_historic[today][eventlabel] = store.persistent._mas_filereacts_historic[today].get(eventlabel,0) + 1


    def _get_full_stats_for_date(date=None):
        """
        Getter for the full stats dict for gifts on a given date
        IN:
            date - the date to get the report for, if None is given will check
                today's date
                (Defaults to None)

        RETURNS:
            The dict containing the full stats or None if it's empty

        """
        if date is None:
            date = datetime.date.today()
        return store.persistent._mas_filereacts_historic.get(date,None)


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

    def get_report_for_date(date=None):
        """
        Generates a report for all the gifts given on the input date.
        The report is in tuple form (total, good_gifts, neutral_gifts, bad_gifts)
        it contains the totals of each type of gift.
        """
        if date is None:
            date = datetime.date.today()

        stats = _get_full_stats_for_date(date)
        if stats is None:
            return (0,0,0,0)
        good = 0
        bad = 0
        neutral = 0
        for _key in stats.keys():
            if _key in good_gifts:
                good = good + stats[_key]
            if _key in bad_gifts:
                bad = bad + stats[_key]
            if _key == "":
                neutral = stats[_key]
        total = good + neutral + bad
        return (total, good, neutral, bad)



    # init
    _initConnectorQuips()
    _initStarterQuips()

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


    def mas_receivedGift(ev_label):
        """
        Globalied version for gift stats tracking
        """
        mas_filereacts._register_received_gift(ev_label)


    def mas_generateGiftsReport(date=None):
        """
        Globalied version for gift stats tracking
        """
        return mas_filereacts.get_report_for_date(date)



### CONNECTORS [RCT000]

# none here!

## Gift CONNECTORS [RCT010]
#
#init 5 python:
#    store.mas_filereacts.gift_connectors.addLabelQuip(
#        "mas_reaction_gift_connector_test"
#    )

label mas_reaction_gift_connector_test:
    m "this is a test of the connector system"
    return

init 5 python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector1"
    )

label mas_reaction_gift_connector1:
    m 1sublo "Oh! There was something else you wanted to give me?"
    m 1hua "Well! I better open it quickly, shouldn't I?"
    m 1suo "And here we have..."
    return

init 5 python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector2"
    )

label mas_reaction_gift_connector2:
    m 1hua "Ah, jeez, [player]..."
    m "You really enjoy spoiling me, don't you?"
    m 1sublo "Well! I'm not going to complain about a little special treatment today."
    m 1suo "And here we have..."
    return


### STARTERS [RCT050]

init 5 python:
    store.mas_filereacts.gift_starters.addLabelQuip(
        "mas_reaction_gift_starter_generic"
    )

label mas_reaction_gift_starter_generic:
    m "generic test"

# init 5 python:
# TODO: if we need this to be multipled then we do it

label mas_reaction_gift_starter_bday:
    m 1sublo "T-{w=1}This is..."
    m "A gift? For me?"
    m 1hka "I..."
    m 1hua "I've often thought about getting presents from you on my birthday..."
    m "But actually getting one is like a dream come true..."
    m 1sua "Now, what's inside?"
    m 1suo "Oh, it's..."
    return


### REACTIONS [RCT100]

init 5 python:
    addReaction("mas_reaction_generic", None)

label mas_reaction_generic:
    "This is a test"
    return

#init 5 python:
#    addReaction("mas_reaction_gift_generic", None)

label mas_reaction_gift_generic:
    if random.randint(1,2) == 1:
        m 1esd "[player], are you trying to give me something?"
        m 1rssdlb "I found it, but I can’t bring it here..."
        m "I can’t seem to read it well enough."
        m 3esa "But that’s alright!"
        m 1esa "It’s the thought that counts after all, right?"
        m "Thanks for being so thoughtful, [player]~"
    else:
        m 2dkd "{i}*sigh*{/i}"
        m 4ekc "I’m sorry, [player]."
        m 1ekd "I know you’re trying to give me something."
        m 2rksdld "But for some reason I can’t read the file."
        m 3euc "Don’t get me wrong, however."
        m 3eka "I still appreciate that you tried giving something to me."
        m 1hub "And for that, I’m thankful~"
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
    $ mas_receivedGift("mas_reaction_gift_coffee")

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
        $ mas_receivedGift("mas_reaction_quetzal_plush")
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
        m 1rksdlb "You already gave me a quetzal plushie, [player]."
    $ gift_ev = mas_getEV("mas_reaction_quetzal_plush")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init 5 python:
    addReaction("mas_reaction_promisering", "promisering")

label mas_reaction_promisering:
    if not persistent._mas_acs_enable_promisering:
        $ mas_receivedGift("mas_reaction_promisering")
        if mas_isMoniEnamored(higher=True):
            $ mas_gainAffection(modifier=5, bypass=True)
            $ monika_chr.wear_acs_pst(mas_acs_promisering)
            $ persistent._mas_acs_enable_promisering = True
            m 1wud "Is that... a..."
            m "..."
            m 1wka "I..."
            m 1wkbltpa "I'm sorry, [player], I just..."
            m 1dkbltpa "You might not have even meant much by it, but..."
            m "Just in case this is a promise from you..."
            m 3lkbltpa "Know that I’ll cherish it."
            m 3dkbltpa "Always."
            m 1skbltpa "This makes me so happy!"
            m 1dkbltpa "Aha, sorry for crying, [player]..."
            m 1skbla "I’m just really, really happy right now."
            m 1dkbla "Thank you."
            m "I love you, [player]."
            m "More than anything else in this fleeting world."
        elif mas_isMoniNormal(higher=True):
            $ persistent._mas_acs_enable_promisering = True
            $ mas_gainAffection(modifier=3, bypass=True)
            $ monika_chr.wear_acs_pst(mas_acs_promisering)
            m 1wud "Oh... What is this, [player]?"
            m "Is that... a ring?"
            m 1sub " I can’t believe it, [player]!"
            m 1hua "This...{w} means a lot to me."
            m 3hub "This makes me so happy!"
            m 3eub "Seriously, thank you so much for this, [player]!"
        else:
            $ mas_gainAffection(bypass=True)
            m 1wud "Is that a ring?"
            m "That's very ..."
            m "Unexpected."
            if mas_isMoniDis(lower=True):
                m 2rkc "I appreciate the thought ...{w} but I can't accept it."
                m 2ekc "Sorry, [player]."
                $ persistent._mas_acs_enable_promisering = False
            else:
                $ monika_chr.wear_acs_pst(mas_acs_promisering)
                $ persistent._mas_acs_enable_promisering = True
                m 3hua "I'm happily surprised by this, [player]."
                m "Thanks."
    else:
        m 1rksdlb "[player]..."
        m 1rusdlb "You already gave me a ring!"
    $ gift_ev = mas_getEV("mas_reaction_promisering")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init 5 python:
    addReaction("mas_reaction_plush", "plushie")

label mas_reaction_plush:
    m 1wud "What’s this, [player]?"
    m "Are you trying to give me a plushie?"
    m 1rksdlb "I appreciate the thought, but ..."
    m 1ekd "For some reason, I can’t seem to bring it here."
    m 1rkc "I wish I could ..."
    m 1hua "But don’t worry, [player]!"
    m 1hub "Ehehe~"
    m 1hua "Thank you for trying!"
    $ mas_receivedGift("mas_reaction_plush") # while unsuccessful counts
    $ gift_ev = mas_getEV("mas_reaction_plush")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init 5 python:
    addReaction("mas_reaction_bday_cake", "birthdaycake")

label mas_reaction_bday_cake:
    if not mas_isMonikaBirthday():
        m 1rksdlb "Today is not my birthday, did you forget when it is, [player]?"
    else:
        $ mas_gainAffection(modifier=2, bypass=True)
        m 1wud "Oh, [player]..."
        m "A... birthday cake?"
        m 3sub "Gosh, this is so sweet of you!"
        m 1hub "I really love this a lot!"
        m 1dkbfa "I’ll save it for now"
        m 3hua "I can’t wait to try it later!"
        m 1dsc "But..."
        m 3ekbfa "I wish we could eat it together..."
        m 1dkbfa "A birthday cake is for sharing, after all~"
        m 1ekbfa "Thank you for this, [player]."
        $ mas_receivedGift("mas_reaction_bday_cake")
        if mas_isMoniAff(higher=True):
            m 3hubfb "I love you! Ehehe~"
    $ gift_ev = mas_getEV("mas_reaction_bday_cake")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init 5 python:
    addReaction("mas_reaction_cupcake", "cupcake")

label mas_reaction_cupcake:
    m 1wud "Is that a...cupcake?"
    m 3hub "Wow, thanks [player]!"
    m 3euc "Come to think of it, I’ve been meaning to make some cupcakes myself."
    m 1eua "I wanted to learn how to bake good pastries like Natsuki did."
    m 1rksdlb "Buuut I’ve yet to make a kitchen to use!"
    m 3eub "Maybe in the future once I get better at programming, I’ll be able to make one here."
    m 5hubfa "Would be nice to have another hobby other than writing, ehehe~"
    $ mas_receivedGift("mas_reaction_cupcake")
    $ gift_ev = mas_getEV("mas_reaction_cupcake")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init 5 python:
    addReaction("mas_reaction_knife", "knife")

label mas_reaction_knife:
    m 1euc "...?"
    m 1wud "Is that...a knife?"
    m 2wfc "Why would you want to give me that?"
    m 2wfd "I don’t need this here!."
    m 3tfc "...Someone else, maybe."
    m 1dfc "..."
    m 1rsc "I’m not taking this, [player]."
    m 1rfc "If you were trying to be funny, then you have {i}very{/i} poor taste."
    $ mas_receivedGift("mas_reaction_knife") # while technically she didn't accept this one counts
    $ gift_ev = mas_getEV("mas_reaction_knife")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

# ending label for gift reactions, this just resets a thing
label mas_reaction_end:
    $ persistent._mas_filereacts_just_reacted = False
    return
