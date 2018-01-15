# This file imports save data from DDLC without changing the original data.
# By default, when this is run all relevant data from DDLC is imported.
# Handling of individual variables can be handled by changing the settings below.
init python:
    def dumpPersistentToFile(dumped_persistent,dumppath):
    #
    # Prints a file containing each dictionary element of a persistent variable
    #
    # IN:
    #   @param dumped_persistent - a renpy persistent variable
    #   @param dumppath - a file path to the text file to be created. Must be a valid write location
    #
        dumped_persistent=vars(dumped_persistent)

        fo = open(dumppath, "w")

        for key in sorted(dumped_persistent.iterkeys()):
            fo.write(str(key) + ' - ' + str(type(dumped_persistent[key])) + ' >>> '+ str(dumped_persistent[key]) + '\n\n')

        fo.close()

label import_ddlc_persistent_in_settings:
    $ prev_songs_enabled = store.songs.enabled
    $ prev_dialogue = allow_dialogue
    $ store.songs.enabled = False
    $ allow_dialogue = False
#    $ disable_esc() # tthis doesnt work somehow
    call import_ddlc_persistent from _call_import_ddlc_persistent_1
    $ quick_menu = True
    $ store.songs.enabled = prev_songs_enabled
    $ allow_dialogue = prev_dialogue
#    $ enable_esc()
    return

