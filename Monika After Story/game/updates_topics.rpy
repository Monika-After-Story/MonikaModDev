# Module that defines changed topics between versions
# this should run before updates.rpy

# start by initalization version update dict
define updates.version_updates = None

# key:version number -> v:changedIDs
# changedIDs structure:
#   k:oldId -> v:newId
define updates.topics = None

# preeerything
init -1 python:
    def clearUpdateStructs():
        #
        # Clears a bunch of uneeded stuff

        updates.topics.clear()
        updates.topics = None
        updates.version_updates.clear()
        updates.version_updates = None
        # TODO
        # is there a way to delete a renpy storemodule?


# runs before updates.rpy
init 9 python:

    if persistent.version_number != config.version:
        renpy.call_in_new_context("vv_updates_topics")


# init label for updats_topics
label vv_updates_topics:
    python:

        # init these dicts
        updates.version_updates = {}
        updates.topics = {}

        # versions
        # use the v#_#_# notation so we can work with labels
        vv0_7_0 = "v0_7_0"
        vv0_6_3 = "v0_6_3"
        vv0_6_2 = "v0_6_1"
        vv0_6_1 = "v0_6_1"
        vv0_6_0 = "v0_6_0"
        vv0_5_1 = "v0_5_1"
        vv0_5_0 = "v0_5_0"
        vv0_4_0 = "v0_4_0"
        vv0_3_3 = "v0_3_3"
        vv0_3_2 = "v0_3_2"
        vv0_3_1 = "v0_3_1"
        vv0_3_0 = "v0_3_0"
        vv0_2_2 = "v0_2_2"

        # update this dict accordingly to every new version
        # k:old version number -> v:new version number
        # some version changes skip some numbers because no major updates
        updates.version_updates[vv0_6_3] = vv0_7_0
        updates.version_updates[vv0_6_2] = vv0_7_0
        updates.version_updates[vv0_6_1] = vv0_7_0
        updates.version_updates[vv0_6_0] = vv0_6_1
        updates.version_updates[vv0_5_1] = vv0_6_1
        updates.version_updates[vv0_5_0] = vv0_5_1
        updates.version_updates[vv0_4_0] = vv0_5_1
        updates.version_updates[vv0_3_3] = vv0_5_1
        updates.version_updates[vv0_3_2] = vv0_3_3
        updates.version_updates[vv0_3_1] = vv0_3_2
        updates.version_updates[vv0_3_0] = vv0_3_1
        updates.version_updates[vv0_2_2] = vv0_3_0


        # version structures:
        # if a version has changed / removed IDS, then add it as a dict
        # here
        # k:oldID -> v:newID
        # if newID is None, the topic is considered removed
        #
        # NOTE: If a potential conflict may occur (removing one topic,
        # changing name of another topic to the one that was removed),
        # do NOT use this to update the IDs
        # All conflicts should be handled in an individual script block in
        # updates.rpy. (SEE updates.rpy)

        # (0.6.1 - 0.6.3) -> 0.7.0
        changedIDs = {
            "monika_deleted": None,
            "monika_whatever": None,
            "monika_games": None,
            "monika_chess": None,
            "monika_pong": None,
            "monika_vulgarity": None,
            "monika_goodbye": None,
            "monika_night": None
        }
        updates.topics[vv0_7_0] = changedIDs 

        # (0.5.1 - 0.6.0) -> 0.6.1
        changedIDs = {
            "monika_piano": None
        }
        updates.topics[vv0_6_1] = changedIDs

        # (0.3.3 - 0.5.0) -> 0.5.1
        changedIDs = dict()
        changedIDs["monika_music"] = None
        changedIDs["monika_keitai"] = None
        changedIDs["monika_subahibi"] = None
        changedIDs["monika_reddit"] = None
        changedIDs["monika_shill"] = None
        changedIDs["monika_dracula"] = None
        changedIDs["monika_undertale"] = None
        changedIDs["monika_recursion"] = None
        changedIDs["monika_lain"] = None
        changedIDs["monika_kyon"] = None
        changedIDs["monika_water"] = None
        changedIDs["monika_computer"] = None
        updates.topics[vv0_5_1] = changedIDs

        # 0.3.1 -> 0.3.2
        changedIDs = dict()
        changedIDs["monika_monika"] = None
        updates.topics[vv0_3_2] = changedIDs

        # 0.3.0 -> 0.3.1
        changedIDs = dict()
        changedIDs["monika_ghosts"] = "monika_whispers"
        updates.topics[vv0_3_1] = changedIDs

        # 0.2.2 -> 0.3.0
        # this is a long list...
        # no_topics_list is defined / checked in updates.rpy
        changedIDs = None
        changedIDs = dict()
        changedIDs["ch30_1"] = "monika_god"
        changedIDs["ch30_2"] = "monika_death"
        changedIDs["ch30_3"] = "monika_bad_day"
        changedIDs["ch30_4"] = "monika_sleep"
        changedIDs["ch30_5"] = "monika_sayori"
        changedIDs["ch30_6"] = "monika_japan"
        changedIDs["ch30_7"] = "monika_high_school"
        changedIDs["ch30_8"] = "monika_nihilism"
        changedIDs["ch30_9"] = "monika_piano"
        changedIDs["ch30_10"] = "monika_twitter"
        changedIDs["ch30_11"] = "monika_portraitof"
        changedIDs["ch30_12"] = "monika_veggies"
        changedIDs["ch30_13"] = "monika_saved"
        changedIDs["ch30_14"] = "monika_secrets"
        changedIDs["ch30_15"] = "monika_color"
        changedIDs["ch30_16"] = "monika_music"
        changedIDs["ch30_17"] = "monika_listener"
        changedIDs["ch30_18"] = "monika_spicy"
        changedIDs["ch30_19"] = "monika_why"
        changedIDs["ch30_20"] = "monika_okayeveryone"
        changedIDs["ch30_21"] = "monika_ghosts"
        changedIDs["ch30_22"] = "monika_archetype"
        changedIDs["ch30_23"] = "monika_tea"
        changedIDs["ch30_24"] = "monika_favoritegame"
        changedIDs["ch30_25"] = "monika_smash"
