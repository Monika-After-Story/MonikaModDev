# selector testing

init -100 python:
    
    def dev_mas_unlock_all_sprites():
        for sel_obj in store.mas_selspr.ACS_SEL_SL:
            sel_obj.unlocked = True

        for sel_obj in store.mas_selspr.HAIR_SEL_SL:
            sel_obj.unlocked = True

        for sel_obj in store.mas_selspr.CLOTH_SEL_SL:
            sel_obj.unlocked = True


    def dev_mas_clear_spritegift(giftname):
        namegift_data = store.mas_sprites_json.giftname_map.get(giftname, None)
        if namegift_data is not None :
            ng_sp, ng_name = namegift_data
            spr_obj = store.mas_sprites.get_sprite(ng_sp, ng_name)

            if namegift_data in persistent._mas_sprites_json_gifted_sprites:
                persistent._mas_sprites_json_gifted_sprites.pop(namegift_data)

            if spr_obj is not None:
                store.mas_selspr._lock_item(spr_obj, ng_sp)

        if giftname in persistent._mas_filereacts_sprite_gifts:
            persistent._mas_filereacts_sprite_gifts.pop(giftname)

        if giftname in persistent._mas_filereacts_sprite_reacted:
            persistent._mas_filereacts_sprite_reacted.pop(giftname)

        if giftname in persistent._mas_filereacts_reacted_map:
            persistent._mas_filereacts_reacted_map.pop(giftname)


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_selector_test",
            category=["dev"],
            prompt="TEST SELECTOR (sidebar raw visual)",
            pool=True,
            unlocked=True
        )
    )


label dev_selector_test:
    m 1eua "Hi [player], I will test the sidebar selector system. (RAW)"

    python:
        start_test_items = [
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 1",
                "test1",
                "ring",
                hover_dlg="You hover over test 1",
                first_select_dlg="You first select test 1",
                select_dlg="You select test 1"
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 2",
                "test1",
                "ring",
                hover_dlg="You hover over test 2",
                select_dlg="You select test 2"
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 3",
                "test1",
                "ring",
                hover_dlg="You hover over test 3",
                select_dlg="You select test 3"
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 4",
                "test1",
                "ring",
                hover_dlg="You hover over test 4",
                select_dlg="You select test 4"
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 5",
                "test1",
                "ring",
                hover_dlg="You hover over test 5",
                select_dlg="You select test 5"
            )
        ]
        for acs in start_test_items:
            acs.unlocked = True

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox("pick test:")
        sel_map = {}

        sb_params = {
            "items": start_test_items,
            "confirm_label": "dev_selector_test_confirm",
            "cancel_label": "dev_selector_test_cancel",
            "mailbox": mailbox,
            "select_map": sel_map
        }

    m "no screen rn, am testing"
    return

    # TODO: this needs to be called, so we need to redo the jump logic.,
#    jump mas_selector_sidebar_select(start_test_items, "dev_selector_test_confirm", "dev_selector_test_cancel", 

label dev_selector_test_confirm:
    hide screen mas_selector_sidebar
    m "you hit the confirm button!"
    return

label dev_selector_test_cancel:
    hide screen mas_selector_sidebar
    m "You hit the cancel button!"
    return

label dev_selector_test_hover:
    m "you hovere in test1"
    return

label dev_selector_test_hover2:
    m " you hver in test2"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_selector_hair_test",
            category=["dev"],
            prompt="TEST SELECTOR (sidebar hair)",
            pool=True,
            unlocked=True
        )
    )

label dev_selector_hair_test:
    python:
        unlock_map = {}
        sorted_hair = store.mas_selspr.HAIR_SEL_SL
        for item in sorted_hair:
            unlock_map[item.name] = item.unlocked
            item.unlocked = True

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox("Pick HAIR:")
        sel_map = {}

    m 1eua "Hi! Lets change my hair!"

    call mas_selector_sidebar_select_hair(sorted_hair, mailbox=mailbox, select_map=sel_map)

    # undo the unlocks 
    python:
        for item in sorted_hair:
            item.unlocked = unlock_map[item.name]

    if _return:
        m 1eub "You confirmed my hair!"

    else:
        m 1eka "You canceled my hair..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_selector_clothes_test",
            category=["dev"],
            prompt="TEST SELECTOR (sidebar clothes)",
            pool=True,
            unlocked=True
        )
    )

label dev_selector_clothes_test:
    python:
        unlock_map = {}
        sorted_clothes = store.mas_selspr.CLOTH_SEL_SL
        for item in sorted_clothes:
            unlock_map[item.name] = item.unlocked
            item.unlocked = True

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox("Pick clothes:")
        sel_map = {}

    m 1eua "Hi! Lets change my clothes!"

    call mas_selector_sidebar_select_clothes(sorted_clothes, mailbox=mailbox, select_map=sel_map)

    # undo the unlocks 
    python:
        for item in sorted_clothes:
            item.unlocked = unlock_map[item.name]

    if _return:
        m 1eub "You confirmed my clothes!"

    else:
        m 1eka "You canceled my clothes..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_selector_acs_ribbons_test",
            category=["dev"],
            prompt="TEST SELECTOR (ribbons acs)",
            pool=True,
            unlocked=True
        )
    )

label dev_selector_acs_ribbons_test:
    python:
        unlock_map = {}
        sorted_acs = store.mas_selspr.ACS_SEL_SL
        use_acs = []
        for item in sorted_acs:
            if item.group == "ribbon":
                unlock_map[item.name] = item.unlocked
                item.unlocked = True
                use_acs.append(item)

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox("Pick ribbon:")
        sel_map = {}

    m 1eua "Hi! Lets change my ribbon!"

    if monika_chr.hair.name != mas_hair_def.name:
        m "But im going to change my clothes and hair back to default."
        $ monika_chr.reset_outfit(False)

    call mas_selector_sidebar_select_acs(use_acs, mailbox=mailbox, select_map=sel_map)

    # undo the unlocks 
    python:
        for item in use_acs:
            item.unlocked = unlock_map[item.name]

    if _return:
        m 1eub "You confirmed my ribbon!"

    else:
        m 1eka "You canceled my ribbon..."

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_selector_hair_disabled",
            category=["dev"],
            prompt="TEST SELECTOR (disabling hair bc clothes)",
            pool=True,
            unlocked=True
        )
    )

label dev_selector_hair_disabled:
    python:
        hdown_sel = store.mas_selspr.get_sel_hair(mas_hair_down)
        hdown_sel_lstat = hdown_sel.unlocked
        hdown_sel.unlocked = True
        hdown_sel.disable_type = store.mas_selspr.DISB_HAIR_BC_CLOTH

        unlock_map = {}
        sorted_hair = store.mas_selspr.HAIR_SEL_SL
        for item in sorted_hair:
            unlock_map[item.name] = item.unlocked
            item.unlocked = True

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox(
            "Which hairstyle would you like me to wear?"
        )
        sel_map = {}

    m 1eua "first reset outfit"
    $ current_state = monika_chr.save_state(True, True, True)
    $ monika_chr.reset_outfit()
    $ monika_chr.remove_all_acs()

    m 1eua "I will disable hair down for no reason"

    call mas_selector_sidebar_select_hair(sorted_hair, mailbox=mailbox, select_map=sel_map)

    # undo unlocks
    python:
        for item in sorted_hair:
            item.unlocked = unlock_map[item.name]

        hdown_sel.unlocked = hdown_sel_lstat

    m 6eua "now restore outfit"
    $ monika_chr.restore(current_state)
    m 1eua "done"

    return
