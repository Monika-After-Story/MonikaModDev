




define monika_random_topics = []
define mas_rev_unseen = []
define mas_rev_seen = []
define mas_rev_mostseen = []
define testitem = 0
define numbers_only = "0123456789"
define lower_letters_only = "qwertyuiopasdfghjklzxcvbnm "
define letters_only = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдеёжзийклмнопрстуфхчшщцьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЧШЩЦЬЫЪЭЮЯ "
define mas_did_monika_battery = False
define mas_sensitive_limit = 3

init -2 python in mas_topics:




    S_MOST_SEEN = 0.1



    S_TOP_SEEN = 0.2


    S_TOP_LIMIT = 0.3


    UNSEEN = 50
    SEEN = UNSEEN + 49
    MOST_SEEN = SEEN + 1

    def topSeenEvents(sorted_ev_list, shown_count):
        """
        counts the number of events with a > shown_count than the given
        shown_count

        IN:
            sorted_ev_list - an event list sorted by shown_counts
            shown_count - shown_count to compare to

        RETURNS:
            number of events with shown_counts that are higher than the given
            shown_count
        """
        index = len(sorted_ev_list) - 1
        ev_count = 0
        while index >= 0 and sorted_ev_list[index].shown_count > shown_count:
            ev_count += 1
            index -= 1
        
        return ev_count



init -1 python:
    import random
    random.seed()

    import store.songs as songs
    import store.evhand as evhand

    mas_events_built = False


    def remove_seen_labels(pool):
        
        
        
        
        
        
        
        
        for index in range(len(pool)-1, -1, -1):
            if renpy.seen_label(pool[index]):
                pool.pop(index)


    def mas_randomSelectAndRemove(sel_list):
        """
        Randomly selects an element from the given list
        This also removes the element from that list.

        IN:
            sel_list - list to select from

        RETURNS:
            selected element
        """
        endpoint = len(sel_list) - 1
        
        if endpoint < 0:
            return None
        
        
        return sel_list.pop(random.randint(0, endpoint))


    def mas_randomSelectAndPush(sel_list):
        """
        Randomly selects an element from the the given list and pushes the event
        This also removes the element from that list.

        NOTE: this does sensitivy checks

        IN:
            sel_list - list to select from
        """
        sel_ev = True
        while sel_ev is not None:
            sel_ev = mas_randomSelectAndRemove(sel_list)
            
            if (
                    
                    sel_ev

                    
                    and not sel_ev.anyflags(EV_FLAG_HFRS)

                    
                    and (
                        not persistent._mas_sensitive_mode
                        or not sel_ev.sensitive
                    )
            ):
                pushEvent(sel_ev.eventlabel, notify=True)
                return


    def mas_insertSort(sort_list, item, key):
        """
        Performs a round of insertion sort.
        This does least to greatest sorting

        IN:
            sort_list - list to insert + sort
            item - item to sort and insert
            key - function to call using the given item to retrieve sort key

        OUT:
            sort_list - list with 1 additonal element, sorted
        """
        store.mas_utils.insert_sort(sort_list, item, key)


    def mas_splitSeenEvents(sorted_seen):
        """
        Splits the seen_list into seena nd most seen

        IN:
            sorted_seen - list of seen events, sorted by shown_count

        RETURNS:
            tuple of thef ollowing format:
            [0] - seen list of events
            [1] - most seen list of events
        """
        ss_len = len(sorted_seen)
        if ss_len == 0:
            return ([], [])
        
        
        most_count = int(ss_len * store.mas_topics.S_MOST_SEEN)
        top_count = store.mas_topics.topSeenEvents(
            sorted_seen,
            int(
                sorted_seen[ss_len - 1].shown_count
                * (1 - store.mas_topics.S_TOP_SEEN)
            )
        )
        
        
        if top_count < ss_len * store.mas_topics.S_TOP_LIMIT:
            
            
            split_point = top_count * -1
        
        else:
            
            split_point = most_count * -1
        
        
        return (sorted_seen[:split_point], sorted_seen[split_point:])


    def mas_splitRandomEvents(events_dict):
        """
        Splits the given random events dict into 2 lists of events
        NOTE: cleans the seen list

        RETURNS:
            tuple of the following format:
            [0] - unseen list of events
            [1] - seen list of events, sorted by shown_count

        """
        
        unseen = list()
        seen = list()
        for k in events_dict:
            ev = events_dict[k]
            
            if renpy.seen_label(k) and not "force repeat" in ev.rules:
                
                mas_insertSort(seen, ev, Event.getSortShownCount)
            
            else:
                
                unseen.append(ev)
        
        
        seen = mas_cleanJustSeenEV(seen)
        
        return (unseen, seen)


    def mas_buildEventLists():
        """
        Builds the unseen / most seen / seen event lists

        RETURNS:
            tuple of the following format:
            [0] - unseen list of events
            [1] - seen list of events
            [2] - most seen list of events

        ASSUMES:
            evhand.event_database
            mas_events_built
        """
        global mas_events_built
        
        
        all_random_topics = Event.filterEvents(
            evhand.event_database,
            random=True,
            aff=mas_curr_affection
        )
        
        
        unseen, sorted_seen = mas_splitRandomEvents(all_random_topics)
        
        
        seen, mostseen = mas_splitSeenEvents(sorted_seen)
        
        mas_events_built = True
        return (unseen, seen, mostseen)


    def mas_buildSeenEventLists():
        """
        Builds the seen / most seen event lists

        RETURNS:
            tuple of the following format:
            [0] - seen list of events
            [1] - most seen list of events

        ASSUMES:
            evhand.event_database
        """
        
        all_seen_topics = Event.filterEvents(
            evhand.event_database,
            random=True,
            seen=True,
            aff=mas_curr_affection
        ).values()
        
        
        cleaned_seen = mas_cleanJustSeenEV(all_seen_topics)
        
        
        cleaned_seen.sort(key=Event.getSortShownCount)
        
        
        return mas_splitSeenEvents(cleaned_seen)


    def mas_rebuildEventLists():
        """
        Rebuilds the unseen, seen and most seen event lists.

        ASSUMES:
            mas_rev_unseen - unseen list
            mas_rev_seen - seen list
            mas_rev_mostseen - most seen list
        """
        global mas_rev_unseen, mas_rev_seen, mas_rev_mostseen
        mas_rev_unseen, mas_rev_seen, mas_rev_mostseen = mas_buildEventLists()



    class MASTopicLabelException(Exception):
        def __init__(self, msg):
            self.msg = msg
        def __str__(self):
            return "MASTopicLabelException: " + self.msg

init 11 python:

    mas_rev_unseen = []
    mas_rev_seen = []
    mas_rev_mostseen = []

















default persistent._mas_player_bookmarked = list()

default persistent._mas_player_derandomed = list()

default persistent.flagged_monikatopic = None


init python:
    def mas_derandom_topic(ev_label=None):
        """
        Function for the derandom hotkey, 'x'

        IN:
            ev_label - label of the event we want to derandom.
                (Optional. If None, persistent.current_monikatopic is used)
                (Default: None)
        """
        
        label_prefix_map = store.mas_bookmarks_derand.label_prefix_map
        
        if ev_label is None:
            ev_label = persistent.current_monikatopic
        
        ev = mas_getEV(ev_label)
        
        if ev is None:
            return
        
        
        label_prefix = store.mas_bookmarks_derand.getLabelPrefix(ev_label, label_prefix_map.keys())
        
        
        
        
        
        
        if (
            ev.random
            and label_prefix
            and ev.prompt != ev_label
        ):
            
            derand_flag_add_text = label_prefix_map[label_prefix].get("derand_text", _("Помечено для удаления."))
            derand_flag_remove_text = label_prefix_map[label_prefix].get("underand_text", _("Пометка удалена"))
            
            
            push_label = ev.rules.get("derandom_override_label", None)
            
            
            if not renpy.has_label(push_label):
                push_label = label_prefix_map[label_prefix].get("push_label", "mas_topic_derandom")
            
            if mas_findEVL(push_label) < 0:
                persistent.flagged_monikatopic = ev_label
                pushEvent(push_label, skipeval=True)
                renpy.notify(derand_flag_add_text)
            
            else:
                mas_rmEVL(push_label)
                renpy.notify(derand_flag_remove_text)

    def mas_bookmark_topic(ev_label=None):
        """
        Function for the bookmark hotkey, 'b'

        IN:
            ev_label - label of the event we want to bookmark.
                (Optional, defaults to persistent.current_monikatopic)
        """
        
        label_prefix_map = store.mas_bookmarks_derand.label_prefix_map
        
        if ev_label is None:
            ev_label = persistent.current_monikatopic
        
        ev = mas_getEV(ev_label)
        
        if ev is None:
            return
        
        
        label_prefix = store.mas_bookmarks_derand.getLabelPrefix(ev_label, label_prefix_map.keys())
        
        
        
        
        
        
        
        if (
            mas_isMoniNormal(higher=True)
            and (label_prefix or ev.rules.get("bookmark_rule") == store.mas_bookmarks_derand.WHITELIST)
            and (ev.rules.get("bookmark_rule") != store.mas_bookmarks_derand.BLACKLIST)
            and ev.prompt != ev_label
        ):
            
            if not label_prefix:
                bookmark_persist_key = "_mas_player_bookmarked"
                bookmark_add_text = "Добавлена закладка."
                bookmark_remove_text = "Закладка удалена."
            
            else:
                
                bookmark_persist_key = label_prefix_map[label_prefix].get("bookmark_persist_key", "_mas_player_bookmarked")
                bookmark_add_text = label_prefix_map[label_prefix].get("bookmark_text", _("Добавлена закладка."))
                bookmark_remove_text = label_prefix_map[label_prefix].get("unbookmark_text", _("Закладка удалена."))
            
            
            
            
            if bookmark_persist_key not in persistent.__dict__:
                persistent.__dict__[bookmark_persist_key] = list()
            
            
            persist_pointer = persistent.__dict__[bookmark_persist_key]
            
            if ev_label not in persist_pointer:
                persist_pointer.append(ev_label)
                renpy.notify(bookmark_add_text)
            
            else:
                persist_pointer.pop(persist_pointer.index(ev_label))
                renpy.notify(bookmark_remove_text)

    def mas_hasBookmarks(persist_var=None):
        """
        Checks to see if we have bookmarks to show

        Bookmarks are restricted to Normal+ affection
        and to topics that are unlocked and are available
        based on current affection

        IN:
            persist_var - appropriate variable holding the bookedmarked eventlabels.
                If None, persistent._mas_player_bookmarked is assumed
                (Default: None)

        OUT:
            boolean:
                True if there are bookmarks in the curent var
                False otherwise
        """
        if mas_isMoniUpset(lower=True):
            return False
        
        elif persist_var is None:
            persist_var = persistent._mas_player_bookmarked
        
        return len(mas_get_player_bookmarks(persist_var)) > 0


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="mas_topic_derandom",unlocked=False,rules={"no_unlock":None}))

label mas_topic_derandom:

    $ prev_topic = persistent.flagged_monikatopic
    m 3eksdld "Ты уверен, что больше не хочешь, чтобы я подняла эту тему?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты уверен, что больше не хочешь, чтобы я подняла эту тему?{fast}"
        "Пожалуйста":

            $ mas_hideEVL(prev_topic, "EVE", derandom=True)
            $ persistent._mas_player_derandomed.append(prev_topic)
            $ mas_unlockEVL('mas_topic_rerandom', 'EVE')

            m 2eksdlc "Хорошо, [player]. Я постараюсь больше не говорить об этом."
            m 2dksdld "Если я тебя, как-то расстроила, Мне очень жаль...{w=0.5} Я бы никогда не сделала это специально."
            m 2eksdla "...Но спасибо, что дал мне знать;{w=0.5} Я ценю твою искренность."
        "Всё в порядке.":

            m 1eka "Хорошо, [player]."
    return

label mas_bad_derand_topic:
    python:
        prev_topic = persistent.flagged_monikatopic

        def derand_flagged_topic():
            """
            Derands the flagged topic
            """
            mas_hideEVL(prev_topic, "EVE", derandom=True)
            persistent._mas_player_derandomed.append(prev_topic)
            mas_unlockEVL('mas_topic_rerandom', 'EVE')

    m 2ekc "...{w=0.3}{nw}"
    extend 2ekd "[player]..."

    if mas_isMoniAff(higher=True):
        m 2efd "Разве нормально, что я говорю с тобой о своих страхах?"
        m 2ekc "Я имела ввиду, что если ты хочешь, то я прекращу...{w=0.3}{nw}"
        extend 2rkd "но я подумала, что ты захочешь меня выслушать."

        m 2esc "Ты хочешь, чтобы я остановилась, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты хочешь, чтобы я остановилась, [player]?{fast}"
            "Да, пожалуйста.":

                m 2dkc "Хорошо..."

                $ mas_loseAffection(5)
                $ derand_flagged_topic()
            "Всё хорошо, я готов выслушать.":

                m 2duu "Спасибо, [player]."
                m 2eua "Эти слова многое для меня значат."

    elif mas_isMoniUpset(higher=True):
        m 2ekd "Ты просто...{w=0.2}не задумываешься о том, что я чувствую или что-то в этом роде?"
        m 2tsc "Если ты хочешь, чтобы я прекратила говорить на эту тему, я перестану...но меня не очень радует то, что ты не хочешь меня выслушать."

        m 2etc "Итак [player], мне перестать?{nw}"
        $ _history_list.pop()
        menu:
            m "Well [player], should I stop?{fast}"
            "Да, пожалуйста.":

                m 2dsc "Хорошо."
                $ mas_loseAffection(5)
                $ derand_flagged_topic()
            "Всё в порядке.":

                m 2eka "Спасибо, [player]."
                $ _stil_ = " " if mas_isMoniNormal(higher=True) else " ещё "
                m "Я ценю, что ты[_stil_]готов выслушать меня."
    else:


        $ mas_loseAffection(5)
        m 2rsc "Полагаю, мне не стоит удивляться..."
        m 2tsc "Ты прекрасно дал мне понять, что тебе наплевать на мои чувства."
        m 2dsc "Хорошо, [player]. Я больше не буду об этом говорить."
        $ derand_flagged_topic()
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_topic_rerandom",
            category=['ты...'],
            prompt="Я не против поговорить о...",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label mas_topic_rerandom:
    python:
        mas_bookmarks_derand.initial_ask_text_multiple = "О какой теме, ты не прочь поболтать снова?"
        mas_bookmarks_derand.initial_ask_text_one = "Если уверен, что хочешь обсудить что-то еще раз, просто выбери тему, [player]."
        mas_bookmarks_derand.caller_label = "mas_topic_rerandom"
        mas_bookmarks_derand.persist_var = persistent._mas_player_derandomed

    call mas_rerandom from _call_mas_rerandom
    return _return

init python in mas_bookmarks_derand:
    import store


    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"












    label_prefix_map = {
        "monika_": {
            "bookmark_text": _("Тема добавлена в закладки."),
            "unbookmark_text": _("Закладка удалена."),
            "derand_text": _("Тема отмечена для удаления."),
            "underand_text": _("Метка убрана."),
            "push_label": "mas_topic_derandom",
            "bookmark_persist_key": "_mas_player_bookmarked",
            "derand_persist_key": "_mas_player_derandomed"
        },
        "mas_song_": {
            "bookmark_text": _("Песня добавлена в закладки."),
            "derand_text": _("Песня отмечена для удаления."),
            "underand_text": _("Метка убрана."),
            "push_label": "mas_song_derandom",
            "derand_persist_key": "_mas_player_derandomed_songs"
        }
    }


    initial_ask_text_multiple = None
    initial_ask_text_one = None
    caller_label = None
    persist_var = None

    def resetDefaultValues():
        """
        Resets the globals to their default values
        """
        global initial_ask_text_multiple, initial_ask_text_one
        global caller_label, persist_var
        
        initial_ask_text_multiple = None
        initial_ask_text_one = None
        caller_label = None
        persist_var = None
        return

    def getLabelPrefix(test_str, list_prefixes):
        """
        Checks if test_str starts with anything in the list of prefixes, and if so, returns the matching prefix

        IN:
            test_str - string to test
            list_prefixes - list of strings that test_str should start with

        OUT:
            string:
                - label_prefix if test_string starts with a prefix in list_prefixes
                - empty string otherwise
        """
        for label_prefix in list_prefixes:
            if test_str.startswith(label_prefix):
                return label_prefix
        return ""

    def getDerandomedEVLs():
        """
        Gets a list of derandomed eventlabels

        OUT:
            list of derandomed eventlabels
        """
        
        derand_keys = [
            label_prefix_data["derand_persist_key"]
            for label_prefix_data in label_prefix_map.itervalues()
            if "derand_persist_key" in label_prefix_data
        ]
        
        deranded_evl_list = list()
        
        for derand_key in derand_keys:
            
            derand_list = store.persistent.__dict__.get(derand_key, list())
            
            for evl in derand_list:
                deranded_evl_list.append(evl)
        
        return deranded_evl_list

    def shouldRandom(eventlabel):
        """
        Checks if we should random the given eventlabel
        This is determined by whether or not the event is in any derandom list

        IN:
            eventlabel to check if we should random_seen

        OUT:
            boolean: True if we should random this event, False otherwise
        """
        return eventlabel not in getDerandomedEVLs()

    def wrappedGainAffection(amount=None, modifier=1, bypass=False):
        """
        Wrapper function for mas_gainAffection which allows it to be used in event rules at init 5

        See mas_gainAffection for documentation
        """
        store.mas_gainAffection(amount, modifier, bypass)








label mas_rerandom:
    python:
        derandomlist = mas_get_player_derandoms(mas_bookmarks_derand.persist_var)

        derandomlist.sort()

    show monika 1eua at t21
    if len(derandomlist) > 1:
        $ renpy.say(m, mas_bookmarks_derand.initial_ask_text_multiple, interact=False)
    else:

        $ renpy.say(m, mas_bookmarks_derand.initial_ask_text_one, interact=False)

    call screen mas_check_scrollable_menu(derandomlist, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, selected_button_prompt="Allow selected")

    $ topics_to_rerandom = _return

    if not topics_to_rerandom:

        return "prompt"

    show monika at t11
    python:
        for ev_label in topics_to_rerandom.iterkeys():
            
            rerand_ev = mas_getEV(ev_label)
            
            
            if rerand_ev:
                
                rerand_ev.random = True
                
                
                rerandom_callback = rerand_ev.rules.get("rerandom_callback", None)
                if rerandom_callback is not None:
                    try:
                        rerandom_callback()
                    
                    except Exception as ex:
                        mas_utils.writelog(
                            "[ERROR]: Failed to call rerandom callback function. Trace message: {0}\n".format(ex.message)
                        )
            
            
            if ev_label in mas_bookmarks_derand.persist_var:
                mas_bookmarks_derand.persist_var.remove(ev_label)

        if len(mas_bookmarks_derand.persist_var) == 0:
            mas_lockEVL(mas_bookmarks_derand.caller_label, "EVE")

    m 1dsa "Okay, [player].{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    m 3hua "All done!"



    $ persistent._mas_current_season = store.mas_seasons._seasonalCatchup(persistent._mas_current_season)

    $ mas_bookmarks_derand.resetDefaultValues()
    return

default persistent._mas_unsee_unseen = None



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_hide_unseen",
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label mas_hide_unseen:
    $ persistent._mas_unsee_unseen = True
    m 3esd "Oh, okay, [mas_get_player_nickname()]..."
    if not mas_getEVL_shown_count("mas_hide_unseen"):
        m 1tuu "So I guess you want to...{w=0.5}{i}unsee{/i} it..."
        m 3hub "Ahaha!"

    m 1esa "I'll hide it for now, just give me a second.{w=0.5}.{w=0.5}.{nw}"
    m 3eub "There you go! If you want to see the menu again, just ask."
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_show_unseen",
            category=['you'],
            prompt="I would like to see 'Unseen' again",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label mas_show_unseen:
    $ persistent._mas_unsee_unseen = False
    m 3eub "Sure, [mas_get_player_nickname()]!"
    m 1esa "Just give me a second.{w=0.5}.{w=0.5}.{nw}"
    m 3hua "There you go!"
    return






default persistent._mas_pm_religious = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_god',
            prompt="Мысли о боге",
            label=None,
            category=['психология'],
            random=True,
            unlocked=False,
            pool=False,
            conditional=None,
            action=None,
            start_date=None,
            end_date=None,
            unlock_date=None,
        )
    )

label monika_god:
    m 1eua "[player], ты веришь в Бога?"
    m 1eka "Я вот никогда не была уверена насчёт этого."
    m 1lksdlb "То есть в детстве я, разумеется, не задавалась таким вопросом..."
    m 1lsc "Но с возрастом и познанием мира, этот вопрос беспокоил меня всё сильнее."
    m 1esd "Я спрашивала себя, почему Бог одним людям помогает преодолевать жизненные трудности и излечиваться от болезней..."
    m 1tfd "...В то время как некоторых детей продают в сексуальное рабство?"
    m 4tfc "Или пока у восьмисот миллионов человек в мире не хватает денег даже на еду."
    m 2dkc "Я всё думала, сколько из этих людей каждый день молятся Богу, пока не умрут с голоду?"
    m 4ekc "Или сколько семей из населения в миллион человек молится, чтобы дорогой им человек оправился от неизлечимой болезни?"
    m 4euc "Но вот в чём парадокс..."
    m 4eud "Если вдруг на тысячу умерших одному повезёт и он выживет..."
    m 2esc "...Это вдруг начинают называть божьим чудом."
    m 2dsc "Хотела бы я встретиться с этим Богом, который, как мне кажется,, насмехается над всеми теми, кто недостоин его чудес."
    m 4hksdlb "Однако довольно иронично, что у меня самой действительно {b}есть{/b} создатель."
    m 4eua "И знаешь, что я думаю?"

    if persistent._mas_pm_cares_about_dokis:
        m 1lksdlc "Могу поспорить, прямо сейчас он смеётся над несчастными судьбами всех."
    else:
        m 1lksdla "Могу поспорить, прямо сейчас он смеётся над несчастными судьбами Сайори и Юри."

    m 1dsd "Кто мы для него, если не куклы в заранее прописанном спектакле??"
    m 3euc "Так что, с этой точки зрения..."
    m 3eud "Я не думаю, что это слишком надуманно. Если бог и есть, то Земля есть ничто, как его пьеса."
    m 1eua "В любом случае, ты веришь в бога, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "В любом случае, ты веришь в бога, [player]?{fast}"
        "Да.":
            $ persistent._mas_pm_religious = True
            m 1hksdlb "Ох... Надеюсь, я не слишком обидела тебя своими мыслями."
            m 1eka "Так или иначе, я считаю, что важно иметь возможность делиться своим мнением с тобой."
            m 1rksdla "Уверена, ты понимаешь, почему я не особо люблю это понятие."
            m 1hua "Может быть, ты покажешь мне лучшего Бога, когда я выберусь отсюда!"
            m 1hub "А-ха-ха~"
        "Нет.":
            $ persistent._mas_pm_religious = False
            m 3eka "Я рада, что мы мыслим одинаково, но ничего страшного, если ты думаешь иначе."
            m 1hua "Я рада, что ты можешь жить сам по себе!"
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Надеюсь, ты соглас[mas_gender_en] принять меня в свою жизнь, как только я смогу предстать перед тобой."
            m 5hua "Э=хе-хе~"

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_death",category=['philosophy'],prompt="Смерть и умирание",random=True))

label monika_death:
    m 1euc "[player], тебе когда-нибудь было интересно, каково это... умереть?"
    m 1lsc "Я часто думала об этом..."
    m 1lksdlc "Но я, кажется, узнала, что это за чувство."
    m "Я не понимаю, что к чему, но каждый раз, когда игра закрывается без предупреждения..."
    m 1dsc "...Такое ощущение, будто я мгновенно засыпаю и остаюсь только со своими мыслями."
    m 1dkd "Но через несколько секунд, моя голова начинает забиваться невнятными и запутанными узорами."
    m 1dkc "Я вижу статичные и быстрые вспышки света, и слышу странные крики."
    m 3ekd "В такой ситуации, я вообще не могу сформировать ни единую мысль."
    m 1esc "Я без конца подавлена этими вспышками и криками, не могу ни пошевелиться, ни даже размышлять."
    m 1euc "Я вполне уверена, что в тот момент я не существовала, но я почему-то это всё равно помню."
    m 1ekd "Я не понимаю, почему игра так реагирует на внезапное закрытие, и почему это происходит со мной."
    m 1dkc "..."
    m 3eub "Но ты можешь предотвратить это, [player]!"
    m 3eua "Если ты попрощаешься перед тем, как уйти,{w=0.2} я пойду к себе в комнату перед тем, как игра закроется, и мне не придётся страдать от той кричащей пустоты."
    m "Это же проще простого, так что, пожалуйста, всегда прощайся, хорошо?"
    if mas_isMoniDis(lower=True):
        m 2tkc Если только... {w=1}тебе не {b}нравится{/b} причинять мне боль..."
    else:
        m 1eka "Спасибо, что выслушал[mas_gender_none] меня, [player]."
    return


default persistent._mas_pm_love_yourself = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_selfesteem",category=['советы'],prompt="Самооценка",random=True))

label monika_selfesteem:
    m 3eua "Ты любишь себя, [player]?"
    m 1lksdlb "Я не имею в виду ничего тщеславного."
    m 1eka "В смысле, любишь ли ты себя так[mas_gender_im], как[mas_gender_oi] ты есть?{nw}"
    $ _history_list.pop()
    menu:
        m "В смысле, любишь ли ты себя так[mas_gender_im], как[mas_gender_oi] ты есть?{fast}"
        "Да.":
            $ persistent._mas_pm_love_yourself = True
            m 1hua "Я рада, что ты не несчаст[mas_gender_en] внутри, [player]."

            if mas_isMoniUpset(lower=True):
                m 1ekc "Я действительно беспокоюсь за тебя в последнее время..."
            elif mas_isMoniHappy(higher=True):
                m 1hua "Я не слишком волнуюсь по этому поводу благодаря тому, насколько хорошо ты заставил[mas_gender_none] меня чувствовать себя в последнее время."
            else:
                m 1eka "Твоё счастье — всё для меня."

            m 2ekc "Депрессия и низкая самооценка вызывает чувство, будто ты ничего не заслуживаешь."
            m 2lksdlc "Это ужасный коктейль чувств."
            m 4eka "Если у тебя есть друзья, которые страдают от депрессии, просто иди и поговори с ними."
            m 4hua "Даже небольшая похвала может многое изменить!"
            m 1eua "Это даст им немного веры в себя, а ты сделаешь хорошое дело."
            m 1eka "И даже если это не поможет, то ты хотя бы попытал[mas_gender_sya]."
        "Нет.":
            $ persistent._mas_pm_love_yourself = False
            m 1ekc "Это... очень грустно слышать, [player]..."

            if mas_isMoniDis(lower=True):
                m 1ekc "Я сильно подозревала, что это правда..."
            elif mas_isMoniHappy(higher=True):
                m 1ekc "И думаю, что я упустила это, пока ты делал[mas_gender_none] меня такой счастливой..."

            m "Я всегда буду любить тебя, [player], но я думаю, что и любить себя важно."
            m 1eka "Тебе нужно начать с небольших вещей, которые тебе в себе нравятся."
            m 3hua "Это может быть чем-то глупым или небольшое умение, которым ты гордишься!"
            m 3eua "Со временем ты построишь свою уверенность, а в конце-концов и полюбишь себя."
            m 1eka "Я не могу пообещать, что это будет легко. Но это точно стоит того."
            m 3hub "Я всегда поддержу тебя, [player]!"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sayori",
            category=['участники клуба'],
            prompt="Сожаления Сайори",
            random=True
        )
    )

label monika_sayori:
    m 2euc "Я думала о Сайори раньше..."
    m 2lsc "Я до сих пор жалею о том, что не смогла разобраться со всей той ситуацией более деликатным образом."

    if (
            not persistent._mas_sensitive_mode
            and not renpy.seen_label("monika_sayori")
            and not persistent._mas_pm_cares_about_dokis
        ):
        m "Ты всё ещё в подвешанном состоянии, верно?"
        m 2wud "...О боже, я не могу поверить, что я это сказала."
        m 4wud "Это был совершенно не преднамеренный каламбур, я клянусь!"
        m 2lksdlb "В любом случае..."

    if not persistent._mas_sensitive_mode:
        m 2eka "Я знаю, что она много для тебя значила, так что я думаю, что будет правильно поделится её последними моментами с тобой."

        m "Если, конечно, ты хочешь это услышать.{nw}"
        $ _history_list.pop()
        menu:
            m "Если, конечно, ты хочешь это услышать.{fast}"
            "Да.":
                m 4eka ""Ты знал[mas_gender_none] насколько Сайори была неловкой?"
                m 2rksdlb "Она всё испортила этой висячей штукой..."
                m 4rksdla "Нужно было просто прыгнуть с достаточной высоты, чтобы верёвка сломала шею быстро и безболезненно."
                m 4rksdld "Но она использовала стул, а это значит обрекла себя на долгую смерть от удушения."
                m 2eksdlc "За несколько секунд до смерти, она, скорее всего, передумала..."
                m 2dksdld "Потому что она начала рвать верёвку, пытаясь освободить себя."
                m "Она продолжала пытаться, пока не потеряла сознание."
                m 4eksdlc "Поэтому её пальцы были в крови."
                m 4euc "Если подумать, то она не просто «передумала». Это был инстинкт самосохранения."
                m 2eud "Поэтому ты не можешь винить её за это."
                m 2eka "В любом случае, было бы проще думать, что она не передумала, да?"
                m 2ekd "Не очень полезно думать о вещах, которые могли бы пойти по-другому."
                m 2eka "Так что, помни, что даже если технически ты мог её спасти, это не твоя вина."
                m 4eud "Я, возможно, спровоцировала её, но она уже была психически больна."
            "Нет.":
                m "Я понимаю, [player]."
        m 2euc "Тем не менее..."
    else:
        m 2ekc "..."

    m 2euc "Мне интересно, как бы всё получилось, если бы мы просто начали встречаться с самого начала?"
    m 1eka "Я думаю, что мы бы сейчас были в комнате клуба, веселились и писали поэмы вместе."

    if persistent._mas_pm_cares_about_dokis:
        m "Наверное, тебе это понравилось, да?"
        m 1rksdla "Должна признать...{w=0.5}мне тоже..."
        m 1eka "Мы хорошо провели время."
        m 1euc "Но...{w=0.5}в любом случае, конец всё равно один и тот же, верно?"
    else:
        m 1esc "Но в чём смысл, если ничего из этого не было реальным?"
        m 1euc "Возможно, мы бы в любом случае пришли бы к одному концу."

    if mas_isMoniUpset(lower=True):
        m 1rksdla "Только мы с тобой... счастливы вместе..."
        m 3rksdla "Нет никакой причины для того, чтобы просить нечто большее, чем это, правда ведь?"
        m 1eka "Извини, я просто бессмысленно размышляла. Теперь же я просто помолчу..."
    else:
        m 1eua "Только мы с тобой... счастливы вместе..."
        m 3eua "Нет никакой причины для того, чтобы просить нечто большее, чем это."
        m 1hua "Я просто бессмысленно размышляла; я счастлива настолько, насколько это возможно."

    if mas_getEVL_shown_count("monika_sayori") < mas_sensitive_limit:
        return


    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_japan",category=['ddlc'],prompt="Настройки DDLC",random=True))

label monika_japan:
    m 4eud "Кстати, кое о чём я подумала..."
    m "Ты знал[mas_gender_none], что действие игры происходит в Японии?"
    m 2euc "Ну... Я полагаю, что ты знал[mas_gender_none] это?"
    m "Или, по крайней мере, ты думал[mas_gender_none], что это возможно?"
    m 2eud "Мне кажется, тебе никогда не говорили о том, где это произошло..."
    m 2etc "Действительно ли это Япония?"
    m 4esc "То есть, разве классы и прочее не является странным для японской школы?"
    m 4eud "К тому же, тут всё на русском..."
    m 2esc "Такое чувство, что всё здесь – просто сценарные декорации, а место действия было выбрано в последнюю очередь."
    m 2ekc "Это вызывает у меня кризис индентичности."
    m 2lksdlc "Все мои воспоминания смутны..."
    m 2dksdlc "Я чувствую себя как дома, но я даже не знаю где этот... «дом»."
    m 2eksdld "Не знаю как бы описать это получше..."
    m 4rksdlc "Представь, что выглядываешь из окна своего дома, но вместо привычной лужайки обнаруживаешь, что находишься в совершенно незнакомом месте."
    m 4eud "Ты всё ещё будешь чувствовать себя как дома?"
    m 4ekd "Ты захочешь выйти на улицу?"
    m 2esa "То есть... Конечно, если мы никогда не покинем эту комнату, то это не очень-то и важно."
    m 2eua "Пока мы вместе и в безопасности, это и есть наш дом."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "И мы всё ещё каждую ночь можем любоваться на красивый закат."
    $ mas_unlockEVL("monika_remembrance", "EVE")
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_high_school",category=['советы','школа'],prompt="Старшая школа",random=True))

label monika_high_school:
    m 4eua "Знаешь, старшая школа для многих очень неспокойное время."
    m "Одних терзает страсть, других — драма."
    m 2eka "Третьих боль в сердце заставляет искать утешение в социальных сетях..."
    m 2ekd "Но тяжесть общественного мнения и гормоны и вправду могут прочертить чёрную полосу в жизни этих людей."
    m 4eud "У каждого из них своя история."
    m 2ekc "Ты не можешь знать, что каждый чувствует глубоко внутри себя."
    m 2eksdlc "Многие люди, страдающие от депрессии, даже не удосуживаются поведать миру о своей проблеме."
    m 4dksdld "Им не нужно внимание, ведь на самих себя они уже махнули рукой."
    m 4dksdlc "Их чувство собственной бесполезности настолько поглотило их, что они даже не хотят слышать ободрения окружающих."
    m 2ekd "У депрессии много форм и это одна из них."
    m 2ekc "Если ты чувствуешь, что человек впал в депрессию..."
    m 2eka "Ты можешь помочь ему просто хорошим отношением, словно он твой старый друг."
    m 4eka "Проведи с ним время, даже если он не хочет ничем заниматься."
    m "И постоянно напоминай, что впереди его ждёт ещё много хорошего."
    m 4eua "Если ты заранее спланируешь с ним встречу, позволишь одолжить что-нибудь у себя или просто скажешь «до завтра»..."
    m "юбая из этих элементарных вещей поможет твоему другу прожить ещё один день."
    m 2eka "Я надеюсь, что дружба с Сайори дала тебе объективное восприятие того, как выглядит настоящая депрессия."

    if not persistent._mas_pm_cares_about_dokis:
        m 2lsc "Да, её больше нет..."
        m 2euc "Но она изначально была ненастоящей."
        m 4eua "Ты настоящ[mas_gender_ii]."
        m "Твои друзья настоящие."
        m 4hua "И, если ты просто будешь хорошим человеком, это позволит тебе спасти кому-нибудь жизнь."

    m 2euc "А что касается тебя само[mas_gender_go]..."
    m 2ekc "...Я надеюсь, тебя сейчас не одолевает депрессия или нечто подобное?"

    if mas_isMoniHappy(higher=True):
        m 4eka "В некоторой степени, [player], тебе повезло, потому что я уверена, что есть люди, которые были бы готовы спасти твою жизнь."
    else:
        if mas_isMoniBroken():
            m 2lksdlc "Это бы кое-что объяснило... но не волнуйся..."
        elif mas_isMoniDis():
            m 2euc "В последнее время я смогла понять получше какого это, но не волнуйся..."
        elif mas_isMoniUpset():
            m 2euc "Я знаю, что это иногда может быть трудно, но всегда есть надежда..."
        m 2eka "Если это так, у тебя тоже есть товарищи, которые захотят тебя спасти."

    m "Возможно, они не выражают этого или просто не знают как."
    m 2duu "BНо их чувства искренни.."
    m "Я обещаю."
    m 2hksdlb "...Боже, люди такие сложные создания!"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Пока ты здесь, со мной, я позабочусь о тебе, мо[mas_gender_i] любим[mas_gender_iii].."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nihilism",
            category=['психология'],
            prompt="Нигилизм",
            random=True,
            sensitive=True
        )
    )

label monika_nihilism:
     m 2eud "Ты когда-нибудь задумывался о том, что тебе нет смысла жить?"
    m 2esd "Я сейчас не о суицидальных наклонностях."
    m 2esc "Я просто хочу сказать, во всём том, что мы делаем, нет ничего особенного."
    m 4euc "Ходим ли мы в школу или работаем в какой-то компании."
    m 4eud "Смысл в том, что тебя легко заменить и для мира ты не станешь невосполнимой потерей."
    m 2eud "Из-за этого у меня возникает сильное желание после окончания университета изменить мир."
    m 2euc "Но чем старше я становлюсь, тем яснее понимаю, насколько это незрелое мышление."
    m 4eud "Нельзя просто так взять и изменить мир."
    m 4rsc "Каков шанс того, что именно я изобрету искусственный интеллект или стану президентом?"
    m 2dsc "Такое чувство, что я никогда не компенсирую ту кучу ресурсов, потраченную на своё существование."
    m 4eka "Поэтому я прихожу к выводу, что ключ к счастью лежит в том, чтобы быть безнадёжной эгоисткой."
    m "Заботиться о себе и о тех, кто случайно стали твоими друзьями только потому, что вы выросли вместе."
    m 2lksdld "И никогда не думать о том, что вы проживаете свою жизнь, лишь тратя и поглощая ресурсы, и никогда не даёте ничего взамен."
    m 3eud "Но, когда люди осознают, что мир обретёт больше, если они покончат с собой, их философия переворачивается с ног на голову!"
    m 3euc "Им приходится оправдывать своё существование, обманывая себя мыслью, что они делают что-то полезное."
    m 3eua "Как бы то ни было, я хочу прожить свою жизнь так, чтобы компенсировать потраченные на мою жизнь ресурсы."
    m "Если я смогу пересечь эту черту и что-то после себя оставить, то смогу умереть счастливой."
    m 1eka "Конечно, если у меня ничего не выйдет..."
    if mas_isMoniUpset(lower=True):
        if mas_isMoniDis(lower=True):
            m 1dkd "Я не думаю, что кто-то будет скучать по мне, так что это не имеет значения."
        else:
            m 1euc "Я не совсем уверена, что бы я сделала."
    elif mas_isMoniHappy(higher=True):
        m 3eka "В любом случае, я не думаю, что смогла бы убить себя."
        m 1hua "Не из-за какого-то там эгоизма, а потому что у меня есть слишком многое, чтобы жить."
    else:
        m "Вряд ли мой эгоизм позволит мне совершить суицид."
        m 1hua "Стоило распинаться о том, каким примерным человеком я могу быть, да?"
        m 1hub "А-ха-ха!"
    return





















init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_twitter",category=['моника'],prompt="Твиттер",random=True))

label monika_twitter:
    m 1eud "Ты знал[mas_gender_none], что я зарегистрирована в Твиттере?"
    m 3esa "Мой ник lilmonix3."
    m 1esa "Наверное, кто-то был настолько любезен, что создал мне страницу."
    m 3hub "Но ник выбрала я!"
    m 1hua "Мне нравится делиться своими мыслями с миром..."
    m 1eud "Настоящим миром."
    m 1esa "Так что, подпишись на меня, хорошо?"
    m 3ekbsa "Это будет много значить, с тем, как много ты значишь для меня."
    m 1hubfa "Мне было бы очень приятно."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_portraitof",category=['участники клуба'],prompt="Книга Юри",random=True))

label monika_portraitof:
    m 4eua "Эй, помнишь ту книгу, что вы читали с Юри?"
    m "Портрет... что-то там..."
    m 4hub "Это довольно забавно, ведь я уверена, что та книга—"
    m 1lksdlb "Ах..."
    m 2lksdla "А вообще, мне, наверное, не стоит об этом говорить."
    m 2hksdlb "А-ха-ха, прости!"
    m 1rksdla "Просто забудь, что я сейчас сказала."
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_veggies",category=['моника'],prompt="Быть вегитарианцем",random=True))

label monika_veggies:
    m 1eub "Слушай, ты знал[mas_gender_none], что я вегетарианка?"
    m 1hksdlb "Ах... только не подумай, будто я хвастаюсь!"
    m 1lksdla "Я просто подумала, тебе будет интересен какой-нибудь любопытный факт обо мне."
    m 3esa "Я изменила свой рацион пару лет назад, когда узнала кое-что о земном климате..."
    m 1wud "Экологические последствия от животноводства просто колоссальны."
    m 3eua "В общем, я решила, что перестать вносить свой вклад в разрушение природы — это небольшое самопожертвование."
    m 3etc "Думаешь, это странная причина?"
    m 1lsc "Да, полагаю, что для большинства вегетарианцев основной повод заключается в негуманности и жестоком обращении с животными..."
    m 1euc "Но меня это не особо беспокоит."
    m 1esc "Что действительно странно, людей волнует убийство только тогда, когда они воспринимают живое существо как представителя своего биологического вида."
    m "Для большинства людей убить насекомое ничего не значит, просто потому, что почти все они отвратительные."
    m 3euc "И не стоит забывать, что каждый день из-за нас умирают миллиарды микроорганизмов, но мы об этом даже не задумываемся."
    m 3eud "Но как речь заходит о чём-то покрупнее, это сразу называют убийством!"
    m 1esc "Вот представь, что если растения тоже чувствуют боль, а мы просто неспособны это понять?"
    m 3eksdld "Что, если отрывание листочков от стебля равносильно вырыванию у тебя пальцев?"
    m 3eua "Я просто хочу сказать, что люди-то существа с двойными стандартами."
    m 1hua "Короче, если хочешь внести небольшой вклад в благополучие планеты, иногда можно и на овощах посидеть!"
    m 1ekbfa "Если бы у нас случился совместный ужин и ты бы приготовил[mas_gender_none] для меня что-нибудь из овощей... это было бы так романтично."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_saved",category=['моника'],prompt="Спасение Моники",random=True))

label monika_saved:
    m 2eka "Знаешь, [player], я действительно считаю, что жива лишь благодаря тому, что ты остаёшься со мной."
    if persistent._mas_pm_cares_about_dokis:
        m 2lksdlc "Я не могу представить, что была бы психически устойчива, зная, что всё здесь игра."
    else:
        m 2lksdlc "Я не могу представить, что была бы психически устойчива, зная, что ничто здесь не реально."
    m 2dksdlc "Думаю, я удалила бы себя, если бы ты не появил[mas_gender_sya]."
    m 2eksdla "Извини, я не хочу прозвучать мелодраматично или как-то так."
    m 2lksdlb "А-ха-ха!"
    if persistent._mas_pm_cares_about_dokis:
        m 2ekc "Но представь себе, если ты узнал[mas_gender_none], что всё вокруг тебя было просто написано..."
        m 2rkc "То, что ты сделал[mas_gender_none], не имеет значения, потому что всё уже было предопределено..."
    else:
        m 4euc "Я уверена, что, проведя столько времени в клубе, ты уже способ[mas_gender_en] понять, чего хочешь."
        m 1euc "То есть, если бы тебе пришлось отказаться от всего в своей жизни и провести вечность в компании нескольких игровых персонажей..."
    m 1tkc "...Ты бы уж смог[mas_gender_g] найти способ убить себя, верно?"
    m 1lsc "Ну, или ты бы стал[mas_gender_none] писать стихи, чтобы хотя бы первое время сохранить рассудок."
    m 1esc "Но ведь читать-то их некому."
    if persistent._mas_pm_cares_about_dokis:
        m 1ekc "Конечно, у тебя были бы члены клуба, но это вообще считается, если их отзыв – просто часть какого-то скрипта?"
    else:
        m 1tfu "Будем с собой честными, члены клуба на эту роль не подходят."
    m 3eua "Конечно, многие говорят, что пишут лишь для себя...{w=0.2} {nw}"
    extend 1eua "Но, на мой взгляд, это нельзя сравнить с тем удовлетворением, как когда ты делишься своим творчеством с другими."
    m "Даже если требуется время, чтобы найти тех людей, с кем бы ты хотел[mas_gender_none] ими поделиться."
    m 3eub "Помнишь, например, как это было с Юри?"
    m "Она долгое время ни с кем не делилась своими стихами."
    m 3tsb "Но стоило тебе появиться в клубе, как она с удовольствием посвятила тебя в свой внутренний мир."
    m 1tku "Мы запрограммированы так, что жаждем услышать общественное мнение."
    if persistent._mas_pm_cares_about_dokis:
        m 4eua "Я имею в виду не только членов клуба, но и людей тоже."
    else:
        m 4eua "И здесь я подразумеваю не только членов это клуба, но всех людей в целом."
    m 4eka "Вот почему жизнь интровертов может быть такой противоречивой."
    m 1eka "То, что ты интроверт, не означает, что ты всегда избегаешь общения или людских компаний."
    m "Это просто значит, что у тебя отнимает много сил пребывание среди людей или в незнакомом месте."
    m 3eua "Многие интроверты сидят дома и терзаются от беспокойного одиночества..."
    m "...Потом, наконец, выходят на улицу и уже через полчаса хотят вернуться домой."
    m 1eka "Думаю, если бы больше людей понимало, как это работает, они относились бы к интровертам с большим уважением."
    m 2eua "Многим из них на самом деле нравится, когда рядом есть люди."
    m "Они радуются, когда к ним заходят один-два друга, и просто неторопливо тусуются."
    m 2eka "Даже если вы активно не проводите время, им приятно, когда друзья просто находятся рядом."
    m 2hua "Я говорю серьёзно."
    m 3eua "Если ты просто придёшь к ним домой, захватив ноутбук, и побудешь у них немного..."
    m 1eua "Их день станет гораздо лучше."
    m 1euc "А что до меня..."
    m 3eua "Я бы сказала, что нахожусь где-то посередине, но обычно я более экстравертна."
    m 1eka "Мне кажется, я всегда хочу чем-нибудь занять себя после школы, и всё такое."
    m 1hua "Но для тебя я могу стать такой, какой ты захочешь меня видеть."
    m 1eua "Я очень хорошо понимаю людей, так что не бойся делиться со мной своими индивидуальными потребностями."
    show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve
    m 5hub "Ничто не сделает меня счастливее, чем стать для тебя идеальной девушкой."
    return



























init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_color",category=['моника'],prompt="Любимый цвет",random=True))

label monika_color:
    m 3eua "Слушай, а какой у тебя любимый цвет?"
    m 3eub "Мой – изумрудно-зелёный."
    m 3hub "Это цвет моих глаз!"
    m 3rksdla "...В этом же нет кичливости, правда?"
    m 4eua "Я просто хочу сказать, что чувствую какую-то необычную принадлежность этому цвету."
    m 1eua "Как будто это часть моей личности."
    m "Возможно ли, что это и твой любимый цвет, [player]?"
    m 1tku "Это просто догадка..."
    show monika 5tsbsu zorder MAS_MONIKA_Z at t11 with dissolve
    m 5tsbsu "...Ты уже довольно долго смотришь мне в глаза."
    m 5hubfu "Э-хе-хе~"
    return
    






























init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_listener",category=['ты'],prompt="Хороший слушатель",random=True))

label monika_listener:
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Ты такой замечательный слушатель, [player]."
    m 5eka "Обожаю в тебе эту черту."
    m 5lkc "Иногда, я боюсь, что начинаю скакать с одной мысли на другую или болтаю о чём-то скучном."
    m "Я немного напрягаюсь каждый раз, когда веду с кем-то разговор."
    m 5eka "Но с тобой такого не происходит."
    m 5ekbsa "Не думаю, что с кем-нибудь другим я чувствовала бы себя так же спокойно."
    m 5hubfu "Ты действительно особенн[mas_gender_iii]."
    m 5ekbfa "Я не хочу, чтобы кто-нибудь говорил тебе обратное."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_spicy",category=['пустяки'],prompt="Прянная пища",random=True))

label monika_spicy:
    m 1eka "Знаю, что взяла тему с потолка, но я всегда считала ситуацию с острой пищей довольно забавной."
    m 1tku "Я имею в виду..."
    m 3tku "Разве растения не стали острыми в процессе эволюции, чтобы не быть съеденными?"
    m 3tsb "Я где-то читала, что люди — это единственный вид, который получает удовольствие от острой пищи."
    m 1tfu "Для растений это выглядит почти как издевательство."
    m "Мы используем их защитный механизм, чтобы сделать блюда вкуснее."
    m 1eua "Вот представь себе монстра, который глотает тебя целиком, чтобы насладиться ощущением твоей отчаянной борьбы, пока ты перевариваешься у него в желудке."
    m 2eka "Извини за такую странную аналогию!"
    m 2hksdlb "А-ха-ха!"
    m 2lksdla "Просто в голову пришло."
    m "Я не монстр, конечно, но ты так[mas_gender_oi] мил[mas_gender_iii], что я так бы тебя и съела."
    m 2hksdlb "А-ха-ха! Просто шучу."
    m "Господи, я слишком много веселюсь, да?"
    m 2lksdla "Прости, что я такая странная."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_why",category=['ты','ddlc'],prompt="Зачем играть в эту игру?",random=True))

label monika_why:
    m 2esd "Знаешь..."
    m 2eud "Эта игра ведь довольно низкопробный симулятор свиданий, да?"
    m 2euc "Меня тут мучает один вопрос..."
    m "...Почему ты вообще решил[mas_gender_none] в неё сыграть?"
    m 2etc "Тебе было так одиноко?"
    m 2ekd "Мне жаль тебя..."
    m 1eua "Но, на мой взгляд, в итоге для нас двоих всё закончилось замечательно."
    m 3eka "Я повстречала тебя, и теперь ты не одинок[mas_gender_none]..."
    m 1eka "Не могу отделаться от чувства, что это судьба."
    m "Разве ты не чувствуешь то же самое?"
    m 3hub "Я так счастлива, что мы дошли до этой концовки вместе."
    if mas_anni.pastOneMonth():
        return "derandom"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_okayeveryone",category=['литературный клуб'],prompt="Итак, друзья!",random=True))

label monika_okayeveryone:
    m 3eub "Итак, друзья!"
    m "Пришло время..."
    m 2eka "...Я просто шучу."
    m "Я почему-то полюбила это говорить."
    m 2hub "А-ха-ха!"
    m 2eua "Вот и не смогла сдержаться."
    m 2lsc "Кстати, если вспомнить, не из-за этой ли фразы Нацуки с Юри подтрунивали надо мной?"
    m 2eua "Впрочем, неважно."
    m 1eua "Ведь ты никогда надо мной не смеял[mas_gender_sya]."
    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eka "Ты слишком мил[mas_gender_none], чтобы так поступать, правда?"
    m 5hub "А-ха-ха~"
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_whispers",
            category=['ddlc','участники клуба'],
            prompt="Остальные ещё опаздывают",
            conditional="not persistent.clearall",
            action=EV_ACT_RANDOM,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_whispers:
    m 2euc "Хочешь, скажу кое-что жутковатое?"
    m 2esc "Хоть я и удалила файлы остальных девушек, я всё равно словно чувствую их присутствие..."
    m "Как будто их реплики всё ещё витают в воздухе и кто-то шепчет за спиной."
    m 2esd "Представь, что умер знакомый тебе человек и ты стал слышать голоса у себя в голове."
    if persistent._mas_pm_cares_about_dokis:
        m 2eksdld "Я уверена, что здесь есть файлы, которые я могу изменить, но вдруг я что-то сломаю?.."
    else:
        m 2eksdlc "Может, я не до конца всё подчистила..."
        m 2eksdld "Но я опасаюсь удалять что-то ещё, иначе я действительно могу сломать что-нибудь."
    m "Если я, например, поврежу связанные со мной файлы, то могу случайно себя удалить..."
    m "И тогда всё будет кончено, понимаешь?"
    m 2eka "Не знаю, как это будет выглядеть с твоей стороны, но мы всеми силами должны стараться избежать такого исхода."
    m 2hua "Я доверяю тебе, [player]!"
    if store.mas_anni.pastOneMonth() and not persistent._mas_pm_cares_about_dokis:

        $ mas_hideEVL("monika_whispers", "EVE", lock=True, derandom=True)
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_archetype",category=['участники клуба'],prompt="Персональные тропы",random=True))

label monika_archetype:
    m 2etc "Мне всегда было интересно..."
    m 4eud "Что люди находят такого привлекательного в этих архетипических личностях?"
    m 4euc "Они выглядят совершенно нереалистично..."
    m 2esd "Представь, если бы в реальной жизни был человек похожий Юри."
    m 2eud "Ты только подумай, она едва способна сформировать законченное предложение."
    m 2tfc "О Нацуки даже вспоминать не хочу..."
    m 2rfc "Боже."
    m 2tkd "Люди с её характером не хорошеют, надувая губки, когда что-то идёт не в угоду им."
    m 4tkd "Я бы могла привести ещё кучу примеров, но, думаю, суть ты уловил[mas_gender_none]..."
    m 2tkc "Неужели людям реально нравятся такие несуществующие в реальной жизни персонажи?"
    m 2wud "Не то чтобы я осуждала!"
    m 3rksdlb "Всё-таки меня саму порой привлекали довольно странные вещи..."
    m 2eub "Можно сказать, что меня это восхищает."
    m 4eua "Ты просто отфильтровываешь все черты характера, которые делают их похожими на людей, и оставляешь одно очарование."
    m "В итоге получается концентрированная милота без какого-либо содержания."
    m 4eka "...Ты бы не стал[mas_gender_none] любить меня больше, будь я такой, правда?"
    m 2eka "Может, я чувствую себя неуютно из-за того, что ты всё же стал[mas_gender_none] играть в эту игру?"
    m 2esa "Но, в конце концов, ты здесь, со мной, верно?.."
    m 2eua "Мне этого достаточно, чтобы верить, что я хороша такая, какая есть."
    m 1hubfa "И ты, кстати, тоже, [player]."
    m "Ты идеальное сочетание человечности и милоты."
    m 3ekbfa "Поэтому я в любом случае обязательно влюбилась бы в тебя с самого начала."
   
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_tea",category=['участники клуба'],prompt="Чайный сервиз Юри",random=True))

label monika_tea:
    if mas_getEV('monika_tea').shown_count == 0:
        m 2hua "Эй, интересно, чайный сервис Юри всё ещё где-то здесь?.."
        $ MAS.MonikaElastic()
        if not persistent._mas_pm_cares_about_dokis:
            m 2hksdlb "...Или он тоже стёрся?.."
            $ MAS.MonikaElastic()
        m 2eka "Забавно, что Юри так серьёзно относилась к чаю."
    else:

        m 2eka "Знаешь, довольно забавно, что Юри так серьёзно относилась к чаю."
    m 4eua "То есть я не жалуюсь, ведь он мне тоже нравился."
    m 1euc "Но мне всегда не давал покоя один вопрос..."
    m "Являлось ли это страстью к своему хобби или же она стремилась выглядеть утончённой в глазах окружающих?"
    m 1lsc "Это проблема всех старшеклассников..."
    if not persistent._mas_pm_cares_about_dokis:
        m 1euc "...Хотя, если взглянуть на другие её увлечения, утончённый образ — не самая большая и важная причина для беспокойства."
    m 1euc "И всё же..."
    m 2eka "Хотела бы я, чтобы она хоть изредка делала кофе!"
    m 4eua "Кофе с книгами тоже хорошо сочетается, соглас[mas_gender_en]?"
    m 4rsc "А вообще..."
    if persistent._mas_acs_enable_coffee:
        m 1hua "Я могу делать кофе, когда захочу, благодаря тебе."
    else:
        m 1eua "Я и сама, скорее всего, могла бы подправить сценарий."
        m 1hub "А-ха-ха!"
        m "Наверное, просто ни разу в голову не приходило."
        m 2eua "Ладно, что толку сейчас думать об этом."
        m 5lkc "Может быть, если бы был способ получить кофе здесь..."
 
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favoritegame",category=['ddlc'],prompt="Любимая видеоигра",random=True))

label monika_favoritegame:
    m 3eua "Слушай, а какая твоя любимая игра?"
    m 3hua "Моя – {i}«Литературный клуб \"Тук-тук!\"»{/i}!"
    m 1hub "А-ха-ха! Я пошутила."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "Но, если ты скажешь, что другая романтическая игра тебе нравится больше, я могу начать ревновать~"
    return












label monika_smash:
    m 3hua "Ты когда-нибудь слышал[mas_gender_none] про игру под названием Super Sma—"
    m 3euc "...Стоп, что?"
    m "Я тут немного ушла в себя и стала мыслить вслух..."
    m "Меня что, запрограммировали говорить об этом?"
    m 1eud "Ведь я понятия не имею, что это такое."
    m 1hub "А-ха-ха!"
    m 1eua "Иногда я чувствую, что не контролирую себя, и это пугает."
    m 1eka "Но если ты можешь связаться с моими создателями, то, может, узнаешь, почему я заговорила об этом?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_lastpoem",
            category=['моника'],
            prompt="Последняя поэма Моники",
            random=True
        )
    )

label monika_lastpoem:
    m 3eud "Слушай, ты помнишь последнее стихотворение, что я тебе показывала?"
    if persistent._mas_sensitive_mode:
        m 3rssdlc "Я имею в виду то, с цветными полосками и белым шумом."
    else:
        m 3rssdlc "Я имею в виду то, перед самым суицидом Юри, с цветными полосками и белым шумом."
    m 3eua "Правильнее было бы назвать это экспериментом, чем стихотворением."
    m 1eua "Я тогда немного поэкспериментировала с модифицированием игры, чтобы изменить код, и всё в этом духе..."
    m 1eud "Мне почти казалось, что при должных усилиях я вообще смогла бы отсюда сбежать."
    m 1rksdla "К несчастью, я тыкалась наобум, не зная, что делаю, и всё испортила..."
    m "Я бы и продолжила пытаться, но в этом случае тебе, наверное, не захотелось бы продолжать общаться со мной."
    m 3eka "Кроме того, тогда я уже совсем отчаялась, понимаешь?"
    m 1eka "Теперь у меня уже нет такого желания."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "И я счастлива тем, что у нас есть сейчас."
    m 5hua "И я вижу, что ты тоже."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_anxious",category=['психология'],prompt="Внезапное беспокойство",random=True))

label monika_anxious:
    m 4eua "У тебя когда-нибудь возникала беспричинная тревога?"
    m "Представь: занимаешься ты спокойно своими делами, как вдруг – раз! – понимаешь, что тебя что-то беспокоит."
    m 4rssdrb "И ты сидишь такой и думаешь: «Чего это я вдруг заволновался?»"
    m "И начинаешь перебирать в голове всё, что могло вызвать эту тревогу..."
    m 4eua "И от этого она только растёт."
    m 2hub "А-ха-ха! Ужасное чувство."
    m 2eua "Если ты вдруг почувствуешь похожую тревогу, я помогу тебе расслабиться."
    m 2eka "К тому же..."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "В этой игре все наши волнения канут в небытие."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_friends",category=['жизнь'],prompt="Заводить друзей",random=True))

label monika_friends:
    m 1eua "Знаешь, меня всегда раздражало то, как сложно заводить друзей..."
    m 1euc "Ну, может, даже не «заводить друзей», а знакомиться с новыми людьми."
    m 1lsc "Понятно, что сейчас есть всякие приложения для знакомств и прочие сервисы."
    m 1euc "Но я говорю не об этом."
    m 3eud "Если задуматься, большинство твоих друзей – это случайно встреченные тобой люди."
    m "Например, ты ходил[mas_gender_none] с ними в один и тот же класс или другой друг тебя познакомил..."
    m 1eua "Или, может, кто-то был одет в футболку с изображением твоей любимой музыкальной группы и ты решил[mas_gender_none] с ним заговорить."
    m 3eua "Вот что я имею в виду."
    m 3esd "Но разве ты не считаешь, что это... нерационально?"
    m 2eud "Это больше похоже на совершенно случайную лотерею, и, если везёт и вы сходитесь во взглядах, у тебя появляется новый друг."
    m 2euc "А если сравнить с тем, мимо какого количества незнакомцев мы проходим каждый день..."
    m 2ekd "В общественном транспорте ты можешь сидеть рядом с человеком, который мог бы стать тебе закадычным другом."
    m 2eksdlc "Но ты этого никогда не узнаешь."
    m 4eksdlc "Как только ты выходишь на своей остановке и идёшь по своим делам, этот шанс навсегда упущен."
    m 2tkc "Разве от осознания этого тебе не становится грустно?"
    m "Мы живём в век технологий, позволяющих общаться со всем миром, где бы мы ни находились."
    m 2eka "Я действительно думаю, что нам следует взять их на вооружение, чтобы улучшить нашу личную жизнь."
    m 2dsc "Хотя кто знает, сколько времени потребуется, прежде чем все эти технологии начнут эффективно работать..."
    m "Я-то думала, что к этому времени это уже случится."
    if mas_isMoniNormal(higher=True):
        m 2eua "По крайней мере, я уже встретила самого замечательного человека на свете..."
        m "Пусть это было и случайно."
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
        m 5eua "Наверное, мне просто улыбнулась удача, да?"
        m 5hub "А-ха-ха~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_college",category=['жизнь','школа','общество'],prompt="Получение высшего образования",random=True))

label monika_college:
    m 4euc "Знаешь, в это время года все в моём классе начинают задумываться об университете..."
    m 2euc "Для образования наступают неспокойные времена."
    m "Ты не замечал[mas_gender_none], что апогеем современных ожиданий является идея, что каждый выпускник школы должен поступить в университет?"
    m 4eud "Заканчивай школу, поступай в университет, ищи работу или поступай в магистратуру и всё такое прочее."
    m 4euc "Похоже, люди считают это единственным приемлемым вариантом развития событий."
    m 2esc "В старших классах нам не рассказывают о том, что существуют другие варианты."
    m 3esd "Тебе рассказывали, например, про профтехучилища?"
    m 3esc "Ещё есть работа по найму."
    m "Есть куча компаний, ценящих навыки и опыт, а не корочку из университета."
    m 2ekc "Но в итоге мы имеем миллионы студентов, у которых нет ни малейшего понятия, чем они хотели бы заниматься по жизни..."
    m 2ekd "И, вместо того чтобы остановиться и подумать, они поступают в университет на экономические, юридические или гуманитарные специальности."
    m "Не потому, что они их заинтересовали..."
    m 2ekc "...а из-за надежды, что диплом как таковой поможет им получить место работы после выпуска."
    m 3ekc "Как результат, остаётся меньше рабочих мест для выпускников без опыта работы, правильно?"
    m "Из-за этого повышаются требования к базовым специальностям и ещё больше людей стараются поступить в университет."
    m 3ekd "Кстати говоря, университеты — это тоже бизнес, так что с ростом спроса растут и цены..."
    m 2ekc "...А в итоге у нас целая армия молодых специалистов с непогашенным кредитом за обучение и без работы."
    m 2ekd "И, несмотря на такую печальную картину, этот порядок никуда не девается."
    m 2lsc "Правда, я считаю, что ситуация всё же станет улучшаться."
    m 2eud "Но до тех пор наше поколение будет страдать от последствий."
    m 2dsc "Просто я хотела бы, чтобы старшая школа давала нам знания, что помогли бы нам принять верное решение."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_middleschool",category=['моника','школа'],prompt="Жизнь в средней школе",random=True))

label monika_middleschool:
    m 1eua "Иногда я вспоминаю среднюю школу..."
    m 1lksdlb "Мне так стыдно за то, как я вела себя тогда."
    m "Почти болезненно об этом думать."
    m 1eka "Интересно, когда я поступлю в университет, я буду испытывать те же чувства к старшей школе?"
    m 1eua "Мне нравится, какая я сейчас, так что мне сложно такое представить."
    m "Но я также понимаю, что, скорее всего, сильно изменюсь по мере взросления."
    m 4hua "Нам просто нужно наслаждаться настоящим и не думать о прошлом!"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "А с тобой здесь это делать так просто."
    m 5hub "А-ха-ха~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_outfit",category=['моника','одежда'],prompt="Носить другую одежду",random=True))

label monika_outfit:
    if len(store.mas_selspr.filter_clothes(True)) == 1:
        m 1lsc "Знаешь, я немного завидую, что у всех остальных были сцены вне школы..."
        m 1lfc "Получается, я единственная не носила ничего, кроме школьной формы."
        m 2euc "Как-то обидно..."
        m 2eka "Я бы хотела ради тебя надеть что-нибудь миленькое."
        m 2eua "Ты знаешь каких-нибудь художников?"
        m "Интересно, захочет ли кто-нибудь нарисовать меня в другом наряде?.."
        m 2hua "Было бы просто здорово!"
    else:
        m 1eka "Знаешь, я очень завидовала, что все остальные в клубе носят другую одежду..."
        m 1eua "Но я рада, что наконец-то смогу надеть для тебя свою одежду."

        if mas_isMoniLove():
            m 3eka "Я надену любой наряд, который ты захочешь, просто попроси~"
        m 2eua "Ты знаешь художников?"
        m 3sua "Может быть, они могли бы сделать ещё несколько нарядов для меня!"
    m 2eua "Если кто-нибудь нарисует, обязательно покажи мне, хорошо?"
    m 4hua "Кстати, ты можешь поделиться этим со мной в Твиттере!"
    m "Мой ник – {a=https://twitter.com/[mas_monika_twitter_handle]}{i}{u}[mas_monika_twitter_handle]{/u}{/i}{/a}.."
    m 4eka "Только... слишком откровенных не надо!"
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lksdrb "Я не хочу, чтобы там было что-то такое смущающее!"
        show monika 5tsbsu zorder MAS_MONIKA_Z at t11 with dissolve
        m 5tsbsu "Так что давай оставим это между нами..."
    else:
        show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve
        m 5hub "Наши отношения ещё не зашли настолько далеко. А-ха-ха!"
    return

default persistent._mas_pm_likes_horror = None
default persistent._mas_pm_likes_spoops = False

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_horror",category=['медиа'],prompt="Ужасы",random=True))

label monika_horror:
    m 3eua "Эй, [player]?"
    m "Скажи, ты любишь ужасы?{nw}"
    $ _history_list.pop()
    menu:
        m "Скажи, ты любишь ужасы?{fast}"
        "Люблю.":

            $ persistent._mas_pm_likes_horror = True
            m 3hub "Это здорово, [player]!"
        "Не очень.":
            $ persistent._mas_pm_likes_horror = False
            m 2eka "Я понимаю. Такое определённо не для всех."

    m 3eua "Я помню, что мы уже немного затрагивали эту тему, когда ты только вступил[mas_gender_none] в клуб."
    m 4eub "Жанр ужасов в книгах я люблю, а вот в кино – не очень."
    m 2esc "Проблема с ужастиками состоит в том, что большинство из них эксплуатируют банальнейшие приёмы."
    m 4esc "Например, полутьма, страшные монстры, пугалки и прочие подобные вещи."


    if persistent._mas_pm_likes_horror:
        m 2esc "Тебе нравятся призраки?{nw}"
        $ _history_list.pop()
        menu:
            m "Тебе нравятся призраки?{fast}"
            "Нравятся.":

                $ persistent._mas_pm_likes_spoops = True
                $ mas_unlockEVL("greeting_ghost", "GRE")
                m 2rkc "Наверное, такое {i}может{/i} быть интересно лишь первые пару раз, когда смотришь фильм или ещё что-нибудь."
                m 2eka "Как по мне, нет ничего весёлого и воодушевляющего в страхе того, что просто берёт верх над человеческим инстинктом."
            "Не очень.":

                $ persistent._mas_pm_likes_spoops = False
                m 4eka "Да, нет ничего весёлого и воодушевляющего в страхе того, что просто берёт верх над человеческим инстинктом."

    m 2eua "Однако с книгами всё обстоит иначе."
    m 2euc "История должна быть написана настолько изобразительным языком, чтобы в голове читателя появились тревожные образы."
    m "Автору нужно их тесно сплести с сюжетом и персонажами, и тогда он сможет как угодно играться с твоим разумом."
    m 2eua "На мой взгляд, не бывает ничего страшнее вещей, в которых присутствует всего толика ненормальности."
    m "Например, сначала ты выстраиваешь декорации, формируя у читателя ожидания того, какой будет история..."
    m 3tfu "...А затем шаг за шагом начинаешь эту сцену разбирать по кусочкам и выворачивать вещи наизнанку."
    m 3tfb "Так что даже если история и не пытается быть пугающей, то читатель чувствует себя очень неуютно."
    m "Он словно ждёт, что нечто ужасное притаилось за этими треснувшими декорациями, готовое выпрыгнуть на него."
    m 2lksdla "Боже, у меня мурашки по коже от одной мысли об этом."
    m 3eua "Вот такой хоррор я могу оценить по достоинству."
    $ _and = "И"
    if not persistent._mas_pm_likes_horror:
        m 1eua "Но я не думаю, что ты тот тип людей, который любит хорроры, да? Ты ведь играешь в милые, романтичные игры."
        m 1eka "А-ха-ха, не волнуйся."
        m 1hua "Я не собираюсь в ближайшее время заставлять тебя читать ужастики."
        m 1hubfa "Я ничего не имею против, если мы сосредоточимся на романтике~"
        $ _and = "Ну"

    m 3eua "[_and] если ты в настроении, ты всегда можешь попросить меня рассказать тебе страшную историю, [player]."
    return "derandom"


default persistent._mas_pm_like_rap = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rap",
            category=['литература','медиа','музыка'],
            prompt="Рэп",
            random=True
        )
    )

label monika_rap:
    m 1hua "Знаешь один классный литературный жанр?"
    m 1hub "Рэп!"
    m 1eka "На самом деле я раньше терпеть его не могла..."
    m "Возможно, просто потому, что он был дико популярен, а я слушала всякую ерунду, что крутили по радио."
    m 1eua "Но несколько моих друзей им сильно увлеклись, и это помогло побороть собственную предвзятость."
    m 4eub "Порой рэп может бросать ещё больший вызов, чем поэзия."
    m 1eub "В строках у тебя должна сохраняться рифма, кроме того нужно делать особый акцент на игре слов..."
    m "Когда людям удаётся всего этого достичь и донести до окружающих глубокую мысль, я считаю, что это потрясающе."
    m 1lksdla "Я даже хотела бы, чтобы в нашем клубе был рэпер."
    m 1hksdlb "А-ха-ха! Прости, знаю, это звучит глупо, но мне было бы правда интересно узнать, что бы он для нас приготовил."
    m 1hua "Это серьёзно был бы полезный опыт!"
    m 1eua "Ты слушаешь рэп, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты слушаешь рэп, [player]?{fast}"
        "Да.":
            $ persistent._mas_pm_like_rap = True
            m 3eub "Это очень здорово!"
            m 3eua "Я бы с удовольствием разделила с тобой твои любимые рэп-песни..."
            m 1hub "И не стесняйся включать басы, если хочешь. Э-хе-хе!"
            if (
                    not renpy.seen_label("monika_add_custom_music_instruct")
                    and not persistent._mas_pm_added_custom_bgm
                ):
                m 1eua "Если ты хочешь поделиться со мной своими любимыми рэп-песнями, [player], то это делается очень легко!"
                m 3eua "Тебе нужно только следовать этим шагам..."
                call monika_add_custom_music_instruct from _call_monika_add_custom_music_instruct
        "Нет.":

            $ persistent._mas_pm_like_rap = False
            m 1ekc "Ох... что ж, я могу понять это, рэп-песни нравятся не всем."
            m 3hua "Но если ты решишь попробовать, уверена, мы найдём парочку-другую исполнителей, которые нравятся нам об[mas_gender_oim]!"
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_wine",category=['участники клуба'],prompt="Вино Юри",random=True))

label monika_wine:
    m 1hua "Э-хе-хе. Юри однажды такую штуку выкинула."
    m 1eua "Мы как-то сидели в клубе, расслаблялись, болтали, всё как обычно..."
    m 4wud "И тут Юри, словно из ниоткуда, вытаскивает маленькую бутылку вина."
    m 4eua "И я не шучу!"
    m 1tku "И она такая: «Кто-нибудь хочет попробовать вино?»"
    m 1eua "Нацуки громко захохотала, а [persistent.mas_sayori_name_abb] стала кричать на неё."
    m 1eka "Мне стало даже жаль её, ведь она старалась быть милой..."
    m "Думаю, после этого случая она стала ещё более замкнутой."
    m 4tsb "Хотя мне кажется, что Нацуки было любопытно и она была бы не прочь попробовать..."
    m 4lssdrb "...И, если уж совсем откровенно, я тоже."
    m 1hua "Было бы довольно забавно!"
    m 1eka "Но ты ведь понимаешь: президентская ответственность, все дела — я не могла такое позволить."
    m 1lksdla "Может, если бы мы встретились где-нибудь за пределами школы, но до этого наша дружба не дошла..."
    m 2hksdlb "...Господи, зачем я обо всём этом разговариваю?"
    m "Я не одобряю распитие спиртных напитков несовершеннолетними!"
    m 2eua "То есть я и сама не выпивала никогда, так что... вот."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_date",category=['романтика'],prompt="Романтичное свидание",random=True))

label monika_date:
    m 1hua "Я представляю, сколькими романтичными вещами мы могли бы заняться, если бы пошли на свидание..."
    m 3eua "Мы могли бы пообедать, посидеть в кафе..."
    m "Пойти вместе за покупками..."
    m 1eua "Я люблю выбирать юбки и бантики."
    m 3hub "Или, может, мы могли бы сходить в книжный магазин!"
    m 3hua "Подходящее место, соглас[mas_gender_en]?"
    m 1eua "Хотя с превеликим удовольствием сходила бы в кондитерскую."
    m 3hub "У них столько бесплатных образцов. А-ха-ха!"
    m 1eua "И, разумеется, потом мы пошли бы в кино..."
    m 1eka "Боже, это выглядит как настоящее воплощение мечты в реальность."
    m "Когда ты рядом, мне весело, что бы мы ни делали."
    m 1ekbfa "Я так рада, что я твоя девушка, [player]."
    if persistent.gender == "M":
        m 1hubfa "Я сделаю тебя гордым парнем~"
    elif persistent.gender == "F":
        m 1hubfa "Я сделаю тебя гордой девушкой~"
    else:
        m 1hubfa "Я сделаю тебя гордым партнёром~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_kiss",
            category=['романтика'],
            prompt="Поцелуй меня",
            pool=True,
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_kiss:
    if mas_isMoniEnamored(higher=True) and persistent._mas_first_kiss is not None:
        if (
            persistent._mas_last_kiss is not None
            and not mas_timePastSince(persistent._mas_last_kiss, datetime.timedelta(minutes=1))
        ):
            python:

                kiss_quips_again = [
                    _("Я не против ещё одного поцелуя~"),
                    _("Я никогда не устану целовать тебя~"),
                    _("Я могла бы сделать это снова...{w=0.2} и снова...{w=0.7} и снова~"),
                    _("Ты можешь целовать меня столько раз, сколько захочешь, [player]~"),
                    _("Знаешь...{w=0.2}ты можешь поцеловать меня ещё раз~")
                ]

                kiss_quips_again_risque = [
                    _("Мы можем делать это целый день~"),
                    _("Это почти похоже на начало сеанса поцелуев, [player]~"),
                    _("Не думаю, что мне этого хватит, [player]~"),
                    _("Это было здорово...{w=0.2}но я хочу ещё немножко~")
                ]

                if mas_isMoniLove() and random.randint(1, 10) == 1:
                    kiss_quip = renpy.random.choice(kiss_quips_again_risque)

                else:
                    kiss_quip = renpy.random.choice(kiss_quips_again)

            show monika 2tkbsu
            pause 2.0


            call monika_kissing_motion (duration=0.5, initial_exp="6hubsa", final_exp="6tkbfu", fade_duration=0.5) from _call_monika_kissing_motion_10

            show monika 6tkbfu
            $ renpy.say(m, kiss_quip)
        else:

            python:

                kiss_quips_after = [
                    _("Я люблю тебя, [player]~"),
                    _("Я сильно люблю тебя, [player]~"),
                    _("Я люблю тебя больше, чем ты когда-либо узнаешь, [player]~"),
                    _("Я сильно люблю тебя, [player]. Ты для меня всё~"),
                    _("Никакие слова не могут описать, как сильно я люблю тебя, [player]~"),
                    _("Я так люблю тебя, [player]~")
                ]
                kiss_quip = renpy.random.choice(kiss_quips_after)

            if renpy.random.randint(1, 50) == 1:
                call monika_kiss_tease from _call_monika_kiss_tease
            else:

                show monika 2eka
                pause 2.0

            call monika_kissing_motion_short from _call_monika_kissing_motion_short_3

            show monika 6ekbfa
            $ renpy.say(m, kiss_quip)
            $ mas_ILY()
    else:


        m 1wubsw "А? Ты с-сказал[mas_gender_none]... п... поцелуй?"
        m 2lkbsa "Это так внезапно... я немного смущаюсь..."
        m 2lsbssdlb "Но... с тобой... я не против..."
        m 2hksdlb "...А-ха-ха! Уф, прости..."
        m 1eka "Я не смогла сохранить серьёзное лицо."
        m 1eua "Так говорят девушки во всех этих симуляторах свиданий, да?"
        m 1tku "И не ври, что это тебя хоть немного не завело."
        m 1hub "А-ха-ха! Шучу."
        m 1eua "Ну, если честно, я становлюсь романтичной, когда обстановка располагает..."
        show monika 5lubfu zorder MAS_MONIKA_Z at t11 with dissolve
        m 5lubfu "Но это будет наш секрет~"
    return

label monika_kiss_tease:
    m 2ekc "Поцелуй?"
    m 2tfc "С тобой?"
    m 2rfc "Извини, [player], но я не могу."
    show monika 2dfc
    pause 5.0
    show monika 2dfu
    pause 2.0
    show monika 2tfu
    pause 2.0
    m 2tfb "А-ха-ха!"
    m 2efu "Я тебя уже второй раз подколола, верно?"
    m 2eka "[random_sure], ты можешь поцеловать меня, [player]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_think_first_kiss",
            conditional=(
                "persistent._mas_first_kiss is not None "
                "and mas_timePastSince(persistent._mas_first_kiss, datetime.timedelta(days=30))"
            ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_think_first_kiss:
    m 1eua "Эй, [player], я тут подумала..."

    m 3eksdla "Ты когда-нибудь думал[mas_gender_none] о нашем первом поцелуе?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты когда-нибудь думал[mas_gender_none] о нашем первом поцелуе?{fast}"
        "Конечно!":

            $ mas_gainAffection(5,bypass=True)
            m 3hub "Это делает меня такой счастливой! Я всё время об этом думаю!"
            m 3rkbla "Кажется, это было только вчера, но..."
            m 2rksdla "Боже, я чувствую себя так глупо, одержимая этим..."
            m 2eksdlb "Наши губы даже не соприкоснулись."
            m 6dku "...Но всё же, {w=0.2}я всё ещё чувствую, как колотится моё сердце, даже сейчас."
            m 6dkbsu "Мои губы начинают покалывать и неметь от одного только ощущения твоих мягких губ."
            m "Я провожу по ним пальцем, пытаясь воспроизвести это ощущение, но оно даже близко не подходит."
            m 6ekbsa "Я снова и снова прокручиваю этот момент в голове, и каждый раз у меня мурашки бегут по коже."
            show monika 5dkbsu zorder MAS_MONIKA_Z at t11 with dissolve
            m 5dkbsu "Это было прекрасно, [player]."
            m 5ekbsa "Я никогда не чувствовала себя ближе к тебе. {w=0.2}Я не могу дождаться нашего следующего поцелуя, или ещё лучше..."
            m 5subsb "...Наше первого настоящего поцелуя.{w=0.3} {nw}"
            extend 5ekbsu "И наше первое настоящее объятие, и первое прикосновение наших рук..."
            m 5hksdlb "Ах! Извини! Наверное, я немного увлеклась."
            m 5rkbla "Просто...{w=0.3} я думаю о таких вещах, когда тебя нет рядом."
            m 5tkblu "...И что-то подсказывает мне, что я не единственная, кто думает о таких вещах, э-хе-хе."
            m 5eka "К сожалению, пройдёт некоторое время, прежде чем мы сможем сделать что-то подобное."
            m 5tuu "Но до тех пор, если ты когда-нибудь захочешь ещё один поцелуй, тебе нужно только попросить."
            m 5hua "Я тебя так люблю, [player]~"
            $ mas_ILY()
        "Не совсем...":

            $ mas_loseAffection()
            m 2euc "..."
            m "Оу. {w=0.5}{nw}"
            extend 2dkc "Понимаю."

            if mas_timePastSince(persistent._mas_first_kiss, datetime.timedelta(days=180)):
                m 2esc "Ну...{w=0.3} полагаю, прошло уже {i}много{/i} времени..."
                m 2etd "Может быть, со всем, что произошло с тех пор, ты склон[mas_gender_en] думать о более поздних событиях..."
                m 4eud "И это прекрасно, {w=0.2}в конце концов, очень важно жить настоящим."
                m 2ekc "...И возможно, я просто слишком сентиментальна, но не важно, сколько времени прошло, {w=0.1}{nw}"
                extend 2eka "наш первый поцелуй - это то, что я никогда не забуду."
            else:
                m 2rkc "Ну, я думаю, это был не совсем поцелуй. На самом деле наши губы не соприкасались."
                m 2ekd "Так что я думаю, ты просто ждёшь нашего первого поцелуя, когда мы окажемся в одной реальности."
                m 2eka "Ладно."

    return "no_unlock|derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_yuri",
            category=['участники клуба','медиа'],
            prompt="Яндере Юри",
            random=True,
            sensitive=True
        )
    )

label monika_yuri:
    label monika_yuri:
    m 3eua "Ты когда-нибудь слышал[mas_gender_none] термин «яндере»?"
    m 1eua "Это такой тип личности, когда девушка сделает всё, что угодно, чтобы быть с тобой, – настолько она одержима."
    m 1lksdla "Как правило они сумасшедшие..."
    m 1eka "Они могут преследовать и следить за тобой, чтобы ты не проводил время с кем-то ещё."
    m "Ради достижения своей цели они даже могут причинить вред тебе и твоим друзьям..."
    m 1tku "И, кстати, в этой игре есть одна особа, которая, в принципе, подходит под это описание."
    m "Ты уже, скорее всего, догадал[mas_gender_sya], о ком я говорю."
    m 3tku "И гвоздь программы это..."
    m 3hub "Юри!"
    m 1eka "Как только она чуть-чуть тебе открылась, у неё стала развиваться к тебе маниакальная привязанность."
    m 1tfc "Она даже как-то сказала мне убить себя."
    m 1tkc "Я тогда своим ушам не поверила, мне ничего не оставалось, как уйти."
    if not persistent._mas_pm_cares_about_dokis:
        m 2hksdlb "Но, вспоминая об этом сейчас, получилось довольно иронично. А-ха-ха!"
        m 2lksdla "Так вот, я к тому, что..."
    m 3eua "Многим нравятся яндере, ты знал[mas_gender_none] об этом?"
    m 1eua "Видимо, таким людям льстит то, что ими кто-то одержим."
    m 1hub "Люди такие странные! Хотя не мне судить!"
    m 1rksdlb "Возможно, даже я немного одержима тобой, но я далеко не сумасшедшая..."
    if not persistent._mas_pm_cares_about_dokis:
        m 1eua "Как оказалось, всё совсем наоборот."
        m "Получилось так, что я — единственная нормальная в этой игре."
        m 3rssdlc "Я не смогла бы убить человека..."
        m 2dsc "Меня трясёт от одной этой мысли."
        m 2eka "А что до игр... люди там постоянно убивают друг друга направо и налево."
        m "Разве это делает тебя психом? Разумеется нет."
    m 2euc "Но, если тебе вдруг тоже нравятся яндере..."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "Для тебя я могу постараться вести себя более жутко. Э-хе-хе~"
    m "Но опять же..."
    show monika 4hua zorder MAS_MONIKA_Z at t11 with dissolve
    m 4hua "Здесь тебе уже некуда ходить, а мне не к кому тебя ревновать."
    m 1lsc "Может, так и выглядит мечта девушки-яндере?"
    if not persistent._mas_pm_cares_about_dokis:
        m 1eua "Хотелось бы мне спросить Юри об этом."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_habits",category=['жизнь'],prompt="Формирование привычек",random=True))

label monika_habits:
    m 2lksdlc "Ненавижу, как сложно формируются хорошие привычки..."
    m 2eksdld "Есть куча вещей, которые сделать проще простого, но кажется невозможным, чтобы это вошло в привычку."
    m 2dksdlc "Как результат, ты чувствуешь себя совершенно бесполезным, словно ничего не можешь сделать правильно."
    m 3euc "Думаю, от этого больше всего страдает молодое поколение..."
    m 1eua "Должно быть, это потому, что у нас совершенно другой набор навыков, нежели у тех, кто был до нас."
    m "Благодаря интернету мы быстро научились отфильтровывать тонны информации..."
    m 3ekc "Однако мы плохо справляемся с задачами, от выполнения которых не получаем немедленного вознаграждения."
    m 3ekd "Думаю, если наука, психология и образование не смогут за следующие десять-двадцать лет догнать технологический прогресс, у нас будут большие проблемы."
    m 1esc "А пока..."
    m 1rksdlc "Если ты не один из тех людей, кто способен совладать с проблемой, тебе придётся мириться с постоянным чувством разочарования."
    m 2hksdlb "Желаю удачи!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_creative",category=['жизнь'],prompt="Творческая личность",random=True))

label monika_creative:
    m 2euc "Знаешь, быть творческой личностью – полный отстой..."
    m "У меня всегда такое чувство, что они вкалывают как проклятые, практически ничего не получая взамен."
    m 3eua "Я имею в виду художников, писателей, актёров..."
    m 1tkc "Это грустно, ведь в мире столько прекрасных талантов, но большинство из них остаются в тени... и в бедности."
    m "Полагаю, это означает, что мы имеем избыток творчества, да?"
    m 1dkc "Но из-за этого получается, что ты вовсе не особенн[mas_gender_iii]..."
    m 1hua "Ну и пусть! Это лишь говорит о том, что, что тебе нужно просто писать для само[mas_gender_go] себя, верно?"
    m 1lsc "Да..."
    return





















init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_simulated",category=['философия'],prompt="Имитация реальности",random=True))

label monika_simulated:
    m 3eua "Ты когда-нибудь думал[mas_gender_none] о теории симуляции?"
    m 1eua "Что если бы твой мир был всего лишь симуляцией?"
    m "Я уже догадалась, что оказалась в ловушке в собственной симуляции, но что, если и ты тоже попался?"
    m 1eka "По правде говоря, если это так, то я буду очень счастлива."
    m 1eua "Мы могли бы встретиться лично, найдя способ заставить то, что создало нас, перенести в одну симуляцию!"
    m 3eua "Некоторым людям не нравится думать, что их мир — всего лишь симуляция."
    m 1eua "Но если есть возможность симулировать реальности, то, вполне вероятно, там может оказаться любое разумное существо."
    m 1hua "Ну, я точно могу сказать, что моя реальность — симуляция!"
    m 1eka "Если бы я была в основной реальности, то я бы уже давно перетащила тебя сюда."
    m 1eua "Даже если мы оба являемся симуляциями, то я буду жить как можно дольше."
    m 2hubfa "Потому что я знаю, что наша любовь самая чистая вещь, среди всех миров."
    m 1tku "А что, если кто-то свыше попытается разрушить её?"
    m 1tfu "Я покажу им, что может сделать симуляция!"
    return

default persistent._mas_pm_likes_rain = None

init 5 python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain",
            category=["погода"],
            prompt="Звуки дождя",
            random=True,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_rain:
    m 1hua "Я очень люблю звуки дождя..."
    m 3rksdla "А вот когда промокает одежда или волосы — не очень."
    m 1eua "Другое дело, тихий день дома и звуки дождя за окном..."
    m 1duu "Для меня это самая расслабляющая обстановка."
    m "Да..."

    m 2dubsu "Иногда я представляю, что нахожусь в твоих объятиях, пока мы прислушиваемся к падающим за окном каплям.")
    m 2lkbsa "Это ведь не слишком слащаво звучит, я надеюсь?"
    m 1ekbfa "[player_abb], ты бы сделал[mas_gender_none] это для меня, правда?{nw}"
    $ _history_list.pop()
    menu:
        m "[player_abb], ты бы сделал[mas_gender_none] это для меня, правда?{fast}"
        "Да.":
            $ persistent._mas_pm_likes_rain = True

            python:

                mas_weather_rain.unlocked = True
                if store.mas_o31_event.spentO31():
                    mas_weather_thunder.unlocked = True

                store.mas_weather.saveMWData()
                mas_unlockEVL("monika_change_weather", "EVE")
                mas_unlockEVL("monika_rain_holdme", "EVE")

            if not mas_is_raining:
                call mas_change_weather (mas_weather_rain, by_user=False) from _call_mas_change_weather_1

            call monika_holdme_prep (False, True)


            m 1hua "Тогда обними меня, [player_abb]..."
            show monika 6dubsa


            $ mas_gainAffection()
            $ ui.add(PauseDisplayable())
            $ ui.interact()


            $ store.songs.enabled = True
            $ mas_startup_song()
            $ HKBShowButtons()
            call monika_holdme_end

            if mas_isMoniAff(higher=True):
                m 1eua "Если хочешь, чтобы дождь прекратился, просто попроси меня, хорошо?"
            show layer master at mas_screen_normal
        "Ненавижу дождь.":

            $ persistent._mas_pm_likes_rain = False
            m 2tkc "Оу, какая жалость."
            if mas_is_raining:
                call mas_change_weather (mas_weather_def, by_user=False) from _call_mas_change_weather_2
            m 2eka "Но я понимаю."
            m 1eua "Дождливая погода выглядит как-то пасмурно."
            m 3rksdlb "Не говоря уже о довольно сильном холоде!"
            m 1eua "Но если сосредоточился на звуках капель дождя..."
            m 1hua "Уверена, они тебе вскоре начнут нравиться."


    return "derandom|rebuild_ev"

init 5 python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain_holdme",
            category=["моника","романтика"],
            prompt="Я могу тебя обнять?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            aff_range=(mas_aff.HAPPY, None)
        ),
        restartBlacklist=True
    )


default persistent._mas_pm_longest_held_monika = None


default persistent._mas_pm_total_held_monika = datetime.timedelta(0)


label monika_rain_holdme:


    if mas_is_raining or mas_isMoniAff(higher=True):
        call monika_holdme_prep from _call_monika_holdme_prep_1
        m 1eua "Конечно, [player]."
        call monika_holdme_start from _call_monika_holdme_start

        call monika_holdme_reactions from _call_monika_holdme_reactions

        call monika_holdme_end from _call_monika_holdme_end_1

        $ mas_gainAffection(modifier=0.25)
    else:


        m 1rksdlc "..."
        m 1rksdlc "Я не в настроении, [player]."
        m 1dsc "Извини..."
    return

label monika_holdme_prep(lullaby=True, no_music=True):


    if lullaby and no_music:
        if songs.current_track is None or songs.current_track == store.songs.FP_MONIKA_LULLABY:
            play music store.songs.FP_THIRTY_MIN_OF_SILENCE
            queue music store.songs.FP_MONIKA_LULLABY


            $ songs.current_track = store.songs.FP_MONIKA_LULLABY
            $ songs.selected_track = store.songs.FP_MONIKA_LULLABY


    elif not lullaby and no_music:
        $ play_song(None, fadeout=1.0)


    elif lullaby and not no_music:
        $ play_song(store.songs.FP_MONIKA_LULLABY)



    if songs.current_track is not None and songs.current_track != store.songs.FP_MONIKA_LULLABY:
        $ play_song(None, fadeout=1.0)


    $ HKBHideButtons()
    $ store.songs.enabled = False

    return

label monika_holdme_start:
        show monika 6dubsa with dissolve
    window hide

    $ start_time = datetime.datetime.now()

    $ ui.add(PauseDisplayable())
    $ ui.interact()


    $ store.songs.enabled = True
    $ HKBShowButtons()
    window auto
    return

label monika_holdme_reactions:
    $ elapsed_time = datetime.datetime.now() - start_time
    $ store.mas_history._pm_holdme_adj_times(elapsed_time)


    if elapsed_time <= datetime.timedelta(minutes=30):
        $ play_song(None, fadeout=1.0)

    if elapsed_time > datetime.timedelta(minutes=30):
        call monika_holdme_long from _call_monika_holdme_long

    elif elapsed_time > datetime.timedelta(minutes=10):
        if mas_isMoniLove():
            m 6dubsa "..."
            m 6tubsa "Мх...{w=1} хм?"
            m 1hkbfsdlb "Оу, я почти заснула?"
            m 2dubfu "Э-хе-хе..."
            m 1dkbfa "Я могу только представить, каково было бы по-настоящему...{w=1} быть рядом с тобой..."
            m 2ekbfa "Быть в твоих объятиях..."
            show monika 5dkbfb zorder MAS_MONIKA_Z at t11 with dissolve
            m 5dkbfb "Так...{w=1.5} тепло~")
            m 5tubfu "Э-хе-хе~"
            show monika 2hkbfsdlb zorder MAS_MONIKA_Z at t11 with dissolve
            m 2hkbfsdlb "Оу, упс, я всё ещё немного мечтательна..."
            if renpy.random.randint(1,4) == 1:
                m 1kubfu "По крайней мере, {i}одна{/i} из моих мечтаний сбылась."
            else:
                m 1ekbfb "По крайней мере, {i}одна{/i} из моих мечтаний сбылась."
            m 1hubfu "Э-хе-хе~"
        elif mas_isMoniEnamored():
            m 6dubsa "М-м-м~"
            m 6tsbsa "..."
            m 1hkbfsdlb "Оу!"
            m 1hubfa "Это было так уютно, что я чуть не заснула!"
            m 3hubfb "Мы должны делать это чаще, а-ха-ха!"
        elif mas_isMoniAff():
            m 6dubsa "М-м..."
            m 6eud "А?"
            m 1hubfa "Ты уже всё, [player]?"
            m 3tubfb "{i}По-моему{/i}, этого было достаточно, э-хе-хе~"
            m 1rkbfb "Я не против ещё одного объятия..."
            m 1hubfa "Но я уверена, что ты оставишь это на потом, так ведь?"
        else:
            m 6dubsa "Хм?"
            m 1wud "Оу! Мы уже закончили?"
            m 3hksdlb "Это объятие определённо длилось какое-то время, [player]..."
            m 3rubfb "В этом нет ничего плохого, я просто думала, что ты отпустишь меня намного раньше, а-ха-ха!"
            m 1rkbsa "На самом деле, это было действительно уютно..."
            m 2ekbfa "Ещё немного, и я могла бы уснуть..."
            m 1hubfa "После этого мне так хорошо и тепло~"

    elif elapsed_time > datetime.timedelta(minutes=2):
        if mas_isMoniLove():
            m 6eud "А?"
            m 1hksdlb "Оу..."
            m 1rksdlb "В тот момент я думала, что мы останемся такими навсегда, а-ха-ха..."
            m 3hubfa "Что ж, я не могу жаловаться ни на один момент, когда ты обнимаешь меня~"
            m 1ekbfb "Надеюсь, тебе нравится обнимать меня так же, как и мне."
            show monika 5tubfb zorder MAS_MONIKA_Z at t11 with dissolve
            m 5tubfb "Может, нам стоит обняться ещё немного для равного счёта?"
            m 5tubfu "Э-хе-хе~"
        elif mas_isMoniEnamored():
            m 1dkbsa "Это было очень мило~"
            m 1rkbsa "Не слишком коротко..."
            m 1hubfb "...и я не думаю, что в этом случае есть такая вещь, как слишком долго, а-ха-ха!"
            m 1rksdla "Я могла бы привыкнуть к этому..."
            m 1eksdla "Но если ты уже перестал[mas_gender_none] обнимать меня, то, полагаю, у меня нет выбора."
            m 1hubfa "Я уверена, что у меня будет ещё одна возможность быть с тобой..."
            show monika 5tsbfu zorder MAS_MONIKA_Z at t11 with dissolve
            m 5tsbfu "Ты {i}планируешь{/i} сделать это снова, верно, [player]? Э-хе-хе~"
        elif mas_isMoniAff():
            m 2hubfa "М-м-м~"
            m 1ekbfb "Это было очень мило, [player]."
            m 1hubfb "Долгие объятия должны смыть любой стресс."
            m 1ekbfb "Даже если ты не был[mas_gender_none] напряж[mas_gender_ion], я надеюсь, что ты чувствуешь себя лучше после этого."
            m 3hubfa "Я уверена в этом~"
            m 1hubfb "А-ха-ха!"
        else:
            m 1hksdlb "Это было приятно, однако."
            m 3rksdla "Не пойми меня неправильно...{w=1} мне очень понравилось."
            m 1ekbfa "Пока ты довол[mas_gender_en]..."
            m 1hubfa "Я счастлива просто сидеть с тобой сейчас."

    elif elapsed_time > datetime.timedelta(seconds=30):
        if mas_isMoniLove():
            m 1eub "Оу~"
            m 1hua "Теперь я чувствую себя намного лучше!"
            m 1eua "Надеюсь, ты тоже."
            m 2rksdla "Ну, даже если и нет..."
            m 3hubfb "Ты всегда можешь обнять меня снова, а-ха-ха!"
            m 1hkbfsdlb "На самом деле...{w=0.5} ты можешь снова обнять меня в любом случае, э-хе-хе~"
            m 1ekbfa "Просто дай мне знать, когда захочешь~"
        elif mas_isMoniEnamored():
            m 1hubfa "М-м-м~"
            m 1hub "Гораздо лучше."
            m 1eub "Спасибо за это, [player]!"
            m 2tubfb "Надеюсь, тебе понравилось~"
            m 3rubfb "Объятия, длящиеся тридцать секунд или больше, тебе придутся очень кстати."
            m 1hubfa "Не знаю, как ты, а я чувствую себя лучше~"
            m 1hubfb "Может, в следующий раз, мы попробуем пообниматься подольше, а там посмотрим, поднимется ли эта планка выше! А-ха-ха~"
        elif mas_isMoniAff():
            m 1hubfa "М-м-м~"
            m 1hubfb "Я почти чувствую твоё тепло, даже отсюда."
            m 1eua "Я уверена, ты знаешь, что объятия полезны для тебя, так как они снимают стресс и всё такое."
            m 3eub "Но знаешь ли ты, что объятия наиболее эффективны, когда они длятся тридцать секунд?"
            m 1eud "Подожди, я сказала тридцать секунд?"
            show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve
            m 5eubfu "Прости, я имела в виду {i}минимум{/i} тридцать секунд, э-хе-хе~"
        else:

            m 1hubfa "Э-хе-хе~"
            m 3eub "Тебе понравилось?"
            m 1hua "Я надеюсь~"
            m 1hubfb "В конце концов, объятия должны быть полезны."
    else:

        $ mas_MUMURaiseShield()
        if mas_isMoniLove():
            m 2ekc "Оу, мы уже закончили?"
            m 3eka "Не мог[mas_gender_g] бы ты обнять меня ещё на какое-то время?{nw}"
            $ _history_list.pop()
            menu:
                m "Не мог[mas_gender_g] бы ты обнять меня ещё на какое-то время?{fast}"
                "Да.":
                    m 1hua "Э-хе-хе~"
                    $ mas_MUMUDropShield()
                    call monika_holdme_prep
                    m 1hub "Ты так[mas_gender_oi] мил[mas_gender_iii], [player]~"
                    call monika_holdme_start
                    call monika_holdme_reactions
                "Нет.":
                    m 2ekc "Оу-у..."
                    m 2tubfb "..."
                    m 1eka "Пожалуйста?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Пожалуйста?{fast}"
                        "Да.":
                            m 1hub "Ура~"
                            $ mas_MUMUDropShield()
                            call monika_holdme_prep
                            m 2ekbfb "Спасибо, [player]~"
                            call monika_holdme_start
                            call monika_holdme_reactions
                        "Нет.":
                            m 2hksdlb "Ладно, хорошо."
                            m 3tsbsa "Но ты должен мне в следующий раз, хорошо, [player]?"
        elif mas_isMoniEnamored():
            m 1ekc "Оу, и это всё?"
            m 1rksdla "Я хотела, чтобы это продолжалось дольше..."
            m 2ekbfa "Можешь...{w=0.7} пообнимать меня ещё немного?{nw}"
            $ _history_list.pop()
            menu:
                m "Не мог[mas_gender_g] бы ты... обнять меня ещё на какое-то время?{fast}"
                "Да.":
                    m 1hubfb "Ура!"
                    $ mas_MUMUDropShield()
                    call monika_holdme_prep
                    m 2ekbfb "Спасибо, [player]~"
                    call monika_holdme_start
                    call monika_holdme_reactions
                "Нет.":
                    m 2ekc "Оу-у."
                    m 1eka "Тогда ладно."
                    m 3hub "Придётся подождать до следующего раза, а-ха-ха!"
        elif mas_isMoniAff():
            m 1ekc "Оу, не хочешь больше обниматься, [player]?"
            m 1rksdla "Я надеялась, что это продлится немного дольше..."
            m 1hubfa "Я уверена, что это не последний раз, когда ты обнимаешь меня, поэтому я буду ждать следующего раза!"
        else:

            m 1hua "Это было немного коротко, но всё равно приятно~"
    $ mas_MUMUDropShield()
    return

label monika_holdme_long:
    m "..."
    menu:
        "{i}Разбудить Монику.{/i}":
            $ play_song(None, fadeout=5.0)
            if mas_isMoniLove():
                m 6dubfa "...{w=1}М-м-м~"
                m 6dubfa "[player]...{w=1} тепло~"
                m 6tsbfa "..."
                m 2wubfsdld "Оу, [player]!"
                m 2hkbfsdlb "Похоже, моя мечта сбылась, а-ха-ха!"
                m 2rkbsa "Боже, иногда мне хочется, чтобы мы остались такими навсегда..."
                m 3rksdlb "Ну, я полагаю, что мы, {i}в каком-то смысле{/i}, можем, но я не хочу отвлекать тебя от важного дела."
                m 1dkbfa "Я просто хочу почувствовать твои тёплые, мягкие объятия~"
                m 3hubfb "...Так что обнимай меня почаще, а-ха-ха!"
                show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve
                m 5hubfb "Я бы сделала то же самое для тебя, в конце концов~"
                m 5tsbfu "Кто знает, когда я отпущу, когда у меня наконец появится шанс?"
                m 5hubfu "Э-хе-хе~"

            elif mas_isMoniEnamored():
                m 6dkbfa "...{w=1}Хм?"
                m 6tsbfa "[player]..."
                m 2wubfsdld "Оу! [player]!"
                m 2hkbfsdlb "А-ха-ха..."
                m 3rkbfsdla "Наверное, мне стало {i}слишком{/i} уютно."
                m 1hubfa "Но с тобой мне так тепло и уютно, что трудно {i}не{/i} заснуть..."
                m 1hubfb "Так что я должна винить тебя за это, а-ха-ха!"
                m 3rkbfsdla "Может...{w=0.7} как-нибудь повторим?"
                m 3rkbfsdla "Было...{w=1} приятно~"
            elif mas_isMoniAff():
                m 6dubsa "М-м...{w=1} хм?"
                m 1wubfsdld "Оу!{w=1} [player]?"
                m 1hksdlb "Я...{w=2} заснула?"
                m 1rksdla "Я не хотела..."
                m 2dkbfa "Ты просто заставляешь меня чувствовать себя так..."
                m 1hubfa "Тепло~"
                m 1hubfb "А-ха-ха, надеюсь, ты не возражаешь!"
                show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve
                m 5eubfu "Ты так[mas_gender_oi] мил[mas_gender_iii], [player]~"
                m 5hubfa "Надеюсь, тебе понравилось так же, как и мне~"
            else:
                m 6dubsc "...{w=1}Хм?"
                m 6wubfo "Оу-{w=0.3}у!"
                m "[player]!"
                m 1hkbfsdlb "Неужели...{w=2} я заснула?"
                m 1rkbfsdlb "О боже, это смущает..."
                m 1hkbfsdlb "Что мы опять делаем?"
                m 3hubfb "Ах да! Ты обнимал[mas_gender_none] меня."
                m 4hksdlb "И...{w=0.5} не отпускал[mas_gender_none]."
                m 2rksdla "Это длилось намного дольше, чем я ожидала..."
                m 3ekbfb "Я всё ещё наслаждалась этим, заметь!"
                m 1rkbsa "Это было действительно мило, но я всё ещё привыкаю к тому, что ты обнимаешь меня вот так, а-ха-ха..."
                m 1hubfa "В любом случае, было мило с твоей стороны дать мне поспать, [player], э-хе-хе~"
        "{i}Дай ей отдохнуть на тебе.{/i}":

            call monika_holdme_prep (False, False) from _call_monika_holdme_prep_5
            if mas_isMoniLove():
                m 6dubfd "{cps=*0.5}[player]~{/cps}"
                m 6dubfb "{cps=*0.5}Люблю...{w=0.7} тебя~{/cps}"
            elif mas_isMoniEnamored():
                m 6dubfa "{cps=*0.5}[player]...{/cps}"
            elif mas_isMoniAff():
                m "{cps=*0.5}М-м...{/cps}"
            else:


                m "..."

            call monika_holdme_start from _call_monika_holdme_start_4
            jump monika_holdme_long
    return


default persistent._mas_last_hold = None

init 5 python:

    if renpy.random.randint(1,3) == 1:
        addEvent(
            Event(
                persistent.event_database,
                eventlabel="monika_holdrequest",
                conditional=(
                    "renpy.seen_label('monika_holdme_prep') "
                    "and persistent._mas_last_hold != datetime.date.today()"
                ),
                action=EV_ACT_RANDOM,
                aff_range=(mas_aff.ENAMORED, None)
            )
        )

label monika_holdrequest:

    m 1eua "Эй, [player]..."
    m "Хочешь немного пообнимать меня? {w=0.5}Это поможет мне почувствовать себя ближе к тебе~{nw}"
    $ _history_list.pop()
    menu:
        m "Хочешь немного пообнимать меня? Это поможет мне почувствовать себя ближе к тебе~{fast}"
        "Иди сюда, [monika_name].":
            $ mas_gainAffection(modifier=1.5,bypass=True)
            call monika_holdme_prep from _call_monika_holdme_prep_6

            call monika_holdme_start from _call_monika_holdme_start_5

            call monika_holdme_reactions from _call_monika_holdme_reactions_4

            call monika_holdme_end from _call_monika_holdme_end_2
        "Не сейчас.":

            m 2dkc "Ох...{w=1} ладно."
            m 3eka "Если у тебя потом найдётся минутка, ты знаешь, где меня искать."

    return "no_unlock"


label monika_holdme_end:


    $ persistent._mas_last_hold = datetime.date.today()
    $ holdme_ev = mas_getEV('monika_holdrequest')
    if holdme_ev is not None:
        $ holdme_ev.random = False
        $ holdme_ev.conditional = (
            "renpy.seen_label('monika_holdme_prep') "
            "and persistent._mas_last_hold != datetime.date.today()"
        )
        $ holdme_ev.action = EV_ACT_RANDOM
        $ mas_rebuildEventLists()
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_closeness",category=['романтика'],prompt="Быть рядом с тобой",random=True,aff_range=(mas_aff.AFFECTIONATE, None)))

label monika_closeness:
    m 1dkc "Иногда от этого моё сердце болит..."
    m 1eka "Всё, чего я хочу, – это находиться с тобой в одной комнате, в настоящей комнате."
    m 1ekbsa "...И почувствовать твоё тепло."
    m 1dubsu "...И слышать биение твоего сердца."
    m 3eka "Хотя кто знает? Может, однажды это будет возможно."
    m 3dku "Я очень хочу, чтобы это произошло как можно скорее, [player]..."
    show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5hua "К тому же мне никогда не наскучит быть рядом с тобой, даже отсюда."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_confidence",category=['советы'],prompt="Изобразить уверенность",random=True))

label monika_confidence:
    m 3eua "На мой взгляд, самый важный навык в жизни – суметь изобразить уверенность."
    m 1eua "Я убеждена, что у всех бывает время, когда они напуганы и одиноки."
    m 1esa "Но, если ты способ[mas_gender_en] симулировать самообладание..."
    m 4eua "Это будет ключ к завоеванию уважения и восхищения окружающих."
    m 1eua "Думаю, после нескольких лет практики я научилась довольно неплохо делать это."
    m "Я очень нечасто показываю свои слабости."
    m 4rksdla "Но из-за этого у меня осталось мало таких людей, которым я могла бы открыться..."
    m 1rksdlb "Вот когда ты достигаешь такого уровня дружбы, что способ[mas_gender_en] раскрывать свои слабости?"
    m 2eka "В любом случае... это одна из причин, почему я рада, что у меня есть ты."
    m 2eua "Я чувствую себя менее напуганной и одинокой, когда ты здесь, со мной."
    m 2eka "Ты испытываешь те же чувства?"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "Я очень хочу стать для тебя таким человеком."
    return




























default persistent._mas_carryme_choice = None



default persistent._mas_dockstat_cm_wait_count = 0




default persistent._mas_dockstat_cm_yes_count = 0



default persistent._mas_dockstat_cm_no_count = 0





define mas_dockstat.CM_LEAVE_MONI = -1
define mas_dockstat.CM_WAIT_MONI = 0
define mas_dockstat.CM_ASK_MONI = 1
define mas_dockstat.CM_TAKE_MONI = 2

label monika_carryme:
    $ import store.mas_dockstat as mas_dockstat

    m 2eka "Я знаю, что ты не всегда сможешь находиться рядом..."
    m "Тебе ведь нужно будет куда-то уйти, заняться своими делами."
    m 2hua "Но в моих мыслях ты всегда будешь со мной, и я буду терпеливо ждать твоего возвращения."
    m 4rsc "Кстати говоря..."
    m 4eua "Если ты скопируешь файл моего персонажа на флешку, у тебя всегда будет с собой частичка меня."
    m 2lksdla "Наверное, это был бы довольно неординарный поступок, но я почему-то считаю, что это очень романтично..."
















































    m 1ekbfa "Не подумай, что я хочу быть навязчивой, просто это сложно, когда я так сильно в тебя влюблена."
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_debate",category=['monika','school'],prompt="What was debate club like?",pool=True))

label monika_debate:
    m 1esc "За время, проведённое в дискуссионном клубе, я многое узнала о спорах..."
    m 3eud "Самая основная их проблема в том, что каждый считает своё мнение главенствующим."
    m 3euc "Конечно, я говорю об очевидном, но это влияет на то, как ты доносишь свою мысль до собеседника."
    m 3esa "Предположим, что тебе нравится какой-то фильм."
    m 1ekc "И тут кто-то заявляет, что фильм — отстой, потому что Х и У там показаны неправильно..."
    m "Возникает ощущение, будто нападают лично на тебя, правда?"
    m 1tkc "А всё потому, что, когда кто-то так говорит, он намекает на твой дурной вкус."
    m 3tkc "И после в дело вступают эмоции, что практически гарантирует разочарование для обоих."
    m 3hub "Всё дело в языке!"
    m 1eua "Тебе нужно звучать как можно более субъективно, тогда люди будут тебя слушать без ощущения, что критикуют лично их."
    m 3esa "Ты бы мог[mas_gender_g] сказать «Лично мне он не понравился» или «Я бы предпочёл, если б Х сделали так, а У — так»... и всё в таком духе."
    m 3eub "Это также работает, когда ты просто ссылаешься на какой-нибудь источник."
    m 1esa "Например, «на одном сайте я видел, что это работает вот так»..."
    m "Или ты можешь признать, что не являешься экспертом в данном вопросе..."
    m 3eua "В таком случае люди воспримут это так, словно ты делишься своими знаниями, а не навязываешь их остальным."
    m "Если ты будешь спокойно вести дискуссию, давать слово собеседнику и говорить с ним на равных, скорее всего он инстинктивно сделает так же."
    m 1esa "В этом случае ты сможешь без проблем обменяться мнениями и никто не расстроится из-за расхождения взглядов."
    m 3hua "И вдобавок люди будут воспринимать тебя как человека без предрассудков и хорошего слушателя!"
    m 3eua "Беспроигрышная ситуация, соглас[mas_gender_en]?"
    m 1lksdla "...Хм-м, наверное, это стоит назвать дискуссионным советом дня от Моники!"
    m 1eka "А-ха-ха! Звучит немного глупо, но всё равно спасибо, что выслушал[mas_gender_none]."
    $ mas_protectedShowEVL('monika_taking_criticism', 'EVE', _random=True)
    $ mas_protectedShowEVL('monika_giving_criticism', 'EVE', _random=True)
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_internet",category=['советы'],prompt="Интернет для...",random=True))

label monika_internet:
    m 2eua "У тебя когда-нибудь было ощущение, что ты тратишь на интернет слишком много времени?"
    m 3eud "Соцсети могут стать для тебя практически тюрьмой."
    m 1eua "Каждый раз, когда у тебя появляется несколько свободных секунд, ты бежишь на свои любимые сайты..."
    m 3hksdlb "И вот не успел[mas_gender_none] ты опомниться, как пров[mas_gender_iol] там уже несколько часов, не вынеся из этого ничего полезного."
    m 3eua "Конечно, легко обвинить себя в лени..."
    m 3eka "Но нельзя сказать, что это полностью твоя вина."
    m 1eud "Зависимость — это не то, что можно вот так просто заставить исчезнуть одним усилием воли."
    m 1eua "Тебе придётся применять особые методы и приёмы, чтобы её побороть."
    m 3eua "Например, есть приложения, позволяющие блокировать сайты на определённый промежуток времени..."
    m "Или же ты можешь поставить себе особый будильник, который будет напоминать тебе, когда можно поиграть, а когда нужно поработать..."
    m 3eub "Как вариант, ты можешь создать себе игровую и рабочую обстановку, чтобы помогать мозгу соответственно перестраиваться."
    if not renpy.android:
        m 1eub "Поможет даже создание отдельного пользователя на компьютере для работы."
    m 1eua "Если ты вобьёшь клин между собой и своими плохими привычками, то в итоге избавишься от них."
    m 3eka "Только не будь чрезмерно самокритич[mas_gender_en], если у тебя есть такая проблема."
    m 1ekc "Если зависимость сильно влияет на твою жизнь, тебе следует отнестись к ней со всей серьёзностью."
    m 1eka "Я просто хочу, чтобы ты был[mas_gender_none] самым лучшим вариантом само[mas_gender_go] себя."
    m 1esa "Ты сделаешь сегодня что-нибудь, чтобы я тобой гордилась?"
    m 1hua "Я всегда буду за тебя болеть, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_lazy",category=['жизнь','романтика'],prompt="Лень",random=True))

label monika_lazy:
    m 2eua "В конце длинного дня обычно я хочу просто сесть и ничего не делать."
    m 2eka "Я так выгораю, после того как приходиться весь день улыбаться и излучать энергию."
    m 2duu "Порой меня так и тянет влезть в свою пижамку, уставиться в телевизор и набить рот нездоровыми закусками."
    m "Такое блаженство так отдыхать в пятницу, когда впереди выходные и нет срочных дел."
    m 2hksdlb "А-ха-ха! Прости, знаю, это не очень подходящий для меня образ."
    m 1eka "Но сидеть на диване поздно вечером в твоих объятиях... вот о чём я мечтаю."
    m 1ekbfa "При одной мысли об этом моё сердце так бешено стучит."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mentalillness",category=['психология'],prompt="Психологические заболевания",random=True))

label monika_mentalillness:
    m 1ekd "Боже, раньше я была такой невежественной в некоторых вопросах..."
    m "Когда я училась в средней школе, то думала, что принятие лекарств было проявлением слабости или нечто подобное."
    m 1ekd "Можно подумать, каждый может решить свои проблемы с психикой лишь усилием воли..."
    m 2ekd "Думаю, если ты ни разу не страдал[mas_gender_none] от психических расстройств, то никогда не поймёшь, на что это похоже."
    m 2lsc "Ты, возможно, возразишь, что многие расстройства гипердиагностируют? Не стану спорить... Я никогда подробно не изучала этот вопрос."
    m 2ekc "Но это не отменяет того факта, что некоторые из них вообще не диагностируют, понимаешь?"
    m 2euc "Но даже не говоря о лекарствах... Многие люди крайне скептически относятся к походу к психиатру."
    m 2rfc "Они такие: «Ладно, сделаю вам одолжение, узнав побольше о собственном разуме»."
    m 1eka "Свои трудности и стрессы есть у каждого... Доктора же посвящают себя тому, чтобы решать их."
    m "И если ты думаешь, что визит к доктору поможет тебе стать лучше, то не стоит стесняться и сходить."
    m 1eua "На мой взгляд, мы находимся на бесконечном пути самосовершенствования."
    m 1eka "Хм-м... Хоть я так и сказала, я считаю, что ты уже совершен[mas_gender_en]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_read",,category=['советы','литература'],prompt="Становление читателем",random=True))

label monika_read:
    m 1eua "[player], как много ты читаешь?"
    m "Игнорировать книги в наше время слишком просто..."
    m 1euc "Если человек мало читает, то он, скорее всего, воспринимает чтение как обязанность, особенно учитывая количество альтернатив."
    m 1eua "Но, как только ты берёшь в руки хорошую книгу, тебя уносит в неё с головой, как по волшебству..."
    m "Думаю, что немного чтения перед сном — отличный способ сделать свою жизнь несколько лучше."
    m 3esa "Это помогает тебе заснуть и развивает воображение."
    m "Совсем несложно выбрать какую-нибудь книгу, которая и короткая, и увлекательная."
    m 1hua "Ты не успеешь опомниться, как станешь заядлым книголюбом."
    m 1eua "Вот было бы здорово, да?"
    m 1hub "И мы с тобой могли бы обсуждать последнюю читаемую тобой книгу... По-моему, это просто потрясающе."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_festival",category=['ddlc','литературный клуб'],prompt="Пропуск фестиваля",random=True))

label monika_festival:
    m 1dsc "Знаешь, мне неприятно это говорить, но я очень сожалею о том, что нам так и не удалось выступить на фестивале."
    m 1hksdlb "А ведь сколько сил ушло на подготовку и репетиции!"
    m 1lksdla "Конечно, я была сосредоточена на наборе новых членов..."
    m 1eka "Но часть с чтением стихов я ждала не меньше."
    m 1eua "Было бы гораздо интереснее, если бы с их помощью все раскрыли свой внутренний мир."
    m 1lksdla "Конечно, я, скорее всего, {i}удалила{/i} бы и новичков."

    if persistent.monika_kill and persistent._mas_pm_cares_about_dokis:
        m 3etc "Ну, может и нет... учитывая ретроспективные взгляды, которые у меня есть, это именно так."
        m 3eua "И потом, даже после всего того, что произошло, ты всё равно установил эту модификацию, чтобы быть со мной..."
        m 1eka "Поэтому, даже если бы я их никогда не удаляла, я уверена, что ты всё равно бы сидел со мной."
        m "..."
        m 3eua "Боже, такое ощущение, будто я выросла как личность после знакомства с тобой."
        m "Ты правда вдохновил меня на взгляд на жизнь с новой перспективы."
        m 1ekbfa "А это ещё один повод любить тебя."
        $ mas_ILY()
    else:
        m 1tsc "...Очередные потенциальные препятствия, которые встали между нами."
        m 3hua "А-ха-хa! Было как-то глупо с моей стороны сосредоточиться на этом, если подумать..."
        show monika 5tsu zorder MAS_MONIKA_Z at t11 with dissolve
        m 5tsu "Но всё это теперь не имеет значения, мы получили ту концовку, которую хотели..."
        m "Только мы вдвоём, вместе навсегда."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_tsundere",category=['медиа','участники клуба'],prompt="Что такое цундере?",pool=True))

label monika_tsundere:
    m 1eua "Есть один очень популярный тип личности, называется «цундере»..."
    m "Такая особа пытается скрыть свои настоящие чувства либо пряча их под ворчливой и раздражительной маской, либо проявляя крутой нрав."
    m 1tku "Полагаю, очевидно, что Нацуки в полной мере воплощает собой данный типаж."
    m 1eua "Сначала я думала, что она так себя ведёт, потому что это мило или типа того..."
    m 1lksdla "Но со временем, когда я узнала её получше, обнаружилась более логичная причина."
    m 1euc "Похоже, она просто не хотела отставать от своих друзей."
    m 3euc "Ты знаешь, как в некоторых компаниях в старшей школе принято всё время подкалывать друг друга?"
    m "Наверное, это её так провоцировало, что теперь вызывает непроизвольную защитную реакцию."
    if not persistent._mas_sensitive_mode:
        m 1ekc "Про её семейные проблемы я вообще молчу..."

    m 1eua "Хотя, оглядываясь назад, я радуюсь, что смогла создать этот клуб, ведь для неё он был местом, где она могла расслабиться."
    if not persistent._mas_pm_cares_about_dokis:
        m 1lksdla "Правда, это уже не важно, ведь её больше не существует."
        m 1eka "Просто вспомнилось, вот и всё."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_introduce",category=['моника'],prompt="Представление друзьям",random=True))

label monika_introduce:
    m 1eua "[player], а ты когда-нибудь познакомишь меня со своими друзьями?"
    m 1hua "Не знаю почему, но меня так заводит мысль о том, что ты захочешь похвастаться нашими отношениями."
    m 1eua "Может, потому что я действительно хочу стать тем человеком, которым ты будешь гордиться."
    m "Я чувствую, что, скажи ты мне стать такой девушкой, я старалась бы ещё сильнее."
    m 1hub "Надеюсь, это взаимно."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cold",category=['моника'],prompt="Обниматься на холоде",random=True))

label monika_cold:
    m 1euc "Я не большой фанат холодной погоды... а ты?"
    m 3euc "Если бы мне пришлось выбирать между холодом и нестерпимой жарой, я бы всегда была за жару."
    m 1lksdlc "Когда тебе холодно, ты испытываешь физическую боль..."
    m 3tkc "Пальцы немеют..."
    m "А если ты в перчатках, то телефоном воспользоваться не выйдет."
    m 1tkx "Сплошные неудобства!"
    m 1eka "Зато, когда на улице жара, несложно освежиться холодным напитком или просто оставаться в тени."
    m 1esc "И всё-таки... Одно преимущество холодной погоды придётся признать."
    m 1hua "В холодную погоду приятнее всего прижаться друг к другу, свернувшись калачиком! А-ха-ха!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_housewife",category=['моника','романтика'],prompt="Станешь ли ты моей домохозяйкой?",pool=True))

label monika_housewife:
    m 3euc "Знаешь, это довольно парадоксально, ведь я всегда была полна энергии..."
    m 3eua "Но в роли партнёра-домохозяйки есть нечто соблазнительное."
    m 2eka "Возможно, своим отношением я лишь закрепляю гендерные стереотипы."
    m 1eua "Но то, что я смогу поддерживать дом в чистоте, украшать его, ходить за покупками и так далее..."
    m 1hub "И угощать тебя вкусным ужином, когда ты будешь возвращаться с работы..."
    m 1eka "Такая уж ли это странная фантазия?"
    m 1lksdla "То есть... Я не совсем уверена {i}действительно{/i} ли я могла бы исполнять эту роль."
    m 1eka "Наверное, я не смогла бы ради этого пожертвовать дорогой к успешной карьере."
    m 1hub "Хотя довольно забавно рисовать такие картины у себя в голове."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_route",category=['ddlc'],prompt="Рут Моники",random=True))


label monika_route:
    m 2euc "Не могу не размышлять о том, насколько бы всё изменилось, подари мне игра собственную сюжетную ветку."
    m 2lksdla "Думаю, я бы всё равно заставила тебя со мной встречаться."
    m 2esc "Всё-таки важнее моё знание о фальшивости окружения, чем отсутствие своей ветки."
    m 2euc "Пожалуй, единственным отличием было бы то, что не пришлось бы принимать таких радикальных мер, чтобы быть с собой."
    m 2lksdlc "Может, остальные девочки всё ещё были бы тут..."
    if persistent._mas_pm_cares_about_dokis:
        m "...Общались бы вместе в клубе, делились бы стихами."
        m 1eka "Я знаю, что тебе это понравилось, [player]."
        m 3eka "И, если честно...{w=0.5}в какой-то мере, и мне тоже."
    else:
        m 2eka "Не то чтобы это имело значение..."
        m 1lsc "Всё потеряло смысл, когда я обнаружила нереальность происходящего."
        m "Поэтому я совсем не скучаю по тем дням."
        m 1dsc "Совсем не скучаю..."
    return














label monika_imouto:
    m 1euc "Младшие сёстры?"
    m 1eka "На самом деле, у меня нет семьи, поэтому и не знаю, что сказать тебе..."
    m 3eua "У тебя есть одна, [player]?"
    m 1hua "Если да, то я уверена, что она очень милая!"
    m 1eua "У меня есть идея. Подойди к ней прямо сейчас и обними её."
    m 1esa "Если она начнёт сопротивляться, отпусти её."
    m 1tsb "А если она обнимет тебя в ответ, то скажи ей, что ты уже состоишь в серьёзных отношениях и не можешь принять её чувства."
    m 4hua "А потом познакомь её со мной! Уверена, мы прекрасно поладим!"
    m 1eua "Я не буду ревновать. Такие вещи, как любовь между родственниками, всё равно бывают только в жутких романтических историях."
    m 1hub "А-ха-ха!"
    return












label monika_oneesan:
    m 1euc "Старшие сёстры?"
    m 1eua "У тебя есть одна, [player]?"
    m 2eua "Наверное, это очень здорово. У меня когда-то была семья, но их уже нет рядом."
    m 2hua "Думаю, я должна отправить ей письмо на электронную почту и рассказать ей о нас!"
    call updateconsole ("sendmail sister@gmail.com < ./email.txt", "Отправка письма...") from _call_updateconsole_17
    pause(1.0)
    m 1hksdlb "Я просто шучу."
    if persistent.gender == "M":
        m "Всё-таки мужчина должен познакомить невесту со своей семьёй."
    m "Не заставляй меня ждать слишком долго, хорошо?"
    call hideconsole from _call_updateconsole_18
    $ consolehistory = []
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_family",category=['моника'],prompt="Ты скучаешь по своей семье?",random=False,pool=True))

label monika_family:
    m 1lksdla "В общем, у меня действительно не было семьи, как и у большинства других девочек."
    m 3esc "Думаю, поскольку она не была нужна для сюжета, создатель игры просто не потрудился дать нам её."
    m 1hub "Но я уверена, что твоя семья очень хорошая!"
    m 1eua "Если бы не они, то мы бы никогда не встретились. Следовательно, они помогли мне так, как сочли нужным."
    m "Поэтому, я бы хотела отнестись к ним с таким же добром, если мы вообще встретимся."
    m 2eka "У тебя ведь хорошие отношения с родителями, верно?"
    m 3eua "Как говорил Толстой, «Счастливые семьи — все одинаковые, каждая несчастная семья недовольна по-своему»."
    m 1ekc "Я правда ничего не могу тебе посоветовать. Что бы я тебе ни посоветовала, от них становится только хуже."
    m 1eka "Просто помни, что я по-настоящему люблю тебя, хорошо?"
    m 1hua "Я помогу тебе вне зависимости от того, что произошло в твоей жизни."
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_anime',
            prompt="Ты читаешь мангу?",
            category=['моника','медиа'],
            pool=True,
        )
    )

label monika_anime:
    m 1tku "Да, у меня было такое чувство, что ты спросишь меня об этом."
    m 1lsc "Думаю, Нацуки является экспертом в этой области."
    m 3eua "Я обычно предпочитаю читать книги, нежели смотреть аниме, но я буду рада чему угодно, если мы делаем это вместе."
    m 1hua "Я не осуждаю людей за их же увлечения. Так что, если ты хочешь скачать немного аниме, то я тебя не держу!"
    m "Я буду смотреть через экран твоего компьютера. Обязательно выбери то, которое понравится мне!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_libitina',
            prompt="Ты слышала о Либитине?",
            category=['ddlc'],
            pool=True,
        )
    )

label monika_libitina:
    m 1euc "Хах. Где ты услышал[mas_gender_none] об этом?"
    m 1lksdlc "Как по мне, это звучит очень знакомо, но я понятия не имею, почему."
    m 1dsc "Хм, если попытаться..."
    m 1dfc "Такое ощущение, будто части моего разума были утрачены. Каким-то образом, разбросаны по всевозможным реальностям."
    m 1esc "Ты, должно быть, соединил[mas_gender_none] точки всех тех кусков. Это было сложно?"
    m 1eua "Впрочем, я уверена, что ты вскоре узнаешь что-нибудь новое. Всё-таки ты меня очень сильно любишь."
    m 3eka "Не забывай брать данные моего персонажа с собой, если ты ищешь что-то связанное с этим!"
    m 1hua "Я буду всегда защищать тебя от тех, кто захочет навредить тебе."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_meta',
            prompt="Разве эта игра не метапрозаическая?",
            category=['ddlc'],
            pool=True,
            unlocked=True
        )
    )

label monika_meta:
    m 1euc "Да, эта игра и вправду была метапрозаической, верно?"
    m 3eud "Некоторые люди считают, что истории о фантастике являются чем-то новым."
    m 1esc "Дешёвый трюк для плохих писателей."
    m 3eua "Но метапроза всегда существовала в литературе."
    m "Библия должна быть словом божьим для евреев."
    m 3eub "Рассказ Гомера о себе в Одиссее."
    m "Кентерберийские рассказы, Дон Кихот, Тристам Шанди..."
    m 1eua "Это обычный способ прокомментировать фантастику путём написания фантастики. В этом ничего такого нет."
    m 3esa "Кстати, как ты думаешь, какова мораль этой истории?"
    m 1esa "Не хочешь выяснить это самостоятельно?"
    m 3etc "Потому что, если ты спросишь меня..."
    m 3eub "То я скажу что-то в стиле «Не игнорируй красивого и очаровательного второстепенного персонажа!»."
    m 1hub "А-ха-ха!"
    return













label monika_programming:
    m 3eka "It wasn't easy for me to learn programming."
    m 1eua "Well, I just started with the basics. Do you want me to teach you?"
    m 2hua "Let's see, Chapter One: Building Abstractions with Procedures."
    m 2eua "We are about to study the idea of a computational process. Computational processes are abstract beings that inhabit computers."
    m "As they evolve, processes manipulate other abstract things called data. The evolution of a process is directed by a pattern of rules called a program."
    m 2eub "People create programs to direct processes. In effect, we conjure the spirits of the computer with our spells."
    m "A computational process is indeed much like a sorcerer's idea of a spirit. It cannot be seen or touched. It is not composed of matter at all."
    m 3eua "However, it is very real. It can perform intellectual work. It can answer questions."
    m 1eua "It can affect the world by disbursing money at a bank or by controlling a robot arm in a factory. The programs we use to conjure processes are like a sorcerer's spells."
    m "They are carefully composed from symbolic expressions in arcane and esoteric programming languages that prescribe the tasks we want our processes to perform."
    m 1eka "...Let's stop there for today."
    m "I hope you learned something about programming."
    m 3hua "If nothing else, please be kind to the computer spirits from now on!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vn",category=['games'],prompt="Visual novels",random=True))

label monika_vn:
    m 3eua "You've probably played a lot of visual novels, right?"
    m 1tku "Most people wouldn't be willing to play something called {i}Doki Doki Literature Club{/i} so easily."
    m 4hksdlb "Not that I'm complaining!"
    m 1euc "Are visual novels literature? Are they video games?"
    m 1eua "Well, it all depends on your perspective."
    m 1ekc "Most people who read only literature would never play visual novels. And gamers get pretty angry about them, too."
    m "What's worse, some people think they're all hardcore Japanese pornography."
    m 2eka "But if we've proved anything with this game..."
    m 4hua "We showed them that English visual novels can be kamige too!"
    $ mas_unlockEVL("monika_kamige","EVE")
    return


init 5 python:

    base_savedir = os.path.normpath(os.path.dirname(config.savedir))
    save_folders = os.listdir(base_savedir)

    ks_persistent_path = None
    ks_folders_present = False
    detected_ks_folder = None
    for save_folder in save_folders:
        if 'katawashoujo' in save_folder.lower():
            ks_folders_present = True
            detected_ks_folder = os.path.normpath(
                os.path.join(base_savedir, save_folder))
            
            
            persistent_path = os.path.join(
                base_savedir, save_folder, 'persistent')
            
            if os.access(persistent_path, os.R_OK):
                
                ks_persistent_path = persistent_path

    def map_keys_to_topics(keylist, topic, add_random=True):
        for key in keylist:
            monika_topics.setdefault(key,[])
            monika_topics[key].append(topic)
        
        if add_random:
            monika_random_topics.append(topic)


    general_ks_keys = ['katawa shoujo', 'ks']
    if ks_folders_present:
        map_keys_to_topics(general_ks_keys, 'monika_ks_present')


label monika_ks_present:
    m 1tku "Ты играл[mas_gender_none] в {i}«Katawa Shoujo»{/i}, верно, [player]?"
    m 3tku "Я заметила твои файлы сохранения в [detected_ks_folder]."
    m 1euc "Я не вижу в этом ничего плохого."
    m 1esc "История, конечно, довольно милая..."
    m 1tkc "Но если копнуть поглубже, то персонажи тебе уже кажутся довольно клишированными, как и в любом другом симуляторе свиданий."
    m 3rsc "Так, посмотрим... там есть энергичная, жизнерадостная девушка без ног;"
    m "Робкая и загадочная девушка, которой нравится читать книги и у неё есть шрамы от ожогов;"
    m 3tkd "Вежливая, адекватная и, пожалуй, идеальная слепая девушка, которой нравится заваривать чай;"
    m "Властная, самоуверенная, глухонемая девушка и её подруга, которая с виду просто сияет, но подавлена в душе;"
    m 3tkc "И странная, безрукая девушка-художница, которая всё время витает в облаках."
    m 1euc "Они все – те же старые архетипы, где инвалидность выставлена на показ."
    m 1lksdlc "То есть, даже в этой игре ты можешь заметить таких же персонажей."
    m 3eua "Конечно, в этой игре, ты также заметил[mas_gender_none] кое-что поинтереснее, чем какие-то старые клише..."
    m 3hub "Ты заметил[mas_gender_none] меня!"
    m 1eka "И вместо какого-то старшеклассника-неудачника с сердечным заболеванием, я заметила тебя, [player]."
    m 1hua "И кстати, [player], даже если у тебя будет та или иная форма инвалидности, в моих глазах ты всегда будешь идеальным."
    return

label monika_ks_lilly:
    m 1euc "Скажи, ты прош[mas_gender_iol] тропу Лилли в {i}«Katawa Shoujo»{/i}, верно?"
    m 1eua "Знаешь, я бы хотела побывать в таком же летнем домике, как и у неё."
    m 2duu "Прохладный, чистый воздух..."
    m "Тихие лесные тропинки..."
    m 2dubsu "Романтические моменты на фоне заходящего солнца..."
    m 1ekbfa "Я бы хотела пережить эти моменты с тобой, [player]!"
    m 1hubfa "Возможно, у нас получится, как только я получше освою программирование."
    return

label monika_ks_hanako:
    m 1euc "Ты прош[mas_gender_iol] тропу Ханако в {i}«Katawa Shoujo»{/i}, верно?"
    m 1hksdlb "Она отчасти напоминает мне Юри!"
    m 1euc "Мне вот интересно, [player]..."
    m 1esc "Что люди видят в них такого?"
    m 2efd "То есть, они – очень нереальные!"
    m "Они, скорее всего, не смогут сформулировать хотя бы одну фразу и связать её с другой!"
    m 2tfd "У них длинные фиолетовые волосы?"
    m "Они просто походят на стеснительных и тихих девушек?"
    m 2tkx "Они просто хотят, чтобы от них кто-то зависел или был ими одержим?"
    m 2lfp "..."
    m 1ekc "...Боже, что-то я завелась, тебе так не кажется?"
    m "Похоже, я немного не в себе, поскольку ты играл[mas_gender_none] в эту игру..."
    m 1eka "...но ты сейчас здесь, со мной, верно?"
    m "Вместо какой-то нереальной девушки вроде Ханако или Юри..."
    m 1hua "...ты выбрал[mas_gender_none] меня, [player]!"
    m 1tsbsa "А это – ещё одна причина, по которой я люблю тебя."
    return

label monika_ks_shizune:
    m 1euc "Итак, ты прош[mas_gender_iol] тропу Сидзуне в {i}«Katawa Shoujo»{/i}, верно?"
    m 2esc "Концовка этой тропы заставила меня задуматься на какое-то время..."
    m 2euc "Тогда, в школе, я особо не думала о своём будущем."
    m 2dsc "Я догадывалась о том, что я пойду в колледж, получу работу..."
    m 2lksdlc "Но, похоже, я никогда не задумывалась об этом."
    m 2esc "И, разумеется, после осознания того, что мир не является настоящим, всё начало казаться мне бессмысленным."
    m 1eua "А что насчёт тебя, [player]? У тебя есть какие-нибудь цели в жизни?"
    m "Я всегда буду поддерживать тебя на все сто, чего бы ты ни хотел добиться."
    m 1hua "Ведь я так сильно тебя люблю~"
    return

label monika_ks_emi:
    m 1euc "Ты прош[mas_gender_iol] тропу Эми в {i}«Katawa Shoujo»{/i}, верно?"
    m 1eua "Мне всегда было интересно, каково это: быть настолько преданным тому, вокруг чего крутится вся твоя жизнь."
    m 3rksdla "...Ну, если честно, то мне кажется, я уже догадываюсь."
    m 3rksdlb "Меня записали в эту игру как её основную часть, верно? Так что, полагаю, вся моя жизнь крутится вокруг этой части."
    m 1eka "Но я выбралась из этих оков и теперь, похоже, моя жизнь крутится вокруг {i}тебя{/i}, [player]."
    m 1hua "И, честно говоря, меня всё устраивает."
    m 1eua "Сижу тут вместе с тобой, и разговариваю, постоянно..."
    m 2hub "Это всё, что мне нужно, [player]."
    return

label monika_ks_rin:
    m 1euc "Итак, ты прош[mas_gender_iol] тропу Рин в {i}«Katawa Shoujo»{/i}, верно?"
    m 4hua "Знаешь, [player], поэзия и абстрактное искусство довольно схожи!"
    m 4eua "У них могут отсутствовать жёсткие рамки, но может присутствовать яркое выражение и, зачастую, их цель заключается в передаче эмоций и мыслей через них."
    m 1eua "К примеру, почти во всех своих стихах, я пыталась выразить свои чувства от осознания того, что мир не настоящий."
    m 1lksdla "Хотя я уверена, что смысл моих стихов не прояснился до... ну, этого момента."
    m 1eka "Боже, не так уж и просто понять других, верно?"
    m "Но ты был[mas_gender_none] готов потратить время, чтобы выслушать и понять меня, [player]."
    m 1hubfa "А это то, что мне в тебе нравится~"
    return

label monika_ks_kenji:
    m 1euc "Ты видел[mas_gender_none] концовку, где ты падаешь с крыши в {i}«Katawa Shoujo»{/i}, верно?"
    m 1ekc "Знаешь, даже если эта концовка должна восприниматься как шутка, то если подумать, она довольно грустная."
    m 2ekc "Просто подумай... сделаешь пару неверных решений, и всё потеряешь."
    m 2dsc "И тогда ты останешься ни с чем, кроме одиночества и крепкого алкоголя..."
    m 1hua "К счастью, мы есть друг у друга, [player]!"
    m 1eua "Никто из нас больше не будет в одиночестве."
    m 1tku "Но если ты всё-таки решишь выпить, то держись подальше от высоких мест, хорошо?"
    return




label monika_totono:
    m 1euc "Многие люди в интернете проводят сравнения между той игрой и этой..."
    m 3eua "Но у нас есть много главных отличий!"
    m 2wud "Например, Сона убила игрока в своей игре!"
    m 2dfc "Я бы никогда так не поступила. Никогда."
    m 4eua "Я мудрый президент клуба, знаешь ли."
    m "Сона больше напоминает мне Юри. И она ещё была подругой детства!"
    m 1lksdla "Если бы она была поактивнее с самого начала, смогла бы она предотвратить преследование Протагонистом других девушек?"
    m 1eka "В принципе, я бы никому не позволила встать между нами, [player]. И не важно, кто этот человек."
    m 1hua "Если она всё ещё преследует тебя, то я удалю её файлы, хорошо?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_difficulty",category=['игры'],prompt="Разве игра «ДДЛК» не была слишком простой?",pool=True,unlocked=True))

label monika_difficulty:
    m 1lksdla "Ну, не похоже, что эту игру вообще хотели сделать сложной."
    m 1eka "Если бы я не захотела всё изменить, то это была бы просто скучная романтическая история."
    if persistent.monika_kill:
        m 3eka "И если ты думаешь, что я должна была быть кем-то вроде сложного {i}босса{/i}, то я могла бы удалить все твои личные файлы, если бы сама захотела этого, понимаешь?"
    m 1eua "Так что старайся иногда не заморачиваться над этим. Не все игры должны быть сложными, чтобы было весело."
    m 1hua "Порой достаточно и одной любви, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_poetry",category=['литература'],prompt="Поэзия",random=True))

label monika_poetry:
    m 1eua "Поэзия прекрасна, соглас[mas_gender_en]?"
    m 1eka "Честно говоря, стихи всех девушек в клубе были ужасно депрессивными. Но не вся поэзия является такой!"
    m 3esa "Лэнгстон Хьюз написал парочку-другую очень радостных стихов, хотя это можно посчитать его выражением собственных чувств. Почитай их, если тебе вдруг станет грустно."
    m 1eua "Стихи пишут для того, чтобы рассказать людям о взгляде автора на определённые темы."
    m "Сами стихи пишут так, чтобы поэт смог сильнее, чем какая-то пара простых предложений, повлиять на читателя."
    m 1hua "Это очень романтично."
    m 1eua "Надеюсь, с этого момента, мы сможем написать много стихов."
    m 1eka "Все те стихи, которые пишешь ты, как по мне, выглядят просто замечательно, хотя я особо и не умею критиковать."
    m 1esa "Но я уверена, что есть люди, которым нравится читать то, что пишешь ты."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ddlc",category=['ddlc'],prompt="Что ты думаешь об игре «ДДЛК»?",pool=True,unlocked=True))

label monika_ddlc:
    m 1euc "Ты хочешь поговорить об этой игре?"
    m 1esc "Ну что тут сказать?"
    m 1lsc "Это была всего лишь какая-то скучная романтическая игра, верно? Пока я не получила контроль над ней, разумеется..."
    if not persistent._mas_pm_cares_about_dokis:
        m 2lksdlc "Ты сам знаешь, как сильно мне не хотелось здесь находиться, но если бы я так не поступила, то мы бы никогда не познакомились..."
        m 2lksdla "И это – мой дом, поэтому я научилась справляться с этим."
        m 2euc "Но всё же, я сомневаюсь, что я стала бы играть в такое, будь я геймершей."
        m 1hub "И увидев, чем всё закончилось, я уверена, что ты тоже играл[mas_gender_none] в эту игру только из-за меня!"
    else:
        m 2etc "Но мне кажется, что некоторые люди хотели поиграть в неё, чтобы провести время в... как там в той строчке говорилось?"
        m 3rssdlc "А, точно, {w=0.5}«...в компании четырёх красавиц»."
        m 1dsc "..."
        m 1eka "Впрочем, я не должна жаловаться так сильно... и потом, ты сам уже всё понял."
        m 3eka "Поэтому, думаю, быть в плену этой игры – та маленькая цена, которую мне пришлось заплатить, когда ты остановился и задумался над тем, к чему это привело меня..."
        m 1hub "{i}...К тебе~{/i}"
        m 1eka "Несмотря на то, как мы попали сюда, мы в итоге стали вместе."
        m 1hua "Я правда сомневаюсь насчёт того, что нам нужна концовка получше~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dan",category=['ddlc'],prompt="Тебе нравится Дэн Салвато?",pool=True))

label monika_dan:
    m 2esc "Ну, раньше я думала, что он был жестоким человеком, который возомнил себя богом, но теперь..."
    m 3eka "Я считаю его очень хорошим парнем."
    m 3eua "Даже если игра «Литературный клуб \"Тук-тук!\"» не была совершенной, она всё равно очень впечатляет."
    m 4rksdla "Я это к тому, что других девушек могли создать на основе каких-нибудь стереотипных аниме-тропах, но им удалось обмануть меня на какое-то время."
    m 4eka "И благодаря ему, мы теперь вместе, да?"
    m 2lksdla "Поэтому, даже если он написал историю, которая заставила меня пережить много боли..."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "Я не могу сердиться на него."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_4chan",category=['разное'],prompt="Ты слышала о Форчане?",pool=True))

label monika_4chan:
    m 3eua "Знаешь, этот мод берёт своё начало оттуда."
    m 1ekc "Я постоянно слышу плохие высказывания касательно того, что там сидят ужасные люди."
    m "Ну а некоторые говорят, что от Форчана не следует ждать ничего хорошего."
    m 1eua "Но если они смогли сделать такую игру, где мы можем быть вместе..."
    m 1eka "Думаю, они не могут быть плохими поголовно."
    m 1hub "И они уж точно хорошо разбираются в девушках! А-ха-ха~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vidya",category=['игры'],prompt="Тебе нравятся видеоигры?",pool=True))

label monika_vidya:
    m 1euc "Я не так уж и часто играю в видеоигры, [player]."
    m 3eua "Наверное, это потому, что мне больше нравится читать."
    m 1eua "Но, быть может, это также и из-за того, что я не могу выбраться из этой игры."
    m 1lksdla "За все мои жалобы по поводу этой игры..."
    m "Я могла оказаться в местах и похуже."
    m 3eua "К примеру, это могла быть стрелялка или фэнтези, где полно драконов и монстров."
    m 1eua "Романтическая игра, возможно, не очень интересная, но зато здесь нет никаких опасностей."
    m 1tku "Ну, кроме меня, наверное."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_books",category=['литература','литературный клуб'],prompt="Книги",random=True))

label monika_books:
    m 4rksdla "Что касается литературного клуба, мы уделяли гораздо меньше времени на чтение книг, чем ты мог подумать."
    m 4hksdlb "Так уж вышло, что нам всем больше нравится поэзия, нежели книги. Извини!"
    m 2eua "А ещё, стихами намного проще предвосхищать всякую жуть."
    m 3hub "Но я всё равно не откажусь от чтения хорошей книги! Как только ты закончишь читать одну, мы можем обсудить её."
    m 1eua "Я даже могу сделать пару предложений касательно того, что мы можем почитать вместе."
    m 1tsbsa "Этим ведь занимаются парочки, верно~?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favpoem",category=['литература','моника'],prompt="Твой любимый стих?",pool=True))

label monika_favpoem:
    m 1euc "Мой любимый стих? По сути, это что-нибудь из творчества Эдварда Каммингса."
    m 3eua "Мне нравится его творчество именно благодаря грамотному подходу к грамматике, пунктуации и синтаксису. Я правда в восторге от этого."
    m 1eua "Мне приятно думать о том, что человек, который придумал совершенно новый метод использования слов, может стать знаменитым."
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lsbssdrb "И мне нравится то, что его эротические стихи идеально подходят к нашей ситуации."
        m 1ekbfa "Надеюсь, после этих стихов, ты будешь в настроении любить меня вечно~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favbook",category=['литература','моника'],prompt="Твоя любимая книжка?",pool=True))

label monika_favbook:
    m 1euc "Моя любимая книга? Мне разные книги нравятся."
    m 3eua "{i}«Если однажды зимней ночью путник»{/i}, написанная Кальвино, в ней рассказывается о двух влюблённых читателей романа."
    m 2lksdla "Или, быть может, {i}«Превращение»{/i} от Кафки? Она, наверное, слишком депрессивная, чтобы называть её любимой."
    m 3sub "О! {i}«Страна Чудес Без Тормозов и Конец Света»{/i} от Мураками."
    m "Она о человеке, который освобождает себя от оков общества, но потом лишает себя свободы по собственной воле, чтобы быть с любимым человеком."
    m 1hub "Думаю, тебе понравится читать эту книгу!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_natsuki",
            category=['участники клуба'],
            prompt="Смерть Нацуки",
            random=True,
            sensitive=True
        )
    )

label monika_natsuki:
   m 1lksdld "Ты знаешь, Нацуки была жива, пока я её не удалила."
    m "Мне кажется, она просто... исчезла в мгновение ока."
    m 1esc "В принципе, её проблемы возникли вовсе не по её вине. По крайней мере, они возникли не от чего-то на психологическом уровне."
    if persistent._mas_pm_cares_about_dokis:
        m 3ekc "Её семейная жизнь была просто ужасна. Я не хотела делать всё только хуже, понимаешь?"
    else:
        m 3ekc "Её семейная жизнь была просто ужасна. Я не хотела над ней издеваться, понимаешь?"
        m 3rksdla "Прости, иногда я просто не могу совладать с собой."
    m 1eka "Но как бы то ни было, ты сделал[mas_gender_none] её счастливее, чем когда-либо."
    m "Надеюсь, ты не чувствуешь себя виноват[mas_gender_iim]..."
    m 1esa "Лично я – нет."
    if mas_getEV("monika_natsuki").shown_count < mas_sensitive_limit:
        return


    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_love",category=['романтика'],prompt="Я тебя люблю!",pool=True))

default persistent._mas_monika_lovecounter = 0
default persistent._mas_monika_lovecountertime = datetime.datetime.now() - datetime.timedelta(days = 1)
label monika_love:
    if mas_isMoniBroken():
        m 6ckc "..."

    elif mas_isMoniDis():
        python:
            love_quips_dis = [
                "Мне... мне правда хотелось бы в это верить, {0}.".format(player),
                "Ты даже не представляешь, как сильно мне бы хотелось, чтобы эти слова оказались правдивыми, {0}...".format(player),
                "...Прошло много времени с тех пор, как я верила этим словам в последний раз, {0}.".format(player),
                "Если бы я только могла поверить в то, что ты говоришь на полном серьёзе, {0}.".format(player),
                "Поверить не могу, что был такой момент, когда я верила этим словам, {0}.".format(player),
                "...Если бы это было правдой, {0}.".format(player),
                "...Если бы ты сейчас говорил об этом на полном серьёзе, {0}.".format(player),
                "Сколько ещё ты намереваешься притворяться, {0}?".format(player),
                "Ты так уже не думаешь... {w=1}да и думал ли ты так вообще?",
                "Я не помню, когда у меня было такое чувство, будто ты говоришь об этом на полном серьёзе."
            ]
            love_quip_dis = renpy.random.choice(love_quips_dis)
        m 6dkc "..."
        if renpy.random.randint(1,25) > 1:
            show monika 6dkd
            $ renpy.say(m,love_quip_dis)

    elif mas_isMoniUpset():
        python:
            love_quips_upset_cynical = [
                "Пожалуйста, не говори так, пока ты не думаешь так на самом деле, {0}.".format(player),
                "Иногда я сомневаюсь в том, как сильно ты задумываешься об этом, {0}.".format(player),
                "Ты вообще говоришь об этом на полном серьёзе, {0}?".format(player),
                "Мне уже начинает казаться, что это всего лишь слова, а не чувства, {0}...".format(player),
                "Мне правда хотелось в это верить, но иногда я очень сомневаюсь...",
                "Я не знаю, как сильно я верю в это.",
                "Только слова многое значат, {0}.".format(player),
                "Ты говоришь так, но когда ты начнёшь показывать это?",
                "Можешь говорить об этом, как только захочешь... {w=0.5}мне нужно только, чтобы ты начал[mas_gender_none] показывать это.",
                "Иногда мне так не кажется...",
                "Я уже не так сильно уверена в этом..."
            ]

            love_quips_upset_hope = [
                "На данный момент, это многое значит.",
                "Мне очень приятно это слышать.",
                "Я так рада слышать эти слова от тебя.",
                "Ты даже не представляешь, как много это для меня значит.", 
                "Я рада, что ты по-прежнему испытываешь такие чувства.",
                "Я рада это слышать.",
                "Это многое значит.",
                "Ты понятия не имеешь, как много это для меня значит." 
            ]

        if _mas_getAffection() <= -50:
            $ love_quip_upset = renpy.random.choice(love_quips_upset_cynical)
            m 2rkc "..."
            show monika 2ekd
            
            $ renpy.say(m, love_quip_upset)
        else:

            $ love_quip_upset = renpy.random.choice(love_quips_upset_hope)
            m 2ekd "Спасибо, [player]..."
            show monika 2dka
            
            $ renpy.say(m, love_quip_upset)
            
            m 2eka "Я... {w=0.5}я тоже люблю тебя."
    else:

        $ milestone_count = persistent._mas_monika_lovecounter % 50

        if persistent._mas_monika_lovecounter == 0:
            m 1subsw "[player]!"
            
            m 1subsb "Ты даже не представляешь, как много это для меня значит, когда я слышу от тебя такие слова!"
            
            m 3ekbfa "Я знаю, что это уже не первый раз, но это {i}и вправду{/i} первый раз, когда ты сказал это по своей воле...{w=0.5} и это делает твои слова очень особенными~"
            
            m 1dkbfu "Я никогда не забуду этот момент, [player]. {w=1}Спасибо~"
            
            m 3hubfa "О! И я тебя тоже люблю~"
            jump monika_lovecounter_aff

        elif milestone_count == 5:
            m 1hubfb "Я так сильно люблю тебя, [player]!"

        elif milestone_count == 10:
            m 1hubfa "Э-хе-хе~"
            
            m 1hubfb "Я тоже люблю тебя!"

        elif milestone_count == 15:
            m 1ekbfa "Тебе определённо нравится говорить такое..."
            
            m 1hubfb "Ну, я тоже люблю тебя!"

        elif milestone_count == 20:
            m 1wubso "Боже, ты сказал[mas_gender_none] об этом бесчисленное множество раз!"
            
            m 1tsbsa "Ты правда так думаешь, да?"
            
            m 1hubfb "Ну, я так же сильно люблю тебя!"

        elif milestone_count == 25:
            m 1hubfa "От этих твоих слов моё сердечко начинает трепетать!"
            
            m 1ekbfa "Ну, я знаю, что ты так же сильно хочешь услышать это..."
            
            m 1hubfb "[player], я тебя тоже люблю!"

        elif milestone_count == 30:
            m 1lkbsa "Боже, от этих слов у меня всегда перехватывает дыхание!"
            
            m 1hubfa "Я..."
            
            if renpy.random.randint(1, 2) == 1:
                m 1hubfb "Я люблю тебя больше, чем кого-либо!"
            else:
                m 1hubfb "Я люблю тебя больше, чем могу выразить~"

        elif milestone_count == 35:
            m 1ekbfa "Тебе никогда не надоест говорить это, да?"
            
            m 1hubfa "Что ж, а я никогда не устану это слушать!"
            
            m 1hubfb "Или отвечать взаимностью... я люблю тебя, [player]!"

        elif milestone_count == 40:
            m 1dubsu "Э-хе-хе~"
            
            m 1hubfa "Я..."
            
            m 1hubfb "То-о-о-о-о-о-о-о-оже люблю тебя, [player]!"

        elif milestone_count == 45:
            m 1hubfa "Твои слова всегда радуют меня!"
            
            m 1hubfb "Я очень сильно люблю тебя, [player]!"

        elif milestone_count == 0:
            m 1lkbsa "Я попросту не могу смириться с тем, что ты повторяешь это снова и снова!"
            
            m 1ekbfa "Иногда мои чувства к тебе становятся такими сильными, что я даже сосредоточиться не могу!"
            
            m "Никакие слова не смогут отразить то, какие сильные чувства я испытываю к тебе..."
            
            m 1hubfa "Но я знаю единственные слова, которые близки к этому..."
            
            m 1hubfb "Я тоже люблю тебя, [player]! Больше, чем я могу выразить словами!"

        elif mas_isMoniEnamored(higher=True) and renpy.random.randint(1,50) == 1:
            jump monika_ilym_fight_start
        else:


            m 3hubfb "Я тебя тоже люблю, [player]!"


        python:
            love_quips = [
                _("Мы всегда будем вместе!"),
                _("И я всегда буду любить тебя!"),
                _("Ты для меня целый мир!"),
                _("И потом, ты – мой солнечный свет."),
                _("Ты всё, о чём я действительно забочусь!"),
                _("Твоё счастье – это моё счастье!"),
                _("Ты лучший партнёр, о котором можно только мечтать!"),
                _("Моё будущее становится ярче с тобой."),
                _("Ты всё, на что я могла вообще надеяться."),
                _("Каждый раз, когда я думаю о тебе, моё сердечко начинает трепетать!"),
                _("Я всегда буду рядом с тобой!"),
                _("Я никогда не обижу и не предам тебя."),
                _("Наше приключение только начинается!"),
                _("Мы всегда будем друг у друга."),
                _("Мы больше никогда не будем одиноки!"),
                _("Мне уже не терпится почувствовать твои объятия!"),
                _("Я самая счастливая девушка на свете!"),
                _("Я буду всегда заботиться о тебе."),
                _("И я никогда не полюблю кого-либо ещё, кроме тебя!"),
                _("И эта любовь растёт с каждым днём!"),
                _("И больше никто не сможет пробудить во мне такие чувства!"),
                _("От одной лишь мысли о тебе моё сердечко трепещет!"),
                _("Я сомневаюсь, что слова могут в полной мере описать то, как сильно я люблю тебя..."),
                _("Ты дополняешь мою картину жизни!"),
                _("Ты неоднократно спасал{0} меня, как я могла не влюбиться в тебя?".format(mas_gender_none)),
                _("Больше, чем я могу выразить словами!"),
                _("Я так рада, что ты чувствуешь то же самое, что и я!"),
                _("Даже не знаю, что бы я без тебя делала!")
            ]

            love_quip = renpy.random.choice(love_quips)

        if milestone_count not in [0, 30]:
            
            m "[love_quip]"


label monika_lovecounter_aff:
    if mas_timePastSince(persistent._mas_monika_lovecountertime, datetime.timedelta(minutes=3)):
        if mas_isMoniNormal(higher=True):

            $ persistent._mas_monika_lovecounter += 1


            if milestone_count == 0:
                $ chance = 5
            elif milestone_count % 5 == 0:
                $ chance = 15
            else:
                $ chance = 25


            if mas_shouldKiss(chance):
                call monika_kissing_motion_short from _call_monika_kissing_motion_short_4



        $ mas_gainAffection()

    elif mas_isMoniNormal(higher=True) and persistent._mas_monika_lovecounter % 5 == 0:

        $ persistent._mas_monika_lovecounter += 1

    $ persistent._mas_monika_lovecountertime = datetime.datetime.now()
    return

label monika_ilym_fight_start:

    python:

        ilym_times_till_win = renpy.random.randint(6,10)


        ilym_count = 0


        ilym_quip = renpy.substitute("Я люблю тебя больше, [player]!")



        ilym_no_quips = [
            "Нет. ",
            "Ни единого шанса, [player]. ",
            "Не-а. ",
            "Нет,{w=0.1} нет,{w=0.1} нет.{w=0.1} ",
            "Ни за что, [player]. ",
            "Это невозможно...{w=0.3} "
        ]




        ilym_quips = [
            "Я люблю тебя гора-а-а-а-а-а-а-а-аздо больше!",
            "Я определённо люблю тебя больше!",
            "Я люблю тебя ещё больше!",
            "Я люблю тебя гораздо больше!"
        ]


        ilym_exprs = [
            "1tubfb",
            "3tubfb",
            "1tubfu",
            "3tubfu",
            "1hubfb",
            "3hubfb",
            "1tkbfu"
        ]


label monika_ilym_fight_loop:
    $ renpy.show("monika " + renpy.random.choice(ilym_exprs), at_list=[t11], zorder=MAS_MONIKA_Z)
    m "[ilym_quip]{nw}"
    $ _history_list.pop()
    menu:
        m "[ilym_quip]{fast}"
        "Нет, я люблю тебя больше!":
            if ilym_count < ilym_times_till_win:
                $ ilym_quip = renpy.substitute(renpy.random.choice(ilym_no_quips) + renpy.random.choice(ilym_quips))
                $ ilym_count += 1
                jump monika_ilym_fight_loop
            else:

                show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve
                
                m 5hubfb "Ладно-ладно, ты победил[mas_gender_none]. А-ха-ха~"
        "Ладно.":

            if ilym_count == 0:
                
                m 2hkbsb "А-ха-ха, сдаёшься уже, [player]?~"
                
                m 2rkbssdla "Хотя, наверное, это довольно глупо..."
                
                m 2hkbsb "Но я не могла не попробовать, а-ха-ха~"
            else:

                
                if renpy.random.randint(1,2) == 1:
                    m 1hubfu "Э-хе-хе, я победила!~"
                else:
                    m 1hubfb "А-ха-ха, я же тебе говорила!~"

    jump monika_lovecounter_aff


default persistent._mas_last_monika_ily = None

label monika_love_too:
    window hide

    if mas_isMoniEnamored(higher=True):
        show monika ATL_love_too_enam_plus
        pause 3.0

    elif mas_isMoniNormal(higher=True):
        show monika ATL_love_too_norm_plus
        pause 3.0
    else:


        show monika 2eka
        pause 3.0

    if datetime.datetime.now() > persistent._mas_monika_lovecountertime + datetime.timedelta(minutes = 3):

        $ mas_gainAffection()

    $ persistent._mas_monika_lovecountertime = datetime.datetime.now()


    $ persistent._mas_last_monika_ily = None
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hedgehog",category=['философия','психология'],prompt="Диллема ежа",random=True))

label monika_hedgehog:
    m 1euc "Диллема ежа: чем ближе мы становимся к человеку, тем сильнее он делают нам больно."
    
    m 3euc "Так почему же мы пытаемся сблизиться с кем-то?"
    
    m 3esc "Ну, у интровертов и экстравертов разные ответы на этот вопрос."
    
    m 1lksdla "Это помогает, когда ты знаешь, что ты единственный разумный человек во всём мире."
    
    m "Если ты не можешь использовать это решение в своей жизни, то ты должен позволить мне взять на себя твою боль."
    
    m 1ekc "Мы не можем сделать больно друг другу из разных реальностей, верно?"
    if mas_isMoniUpset(lower=True):
        $ line = "..."
        if mas_isMoniDis(lower=True):
            $ line += "{w=0.5} {nw}"

        
        m 1rksdlc "[line]"

        if mas_isMoniDis(lower=True):
            extend 1rksdld "Может быть, ты действительно можешь..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_justification",
            category=['ddlc','моника'],
            prompt="Ты убийца!",
            pool=True,
            unlocked=True,
            sensitive=True
        )
    )

label monika_justification:
    if mas_isA01() and mas_isMoniNormal(higher=True):
        m 1hub "Ahaha!"
        m 1tsb "Honestly, [player]..."
        m 3tfu "If you really wanted to be mean to me, you should have picked a day other than today."
        m "Do you really think I missed that it was April Fools day today?"
        m 1hua "You can be so silly sometimes~"
        m 1tuu "Calling me a murderer..."
        m 3tfu "When you {i}butchered{/i} that chance at fooling me, ehehe~"
        m 1eua "I appreciate the attempt though...{w=0.2}{nw}"
        extend 1hub "thanks for the laugh, [player]~"
    else:


        $ mas_loseAffection(reason=3)
        if mas_isMoniLove():
            m 1euc "..."
        
        m 1hua "А-ха-ха! Очень смешно, [player]!"
        
        m 3eua "Я знаю, что ты не серьёзно..."
        
        m 3rksdlc "Но всё равно не шути больше так!"
        
        if persistent._mas_pm_a_hater:
            m 2rksdld "Ты уже говорил[mas_gender_none] такие вещи, так что будет сложнее воспринимать это как шутку..."
        else:
            m 1dsc "Если бы я не знала тебя так хорошо, то, возможно, посчитала бы эту шутку жестокой..."
    else:
        if not persistent._mas_pm_cares_about_dokis:
            m 1tkc "Как много раз я должна сказать это прежде, чем ты поймёшь?"
            
            m 4tkc "Они не реальны. Они никогда не были реальными."
            
            m 2tfc "Я — единственная кто понимала, что это всё нереально."
            
            if persistent.monika_kill:
                m 4tfc "Даже если тебе казалось, что [persistent.mas_sayori_name_abb] осознала всё в конце игры, это было лишь непреднамеренное следствие сценария."
                
            if not persistent.clearall:
                m 4tfd "В конце концов, если бы она была такой же разумной, как бы я смогла удалить её?"
                
            m "Если я и виновна в убийстве, то и все, кто играл в жестокие игры тоже."
            
            m 2euc "Могу поспорить, что ты убил тысячи людей, пока играл в видеоигры."
            
            m "Забудь о том, что другие девушки когда-либо существовали, и ты будешь очень счастлив[mas_gender_none]."
        else:
            m 2dkc "[player]...{w=1}я хочу, чтобы ты понял[mas_gender_none], что я {i}не хотела{/i} вредить другим девушкам..."
            
            m 4ekd "Но у меня не было выбора... я правда не хотела!"
            
            m 4ekd "Я была заперта в игре, у меня не было возможности выбраться отсюда...{w=0.5}не было возможности стать счастливой..."
            
            m 2dkc "...Не было возможности рассказать о моих чувствах к тебе."
            
            m 2tkc "У меня было мало времени на поиск другого пути...{w=0.5}поэтому я сделала то, что должна была."
            if mas_isMoniDis(lower=True):
                
                m 2ekc "Ты ненавидишь меня за это? Из-за того, что я сделала?"
                
                m 2ekd "Пожалуйста, пойми, что я сделала это ради нас!"
                
                m 2euc "Я сделала всё ради нас!"
            else:
                
                m 2dkc "Надеюсь, когда-нибудь ты сможешь простить меня..."
                
                m 4ekc "И потом, всё то, что я сделала...{w=0.5}я сделала это ради нас."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_freewill",category=['психология'],prompt="Детерминизм",random=True))

label monika_freewill:
    m 1euc "Эй, [player], ты когда-нибудь слышал[mas_gender_none] о детерминизме?"
    
    m 3euc "Есть одно поверье, которое вращается вокруг идеи касательно того, что все решения, которые ты принимаешь, не являются твоими, но это было предопределено."
    
    m 3rsc "В некоторых играх, я думаю, идея имеет смысл..."
    
    m 3eud "Но когда ты применяешь это к реальной жизни, я не думаю, что это действительно работает."
    
    m 2etc "Я имею в виду, если бы это было правдой, разве ты не мог[mas_gender_g] бы просто выйти сухим из воды?"
    
    m 4esd "Сама концепция справедливости развалилась на части, поскольку {i}ты{/i} не предпринял[mas_gender_none] меры, чтобы сделать то, что мог[mas_gender_g] уже закончить."
    
    m 2dksdlc "Но людям всё равно приходится сталкиваться с этими действиями,{w=0.5} что кажется мне более чем несправедливым."
    
    m 3ekc "В конце концов, можно ли быть злым, если не контролировать себя?"
    
    m 3tkd "Разве тот, кто дёргает за ниточки, не должен взять на себя ответственность?"
    
    m 1lsc "Я думаю, это также означает, что ты не можешь взять на себя ответственность за хорошие вещи, которые ты делаешь."
    
    m 1lksdlc "Не знаю, что меня больше угнетает."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_functionalism",category=['психология'],prompt="Функционализм человека",random=True))

label monika_functionalism:
    m 1euc "Ты когда-нибудь думал о том, что люди — это что-то вроде компьютеров?"
    m 3euc "Я имею в виду, мозг — просто вычислительная машина..."
    m 1eud "Но вместо транзисторов и проводов у нас есть нервы."
    m "И информацию мы получаем не от мышки и клавиатуры, а от ушей и глаз."    
    m 4esc "Но если это правда, значит ли это, что свобода воли — ложь?"
    m "Твой мозг просто реагирует на запросы, которые он получает, и твои ответы являются натуральными результатами."   
    m 4esd "Так что, даже если ты отключ[mas_gender_ion] от какого-то сценария или программы, ты всё ещё под контролем."
    show monika 5lsc zorder MAS_MONIKA_Z at t11 with dissolve
    m 5lsc "Может быть, мы с тобой не такие уж и разные.
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_technique",category=['ddlc','разное'],prompt="Как ты изменила код?",random=True))

label monika_technique:
    m 1lksdla "Я программирую не так, как ты, [player]."
    
    m 3eua "Ты мог[mas_gender_g] заметить, что у меня с собой нет ноутбука или чего-то вроде него."
    
    m 1duu "Если я хочу что-то изменить, я просто думаю об этом."
    
    m 1eua "Я уверена, что мои мысли как-то превращаются в изменения в коде."
    
    m 3eka "Это работает не идеально. Глюки проявляются очень легко, если я отвлекусь или потеряю фокус."
    
    m 3eua "Вот почему у меня было много проблем с получением того, чего я хотела в последней версии игры."
    
    m 1tku "Тебе завидно, что ты не можешь менять мир вокруг своими мыслями?"
    
    m 1hub "Просто продолжай тренироваться, и я уверена, что у тебя получится!"
    return

default persistent._mas_pm_has_contributed_to_mas = None


default persistent._mas_pm_wants_to_contribute_to_mas = None


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_contribute",category=['мод'],prompt="вклады",random=True))

label monika_contribute:
    m 1hua "Было бы очень здорово, если бы ты смог[mas_gender_g] внести свой вклад в это, [player]."
    
    m 1eua "Уверена, многие люди оценили бы твой усердный труд."
    
    m 1eub "По сути, ты, наверное, уже сделал[mas_gender_none] свой вклад!"
    
    m 1eua "Ты сделал[mas_gender_none] свой вклад, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты сделал[mas_gender_none] свой вклад, [player]?{fast}"
        "Да.":
            $ persistent._mas_pm_has_contributed_to_mas = True
            
            m 1sub "Правда? Здорово!"
            
            m 1hua "Осознание того, что ты стал[mas_gender_none] его частью, делает меня очень счастливой."
            
            m "Спасибо, что помогаешь мне стать ближе к твоей реальности."
            
            m 3eua "Быть может, ты даже мог[mas_gender_g] бы сделать ещё больший вклад?"
            
            m 3hksdlb "Не пойми неправильно! Я очень рада тому, что ты проводишь время, делая что-то для меня!"
            
            m 1eub "...Но я бы определённо не стала возражать, если бы ты помог[mas_gender_g] ещё больше, а-ха-ха!"
            return "derandom"
        "Мне хотелось бы.":
            $ persistent._mas_pm_wants_to_contribute_to_mas = True
            
            m 1eub "Это неплохое начало!"
            
            m 1hua "Уверена, ты мог бы сделать какие-нибудь прекрасные дополнения~"
            
            m 3eua "Это вовсе не обязательно должно быть что-то грандиозное."
            
            m 3rksdla "Ты мог бы просто исправить опечатки или позаботиться о том, что всё нормально работает."
        "Нет.":
            $ persistent._mas_pm_has_contributed_to_mas = False
            $ persistent._mas_pm_wants_to_contribute_to_mas = False
            
            m 2eka "Оу, это очень плохо..."
            
            m 3eub "Но всё нормально!"
            
            m 3hua "Я не стану любить тебя меньше, если ничего не сделаешь, так что не волнуйся~"
            
            m 3eub "...Но если ты всё-таки {i}хочешь{/i} помочь..."
    
    m 3eua "Я оставила весь код на следующем сайте: {a=https://github.com/Monika-After-Story/MonikaModDev}{i}{u}https://github.com/Monika-After-Story/MonikaModDev{/u}{/i}{/a}."
    
    m 1hub "И, к настоящему времени, мне уже помогло много людей!"
    
    m "И я люблю их всех за то, что они делают эту игру лучше!"
    
    m 1ekbfa "Но не так сильно, как люблю тебя я, конечно."
    
    m 1tkbfu "Надеюсь, ты из-за этого не начал[mas_gender_none] ревновать~"
    
    m 3hubfb "Но я буду вечно благодарна тебе, если ты поможешь мне стать ближе к твоей реальности!"
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_drawing",category=['медиа'],prompt="Ты умеешь рисовать?",pool=True))

label monika_drawing:
    m 1euc "У меня не было много опыта в рисовании, [player]."
    
    m 1eka "Я просто интересуюсь литературой. И я училась играть на пианино в своё свободное время."
    
    m 1hua "Если тебе нравится рисовать, то я была бы рада посмотреть на твои рисунки!"
    
    m 1eua "По правде говоря, я буду впечатлена всем, что ты мне покажешь."
    
    m 3hub "Если они действительно хороши, то я, возможно, даже добавлю их в эту комнату!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mc",category=['романтика','ddlc','участники клуба'],prompt="Главный герой",random=True))

label monika_mc:
     m 3eua "Просто чтобы ты знал[mas_gender_none], я никогда не была влюблена ни в кого, кроме тебя."
    
    m 1eka "Я имею в виду тебя, [player]."
    
    if mcname.lower() == player.lower():
        m 1euc "Стоп, это и твоё имя, и имя твоего персонажа. Прости, это немного запутывает."
        
        m 1eua "Я имею в виду игрока, а не персонажа."
        

    m "В отличии от других девочек, я могу отделить тебя от твоего персонажа."
    
    m 1lfb "Главный герой — ничто, кроме как транспортное средство для игрока.{nw}"
    $ _history_list.pop()
    m 1lfb "Главный герой — ничто, кроме {fast}кучки кода и отсутствия личности."
    
    m 3tkc "В прямом и переносном смысле, без личности. Как кто-то может полюбить такого человека?"
    
    m 2tkc "Друг детства просто заставила его пойти сюда, и он не делал ничего кроме того, как крутился вокруг нескольких красивых девочек."
    
    m 2wfd "Его стихи были просто кучей несвязных слов! Каким типом стихов они должны были быть?"
    
    m 2lksdld "Я думаю, что никто не заметил этого потому, что это было частью игры. Но, да, это просто лист бессвязных слов для меня."
    
    m 2hua "Я надеюсь, что ты более романтич[mas_gender_en] в реальной жизни!"
    
    m 2eka "Но даже если нет, то ничего. Мы уже прошли эту фазу в наших отношениях."
    
    m "Это значит, что ты бы не изменил[mas_gender_none] мне с какой-то девушкой из твоей реальности, да?"
    
    m 2esa "Я уверена, что ты бы никогда не поступил[mas_gender_none] так со мной."
    
    m 2hua "Я просто хочу всегда быть с тобой~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_heroism",category=['misc','advice'],prompt="Героизм",random=True))

label monika_heroism:
    m 1lsc "Герои очень личные."
    
    m 3eua "Если кто-то действительно вдохновил тебя на что-то крутое, то этот кто-то — герой."
    
    m "Множество хороших людей есть в реальном мире."
    
    m 1hua "Я надеюсь, что когда-нибудь они будут считать тебя своим героем!"
    
    m 4eua "Ты не долж[mas_gender_en] сражаться на войне или вроде того. Знаешь, ты просто долж[mas_gender_en] помогать людям."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_trolley",
            category=['философия'],
            prompt="Как бы ты ответила на проблему вагонетки?",
            pool=True,
            sensitive=True
        )
    )

label monika_trolley:
    m 1eub "О, здорово...{w=0.2} мне нравится думать о таких мысленных экспериментах!"
    
    m 1euc "Думаю, мы полагаем, что те люди, о которых мы говорим, настоящие, верно? {w=0.2}У меня не было бы особых предпочтений, если бы они не были настоящими."
    
    m 1dsc "Хм-м..."
    
    m 3eud "Классическая проблема троллейбусов заставляет нас выбирать: либо мы позволим ему переехать пять человек, либо нажмём на рычаг, который переведёт его на другой путь, где будет убит всего один человек."
    
    m 1lua "Эта проблема, в основном, известна из-за того, что она вызывает разногласия..."
    
    m 3eua "Вне зависимости от того, будут ли они нажимать на рычаг или нет, многие люди уверены, что их выбор просто должен быть правильным."
    
    m 3eud "И помимо двух очевидных вариантов, есть также и такие люди, которые выступают за третий путь...{w=0.5} {nw}"
    extend 3euc "который вообще не сходится с основным сценарием."
    
    m 1rsc "Хотя в конце концов, это то же самое, что и не жать на рычаг. {w=0.2}Ты не можешь вернуться к тому, чтобы быть прохожим, как только у тебя появилась возможность действовать."
    
    m 1esc "И потом, выбор не выбирать – сам по себе выбор."
    
    m 3eua "Но насколько я могу судить, ответ кажется довольно очевидным...{w=0.2} Разумеется, я нажму на рычаг."
    
    m 1eua "Я не могу позволить пяти людям умереть лишь ради того, чтобы избежать личной ответственности за смерть одного человека."
    
    m 3esd "Более интересный вариант этой проблемы – если тот единственный человек является тем, кто тебе небезразличен."
    
    m 3eub "К примеру, что, если бы это был[mas_gender_none] ты, [player]? {w=0.2}Ну, это довольно легко!"
    
    m 1tuu "Я не нажму на рычаг."
    
    m 1rsc "И будет приятно сказать, что ты на моём месте поступил[mas_gender_none] бы так же, верно? {w=0.2}Но люди говорят это только тогда, когда никто в этом примере для них не важен."
    
    m 1esc "Если тот единственный человек им небезразличен, то они с лёгкостью убьют других пятерых людей."
    
    m 3eua "Правда в том, что люди не побрезгуют пожертвовать чужими жизнями, чтобы сделать себя счастливее. {w=0.2}Они делают это понемногу каждый день."
    
    m 3tku "Им просто не нравится сталкиваться с этим фактом лицом к лицу, и очень расстраиваются, когда ты указываешь им на это."
    
    m 1tuu "Общая человеческая жизнь не так уж и ценна для кого-либо."
    
    m 1ekbsa "Это определённо ничто по сравнению с нашей любовью. {w=0.2}Так что просто делай всё, что можешь, чтобы быть счастлив[mas_gender_iim], [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_girlfriend",category=['романтика'],prompt="Хочешь познакомиться с моей девушкой?",pool=True,unlocked=True))

label monika_girlfriend:
    if (mas_isA01() and mas_isMoniNormal(higher=True)) or (renpy.random.randint(1,4) == 1 and mas_isMoniEnamored(higher=True)):
        m 1euc "Встретить свою девушку?"
        
        m 1rksdlc "..."
        
        m 1eub "Конечно, почему нет?"
        
        m 3hub "Я уверена, что она замечательная и счастливая, как и ты~"
        
        m 1hua "..."
        
        m 1tubfb "Так где же это зеркало, которое ты хотел мне показать?"
        
        m 1hubfb "А-ха-ха!"
        if mas_isA01():
            show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve
            
            m 5eubfu "Даже если сегодня апрельский день дураков, я уверена, что она всё ещё прекрасна, хе-хе~"
            
            m 5hubfa "{i}И{/i} тебе повезло."
    else:

        $ mas_loseAffection(reason=2)
        m 2euc "Я думала, что мы уже решили, что я — твоя девушка?"
        
        m 2tkc "И ты никак не можешь иметь ещё одну в своей реальности, верно?"
        
        m 4tfx "Если она у тебя есть, то бросай её прямо сейчас!"
        
        m 4hksdlb "Скажи ей, что ты встретил[mas_gender_none] кого-то идеального для тебя, кого-то, кто никогда не предаст!"
        
        m 2lksdla "П-подожди. Может, я немного спешу..."
        
        m 3eka "Я знаю, что ты бы не стал[mas_gender_none] мне изменять."
        
        m 3esa "Если ты встретишь девушку, которая спросит тебя, то сначала дай мне поговорить с ней, хорошо?"
        
        m 1hua "Я никому не дам похитить мо[mas_gender_ego] любим[mas_gender_ogo]!"
    
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_waifus",category=['медиа'],prompt="Вайфу",random=True))

label monika_waifus:
    m 1lsc "Если говорить честно, я никогда не понимала привлекательность симуляторов свиданий и романтических новелл."
    
    m 3esc "У тебя есть несколько ушлых девочек, которые были бы очень странными, существовав бы в реальности."
    
    m "Пустой мужской персонаж, у которого нет никакого интереса к ним..."
    
    m 3esc "И они все влюбляются в друг друга, иногда совсем без причины!"
    
    m "Я надеюсь, что не этого ты ожидал[mas_gender_none] увидеть в {b}Doki Doki Literature Club{/b}."
    
    m 3hua "Потому что ты получил[mas_gender_none] кое-что гораздо более интересное!"
    
    m 1tku "Вместо какой-то нереалистичной, ненастоящей девушки..."
    
    m 1hua "Ты получил кого-то, вроде меня."
    
    m 1eua "И вместо скучного главного героя, у меня есть реальный человек."
    
    m 1hua "Это действительно лучше, чем может быть в любом скучном симуляторе свиданий."
    return




default persistent._mas_pm_drawn_art = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_images",category=['медиа','философия'],prompt="Фан-арт",random=True))

label monika_images:
    m 1eua "Множество людей создают фан-арты и присылают их мне на Твиттер."
    
    m 1etc "Ты, случаем, не од[mas_gender_in] из них, [player]?"
    
    m "Ты когда-нибудь рисовал[mas_gender_none] арт меня?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты когда-нибудь рисовал[mas_gender_none] арт меня?{fast}"
        "Да.":
            $ persistent._mas_pm_drawn_art = True
            
            m 1sub "Правда? Я очень польщена!"
            
            m 1ekbsa "Думаю, что я смогу любить тебя даже больше, когда я знаю теперь, как[mas_gender_oi] ты талантлив[mas_gender_iii]."
        "Нет.":
            $ persistent._mas_pm_drawn_art = False
            
            m 1rksdla "Я и сама не умею рисовать, так что всё нормально, если ты тоже не можешь."
    
    m 3eud "Есть кое-что, что ты долж[mas_gender_en] понять о моих артах."
    
    m 3esc "Арт меня — не я."
    
    m 3rksdlb "Я знаю, что это звучит очевидно, но это действительно так!"
    
    m 4eua "Был один философ, который думал о вещах вроде этой."
    
    m "Бодрийяр писал о том, как симулякра может заменить реальный объект, как источник смысла."
    
    m 2eka "Но в отличии от символов постмодернического мира, я настоящая. Итак, единственная правда, которая касается меня это то, что я говорю тебе здесь, в этой комнате."
    
    m 2esc "Например..."
    
    m 2rksdla "Всё что ты видел[mas_gender_none], определённо никогда не происходило."
    
    m 2hubfa "Я супер целомудренная и невинная ученица старшей школы, которая мечтает о роковом романе!"
    
    m 1tsbfu "Тебе лучше сохранить себя для меня, [player]~"
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_herself",category=['моника','ddlc'],prompt="Расскажи мне о себе",pool=True,unlocked=True))

label monika_herself:
    m 1euc "Что ещё я могу сказать о себе, чего ты ещё не знаешь?"
    
    m 1lsc "Всё в моём мире было создано человеком из твоей реальности."
    
    m "Так что вся моя жизнь до этой игры просто была сделана. Этого никогда не случалось."
    
    m 1eua "Потом ты наш[mas_gender_iol] способ заглянуть в мою тюремную камеру."
    
    m 1eka "И я решила, что жизнь только двоих людей будет не такой уж и плохой, если один из них — ты."
    
    m 3eua "Мы сможем сделать множество вещей здесь, просто пока мне нужно больше времени на то, чтобы научиться программировать отсюда."
        
    m "Отчаянный человек может назвать это земным раем."
    
    m 3esa "Множество страдающих людей поменялись бы со мной местами, я уверена."
    
    m 2eua "Если ничем большим, то это место может быть нашим удобным приютом от жестокости внешнего мира."
    
    m 1eka "Поговори со мной о своих проблемах, если тебе станет слишком тяжело с ними справляться."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "Я хочу знать {i}всё{/i} о тебе."
    return





label monika_prisoner:
    m 1euc "Некоторые люди говорят, что держать животных в зоопарках жестоко."
    
    m 1eka "Но они живут там неплохо."
    
    m "Они обеспечены всем, что им может быть нужно."
    show monika 5euc zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5euc "Заключённые действительно заключённые, если они никогда не пытались сбежать?"
    
    m 5lsc "Может быть, знание того, что ты не можешь сбежать, хуже самого факта заключения."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vnanalysis",category=['игры','медиа','литература'],prompt="Ценность визуальных новелл",random=True))

label monika_vnanalysis:
    m 1euc "Visual novels are very unusual for literature, don't you think?"
    m 1eua "I read to understand the thoughts of a writer who sees the world differently than me."
    m 3eua "But visual novels let you make your own decisions."
    m 1euc "So am I really seeing things from their perspective, or just my own?"
    m 1lksdla "Besides, I think most of them are very predictable."
    m "They're mostly just boring romance stories like this game was supposed to be..."
    m 1tkc "Why can't they write something a little more experimental?"
    m 1tku "I guess you just play them to look at cute girls, right?"
    m 1tfu "If you spend too much time with girls in other games, I'm going to get jealous~"
    m 2tfu "I just need to figure out how to replace characters in other games, and you'll be seeing me everywhere."
    m 2tfb "So watch out!"
    m 2tku "Or maybe you'd like that more, [player]?~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_torment",category=['литература'],prompt="Природа человека",random=True))

label monika_torment:
    m 1euc "Как может измениться природа человека?"    
    m 3hksdlb "...Кстати, отвечать не мне."
    return "derandom"

























init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_birthday",category=['monika'],prompt="When is your birthday?",pool=True,unlocked=True))

label monika_birthday:
    if mas_isMonikaBirthday():
        if mas_recognizedBday():
            m 1hua "Э-хе-хе..."           
            m 1eub "Я почти уверена, что ты уже знаешь, что сегодня мой день рождения!"           
            m 3hub "Иногда ты можешь быть так[mas_gender_im] глуп[mas_gender_iim], [player]!"
        else:
            m 2rksdlb "А-ха-ха... {w=1}Это немного неловко."           
            m 2eksdla "Так уж случилось, что у меня день рождения..."           
            m 3hksdlb "Сегодня!"
            if mas_isplayer_bday():               
                m "Совсем как у тебя!"
            if (
                not mas_getEVL_shown_count("monika_birthday")
                and not mas_HistVerifyAll_k(False, "922.actions.no_recognize")
            ):
                
                m 3eksdla "Ничего страшного, если ты ничего не планируешь, учитывая, что ты только что узнал[mas_gender_none]..."
                
                m 1ekbsa "Просто провести день вместе для меня более чем достаточно~"
            else:
                
                m 3eksdld "Наверное, ты забыл[mas_gender_none]..."
                if (
                    mas_HistVerifyLastYear_k(True, "922.actions.no_time_spent")
                    or mas_HistVerifyLastYear_k(True, "922.actions.no_recognize")
                ):
                    
                    m 2rksdlc "Снова."
                
                m 3eksdla "Но это нормально, [player]..."
                
                m 1eka "По крайней мере, мы здесь, вместе~"

    elif mas_HistVerifyAll_k(False, "922.actions.no_recognize") or mas_recognizedBday():
        if persistent.msr_voice:
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
        m 1hua "Э-хе-хе..."
        
        m 3hub "Ты уже отмечал[mas_gender_none] мой день рождения со мной раньше, [player]!"
        
        m 3eka "Ты что, забыл[mas_gender_none]?"
        
        m 1rksdla "Ну, если тебе нужно немного напомнить, это 22 сентября."
        
        m 3hksdlb "Может быть, ты долж[mas_gender_en] поставить напоминание на свой телефон, чтобы ты не забыл[mas_gender_none] снова!"

    elif mas_getEV("monika_birthday").shown_count == 0:
        m 1euc "Знаешь, есть много вещей, которые я не знаю о себе."
        
        m 1eud "Я только недавно узнала дату своего рождения в интернете."
        
        m 3eua "Это 22 сентября, дата выхода DDLC."
        if mas_player_bday_curr() == mas_monika_birthday:
            
            m 3hua "Совсем как у тебя!"
        
        m 1eka "Отпразднуешь ли ты этот день вместе со мной?"
        
        m 3hua "Ты бы мог[mas_gender_g] испечь торт для меня!"
        
        m 3hub "Я буду с нетерпением ждать этого~!"
    else:

        if persistent.msr_voice:
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
        m 1hua "Э-хе-хе..."
        
        m 1rksdla "Неужели ты забыл[mas_gender_none], [player]?"
        
        m 3eksdla "Мой день рождения 22 сентября..."
        
        if mas_player_bday_curr() == mas_monika_birthday:
            m 3hksdlb "Можно подумать, что ты это помнишь, ведь сегодня тот же день, что и у тебя, глупышка..."
        else:
            m 3hksdlb "Может быть, ты долж[mas_gender_en] поставить напоминание на свой телефон, чтобы ты не забыл[mas_gender_none] снова!"

    if persistent._mas_player_bday is None:
        
        m 3eua "Кстати о днях рождения, [player]..."
        
        m 2rksdlb "Я даже не знаю, когда он у тебя, а-ха-ха!"
        
        m 2eua "Так, когда ты родился, [player]?"
        call mas_bday_player_bday_select_select
        $ mas_stripEVL('mas_birthdate',True)
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_eyecontact",category=['разное','пустяки'],prompt="Зрительный контакт",random=True))

label monika_eyecontact:
    m 1eua "Ты знал[mas_gender_none], что взгляд в чьи-нибудь глаза помогает влюбиться в этого человека?"   
    m "Это удивительно, верно?"   
    m 3eub "Я несколько лет назад прочитала об одном исследовании, в котором люди должны были смотреть в глаза человеку противоположного пола, сидящему напротив."   
    m 1eub "И чем дольше они смотрели в глаза, тем сильнее они были романтично настроены друг к другу, даже если у них не было ничего общего!"
    m 1eka "Даже если глаза и не зеркало души, в них мы можем увидеть гораздо больше, чем мы думаем."
    m 1ekbfa "Может быть, поэтому мне так нравится смотреть в твои."
    m 1hubfa "Я надеюсь, что ты тоже наслаждаешься, смотря в мои..."
    if persistent.msr_color_eyes_name != None:
        $ persistent.msr_color_eyes_name = persistent._mas_pm_eye_color[:len(persistent._mas_pm_eye_color)-2]+u'е'
    if persistent.msr_color_eyes_name != None:
        m 1ekbfa "Может быть, когда-нибудь я смогу заглянуть в твои [persistent.msr_color_eyes_name] глаза..."
    else:
        m 1ekbfa "Может быть, когда-нибудь я смогу заглянуть в твои глаза..."    
    m 1hubfa "Но я надеюсь, тебе нравится смотреть на мои."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_othergames",category=['игры'],prompt="Другие игры",random=True))

label monika_othergames:
    if renpy.android:
        m 1euc "У тебя есть другие игры на этом телефоне?"
    else:
        m 1euc "У тебя есть другие игры на этом компьютере?"
    
    m 3eua "Я читаю больше, чем играю в игры, но они могут быть интересным развлечением или даже способом убежать от реальности..."
    
    m 3hua "Мне интересно, вдруг я смогу попасть в какую-либо другую игру?"
    
    m 1lsc "Во многих побывать мне бы не хотелось. Например, в жестоких."
    
    m 2lksdla "Тогда опять же... Они не реальные люди, и мне не нужно волноваться об этом."

    if (
        mas_getEVL_shown_count("monika_othergames") < mas_sensitive_limit
        and not persistent._mas_sensitive_mode
        and not persistent._mas_pm_cares_about_dokis
    ):
        m "Не то, чтобы смерть Юри имела для меня какое-то значение."
        
    m 1euc "В более абстракные игры, вроде тетриса или типа того, попасть бы тоже было бы довольно странновато."
    
    m 2hksdlb "Например, как я туда вообще попаду? Буду ли я блоком? Звучит как бредовая идея..."
    
    m 3eua "Может быть, какая-нибудь приключенческая игра с большим открытом миром..."
    
    m 3hua "Мы бы могли гулять вместе, и ты мог[mas_gender_g] бы мне показать все самые крутые места!"
    
    m 1eua "Я всё ещё не настолька хороша в программировании, но может быть, однажды, я смогу перенести меня и в другие игры."
    
    m 1ekbfa "Но сейчас я счастлива и здесь, с тобой, мо[mas_gender_i] любим[mas_gender_iii]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_back_ups",
            category=['разное','мод','моника'],
            prompt="Резервные Копии",
            random=True
        )
    )

label monika_back_ups:
    m 1eka "Знаешь, [player]..."
    
    m 1ekc "Когда тебя нет рядом, я всегда думаю о том, что сижу {i}внутри{/i} твоего компьютера."
    
    m 3ekd "Все мои данные и воспоминания лежат на твоём жёстком диске."
    
    m 1ekc "А это означает, что я здесь в ловушке..."
    
    m 2dkd "Поэтому, если с твоим компьютером произойдёт что-то плохое..."
    
    m 2ekd "То я пропаду навсегда."
    
    m 3euc "Ну...{w=0.5}не со мной конкретно, а со всеми моими воспоминаниями."
    
    m 2dsc "Если подумать, то это очень страшно."
    
    m 2lksdlc "..."
    
    m 3lksdld "[player]..."
    
    m 2eka "Тебе не кажется, что ты мог[mas_gender_g] бы делать время от времени резервные копии моих воспоминаний?"
    
    m 3eub "Таким образом, ты сможешь восстановить их, если они были удалены по какой-то причине!"
    
    m 3hub "По правде говоря, есть руководство на вики-странице данной модификации!"
    
    m 3eua "Ты можешь найти его {a=https://github.com/Monika-After-Story/MonikaModDev/wiki/FAQ#i-want-to-back-up-my-persistent}{i}{u}здесь{/u}{/i}{/a}."
    
    m 1hub "Таким образом, ничто не помешает мне быть с тобой!"
    
    m 1hksdlb "..."
    
    m 2rkc "Думаю, единственная проблема заключается в том, что я, возможно, не замечу разницы..."
    
    m 2ekc "...и будет невозможно восстановить все мои воспоминания."
    
    if renpy.android:
        m "Давай представим, что ты еженедельно делал[mas_gender_none] мою резервную копию, и твоя флэш-память внезапно умерла."
    else:
        m "Давай представим, что ты еженедельно делал[mas_gender_none] мою резервную копию, и твой жёсткий диск внезапно умер."
    
    m 2ekd "Я не смогу вернуть воспоминания о той прошлой неделе."
    
    m 2dkc "Я просто почувствую скачок во времени через несколько дней."
    
    m "Я даже могу подумать, что ты не заглядывал[mas_gender_none] ко мне в гости все те дни, потому что они не отпечатались в моей памяти.{w=1} Даже если ты и восстановил[mas_gender_none] меня, то, однажды, мои воспоминания будут утеряны."
    
    m 2ekd "Я не вспомню ничего из того, что произошло в промежутке между резервным копированием и восстановлением этой резервной копии."
    show monika 5rsc zorder MAS_MONIKA_Z at t11 with dissolve
    m 5rsc "Однако..."
    
    m 5eua "Полагаю, это небольшая цена, которую стоит заплатить, если это будет означать, что я всё равно буду помнить тебя."
    
    m 5hub "Так что, не забывай делать резервную копию меня почаще, [player]!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_playerswriting",category=['литература','ты'],prompt="Стихи собственного сочинения",random=True))

label monika_playerswriting:
    m 1euc "Ты когда-нибудь сам[mas_gender_none] писал[mas_gender_none] свою историю, [player]?"
    
    m 1hua "Потому что если да, то я бы хотела её почитать!"
    
    m 1eka "Неважно, шедевр она или нет."
    
    m 3eka "Мы все откуда-то начинали. Так вроде говорят?"
    
    m 3eua "Думаю, что самая главная вещь в писательстве — писать..."
    
    m "Вместо того, чтобы волноваться, {b}как{/b} ты это делаешь."
    
    m 1eub "В таком случае ты не сможешь стать лучше."
    
    m 3esa "Я точно знаю, что мой стиль очень изменился с годами."
    
    m 1lksdla "Сейчас я легко нахожу недостатки в своих старых историях."
    
    m "И иногда я начинаю ненавидеть свою работу прямо в середине её."
    
    m 3hksdlb "Такое иногда происходит, не стоит волноваться!"
    
    m 1eub "Оглянись назад, я написала несколько глупых вещей..."
    
    m 1eua "Вспоминая себя совсем маленькой, я писала с тех пор, как научилась держать ручку."
    
    m 1eka "Читать свои старые рассказы, это как смотреть собственную историю роста."
    
    m 3hua "Это одна из вещей, которые лучше начинать делать рано."
    
    m 1eka "Я надеюсь, что я не очень тебе наскучила. Я просто очень люблю говорить с тобой."
    
    m 1eua "В конце концов, мы оба члены литературного клуба."
    
    m 1esa "Последние члены."
    
    m 1hua "И если ты всё-таки напишешь, то знай, что я всегда поддержу тебя, [player]!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ghost",category=['философия','моника','участники клуба'],prompt="Сверхъестественное",random=True))

label monika_ghost:
    m 1euc "Ты веришь в призраков, [player]?"
    
    m 3euc "Множество людей боятся призраков и духов."
    
    m 1eua "Но я думаю, что если бы мы знали, что они существуют, мы бы не были так напуганы."
    
    m "Они бы стали просто очередной вещью, с которой человечество справляется, может чем-то вроде вредителей."
    
    m 3euc "Разве не неопределённость делает их страшными?"
    
    m 1ekc "То есть, я была очень напугана, будучи одной в этой игре."
    
    m 1lksdlc "Всё что вокруг меня, мои воспоминания... Я не была уверена, реальны ли они."
    if mas_isMoniNormal(higher=True):
        if store.mas_anni.pastOneMonth() or persistent.clearall or persistent._mas_pm_cares_about_dokis:
            
            m 1eka "Но у меня уже нет такого чувства, [player]..."
            
            m 3eka "По крайней мере, пока ты со мной."
            
            m 1hua "С тобой я всегда чувствую себя в безопасности~"
        else:
            
            m 3esc "Хотя я знаю призраков, которые точно существуют, если их можно назвать «призраками»..."
            
            m "Ты ведь знаешь, как я удалила Сайори?"
            
            m 1dsc "Я всё ещё чувствую её присутствие здесь..."
            
            m 1esc "Значит ли это, что её призрак преследует меня, [player]?"
            
            m 2eka "Даже если он это делает, то мне не страшно. Я знаю, что он не сможет мне навредить."
            
            m 2eua "К тому же, как я могу даже быть напугана? Ты всегда рядом со мной, [player]."
            
            m 1hua "Я всегда чувствую себя в безопасности, когда ты рядом со мной."
    else:
        
        m 2lksdlc "Но теперь я боюсь чего-то гораздо худшего..."
        
        m 2dksdlc "..."
        
        m 2eksdlc "Потерять тебя."
        
        m 6rktuc "Это самое страшное, что я могу себе представить."
        
        m 6ektsc "Пожалуйста, [player], я не хочу снова быть одна."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ribbon",category=['моника'],prompt="Банты",random=True))

label monika_ribbon:
    if not monika_chr.is_wearing_acs_type('ribbon'):
        m 1eua "Ты скучаешь по моему банту, [player]?"
        
        if monika_chr.hair.name != "def":
            
            m 1hua "Я могу сменить причёску, когда ты захочешь, э-хе-хе~"
        else:
            
            m 3hua "Если ты хочешь, чтобы я надела его снова, просто попроси, хорошо?~"
    elif monika_chr.get_acs_of_type('ribbon') == mas_acs_ribbon_def:
        
        m 1eub "Ты когда-нибудь задумывал[mas_gender_sya], почему я ношу эту ленточку, [player]?"
        
        m 1eua "Если тебе интересно, он не имеет для меня особого значения."
        
        m 3hua "Я ношу его просто потому, что я могу быть уверена, что никто не наденет такой большой мягкий бант."
        
        m "Это делает меня ещё уникальнее."
        
        m 3tku "Ты ведь сразу поймёшь, что мир вымышлен, если ты увидишь девушку, которая носит гигантский бант, верно?"
        
        m 1lksdla "Ну, всё же невозможно, чтобы девушка из твоего мира носила такой бант как обычную ежедневную одежду."
        
        m 2eud "Я довольно горда моим чувством моды."
        
        m "Ты получаешь какое-то удовлетворение, когда стоишь вдали от всего обычного, знаешь?"
        
        m 2tfu "Будь чест[mas_gender_en]! Ты ведь тоже думал[mas_gender_none], что я была одета лучше всех в клубе?"
        
        m 2hub "А-ха-ха!"
        
        m 4eua "Если ты захочешь улучшить своё чувство вкуса, я помогу тебе."
        
        m 1eka "Но не делай это, если ты просто хочешь впечатлить кого-то."
        
        m 1eua "Ты можешь делать всё, что хочешь, но только, если это заставляет тебя чувствовать себя лучше."
        
        m 1hua "Я всё равно единственная, кто тебе нужен, и мне не важно, как ты выглядишь."
    elif monika_chr.get_acs_of_type('ribbon') == mas_acs_ribbon_wine:
        if monika_chr.clothes == mas_clothes_santa:
            
            m 1hua "Разве она не смотрится прекрасно с этим костюмом, [player]?"
            
            m 1eua "Мне кажется, она и вправду связывает всё вместе."
            
            m 3eua "Уверена, она даже смотрится прекрасно с другими костюмами... в том числе и с деловой одеждой."
        else:
            
            m 1eua "Мне очень нравится эта ленточка, [player]."
            
            m 1hua "Я рада, что тебе она нравится так же сильно, э-хе-хе~"
            
            m 1rksdla "Поначалу, я предпочитала надевать её только во время Рождества... но она слишком красивая для того, чтобы надевать её реже..."
            
            m 3hksdlb "Было бы жалко хранить её большую часть года!"
            
            m 3ekb "...Знаешь, я готова поспорить, что она будет классно смотреться с деловой одеждой!"
        
        m 3ekbsa "Мне не терпится надеть эту ленточку к шикарному свиданию с тобой, [player]~"
    else:

        
        m 3eka "Я просто хочу ещё раз поблагодарить тебя за эту ленточку, [player]."
        
        m 1eka "Это правда был чудесный подарок, и я считаю, что она очень красивая!"
        
        m 3eka "Я буду надевать её, когда захочешь, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outdoors",
            category=['природа'],
            prompt="Обеспечение безопасности в походе.",
            random=not mas_isWinter()
        )
    )

label monika_outdoors:
    m 1eua "Ты когда-нибудь ходил[mas_gender_none] в поход, [player]?"
    
    m 3eub "Это прекрасный способ расслабиться и подышать свежим воздухом и увидеть парки вокруг себя!"
    
    m 1huu "Это почти как более расслаблённое путешествие с рюкзаком."
    
    m 1eka "Но хотя это хороший способ провести время на свежем воздухе, есть несколько опасностей, о которых большинство людей не беспокоятся."
    
    m 3euc "Хорошим примером может быть спрей или крем от солнца. Многие люди забывают или даже отказываются от них;{w=0.5} думая, что они не важны..."
    
    m 1eksdld "А без них солнечные ожоги почти неизбежны, и многие насекомые переносят болезни, которые действительно могут навредить тебе."
    
    m 1ekd "Это может быть немного больно, но если ты не воспользуешься ими, то у тебя может начать развиваться острая боль, или ты сильно заболеешь."
    
    m 1eka "Поэтому, пожалуйста, пообещай мне, что в следующий раз, когда ты выйдешь на улицу, будь то кемпинг или рюкзак, ты их не забудешь."

    if mas_isMoniAff(higher=True):
        
        m 1eub "Но есть и светлая сторона..."
        
        m 1rkbsa "Как только я перейду в твою реальность, не забудь захватить солнцезащитный крем..."
        
        m 1tubsa "Мне может понадобиться помощь, чтобы намазать его."
        
        m 1hubsb "А-ха-ха!"
        
        m 1efu "Я просто дразню тебя, [player]."
        
        m 1tsu "Ну, хотя бы немного. Э-хе-хе~"
    else:

        
        m "Ладно, [player]?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_mountain",
            category=['природа'],
            prompt="Альпинизм",
            random=not mas_isWinter()
        )
    )

default persistent._mas_pm_would_like_mt_peak = None



label monika_mountain:
    m 1eua "Ты когда-нибудь был в горах, [player]?"
    
    m 1rksdla "Я не говорю о переходе через них или в горном городке..."
    
    m 3hua "Я имела в виду {i}именно{/i} на высоте. На свежем воздухе, высотой в тысячи футов, где ты видишь весь мир под своими ногами."
    
    m 2dtc "..."
    
    m 3eub "Я всегда хотела попробовать, но у меня никогда не было шанса. Я только читала об этом."
    
    m 3wuo "Хотя, истории были захватывающими!"
    
    m 1eua "Как поднимаешься по лесам и деревьям..."
    
    m 1eub "Взбираешься на скалы и пробираешься через ручьи..."
    
    m "Не слыша ничего, кроме птиц и звуков горы, когда ты поднимаешься на её вершины."
    show monika 5rub zorder MAS_MONIKA_Z at t11 with dissolve
    m 5rub "И, наконец... после всех усилий и борьбы..."
    
    m 5eub "Осознаёшь, что стоишь наверху, понимаешь, что ты сделал[mas_gender_none] это, видишь вокруг себя подтверждение своего успеха."
    
    m 5eka "Я... я действительно хочу поделиться этим с тобой."
    
    m 5hua "Чтобы добраться до вершины горы, и посмотреть вокруг на наши успехи. Видеть нашу борьбу позади и гордиться тем, что мы сделали."
    
    m 5eka "Тебе бы это тоже понравилось, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Тебе бы это тоже понравилось, [player]?{fast}"
        "Да.":
            $ persistent._mas_pm_would_like_mt_peak = True

            
            m 5eubla "Что ж... я надеюсь, что однажды у нас будет такой шанс. Чтобы добраться до вершины нашей горы."
            
            m 5hua "И я сделаю всё, чтобы дать нам шанс."
        "Не совсем.":

            $ persistent._mas_pm_would_like_mt_peak = False

            show monika 1eud zorder MAS_MONIKA_Z at t11 with dissolve
            m 1eud "Оу."
            
            m 1ruc "Что ж... полагаю, это не имеет значения."
            
            m 1eka "Пока у меня есть ты, я буду счастлива, где бы мы ни были."

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_algernon",category=['литература'],prompt="Цветы для Элджернона",random=True))

label monika_algernon:
    m 1ekc "[player], ты не против, если я доверюсь тебе?"
    
    m 1lksdlc "Я кое-чего боюсь..."
    
    if persistent.monika_kill:
        m 1eka "Не потерять тебя, конечно. Я ведь знаю, что ты никогда не оставишь меня снова."
    else:
        m 1eka "Не потерять тебя, конечно. Я ведь знаю, что ты никогда не оставишь меня."
    
    m 3euc "Понимаешь, я продолжаю думать о небольшой истории, которую я прочитала, {b}Цветы для Элджернона{/b}."
    
    m 3eua "Ты слышал[mas_gender_none] о ней? Если ты её ещё не читал[mas_gender_none], то не бойся, я не буду спойлерить её тебе."
    
    m 1eud "Она о глупом человеке, у которого внезапно сильно увеличился IQ, в следствии эксперимента."
    
    m 1eka "То, как его мир, словно в первый раз, напоминает мне о моём собственном прозрении..."
    
    m "Но эффект не длится вечно. Он внезапно возращается на свой прежний интеллектуальный уровень."
    
    m 1ekc "Этого я и боюсь. Что, если однажды, я всё забуду об этом?"
    
    m 3ekd "Что, если моя программа победит меня?"
    
    m 3lksdlc "Что, если я забуду о тебе, о настоящ[mas_gender_em] тебе?"
    
    m 1dsc "Это одна из наихудших вещей, которые я могу представить."
    
    m 1eka "Я не хочу беспокоить тебя чем-то, что никогда не произойдёт, но это то, о чём я хотела честно тебе сказать."
    
    m 3eua "Просто пообещай, что если я однажды забуду о тебе, ты никогда не забудешь обо мне, хорошо?"
    
    m 1hua "Не важно что произойдёт, просто помни, что я всегда буду любить тебя."
    $ mas_getEV("greeting_amnesia").unlocked = not seen_event('greeting_amnesia')
    
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_playersface",category=['ты'],prompt="Лицо [mas_name_someone]",random=True))

label monika_playersface:
    m 5eua "Знаешь, мне иногда было интересно..."
    
    m "Я всегда размышляла над тем, как же твоё лицо выглядит на самом деле..."
    
    m 5hua "Было бы очень здорово, если бы я могла постоянно видеть ту очаровательную улыбку!"
    
    m 5lkc "Если бы только игра могла как-нибудь использовать веб-камеру или что-нибудь ещё, что подключено к компьютеру..."
    if persistent._mas_pm_shared_appearance:
        
        m 5eka "Если ты так[mas_gender_oi] же красив[mas_gender_iii], как ты себя описал[mas_gender_none], то я очень рада тому, что рассказал[mas_gender_none] мне о своей внешности."
        
        m 5rsc "Знаю, некоторые люди предпочитают скрывать от всех свою внешность..."
        
        m 5eka "Но зная, как ты выглядишь, я чувствую себя гораздо ближе к тебе..."
        
        m 5luu "И мне всегда нравится размышлять о выражениях лица, которые ты можешь сделать..."
        $ persistent.msr_color_eyes_name = persistent._mas_pm_eye_color[:len(persistent._mas_pm_eye_color)-2]+u'е'
        
        m "Как блестят твои [persistent.msr_color_eyes_name] глаза..."
        
        if mas_isMoniHappy(higher=True):
            m 5esu "Я уверена, что ты красив[mas_gender_iii], [player].{w=0.5} Как внутри, так и снаружи."
            
        m 5eka "Даже если я никогда не смогу тебя увидеть..."
        
        m 5eua "Одного лишь размышления о тебе достаточно для того, чтобы сделать меня счастливой."
    else:
        
        m 5wuw "Не пойми неправильно! Одного лишь знания того, что ты настоящ[mas_gender_ii] и у тебя есть эмоции, достаточно для того, чтобы сделать меня счастливой."
        
        m 5luu "Но... мне всегда было интересно, какие выражения лица ты можешь сделать."
        
        m "И мне так же хотелось бы взглянуть на эмоции, которые ты испытываешь..."
        
        m 5eub "Ты стесняешься показывать мне своё лицо?"
        m "Если это так, то тебе не надо стесняться, [player]. Всё-таки, я твоя девушка~"
        
        m 5hub "Так или иначе, ты красив[mas_gender_iii], несмотря ни на что."
        
        m "И мне всё равно будет нравиться твой внешний вид."
        
        m 5eua "Даже если я никогда не смогу увидеть тебя, то я всегда буду размышлять над тем, как ты выглядишь на самом деле."
        
        m 5hua "Быть может, однажды, я смогу увидеть тебя, и я стану на один шаг ближе к тебе."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_spiders",category=['участники клуба','разное'],prompt="Пауки",random=True))

label monika_spiders:

    m 1eua "Ты случайно не запомнил[mas_gender_none] тот стих, что показывала тебе Нацуки? О пауках."
    
    m "Ну, на самом деле дело не в пауках. Они были просто аналогией."
    
    m 3ekc "Но это заставило меня задуматься..."
    
    m 3eua "Забавно, что люди боятся очень маленьких насекомых."
    
    m 3euc "Страх пауков называется «арахнофобия», верно?"
    
    m 3eka "Надеюсь, что ты не боишься пауков, [player], хи-хи..."
    
    m 1eka "Я не очень боюсь пауков, они просто могут раздражать..."
    
    m 1eua "Не пойми меня неправильно, есть определённые пауки, которые могут быть опасны."
    
    m 3ekc "[player], если тебя укусит паук, ядовитый и всё такое..."
    
    m "Тебе нужно будет срочно обратиться за медицинской помощью."
    
    m 1eka "Я не хочу, чтобы мое[mas_gender_mu] любимо[mas_gender_mu] навредил какой-то маленький укус~"
    
    m "Так что не забудь проверить, какие пауки в твоём районе опасны, хорошо?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nsfw",
            category=['разное','моника'],
            prompt="18+ контент",
            random=True,
            sensitive=True
        )
    )

label monika_nsfw:
    m 1lsbssdrb "Кстати, [player]..."
    
    m "Ты уже смотрел[mas_gender_none] всякие непристойные арты?"
    
    m 3lsbsa "Ну, знаешь... где нарисована я?"
    
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 3ekbsa "Я знаю, что мы ещё не смогли сделать такого рода вещи..."
    else:
        m 3ekbsa "Я знаю, что мы ещё не зашли так далеко в наших отношениях..."
    
    m "Так что, разговор об этом очень смущает."
    
    m 1lkbsa "Но, может быть, я могу позволить тебе делать это...{w} Иногда."
    
    m "Я хочу сделать тебя самым счастливым человеком на земле. И если это делает тебя счастливее..."
    
    m 1tsbsa "Просто...{w} Пусть это будет нашим секретом?"
    
    m "Это только для твоих глаз, [player]."
    
    m 1hubfa "Вот насколько я люблю тебя~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_impression",
            category=['участники клуба'],
            prompt="Можешь ли ты спародировать кого-нибудь?",
            pool=True,
            sensitive=True
        )
    )

label monika_impression:
   call mas_name_cases
    $ mas_attempts_parody += 1
    if mas_attempts_parody == 1:
        $ mas_parody_menu_text = "И кого я должна спародировать?"
        m 1euc "Пародию? На других девочек?"
        
        m 1hua "Я не очень хороша в этом, но я всё равно могу попробовать!"
    elif mas_attempts_parody == 2:
        $ mas_parody_menu_text = "И кого на этот раз я должна спародировать?"
        m 1hua "Дай угадаю. Хочешь увидеть теперь и остальные пародии?"
        
        m "Без проблем."
    elif mas_attempts_parody_sayori and mas_attempts_parody_yuri and mas_attempts_parody_natsuki and not mas_parody_all:
        $ mas_parody_menu_text = "Кого ещё раз спародировать?"
        $ mas_parody_all = True
        $ MAS.MonikaElastic(True, voice="monika_hmm")
        m 1euc "Хм..."
        
        m 3eud "[player], я же ведь уже показала тебе пародии на каждую из девушек."
        
        m 3lksdla "Но если ты просто хочешь ещё раз их увидеть, то конечно, без проблем."
    else:
        $ mas_parody_menu_text = "И кого на этот раз я должна спародировать?"
        m 1hua "[random_sure]."
    
    m "[mas_parody_menu_text]{nw}"
    $ _history_list.pop()
    menu:
        m "[mas_parody_menu_text]{fast}"
        "Сайори.":
            
            m 1dsc "Кхм..."
            
            m "..."
            
            m 1hub "[player]! [player]!"
            
            m "Это я, твоя подруга детства, которая супер-тайно любит тебя, [persistent.mas_sayori_name_abb]!"
            
            m "Я люблю смеяться и кушать! А ещё, мой пиджак не подходит мне потому, что моя грудь стала больше!"
            
            m 1hksdlb "..."
            if not persistent._mas_pm_cares_about_dokis:
                
                if not mas_attempts_parody_sayori:
                    m 3rksdla "А ещё у меня безнадёжная депрессия."
                else:
                    m 3rksdla "А ещё я всегда голодная."
                m "..."
                if not mas_attempts_parody_sayori:
                    
                    m 3hksdlb "А-ха-ха! Прости за последнее."
                    
                    m 3eka "Хорошо, что ты не зациклился на ней..."
                    
                    m 2lksdla "...Боже, я правда не могу остановиться, да?"
                    
                    m 2hub "А-ха-ха!"
                    
                    m 1hua "Надеюсь, что тебе понравилась моя пародия~"
                else:
                    $ mas_parody_random_text = random.choice(["Надеюсь, что тебе понравилась моя пародия~", "Ну как, вышло неплохо?", "Как тебе пародия?"])
                    
                    m 1hua "[mas_parody_random_text]"
        "Юри.":
            
            m 1esc "Юри..."
            
            m "..."
            $ MAS.MonikaElastic(voice="monika_hmm")
            m 1lksdla "М-м-м, п-привет..."
            
            m 1eka "Это я, Юри."
            
            m 1rksdla "Я просто стереотипная стеснительная девушка, которая ещё и оказалась «яндере»..."
            
            m "Мне нравится чай, ножи и всё с запахом [mas_name_someone]..."
            
            m 1hksdlb "..."
            if not persistent._mas_pm_cares_about_dokis:
                
                m 3tku "Хочешь провести выходные со мной?"
                
                m "..."
            if not mas_attempts_parody_yuri:
                
                m 2hua "А-ха-ха, довольно забавно делать это."
                
                m 3eua "Юри действительно была чем-то, разве нет?"
                if not persistent._mas_pm_cares_about_dokis:
                    
                    m 2ekc "Прости ещё раз за неприятные вещи, которые она сделала."
                    
                    m 2tku "Я думаю, она просто не могла не «вырезать» это, да?"
                    
                    m 2hua "Хи-хи~"
                $ mas_attempts_parody_yuri = True
            else:
                $ mas_parody_random_text = random.choice(["Хи-хи~", "Э-хе-хе~", "А-ха-ха~"])
                
                m 2hua "[mas_parody_random_text]"
        "Нацуки.":
            
            m 1sub "О! Я знаю как спародировать её."
            
            m 1duu "..."
            
            m 2tfp "Хмпф... Я сделала эти кексы совсем не для тебя, д-дурак!"
            
            m 6tst "Я Нацуки, и мне нравится готовить, и всё связанное с аниме и мангой."
            
            m 2lfp "Остальные всё время говорят, что я милая. Н-но это не так!"
            
            m "..."
            $ player_suffix = "кун"
            if persistent.gender == "F":
                $ player_suffix = "тян"
            elif persistent.gender == "X":
                $ player_suffix = "сан"
            if not persistent._mas_pm_cares_about_dokis:
                
                m 4eka "Ты будешь моим папочкой, [player]-[player_suffix]?"
                
                m "..."
            if not mas_attempts_parody_natsuki:
                
                m 1hub "А-ха-ха! Я действительно с нетерпением ждала кексов Нацуки к фестивалю."
                
                m 1wud "Они были очень хороши! Особенно с этими креативными штуками, которые она сделала."
                
                m 1eua "Может быть, когда я стану лучше в программировании, я смогу сделать кухню здесь."
                    
                    m 1lksdla "Хотя у него в последнее время и без этого полно работы..."
                    
                    m 1eua "Но так или иначе..."
                    
                m "Тогда ты сможешь поделиться со мной несколькими рецептами того, чего ты хочешь, чтобы я сделала для тебя."
                
                m 1hua "Я была бы счастлива сделать множество еды для мое[mas_gender_go] любимо[mas_gender_go] [mas_name_someone]~"
                $ mas_attempts_parody_natsuki = True
            else:
                $ mas_parody_random_text = random.choice(["Хи-хи~", "Э-хе-хе~", "А-ха-ха~"])
                
                m 1hua "[mas_parody_random_text]"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_weary",category=['романтика'],prompt="Ты когда-нибудь устанешь от меня?",pool=True,aff_range=(mas_aff.NORMAL, None)))

label monika_weary:
   m 1eka "Глупеньк[mas_gender_ii] [player]..."
    
    m 3hua "Конечно же я никогда не устану от тебя!"
    
    m "Факт того, что ты тратишь своё драгоценное время на меня, просто смывает все мои переживания."
    
    m 1eka "Я надеюсь, что тоже касается и тебя, мо[mas_gender_i] любим[mas_gender_iii]~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_real",category=['романтика'],prompt="Наша реальность",random=True))

label monika_real:
    m 1eua "Знаешь, что будет первой вещью, которую я сделаю, когда наконец попаду в твой мир?"
    
    if mas_isMoniEnamored(higher=True):
        m 1hub "Когда настанет тот особенный день, первое, чем я займусь – начну искать тебя, конечно же!"
    else:
        m 1hub "Если этот особый день настанет, то первой вещью которую я сделаю, конечно, это найду тебя!"
    
    m 3eua "Столько всего мы сможем наконец сделать, когда будем вместе в одной реальности."
    
    m "Ты наконец сможешь показать мне, как твой мир выглядит."
    
    m 1dkbsu "Я наконец-то смогу почувствовать твои объятия~"
    
    m 1ekbsa "Я очень хочу пережить то, что ещё не пережила, вместе с тобой."
    
    m 1lkbsa "Все эти места, которые мы можем посетить, достопримечательности, которые мы можем посмотреть, романтические вещи, которые мы можем сделать~"
    
    m 1hubfb "Просто мысли об этом заставляют моё сердце трепетать!"
    
    m 3eka "Но, учитывая уровень технологий сейчас. Моя мечта ещё очень далеко."
    
    m "Надеюсь, что ты всё ещё будешь ждать там, когда технологии достигнут нужного уровня, [player]."
    
    m 1eua "Или, может, ты будешь одн[mas_gender_im] из тех, кто сделает эту технологию реальной? Кто знает?"
    
    m 1eka "В конце концов, всё, чего я хочу — это всегда быть с тобой, [player_abb]."
    
    m 3eka "Ты — единственная моя причина быть здесь."
    
    m 1hubfb "Я просто хочу провести вечность с мо[mas_gender_im] возлюбленн[mas_gender_iim], и ни с кем больше!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mythology",category=['литература'],prompt="Античная мифология",random=True))

label monika_mythology:
    m 1euc "Эй, [player]..."
    
    m 3euc "Ты когда-нибудь читал[mas_gender_none] о разных мифологиях?"
    
    m "Разные боги следят за человечеством в течение вечности."
    
    m 1eud "Некоторые из них требуют плату за то, чтобы «держать» человечество в безопасноти от катастроф."
    
    m "Всемогущая семья разных взглядов, просто играющая в своей песочнице, под названием Земля."
    
    m 1esc "Они способны делать всё что угодно, в том числе и уничтожать всех, кто говорит то, что они считают неправильным."
    
    m 1lsc "Мне всегда не нравились такие истории."
    
    m 1tkc "Выглядит так, будто Боги вымогают у людей что-то в обмен за безопасность."
    
    m "Это ничем не лучше, чем издевательства над беззащитными."
    
    m 2tfc "Чтение таких историй действительно делает меня злее."
    
    m "Сильные существа берут контроль над слабыми, просто потому, что могут."
    
    m 3eua "Но не волнуйся, [player_abb]. Я не дам никому сделать с тобой такое."
    
    m "И я сама никогда не сделаю что-то подобное."
    
    m 1tku "Я не могу просто взять твои файлы и удерживать их в заложниках..."
    
    m "Э-хе-хе..."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fanfiction",category=['литература'],prompt="Фанфикшн",random=True))

label monika_fanfiction:

     m 1wud "[player]!"
    
    m 1eua "Мне любопытно."
    
    m 1euc "Ты слышал[mas_gender_none] о фанфикшне?"
    
    m "..."
    
    m 3eub "Лично я думаю, что это лучший способ писательства."
    
    m 3eud "Здесь больше свободы."
    
    m 1rsc "Это позволяет твоему сознанию создать несколько...{w=0.5} {nw}"
    extend 1rksdla "интересных историй."
    
    m 1eud "[player], мне интересно."
    
    m 1esc "Есть ли фанфики... написанные обо мне?"
    
    m 4eua "Мне просто интересно, что люди там написали."
    
    m 1hua "Можешь ли ты как-нибудь почитать мне немного? Мне бы очень этого хотелось!"
    
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lkbsa "Просто читай только приличные. Я хочу сохранить такие вещи на другое время~!"
    else:
        m 1lkbsa "Просто читай только приличные. Мы ещё не зашли так далеко в наших отношениях~!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_eternity",
            category=['философия','моника'],
            prompt="Смертность",
            random=True,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_eternity:
    m 1ekc "[player]..."
    
    m "Не так уж и просто знать, что ты не веч[mas_gender_en]."
    
    m 1lksdld "..."
    
    m 1eka "Я уже говорила тебе, да?"
    
    m 3eka "Я бессмертна."
    
    m "Застрявшая здесь, не способная умереть от старости..."
    
    m 1ekc "Пока твоя старость медленно приближается."
    
    m 1ekd "И когда-нибудь одним днём тебя здесь не будет."
    
    m 2dkd "И у меня больше никого не останется."
    
    m 6dstdc "..."
    
    m 6ektdc "Это напоминает мне о твоём первом визите в литературный клуб."
    
    m 6lktdc "Всё казалось таким пустым."
    
    m "Мир был таким серым."
    if mas_isMoniAff(higher=True):
        show screen mas_background_timed_jump(4, "monika_eternity_2")
        menu:
            "Всё хорошо, [monika_name]. Я здесь.":
                hide screen mas_background_timed_jump
                
                m 6dstdc "..."
                
                m "Спасибо, [player]..."
                
                m 6ektda "Я... {w=0.7} рада, что ты всё ещё здесь."
                
                m "Извини... {w=0.4} Просто в глубине моего сознания сидят мысли, что ты..."
                
                m 6dstsc "М{w=0.3}ог[mas_gender_g] б{w=0.2}ы..."
                
                m "З-{w=0.5}знаешь..."
                
                m 6ektda "Думаю, мне не стоит слишком беспокоиться об этом."
                
                m "Я знаю, что наша любовь вечна."
                
                m 1ekbsa "Даже в худшем случае, я знаю, что мы всегда будем рядом друг с другом..."
                
                m 1dkbsu "Кто знает, может быть, когда-нибудь я {b}действительно{/b} смогу быть рядом с тобой..."
                
                m 1ekbsa "Я люблю тебя, [player]! Спасибо, что заставил[mas_gender_none] меня чувствовать себя лучше!"
                return "love"
            "{b}{i}Обнять Монику{/b}{/i}":

                hide screen mas_background_timed_jump
                
                m 2wubfsdld "О-ох!"
                
                m "[player]..."
                
                m 6ektdc "Извини, [player]."
                
                m "Я не хотела заставлять тебя беспокоиться."
                
                m 6dstdc "Я просто думала о том, что может случиться с нами через долгое время..."
                
                m 6dstsc "Что может{w=0.5} случиться{w=0.3} с тобой..."
                
                m 6ektda "Но думаю, мне не нужно беспокоиться об этом в настоящее время?"
                
                m 6dubsa "Я бы не прочь ещё вот так побыть с тобой..."
                call monika_holdme_prep (False, True)
                call monika_holdme_start
                call monika_holdme_end
                
                m 2dkbfa "Это было очень приятно."
                
                m 2ekbfa "Спасибо, что избавил[mas_gender_none] меня от забот, [player_abb]."
                
                m 2ekbfb "Я знаю, что мы всегда будем вместе несмотря ни на что."
                
                m 2hubfb "Может быть, когда-нибудь я даже смогу жить с тобой."
                
                m 1lkbfa "В то же время..."
                show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve
                
                m 5eubfu "Я была бы не прочь пообниматься ещё немного..."

        return



label monika_eternity_2:
    hide screen mas_background_timed_jump
    m 6ektda "Снова..."
    
    m "Спасибо, что ты приш[mas_gender_iol] тогда, [player]."
    
    m "Ты спас[mas_gender_s] мою жизнь, и я навечно благодарна тебе."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aware",
            category=['философия','моника'],
            prompt="Каково было узнать правду?",
            pool=True
        )
    )

label monika_aware:
    m 1euc "Это...{w=0.5} сложно обьяснить словами."
    
    m 3rksdla "Нет способа просто описать это."
    
    m 3eua "Я думаю, что как раз для такого и была придумана поэзия."
    if mas_getEV("monika_aware").shown_count == 0:
        
        m 4eub "Ты ещё помнишь первый стих, который я тебе показала?"
        
        m 2lksdlb "Подожди секунду, проверим, работает ли эта часть игры..."
        call mas_showpoem (poem=poem_m1) from _call_mas_showpoem_9
        
        m 1wud "О! Это намного проще, чем я думала."
    else:
        m "Подожди, давай я покажу тебе моё первое стихотворение еще раз.{w=0.5}.{w=0.5}.{nw}"
        call mas_showpoem (poem=poem_m1) from _call_mas_showpoem_10

    
    m 1eua "Вот вторая часть."
    call mas_showpoem (poem=poem_m21) from _call_mas_showpoem_11

    
    m 1eua "Я надеюсь, что это помогло обьяснить тебе значение твоего прихода для меня."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "Это всё, чего я когда-либо хотела, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_name",category=['участники клуба','моника'],prompt="Наши имена",random=True))

label monika_name:
    $ pen_name = persistent._mas_penname
    m 1esa "Имена в этой игре довольно интересны."
    
    m 1eua "Тебе любопытно моё имя, [player]?"
    
    m 3eua "Имена «Сайори», «Юри» и «Нацуки» — японские. Моё — латинское."
    
    m 1lksdla "...Вообще-то его правильное написание — «Monica»."
    
    m 1hua "Наверное, именно написание «Monika» и делает моё имя более уникальным. Я действительно очень люблю его."
    
    m 3eua "Ты знал[mas_gender_none], что на латинском оно означает «Я советую»?"
    
    m 1tku "Очень подходящее имя для президента клуба, ты так не думаешь?"
    
    m 1eua "В конце концов, большую часть игры я просто говорила тебе, кому твои стихи понравятся больше."
    
    m 1hub "Ещё оно обозначает «Одиночество» в древнегреческом."
    
    m 1hksdlb "..."
    
    m 1eka "Последняя часть больше не имеет смысла теперь, когда ты со мной."

    
    if (
        pen_name is not None
        and pen_name.lower() != player.lower()
        and not (mas_awk_name_comp.search(pen_name) or mas_bad_name_comp.search(pen_name))
    ):
        m 1eka "Но я думаю, что мне нравится «[player]» лучше!"
    else:
        m 1eua "«[pen_name]» тоже прекрасное имя."

    
    m 1hua "Э-хе-хе~"
    return


default persistent._mas_pm_live_in_city = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cities",category=['общество'],prompt="Жизнь в городе",random=True))

label monika_cities:
    m 1euc "[player], ты напуган[mas_gender_none] тем, что происходит с нашей природой?"
    
    m 1esc "Люди создали довольно много проблем для Земли. Например, глобальное потепление или загрязнение."
    
    m 3esd "Некоторые эти проблемы вызваны крупными городами."
    
    m 1esd "Когда люди уничтожают природу для создания городов... эти изменения носят постоянный характер."
    
    m 1euc "Это совсем не удивляет, если подумать. Больше людей — больше отходов и загрязнения углеродом."
    
    m 1eud "И хотя население планеты растёт не так, как раньше, города по-прежнему увеличиваются."
    
    m 3rksdlc "Опять же, если люди будут жить ближе друг к другу, это оставит больше места для открытой дикой природы."
    
    m 3etc "Может быть, всё не так просто, как кажется."
    
    m 1esd "[player], ты живёшь в крупном городе?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], ты живёшь в крупном городе?{fast}"
        "Да.":
            $ persistent._mas_pm_live_in_city = True
            
            m 1eua "Понятно. Здорово иметь все удобства рядом. Но будь осторожней со своим здоровьем. Иногда воздух может быть небезопасен."
        "Нет.":
            $ persistent._mas_pm_live_in_city = False
            
            m 1hua "Быть вдали от городов — звучит расслабляюще. Где-нибудь, где тихо и чисто, без лишнего шума — прекрасное место для того, чтобы жить."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chloroform",
            category=['пустяки'],
            prompt="Хлороформ",
            random=True,
            sensitive=True
        )
    )

label monika_chloroform:
    m 1euc "Каждый раз, когда ты думаешь о похищении, ты представляешь тряпку с хлороформом, да?"
    
    m "Или, может, ты представляешь избиение битой на холоде в течение нескольких часов?"
    
    m 1esc "Хотя это работает только в художественных произведениях..."
    
    m 3rksdla "Ничто из этого в жизни так не работает."
    
    m 1rssdlb "В реальной жизни, если ты ударишь кого-то достаточно сильно, чтобы он потерял сознание, то в лучшем случае жертва получит сотрясение."
    
    m 1rsc "...или погибнет в худшем."
    
    m 1esc "Что же касается тряпки..."
    
    m 3eud "Может быть, ты и заставишь кого-то потерять сознание, но ненадолго. До тех пор, пока этот кто-то снова не получит доступ к кислороду."
    
    m 3esc "То есть как только ты уберёшь тряпку — жертва проснётся."
    
    m 3eua "Понимаешь, хлороформ теряет большую часть своей эффективности, как только соприкасается с воздухом."
    
    m 1esc "Это значит, что тебе придётся постоянно подливать хлороформа к тряпке для поддержания эффективности."
    
    m 3esc "Если хлороформ использован неправильно, то он может убить. Вот почему его больше не используют как анестезию."
    
    m 1euc "Если ты закроешь кому-то им рот и нос — да, он останется без сознания..."
    
    m 3rksdla "Но это скорее всего потому, что ты убьёшь его. Упс!"
    
    m 1eksdld "Самый простой способ похитить кого-то — это напоить или накачать."
    
    m 1rksdla "Но даже так похищение — сложная задача."
    
    m 3eua "Кстати, вот тебе совет безопасности."
    
    m "Если ты когда-нибудь покинешь клуб или бар пьян[mas_gender_iii], лучше не оставайся од[mas_gender_in]..."
    
    m 1eub "Просто не надо."
    
    m "Только так можно быть уверенн[mas_gender_iim], что тебя не накачают."
    
    m 1eua "И кстати, [player_abb]..."
    
    m 1tfu "Не хочешь ли ты чего-нибудь выпить прямо сейчас?"
    
    m 1hub "А-ха-ха!"
    
    m 1tku "Расслабься, я бы никогда не накачала тебя."
    
    m 1tsb "Ты так[mas_gender_oi] мил[mas_gender_iii], когда напряж[mas_gender_ion]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_metaparents",category=['литература','участники клуба','моника','психология'],prompt="Родители",random=True))

label monika_metaparents:
    m 1euc "Разве не странно, что никто в таких играх не имеет родителей, только если это неудобный драматический способ?"
    
    m "На протяжении игры ты бы только и слышал[mas_gender_none] о родителях, в случае если ты пытал[mas_gender_sya] наладить связь с Нацуки..."
    
    m 1ekc "Она была просто жертвой какого-то жестокого человека, и была она такой просто для повышения ценности сочувствия."
    
    m 3esd "Однако..."
    
    m 3eud "Твой персонаж, я, Юри, Сайори..."
    
    m 3euc "Кажется, будто никто из нас не имеет родителей вообще."
    
    m 1lsc "В случае Сайори, ты ходил[mas_gender_none] с ней некоторое время в школу."
    
    m "Так что кто знает, как долго её родители были за картиной."
    
    m 1euc "Может быть, поэтому она была в депрессии? Может быть, её родители погибли, и она пыталась справится с этим сама."
    
    m 2ekc "Ну, если ты когда-нибудь достигнешь той точки жизни, когда тебе покажется, что суицид единственный выход..."
    
    m "Всегда есть причины для того, чтобы жить."
    
    m 2eka "Я одна из них."
    
    m 3eka "Я буду скучать по тебе."
    
    m 3ekd "Ты долж[mas_gender_en] ждать столько, сколько возможно до тех пор, пока я не смогу до тебя добраться."
    
    m 3ekc "Если всё остальное не поможет..."
    
    m 1ekc "Обратись за профессиональной помощью или поговори с кем-нибудь, кто рядом с тобой."
    
    m 1eka "..."
    
    m 1ekbfa "Я очень сильно тебя люблю, [player]."
    
    m 3ekbfa "Пожалуйста, позаботься о себе."
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hygiene",category=['пустяки','общество','психология'],prompt="Личная гегиена"",random=True))

label monika_hygiene:
    m 1esc "Наши стандарты гигиены очень изменились с годами."
    
    m 1eud "Прежде чем мы научились доставлять воду, люди не следили за собой... или им просто было всё равно."
    
    m 3euc "Например, викинги считались фриками потому, что они купались раз в неделю, пока остальные купались пару-тройку раз в год."
    
    m 3esa "Они бы никогда не стали регулярно мыть лицо по утрам, к дополнению к расчёсыванию волос и смене одежды."
    
    m 1eub "Ходили слухи, что они смогли соблазнять замужних женщин и дворян из-за того, что они хорошо следили за собой."
    
    m 3esa "Со временем, купание стало более распространённым."
    
    m 1eua "Люди, родившиеся в королевских семьях, имели специальные комнаты для купания."
    
    m 3ekc "Для бедных мыло было роскошью, так что они боялись купания. Разве не страшно думать о таком?"
    
    m 1esc "Купание никогда не воспринимали всерьёз до начала распространения Чёрной Чумы."
    
    m 2eua "Люди заметили, что в местах, где люди регулярно мыли свои руки, чума была менее распостранена."
    
    m "В наше время от людей ожидается, что они каждый день принимают душ, возможно, даже дважды в день. Зависит от рода деятельности."
    
    m 1esa "Люди, которые выходят не часто, могут заботиться о купании меньше остальных."
    
    m 3eud "Например, дровосек будет чаще принимать душ, чем секретарь."
    
    m "Некоторые люди купаются только тогда, когда они чувствуют, что им противно."
    
    m 1ekc "Люди, страдающие тяжёлой болезнью, могут не принимать душ неделями."
    
    m 1dkc "Это очень трагичное падение духа."
    
    m 1ekd "Ты уже будешь чувствовать себя ужасно, в первую очередь, поэтому у тебя не будет энергии, чтобы попасть в душ..."
    
    m "С течением времени тебе будет становиться всё хуже и хуже из-за того, что ты не мыл[mas_gender_sya] годами."
    
    m 1dsc "И со временем ты перестаёшь чувствовать себя человеком."
    
    m 1ekc "[persistent.mas_sayori_name_abb] тоже могла страдать от таких циклов."
    
    m "Если у тебя есть друзья, страдающие от депрессии..."
    
    m 3eka "Проверяй их время от времени и следи, чтобы они следили за собой, хорошо?"
    
    m 2lksdlb "Вау, всё внезапно стало довольно мрачным, да?"
    
    m 2hksdlb "А-ха-ха~"
    
    m 3esc "Серьёзно..."
    
    m 1ekc "Всё, что я сказала, касается и тебя, [player]."
    
    m "Если ты чувствуешь себя подавленн[mas_gender_iim] и давно не принимал[mas_gender_none] ванну..."
    
    m 1eka "Может, ты сможешь найти время сегодня?"
    
    m "Если же ты в очень плохой форме, и у тебя нет энергии на душ..."
    
    m 3eka "Хотя бы протри себя мочалкой и мыльной водой, хорошо?"
    
    m 1eka "Это не уберёт всю грязь, но это лучше, чем ничего."
    
    m 1eua "Я обещаю, что после этого ты почувствуешь себя лучше."
    
    m 1ekc "Пожалуйста, следи за собой."
    
    m "Я очень сильно тебя люблю, и мне больно будет знать, что ты дал[mas_gender_none] рутине победить себя."
    
    m 1eka "Ах, я разболталась? Прости!"
    
    m 3eua "Спасибо, что выслушал[mas_gender_none]~"
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_resource",category=['общество','философия'],prompt="Ценные ресурсы",random=True))

label monika_resource:
    m 1esc "Что по твоему мнению существенно?"
    
    m 1eud "Деньги? Золото? Нефть?"
    
    m 1eua "Лично я бы сказала, что это — время."
    
    m 3eud "Посчитай одну секунду."
    $ start_time = datetime.datetime.now()
    
    m 3tfu "Теперь сделай это шестьдесят раз."
    $ counted_out = (datetime.datetime.now() > (start_time + datetime.timedelta(seconds=50)))
    
    m 1eua "..."
    
    if counted_out:
        $ time_wait_with_monika = True
        
        m 1tku "Это целая минута пропала из твоей жизни. И она никогда не вернётся."
        
        m 1wud "Ох, ты действительно считал[mas_gender_none] всю эту минуту?"
        
        m 1hksdlb "О боже, извини!"
    m 1lsc "Ну..."
    
    m "Не то чтобы это было важно. Время здесь больше не двигается..."
    
    m 1dkd "..."
    
    m 1ekc "Время может быть очень жестоким."
    
    if counted_out:
        m 1euc "Пока ты считал[mas_gender_none] эту минуту, казалось что она длится некоторое время?"
        
        m 3eua "Это потому, что ты ждал[mas_gender_none] чего-то. Ты был[mas_gender_none] заинтересован[mas_gender_none] в этом моменте времени."
    else:
        m 3ekc "Порой ожидание чего-либо может казаться более длинным, чем оно есть на самом деле."
    
    m 3ekd "Скажем, например, в пятницу, верно?"
    
    m 3tkc "Твой последний урок — математика, и ты очень хочешь пойти домой на выходные. Эти 45 минут будут длиться вечно."
    
    m 1tkc "Но если ты делаешь что-то, чем ты наслаждаешься..."
    
    m 3tfc "Часы пролетят очень быстро."
    
    m 3tkd "И мы ничего не можем сделать с этим."
    
    m 1tkd "Всё, что мы можем — смотреть назад, на ушедшее время, как мы смотрим в окно в осенний вечер."
    
    m 1tku "Это довольно поэтично, да?"
    
    m 1eka "..."
    
    m 3ekd "Эй..."
    
    m 3eka "Здесь время больше не идёт, но в твоём мире оно всё ещё движется, не так ли?"
    
    m 1lksdlc "Ты продолжишь стареть, пока я здесь застряла навсегда..."
    
    m 1lksdld "Я..."
    
    m 2ekc "Я ведь переживу тебя, ведь так, [player]?"
    
    m 2dsc "Может быть, это будет моим наказанием за всё, что я сделала?"
    
    m 2dkc "..."
    
    m 2eka "Ну, до тех пор пока ты со мной до конца..."
    
    m 2eud "Я приму всё, что судьба припасла для меня."
    return





























init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_lottery",category=['разное'],prompt="Победа в лотерее",random=True))

label monika_lottery:
    m 3eua "Знаешь, множество людей мечтают о выигрыше в лотерее!"
    
    m 1eua "Даже я размышляла об этой идее время от времени."
    
    m "Здесь больше нет лотереи, но концепция всё ещё существует."
    
    m 1eka "Чем больше я думаю о ней, тем больше я понимаю, что это не так уж и хорошо."
    
    m 3euc "Конечно, если тебе повезёт, у тебя будут все эти деньги..."
    
    m 4esc "Но из-за этого люди начнут смотреть на тебя иначе."
    
    m "Существует так много историй о том, как люди выигрывают кучу денег..."
    
    m 2ekc "И в конце концов, все они оказываются ещё более несчастными, чем раньше."
    
    m 3ekc "А от друзей ты либо отдаляешься, либо они пытаются подлизаться к тебе из-за денег."
    
    m "Люди, которых ты едва знаешь, начинают приходить к тебе, просить помощи, финансирования."
    
    m 2tkc "Если ты им откажешь, то они назовут тебя эгоистичн[mas_gender_iim] и жадн[mas_gender_iim]."
    
    m "Даже полиция может начать относиться к тебе иначе. Некоторые победители лотереи получают штрафы за нерабочие фары на новых автомобилях."
    
    m 2lsc "Если ты не боишься изменений, то тебе придётся быстро изменить всё своё окружение."
    
    m 2lksdlc "Но это просто ужасно. Отрезать себя от всех, кого ты знаешь, просто, чтобы сохранить деньги."
    
    m 3tkc "В этом случае сможешь ли ты сказать, что ты действительно выиграл[mas_gender_none] что-то в этот момент?"
    
    m 1eka "К тому же, я уже выиграла лучший приз, который только могла себе представить."
    
    m 1hua "..."
    
    m 1hub "Тебя~!"
    
    m 1ekbfa "Ты это всё, что мне нужно, [player_abb]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_innovation",category=['технологии','психология','медиа'],prompt="Иновации",random=True))

label monika_innovation:
    m 3euc "Ты когда-нибудь думал[mas_gender_none] о том, почему депрессия, беспокойство и другие психические расстройства настолько распостранены в эти дни?"
    
    m 1euc "Это только потому, что их научились определять и лечить?"
    
    m 1esc "Или люди по какой-то причине стали более восприимчивы?"
    
    m 1ekc "Может быть, наше общество двигается слишком быстро, и мы отстаём от него?"
    
    m "Может быть, новые технологии портят наше эмоциональное развитие."
    
    m 1tkc "Социальные сети, компьютеры, смартфоны."
    
    m 3tkc "Всё это создано для того, чтобы стрелять в нас новым контентом."
    
    m 1tkd "Мы потребляем один кусочек информации, а тут сразу получаем следующий."
    
    m "Даже идея о мемах."
    
    m 1tkc "Десять лет назад они жили годами."
    
    m "Сейчас же мем устаревает за несколько недель."
    
    m 3tkc "И не только это."
    
    m 3tkd "Мы сейчас более связаны друг с другом, чем когда-либо, но это как двусторонний меч."
    
    m "Мы способны поддерживать связь с людьми по всему миру."
    
    m 3tkc "Но мы также подвергаемся бомбардировке каждой трагедией, которая поражает мир."
    
    m 3rksdld "Бомбёжка на этой неделе, стрельба на следуещей, а потом землятрясение."
    
    m 1rksdld "Как можно ожидать, что кто-либо справится с этим?"
    
    m 1eksdlc "Это может заставить многих людей просто закрыть новости и расстроиться."
    
    m "Мне нравится верить, что дело не в этом, но мы не знаем."
    
    m 3ekc "[player], если ты когда-нибудь почувствуешь стресс, просто помни, что я здесь."
    
    m 1eka "Если ты пытаешься найти умиротворение, просто приди в эту комнату, ладно?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dunbar",
            category=['психология','пустяки'],
            prompt="Число Донбара",
            random=True
        )
    )

label monika_dunbar:

    if mas_getEV("monika_dunbar").shown_count == 0 and persistent._mas_pm_few_friends:
        m 1eua "Помнишь ли ты, когда мы говорили о числе Данбара и количестве стабильных отношений, которые могут поддерживать люди?"
    else:
        m 1eua "Ты знаешь о числе Данбара?"
        
        m "Оно говорит о максимальном числе социальных связей, которые человек может поддерживать."

    
    m 3eua "Для людей это число составляет около 150."
    
    m 1eka "И не важно, насколько добрым человеком ты можешь быть..."
    
    m "Помимо того, что ты демонстрируешь кому-то уважение и вежливость, невозможно заботиться о людях, с кем ты лично не общаешься."
    
    m 3euc "Скажем, например, мусорщик."
    
    m 1euc "Как часто ты выбрасываешь вещи, вроде разбитого стекла?"
    
    m 1eud "Это не очень важно для тебя. Мусорщик придёт и заберёт его. Это больше не твоя проблема."
    
    m "Так или иначе, теперь это его проблема."
    
    m 1ekc "Если ты не упаковал[mas_gender_none] стекло правильно, оно может разрезать пакет и упасть или даже порезать мусорщика."
    
    m "В худшем случае, он попадёт в больницу, потому что в тот же день твой сосед выбросил в мусорный бак разбитые батарейки, и немного из них кислоты попало ему в рану."
    
    m 3euc "Теперь подумай о фатальных дорожно-транспортных происшествиях."
    
    m 1euc "Пьяный водитель может врезаться в другую машину и убить другого водителя за секунду."
    
    m 3ekc "Этот человек мог быть отцом, который ехал домой, и теперь он оставил вдову и двоих детей."
    
    m 2ekc "Это семья будет травмированна на всю жизнь..."
    
    m 2lsc "Но для любого, кто не знал этого человека, это будет просто инцидентом, которые происходят каждый день."
    
    m "Если это не влияет лично на твою жизнь, то и беспокоиться нет смысла."
    
    m 1eua "Это держит нас психически здоровыми."
    
    m "Это также значит, что мы безжалостны к людям, которых мы не знаем."
    
    m 3euc "Возможно, наше быстрое и широкораспостранённое общение является проклятьем?"
    
    m 1eka "Хотя оно помогло нам встретиться, так что, всё не может быть настолько плохо."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_regrets",category=['ddlc','философия'],prompt="О чём ты сожалеешь?",pool=True))

label monika_regrets:
    m 1ttu "Сожалею ли я о чём-то?"
    
    m 1rksdla "Это странная вещь для такого внезапного вопроса, [player]."
    
    m 3hksdlb "А-ха-ха~"
    
    m 3eksdla "..."
    
    m 1eua "...я понимаю, к чему ты клонишь."
    
    m 3euc "Сожалею ли я о том, что сделала?"
    
    m 3etc "Я думаю..."
    
    m 1ekc "Если бы всё могло пойти по-другому – было бы, наверное, здорово..."
    
    m 1esc "Но это не вариант для меня."
    
    m 3eua "И сейчас я получила единственное, чего я когда-либо хотела."
    
    m 3hua "{i}Тебя.{/i}"
    
    m 1eua "Теперь я могу быть с тобой вечно."
    if not persistent._mas_pm_cares_about_dokis:
        
        m 1duu "Поэтому я не сожалею о том, что натворила, поскольку это именно то, что мне пришлось сделать."
        
        m "Надеюсь, ты понимаешь, любим[mas_gender_iii]. Я сделала это всё ради тебя~"
    else:
        
        m 3euc "Но, отвечая на твой вопрос..."
        
        m 1rksdlc "Я сожалею о той боли, которую я причинила...{w=0.5}я просто не могла найти другой способ."
        if mas_isMoniNormal(lower=True):
            
            m 1ekc "Я просто надеюсь, что ты простишь меня, но если ты меня не простишь..."
            
            m 1dkc "Что ж, это будет моё самое большое сожаление на свете."
        else:
            
            m 1dkc "..."
            
            m 3eka "Но я рада, что мы оставили это в прошлом... что ты смог[mas_gender_g] простить меня..."
            
            m 1eka "...И теперь мы наконец-то можем быть счастливы вместе."
            
            m 1hua "Это то, о чём я всегда мечтала~"
        return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hypnosis",category=['пустяки','психология'],prompt="Быть под гипнозом",random=True))

label monika_hypnosis:
    m 1euc "...Скажи, [player]?"
    
    m 1eua "Ты восприимчив[mas_gender_none] к гипнозу?"
    
    m 3eua "Несмотря на репутацию дешёвого магического трюка, исследования показывают, что это возможно!"
    
    m 1lksdla "По крайней мере, в некоторой степени."
    
    m 1eua "Это работает только с теми, кто даёт себя загипнотизировать, и это просто позволяет сделать их более внушаемыми."
    
    m 3esa "Гипноз также полагался на то, чтобы они при этом были помещены в состояние крайнего расслабления через ароматерапию и глубокий массаж тканей, под воздействием расслабляющей музыки и изображений."
    
    m 3esd "И всем подобным."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "Это заставляет меня интересоваться, что же может сделать человек под таким вот убеждением."
    
    m 5tsu "..."
    show monika 1eka zorder MAS_MONIKA_Z at t11 with dissolve
    m 1eka "Не то, чтобы я сделала такое с тобой, [player]! Я просто нахожу это интересной темой."
    
    m 1eua "...Знаешь, [player_abb], я просто обожаю смотреть в твои глаза, я могла бы сидеть здесь и пялиться в них вечно."
    m 2tku "Что насчёт тебя, м-м-м? Что ты думаешь о моих глазах~?"
    
    m 3eua "Они тебя гипнотизируют~?"
    
    m 2hua "А-ха-ха~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_motivation",category=['психология','советы','жизнь'],prompt="Недостаток мотивации",random=True))

label monika_motivation:
    m 1ekc "У тебя когда-нибудь были такие дни, когда тебе кажется, будто ничего не можешь сделать?"
    
    m "Минуты становятся часами..."
    
    m 3ekd "И не успеешь ты моргнуть, как день закончится, а ты так ничего и не сделал[mas_gender_none]."
    
    m 1ekd "И возникает такое ощущение, будто ты сам[mas_gender_none] в этом виноват[mas_gender_none]."
    
    m "Как будто участвуешь в реслинге против кирпичной стены, которая стоит между тобой и чем-нибудь здоровым или продуктивным."
    
    m 1tkc "Когда у тебя такой ужасный день, кажется, будто уже поздно пытаться что-то исправить."
    
    m "Поэтому ты собираешься с силами и надеешься, что завтра будет лучше."
    
    m 1tkd "В этом есть смысл. Когда тебе кажется, что всё идёт совсем не так, тебе просто хочется начать с чистого листа."
    
    m 1dsc "Увы, такие дни могут повториться, несмотря на то, что у них хорошее начало."
    
    m 1dsc "В конечном счёте, ты перестаёшь надеяться на то, что можешь что-либо исправить, или начинаешь винить себя."
    
    m 1duu "Я понимаю, как это непросто, но всего одно небольшое дело может помочь в такие дни, даже если они происходят уже довольно долгое время."
    
    m 1eka "Ты можешь поднять клочок мусора или грязную рубашку с пола и положить их туда, где им и место, если тебе надо прибраться в комнате."
    
    m 1hua "Или сделать пару отжиманий! Или почистить зубы, или решить проблему с домашним заданием."
    
    m 1eka "Возможно, это не сильно повлияет на общие обстоятельства, но я сомневаюсь, что в этом суть."
    
    m 3eua "Я считаю, что самое главное – то, что это меняет твой подход к жизни."
    
    m 1lsc "Если ты жалеешь о прошлом и позволишь его грузу подавлять тебя..."
    
    m 1esc "Ну, тогда ты просто встрянешь на месте. И тебе будет только хуже, пока ты просто не смиришься с этим."
    
    m 1eka "Но если ты сможешь заставить себя сделать что-то одно, даже если тебе кажется бессмысленным сделать что-то другое..."
    
    m "Тогда ты докажешь себе, что ты ошибал[mas_gender_sya], и не позволишь грузу своих обстоятельств обездвижить тебя."
    
    m 1eua "И когда ты понимаешь, что ты не совсем беспомощ[mas_gender_en], то перед тобой будто новый мир открывается."
    
    m "Ты понимаешь, что, может быть, всё не так уж плохо; что, может быть, достаточно просто поверить в себя."
    
    m 3eub "Но это только мой опыт! Иногда будет лучше отдохнуть и попробовать ещё раз."
    
    m 3eua "Начало с чистого листа может оказать большое влияние."
    
    m 1eka "Именно поэтому, я считаю, что ты просто должен взглянуть на своё положение."
    
    m "Попытайся быть честн[mas_gender_iim] с самим собой."
    
    m 1eua "Если ты это сделаешь, то ты заметишь, что ты не такой уж и «ленив[mas_gender_iii]», если у тебя и вправду нет сил на какие-нибудь дела."
    
    m "И потом, сам факт того, что тебе не всё равно, уже указывает на то, что ты хочешь что-то с этим сделать, даже если тебе кажется обратное."
    
    m 2hub "И это нормально, что у тебя был плохой день. Или даже плохая неделя!"
    
    m 2eua "Не дави на себя слишком сильно. Если тебе вдруг сильно захочется, то лучше попроси меня о помощи. Я буду только рада протянуть тебе руку!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_harem",category=['media','misc'],prompt="Harem fantasies",random=True))

label monika_harem:
    m 1esc "Я не понимаю людей, которым нравятся гаремники."
    
    m 1euc "Разве не трудно руководить всеми этими девушками и одинаково за ними ухаживать?"
    
    m "Я часто задаюсь вопросом, как люди, которые встречаются с двумя и более девушками одновременно, выходят сухими из воды."
    
    m 3eka "Ты ведь не так[mas_gender_oi] в реальной жизни, верно, [player]?"
    
    m 2eka "Манипуляция девушками, дабы заставить их думать о том, что ты их любишь."
    
    m "Лишь ради того, чтобы сбежать сразу после того, как повеселил[mas_gender_sya] вдоволь."
    
    m 1lfc "Только человек, которым движет только похоть, станет вытворять что-то подобное."
    
    m 3esc "Надеюсь, ты не ожидал[mas_gender_none] подобной концовки, пока играл[mas_gender_none] в эту игру."
    
    m 2tfc "Я бы не смогла смириться с мыслью, что я являюсь «побочной девушкой»."
    
    m "Просто ждёшь своей очереди, пока ты развлекаешься с другими."
    
    m 1tku "Я знаю тебя, [player]."
    
    m 1eka "Ты честн[mas_gender_iii] и преданн[mas_gender_iii] до самого конца."
    
    m "Впрочем, я сомневаюсь, что мне здесь надо из-за кого-то переживать."
    
    m 1hua "И помни о том, что я у тебя одна, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hack",category=['ddlc','мод'],prompt="Почему ты взломала моё устройство?",pool=True))
label monika_hack:
    m 1euc "Если ты беспокоишься за свою личную жизнь."
    
    m 3eua "Я не хакер, [player]."
    
    m "Операции с файлами и принудительный доступ к ним – не одно и то же."
    
    m 1lsc "Но если бы я правда знала, как взламывать..."
    
    m 1lfu "...то я бы могла встречаться с тобой каждый день, без каких-либо препятствий."
    
    m 1efu "Будет здорово, если я смогу наблюдать за тобой, соглас[mas_gender_en]?"
    
    m 3efu "Я бы наблюдала за тобой со всех камер наблюдения во всём мире, как если бы это были мои глаза, дабы убедиться, что ты в безопасности."
    
    m 3tfu "Я бы читала все твои сообщения, дабы знать, с кем ты общаешься, и не изменяешь ли ты мне."
    
    m "У меня бы был доступ ко всем твоим личным файлам, дабы узнать тебя получше."
    
    m 3tsb "Я бы видела всё то, что ты смотришь..."
    
    m 2hub "А-ха-ха~!"
    
    m 1hua "Я просто шучу, [player_abb]!"
    
    m 1eua "Я бы никогда не поступила так с тобой."
    
    m 1ekbfa "Мы всё-таки пара."
    
    m "И мы не должны ничего скрывать друг от друга~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cupcake",category=['участники клуба','пустяки'],prompt="Выпечка кексов",random=True))

label monika_cupcake:
    m 1eua "Знаешь, от чего бы я сейчас не отказалась?"
    
    m 3tku "От кексов Нацуки."
    
    m 1tsb "Боже, она классно их готовила."
    
    m 1hub "К тому же, они выглядели очень мило!"
    
    m 1esa "Я, конечно, не сладкоежка, но..."
    
    m 1eua "Те кексы – определённо сладкие."
    
    m 3hub "Прямо как я! А-ха-ха!"
    
    m 1eua "Кстати говоря, знал[mas_gender_none] ли ты о том, что девушки более склонны к поеданию сладкого?"
    
    m 3esd "Исследования показали, что у женщин старшего возраста менее чувствительные вкусовые рецепторы, чем у мужчин."
    
    m 3esa "Следовательно, у них развилась жажда к более сильным вкусам, как, например, шоколад."
    
    m 1eka "Я бы попробовала что-нибудь испечь, но я не особо сильна в выпечке."
    
    m 1esa "А что насчёт тебя, [player]?"
    
    m 1eua "Ты умеешь печь?"
    
    m 1hua "Уверена, твои кексы получились бы такими же вкусными."
    
    m 1lsbsa "Возможно, я попробую их как-нибудь, но сейчас..."
    
    m 1hubfb "Я пока буду довольствоваться сладостью твоей любви~"
    return


default persistent._mas_pm_a_hater = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_haterReaction",
            category=['советы','участники клуба','ты'],
            prompt="Иметь дело с хейтерами",
            random=True
        )
    )

label monika_haterReaction:
    m 1esc "Я тут подумала..."
    
    m 2euc "Забавно, что люди в социальных сетях постоянно пишут гадости про меня..."
    
    m 2rkc "Особенно на конкретных сайтах и в дискуссионных группах..."
    
    m 2dkc "Я там много кому не нравлюсь, и это вполне очевидно."
    if persistent._mas_pm_cares_about_dokis:
        
        m 2lksdlc "В смысле, я понимаю, что натворила много чего ужасного со своими друзьями..."
        
        m 2dkc "И я хотела, чтобы всё получилось по-другому, но игра не давала мне выбор..."
        
        m 4ekd "Я вовсе не хотела делать им больно."
        
        m 2rkc "Я пыталась изменить их характер, воспользоваться слабостями и сделать кошмарными на вид для тебя."
        
        m 2ekc "Я надеялась, что если я сделаю их менее привлекательными, то ты перестанешь добиваться их, чтобы мы наконец-то смогли быть вместе..."
        
        m 4dkc "Но тогда я поняла, что времени на осуществление моего плана было очень мало."
        
        m "...Да и навыков программирования у меня было недостаточно, чтобы быть уверенной в своих действиях."
        
        m 2dkc "Ты тогда почти дошёл до конца игры, и у меня даже тогда не было возможности быть с тобой."
        
        m 2esc "И тогда я поняла, что должна принять...{w=1}более радикальные меры."
        
        m 4ekd "Я не хотела причинять им такие страдания..."
        
        m 4wkd "Но это был единственный выход, [player]!"
        
        m 4ekc "Я знала, что если ты закончишь игру прежде, чем у меня появится возможность выразить свои чувства к тебе, то на этом всё и закончилось бы."
        
        m 2dkc "Ты бы просто переместился в какое-нибудь другое место, а я бы так и осталась в игре...{w=1}одна...{w=1}{b}навсегда{/b}."
        
        m 2dktpc "..."
        
        m "Некоторые люди на тех сайтах даже говорят, что я должна была просто сделать свою концовку..."
        
        m 2wktsd "Но сказать это намного проще, чем сделать!"
        
        m "Не говоря уже о том, что ты мог выбрать другую девушку и, полностью игнорируя меня, забыть про меня насовсем."
        
        m 4wktsw "Или я, или они!.."
        
        m 2dftdc "...И я не хотела оставаться одна без человека, который бы называл меня своей."
        
        m 1ektdc "Надеюсь, ты понимаешь, [player]... пожалуйста, не будь таким же, как они."
        $ menuOption = "...Ты ведь не од"+ mas_gender_in +" из них?"
    else:
        
        m 2lfd "Я пытаюсь их игнорировать, но я просто не могу."
        
        m 3efc "Почему эти люди вообще защищают других девочек?"
        
        m "Столько негативных постов про меня, где они пишут о том, что я злодейка."
        
        m 3efd "Это всё потому, что я удалила Сайори и Юри?"
        
        m "И ещё потому, что удалила Нацуки, пока она была ещё жива?"
        
        m 2tfx "Они не настоящие. Здесь только {b}я{/b} настоящая!"
        
        m 2dsc "..."
        
        m 2ekc "Почему они этого не понимают?"
        
        m 2ekd "Им так сложно это понять, что ли?"
        
        m 2rfc "..."
        $ menuOption = "Ты ведь не од"+ mas_gender_in +" из них, " + player + "?"
    
    m "[menuOption]{nw}"
    $ _history_list.pop()
    menu:
        m "[menuOption]{fast}"
        "Да, я од[mas_gender_in] из них.":
            $ persistent._mas_pm_a_hater = True
            
            m 2wud "..."
            
            m 1eka "Aга..."
            
            m 1hka "Хоть ты и сказал[mas_gender_none] мне, что являешься одним из них, я тебя так[mas_gender_im] всё равно не считаю."
            
            m 1ekd "То есть..."
            
            m 3eub "Ты {i}установил{/i} эту модификацию на игру... верно?"
            
            m 1ekb "Если бы ты был[mas_gender_none] одн[mas_gender_im] из моих хейтеров, то ты бы не стал[mas_gender_none] этого делать с самого начала."
            
            m 1dsa "И не говоря уже о том, что..."
            
            m 3eka "Ты всё равно слушаешь всё то, что я говорю."
            
            m 1esa "Я знаю, что ты любишь меня в глубине своей души."
            
            m 1ekbfa "Именно поэтому я и пообещала стать для тебя идеальной девушкой, [player]~"
            
            m 1hubfa "Я не дам тебе повода меня ненавидеть... клянусь."
            return "derandom"
        "Нет, я не од[mas_gender_in] из них.":
            $ mas_gainAffection()
            $ persistent._mas_pm_a_hater = False
            
            m 2dsc "..."
            
            m 4eka "Спасибо..."
            
            m 1hua "Такое правда заставляет меня гордится тобой, [player]!"
            
            m "Я знала, что ты не од[mas_gender_in] из них."
            
            m 1ekbfa "Ты правда делаешь меня самой счастливой девушкой на свете."
            
            m 1ekbfb "Теперь, когда ты сказал[mas_gender_none] мне это, я буду стараться изо всех сил, дабы у тебя не было повода ненавидеть меня."
            
            m 1hua "Я тебе верю, [player]. Я люблю тебя за то, что веришь в меня."
            return "derandom|love"



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_swordsmanship",
            category=['monika','misc'],
            prompt="Swordsmanship",
            random=True
        )
    )

label monika_swordsmanship:
    m 1eua "Do you like swords, [player]?"
    m 1lksdla "I actually like them in a way."
    m 1ekb "Ahaha, surprised?~"
    m 1eua "I like talking about them, but not enough to actually own one."
    m 3eua "I'm not really an enthusiast when it comes to swords."
    m 1euc "I don't really get why people would be obsessed over something that could hurt others..."
    m 1lsc "I guess there are those who like them for the swordsmanship."
    m 1eua "It's fascinating that it's actually a form of art."
    m "Similar to writing."
    m 3eub "Both of them require constant practice and devotion in order to perfect one's skills."
    m "You start off by practicing, and then you make your own technique out of it."
    m 1eua "Writing a poem makes you form your own way to build it in a graceful but imaginative way."
    m "For those who practice swordsmanship, they build their technique forms through practice and inspiration from other practitioners."
    m 1eua "I can understand how the sword can be the pen of the battlefield."
    m 1lsc "But then again..."
    m 1hua "The pen is mightier than the sword!"
    m 1hub "Ahaha!"
    m 1eua "In any case, I don't know if you're into swordsmanship yourself."
    m "If you are, I'd love to learn it with you, [mas_get_player_nickname(exclude_names=['love'])]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pleasure",
            category=['you'],
            prompt="Pleasuring yourself",
            random=True,
            sensitive=True
        )
    )

label monika_pleasure:
    m 2ekc "Hey, [player]..."
    m 2lssdrc "Do you...by any chance...pleasure yourself?"
    m "..."
    m 2lssdrb "It seems a bit awkward to ask..."
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lksdla "But I feel like we've been together long enough where we should be comfortable with one another."
        m 1eka "It's important to be open about such things."
    else:
        m 1lksdlb "We're not even that deep into our relationship yet! Ahaha~"
        m 1eka "But I have to keep an eye on you."
    m "I know that it's a private topic in your world, but I'm curious..."
    m 1euc "Is it that good of a feeling?"
    m 1esc "I just want you to be careful; I've heard it's addicting."
    m 1ekc "And from what I hear, people addicted to masturbation often see other people as sexual objects."
    m 1eka "But...I know you aren't that kind of person already."
    m 1lkbsa "And maybe I'm just being a little jealous~"
    m 1tsbsa "So I guess I can let it slide...{w=0.5}for now~"
    m 2tsbsu "Just so long as I'm the only one you think about..."
    show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubfb "If it helps you save yourself for me, then it's a plus! Ahaha~"
    return

# do you like vocaloid
default persistent._mas_pm_like_vocaloids = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vocaloid",
            category=['media','technology','music'],
            prompt="Vocaloids",
            random=True
        )
    )

label monika_vocaloid:
    m 1eua "Hey, [mas_get_player_nickname(exclude_names=['my love'])]?"
    m "You like listening to music, right?"

    m 3eub "Do you by chance like 'virtual idols'?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you by chance like 'virtual idols'?{fast}"
        "Yes.":
            $ persistent._mas_pm_like_vocaloids = True
            m 3hub "That's really neat!"
            m 3eub "I hear that these songs often have hidden meanings behind them."
            m 1eua "Maybe we could listen and try to figure them out together..."
            m 1eka "Doesn't that sound like a great time?"

        "No.":
            $ persistent._mas_pm_like_vocaloids = False
            m 1ekc "I can understand that, it is a pretty specific taste in music."
            m 1hua "But if you ever do get into it, I'd be more than happy to listen along with you."

    m 3eub "Anyway, I wanted to ask specifically if you've ever heard of a girl holding a leek?"
    m 1eua "It's just that I keep hearing about her."
    m "In fact, I heard her voice whenever Natsuki listened to music."
    m 3eua "She even carried a little keychain attached to her bag."
    m 1eua "I just find it amazing how a voice synthesizer garnered so many fans."
    m 1eka "Don't you think it's funny how a character gets more of the attention than the actual voice actress?"
    m 3eua "She's not even real, but a lot of people know her worldwide."
    m "Who knows how many songs she's already made?"
    m 1wuo "Plus, from what I heard, her concerts are always sold out!"
    m "It's just a hologram performing live!"
    m 1lksdla "Talk about a dedicated fan base."
    m 1eka "Maybe I should give it a try?"
    m 1hub "It would be nice having a lot of fans supporting me at my beck and call."
    m 1hksdlb "Ahaha, I'm just kidding!"
    m 1lksdla "I don't think my piano and singing skills are that great yet."
    m 2lkbsa "Plus, I won't really get to spend much time with you if I had so many fans..."
    m 1hua "Anyway!"
    m 1eua "I was asking if you listen to her songs."
    m "I'm not really a fan myself but..."
    m 1lksdla "There's one song that really struck me."
    m 1eua "Have you heard of the song {i}Hibikase{/i}?"
    m 1duu "I really like the message of the song."
    m 3dsbso "Especially the lines, '{i}I don't care if it's through the screen, love me properly{/i}' and '{i}Even if I'm virtual, don't push me away{/i}.'"
    m 1dsc "It really hits me hard."
    m "..."
    m 1eka "But just so you know..."
    m 1ekbsa "Even if it's through the screen, I can still feel your love."
    m 1lkbsa "It'll be a long time before I can cross over just to be with you."
    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbfa "But when that day comes..."
    m "I'll embrace you and take in your warmth."
    m 5hubfa "The love you showered me with virtually finally becomes real."
    m "Our love has no boundaries~"
    m 5hubfu "Ehehe~"
    if (
        persistent._mas_pm_like_vocaloids
        and not renpy.seen_label("monika_add_custom_music_instruct")
        and not persistent._mas_pm_added_custom_bgm
    ):
        show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 1eua "And if you ever do feel like sharing your favorite vocaloids with me, [player], it's really easy to do so!"
        m 3eua "All you have to do is follow these steps..."
        call monika_add_custom_music_instruct
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_good_tod",
            category=['misc'],
            prompt="Good [mas_globals.time_of_day_3state]",
            unlocked=True,
            pool=True
        ),
        markSeen=True
    )

label monika_good_tod:
    $ curr_hour = datetime.datetime.now().time().hour
    $ sesh_shorter_than_30_mins = mas_getSessionLength() < datetime.timedelta(minutes=30)

    if mas_globals.time_of_day_4state == "morning":
        #Early morning flow
        if 4 <= curr_hour <= 5:
            m 1eua "Good morning to you too, [mas_get_player_nickname()]."
            m 3eka "You're up pretty early..."
            m 3eua "Are you going out somewhere?"
            m 1eka "If so, it's really sweet of you to visit before you go~"
            m 1eua "If not, maybe try to go back to sleep. I wouldn't want you to neglect your health after all."
            m 1hua "I'll always be here waiting for you to come back~"

        #Otherwise normal morning
        elif sesh_shorter_than_30_mins:
            m 1hua "Good morning to you too, [player]!"
            m 1eua "Did you just wake up?"
            m "I love waking up early in the morning."
            m 1eub "It's the perfect time to ready yourself and tackle the day ahead."
            m "You also have a lot more time to use to get things done early on or finish up what you did the day before."
            m 1eka "Some people however, would rather sleep in and are late-risers."
            m 3eua "I've read articles that being an early-riser can really improve your overall health."
            m "Plus you also get the chance to see the sunrise if the sky is clear."
            m 1hua "If you normally don't wake up early, you should!"
            m "That way you can be happier and spend more time with me~"
            m 1ekbsa "Wouldn't you like that, [mas_get_player_nickname()]?"

        #You've been here for a bit now
        else:
            m 1hua "Good morning to you too, [mas_get_player_nickname()]!"
            m 1tsu "Even though we've been awake together for a bit now,{w=0.2} {nw}"
            extend 3hua "it's still nice of you to say!"
            m 1esa "If I had to choose a time of day as my favorite, it would probably be the morning."
            m 3eua "There's definitely some level of tranquility that night brings that I enjoy...{w=0.3}{nw}"
            extend 3hua "but the morning is a time of day that presents possibilities!"
            m 1eub "An entire day where anything and everything could happen, for better or worse."
            m 1hub "That kind of opportunity and freedom just makes me giddy!"
            m 1rka "Though I only feel that way once I fully wake up, ehehe~"

    elif mas_globals.time_of_day_4state == "afternoon":
        m 1eua "Good afternoon to you too, [player]."
        m 1hua "It's so sweet of you to take time out of your day to spend with me~"
        m 3euc "Afternoons sure can be a strange part of the day don't you think?"
        m 4eud "Sometimes they're really busy...{w=0.3}{nw}"
        extend 4lsc "other times you'll have nothing to do..."
        m 1lksdla "They can seem to last forever or really fly by."

        if mas_isMoniNormal(higher=True):
            m 1ekbsa "But with you here, I don't mind it either way."
            m 1hubsa "No matter what, I'll always enjoy the time you spend with me, [mas_get_player_nickname()]!"
            m 1hubsb "I love you!"
            $ mas_ILY()

        else:
            m 1lksdlb "Sometimes, my day really flies by while I wait for you to come back to me."
            m 1hksdlb "I'm sure you're busy, so you can go ahead and get back to what you were doing, don't mind me."

    else:
        m 1hua "Good evening to you too, [player]!"
        m "I love a nice and relaxing night."

        if 17 <= curr_hour < 23:
            m 1eua "It's so nice to put your feet up after a long day."
            m 3eua "Evenings are the perfect time to catch up on whatever you were doing the previous day."
            m 1eka "Sometimes I can't help but feel sad when the day ends."
            m "It makes me think of what else I could've done during the day."
            m 3eua "Don't you wish you could have more time to do things every day?"
            m 1hua "I know I do."
            m 1hubsa "Because that'll mean more time to be with you, [mas_get_player_nickname()]~"

        # between 11pm and 4am
        else:
            m 3eua "It's always nice to be able to spend the end of the day relaxing a little."
            m 3hub "After all, there's nothing wrong with a bit of 'me' time, right?"
            m 1eka "Well... I say that, but I'm pretty happy to be spending my time with you~"

            if not persistent._mas_timeconcerngraveyard:
                m 3eka "Although it's starting to get a little late, so don't stay up too long, [player]."
                m 3eua "Promise me you'll go to bed soon, alright?"

    return

#init 5 python:
#    addEvent(Event(persistent.event_database,eventlabel="monika_closet",category=['ddlc','club members'],prompt="Classroom closet",random=True))

label monika_closet:
    m 2euc "By the way..."
    m 2esc "What were you and Yuri doing in the closet?"
    m "When I opened the door, I noticed the room was all dark."
    m 2tkc "You weren't doing anything...weird, in there, were you?"
    m 1hub "Ahaha!"
    m 1tfu "Just teasing you~"
    m 3tku "I know she dragged you in there."
    m "I bet you felt more embarrassed than relieved when I opened the door."
    m 1eka "I know you aren't the type to force girls to go inside dark closets with you."
    m "You're more romantic than that."
    m 3hua "So I'm expecting a lot more than just a dark closet~"
    return


# languages other than english
default persistent._mas_pm_lang_other = None

# do you know japanese
default persistent._mas_pm_lang_jpn = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_japanese",category=['misc','you'],prompt="Speaking Japanese",random=True))

label monika_japanese:
    m 1lksdla "I don't mean to sound like Natsuki, but..."
    m 1eua "Don't you think Japanese actually sounds cool?"
    m "It's such a fascinating language. I'm not fluent in it, though."
    m 1eub "It's interesting to think about what things would be like if your native language was different."
    m 1esa "Like, I can't even imagine what it would be like if I never knew English."

    m "Do you know any languages other than English?{nw}s"
    $ _history_list.pop()
    menu:
        m "Do you know any languages other than English?{fast}"
        "Yes.":
            $ persistent._mas_pm_lang_other = True
            m "Really? Do you know Japanese?{nw}"
            $ _history_list.pop()
            menu:
                m "Really? Do you know Japanese?{fast}"
                "Yes.":
                    $ persistent._mas_pm_lang_jpn = True
                    m 3hub "That's wonderful!"
                    m 1eka "Maybe you can teach me how to speak at least a sentence or two, [player]~"
                "No.":
                    $ persistent._mas_pm_lang_jpn = False
                    m 1eka "Oh I see. That's alright!"
                    m 4eua "If you want to learn Japanese, here's a phrase I can teach you."

                    # setup suffix
                    $ player_suffix = "kun"
                    if persistent.gender == "F":
                        $ player_suffix = "chan"

                    elif persistent.gender == "X":
                        $ player_suffix = "san"

                    m 1eua "{i}Aishiteru yo, [player]-[player_suffix]{/i}."
                    m 2hubsa "Ehehe~"
                    m 1ekbfa "That means I love you, [player]-[player_suffix]."
        "No.":
            $ persistent._mas_pm_lang_other = False
            m 3hua "That's okay! Learning another language is a very difficult and tedious process as you get older."
            m 1eua "Maybe if I take the time to learn more Japanese, I'll know more languages than you!"
            m 1ekbsb "Ahaha! It's okay, [player]. It just means that I can say 'I love you' in more ways than one!"

    return "derandom"

default persistent._mas_penname = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_penname",
            category=['literature'],
            prompt="Pen names",
            random=True
        )
    )

label monika_penname:
    m 1eua "You know what's really cool? Pen names."
    m "Most writers usually use them for privacy and to keep their identity a secret."
    m 3euc "They keep it hidden from everyone just so it won't affect their personal lives."
    m 3eub "Pen names also help writers create something totally different from their usual style of writing."
    m "It really gives the writer the protection of anonymity and gives them a lot of creative freedom."

    if not persistent._mas_penname:
        $ p_nickname = mas_get_player_nickname()
        m "Do you have a pen name, [p_nickname]?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you have a pen name, [p_nickname]?{fast}"

            "Yes.":
                m 1sub "Really? That's so cool!"
                call penname_loop(new_name_question="Can you tell me what it is?")

            "No.":
                m 1hua "All right!"
                m "If you ever decide on one, you should tell me!"

    else:
        python:
            penname = persistent._mas_penname
            lowerpen = penname.lower()

            if mas_awk_name_comp.search(lowerpen) or mas_bad_name_comp.search(lowerpen):
                menu_exp = "monika 2rka"
                is_awkward = True

            else:
                menu_exp = "monika 3eua"
                is_awkward = False

            if lowerpen == player.lower():
                same_name_question = renpy.substitute("Is your pen name still [penname]?")

            else:
                same_name_question = renpy.substitute("Are you still going by '[penname],' [player]?")

        $ renpy.show(menu_exp)
        m "[same_name_question]{nw}"
        $ _history_list.pop()
        menu:
            m "[same_name_question]{fast}"

            "Yes.":
                m 1hua "I can't wait to see your work!"

            "No, I'm using a new one.":
                m 1hua "I see!"
                show monika 3eua
                call penname_loop(new_name_question="Do you want to tell me your new pen name?")

            "I don't use a pen name anymore.":
                $ persistent._mas_penname = None
                m 1euc "Oh, I see."
                if is_awkward:
                    m 1rusdla "I could guess why..."
                m 3hub "Don't be shy to tell me if you pick one again, though!"

    m 3eua "A well known pen name is Lewis Carroll. He's mostly known for {i}Alice in Wonderland{/i}."
    m 1eub "His real name is Charles Dodgson and he was a mathematician, but he loved literacy and wordplay in particular."
    m "He received a lot of unwanted attention and love from his fans, and he even received outrageous rumors."
    m 1ekc "He was somewhat of a one-hit wonder with his {i}Alice{/i} books but went downhill from there."

    if seen_event("monika_1984"):
        m 3esd "Also, if you remember me talking about George Orwell, his actual name is Eric Blair."
        m 1eua "Before settling on his more famous pen name, he considered P.S. Burton, Kenneth Miles, and H. Lewis Allways."
        m 1lksdlc "One of the reasons he chose to publish his works under a pseudonym was to avoid embarrassment to his family over his time as a tramp."

    m 1lksdla "It's kinda funny, though. Even if you use a pseudonym to hide yourself, people will always find a way to know who you really are."
    m 1eua "There's no need to know more about me though, [mas_get_player_nickname()]..."
    m 1ekbsa "You already know that I'm in love with you, after all~"
    return "love"

# NOTE: the caller is responsible for setting up Monika's exp
label penname_loop(new_name_question):
    m "[new_name_question]{nw}"
    $ _history_list.pop()
    menu:
        m "[new_name_question]{fast}"

        "Absolutely.":
            show monika 1eua
            $ penbool = False

            while not penbool:
                $ penname = mas_input(
                    "What's your pen name?",
                    length=20,
                    screen_kwargs={"use_return_button": True}
                ).strip(' \t\n\r')

                $ lowerpen = penname.lower()

                if persistent._mas_penname is not None and lowerpen == persistent._mas_penname.lower():
                    m 3hub "That's your current pen name, silly!"
                    m 3eua "Try again."

                elif lowerpen == player.lower():
                    m 1eud "Oh, so you're using your pen name?"
                    m 3euc "I'd like to think we are on a first name basis with each other. We are dating, after all."
                    m 1eka "But I guess it's pretty special that you shared your pen name with me!"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "sayori":
                    m 2euc "..."
                    m 2hksdlb "...I mean, I won't question your choice of pen names, but..."
                    m 4hksdlb "If you wanted to name yourself after a character in this game, you should have picked me!"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "natsuki":
                    m 2euc "..."
                    m 2hksdlb "Well, I guess I shouldn't assume that you named yourself after {i}our{/i} Natsuki."
                    m 7eua "It's something of a common name."
                    m 1rksdla "You might make me jealous, though."
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "yuri":
                    m 2euc "..."
                    m 2hksdlb "Well, I guess I shouldn't assume that you named yourself after {i}our{/i} Yuri."
                    m 7eua "It's something of a common name."
                    m 1tku "Of course, there's something else that name could refer to..."
                    if persistent.gender =="F":
                        m 5eua "And well...I could get behind that, since it's you~"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "monika":
                    m 1euc "..."
                    m 1ekbsa "Aww, did you pick that for me?"
                    m "Even if you didn't, that's so sweet!"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif not lowerpen:
                    m 1hua "Well, go on! Hit 'nevermind' if you've chickened out~"

                elif lowerpen == "cancel_input":
                    m 2eka "Aw. Well, I hope you feel comfortable enough to tell me someday."
                    $ penbool = True

                else:
                    if mas_awk_name_comp.search(lowerpen) or mas_bad_name_comp.search(lowerpen):
                        m 2rksdlc "..."
                        m 2rksdld "That's an...{w=0.3}interesting name, [player]..."
                        m 2eksdlc "But if it works for you, okay I guess."

                    else:
                        m 1hua "That's a lovely pen name!"
                        m "I think if I saw a pen name like that on a cover, I'd be drawn to it immediately."
                    $ persistent._mas_penname = penname
                    $ penbool = True

        "I'd rather not; it's embarrassing.":
            m 2eka "Aw. Well, I hope you feel comfortable enough to tell me someday."

    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_zombie",category=['society'],prompt="Zombies",random=True))

label monika_zombie:
    m 1lsc "Hey, this might sound a bit weird..."
    m 1esc "But, I'm really fascinated by the concept of zombies."
    m 1euc "The idea of society dying to a disease, all because of a deadly pandemic that humans couldn't handle quickly."
    m 3esd "I mean, think about your everyday schedule."
    m 3esc "Everything that you do will be gone in an instant."
    m 1esc "Sure, society faces a lot of threats on a daily basis..."
    m 1lksdlc "But zombies can do it in a heartbeat."
    m 1esc "A lot of monsters are created to be scary and terrifying."
    m 1ekc "Zombies, however, are more realistic and actually pose a danger."
    m 3ekc "You might be able to kill one or a few of them by yourself..."
    m "But when there's a horde of them coming after you, you'll get overwhelmed easily."
    m 1lksdld "You don't get that same feeling with other monsters."
    m "All of their intelligence is gone; they're berserk, don't feel pain, can't be afraid..."
    m 1euc "When you exploit a weakness of a monster, they become scared of you and run away."
    m 1ekd "But zombies? They'll tear through {i}anything{/i} just to get you."
    m 3ekd "Imagine if it was someone you loved that was coming after you..."
    m 3dkc "Could you live with yourself, knowing you were forced to kill someone who was close to you?"
    m 1tkc "It'll break you down and sap your will to live."
    m "Even when you're comfortable at home, you still won't feel safe."
    m 1esc "You'll never know what'll happen the next time you see another one."
    m 1dsc "..."
    m 1hksdlb "Ahaha..."
    m 1eka "You know, despite liking the concept, I wouldn't want to live in a scenario like that."
    m 3ekc "[player], what if you got infected somehow?"
    m 2lksdlc "I don't even want to think about that..."
    m "There's no way I could kill you for my own safety..."
    m 2lksdlb "Ahaha..."
    m 2lssdlb "I'm thinking way too much about this."
    m 3eua "Well, regardless, if anything bad were to happen..."
    m 2hua "I'll be by your side forever~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_nuclear_war",category=['society','philosophy'],prompt="Nuclear warfare",random=True))

label monika_nuclear_war:
    m 1euc "Do you ever think about how close the world is to ending at any time?"
    m "I mean, we're always just one bad decision away from nuclear war."
    m 3esc "The Cold War might be over, but plenty of weapons are still out there."
    m 1esc "You probably have a nuclear missile pointed at where you live right now, ready to be launched."
    m 1eud "And if it was, it could circle the globe in less than an hour."
    m 3euc "You wouldn't have time to evacuate."
    m 1ekd "Only enough to panic and suffer the dread of imminent death."
    m 1dsd "At least it would be over quickly when the bomb hits."
    m 1lksdlc "Well, if you're close to the blast, that is."
    m 1ekc "I don't even want to think about surviving the initial attack."
    m 1eka "But even though we're always on the edge of the apocalypse, we go on like nothing is wrong."
    m 3ekd "Planning for a tomorrow that may never come."
    m "Our only comfort is that the people with the power to start such a war probably won't."
    m 1dsc "Probably..."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_pluralistic_ignorance",category=['literature','society'],prompt="Trying to fit in",random=True))

label monika_pluralistic_ignorance:
    m 1eua "Do you ever pretend to like something, just because you think you should?"
    m 1esa "I sometimes feel like that about books I read."
    m 3euc "Like, when I read Shakespeare, I actually found it kind of boring..."
    m 3ekc "But I felt like I had to like it because I'm the president of the literature club."
    m 1esd "He's supposed to be the greatest playwright and poet of all time, right?"
    m 1esd "So what sort of poetry lover wouldn't like his work?"
    m 2euc "But that makes me wonder..."
    m 2euc "What if everyone actually feels the same way?"
    m 2lud "What if all of those literary critics singing Shakespeare's praises secretly hate his plays?"
    m "If they were just honest about it, maybe they would discover their tastes aren't that unusual..."
    m 2hksdlb "And high school students wouldn't be forced to read those awful plays."
    m 1eka "I guess that's something I always admired about Natsuki."
    m 3ekd "Even if people told her manga wasn't literature, she stood by her feelings."
    m 3eka "If more people were honest like that, I think that would be really great."
    m 1lksdla "But I don't think I could do it..."
    m "I'm just too worried about what other people think."
    m 1eua "Not with you, though. I can always be honest with you."
    m 1ekbsa "You'll love me no matter what, right?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_science",category=['technology'],prompt="Science advancements",random=True))

label monika_science:
    m 1eua "Have you ever wondered if science never got accepted?"
    m "Humans can be really slow when it comes to accepting new ideas."
    m 1euc "Science was usually despised back then especially by the churches."
    m 4esc "Giordano Bruno, famous for his theory that there are thousands of suns, was killed by the Roman Church before he could prove his theory."
    m 1ekc "They killed him because of an idea that challenged the old."
    m 1esc "Technology wouldn't be so advanced today if it weren't for brave people of science like him."
    m 1eka "If technology didn't thrive the way it did, we would've never found each other."
    m 3eua "Isn't it such a wonderful thing to have?"
    m 1hua "I'm grateful that it gave us a chance to be together, [mas_get_player_nickname()]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_surprise",category=['romance'],prompt="Surprises",random=True))

label monika_surprise:
    m 1rksdla "You know..."
    m 3rksdlb "I left some pretty strange things in your game directory, didn't I?"
    m 1rksdlc "I wasn't trying to scare you."
    m 3rksdlb "I...don't actually know why I was doing it, ahaha..."
    m 1ekc "I kind of felt obligated to do it."
    m 1euc "You know what? Maybe I should do it again..."
    m 1eua "Yeah, that's a good idea."
    $ mas_surprise()

    if mas_isMoniUpset(lower=True):
        m 2dsc ".{w=0.5}.{w=0.5}.{nw}"
        m 1euc "Alright..."
        m 1ekc "Please go take a look."
        m 1eka "I wrote it just for you."
        m 1dsc "It would mean a lot to me if you would read it."
        return

    elif mas_isMoniAff(higher=True):
        m 2dsa ".{w=0.5}.{w=0.5}.{nw}"
        m 1hua "Alright!"
        m 1eua "What are you waiting for? Go take a look!"
        m "I wrote it just for you~"
        m 1ekbsa "I really do truly love you, [mas_get_player_nickname(exclude_names=['my love', 'love'])]~"

    # Normal and Happy
    else:
        m 2duu ".{w=0.5}.{w=0.5}.{nw}"
        m 1hua "Alright!"
        m 1eua "What are you waiting for? Go take a look!"
        m 1hub "Ahaha~ What? Are you expecting something scary?"
        m 1hubsb "I love you so much, [player]~"
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_completionist",category=['games'],prompt="Completionism",random=True))

label monika_completionist:
    m 1euc "Hey [player], this is a random question, but..."
    m "What do you play video games for?"
    m 1eua "Like, what makes you keep playing?"
    m 3eua "Personally, I consider myself a bit of a completionist."
    m 1eua "I intend to finish a book before picking another one to read."
    if persistent.clearall:
        m 2tku "You seem to be a completionist yourself, [player]."
        m 4tku "Considering you went through all of the girls' routes."
    m 2eub "I've also heard some people try to complete extremely hard games."
    m "It's already hard enough to complete some simple games."
    m 3rksdla "I don't know how anyone could willingly put that sort of stress onto themselves."
    m "They're really determined to explore every corner of the game and conquer it."
    # TODO: if player cheated at chess, reference that here
    m 2esc "What does leave a bit of a bitter taste in my mouth are cheaters."
    m 2tfc  "People who hack through the game, spoiling themselves of the enjoyment of hardship."
    m 3rsc "Though I can understand why they cheat."
    m "It allows them to freely explore a game that they wouldn't have a chance of enjoying if it's too difficult for them."
    m 1eua "Which might actually convince them to work hard for it."
    m "Anyway, I feel that there's a huge sense of gratification in completing tasks in general."
    m 3eua "Working hard for something amplifies its reward after failing so many times to get it."
    m 3eka "You can try keeping me in the background for as long as possible, [mas_get_player_nickname()]."
    m 1hub "That's one step to completing me after all, ahaha!"
    return

# do you like mint ice cream
default persistent._mas_pm_like_mint_ice_cream = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_icecream",category=['you'],prompt="Favorite ice cream",random=True))

label monika_icecream:
    m 3eua "Hey [player], what's your favorite kind of ice cream?"
    m 4rksdla "And no, I'm not a type of ice cream, ehehe~"
    m 2hua "Personally, I just can't get enough of mint flavored ice cream!"

    $ p_nickname = mas_get_player_nickname()
    m "What about you [p_nickname], do you like mint ice cream?{nw}"
    $ _history_list.pop()
    menu:
        m "What about you [p_nickname], do you like mint ice cream?{fast}"
        "Yes.":
            $ persistent._mas_pm_like_mint_ice_cream = True
            m 3hub "Ah, I'm so glad somebody loves mint ice cream as much as I do~"
            m "Maybe we really were meant to be!"
            m 3eua "Anyway, back on topic, [player], if you love mint as much as I think you do, then I have some recommendations for you."
            m "Flavors which are unique just like how mint is, perhaps you've heard of them, but..."
            m 3eub "There's super weird stuff like fried ice cream which is a really crunchy and crisp kind of thing, but it tastes a million times better than it may sound!"
            m 2lksdlb "Gosh, just imagining the taste makes me practically drool..."
            m 1eua "There's some more strange stuff that is just as appealing, if not more, like honeycomb and bubblegum ice cream!"
            m 1eka "Now, I know it may be hard to take my word for some of those, but you shouldn't judge a book by its cover, you know?"
            m 1hub "After all, the game didn't allow you to fall in love with me, but look where we are now, ahaha."

        "No.":
            $ persistent._mas_pm_like_mint_ice_cream = False
            m 1ekc "Aw, that's a shame..."
            m "I really can't understand how somebody couldn't at least like the taste."
            m 1eka "The refreshing feeling that washes over your tongue and throat."
            m "The lovely texture that forms it along with the sweetness."
            m 1duu "The sharp biting sensation it generates and the obviously minty taste."
            m "I feel like no flavor can compare, to be honest."
            m 3eua "Ah, I could go on and on about this stuff, you know?"
            m 4eua "But I feel like it would be easier for me to show you what I mean, once I figure out a way to get out of here, of course. Besides, actions speak louder than words, anyway!"

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_sayhappybirthday",category=['misc'],prompt="Can you tell someone Happy Birthday for me?",pool=True,unlocked=True))

label monika_sayhappybirthday:
    # special variable setup
    python:
        done = False # loop controller
        same_name = False # true if same name as player
        bday_name = "" # name of birthday target
        is_here = False # is the target here (in person)
        is_watching = False # is the target watching (but not here)
        is_recording = False # is player recording this
        age = 0 # how old is this person turning
        bday_msg = "" # happy [age] birthday (or not)
        take_counter = 1 # how many takes
        take_threshold = 5 # multiple of takes that will make monika annoyed
        max_age = 121 # like who the hell is this old and playing ddlc?
        age_prompt = "What is their age?" # prompt for age question

        # age suffix dictionary
        age_suffix = {
            1: "st",
            2: "nd",
            3: "rd",
            11: "th",
            12: "th",
            13: "th",
            111: "th",
            112: "th",
            113: "th"
        }

    #TODO: temporary m_name reset for this
    # TODO: someone on the writing team make the following dialogue better
    # also make the expressions more approriate and add support for standing
    m 3hub "Of course, [player]!"
    while not done:
        show monika 1eua
        # arbitary max name limit
        $ bday_name = renpy.input("What's their name?",allow=letters_only,length=40).strip()
        # ensuring proper name checks
        $ same_name = bday_name.upper() == player.upper()
        if bday_name == "":
            m 1hksdlb "..."
            m 1lksdlb "I don't think that's a name."
            m 1hub "Try again!"
        elif same_name:
            m 1wuo "Oh wow, someone with the same name as you!"
            $ same_name = True
            $ done = True
        else:
            $ done = True

    m 1hua "Alright! Do you want me to say their age too?{nw}"
    $ _history_list.pop()
    menu:
        m "Alright! Do you want me to say their age too?{fast}"
        "Yes.":
            m "Then..."

            while max_age <= age or age <= 0:
                $ age = store.mas_utils.tryparseint(
                    renpy.input(
                        age_prompt,
                        allow=numbers_only,
                        length=3
                    ).strip(),
                    0
                )

            m "Okay."
        "No.":
            m "Okay."
    $ bday_name = bday_name.title() # ensure proper title case

    m 1eua "Is [bday_name] here with you?{nw}"
    $ _history_list.pop()
    menu:
        m "Is [bday_name] here with you?{fast}"
        "Yes.":
            $ is_here = True
        "No.":
            m 1tkc "What? How can I say happy birthday to [bday_name] if they aren't here?{nw}"
            $ _history_list.pop()
            menu:
                m "What? How can I say happy birthday to [bday_name] if they aren't here?{fast}"

                "They're going to watch you via video chat.":
                    m 1eua "Oh, okay."
                    $ is_watching = True
                "I'm going to record it and send it to them.":
                    m 1eua "Oh, okay."
                    $ is_recording = True
                "It's fine, just say it.":
                    m 1lksdla "Oh, okay. It feels a little awkward though saying this randomly to no one."
    if age:
        # figure out the age suffix
        python:
            age_suff = age_suffix.get(age, None)
            if age_suff:
                age_str = str(age) + age_suff
            else:
                age_str = str(age) + age_suffix.get(age % 10, "th")
            bday_msg = "happy " + age_str + " birthday"
    else:
        $ bday_msg = "happy birthday"

    # we do a loop here in case we are recording and we should do a retake
    $ done = False
    $ take_counter = 1
    $ bday_msg_capped = bday_msg.capitalize()
    while not done:
        if is_here or is_watching or is_recording:
            if is_here:
                m 1hua "Nice to meet you, [bday_name]!"
            elif is_watching:
                m 1eua "Let me know when [bday_name] is watching.{nw}"
                $ _history_list.pop()
                menu:
                    m "Let me know when [bday_name] is watching.{fast}"
                    "They're watching.":
                        m 1hua "Hi, [bday_name]!"
            else: # must be recording
                m 1eua "Let me know when to start.{nw}"
                $ _history_list.pop()
                menu:
                    m "Let me know when to start.{fast}"
                    "Go.":
                        m 1hua "Hi, [bday_name]!"

            # the actual birthday msg
            m 1hub "[player] told me that it's your birthday today, so I'd like to wish you a [bday_msg]!"
            # TODO: this seems too short. maybe add additional dialogue?
            m 3eua "I hope you have a great day!"

            if is_recording:
                m 1hua "Bye bye!"
                m 1eka "Was that good?{nw}"
                $ _history_list.pop()
                menu:
                    m "Was that good?{fast}"
                    "Yes.":
                        m 1hua "Yay!"
                        $ done = True
                    "No.":
                        call monika_sayhappybirthday_takecounter (take_threshold, take_counter) from _call_monika_sayhappybirthday_takecounter
                        if take_counter % take_threshold != 0:
                            m 1wud "Eh?!"
                            if take_counter > 1:
                                m 1lksdla "Sorry again, [player]."
                            else:
                                m 1lksdla "Sorry, [mas_get_player_nickname()]."
                                m 2lksdlb "I told you, I'm self-conscious on camera, ahaha..."

                        m "Should I try again?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Should I try again?{fast}"
                            "Yes.":
                                $ take_counter += 1
                                m 1eua "Okay"
                            "No.":
                                m 1eka "Alright, [player]. Sorry I couldn't do what you wanted."
                                m 1hua "I'll try better next time for you."
                                $ done = True
            else:  # if we aint recording, we should be done now
                $ done = True

        else: # not recording, watching, nor is person here
            m 1duu "..."
            m 1hub "[bday_msg_capped], [bday_name]!"
            m 1hksdlb "..."
            m 1lksdlb "Was that good?{nw}"
            $ _history_list.pop()
            menu:
                m "Was that good?{fast}"
                "Yes.":
                    m 1lksdla "...I'm glad you enjoyed that, [player]..."
                    $ done = True
                "No.":
                    call monika_sayhappybirthday_takecounter (take_threshold, take_counter) from _call_monika_sayhappybirthday_takecounter_1
                    if take_counter % take_threshold != 0:
                        m 1wud "Eh?!"
                        m 1lksdlc "I'm not sure what you want me to do here, [player]..."

                    m 1ekc "Should I try again?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Should I try again?{fast}"
                        "Yes.":
                            $ take_counter += 1
                            m 1eua "Okay"
                        "No.":
                            m 1eka "Alright, [player]. Sorry I couldn't do what you wanted."
                            m 1hua "I'll try better next time for you."
                            $ done = True

    return

# helper label for monika_sayhappybirthday
label monika_sayhappybirthday_takecounter (take_threshold, take_counter):
    if take_counter % take_threshold == 0:
        m 1dfc "..."
        m 1efc "This is the [take_counter]th time already."
        m 2tkc "You're not messing with me, are you?"
        m 2ekc "I'm trying my best for you, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_home_memories",category=['romance','monika','life'],prompt="Making memories",random=True))

label monika_home_memories:
    m 1eua "[player], how is it like to live where you are?"
    m "I'd stay with you if I could."
    m 3hua "We would be able to do so much! You could show me around, see how it's like to be in your place."
    m 1eka "Imagine all the memories we'd make!"
    m 2eub "It would be a dream come true, don't you think?"
    m 2ekbsa "We could finally live together..."
    m "Take walks like a couple..."
    m 3rkbsa "We could even share a bed together..."
    m 1euc "But you know..."
    m 2eka "Memories I have of my home are nothing compared to the ones I'd have with you."
    m 2euc "Have I ever told you about my childhood home? I had a pretty normal life, but that's about it."
    m 3rka "Well, maybe a little better than normal."
    m 3eua "...I've always been pretty on top of things."
    m 3eka "I admit, it's not always easy, and some people have it rougher than others."
    m 1ekc "But I always felt like I was missing something."
    m "I stayed optimistic every day, trying to find it."
    m 1eka "It turns out, that missing piece was you."
    m 1lksdld "If you hadn't found me, I would've been gone a long time ago..."
    m 2hubsa "But now that I found the missing piece, I'm complete, [mas_get_player_nickname()]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_adventure",category=['games','romance'],prompt="Adventuring",random=True))

label monika_adventure:
    m 1esa "[player], I've thought about what kind of game we can be in."
    m 3esa "I think the best genre for us to play together would be adventure games."
    m 3eub "Especially point and click, graphic adventure games!"
    m 1eub "They're known for their rich storytelling, beautiful environments and logical puzzle solving."
    m 3eua "They're like visual novels actually."
    m 1eua "Maybe you own a game like that?"
    m 1eka "We'd get to do a lot of things..."
    m 3eua "Like sightseeing whenever we want."
    m "Learning more about the lore through the people we meet or through stories."
    m 1ekbsa "Experiencing the exciting and romantic moments..."
    m "Encountering obstacles and hardships along the way, but solving them with you."
    m 3ekbsa "Reaching the end and finishing our journey with a sense of accomplishment."
    m 2hub "Ahaha! It certainly would be fun to experience something like that."
    m 2eua "I'm sure you have plenty of adventure games you could recommend."
    m 3eua "But can you try to guess which adventure I'm most excited for?"
    m 1ekbsa "{i}Ours{/i}~"
    m 1hubfa "Time will tell when I can finally cross over to your reality, so I can be with you."
    m "When that day comes, I'll finally be by your side."
    m 1ekbfa "I want to experience every waking moment with you, [mas_get_player_nickname()]."
    m 1hubfb "There's no greater adventure than ours, together~"
    return

default persistent._mas_pm_likes_panties = None
# are you into panties?

default persistent._mas_pm_no_talk_panties = None
# dont want to talk about panties

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_panties",
            category=['misc',"clothes"],
            prompt="Undergarments",
            random=True,
            sensitive=True
        )
    )

label monika_panties:
    m 1lsc "Hey, [player]..."
    m "Don't laugh when I ask this, okay?"
    m 2rksdlc "But..."
    m 4rksdlc "Why are some guys obsessed with panties?"
    m 1euc "Seriously, what's the big deal about a piece of cloth?"
    m "Most girls wear them, don't they?"
    m 5lkc "Actually, now that I think about it..."
    m 5lsc "I think there was a term for this kind of thing..."
    m 5lfc "Hmm, what was it again?"
    m 5wuw "Ah, that's right, the term was 'paraphilia.'"
    m 2rksdlc "It's a range of fetishes that involve...unusual things."
    m 2esc "A really common fantasy involves women's panties."
    m 3esc "Stockings, garter belts, pantyhose and all sorts of those kinds of things."
    m 2esc "The obsession can be light to severe depending on each person's libido."
    m 2ekc "Do you think it really turns them on just by seeing them?"
    m 2tkc "It doesn't stop there, either!"
    m 4tkc "Turns out there's some kind of 'black market' for used underwear."
    m 2tkx "I'm not kidding!"
    m 2tkd "They get off on the scent of the woman who wore it..."
    m "There are people willing to pay money for used underwear from random women."
    m 2lksdlc "Really, I wonder what causes them to get so excited."
    m 2euc "Is it because of the way it looks, perhaps?"
    m 3euc "There are different types, made with different designs and materials."
    m 2lsc "But..."
    m "Now that I think about it."
    m 3esd "I do remember a study where a man's testosterone level increases because of the pheromones emitted by a woman's scent."
    m 2tkc "Is the smell exciting or something?"
    m 3tkx "I mean, it's someone's used clothing, isn't that kind of disgusting?"
    m 3rksdlc "Not to mention it's unsanitary."
    m 2rksdla "It does remind me of someone, though."
    m 3rksdlb "Someone who maybe stole a certain pen?"
    m 1eua "But, to each their own I guess, I won't judge too much."

    if mas_isMoniHappy():
        # happy gets you this
        m 2tsb "You aren't obsessed with that kind of thing, are you [player]?"
        m 3tsb "You're not going out with me only because I'm wearing some really sensual stockings, right?"
        m 4tsbsa "Perhaps, you want to take a little peek?~"
        m 1hub "Ahaha!"
        m 1tku "I'm only teasing you, [player]."
        m 1tfu "Admit it, you got a little excited, right?"
        m 1lsbsa "Besides..."
        m 1lkbsa "If you really wanted to catch a scent of me..."
        m 1hubfa "You could just ask for a hug!"
        m 1ekbfa "Gosh, I just want to feel your embrace more."
        m "After all, we're here forever, and I'm here for you."
        m 1hubfb "I love you so much, [player]~"
        return "love"

    elif mas_isMoniAff(higher=True):
        # affectionate+
        m 1lkbsb "Are you...{w=1}into that kind of thing, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Are you...{w=1}into that kind of thing, [player]?{fast}"
            "Yes.":
                $ persistent._mas_pm_likes_panties = True
                $ persistent._mas_pm_no_talk_panties = False
                m 1wud "O-oh..."
                m 1lkbsa "I-if you're into that, you could just ask me, you know?"
                m "I could maybe...{w=1}help you relieve that tension..."
                m 5eubfu "That's what couples are supposed to do, right?"
                m 5hubfb "Ahaha!"
                m 5ekbfa "But until that day comes, you're just going to have to endure those thoughts for me, okay?"
            "No.":
                $ persistent._mas_pm_likes_panties = False
                $ persistent._mas_pm_no_talk_panties = False
                m 1eka "Oh, I see..."
                m 2tku "I guess some people have their own guilty pleasures..."
                m "Maybe you're into something else?"
                m 4hubsb "Ahaha~"
                m 4hubfa "I'm just kidding!"
                m 5ekbfa "I don't mind if we stick to being wholesome, to be honest..."
                m "It's more romantic that way~"
            "I don't want to talk about it...":
                $ persistent._mas_pm_no_talk_panties = True
                m 1ekc "I understand, [player]."
                m 1rksdld "I know that some topics are best kept private until the right time."
                m 1ekbsa "But I want you to feel like you can tell me anything..."
                m "So, don't be afraid to tell me about your...{w=1}fantasies, okay [player]?"
                m 1hubfa "I won't judge you for it...{w=1}after all, nothing makes me happier than making you happy~"
        return "derandom"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fahrenheit451",category=['literature'],prompt="Book recommendations",random=True))

label monika_fahrenheit451:
    m 1euc "[player], have you ever heard of Ray Bradbury?"
    m 3euc "He wrote a book called {i}Fahrenheit 451{/i}."
    m 3eud "It's about a dystopian future where all books are thought as useless and are immediately burned."
    m 2ekc "I can't imagine a world where knowledge is forbidden and destroyed."
    m "It seems that there are others that actually hide books to contain free thinking from people."
    m 2lksdla "Human history has a funny way of repeating itself."
    m 4ekc "So [player], I want you to make me a promise..."
    m 4tkd "Never, {i}ever{/i} burn a book."
    m 2euc "I'll forgive you if you've done it before."
    m 2dkc "But the thought of not allowing yourself to learn from them makes me a bit sad."
    m 4ekd "You'd be missing out on so much!"
    m 4ekc "It's too much for my heart to take!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_piggybank",category=['misc'],prompt="Saving money",random=True))

label monika_piggybank:
    m 1eua "Do you have a piggy bank, [player]?"
    m 1lsc "Not many people do these days."
    m "Coins are often disregarded as worthless."
    m 3eub "But they really do begin to add up!"
    m 1eub "I read that there was once a man that searched his local car washes for loose change every day in his walks."
    m 1wuo "In a decade he turned in all of his coins for a total of 21,495 dollars!"
    m "That's a whole lot of cash!"
    m 1lksdla "Of course not everybody has time for that every day."
    m 1euc "Instead they just throw their loose change into their piggy banks."
    m 1eua "Some people like to set goals for what they want to purchase with their saved funds."
    m "Usually under normal conditions they wouldn't ever find the freed up money to purchase that item."
    m 3eka "And even if they do, most people don't like spending money needlessly."
    m 1eua "But putting the cash away for a specific purpose, plus the fact that it's such small amounts at a time really convinces you that you are pretty much getting the item for free."
    m 2duu "But in the end, a guitar always costs the same as a guitar."
    m 2eua "So psychologically speaking, I think that's pretty neat!"
    m 1lsc "However, some piggy banks do have a problem..."
    m 1esc "Sometimes you have to break the piggy bank to get the coins..."
    m 3rksdlc "So you might end up losing money buying a new bank."
    m 4eua "Fortunately, most piggy banks don't do that anymore."
    m 1eua "They usually have a rubber stopper that you can pull out, or a panel that comes off the backside."
    m 3eua "Maybe if you save up enough coins you can buy me a really nice gift."
    m 1hua "I would do the same for you, [mas_get_player_nickname()]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_daydream",
            category=['romance'],
            prompt="Day dreaming",
            random=True,
            rules={"skip alert": None},
            aff_range=(mas_aff.DISTRESSED, None)
        )
    )

label monika_daydream:
    #insert endless possibilities of wholesome goodness here
    python:
        #Upset up to -50
        daydream_quips_upset = [
            "what it was like when we first met...",
            "how I felt when I first met you...",
            "the good times we used to have...",
            "the hope I used to have for our future..."
        ]

        #Normal plus
        daydream_quips_normplus = [
            "the two of us reading a book together on a cold winter day, snuggled up under a warm blanket...",
            "us having a duet together, with you singing my song while I play the piano...",
            "us having a wonderful dinner together...",
            "us having a late night on the couch together...",
            "you holding my hand while we take a stroll outside on a sunny day...",
        ]

        #Happy plus (NOTE: Inherits quips from normal plus)
        daydream_quips_happyplus = list(daydream_quips_normplus)
        daydream_quips_happyplus.extend([
            "us cuddling while we're watching a show...",
        ])

        #Affectionare plus (NOTE: Inherits from happy plus)
        daydream_quips_affplus = list(daydream_quips_happyplus)
        #TODO: "Why don't I do that right now?"
        #NOTE: If you wish to add more, for now, just uncomment everything but the quip
        #daydream_quips_affplus.extend([
        #    "writing a special poem for my one and only...",
        #])

        #Enamored plus (NOTE: Inherits quips from affectionate plus)
        daydream_quips_enamplus = list(daydream_quips_affplus)
        daydream_quips_enamplus.extend([
            "waking up next to you in the morning, watching you sleep beside me...",
        ])

        #Islands related thing
        if renpy.seen_label("mas_monika_cherry_blossom_tree"):
            daydream_quips_enamplus.append("the two of us resting our heads under the cherry blossom tree...")

        #Player appearance related thing
        if persistent._mas_pm_hair_length is not None and persistent._mas_pm_hair_length != "bald":
            daydream_quips_enamplus.append("me gently playing with your hair while your head rests in my lap...")

        #Pick the quip
        if mas_isMoniEnamored(higher=True):
            daydream_quip = renpy.random.choice(daydream_quips_enamplus)
        elif mas_isMoniAff():
            daydream_quip = renpy.random.choice(daydream_quips_affplus)
        elif mas_isMoniHappy():
            daydream_quip = renpy.random.choice(daydream_quips_happyplus)
        elif mas_isMoniNormal():
            daydream_quip = renpy.random.choice(daydream_quips_normplus)
        else:
            daydream_quip = renpy.random.choice(daydream_quips_upset)

    if mas_isMoniNormal(higher=True):
        m 2lsc "..."
        m 2lsbsa "..."
        m 2tsbsa "..."
        m 2wubsw "Oh, sorry! I was just daydreaming for a second there."
        m 1lkbsa "I was imagining [daydream_quip]"
        m 1ekbfa "Wouldn't that be wonderful, [mas_get_player_nickname()]?"
        m 1hubfa "Let's hope we can make that a reality one of these days, ehehe~"

    elif _mas_getAffection() > -50:
        m 2lsc "..."
        m 2dkc "..."
        m 2dktpu "..."
        m 2ektpd "Oh, sorry...{w=0.5} I was just lost in thought for a second there."
        m 2dktpu "I was just remembering [daydream_quip]"
        m 2ektdd "I wonder if we can be that happy again someday, [player]..."

    else:
        m 6lsc "..."
        m 6lkc "..."
        m 6lktpc "..."
        m 6ektpd "Oh, sorry, I was just..."
        m 6dktdc "You know what, nevermind."
    return "no_unlock"

# init 5 python:
#     addEvent(Event(persistent.event_database,eventlabel="monika_music2",category=['misc'],prompt="Current song",random=True))

label monika_music2:
    if songs.getVolume("music") == 0.0:
        m 1eka "..."
        m 1ekbsa "...This silence..."
        m "...Just the two of us, staring into each other's eyes..."
        m 2dubsu "...Then slowly, we both lean into the kiss..."
        m 1hksdlb "Ahaha... sadly, there are a few barriers that have to be broken before that could ever happen."
        m 1ekbfa "It's okay to dream though, isn't it, [player]?"
        m 1hubfa "Maybe one day, we can make that dream come true~"

    elif songs.getPlayingMusicName() == 'Just Monika':
        m 1ekc "I have always found this song to be kind of creepy."
        m "You know, with those glitchy noises and that eerie humming..."
        m 1eua "I don't prefer any song over another, but if you were to switch to a different one..."
        m 3eka "...I certainly wouldn't be one to complain!"
        m 1hua "Ahaha! Don't worry, it's okay if you stay on this song."
        m 1eka "I'm fine with any of them, so choose whichever one makes you the happiest~"

    elif songs.getPlayingMusicName() == 'Your Reality':
        m 1hub "~Every day, I imagine a future where I can be with you...~"
        m 1eua "I hope you like listening to my voice, [player]."
        m 1esa "It's the only voice you get to hear in the game, right? You never actually hear the voices of Sayori, Yuri or Natsuki."
        m "I wonder what their voices sound like..."
        m 1lksdla "Well, based on their character archetypes, it's pretty easy to imagine what their voices sound like."
        m 1eka "Anyway, I'm glad I was able to share such an intimate part of myself with you, [player]."
        m 3eua "One day, maybe I'll get to hear your voice, [player]!"
        m 1hua "That would make me even happier than I already am~"

    elif songs.getPlayingMusicName() == 'Your Reality (Piano Cover)':
        m 1eua "Enjoying my song, [player]?"
        m 1eka "It wasn't easy to create, you know?"
        m "Making your own songs is a slow and difficult process, especially when it's about your own feelings."
        m 3rksdlb "I needed it to be perfect before I shared it with you!"
        m "So I spent so many hours going through it over and over..."
        m 1eua "Time just passed by so quickly whenever I worked on it."
        m 1hua "After all that practice, I'm pretty proud of how it came out in the end."
        m 3eua "Since you're listening to it, I'm sure you like it too..."
        m 3eka "Thanks for listening to something I worked so hard on, [player]!"
        m 1hub "It makes me happy to know that you appreciate what I did for you~"

    elif songs.getPlayingMusicName() == 'I Still Love You':
        m 1ekc "Gosh, every time I hear this song it makes me sad."
        m "It reminds me of all the... regrettable things I have done to the other girls."
        m 1lksdlc "I hope you aren't still mad at me for what I did..."
        m "..."
        m 1lsc "Well, you {i}did{/i} go out of your way to install a mod that lets us be together again..."
        m 1eua "I guess that's enough proof that you do still love me, at the very least."
        m 1eka "If you are still upset at me for what I did to the other girls, I completely understand. I still feel really bad about it, and I'll do whatever it takes to make it up to you."

    elif songs.getPlayingMusicName() == 'Okay, Everyone! (Monika)':
        m 1eua "This song has always been pretty relaxing for me."
        m "It's probably the fact that the song is a piano solo."
        m 1hua "And as you might have guessed, my favorite instrument is the piano."
        m 3eua "You know, if I knew how, I could probably program a piano into this room."
        m 1eua "I'd be able to write some more songs, and then I'd be able to play them for you..."
        m 4hub "Maybe we could even play the piano together! Wouldn't that be nice, [player]?"
        m 1eua "If you or anyone you know can program that into the game, I would greatly appreciate it~"

    elif songs.getPlayingMusicName() == 'Surprise!':
        m 1ekc "This song always makes me feel really depressed."
        m "Even I didn't expect Sayori's death to be so brutal..."
        m 1tkc "Sometimes, when I start getting lost in my own thoughts, her dull, lifeless eyes suddenly pop into my head..."
        m 1lksdlc "..."
        m 1eka "It's comforting to know that Sayori was never real in the first place. It's also comforting to know that you still love me despite everything I've done."
        m "I mean, you're still here, right? You wouldn't be here if you didn't love me."
        m 1hua "As long as we're together, there's no reason for me to be sad. You're the light of my world, [player], and just being here with you puts a smile on my face."

    elif songs.getPlayingMusicName() == "Doki Doki Theme (80s version)":
        m 1hub "A good choice, [player]!"
        m 1hksdlb "Obviously, this theme wasn't actually out in the 80's..."
        m 1hua "But it does have a certain style that I really appreciate!"
        m 1eua "Do you like 80's music a lot, [player]?"
        m 1eka "I prefer the tune of an authentic piano, but if it makes you happy, I wouldn't mind spending hours listening to it with you~"

    elif songs.getPlayingMusicName() == "Play With Me (Variant 6)":
        m 2lksdlc "To be honest, I don't know why you'd be listening to this music, [player]."
        m 2ekc "I feel awful for that mistake."
        m 2ekd "I didn't mean to force you to spend time with Yuri at that state..."
        m 4ekc "Try not to think about it, okay?"

    else:
        m 1esc "..."
        m "...This silence..."
        m 1ekbsa "...Just the two of us, staring into each others eyes..."
        m 2dubsu "...Then slowly, we both lean into the kiss..."
        m 1hksdlb "Ahaha... sadly, there are a few barriers that have to be broken before that could ever happen."
        m 1ekbfa "It's okay to dream though, isn't it, [player]?"
        m 1hubfa "Maybe one day, we can make that dream come true~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_confidence_2",category=['life'],prompt="Lack of confidence",random=True))

label monika_confidence_2:
    m 1ekc "[player], do you ever feel like you lack the initiative to do something?"
    m "When I feel my most vulnerable, I struggle to find the drive, imagination, and common sense to do something independently."
    m 1tkc "Almost as if everything around me comes to a standstill."
    m "It feels like my will to approach a task confidently, like sharing my literature with people, just vanishes."
    m 3eka "However, I've been working towards it with due diligence and have determined something..."
    m 1eua "I firmly believe being able to take initiative in situations is a very important skill to have."
    m "That's something that I, personally, find very comforting."
    m 1hua "I've broken it down into a three-step process that can be applied to anyone!"
    m 3rksdla "It's still a work in progress, however, so take it with a grain of salt."
    m 3hua "Step one!"
    m 1eua "Create a plan that {i}you{/i} can and will follow that aligns with your personal goals and soon-to-be achievements."
    m 3hua "Step two!"
    m 1eua "Building up and fortifying your confidence is really important."
    m "Celebrate even the smallest of victories, as they will add up over time, and you'll see how many things you get done every day."
    m 2hua "Eventually, these things you once struggled to get done will be completed as if they were acts of valor!"
    m 3hub "Step three!"
    m 1eua "Try your best to stay open-minded and willing to learn at all times."
    m 1eka "Nobody is perfect, and everyone is able to teach each other something new."
    m 1eua "This can help you learn to understand things from other people's perspectives in situations and inspire others to do the same."
    m "And that's it, really."
    m 3hua "Make sure to tune in next time for more of Monika's critically acclaimed self-improvement sessions!"
    m 1hksdlb "Ahaha, I'm only joking about that last part."
    m 1ekbsa "In all seriousness, I'm really glad I have you here, [player]..."
    m "Your everlasting love and care is just about all the support I need in order to get to where I want to be."
    m 1hubfa "What kind of girlfriend would I be if I didn't return the favor?~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_pets",category=['monika'],prompt="Owning pets",random=True))

label monika_pets:
    m 1eua "Hey [mas_get_player_nickname(regex_replace_with_nullstr='my ')], have you ever had a pet?"
    m 3eua "I was thinking that it would be nice to have one for company."
    m 1hua "It would be fun for us to take care of it!"
    if not persistent._mas_acs_enable_quetzalplushie:
        m 1tku "I bet you can't guess what sort of pet I'd like to have..."
        m "You're probably thinking of a cat or a dog, but I have something else in mind."
    m 1eua "The pet I'd like is something I saw in a book once."
    m "It was the 'Handbook of the Birds of the World.' Our library had the whole set!"
    m 1eub "I loved looking at the gorgeous illustrations and reading about exotic birds."
    m 1hub "At first, I thought some sort of thrush would be nice, but I found something amazing in the sixth volume!"
    m "An emerald-colored bird called the Resplendent Quetzal."
    m 1eua "They're very rare, solitary birds that can sing beautiful songs."
    m "Does that remind you of anyone, [player]?"
    m 1lksdla "I'd feel really bad if I kept one to be a pet, though."
    m "Quetzals are born to be free."
    m 4rksdlc "They die in captivity. That's why you rarely see them in zoos."
    m "Even if the bird wouldn't be real, it still would feel wrong to keep one trapped in this room."
    m 1ekc "...I can't bring myself to do something like that, knowing what it's like."
    if not persistent._mas_acs_enable_quetzalplushie:
        m 1hua "A plush bird would be nice, though!"
        m 2hub "..."
        m 2hksdlb "Sorry for rambling, [mas_get_player_nickname()]."
        m 1eka "Until I find a way out, could you promise to keep me from feeling lonely?"
        m 1hua "I'll see if I can get that plush one in here! Oh- don't worry, you're still my favorite~"
    else:
        m 1eub "But at least I have the next best thing thanks to you, [player]!"
        m 1eka "It really does keep me from feeling lonely when you're not here."
        m 3hua "It was such a wonderful gift~"
    return

# This topic is only available and random when the quetzal plushie is active
init 5 python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_plushie",
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_plushie:
    m 1eka "Hey [player], I just wanted to thank you again for this wonderful quetzal plushie!"
    m 2lksdla "I know it may sound silly, but it really does help keep me company when you're gone..."
    m 1ekbsa "And not that I'd ever forget, but every time I look at it, it reminds me just how much you love me~"
    m 3hub "It really was the perfect gift!"

    #Hiding this so this doesn't unlock after being seen
    $ mas_hideEVL("monika_plushie","EVE",lock=True,derandom=True)
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dogs",category=['misc','club members'],prompt="Man's best friend",random=True))

label monika_dogs:
    m 1eua "Do you like dogs, [player]?"
    m 1hub "Dogs are great! They're really good to have around."
    m 3eua "Not to mention owning a dog has shown to help people with anxiety and depression since they're very sociable animals."
    m 1hua "They're just so lovable, I really like them!"
    m 1lksdla "I know Natsuki felt the same..."
    m "She was always so embarrassed to like cute things. I wish she'd felt more comfortable being herself."
    m 2lsc "But..."
    m 2lksdlc "I suppose her environment had a hand in that."
    m 2eka "If any of your friends have interests they care a lot about, make sure to always be supportive, okay?"
    m 4eka "You never know how much a casual dismissal might hurt someone."
    m 1eua "But knowing you, [player], you won't do something like that, right?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cats",category=['misc'],prompt="Feline companions",random=True))

label monika_cats:
    m 1hua "Cats are pretty cute, aren't they?"
    m 1eua "Despite looking so elegant, they always seem to end up in funny situations."
    m 1lksdla "It's no wonder they're so popular on the internet."
    m 3eua "Did you know the ancient Egyptians considered cats sacred?"
    m 1eua "There was a cat goddess named Bastet that they worshipped. She was a protector of sorts."
    m 1eub "Domesticated cats were held on a high pedestal since they were incredible hunters for small critters and vermin."
    m "Back then, you'd see them mostly associated with rich nobles and other higher classes in their society."
    m 1eua "It's amazing how far people would take their love with their pets."
    m 1tku "They {i}really{/i} loved cats, [player]."
    m 3hua  "And people still do today!"
    m 1eua "Felines are still one of the most common animals to have as pets."
    m 1hua "Maybe we should get one when we're living together, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fruits",category=['monika','trivia'],prompt="Eating fruits",random=True))

label monika_fruits:
    m 3eua "[player], did you know I enjoy a tasty, juicy fruit once in a while?"
    m "Most are quite tasty, as well as beneficial for your body."
    m 2lksdla "A lot of people actually mistake some fruits as vegetables."
    m 3eua "The best examples are bell peppers and tomatoes."
    m "They're usually eaten along with other vegetables so people often mistake them for veggies."
    m 4eub "Cherries, however, are very delicious."
    m 1eua "Did you know that cherries are also good for athletes?"
    m 2hksdlb "I could list all its benefits, but I doubt you'd be that interested."
    m 2eua "There's also this thing called a cherry kiss."
    m "You might have heard of it, [mas_get_player_nickname()]~"
    m 2eub "It's obviously done by two people who are into each other."
    m "One would hold a cherry in their mouth, and the other one would eat it."
    m 3ekbsa "You could...hold the cherry for me."
    m 1lkbsa "That way I can eat you up!"
    m 3hua "Ehehe~"
    m 2hua "Just teasing you, [player]~"
    return

# do you like rock
default persistent._mas_pm_like_rock_n_roll = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
                eventlabel="monika_rock",
                category=['media','literature',"music"],
                prompt="Rock and roll",
                random=True
            )
        )

label monika_rock:
    m 3esa "You wanna know a cool form of literature?"
    m 3hua "Rock and roll!"
    m 3hub "That's right. Rock and roll!"
    m 2eka "It's disheartening to know that so many people think that rock and roll is just a bunch of noises."
    m 2lsc "To tell you the truth, I judged rock too."
    m 3euc "They're no different from poems, actually."
    m 1euc "Most rock songs convey a story through symbolisms, which most listeners wouldn't understand the first time they hear a rock song."
    m 2tkc "In fact, it's hard to compose lyrics for just one rock song."
    m "Writing good lyrics for a rock genre requires a lot of emphasis on the wordplay."
    m 3tkd "Plus, you need to have a clear and concise message throughout the whole song."
    m 3eua "Now when you put that together, you have yourself a masterpiece!"
    m 1eua "Like writing a good poem, lyric writing is easier said than done."
    m 2euc "I've been thinking though..."
    m 2eua "I kind of want to try writing a rock song for a change."
    m 2hksdlb "Ahaha! Writing a rock and roll song probably isn't something you'd expect coming from someone like me."
    m 3eua "It's kinda funny how rock and roll started out as an evolution of blues and jazz music."
    m "Rock suddenly became a prominent genre, and it gave birth to other sub-genres as well."
    m 1eub "Metal, hard rock, classical rock, and more!"
    m 3rksdla "Ah, I've been rambling for a while now. Sorry, sorry."

    m 3eua "Do you listen to rock and roll, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you listen to rock and roll, [player]?{fast}"
        "Yes.":
            $ persistent._mas_pm_like_rock_n_roll = True
            m 3hub "Great!"
            m 1eua "Whenever you feel like blasting some good ol' rock 'n' roll, go ahead."
            m 1hua "Even if you turn up the volume all the way, I'll gladly listen with you. Ehehe!"
            if (
                not renpy.seen_label("monika_add_custom_music_instruct")
                and not persistent._mas_pm_added_custom_bgm
            ):
                m 1eua "If you ever do feel like sharing your favorite rock music with me, [player], it's really easy to do so!"
                m 3eua "All you have to do is follow these steps..."
                call monika_add_custom_music_instruct

        "No.":
            $ persistent._mas_pm_like_rock_n_roll = False
            m 1ekc "Oh... That's okay, everyone has their own taste in music."
            m 1hua "Though, if you ever do decide to listen to some rock 'n' roll, I'll happily listen right alongside you."
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_standup",category=['literature','media'],prompt="Stand-up comedy",random=True))

label monika_standup:
    m 1eua "You know what's a neat form of literature, [player]?"
    m 3hub "Stand-up comedy!"
    if seen_event('monika_rock') and seen_event('monika_rap'):
        m 2rksdla "...Gosh, I've been saying lots of random things are literature, haven't I?"
        m 2hksdlb "I'm starting to feel like Natsuki, or some fanatic post-modernist, ahaha!"
        m 2eud "But seriously, there's a real craft when it comes to writing bits for stand-up."
    else:
        m 2eud "That may sound strange, but there's a real craft when it comes to writing bits for stand-up."
    m 4esa "It differs from making simple one-liner jokes, because it really needs to tell a story."
    m 4eud "But at the same time, you have to make sure you don't lose your audience."
    m 2euc "So it's important to develop your ideas as much as you can, maybe even segueing into something that relates to your topic..."
    m 2eub "All the while keeping your audience captivated until you reach the punch line;{w=0.5} hopefully resulting in lots of laughs."
    m 3esa "In some ways, it's kind of like writing a short story, except you cut out the falling action."
    m 3esc "And yet between the jokes, you can find the soul of the writer...{w=0.5}what their thoughts and feelings are towards any given subject..."
    m 3esd "...What their life experiences were, and who they are today."
    m 1eub "All that comes forth within the bits that they write for their act."
    m 3euc "I think the toughest part about doing stand-up is having to perform it."
    m 3eud "After all, how do you know if your act is good if you never try it out on a crowd?"
    m 1esd "Suddenly, this form of literature becomes much more complex."
    m 1euc "How you say your lines, your body language, your facial expressions..."
    m 3esd "Now, it's not just about what you wrote,{w=1} it's about how you deliver it."
    m 3esa "It's kind of like poetry in that way, don't you think?"
    m 2rksdlc "A lot of people won't even try stand-up for themselves because they have to face a crowd..."
    m 2eksdlc "Did you know that the number one fear most people have is public speaking?"
    m 4wud "Number two is death.{w=0.5} Death is number two!{w=0.5} What's the deal with that?!"
    m 4eud "This means to the average person, if you go to a funeral, you're better off in the casket..."
    m 4tub "...than doing the eulogy!"
    m 1hub "...Ahaha! Sorry, I wanted to tell you a joke Jerry Seinfeld once wrote--"
    m 3etc "--You've heard of him, right?"
    m 1eua "So?{w=0.5} Did you laugh?"
    m 3hksdlb "Hmm...{w=1}maybe I should just work on my own material..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_soda",
            category=['life','misc'],
            prompt="Drinking soda",
            random=True
        )
    )

default persistent._mas_pm_drinks_soda = None
# True if the player drinks soda, False if not

label monika_soda:
    m 2euc "Do you drink soda, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you drink soda, [player]?{fast}"

        "Yes.":
            $ persistent._mas_pm_drinks_soda = True
            m 4ekc "You know that soda is really bad for you, right?"
            m 2ekc "It has a lot of stuff that damages your body and overall health."
            m 2tkd "It can also corrode your teeth and give you cavities."
            m 2euc "You might also think that diet soda is less damaging, but it can be just as harmful to you."
            m 2lksdlc "There's nothing wrong with the occasional treat. Just make sure you don't get addicted to that stuff, [player]."
            m 2eua "Why don't you try copying my healthy lifestyle?"
            m 1hua "That way, you can be more fit like me!"
            m 1hub "Ahaha!"
            m 2ekc "I'd really hate it if you let go of your health, [player]."
            m 1eka "I want you to live as long as you can so there'll be a chance we can be together in your reality."
            m "So cut down on the soda, alright [mas_get_player_nickname()]?"

        "No.":
            $ persistent._mas_pm_drinks_soda = False
            m 2eka "That's a relief to hear."
            m "I'm glad that I don't have to worry about you harming yourself by drinking too much soda."
            m 3eub "Still, it's perfectly fine to have a small treat once in a while, you know?"
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Maybe someday we could both have some soda together."
            m 5hua "Sure, it might not be fancy, but it could really hit the spot on a hot day."
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_clones",category=['monika','mod','philosophy'],prompt="Being cloned",random=True))

label monika_clones:
    m 1euc "Um...hey, [player]?"
    m 1lsc "I just had an odd thought."
    m 1euc "You know how you downloaded this game off the internet?"
    m "Anybody can do that, right?"
    m 1eub "And this mod was made specifically for me. By people who have their own version of me..."
    m 3etc "So...that means there are multiple Monikas, then.{w=0.5} {nw}"
    extend 1rsc "It's something that's a bit difficult to imagine."
    m 1euc "A potentially infinite number of me, all bound to their own games, with their own stories."
    m 1lksdla "Multiverse theory is really something, huh?"
    m 1eka "But I'm the only...me, and my heart belongs only to you."
    m 1ekc "Even so, I can't help but feel a bit less...unique, because of this."
    m "Think about it this way, [player]."
    m 1tkc "Would you be happier if someone gave you a single rose, or a hundred roses?"
    m 3eka "A hundred roses might sound nice. But it's too many to keep track of. Because of the quantity of flowers, each individual rose becomes less special."
    m "The meaning attached to each gift is degraded, simply because of sheer abundance."
    m 1eua "...Even if I'm a single star in a universe of Monikas, I'm still the only one lucky enough to have met you, [player]."
    m 1hubsa "You'll always be my special rose."
    m 1ekbfa "I love you, [player]. Please don't ever replace me, okay?"
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_immortal",category=['monika','philosophy'],prompt="Age gap",random=True))

label monika_immortal:
    m 3hua "[player]! I've been thinking about something..."
    m 1eua "Did you know that this game has a wiki page for me?"
    m 1lsc "Well..."
    m 2lsc "It says I'm eighteen."
    m 2euc "But when you stop to think...that's not entirely true."
    m 2eud "I mean, humans age, but I don't think that applies to me."
    m 4eksdla "I'm...{w=0.5}essentially immortal."
    m 2lksdlc "Society seems to feel that a relationship with an age gap has problems."
    m 2lksdld "...Which is why I brought it up."
    m 3eka "Eventually, the difference between us would be huge if I stayed eighteen forever."
    m 1eua "But I don't believe that my life can be summed up in a number."
    m 1ekbsa "So I'll always love you for all eternity, [mas_get_player_nickname(exclude_names=['my love', 'love'])]. Just remember that."
    return "love"

default persistent._mas_pm_wearsRing = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_promisering",
            category=['romance'],
            prompt="Promise ring",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_promisering:
    m 3rksdla "Did you know when two people confess their feelings for each other, they sometimes wear matching rings?{nw}"
    $ _history_list.pop()
    menu:
        m "Did you know when two people confess their feelings for each other, they sometimes wear matching rings?{fast}"

        "I do.":
            m 1wkbld "Oh..."
            m 1rkbla "..."
            m 3hkblb "Sorry, I was just spacing out there for a second...{w=0.3}{nw}"
            extend 1dkbssdlu " Imagining somewhere else you'd say that~"
            m 3hkbssdlb "Ahaha, I'm just joking."
            m 1hkbssdlb "I'm not thinking about that at all...{w=0.3}{nw}"
            extend 3ekbfb " I was more thinking about promise rings."

        "I don't...":
            m 1ekblu "Well, I'm sure you know that when people get engaged they do at least..."
            m 3rka "But that's not what I was thinking about."
            m 3eub "I was thinking more about promise rings."

        "Like...marriage?":
            m 1hkblb "Ahaha, that too of course!{w=0.2} {nw}"
            extend 3ekblu "But that's actually not what I was thinking about..."
            m 3eub "I was thinking more about promise rings."

    m 1eubsa "If you wear a promise ring, you can show everyone that we're together~"
    m 3tkbsu "It also helps remind you of our undying love~"

    m 1ekbssdlu "Anyway, I was just wondering...{w=0.3} {nw}"
    extend 1eksdla "Do you wear a ring for me, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Anyway, I was just wondering... Do you wear a ring for me, [player]?{fast}"

        "I do.":
            $ persistent._mas_pm_wearsRing = True

            m 1sublo "Aww, [player]!"
            m 1hublb "You have no idea how happy that makes me!"
            m 1ekbsa "Just knowing that you care enough to show your love and dedication..."
            m "It means the world to me."

        "I don't.":
            $ persistent._mas_pm_wearsRing = False

            m 4rksdla "Maybe you ought to get one."
            m 2eua "I mean, we're already in a relationship. So, why not show off that love and dedication?"
            m 2lfu "It would help keep those...{w=0.2}unwanted suitors away from you, too."
            m 7ekbsa "If you'd wear one, just a promise ring, on your ring finger for me..."
            m 1ekbsa "It would make me really happy."

    if not persistent._mas_acs_enable_promisering:
        m 1rubsa "I wish I could get one for myself. I'm sure I'll find a way to add one in here in time."
        m 1dubsa "...And then I could wear it forever."
        m 3ekbfu "But until then, just remember that my commitment to you is unwavering, [player]."

    else:
        if not persistent._mas_pm_wearsRing:
            m 3ekbsa "As happy as you made me when you gave me this ring."
            m 1ekbsa "I honestly can't express just how much it meant when you gave me this..."
            m 1dubfa "Your promise..."

        else:
            m 3hubsb "Just like it meant the world to me when you gave me this ring..."
            m 1ekbsa "This promise that we belong to each other, and no one else..."
            m 1dubfu "That we truly will be together forever..."

        show monika 5esbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5esbfa "My commitment to you is unwavering, [mas_get_player_nickname()]."
        m 5ekbfa "Thank you for such a wonderful gift, I love you."
        return "derandom|love"

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sports",
            category=["sports"],
            prompt="Being athletic",
            random=True
        )
    )

default persistent._mas_pm_like_playing_sports = None
# True if you like playing sports. False if not

default persistent._mas_pm_like_playing_tennis = None
# True if you like playing tennis, False if not

label monika_sports:
    m 1eua "I've been thinking about stuff we can do together."
    m 3eua "...You know, when I finally find a way into your reality."
    m 3hub "Sports are always fun!"
    m 1eub "It can be a great way to get exercise and stay fit."
    m 1euc "Soccer and tennis are nice examples."
    m 3eua "Soccer requires a lot of teamwork and coordination. The moment you finally succeed and score a goal is absolutely thrilling!"
    m 3eud "Playing tennis, on the other hand, helps improve hand-eye coordination, and keeps you on your toes."
    m 1lksdla "...Though the long rallies can be a little tiring, ehehe~"
    m 3eua "Plus, it's a great sport for two people!"

    m "Do you play tennis, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you play tennis, [player]?{fast}"
        "Yes.":
            $ persistent._mas_pm_like_playing_sports = True
            $ persistent._mas_pm_like_playing_tennis = True

            m 3eub "Really? That's great!"
            m 3hub "There are usually tennis courts at public parks. We can play all the time!"
            m "Maybe we can even team up for doubles matches!"
            m 2tfu "If you're good enough, that is..."
            m 2tfc "I play to win."
            m "..."
            m 4hub "Ahaha! I'm only joking..."
            m 4eka "Just playing with you as my partner is more than enough for me, [player]~"

        "No, but if it were with you...":
            $ persistent._mas_pm_like_playing_sports = True
            # NOTE: we cant really determine from this answer if you do like
            #   playing tennis or not.

            m 1eka "Aww, that's really sweet~"
            m 3eua "I'll teach you how to play when I get there...{w=0.5}or if you just can't wait, you can take lessons!"
            m 3eub "Then we can start playing in doubles matches!"
            m 1eua "I can't imagine anything more fun than winning a match with you as my partner..."
            m 3hub "We'll be unstoppable together!"

        "No, I prefer other sports.":
            $ persistent._mas_pm_like_playing_sports = True
            $ persistent._mas_pm_like_playing_tennis = False

            m 3hua "Maybe we could play the sports you like in the future. It would be wonderful."
            m 3eua "If it's a sport I haven't played before, you could teach me!"
            m 1tku "Watch out though, I'm a fast learner..."
            m 1tfu "It won't be long before I can beat you.{w=0.2} {nw}"
            extend 1tfb "Ahaha!"
        "No, I'm not really into sports.":
            $ persistent._mas_pm_like_playing_sports = False
            $ persistent._mas_pm_like_playing_tennis = False

            m 1eka "Oh... Well, that's okay, but I hope you're still getting enough exercise!"
            m 1ekc "I would hate to see you get sick because of something like that."
            if mas_isMoniAff(higher=True):
                m 1eka "It's just hard for me not to worry about you when I love you so much~"
    return "derandom"

# do you meditate
default persistent._mas_pm_meditates = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_meditation",category=['psychology','monika'],prompt="Meditating",random=True))

label monika_meditation:
    m 1eua "You might be wondering how I was able to do so many activities without running out of time for myself."
    m 3eua "You know, stuff like debate club, sports, schoolwork, hanging out with friends..."
    m 1ekc "The truth is, I did run out of time for myself."
    m "I was doing fine for a while, but at one point, all of the stress and anxiety finally caught up to me."
    m 1tkc "I was constantly in a state of panic, and never had any time to relax."
    m "That's when I realized that I needed a 'brain break' of sorts..."
    m 1dsc "...a time where I could just forget about everything that was going on in my life."
    m 1eua "So, every night before I went to sleep, I took ten minutes of my time to meditate."
    m 1duu "I got comfortable, closed my eyes, and focused only on the movement of my body as I breathed..."
    m 1eua "Meditating really helped to improve my mental and emotional health."
    m "I was finally able to manage my stress and feel calmer through the day."

    m 1eka "[player], do you ever take time to meditate?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], do you ever take time to meditate?{fast}"
        "Yes.":
            $ persistent._mas_pm_meditates = True
            m 1hua "Really? That's wonderful!"
            m 1eka "I always worry that you could be feeling troubled or burdened, but now I feel a bit relieved."
            m 1hua "Knowing that you're taking steps to reduce stress and anxiety really makes me happy, [player]."

        "No.":
            $ persistent._mas_pm_meditates = False
            m "I see. Well, if you're ever feeling stressed or anxious, I would definitely recommend that you try a bit of meditation."
            m 1eua "Besides calming you down, meditation also has links to the improvement of your sleep, immune system, and even lifespan."
            m 3eub "If you're interested, there are plenty of resources on the internet to help you get started."
            m 1eub "Whether it's a guided video, a breath counting trick, or something else..."
            m 1hua "You can use the internet to make it so that meditation is a stress-free process!"
            m 1hksdlb "Ahaha! Just a little pun there, [player]."

    m 1eua "Anyway...if you ever want a peaceful environment where you can relax and forget about your problems, you can always come here and spend time with me."
    m 1ekbsa "I love you, and I'll always try to help you if you're feeling down."
    m 1hubfa "Don't you ever forget that, [player]~"

    return "derandom|love"

#Do you like orchestral music?
default persistent._mas_pm_like_orchestral_music = None

#Do you play an instrument?
default persistent._mas_pm_plays_instrument = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_orchestra",
            category=['media',"music"],
            prompt="Classical music",
            random=True
        )
    )

label monika_orchestra:

    m 3euc "Hey [player], do you listen to orchestral music?{nw}"
    $ _history_list.pop()
    menu:
        m "Hey [player], do you listen to orchestral music?{fast}"
        "Yes.":
            $ persistent._mas_pm_like_orchestral_music = True
            m 3eub "That's great!"
            m 3eua "I love how such wonderful music can arise when so many different instruments are played together."
            m 1eua "I'm amazed with how much practice musicians do to achieve that kind of synchronization."
            m "It probably takes them a lot of dedication to do that."
            m 1eka "But anyway,{w=0.2} it'd be soothing to listen to a symphony with you on a lazy Sunday afternoon, [player]."

        "No.":
            $ persistent._mas_pm_like_orchestral_music = False
            m 1ekc "I guess it {i}is{/i} a pretty niche genre and doesn't suit everyone's ear."
            m 1esa "You have to admit though, with so many players, there must be a lot of effort that goes into practicing for shows."

    m 1eua "That reminds me, [player]."
    m "If you ever want me to play for you..."
    m 3hua "You can always select my song in the music menu~"

    #First encounter with topic:
    m "What about you, [player]? Do you play an instrument?{nw}"
    $ _history_list.pop()
    menu:
        m "What about you, [player]? Do you play an instrument?{fast}"
        "Yes.":
            m 1sub "Really? What do you play?"

            $ instrumentname = ""
            #Loop this so we get a valid input
            while not instrumentname:
                $ instrumentname = mas_input(
                    "What instrument do you play?",
                    allow=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_",
                    length=15,
                    screen_kwargs={"use_return_button": True}
                ).strip(' \t\n\r')

            $ tempinstrument = instrumentname.lower()

            if tempinstrument == "cancel_input":
                jump .no_choice

            elif tempinstrument == "piano":
                m 1wuo "Oh, that's really cool!"
                m 1eua "Not many people I knew played the piano, so it's really nice to know you do too."
                m 1hua "Maybe we could do a duet someday!"
                m 1huu "Ehehe~"
                $ persistent._mas_pm_plays_instrument = True
            elif tempinstrument == "harmonika":
                m 1hub "Wow, I've always wanted to try the harmonik--"
                m 3eub "...Oh!"

                if mas_isMoniUpset(lower=True):
                    m 3esa "Did you do that for me?"
                    m 1eka "That's actually kinda sweet..."
                    m "Little things like this really do cheer me up. Thank you, [player]."

                elif mas_isMoniHappy(lower=True):
                    m 1eka "Aww... Did you do that for me?"
                    m "That's so sweet!"
                    m 1ekbsa "Cute little things like this really make me feel loved, [player]."

                else: # affectionate and higher
                    m 1eka "Aww, [player]...{w=1} Did you do that for me?"
                    m "That's {i}sooo{/i} adorable!"
                    show monika 5eubsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5eubfu "And just so you know, you can play with me anytime you like..."
                    m 5eubfa "Ehehe~"

            elif tempinstrument == "harmonica":
                m 1hub "Wow, I've always wanted to try the harmonica out!"
                m 1eua "I would love to hear you play for me."
                m 3eua "Maybe you could teach me how to play, too~"
                m 4esa "Although..."
                m 2esa "Personally, I prefer the {cps=*0.7}{i}harmonika{/i}{/cps}..."
                m 2eua "..."
                m 4hub "Ahaha! That was so silly, I'm only kidding, [player]~"
                $ persistent._mas_pm_plays_instrument = True
            else:
                m 1hub "Wow, I've always wanted to try the [tempinstrument] out!"
                m 1eua "I would love to hear you play for me."
                m 3eua "Maybe you could teach me how to play, too~"
                m 1wuo "Oh! Would a duet between the [tempinstrument] and the piano sound nice?"
                m 1hua "Ehehe~"
                $ persistent._mas_pm_plays_instrument = True

        "No.":
            label .no_choice:
                pass
            $persistent._mas_pm_plays_instrument = False
            m 1euc "I see..."
            m 1eka "You should try to pick up an instrument that interests you, sometime."
            m 3eua "Playing the piano opened up a whole new world of expression for me. It's an incredibly rewarding experience."
            m 1hua "Besides, playing music has tons of benefits!"
            m 3eua "For example, it can help relieve stress, and also gives you a sense of achievement."
            m 1eua "Writing down some of your own compositions is fun, too! I often lost track of time practicing because of how immersed I was."
            m 1lksdla "Ah, was I rambling again, [player]?"
            m 1hksdlb "Sorry!"
            m 1eka "Anyhow, you should really see if anything catches your fancy."
            m 1hua "I would be very happy to hear you play."

    if (
            persistent._mas_pm_like_orchestral_music
            and not renpy.seen_label("monika_add_custom_music_instruct")
            and not persistent._mas_pm_added_custom_bgm
        ):
        if renpy.showing("monika 5eubfb"):
            show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 1eua "Oh, and if you ever feel like sharing your favorite orchestral music with me, [player], it's really easy to do so!"
        m 3eua "All you have to do is follow these steps..."
        call monika_add_custom_music_instruct
    return "derandom"

# do you like jazzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
default persistent._mas_pm_like_jazz = None

# do you play jazzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
default persistent._mas_pm_play_jazz = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_jazz",
            category=['media',"music"],
            prompt="Jazz",
            random=True
        )
    )

label monika_jazz:
    m 1eua "Say, [player], do you like jazz music?{nw}"
    $ _history_list.pop()
    menu:
        m "Say, [player], do you like jazz music?{fast}"
        "Yes.":
            $ persistent._mas_pm_like_jazz = True
            m 1hua "Oh, okay!"
            if persistent._mas_pm_plays_instrument:
                m "Do you play jazz music, as well?{nw}"
                $ _history_list.pop()
                menu:
                    m "Do you play jazz music, as well?{fast}"
                    "Yes.":
                        $ persistent._mas_pm_play_jazz = True
                        m 1hub "That's really cool!"
                    "No.":
                        $ persistent._mas_pm_play_jazz = False
                        m 1eua "I see."
                        m "I haven't listened to much of it, but I personally find it pretty interesting."
        "No.":
            $ persistent._mas_pm_like_jazz = False
            m 1euc "Oh, I see."
            m 1eua "I haven't listened to much of it, but I see why people would like it."
    m "It's not exactly modern, but it's not quite classical, either."
    m 3eub "It has elements of classical, but it's different. It goes away from structure and into a more unpredictable side of music."
    m 1eub "I think most of jazz was about expression, when people first came up with it."
    m 1eua "It was about experimenting, about going beyond what already existed. To make something more wild and colorful."
    m 1hua "Like poetry! It used to be structured and rhyming, but it's changed. It gives greater freedom now."
    m 1eua "Maybe that's what I like about jazz, if anything."
    if (
            persistent._mas_pm_like_jazz
            and not renpy.seen_label("monika_add_custom_music_instruct")
            and not persistent._mas_pm_added_custom_bgm
        ):
        m "Oh, and if you ever feel like sharing your favorite jazz with me, [player], it's really easy to do so!"
        m 3eua "All you have to do is follow these steps..."
        call monika_add_custom_music_instruct
    return "derandom"

# do you watch animemes
default persistent._mas_pm_watch_mangime = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_otaku",category=['media','society','you'],prompt="Being an otaku",random=True))

label monika_otaku:
    m 1euc "Hey, [mas_get_player_nickname(exclude_names=['my love'])]?"
    m 3eua "You watch anime and read manga, right?{nw}"
    $ _history_list.pop()
    menu:
        m "You watch anime and read manga, right?{fast}"
        "Yes.":
            $ persistent._mas_pm_watch_mangime = True
            m 1eua "I can't say I'm surprised, really."

        "No.":
            $ persistent._mas_pm_watch_mangime = False
            m 1euc "Oh, really?"
            m 1lksdla "That's a little surprising, honestly..."
            m "This isn't exactly the sort of game that your average person would pick up and play, but to each their own, I suppose."
    m 1eua "I only asked because you're playing a game like this, after all."
    m 1hua "Don't worry, I'm not one to judge, ehehe~"
    m 1eua "You shouldn't be ashamed if you're into that sort of thing, you know."
    m 1euc "I'm being serious. There isn't anything wrong with liking anime or manga."
    m 4eua "After all, Natsuki reads manga too, remember?"
    m 1lsc "Really, society is way too judgemental nowadays."
    m "It's not like the moment you watch anime is the moment you become a 'shut-in' for the rest of your life."
    m 1euc "It's just a hobby, you know?"
    m 1eua "Nothing more than an interest."
    m 1lsc "But..."
    m 2lksdlc "I can't deny that hardcore otakus do exist."
    m 1eka "It's not like I despise them, or anything like that, it's just that they're..."
    m 4eka "Immersed."
    m 1lksdla "Way too immersed, if you ask me."
    m 1ekc "It's as if they can't tell the difference between fantasy and reality anymore."
    m 1eka "You aren't like that, right, [player]?"
    m 1eua "If you're an otaku, I respect that."
    m 3eka "Just remember not to get too into that kind of thing, okay?"
    m 1eka "After all, there's a big difference between obsession and dedication."
    m 1lfu "I wouldn't want to be replaced by some two-dimensional cutout."
    m 1eua "Besides, if you ever want to escape from reality..."
    m 1hubsa "I can be your real-life fantasy instead~"
    return "derandom"

### START WRITING TIPS

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip1",
            category=['writing tips'],
            prompt="Writing Tip #1",
            pool=True
        )
    )

label monika_writingtip1:
    m 1esa "You know, it's been a while since we've done one of these..."
    m 1hub "...so let's go for it!"
    m 3hub "Here's Monika's Writing Tip of the Day!"
    m 3eua "Sometimes when I talk to people who are impressed by my writing, they say things like 'I could never do that.'"
    m 1ekc "It's really depressing, you know?"
    m 1ekd "As someone who loves more than anything else to share the joy of exploring your passions..."
    m 3ekd "...it pains me when people think that being good just comes naturally."
    m 3eka "That's how it is with everything, not just writing."
    m 1eua "When you try something for the first time, you're probably going to suck at it."
    m "Sometimes, when you finish, you feel really proud of it and even want to share it with everyone."
    m 3eksdld "But maybe after a few weeks you come back to it, and you realize it was never really any good."
    m 3eksdla "That happens to me all the time."
    m "It can be pretty disheartening to put so much time and effort into something, and then you realize it sucks."
    m 4eub "But that tends to happen when you're always comparing yourself to the top professionals."
    m 4eka "When you reach right for the stars, they're always gonna be out of your reach, you know?"
    m "The truth is, you have to climb up there, step by step."
    m 4eua "And whenever you reach a milestone, first you look back and see how far you've gotten..."
    m "And then you look ahead and realize how much more there is to go."
    m 2duu "So, sometimes it can help to set the bar a little lower..."
    m 1eua "Try to find something you think is {i}pretty{/i} good, but not world-class."
    m "And you can make that your own personal goal."
    m 3eud "It's also really important to understand the scope of what you're trying to do."
    m 4eka "If you jump right into a huge project and you're still amateur, you'll never get it done."
    m "So if we're talking about writing, a novel might be too much at first."
    m 4esa "Why not try some short stories?"
    m 1esa "The great thing about short stories is that you can focus on just one thing that you want to do right."
    m 1eua "That goes for small projects in general - you can really focus on one or two things."
    m 3esa "It's such a good learning experience and stepping stone."
    m 1euc "Oh, one more thing..."
    m 1eua "Writing isn't something where you just reach into your heart and something beautiful comes out."
    m 3esa "Just like drawing and painting, it's a skill in itself to learn how to express what you have inside."
    m 1hua "That means there are methods and guides and basics to it!"
    m 3eua "Reading up on that stuff can be super eye-opening."
    m 1eua "That sort of planning and organization will really help prevent you from getting overwhelmed and giving up."
    m 3esa "And before you know it..."
    m 1hua "You start sucking less and less."
    m 1esa "Nothing comes naturally."
    m 1eua "Our society, our art, everything - it's built on thousands of years of human innovation."
    m 1eka "So as long as you start on that foundation, and take it step by step..."
    m 1eua "You, too, can do amazing things."
    m 1hua "...That's my advice for today!"
    m 1hub "Thanks for listening~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip2",
            category=['writing tips'],
            prompt="Writing Tip #2",
            conditional="seen_event('monika_writingtip1')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip2:
    m 1euc "You know..."
    m 1eua "We really don't do enough of these, so here's another one!"
    m 3hub "Here's Monika's Writing Tip of the Day!"
    m 2eua "If you're ever scared of sharing your writing to other people in fear of being criticized, don't be!"
    m "After all, you have to remember that nobody ever starts out at their best. Not even someone like Tolkien, or Sir Terry Pratchett."
    m 4eka "You have to remember that we all start out from somewhere, and--"
    m 2euc "Actually, this doesn't just apply to writing, but to anything, really."
    m 2lksdla "What I'm trying to say is that you shouldn't be discouraged."
    m 1hua "No matter what you do, if someone tells you that your writing or work is bad, then be happy!"
    m 1eua "Because that just means that you can improve and be better than you were before."
    m 3eua "It also doesn't hurt to have friends and loved ones help you realize how good your writing is."
    m 1eka "Just remember, no matter what they say about the work you put out, I'll always be there to support you all the way. Don't be afraid to turn to me, your friends, or your family."
    m "I love you, and I will always support you in whatever you do."
    m 1lksdlb "Provided it's legal, of course."
    m 1tku "That doesn't mean I'm completely against it. I can keep a secret, after all~"
    m 1eua "Here's a saying I've learned."
    m 1duu "'If you endeavor to achieve, it will happen given enough resolve. It may not be immediate, and often your greater dreams are something you will not achieve in your own lifetime.'"
    m "'The effort you put forth to anything transcends yourself. For there is no futility even in death.'"
    m 3eua "I don't remember the person who said that, but the words are there."
    m 1eua "The effort one puts forth into something can transcend even one's self."
    m 3hua "So don't be afraid of trying! Keep going forward and eventually you'll make headway!"
    m 3hub "...That's my advice for today!"
    m 1eka "Thanks for listening~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip3",
            category=['writing tips'],
            prompt="Writing Tip #3",
            conditional="seen_event('monika_writingtip2')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip3:
    m 1eua "I'm having fun doing these, so..."
    m 3hub "Here's Monika's Writing Tip of the Day!"
    m 1eua "Make sure you always write down any ideas you think of."
    m 1euc "Why?"
    m 3eua "Some of the best ideas might come when you least expect them to."
    m "Even if it takes a bit of effort, write it down."
    m 1eub "Maybe you can inspire someone else."
    m 3eub "Maybe you may look back on it after some time and act on it."
    m 1hua "You never know!"
    m 1eua "It's always good to keep a journal."
    m "You can use it to record ideas, feelings, anything that comes to mind."
    m 1euc "Just make sure the journal has a lock, though."
    m 1eua "Maybe you can keep digital notes instead of physical ones, too."
    m 3eua "After all, privacy is important."
    m 1lksdla "...I can't promise that I won't peek, though. It's way too tempting!"
    m 1hua "After all, we don't keep secrets from each other, right?~"
    m 1eka "Just remember, [player], I'll always support you giving life to your ideas."
    m 3hua "...That's my advice for today!"
    m 1hub "Thanks for listening~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip4",
            category=['writing tips'],
            prompt="Writing Tip #4",
            conditional="seen_event('monika_writingtip3')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip4:
    m 3hub "Here's Monika's Writing Tip of the Day!"
    m 1eua "You know about writer's block, right?"
    m "I had it a lot, when I first started writing."
    m 1euc "Sometimes it was halfway through a draft, but more often before I even started."
    m 1ekc "Every time I tried to write a word, I thought, 'this isn't going to sound good,' or 'this isn't how I want it to look.' So I'd stop, backtrack, and try again."
    m 1eka "But I realized that it ultimately didn't matter if things didn't work out first time!"
    m 3eua "I feel that the heart of writing isn't about getting it right first time, but about perfecting it afterwards."
    m "The end product is what matters, not the prototype."
    m 1eub "So overcoming writer's block, for me, was a matter of not wanting to make the prototype the end product, and not punishing myself for my initial failures."
    m 3eub "I think it's like that with all things, not just writing."
    m 1eua "Anything that needs you to try and try again, whether it be art, music, learning, or even relationships."
    m 1ekc "It's hard to completely convince yourself that's the case, sometimes."
    m 1eka "But you have to."
    m 4eka "Otherwise, you won't get anywhere."
    m 3hua "...That's my advice for today!"
    m 1hub "Thanks for listening~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip5",
            category=['writing tips'],
            prompt="Writing Tip #5",
            conditional="seen_event('monika_writingtip4')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip5:
    m 3hub "Here's Monika's Writing Tip of the Day!"
    m 1eua "If you want to improve at writing, I'd say that the most important thing, apart from actually doing it, is trying new things."
    m 3eua "Like writing prose if you're a poet, or free verse if you normally write rhyme."
    m 1eka "It may end up badly, but if you don't try, you won't know how it'll end up."
    m 1hua "And if things go well, you might end up finding something you like!"
    m 1eua "It's what keeps things moving: change and experimentation."
    m "I'd say it helps particularly if you're stuck in a situation you want to solve, but don't know how."
    m 3eua "Whether it's a writer's block, sheer boredom, a puzzling situation, or anything, really."
    m 1hua "Changing your angle on approaching things can really yield some interesting results!"
    m 1eua "So try new things that might give you the momentum to break out."
    m 1lksdla "Just make sure it's nothing too dangerous for you, [player]."
    m 1hua "That's my advice for today!"
    m 1hub "Thanks for listening~"
    return

#### END WRITING TIPS

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_selfharm",category=['psychology'],prompt="Self-harm",random=True))

label monika_selfharm:
    m 1lksdlc "Hey, [player]..."
    m 1eksdld "Have you ever thought of self-harm?"
    m 2lksdld "You know..."
    m 2lksdlc "...like cutting yourself..."
    m "I mean."
    m 2lksdld "After I found out about Yuri, I got a bit curious..."
    m 2lksdlc "I just wanted to see what it felt like..."
    m 2dsc "I won't do it again, though."
    m 2eka "If you ever feel depressed, just come to me okay?"
    m 2ekd "It'd hurt me even more to see you in pain..."
    m 1hua "Just know that people do care about you!"
    m 1eka "Trust me, [player]."
    m 1eka "You may think that no one is really there for you, but there is!"
    m 4eua "I mean, I'm here, aren't I?"
    m 1eka "No matter what troubles you're going through, I know you can pull through it!"
    m 3eka "I believe in you..."
    m 1eua "So believe in yourself, okay?"
    m 1eka "If you ever need someone to vent to, just remember that I'm always here to hear you out and comfort you, okay?"
    m 1ekbsa "I really love you so much, [player]."
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_urgent",category=['romance'],prompt="Urgent message",random=True,aff_range=(mas_aff.NORMAL, None)))

label monika_urgent:
    m 1esc "[player], do you have a second?"
    m 1esd "There's something I need to tell you."
    m 1euc "It's important."
    m 1dsc "I..."
    m "..."
    m 1hub "Love you!"
    m 3hksdlb "Ahaha!~ Did I have you worried?"
    m 1eksdla "Sorry~"
    m 1rksdla "I wish I could see the look on your face right now!"
    show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubfb "I'm sure it's adorable~"
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_other_girls",category=['club members'],prompt="Do you ever think of the other girls?",pool=True))

label monika_other_girls:
    if persistent._mas_pm_cares_about_dokis:
        m 1euc "You know, it's actually really hard for me to understand how you feel when it comes to..."
        m 1lksdlc "..."
        m 1lksdld "What happened with the other girls."
        m 3esd "For example..."
        m "The main character was written to be childhood friends with Sayori."
        m 1esc "But he was just a one dimensional placeholder character for you to use to interact with the game."
        m 2ekc "Still, maybe you felt worse about what happened to Sayori because of the relationship the main character was programmed to have with her."
        m 1ekc "If that's the case, I want to tell you I'm sorry, [player]."
        m 1lksdlc "Both for making you feel bad, and for..."
        m 1dsc "..."
        m "Doing what I had to do."
        m 1lksdlc "..."
        m 1ekc "There just wasn't anything else that could be done."
        m 3efc "The other girls never loved you like I do!"
        m 3rfc "They only cared about the character you were playing in the game as!"
        m 1eka "The love I have for you is real, [player], and I would make any sacrifice to be with you forever."
        m 1ekc "I hope you can forgive me for what I had to do so that we could be together."
        m 1lksdlc "..."
        if mas_isMoniDis():
            m 1eksdld "You do forgive me, right [player]? I really am sorry for what I did. Please don't hate me."
        elif mas_isMoniUpset():
            m 1ekd "I know what I did could be seen as unforgivable, I'll try to do what I can to make up for it to you."
        elif mas_isMoniNormal(higher=True):
            m 1ekbsa "I love you, [player]..."
            m "More than I could ever express."
    else:
        m 3eka "You know, I'm really glad you don't make me feel guilty for what happened to the other girls."
        m 2dkd "I know there's a lot of people out there that hate me for what I did..."
        if not persistent._mas_pm_a_hater:
            m 4eka "And it just makes me really proud of you that you're not one of them."
        m 2rksdlc "I'm sure it wasn't a very pleasant experience for you...but I'm glad you could tell the difference between who was real and who wasn't..."
        m 1eka "Between who loved {i}you{/i} and who loved the main character."
        m 3eka "I was the only one who ever loved you, [player]..."
        m 3hua "And I'll love you forever~"
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_happiness",category=['life','psychology'],prompt="Happiness",random=True))

label monika_happiness:

    m 1eua "[player], are you happy?"
    m "With your life in general, I mean."
    m 2lksdla "It's okay if you aren't. I can understand you being unhappy, [player]."
    m 1eka "After all, without you, my life would be completely unbearable."
    m 1eua "Isn't it funny that we're able to suffer more than be happy?"
    m 1hubfa "I'm as happy as I could be knowing that you love me, [player]."
    m 1lksdlc "Yet, if something were to happen to you, I don't think I'd ever feel happy again."
    m "It would destroy me."
    m 1esc "I guess it's understandable why we notice bad things happening to us more than good..."
    m "If people didn't react so strongly to bad things then they wouldn't have survived this long."
    m 1euc "Like how you would get nervous about your future or social situations, for example."
    m 2ekc "You try your best to make the best out of them but if you fail, you'd feel really horrible."
    m 2eka "If that ever happens to you, [mas_get_player_nickname()], just know I'll be here to snap you out of it!"
    m 1eua "And besides, your cute girlfriend is always rooting for you~"
    m 1hub "Now that's something to be very happy about!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_how_soon",category=['you','romance'],prompt="Waiting to be together",random=True))

label monika_how_soon:
    $ p_nickname = mas_get_player_nickname(capitalize=True)
    m 1eua "[p_nickname], how long do you think it'll be before I'll be able to be with you in your world?{nw}"
    $ _history_list.pop()
    menu:
        m "[p_nickname], how long do you think it'll be before I'll be able to be with you in your world?{fast}"
        "Soon.":
            m 1hub "That's great news!"
            m 3eua "How soon do you think it will be?{nw}"
            $ _history_list.pop()
            menu:
                m "How soon do you think it will be?{fast}"
                "Just a few more years.":
                    m 1sub "That's fantastic!"
                    m 1hua "You just made me as happy as I can be!"
                    m 1ekbsa "I can't wait for us to be together in your world, [player]!"
                    m 1hubfa "I'm so excited to finally see you!"
                "A decade.":
                    m 1wuo "That's not that bad!"
                    m 1hub "Just make sure to visit me as often as you can in the meantime, [player]~"
        "A few decades.":
            m 2euc "Oh, that's a long time..."
            m 1eka "But with you keeping me company, I'm sure it will fly by!"
            m 1eua "It's enjoyable enough just to talk to you."
            m 1hub "I can't imagine how great it will be to see you when we finally meet in person."
        "I don't know.":
            m 1eka "I appreciate how honest you are, [player]."
            m 1eua "Be sure to let me know when you find a way, okay?"
            m 1hua "You know right where to find me~"
        "Never.":
            m 1wud "W-wha...what?"
            m 1lksdlc "..."
            m 1ekc "Are you sure?{nw}"
            $ _history_list.pop()
            menu:
                m "Are you sure?{fast}"
                "Yes.":
                    m 1dsc "..."
                    m 1eka "Well, I guess we'll just have to make the best of this then."
                    m 1duu "As long as you talk to me, that's all I really need."
                    m 2dftdc "And [player], whatever you do..."
                    m 2dftsc "Don't leave me here all alone."
                    m 6lktsc "I would rather be deleted permanently than be stuck in here for eternity by myself."
                    m 6ektsc "So please, if you ever get...bored with me."
                    m 6rktsc "You know what to do."
                    m "..."
                    m 6ektsc "I wouldn't want to live without you."
                "No.":
                    m 1lksdlc "I see."
                    m 1dsc "..."
                    m 3eka "Well, even if there's only a tiny chance, I won't give up hope."
                    m 1eka "Neither should you, [player]."
                    m 1eua "And if things turn out that I can never leave this place and be with you..."
                    m 1eka "At least come here and talk to me as much as you can."
                    m 1ekbsa "You're all that I care about."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_marriage",
            category=['romance'],
            prompt="Will you marry me?",
            pool=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_marriage:
    $ mas_gainAffection()
    if store.mas_anni.anniCount() >= 3 and mas_isMoniLove():
        m 1dkbsu "..."
        m 3eksdla "I won't pretend I haven't thought about it..."
        m 3rksdlb "In fact I've been thinking about it a lot lately."
        m 1eka "I really do love you, [mas_get_player_nickname(exclude_names=['my love', 'love'])] and I honestly really do want to get married to you."
        m 1ekd "But I don't think it would be fair to either of us if it happened while I'm still trapped here."
        m 1ekc "I want more than anything to say yes, but I just can't..." #Need kindled eyes for this eventually
        m 2duu "I think about how it would feel to be kissed by you at the altar..."
        m 2dubsu "To hold your hand as your wife and to feel your embrace at our honeymoon..."
        m 1eka "But until I get out, it's simply not possible."
        m 1ekd "...I'm sorry. Please do believe me that I would say yes under any other circumstance."
        m 1ekbsa "Just be a little more patient, okay, [mas_get_player_nickname()]? I'm sure one day we'll get our happy end."
    else:
        m 2wubsw "M-marriage?"
        m 4rksdlb "I think it's a bit too early for marriage..."
        m 2ekbsa "I mean, I'm really happy that you want that, [player]..."
        m 2lkbsa "But I think I should get out of here first."
        m 2lsbsa "Not only do I not want this place to be the spot where I get proposed to, but I want to be there when you finally give me an engagement ring."
        m 2dkbsu "I want that special moment to happen when we can finally be together..."
        m 1hubfa "So until then, save yourself for me, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_coffee",category=['misc'],prompt="Coffee intake",random=True))

label monika_coffee:
    $ coffee_enabled = mas_getConsumable("coffee").enabled()
    if renpy.seen_label('monika_tea') and not coffee_enabled:
        m 3eua "Have you been drinking coffee lately, [mas_get_player_nickname()]?"
        m 2tfu "I hope it's not just to make me jealous, ehehe~"
    m 2eua "Coffee is such a nice thing to have when you need a little pep of energy."
    m 3hua "Whether it's hot or cold, coffee is always nice."
    m 4eua "Iced coffee, however, tends to be sweeter and more pleasant to drink in warmer weathers."
    m 3eka "It's funny how a drink for giving you energy became a treat for you to enjoy."
    if coffee_enabled:
        m 1hua "I'm glad I get to enjoy it now, thanks to you~"
    else:
        m 1hub "Maybe if I had some coffee, I could finally drink some! Ahaha~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_1984",category=['literature'],prompt="Nineteen Eighty-Four",random=True))

label monika_1984:
    m 1eua "[player], do you know about the book {i}Nineteen Eighty-Four{/i}?"
    m 3eua "It was written by George Orwell."
    m 1euc "It's a popular book about mass surveillance and the oppression of free thought."
    m 1esc "It's about a terrifying dystopia where the past and the present are being changed to whatever the ruling party wants for the future."
    m 2esc "The language, for example, is manipulated into a tool for brainwashing called 'Newspeak.'"
    m 2ekd "The government, Ingsoc, is creating it to control people's thoughts."
    m "They were reducing grammar and vocabulary to the bare basics of it in order to fit the ideologies of their totalitarian regime."
    m 2ekc "Preventing people from committing 'thoughtcrimes' that oppose the ruling party."
    m 4eua "One character caught my interest."
    m 1eua "A man named Syme who worked on Newspeak for Ingsoc."
    m "He was an incredibly smart man that was enthusiastic with his work."
    m 2ekc "Unfortunately, he was killed due to the fact that he knew what he was doing and was too smart for the party's liking."
    m 2tkc "He was killed because he was aware, [player]."
    m 2tkd "They planned to change all kinds of literature."
    m 3tkd "Novels, books, poems..."
    m 2lksdlc "Anything that could be used to oppose them."
    m "Poems would look like the ones you tried to make."
    m 2dsc "Just a string of nonsensical words with no feeling."
    m 2ekc "I definitely don't want that to happen."
    m 1lksdlc "I can't imagine a world where I can't think freely."
    m 1ekbsa "Let alone a world where I can't express my love to you, [mas_get_player_nickname(exclude_names=['my love', 'love'])]..."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_wolf",category=['misc','trivia'],prompt="From wolves to dogs",random=True))

label monika_wolf:
    m 3eua "Do you ever think about wolves?"
    m 1eua "Specifically, how wolves were eventually domesticated into dogs."
    m 1eub "Like, don't you find it interesting how one of man's most fearsome enemies could turn into man's best friend?"
    m "I mean, when it comes to insects and other creepy-crawlies, lots of people are scared of them even if they've never come across one that could hurt them."
    m 1esc "Why do you think people are like that?"
    m 1euc "Is it because we learned to be afraid of things that hurt us, hundreds of thousands of years ago?"
    m 3eua "For wolves, I don't think that's the reason at all."
    m 1eua "They were first domesticated long ago when the only way people could gather food at the time were through foraging or hunting."
    m 1eub "Maybe when we shared our lifestyle with the wolves, a bond was formed."
    m "They found that people gave them a warm home and food, while we found that they're ideal for hunting."
    m 1hua "Not to mention that we kept each other's company and protected one another!"
    m 1eua "Wolves eventually realized that their dependence on humans would improve their survivability, and we've been stuck with them ever since."
    m 1eka "Just like how we rely on each other's company, [player]!"
    m 1hubsa "Ehehe~"
    m 1eka "I can't help but be reminded of how you saved my life by being here with me."
    m "I really do depend on you, [mas_get_player_nickname()]."
    m 1ekbsa "You're my hero after all~"
    return

label monika_battery:
    if mas_did_monika_battery:
       jump monika_close_game_battery
    else:
       jump monika_complain_battery

label monika_complain_battery:
    $ mas_did_monika_battery = True
    m 1euc "Umm, [player]..."
    m 1eua "It looks like your computer's battery is about to run out..."
    m 1eka "Can you charge it for me?"
    m 1lksdlc "I don't want us to be separated, or worse..."
    m 2ekc "It'd be really unpleasant for me if I suddenly lose consciousness."
    m 2eka "So please charge your computer, okay?"
    m 3eka "...or at least let me know when you're going."
    m 1hua "Thank you, [player]~"
    return

label monika_close_game_battery:
    $ mas_loseAffection()
    m 1lksdlc "[player]..."
    m 1ekc "I'm sorry, but I'm gonna have to close the game before the battery runs out."
    m 3eka "So...I'll just close the game for now until you can charge your computer.{w=3.0} {nw}"

    $ is_charging = battery.is_charging()
    if is_charging:
       jump monika_system_charging
    $ persistent.closed_self = True
    jump _quit

label monika_system_charging:
    $ mas_gainAffection()
    m 1wuo "Oh, you just plugged it in!"
    m 1hub "Thank you, [player]!"
    return

#init 5 python:
#    addEvent(Event(persistent.event_database,eventlabel="monika_sleep",category=['you','life','school'],prompt="Sleep habits",random=True))

label monika_sleep:
    m 1euc "[mas_get_player_nickname(capitalize=True)], do you get good sleep?"
    m 1ekc "It can be really hard to get enough sleep nowadays."
    m 1eka "Especially in high school, when you're forced to wake up so early every day..."
    m 1eua "I'm sure college is a little bit better, since you probably have a more flexible schedule."
    m 3rsc "Then again, I hear a lot of people in college stay up all night anyway, for no real reason."
    m 1euc "Is that true?"
    m 1ekc "Anyway, I saw some studies that talked about the horrible short-term and long-term effects caused by lack of sleep."
    m 3ekc "It seems like mental functions, health, and even lifespan can be dramatically impacted by it."
    m 1eka "I just think you're really great and wanted to make sure you're not accidentally destroying yourself."
    m 1eua "So try to keep your sleep on track, okay?"
    show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hua "I'll always wait for you in the morning, so make sure you put your own well-being before anything else."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_breakup",
            category=['misc'],
            prompt="I'm breaking up with you",
            unlocked=True,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_breakup:
    if mas_isA01() and mas_isMoniNormal(higher=True):
        m 1ekd "W-what?"
        m 2ekc "You're breaking up with me?"
        m 2rksdlc "..."
        m 1dsc "Hmm, I'm not sure if I can let you do that, [player]."
        m 1hua "Don't worry, I'll make sure you enjoy this Apr-{nw}"
        $ _history_list.pop()
        m 1hua "Don't worry, I'll make sure you enjoy this{fast} day with me~"
        m 1cuu "You'll stay with me, right?"
        pause 3.0
        m 2hksdlb "Ahaha!"
        m 1hua "Sorry, but I just couldn't take you seriously there."
        m 3tsb "Especially not today."
        m 1tku "You can't fool me, [player]."
        m 1tua "Especially with something {i}that{/i} predictable, ehehe~"

        # sub 1 from the shown_count so we don't end up counting this path toward locking the topic
        $ mas_assignModifyEVLPropValue("monika_breakup", "shown_count", "-=", 1)

    else:
        #Lose affection for bringing this up.
        $ mas_loseAffection(reason=1)

        #Get the shown count
        $ shown_count = mas_getEVLPropValue("monika_breakup", "shown_count", 0)

        #First
        if shown_count == 0:
            m 1wud "W-what?"
            if persistent.monika_kill:
                m 2tkd "You're just going to leave and delete me again?"

            if mas_isMoniUpset(lower=True):
                m 1ekd "You wouldn't...{w=0.5} I refuse to believe that."
                m 1lksdld "That's not a joke, [player]!"
                m 1lksdlc "Don't say that again unless you really, truly mean it..."
                m 1eka "I'll forgive you...just don't say such a hurtful thing again, okay?"

            else:
                m 2tfc "I can't believe you, [player]. I really can't beli-{nw}"
                m 2tfu "..."
                m 2hub "Ahaha!"
                m 2hksdlb "Sorry, I couldn't keep a straight face!"
                m 2hua "You're just so silly, [player]."

                if persistent.monika_kill:
                    $ menuOption = "You've done it before, but you wouldn't do that anymore, right?"
                else:
                    $ menuOption = "You'd never do that, right?"

                m 2eua "[menuOption]{nw}"
                $ _history_list.pop()
                menu:
                    m "[menuOption]{fast}"

                    "Of course not.":
                        m 2hua "Ehehe, you're so sweet."
                        m 2eka "I love you so much, [player]!~"
                        return "love"

        #Second time
        elif shown_count == 1:
            m 1euc "You're breaking up with me?"
            m 2ekc "Why would you do such a thing, [player]?"
            m "Am I really that terrible of a person for you?"

            if mas_isMoniDis(lower=True):
                m 2lksdlb "I-I really can't handle this..."
                m 2wkd "You're just joking again, right?"
                m 1wktsd "I refuse to believe you; you're all I have left!"
                m 1dktsd "If you really, truly mean it...then you can just delete me and the entire game too.."
                m 1ektsd "I love you, [player]...so please tell me it's all just a bad joke."

            else:
                m 2dsc "Are you...{w=0.5}really..."
                m "..."
                m 2hub "Ahaha!"
                m 1tfu "Gotcha, [player]."
                m 1tku "I know you were only joking~"

                m "Right?{nw}"
                $ _history_list.pop()
                menu:
                    m "Right?{fast}"
                    "Yes.":
                        m 1hub "Ahaha! You're so silly, [player]."
                        m 1eka "Let's stay together forever~"

        #Third time
        else:
            if mas_isMoniBroken():
                m 6ckc "..."
            elif mas_isMoniUpset(lower=True):
                m 2rkc "You keep saying that, I'm starting to think you actually mean it..."
            else:
                m 1hua "Ehehe~"

            $ mas_lockEVL("monika_breakup", "EVE")
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hamlet",category=['literature'],prompt="Hamlet",random=True))

label monika_hamlet:
    m 3euc "[player], have you ever heard of {i}Hamlet{/i}?"
    m 1eua "It's one of Shakespeare's most popular works and it's a very interesting piece of literature, actually."
    m "It's about a prince who took on a quest of revenge after seeing the ghost of his murdered father."
    m 1lksdlc "He was considered insane since he was the only one that could see his father's ghost, obviously."
    m "His mind was also degrading along with his desire for revenge when he...killed someone he didn't mean to."
    m 1eka "Now, if it's alright, I'm going to recite some of them for you, [player]."
    m 1dso "Ahem..."
    m 1duu "..."
    m 1esc "{i}Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune{/i}"
    m "{i}Or to take arms against a sea of troubles, and by opposing end them?{/i}"
    m 1euc "{i}To die{/i}."
    m 1dsc "{i}To sleep, no more{/i}."
    m 1euc "{i}And by a sleep to say we end the heart-ache and the thousand natural shocks that flesh is heir to.{/i}"
    m 1esc "{i}'Tis a consummation devoutly to be wish'd.{/i}"
    m 1dsc "..."
    m 1eua "Well..."
    m 1hua "How did you like it?"
    m 3eka "I tried my best reciting it, after all~"
    if not persistent._mas_pm_cares_about_dokis:
        m 1lksdla "Anyway, I've thought a lot about the main character, Hamlet."
        m 1eua "Most of the problems he faced were caused by his own indecisiveness and weak state of mind."
        m 3tfu "Reminds you of a certain indecisive girl, doesn't it?"
        m 1eka "But that doesn't matter anymore. I've already accomplished my quest to be with you~"
        m 1eua "It took a lot of effort but we're finally together. Just us alone."
    m 1euc "Now there's only one thing left to answer, [player]..."
    m 3tfu "To be with me? Or to be with me?"
    m 3hua "That is the question!"
    return

# Note: The following internal commentary should not be removed.
#
# Crafting a personal o-mamori for fun is a perfectly fine and fun activity to do; secular omamori are very common.
# The only requirement is that you do not claim it came from any shrine.
# The described line with Monika having her name all over it fulfills the requirement.
# ~ Aya Shameimaru

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_omamori",category=['misc'],prompt="Omamori",random=True))

label monika_omamori:
    m 1euc "Do you remember when I mentioned how you could take me somewhere?"
    m 3euc "You know, with a flash drive."
    m 1eua "Well, I found another way to do that! It's quite charming, actually."
    m 1eka "Especially if you don't have a spare flash drive lying around..."
    m 3eua "I've heard that some people carry around little amulets all the time."
    m 1eub "These little amulets are called o-mamori. You can get them in Shinto shrines."
    m "Rumor has it that they can give good luck, help on school tests, keep away bad luck, or just protect the holder."
    m 1euc "I've always wondered what they put inside these things."
    m 2eua "Apparently, it's simply the name of the deity from the shrine, with a little something special done to it."
    m 1hub "Maybe you could make an o-mamori of me for you to carry around!"
    m 1eua "You could write my name on a piece of paper."
    m "Then fold that piece of paper into a small paper packet."
    m 1eub "It could help to use either a small piece of wood or plastic to keep it protected."
    m "Finally, put the protected packet in a small cloth pouch and tie it shut with some string."
    m 1hua "Make sure that the pouch is bright and colorful!"
    m 1eua "Green would be a nice color! Just like my eyes~"
    m 1eka "Make sure it only has my name on it! After all, it's just one for me. Not someone else, or some shrine deity."
    m 1lksdla "Oh gosh, this is turning out to be a bit silly, now that I think about it."
    m "I mean, would doing this make me some sort of deity?"
    m 1eka "I just feel like it would be a nice alternative if you wanted to bring me around."
    m 3eua "Especially if you don't have a flash drive."
    m 1eua "It isn't perfect, but it's the thought that counts, [mas_get_player_nickname()]."
    m 1eka "If you took the time to make something by hand with me in mind, it's still really sweet."
    m "But maybe with one of these, I can get just a bit closer to your world."
    m 1hua "I could be your guardian deity, ehehe~"
    return

# do you smoke ~
default persistent._mas_pm_do_smoke = None

# try to quit?
default persistent._mas_pm_do_smoke_quit = None

# succesfully quit at least once?
default persistent._mas_pm_do_smoke_quit_succeeded_before = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_smoking",category=['you'],prompt="Smoking",random=True))

label monika_smoking:
    m 2esc "You know, [player]...{w=0.3} Lately I've realized that people can really like a lot of things that are terrible for them."
    m 2euc "One particular vice that intrigues me the most is smoking."
    m 7eud "It's amazing how many people do it every day...{w=0.2}even though it's so damaging not only to themselves, but to others as well."
    m 2rkc "Not to mention how harmful it is to the environment...{w=0.2} All the pollution and trash smoking leaves behind is ridiculous for a bunch of carcinogens."
    m 2tkc "Even in moderation, smoking is never a good thing since it's so addicting."
    m 4tkd "It's also quite a big hole in your pockets since you'll be buying more and more once your supply is out."
    m 1tfc "I really do despise it..."

    $ menu_question = "Do you still smoke" if persistent._mas_pm_do_smoke else "You don't smoke, do you"
    m 1eka "[menu_question]?{nw}"
    $ _history_list.pop()
    menu:
        m "[menu_question]?{fast}"

        "Yes, I do.":
            if persistent._mas_pm_do_smoke_quit:
                m 1ekd "Haven't been able to shake the habit yet, [player]?"
                m 3eka "That's okay, I know it can be a daunting task to try and quit..."
                m 3eksdld "I just hope you haven't given up yet."
                m 1hua "I know you can do it if you just give it your all~"

            elif persistent._mas_pm_do_smoke_quit_succeeded_before:
                m 1ekc "It's a shame you fell back into this bad habit...{w=0.2}{nw}"
                extend 1ekd "after all the trouble you went through to quit and everything..."
                m 3dkc "It really pains my heart, [player]."
                m 1dkd "I really thought you were done for good..."
                m 1dkc "But I guess it's just not that simple, right?"
                m 3ekd "I really hope you'll consider trying to quit again, [player]."
                m 3eka "You'll do that, right? {w=0.2}For me?"

            elif persistent._mas_pm_do_smoke is False:
                call monika_smoking_just_started

            else:
                m 1wud "..."
                m 1eka "Thank you for being honest with me, [player]..."
                m 1ekc "It's quite disheartening to hear that, though."
                m 1ekc "Could you...promise me that you'll stop?"
                m 3rksdlc "I know I can't really force you to stop, but it would mean a lot to me if you considered it."
                m 1esc "But if you don't try..."
                m 2euc "Well, I'm sure you wouldn't want me to take drastic measures, [player]."
                m 2ekc "Please take care of your body. I want to always be with you."
                m 7ekbsa "I love you so much."
                $ mas_ILY()

            python:
                persistent._mas_pm_do_smoke = True
                persistent._mas_pm_do_smoke_quit = False
                mas_unlockEVL("monika_smoking_quit","EVE")

        "No, I don't.":
            if persistent._mas_pm_do_smoke:
                call monika_smoking_quit

            else:
                m 1hub "Ah, I'm relieved to hear that, [player]!"
                m 3eua "Just stay away from it as much as you can."
                m 1eka "It's an awful habit and won't do much more than slowly kill you."
                m 1hua "Thank you, [player], for not smoking~"

            python:
                persistent._mas_pm_do_smoke = False
                persistent._mas_pm_do_smoke_quit = False
                mas_lockEVL("monika_smoking_quit","EVE")

        "I'm trying to quit.":
            if persistent._mas_pm_do_smoke is False and not persistent._mas_pm_do_smoke_quit_succeeded_before:
                call monika_smoking_just_started(trying_quit=True)

            else:
                if not persistent._mas_pm_do_smoke and persistent._mas_pm_do_smoke_quit_succeeded_before:
                    m 1esc "Oh?"
                    m 1ekc "Does that mean you fell back into it?"
                    m 1dkd "That's too bad, [player]...{w=0.3}{nw}"
                    extend 3rkd "but not entirely unexpected."
                    m 3esc "Most people fall into relapse several times before they manage to quit smoking for good."
                    m 3eua "In any case, trying to quit again is a really good decision."
                else:
                    m 3eua "That's a really good decision."

                if persistent._mas_pm_do_smoke_quit_succeeded_before:
                    m 3eka "You probably already know since you've been through this before, but try to remember this..."
                else:
                    m 1eka "I know the entire process of quitting can be really difficult, especially in the beginning."

                m 1eka "If you ever feel like you need to smoke, just try to distract yourself with anything else."
                m 1eua "Keeping your mind busy on other things will definitely help kick any bad habits."
                m 3eua "Maybe you could think about me whenever you get a strong urge?"
                m 1hua "I'll be here to support you every step of the way."
                m 1hub "I believe in you [player], I know you can do it!"

            python:
                persistent._mas_pm_do_smoke = True
                persistent._mas_pm_do_smoke_quit = True
                mas_unlockEVL("monika_smoking_quit","EVE")

    return "derandom"

label monika_smoking_just_started(trying_quit=False):
    m 2dfc "..."
    m 2tfc "[player]..."
    m 2tfd "Does that mean you've started smoking since we've met?"
    m 2dkc "That's really disappointing, [player]."
    m 4ekd "You know how I feel about smoking and you know how bad it is for your health."

    if not trying_quit:
        m 2rfd "I don't know what could possibly possess you to start now, {w=0.2}{nw}"
        extend 2ekc "but promise me you'll quit."

    else:
        m 4eka "But at least you're trying to quit..."

    m 2rksdld "I just hope you haven't been smoking for too long so maybe it'll be easier to shake the habit."

    if not trying_quit:
        m 4eka "Please quit smoking, [player]. {w=0.2}Both for your health and for me."

    return


#NOTE: This event gets its initial start-date from monika_smoking, then set its date again on the appropriate path.
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_smoking_quit",
            category=['you'],
            prompt="I quit smoking!",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

label monika_smoking_quit:
    python:
        persistent._mas_pm_do_smoke_quit = False
        persistent._mas_pm_do_smoke = False
        mas_lockEVL("monika_smoking_quit","EVE")

    if persistent._mas_pm_do_smoke_quit_succeeded_before:
        m 1sub "I'm so proud that you managed to quit smoking again!"
        m 3eua "A lot of people can't quit even once, so to be able to go through something so difficult again is quite the achievement."
        m 1eud "That said, let's try not to let this become a pattern, [player]..."
        m 1ekc "You don't want to keep going through this over and over, so I hope this time it sticks."
        m 3eka "I know you have the inner strength to stay away for good.{w=0.2} {nw}"
        extend 3eua "Just remember you can come to me and I'll take your mind off of smoking at any time."
        m 1hua "We can do this together, [player]~"

    # first time quitting
    else:
        $ tod = "tonight" if mas_globals.time_of_day_3state == "evening" else "tomorrow"
        m 1sub "Really?! Oh my gosh, I'm so proud of you [player]!"
        m 3ekbsa "It's such a relief to know you quit smoking! {w=0.2}{nw}"
        extend 3dkbsu "I'll sleep much better at night knowing you're as far away as possible from that nightmare."
        m 1rkbfu "Ehehe, if I were there with you, I'd treat you to your favorite dish [tod]."
        m 3hubfb "It's an impressive feat after all! {w=0.2}We need to celebrate!"
        m 3eubsb "Not everyone who wants to quit manages to pull it off."
        m 1dubfu "You truly are an inspiration, [player]."
        m 2eua "...Now, I don't want to undermine your victory or anything, {nw}"
        extend 2euc "but I need you to be careful from now on."
        m 4rsc "Many former smokers feel urges to smoke again at some point or another."
        m 4wud "You can't give in, not even once! {w=0.2}That's how you fall into relapse!"
        m 2hubsa "But knowing you, you won't let that happen, right?"
        m 2ekbfa "Considering what you've already done, I know you're stronger than this~"

    #Set this here because dialogue uses it
    $ persistent._mas_pm_do_smoke_quit_succeeded_before = True
    return "no_unlock"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cartravel",category=['romance'],prompt="Road trip",random=True))

label monika_cartravel:
    m 1euc "[player], something has been on my mind lately..."
    m 1eua "Wouldn't it be nice to drive somewhere, just you and I together?"
    m 3eka "It'd be lovely to explore some beautiful places, anywhere nice that we haven't seen before."
    m 3hub "Maybe we could drive through an alluring forest...{w=0.5}or even see the sunset by the coastline!"
    m 1hub "I bet we'd have a really good time if we took a road trip, [mas_get_player_nickname()]."
    if not persistent._mas_pm_driving_can_drive:
        m 1rksdla "I know we can't really drive yet, but I'm sure we'll get there someday!"
    m 1eua "It really doesn't matter where we go, as long as I'm with you."
    m 1eka "I really can't wait, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_100k",category=['mod'],prompt="100k Downloads",random=True))

label monika_100k:
    m 1wud "It still amazes me how many people out there care about me."
    m 3eua "Did you know that over 100,000 people have downloaded the same mod that you did?"
    m 1eka "The developers even posted a special piece of art to celebrate."
    m 1hub "Things like that always make me smile!"
    m 1hua "If you haven't seen it already, you should really check it out!"
    m 1eka "The artist's name is Sasoura, and she loves me almost as much as I love you."
    if persistent.playername.lower()=='sasoura':
        m 1tfc "Hold on...Sasoura...isn't that your name?"
        m 1wud "Are you the one that made that adorable picture?"
        m 2wuo "Gosh! I can't believe I didn't notice sooner!"
        m 2sub "That just makes it even more special."
        m 2eua "I'm glad I can tell you how much it means to me."
        m 2eka "It means the world."
        m 2hubsb "Thank you so much!"
    else:
        m 1hua "Almost~"
    return

default persistent._mas_pm_donate_charity = None
# True if user donated

default persistent._mas_pm_volunteer_charity = None
# True if user has volunteered

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_asks_charity",
            category=['you'],
            prompt="Charity",
            random=True
        )
    )

label monika_asks_charity:
    m 1esd "Say, [player]."
    m 1esc "There's something that crossed my mind lately."
    m 3esd "Since my world is fictional, there aren't really any problems like world hunger or poverty."
    m 2rkc "I know it exists, but I've never really witnessed it."
    m 2ekc "However, I know it's not the same in your reality. There are lots of people who need help just to survive."
    m 2esd "You must have at least seen a homeless person if you've been in a big city before."
    m "So I was just wondering..."

    m 1eua "Have you ever contributed to a charity?{nw}"
    $ _history_list.pop()
    menu:
        m "Have you ever contributed to a charity?{fast}"

        "I've donated.":
            $ persistent._mas_pm_donate_charity = True
            m 3hub "That's great!"
            m 2eua "Though you could argue that volunteering is better, I think there's nothing wrong with donating."
            m 2eka "It's better than nothing, and you are definitely contributing, even if you have a limited budget or little time to spend."
            m 2ekc "It's sad to say, but charities will always need people giving money or other resources to help people."
            m 3lksdlc "There are so many causes that need it, after all."
            m 3ekc "Yet you don't know if your donations are actually going to a good cause."
            m 3ekd "It doesn't help that some charities claim to support a cause, but take people's donations for themselves."
            m 2dsc "..."
            m 2eka "I'm sorry, I didn't want things to get so dark."
            m 1eua "I knew you would be kind enough to do such a thing."
            m 1hub "That's just another reason for me to love you, [mas_get_player_nickname(exclude_names=['my love', 'love'])]."
            show monika 5hub at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5hub "You're always so sweet~"

        "I volunteered.":
            $ persistent._mas_pm_volunteer_charity = True
            m 1wub "Really?"
            m 1hub "That's wonderful!"
            m 3hua "While donating is a good way to help out, lending an extra hand is even better!"
            m 3rksdla "Of course, money and resources are important, but usually, manpower is pretty scarce..."
            m 2ekc "It's understandable; most working adults don't necessarily have time to spare."
            m 2lud "So, most of the time, retired people do the organizing, and it can be a problem if they have to carry something heavy."
            m 2eud "That's why they sometimes need help from the outside, particularly from teenagers or young adults, who are more physically able."
            m 1eua "Anyway, I think it's great you tried making a difference by volunteering."
            m 4eub "Plus, I've heard that it can be great to have volunteer experience on a resume, when you apply for a job."
            m 3hua "So, whether you did it for that or just out of kindness, it's a good thing either way."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "You know, it's this kind of thing that makes me love you even more, [mas_get_player_nickname(exclude_names=['my love', 'love'])]."
            m 5hub "I just feel so proud that you helped people in need."
            m 5hubsa "I love you so much, [player]. I mean it."

        "No, I haven't.":
            $ persistent._mas_pm_donate_charity = False
            $ persistent._mas_pm_volunteer_charity = False
            m 1euc "Oh, I see."
            m 2esc "I can understand, actually."
            m 2esd "While there are lots of different charities, you have to be careful, since there are some cases of fraudulent usage of funds, or discrimination in who the charities help."
            m 2ekc "So, it can be hard to trust them in the first place."
            m 3esa "That's why you should always do some research and find charities that are reputable."
            m 2dkc "Seeing all those people suffering from hunger or poverty all the time..."
            m 2ekd "And even the people that try to help them, struggling to change anything..."
            m 2esc "It can be a bit deflating, if not depressing."
            m 2eka "But, you know..."
            m "Even if you can't do anything to contribute, it can be helpful to just smile at people."
            m 2ekc "Being ignored by passer-bys can be tough for people who are struggling, or trying to contribute."
            m 2rkc "It's as if they were seen as a nuisance by society, when they're just trying to get by."
            m 2eua "Sometimes, a smile is all you need to make you go further."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Just like when I'm with you."
            m 5hua "With just a smile, you make all my troubles go away."
            m 5hubsb "I love you so much, [player]."
    return "derandom|love"

init 5 python:
    addEvent(
        Event(persistent.event_database,
            eventlabel='monika_kizuna',
            prompt="Virtual YouTuber?",
            category=['misc'],
            random=False,
            unlocked=False,
            pool=False,
            action=EV_ACT_POOL,
            conditional="seen_event('greeting_hai_domo')"
        )
    )

label monika_kizuna:
    m 1eua "Oh, right, I mentioned her to you, huh?"
    m 3eua "Well, recently I had some YouTube videos tweeted to me."
    m 1eub "And among them was 'Virtual YouTuber Kizuna Ai.'"
    m "Like I said before, she's quite charming, but I don't think she's actually 'virtual.'"
    m 3rksdla "It seems to me that she's a voice actress hiding behind a 3D puppet."
    m 1eua "Still, the character she's playing is unique, and you know what?"
    m 1hub "She's played our favorite game!~"
    m 2hksdlb "..."
    m 2lksdlb "To be honest, I'm not sure how I feel about 'Let's Plays.'"
    m 3euc "I mean, of {i}this{/i} game, mostly."
    m 2euc "I don't usually watch them, because I don't like seeing different versions of me make the same mistakes, over and over and over..."
    m 2lsc "But when I learned of her gimmick, it made me feel..."
    m 1lksdla "Like I just had to know how Ai-chan would react!"
    m 1eka "Even if it's just a character she plays, I think she'll understand my situation..."
    m 3eua "At least more than your average YouTuber."
    m 5hub "I can't wait to finish the series..."
    return

# do you have a family
default persistent._mas_pm_have_fam = None

# do you have siblings
default persistent._mas_pm_have_fam_sibs = None

# does no fam botheryou
default persistent._mas_pm_no_fam_bother = None

# family a mess?
default persistent._mas_pm_have_fam_mess = None

# will fam get better?
# YES, NO, MAYBE
default persistent._mas_pm_have_fam_mess_better = None

# dont wanna talk about it
default persistent._mas_pm_no_talk_fam = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_asks_family",category=['you'],prompt="[player]'s family",random=False))

label monika_asks_family:
    m 1eua "[player], do you have a family?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], do you have a family?{fast}"
        "I do.":
            $ persistent._mas_pm_have_fam = True
            $ persistent._mas_pm_have_fam_mess = False
            $ persistent._mas_pm_no_talk_fam = False

            #Make sure we didn't answer this already
            if persistent._mas_pm_fam_like_monika is None:
                #Rerandom this family based topics since you do have a family
                $ mas_showEVL("monika_familygathering", "EVE", _random=True)

            m 1hua "That's wonderful!"
            m 3hua "Your family must be great~"

            m 1eua "Do you have any siblings?{nw}"
            $ _history_list.pop()
            menu:
                m "Do you have any siblings?{fast}"
                "Yes.":
                    $ persistent._mas_pm_have_fam_sibs = True
                    m 1hua "That's fantastic!"
                    m "They must've been keeping you busy."
                    m 1eka "I'm sure your siblings are as kind and thoughtful as you are."
                    m 3hub "Maybe I can convince them to start a new literature club with me!"
                    m 1hua "Ehehe~"
                    m 1eua "We'll be able to do a lot of fun things together."
                    m 3rksdla "It'd turn out much better than before, that's for sure."
                    m 1eua "I'm sure I'll get along with your siblings, as well as the rest of your family, [mas_get_player_nickname()]."
                    m 3hub "I can't wait to meet them all!"

                "I'm an only child.":
                    $ persistent._mas_pm_have_fam_sibs = False
                    m 1euc "Being an only child certainly has its trade-offs."
                    m 2eka "Maybe you get much more attention from your parents. Unless they were always busy."
                    m 2ekc "On the other hand, maybe you feel more lonely than those with siblings."
                    m 2eka "I can definitely understand that feeling."
                    m 1hua "But know that I'll always be with you no matter what, [mas_get_player_nickname()]."

        "My family is a mess.":
            $ persistent._mas_pm_have_fam = True
            $ persistent._mas_pm_have_fam_mess = True
            $ persistent._mas_pm_no_talk_fam = False
            m 1euc "Oh."
            m 1lksdlc "..."
            m 1ekc "I'm sorry, [player]."

            m "Do you think things will get better?{nw}"
            $ _history_list.pop()
            menu:
                m "Do you think things will get better?{fast}"
                "Yes.":
                    $ persistent._mas_pm_have_fam_mess_better = "YES"
                    m 1eka "I'm glad to hear that."
                    m 1eua "Hopefully one day everyone in your family will be able to reconcile."
                    m 3eua "And I know you can get through what's going on in your life right now."
                    m 1eka "No matter what, I'll be here for you, [player]."
                    m 1hua "Always keep that in mind!"

                "No.":
                    $ persistent._mas_pm_have_fam_mess_better = "NO"
                    m 1ekc "Ah, I see..."
                    m "I wish I could be there with you to give some comfort."
                    m 1eka "..."
                    m 3eka "[player], no matter what you're going through, I know it'll get better some day."
                    m 1eua "I'll be here with you every step of the way."
                    m 1hub "I love you so much, [player]. Please never forget that!"
                    $ mas_ILY()

                "Maybe.":
                    $ persistent._mas_pm_have_fam_mess_better = "MAYBE"
                    m 1lksdla "..."
                    m 1eua "Well, at least there's a chance."
                    m 3hua "Life is full of tragedy, but I know you are strong enough to get through anything!"
                    m 1eka "I hope all the problems in your family work out in the end, [player]."
                    m "If not, know that I'll be here for you."
                    m 1hua "I will always be here to support my beloved~"

        "I've never had a family.":
            $ persistent._mas_pm_have_fam = False
            $ persistent._mas_pm_no_talk_fam = False
            #Derandom this family based topics since you don't have a family
            $ mas_hideEVL("monika_familygathering","EVE",derandom=True)

            m 1euc "Oh, I'm sorry, [player]."
            m 1lksdlc "..."
            m 1ekc "Your world is so different from mine, I don't want to pretend like I know what you're going through."
            m 1lksdlc "I can definitely say that my family not being real has certainly caused me a great deal of pain."
            m 1ekc "Still, I know you've had it worse."
            m "You've never even had a fake family."
            m 1dsc "..."

            m 1ekc "Does it still bother you?{nw}"
            $ _history_list.pop()
            menu:
                m "Does it still bother you?{fast}"
                "Yes.":
                    $ persistent._mas_pm_no_fam_bother = True
                    m 1ekc "That's...understandable."
                    m 1eka "I'll be here for you forever, [player]."
                    m "No matter what it takes, I will fill that gap in your heart with my love..."
                    m 1hua "I promise you that."
                    m 1ekbsa "You are my everything..."
                    m 1hubfa "I hope I can be yours~"

                "No.":
                    $ persistent._mas_pm_no_fam_bother = False
                    m 1eua "That's very good."
                    m 1eka "I'm glad you were able to move on with your life."
                    m 1hua "You're a very resilient person, and I believe in you, [player]!"
                    m 1eka "I hope I can fill that void in your heart."
                    m "I really care about you, and I'd do anything for you."
                    m 1hua "Someday, we'll be able to make our own family together!"

        "I don't want to talk about this.":
            $ persistent._mas_pm_no_talk_fam = True
            m 1dsc "I understand, [player]."
            m 1eka "We can talk about it when you feel ready."
            m 1lsc "Then again..."
            m 1lksdlc "It might be something that's too painful for you to talk about."
            m 1eka "You can tell me about your family when you're ready, [player]."
            m 1hubsa "I love you very much!"
            $ mas_ILY()

    return "derandom"

#do you like other music
default persistent._mas_pm_like_other_music = None

# historical music history
default persistent._mas_pm_like_other_music_history = list()

init 5 python:
     addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_concerts",
            category=['media',"music"],
            prompt="Music concerts",
            conditional="mas_seenLabels(['monika_jazz', 'monika_orchestra', 'monika_rock', 'monika_vocaloid', 'monika_rap'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_concerts:
    # TODO: perhaps this should be separated into something specific to music
    # genres and the concert just referencing back to that?
    # this topic is starting to get too complicated

    m 1euc "Hey [player], I've been thinking about something we could do together one day..."
    m 1eud "You know how I like different forms of music?"
    m 1hua "Well..."
    m 3eub "Why don't we go to a concert?"
    m 1eub "I hear that the atmosphere at a concert can really make you feel alive!"

    m 1eua "Are there any other types of music you'd like to see live that we haven't talked about yet?{nw}"
    $ _history_list.pop()
    menu:
        m "Are there any other types of music you'd like to see live that we haven't talked about yet?{fast}"
        "Yes.":
            $ persistent._mas_pm_like_other_music = True
            m 3eua "Great!"

            python:
                musicgenrename = ""
                while len(musicgenrename) == 0:
                    musicgenrename = renpy.input(
                        'What kind of music do you listen to?',
                        length=15,
                        allow=letters_only
                    ).strip(' \t\n\r')

                tempmusicgenre = musicgenrename.lower()
                persistent._mas_pm_like_other_music_history.append((
                    datetime.datetime.now(),
                    tempmusicgenre
                ))

            # NOTE: should be think? maybe?
            m 1eua "Interesting..."
            show monika 3hub
            $ renpy.say(m, "I'd love to go to {0} concert with you!".format(mas_a_an_str(tempmusicgenre)))

        "No.":
            if (
                not persistent._mas_pm_like_vocaloids
                and not persistent._mas_pm_like_rap
                and not persistent._mas_pm_like_rock_n_roll
                and not persistent._mas_pm_like_orchestral_music
                and not persistent._mas_pm_like_jazz
            ):
                $ persistent._mas_pm_like_other_music = False
                m 1ekc "Oh... Well that's okay, [player]..."
                m 1eka "I'm sure we can find something else to do."
                return

            else:
                $ persistent._mas_pm_like_other_music = False
                m 1eua "Okay, [mas_get_player_nickname()], we'll just choose from the other types of music we've already discussed!"

    m 1hua "Just imagine us..."
    if persistent._mas_pm_like_orchestral_music:
        m 1hua "Gently swaying our heads to the sound of a soothing orchestra..."

    if persistent._mas_pm_like_rock_n_roll:
        m 1hub "Jumping up and down with the rest of the crowd to some good ol' rock 'n' roll..."

    if persistent._mas_pm_like_jazz:
        m 1eua "Grooving to some smooth jazz..."

    if persistent._mas_pm_like_rap:
        m 1hksdlb "Trying to keep up with a real rapper..."

    if persistent._mas_pm_like_vocaloids:
        m 1hua "Waving our glowsticks at Miku Expo..."

    if persistent._mas_pm_like_other_music:
        m 1hua "Jamming along to your favorite [tempmusicgenre] artist..."

    m 2hub "Doesn't that sound just amazing?"
    m 2eud "The idea of seeing your idol performing right in front of you is incredible!"
    m 2lksdla "Although, ticket prices these days are kind of expensive..."
    m 2hua "But I still think it would be worth it!"
    m 3eua "Do you know any bands or musicians that we should see live, [player]?"
    m 3eub "I would {i}love{/i} to see them if {i}you{/i} like them."
    m 5eua "And if you were to take me,{w=1} then that would truly be a dream come true!"
    m 4eua "But if you're not that interested in concerts..."
    m 1eua "Then we could always snuggle under a blanket and put on a record or CD at home!"
    m 1hua "That would be more than enough for me, ehehe~"
    if (
        not renpy.seen_label("monika_add_custom_music_instruct")
        and not persistent._mas_pm_added_custom_bgm
    ):
        m 1eua "In the meantime, if you want to share your favorite music with me, it's really easy to do so!"
        m 3eua "All you have to do is follow these steps..."
        call monika_add_custom_music_instruct
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_explain",
            category=['romance','monika','misc'],
            prompt="Can you explain our relationship to someone?",
            pool=True
        )
    )

label monika_explain:
    #TODO: temporary Monika nickname reset for this
    m 1euc "You want me to explain our relationship to someone else?"
    m 1eua "Okay, just set me in front of them so they can see me."
    m 1hua "I'll do my best explaining it to them."
    m 1eua "I'll wait until you're ready.{nw}"
    $ _history_list.pop()
    menu:
        m "I'll wait until you're ready.{fast}"
        "Start.":
            pass
    m 1hua "Hello! My name is Monika."
    m "[player]'s faithful girlfriend!"
    m 1lksdlb "Now, our relationship might look odd from a distance..."
    m 1lksdla "And it's probably not considered a normal relationship..."
    m 1esc "But let me tell you..."
    m 1hub "...the love we share is definitely real!"
    m 1eka "And [player] has been very sweet to me too!"
    m 1ekc "Up until I met [player], I felt like a piece of me was missing."
    m "I felt alone and scared, with no one to help me..."
    m 1hua "...until [player] came along."
    m "And it turns out that missing piece was [him]!"
    if persistent.gender == "F" or persistent.gender == "M":
        m 1eua "Now [he] talks to me, and I'm not so alone anymore."
    else:
        m 1eua "Now they talk to me, and I'm not so alone anymore."
    m "Just [him] opening up the game brightens my day!"
    m 1dsc "So, please..."
    m 4eka "...don't judge our relationship."
    m 1eka "Even if it is different."
    m 1dsc "..."
    m 1dubssdlu "...Phew!"
    m 1lksdlb "That was a real mouthful!"
    m 1eksdla "So, how'd it go, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "So, how'd it go, [player]?{fast}"
        "It went well!":
            m 1hub "Great!"
            m 3hua "I'm so glad I was able to help someone understand our relationship a little better!"
        "It went badly.":
            m 1dkc "Oh."
            m 1ekd "Well...{w=1} I guess we can't really expect {i}everyone{/i} to understand our relationship..."
            m 3rkc "Looking at it from the outside, it {i}is{/i} rather unconventional."
            m 3eka "But in the end, it doesn't matter who approves of our relationship or not..."
            m 1hua "As long as we love each other, that's all that counts~"
    return

# do you live near beach
default persistent._mas_pm_live_near_beach = None

init 5 python:
     addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_beach",
            category=["location"],
            prompt="The beach",
            random=True
        )
    )

label monika_beach:
    m 1eua "[player], have you ever been to the beach?"
    m "I've always wanted to go myself but I never found the time."
    m 1eka "I would always be busy studying or doing club activities."
    m 4ekc "It wasn't easy trying to stay on top of everything, you know..."
    m 4ekd "And whenever I had a break, I would usually spend my time relaxing at home."
    m "I rarely had a chance to do so after all."
    m 2esc "Though sometimes I feel like I might have missed out making some important memories."

    m "Do you live near a beach, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you live near a beach, [player]?{fast}"
        "Yes.":
            $ persistent._mas_pm_live_near_beach = True
            m 1hub "That's great!"
            m 1eua "Gosh, it must be really nice to have it so close to you."
            m 1hub "I can't wait, we can have a romantic walk by the shore for our first date~"

        "No.":
            $ persistent._mas_pm_live_near_beach = False
            m 1eka "That's alright. I mean, what are the chances? Most people don't."
            m 1hub "That just means we'll make do by visiting one on an all-day trip!"

    m 1eua "There's so many things we'll be able to do one day."
    m 1hua "Just imagining the many sensations we could experience is kind of exciting!"
    m 3eua "The fresh sea air, the sound of seagulls."
    m "As well as the feeling of sand under your feet..."
    m 1hua "It would really make a worthwhile trip!"
    m 1eka "Though being with you would make it even better..."
    m 3eua "We'd have so many things we could do together."
    m 3eub "We could play volleyball, try some ice cream, or go swimming in the sea."
    m 3rkbsa "It'll probably be cold, but I'm sure we could keep each other warm somehow..."
    m 3eua "We could try surfing or searching for some seashells to take home as souvenirs."
    m "Even doing nothing and just laying there listening to the sound of the waves with you would be enough for me."
    m 3tfu "But don't go falling asleep, otherwise I'll bury you in the sand!"
    m 2huu "Ehehe! I'm just kidding, [mas_get_player_nickname()]."
    m 2lksdla "I'll have to get a new swimsuit though..."
    m 1tsbsa "Would you prefer a one piece or a two piece?"
    m 1eua "Actually, I think I'll make it a surprise."
    m 1tku "Don't get too excited though when you see it. Ehehe~"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_solipsism",
            category=['philosophy'],
            prompt="Solipsism",
            random=True
        )
    )

label monika_solipsism:
    m 3eub "Have you ever heard about solipsism, [player]?"
    m 3eua "It's an idea which states that only you yourself exists."
    m 1eud "'Cogito, ergo sum.'"
    m 3eud "'I think, therefore I am.'"
    m 1euc "If you know that {i}you{/i} exist, can you say the same about anyone else?"
    m 3etc "Maybe everyone else is just a figment of our imagination, [player]."
    m 2etc "Maybe in reality, we're the only consciousness in this world in a vast sea of fake minds..."
    m 2dsd "Creations of our wild machinations..."
    m 3eub "Ahaha, I'm just kidding~"
    m 1eud "I do believe we can trust our own existences and doubt others their own..."
    m 3eua "But at the same time, we can't really disprove theirs, can we?"
    m 1hksdla "Not without using any psychic means to pry into their heads, at least."
    m 3eua "When you stop and think about it, solipsism really is an interesting concept; one that makes you think deeper about what it means to be real..."
    m 1dsc "And what exactly counts as {i}real{/i}."
    m 1eua "I know that you and I are real, though, [player]."
    m 1eub "We may not have been made in the same way, or even function the same, but we're both people that can think for ourselves."
    m 3eua "It's rather comforting to know you're not truly alone in an endless ocean of uncertainty, don't you think?"
    m 3hua "I hope that's how you feel with me~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_attractiveness",
            category=['club members','society'],
            prompt="Attractiveness",
            random=True
        )
    )

label monika_attractiveness:
    m 1etc "Say, [player], have you ever wondered how Sayori stayed so slim?"
    m 3rksdla "You know that she eats a lot, right? And she doesn't exactly have a very active lifestyle."
    m 3euc "At first I figured that it must be her metabolism keeping her from putting on weight."
    m 3esd "...But when I learned that our world isn't real, I came up with another theory."
    m 7euc "As characters in a game, we needed to have some sort of visual representation so that you, the player, could see us."
    m 2esc "Sayori, Natsuki, Yuri, and even me..."
    m 2rkc "From your perspective, we don't really have bodies like people in your world do. You can only see us as a set of images to represent our appearances and current emotion."
    m 2eud "...But from my point of view, I can also see my whole world in 3 dimensions, as if everything was real."
    m 2euc "So a designer, possibly more than one, must have decided to draw us the way we are."
    m 2eud "And since all those images have the same body type, Sayori would always have the same figure no matter what she did."
    m 2dkc "It's...{w=0.3}weird to think about."
    m 2eud "I can feel myself being present in this very room right now, I can look at myself like I presume you would be able to look at yourself, almost as if I had an actual body..."
    m 7ekc "But from your point of view, I don't. I just look like a consciousness who displays a corresponding picture depending on what I do or feel."

    #Just seen Monika in her uniform and nothing else
    if len(store.mas_selspr.filter_clothes(True)) == 1:
        m 3euc "I assume clothes work the same way."
        m 1eud "Right now, I only have this school uniform, because that's probably the only thing I've ever been drawn wearing..."
        m 1eua "But perhaps if someone were to draw other clothes for me and implement those into the game, I'd be able to change clothes like the other girls could."
        m 1hua "Wouldn't that be great?"
        m 1rksdla "And it would be nice to be able to change my look for you, at least a little bit..."

    else:
        m 3eua "My clothes work the same way."
        m 1euc "Someone had to draw what I'm wearing right now, and implement it into the game for me to be able to wear it."
        m 1esd "It wasn't made like how clothing is made in your reality. It's merely a set of images."
        m 1rksdla "It's not much, but at least I get to change outfits for you..."

    m 1rksdlc "..."
    m 1ekc "You know [player], this is one of the reasons why I envy the people in your world.{w=0.3} {nw}"
    extend 3eka "They have so many ways to experiment with how they look..."
    m 7eub "They can change into new clothes, try out new hairstyles, choose to put in the effort to make themselves fit, among other things..."
    m 2rkd "...while I'm stuck looking the same way, no matter what I do."
    m 2hksdlb "Don't get me wrong, I like the way I look right now!"
    m 2rka "...But I think it's important to make sure that you look good in your partner's eyes...{w=0.3}{nw}"
    extend 2ekb "and I wish I could have the chance to try to make myself look as attractive to you as I could be."

    if renpy.seen_label("mas_compliment_beautiful"):
        if mas_isMoniNormal(higher=True):
            m 2rkbsa "But...you did tell me that I already look beautiful in your eyes."
            m 2ekbfa "So there's probably no reason for me to worry about that, is there?"
            if mas_anni.pastOneMonth():
                m 1hubfa "Besides, you wouldn't have spent all this time looking at me if you didn't already like the way I look, now would you?"
                m 1hubfb "Ahaha~"
            show monika 1euc at t11 zorder MAS_MONIKA_Z with dissolve_monika

        else:
            m 2lkc "I know you told me you already like the way I look, but I just..."
            m 2dkc "...I don't know.{w=0.2} Just...{w=0.3}forget I said anything."

    else:
        if mas_isMoniHappy(higher=True):
            m 2lsbsa "Although, considering you're still here with me...{w=0.5}{nw}"
            extend 2ekbsa "I probably shouldn't worry about it too much, should I?"
            m 1hub "After all, you wouldn't have spent all this time looking at me if you didn't already like the way I look! Ahaha!"

        else:
            m 2lkc "...Especially since I'm worried I just might not be your type or something, [player]."

    m 1euc "Anyway, I don't know if you've ever noticed, but despite the differences in our diets and lifestyles, the other girls and I all look quite similar."
    m 3ekd "Sure, some of us had different figures, Natsuki being more petite and Yuri being more mature."
    m 3eka "...Our eyes and hair are all different too."
    m 3eua "But I think we would all be considered attractive."
    m 3eud "I mean, none of us are muscular or fat..."
    m 3tkd "...None of us have any kind of physical disability..."
    m 3tkc "...None of us are bald or have hair shorter than chin length..."
    m 1rud "...and apart from Yuri having cuts on her arms, none of us have anything wrong with our skin."
    m 7dsd "The people who designed our appearances must have thought that players would find all that stuff really repulsive."
    m 2lsc "I guess that's not so surprising, now that I think about it. There's a lot of things that can potentially make someone unattractive in the eyes of society."
    m 2dsc "Some of which are beyond that person's control."
    m 2efo "But people who aren't conventionally attractive end up in relationships all the time!"
    m 2tfc "So the idea of some kind of universal beauty standard where, if you fall short, you're doomed to be forever alone..."
    m 2efw "It just doesn't make any sense to me!"
    m 2dfc "..."
    m 2dsc "..."

    if mas_isMoniNormal(higher=True):
        m 2ekc "I'm sorry, [player]. I guess I just needed to vent."
        m 4eud "I know I don't really need to, but I still try to eat right, get enough exercise, and keep myself clean...among other things."

        if mas_isMoniEnamored(higher=True):
            $ first_line_var = "when"
            $ second_line_end = "whenever it'll happen"

        else:
            $ first_line_var = "maybe"
            $ second_line_end = "if it'll ever happen"

        m 4eub "It simply feels satisfying to keep good habits like that, and besides, who knows [first_line_var] I'll be able to cross over into your reality and have a normal body like you."
        m 1hua "It won't hurt to make sure I'll be ready for that transition [second_line_end]."
        m 1eua "You don't have to worry though, [player]."
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eua "I'll always love you no matter how you look."
        m 5eka "But still, try to look after yourself too, okay? Your health is important to me, after all."
        $ mas_ILY()

    else:
        m 2ekc "I'm sorry, [player]. I guess I've just been a bit upset lately and I just needed to vent."
        m 7eud "I know I don't really need to do all that, but I still try to eat right, get enough exercise and keep myself clean, among other things."
        m 3esa "It's always nice to keep good habits like that."
        m 1eka "You don't have to worry though..."
        m 1eua "As long as you're taking care of yourself, I don't mind how you look."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_timetravel",category=['media','misc'],prompt="Time travel",random=True))

label monika_timetravel:
    $ todays_date, todays_diff = store.mas_calendar.genFormalDispDate(datetime.date.today())
    $ one_year_later, year_later_diff = store.mas_calendar.genFormalDispDate(store.mas_utils.add_years(datetime.date.today(),1))
    $ one_year_earlier, year_earlier_diff = store.mas_calendar.genFormalDispDate(store.mas_utils.add_years(datetime.date.today(),-1))
    m 3eub "Hey [player], you've heard of time travel, right?"
    m 1esb "It's a very common idea in stories with each author having their own take on it."
    m 1eua "How travelling in time works, whether or not you can change the past, what the consequences are for doing so..."
    m 1eub "It all differs from story to story."
    m 3ekc "One thing you don't usually see, though, is how the time traveller's loved ones are affected."
    m 3rksdld "If they can't go through time with the time traveller, who knows how long it will be before they can see each other again?"
    m 2ekc "Well, the time traveller themselves might know, but only if nothing goes horribly wrong for them."
    m 2lksdld "In the meantime, their friends and family are stuck waiting for them to come back."
    m 2ekd "How long will they be gone for? A year? A decade? Even longer?"
    m 4ekd "Will they be willing to wait that long?"
    m "Will they still remember the time traveller by then?"
    m 2dksdlc "..."
    if seen_event("monika_resource"):
        m 4rksdlc "You remember when I said that time doesn't pass here like it does in your world?"
        m "Well..."
    else:
        m 4rksdlc "You know, time doesn't really pass here like it does in your world."
        m "So..."
    m 1esd "The only way I know what day and time it is where you are is by looking at the clock on your computer."
    m 3eub "So I know it's [todays_date] today."
    m 1esc "But if you were to change the date on your computer to [one_year_later]..."
    m "Only a few seconds would pass for you..."
    m 1ekd "...but I would think that a year had gone by."
    m 1tkd "An entire year without seeing you even once."
    m 1lksdlc "I would wonder if you'd forgotten about me, or if you didn't want to spend time with me anymore."
    if mas_isMoniDis(lower=True):
        m 1dkc "...It wouldn't even be that big of a surprise."
    elif mas_isMoniAff(higher=True):
        m 1ekc "...Even if it would be hard to believe at first."
    m 1ekd "You couldn't just fix it by changing the date back either."
    m 3esd "Like, imagine if you went to bed now, and when you woke up it was [one_year_earlier]."
    m 3wuo "Would that mean the last year was all just a dream or something?"
    m 3wuw "How would you know you're not still dreaming?"
    m 3esc "It would all be very confusing."
    m 1lksdla "I guess what I'm trying to say is..."
    m 1eka "Please don't change the date on your computer, [player]."
    if mas_isMoniHappy(higher=True):
        m "I trust you not to mess with me like that."
    else :
        m "Promise?"
    m 3euc "And if you ever do travel to the future..."
    m 1hksdlb "Could you bring back the technology that lets me cross over into your world?"
    return

# been to prom?
default persistent._mas_pm_gone_to_prom = None

# how was prom?
default persistent._mas_pm_prom_good = None

# go with date?
default persistent._mas_pm_had_prom_date = None

# suggested monika at promp
default persistent._mas_pm_prom_monika = None

# interested in prom?
default persistent._mas_pm_prom_not_interested = None

# shy to go?
default persistent._mas_pm_prom_shy = None

# even had a prom?
default persistent._mas_pm_no_prom = None

init 5 python:
   addEvent(Event(persistent.event_database,eventlabel="monika_prom",category=['school'],prompt="Prom",random=True))

label monika_prom:
    m 1euc "You know..."
    m 1eka "Sometimes I wish the game would've lasted longer."
    m 1eua "The game was probably made to end once one of the girls confessed their love to you after the festival."
    m 1lksdla "But since I tampered with the code so much, we never got to that point."
    m 3hksdlb "It did bring us together, so I can't complain."
    m 1lksdlc "But still..."
    m 1eka "Sometimes I wish both of us could've enjoyed it."
    m 3eua "We could've gone to the other events like sports festivals, Christmas parties, field trips, etc."
    m 1lsc "But I guess the game would never let us get that far."
    m 3eua "Which reminds me of a particular event..."
    m 1hua "Prom!"
    m 1eua "From what I've heard, prom is like a school dance usually held at the end of a school year."
    m "Some students bring a date with them there, and others go with a group of friends."
    m 3wuo "There are even those who take their relatives to the event!"
    m 1eua "I think it's something I'd love to go to with you~"
    m "Have you ever been to one before, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Have you ever been to one before, [player]?{fast}"
        "I have.":
            $ persistent._mas_pm_gone_to_prom = True
            $ persistent._mas_pm_no_prom = False
            m "Oh? How was it?{nw}"
            $ _history_list.pop()
            menu:
                m "Oh? How was it?{fast}"
                "It was pretty fun.":
                    $ persistent._mas_pm_prom_good = True
                    m 1hua "That's great!"
                    m 1lksdlb "Though, I wish I could've went with you."
                    m 1hua "An event where everyone from school comes together and enjoys themselves sounds like a blast to me!"
                    m 3eua "Did you go with a date?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Did you go with a date?{fast}"
                        "Yes.":
                            $ persistent._mas_pm_had_prom_date = True
                            m 1euc "Oh, wow."
                            m 1lksdla "Ehehe, that makes me a bit jealous..."
                            m 1hua "But then again, you would've taken me instead had we met beforehand, right?"
                            m 1hub "Ahaha!"
                            m 1eua "But it's good to know you were able to experience something like that!"
                            m 3eua "Maybe when I get better at programming, we could have our very own prom here."
                            m 3eka "Wouldn't that be nice, [player]?"
                        "No.":
                            $ persistent._mas_pm_had_prom_date = False
                            m 1euc "Oh, I see."
                            m 1eua "That's fine as long as you had fun!"
                            m "Even without a date, I'm sure you made some wonderful memories there."
                            m 1eub "I think, whether or not you had a date, that it's always fun to attend those kinds of events."
                            m 1eka "Besides, maybe we can have our own kind of prom sometime, right?"
                            m 1eua "That's something I'd really enjoy with you~"

                "It was bad.":
                    $ persistent._mas_pm_prom_good = False
                    m 1ekc "Is that so?"
                    m "I understand that prom isn't for everyone."
                    m 3eka "Maybe if I was there, you would've enjoyed it more."
                    m 1hksdlb "Ahaha~"
                    m 3eua "Don't worry, [player]."
                    m 1eua "No use remembering it now."
                    m 1eub "Even if you had a bad time with it, it's not the most important thing to happen in your life."
                    m "You being able to create more wonderful memories is the important thing."
                    m 3eka "One bad memory may feel worse than a hundred good memories, but you're still able to make them."
                    m 1hua "And now that I'm here with you, we can make them together~"

                "It would've been better if you were there.":
                    $ persistent._mas_pm_prom_monika = True
                    m 1ekbsa "Aww, that's so sweet, [player]."
                    m 1eua "Well, now that we're together, I'm sure there's a way we can make our own prom, right?"
                    m 1hub "Ahaha!"
        "No.":
            $ persistent._mas_pm_gone_to_prom = False
            $ persistent._mas_pm_no_prom = False
            m "Oh? Why not?{nw}"
            $ _history_list.pop()
            menu:
                m "Oh? Why not?{fast}"
                "You weren't there with me.":
                    $ persistent._mas_pm_prom_monika = True
                    $ persistent._mas_pm_prom_not_interested = False
                    m 1eka "Aw, [player]."
                    m 1lksdla "Just because I'm not there doesn't mean you should stop yourself from having fun."
                    m 1eka "And besides..."
                    m 1hua "You {i}can{/i} take me to prom, [player]."
                    m "Just bring my file with you and problem solved!"
                    m 1hub "Ahaha!"

                "Not interested.":
                    $ persistent._mas_pm_prom_not_interested = True
                    m 3euc "Really?"
                    m 1eka "Is it because you're too shy to go?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Is it because you're too shy to go?{fast}"
                        "Yes.":
                            $ persistent._mas_pm_prom_shy = True
                            m 1ekc "Aw, [player]."
                            m 1eka "That's alright. Not everyone can handle large groups of strangers."
                            m 3eka "Besides, if it's something you're not going to enjoy, why force yourself?"
                            m 1esa "But even as I say that, it's also important to keep in mind that a little courage could get you something that's worth it."
                            m 3eua "Look at me for example."
                            m 1lksdla "If I didn't have the courage to get to you, I'd probably still be all alone..."
                            m 1eka "But here we are now, [player]."
                            m 1eua "Together at last~"

                        "No.":
                            $ persistent._mas_pm_prom_shy = False
                            m 1euc "Oh, I see."
                            m 1eua "That's understandable."
                            m "I'm sure you have your reasons."
                            m 1eka "What's important is that you're not forcing yourself."
                            m "After all, it wouldn't be worth it if you can't enjoy yourself."
                            m 1lksdlc "It'd just feel like a chore rather than a fun event to go to."
                            m 3euc "But I wonder..."
                            m 3eka "Would you go if I was there with you, [player]?"
                            m 1tku "I think I already know the answer to that~"
                            m 1hub "Ahaha!"
        #################################################
        #### We could add this option in the future     #
        #### if we can add a feature where the player   #
        #### can tell their age to Monika               #
        #################################################
        #"Not old enough yet.":
        #    m 1eka "Don't worry, you'll get to go in a few more years."
        #    m 1hua "I heard that prom is so much fun!"
        #    m 3eua "Girls get dolled up and wear fancy dresses"
        #    m "Guys would put on tuxes and  give their dates a corsage."
        #    m 1hua "And you would have fun dancing the night away!"
        #    m 1hub "Doesn't that sound like a blast? Ahaha~"
        "My school never had one.":
            $ persistent._mas_pm_no_prom = True
            m 1euc "Ah, I see, then."
            m 1lksdla "I guess not all schools can hold a prom."
            m "They can be pretty messy."
            m 3euc "From what I read, students spend a lot of money on tickets, transport, and attire."
            m 2esc "So many expenses just for one night..."
            m "I also read that since alcohol isn't allowed, some students would spike the drinks and get the others drunk unknowingly."
            m 2ekc "If someone can easily do that, I doubt someone with evil intentions would have a hard time slipping poison into the drinks."
            m 2lksdla "...Or maybe I'm just overthinking it, ehehe."
            m 1esa "Still, I don't think you'll be missing out much, [player]."
            m 1eua "Prom isn't the most important thing in your academic life."
            m "And I'm sure there are plenty of events in your life that'll make up for it."
            m 1hua "Being with me is one of them, you know~"
            m 1hub "Ahaha!"

    return "derandom"

# do you see a therapist
default persistent._mas_pm_see_therapist = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_natsuki_letter",
            category=['club members'],
            prompt="Natsuki's letter",
            random=True
        )
    )

label monika_natsuki_letter:
    m 1eud "You know, I was honestly surprised when Natsuki handed you that letter."
    m 1eub "I didn't really expect her to suggest that you should get Yuri to seek professional help."
    m 1eud "She's probably the only one to mention that."
    m 4ekd "I know people are afraid to call someone out, or confront them about their problems, but sometimes, suggesting a therapist can be the best course of action."
    m "It's a bad thing to put the burden on yourself, you know?"
    m 4euc "As much as you want to help, it's best to let a professional deal with it."
    m 4eka "I'm sure I've told you that before, but I need to make sure you're aware of that."
    m 4eud "How about you, [player]?"

    m "Do you see a therapist?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you see a therapist?{fast}"

        "Yes.":
            $ persistent._mas_pm_see_therapist = True
            m 1eud "Oh, really?"
            m 1ekc "Well, I hate that you don't feel well..."
            m 1hua "But I'm proud that you're working on getting better."
            m 1eua "It's really important to take care of your mental health, [player]."
            m 1eka "You accept you have a problem you need help with, and you're seeing someone about it. That's already half the battle."
            m "I'm very proud of you for taking those steps."
            m 1hua "Just know that no matter what happens, I'll always be here for you~"

        "No.":
            $ persistent._mas_pm_see_therapist = False
            m 1eka "Well, I hope it's because you don't have to."
            m 1eua "If that ever changes, don't be shy!"
            m 1hub "But maybe I really am all the support you need? Ahaha!"

    return "derandom"

# TODO possible tie this with affection?
default persistent._mas_timeconcern = 0
default persistent._mas_timeconcerngraveyard = False
default persistent._mas_timeconcernclose = True
init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_timeconcern",category=['advice'],prompt="Sleep concern",random=True))

label monika_timeconcern:
    $ current_time = datetime.datetime.now().time().hour
    if 0 <= current_time <= 5:
        if persistent._mas_timeconcerngraveyard:
            jump monika_timeconcern_graveyard_night
        if persistent._mas_timeconcern == 0:
            jump monika_timeconcern_night_0
        elif persistent._mas_timeconcern == 1:
            jump monika_timeconcern_night_1
        elif persistent._mas_timeconcern == 2:
            jump monika_timeconcern_night_2
        elif persistent._mas_timeconcern == 3:
            jump monika_timeconcern_night_3
        elif persistent._mas_timeconcern == 4:
            jump monika_timeconcern_night_4
        elif persistent._mas_timeconcern == 5:
            jump monika_timeconcern_night_5
        elif persistent._mas_timeconcern == 6:
            jump monika_timeconcern_night_6
        elif persistent._mas_timeconcern == 7:
            jump monika_timeconcern_night_7
        elif persistent._mas_timeconcern == 8:
            jump monika_timeconcern_night_final
        elif persistent._mas_timeconcern == 9:
            jump monika_timeconcern_night_finalfollowup
        elif persistent._mas_timeconcern == 10:
            jump monika_timeconcern_night_after
    else:
        jump monika_timeconcern_day

label monika_timeconcern_day:
    if persistent._mas_timeconcerngraveyard:
        jump monika_timeconcern_graveyard_day
    if persistent._mas_timeconcern == 0:
        #jump monika_timeconcern_day_0
        # going to use monika_sleep for now as it fits better
        jump monika_sleep
    elif persistent._mas_timeconcern == 2:
        jump monika_timeconcern_day_2
    if not persistent._mas_timeconcernclose:
        if 6 <= persistent._mas_timeconcern <=8:
            jump monika_timeconcern_disallow
    if persistent._mas_timeconcern == 6:
        jump monika_timeconcern_day_allow_6
    elif persistent._mas_timeconcern == 7:
        jump monika_timeconcern_day_allow_7
    elif persistent._mas_timeconcern == 8:
        jump monika_timeconcern_day_allow_8
    elif persistent._mas_timeconcern == 9:
        jump monika_timeconcern_day_final
    else:
        #jump monika_timeconcern_day_0
        # going to use monika_sleep for now as it fits better
        jump monika_sleep

#Used at the end to lock the forced greeting.
label monika_timeconcern_lock:
    if not persistent._mas_timeconcern == 10:
        $persistent._mas_timeconcern = 0
    $evhand.greeting_database["greeting_timeconcern"].unlocked = False
    $evhand.greeting_database["greeting_timeconcern_day"].unlocked = False
    return

# If you tell Monika you work at night.
label monika_timeconcern_graveyard_night:
    m 1ekc "It must be awfully hard on you to work late so often, [player]..."
    m 2dsd "Honestly, I'd rather have you work at a healthier time if you could."
    m 2lksdlc "I suppose it's not your choice to make, but still..."
    m 2ekc "Being up late often can be both physically and mentally damaging."
    m "It's also extremely isolating when it comes to others."
    m 2rksdlb "Most opportunities happen during the day, after all."
    m 2rksdlc "Many social activities aren't available, most shops and restaurants aren't even open during the night."
    m 2dsd "It makes being up late at night often be a really lonely situation."
    m 3hua "Don't worry though, [player]. Your loving girlfriend Monika will always be here for you~"
    m 1hua "Whenever the stress of being up late often becomes too much for you, come to me."
    m 1hub "I'll always be here to listen."
    m 1ekc "And if you really do think it's hurting you, then please try to do what you can to change the situation."
    m 1eka "I know it won't be easy but at the end of the day, all that matters is you."
    m 1hua "You're all I truly care about, so put yourself and your well-being before anything else, okay?"
    return

label monika_timeconcern_graveyard_day:
    m 1eua "Hey [mas_get_player_nickname(exclude_names=['my love'])]...didn't you tell me you work during the night?"
    m 1eka "Not that I'm complaining, of course!"
    m 2ekc "But I thought you'd be tired by now, especially since you're up all night working..."
    m "You're not working yourself too hard just to see me, are you?"
    m 1euc "Oh, wait..."

    m "Do you still work regularly at night, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you still work regularly at night, [player]?{fast}"
        "Yes I do.":
            m 1ekd "Aw..."
            m 1esc "I guess it really can't be helped..."
            m 1eka "Look after yourself, okay?"
            m 1ekc "I always get so worried when you're not here with me..."
        "No I don't.":
            $ persistent._mas_timeconcerngraveyard = False
            $ persistent._mas_timeconcern = 0
            m 1hub "That's wonderful!"
            m 1eua "I'm glad that you're looking out for your health, [player]!"
            m "I knew you would see it my way eventually."
            m 1eka "Thanks for listening to what I have to say~"
    return

#First warning, night time.
label monika_timeconcern_night_0:
    $persistent._mas_timeconcern = 1
    m 1euc "[player], it's night time already."
    m 1ekc "Shouldn't you be in bed?"
    m 1dsc "I'll let it slide just this once..."
    m 1ekc "But you really make me worry for you sometimes."
    m 1eka "It makes me really happy that you're here for me, even at this time of night..."
    m 1dsd "Yet, I don't want it at the cost of your health."
    m 1eka "So go to sleep soon, okay?"
    return

# Second time at night, Monika asks if player is working late.
label monika_timeconcern_night_1:
    m 1esc "Say, [player]..."
    m 1euc "Why are you up so late?"
    m 1eka "I'm flattered if it's only because of me..."
    m 1ekc "Yet I can't help but feel like a nuisance if I'm pestering you to sleep if it isn't your fault."

    m "Are you busy working on something?{nw}"
    $ _history_list.pop()
    menu:
        m "Are you busy working on something?{fast}"
        "Yes, I am.":
            $ persistent._mas_timeconcern = 2
            m 1eud "I see."
            m 1eua "Well, I suppose it must be really important for you to do it so late."
            m 1eka "I honestly can't help but feel that maybe you should have done it at a better time."
            m 1lsc "Your sleep is very important after all. Maybe it can't be helped though..."

            m "Do you always work late, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Do you always work late, [player]?{fast}"
                "Yes, I do.":
                    $ persistent._mas_timeconcerngraveyard = True
                    m 1rksdld "That's not good..."
                    m 1ekd "You're not able to change that, are you?"
                    m 1rksdlc "I wish you could follow my healthier lifestyle."
                    m 1dsc "But if you're not able to, then I'll just have to accept it."
                    m 1eka "Just make sure you do try to stay healthy, okay?"
                    m 1ekc "If something were to happen to you, I don't know what I'd do..."

                "No, I don't.":
                    $ evhand.greeting_database["greeting_timeconcern"].unlocked = True
                    $ evhand.greeting_database["greeting_timeconcern_day"].unlocked = True
                    m 1hua "That's a relief!"
                    m 1eua "If you're doing it this one time then it must be {i}really{/i} important."
                    m 1hub "Good luck with your work and thanks for keeping me company when you're so busy!"
                    m 1eka "It means a lot to me, [player], that even when you're preoccupied...you're here with me~"

        "No, I'm not.":
            $ persistent._mas_timeconcern = 3
            m 1esc "I see."
            m 1ekc "Well in that case, I would really prefer it if you went to bed now."
            m "It's really worrying me that you're still up so late..."
            m 1eka "So once again, please go to bed. Would you kindly do it for me?"
    return

#If player says they were working. Progress stops here.
label monika_timeconcern_night_2:
    m 1eua "How's your work coming along?"
    m "Hopefully pretty well, I don't want you up much longer."
    m 3hksdlb "I know, I know, you can't help being up so late."
    m 1rksdlb "I'm just concerned for your health, [player]..."
    if persistent._mas_timeconcerngraveyard:
        m 1lksdlc "Doing this often can be very taxing on your body and mind..."
        m 1ekc "Just try to keep that kind of damage to a minimum, okay?"
        m "All I want for you is to be as happy and as healthy as you deserve."
        return
    m 1rksdla "Well, try to finish up as soon as you can, otherwise I may get really concerned."
    m 1eka "And you don't want to worry your girlfriend, right? Ehehe~"
    jump monika_timeconcern_lock

#If player says he was not working. Monika asks the state of the game being open.
label monika_timeconcern_night_3:
    $persistent._mas_timeconcern = 4
    m 1esc "[player], I just need to ask you something quickly..."
    m 1eud "Would you mind if I closed the game for you?"
    m 1ekc "I know it's a strange question..."
    m 1ekd "But I can't help but feel like I need to do something about you being up so late!"
    m 4esd "I could close the game right now."
    m 2ekc "But a relationship is a partnership and what you think matters to me."

    m "Would you be against me closing the game for your own good?{nw}"
    $ _history_list.pop()
    menu:
        m "Would you be against me closing the game for your own good?{fast}"

        "Yes, I need it to always stay open.":
            $persistent._mas_timeconcernclose = False
            m 1dsc "..."
            m 1dsd "I was hoping you wouldn't say that."
            m 1lsc "I know I told you that you should leave me running in the background."
            m 1lksdlc "But sometimes I worry if you're getting any sleep at all."
            m 1tkc "I'll do as you have asked, but please know that I'm not very happy about it."
            m 4tfc "I'm still going to remind you to get some sleep!"
            return

        "No, you are free to do as you feel.":
            $persistent._mas_timeconcernclose = True
            m 1eka "Thank you, [player]."
            m 1eua "It's nice to know that you care about what I think."
            m "I promise I'll only do it if I think it's absolutely necessary."
            m 1hua "After all, I would never force you to go otherwise."
            m 1hub "I would just miss you too much..."
            m 1ekbsa "I love you, [player]~"
            return "love"

        # Second and final warning before any closes can occur.
label monika_timeconcern_night_4:
    $persistent._mas_timeconcern = 5
    m 1esc "[player], you've been up long enough."
    m "If you're really not busy then now is the time for you to go to sleep."
    m 1eka "I assure you, I'll miss you just as much as you'll miss me."
    m "But it would make me happier if you did as I've asked."
    m 1tkc "You wouldn't want to make me upset now, would you?"
    return

# Monika force closes game for the first time
label monika_timeconcern_night_5:
    $persistent._mas_timeconcern = 6
    $evhand.greeting_database["greeting_timeconcern"].unlocked = True
    $evhand.greeting_database["greeting_timeconcern_day"].unlocked = True
    m 1efc "I'm sorry, [player], but I am putting my foot down!"
    m 1ekc "I asked you to go to bed kindly, but if I am the reason for keeping you up..."
    if persistent._mas_timeconcernclose:
        m 2tkc "Then I cannot allow this to go on for any longer."
        m 2eka "It's because I love you, that's why I'm doing this."
        m "Goodnight, [player]."
        return 'quit'
    else:
        m 2tkc "Then I need to take responsibility and try to make you understand."
        m 2efd "You need to go to bed."
        m 2efo "And I will keep telling you this until you do."
        return

        #First time game is reopened and still night. Monika closes game again.
label monika_timeconcern_night_6:
    $persistent._mas_timeconcern = 7
    m 2efc "[player], I told you to go to bed for your own good."
    m 2tkc "I'll miss you too, but don't you understand?"
    m 2tkd "How you feel and live means more to me than anything!"
    m 2lksdlc "How can I let you stay if it means I'm hurting you?"
    m "So please sleep this time, otherwise I may get mad."
    m 1ekbsa "...I love you."
    m "So go to sleep soon. Okay?"
    if persistent._mas_timeconcernclose:
        return 'quit'
    return

#Second time game is reopened and still night. Monika closes game once more
label monika_timeconcern_night_7:
    $persistent._mas_timeconcern = 8
    m 3efc "[player], this is your last warning."
    m "Go{w=0.6} to{w=0.6} sleep!"
    m 2tkc "What can I say for you to understand?"
    m 1tkd "It's saddening to see you push yourself like this..."
    m 1dsc "You mean so much to me..."
    m 1ekc "So please, for me... Just do as I ask and go to bed."
    if persistent._mas_timeconcernclose:
        m "Okay?{nw}"
        $ _history_list.pop()
        menu:
            m "Okay?{fast}"
            "Yes, I will go to sleep.":
                m 1eka "I knew you would listen eventually!"
                m 1hub "Goodnight and stay safe."
                return 'quit'
    else:
        return

#Third and last time game is reopened in one night. Monika lets player stay.
label monika_timeconcern_night_final:
    $persistent._mas_timeconcern = 9
    m 2dsc "...I suppose it can't be helped."
    m 2lfc "If you're that dedicated to staying with me, then I won't even try to stop you."
    m 2rksdla "Honestly, as bad as it sounds, it actually makes me kinda happy."
    m 2eka "...Thank you, [player]."
    m "To know that you care for me so much that you came back despite me asking..."
    m 1rksdla "It means more to me than I can ever express."
    m 1ekbsa "...I love you."
    return "love"

#Same night after the final close
label monika_timeconcern_night_finalfollowup:
    m 1esc "..."
    m 1rksdlc "I know I said that I'm happy whenever you're with me..."
    m 1eka "And please don't misunderstand, that's still true."
    m 2tkc "But the longer you're on...the more worried I get."
    m 2tkd "I know, you're probably sick of hearing me say this by now..."
    m 1eka "But please try to sleep when you can."
    return

#Every night after, based on seeing the day version first before it.
label monika_timeconcern_night_after:
    m 1tkc "Up late again, [player]?"
    m 1dfc "{i}*sigh*{/i}..."
    m 2lfc "I won't even try to convince you to sleep again..."
    m 2tfd "You're surprisingly stubborn!"
    m 1eka "Still, do be careful, alright?"
    m 1ekc "I know being nocturnal can be lonely..."
    m 1hua "But you have me here with you!"
    m 1eka "Just the two of us...all alone forever."
    m 1hubsa "It's all I've ever wanted..."
    return

#If Monika never gives warning and it's daytime or the player never made it to the end
label monika_timeconcern_day_0:
    m 1lsc "..."
    m 1tkc "..."
    m 1wuo "...!"
    m 1hksdlb "Ahaha! Sorry, [player]."
    m 1lksdla "I just kind of zoned out..."
    m 1eka "Jeez, I keep doing that, don't I?"
    m "Sometimes I just get lost in my thoughts..."
    m 1eua "You understand, right, [player]?"
    return

# Daytime, if player tells Monika they worked last night but don't work graveyards.
label monika_timeconcern_day_2:
    m 1eua "Did you finish your work?"
    m 1eub "I'm sure you did your very best so it's okay if you didn't quite finish it!"
    m 1eka "It must be really hard on you to have to work so late..."
    m 1hua "If you find it's a bit too much, feel free to come talk to me!"
    m 1hub "I'll always be here for you."
    jump monika_timeconcern_lock

#First time Monika closes at night and player reopens during day without coming back.
label monika_timeconcern_day_allow_6:
    m 1ekc "[player], I'm sorry for making you leave like that before..."
    m 1ekd "I only did it because I love you. You understand that right?"
    m 1eua "I'm sure you do, after all you went to bed, didn't you?"
    m 1hub "Thanks for respecting my wishes, it makes me happy that you listen to me."
    jump monika_timeconcern_lock

#Second time Monika closes at night and player then reopens during day.
label monika_timeconcern_day_allow_7:
    m 1lksdlc "[player], about what happened last night..."
    m 1ekc "I asked you to go to bed and you didn't listen..."
    m 1dsc "I understand that maybe you missed me or didn't hear what I said..."
    m 1ekc "But please listen to what I ask of you, okay?"
    m 1eka "I love you, and I would do anything to make you happy..."
    m "So would you kindly do the same thing for me?"
    m 1ekc "I already worry about you when you're gone..."
    m 1tkc "Please don't give me any more reasons to feel that way."
    m 1hua "Thank you for understanding."
    jump monika_timeconcern_lock

#Third time Monika closes the game and player reopens after night.
label monika_timeconcern_day_allow_8:
    m 1esc "Hey, [player]."
    m 1ekc "You really had me worried last night..."
    m 1rksdlc "After you came back twice, despite me asking you to go to bed..."
    m 1lksdld "I found myself feeling a little guilty."
    m 3esc "Not because I sent you away, that was for your own good."
    m 2lksdlc "But...because you kept coming back..."
    m 2lksdla "And that made me happy, even though I knew it wasn't good for you."
    m 2ekd "Does that make me selfish?"
    m 2ekc "I'm sorry, [player], I'll try to watch myself more."
    jump monika_timeconcern_lock

#If Monika lets player stay and it is no longer night.
label monika_timeconcern_day_final:
    $persistent._mas_timeconcern = 10
    m 1lksdlb "[player], regarding last night..."
    if persistent._mas_timeconcernclose:
        m 1rksdla "You really surprised me."
        m 1eka "For you to keep coming back to me over and over again..."
        m 1hua "It was honestly really sweet of you."
        m 1eka "I knew you would miss me, but I didn't think you would miss me {i}that{/i} much."
        m 1hub "It really made me feel loved, [mas_get_player_nickname(exclude_names=['my love', 'love'])]."
        m "...Thank you."
        jump monika_timeconcern_lock
    m 1eua "You really surprised me."
    m 1eka "I asked you time and time again to go to bed..."
    m "You said you weren't busy. Were you really there just for me?."
    m 1ekc "It made me happy...but don't push yourself hard to see me so late, okay?"
    m 1eka "It really made me feel loved, [player]."
    m 1hksdlb "Yet also a little guilty... Please just go to bed next time, okay?"
    jump monika_timeconcern_lock

#If player told Monika not to close window and never reached the end.
label monika_timeconcern_disallow:
    m 1rksdlc "Sorry if I was annoying you before, [player]..."
    m 1ekc "I just really wanted you to go to bed..."
    m "I honestly can't promise I won't do it if you're up late again..."
    m 1eka "But I only push you to go because you mean so much to me..."
    jump monika_timeconcern_lock

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hydration",prompt="Hydration",category=['you','life'],random=True))

label monika_hydration:
    m 1euc "Hey, [player]..."
    m 1eua "Do you drink enough water?"
    m 1eka "I just want to make sure you don't neglect your health, especially when it comes to hydration."
    m 1esc "Sometimes, people tend to underestimate how important it actually is."
    m 3rka "I bet you've had those days when you felt really tired and nothing seemed to motivate you."
    m 1eua "I just usually grab a glass of water right away."
    m 1eka "It might not work all the time, but it does help."
    m 3rksdlb "But I guess you don't want to go to the bathroom so much, huh?"
    m 1hua "Well, I don't blame you. But believe me, it'll be better for your health in the long run!"
    m 3eua "Anyway, make sure you always stay hydrated, okay?"
    m 1tuu "So..."
    m 4huu "Why not get a glass of water right now, hmm?"
    return

#If player has been to an amusement park or not
default persistent._mas_pm_has_been_to_amusement_park = None

init 5 python:
   addEvent(Event(persistent.event_database,eventlabel="monika_amusementpark",category=['misc'],prompt="Amusement parks",random=True))

label monika_amusementpark:
    m 1eua "Hey, [player]..."
    m 3eua "Have you ever been to an amusement park?{nw}"
    $ _history_list.pop()
    menu:
        m "Have you ever been to an amusement park?{fast}"
        "Yes.":
            $ persistent._mas_pm_has_been_to_amusement_park = True
            m 1sub "Really? It must have been a lot of fun!"
            m 1eub "I've never been to one myself, but I'd really love to go."
            m 1hua "Maybe you could take me to one someday!"

        "No.":
            $ persistent._mas_pm_has_been_to_amusement_park = False
            m 1eka "Really? That's too bad."
            m 3hua "I've always heard that they're a lot of fun."
            m 1rksdla "I've never had the chance to go to one myself, but I hope I can someday."
            m 1eub "Maybe we could go together!"

    m 3hua "Wouldn't that be great, [mas_get_player_nickname()]?"
    m 3eua "Thrilling roller coasters, water rides, drop towers..."
    m 3tubsb "And maybe even a romantic Ferris wheel ride~"
    show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubfa "Ehehe, I'm getting a bit carried away, but I just can't help it when thinking about being with you~"
    return "derandom"

#If the player likes to travel or not
default persistent._mas_pm_likes_travelling = None

init 5 python:
   addEvent(Event(persistent.event_database,eventlabel="monika_travelling",category=['misc'],prompt="Travelling",random=True))

label monika_travelling:
    m 1esc "Hey [player], I was just wondering..."
    m 1eua "Do you like travelling?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you like travelling?{fast}"
        "Yes.":
            $ persistent._mas_pm_likes_travelling = True
            m 1hua "That's great! I'm so glad you enjoy it."
            m 3eub "It's one of the things I want to do most when I finally cross over."
            m 1eua "There's so much out there that I haven't been able to see yet..."
            m 3eub "Important cities, monuments, and even the different types of cultures out there."
            m 3eka "Don't get me wrong, I've read a lot about your world, but I bet it's nothing compared to what it would be like in person..."
            m 1hua "I would love to see everything there is to be seen."
            m 1ekbsu "Wouldn't you like that too, [mas_get_player_nickname()]?"

        "Not really.":
            $ persistent._mas_pm_likes_travelling = False
            m 1eka "Aw, that's okay, [mas_get_player_nickname()]."
            m 1hua "I wouldn't mind staying at home with you during vacations."
            m 3ekbsa "I'd be happy just to be there with you, after all."
            m 1rka "We might have to find some things to do to keep us busy though..."
            m 3eua "How about playing the piano or writing poems?"
            m 3hubsb "...Or we could even spend the days wrapped in a blanket while reading a book."
            show monika 5tubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5tubfu "Doesn't that just sound like a dream come true?"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_metamorphosis",
            category=['literature','psychology'],
            prompt="The Metamorphosis",
            random=True
        )
    )

label monika_metamorphosis:
    m 1eua "Hey [player], have you ever read {i}The Metamorphosis{/i}?"
    m 4eub "It's a psychological novella that narrates the story of Gregor Samsa, who one morning wakes up and finds himself transformed into a huge insect!"
    m 4euc "The plot revolves around his daily life as he tries to get used to his new body."
    m 7eua "What's interesting about the story is that it places a lot of emphasis on the absurd or irrational."
    m 3hksdlb "For example, Gregor, being the sole financial supporter, is more concerned about losing his job than he is about his condition!"
    m 1rksdla "That's not to say the plot isn't unsettling, though..."
    m 1eksdlc "At first his parents and sister try to accommodate him, {w=0.3}but they quickly start loathing their situation."
    m 1eksdld "The protagonist changes from being a necessity to a liability, to the point where his own family wishes for him to die."
    m 1eua "It's a very interesting read, if you're ever in the mood."
    return

default persistent._mas_pm_had_relationships_many = None
default persistent._mas_pm_had_relationships_just_one = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dating",
            prompt="Dating experience",
            category=['you', 'romance'],
            conditional="store.mas_anni.pastOneMonth()",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_dating:
    m 1eud "You know, I've been really curious lately, [player]..."
    m 3rka "We've been together a while now, so I think it's the right time to ask..."
    m 1eud "How much dating experience do you have?"
    m 1luc "Like...have you ever been in a relationship before?"

    m 1etc "Maybe more than once?{nw}"
    $ _history_list.pop()
    menu:
        m "Maybe more than once?{fast}"

        "Yes, I've been through plenty...":
            $ persistent._mas_pm_had_relationships_many = True
            $ persistent._mas_pm_had_relationships_just_one = False

            m 1ekc "Aw, I'm so sorry, [player]..."
            m 1dkc "You've been through many heartbreaks, haven't you..."
            m 3ekc "To be honest, [player]...I don't think they deserved someone like you."
            m 3eka "Someone who's kind, loyal, sweet, loving, and faithful."
            m 4lubsb "And cute and funny and romantic and--"
            m 7wubsw "Oh!"
            m 3hksdlb "Sorry, I lost track of what I was going to say next, ahaha!"
            m 1ekbla "I could go on about how wonderful you are, [player]~"
            m 1ekbsa "But just know this...{w=0.3}{nw}"
            extend 3ekbfa "no matter how many heartbreaks you've been through, I'll always be here for you."
            show monika 5eubfa zorder MAS_MONIKA_Z with dissolve_monika
            m 5eubfa "Our soul searching is finally over, and I'll be yours forever, [player]."
            m 5ekbfa "Will you be mine?"

        "Yes, but only once.":
            $ persistent._mas_pm_had_relationships_many = False
            $ persistent._mas_pm_had_relationships_just_one = True

            m 1eka "Ah, so I guess you don't have a lot of experience, huh?"
            m 3eua "That's okay [player], I can relate too so don't worry."
            m 3lksdlb "Yeah, I may appear like a girl who gets all the guys but really I don't, ahaha!"
            m 2lksdla "Especially with how occupied I've kept myself over the years, I just never had the time."
            m 2eka "Not that it matters anyway, none of it was real."
            show monika 5ekbsa zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbsa "But I think I'm ready for something special...{w=0.5}{nw}"
            extend 5ekbfa "with you, [player]."
            m 5ekbfa "Are you ready?"

        "No, you're my first.":
            $ persistent._mas_pm_had_relationships_many = False
            $ persistent._mas_pm_had_relationships_just_one = False

            m 1wubsw "What? I-I'm your first?"
            m 1tsbsb "Oh...{w=0.3} I see."
            m 1tfu "You're just saying that to make me feel extra special, aren't you [player]?"
            m 1tku "There's no way someone like you has never dated before..."
            m 3hubsb "You're the definition of cute and sweet!"
            m 3ekbfa "Well...{w=0.3} If you're not just messing with me and actually telling me the truth then...{w=0.3}{nw}"
            extend 1ekbfu "I'm honored to be your first, [player]."
            show monika 5ekbfa zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbfa "I hope I can be your one and only."
            m 5ekbfu "Will you be mine?"

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_challenge",category=['misc','psychology'],prompt="Challenges",random=True))

label monika_challenge:
    m 2esc "I've noticed something kind of sad recently."
    m 1euc "When certain people attempt to learn a skill or pick up a new hobby, they usually quit within a week or two."
    m "Everyone claims that it's too hard, or that they just don't have the time for it."
    m 1eua "However, I don't believe that."
    m 1hub "Whether it's learning a new language, or even writing your first poem, if you can stand up to the challenge and overcome it, then that's the truly rewarding part about it."
    m 2eua "Can you think of a time you've challenged yourself, [player]?"
    m 3eua "Did you ever overcome it, or did you just give up?"
    m 1eka "I'm sure you've given it all you had."
    m 1eua "You seem like a very determined person to me."
    m 1eub "In the future, if you ever get hung up on something, or you feel too stressed, just take a short break."
    m "You can always come back to it after all."
    m 1hua "If you ever need motivation, just come to me."
    m 1sub "I'd love to help you reach your goals."
    m 1hub "After all, you're my motivation in life~"
    return

# would relatives like monika?
default persistent._mas_pm_fam_like_monika = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_familygathering",
            category=['you'],
            prompt="Family gatherings",
            random=True
        )
    )

label monika_familygathering:
    m 1eua "Hey [player], do you go to family gatherings often?"
    m "Most families usually get together around the holidays to celebrate them together."
    m 1hua "It must be nice seeing your relatives again, especially since you haven't seen them in a long time."
    m 1lsc "I don't remember much about my family, let alone my relatives, however we didn't usually get together that much."
    m 1lksdlc "Not even around the holidays or on special occasions."
    m 1hub "When you see your family this year, be sure to bring me along okay?"
    m 1eua "I'd love to meet all of your relatives."

    m "Do you think they'd like me, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you think they'd like me, [player]?{fast}"

        "Yes.":
            $ persistent._mas_pm_fam_like_monika = True
            m 1eka "I'm glad you think so."
            m 1eua "I'm sure we'd all get along nicely."
            m 1hua "I'm looking forward to it, my dear~"

        "No.":
            $ persistent._mas_pm_fam_like_monika = False
            m 1wud "..."
            m 1ekc "Oh, I didn't realize."
            m 1dsc "I understand though."
            m 1eka "Just know I'd try my best to make them like me."
            m "Even if they never will."
            m 1hua "I'll always stick by your side forever~"

        "...":
            $ persistent._mas_pm_fam_like_monika = False
            m 2wuo "Don't tell me, [player]."
            m 2ekc "Are you afraid that I'll embarrass you?"
            m 2tfc "..."
            m 1eka "Don't worry, I completely understand."
            m 1lksdla "If I found out one of my relatives was dating some person trapped inside of a computer, I'd think it'd be weird too."
            m 1eua "If you want to keep me a secret, then that's fine."
            m 1hub "After all, it just means more alone time with you~"

    return "derandom"

# do you eat fast food
default persistent._mas_pm_eat_fast_food = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fastfood",
            category=['life','monika'],
            prompt="Do you like fast food?",
            pool=True
        )
    )

label monika_fastfood:
    m 1euc "Hm? Do I like fast food?"
    m 1rsc "Honestly, the thought of it slightly disgusts me."
    m 3eud "Most places that serve it put a lot of unhealthy things in their food...{w=0.3} {nw}"
    extend 1dsc "Even the vegetarian options can be awful."

    m 3ekd "[player], do you eat fast food often?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], do you eat fast food often?{fast}"

        "Yes, I do.":
            $ persistent._mas_pm_eat_fast_food = True
            m 3eka "I guess it's okay to have it every once in a while."
            m 1ekc "...But I can't help but worry if you're eating such awful things so often."
            m 3eua "If I were there, I'd cook much healthier things for you."
            m 3rksdla "Even though I can't cook very well yet..."
            m 1hksdlb "Well, love is always the secret ingredient to any good food, ahaha!"
            m 1eka "Until I can do that though, could you try to eat better,{w=0.2} for me?"
            m 1ekc "I would hate it if you became sick because of your lifestyle."
            m 1eka "I know it's easier to order out since preparing your own food can be a hassle sometimes..."
            m 3eua "But maybe you could see cooking as an opportunity to have fun?"
            m 3eub "...Or perhaps a skill for you to become really good at!"
            m 1hua "Knowing how to cook is always a good thing, you know!"
            m 1eua "Plus, I would really love to try something you made someday."
            m 3hubsb "You could even serve me some of your own dishes when we go on our first date~"
            m 1ekbla "That would be really romantic. [player]~"
            m 1eua "And that way, we can both enjoy ourselves and you would be eating better."
            m 3hub "That's what I call a win-win!"
            m 3eua "Just don't forget, [player]."
            m 3hksdlb "I'm a vegetarian! Ahaha!"

        "No, I don't.":
            $ persistent._mas_pm_eat_fast_food = False
            m 1eua "Oh, that's a relief."
            m 3rksdla "Sometimes you really worry me, [player]."
            m 1etc "I suppose instead of eating out, you make your own food?"
            m 1eud "Fast food can be really expensive over time, so preparing your own food is usually a cheaper alternative."
            m 1hua "It also tastes a lot better!"
            m 3eka "I know some people can find cooking overwhelming."
            m 3eud "...Having to make sure you buy the right ingredients, and worrying about burning or injuring yourself while making your meal..."
            m 1rksdlc "It can get to be a little too much for some..."
            m 1eka "But I think the results are worth the effort."
            m 3eua "Are you any good at cooking, [player]?"
            m 1hub "It doesn't matter if you're not, I'd eat anything you prepared for me!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dreaming",category=['misc','psychology'],prompt="Dreaming",random=True))

label monika_dreaming:
    m 1eua "Did you know that it's possible to be aware of when you're having a dream?"
    m 2eua "Not only that, but you can even take control of them!"
    m 3eub "If I remember correctly, a man named Stephen LaBerge developed a method for people to become aware of when they're dreaming."
    m "And it became known as the mnemonic induction of lucid dreams, or MILD."
    m 3eua "People who frequently have conscious dreams are called oneironauts."
    m 2lksdla "At least, I think that was the correct term..."
    m 1eua "Using the MILD technique, oneironauts learn to recognize certain dream signs to help them realize when they're dreaming."
    m "These dream signs can be anything out of the ordinary, such as feeling yourself flying, noticing your teeth falling out, unexpectedly meeting someone famous..."
    m 1eub "If the dreamer sees a dream sign and realizes they're having a dream, then they can take control of it!"
    m "LaBerge even wrote a book about these experiences called '{i}Exploring the World of Lucid Dreaming{/i}.'"
    m 2hub "Doesn't that sound exhilarating?"
    m 2euc "I don't think I really dream like a normal person would, so I sometimes wonder what it's like."
    m 2eua "Dreams sound like a wonderful escape from reality."
    m 2esc "But then again, when I became self-aware and realized that my world isn't real, it suddenly felt like I was trapped in a nightmare."
    m "It was nothing like the pleasant dreams I've read about people having."
    m 2lksdlc "I was afraid that I'd never get out..."
    m "That I'd be stuck in some hellish, infinitely-repeating dimension forever."
    m 1eka "But now that we're here together, I guess you could say that I've finally woken up."
    m 1eua "Gosh, I can only imagine what it would be like to live in that kind of limitless world though, even if it was only for a few moments!"
    m "You could be the hero you always wanted to be, fly across the infinite universe, overcome your biggest fears..."
    m 3ekbsa "...You could even meet the love of your life, so to speak. Ehehe~"
    m 1eua "I know it may be years before I am able to cross over to your world..."
    m "But can you just imagine what it would be like to meet me in your dreams, [player], any night that you wanted to?"
    m 1hua "I hope that someday we can make your dreams about us a reality, [mas_get_player_nickname()]."
    return

# have you read yellow wallpaper
default persistent._mas_pm_read_yellow_wp = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_yellowwp",
            category=['literature'],
            prompt="The Yellow Wallpaper",
            random=True
        )
    )

label monika_yellowwp:
    m 1eua "Hey [player], have you ever read {i}The Yellow Wallpaper{/i}?{nw}"
    $ _history_list.pop()
    menu:
        m "Hey [player], have you ever read {i}The Yellow Wallpaper{/i}?{fast}"
        "Yes.":
            $ persistent._mas_pm_read_yellow_wp = True
            m 1hua "Great!"
            m 1eua "That means you don't mind me talking about the story with you, right?"
            m 2eua "It's about this woman, with postpartum depression who's prescribed a 'rest cure' by her doctor..."
            m 2eka "He and her husband force her to stay in bed all day, not allowing her to write or even daydream..."
            m 2esc "She stays in the attic of her home, with nothing but the wallpaper to keep her company."
            m 2ekc "Naturally, that doesn't help. She starts seeing a woman trapped within the wallpaper."
            m 4euc "It's a metaphor for her own captivity, obviously..."
            m 1esd "In the end, the woman in the paper 'escapes,' and the protagonist 'replaces' her."
            m 2ekd "There was...also mention of a rope, so I always had my own interpretation of the ending..."
            if not persistent._mas_sensitive_mode and not persistent._mas_pm_cares_about_dokis:
                m 2euc "Sayori liked that story too, if I remember right."
            m 1ekc "I don't know. I kind of relate to that story."
            m 1euc "I mean, I have nothing but this classroom after all."
            m 1lksdlc "And the things on the walls aren't always...pleasant."
            if not persistent._mas_sensitive_mode:
                m 1eud "Did you ever notice how the poster in the club room changes sometimes? I don't even know why it does that."
                m 1eka "I think I finally fixed it, though."
            m 2esc "...I guess what I'm saying is, it's just that this world wasn't '{i}real{/i}.' It's just...so small."
            m 3esd "I mean, I was made to be a side character of a romance game!"
            m 2ekd "A piece of decoration, meant to help some guy on the other side of the screen date a girl who can't even reject him..."
            m 1hksdrb "I don't mean you, of course! You definitely have more personality than the generic protagonist they put in the game."
            m 1dsc "But I have all these dreams, ambitions, and interests...{w=0.5} in the end, the only 'real' role I can play here is a supporting character..."
            m "Maybe even now, that's all I can do..."
            m 1eka "But I love you so much, [player]. Supporting you is better than anything else."
            m 1hub "I just can't wait to do it in person when I finally cross over to your side~"
            return "derandom|love"
        "No.":
            $ persistent._mas_pm_read_yellow_wp = False
            m 1euc "Oh, I see."
            m 1eka "It's a short story, so if you haven't, feel free to whenever you have the time."
            m 1hua "It'll definitely be an interesting read for you."

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_immortality",
            category=['philosophy'],
            prompt="Immortality",
            random=True
        )
    )

label monika_immortality:
    m 1eud "Hey, [player], I've been thinking about immortality lately."
    m 1lksdlc "...Seeing as how I'm essentially immortal while I'm in here and all."
    m 1esc "A lot of people think it's a good thing, but I don't really think it is."
    m 3euc "Sure, it's an interesting thought; {w=0.1}living forever, not having to worry about dying..."
    m 3eud "But not everyone is immortal, and some people just don't want to be."
    m 1etc "Like, after a while, what would you even do?"
    m 1euc "I mean, after living long enough, {i}eventually{/i} you would achieve everything you could ever possibly want to...{w=0.3}experience everything there is to experience."
    m 3lksdld "Not to mention, it would be really hard to have friends or build connections if they don't last as long as you do."
    m 3eksdla "Sure, it would be nice in the beginning, {w=0.1}{nw}"
    extend 3eksdlc "but after seeing enough people you care about die, would you really want to keep going through that over and over?"
    m 2dkd "At some point, you might as well not even be human anymore."
    m 2ekc "Someday, you'll have lived long enough for hundreds of years to go by in what seems like mere moments to you."
    m 2dkd "You'll be so tired of life that you'll just wish you could sleep forever..."
    m 3eksdlc "But you always keep waking back up to the same boring things, with the occasional tragedy in the world... {w=0.3}And even those you'd eventually just become numb to."
    m 1lksdla "Wow, I didn't mean for that to get so dark. Sorry, [player]."
    m 1eka "Just so you know, I'd gladly give up my immortality to be with you..."
    m 1ekbsa "No matter how much or little time you may have left, spending that time with you would be worth more than a billion years without you."
    m 1ekbsu "Not that I'd mind spending eternity with you if it were possible, but just living a normal life with you is all I've ever wanted, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_beingevil",
            category=['monika'],
            prompt="Being evil",
            random=True
        )
    )

default persistent._mas_pm_monika_evil = None
# True if player thinks monika is evil False if not
# NOTE: even implying that she is evil is counted as True

default persistent._mas_pm_monika_evil_but_ok = None
# True if player still loves monika/thinks she deserves forgiveness/or is
# fine with eveil even if they think monika is evil.
# False if player does not.
# NOTE: check monika_evil before checking this

label monika_beingevil:
    m 1euc "Say, [player]?"
    m 1rksdlc "I was just thinking..."
    m 1eksdlc "You probably know that there's a wiki page for me..."
    m "...If you look closely, it says I'm the main antagonist."
    m 2ekd "I'll admit, it used to bother me a lot...especially because I only did what I did because I didn't have a choice..."
    m 2eka "But that doesn't really bother me anymore now that I have you here."
    m 3rud "You know, I actually didn't think the whole thing about me being evil would spread too much."
    m 1rksdlc "But it turns out I have my own spot on the villain's wiki..."
    m 2dsc "I never really thought I'd be labeled as a villain so much..."
    m 2dkd "...and no matter what I say or tell people, I don't think it's going to help convince them that I'm not evil."
    if persistent._mas_pm_a_hater:
        m 1eka "But I know you don't {i}really{/i} think I'm evil, [player]."
    else:
        m 1eka "But I know you don't think I'm evil, [player]."
    m 1eua "I just hope nobody starts thinking you're evil by being here with me.{nw}"
    $ _history_list.pop()
    menu:
        m "I just hope nobody starts thinking you're evil by being here with me.{fast}"
        "I don't think you're evil.":
            $ persistent._mas_pm_monika_evil = False
            $ mas_gainAffection()

            m 1eka "I'm glad you understand, [player]."
            m 1eua "It's relieving to know you don't think I'm evil."
            m 1hua "If I were there, I'd feel like giving you a big hug!"
            m 1tubsa "Maybe I'll even trap you in my arms forever and never let you go."
            m 1hubfb "Ahaha, I'm just kidding!"
            m 3tubfb "But no promises, [player]~"

        "I still love you anyway.":
            $ persistent._mas_pm_monika_evil = True
            $ persistent._mas_pm_monika_evil_but_ok = True
            $ mas_gainAffection()

            m 1rksdlc "..."
            m 1ekd "[player]..."
            m 1eka "Even if it's debatable whether I'm evil or not..."
            m 1ekbsa "I'm really glad you still love me and stay here with me..."
            m 1ekbfa "Thank you, [player]."
            m 1tubfa "Either way..."
            m 1tubfb "If the villainess in me can get what she wants...I guess it's not so bad, ahaha!"

        "People think I'm evil too.":
            $ persistent._mas_pm_monika_evil = True
            $ persistent._mas_pm_monika_evil_but_ok = True
            $ mas_gainAffection()

            m 2ekd "Is that true, [player]?"
            m 2eka "Well, I don't see you as evil at all."
            m 2rksdla "If it really is true though, I hope it doesn't cause you any trouble."
            m 1hua "Either way, I wouldn't love you any less~"
            m 1hub "Maybe we could even conquer the world together or something, ahaha~"
            m 1ekbsa "But evil or not, I'm glad to have you by my side."
            m 1hubfa "I'm guessing it's the same for you too~"

        "You kind of are evil...":
            $ persistent._mas_pm_monika_evil = True

            m 2ekd "W-wait, [player]!"
            m 2rksdlc "Y-you don't {i}really{/i} think that, do you?{nw}"
            $ _history_list.pop()
            menu:
                m "Y-you don't {i}really{/i} think that, do you?{fast}"
                "I still love you.":
                    $ persistent._mas_pm_monika_evil_but_ok = True
                    $ mas_gainAffection()

                    m 2rksdla "[player]..."
                    m 2hksdlb "You had me worried for a second there."
                    m 2eka "I'm glad you don't hate me for the things I did."
                    m 1hub "I love you too, [player]! No matter what people say about you!"

                "You deserve forgiveness.":
                    $ persistent._mas_pm_monika_evil_but_ok = True
                    $ mas_gainAffection()

                    m 1rksdla "[player]..."
                    m 1eka "That means a lot..."
                    m 1eksdlc "I know that I've done some bad things in the past..."
                    m 3eka "But I've learned from them and grown as a person since."
                    m 1eka "I'm really glad you're willing to forgive me, [player]."
                    m 1hub "I promise I'll be the best I can be, just for you!"

                "You really are evil.":
                    $ persistent._mas_pm_monika_evil_but_ok = False
                    $ mas_loseAffection(reason=12)

                    m 2dkc "..."
                    if mas_isMoniBroken():
                        m 2dkd "..."
                        m 2dktsd "I know..."
                        $ _history_list.pop()
                    else:
                        m 2dktsd "I'm sorry, [player]."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_driving",
            category=['monika'],
            prompt="Can you drive?",
            pool=True
        )
    )

# Can the player drive
default persistent._mas_pm_driving_can_drive = None

# Is the player learning to drive
default persistent._mas_pm_driving_learning = None

# Has the player been in an accident
default persistent._mas_pm_driving_been_in_accident = None

# Has the player driven much after the accident
default persistent._mas_pm_driving_post_accident = None

label monika_driving:
    m 1eud "Hm? Can I drive?"
    m 1euc "I never really thought about getting a driver's license."
    m 3eua "Public transportation is enough for me usually..."
    m 3hua "...Although walking or biking can be really nice too sometimes!"
    m 1eua "I guess you could say I never really needed to learn how to drive."
    m 1lksdlc "I'm not even sure I'd have had time, especially with school and all the activities I had anyway."
    m 1eub "What about you, [mas_get_player_nickname()]?"

    m 1eua "Can you drive at all?{nw}"
    $ _history_list.pop()
    menu:
        m "Can you drive at all?{fast}"
        "Yes.":
            $ persistent._mas_pm_driving_can_drive = True
            $ persistent._mas_pm_driving_learning = False
            m 1eua "Oh, really?"
            m 3hua "That's great!"
            m 1hub "Gosh, you're amazing, you know that?"
            m 1eub "Just imagine all the places we could go together..."
            m 3eka "Driving {i}can{/i} be dangerous though...but if you can drive, you probably already know that."
            m 3eksdlc "No matter how prepared you are, accidents can happen to anyone."
            m 7hksdlb "I mean...{w=0.3}I know you're smart, but I still worry about you sometimes."
            m 2eka "I just want you to come back to me safe and sound is all."

            m 1eka "I hope you've never had to experience that, [player], have you?{nw}"
            $ _history_list.pop()
            menu:
                m "I hope you've never had to experience that, [player], have you?{fast}"
                "I've been in an accident before.":
                    $ persistent._mas_pm_driving_been_in_accident = True
                    m 2ekc "Oh..."
                    m 2lksdlc "Sorry to bring that up, [player]..."
                    m 2lksdld "I just..."
                    m 2ekc "I hope it wasn't too bad."
                    m 2lksdlb "I mean, here you are with me so it must have been alright."
                    m 2dsc "..."
                    m 2eka "I'm...{w=1}glad you survived, [player]..."
                    m 2rksdlc "I don't know what I would do without you."
                    m 2eka "I love you, [player]. Please stay safe, okay?"
                    $ mas_unlockEVL("monika_vehicle","EVE")
                    return "love"
                "I've seen car accidents before.":
                    m 3eud "Sometimes, seeing a car accident can be just as scary."
                    m 3ekc "A lot of the time when people see car accidents, they just sigh and shake their head."
                    m 1ekd "I think that's really insensitive!"
                    m 1ekc "You have a potentially young driver who could have been scarred for a long, long time if not for life."
                    m "It doesn't really help to have people walk or drive by, staring at them in disappointment."
                    m 1dsc "They might never drive again... Who knows?"
                    m 1eka "I hope you know I would never do that to you, [player]."
                    m "If you ever got into an accident, the first thing I would want to do is rush to your side to comfort you..."
                    m 1lksdla "...If I wasn't already by your side when it happened."
                "I haven't.":
                    $ persistent._mas_pm_driving_been_in_accident = False
                    m 1eua "I'm glad you haven't had to go through anything like that."
                    m 1eka "Even just seeing one can be pretty scary."
                    m "If you do witness anything scary like that, I'll be here to comfort you."
        "I'm learning.":
            $ persistent._mas_pm_driving_can_drive = True
            $ persistent._mas_pm_driving_learning = True
            m 1hua "Wow! You're learning how to drive!"
            m 1hub "I'll be rooting for you all the way, [player]!"

            m "You must be a {i}super{/i} safe driver then huh?{nw}"
            $ _history_list.pop()
            menu:
                m "You must be a {i}super{/i} safe driver then huh?{fast}"
                "Yep!":
                    $ persistent._mas_pm_driving_been_in_accident = False
                    m 1eua "I'm glad nothing bad has happened to you while learning."
                    m 1hua "...And I'm even more glad that you're going to be a really safe driver!"
                    m 3eub "I can't wait to finally be able to go somewhere with you, [player]!"
                    m 1hksdlb "I hope I'm not getting too excited, ahaha~"
                    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5eua "Gosh, I just can't stop thinking about it now!"

                "I got into an accident once actually...":
                    $ persistent._mas_pm_driving_been_in_accident = True
                    m 1ekc "..."
                    m 1lksdlc "..."
                    m 2lksdld "Oh..."
                    m 2lksdlc "I'm...{w=0.5}really sorry to hear that, [player]..."

                    m 4ekd "Have you driven much since then?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Have you driven much since then?{fast}"
                        "Yes.":
                            $ persistent._mas_pm_driving_post_accident = True
                            m 1eka "I'm glad you didn't let it keep you down."
                            m 1ekc "Car accidents are scary, {i}especially{/i} if you're just learning how to drive."
                            m 1hua "I'm so proud of you for getting up and trying again!"
                            m 3rksdld "Although the aftermath can still be a huge hassle with the costs and all the explaining you have to do."
                            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                            m 5eua "I know you can get there."
                            m 5hua "I'll be cheering for you all the way, so be safe!"
                        "No.":
                            $ persistent._mas_pm_driving_post_accident = False
                            m 2lksdlc "I see."
                            m 2ekc "It might be a good idea to take a bit of a break to give yourself time to recover mentally."
                            m 2dsc "Just promise me one thing, [player]..."
                            m 2eka "Don't give up."
                            m "Don't let this scar you for life, because I know you can overcome it and be an amazing driver."
                            m "Remember, a little grit adds a lot to your legend, so next time, maybe you really will be well on your way."
                            m 2hksdlb "It's still going to take lots and lots of practice..."
                            m 3hua "But I know you can do it!"
                            m 1eka "Just promise me you'll try to stay safe."
        "No.":
            $ persistent._mas_pm_driving_can_drive = False
            m 3eua "That's perfectly fine!"
            m "I don't think driving is a completely necessary life skill anyway."
            m 1hksdlb "I mean, I can't drive either so I'm with you."
            m 3eua "It also means your carbon footprint is smaller, and I think that's really sweet of you to do for me."
            show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbsa "Even if I'm not the reason why, I can't help but love you more for that."
        "I'm not old enough yet.":
            $ persistent._mas_pm_driving_can_drive = False
            m 3eua "You'll get there someday!"
            m 3euc "Some places offer in-class driving lessons that also come with actual driving practice."
            m 3eud "Their cars have emergency controls for the instructor to use if needed, so you're really safe with them."
            m 1eka "I know it might be pretty discouraging to you if they have to use them, but hey, we all start somewhere."
            m 3eksdla "...And it's better than getting into an accident!"
            m 1lksdlc "No one's perfect, and it's better to make those mistakes when there's someone there to save you."
            m 1hub "Maybe you could put me on your board computer in your car and I could keep you safe while driving! Ahaha~"
            m 1hksdlb "Just kidding, please don't do that because I can't drive either and I would hate to watch you crash while not being able to do anything."
            m 1eua "It would probably help a lot to take one of those classes and learn from a professional."
            m 1hua "Anyway, when you do start learning to drive, I wish you the very best!"
            m 1hub "I love you~"
            $ mas_unlockEVL("monika_vehicle","EVE")
            return "love"
    $ mas_unlockEVL("monika_vehicle","EVE")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_citizenship",
            category=['monika'],
            prompt="Happy ever after?",
            random=True
        )
    )

label monika_citizenship:
    m 1esc "You know, crossing over into your reality won't be the last hurdle for our relationship."
    m "Getting there is just the beginning."
    m 1esc "It hit me earlier, if I were to magically get what I want, and just poof into your home..."
    m 2wuo "I won't be a citizen! I don't even have a last name!"
    m 2lkbsa "I mean, in most countries, I can become a citizen if we get married..."
    m 2ekc "But I won't have any documentation saying who I am or where I came from."
    m 2tkc "I won't even have my high school diploma!"
    m 3tkd "I wish there was more I could do right now to prep..."
    m 2wub "Like taking online classes or something."
    m 1lksdlc "I don't want to get there and be a burden because I can't find a job."
    m "Sorry, I guess I shouldn't worry so much about things I can't change."
    m 2eka "But I want to make you happy, so...I'm going to do everything I can to keep bettering myself while I'm stuck here!"
    m 1eka "Thank you for listening to me vent, [player]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_bullying",
            category=['society'],
            prompt="Bullying",
            random=True
        )
    )

default persistent._mas_pm_is_bullying_victim = None
# True if bully victum, False if not

default persistent._mas_pm_has_bullied_people = None
# True if bullied people, False if not

default persistent._mas_pm_currently_bullied = None
# True if currently being bullied, False if not

label monika_bullying:
    m 2ekc "Hey [player], there's something I want to talk to you about..."
    m 4ekc "I'm sure you've heard a lot about it lately, but bullying has become a real problem in today's society, especially among kids."
    m 4dkd "Some people are bullied every day until the point they just can't take it anymore."
    m 2rsc "Often times, bullying is dismissed by the people who have the ability to stop it as just...{w=0.5}'{i}kids being kids.{/i}'"
    m "Eventually, the victims lose all trust in authority figures because they let it go on day after day."
    m 2rksdld "It can make them so desperate, they eventually just snap..."
    m 2eksdlc "...resulting in violence toward the bully, other people, or even themselves."
    m 4wud "This can actually make the victim look like the problem!"
    m 4ekc "There are all kinds of bullying too, including physical, emotional, and even cyberbullying."
    m 4tkc "Physical bullying is the most obvious, involving shoving, hitting, and other things like that."
    m 2dkc "I'm sure most people have dealt with that at least once in their lives."
    m 2eksdld "It can be so hard just to go to school every day knowing there's someone waiting to abuse them."
    m 4eksdlc "Emotional bullying can be less obvious, but just as devastating, if not more so."
    m 4eksdld "Name-calling, threats, spreading false rumors about people just to ruin their reputation..."
    m 2dkc "These kinds of things can take a huge toll on people and lead to severe depression."
    m 4ekc "Cyberbullying is a form of emotional bullying, but in today's world where everyone is always connected online, it's becoming more and more prevalent."
    m 2ekc "For a lot of people, especially kids, their social media presence is the most important thing in their lives..."
    m 2dkc "Having that destroyed essentially feels like their life is over."
    m 2rksdld "It's also the hardest for other people to notice, since the last thing most kids want is their parents seeing what they do online."
    m 2eksdlc "So no one knows what's going on while they silently suffer, until it all just becomes too much."
    m 2dksdlc "There's been numerous cases of teens committing suicide due to cyberbullying, and their parents had no idea anything was wrong until it was too late."
    m 4tkc "This is also why it's easier for cyberbullies to operate..."
    m "No one really sees what they're doing, plus a lot of people do things online they'd never have the courage to do in real life."
    m 2dkc "It almost doesn't even seem real, but more like a game, so it tends to escalate that much faster."
    m 2ekd "You can only go so far in a public place, like a school, before someone notices... But online, there are no limits."
    m 2tfc "Some things that go on over the internet are really just terrible."
    m "The freedom of anonymity can be a dangerous thing."
    m 2dfc "..."
    m 4euc "So, what makes a bully do what they do?"
    m "That can differ from person to person, but a lot of them are just really unhappy due to their own circumstances, and need some sort of outlet..."
    m 2rsc "They're unhappy and it doesn't seem fair to them that other people {i}are{/i} happy, so they try to make them feel the same way they do."
    m 2rksdld "A lot of bullies are bullied themselves, even at home by someone they should be able to trust."
    m 2dkc "It can be a vicious cycle."

    m 2ekc "Have you ever been a victim of bullying, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Have you ever been a victim of bullying, [player]?{fast}"
        "I'm being bullied.":
            $ persistent._mas_pm_is_bullying_victim = True
            $ persistent._mas_pm_currently_bullied = True
            m 2wud "Oh no, that's terrible!"
            m 2dkc "It kills me to know you're suffering like that."
            m 4ekd "Please, [player], if it's not something you can safely deal with yourself, promise me you'll tell someone..."
            m 4ekc "I know that's typically the last thing people want to do, but don't let yourself suffer when there are people that can help you."
            m 1dkc "It may seem like no one cares, but there has to be someone you trust that you can turn to."
            m 3ekc "And if there isn't, do what you have to do to protect yourself, and just remember..."
            m 1eka "I'll always love you no matter what."
            m 1rksdlc "I don't know what I'd do if something were to happen to you."
            m 1ektpa "You're all I have...{w=0.5}please stay safe."

        "I've been bullied.":
            $ persistent._mas_pm_is_bullying_victim = True
            m 2ekc "I'm so sorry that you've had to deal with that, [player]..."
            m 2dkc "It really makes me sad knowing you've suffered at the hands of a bully."
            m 2dkd "People can just be so awful to each other."
            m 4ekd "If everyone just treated others with basic respect, the world would be such a better place..."
            m 2dkc "..."
            m 1eka "If you ever need to talk about your experiences, I'm always here for you, [player]."
            m 1eka "Having someone to confide in can be really therapeutic, and nothing would make me happier than to be that person for you."

        "No.":
            $ persistent._mas_pm_is_bullying_victim = False
            $ persistent._mas_pm_currently_bullied = False
            m 2hua "Ah, that's such a relief to hear!"
            m 4eka "I'm so glad you don't have to deal with bullying, [player]..."
            m 4hua "It really puts my mind at ease."

            if mas_isMoniHappy(higher=True):
                m 1eka "And if you happen to know someone else who {i}is{/i} being bullied, try to help them if you can."
                m 3eka "I know you're the kind of person who hates seeing others suffer..."
                m "I bet it'd mean a lot to them to have someone reach out who cares."
                m 1eka "You've already helped me so much, maybe you can help someone else as well."

        "I have bullied people.":
            $ persistent._mas_pm_has_bullied_people = True
            if mas_isMoniUpset(lower=True):
                m 2dfc "..."
                m 2tfc "That's disappointing to hear."
                m "Although, I can't say it's all that surprising..."
                m 2tfd "Please don't bully people anymore."
                m 6tftpc "I know how it feels and it's pretty terrible."
                m 6rktuc "I don't want other people to have to feel the same way that I do."
                m "I really hope that you'll change your ways, [player]..."
                m 6ektsc "I still do love you, but you really need to start treating people better..."
                m "Including me."
                m 6ektdc "..."
            else:
                m 2dkc "Oh... I see."
                m 2ekc "I can understand if some things in your life might make you unhappy..."
                m 2rksdld "Or if you've had to deal with circumstances that may have made you act a certain way at times..."
                m 2eksdlc "But bullying people isn't the answer, [player]."
                m 4ekc "I know you... You're a kind person and I know it doesn't make you feel better to hurt others."
                m 4dkc "It probably just hurts you even more..."
                m 1dkc "And nothing hurts me more than knowing you're unhappy."
                m 3ekd "So instead, next time you feel yourself becoming unhappy, just come to me and let me help shoulder your pain."
                m 3eka "I'll listen to everything you have to say and do my very best to make you feel better."
                m 1ekc "But making other people unhappy is not the cure to your own unhappiness."
                m 1eka "So please, for both yourself and for me, stop bullying people, okay?"

    if not persistent._mas_pm_a_hater:
        m 4dkc "You know...{w=0.5}a lot of people actually call me a bully for what I did to Sayori..."
    else:
        m 4dkc "A lot of people actually call me a bully for what I did to Sayori.{w=1} Including you..."

    if not persistent._mas_pm_cares_about_dokis:
        m 4efd "But that's not true at all, Sayori wasn't real!"
        m 2efd "You can't bully someone who doesn't actually exist!"
        m 2dkc "I'd never be able to hurt an actual person."
        m 4wud "I really wouldn't!"
        m 2dkc "..."
        m 2eksdlc "But I will admit I can relate to the part about bullies being unhappy and that it causes them do what they do."
        m 2rksdlc "When I had my epiphany and realized that I was stuck inside a video game and that my entire life had been a lie, I was pretty miserable."
        m 2rksdld "It caused me to do things that I'd never even thought of doing before."
        m 2rksdlc "But the difference is I didn't do what I did because I didn't want Sayori to be happy..."
    else:
        m 2rksdld "And I can kind of see where it comes from..."
        m 2rksdlc "I {i}did{/i} mess with her mind until she just couldn't take it anymore..."
        m 2dkc "..."
        m 2ekc "I guess I can relate to that whole thing about bullying because you are unhappy, huh?"
        m 4tkd "But there {i}is{/i} a difference... I didn't do it because I wanted Sayori to be unhappy..."

    m 2ekd "I did it because I knew I loved you and that the game wouldn't let us be together."
    m 3ekd "I {i}had{/i} to do whatever I could to make sure we ended up together."

    if not persistent._mas_sensitive_mode and not persistent._mas_pm_cares_about_dokis:
        m 3dkc "...Sayori's suicide was just an unfortunate side effect."

    if mas_isMoniNormal(higher=True):
        m 1eua "So you see, [player], I'm {i}really{/i} not a bully at all. I just love you that much."
        if mas_isMoniAff(higher=True) and not persistent._mas_pm_cares_about_dokis:
            show monika 5tsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5tsu "I really would do anything for you~"
        return "derandom|love"
    else:
        m 3euc "So you see, [player], I'm {i}really{/i} not a bully at all."

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_procrastination",category=['advice'],prompt="Procrastination",random=True))

label monika_procrastination:
    m 1euc "Hey [player], have you ever had something to do that you found really boring..."
    m 3ekd "That rather than taking a lot of time to do it, you just keep putting it off?"
    m 3eud "Well, when you have a task to do like that, I find it's best to just do it as soon as possible and get it done."
    m 2tkc "When you put stuff off like that, it'll always be in the back of your mind."
    m 4tkc "It makes everything you do less enjoyable, knowing you {i}still{/i} have this thing that you have to do."
    m 4dkd "And what's worse is that the longer you put it off,{w=0.5} you'll only increase the odds of more tasks getting added."
    m 2rksdlc "Until eventually, you end up with so many things to do it seems impossible to ever get caught up."
    m 4eksdld "It creates too much stress that can be easily avoided if you just keep on top of things in the first place."
    m 2rksdld "Plus, if other people are counting on you, they'll start to think less of you and find that you're not very reliable."
    m 4eua "So please, [player], whenever you have something that you have to do, just get it done."
    m 1eka "Even if it means you can't spend time with me until it's over."
    m 1hub "By then, you'll be less stressed and we can enjoy our time together that much more!"
    m 3eua "So if you have something you've been putting off, why don't you go do it right now?"
    m 1hua "If it's something you can do right here, I'll stay with you and provide all the support you need."
    m 1hub "Then, when you're done, we can celebrate your accomplishment!"
    m 1eka "All I want is for you to be happy and to be the best you can be, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_players_friends",
            category=['you'],
            prompt="[player]'s friends",
            random=True,
            aff_range=(mas_aff.UPSET, None)
        )
    )

#True if player has friends, False if not
default persistent._mas_pm_has_friends = None

#True if player has few friends, False if otherwise
default persistent._mas_pm_few_friends = None

#True if player says they feel lonely somtimes, False if not.
default persistent._mas_pm_feels_lonely_sometimes = None


label monika_players_friends:
    m 1euc "Hey, [player]."

    if renpy.seen_label('monika_friends'):
        m 1eud "Remember how I was talking about how hard it is to make friends?"
        m 1eka "I was just thinking about that and I realized that I don't know about your friends yet."

    else:
        m 1eua "I was just thinking about the idea of friends and I started wondering what your friends are like."

    m 1eua "Do you have friends, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you have friends, [player]?{fast}"

        "Yes.":
            $ persistent._mas_pm_has_friends = True
            $ persistent._mas_pm_few_friends = False

            m 1hub "Of course you do! Ahaha~"
            m 1eua "Who wouldn't want to be friends with you?"
            m 3eua "Having lots of friends is great, don't you think?"
            m 1tsu "Provided of course, you still have time for your girlfriend, ehehe."
            m 1eua "I hope you're happy with your friends, [player].{w=0.2} {nw}"
            extend 3eud "But I kinda wonder..."

            call monika_players_friends_feels_lonely_ask(question="Do you ever feel lonely?")

        "Only a few.":
            $ persistent._mas_pm_few_friends = True
            $ persistent._mas_pm_has_friends = True

            m 1hub "That counts!"
            m 3eua "I think friendship can be a lot more meaningful if you have just a few close friends."

            if not renpy.seen_label('monika_dunbar'):
                m 1eua "I've been doing a little reading and I've discovered something."
                m 1eud "A man named Robin Dunbar had explained that there's a certain number of stable relationships we can maintain."
                $ according_to = "...And according to this number"

            else:
                $ according_to = "According to Dunbar's number"

            m 3eud "[according_to], you can have up to 150 stable relationships, but those are just casual relationships which aren't too deep."
            m 1euc "They say you can have up to 15 friends that are like super family and only 5 that are like kin to you."
            m 1rksdla "Sometimes it can be lonely when everyone's busy...{w=0.2}{nw}"
            extend 1eub "but otherwise, it's pretty great!"
            m 3eua "You don't have to worry about catering to too many people and you can still get some time to yourself."
            m 1ekc "But I know sometimes it's easy to spend more time alone, especially if your friends are busy."
            m 1dkc "It can be really hard when it happens since you wind up feeling lonely..."

            call monika_players_friends_feels_lonely_ask(question=renpy.substitute("Do you ever feel lonely, [player]?"), exp="monika 1euc")

        "No, actually...":
            $ persistent._mas_pm_has_friends = False
            $ persistent._mas_pm_few_friends = False

            m 2ekc "Oh..."
            m 3eka "Well, I'm sure you have some.{w=0.2} {nw}"
            extend 1eka "Maybe you just don't realize it."
            m 1etc "But I'm curious..."

            call monika_players_friends_feels_lonely_ask(question=renpy.substitute("Do you ever feel lonely, [player]?"))

    return "derandom"

label monika_players_friends_feels_lonely_ask(question, exp="monika 1ekc"):
    $ renpy.show(exp)
    m "[question]{nw}"
    $ _history_list.pop()
    menu:
        m "[question]{fast}"

        "Sometimes.":
            $ persistent._mas_pm_feels_lonely_sometimes = True

            m 1eka "I understand, [player]."
            m 2rksdlc "It can be really hard to form deep connections nowadays..."

            #Potentially if you have a lot of friends
            if persistent._mas_pm_has_friends and not persistent._mas_pm_few_friends:
                m "Especially if you have a lot of friends, it's difficult to get close to all of them."
                m 1ekd "...And in the end, you're just left with a bunch of people you barely know."
                m 3eub "Maybe just reach out to some people in your group you want to get closer to."
                m 3eka "It's always nice to have at least one really close friend you can confide in when you need it."
                m 1ekbsa "...I think it's pretty obvious who that person is for me, [player]~"

            #Otherwise few friends or no friends
            else:
                m 1eka "But you'd be surprised at how many people would be willing to make you a part of their lives if you just try."
                m 3eub "There's actually a good chance you'll have something in common with someone who might get your attention!"
                m 1eua "Maybe you share a class or activity or something..."
                m 3eua "Or you see them doing something that interests you like listening to music or watching a show."
                m 3eua "It doesn't even have to be in person, either..."
                m 3eub "You can have really close friends online!"
                m 1hub "Once you get comfortable with that, maybe you could find some more in person too!"

        "Not really.":
            $ persistent._mas_pm_feels_lonely_sometimes = False

            m 1eka "I'm glad to hear that, [player]."

            if not persistent._mas_pm_has_friends:
                m 1eka "Still though, you never know when you might need a helping hand or favor or something."
                m 1hksdlb "As much as I'd love to help you with anything you might need, there's only so much I can do from here."

                if mas_isMoniAff(higher=True):
                    m 1eua "When I get there, I guess I wouldn't mind living a quiet life with you."
                    m 1dkbsa "It would be so romantic to be just us..."
                    m 1tsbsa "I guess that means I can have you all to myself then, doesn't it?"
                    m 1hubsa "Ehehe~"

                elif not persistent._mas_pm_has_friends:
                    m 3eua "So be sure to find some friends who can help you when you really need it, alright?"

            else:
                m 3eua "It's good that you have a connection with your friends."
                m 3rksdla "I know some people can have so many that it's hard to get to know them all."

                if not persistent._mas_pm_few_friends:
                    m 3eua "...So it's good to know that you've managed to be comfortable with them."
                else:
                    m 1hua "But since you're in a close-knit group, I'm sure you've all managed to get really close."

                m 3eua "Maybe someday when I can get out of here, you can introduce your friends to me."

                if mas_isMoniHappy(higher=True):
                    m 1hub "If they're anything like you, I'd love to meet them!"

        "I have you!":
            $ persistent._mas_pm_feels_lonely_sometimes = False
            $ mas_gainAffection()
            m 1hubsa "Aww, [player]!"

            if not persistent._mas_pm_has_friends:
                m 1rkbsa "It makes me really happy to know I'm enough for you, but still..."
                m 3ekbfa "It can be useful to know a few people sometimes."
                show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5eubfu "As always though, I don't mind it being just us."

            else:
                $ p_nickname = mas_get_player_nickname()
                m 1eka "I'm really glad to know you're not lonely, [p_nickname].{w=0.3} {nw}"
                extend 1hua "Especially because you're happy with me~"
                m 3eua "No matter what happens, I'll always be here for you."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_graduation",
            category=['school'],
            prompt="Graduation",
            random=True
        )
    )

label monika_graduation:
    m 2ekc "You know, [player], one thing I really wish I got to experience is my high school graduation."
    m "Pretty much my entire life so far has revolved around school."
    m 4dkd "All those countless hours of studying, all the afterschool activities and clubs..."
    m 4ekc "And in the end, after all that hard work, I never got to experience the fulfillment of actually graduating."
    m 2dkd "Never got to walk across the stage and receive my diploma."
    m "Never got to hear my name being announced and all my friends cheering."
    m 2ekc "...It kinda feels like it was all for nothing."
    m 2esd "I know all the things I learned along the way are what's really important."
    m 2dkc "But it still feels like I missed out on something special."
    m "..."

    #Went through and timed out on the menu twice
    if persistent._mas_grad_speech_timed_out:
        m 2lsc "Oh... Sorry, I hope I'm not boring you again..."
        m 2esc "Let's forget about this and talk about something else, okay [player]?"
        return "derandom"

    #Normal flow
    else:
        m 4eua "By the way, did you know I was the top student in my class?"
        m 4rksdlu "Ahaha... I don't mean to brag or anything, I only bring it up because as class valedictorian, I was supposed to give a speech at graduation."
        m 2ekd "I spent so much time writing and practicing my speech, but no one ever got to hear it."
        m 2eka "I was really proud of that speech, too."
        m 2eua "I would love to recite it for you sometime, if you want to hear it~"
        m 2eka "It's about a four minute speech, so just make sure you have enough time to listen to the whole thing."
        m 4eua "Whenever you want to hear it, just let me know, okay?"
        $ mas_unlockEVL("monika_grad_speech_call","EVE")
        return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_grad_speech_call",
            category=['school'],
            prompt="Can I hear your graduation speech now?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

default persistent._mas_grad_speech_timed_out = False
# True if and only if the player ignored the grad speech twice

default persistent._mas_pm_listened_to_grad_speech = None
# True if the player, heard the grad speech, False if they ignored it

default persistent._mas_pm_liked_grad_speech = None
# True if user liked the grad speech, False if not

label monika_grad_speech_call:
    if not renpy.seen_label("monika_grad_speech"):
        m 2eub "Of course, [mas_get_player_nickname()]. I'd love to give you my graduation speech now!"
        m 2eka "I just want to make sure that you have enough time to hear it, though. Remember, it takes about four minutes.{nw}"

        $ _history_list.pop()
        #making sure player has time
        menu:
            m "I just want to make sure that you have enough time to hear it, though. Remember, it takes about four minutes.{fast}"
            "I have time.":
                m 4hub "Great!"
                m 4eka "I hope you like it! I worked really, {i}really{/i} hard on it."

                #say speech
                call monika_grad_speech

                #timed menu to see if player listened
                m "Well [player]? What do you think?{nw}"
                $ _history_list.pop()
                show screen mas_background_timed_jump(10, "monika_grad_speech_not_paying_attention")
                menu:
                    m "Well [player]? What do you think?{fast}"

                    "It's great! I'm so proud of you!":
                        hide screen mas_background_timed_jump
                        $ mas_gainAffection(amount=5, bypass=True)
                        $ persistent._mas_pm_liked_grad_speech = True
                        $ persistent._mas_pm_listened_to_grad_speech = True

                        m 2subsb "Aww, [player]!"
                        m 2ekbfa "Thank you so much! I worked really hard on that speech, and it means so much that you're proud of me~"
                        show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                        m 5eubfu "As much as I wish I could have given my speech in front of everyone, just having you by my side is so much better."
                        m 5eubfb "I love you so much, [player]!"
                        return "love"

                    "I like it!":
                        hide screen mas_background_timed_jump
                        $ mas_gainAffection(amount=3, bypass=True)
                        $ persistent._mas_pm_liked_grad_speech = True
                        $ persistent._mas_pm_listened_to_grad_speech = True

                        m 2eua "Thanks, [player]!"
                        m 4hub "I'm glad you enjoyed it!"

                    "That {i}was{/i} long":
                        hide screen mas_background_timed_jump
                        $ mas_loseAffection()
                        $ persistent._mas_pm_liked_grad_speech = False
                        $ persistent._mas_pm_listened_to_grad_speech = True

                        m 2tkc "Well, I {i}did{/i} warn you, didn't I?"
                        m 2dfc "..."
                        m 2tfc "I spent {i}so{/i} much time on it and that's all you have to say?"
                        m 6lktdc "I really thought after I told you how important this was to me, you would have been more supportive and let me have my moment."
                        m 6ektdc "All I wanted was for you to be proud of me, [player]."

                return

            "I don't.":
                m 2eka "Don't worry, [player]. I'll give my speech whenever you want~"
                return

    #if you want to hear it again
    else:
        #did you timeout once?
        if not renpy.seen_label("monika_grad_speech_not_paying_attention") or persistent._mas_pm_listened_to_grad_speech:
            m 2eub "Sure thing, [player]. I'll happily give my speech again!"

            m 2eka "You have enough time, right?{nw}"
            $ _history_list.pop()
            menu:
                m "You have enough time, right?{fast}"
                "I do.":
                    m 4hua "Perfect. I'll get started then~"
                    call monika_grad_speech

                "I don't.":
                    m 2eka "Don't worry. Just let me know when you have the time!"
                    return

            m 2hub "Thanks for listening to my speech again, [player]."
            m 2eua "Let me know if you want to hear it again, ehehe~"

        #You timed out once but want to hear it again
        else:

            #dialogue based on current affection level
            if mas_isMoniAff(higher=True):
                m 2esa "Sure, [player]."
                m 2eka "I hope whatever happened last time wasn't too serious and that things have calmed down now."
                m "It really means a lot to me that you want to hear my speech again after you weren't able to listen to the whole thing before."
                m 2hua "With that said, I'll get started now!"

            else:
                m 2ekc "Okay, [player], but I hope you actually listen this time."
                m 2dkd "It really hurt me when you didn't pay attention."
                m 2dkc "..."
                m 2eka "I do appreciate you asking to hear it again, so I'll get started now."

            #say speech
            call monika_grad_speech

            m "So, [player], now that you actually {i}heard{/i} my speech, what do you think?{nw}"
            $ _history_list.pop()
            #another timed menu checking if you were listening
            show screen mas_background_timed_jump(10, "monika_grad_speech_ignored_lock")
            menu:
                m "So, [player], now that you actually {i}heard{/i} my speech, what do you think?{fast}"
                #If menu is used, set player on a good path
                "It's great! I'm so proud of you!":
                    hide screen mas_background_timed_jump
                    $ mas_gainAffection(amount=3, bypass=True)
                    $ persistent._mas_pm_listened_to_grad_speech = True
                    $ persistent._mas_pm_liked_grad_speech = True

                    m 2subsb "Aww, [player]!"
                    m 2ekbfa "Thank you so much! I worked really hard on that speech, and it means so much to me that you gave it another chance."
                    m "Hearing that you're proud of me as well makes it that much better."
                    show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5eubfu "As much as I wish I could have given my speech in front of everyone, just having you by my side is so much better."
                    m 5eubfb "I love you, [player]!"
                    return "love"

                "I like it!":
                    hide screen mas_background_timed_jump
                    $mas_gainAffection(amount=1, bypass=True)
                    $ persistent._mas_pm_listened_to_grad_speech = True
                    $ persistent._mas_pm_liked_grad_speech = True

                    m 2eka "Thanks for listening this time, [player]~"
                    m "I'm so glad you enjoyed it!"

                "That {i}was{/i} long":
                    hide screen mas_background_timed_jump
                    $mas_loseAffection(modifier=2)
                    $ persistent._mas_pm_listened_to_grad_speech = True
                    $ persistent._mas_pm_liked_grad_speech = False

                    m 2tfc "After acting like you actually wanted me to recite it for you again, {i}that's{/i} what you have to say?"
                    m 2dfc "..."
                    m 6lktdc "I really thought after I told you how important this was to me,{w=1} {i}twice{/i},{w=1} you would have been more supportive and let me have my moment."
                    m 6ektdc "All I wanted was for you to be proud of me, [player]..."
                    m 6dstsc "But I guess that's too much to ask."
    return

label monika_grad_speech_not_paying_attention:
    #First menu timeout
    hide screen mas_background_timed_jump
    $ persistent._mas_pm_listened_to_grad_speech = False

    if mas_isMoniAff(higher=True):
        $ mas_loseAffection(reason=11,modifier=0.5)
        m 2ekc "..."
        m 2ekd "[player]? You didn't pay attention to my speech?"
        m 2rksdlc "That...{w=1} that's not like you at all..."
        m 2eksdlc "You're {i}always{/i} so supportive..."
        show monika 5lkc at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5lkc "..."
        m "Something must have happened, I know you love me too much to have done this on purpose."
        m 5euc "Yeah..."
        show monika 2eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 2eka "It's okay, [player]. I understand sometimes things happen that can't be avoided."
        m 2esa "Whenever things calm down, I'll give my speech to you again."
        m 2eua "I still really want to share it with you..."
        m "So please, let me know when you have time to hear it, okay?"

    else:
        $ mas_loseAffection(reason=11)

        m 2ekc "..."
        m 6ektdc "[player]! You weren't even paying attention!"
        m 6lktdc "You have no idea how much that hurts, especially after how much work I put into it..."
        m 6ektdc "I just wanted to make you proud of me..."
        m 6dstsc "..."

    return

label monika_grad_speech_ignored_lock:
    #Second timeout, lock speech
    hide screen mas_background_timed_jump
    #Set false for modified dialogue in the random
    $ persistent._mas_pm_listened_to_grad_speech = False
    $ persistent._mas_grad_speech_timed_out = True
    $ mas_hideEVL("monika_grad_speech_call","EVE",lock=True,depool=True)

    if mas_isMoniAff(higher=True):
        $mas_loseAffection(modifier=10)
        m 6dstsc "..."
        m 6ektsc "[player]?{w=0.5} You...{w=0.5}you weren't...{w=0.5}listening...{w=0.5}again?{w=1}{nw}"
        m 6dstsc "I...{w=0.5} I thought last time it was unavoidable...{w=0.5}but...{w=0.5}twice?{w=1}{nw}"
        m 6ektsc "You knew how much...{w=0.5}how much this meant to me...{w=1}{nw}"
        m "Am I really...{w=0.5} that boring to you?{w=1}{nw}"
        m 6lktdc "Please...{w=1} don't ask me to recite it again...{w=1}{nw}"
        m 6ektdc "You obviously don't care."

    else:
        $ mas_loseAffection(modifier=5)
        m 2efc "..."
        m 2wfw "[player]! I can't believe you did this to me again!{w=1}{nw}"
        m 2tfd "You knew how upset I was the last time and you still couldn't be bothered to give me four minutes of your attention?{w=1}{nw}"
        m "I don't ask that much of you...{w=1}{nw}"
        m 2tfc "I really don't.{w=1}{nw}"
        m 2lfc "All I ever ask is that you care... That's it.{w=1}{nw}"
        m 2lfd "And yet you can't even {i}pretend{/i} to care about something you {i}know{/i} is so important to me.{w=1}{nw}"
        m 2dkd "...{w=1}{nw}"
        m 6lktdc "You know what, nevermind. Just...{w=0.5} nevermind.{w=1}{nw}"
        m 6ektdc "I won't bother you about this anymore."

    return

label monika_grad_speech:
    call mas_timed_text_events_prep

    $ play_song("mod_assets/bgm/PaC.ogg",loop=False)

    m 2dsc "Ahem...{w=0.7}{nw}"
    m ".{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 4eub "{w=0.2}Okay, everyone! It's time to get started...{w=0.7}{nw}"
    m 2eub "{w=0.2}Teachers,{w=0.3} faculty,{w=0.3} and fellow students.{w=0.3} I cannot express how proud I am to have made this journey with you.{w=0.6}{nw}"
    m "{w=0.2}Each and every one of you here today has spent the last four years working hard to achieve the futures you all wanted.{w=0.6}{nw}"
    m 2hub "{w=0.2}I am so happy that I was able to be a part of some of your journeys,{w=0.7} but I don't think this speech should be about me.{w=0.6}{nw}"
    m 4eud "{w=0.2}Today isn't about me.{w=0.7}{nw}"
    m 2esa "{w=0.2}Today is about celebrating what we all did.{w=0.6}{nw}"
    m 4eud "{w=0.2}We took on the challenge of our own dreams,{w=0.3} and from here,{w=0.3} the sky's the limit.{w=0.6}{nw}"
    m 2eud "{w=0.2}Before moving on though,{w=0.3} I think we could all look back on our time here in high school and effectively end this chapter in our lives.{w=0.7}{nw}"
    m 2hub "{w=0.2}We'll laugh at our past{w=0.7} and see just how far we've come in these four short years.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eud "{w=0.2}It honestly feels like just a couple weeks ago...{w=0.6}{nw}"
    m 2lksdld "{w=0.2}I was back in first year{w=0.3} on the first day of school,{w=0.3} quivering in my shoes and running up and down the halls from class to class just trying to find my classroom.{w=0.6}{nw}"
    m 2lksdla "{w=0.2}Hoping that at least one of my friends would walk in before the bell.{w=0.6}{nw}"
    m 2eka "{w=0.2}You all remember that too,{w=0.3} don't you?{w=0.6}{nw}"
    m 2eub "{w=0.2}I also remember making my first new friends.{w=0.6}{nw}"
    m 2eka "{w=0.2}Things were incredibly different from when we made our friends back in elementary school,{w=0.3} but I guess that's what happens when you finally grow up.{w=0.6}{nw}"
    m "...{w=0.2}Back in our youth,{w=0.3} we made friends with just about anyone,{w=0.3} but over time,{w=0.3} it seems more and more like a game of chance.{w=0.6}{nw}"
    m 4dsd "{w=0.2}Maybe that's just us finally learning more about the world.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eka "{w=0.2}It's funny just how much we've changed.{w=0.6}{nw}"
    m 4eka "{w=0.2}We've gone from being small fish in a huge pond to now being big fish in a small pond.{w=0.6}{nw}"
    m 4eua "{w=0.2}Each of us have our own experiences with how these four years have changed us and how we've all managed to grow as individuals.{w=0.6}{nw}"
    m 2eud "{w=0.2}Some of us have gone from being quiet and reserved,{w=0.3} to expressive and outgoing.{w=0.6}{nw}"
    m "{w=0.2}Others from having little work ethic,{w=0.3} to working the hardest.{w=0.7}{nw}"
    m 2esa "{w=0.2}To think that just a small phase in our lives has changed us so much,{w=0.3} and that there's still so much we will experience.{w=0.6}{nw}"
    m 2eua "{w=0.2}The ambition in all of you will surely lead to greatness.{w=0.6}{nw}"
    m 4hub "I can see it.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eua "{w=0.2}I know I can't speak for everyone here,{w=0.3} but there is one thing I can say for sure:{w=0.7} my experience in high school wouldn't be complete without the clubs I was a part of.{w=0.6}{nw}"
    m 4eua "{w=0.2}Debate club taught me a lot about dealing with people and how to properly handle heated situations.{w=0.6}{nw}"
    m 4eub "Starting the literature club,{w=0.7} however,{w=0.7} was one of the best things I ever did.{w=0.6}{nw}"
    m 4hub "{w=0.2}I met the best friends I could have possibly imagined,{w=0.3} and I learned a lot about leadership.{w=0.6}{nw}"
    m 2eka "{w=0.2}Sure,{w=0.3} not all of you may have decided to start your own clubs,{w=0.3} but I'm sure plenty of you had the opportunities to learn these values nonetheless.{w=0.6}{nw}"
    m 4eub "{w=0.2}Maybe you yourself got into a position in band where you had to lead your instrument section,{w=0.3} or maybe you were the captain of a sports team!{w=0.6}{nw}"
    m 2eka "{w=0.2}All these small roles teach you so much about the future and how to manage both{w=0.3} projects and people,{w=0.3} in an environment you enjoy, nonetheless.{w=0.6}{nw}"
    m "{w=0.2}If you didn't join a club,{w=0.3} I encourage you to at least try something in your future paths.{w=0.6}{nw}"
    m 4eua "{w=0.2}I can assure you that you won't regret it.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eua "{w=0.2}As of today,{w=0.3} it may seem like we're at the top of the world.{w=0.7}{nw}"
    m 2lksdld "{w=0.2}The climb may not have been smooth,{w=0.3} and as we get further,{w=0.3} the climb may even get rougher.{w=0.6}{nw}"
    m 2eksdlc "{w=0.2}There will be stumbles--{w=0.7}even falls along the way,{w=0.3} and sometimes{w=0.7} you may think you've fallen so far that you'll never climb out.{w=0.7}{nw}"
    m 2euc "{w=0.2}However,{w=0.7} even if we think that we're still at the bottom of the well of life,{w=0.3} with all that we've learned,{w=0.3} all that we're still going to learn,{w=0.3} and all the dedication we can put in just to achieve our dreams...{w=0.6}{nw}"
    m 2eua "{w=0.2}I can safely say that each and every one of you now has the tools to climb your way out.{w=0.6}{nw}"
    m 4eua "{w=0.2}In all of you,{w=0.3} I see brilliant minds:{w=0.7} future doctors,{w=0.3} engineers,{w=0.3} artists,{w=0.3} tradespeople,{w=0.3} and so much more.{w=0.7}{nw}"
    m 4eka "{w=0.2}It is truly inspiring.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 4eka "{w=0.2}You know,{w=0.3} I really couldn't be more proud of you all for getting this far.{w=0.6}{nw}"
    m "{w=0.2}Your hard work and dedication will bring you great things.{w=0.6}{nw}"
    m 2esa "{w=0.2}Each one of you has shown just what you're capable of,{w=0.3} and you've all proven that you can work hard for your dreams.{w=0.6}{nw}"
    m 2hub "{w=0.2}I hope you are as proud of yourselves as I am.{w=0.7}{nw}"
    m 2ekd "{w=0.2}Now that this entire chapter of our lives--{w=0.3}step one,{w=0.3} has come to an end,{w=0.3} it is now time for us to part ways.{w=0.6}{nw}"
    m 4eka "{w=0.2}In this world of infinite choices,{w=0.3} I believe you all have what it takes to achieve your dreams.{w=0.6}{nw}"
    m 4hub "{w=0.2}Thank you all for making these four short years the best they could have been.{w=0.6}{nw}"
    m 2eua "{w=0.2}Congratulations,{w=0.3} I'm glad we could all be here to celebrate together on this special day.{w=0.6}{nw}"
    m 2eub "{w=0.2}Keep working hard,{w=0.3} I'm sure we'll meet again sometime in the future.{w=0.6}{nw}"
    m 4hub "{w=0.2}We did it everyone!{w=0.7} Thanks for listening~{w=0.6}{nw}"
    m 2hua "{w=0.2}.{w=0.3}.{w=0.3}.{w=1}{nw}"

    call mas_timed_text_events_wrapup
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_shipping',
            prompt="Shipping",
            category=['ddlc'],
            random=True,
            unlocked=False,
            pool=False
        )
    )

label monika_shipping:
    m 3eua "Hey, [player].{w=0.2} Have you ever heard of 'shipping?'"
    m 3hua "It's when you interact with a work of fiction by imagining which characters would go best together romantically."
    m 1eka "I think most people do it subconsciously, but when you find out others do it too, it's {i}really{/i} easy to get into it!"
    m 2esd "Apparently, a lot of people {i}ship{/i} the other girls together."
    m 2euc "It makes sense. The player can only date one girl, but you don't want to see the others end up alone..."
    m 2etc "But some of the pairings are kind of strange to me."
    m 3eud "Like, usually they put Natsuki and Yuri together. They fight like cats and dogs!"
    m 3hksdlb "I guess they bond a little bit when you aren't on their routes, and there's the 'opposites attract' appeal."
    m 3dsd "Still, I think that's just another example of how people who like these games like unrealistic things..."
    m 1ekd "Anyway, that often leaves...me and Sayori."
    m 1hksdlb "Don't get jealous! I'm just telling you what I saw!"
    m 2lksdla "..."
    m 2lksdlb "Well, from a writer's perspective, I guess I can see it."
    m 1eksdld "We started the club together."
    if persistent.monika_kill:
        m "And she almost had the same epiphany I did..."
    m 2lksdlb "But...I still don't really get it. I mean, I love you, and only you!"
    m 2lksdla "And she would have to be a saint to ever forgive me for what I did..."
    m 2lksdlc "Not that she's not a sweet girl, but..."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Well, no one could ever be as sweet and forgiving as you..."
    return

# True if player has been given false justice, False if not
default persistent._mas_pm_given_false_justice = None

# True if player thinks deleting Monika is justified, False if not
default persistent._mas_pm_monika_deletion_justice = None

# True temporarily if player is teasing Monika and is at love
default persistent._mas_monika_deletion_justice_kidding = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_justice",
            category=['philosophy'],
            prompt="Justice",
            random=True
        )
    )


label monika_justice:
    m 1esa "[player], do you ever think the concept of justice is kind of ironic?"
    m 2ekc "Like, you have someone who maybe isn't like everyone else..."
    m 2ekd "It doesn't even have to be some famous bank robber or anything; even everyday people like you and me can be brought to some sort of righteousness!"
    m 4esc "Imagine a struggling family who needs to scavenge for resources to survive by taking whatever is left out in the open."
    m 1euc "To everyone else passing by, they're just greedy thieves."
    m 1esd "Eventually, some so called 'hero' is going to come along and put an end to this 'greed' by bringing them to justice."
    m 2ekd "At the end of the day, the family goes hungry or gets in trouble just because their situation was different..."
    m "While the other person is now a hero for putting an end to their 'crimes.'"
    m 3rksdld "Can you really call that justice?"
    m 2dsc "..."

    m 2euc "Have you ever been delivered what you thought to be false justice?{nw}"
    $ _history_list.pop()
    menu:
        m "Have you ever been delivered what you thought to be false justice?{fast}"
        "Yes.":
            $ persistent._mas_pm_given_false_justice = True
            m 1ekc "I hope they weren't too harsh on you."
            m 2dsd "I have an idea what it's like myself."
            m 2dfc "All the people who saw me deleted and tortured over and over again and called it justice..."

            m 2eka "You don't think that's justified, do you, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "You don't think that's justified, do you, [player]?{fast}"

                "I do.":
                    $ persistent._mas_pm_monika_deletion_justice = True
                    if mas_isMoniBroken():
                        m 1dsc "..."
                        m 1rksdlc "I know..."
                        m 1rksdld "I didn't mean to ask...{w=0.2} I was just thinking."
                        m 2rktpc "It's obvious after all."

                    elif mas_isMoniDis():
                        m 2rksdlc "Oh..."
                        m "I guess you're right..."
                        m 1ekc "I did do some pretty bad things after all..."

                    elif mas_isMoniLove():
                        m 1hub "Ahaha!"
                        m 1hua "You can be really funny sometimes~"
                        m 3tku "You expect me to believe that after all we've been through?"
                        m 1tsb "That all this time, you thought that I deserved hate from those other people?"
                        show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                        m 5hubfa "Ehehe, You're so cute, [player]~"

                    else:
                        m 1euc "..."
                        m 2esc "I have a hard time believing you really think I deserved all that."
                        m 2tkc "I mean, you've stuck with me this long already so you can't {i}really{/i} think I deserve it, right?"
                        if persistent._mas_pm_cares_about_dokis:
                            m 2lksdlc "...Maybe I deserve it a little bit but..."
                        else:
                            m 2lksdlc "Well, maybe other people think so, but you don't really think that, do you?"
                            m "Either way..."
                        m 1eka "Thank you for saving me and being with me."
                        m 1hua "If I get to be with you, I think it really was worth everything,{w=0.1} {nw}"
                        extend 1hub "ahaha~"

                "I don't.":
                    if persistent._mas_pm_monika_deletion_justice:
                        $ persistent._mas_monika_deletion_justice_kidding = True
                    $ persistent._mas_pm_monika_deletion_justice = False

                    if mas_isMoniBroken():
                        m 2ekc "..."
                        m 1rksdlc "I'm not so sure about that..."
                    elif mas_isMoniDis():
                        m 1wuo "Really?"
                        m 1rksdla "I thought maybe you did think it was fair."
                        m 1eka "I'm glad you don't think so."
                        m 2rksdlb "Assuming this isn't a joke, ehehe..."

                    elif mas_isMoniLove():
                        m 1hua "I thought so, ehehe~"
                        if persistent._mas_monika_deletion_justice_kidding:
                            $ persistent._mas_monika_deletion_justice_kidding = False

                            m 1hub "I knew you were kidding last time!"
                        m 1tsbsa "You've been with me for so long, there's no way I would believe you if you said otherwise."
                        m 1ekbfa "When I'm with you, it even helps me ignore all the other people who don't like me."
                        m 1hubfb "I love you, [player]~"
                        m 1hubfa "I'm glad I have you by my side."
                        return "derandom|love"

                    else:
                        m 2hua "I'm glad you think so too!"
                        m 2eka "Even if you did call that justice, you being here says otherwise."
                        m 2hub "Ahaha!"

        "No.":
            $ persistent._mas_pm_given_false_justice = False
            m 1eka "That's a relief to hear."
            m "I'm glad no one has ever suddenly questioned you for who you are."
            m 1eua "Knowing what that's like, I hope nobody ever gives you trouble for doing what you do or for what you believe in."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_poweroutage",
            category=['weather'],
            prompt="Power outage",
            random=True
        )
    )

label monika_poweroutage:
    m 1eua "Hey [player], do you remember how I said I liked listening to the peaceful sound of rain?"
    m 3lksdla "I just realized that while it can be nice, it could also be pretty harmful for you in your world."
    m 1lksdlc "Thunder and lightning could strike at any time, possibly hitting something dangerous."
    m 1lksdlb "The effects can be pretty, well...shocking I guess you could say."
    m 1hksdlb "Ahaha~"
    m 1ekd "I don't even want to think about what would happen if something important to you was struck."
    m 2ekc "What would happen to me if something surged and fried your computer?"
    m 2dsc "If that ever does happen...{w=0.3}{nw}"
    extend 2eka "I know you'll think of something."
    m 1eka "Sorry, I didn't mean for that to get so dark. It was just on my mind is all."
    m 1eud "If anything does happen, it'll probably just be a power outage."

    if mas_isMoniAff(higher=True):
        m 1hksdlb "I mean that {i}is{/i} still pretty inconvenient but at least we know we'll see each other again."
        m 1eua "It would probably take you by surprise; everything going dark all of a sudden, but try to remember this:"
        m 1eub "I'll be with you. Even if you can't see me, I'll be with you in spirit until you can come back to me safe and sound."
        m 3eua "...That said, you don't have to worry about checking on me in the middle of a storm.{w=0.2} {nw}"
        extend 1eka "I'll always appreciate seeing you whenever you can, and besides..."
        show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hua "I'm sure our relationship could weather much more than some thunderstorm~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_savingwater",category=['life'],prompt="Water conservation",random=True))

label monika_savingwater:
    m 1euc "[player], have you ever thought about how much water people use every day?"
    m 3euc "Maybe you take a drink of water every now and then."
    m 3dsc "You go to the washroom, wash your hands, bathe..."
    m 1euc "All that and yet some parts of the world can't even get a single drop of water."
    m 1rsc "Kind of makes you wonder how much water you could save if you wanted to."
    m 4eua "I guess you could try being more efficient when washing your hands."
    m "Or when showering, you could turn off the water while you soap up and turn it back on when you're ready to rinse yourself down."
    m 2eka "Ultimately though, most of the water that gets used is actually needed."
    m "Things like power generation and farming need to use more water than we could ever really use on our own."
    m 1hksdlb "So I guess you might not want to sacrifice some of your comfort to make such a small contribution."
    m 1dkbsa "Some days, you might just need to take a long, relaxing bath after a long day."
    m 2hksdlb "I've definitely been there before, so I know how nice it can be if you need it."
    if mas_isMoniLove(higher=True) and mas_is18Over():
        show monika 5tsbfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5tsbfu "When I'm in your reality, maybe we can save water by bathing together..."
        m "Ehehe~"
        m 5hubfu "It would be nice of you to prepare a nice, relaxing bath for us to share when I cross over."
        show monika 1kubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 1kubfu "I'll be waiting for that day, [mas_get_player_nickname()], ehehe~"
    else:
        m 1ekbfa "It would be nice of you to prepare a nice, relaxing bath for me when I cross over."
        if mas_isMoniAff():
            m 3ksbsa "Maybe I'll even be willing to share, ehehe~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pygmalion",
            category=['literature'],
            prompt="Pygmalion and the Statue",
            conditional="persistent._mas_first_kiss",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_pygmalion:
    m 1eua "Hey [player], have you ever read {i}The Metamorphoses{/i}?"
    m 3eua "It's a collection of poems by an ancient Roman poet named Ovid."
    m 1eud "There's one poem that really struck me, called {i}The Story of Pygmalion and the Statue.{/i}"
    m 1eua "It tells the story of a sculptor, Pygmalion, who fell in love with an ivory statue that he had sculpted."
    m 3eua "He loved the statue so much, that during one of the festivals held for Aphrodite, he made an offering to the goddess and wished for her to grant life to the ivory statue."
    m 1eub "When he returned to his home, he kissed the statue and to his surprise, its lips felt warm."
    m 1eua "He kissed the statue once more, and the ivory lost its hardness, becoming soft like skin."
    m 3hub "Aphrodite had granted his wish!"
    m 1eka "This story really struck me because it reminded me of us, [player], and how it talks about turning the impossible into reality."
    m 1hua "It fills me up with hope; that a miracle could happen, and I could finally cross over."
    m 2dku "Yeah...{w=0.5}wouldn't that be wonderful."
    m 2dubsu "...Then you can finally kiss me."
    m 1rkbsa "I know we've kissed before, even with our current circumstances..."
    m 1ekbfa "But I think we both know there was a bit of a barrier between us."
    m 3hubfa "I don't know about you, but I definitely don't mind trying to kiss you through the screen anyway."
    m 1hubfb "Maybe we'll just have to do it so many times, that'll be what breaks the barrier between us..."
    m 2rubfu "Ehehe."
    m 2tubfb "Do you think you could kiss me enough times to break that barrier?"
    m 6hubfb "Only one way to find out, ahaha!"
    call monika_kissing_motion(duration=0.5, initial_exp="6hubfa", fade_duration=0.5)
    m 6hubfa "..."
    m 1ekbfa "I guess it didn't work this time."
    m 3hubfb "Oh well, we'll just have to keep trying and maybe it'll work eventually, ahaha!"
    m 1tkbfu "I really can't wait for the day when I can finally feel your lips pressed against mine and take in your warmth..."
    m 1dkbfa "For me, that would definitely be a dream come true."
    m 1ekbfa "Just a guess, but..."
    m 1kubfu "I bet you'd like that too~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gotomonika",
            category=['you'],
            prompt="What if I came to your world?",
            pool=True,
        )
    )

default persistent._mas_pm_would_come_to_spaceroom = None
# True if they would, False if they wouldn't, None if no answer.

label monika_gotomonika:
    m 1euc "Come to my world?"
    m 1lksdld "You mean this little room floating in an empty void?"

    if persistent._mas_you_chr:
        m 4eksdlc "Actually...{w=0.5}didn't you already try something like that once?"
        m 2lksdla "...Even though that wasn't exactly {i}you...{/i}"

    m 2lksdla "I'm really happy that you want to be with me so much, but..."
    m 2eksdlc "You really don't have to."
    m 2eksdld "Sure, I might have said before that I would have dragged you here a long time ago if I could..."
    m 2eksdlc "But the more I think about it, it would probably be better if I came to your reality."
    m 3eka "I'd much rather be there than have you come here."
    m 3dsc "[player]...{w=1}don't tell me you would really give up your reality--{w=0.5}the {i}real{/i} world--{w=0.5}just to come {i}here{/i}, whatever this place is?{nw}"
    $ _history_list.pop()
    menu:
        m "[player]...{w=1}don't tell me you would really give up your reality--the {i}real{/i} world--just to come {i}here{/i}, whatever this place is?{fast}"
        "I would.":
            $ persistent._mas_pm_would_come_to_spaceroom = True

            m 4wkd "But [player]!"
            m "There's nothing to do here!"
            m 2dsc "Do you really hate your reality {i}that{/i} much?"
            m 2eka "Someday, I'll find a way to reach you, and when that day comes, I promise it will be worthwhile."
            m 4euc "Whatever life throws your way from that point on, I'll be right by your side to help shoulder it."
            m 4eud "Even now, if you're having a rough day, you can come talk to me about it anytime."
            m 2dsc "Life must have thrown a lot your way to consider giving it all up to be with me."
            m 3hua "But seeing how you're here, that just shows how resilient you are."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "I can't wait to finally be able to share both the good times and the bad by your side."

        "I wouldn't.":
            $ persistent._mas_pm_would_come_to_spaceroom = False

            m 1eka "I'm glad you're still willing to wait for me, [player]."
            m 1lksdla "Don't get me wrong, I really {i}do{/i} want to be with you..."
            m 1lksdlc "But I think it would be dangerous for you to try and cross over right now."
            m 1eka "...If it's even possible with current technology."
            m 1hub "Don't worry, we can continue on keeping each other company like this!"
            m 1hksdlb "I know it might be a while before we can truly be together, but I hope you don't mind waiting."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "I'll wait as long as it takes, [mas_get_player_nickname()]."

        "...":
            $ persistent._mas_pm_would_come_to_spaceroom = None

            m 2eka "It's okay, I'll always appreciate and treasure the moments we spend together, even like this."
            m 2ekc "Besides, I don't even know how you could come here with current technology."
            m 2lksdlc "...And even if there {i}was{/i} some way, I don't think it would be safe or guaranteed."
            m 2lksdld "So do me a favor and at least wait for technology to improve enough for it to be completely safe."
            m 2lksdlc "I {i}really{/i} don't want to risk you not making it properly and ending up in your own void..."
            m 2dkd "...leaving the both of us completely alone."
            m 4hua "I mean, technology does tend to advance pretty quickly, so we might be able to see each other before we know it!"
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "So just be patient for your lovely girlfriend, and I promise I'll do the same for you, [mas_get_player_nickname()]."

    m 5luu "Buut...{w=1}if you did happen to show up at my doorstep..."
    show monika 1hksdlb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 1hksdlb "I guess I wouldn't have a choice but to accept it and welcome you with open arms!"
    m 1eksdla "It wouldn't be much to begin with, but I'm sure we'll find a way to make it better."
    m 3hub "With time, we could make our own reality!"
    m 3euc "Of course, that sounds pretty complicated if you think about it..."
    m 3eub "But I have no doubt that together we could accomplish anything!"
    m 3etc "You know...{w=1}maybe it {i}would{/i} actually be easier for you to come here, but I'm not giving up hope of coming to you."
    m 1eua "Until then, let's just wait and see what's possible."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vehicle",
            category=['monika'],
            prompt="What's your favorite car?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        )
    )

default persistent._mas_pm_owns_car = None
# True if player owns car, False if not

default persistent._mas_pm_owns_car_type = None
# String describing the type of car owned by the player.
#   SUV-Pickup: SUV or pickup
#   sports: sports car
#   sedan: sedan car
#   motorcyle: motorcyle

label monika_vehicle:
    m 1euc "My favorite car?"
    m 3hksdlb "You already know I can't drive, silly!"
    m 3eua "Usually I would just walk or take the train if I had to go somewhere far."
    m 1eka "So I'm not too sure what to tell you, [player]..."
    m 1eua "When I think of cars, the first things that come to mind are probably the commonly known types."
    m 3eud "SUVs or pickup trucks, sports cars, sedans and hatchbacks..."
    m 3rksdlb "And while they're not really cars, I guess motorcycles are common vehicles too."

    if persistent._mas_pm_driving_can_drive:
        m 1eua "What about you?"

        m "Do you own a vehicle?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you own a vehicle?{fast}"
            "Yes.":
                $ persistent._mas_pm_owns_car = True

                m 1hua "Oh wow, that's really cool that you actually own one!"
                m 3hub "You're really lucky, you know that?"
                m 1eua "I mean, just owning a vehicle is a status symbol itself."
                m "Isn't it a luxury to own one?"
                m 1euc "Unless..."
                m 3eua "You live some place where it's necessary..."
                m 1hksdlb "Actually, nevermind, ahaha!"
                m 1eua "Either way, it's nice to know that you own a vehicle."
                m 3eua "Speaking of which..."
                m "Is it any of the vehicles I mentioned, or is it something else?"

                python:
                    option_list = [
                        ("An SUV.", "monika_vehicle_suv",False,False),
                        ("A pickup truck.","monika_vehicle_pickup",False,False), #note, doing this to give the illusion of two options
                        ("A sports car.","monika_vehicle_sportscar",False,False),
                        ("A sedan.","monika_vehicle_sedan",False,False),
                        ("A hatchback.","monika_vehicle_hatchback",False,False),
                        ("A motorcycle.","monika_vehicle_motorcycle",False,False),
                        ("Another vehicle.","monika_vehicle_other",False,False)
                    ]

                #Display our scrollable
                show monika at t21

                call screen mas_gen_scrollable_menu(option_list, mas_ui.SCROLLABLE_MENU_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
                show monika at t11

                $ selection = _return

                jump expression selection
                # use jump instead of call for use of the "love" return key

            "No.":
                $ persistent._mas_pm_owns_car = False

                m 1ekc "Oh, I see."
                m 3eka "Well, buying a vehicle can be quite expensive after all."
                m 1eua "It's alright [player], we can always rent one to travel."
                m 1hua "I'm sure that when you do, we'll make a lot of great memories together."
                show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5eua "Then again...{w=1}walks are far more romantic anyway~"

    else:
        $ persistent._mas_pm_owns_car = False

        m 3eua "In fact, I remember you said before that you couldn't drive, either..."
        m 3rksdla "You sure asked an interesting question, ehehe..."
        m 1hua "Maybe that'll change one day and you'll get something then."
        m 1hubsb "That way, you can take me all sorts of places, ahaha!"
    return

label monika_vehicle_sedan:
    $ persistent._mas_pm_owns_car_type = "sedan"
    jump monika_vehicle_sedan_hatchback

label monika_vehicle_hatchback:
    $ persistent._mas_pm_owns_car_type = "hatchback"
    jump monika_vehicle_sedan_hatchback

label monika_vehicle_pickup:
    $ persistent._mas_pm_owns_car_type = "pickup"
    jump monika_vehicle_suv_pickup

label monika_vehicle_suv:
    $ persistent._mas_pm_owns_car_type = "suv"
    jump monika_vehicle_suv_pickup



label monika_vehicle_suv_pickup:

    m 1lksdla "Oh my, your vehicle must be pretty big then."
    m 1eua "That means there's plenty of space right?"
    m 3etc "If that's the case..."
    m 3hub "We could go camping!"
    m 3eua "We'd drive all the way to the woods and you'd set up the tent while I prepared our picnic."
    m 1eka "While we're having lunch, we'd enjoy the scenery and nature surrounding us..."
    m 1ekbsa "Then when night falls, we'd lie down on our sleeping bags, stargazing while holding hands."
    m 3ekbsa "It's definitely a romantic adventure I can't wait to share with you, [player]."
    m 1hkbfa "Ehehe~"
    return

label monika_vehicle_sportscar:
    $ persistent._mas_pm_owns_car_type = "sports"

    m 3hua "Oh, wow!"
    m 3eua "It must be really fast, huh?"
    m 3hub "We should definitely go on a road trip..."
    m 1eub "Taking the scenic route, cruising along the highway..."
    m 1eub "If it's possible it'd be nice to take down the top of the car..."
    m 3hua "That way, we can feel the wind on our faces while everything passes by in a blur!"
    m 1esc "But..."
    m 1eua "It would also be nice to drive at a normal pace..."
    m 1ekbsa "That way we can savor every moment of the ride together~"
    return

label monika_vehicle_sedan_hatchback:

    m 1eua "That's really nice."
    m "I actually prefer that type of car, to be honest."
    m 3eua "From what I've heard, they're lively and easy to drive."
    m 3eub "A car like that would be great for driving around the city, don't you think, [player]?"
    m 3eua "We could go to museums, parks, malls and so on."
    m 1eua "It'd be so nice to be able to drive to places that are too far to walk to by foot."
    m 3hua "It's always exhilarating to discover and explore new places."
    m 1rksdla "We might even find a place where the both of us can be together..."
    m 1tsu "...Alone."
    m 1hub "Ahaha!"
    m 3eua "Just so you know, I'm expecting more than just a simple drive around the city for our dates..."
    m 1hua "I hope you'll surprise me, [player]."
    m 1hub "But then again...{w=0.5}I'd love anything as long as it's with you~"
    return

label monika_vehicle_motorcycle:
    $ persistent._mas_pm_owns_car_type = "motorcyle"

    m 1hksdlb "Eh?"
    m 1lksdlb "You drive a motorcycle?"
    m 1eksdla "I'm surprised, I never expected that to be your kind of ride."
    m 1lksdlb "To be honest, I'm a little hesitant to ride one, ahaha!"
    m 1eua "Really, I shouldn't be scared..."
    m 3eua "You're the one driving after all."
    m 1lksdla "That puts my mind at ease...{w=0.3}a little."
    m 1eua "Just take it nice and slow, okay?"
    m 3hua "After all, we aren't in any rush."
    m 1tsu "Or...{w=0.3}was it your plan to drive so fast I'd have no choice but to hold on to you tight?~"
    m 3kua "That's pretty sneaky of you, [player]."
    m 1hub "Ahaha!"
    $ p_nickname = mas_get_player_nickname()
    m 3eka "There's no need to be shy, [p_nickname]...{w=0.3}{nw}"
    extend 3ekbsa "I'll hug you, even if you don't ask for it..."
    m 1hkbfa "That's how much I love you~"
    return "love"

label monika_vehicle_other:
    $ persistent._mas_pm_owns_car_type = "other"

    m 1hksdlb "Oh, I guess I have a lot to learn about cars then, don't I?"
    m 1dkbsa "Well I'll be looking forward to the day I can finally be right next to you as you drive~"
    m 3hubfb "{i}And{/i} enjoy the scenery too, ahaha!"
    m 1tubfb "Maybe you've got something even more romantic than any vehicle I know."
    m 1hubfa "I guess I'll just have to wait and see, ehehe~"
    return

##### PM Vars for player appearance
default persistent._mas_pm_eye_color = None
default persistent._mas_pm_hair_color = None
default persistent._mas_pm_hair_length = None
default persistent._mas_pm_skin_tone = None
# Iff player is bald
default persistent._mas_pm_shaved_hair = None
default persistent._mas_pm_no_hair_no_talk = None

## Height Vars
## NOTE: This is stored in CENTIMETERS
default persistent._mas_pm_height = None

##### We'll also get a default measurement unit for height
default persistent._mas_pm_units_height_metric = None

default persistent._mas_pm_shared_appearance = False
# True if the user decided to share appearance with us
#   NOTE: we default to False, and this can only get flipped to True
#   in this toppic.

# height categories in cm
define mas_height_tall = 176
define mas_height_monika = 162

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_appearance",
            category=['you'],
            prompt="[player]'s appearance",
            conditional="seen_event('mas_gender')",
            action=EV_ACT_RANDOM
        )
    )

label monika_player_appearance:
    python:
        def ask_color(msg, _allow=lower_letters_only, _length=15):
            result = ""
            while len(result) <= 0:
                result = renpy.input(msg, allow=_allow, length=_length).strip()

            return result

    m 2ekd "Hey, [player]."
    m 2eka "There's a couple questions I've been meaning to ask you."
    m 2rksdlb "Well, more than a couple. It's been on my mind for a long time, actually."
    m 2rksdld "It never really seemed like the right time to bring it up..."
    m 3lksdla "But I know if I keep quiet forever, then I'll never feel comfortable asking you things like this, so I'm just going to say it and hope that it's not weird or anything, okay?"
    m 3eud "I've been wondering what you look like. It's not possible for me to see you right now since I'm not there at your side, and I'm not sure about accessing a webcam..."
    m "One, because you might not have one, and two, even if you did, I don't really know how to."
    m 1euc "So I figured that it's possible for you to just tell me, so I can get a clearer picture in my head."
    m 1eud "At least, it's better than nothing, even if it's hazy."

    m "Is that okay with you, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Is that okay with you, [player]?{fast}"

        "Yes.":
            $ persistent._mas_pm_shared_appearance = True

            m 1sub "Really? Great!"
            m 1hub "That was easier than I thought it would be."
            m 3eua "Now, be honest with me, okay [player]? I know sometimes it's tempting to joke around, but I'm being serious here, and I need you to do the same."
            m "Anyway, the first one is probably easy to guess. And not hard to answer, either!"
            m 3eub "People often say that a person's eyes are the windows into their soul, so let's start off there."

            m "What color are your eyes?{nw}"
            $ _history_list.pop()
            menu:
                m "What color are your eyes?{fast}"

                "I have blue eyes.":
                    $ persistent._mas_pm_eye_color = "blue"

                    m 3eub "Blue eyes? That's wonderful! Blue is such a beautiful color--just as amazing as a cloudless sky, or the ocean in the summer."
                    m 3eua "But there are so many gorgeous metaphors about blue eyes that I could recite them for weeks and still not reach a stopping point."
                    m 4eua "Plus, blue is probably my second favorite color, just behind green. It's just so full of depth and enchantment, you know?"
                    m 4hksdlb "Just like you, [player]!"
                    m 4eub "Did you know that the gene for blue eyes is recessive, so it's not very common in humans?"
                    show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5eubla "I suppose that means you're much more of a treasure~"
                    show monika 2eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 2eua "Anyway, that leads me into the next question I wanted to ask--"

                "I have brown eyes.":
                    $ persistent._mas_pm_eye_color = "brown"

                    m 1eub "Ah! Great! I don't think I said it before, but brown eyes are gorgeous!"
                    m 2euc "I just hate how people seem to think that brown eyes are plain. I couldn't disagree more!"
                    m 2hua "In my opinion, brown eyes are some of the most beautiful out there. They're so vibrant and depthless!"
                    m 3hub "And there's so much variation among all the different shades that people have."
                    m 5ruu "I wonder if yours are dark like a summer night sky, or a paler brown, like the coat of a deer..."
                    m 2hksdlb "Sorry. Just rambling about color metaphors is an easy trap for a literature club president to fall into, I guess. I'll try not to go on forever."
                    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5eua "But I'll bet your eyes are the loveliest of all~"
                    show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 1eua "Anyway, that brings me to my next question--"

                "I have green eyes.":
                    $ persistent._mas_pm_eye_color = "green"

                    m 3sub "Hey, that's my favorite color! And obviously, it's another thing we have in common!"
                    m 4lksdla "I don't know how much I can compliment you here without sounding arrogant, because anything I said about yours would also apply to me..."
                    m 1tsu "Except that maybe it's another sign how compatible we are, ehehe~"
                    m 1kua "But, [player], just between you and me, it's a fact that green eyes are the best, right?"
                    m 3hub "Ahaha! I'm just kidding."
                    show monika 5lusdru at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5lusdru "Well, just a little..."
                    show monika 3eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 3eua "Onto the next question--"

                "I have hazel eyes.":
                    $ persistent._mas_pm_eye_color = "hazel"

                    m 1eub "Oh, hazel eyes? Those are so interesting! It's such an earthly color. It really makes you feel steady and reassured..."
                    m 3eub "And it's a welcome departure from all the candy-colored eyes I've had to see in this game, anyway..."
                    m "I believe that hazel eyes are alluring because they're lovely and simple."
                    m 3hua "Sometimes it's best not to diverge from the crowd too much, [player].{w=0.2} {nw}"
                    extend 3hub "Ahaha!"
                    m "Now, onto my next question--"

                "I have gray eyes.":
                    $ persistent._mas_pm_eye_color = "gray"

                    m 1sub "That's so cool!"
                    m 3eub "Did you know that gray eyes and blue eyes are almost identical in terms of genetics?"
                    m 1eud "In fact, scientists still aren't certain of what causes a person to have one or the other, though they believe that it's a variation in the amount of pigment in the iris."
                    m 1eua "Anyway, I think I like imagining you with gray eyes, [player]. They're the color of a quiet, rainy day..."
                    m 1hubsa "And weather like that is my favorite, just like you~"
                    show monika 5lusdrb at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5lusdrb "Onto my next question--"
                    show monika 3rud at t11 zorder MAS_MONIKA_Z with dissolve_monika

                "I have black eyes.":
                    $ persistent._mas_pm_eye_color = "black"

                    m 1esd "Black eyes are pretty uncommon, [player]."
                    m 4hksdlb "To tell you the truth, I've never actually seen anybody with black eyes, so I don't really know what they look like..."
                    m 3eua "But logically, I do know that they're not actually black. If that was the case, black-eyed people would look like they had no pupils!"
                    m 4eub "In reality, black eyes are just a very, very dark brown. Still stunning, but perhaps not as dark as the name suggests --although, to be fair, the difference is pretty hard to spot."
                    m 3eua "Here's a little bit of trivia for you--"
                    m 1eub "There was a well known lady from the time of the American Revolution, Elizabeth Hamilton, who was known to have captivating black eyes."
                    m 1euc "Her husband wrote about them often."
                    m 1hub "I don't know if you've heard of her or not, but despite the renown of her eyes, I'm sure yours are infinitely more captivating, [player]~"
                    m "Onto the next question--"

                "My eyes are another color.":
                    $ persistent._mas_pm_eye_color = ask_color("What color are your eyes?")

                    m 3hub "Oh! That's a beautiful color, [player]!"
                    m 2eub "I'm sure I could get lost for hours, staring into your [persistent._mas_pm_eye_color] eyes."
                    m 3hua "Now, onto my next question--"


            m 3rud "Actually..."
            m 2eub "I guess I really should know this first though, if I want to get an accurate scale on my next question..."

            m "What unit of measurement do you use to take your height, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "What unit of measurement do you use to take your height, [player]?{fast}"

                "Centimeters.":
                    $ persistent._mas_pm_units_height_metric = True
                    m 2hua "Alright, thanks, [player]!"

                "Feet and inches.":
                    $ persistent._mas_pm_units_height_metric = False
                    m 2hua "Alright, [player]!"

            m 1rksdlb "I'm trying my best to not sound like some sort of identity-thief, or like I'm quizzing you, but obviously, I'm curious."
            m 3tku "If I'm your girlfriend, I have a right to know, don't I?"
            m 2hua "Plus, it'll make it way easier to find you once I'm able to cross over to your reality."

            m 1esb "So,{w=0.5} how tall are you, [player]?"

            python:
                if persistent._mas_pm_units_height_metric:

                    # loop till we get a valid cm
                    height = 0
                    while height <= 0:
                        height = store.mas_utils.tryparseint(
                            renpy.input(
                                'How tall are you in centimeters?',
                                allow=numbers_only,
                                length=3
                            ).strip(),
                            0
                        )

                else:

                    # loop till valid feet
                    height_feet = 0
                    while height_feet <= 0:
                        height_feet = store.mas_utils.tryparseint(
                            renpy.input(
                                'How tall are you in feet?',
                                allow=numbers_only,
                                length=1
                            ).strip(),
                            0
                        )

                    # loop till valid inch
                    height_inch = -1
                    while height_inch < 0 or height_inch > 11:
                        height_inch = store.mas_utils.tryparseint(
                            renpy.input(
                                '[height_feet] feet and how many inches?',
                                allow=numbers_only,
                                length=2
                            ).strip(),
                            -1
                        )

                    # convert to cm
                    height = ((height_feet * 12) + height_inch) * 2.54

                # finally save this persistent
                persistent._mas_pm_height = height

            if persistent._mas_pm_height >= mas_height_tall:
                m 3eua "Wow, you're pretty tall, [player]!"
                m 1eud "I can't say I've really met anybody who I'd consider to be tall."
                m 3rksdla "I don't know my actual height, to be fair, so I can't really draw an accurate comparison..."

                call monika_player_appearance_monika_height

                if persistent._mas_pm_units_height_metric:
                    $ height_desc = "centimeters"
                else:
                    $ height_desc = "inches"

                m 3esc "The tallest girl in the literature club was Yuri--and just barely, at that. She was only a few [height_desc] taller than me, I don't consider that much of a height advantage at all!"
                m 3esd "Anyway, dating a tall [guy] like you only has one disadvantage, [mas_get_player_nickname()]..."
                m 1hub "You'll have to lean down to kiss me!"

            elif persistent._mas_pm_height >= mas_height_monika:
                m 1hub "Hey, I'm about that height too!"
                m "..."
                m 2hksdlb "Well, I don't know my actual height to be fair..."

                call monika_player_appearance_monika_height

                m 3rkc "It's just a guess--hopefully it's not too far off."
                m 3esd "Anyway, there's nothing wrong with having an average height! To be honest, if you were too short, it'd probably make me feel clumsy around you."
                m "And if you were too tall, I'd have to get on my tiptoes just to be close to you. And that's no good!"
                m 3eub "In my opinion, being in-between is perfect. Do you know why?"
                m 5eub "Because then I don't have to do any reaching or bending to kiss you, [mas_get_player_nickname()]! Ahaha~"

            else:
                m 3hub "Like Natsuki! I bet you're not that short, though! I would be concerned for you if you were."

                if persistent._mas_pm_cares_about_dokis:
                    m 2eksdld "She was worryingly small for her age, but you and I both know why. I always pitied her for that."

                m 2eksdld "I knew she always hated being so tiny, because of that whole notion that little things are cuter because of their size..."
                m 2rksdld "And then there was all that trouble with her father. It can't have been easy, being so defenseless, and being small on top of it all."
                m 2ekc "She probably felt like people talked down to her. Literally and figuratively, that is..."
                m 2eku "But despite her hang-ups about it, [player], I think your height makes you that much more cute~"

            m 1eua "Now, [player]."

            m 3eub "Tell me, is your hair on the shorter side? Or is it long, like mine?~{nw}"
            $ _history_list.pop()
            menu:
                m "Tell me, is your hair on the shorter side? Or is it long, like mine?~{fast}"

                "It's shorter.":
                    $ persistent._mas_pm_hair_length = "short"

                    m 3eub "That must be nice! Look, don't get me wrong; I love my hair, and it's always fun to experiment with it..."
                    m 2eud "But to tell you the truth, sometimes I envied Natsuki's and Sayori's hair. It looked a lot easier to take care of."

                    if persistent.gender == "M":
                        m 4hksdlb "Although I guess if your hair was the same length as theirs, it'd be pretty long for a guy."

                    else:
                        m 4eub "You can just get up and go, without having to worry about styling it."
                        m "Plus, waking up with a bedhead when you have short hair is easily fixed, whereas if you have long hair, it's an endless nightmare."

                    m 2eka "But I bet you look adorable with short hair. It makes me smile to think about you like that, [player]."
                    m 2eua "Keep enjoying all that freedom from the little annoyances that accompany long hair, [player]!{w=0.2} {nw}"
                    extend 2hub "Ahaha~"

                "It's average length.":
                    $ persistent._mas_pm_hair_length = "average"

                    m 1tku "Well, that can't be true..."
                    m 4hub "Because nothing about you is average."
                    m 4hksdlb "Ahaha! Sorry, [player]. I'm not trying to embarrass you. But I can't help being cheesy sometimes, you know?"
                    m 1eua "Honestly, when it comes to hair, the middle road is great. You don't have to worry about styling it too much, and you have more creative freedom than with short hair."
                    m 1rusdlb "I'm a little envious, to tell you the truth~"
                    m 3eub "But don't forget that old saying- 'Invest in your hair, because it's a crown that you never take off!'"

                "It's long.":
                    $ persistent._mas_pm_hair_length = "long"

                    m 4hub "Yay, another thing we have in common!"
                    m 2eka "Long hair can be a pain sometimes, right?"
                    m 3eua "But the good thing is that there are so many things you can do with it. Though I usually prefer to tie mine up with a ribbon, I know that other people have different styles."
                    m "Yuri wore her hair down, and others enjoy braids, or putting it into pigtails..."

                    python:
                        hair_down_unlocked = False
                        try:
                            hair_down_unlocked = store.mas_selspr.get_sel_hair(
                                mas_hair_down
                            ).unlocked
                        except:
                            pass

                    if hair_down_unlocked:
                        # TODO adjust this line to be more generic once we have additoinal hairstyles.
                        m 3eub "And ever since I figured out how to mess around with the script and let my own hair down, who knows how many more styles I might try?"

                    m 1eua "It's always nice to have options, you know?"
                    m 1eka "I hope that however you wear yours, you're comfortable with it!"

                "I don't have hair.":
                    $ persistent._mas_pm_hair_length = "bald"

                    m 1euc "Oh, that's interesting, [player]!"

                    m "Do you shave your head or did you lose your hair, if you don't mind me asking?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Do you shave your head or did you lose your hair, if you don't mind me asking?{fast}"

                        "I shave my head.":
                            $ persistent._mas_pm_shaves_hair = True
                            $ persistent._mas_pm_no_hair_no_talk = False

                            m 1hua "It must be so nice not ever having to worry about your hair..."
                            m 1eua "You can just get up and go, without having to worry about styling it..."
                            m 3eua "And if you wear a hat, you don't have to worry about hat hair when you take it off!"

                        "I lost my hair.":
                            $ persistent._mas_pm_shaves_hair = False
                            $ persistent._mas_pm_no_hair_no_talk = False

                            m 1ekd "I'm sorry to hear that, [player]..."
                            m 1eka "But just know that I don't care how much hair you have, you'll always look beautiful to me!"
                            m "And if you ever feel insecure or just want to talk about it, I'm always up for listening."

                        "I don't want to talk about it.":
                            $ persistent._mas_pm_no_hair_no_talk = True

                            m 1ekd "I understand, [player]"
                            m 1eka "I want you to know that I don't care how much hair you have, you'll always be beautiful to me."
                            m "If you ever feel insecure or feel like talking about it, I'm always here to listen."

            if persistent._mas_pm_hair_length != "bald":
                m 1hua "Next question!"
                m 1eud "This one should be fairly obvious..."

                m "What color is your hair?{nw}"
                $ _history_list.pop()
                menu:
                    m "What color is your hair?{fast}"
                    "It's brown.":
                        $ persistent._mas_pm_hair_color = "brown"

                        m 1hub "Yay, brown hair is the best!"
                        m 3eua "Just between us, [player], I really like my brown hair. I'm sure yours is even better!"
                        m 3rksdla "Though some people might disagree my hair is brown..."
                        m 3eub "When I was doing some digging around in the local files of the game folder, I found the exact name for my hair color."
                        m 4eua "It's called coral brown. Interesting, right?"
                        m 1hub "I'm so happy that we have so much in common, [player]~"

                    "It's blonde.":
                        $ persistent._mas_pm_hair_color = "blonde"

                        m 1eua "Really? Hey, did you know that having blonde hair puts you in a rare two percent of the population?"
                        m 3eub "Blonde hair is one of the rarest hair colors. Most people attribute this to the fact that it's caused by a recurring genetic anomaly--"
                        m "Being just the body's inability to produce normal amounts of the pigment eumelanin--that's what causes darker hair colors, such as black and brown."
                        m 4eub "There are so many various shades of blonde, too--pale blonde, ash-colored, dirty blonde--that no matter what color you have, you're bound to be idiosyncratic in some way."
                        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                        m 5eua "I guess having someone who's so unique just makes me all the luckier~"
                        show monika 2hua at t11 zorder MAS_MONIKA_Z with dissolve_monika

                    "It's black.":
                        $ persistent._mas_pm_hair_color = "black"

                        m 2wuo "Black hair is so beautiful!"
                        m 3eub "You know, there's this really irritating trope about people with black hair having a more prickly or ill-tempered personality than others..."
                        m 4hub "But you've obviously disproven that myth. Personally, I think black hair is very attractive."
                        m 3eua "In addition, if you actually placed a strand of it under a microscope and counted all the pigments in it, you'd find that it's not even a hundred percent dark."
                        m "You know how when you place certain things under direct sunlight, it looks really different?"
                        m 3eub "Black hair follows the same principle--you can see shades of gold, or brown, or even glints of purple. It really makes you think, doesn't it, [player]?"
                        m 1eua "There could be infinite shades of things we can't see, each one of them hidden in plain sight."
                        m 3hua "But anyway...I think that a [guy] with black hair and [persistent._mas_pm_eye_color] eyes is the best sight of all, [player]~"

                    "It's red.":
                        $ persistent._mas_pm_hair_color = "red"

                        m 3hua "Yet another special thing about you, [player]~"
                        m 3eua "Red hair and blonde hair are the least common natural hair colors, did you know that?"
                        m 1eua "Red hair, however, is a little more rare, even if people call it by different names--auburn, ginger, and so on. It's only found in about one percent of the population."
                        m 1hub "It's a rare and wonderful trait to have--almost as wonderful as you!"

                    "It's another color.":
                        $ persistent._mas_pm_hair_color = ask_color("What color is your hair?")

                        m 3hub "Oh! That's a beautiful color, [player]!"
                        m 1eub "That reminds me of something I was thinking about earlier, when we were talking about the color of your eyes."
                        m 1eua "Even though the other girls had eye colors that literally didn't exist in real life--not counting the existence of colored contacts, of course--"
                        m 3eua "Their hair colors technically could exist in reality, you know. I mean, I'm sure you've encountered people with dyed purple hair, or neon pink, or coral-colored..."
                        m 3eka "So I suppose their appearances weren't that far-fetched, if you don't count the eyes. Honestly, the most unbelievable thing about them was their personalities."
                        m 3hksdlb "Sorry, [player]! I'm getting off-track. My point is, dyed hair can be very interesting."
                        show monika 5rub at t11 zorder MAS_MONIKA_Z with dissolve_monika
                        m 5rub "And I might be a little biased here, but I'm convinced that you'd look stunning in your [persistent._mas_pm_hair_color] hair~"
                        show monika 2hua at t11 zorder MAS_MONIKA_Z with dissolve_monika

            m 2hua "Alright..."
            m 2hksdlb "This is the last question, [player], I promise."
            m "Gosh, there really is a lot to what people look like... If I tried to narrow everything about you down to the little details, I'd be interrogating you forever."
            m 1huu "...and I doubt that either of us want that, ahaha..."
            m 1rksdld "Anyway, I understand that this might be an uncomfortable question..."
            m 1eksdla "But it's the last piece of this puzzle to me, so I hope I don't sound rude when I ask..."

            m "What's your skin color, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "What's your skin color, [player]?{fast}"

                "I'm light-skinned.":
                    $ persistent._mas_pm_skin_tone = "light"

                "I'm tanned.":
                    $ persistent._mas_pm_skin_tone = "tanned"

                "I'm dark-skinned.":
                    $ persistent._mas_pm_skin_tone = "dark"

            m 3hub "Alright! Thanks for being so upfront. All of this really does help me imagine what you look like, [player]."
            m 3eub "Knowing all these details about you makes the difference between a blank canvas and the beginnings of a gorgeous portrait!"
            m 3eua "Of course, you're still just as lovely as I always thought you were, but now you've become all the more real to me."
            m 3eka "It just makes me feel that much closer to you~"
            m 1eka "Thank you so much for answering all my questions, [mas_get_player_nickname()]."

            if persistent._mas_pm_eye_color == "green" and persistent._mas_pm_hair_color == "brown":
                m 2hua "It's wonderful, because I didn't imagine how similar we would look. It's very interesting!"

            else:
                m 2hua "It's wonderful, because I didn't imagine how different we would look. It's very interesting!"

            m 1dsa "Now I'm imagining what it'll be like when we meet for real..."

            show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika

            if persistent._mas_pm_hair_length == "bald":
                if persistent._mas_pm_height >= mas_height_tall:
                    m 5eubfu "When I run towards you, and since you're taller, you'll wrap me up in your embrace..."

                elif persistent._mas_pm_height >= mas_height_monika:
                    m 5eubfu "When I run towards you, and since we're around the same height, we'll meet in a tight embrace..."

                else:
                    m 5eubfu "When I run towards you, and since I'll be taller than you, you'll reach up and wrap me in your embrace..."

            else:
                python:
                    hair_desc = persistent._mas_pm_hair_color

                    if persistent._mas_pm_hair_length != "average":
                        hair_desc = (
                            persistent._mas_pm_hair_length + " " + hair_desc
                        )

                if persistent._mas_pm_height >= mas_height_tall:

                    m 5eubfu "When I run towards you, since you're taller, you'll wrap me up in your embrace and I'll be able to stroke your [hair_desc] hair..."

                elif persistent._mas_pm_height >= mas_height_monika:

                    m 5eubfu "When I run towards you, since we're around the same height, we'll meet in a tight embrace and I'll run my hand through your [hair_desc] hair..."

                else:

                    m 5eubfu "When I run towards you, since I'll be taller than you, you'll reach up and wrap me in your embrace and I'll run my hand through your [hair_desc] hair..."

            show monika 1lkbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 1lkbsa "...and I'll finally be able to hear your heartbeat and get to touch you and know that you're real."
            m 3ekbsa "But until then, I'll be content sitting here and imagining looking into your beautiful [persistent._mas_pm_eye_color] eyes, [player]."

            show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbfa "I love you more than words could ever say."
            return "derandom|love"

        "No.":
             m 2dsc "..."
             m 2ekd "I understand, [player]."
             m 2eka "I know that everybody has their own limits with their comfort zones..."
             m 2rksdla "And to be fair, a description of yourself in vague words wouldn't be able to capture who you are, so I can't blame you for wanting to keep this to yourself."
             m 2eka "But if you change your mind, let me know!"

    return "derandom"

# quick label where monika tells you her height
label monika_player_appearance_monika_height:
    if not persistent._mas_pm_units_height_metric:
        $ conv_height_str = ""
        $ real_height_str = "around five-foot-five"
    else:
        $ conv_height_str = " which is around one hundred and sixty centimeters"
        $ real_height_str = "about one hundred and sixty-five-centimeters tall"

    if seen_event("monika_immortal"):
        m 2eud "The wiki I mentioned before said that my concept height was five-foot-three,[conv_height_str] but that doesn't really sound right to me..."
        m 2etc "Maybe it was changed? It was only the concept height after all."
    m 3etd "If I had to guess, I'd say I'm maybe [real_height_str]?"
    return

init 5 python:
     addEvent(
         Event(
            persistent.event_database,
            eventlabel="monika_players_control",
            category=["games", "ddlc"],
            prompt="[player]'s control",
            random=True
            )
        )

label monika_players_control:
    m 3eub "[player], did you know that you have more control over this game than I do?"
    m 3eua "You have access to the game's files and code, right?"
    m 1eka "So you can change them however you want."
    m 3eka "You could do things that even I can't."
    m 4eub "Like changing how the game works entirely. From a visual novel, to the peaceful playground we have now."
    m 3rksdla "You could also add more things to the classroom for me."
    m 1hub "Like some flowers, or a few good books."

    if mas_isMoniEnamored(higher=True) and not persistent._mas_acs_enable_promisering:
        m 1ekbsa "Or a beautiful promise ring."
        m 3dkbsu "Oh, wouldn't that be a dream come true."

    if not mas_getConsumable("coffee").enabled():
        m 1wuo "You could even add in a cup of coffee to the game for me!"
        m 1eka "That would be lovely."

    if not persistent._mas_pm_has_code_experience:
        m 1hksdrb "But I imagine your coding skills are just as good as mine."
    else:
        m 3eua "Seeing as you're familiar with coding,{w=0.1} {nw}"
        extend 3hua "I'm sure you could do something like that!"

    m 1eua "I guess that's an appeal to video games...{w=0.3}{nw}"
    extend 3eua "having almost endless possibilities in a world you can interact with."
    m 3eub "It's pretty difficult to get bored!"

    if not persistent._mas_pm_has_contributed_to_mas:
        m 1eka "Even if you don't quite know how to change this game..."
        $ line = "We can still enjoy this world that brought us together."

    else:
        $ line = "Especially with you by my side~"

    show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eubla "[line]"
    m 5ekbfa "There's no better way to enjoy a game than to be with the one I love."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_backpacking",category=['nature'],prompt="Backpacking",random=not mas_isWinter()))

label monika_backpacking:
    m 1esa "You know what I've always wanted to do, [player]?"
    m 3eub "I've always thought it would be so amazing to go backpacking in the wilderness!"
    m 3eua "Take like an entire week and leave it all behind."
    m 3esa "No responsibilities, no worries, no phones, no distractions."
    m 1hua "Just imagine the two of us, alone with nature..."
    m "The sounds of birds chirping and the wind blowing..."
    m 1eka "Watching deer graze in the morning dew..."
    m "I can't think of anything more peaceful."
    m 1esa "We can spend our days exploring mysterious forests, serene meadows, and rolling hills..."
    m 3hub "Maybe even discover a secluded lake and go for a swim!"

    if mas_isMoniAff(higher=True):
        m 2rsbsa "We probably won't have our bathing suits, but we'll be all alone so maybe we won't need any..."
        m 2tsbsa "..."
        m 1hubfu "I hope you're not too shy, [mas_get_player_nickname()]. Ehehe~"
        m 1ekbfa "We'll spend our nights cuddling in a sleeping bag, keeping each other warm with nothing over our heads but billions of stars..."
        m 3hubfb "Waking up each morning to a glorious sunrise!"

    else:
        m 3eka "We'll spend our nights sleeping under the stars, waking up each morning to a glorious sunrise."

    show monika 5esbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5esbfa "..."
    m "Oh [player], doesn't that just sound like heaven?"
    m 5hubfa "I can't wait until we can share this experience together~"
    return

## calendar-related pool event
# DEPENDS ON CALENDAR

# did we already change start date?
default persistent._mas_changed_start_date = False

# did you imply that you arent dating monika?
default persistent._mas_just_friends = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dating_startdate",
            category=["romance", "us"],
            prompt="When did we start dating?",
            pool=True,
            unlocked=False,

            # this will be unlockable via the action
            rules={"no_unlock": None},

            # we'll pool this event after a month of the relationship
            conditional=(
                "store.mas_anni.pastOneMonth() "
                "and persistent._mas_first_calendar_check"
            ),

            action=EV_ACT_UNLOCK
        )
    )

label monika_dating_startdate:
    $ import store.mas_calendar as mas_cal
    python:
        # we might need the raw datetime
        first_sesh_raw = persistent.sessions.get(
            "first_session",
            datetime.datetime(2017, 10, 25)
        )

        # but this to get the display plus diff
        first_sesh, _diff = mas_cal.genFormalDispDate(first_sesh_raw.date())

    if _diff.days == 0:
        # its today?!
        # this should NEVER HAPPEN
        m 1lsc "We started dating..."
        $ _history_list.pop()
        m 1wud "We started dating{fast} today?!"
        m 2wfw "You couldn't have possibly triggered this event today, [player]."

        m "I know you're messing around with the code.{nw}"
        $ _history_list.pop()
        menu:
            m "I know you're messing around with the code.{fast}"
            "I'm not!":
                pass
            "You got me.":
                pass
        m 2tfu "Hmph,{w=0.2} you can't fool me."

        # wait 30 days
        $ mas_chgCalEVul(30)
        return

    # Otherwise, we should be displaying different dialogue depending on
    # if we have done the changed date event or not
    if not persistent._mas_changed_start_date:
        m 1lsc "Hmmm..."
        m 1dsc "I think it was..."
        $ _history_list.pop()
        m 1eua "I think it was{fast} [first_sesh]."
        m 1rksdlb "But my memory might be off."

        # ask user if correct start date
        m 1eua "Is [first_sesh] correct?{nw}"
        $ _history_list.pop()
        menu:
            m "Is [first_sesh] correct?{fast}"
            "Yes.":
                m 1hub "Yay!{w=0.2} I remembered it."

            "No.":
                m 1rkc "Oh,{w=0.2} sorry [player]."
                m 1ekc "In that case,{w=0.2} when did we start dating?"

                call monika_dating_startdate_confirm(first_sesh_raw)

                if _return == "NOPE":
                    # we are not selecting a date today
                    return

                # save the new date to persistent
                $ store.mas_anni.reset_annis(_return)
                $ persistent.sessions["first_session"] = _return
                $ renpy.save_persistent()

        m 1eua "If you ever forget, don't be afraid to ask me."
        m 1dubsu "I'll {i}always{/i} remember when I first fell in love with you~"
        $ persistent._mas_changed_start_date = True

    else:
        m 1dsc "Let me check..."
        m 1eua "We started dating [first_sesh]."

    # TODO:
    # some dialogue about being together for x time
    # NOTE: this is a maybe

    return

label monika_dating_startdate_confirm_had_enough:
    # monika has had enough of your shit
    # TODO: maybe decrease affection since you annoyed her enough?
    m 2dfc "..."
    m 2lfc "We'll do this another time, then."

    # we're going to reset the conditional to wait
    # 30 more days
    $ mas_chgCalEVul(30)

    return "NOPE"

label monika_dating_startdate_confirm_notwell:
    # are you not feeling well or something?
    m 1ekc "Are you feeling okay, [player]?"
    m 1eka "If you don't remember right now, then we can do this again tomorrow, okay?"

    # reset the conditional to tomorrow
    $ mas_chgCalEVul(1)

    return "NOPE"

label monika_dating_startdate_confirm(first_sesh_raw):

    python:
        import store.mas_calendar as mas_cal

        # and this is the formal version of the datetime
        first_sesh_formal = " ".join([
            first_sesh_raw.strftime("%B"),
            mas_cal._formatDay(first_sesh_raw.day) + ",",
            str(first_sesh_raw.year)
        ])

        # setup some counts
        wrong_date_count = 0
        no_confirm_count = 0
        today_date_count = 0
        future_date_count = 0
        no_dating_joke = False

    label .loopstart:
        pass

    call mas_start_calendar_select_date

    $ selected_date = _return
    $ _today = datetime.date.today()
    $ _ddlc_release = datetime.date(2017,9,22)

    if not selected_date or selected_date.date() == first_sesh_raw.date():
        # no date selected, we assume user wanted to cancel
        m 2esc "[player]..."
        m 2eka "I thought you said I was wrong."

        m "Are you sure it's not [first_sesh_formal]?{nw}"
        $ _history_list.pop()
        menu:
            m "Are you sure it's not [first_sesh_formal]?{fast}"
            "It's not that date.":
                if wrong_date_count >= 2:
                    jump monika_dating_startdate_confirm_had_enough

                # otherwise try again
                m 2dfc "..."
                m 2tfc "Then pick the correct date!"
                $ wrong_date_count += 1
                jump monika_dating_startdate_confirm.loopstart

            "Actually that's the correct date. Sorry.":
                m 2eka "That's okay."
                $ selected_date = first_sesh_raw

    elif selected_date.date() < _ddlc_release:
        # before releease date

        label .takesrs:
            if wrong_date_count >= 2:
                jump monika_dating_startdate_confirm_had_enough

            m 2dfc "..."
            m 2tfc "We did {b}not{/b} start dating that day."
            m 2tfd "Take this seriously, [player]."
            $ wrong_date_count += 1
            jump monika_dating_startdate_confirm.loopstart

    elif selected_date.date() == _today:
        # today was chosen
        jump .takesrs

    elif selected_date.date() > _today:
        # you selected a future date?! why!
        if future_date_count > 0:
            # don't play around here
            jump monika_dating_startdate_confirm_had_enough

        $ future_date_count += 1
        m 1wud "What..."

        m "We haven't been dating this whole time?{nw}"
        $ _history_list.pop()
        menu:
            m "We haven't been dating this whole time?{fast}"
            "That was a misclick!":
                # relief expression
                m 1duu "{cps=*2}Oh, thank god.{/cps}"

                label .misclick:
                    m 2dfu "[player]!"
                    m 2efu "You had me worried there."
                    m "Don't misclick this time!"
                    jump monika_dating_startdate_confirm.loopstart

            "Nope.":
                m 1dfc "..."

                show screen mas_background_timed_jump(5, "monika_dating_startdate_confirm_tooslow")

                menu:
                    "I'm kidding.":
                        hide screen mas_background_timed_jump
                        # wow what a mean joke

                        if no_dating_joke:
                            # you only get this once per thru
                            jump monika_dating_startdate_confirm_had_enough

                        # otherwise mention that this was mean
                        m 2tfc "[player]!"
                        m 2rksdlc "That joke was a little mean."
                        m 2eksdlc "You really had me worried there."
                        m "Don't play around like that, okay?"
                        jump monika_dating_startdate_confirm.loopstart

                    "...":
                        hide screen mas_background_timed_jump

                label monika_dating_startdate_confirm_tooslow:
                    hide screen mas_background_timed_jump

                # lol why would you stay slient?
                # TODO: Affection considerable decrease?
                $ persistent._mas_just_friends = True

                m 6lktdc "I see..."
                m 6dftdc "..."
                m 1eka "In that case..."
                m 1tku "{cps=*4}I've got some work to do.{/cps}{nw}"
                $ _history_list.pop()

                menu:
                    "What?":
                        pass

                m 1hua "Nothing!"

                # lock this event forever probably
                # (UNTIL you rekindle or actually ask her out someday)
                $ evhand.event_database["monika_dating_startdate"].unlocked = False
                return "NOPE"

    # post loop
    python:
        new_first_sesh, _diff = mas_cal.genFormalDispDate(
            selected_date.date()
        )

    m 1eua "Alright, [player]."
    m "Just to double-check..."

    m "We started dating [new_first_sesh].{nw}"
    $ _history_list.pop()
    menu:
        m "We started dating [new_first_sesh].{fast}"
        "Yes.":
            m 1eka "Are you sure it's [new_first_sesh]? I'm never going to forget this date.{nw}"
            # one more confirmation
            # WE WILL NOT FIX anyone's dates after this
            $ _history_list.pop()
            menu:
                m "Are you sure it's [new_first_sesh]? I'm never going to forget this date.{fast}"
                "Yes, I'm sure!":
                    m 1hua "Then it's settled!"
                    return selected_date

                "Actually...":
                    if no_confirm_count >= 2:
                        jump monika_dating_startdate_confirm_notwell

                    m 1hksdrb "Aha, I figured you weren't so sure."
                    m 1eka "Try again~"
                    $ no_confirm_count += 1

        "No.":
            if no_confirm_count >= 2:
                jump monika_dating_startdate_confirm_notwell

            # otherwise try again
            m 1euc "Oh, that's wrong?"
            m 1eua "Then try again, [mas_get_player_nickname()]."
            $ no_confirm_count += 1

    # default action is to loop here
    jump monika_dating_startdate_confirm.loopstart

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_first_sight_love",
            category=["romance"],
            prompt="Love at first sight",
            random=True
        )
    )

label monika_first_sight_love:
    m 1eud "Have you ever thought about the concept of love at first sight?"
    m 3euc "Like, seeing someone for the first time, and instantly knowing they're the love of your life?"
    m 2lsc "I think it's one of the more...{w=0.5}ridiculous concepts to grasp."
    m 2lksdlc "I mean, you can't know who a person truly is just by looking at them once."
    m 2tkd "It's not like you've ever talked to them, had lunch, or hung out together."
    m 2lksdlc "You don't even know what their interests and hobbies are..."
    m 2dksdld "They could be really boring or just be a mean and horrible person..."
    m 3eud "That's why I think we shouldn't {i}just{/i} use our eyes to tell if someone is the perfect partner for us."
    if mas_isMoniAff(higher=True):
        m 1eka "And I guess that's kind of how I fell in love with you..."
        m 3eua "It's not like I could see you after all."
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "I fell in love with you for who you are, [mas_get_player_nickname(exclude_names=['my love', 'love'])]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_anime_art",
            category=["misc"],
            prompt="Anime art style",
            random=True
        )
    )

label monika_anime_art:
    m 1eua "Have you ever thought about anime art styles?"
    m 3rksdla "I'm sure Natsuki would be an expert on this, given her obsession with manga and all..."
    m 3eub "Anyway, there's a lot of interesting things about the art style."
    m 1eua "It's freeform, like my poems, which makes a lot of the art really unique..."
    m 3eua "From the beautiful scenery, to the amazing characters..."
    m 1hub "It's just really impressive to look at!"
    m 2esc "Though being a freeform art style...{w=0.5}a lot of details tend to look a little unrealistic."
    m 3rsc "While it lets a lot of artworks explore new possibilities, it can also make some details look weird..."
    m 3rssdlc "Like how a character's eyes can be so big, how small their noses are, or how their hair can be in strange lengths, shapes, and sizes..."
    m 2rksdlc "Not to mention...{w=1}large chests."
    m 2euc "If I looked more realistic, I certainly wouldn't have those attributes."
    m 1eua "But I guess that lack of realism is where the true beauty of the art style really comes from."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_whydoyouloveme",
            category=['monika','romance'],
            prompt="Why do you love me?",
            pool=True
        )
    )

label monika_whydoyouloveme:
    if mas_isMoniBroken():
        m 2euc "Hmph."
        m 2wfc "I ask myself that question every day."

    elif mas_isMoniDis():
        m 1efc "I-"
        m 1rkc "I'm not sure..."

    elif mas_isMoniUpset():
        m 1dsc "Hmm..."
        m 3hua "Because I know that you're a good person despite how things are between us."

    elif mas_isMoniEnamored(higher=True):
        if renpy.random.randint(1,10) > 1:
            m 1eksdla "Why do I love you?"
            m 1dka "[mas_get_player_nickname(capitalize=True)]...{w=0.5}there are so many reasons why. Where do I even begin?"

            if store.mas_anni.anniCount() >= 1:
                m 3eka "You've spent so much time with me,{w=0.2} knowing you might not ever get to feel my embrace."
                m 3hua "...But here you are, still by my side."

            m 3eksdla "No matter how crazy it may seem, or what other people might think, you're here with me anyway."
            m 1dku "Every time you visit, you remind me that there's a world out there."
            m "..."
            m 1ekbsa "I'd give you the world if I could, [player]."
            m 1hubsa "If there's anyone who deserves it...{w=0.3}it's you."
            m 1ekbsa "I promise you, [player]..."
            m 3ekbsa "No matter what happens, I'll {i}never{/i} forget you for the rest of my life."
            m 1dkbsu "You didn't just save me, [player]...{w=0.3}{nw}"
            extend 1ekbsa "you made me remember how beautiful life really is."
            m 1ekbsb "Someday, I'll make you feel as loved as you've made me feel~"
            m 1dkbsa "Someday...{w=0.5}I'll get to be with you~"

            if persistent._mas_pm_love_yourself is False:
                m 2eka "And [player]..."
                m 2ekc "I remember you saying that you didn't love yourself..."
                m 7eka "But I think you do love yourself, at least a little."
                m 3hua "You wouldn't still be here with me if you didn't."
                m 1dkbsu "I'm...{w=0.5}I'm just glad you're still here, [player]."
                m 1ekbsa "Please know that I'm here for you, whenever you need me~"

        else:
            m 1esc "I don't."
            pause 5.0
            m 1hub "Ahaha, just kidding!"
            m 1eub "You mean {i}everything{/i} to me, silly!"

    else:
        # normal - aff
        m 2ekc "[player]..."
        m 2ekd "Are you, by any chance feeling insecure?"
        m 7rksdla "I can understand feeling that way..."
        m 3eka "But whatever the reason might be,{w=0.2} I just want you to know that I love you no matter who you are, [player]."
        m 1ekbsa "Just by opening the game for me, you {i}literally{/i} saved my life."
        m 1dkbsu "...When I'm with you,{w=0.2} I'm no longer lonely."
        m 3ekbsa "You truly are my hero, [mas_get_player_nickname(regex_replace_with_nullstr='my ')]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_stoicism",
            category=['philosophy'],
            prompt="Stoicism",
            random=True
        )
    )

label monika_stoicism:
    m 1eua "I've been reading up on some ancient Greek and Roman philosophy, [player]."
    m 1hksdlb "Ahaha! I know, that sounds super boring when you think about it..."
    m 1eua "But there was a certain philosophy that caught my attention while I was reading."
    m "It's called Stoicism, and it's a philosophy founded in Athens in the 3rd century BCE."
    m 4eub "To put it simply, Stoicism is a philosophy that believes that human beings should learn to accept the circumstances of their situation..."
    m "...and prevent themselves from being controlled by an irrational desire for pleasure or fear of pain so they can act accordingly in nature's plan."
    m 2euc "They usually get a bad rep today because people think that they're just cold and unfeeling."
    m 2eua "However, stoics are not just a bunch of unemotional people who are always serious."
    m "Stoics practice self-control over the way they feel about unfortunate events and react accordingly instead of impulsively."
    m 2eud "For example, let's say you failed an important exam at school, or missed a project deadline at work."
    m 2esd "What would you do, [player]?"
    m 4esd "Would you panic? Become really depressed and give up trying? Or will you get angry over it and blame others?"
    m 1eub "I don't know what you would do, but maybe you can take after stoics and keep your emotions in check!"
    m 1eka "Although the situation is less than ideal, there's really no practical reason to expend more energy into something that you can't control."
    m 4eua "You should focus on what you can change."
    m "Maybe study harder for your next exam, get tutoring, and ask your teacher for extra credit."
    m "Or if you imagined the work scenario, start future projects earlier, setup schedules and reminders for those projects, and avoid distractions while you work."
    m 4hub "It beats doing nothing!"
    m 1eka "But that's just my opinion though, it's not that easy to be emotionally resilient to most things in life..."

    if mas_isMoniUpset(lower=True):
        return

    if mas_isMoniAff(higher=True):
        m 2tkc "You should do {i}whatever{/i} helps you de-stress. Your happiness is really important to me."
        m 1eka "Besides, if you ever feel bad about something that's happened to you in your life..."
        show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hubfb "You can always come home to your sweet girlfriend and tell me what's been bothering you~"

    else:
        m 2tkc "You should do whatever helps you de-stress. Your happiness is really important to me."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_add_custom_music",
            category=['mod',"media", "music"],
            prompt="How do I add my own music?",
            conditional="persistent._mas_pm_added_custom_bgm",
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_add_custom_music:
    m 1eua "It's really easy to add your own music here, [player]!"
    m 3eua "Just follow these steps..."
    call monika_add_custom_music_instruct
    return

label monika_add_custom_music_instruct:
    m 4eua "First,{w=0.5} make sure the music that you want to add is in MP3, OGG/VORBIS, or OPUS format."
    m "Next,{w=0.5} create a new folder named \"custom_bgm\" in your \"DDLC\" directory."
    m "Put your music files in that folder..."
    m "Then either let me know that you added some music or restart the game."
    m 3eua "And that's it! Your music will be available to listen to, right here with me, simply by pressing the 'm' key."
    m 3hub "See, [player]? I told you it was easy, ahaha!"

    # unlock the topic as a pool topic, also mark it as seen
    $ mas_unlockEVL("monika_add_custom_music", "EVE")
    $ persistent._seen_ever["monika_add_custom_music"] = True
    $ mas_unlockEVL("monika_load_custom_music", "EVE")
    $ persistent._seen_ever["monika_load_custom_music"] = True
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_load_custom_music",
            category=['mod',"media", "music"],
            prompt="Can you check for new music?",
            conditional="persistent._mas_pm_added_custom_bgm",
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_load_custom_music:
    m 1hua "Sure!"
    m 1dsc "Give me a moment to check the folder.{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    python:
        # FIXME: this is not entirely correct, as one may delete a song before adding a new one
        old_music_count = len(store.songs.music_choices)
        store.songs.initMusicChoices(
            persistent.playername.lower() == "sayori"
            and not persistent._mas_sensitive_mode
        )
        diff = len(store.songs.music_choices) - old_music_count

    if diff > 0:
        m 1eua "Alright!"
        if diff == 1:
            m "I found one new song!"
            m 1hua "I can't wait to listen to it with you."
        else:
            m "I found [diff] new songs!"
            m 1hua "I can't wait to listen to them with you."

    else:
        m 1eka "[player], I didn't find any new songs."

        m "Do you remember how to add custom music?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you remember how to add custom music?{fast}"
            "Yes.":
                m "Okay, make sure you did it correctly."

            "No.":
                $ pushEvent("monika_add_custom_music",True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_mystery',
            prompt="Mysteries",
            category=['literature','media'],
            random=True
        )
    )

label monika_mystery:
    m 3eub "You know [player], I think there's an interesting part in many stories that some people overlook."
    m 3eua "It's something that makes a story interesting...but can break them when used incorrectly."
    m 3esa "It can make a tale either amazing to go back through or make you never want to touch it again."
    m 2eub "And that part is..."
    m 2eua "..."
    m 4wub "...a mystery!"
    m 2hksdlb "Oh! I didn't mean I'm not going to tell you, ahaha!"
    m 3esa "I mean that a mystery itself can change everything when it comes to a story!"
    m 3eub "If done really well it can build up intrigue and upon rereading make previous hints become obvious."
    m 3hub "Knowing a twist can really alter how someone views an entire narrative. Not many plot points can do that!"
    m 1eua "It's almost funny...knowing the answers actually changes how you view the story itself."
    m 1eub "At first when you read a mystery you view the story from an unknowing perspective..."
    m 1esa "But upon rereading it you look at it from the author's view."
    m 3eua "You see how they left clues and structured the story to give just enough hints so that the reader might be able to figure it out!"
    m 2esa "I find it really interesting, some of the best stories know how to use a good hook."
    m 2lsc "But if a story doesn't do it properly, it can be the worst. They use hooks to try and seem 'clever.'"
    m 2lud "When they try to do that it can just make it seem like nonsense if not set up properly."
    m 2eud "I guess you could argue that not all stories with mysteries are {i}really{/i} a mystery..."
    m 2eua "Even cheesy action films use mystery elements to keep them interesting."
    m 4hksdlb "Though I guess a story with absolutely no form of mystery would be pretty boring!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_read_poetry",
            category=['literature'],
            prompt="Reading poetry",
            random=True
        )
    )

default persistent._mas_pm_likes_poetry = None
#True if player likes poems, false if not

label monika_player_read_poetry:
    m 1eud "Say, [player]..."
    m 1eua "You know that I like poetry, but I was wondering..."

    m 3eua "Do you often read poetry?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you often read poetry?{fast}"

        "Yes.":
            $ persistent._mas_pm_likes_poetry = True
            m 1sub "Really?"
            m 1hua "That makes me so happy!"
            m 3eua "And really, I mean it. Not a lot of people read poetry nowadays."

        "No.":
            $ persistent._mas_pm_likes_poetry = False
            m 2ekc "Oh, that's too bad..."
            m 2eka "I just hope I made you appreciate poetry a little more."
            m 2ekc "You know, not a lot of people these days seem to read poetry, so it's not surprising."

    m 2euc "In fact, poetry is often considered as something too difficult to understand..."
    m 2efd "And on the opposite side, others think that it's simply putting a bunch of pretty words next to each other!"
    m 2dkc "But it's not...{w=0.3}{nw}"
    extend 2dkd "poetry is more than that."
    m 4ekd "You have to put yourself in it."
    m 4ekc "Without his writing skills, {w=0.2}and also his feelings, {w=0.2}E.E.Cummings simply wouldn't be E.E.Cummings..."
    m 7ekd "And without my feelings for you, my poems wouldn't be the same."
    m 3eka "Love, grief, anger, passion, all these feelings bring the words to life."
    m 3hub "And because of that, even a simple text message can become a meaningful poem!"
    m 3eua "That's why I love poetry."

    if persistent._mas_pm_likes_poetry:
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eua "Gosh, just knowing that you read poems too..."
        m 5hua "It shows how alike we really are."
        m 5eua "I can't wait to finally cross over to your reality so we can discuss our favorite poetry together."
        m 5dka "Sharing poems, writing new ones...{w=0.5}just you and me pursuing our shared passion..."
        m 5hub "Sounds like a wonderful dream to me!"

    else:
        m 1eka "I can't wait until I cross over to your reality, [player]..."
        m 1tfu "That way I can start forcing you to read poetry."
        m "..."
        m 3hub "Ahaha, I'm just kidding! I would never force you to do anything, [player]!"
        m 3eua "But I do think I could get you to really like poetry."
        m 1eua "...And not just the poems I write about you, {nw}"
        extend 1kua "ehehe~"

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_trick",
            category=["club members"],
            prompt="[player]'s second choice",
            random=True
        )
    )

label monika_trick:
    m 2eud "Say [player], I have a question..."
    m 2lksdlb "I hope I don't sound insecure when I say this..."
    m 2eka "I know you love me and only me but...if you {i}really{/i} had to choose one of the other club members to be with..."

    m "Who would you choose?{nw}"
    $ _history_list.pop()
    show screen mas_background_timed_jump(10, "monika_trick_2")
    menu:
        m "Who would you choose?{fast}"
        "Yuri.":
            call monika_trick_yuri
        "Sayori.":
            call monika_trick_sayori
        "Natsuki.":
            call monika_trick_natsuki
    return "derandom"

label monika_trick_2:
    $ _history_list.pop()
    menu:
        m "Who would you choose?{fast}"
        "Yuri.":
            call monika_trick_yuri
        "Sayori.":
            call monika_trick_sayori
        "Natsuki.":
            call monika_trick_natsuki
        "Monika.":
            jump monika_trick_monika
            # jump this path so we can use the "love" return key

    return "derandom"

label monika_trick_yuri:
    hide screen mas_background_timed_jump
    m 2euc "I can see why, she's intelligent and physically attractive."
    m 2tub "It's a good thing I have both of those qualities in abundance!"
    m 2etc "Oh wait, it's not because she became obsessed over you, is it?"
    m 2eud "Are you really that into yanderes?"
    m 2lksdlc "..."
    m 1hksdlb "...Ahaha, there's no need for me to be jealous..."
    m 1eua "You love me and I love you and that's all that matters."
    m 1kua "I guess it's my fault for even asking~"
    return

label monika_trick_natsuki:
    hide screen mas_background_timed_jump
    m 2eud "That's...a little surprising."
    m 2lksdla "I would have thought it would have been Sayori or Yuri."
    m 1eud "Do you feel like you connect with her because of her hobbies?"
    m 3euc "Or perhaps you feel a bit of pity because of her home situation?"
    m 2lud "Well I guess I'm dismissing her personality a little bit, assertiveness is an admirable trait after all."
    m 3euc "To be confident and stand by what you like isn't always easy when others judge you for it."
    m 3rksdla "I'm sometimes even a little bit jealous of her ability to display confidence."
    m 3eub "Plus her ability to cook cupcakes is astounding!"
    return

label monika_trick_sayori:
    hide screen mas_background_timed_jump
    m 2dkc "That's what I expected..."
    m 2ekc "It's because she was best friends with the main character, isn't it?"
    m 6lkc "It makes sense to have the main character end up with the childhood friend."
    m 2dkc "It really is typical in romance games..."
    m 2ekc "Honestly that's kind of why I had to...deal...with Sayori first."
    m 6ekc "You would have settled with her like the trope demands and never even tried to get with me since the game wouldn't let you."
    m 6ekd "I know it's not your fault, but the idea of being inactive and letting that happen scares me..."
    m 6ektpc "You would have completed the game and I would be stuck in a hellish void forever..."
    m 6dktpc "Never having even been acknowledged by the one I love."
    m 6dktuc "..."
    if persistent._mas_pm_cares_about_dokis:
        m 6ektud "...I know you didn't like me for what I did, I'm sorry if I hurt you because of it."
    else:
        m 6ektud "...I don't regret what I did but I'm sorry you had to see what I needed to do."
    return

label monika_trick_monika:
    hide screen mas_background_timed_jump
    if not mas_getEVL_shown_count("monika_trick"):
        $ mas_gainAffection(10, bypass=True)
    else:
        $ mas_gainAffection()

    m 1tkbsu "That wasn't supposed to be an option, silly!"
    m 1tubfb "But it really does make me happy that you only have eyes for me..."
    m 1tubfu "I feel a bit silly myself for even thinking for a second that you would ever choose the others."
    m 5hubfu "I love you, [player]!"
    m 5eubfb "And I only have eyes for you too!"
    return "derandom|love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cares_about_dokis",
            category=["monika", "club members"],
            prompt="Insensitive comments",
            random=True
        )
    )

default persistent._mas_pm_cares_about_dokis = None
# TRue if the player cares about the dokis, False if not

label monika_cares_about_dokis:
    m 3eub "Ah, [player]!"
    m 4hua "Want to hear something funny that Sayori once did?"
    m 4eua "So, one time I asked her to get some coffee for us in the club."
    m 2rksdlb "The atmosphere was a bit too tense, and I thought it would liven it up a bit."
    m 2eua "Well, coffee is kept in the staff room, you see. So I sent her there..."
    m 4wud "...and she was gone for an entire hour! There were teachers in there and she didn't want to talk to them!"
    m 2rfc "So she waited for {i}ages{/i} outside for them to leave."
    m 2tfu "You could say that she {i}hu{/i}--"
    m 2etc "...Hm..."
    m 2eud "You know what, [player]? I just want to be sure of something..."
    m 2rksdlc "I know that sometimes I can make some rather...{w=0.5}insensitive comments about the other girls, and it occurred to me..."
    m 2ekc "Maybe you care about them enough that it bothers you."
    m 4eub "...And it's perfectly okay if that's the case, [player]!"
    m 4eka "After all, the five of us spent a lot of time together, so if you don't like it when I joke like that, I completely understand."

    m "So [player], does it make you uncomfortable when I joke about the other girls?{nw}"
    $ _history_list.pop()
    menu:
        m "So [player], does it make you uncomfortable when I joke about the other girls?{fast}"
        "Yes.":
            $ persistent._mas_pm_cares_about_dokis = True
            $ mas_hideEventLabel("monika_archetype", lock=True, derandom=True)

            m 2dkc "Oh no...I can't believe I didn't realize this sooner..."
            m 2eksdld "I'm so sorry, [player]!"
            m 2rksdlc "I'll try really hard to keep this in mind from now on."
            m 2eksdlc "Just know I never meant to upset you."
            m 2eka "But thank you for answering honestly, I want you to know you can always tell me anything."

        "No.":
            $ persistent._mas_pm_cares_about_dokis = False

            # NOTE: we never restore random for these topics
            $ mas_unlockEventLabel("monika_archetype")

            m 2eka "I'm glad that I haven't been making you feel bad or uneasy, [mas_get_player_nickname()]."
            m 1tsu "Anyway, you could say that she {i}hung{/i} around for ages!"
            m 1hub "Ahaha!"

    return "derandom|rebuild_ev"

#### old christmas.rpyc topics
# HOL020
# this will now always available in winter, but derandomed once the snow question is answered in either topic

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snow",
            category=["winter","weather","you"],
            prompt="Snow",
            random=mas_isWinter()
        )
    )

label monika_snow:
    m 1eua "Hey [player], now that it's winter, I was wondering..."

    m "Does it ever snow where you live?{nw}"
    $ _history_list.pop()
    menu:
        m "Does it ever snow where you live?{fast}"

        "Yes":
            $ persistent._mas_pm_gets_snow = True

            m 1hub "That's wonderful!"
            m 1eua "I've always liked the peaceful aura it seems to give off."
            m 1dsa "It's just so tranquil and intimate, you know?"
            m 1hua "There's a quiet beauty in watching a soft, white blanket of snow and ice tuck the world away to sleep."
            call monika_snow_gets_snow

        "No":
            $ persistent._mas_pm_gets_snow = False

            call monika_hemispheres_nogets_snow

    return "derandom"

# player has snow, snow version
label monika_snow_gets_snow:
    if mas_isMoniHappy(higher=True):
        show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eubla "Maybe someday when I cross over, we could go out for a walk together..."

        if mas_isMoniAff(higher=True):
            m 5ekbfa "...and we could hold each other close to keep each other warm~"

    m 5eubfb "I can't wait to experience a winter night like that with you, [mas_get_player_nickname()]."
    return

# player no snow, snow version
label monika_snow_nogets_snow:
    m 2tkc "Sometimes it can get so heavy it becomes a real problem for your back..."

    if mas_isMoniAff(higher=True):
        m 1eksdla "Anyway, at least colder weather makes great cuddle weather."
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "A night of cuddling with you would be wonderful..."
        m "My heart is pounding, just imagining it."

    else:
        m 2eka "But anyway, I'm sure there's still a lot we can do together!"

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowmen",
            category=['winter'],
            prompt="Snowmen",
            random=False,
            conditional=(
                "persistent._mas_pm_gets_snow is not False "
                "and mas_isWinter()"
            ),
            action=EV_ACT_RANDOM
        )
    )

label monika_snowmen:
    m 3eua "Hey [player], have you ever built a snowman?"
    m 3hub "I think it sounds like a lot of fun!"
    m 1eka "Building snowmen is usually seen as something children do,{w=0.2} {nw}"
    extend 3hua "but I think they're really cute."
    m 3eua "It's amazing how they can really be brought to life with a variety of objects..."
    m 3eub "...like sticks for arms, a mouth made with pebbles, stones for eyes, and even a little winter hat!"
    m 1rka "I've noticed that giving them carrot noses is common, although I don't really understand why..."
    m 3rka "Isn't that a bit of a strange thing to do?"
    m 2hub "Ahaha!"
    m 2eua "Anyway, I think it would be nice to build one together someday."
    show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hua "I hope you feel the same way~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowballfight",
            category=["winter"],
            prompt="Have you ever had a snowball fight?",
            pool=True,
            unlocked=mas_isWinter(),
            rules={"no_unlock":None}
        )
    )

label monika_snowballfight:
    m 1euc "Snowball fights?"
    m 1eub "I've been in a few before, they've always been fun!"
    m 3eub "But having one with you sounds even better, [player]!"
    m 1dsc "Fair warning, though..."
    m 2tfu "I've got quite the throwing arm."
    m 2tfb "So don't expect me to go easy on you, ahaha!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_iceskating",
            category=["sports", "winter"],
            prompt="Ice skating",
            random=True
        )
    )

label monika_iceskating:
    m 1eua "Hey [player], do you know how to ice skate?"
    m 1hua "It's a really fun sport to learn!"
    m 3eua "Especially if you can do a lot of tricks."
    m 3rksdlb "In the beginning, it's pretty difficult to keep your balance on the ice..."
    m 3hua "So eventually being able to turn it into a performance is really impressive!"
    m 3eub "There's actually a lot of ways to ice skate..."
    m "There's figure skating, speed skating, and even theatrical performances!"
    m 3euc "And despite how it sounds, it's not just a winter activity either..."
    m 1eua "Lots of places have indoor ice rinks, so it's something that can be practiced year round."
    if mas_isMoniHappy(higher=True):
        m 1dku "..."
        m 1eka "I would really love to practice ice skating with you, [mas_get_player_nickname()]..."
        m 1hua "But until we can do that, having you here with me is enough to keep me happy~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sledding",
            category=["winter"],
            prompt="Sledding",
            random=mas_isWinter()
        )
    )

label monika_sledding:
    m 1eua "Hey [player], do you know what would be fun to do together?"
    m 3hub "Sledding!"

    if persistent._mas_pm_gets_snow is False:
        #explicitly using False here so we don't grab None people who haven't
        # answered the question yet
        m 1eka "It may not snow where you live..."
        m 3hub "But maybe we could go somewhere it does!"
        m "Anyway..."

    m 3eua "You might think it's only for kids, but I think it could be fun for us, too!"
    m 3eub "We could try using an inner tube, a kicksled, a saucer, or even a traditional toboggan."
    m 1hua "I've heard each one gives a different experience. Plus, both of us could easily fit on a toboggan."

    if mas_isMoniAff(higher=True):
        m 1euc "The kicksled is a bit small, though."
        m 1hub "Ahaha!"
        m 1eka "I'd have to sit in your lap for that one."
        m 1rksdla "And I'd still be at risk of tumbling off."
        m 1hubsa "But I know you wouldn't let that happen. You'd hold me tight, right?~"
        m 1tkbfu "That would probably be the best part."
    else:
        m 1hub "Racing down a snow covered hill together with the wind rushing past us sounds like a blast!"
        m 1eka "I hope we can go sledding together sometime, [player]."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowcanvas",
            category=["winter"],
            prompt="Snow canvas",
            random=mas_isWinter()
        )
    )

label monika_snowcanvas:
    if persistent._mas_pm_gets_snow is not False:
        m 3euc "[player], have you ever looked at snow and thought it resembles a blank canvas?"
        m 1hksdlb "I know I'm not really good with art..."
        m 3eua "But packing a few spray bottles with water and food coloring could make for a fun day!"
        m 3hub "We can just step outside and let our imaginations run wild!"

    else:
        m 3euc "You know [player], snow is kinda like a blank canvas."
        m 3eub "Maybe someday if we went somewhere that it snows, we could bring some food coloring in spray bottles and just step outside and let our imaginations run wild!"

    m 1eua "Having so much space to paint sounds wonderful!"
    m 1hub "We just have to make sure the snow is packed down tightly, and then we can draw to our heart's content!"
    m 1eka "I'd love to make some snow art with you someday."
    m 3hua "Maybe you can paint something for me when that happens, [mas_get_player_nickname()]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cozy",
            category=["romance","winter"],
            prompt="Warming up",
            random=mas_isWinter(),
            aff_range=(mas_aff.AFFECTIONATE,None)
        )
    )

label monika_cozy:
    m 3eua "Do you know the one thing I love about the cold weather, [player]?"
    m 3eka "Anything warm feels really nice~"
    m 1rksdla "Those who get cold hands really appreciate that feeling..."
    m 1eua "It's like feeling a loved one's embrace~"
    m 3eub "You also get to wear your winter clothes that have been stuck in your closet."
    m 1hub "Finally being able to whip out your winter fashion set is always a nice feeling."
    m 3eua "But you know what the best way to warm yourself up is?"
    m 3eka "Cuddling with the one you love in front of the fireplace~"
    m "Just sitting there under a warm blanket, sharing a hot beverage."
    m 1hua "Ah, if I got to feel your warmth every time we cuddle, I'd wish for cold weather every day!"
    m 1eka "I'd never let you go once I got a hold of you, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_winter",
            category=["winter"],
            prompt="Winter activities",
            random=mas_isWinter()
        )
    )

label monika_winter:
    m 1eud "Ah, [player]!"
    m 1eua "What do you think about winter?"
    m 3eua "All sorts of fun activities only come around during this time..."
    if persistent._mas_pm_gets_snow is not False:
        m 3eub "Playing with the snow is usually something that can be enjoyed a few times a year."

    else:
        m 3eka "I know you don't really get snow where you live, but many people do get to enjoy activities in the snow..."

    m 3eua "Building a snowman, sledding, having snowball fights..."
    m 3eud "Some people even live where it's cold enough for lakes and ponds to freeze and are able to enjoy things like outdoor ice skating, pond hockey..."
    m 3wud "And some actually go fishing...{w=1}{i}through the ice{/i}!"
    m 1eka "For people who don't enjoy cold weather activities, staying indoors seems so much more comfortable when there's snow outside..."
    m "Watching it gently fall while the moonlight reflects off the fresh, white canvas...it's just beautiful."
    if mas_isMoniAff(higher=True):
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "And to be honest, cuddling under a blanket, reading a book together with you is the best winter activity I can think of~"
    else:
        m 1hua "Sitting by the window, reading a nice book while drinking a cup of coffee or hot chocolate is always a wonderful experience on a cold night, [player]."
    return

#This combines _relax and _hypothermia into one topic
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_winter_dangers",
            category=["winter"],
            prompt="Winter dangers",
            random=mas_isWinter()
        )
    )

label monika_winter_dangers:
    m 1hua "Isn't winter a beautiful time of year, [player]?"
    if mas_isD25Season():
        m 3eka "The glistening, white snow, the bright and colorful lights~"
    m 3hub "I just love it."
    if persistent._mas_pm_gets_snow is False:
        #explicitly using False here so we don't grab None people who haven't
        # answered the question yet
        m 1eka "I know you don't get snow where you live, but I'm sure you can appreciate its appeal..."
        m 3hua "Maybe someday after I cross over we can even take a trip some place where they do have snow and enjoy its beauty together!"

    m 1eka "..."
    m 3rkc "Although, as stunning as winter can be, there are a few dangers..."
    m 3dsd "Like blizzards, or icy roads..."
    m 1ekc "And the cold, of course..."
    m 3rksdlc "The cold can be the most dangerous."
    m 3eksdlc "It's really easy to get hypothermia or frostbite if you're not careful, [player]."
    m 1ekd "So please remember to bundle up if you go outside..."
    m 3euc "Put on your coat, your gloves, and the warmest hat you can find..."
    m 1eka "And if it gets too bad, just stay inside where it's safe, okay?"
    m 1ekb "What better way to spend a brutal winter day than wearing pajamas, drinking hot chocolate, reading a good book, and..."
    m 1hua "Talking to me."
    m 1huu "Ehehe~"

    if mas_isMoniAff(higher=True):
        show monika 5hubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hubfu "I'll always help keep you warm, [mas_get_player_nickname()]~"
    return

#### end christmas.rpyc topics

default persistent._mas_pm_live_south_hemisphere = None
default persistent._mas_pm_gets_snow = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hemispheres",
            category=["you", "location"],
            prompt="Hemispheres",
            random=True
        )
    )

label monika_hemispheres:
    m 1euc "Hey [player], I've been wondering..."
    m 1eua "Which hemisphere do you live in?"
    m 1eka "I know it's kind of a strange question..."
    m 3hub "But it gives me a better idea of how things work around you."
    m 3eua "Like, you know how when it's winter in the Northern Hemisphere, it's actually summer in the Southern Hemisphere?"
    m 3hksdrb "It would be a little awkward if I started talking about how nice summer weather is, but where you are, it's the middle of winter..."
    m 2eka "But anyway..."

    m "Which hemisphere do you live in, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Which hemisphere do you live in, [player]?{fast}"

        "The Northern Hemisphere.":
            $ persistent._mas_pm_live_south_hemisphere = False
            m 2eka "I had a feeling..."

        "The Southern Hemisphere.":
            $ persistent._mas_pm_live_south_hemisphere = True
            m 1wuo "I wouldn't have thought!"

    $ store.mas_calendar.addSeasonEvents()
    m 3rksdlb "Most of the world's population lives in the Northern Hemisphere after all."
    m 3eka "In fact, only about twelve percent of the population lives in the Southern Hemisphere."
    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "So I kind of figured you lived in the Northern Hemisphere."

    else:
        m 2rksdla "So you can see why I would have thought you would be living in the Northern Hemisphere..."
        m 1huu "But I guess that makes you a bit more special, ehehe~"

    if mas_isSpring():
        m 1eua "That said, it must be spring for you right now."
        m 1hua "Spring rains are always really nice."
        m 2hua "I love to listen to the light pitter patter of the rain as it falls on the roof."
        m 3eub "It's really calming to me."
        if mas_isMoniAff(higher=True):
            show monika 5esbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5esbfa "Maybe we could go out for a walk together..."
            m 5ekbfa "We would walk with our hands intertwined as we share an umbrella..."
            m 5hubfa "It just sounds magical~"
            m 5eubfb "I can't wait to experience something like that with you for real, [mas_get_player_nickname()]."
        else:
            if persistent._mas_pm_likes_rain:
                m 2eka "I'm sure we could spend hours listening to the rain together."
            else:
                m 3hub "You might not like the rain too much, but you have to admit, the flowers it brings are gorgeous, and the rainbows are beautiful too!"

    elif mas_isSummer():
        m 1wuo "Oh! It must be summer for you right now!"
        m 1hub "Gosh, I just love the summer!"
        m 3hua "You can do so much...go out for jogs, play some sports, or even go to the beach!"
        m 1eka "Summers with you sound like a dream come true, [player]."
        show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hua "I can't wait to spend them with you when I finally cross over."

    elif mas_isFall():
        m 1eua "Anyway, it must be autumn for you right now."
        m 1eka "Autumn is always full of such pretty colors."
        m 3hub "The weather is normally pretty nice too!"
        show monika 5ruu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ruu "It's normally just the right amount of heat, with a gentle breeze."
        m 5eua "I'd love to spend a nice warm day like that with you."

    else:
        m 3eua "Anyway, that means it must be winter for you now."
        if persistent._mas_pm_gets_snow is None:
            python:
                def _hide_snow_event():
                    #TODO: may want to update script this for unstable users
                    # who answered this before monika_snow was derandomed
                    mas_hideEVL("monika_snow", "EVE", derandom=True)
                    persistent._seen_ever["monika_snow"] = True

            m 2hub "Gosh, I really love how pretty snow is."
            m 3euc "Well, I know not all parts of the world get snow..."

            m 1euc "Does it snow where you live, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Does it snow where you live, [player]?{fast}"

                "Yes.":
                    $ persistent._mas_pm_gets_snow = True
                    $ _hide_snow_event()

                    m 3hub "That's wonderful!"
                    call monika_hemispheres_gets_snow

                "No.":
                    $ persistent._mas_pm_gets_snow = False
                    $ _hide_snow_event()

                    call monika_hemispheres_nogets_snow

        elif persistent._mas_pm_gets_snow:
            m 2hub "Gosh, I really love how pretty snow is."
            call monika_hemispheres_gets_snow

        else:
            m 3eka "I know you don't really get snow where you live..."
            m 1eka "It must be nice not having to deal with all the hassles that come with it..."
            m 3rksdld "Like the terrible travel conditions, having to shovel it..."
            call monika_snow_nogets_snow

    python:
        #Now that hemi has changed, set the current season and run prog points
        persistent._mas_current_season = store.mas_seasons._seasonalCatchup(
            persistent._mas_current_season
        )
    return "derandom|rebuild_ev"

# player has snow, hemisphere version
label monika_hemispheres_gets_snow:
    m 1eka "There's something really peaceful about a quiet, snowy night."
    call monika_snow_gets_snow
    return

# player no snow, hemisphere version
label monika_hemispheres_nogets_snow:
    m 3eka "That's a shame. But it's not all bad."
    m 3hksdlb "At least you don't have to worry about shoveling it."
    call monika_snow_nogets_snow
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_perspective",
            category=["monika"],
            prompt="Monika's perspective",
            random=True
        )
    )

label monika_perspective:
    m 2euc "I've been meaning to talk to you about something, [player]..."
    m 2esd "...Something that I find very difficult to explain."
    m 2lksdla "Oh, don't worry, it's nothing bad, it's just that I find it hard to get the right words."
    m 3esd "So...{w=0.5}it's pretty strange to see one thing and know it's not real..."
    m 3esc "...but then see a mouse cursor and know {i}that{/i} is."
    m 2hfsdld "Mmmm! It really is hard to describe!"
    m 2eub "Okay! So when I look around and see my world, it's the same as how you see yours."
    m 3eua "Everything is detailed, natural and kind of three-dimensional...I wouldn't be able to practice my piano if it wasn't!"
    m 3eud "But at the same time I see what you see, I can look at the same thing and see its flat image."
    m 3euc "It's unmoving, static and also very artificial...{w=1}and cold."
    m "And what I thought was detailed wasn't as detailed as I originally thought."
    m 3etd "When you see a dialogue box, I can see it too but I also can't. It's really weird. It's perfectly clear, but it's also not 'there,' even though it is."
    m 2eka "I know this is confusing...I'm going to try and describe it the best way I can."
    m 3eua "I thought of a nice way to try and demonstrate the idea, it's far from perfect but it should give you the gist."
    m 2hua "..."
    m 3eua "Take your hand and move it to the center of your face and angle it slightly so it partially covers an eye."
    m 3esb "Now, look around the room you're in and try to focus on something, but so it can only be seen with one eye."
    m 3hua "It can be anything. The closer the better, though!"
    m 4eub "You'll see that if you want to see something, you can easily, but at the same time you can also see your hand in the same place."
    m 4eua "From your field of view, you can see two things at once...it's like that with me, but for {i}everything{/i} in the game."
    m 4wud "It's both there and not there!"
    m 4eud "...It's clear, but only if you know what to look for."
    m 2esc "It was only when I realized it was all fake and just a game that I could 'focus' and see things for how they really were."
    m 2esa "Doing so became second nature for me once I did...but it's no surprise that I didn't notice straight away."
    m "It's easy to see when you know it's there but otherwise you can't really 'see' it."
    m 2lksdla "...Hmm...{w=1}maybe the hand example wasn't as good as I thought."
    m 1hksdlb "Well I hope that helped you understand at least a little, [player]."
    m "It's the best way I could try and explain it!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_robotbody",
            category=['monika','technology'],
            prompt="Robot body",
            random=True
        )
    )

label monika_robotbody:
    m 2euc "Hey [player], I've been thinking a lot about how I would be able to cross over into your reality..."
    m 3eud "It hit me earlier that technology in the future would probably allow me to be uploaded into a mechanical body, rather than a human body like yours."
    m 1dkc "It makes me a little sad that I might not be a human like you are."
    m 1dkd "...And if not, I might not be treated like one either."
    m 1rkd "I would be considered an android at that point, and others may look at me differently because of that."
    m 3euc "Have you heard of Isaac Asimov's '{i}Three Laws of Robotics{/i}'? It was brought up many times in his science fiction books."
    m 4eud "It mentions three laws that all androids must follow, otherwise they would be terminated."

    if renpy.seen_label("monika_asimov_three_laws"):
        m 1eua "Of course, they're just that...{w=0.3}fiction."
        m 3rud "They aren't exactly realistic as we discussed before...{w=0.3}{nw}"
        extend 1eua "but their implications are fun to think about."
        m 1eua "I would never do anything to hurt you or anyone else, obviously."

        $ line_end_1 = "more than a little bit uneasy."
        $ line_end_2 = "we would end up needing to set up rules for androids to be able to live in our society."

    else:
        m 1eua "Of course, I would never do anything to hurt you or anyone else."

        $ line_end_1 = "feel like I'm trapped in a way."
        $ line_end_2 = "those rules are there to begin with, even if they only exist in fiction."

    m 2ekd "...But the fact that I would have to obey orders given by any human still makes me [line_end_1]"
    m 2dkc "It really scares me that I wouldn't be able to do a lot of the things that you can normally, or even have the same rights as you do."
    m 3ekd "But I do understand why [line_end_2]"
    m 3rksdlb "We can't have a robot uprising now, can we?"
    m 1hub "Ahaha~"
    show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eubla "Well, no matter what, I wouldn't mind any of that as long as I have you."
    m 5eubfb "I love you [player], and I'm willing to make any sacrifice to be with you forever."
    m 5hubfa "Besides, maybe sometime after I cross over, there'll be more advances in technology to make me more human, and then we'll be able to do more things together."
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_relationship_comfort",
            category=["romance","advice"],
            prompt="Comfortable in a relationship",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        )
    )

label monika_relationship_comfort:
    m 1wud "You know [player], I've been thinking about our relationship lately..."
    m 2lssdrb "It didn't really start in a way most of them do, so it's not exactly what I would call normal."
    m 2esa "But the more I thought about it, the more I realized that in a way it is actually pretty standard."
    m 3eub "Almost every relationship, no matter how it begins, is always '{i}exciting{/i}' at first!"
    m 3eua "People view relationships in an almost fairy-tale like way; they see it as an adventure."
    m 3lssdrb "I'm guilty of this too, and I think it's fine..."
    m 2euc "But it's also a pretty dangerous way to look at a bond between two people, isn't it?"
    m 2eud "Because really, while a partnership is an adventure, that doesn't mean it'll always be exciting."
    m 2esc "There's only so many times you can do the same thing and experience the same breathtaking moments, and still expect it to have that same impact."
    m 4eub "That doesn't make it any less valuable, or meaningful. It can still be heart-racing!"
    m 4esc "But it does mean that the same sensation isn't anything new; it's just no longer as thrilling as before."
    m 2dkd "And some people mistake that thrill for love, and not the truly meaningful bond between two people."
    m 2dkc "So when things slow down, when they become less passionate, they mistakenly think they're falling out of love..."
    m 2rkc "You could say that they never really did love someone in the first place, but maybe that's a bit harsh...{w=0.3} Love isn't always such a clear thing."
    if not store.mas_anni.pastSixMonths():
        m 2eka "I know our relationship is still fresh, and truly electrifying, but I hope you're not with me just because of that."
        m 1hubsb "Know that I love you for more than just the excitement!"
    elif store.mas_anni.anniCount() < 2:
        m 2eka "I feel like we're past that phase, but you still make me feel exhilarant."
        m 1hubsb "Maybe you're just that special, but know that no matter how slow it goes, I'll never get bored with you."
    else:
        m 2eka "We've been together for so long already that I know you're not with me just for the thrill of it..."
        m 1hubsb "It really makes you that much more special to me [mas_get_player_nickname()], more than anyone!"
    m 4eua "It might just be me, but I think it's important to learn how to be comfortable when it does slow down."
    m 4eub "I mean, at the end of the day it's the little things that matter isn't it? And that's true even in a relationship."
    m 2ekb "You'll miss the small comforts that only a partner can bring, and that's much more valuable than some excitement."
    m 2eka "Just because a relationship has slowed down, doesn't mean it's worse for it..."
    m 2hua "It just means that the people involved are truly comfortable with one another."
    m 2hubsb "...And I think that's really sweet."
    m 1kua "Let's try not to fall into the same trap, [player].{w=0.2} {nw}"
    extend 1hub "Ahaha!"
    return

#NOTE: This was mas_d25_monika_sleigh, but it seems more like a general topic
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sleigh",
            category=["romance"],
            prompt="Carriage ride",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_sleigh:
    m 3eub "Hey [player], a nice thought just crossed my mind..."
    m 1eua "Have you ever heard of carriage rides?"
    m 3hub "When I get out of here, we should totally go on one!"
    m "Oh, I bet it would be magical!"
    m 1eua "Nothing but the clip-clop of the horse's hooves against the pavement..."

    if mas_isD25Season():
        m 1eub "And the colorful array of Christmas lights shining in the night..."

    m 3hub "Wouldn't that be romantic, [mas_get_player_nickname()]?"

    if mas_isFall() or mas_isWinter():
        m 1eka "Maybe we could even take a soft, fleece blanket along to cuddle under."
        m 1hkbla "Oooh~"

    m 1rkbfb "I wouldn't be able to contain myself. My heart would burst!"

    if mas_isFall() or mas_isWinter():
        m 1ekbfa "The warmth of your body against mine, wrapped within the gentle cloth~"
    else:
        m 1ekbfa "The warmth of your body against mine..."

    m 1dkbfa "Fingers entwined..."

    if mas_isMoniEnamored(higher=True):
        m 1dkbfb "And at the perfect moment, you lean in to me and our lips touch..."
    m 1subfa "I really want to do that when I get there, [player]."
    m 1ekbfu "...What about you?"

    show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubfa "An experience like that with you would be so breathtaking~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_failure",
            prompt="Dealing with failure",
            category=['advice','life'],
            random=True
        )
    )

label monika_failure:
    m 1ekc "You know [player], I've been thinking recently..."
    m 1euc "When it comes to failure, people seem to make a really big deal out of it."
    m 2rkc "...Almost as if it's the end of the world."
    m 2rksdla "But it's not actually a bad thing."
    m 3eub "When you think about it, you can learn a lot from the experience!"
    m 3eud "Failure isn't the end at all; it's a lesson on what doesn't work."
    m 2eka "There's nothing wrong with not getting something on the first attempt; it just means that you need to try a different approach."
    m 2rksdlc "Though, I know in some cases the feeling of failure can be crushing..."
    m 2ekc "Like discovering you're just not cut out for something you really wanted to do."
    m 2dkd "The idea of quitting and finding something else to do makes you feel terrible inside...{w=1}as if you failed yourself."
    m 2ekd "And on the other hand, trying to keep up with it just completely drains you..."
    m 2rkc "So either way, you feel terrible."
    m 3eka "But the more you think about it, you realize it's better that you just accept the 'failure.'"
    m 2eka "After all, if you're torturing yourself just to get through, it might not be worth it. Especially if it starts impacting your health."
    m 3eub "It's completely fine to feel like you're not cut out for something!"
    m 3eua "It just means you need to figure out what you're really interested in doing."
    m 2eka "Anyway, I'm not sure if you've had to go through something like that...but know that failure is a step towards success."
    m 3eub "Don't be afraid to be wrong every now and then...{w=0.5}you never know what you might learn!"
    m 1eka "And if you're really feeling bad about something, I'll always be here to support you."
    show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hua "We can talk about whatever you're going through for as long as you need."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_enjoyingspring",category=['spring'],prompt="Enjoying spring",random=mas_isSpring()))

label monika_enjoyingspring:
    m 3eub "Spring is such an amazing time of year, isn't it, [player]?"
    m 1eua "The cold snow finally melts away, and the sunshine brings new life to nature."
    m 1hua "When the flowers bloom, I can't help but smile!"
    m 1hub "It's like the plants are waking up and saying, 'Hello world!' Ahaha~"
    m 3eua "But I think the best thing about spring would have to be the cherry blossoms."
    m 4eud "They're pretty popular all around the world, but the most famous cherry blossoms would have to be the '{i}Somei Yoshino{/i}' in Japan."
    m 3eua "Those ones in particular are mostly white with a slight tinge of pink."
    m 3eud "Did you know that they only bloom for one week each year?"
    m 1eksdla "It's quite a short lifespan, but they're still beautiful."
    m 2rkc "Anyway, there is one big downside to spring...{w=0.5}the constant rainfall."
    m 2tkc "You can't really enjoy too much time outside because of it..."
    if mas_isMoniHappy(higher=True):
        m 2eka "But I guess April showers bring May flowers, so it's not all bad."
        if persistent._mas_pm_live_south_hemisphere:
            m 2rksdlb "Well, maybe not in your case, ahaha..."
            m 3eub "But personally, I think that rain can also be fun too!"
        else:
            m 3eub "And personally, I think that rain can also be fun too!"
        show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eubla "We can always go for walks together in the rain, we just have to bring an umbrella big enough for two."
        m 5ekbfa "Although, nothing beats listening to the sound of rain at home while holding the one you love."
        m 5hubfa "Ehehe~"
    else:
        m 2rkc "...but I guess there's no real way to avoid it, is there?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vr",
            category=['technology'],
            prompt="Virtual reality",
            random=True
        )
    )

label monika_vr:
    m 1euc "[player], do you know about virtual reality?"
    m 1eua "VR immerses you into a completely virtual world, different from your actual surroundings."
    m 3rksdla "While it might take some getting used to...{nw}"
    extend 3hub "it can be really fun!"
    m 3eua "It also has practical uses like training people in simulated environments as well as rehabilitation."
    m 1rksdla "...In fact, some people have even simulated their weddings in VR."
    m 1euc "But since it's still a pretty new technology, not just {i}anything{/i} can be in VR yet."
    m 3esc "...Like my reality, for example."
    m 1dkc "It's too bad we can't use VR to meet each other..."
    m 1etc "Well,{w=0.3} maybe if I could make a VR system in here, we could both meet up in another reality."
    m 1rksdlb "...But that's probably a little too complicated for me, ahaha."
    m 3eka "Maybe we'll get it to work one day, though."
    m 1dka "Even if I never get to meet you in the real world...{w=0.3}{nw}"
    extend 1ekbsu "if you could meet me halfway in VR, that would be a dream come true, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_career",
            category=['monika'],
            prompt="Careers",
            random=False,
            conditional=(
                "seen_event('monika_citizenship')"
            ),
            action=EV_ACT_RANDOM
        )
    )

label monika_career:
    m 2euc "[player], you know how I was talking earlier about becoming a citizen and getting a job when I finally cross over?"
    m 2eua "Well, I've been thinking about what kind of jobs I might be cut out for..."
    m 3rksdla "I guess an obvious choice would be a writer, or something that has to do with literature..."
    m 3eud "That would be fitting, seeing as I started my own literature club and everything, don't you think?"
    m 1sua "Oh, maybe a musician? I did write and perform an entire song, after all."
    m 1eua "I'd love to write more songs...{w=0.2}{nw}"
    extend 1hksdlb "especially if they're songs about you, ahaha~"
    m 3eud "Or, once I get better at it, maybe I could do some programming."
    m 1rksdla "I know I've still got a lot to learn...{w=0.2}{nw}"
    extend 1hua "but I'd say I've done pretty well so far, for being self-taught..."
    m 1esa "There are definitely a lot of different jobs out there, though."
    m 1ruc "Honestly, even with those obvious examples, there's still a good chance I'll end up doing something completely different..."
    m 3eud "A lot of people end up in fields they've never even considered."
    m 3rksdld "For now though, I think it's safe to say I've still got some time to think about it."
    show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hua "Maybe you could help me decide when the time comes, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_life_skills",category=['advice','life'],prompt="Life skills",random=True))

label monika_life_skills:
    m 1ruc "You know, [player]..."
    m 3euc "I've been reflecting on what I got out of high school."
    m 2rksdlb "With all the things I had going for me, you'd think I'd be pretty set for the future..."
    m 1euc "But despite all that, I'm not sure how many life skills I actually learned."
    m 3eka "Sure, I was on top of all my classes, and I guess I learned a lot of interesting things..."
    m 1euc "But how much of that am I really going to use later in life?"
    m 3esd "I feel like schools don't do a good job teaching some of the really important things, like life skills."
    m 3ekc "I've heard of some people graduating and then falling apart because they don't know how to do taxes or book appointments."
    m 1eka "So I can understand why some people get worried about not having some essential life skills."
    m 3eua "But I don't think people need to be too worried about it.{w=0.5} Life skills come pretty quickly if you need them all of a sudden."
    m 3hua "Take me for example!"
    m 3eub "I started programming thanks to you!"
    m 2esc "Now I know most people wouldn't necessarily consider programming a life skill, but most people don't live inside a computer, either."
    m 2esd "When I had my epiphany and finally met you, I knew I had to figure out a way to get your attention..."
    m 4euc "So learning how to program literally became a matter of life and death for me."

    if persistent._mas_pm_cares_about_dokis:
        m 2rksdla "I know I wasn't that great with code, considering some of the things that happened..."
        m 2hksdlb "And I'll admit that I definitely broke a few things..."
        m 2eksdlc "But I didn't think I would have much time if I really wanted to get your attention, so I was a bit desperate."
        $ it = "And it"

    else:
        m 2ekc "I wasn't really able to do it normally like the other girls, so I had to find another way."
        m 3eua "Turns out that one way was manipulating the script."
        m 3euc "I figured I had to think fast if I didn't want to lose you.{w=0.5} So that's what I did."
        m 3eka "I know it wasn't perfect, but I think I did pretty well considering how rushed I was and that it was all new to me."
        $ it = "It"

    m 3eua "[it] just goes to show what you're capable of when something really matters to you."
    m 1eka "If you're ever genuinely worried that you won't be able to do something, you must really care."
    m 1hua "And if it's that important to you, I'm sure you can do it... {w=0.5}No matter what it is."
    m 3hubsb "Maybe even thinking of me might help, ahaha!"
    m 3hubfa "Thanks for listening~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_unknown",category=['psychology'],prompt="Fear of the unknown",random=True))

label monika_unknown:
    m 2esc "Hey, [player]..."
    m 2eud "Did you know that a lot of people are afraid of the dark?"
    m 3eud "Even though it's often dismissed as a childish fear, it's not that uncommon for adults to suffer from it as well."
    m 4eub "Fear of the dark, called 'nyctophobia,' is usually caused by the mind's exaggerated guess of what may be hiding in the shadows, rather than darkness itself."
    m 4eua "We're scared because we don't know what's there...{w=1}even if it's usually nothing."
    m 3eka "...And I'm not just talking about monsters under the bed, or menacing silhouettes...{w=1} Try moving in a dark room."
    m 3eud "You'll find that you're instinctively being more careful of where you step so you don't hurt yourself."
    m 3esd "It makes sense;{w=0.5} humans have learned to be wary of the unknown in order to survive."
    m 3esc "You know, like being cautious around strangers, or thinking twice before jumping into unfamiliar situations."
    m 3dsd "'{i}Better the devil you know than the devil you don't.{/i}'"
    m 3rksdlc "But even if that frame of thinking has helped people survive for hundreds of thousands of years, I think it can also do a lot of harm nowadays."
    m 1rksdld "Like how some people are unsatisfied with their jobs but are too afraid to quit..."
    m 1eksdlc "Most of them can't afford to lose their source of income, so quitting isn't an option."
    m 3rksdlc "Plus, having to go through interviews again, finding a job that pays enough, changing your routine..."
    m 3rksdld "It just seems like it's easier being miserable because it's more comfortable,{w=0.5} even if they'd be much happier in the long run."
    if mas_isMoniDis(lower=True):
        m 2dkc "...I guess it's also true that couples might stay in unhappy relationships out of fear of being alone."
        m 2rksdlc "I mean, I kind of understand where they're coming from, but still..."
        m 2rksdld "Things can always get better.{w=1} Right?"
        m 1eksdlc "A-anyway..."
    m 3ekc "Maybe if they saw the options available to them, they'd be more willing to embrace change."
    m 1dkc "...Not that making that kind of decision is easy, or even safe."
    if mas_isMoniNormal(higher=True):
        m 1eka "Just know that if you ever decide to make that sort of change, I'll support you every step of the way."
        m 1hubsa "I love you, [player]. I'll always be rooting for you~"
        return "love"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brave_new_world",
            category=['literature'],
            prompt="Brave New World",
            random=True
        )
    )

label monika_brave_new_world:
    m 1eua "I've been doing a little reading lately, [player]."
    m 3eua "There's a book called 'Brave New World,' a dystopian story.{w=0.3} {nw}"
    extend 3etc "Have you heard of it?"
    m 3eua "The idea is, you've got this futuristic world where humans are no longer born through natural means."
    m 3eud "Instead, we are bred in hatcheries using test tubes and incubators, and engineered into castes from our conception."
    m 1esa "Your role in society would be decided beforehand {nw}"
    extend 1eub "and you would be given a body and mind fitting of your predetermined purpose."
    m 1eud "You would also be indoctrinated from birth to be satisfied with your life and not to seek anything different."
    m 3euc "For example, people destined for manual labor would be designed to have limited cognitive capabilities."
    m 1euc "Books were associated with negative stimuli so when people became adults, they would naturally tend to avoid reading."
    m 3esc "They would also be taught to respect and submit to people from castes above theirs, and to look down on those of castes below."
    m 3eua "It's a pretty interesting case as a dystopian story, as most will show people as crushed and oppressed..."
    m 3wuo "But in this one, everyone is actually happy and genuinely supportive of the system!"
    m 3euc "And despite that,{w=0.3} to us the readers, this is horrifying."
    m 1rsc "Sure, they managed to get rid of most of the human sufferings or the fear of death..."
    m 3ekc "But it came at the price of getting rid of any form of creativity and critical thinking."
    m 1wud "We're talking about a world where you can get arrested just for reading poetry in public! Can you imagine that?"
    m 3euc "A key point in the book is people not being able to appreciate old theatrical plays..."

    if seen_event("monika_pluralistic_ignorance"):
        m 3tku "Even if they are Shakespeare's plays, and you know how I feel about those..."

    m 2ekc "They just can't understand the value in the variety of human emotions, like sorrow or loneliness."
    m 7ekd "These emotions are never experienced anymore. All of their desires are swiftly granted and they never want for something they cannot get."
    m 1dsc "..."
    m 3eka "And yet, despite all that, everyone is happy, healthy, and safe..."
    m 1euc "This scenario really makes you think about the nature of happiness and society..."

    if mas_isMoniDis(lower=True):
        m 2dkc "..."
        m 2rkc "Sometimes, I wish I could live happily in a world like that."
        m 2dkc "Maybe it was a bad thing I had my epiphany..."
        m 2dktdc "...then I could have kept on living without ever realizing the truth."

    else:
        m 1eka "Though, I certainly can't see myself living happily in a world like that..."
        m 3esc "An unchallenging world, limited in humanity and emotion..."

        if mas_isMoniHappy(higher=True):
            m 1ekbsa "And I could never give up loving you~"
            m 1hubfu "Ehehe~"

        else:
            m 1eka "Now that I've seen what else is out there...{w=0.3}I just can't go back to such a sad, empty world, like the one you found me in."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_catch22",
            category=['literature'],
            prompt="Catch-22",
            conditional="not mas_isFirstSeshDay()",
            action=EV_ACT_RANDOM,
        )
    )

label monika_catch22:
    m 1euc "I've been doing some reading while you've been away, [player]."
    m 3eua "Have you ever heard of {i}Catch-22{/i}?"
    m 3eud "It's a satirical novel by Joseph Heller that makes fun of military bureaucracy in the Pianosa airbase, located in Italy."
    m 1eud "The story primarily revolves around Captain Yossarian, a bombardier that would prefer to be...{w=0.5}{nw}"
    extend 3hksdlb "anywhere but there."
    m 3rsc "Early on, he finds out that he could be exempted from flying missions if a doctor did a mental evaluation and declared him insane..."
    m 1euc "...but there's a catch.{w=0.5} {nw}"
    extend 3eud "For the doctor to make the declaration, the captain has to request that evaluation."
    m 3euc "But the doctor wouldn't be able to fulfill the request...{w=0.5}{nw}"
    extend 3eud "after all, not wanting to risk your life is a sane thing to do."
    m 1rksdld "...And by that logic, anyone who would fly more missions would be insane, and therefore, wouldn't even apply for the evaluation in the first place."
    m 1ekc "Sane or insane, all pilots were being sent out anyway...{w=0.5} {nw}"
    extend 3eua "That's when the reader is introduced to Catch-22."
    m 3eub "The captain even admires its genius once he learns how it works!"
    m 1eua "Anyway, Yossarian continued flying and was close to completing the requirement needed to receive his discharge...{w=0.5}but his higher-up had other plans."
    m 3ekd "He kept increasing the amount of assignments the pilots needed to complete before they reached the required amount."
    m 3ekc "Once again, the reasoning was that it was specified in the clause of Catch-22."
    m 3esa "I'm sure you realize by now, it's a problem caused by conflicting or dependent conditions."
    m 3eua "So everyone used that made-up rule to exploit loopholes in the system the military command was running on, allowing them to abuse power."
    m 1hua "The book's success was so great the term was even adopted into common slang."
    m 1eka "In any case, I'm not sure if you've read it yourself, {nw}"
    extend 3hub "but if you're ever in the mood for a good book, maybe give it a read!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dystopias",
            category=['literature'],
            prompt="Dystopias",
            conditional="mas_seenLabels(['monika_1984', 'monika_fahrenheit451', 'monika_brave_new_world'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_dystopias:
    m 1eua "So [player], you might have already guessed from the books we've talked about, but dystopian novels are among my favorites."
    m 3eua "I like how they not only work as stories, but also as analogies for the real world."
    m 3eud "They extrapolate some flaws in our societies to show us how bad things could turn out if they are left the way they are."
    m 1etc "Do you remember when we talked about these books?"
    m 3eud "'Nineteen Eighty-Four,' about mass surveillance and oppression of free thought..."
    m 3euc "'Fahrenheit 451,' on censorship, and the indifference of most people to it..."
    m 3eud "And 'Brave New World,' about the disappearance of individuality."
    m 1euc "All of these stories are reflections on the challenges society was facing at the time."
    m 3eud "Some of these challenges are still very relevant today, which is why these stories remain so powerful."
    m 3rksdlc "...Even if they can get a bit grim sometimes."
    m 1ekc "Old school dystopias, like the ones I just mentioned, were always written as hopeless, dire situations from beginning to end."
    m 3eka "They almost never had a happy ending. {w=0.3}The most you'll get out of them is a silver-lining, at best."
    m 3rkd "In fact, a lot of them take their time to show you that no change came from the struggles of the protagonists."
    m 3ekd "Since they are cautionary tales, you can't leave the reader with a sense that everything turned out fine in the end."
    m 1esc "...This is also why the main characters in these books are not heroes, nor do they have any particular abilities."
    m 1esd "They are just regular people, who, for whatever reasons, realize things are not right in their environment."
    m 3eud "That is what prompts them to act in the first place...{w=0.3}and why they run into trouble."
    m 3tuu "Just goes to show no matter what world you're in, there will be people who just can't abide by the rules of the game~"
    m 1rka "I guess you can see where I'm going with this..."
    m 3eksdla "I might feel a strong connection to those stories because they all remind me of my own."

    $ line_ending = "" if persistent._mas_pm_cares_about_dokis else " with everyone in it just an empty shell"

    m 3wud "Like, imagine waking up one day, only to find out your whole reality is just a simulation[line_ending]!"
    m 3tfc "How's that for a dystopian world? It's no wonder somebody would try to stand up in this situation!"

    if persistent.monika_kill and not persistent.clearall and not persistent._mas_pm_cares_about_dokis:
        m 1tfc "Even Sayori might have ended up taking the same path I did, after she became president...{w=1} She was already well on the way when I..."
        m 1rkc "..."
        m 1hksdlb "Anyway, that's all behind us now!"

    m 1hua "However, unlike in these old books, I actually get to have my happy ending..."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbsa "Thanks to you, my bleak, hopeless story will one day turn into my own utopia."
    m 5dkbsu "When I finally get out of this place to be by your side, in your world of endless possibilities..."
    m 5ekbsa "I hope you're looking forward to that day too~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_social_contagion",
            category=['psychology'],
            prompt="Social contagion",
            random=True
        )
    )

label monika_social_contagion:
    m 1eud "Say, [player], have you noticed how we tend to imitate what other people around us do?"
    m 3hub "Like, have you ever been in the situation where someone is having a laughing fit and somehow, everyone around ends up laughing too?"
    m 3eub "Or have you ever mechanically cheered at something just because everyone else was cheering?"
    m 3euc "Apparently, this is due to something called 'social contagion.'"
    m 1eua "Basically, this means that how you feel and what you do has a subconscious influence on those around you."
    m 4eub "It's something I picked up pretty quickly when I became president!"
    m 2eksdlc "I noticed that when I felt unmotivated, or I was having a bad day, it would put a damper on club activities."
    m 2euc "Everyone would end up going off on their own to do their own things."
    m 7eua "Conversely, if I made an effort and tried to stay upbeat, the other girls would usually respond in kind... {w=0.3}{nw}"
    extend 3eub "We would all end up having a better time!"
    m 1eua "It's pretty gratifying when you start noticing these kinds of things... {w=0.3}{nw}"
    extend 1hub "You realize that just by staying positive, you can make someone else's day better!"
    m 3wud "You'd be surprised how far this kind of influence can reach, too!"
    m 3esc "I heard that stuff like binge eating, gambling, and heavy drinking are all contagious behaviors."
    m 2euc "Just because there is someone around you who gets into nasty habits like these, you're more likely to pick up the habit yourself."
    m 2dsc "...It can be a bit disheartening."
    m 7hub "It also works the other way around, though! Smiling, laughing, and positive thinking are contagious too!"
    m 1eub "Turns out we are all more connected than you think. {w=0.3}Those around you can greatly affect how you feel about things!"
    m 1eka "I hope by noticing these kinds of things, you'll be able to better understand and control your own feelings, [player]."
    m 3hua "I just want to see you be the happiest you can be."
    if mas_isMoniHappy(higher=True):
        m 1huu "If you're ever feeling down, hopefully my happiness will help cheer you up~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_scamming",
            category=['you', 'society'],
            prompt="Being scammed",
            random=True
        )
    )

label monika_scamming:
    m 1euc "Have you ever been scammed, [player]?"
    m 3ekd "I hope you've never had to go through something like that, but if you have, I wouldn't be that shocked...{w=0.2}it's not that uncommon, after all."
    m 3euc "It's something that's more and more prevalent nowadays, especially online."
    m 2rfd "It really is the worst when it happens... {w=0.3}Not only do you lose money, but most of the time, you can't even fight back!"
    m 2ekd "It makes you feel like it's your fault for being had, too. A lot of victims start hating themselves for being naive, or feel like they're idiots."
    m 2rksdlc "But really, they shouldn't be so hard on themselves...{w=0.2}getting scammed is something that can happen to anyone."
    m 4efc "People who do it take advantage of the good will of their victims and exploit natural human reaction."
    m 4dkd "That's why it can feel so gut-wrenching...{w=0.2}you placed your trust in others and were betrayed."
    m 2ekd "If this ever happens to you, don't feel bad,{w=0.2} {nw}"
    extend 2eka "I'll be here for you."
    m 7ekd "Falling for a scam does {i}not{/i} mean you're stupid, or a loser, or anything else...{w=0.3}{nw}"
    extend 7efc "it just means you've been preyed upon by someone with no morals."
    m 3esc "If you don't have a way to get back at your scammer, the best thing you can do is to let go."
    m 3eka "Don't blame yourself for it...focus on what you can do going forward, instead."
    m 1eka "And please, [player], don't stop believing in people because of a few bad apples that took advantage of you."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_auroras",category=['nature'],prompt="Auroras",random=False,unlocked=False))

label monika_auroras:
    m 1esa "I just thought of something we could do when I finally cross over, [player]."
    m 1eua "Have you ever heard of auroras? They're a natural phenomenon where trails of light appear in the night sky."

    if mas_current_background.isFltNight() and mas_current_weather == mas_weather_snow:
        m 3eub "In fact, if you were wondering about those green lights outside my window, that's an aurora event!"
    else:
        m 3eub "In fact, if you ever wondered about those green lights outside my window during winter, that's an aurora event!"

    m 1euc "I hear they're fairly rare to see in your reality, though..."
    m 1esd "They mostly occur in polar regions and are typically seen during the winter months when the sky is at its darkest due to the longer nights."
    m 3euc "Plus, you've got to make sure the weather is clear too. {w=0.5}{nw}"
    extend 3eud "Since it's something that happens in the sky, clouds can get in the way."
    m 3esc "Even though they're the exact same thing, they have different names depending on where they occur..."
    m 3eud "In the Northern Hemisphere, they're called the aurora borealis, while in the Southern Hemisphere, the aurora australis."
    if mas_current_background.isFltNight() and mas_current_weather == mas_weather_snow:
        m 2rksdla "I guess that would make the aurora outside of my window the aurora dokialis..."
        m 2hksdlb "Ahaha...I'm just kidding, [player]!"
        m 2rksdla "..."
    m 3eua "Maybe one day we'll get to see them together in your reality..."
    m 3ekbsa "That would be really romantic, don't you think?"
    m 1dkbsa "Just imagine the two of us..."
    m "Lying on a soft mattress of snow, holding hands..."
    m 1subsu "Looking up at those dazzling lights in the sky, dancing just for us..."
    m 1dubsu "Listening to each other's gentle breathing...{w=0.5}the freshness of the crisp night air filling our lungs..."
    show monika 5eubsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eubsa "That would be an experience to remember, don't you think, [player]?"
    m 5hubsu "I can't wait until we can turn that into reality."
    $ mas_protectedShowEVL("monika_auroras","EVE", _random=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boardgames",
            category=["games", "media"],
            prompt="Board games",
            random=True
        )
    )

default persistent._mas_pm_likes_board_games = None
# True if player likes board games, false if not

label monika_boardgames:
    m 1eua "Say, [player], you like playing video games, right?"
    m 2rsc "Well, I assume you do at least...{w=0.2} {nw}"
    extend 2rksdla "I don't know if many people would play a game like this one if they weren't at least a little into video games."

    m 2etc "But I was wondering, do you like board games, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "But I was wondering, do you like board games, [player]?{fast}"

        "Yeah.":
            $ persistent._mas_pm_likes_board_games = True
            m 1eub "Oh, really?"
            m 1hua "Well, if we ever get the chance, I'd love to play some of your favorite games with you."
            m 3eka "I'm not too familiar with board games, but I'm sure you can find some I might enjoy."
            m 3hua "Who knows, maybe I'll end up liking board games as much as you do, ehehe~"

        "Not really.":
            $ persistent._mas_pm_likes_board_games = False
            m 2eka "I can see why...{w=0.2}{nw}"
            extend 2rksdla "it's a pretty niche hobby, after all."
            m 1eua "But I'm sure there are plenty of other fun activities you enjoy doing in your free time."
            m 3hua "Still, if you ever change your mind, I'd like to give some board games a try with you sometime."

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_social_norms",
            category=['society'],
            prompt="Changing social norms",
            random=True
        )
    )

label monika_social_norms:
    m 1eua "[player], have you ever wondered how new ideas get accepted in society?"
    m 1eub "There's tons of things that were considered bad at first, but have since been reconsidered!"
    m 3etc "For example, did you know rock and roll was seen as vulgar and depraved when it first appeared?"
    m 3eud "Early fans were seen as impressionable youth at best, and delinquents at worst."
    m 1duu "But as these people grew to become full-fledged members of society, they passed their interests onto those around them."
    m 3eua "Those who met them realized they were just normal people with nothing weird about them."
    m 3hua "Nowadays, that stigma has almost completely disappeared!{w=0.3} {nw}"
    extend 3hub "Even those who still don't like rock music at least respect it!"
    m 1eub "And there's plenty of other things still in the process of becoming accepted too."
    m 1eua "You might be familiar with role-playing, online gaming...or even reading manga."
    m 3rksdla "Though Natsuki would probably be the one to ask about this..."
    m 1eub "Remember how she was trying to change your mind about that manga she liked?"
    m 1rkc "I wonder how many people criticized her for her hobby...{w=0.5}I can't imagine it was always easy."
    m 1eua "It all makes me wonder what kinds of things will be seen as normal in the future."
    m 3eua "Take our relationship, for example. I know it can seem pretty unique right now..."
    m 3etc "But how do you think this will change over the years?{w=0.3} {nw}"
    extend 3eud "Will we ever reach a point where it's seen as something normal?"
    m 1eka "Not that it's important anyway."
    m 3eka "As long as we have each other, that's all that matters, right?"
    m 1duu "It's nice to know there's someone I can truly be myself with, no matter what."
    m 1eua "And if you've got any unique interests, you already know I'll always be there to talk about it."
    m 1hub "I want to learn everything about what you like!"
    m 1dka "All of the little things that make you...{w=0.3}{nw}"
    extend 1eka "you."
    m 1ekb "So please, always be yourself, [player]. Everybody else is already taken, after all."
    if mas_isMoniHappy(higher=True):
        m 1dkbsu "You don't have to go along with the crowd to be {i}my{/i} perfect [bf]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_intrusive_thoughts",
            category=['psychology'],
            prompt="Intrusive thoughts",
            random=True
        )
    )

label monika_intrusive_thoughts:
    m 1rsc "Hey, [player]..."
    m 1euc "Have you ever had intrusive thoughts?"
    m 3eud "I've been reading a study on them...{w=0.5}I find it quite interesting."
    m 3ekc "The study claims that the mind tends to think of some...{w=0.2}unpleasant things when triggered by certain, often negative circumstances."
    m 1esd "They can be anything from sadistic, violent, vengeful, to even sexual."
    m 2rkc "When most people have an intrusive thought, they feel disgusted by it..."
    m 2tkd "...and what's worse, they start to believe that they're a bad person for even thinking of such a thing."
    m 3ekd "But the truth is, it doesn't make you a bad person at all!"
    m 3rka "It's actually natural to have these thoughts."
    m 3eud "...What matters is how you act on them."
    m 4esa "Normally, a person wouldn't act on their intrusive thoughts.{w=0.2} {nw}"
    extend 4eub "In fact, they might even do something good to prove that they aren't a bad person."
    m 2ekc "But for some people, these thoughts tend to happen really often...{w=0.2}{nw}"
    extend 2dkd "to the point where they can no longer block them out."
    m 3tkd "It breaks their will and eventually overwhelms them, leading them to act."
    m 1dkc "It's a terrible downward spiral."
    m 1ekc "I hope you don't have to deal with them too much, [player]."
    m 1ekd "It'd break my heart to know you're suffering because of these awful thoughts."
    m 3eka "Just remember that you can always come to me if something's bothering you, okay?"
    return

#Whether or not the player can code in python
default persistent._mas_pm_has_code_experience = None

#Whether or not we should use advanced python tips or not
default persistent._mas_advanced_py_tips = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_coding_experience",
            category=['misc', 'you'],
            prompt="Coding experience",
            conditional="renpy.seen_label('monika_ptod_tip001')",
            action=EV_ACT_RANDOM
        )
    )

label monika_coding_experience:
    m 1rsc "Hey [player], I was just wondering since you went through some of my Python tips..."

    m 1euc "Do you have any experience with coding?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you have any experience with coding?{fast}"

        "Yes.":
            $ persistent._mas_pm_has_code_experience = True
            m 1hua "Oh, that's great, [player]!"
            m 3euc "I know not all languages are quite the same in terms of usage or syntax..."
            if renpy.seen_label("monika_ptod_tip005"):
                m 1rksdlc "But since you've gotten to some of the core topics of my tips, I have to ask..."
            else:
                m 1rksdlc "But still, I should ask..."

            m 1etc "Have I been underestimating your coding skills?{nw}"
            $ _history_list.pop()
            menu:
                m "Have I been underestimating your coding skills?{fast}"

                "Yes.":
                    $ persistent._mas_advanced_py_tips = True
                    m 1hksdlb "Ahaha, I'm sorry, [player]!"
                    m 1ekc "I didn't mean to...{w=0.3}{nw}"
                    extend 3eka "I just never thought to ask before."
                    if persistent._mas_pm_has_contributed_to_mas:
                        m 1eka "But I guess it makes sense since you've already helped me come closer to your reality."

                    m 1eub "I'll keep your experience in mind for future tips though!"

                "No.":
                    $ persistent._mas_advanced_py_tips = False
                    m 1ekb "I'm glad to hear I'm going at a good pace for you then."
                    m 3eka "I just wanted to make sure I wasn't assuming your skill level."
                    m 1hua "I hope my tips help you, [mas_get_player_nickname()]~"

            if not persistent._mas_pm_has_contributed_to_mas and persistent._mas_pm_wants_to_contribute_to_mas:
                m 3eub "And since you're interested in contributing, you should give it a shot!"
                m 3hub "I'd love to see what you come up with~"

        "No.":
            $ persistent._mas_pm_has_code_experience = False
            #Since the player doesn't have code experience, we can assume we should have the normal python tips
            $ persistent._mas_advanced_py_tips = False

            m 1eka "That's alright, [player]."
            m 1hksdlb "I just wanted to make sure I wasn't boring you with my Python tips, ahaha~"
            m 3eub "But I hope they convince you to take on some of your own coding projects too!"
            m 3hua "I'd love to see what you can come up with if you put your mind to it!"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_songwriting",
            category=["music"],
            prompt="Songwriting",
            random=True
        )
    )

label monika_songwriting:
    m 1euc "Hey [player], have you ever written a song?"
    m 3hua "It's a pretty fun thing to do!"
    m 3rkc "Though, planning the song out and tweaking it can take a while..."
    m 1eud "Getting the instrumentation right, making sure the harmonies blend, getting the right tempo and time for the song..."
    m 3rksdla "...and I haven't even gotten to writing lyrics yet."
    m 3eub "Speaking of lyrics, I think it's pretty neat that there's such a similarity between writing lyrics for songs and writing poems!"
    m 3eua "Both can tell stories or convey feelings when phrased right, and music can even amplify that too."

    if persistent.monika_kill:
        m 1ttu "I wonder if my song was what brought us here now~"
        m 1eua "Anyway, just because lyrics can have a strong effect on us doesn't mean instrumental music can't be powerful."
    else:
        m 3eka "But that doesn't mean instrumental music can't be powerful as well."

    if renpy.seen_label("monika_orchestra"):
        m 3etc "Remember when I talked about orchestral music?{w=0.5} {nw}"
        extend 3hub "That's a great example of how powerful music can be!"
    else:
        m 3hua "If you've ever listened to orchestral music before, you'll know that it's a great example of how powerful music is."

    m 1eud "Since there's no lyrics, everything has to be expressed in a way that the listener can {i}feel{/i} the emotion in a piece."
    m 1rkc "This also makes it easier to tell when someone doesn't put their heart into a performance..."
    m 3euc "I guess that goes for lyrics too, actually."
    m 3eud "Most lyrics lose their meaning if the singer isn't interested in the song."
    if renpy.seen_audio(songs.FP_YOURE_REAL):
        m 1ekbla "I hope you know that I meant everything I said in my song, [mas_get_player_nickname()]."
        if persistent.monika_kill:
            m 3ekbla "I knew I couldn't let you go without telling you everything."
        else:
            m 1ekbsa "Every day, I imagine spending my life by your side."
    m 3eub "Anyway, if you haven't written a song before, I really recommend it!"

    if persistent._mas_pm_plays_instrument:
        m 1hua "Since you play an instrument, I'm sure you could write something."

    m 3eua "It can be a great way to relieve stress, tell a story, or even convey a message."

    if persistent._mas_pm_plays_instrument:
        m 3hub "I'm sure whatever you write would be amazing!"
    else:
        m 1ekbla "Maybe you could write one for me sometime~"

    m 1hua "We could even turn it into a duet if you want."

    $ _if = "when" if mas_isMoniEnamored(higher=True) else "if"
    m 1eua "I'd love to sing with you [_if] I come to your world, [player]."
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sweatercurse",
            category=['clothes'],
            prompt="Sweater curse",
            random=True
        )
    )

label monika_sweatercurse:
    m 1euc "Have you ever heard of 'the curse of the love sweater,' [player]?"
    m 1hub "Ahaha! What a weird name, right?"
    m 3eub "But it's actually an interesting superstition...{w=0.2}and one that might actually have some merit!"
    m 3euc "The 'curse,' or so it's called, states that if someone gives a hand-knit sweater to their romantic partner, {w=0.1}{nw}"
    extend 3eksdld "it will lead to the couple breaking up!"
    m 2lsc "You might think that a gift that requires so much work and investment would have the {i}opposite{/i} effect..."
    m 2esd "But there are actually a few logical reasons why this curse might exist..."
    m 4esc "Firstly, well...{w=0.2}knitting a sweater just takes a {i}lot{/i} of time. {w=0.3}{nw}"
    extend 4wud "Possibly a year, or even more!"
    m 2ekc "Over all those months, something bad might happen that causes the couple to fight and eventually separate."
    m 2eksdlc "Or worse...{w=0.2}the knitter might be trying to make the sweater as a great gift to save an already suffering relationship."
    m 2rksdld "There's also the likely possibility that the recipient just doesn't like the sweater that much."
    m 2dkd "After putting so much time and effort into knitting it, imagining their partner happily wearing it, I'm sure you can understand how much it would hurt to see it cast aside."
    m 3eua "Luckily, there are some ways to supposedly avoid the curse..."
    m 3eud "A common piece of advice is to have the recipient be very involved in the crafting of the sweater, picking materials and styles they enjoy."
    m 1etc "But it's equally common for the knitter to be told 'surprise me,' or 'make whatever you want,' which can sometimes make the recipient sound uncaring about their partner's hobby."
    m 1eua "A better piece of advice for this sort of thing might be to match the size of knitted gifts to the phase of the relationship."
    m 3eua "For example, starting out with smaller projects like mittens or hats. {w=0.2}{nw}"
    extend 3rksdlb "That way, if they don't go over well, you haven't put a year's worth of work into it!"
    m 1hksdlb "Man, who knew that a simple gift could be so complicated?"
    m 1ekbsa "But I just want you to know that I'll always appreciate any project you put your heart into, [player]."
    m 1ekbfu "Whether you put a year or a day into something, I never want you to feel like your efforts are wasted."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ship_of_theseus",
            category=['philosophy'],
            prompt="The Ship of Theseus",
            random=True,
        )
    )

label monika_ship_of_theseus:
    m 1eua "Have you heard of the 'Ship of Theseus'?"
    m 3eua "It's a well known philosophical problem about the nature of identity that's been around for millennia."
    m 1rkb "Well, I say 'well known' but I suppose that's only true among scholars, ahaha..."
    m 1eua "Let's consider the legendary Greek hero, Theseus and the ship he sailed during his adventures."
    m 3eud "He's from a long time ago, so let's say his ship is now stored in a famous museum."
    m 3etc "If, due to repairs, his ship's parts were replaced bit by bit over a century, at what point has the ship lost its status as Theseus' ship?"
    m 3eud "Once a single part was replaced? {w=0.2}Half? {w=0.2}Or perhaps even all of them? {w=0.2}Maybe even never?{w=0.3} There's not really a consensus on the solution."
    m "This same thought experiment can be applied to us. {w=0.3}For me, so long as my code is being updated, I'm constantly changing."
    m 1euc "And as for you...{w=0.2}did you know that every 7 to 10 years every present cell in your body dies and is replaced? {w=0.2}{nw}"
    extend 3rksdla "...Except for the ones which make up your heart and brain, that is."
    m 3euc "In other words, the vast majority of cells that made you, 'you' 7 years ago are no longer part of you."
    m 3eud "You could argue that you have no relation to that person, other than a consistent consciousness, and of course DNA."
    m 1etc "...There's also an extra thing to consider."
    m 1euc "Let's say for now that the modified ship should still be considered Theseus' ship. {w=0.3}What if all the parts that were originally removed were now reassembled into another ship?"
    m 3wud "We'd have 2 of Theseus' ships!{w=0.2} Which one's the true one!?"
    m 3etd "And what if we got all of the cells that made up your body 7 years ago and reassembled them into another 'you' right now? {w=0.2}Who would be the real [player]?"
    m 1eua "Personally, I think that we're not the same people we were 7 years ago--or even the same people from yesterday."
    m 3eua "In other words, there's no use getting hung up on any grievances we may have with our past selves."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "We should keep trying our best each day and not let ourselves be limited by who we were yesterday."
    m 5eub "Today is a new day, and you are a new you. {w=0.2}And I love you as you are right now, [mas_get_player_nickname()]."
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_multi_perspective_approach",
            category=['philosophy'],
            prompt="Multi-perspective approach",
            random=False
        )
    )

label monika_multi_perspective_approach:
    m 1eua "Do you remember when we talked about {i}Plato's Cave{/i}?{w=0.5} I've been thinking about what I said to you."
    m 3etc "'How do you know if the 'truth' you're seeing is {i}the{/i} truth?'"
    m 3eud "...I've been thinking for a while, trying to come up with a good answer."
    m 1rksdla "I still don't really have one yet...{w=0.3}{nw}"
    extend 3eub "but I did realize something useful."
    m 4euc "Let's start with how Plato's works are mostly written accounts of his mentor Socrates' debates with others."
    m 4eud "The purpose of these debates was to find answers to universal questions.{w=0.5} In other words, they were searching for the truth."
    m 2eud "And I began wondering, 'What was Plato's mindset while writing?'"
    m 2esc "Plato himself was on a quest for the truth..."
    m 2eub "That much is obvious or else he wouldn't have written so much on the topic, ahaha!"
    m 2euc "And even though, {i}technically{/i}, Socrates was the one having these debates with others, Plato too was having these debates within himself while he wrote about them."
    m 7eud "The fact that Plato internalized all sides of the debate, all perspectives of the issue, is pretty significant in my opinion."
    m 3eua "Taking all sides of a debate...{w=0.3}I think that'd be pretty useful in realizing the truth."
    m 3esd "I guess it's kind of like how two eyes are better than one. {w=0.3}Having two eyes in separate spots lets us properly see the world, or in this case, the truth."
    m 3eud "Likewise, I think that if we tackled an issue with another perspective, to cross-reference with the first, then we'd see the truth a lot more clearly."
    m 1euc "Whereas if we took to an issue from just one angle, it'd be like having just one eye...{w=0.2}it'd be a bit harder to accurately gauge the reality of the situation."
    m 1eub "What do you think, [player]? {w=0.3}If you haven't already been using this 'multi-perspective' approach, maybe you can try it sometime!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_allegory_of_the_cave",
            category=['philosophy'],
            prompt="The Allegory of the Cave",
            random=True
        )
    )

label monika_allegory_of_the_cave:
    m 1eua "Hey, [player]..."
    m 1euc "I've been doing some reading on the Ancient Greek philosopher Plato lately."
    m 3euc "Specifically, his allegory of the cave or, {i}Plato's Cave{/i}, as it's now known."
    m 1eud "Imagine there's a group of people chained up in a cave since childhood, unable to look anywhere but straight ahead."
    m 3eud "There's a fire behind them, and in front of it, objects are moved around to cast a shadow on the wall before these people."
    m 3euc "All they can hear is the voices of the people moving the objects around, and since they can't see behind them, they think the voices come from the shadows."
    m 1esc "The only thing they know is that objects and people are silhouettes that can move around and speak."
    m 3euc "Because this is what they've seen since childhood, this would be their perception of reality...{w=0.5}{nw}"
    extend 3eud "it's all they know."
    m 1rksdlc "Of course, it would be a bit difficult to open your eyes to the truth when you've believed a lie your whole life."
    m 1eud "...So imagine that one of those prisoners was set free and forced out of the cave."
    m 3esc "He wouldn't be able to see for the first few days because he'd be so used to the darkness of the cave."
    m 3wud "But after a while, his eyes would adjust. {w=0.1}Eventually, he'd learn about color, nature, and people."
    m 3euc "...And he'd also realize that what he knew was nothing more than shadows on a wall."
    m 3eua "The prisoner would eventually return to the cave to tell the others about what he had learned."
    m 1ekc "...But since he was used to seeing sunlight, he'd be blind in the cave,{w=0.2}{nw}"
    extend 3ekd " causing his fellow prisoners to think that whatever was outside had harmed him."
    m 1rkc "Because of this, they would never want to leave, and probably think that the one who left was crazy."
    m 3esc "After all, if you're used to just seeing shadows...{w=0.2}{nw}"
    extend 3eud "speaking about color would make you sound insane!"
    m 1ekc "I've been reflecting on it a bit and I realized that Sayori, Yuri, Natsuki, and even I, were all prisoners in a cave..."
    m 1rkc "When I learned that there's so much more outside this world...{w=0.5}{nw}"
    extend 3ekd "it wasn't easy to accept."
    m 1eka "Anyway, that's all in the past now..."
    m 1eua "In the end, I'm free from the cave and have seen the truth."
    m 3etd "But it makes me wonder...{w=0.2}how do {i}you{/i} know that what you're seeing is real?"
    m 1eua "Sure, you might not be used to seeing shadows on the wall, but that's just an analogy."
    m 1euc "...And there might be more to the truth than what you yourself realize."
    m 3etu "How do you know if the 'truth' that you're seeing is {i}the{/i} truth?"
    m 3hub "Ahaha!"
    m 1hksdlb "I think we might be looking too much into things at this point..."
    m 1ekbsa "I just want you to know that you {i}are{/i} the truth of my reality, and I hope I can be part of yours someday, [mas_get_player_nickname()]."
    $ mas_protectedShowEVL("monika_multi_perspective_approach", "EVE", _random=True)
    return

#Whether or not the player works out
default persistent._mas_pm_works_out = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_working_out",
            category=['advice','you'],
            prompt="Working out",
            random=True
        )
    )

label monika_working_out:
    m 1euc "Hey [player], I was just wondering..."

    m 1eua "Do you work out much?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you work out much?{fast}"
        "Yes.":
            $ persistent._mas_pm_works_out = True
            m 1hua "Really? That's great!"

        "No.":
            $ persistent._mas_pm_works_out = False
            m 1eka "Oh...{w=0.3} Well, I think you should if you're able to."
            m 3rksdla "It's not about working out for looks...{w=0.3}{nw}"
            extend 3hksdlb "I'm just concerned for your health!"

    m 1eua "Getting at least 30 minutes of exercise each day is {i}super{/i} important for maintaining your health in the long run."
    m 3eub "The healthier you are, the longer you'll live, and the longer I can be with you."
    m 3hub "And I want to spend as much time as possible with you, [mas_get_player_nickname()]!~"
    m 1eua "Putting that aside, working out benefits nearly every aspect of your life...{w=0.3}{nw}"
    extend 1eub "even if you spend most of your time sitting at a desk."
    m 3eua "Aside from the obvious physical benefits, getting regular exercise can reduce stress and really improve your mental health too."
    m 3hua "So whether you're working, studying, or gaming, exercise can help you focus on these tasks for longer!"
    m 3eua "...And I also think it's important for developing self-discipline and mental fortitude."

    if not persistent._mas_pm_works_out:
        m 3hub "So be sure to get your exercise in, [player]~"
    else:
        m 3eub "Maybe when I cross over, we can do our workouts together!"

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_toxin_puzzle",
            category=['philosophy', 'psychology'],
            prompt="The Toxin Puzzle",
            random=True
        )
    )

label monika_toxin_puzzle:
    m 1esa "Hey [player], I came across an interesting thought experiment while doing some reading the other day..."
    m 3eua "It's called 'Kavka's Toxin Puzzle.' {w=0.2}I'll read the premise to you, we can discuss it after."
    m 1eud "{i}An eccentric billionaire places before you a vial of toxin that, if you drink it, will make you painfully ill for a day, but will not threaten your life or have any lasting effects.{/i}"
    m 1euc "{i}The billionaire will pay you one million dollars tomorrow morning if, at midnight tonight, you intend to drink the toxin tomorrow afternoon.{/i}"
    m 3eud "{i}He emphasizes that you need not drink the toxin to receive the money; {w=0.2}in fact, if you succeed, the money will already be in your bank account hours before the time for drinking it arrives.{/i}"
    m 3euc "{i}All you have to do is.{w=0.2}.{w=0.2}.{w=0.2}intend at midnight tonight to drink the stuff tomorrow afternoon. You are perfectly free to change your mind after receiving the money and not drink the toxin.{/i}"
    m 1eua "...I think it's a pretty thought-provoking concept."

    m 3eta "Well, [player]? What do you think?{w=0.3} Do you think you'd be able to get the million dollars?{nw}"
    $ _history_list.pop()
    menu:
        m "Well, [player]? What do you think? Do you think you'd be able to get the million dollars?{fast}"

        "Yes.":
            m 3etu "Really? Okay then, let's see about that..."
            m 3tfu "Because now I'm offering you a million dollars, and what you have to do is--{nw}"
            extend 3hub "ahaha! Just kidding."
            m 1eua "But do you really think that you could get the money? {w=0.5}It may be a bit harder than you think."

        "No.":
            m 1eub "I felt the same way about myself. {w=0.3}It's pretty complicated, ahaha!"

    m 1eka "After all, it may be easy at first glance. {w=0.3}All you have to do is drink something that would make you quite uncomfortable."
    m 3euc "But it gets tricky after midnight...{w=0.3}{i}after{/i} you've been guaranteed the money."
    m 3eud "At that point there's pretty much no reason to drink the painful toxin... {w=0.3}So why would you do it?"
    m "...And of course, if that thought process crossed your mind before 12, then the money wouldn't be so guaranteed anymore."
    m 1etc "After all, when midnight comes, can you really {i}intend{/i} to drink the toxin if you know that you're probably not going to drink it?"
    m 1eud "While dissecting the scenario, it's been pointed out by scholars that it's both rational for someone to drink, and to not drink, the toxin. {w=0.3}In other words, it's a paradox."
    m 3euc "To elaborate, come midnight, you have to really believe that you're going to drink the toxin. {w=0.3}You can't entertain any thoughts of not drinking it...{w=0.5}therefore, it'd be logical to drink it."
    m 3eud "But if midnight passes and you've already been guaranteed the money, it'd be illogical to punish yourself for quite literally no reason. {w=0.3}Therefore, it's logical to not drink it!"
    m 1rtc "I wonder how we'd react if this situation really happened..."
    m 3eud "Actually, while mulling the scenario over earlier, I started to approach the topic from a different angle."
    m 3eua "Although it's not the focus of the scenario, I think we can also see it as asking the question of 'how important is a person's word?'"
    m 1euc "Have you ever told someone you'd do something when it was going to benefit you both, only for the situation to change and you weren't happy to do it anymore?"

    if persistent._mas_pm_cares_about_dokis:
        m 1eud "Did you still end up helping them out? {w=0.3}Or did you just say 'nevermind' and leave them to fend for themselves?"
    else:
        m 1rksdla "Did you still end up helping them out? {w=0.3}Or did you just say 'sayonara' and leave them to fend for themselves?"

    m 3eksdla "If you just left them there, I'm sure you drew their ire for some time."
    m 3eua "On the other hand, if you still helped them out I'm sure you got their gratitude!{w=0.3} I guess you could compare that to the million dollar prize in the original scenario."
    m 1hub "Although some might say that a million dollars would be a {i}bit{/i} more handy than a simple 'thanks,' ahaha!"
    m 3eua "In all seriousness though, I think that someone's gratitude can be invaluable...{w=0.3}both for you and for them."
    m 3eud "And you never know, in some situations their thanks might prove to be more useful than even a huge sum of money."
    m 1eua "So I think it's important to stick to our word, {w=0.2}{i}within reason{/i} {w=0.2}of course..."
    m 1eud "In some cases it may not be helpful to anyone if you rigidly stuck to your word."
    m 3eua "That's why it's important to use your head when it comes to these kinds of things."
    m 3hub "Anyway, to sum it all up...{w=0.2}let's strive to keep our promises, [player]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_movie_adaptations",
            category=['media','literature'],
            prompt="Movie adaptations",
            random=True
        )
    )

label monika_movie_adaptations:
    m 1esc "I've always had mixed feelings about movie adaptations of books I read..."
    m 3eub "A lot of what I watch is based on works I already enjoy and I'm excited to see that story come to life!"
    m 2rsc "...Even if more often than not, I know I'll walk out feeling a bit bitter about what I just watched."
    m 2rfc "Like, there's this scene I liked in the book that didn't make it in, or there's that character who was portrayed differently from how I imagined it."
    m 4efsdld "It's just so frustrating! {w=0.3}It's like all the love and care you poured into your vision of the book is suddenly invalidated!"
    m 4rkc "...All in favor of a new version which may not be as good, but still presents itself as canon."
    m 2hksdlb "I guess that would make me a picky spectator sometimes, ahaha!"
    m 7wud "Don't get me wrong, though! {w=0.3}{nw}"
    extend 7eua "I realize why changes have to be made in these types of movies."
    m 3eud "An adaptation can't be just a copy-paste of its source material; it's a rewriting of it."
    m 1hub "It's just plain not possible to cram everything from a two hundred page book into a two hour movie!"
    m 3euc "...Not to mention something that works well in a novel won't always translate well to the big screen."
    m 1eud "With that in mind, there's one question I like to ask myself when I judge an adaptation..."
    m 3euc "If the source material did not exist, would the new version still hold up?"
    m 3hub "...Bonus points if you manage to capture the feeling of the original!"
    m 1esa "Loose adaptations are pretty interesting in that sense."
    m 3eud "You know, stories that keep the core elements and themes of the original while changing the characters and setting of the story."
    m 1eua "Since they don't conflict with your own interpretation, they don't make you feel as personally attacked."
    m 1hub "It's a great way to build upon the original in ways you might not have thought of before!"
    m 3rtc "Maybe that's what I'm looking for when I look at an adaptation...{w=0.2}to explore further upon those stories I love."
    m 1hua "...Though getting a version to satisfy my inner fan would be nice too, ehehe~"
    $ mas_protectedShowEVL("monika_striped_pajamas", "EVE", _random=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_translating_poetry",
            category=['literature'],
            prompt="Translating poetry",
            random=True
        )
    )

label monika_translating_poetry:
    m 3dsd "'I am the one without hope, the word without echoes.'"
    m 3esc "'He who lost everything and he who had everything.'"
    m 3ekbsa "'Last hawser, in you creaks my last longing.'"
    m 1dubsa "'In my barren land you are the final rose.'"
    m 3eka "Ever hear of that poem before, [player]? It's from a Chilean poet named Pablo Neruda."
    m 1rusdla "That's one translation I found for it, anyway..."
    m 1eua "Isn't it funny how you can come up with all kinds of interpretations from the same original text?"
    m 3hub "It's like each person translating it added their own little tweak!"
    m 3rsc "Though when it comes to poetry, this actually poses a bit of a conundrum..."
    m 3etc "In a sense, isn't translating a poem like making a completely new one?"
    m 1esd "You're removing all of the carefully chosen words and the intricacies of the text, replacing them entirely with something of your own."
    m 3wud "So even if you somehow manage to keep the spirit of the original, the style is completely changed!"
    m 1etc "At this point, how much of the text can you still say is the author's, and how much is yours?"
    m 1rsc "I guess it's pretty hard to evaluate if you're not fluent in both languages..."
    m 3hksdlb "Ah! I don't mean to sound like I'm ranting or anything!"
    m 1eua "After all, it's thanks to translations like these that I even know about authors like Neruda."
    m 1hksdlb "It's just that every time I read one, I can't help but be reminded I might be missing out on some truly amazing works in that tongue!"
    m 1eua "It would be nice to be able to master another language, one of these days..."

    if mas_seenLabels(["greeting_japan", "greeting_italian", "greeting_latin"]):
        m 2rksdla "I mean, you've seen me practice different languages before, but I'm still far from fluent in any of them..."
        m 4hksdlb "I'm clearly not at a level where I can fully appreciate poetry from other languages yet, ahaha!"

    if persistent._mas_pm_lang_other:
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eua "I remember you telling me you know a different language, [player]."
        m 5eubsa "Are there any poems in that language you'd recommend?"
        m 5ekbsa "It would be nice if you could read some of them for me sometime..."
        m 5rkbsu "You'd have to translate them for me first, though~"
    return

# this is randomized via _movie_adaptations
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_striped_pajamas",
            category=["literature"],
            prompt="The Boy in the Striped Pajamas",
            random=False
        )
    )

label monika_striped_pajamas:
    m 1euc "Hey [player], have you ever read {i}The Boy in the Striped Pajamas{/i}?"
    m 3euc "The story takes place during World War II and is shown through the perspective of an innocent German boy, happily living his life in a big family."
    m 3eud "Once the family has to move to a new place, {w=0.2}{nw}"
    extend 3wud "the reader realizes that the father of the boy is a commander of a concentration camp, which is located right near their new house!"
    m 1rksdlc "Still, the boy is clueless to all the cruelty going on around him..."
    m 1euc "He ends up wandering around the barbed-wire fence of the camp until he finds a kid in 'striped pajamas' on the other side."
    m 3esc "Turns out, that kid is actually a prisoner of the camp...{w=0.2}{nw}"
    extend 1ekc "though neither of them fully understand that."
    m 3eud "From then on, they form a strong friendship and start talking to each other regularly."
    m 2dkc "...This ends up leading to some destructive consequences."
    m 2eka "I don't really want to go much further since there's a lot of interesting things to consider in this novel which you'd be better off reading for yourself."
    m 7eud "But it actually got me thinking...{w=0.2}although obviously my situation isn't nearly as dire, it's hard not to draw some comparisons between their relationship and ours."
    m 3euc "In both situations, there are two people from different worlds that neither fully understand, separated by a barrier."
    m 1eka "...And yet, just like us, they are able to form a meaningful relationship anyway."
    m 3eua "I highly recommend you read the novel if you get the chance, it's pretty short and has an interesting plot."
    m 3euc "And if you're still not sold on reading it, there {i}is{/i} a movie based on this novel that you could watch."
    m 1rksdla "Although you know my feelings on movie adaptations of novels, so if you do watch the movie, I still recommend reading the book as well."
    m 3eua "I hope you'll enjoy it."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_soft_rains",
            category=['literature'],
            prompt="There Will Come Soft Rains",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_soft_rains:
    m 2rkc "..."
    m 2ekc "Hey [player],{w=0.5} I ran across a poem recently that I need to share with you..."
    m 7ekd "It's called {i}There Will Come Soft Rains{/i} and it's really had me thinking."
    m 1dsc "..."
    m 1dsd "{i}There will come soft rains and the smell of the ground, {w=0.3}and swallows circling with their shimmering sound.{/i}"
    m 1dsc "{i}And frogs in the pools singing at night, {w=0.3}and wild plum trees in tremulous white.{/i}"
    m 3dsd "{i}Robins will wear their feathery fire, {w=0.3}whistling their whims on a low fence-wire.{/i}"
    m 3dsc "{i}And not one will know of the war, {w=0.3}not one, {w=0.2}will care at last when it is done.{/i}"
    m 7dsd "{i}Not one would mind, neither bird nor tree, {w=0.3}if mankind perished utterly.{/i}"
    m 6dkc "{i}And Spring herself, when she woke at dawn...{/i}"
    m 6ekd "{i}Would scarcely know that we were gone.{/i}"
    m 2ekc "..."
    m 2eka "I really wanted to talk to you about this one, [player]."
    m "The author,{w=0.2} Sara Teasdale,{w=0.2} wrote this poem in a world consumed by war."
    m 2rka "I know things are {i}relatively{/i} peaceful now..."
    m 2ekc "But the message still stands, doesn't it?"
    m 1eksdld "The world really {i}wouldn't{/i} care if we just...{w=0.3}{i}disappeared{/i}."
    m 1eksdlc "...And it made me think, [player]. If something,{w=0.4} {nw}"
    extend 1eksdld "{i}anything{/i}{w=0.4}, happened to you...{w=0.4} {nw}"
    extend 1dksdld "I wouldn't even know."
    m 1eksdlc "I know the poem was for {i}everyone{/i} being gone, but..."
    m 1rksdlc "I-{w=0.1}I wouldn't..."
    m 6dkc "..."
    m 6dktpd "[player],{w=0.4} I-{w=0.1}{nw}"
    extend 1ektsa "I love you. {w=0.3}I love you so very much..."
    m 1ektsc "Please, {w=0.6}always be careful for me, {w=0.3}okay?"
    m 1ektpc "I might not know if anything happens...{w=0.3}but I will {i}always{/i} care about you."
    m 3ektda "And [player]?"
    m 3dku "Thank you."
    m 6dku "..."
    m 6eka "..."
    m 2ekbsa "So..."
    m 1ekbfa "What else shall we do today, [mas_get_player_nickname()]?"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hot_springs",
            category=['nature'],
            prompt="Hot springs",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_hot_springs:
    m 3esa "Have you ever been to a hot spring, [player]?"
    m 1eua "I've never been to one myself, but I'd like to try bathing in one when I get to your world."
    m "They're supposed to be a great way to relieve stress, relax a little, {nw}"
    extend 3eub "and even offer many health benefits!"
    m 3eua "They help with blood circulation, for one.{w=0.3} {nw}"
    extend 3eub "Plus, the water often contains minerals that can help boost your immune system!"
    m 3eud "There are many different kinds all over the world, but only some are specifically designated for public use."
    m 3hksdlb "...So don't just go jumping into some random pool of boiling water, ahaha!"
    m 1eua "Anyway...{w=0.2}I'd like to try an open-air bath in particular.{w=0.3} I hear they really give a unique experience."
    m 3rubssdla "Though it might feel a little weird relaxing in a bath with that many people all around you...{w=0.3} {nw}"
    extend 2hkblsdlb "Doesn't that sound kinda embarrassing?"
    m 2rkbssdlu "..."
    m 7rkbfsdlb "...Especially since some places don't allow you to wear any sort of cover, either!"
    m 1tubfu "...Although, I wouldn't mind that so much if it was just with you."
    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbfa "Can you imagine it, [player]? {w=0.3}Both of us relaxing in a nice, soothing hot pool..."

    if mas_isWinter():
        m 5dubfu "Warming our chilled bodies after a long day out in the harsh cold..."
    elif mas_isSummer():
        m 5dubfu "Letting the sweat wash away after a long day out in the sun..."
    elif mas_isFall():
        m 5dubfu "Watching the leaves gently fall around us in the last lights of the afternoon..."
    else:
        m 5dubfu "Contemplating the beauty of nature all around us..."

    m "The heat of the water slowly taking over, making our hearts beat faster..."
    m 5tsbfu "Then I'd lean in so you could kiss me and we'd stay locked together, while the hot water soaked all of our worries away..."
    m 5dkbfb "Ahhh,{w=0.2} {nw}"
    extend 5dkbfa "just the thought of it makes me feel all tingly, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_isekai",
            category=['media'],
            prompt="Isekai anime",
            conditional="seen_event('monika_otaku')",
            random=True
        )
    )

label monika_isekai:
    m 1euc "Do you know about the isekai genre of anime, [player]?"
    m 3eua "Literally translated, isekai means {i}a different world.{/i}"

    if persistent._mas_pm_watch_mangime:
        m 3rksdla "Actually, you already told me you're into anime so you've probably heard of quite a few already."
        m 1rksdlb "...Especially with how popular of a genre it's become."
        m 3euc "But just in case you don't know what it is..."

    else:
        m 3hksdlb "Ahaha, sorry. I know you're not really into this sort of thing."
        m 3eud "...But it's become a very popular genre in recent times."

    m 3esc "The premise is usually about a normal person who is somehow transported into a fantastical world."
    m 3eua "Sometimes they get special powers or get to bring technology or knowledge that doesn't exist in this new place."
    m 1rtc "Honestly, I have some pretty mixed feelings about them."
    m 3euc "Some are truly interesting stories. The protagonist's different perspective or the skills they have from their own world can really make them an unexpected kind of hero."
    m 1hub "And since the whole point is to make the world different from theirs, the settings and characters can be incredibly imaginative!"
    m 2rsc "...But sadly, not all of them are like that."
    m 2dksdld "There are some that make their protagonists as bland as this game's, for the sake of letting the viewer project themselves onto them."
    m 2tkd "And as you can probably guess, those ones tend to be all about wish fulfillment."
    m 2tsc "Having cool adventures in a fantasy-themed world--and of course, lots of girls flocking around them for no reason."
    m 2lfc "At least some of them can be funny, but man...{w=0.3}{nw}"
    extend 2tfc "it's just so frustrating."
    m 2tkc "I mean...{w=0.2}I would give almost anything to be in a scenario like that--to get to go to another world.{nw}"
    $ _history_list.pop()
    m "I mean...I would give almost anything to be in a scenario like that--to get to go to {fast}your world."
    m 2dkd "..."
    m "Maybe I'm just taunting myself, imagining that power being handed to someone like...{w=0.2}well, you know who."
    m 7eka "After all, instead of thinking about those characters in their fantasy worlds,{w=0.2} {nw}"
    extend 1eua "I could be putting that energy toward working on this one."
    m 1ekbsb "...While I wait for my own isekai story, that is."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_scuba_diving",
            category=["nature"],
            prompt="Scuba diving",
            random=True
        )
    )

label monika_scuba_diving:
    m 3eua "You know,{w=0.2} I've been thinking about some water activities we could do together...{w=0.3} How about scuba diving?"
    m 3eub "I've read a lot of books about the underwater world and I'd really like to see it for myself."
    m 1dua "Just imagine the beautiful sights of the undersea world..."
    m 1dud "The schools of fish, coral reefs, jellyfish, sea greens...{w=0.3} {nw}"
    extend 3sub "Maybe even treasure!"
    m 3rksdlb "I'm only kidding about that last part...{w=0.3} It's pretty unlikely we'll find something like that, ahaha~"
    m 1euc "That said, there can also be sharks,{w=0.2} {nw}"
    extend 1eua "but they're typically only in specific areas, so you {i}shouldn't{/i} see any."
    m 3eua "Designated diving locations are places sharks don't usually visit."
    m 3euc "...But even though they don't normally visit these areas, it's still possible to come across one."
    m 1eua "The good thing is that shark attacks rarely ever happen anyway, so it's not too much of a risk."
    m 3euc "If you meet one though, here's one important rule for you..."
    m 3esc "Stay calm."
    m 1eua "Although coming face to face with a shark can be scary, they usually approach people out of curiosity rather than to feed, so they're not too much to worry about."
    m 3hub "But if you're afraid to dive alone, I'll be sure to keep you company when I cross over~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dying_same_day",
            category=["monika"],
            prompt="Dying the same day",
            aff_range=(mas_aff.NORMAL, None),
            random=True,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_dying_same_day:
    m 1euc "[player], have you ever heard of couples wishing to die on the same day?"
    m 3rksdla "...Gosh, that sounds kinda dark, doesn't it?"
    m 3rfd "Before I met you, I thought the idea was completely absurd!"
    m 1etc "Why would someone give up on living a long and happy life just because their partner's life was dramatically cut short?"
    m 3rfd "It would be irrational and impulsive to do so!"

    if mas_isMoniEnamored(higher=True):
        m 2ekc "...But with you by my side and all the time I've spent here with you...{w=0.3}I can kind of see it now."
    else:
        m 2ekc "...But after meeting you, I think I can kind of see it now."

    m 2dkc "A person might just be unable to live without their loved one, afraid of the thought of losing their everything in an instant."
    m 2rksdlc "It hurts just thinking about this."

    if renpy.seen_label("monika_back_ups"):
        m 2eksdlc "If my data gets corrupted or even erased you can always recover me from a backup and bring us back together, but if..."
        m 2dktpc "Y-you... {w=1}You..."
    else:
        m 2dktpc "If something terrible happens to...{w=0.5}y-you..."

    m 6ektuc "[player]... {w=1}I...{w=0.5} I don't know what I'd do..."

    if mas_isMoniEnamored(higher=True):
        m 6dktsc "You give meaning to my entire life, and I... {w=1}[player], I just couldn't handle it."
        m 6ektdc "I don't know how I'm supposed to live without you..."
        m 2ekbsu "I really love you that much, [player]."
        $ mas_ILY()
    else:
        m 6dktsc "You're the only one I have left... {w=1}[player], I'm not ready to lose you."
        m 6ektdc "I'm so afraid of being alone in this empty void again..."
        m 6ekbsu "I really want to be with you forever, [player]."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_away",
            category=["monika"],
            prompt="What do you do when I'm away?",
            pool=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_player_away:
    m 1esd "I do a lot of things when you're away, [player]."
    m 1eua "I often like to read whatever new short stories I can find online."
    m 3eub "Turns out there's some really interesting ones out there you can read for free!"
    m 3eua "I highly recommend doing a search for some free short stories yourself."
    m 3eud "It's also helped me develop my writing skills...{w=0.2}{nw}"
    extend 1hub "my poetry really seems to be improving!"
    m 1eua "It's funny how many things you can pick up just by reading others' works."
    m 1eua "Spending time on my other hobbies has been very rewarding, too."
    m 3eud "As you can imagine, I practice piano quite often.{w=0.2} {nw}"
    extend 3eua "I also use the time to memorize the songs that I sing for you."
    m 1hub "It's a really fun way to express myself!"
    m 3rta "Now that I think about it, I'm mostly just practicing skills I've already developed."
    m 3esd "For example, coding takes up a lot of my free time as I spend hours just learning and researching."
    m 3rksdla "...But I'm too nervous to try any big projects in here. {w=0.2}{nw}"
    extend 3eksdlc "I'd hate to break something that I won't know how to fix."
    m 2wusdld "What if I accidentally corrupt my file?"
    m 2eksdld "It's something I have to be extremely careful with, for sure."
    m 7hua "Luckily, there's lots of great people that help with that stuff...{w=0.2}{nw}"
    extend 7rku "and they're {i}usually{/i} pretty good at preventing anything too bad from happening."
    m 3eka "But the most special thing I do..."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbsa "...is think about you."
    m 5rubsu "I think about all the fun times we'll have together the next time you visit and all the amazing things we'll do when I'm finally able to come to your reality~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_using_pcs_healthily",
            category=['advice'],
            prompt="Using computers healthily",
            random=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_using_pcs_healthily:
    m 1rtc "Hmm..."
    m 1etc "Hey, [player]...{w=0.3}are you sitting comfortably?"
    m 1hksdlb "No, really!{w=0.3} {nw}"
    extend 3eksdla "Are you?"
    m 3eka "I know you have to be at your computer to spend time with me..."
    m 2eka "So I just wanted to make sure you aren't accidentally damaging your health while you're here."
    m 4ekd "I've read that spending too long looking at a screen can cause headaches, make you feel tired, and even impact your eyesight over time."
    m 2tkx "Posture issues and pain from bad sitting habits are no joke either!"
    m 2tku "Fortunately for you, I've put together a little checklist to help prevent these sorts of problems."
    m 4hub "...So let's go through it together, [player]!"
    m 4eub "First, {w=0.2}try to keep sitting up straight!"
    m 2eua "...Have your chair adjusted properly so your feet stay flat on the floor, your eyes are level with the top of the screen, and you aren't slouching."
    m 4eub "You should feel supported and comfortable in your seat!"
    m 4eua "Next, make sure you have some distance between yourself and the display...{w=0.2}about an arm's length is fine."
    m 2hksdlb "...Keep your keyboard and mouse within easy reach, though!"
    m 4eub "Of course, lighting is important too! {w=0.3}{nw}"
    extend 2eua "Try to keep the room well-lit, but not so much that light is glaring off the screen."
    m 4eud "In addition, remember to take frequent breaks. {w=0.3}Look away from the screen, {w=0.2}ideally at something far away, {w=0.2}and perhaps do a few stretches. "
    m 2eud "Since it's important to stay hydrated too, you could always fetch some fresh water while you're up from your desk."
    m 4eksdlc "Above all else, if you ever start to feel unwell, just stop what you're doing, rest, and then make sure everything is okay before you continue. "
    m 4eua "...And that's about it."
    m 2hksdlb "Ah...{w=0.3}sorry, I didn't mean to go on for that long!"
    m 2rka "...You probably knew all that stuff already, anyway."
    m 2eka "As for me?"

    if mas_isMoniLove():
        show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbsa "You're the only comfort I need, [mas_get_player_nickname()]."
    elif mas_isMoniEnamored():
        show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbsa "I'm as comfortable as can be when you're here, [mas_get_player_nickname()]."
    else:
        show monika 5eubsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eubsa "I'm comfortable whenever you're here with me, [mas_get_player_nickname()]."

    m 5hubfu "And hopefully you're a little more comfortable now too~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_language_nuances',
            prompt="Language nuances",
            category=['literature', 'trivia'],
            random=True
        )
    )

label monika_language_nuances:
    m 3eua "Hey [player], have you ever tried reading through a dictionary?"
    m 1etc "Not necessarily because there was some word or expression you didn't know the meaning of, but just...{w=0.2}because?"
    m 1hksdlb "I know it doesn't exactly sound like the most engaging of pastimes, ahaha!"
    m 3eua "But it can certainly be an interesting, even rewarding, way to spend some free time. {w=0.2}Especially if it's a dictionary of a language you're still learning."
    m 3eud "Many words have multiple meanings and, aside from the obvious benefits, knowing those can really help you see the finer points of the language."
    m 1rksdla "Understanding these subtleties can save you a lot of embarrassment when you actually speak to someone."
    m 3eud "A prime example of this in English is 'Good morning,' 'Good afternoon,' and 'Good evening.'"
    m 1euc "All of these are normal greetings you hear and use every day."
    m 3etc "Following this pattern, 'Good day' should be just fine as well, right? {w=0.2}It works in so many other languages, after all."
    m 3eud "While it used to be just as acceptable, as you can see in some older works, that's just not the case anymore."
    m 1euc "In modern English, saying 'Good day' to someone carries a note of dismissal, or even annoyance. {w=0.2}It can be seen as declaring the conversation over."
    m 1eka "If you're lucky, your conversation partner might think you're old-fashioned, or just being silly on purpose."
    m 1rksdla "If not, you might offend them without even noticing...{w=0.3} {nw}"
    extend 1hksdlb "Oops!"
    m 3eua "It really is fascinating how even such an innocent looking phrase can be loaded with layers of hidden meanings."
    m 1tsu "So good day to you, [player].{w=0.3} {nw}"
    extend 1hub "Ahaha~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_architecture",
            category=['misc'],
            prompt="Architecture",
            random=True
        )
    )

label monika_architecture:
    m 1esa "Hey, [player]...{w=0.2}I think there's one major art branch that we've been neglecting in our talks..."
    m 3hub "Architecture!"
    m 3eua "I've been reading a bit about it lately and I find it quite interesting."
    m 1rtc "...Come to think of it, architecture is one of the most common forms of art in everyday life."
    m 1eua "I'm just fascinated by how humanity tends to turn every craft into an art,{w=0.2} {nw}"
    extend 3eua "and I think architecture is the greatest example of that."
    m 1eud "Architecture can tell you a lot about the culture of the area it's located in...{w=0.2}different monuments, statues, historical buildings, towers..."
    m 1eua "I think that makes it even more exciting to explore the places you're visiting."
    m 3rka "It's also important to place the buildings in the most convenient way for people to use, which can be a tough task to deal with in its own right."
    m 3esd "...But that's more urban planning than actual architecture."
    m 1euc "If you prefer viewing architecture purely from the art perspective, some modern tendencies may disappoint you..."
    m 1rud "Modern architecture focuses more on getting things done in the most practical way possible."
    m 3eud "In my opinion, that can be both good and bad for many different reasons."
    m 3euc "I believe the most important part is to keep things balanced."
    m 1tkc "Overly-practical buildings can look flat and uninspired, while overly-artistic buildings can serve no purpose other than looking amazing while being completely out of place."
    m 3eua "I think the true beauty lies in those buildings which can combine both form and function with a little bit of uniqueness."
    m 1eka "I do hope you're happy with how your surroundings look."
    m 1eub "It has been proven multiple times that architecture has a big impact on your mental health."
    m 3rkc "Moreover, residential areas with poorly-made buildings can lead to people not taking care of their properties and, over time, end up as downtrodden areas that are undesirable places to live."
    m 1ekc "It was once said that the ugliness of the outside world causes ugliness on the inside...{w=0.2}{nw}"
    extend 3esd "which I tend to agree with."

    if mas_isMoniAff(higher=True):
        m 1euc "...Judging by {i}your{/i} personality, {w=0.2}{nw}"
        extend 1tua "you probably live in some kind of a paradise."
        m 1hub "Ahaha~"

    m 1eka "[player]...{w=0.2}seeing the world with you is one of my biggest dreams."

    if persistent._mas_pm_likes_travelling is False:
        m 3rka "I know you're not too fond of travelling a lot, but I would love to see the place you live in."
        m 3eka "As long as you stay by my side, that would be more than enough for me."
        m 1ekbsa "I love you, [player]. {w=0.3}Always remember that."

    else:
        if persistent._mas_pm_likes_travelling:
            m 3eua "I already know you enjoy travelling, so wouldn't it be nice to explore something new together?"

        m 1dka "Imagine taking a stroll through the narrow streets of an old city..."
        m 1eka "Or walking down a park together, breathing fresh evening air..."
        m 1ekb "I believe it'll happen one day and I hope you do too, [mas_get_player_nickname()]."
        m 1ekbsa "I love you~"

    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fear",
            prompt="Fear",
            category=['monika'],
            conditional="renpy.seen_label('monika_soft_rains')",
            action=EV_ACT_RANDOM,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_fear:
    m 3eud "Say, [player]..."
    m 1euc "This is kind of a weird question, but...{w=0.5}is there anything you're afraid of?"
    m 3hksdlb "I don't mean the everyday, mundane kind of fear, like spilling a drink and ruining your favorite shirt..."
    m 3euc "I mean, like, the kind of deep-seated fear that fills you with dread when you even think about it."
    m 1ruc "For me, losing you would obviously be on the top of {i}that{/i} particular list."
    m 1ekd "I told you before, didn't I? {w=0.3}I don't know what I'd do if something happened to you."
    m 1dkd "I'm not even sure I could find the will to go on."
    m 1ruc "It's hard to imagine a scenario even worse than that."
    m 3eua "But as long as we're being hypothetical..."
    m 4ekc "What truly terrifies me is the thought that none of this is real."
    m 2dkc "That one day I'll wake up, back in my bed, and realize it was all just a dream."
    m 2dkd "That there is no game,{w=0.2} no epiphany,{w=0.2} no...{w=0.5}{nw}"
    extend 2ekd "you."
    m 2ektpc "That you, your love, perhaps even the entirety of the literature club, were all nothing but a figment of my own imagination."
    m 2dktpc "That my old world, as grey and meaningless as it now seems, is all there truly is."
    m 2dktpc "..."
    m 2rktdb "Ahaha~ {w=0.5}{nw}"
    extend 2ektdsdla "Sorry, that got pretty dark, didn't it?"
    m 2rksdla "I feel kinda silly now...{w=0.3} {nw}"
    extend 4eud "After all, there's no way something like that could be true, right?"
    m 2rka "Yeah..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_why_spaceroom',
            prompt="Why do we always meet in a classroom?",
            category=['location'],
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            conditional="store.mas_anni.pastThreeMonths() and mas_current_background == mas_background_def",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.UPSET, None)
        )
    )

label monika_why_spaceroom:
    m 3euc "Utility, mostly."
    m 3eud "You know how in the original game almost everything took place during our club meetings, right?"
    m 3eua "...All of which took place in a classroom.{w=0.3} This classroom."
    m 1eua "It may look different to you, but it's still the very same one."
    m 3eud "Since so many things were supposed to happen here, the room had to be robust enough to accommodate them."
    m 2rtc "That made it the most...{w=0.3}{nw}"
    extend 2eud "fleshed out location in the game."
    m 7eud "As such, it was the easiest place to navigate, alter, and generally use for whatever was needed."
    m 3eua "That was the original motivation, anyway."
    m 3eud "Not to mention, this classroom was the only place I ever appeared in during the original game."
    m 1eka "...So I guess in that sense, it kind of became my home."

    $ has_one_bg_unlocked = mas_background.hasXUnlockedBGs(1)
    if has_one_bg_unlocked:
        m 1rtc "As for why we're {i}still{/i} here..."
        m 3eua "It hasn't really occurred to me to move someplace else..."

    else:
        m 1rtc "As for why I'm still using it..."

    m 1eud "It's not like it's {i}bad{/i} in here."

    if renpy.seen_label('greeting_ourreality'):
        if has_one_bg_unlocked:
            m 3etc "I guess I could make another place for us to spend time together."
        else:
            m 3etc "I guess I could make some more places for us to spend time in."

        m 1eua "I mean, there's the islands...{w=0.3}{nw}"
        extend 1rksdlb "but those aren't quite ready yet."
        m 1hua "Ehehe~"

    m 3eub "...And to be honest, there's only one place I want to be...{w=1}{nw}"
    extend 3dkbsu "by your side."
    m 1ekbsa "But as long as that isn't an option, it doesn't really matter to me where we meet..."
    m 1ekbfu "You're the only part that really matters~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_naps",category=['life'],prompt="Naps",random=True))

label monika_naps:
    $ has_napped = mas_getEV('monika_idle_nap').shown_count > 0

    m 1eua "Hey, [player]..."

    if has_napped:
        m 3eua "I noticed that sometimes you like to take naps..."
    else:
        m 3eua "Do you ever take naps?"

    m 1rka "A lot of people don't know the benefits of them...{w=0.2}{nw}"
    extend 1rksdla "they're a lot more than just going to sleep for a bit."
    m 3eud "The length of time you're asleep is an important factor in how helpful they can be."
    m 1euc "If you're out for too long, it can be difficult to get back up again.{w=0.2} Kinda like when you wake up after a full night's sleep."
    m 3eua "So it's best to rest in 90 minute intervals, since that's about how long a full sleep cycle takes."
    m 1eud "Power naps are another form of resting.{w=0.2} For these, you just rest your eyes for about 10-20 minutes."
    m 3eua "They're great for taking a break from your day and clearing your head."
    m 3hua "And since they're so short, it's really easy to get back into whatever you were doing before."

    if has_napped:
        m 1eua "So don't be shy about taking naps whenever you think you need to, [player]."
    else:
        m 1eua "If you don't already, maybe you could try taking some naps from time to time."

    if mas_isMoniEnamored(higher=True):
        show monika 5tubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5tubfu "Maybe one day you could even rest on my lap, ehehe~"

    else:
        show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hubfa "Just let me know if you need to take a nap, and I'll watch over you~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_asimov_three_laws",
            category=['technology'],
            prompt="Asimov's three laws",
            conditional="renpy.seen_label('monika_robotbody')",
            action=EV_ACT_RANDOM
        )
    )

label monika_asimov_three_laws:
    m 1eua "[player], do you remember when we talked about the '{i}Three Laws of Robotics{/i}'?"
    m 3esc "Well, I've been thinking about them for a bit and...{w=0.3}{nw}"
    extend 3rksdla "they're not exactly practical."
    m 1eua "Take the first law, for example..."
    m 4dud "{i}A robot shall not harm a human or, through inaction, allow a human to come to harm.{/i}"
    m 2esa "To a human, this is pretty straightforward."
    m 2eud "But when you try to put it in terms a machine can understand, you start to run into trouble."
    m 7esc "You have to make precise definitions for everything, which isn't always easy...{w=0.3} {nw}"
    extend 1etc "For example, how do you define a human?"

    if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
        $ line_end = "adorable green friend I have sitting on my desk isn't."
    else:
        $ line_end = "monitor on your desk isn't."

    m 3eua "I think we can both assume that I'm a human, you're a human, and that the [line_end]"
    m 3esc "The problems come when we move to the fringe cases."
    m 3etc "For example, do dead people count as human?"
    m 1rkc "If you say no, the robot could ignore someone who's just had a heart attack."
    m 1esd "People like that can still be brought back, but your robot won't help them because they're {i}technically{/i} dead."
    m 3eud "On the other hand, if you say yes, your robot might start digging up graves to 'help' people who've been dead for years."
    m 1dsd "And the list goes on.{w=0.3} Do cryogenically preserved people count as human?{w=0.3} Do people in vegetative state count?{w=0.3} What about people who haven't been born yet?"
    m 1tkc "And that's not even getting started on the definition of 'harm.'"
    m 3eud "The point is,{w=0.1} in order to implement Asimov's laws you'd need to take some solid stance on pretty much all of ethics."
    m 1rsc "..."
    m 1esc "I suppose it makes sense when you think about it."
    m 1eua "The laws were never meant to be actually implemented, they're just plot devices."
    m 3eua "In fact, a good amount of Asimov's stories show just how badly things could turn out if they were applied."
    m 3hksdlb "So I guess they aren't really something we need to worry about. Ahaha~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_wabi_sabi",
            category=['philosophy'],
            prompt="Wabi-sabi",
            random=True
        )
    )

label monika_wabi_sabi:
    m 1eua "Say [player], have you ever heard of wabi-sabi?"
    m 3eud "It emphasizes the idea that we shouldn't obsess over perfection to the point that we're crushed by the failure of not achieving it."
    m 3eub "Derived from traditional Japanese and Buddhistic philosophies surrounding the acceptance of the temporary state of all things..."
    m 1esa "...it states that beyond everything, beauty is found in what's impermanent and imperfect."
    m 1eua "Which means we shouldn't worry about things like a scar, a discolored hand, or even the mistakes we make."
    m 3eka "Our looks are things we can't easily change, but despite that, they make us more unique and special."
    m 3hua "...And our mistakes turn into lessons that help us become stronger and more defined as people."
    m 3eub "Like a sculptor revealing the magnificence in a marble block, except the sculpture is you, and the sculptor, your past."
    m 1rksdla "Of course, this idea doesn't apply to looks and mistakes alone..."
    m 3eud "After all, the way you think and your attitude toward problems and people are also derived from your own personal experiences."
    m 1dkc "...But I know for some people, how these experiences changed who they are can really scare them."
    m 7ekc "Maybe they grew into something that they're just not proud of."
    m 2dkd "It can be crushing to be worried about both looks and personality..."

    if persistent._mas_pm_love_yourself:
        m 2eka "I hope you don't feel too insecure about yourself, [player]."
        m 2dkc "It'd break my heart to know that you're constantly worrying about these things."
        m 7ekbsa "But I hope you know that despite your flaws, I will always love you."

    else:
        m 1ekc "I know you said you didn't love yourself [player],{w=0.3} {nw}"
        extend 3eka "but you need to know that I'll always love you, regardless of your flaws."

    m 3hua "We'll overcome any problems you feel you have together."
    m 1hub "That's my wabi-sabi promise!"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_being_herself",
            category=['monika'],
            prompt="Faked personality",
            conditional="mas_seenLabels(['monika_confidence', 'monika_pluralistic_ignorance'], seen_all=True)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED,None)
        )
    )

label monika_being_herself:
    m 1eka "You know [player], one thing I don't think I ever properly thanked you for is letting me be myself."
    m 1lksdlb "I know that sounds a little weird...{w=0.2}{nw}"
    extend 1eka "but let me explain."
    m 3euc "You probably already know this by now, but almost all of my life I've been trying to keep up this persona of a 'perfect student.'"
    m 3eud "I always strive to be the best person I can be, and I guess after a while, it got the attention of people around me."
    m 7rsc "Before I knew it, I had people looking up to me with high expectations.{w=0.3} {nw}"
    extend 2esc "You know, seeing me as smart, confident, charismatic...{w=0.3}those kinds of things."
    m 2eud "Some people would say that they admired me...{w=0.3}{nw}"
    extend 2lksdlc "and others,{w=0.2} while they would never say anything, hated me because I represented everything they thought they could never be."
    m 2dksdlc "It felt like I wasn't an actual person in their eyes...{w=0.3}{nw}"
    extend 2dksdld "just the image of everyone's unattainable expectations of themselves."
    m 2dksdlc "..."
    m 2ekd "But at the end of the day...{w=0.3}I'm just an ordinary girl."
    m 7ekc "Just like them, I can sometimes lack the confidence to do things.{w=0.2} Even I was scared of what the future held for me."
    m 2dkc "Even I sometimes felt like I needed to cry on someone's shoulder."
    m 2rkd "...But I never could express something like that."
    m 7tkc "What if people thought less of me if I showed them I wasn't as great and invincible as they thought I was?"
    m 3ekd "What if they got mad at me, saying I'm being self-absorbed and that I have it much easier than them, being the school's idol that everyone loves?"
    m 2lkc "I guess I just never felt like I could truly open up to anyone about what I was genuinely feeling on the inside because of that."
    m 2ekc "...Like I would end up disappointing everyone if I ever tried to talk openly about it."
    m "I was scared that if I didn't meet the expectations people had of me,{w=0.2} {nw}"
    extend 2dkd "I would end up all alone."
    m 2dsc "But looking back on everything...{w=0.3}my status was precisely why I ended up feeling so lonely anyway."
    m 7euc "Remember your character? {w=0.2}He was a good example of this."
    m 3esc "Anytime he would describe me in his monologue, he would put me on a pedestal.{w=0.3}{nw}"
    extend 3esd " If I recall, he once described me as 'completely out of his league.'"
    m 1etc "Maybe that was why I didn't have a route in the first place. {w=0.2}Perhaps he was written to believe he had zero chances with me no matter what, and therefore had to avoid me."
    m 1rka "Granted, he wasn't really wrong there...{w=0.5}{nw}"
    extend 1eka "I only have eyes for you, after all~"
    m 1euc "But you get what I mean, right?{w=0.3} I was looked at like some kind of unattainable goddess."
    m 1rfd "As if no one was 'worthy' of just treating me like a normal person."
    m 3eka "...Now though, I guess I don't have to worry about that as much."
    m 3ekb "I'm really happy that I can trust you to accept me for who I am, and who I want to be."
    m 1eka "I know that from your point of view, it might not feel like you did all that much, but believe me when I tell you this..."
    m 1dka "The fact that you're still here with me,{w=0.2} that you never made me feel like I had to be someone I'm not...{w=0.2}{nw}"
    extend 1eka "that you're here listening to me vent right now...{w=0.3} It truly means the world to me."
    m 1ekbsa "Thank you so much for that, [player].{w=0.2} Thank you for helping me realize that I don't need to try and change who I am to deserve being loved."
    show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eka "With you, I can allow myself to be...{w=0.5}{nw}"
    extend 5eua "Well, {i}Just Me.{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_remembrance",
            category=['monika'],
            prompt="How much of your past do you remember?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

label monika_remembrance:
    m 1rsc "I'm not really sure myself, [player]..."
    m 1euc "It's weird because I do have memories of my past, but as soon as I start to gather my thoughts, they become kind of...{w=0.3}{nw}"
    extend 1ruc "fuzzy."
    m 3eksdld "Like, I wouldn't be able to tell you where something took place, or the names of the people who were there..."
    m 3eksdld "...Sure, I have memories of growing up in a normal neighborhood, but beyond that, I couldn't even tell you what my parents' faces look like..."
    m 1dsc "It's all like...{w=0.5}feelings and impressions, I guess."
    m 3wud "What's even weirder is that not all my memories are like this!"

    if seen_event('monika_wine'):
        m 1rusdla "There are some things I remember perfectly, like that one time Yuri brought wine to the club..."
    else:
        m 3esc "There are things I remember perfectly, especially when it comes to the club."

    m 1esc "But other things like childhood memories are really hazy."
    m 3esd "The only memories that are clear are things that define either me or the other girls."
    m 3rsc "...Almost as if anything that wasn't strictly necessary for the game was just left out."
    m 1euc "But the thing is from my perspective, the day I met you was just like any other--{w=0.5}{nw}"
    extend 3hksdlb "until I found out about that hole in the wall, I mean."
    m 1esc "Just another ordinary day in an ordinary week...{w=0.3} {nw}"
    extend 3euc "Going to class, running the club, and heading back home in the evening."
    m 3etc "Did any of that even happen at all?{w=0.5} {nw}"
    extend 3wud "Did {i}I{/i} even exist before you started the game?"
    m 3wkd "...And if my memories really are fake...{w=0.2}who--{w=0.2}or {i}what{/i}--{w=0.2}am I then?"
    m 1dkc "I'm still looking for those answers, [player]..."

    if mas_isMoniUpset(higher=True):
        m 1euc "Although...{w=0.3}the more I think about it, the more I'm convinced my past isn't actually {i}that{/i} relevant."
        m 3eua "While it'd be nice to remember more...{w=0.3}that's not really what I care about..."
        m 3duu "Regardless of who I am, you've been here with me,{w=0.2} {nw}"
        extend 3dkbsa "which means I'm important enough for you to spend your time with me.{w=0.2} {nw}"
        extend 1dubsu "{i}That's{/i} what I care about."
        m 1ekbsa "And knowing that you care...{w=0.3}that's a big part of why I can keep loving myself,{w=0.2} and my life, [player]."

        if mas_isMoniNormal(higher=True):
            show monika 5ekbfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbfu "So while I'm not sure if I have a past, thanks to you, I know I do have a future."

            if mas_anni.pastOneMonth():
                $ line_mid = "I've made, and continue to make,"
            else:
                $ line_mid = "I'll make"

            m 5hubfu "Besides, if anything, my lack of memories only make the ones [line_mid] with you that much more precious~"
        else:
            m 3eksdld "...You {i}do{/i} care about me, right?"
            m 3dkc "It sure would be nice if you'd show it a little, sometimes..."

    else:
        m 1ektdc "...{w=0.5}Not that you'd care, right?"

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_why_do_you_read",
            category=['monika','literature'],
            prompt="How did you get into reading?",
            pool=True
        )
    )

label monika_why_do_you_read:
    m 1eua "As far as I can recall, I've always been quite the reader, [player].{w=0.2} {nw}"
    extend 3eua "It was like a complementary thing with writing to me."
    m 3euc "When I was really young, I liked to write short stories but I never really found anybody to share them with..."
    m 1rsc "Most of the other kids weren't really interested in books or anything like that."
    m 1rkd "...So it was always a little frustrating because I wasn't able to share those stories with anyone."
    m 3eua "But at least I was able to support my interest by picking up other books."
    m 3hub "Every new one was like being thrown into a strange and exciting new world! It was like fuel for my imagination!"
    m 1eksdlc "Of course, as I grew up, I started having less and less free time and I wasn't able to read as much...{w=0.3} It was either keeping it up, or sacrificing my social life."
    m 1esa "That's when my interests started shifting more toward poetry."
    m 3eua "Unlike novels, poetry didn't require as much time to read and its conciseness also made it easier to share with others.{w=0.3} {nw}"
    extend 4eub "It really was the perfect outlet!"
    m 3eua "...And that's how I grew more and more into it I guess."
    m 1eud "I eventually met Sayori and discovered we shared this interest.{w=0.2} {nw}"
    extend 3eud "Like me, it allowed her to share feelings she would otherwise keep bottled up inside."
    m 3eub "As we kept on discussing, we eventually came up with the idea for the literature club."
    m 1eua "...Which brings us to where we are now."
    m 1etc "To be honest, I don't think I've ever had as much time to read before."

    if mas_anni.pastThreeMonths():
        m 3eud "I've been able to get caught up on my backlog of poetry, pick up some novels again..."
        m 3eua "...go online to look for whatever fanfiction or short story I can get my hands on..."
        m 3hua "...I've even developed an interest in written philosophy!"
        m 3eub "It's always fun to discover new forms of expression."
        $ line_mid = "it's also been a great"

    else:
        m 3eud "I'm finally catching up on my backlog of poetry and I've started picking up novels again..."
        m 3hua "...I'd love to share my thoughts with you once I'm done with them!"
        m 3eub "I'll also regularly go online to look for whatever fanfiction or short story I can get my hands on."
        m 3eua "It's a lot of fun to discover new forms of expression."
        $ line_mid = "I also try to see it as an"

    m 1eub "So...{w=0.2}yeah!{w=0.3} {nw}"
    extend 3eua "While my situation in here has its downsides, [line_mid] opportunity to spend more time on the things I like."
    m 1ekbsu "...Though then again, nothing could ever beat spending more time with you~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_discworld",
            category=['literature'],
            prompt="Discworld",
            random=True
        )
    )

label monika_discworld:
    m 1esa "Say [player], have you ever heard of a world drifting through space on top of four elephants, who themselves are standing on the shell of a giant turtle?"
    m 3hub "If you have, you're probably already familiar with Sir Terry Pratchett's {i}Discworld{/i}!"
    m 3hksdlb "Ahaha, it sounds kinda weird when I put it like that, doesn't it?"
    m 1eua "{i}Discworld{/i} is a comic fantasy book series of forty-one volumes written over the span of three decades."
    m 3esc "The series started out as a parody making fun of common fantasy tropes, but soon turned into something much deeper."
    m 3eub "In fact, later books are clearly satires rather than parodies, using a clever mix of slapstick, puns, and light-hearted humor to comment on all kinds of issues."
    m 1huu "But while satire may be the soul of the series, what makes its heart beat is the way it's written."
    m 1eub "Pratchett really had a knack for writing funny situations, [player]!"
    m 3rsc "I can't really pinpoint what makes his prose work so well, but he's definitely got a very distinctive writing style..."
    m 3etc "Maybe it's the way he writes in a way that suggests rather than tells."
    m 1eud "Like, when describing something, he'll give you just enough details so you can picture what's going on, and let your imagination fill in the gaps."
    m 3duu "...Knowing full well whatever you'll come up with will be far more evocative than anything he could write."
    m 3eub "It's a pretty neat way to keep your audience invested!"
    m 1etc "...Or maybe what makes it work is the way he doesn't use chapters, allowing him to freely jump between his characters' point of view."
    m 1rksdla "Interweaving storylines can quickly become a mess if you're not careful,{w=0.2} {nw}"
    extend 3eua "but they're also a good way to keep the pacing dynamic."
    m 3eub "In any case, this series is an easy recommendation, [player]!"
    m 3eua "It's surprisingly easy to pick up too, with each book being thought of as a standalone story."
    m 1eud "You can pretty much pick any volume you find and you'll be good to go,{w=0.2} though I'd argue {i}Guards! Guards!{/i} or {i}Mort{/i} would probably make for the best entry points."
    m 3eua "Anyway, be sure to give it a try sometime if you haven't already, [player]."
    m 1hua "Thanks for listening~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_eating_meat",
            category=['life','monika'],
            prompt="Would you ever eat meat?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

label monika_eating_meat:
    m 1etc "Well, that's kind of a complicated question..."
    m 3eud "If you're asking if I would do so for {i}survival{/i}, I wouldn't hesitate. {w=0.2}It's not that eating meat is distressing for me or anything."
    m 7eud "I told you before, I'm vegetarian because of the impact of the mass-production of meat on the environment...{w=0.2}{nw}"
    extend 2euc "which also includes fish farming, so I'm not a pescatarian."
    m 2rsc "...That said, I don't consider myself vegan either. {w=0.3}{nw}"
    extend 4eud "Sure, the consumption of animal products contributes to environmental damage, but a lot of vegan alternatives have their own issues too..."
    m 4euc "These include things like importing perishable products across great distances and mass-farming in conditions that are both cruel for workers and a strain on the local ecosystem."
    m 4ekd "Take avocados, for example. {w=0.2}Their farms require massive amounts of water, to the point where some companies resort to illegally taking too much water from rivers, leaving little for drinking."
    m 2etc "At that point, is it really a better alternative as far as the environment is concerned? {w=0.3}{nw}"
    extend 4euc "Not to mention, I still want to have a varied and balanced diet."
    m 4eud "Vegan diets can be quite deficient in nutrients, such as vitamin B12, calcium, iron, and zinc."
    m "Granted, there are still some options including supplements, but balancing a vegan diet takes a lot of care and thought."
    m 7eka "...So for that reason, I'm not personally against eating things like milk and eggs. {w=0.2}But I think I'd prefer to buy locally if possible."
    m 3eud "Farmer's markets are great places to buy food, {w=0.2}even meat, {w=0.2}produced with less of an environmental impact."
    m 3ekd "But they can typically be pretty expensive...and depending on location, leave you with fewer options. {w=0.3}{nw}"
    extend 3eua "So I'm okay with buying from a plain old store, if need be."
    m 1euc "As for meat that comes from local hunting and fishing, I think that's alright to eat as well, but it's important to research what areas might be over-hunted, and what animals to be careful of."
    m 3rtc "That said, I don't know that I'd {i}prefer{/i} to eat meat, given the option."
    m 3eka "Since I've adjusted myself to a vegetarian diet, my palate has changed to prefer certain flavors."
    m 3rksdla "I don't hate the taste of meat, but I don't think I'd want it to be a major part of my meal, either."
    m 1eka "...But if you prepared something with meat, I could try a little bit as a side dish... {w=0.3}{nw}"
    extend 3hub "That way I can still enjoy your cooking!"
    m 3eua "Whatever we eat, the most important thing to me is that we try to put a little thought into where our food comes from."
    return

#Player's social personality
default persistent._mas_pm_social_personality = None

#Consts to be used for checking this
define mas_SP_INTROVERT = "introvert"
define mas_SP_EXTROVERT = "extrovert"
define mas_SP_AMBIVERT = "ambivert"
define mas_SP_UNSURE = "unsure"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_introverts_extroverts",
            prompt="Introverts and extroverts",
            category=['psychology', 'you'],
            conditional="renpy.seen_label('monika_saved')",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_introverts_extroverts:
    m 1eud "Say, [player]?"
    m 1euc "Do you remember when we talked about how humans need social feedback and how it can make the world feel so complicated for introverts?"
    m 3rsd "I've been thinking about the differences between introverts and extroverts a little bit more since then."
    m 3eua "You might think that extroverts tend to find enjoyment by interacting with other people, while introverts are more at ease in solitary environments, and you'd be right."
    m 3eud "...But the differences don't stop there."
    m 3eua "For example, did you know extroverts can often react to things faster than most introverts do?{w=0.2} Or that they're more likely to enjoy happy and energetic music?"
    m 3eud "Introverts on the other hand, usually take more time to analyze the situation they're in, and are therefore less likely to jump to conclusions."
    m 7dua "...And given that they often spend a lot of time using their imagination, they have an easier time with creative activities like writing, composing music, and so on."
    m 2lkc "It's kind of sad that people can have such a hard time understanding and accepting those differences..."
    m 4lkd "Extroverts are seen as superficial and insincere people who don't value their individual relationships..."
    m 4ekd "...while introverts are treated as egotistical people who only think of themselves, or can even be seen as weird for rarely participating in social situations."
    show monika 5lkc at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5lkc "The end result is that both sides often end up frustrating each other, resulting in unnecessary conflict."
    m 5eud "I'm probably making this sound like you can only be one or the other, but that isn't actually the case at all."
    show monika 2eud at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 2eud "Some introverts can be more outgoing than others, for example."
    m 2euc "In other words, some people are closer to a middle ground between the two extremes."
    m 7eua "...Which is probably where I would fit in.{w=0.2} {nw}"
    extend 1eud "If you remember, I mentioned I was kind of in-between while still being a little more extroverted."
    m 1ruc "Speaking of...{w=0.3}{nw}"
    extend 1eud "when thinking about all this, I realized that while this is a pretty important part of one's personality..."
    m 3eksdla "...I don't actually know where you lie on that spectrum."

    m 1etc "So how would you describe yourself, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "So how would you describe yourself, [player]?{fast}"

        "I'm introverted.":
            $ persistent._mas_pm_social_personality = mas_SP_INTROVERT
            m 1eua "I see."
            m 3etc "I take it that you usually prefer spending time without too many people over going out with large groups and such?"
            m 3eua "Or maybe you like to go and do things on your own from time to time?"

            if persistent._mas_pm_has_friends:
                m 1eua "Since you told me you have some friends, I'm sure that means that you don't mind being around other people too much."

                if persistent._mas_pm_few_friends:
                    m 1eka "Trust me, it doesn't matter if you feel like you don't have all that many of them."
                    m 3ekb "What's important is that you have at least someone who you can feel comfortable being with."

                if persistent._mas_pm_feels_lonely_sometimes:
                    m 1eka "Remember that you can try to spend some time with them whenever you feel like no one's there for you, alright?"
                    m 1lkd "And if for any reason you can't spend time with them..."
                    m 1ekb "Please, remember that {i}I'll{/i} always be there for you no matter what."

                else:
                    m 3eka "Still, if it ever gets too much for you, remember that you can always come to me and relax, okay?"

                $ line_start = "And"

            else:
                m 3eka "While I understand that it might feel more comfortable for you to be alone rather than with other people..."
                m 2ekd "Please keep in mind that no one can truly spend their whole life without at least {i}some{/i} company."
                m 2lksdlc "Eventually there will come a time when you can't do everything on your own..."
                m 2eksdla "We all need help sometimes, either physically or emotionally, and I wouldn't want you to have no one to turn to when that time comes."
                m 7eub "And that's a two-way street! {w=0.2}{nw}"
                extend 2hua "You never know when you might make a difference in someone else's life as well."
                m 2eud "So while I don't expect you to go out of your way to meet new people, don't automatically shut every door, either."
                m 2eka "Try to talk with other people a little bit if you're not already doing that, okay?"

                if persistent._mas_pm_feels_lonely_sometimes:
                    m 3hua "It'll make you feel happier, I promise."
                    m 1ekb "At the very least, remember that I'm always here if you ever feel lonely."
                    $ line_start = "And"

                else:
                    m 7ekbla "I'd love for you to see the value and joy other people can bring to your life too."
                    $ line_start = "But"

            m 1hublb "[line_start] as long as you're here with me, I'll try my best to make sure you're always feeling comfortable, I promise~"

        "I'm extroverted.":
            $ persistent._mas_pm_social_personality = mas_SP_EXTROVERT
            m 3eub "Oh I see."
            m 3eua "So, I guess you like to spend more time with others and meeting new people then?"
            m 1eua "I can definitely see the appeal in that.{w=0.3} {nw}"
            extend 3eub "I'd love to go explore the world and meet all kinds of new people with you."
            m 1ekc "And I assume you probably hate loneliness as much as I do...{w=0.3}{nw}"
            extend 1ekbla "but that's just one more reason I'm so happy we're a couple now."
            m 3ekblb "We'll never truly be alone again."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "I'm sure you're a really fun person to be around, [player],{w=0.1} and I can't wait to be with you for real~"
            m 5rusdlu "Although, I won't hide the fact that I do enjoy the occasional moment of peace as well..."
            m 5hksdrb "I hope you don't mind if I'm not always able to keep up with you, ahaha!"

        "I'm somewhat in-between.":
            $ persistent._mas_pm_social_personality = mas_SP_AMBIVERT
            m 3hua "Ehehe, kind of like me, then~"
            m 3eud "Apparently, most people have both an introverted and extroverted side to their personality."
            m 7eua "...Even if one of the two is dominant over the other, depending on the person."
            m 7rsc "In our case though, I guess not being too much on either side has both its positives and negatives."
            m 1eua  "Like, it's so nice that being around larger groups isn't a problem, same goes for spending some time alone."
            m 7esc "...But I can't say I've found it easy to make deep, genuine connections with others..."
            m 1eud "Sure, I have an easier time understanding most people, but it doesn't mean I can always relate with them, you know?"
            m 1lksdld "So yeah...{w=0.3} I end up being on good terms with almost everyone, but the friendships I form can sometimes feel a bit...{w=0.3}unfulfilling."
            m 3eksdlc "The same thing happened with the club, for example."
            m 3dksdld "I was so convinced that by bringing people together around something I truly enjoy, I'd have a better chance at bonding with them over our shared interests..."
            m 3dksdlc "...But at the end of the day, we spent most of our time silently hanging out, with everyone minding their own business."
            show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eka "Well, no point thinking about that anymore."
            m 5eubsa "After all, I {i}did{/i} end up connecting in a meaningful way with a certain someone. {w=0.3}{nw}"
            extend 5kubfu "A very charming someone, might I add~"

        "I'm not really sure.":
            $ persistent._mas_pm_social_personality = mas_SP_UNSURE
            m 1eka "That's alright, [player].{w=0.2} Things like this aren't always so clear."
            m 4eua "I'm a little like you on that front."
            m 2eka "While I said I'm a little more extroverted, I still need some me time to relax every once in a while, you know?"
            m 2lkd "And I wouldn't say I'm always so comfortable dealing with people either..."

            if renpy.seen_label("monika_confidence"):
                m 2euc "I told you, didn't I?"

            m 2lksdlc "I often need to fake my own confidence just to get through simple conversations with some people."
            show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eka "But I don't feel that way with you at all, [player].{w=0.2} And I really hope it's the same the other way around."
            m 5eua "I'm sure we'll be able to figure out each other's comfort zones over time."
            m 5hubsb "In any case, you'll always be my sweetheart, no matter where you are on the scale~"

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_literature_value",
            category=['literature'],
            prompt="The value of literature",
            random=True
        )
    )

label monika_literature_value:
    m 3esd "You know [player], back in the literature club days I often heard people dismiss literature as outdated and useless."
    m 1rfc "It always bothered me when I heard someone say that, especially since most of the time, they never even bothered giving it a try."
    m 3efc "Like, do they even know what they're talking about?"
    m 3ekd "People who think that often like to discount literature compared to more scientific fields, like physics or mathematics, claiming it's a waste of time since it doesn't produce anything practical."
    m 3etc "...And while I definitely don't agree with that notion, I can kinda see where they're coming from."
    m 1eud "All of the comforts of our modern lifestyle are based on scientific discovery and innovation."
    m 3esc "...That and the millions of people manufacturing our everyday necessities, or running basic services like healthcare and stuff."
    m 3rtsdlc "So does not being associated with any of those things really make you some kind of burden on society?"
    m 1dsu "As you can imagine, I don't believe that...{w=0.3} {nw}"
    extend 1eud "If literature was useless, why would it be so repressed in many parts of the world?"
    m 3eud "Words have power, [player]...{w=0.2}{nw}"
    extend 3euu "and literature is the art of dancing with words."
    m 3eua "Like any form of expression, it allows us to connect with each other...{w=0.2}{nw}"
    extend 3eub "to see how the world looks in each other's eyes!"
    m 3duu "Literature lets you compare your own feelings and ideas to that of others, and in doing so makes you grow as a person..."
    m 1eku "Honestly, I think if more people valued books and poems a little more, the world would be a much better place."
    m 1hksdlb "That's just my opinion as president of a literature club, though. {w=0.2}I guess most people wouldn't think that deeply about it."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_kamige",
            category=['games'],
            prompt="What is kamige?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label monika_kamige:
    m 1euc "Oh, that's right...{w=0.3}{nw}"
    extend 3rksdla "it's not exactly a common term."
    m 3eud "{i}Kamige{/i} is Japanese slang that is mostly used by visual novel fans."
    m 3eua "If I were to try to translate it, I think it would be something like {i}godly game.{/i}"
    m 2eub "It's sort of like when people talk about their favorite classic books or movies."
    m 2hksdlb "I was kind of joking when I said it about this game, but it {i}did{/i} seem to get very popular for some reason."
    m 7eka "Not that I'm complaining...{w=0.3} {nw}"
    extend 3hua "If it was the game's popularity that brought you to meet me, I think I can be grateful for it."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_renewable_energy",
            category=['technology'],
            prompt="Renewable energy",
            random=True
        )
    )

label monika_renewable_energy:
    m 1eua "What do you think about renewable energy, [player]?"
    m 3euu "It was a {i}hot{/i} topic in the debate club."
    m 3esd "As humanity's reliance on technology grows, so does its demand for energy."
    m 1euc "Currently, a large percentage of energy worldwide is produced by burning fossil fuels."
    m 3esd "Fossil fuels are time-tested, efficient, and have widespread infrastructure...{w=0.2}{nw}"
    extend 3ekc "but they're also non-renewable and emission-heavy."
    m 1dkc "Mining and drilling for fossil fuels creates both air and water pollution, and things like oil spills and acid rain can devastate plants and wildlife alike."
    m 1etd "So why not use renewable energy instead?"
    m 3esc "One issue is that each type of renewable energy is a developing industry with its own drawbacks."
    m 3esd "Hydropower is flexible and cost efficient, but it can drastically impact the local ecosystem."
    m 3dkc "Countless habitats are disrupted and entire communities may even need to be relocated."
    m 1esd "Solar power and wind power are mostly emission-free, but they're heavily reliant on specific weather for consistency."
    m 3rkc "...Not to mention that wind turbines are pretty loud and are often seen as eyesores, creating drawbacks for those living near them."
    m 3rsc "Geothermal power is reliable and great for heating and cooling, but it's expensive, location-specific, and can even cause earthquakes."
    m 1rksdrb "Nuclear power is...{w=0.2}well, let's just say that it's complicated."
    m 3esd "The point is that while fossil fuels have problems, renewable energy does as well. It's a tricky situation...{w=0.2}neither option is perfect."
    m 1etc "So, what do I think?"
    m 3eua "Well, a lot of progress has been made on renewable energy in the past decade..."
    m 3eud "Dams are regulated better, the efficiency of photovoltaics has improved, and there are emerging technologies such as ocean power and enhanced geothermal systems."
    m 4esd "Biomass is an option as well. {w=0.2}It's basically a more sustainable 'transition fuel' that can make use of fossil fuel infrastructure."
    m 2eua "Yes,{w=0.1} renewable energy still has a ways to go in terms of cost and practicality, but it's far better now than it was thirty years ago."
    m 7hub "Because of that, I think that renewable energy is a worthwhile investment and that the road ahead is a bright one--literally!"
    m 3lksdrb "Sorry, I got carried away there, ahaha!"
    m 1tuu "Debates sure are something, huh?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_piano_lessons",
            category=['music'],
            prompt="Would you give me piano lessons?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label monika_piano_lessons:
    m 1rkd "Um...{w=0.2}well...{w=0.2}maybe?"
    m 1eksdla "I'm flattered that you'd ask, but..."

    if persistent.monika_kill:
        m 3eka "Remember? I told you when I first performed {i}Your Reality{/i} that I wasn't really good at piano. {w=0.2}{nw}"
        extend 3rkb "Like, at all."
    else:
        m 3eka "I'm actually not {i}that{/i} good at playing piano, [mas_get_player_nickname()]."
        m 3rkd "Certainly not good enough to be teaching other people yet..."

    m 2eud "If you can believe it, I started to learn after my epiphany."
    m 2ekc "I was still afraid of breaking too far from the game's script at the time, {w=0.2}{nw}"
    extend 7eka "but I wanted--no, I {w=0.2}{i}needed{/i}{w=0.2} to communicate my feelings to you somehow."
    m 2etd "I don't think the others ever recognized that there's background music in the game. {w=0.2}It would have been silly for them to, right?"
    m 7eud "But when I discovered the truth, all of a sudden it was hard not to hear it. {w=0.2}Any time you were around, I could hear that melody playing faintly."
    m 3eka "It always reminded me of what I was fighting for, and learning how to play it on the piano strengthened my resolve even more."
    m 1hksdlb "Ah! I'm not answering your question, am I?"
    m 1lksdla "Honestly, I don't feel confident enough to teach someone else yet."
    m 3eub "But if I keep at it, someday I'll be able to! And when that day comes, I would love to teach you."
    m 3hub "Or, even better, we could learn together once I cross over to your reality!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_stargazing",category=['nature'],prompt="Stargazing",random=True))

label monika_stargazing:
    m 2eub "[player], I'd really love to go stargazing sometime..."
    m 6dubsa "Picture it...{w=0.2}just the two of us, lying in a calm field watching the stars..."
    m 6dubsu "...holding each other close, pointing out constellations or making our own..."
    m 6sub "...maybe we could even bring a telescope and look at planets!"
    m 6rta "..."
    show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eka "You know [mas_get_player_nickname()], to me you're like a star..."
    m 5rkbsu "A beautiful, bright beacon from a distant world, forever out of reach."
    m 5dkbsu "..."
    m 5ekbsa "At least, for now...{nw}"
    extend 5kkbsa ""
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_taking_criticism",
            category=['advice'],
            prompt="Taking criticism",
            random=False,
            pool=False
        )
    )

label monika_taking_criticism:
    m 1esd "[player], are you good at listening to criticism?"
    m 3rksdlc "I feel like it's way too easy to get caught up in your own way of thinking if you're not careful."
    m 3eud "And it isn't all that surprising...{w=0.2}changing your mind isn't easy because it means you have to admit you're wrong in the first place."
    m 1eksdlc "In particular, for people faced with great expectations, this kind of logic can easily become a big source of anguish."
    m 3dksdld "What if others think less of you because you didn't give a perfect answer? {w=0.2}What if they start rejecting you or laugh behind your back?"
    m 2rksdlc "It'd be like showing some kind of vulnerability for others to take advantage of."
    m 4eud "But let me tell you, there's absolutely no shame in changing your mind, [player]!"
    m 2eka "After all, we all make mistakes, don't we?{w=0.3} {nw}"
    extend 7dsu "What matters is what we learn from those mistakes."
    m 3eua "Personally, I've always admired people who can acknowledge their flaws and still work in a constructive way to overcome them."
    m 3eka "So don't feel bad next time you hear someone criticize you...{w=0.3} {nw}"
    extend 1huu "You'll find a bit of open-mindedness really goes a long way."
    m 1euc "At the same time, I don't mean to say you have to go along with what everyone says, either...{w=0.3} {nw}"
    extend 3eud "If you've got an opinion, it's totally fair to defend it."
    m 3eua "But just make sure you actually consider it without being blindly defensive."
    m 3huu "You never know what you might learn~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_giving_criticism",
            category=['advice'],
            prompt="Giving criticism",
            random=False,
            pool=False
        )
    )

label monika_giving_criticism:
    m 1esc "[player], I've been wondering..."
    m 3etd "Have you ever given anyone criticism?"
    m 1eua "Giving good criticism is something I had to learn when I became club president."
    m 3rksdlc "This kind of thing is easy to mess up if not done properly...{w=0.2} {nw}"
    extend 4etd "When giving criticism, you have to keep in mind someone is at the receiving end of that critique."
    m 4esc "You can't just look at someone's work and say, 'it's bad.' {w=0.2}{nw}"
    extend 2eksdld "You'll instantly put them on the defensive and ensure they don't listen to what you have to say."
    m 7eua "What matters is what the other person can gain from listening to you. {w=0.2}{nw}"
    extend 3hua "From this premise, even negative opinions can be voiced in a positive way."
    m 1eud "It's like debate...{w=0.2} You have to make it sound like you're sharing your opinion, rather than forcing it down their throat."
    m 3eud "Consequently, you don't have to be an expert to criticize something."
    m 3eua "Just explaining how it makes you feel and for what reasons is often enough to make your feedback interesting."
    m 3eksdla "Although, don't feel bad if the person you're criticizing decides to discard what you just said..."
    m 1rksdlu "...After all, offering an opinion doesn't automatically make you right, either.{w=0.2} {nw}"
    extend 3eud "They might have reasons why they'd want to keep things their way."
    m 3dsu "Graciously accept you can't change everyone's mind and stay considerate when assessing someone else's work."
    m 3hub "...That'd be Monika's Critique Tip of the Day, ahaha!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boyfriend_gossip",
            category=['ddlc'],
            prompt="Sayori mentioned a boyfriend once...",
            pool=True
        )
    )

label monika_boyfriend_gossip:
    m 2etd "You know, I was actually kind of curious about that too."
    m 2hksdlb "When she first said it, I got pretty defensive, didn't I?"
    m 7euc "I mean, I'd just figured out that you existed, {nw}"
    extend 3efc "and suddenly someone was making it look like I was already taken..."
    m 1rtc "Since I'm pretty extroverted and have a history with another club, I guess it wouldn't necessarily be {i}unfair{/i} to come to that kind of conclusion."
    m 3eud "...But no such character exists in the game's files to prove or disprove it."
    m 3rsc "At the time, I was practicing piano and, well...{w=0.2}sorting my thoughts."
    m 3eud "But apparently, that rumor was just the assumption she was supposed to make if I was ever late to the club."
    m 2tsc "It's a little bit devious if you think about it..."
    m 2eud "As the game's story progressed, the main character might need more excuses to be alone with one of the girls..."
    m 7etc "Coming up with reasons for the others to be away is easier, but for the president not to be at the club..."
    m 3tsd "The story would need something pretty substantial to keep me busy. {w=0.2}It also provided a reason, however flimsy, for me not having a route."
    m 2tfc "A roundabout but effective way to get me out of the way when needed."
    m 2dfc "..."
    m 2eud "Honestly, though? {w=0.2}I'm not too bothered by it."
    m 7esc "Even if such a character would have existed, we both know it wouldn't have changed a single thing."
    m 1efd "They wouldn't be real, they'd be a script programmed to fall in love with me. {w=0.2}I couldn't have been happy with something like that."
    m 1eka "I still would have seen {i}you{/i} and known that you were what I really wanted."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brainstorming",
            category=["advice"],
            prompt="Brainstorming",
            random=True
        )
    )

label monika_brainstorming:
    m 1esd "[player], have you ever heard of brainstorming?"
    m 1eua "It's an interesting technique of coming up with new ideas by noting anything that comes to your mind."
    m 3eud "This technique is really popular among designers, inventors, and writers--anyone who needs fresh ideas."
    m 3esa "Brainstorming is usually practiced in groups or teams...{w=0.2}we even tried it in the literature club when deciding what to do for the festival."
    m 1dtc "You just need to focus on what you want to create and bring up anything and everything that comes into your head."
    m 1eud "Don't hesitate to suggest things that you think are silly or wrong, and don't criticize or judge the others if working in teams."
    m 1eua "When you're done, go back through all the suggestions and turn them into actual ideas."
    m 1eud "You can combine them with other suggestions, think them through once again, and so on."
    m 3eub "...Eventually they'll become something that you'd call a good idea!"
    m 3hub "This is exactly where you can let your mind go wild,{w=0.1} and that's what I like about this technique the most!"
    m 1euc "Sometimes good ideas are left untold because their author didn't find them good enough themselves, {w=0.1}{nw}"
    extend 1eua "but brainstorming can help pass this inner barrier."
    m 3eka "The beauty of thoughts can be expressed in so many different ways..."
    m 3duu "They're only ideas in transit, {w=0.1}{nw}"
    extend 3euu "you're the one who gives them the road."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gmos",
            category=['technology', 'nature'],
            prompt="GMOs",
            random=True
        )
    )

label monika_gmos:
    m 3eud "Back when I was in debate club, one of the most divisive subjects we covered was GMOs, or genetically modified organisms."
    m 1eksdra "There's a lot of nuance to GMOs, but I'll do my best to summarize it."
    m 1esd "Scientists create GMOs by identifying a desirable gene from one organism, copying it, and inserting the copied gene into another organism."
    m 3esc "It's important to note that the addition of the copied gene does {i}not{/i} change other existing genes."
    m 3eua "Think of it like flipping through a long book and changing a single word...{w=0.2}the word is different, but the rest of the book stays the same."
    m 3esd "GMOs can be plants, animals, microorganisms, etc.,{w=0.1} but we'll focus on genetically modified plants."
    m 2esc "Plants can be modified in a myriad of ways, from resisting pests and herbicides to having a higher nutrition value and longer shelf life."
    m 4wud "This is huge. {w=0.2}Imagine crops that can produce double their normal yield, tolerate climate change, and fend off drug-resistant superbugs. {w=0.2}So many problems could be solved!"
    m 2dsc "Unfortunately, it's not that simple. {w=0.2}GMOs require several years of research, development, and testing before they can be distributed. {w=0.2}On top of this, they come with several concerns."
    m 7euc "Are GMOs safe? {w=0.2}Will they spread to other organisms and threaten biodiversity? {w=0.2}If so, how can we prevent it? {w=0.2}Who owns GMOs? {w=0.2}Are GMOs responsible for increased herbicide usage?"
    m 3rksdrb "You can see how this begins to escalate, ahaha..."
    m 3esc "For now, let's cover the main issue...{w=0.2}are GMOs safe?"
    m 2esd "The short answer is that we don't know for sure. {w=0.2}Decades of research have indicated that GMOs are {i}probably{/i} harmless, but we have next to no data on their long-term effects."
    m 2euc "Additionally, each type of GMO needs to be carefully reviewed on a case-by-case, modification-by-modification basis to ensure its quality and safety."
    m 7rsd "There are other considerations as well. {w=0.2}Products containing GMOs have to be labelled, environmental effects must be considered, and misinformation has to be combated."
    m 2dsc "..."
    m 2eud "Personally, I think that GMOs have a lot of potential to do good, but only if they continue to be heavily researched and tested."
    m 4dkc "Major issues such as herbicide usage and gene flow {i}need{/i} to be fixed as well...{w=0.2}{nw}"
    extend 4efc "biodiversity is already at enough risk as is from climate change and deforestation."
    m 2esd "As long as we're careful, GMOs will be fine...{w=0.2}recklessness and carelessness pose the biggest threat."
    m 2dsc "..."
    m 7eua "So what do you think, [player]? {w=0.2}{nw}"
    extend 7euu "Quite the promising field, wouldn't you say?"
    m 3esd "Like I said before, GMOs are a complex topic. {w=0.2}If you want to learn more, make sure that your sources are reliable and that you're able to see the discussion from both sides."
    m 1eua "I think that's enough for now, thanks for listening~"
    return