label import_ddlc_persistent:
    python:
        from renpy.loadsave import dump, loads

        import glob

        # Check for saves in platform-specific location.
        if renpy.macintosh:
            rv = "~/Library/RenPy/"
            check_path = os.path.expanduser(rv)

        elif renpy.windows:
            if 'APPDATA' in os.environ:
                check_path =  os.environ['APPDATA'] + "/RenPy/"
            else:
                rv = "~/RenPy/"
                check_path = os.path.expanduser(rv)

        else:
            rv = "~/.renpy/"
            check_path = os.path.expanduser(rv)

        save_path=glob.glob(check_path + 'DDLC/persistent')
        if not save_path:
            save_path=glob.glob(check_path + 'DDLC-*/persistent')

    $quick_menu = False
    scene black
    with Dissolve(1.0)
    #If you found a DDLC save to import
    if save_path:
        $save_path=save_path[0]
        "Save data for Doki Doki Literature Club was found at [save_path]."
        menu:
            "Would you like to import Doki Doki Literature Club save data into [config.name]?\n(DDLC will not be affected)"
            "Yes, import DDLC save data.":
                pause 0.3
                pass
            "No, do not import.":
                pause 0.3
                return
    else:
        #Tell the player that the save wasn't found
        $quick_menu = False
        "Save data from Doki Doki Literature Club could not be found."
        menu:
            "Save data will not be imported at this time."
            "Okay":
                pause 0.3
                pass
        return

    #Open the persistent save file as old_persistent
    python:
        from renpy.loadsave import dump, loads

        #open the persistent save file at save_path
        f=file(save_path,"rb")
        s=f.read().decode("zlib")
        f.close()

        old_persistent=loads(s)

        #Bring old_persistent data up to date with current version
        renpy.call_in_new_context("vv_updates_topics") # init the updates lists
        old_persistent = updateTopicIDs("v030",old_persistent)
        old_persistent = updateTopicIDs("v031",old_persistent)
        old_persistent = updateTopicIDs("v032",old_persistent)
        old_persistent = updateTopicIDs("v033",old_persistent)
        clearUpdateStructs()

        #dumpPersistentToFile(old_persistent,basedir + '/old_persistent.txt')

    #Check if previous MAS data exists
    default merge_previous=False
    if persistent.first_run:
        label .save_merge_or_replace:
        menu:
            "Previous Monika After Story save data has also been found.\nReplace or merge with DDLC save data?"
            "Merge save data.":
                $merge_previous=True #Time to merge data

            "Delete After Story data.":
                menu:
                    "Monika After Story data will be deleted. This cannot be undone. Are you sure?"
                    "Yes":
                        m "You really haven't changed. Have you?"
                    "No":
                        jump save_merge_or_replace
            "Cancel.":
                "DDLC data can be imported later in the Settings menu."
                return


    python:
        #These are all of the persistent variables from a DDLC save
        ##Unimportant/unused variables
        #_achievement_progress #Achievements not yet implemented. Might change in the future
        #_achievements
        #_changed #Dictionary tracks when its values were changed
        #_character_volume #Empty
        #_file_folder
        #_file_page
        #_file_page_name
        #_iap_purchases
        #_preference_default
        #_preferences
        #_set_preferences
        #_style_preferences
        #_virtual_size
        #_voice_mute
        #demo
        #first_poem #Unused?
        #menu_bg_m #True if the player opened the main menu
        #monika_back #Unused
        #seen_colors_poem #Unused

        #Update variables
        #These are currently not used, but may be in the future
        #We could also use this to inform players of new versions for MAS
        #_update_last_checked
        #_update_version

        #Anticheat
        #An integer number used for checking if persistent has been tampered with. Don't change this value even if replacing old save
        #anticheat

        #Autoload
        #Label that tells splash.rpy where to go when the game starts. We don't want to carryover that part of the game flow.
        #autoload

        #first_load
        #Used to tell if a specific user tip was shown on startup...seems redundant with #first_run
        #first_load

        #first_run
        #Used to tell if the game has completed a full start-up sequence on this save.
        #Not to be confused with the firstrun file found in the install folder
        #first_run

        #######################
        ##Important variables##
        #######################
        #Renpy defined list of every menu choice the player has made.
        #Format: dict with (keys) with file name, choice picked (value) Boolean for if chosen
        #Example: ((u'D:\\Documents\\DDLC\\DDLC/game/script-ch1.rpy', 1469568700, 980), u'Natsuki.'): True
        if merge_previous is True and old_persistent._chosen is not None and persistent._chosen is not None:
            persistent._chosen.update(old_persistent._chosen)
        elif old_persistent._chosen is not None:
            persistent._chosen=old_persistent._chosen

        #Renpy defined list of all audio heard in the game
        #Format: dict with (keys) song paths from basedir (value) Boolean for if played
        #Example: u'bgm/heartbeat.ogg': True
        if merge_previous is True and old_persistent._seen_audio is not None and persistent._seen_audio is not None:
            persistent._seen_audio.update(old_persistent._seen_audio)
        elif old_persistent._seen_audio is not None:
            persistent._seen_audio=old_persistent._seen_audio

        #Renpy defined list of all seen files and labels
        #Format: dict with (keys) label or file seen (value) Boolean for if seen
        #Example: (u'D:\\Documents\\DDLC\\DDLC/game/script-poemresponses.rpy', 1469568838, 692): True
        #Example: u'ch20_main2': True
        if merge_previous is True and old_persistent._seen_ever is not None and persistent._seen_ever is not None:
            persistent._seen_ever.update(old_persistent._seen_ever)
        elif old_persistent._seen_ever is not None:
            persistent._seen_ever=old_persistent._seen_ever

        #Renpy defined list of all seen images
        #Format: dict with (keys) file path (value) Boolean for if seen
        #Example: (u'yuri', u'2m'): True
        if merge_previous is True and old_persistent._chosen is not None and persistent._chosen is not None:
            persistent._seen_images.update(old_persistent._seen_images)
        elif old_persistent._chosen is not None:
            persistent._seen_images=old_persistent._seen_images

        #Renpy translates, not sure what this does, but likely works in concert with _seen_ever for renpy.seen_label()
        #Format: set with keys that look like renpy labels followed by some hash
        #Example: u'ch40_main_496daacd'
        if merge_previous is True and old_persistent._seen_translates is not None and persistent._seen_translates is not None:
            persistent._seen_translates.update(old_persistent._seen_translates)
        elif old_persistent._seen_translates is not None:
            persistent._seen_translates=old_persistent._seen_translates

        #clear
        #A list of 10 booleans marking which CG's were unlocked in play
        #For reference order is the same as the numbering in images/cg
        if merge_previous is True and old_persistent.clear is not None and persistent.clear is not None:
            for flag in persistent.clear:
                persistent.clear[flag] = persistent.clear[flag] or old_persistent.clear[flag]
        elif old_persistent.clear is not None:
            persistent.clear=old_persistent.clear

        #clearall
        #This boolean simply says if the "perfect endging" was unlocked
        if merge_previous is True and old_persistent.clearall is not None and persistent.clearall is not None:
            persistent.clearall = persistent.clearall or old_persistent.clearall
        elif old_persistent.clearall is not None:
            persistent.clearall=old_persistent.clearall

        #deleted_saves
        #Deletes save files, set to True after Sayori hangs herself
        #old_persistent.deleted_saves

        #ghost_menu & seen_ghost_menu
        #There's a 1 in 64 chance Easter Egg of a ghost menu showing up in act 2
        if merge_previous is True and old_persistent.ghost_menu is not None and persistent.ghost_menu is not None:
            persistent.ghost_menu=persistent.ghost_menu or old_persistent.ghost_menu
            persistent.seen_ghost_menu=persistent.seen_ghost_menu or old_persistent.seen_ghost_menu
        elif old_persistent.ghost_menu is not None:
            persistent.ghost_menu=old_persistent.ghost_menu
            persistent.seen_ghost_menu = old_persistent.seen_ghost_menu

        #monika_kill
        #Has monika died? (Had her character file deleted in act 3)
        if merge_previous is True and old_persistent.monika_kill is not None and persistent.monika_kill is not None:
            persistent.monika_kill = persistent.monika_kill or old_persistent.monika_kill
        elif old_persistent.monika_kill is not None:
            persistent.monika_kill=old_persistent.monika_kill

        #monika_reload
        #How many times have you restarted in chapter 30 (spaceroom scene)
        if merge_previous is True and old_persistent.monika_reload is not None and persistent.monika_reload is not None:
            persistent.monika_reload = persistent.monika_reload + old_persistent.monika_reload
        elif old_persistent.monika_reload is not None:
            persistent.monika_reload=old_persistent.monika_reload

        #monikatopics
        #A list with numbers for the random topics in Act 3 that Monika can talk about
        #The numbers line up with the ch30_## labels at the end of ch30
        #old_persistent.monikatopics #Deprecated in Monika After Story 0.4.0

        #playername
        #What name did the player set for the main character at the start of the game
        if merge_previous is True and persistent.playername is not "" and old_persistent.playername is not None and persistent.playername is not None:
            if persistent.playername == old_persistent.playername:
                persistent.playername
            else:
                renpy.call_in_new_context('merge_unmatched_names')
        elif old_persistent.playername is not None:
            persistent.playername=old_persistent.playername
        player=persistent.playername

        #playthrough
        #Marks which act the game is on
        #0 = intro, 1 = Sayori was just deleted, 2 = Act 2 without Sayori, 3 = Spaceroom Act 3, 4 = Post spaceroom finale
        if merge_previous is True and old_persistent.playthrough is not None and persistent.playthrough is not None:
            if persistent.playthrough >= old_persistent.playthrough:
                persistent.playthrough
            else:
                persistent.playthrough = old_persistent.playthrough
        elif old_persistent.playthrough is not None:
            persistent.playthrough = old_persistent.playthrough

        #seen_eyes
        #Marks if the player saw an easter egg in Act 2 poem game with eyes (1 in 6 chance)
        if merge_previous is True and old_persistent.seen_eyes is not None and persistent.seen_eyes is not None:
            persistent.seen_eyes = persistent.seen_eyes or old_persistent.seen_eyes
        elif old_persistent.seen_eyes is not None:
            persistent.seen_eyes=old_persistent.seen_eyes

        #seen_sticker
        #Marks if the player saw an easter egg in Act 2 poem game where Monika's sticker jumped off screen
        if merge_previous is True and old_persistent.seen_sticker is not None and persistent.seen_sticker is not None:
            persistent.seen_sticker = persistent.seen_sticker or old_persistent.seen_sticker
        elif old_persistent.seen_sticker is not None:
            persistent.seen_sticker=old_persistent.seen_sticker

        #special_poems
        #Which special poems did the player unlock
        if merge_previous is True and old_persistent.special_poems is not None and persistent.special_poems is not None:
            persistent.special_poems = persistent.special_poems + old_persistent.special_poems
        elif old_persistent.special_poems is not None:
            persistent.special_poems=old_persistent.special_poems

        #steam
        #Steam version of the DDLC?
        #There's no real way to merge this, so just use the old version
        persistent.steam=old_persistent.steam

        #tried_skip
        #Did the player try to skip Monika's dialogue in Act 3?
        if merge_previous is True and old_persistent.tried_skip is not None and persistent.tried_skip is not None:
            persistent.tried_skip = persistent.tried_skip or old_persistent.tried_skip
        elif old_persistent.tried_skip is not None:
            persistent.tried_skip=old_persistent.tried_skip

        #yuri_kill
        #Did yuri stab herself?
        if merge_previous is True and old_persistent.yuri_kill is not None and persistent.yuri_kill is not None:
            persistent.yuri_kill = persistent.yuri_kill or old_persistent.yuri_kill
        elif old_persistent.yuri_kill is not None:
            persistent.yuri_kill=old_persistent.yuri_kill

        #dumpPersistentToFile(persistent,basedir + '/merged_persistent.txt')
        persistent.has_merged = True

    return

label merge_unmatched_names:
    menu:
        "Save file names do not match. Which would you like to keep?"
        "[old_persistent.playername]":
            $persistent.playername=old_persistent.playername
        "[persistent.playername]":
            $persistent.playername

    return