#        changedIDs["ch30_26"] = ""
        changedIDs["ch30_27"] = "monika_lastpoem"
        changedIDs["ch30_28"] = "monika_anxious"
        changedIDs["ch30_29"] = "monika_friends"
        changedIDs["ch30_30"] = "monika_college"
        changedIDs["ch30_31"] = "monika_middleschool"
        changedIDs["ch30_32"] = "monika_outfit"
        changedIDs["ch30_33"] = "monika_horror"
        changedIDs["ch30_34"] = "monika_rap"
        changedIDs["ch30_35"] = "monika_wine"
        changedIDs["ch30_36"] = "monika_date"
        changedIDs["ch30_37"] = "monika_kiss"
        changedIDs["ch30_38"] = "monika_yuri"
        changedIDs["ch30_39"] = "monika_writingtip"
        changedIDs["ch30_40"] = "monika_habits"
        changedIDs["ch30_41"] = "monika_creative"
        changedIDs["ch30_42"] = "monika_deleted"
        changedIDs["ch30_43"] = "monika_keitai"
        changedIDs["ch30_44"] = "monika_simulated"
        changedIDs["ch30_45"] = "monika_rain"
        changedIDs["ch30_46"] = "monika_closeness"
        changedIDs["ch30_47"] = "monika_confidence"
        changedIDs["ch30_48"] = "monika_carryme"
        changedIDs["ch30_49"] = "monika_debate"
        changedIDs["ch30_50"] = "monika_internet"
        changedIDs["ch30_51"] = "monika_lazy"
        changedIDs["ch30_52"] = "monika_mentalillness"
        changedIDs["ch30_53"] = "monika_read"
        changedIDs["ch30_54"] = "monika_festival"
        changedIDs["ch30_55"] = "monika_tsundere"
        changedIDs["ch30_56"] = "monika_introduce"
        changedIDs["ch30_57"] = "monika_cold"
        changedIDs["ch30_58"] = "monika_housewife"
        changedIDs["ch30_59"] = "monika_route"
        changedIDs["monika_literatureclub"] = "monika_ddlc"
        changedIDs["monika_religion"] = None

            # here is a list of new ids, for reference. These are automatically
            # handled via new topic generation.
            # monika_credits_song
            # monika_whatever (special topic launcher)
            
            # here is a list of IDS present in v0.2.2, again for reference
            # monika_imouto
            # monika_oneesan
            # monika_family
            # monika_anime
            # monika_libitina
            # monika_meta
            # monika_programming
            # monika_vn
            # monika_totono
            # monika_subahibi
            # monika_difficulty
            # monika_poetry
            # monika_dan
            # monika_4chan
            # monika_reddit
            # monika_vidya
            # monika_books
            # monika_favpoem
            # monika_favbook
            # monika_natsuki
            # monika_love
            # monika_hedgehog
            # monika_justification
            # monika_freewill
            # monika_shill
            # monika_technique
            # monika_contribute
            # monika_drawing
            # monika_mc
            # monika_heroism
            # monika_dracula
            # monika_undertale
            # monika_bestgrill
            # monika_trolley
            # monika_girlfriend
            # monika_waifus

            # CONFLICTING CHANGES ALERT
            # the following ids have been changed/removed and conflict with
            # changedIDs dict (these must be handled in updates.rpy)
            # monika_piano
            # monika_college was pointing to ch30_31 (monika_middleschool)
        updates.topics[vv0_3_0] = changedIDs

        # ensuring no refs to old dicts
        changedIDs = None
