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

label import_ddlc_persistent:
    #Open the persistent save file as old_persistent
    python:
        from renpy.loadsave import dump, loads
        
        #open the persistent save file at save_path
        f=file(save_path,"rb")
        s=f.read().decode("zlib")
        f.close()
        
        old_persistent=loads(s)
        
        #Bring old_persistent data up to date with current version
        old_persistent = updateTopicIDs("v030",old_persistent)
        old_persistent = updateTopicIDs("v031",old_persistent)
        old_persistent = updateTopicIDs("v032",old_persistent)
        old_persistent = updateTopicIDs("v033",old_persistent)
        
        dumpPersistentToFile(old_persistent,basedir + '/old_persistent.txt')
    
    #Check if previous MAS data exists
    
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
                    $merge_previous=False
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
        if merge_previous is True:
            persistent._chosen.update(old_persistent._chosen)
        else:
            persistent._chosen=old_persistent._chosen
        
        #Renpy defined list of all audio heard in the game
        #Format: dict with (keys) song paths from basedir (value) Boolean for if played
        #Example: u'bgm/heartbeat.ogg': True
        if merge_previous is True:
            persistent._seen_audio.update(old_persistent._seen_audio)
        else:
            persistent._seen_audio=old_persistent._seen_audio
        
        #Renpy defined list of all seen files and labels
        #Format: dict with (keys) label or file seen (value) Boolean for if seen
        #Example: (u'D:\\Documents\\DDLC\\DDLC/game/script-poemresponses.rpy', 1469568838, 692): True
        #Example: u'ch20_main2': True
        if merge_previous is True:
            persistent._seen_ever.update(old_persistent._seen_ever)
        else:
            persistent._seen_ever=old_persistent._seen_ever
        
        #Renpy defined list of all seen images
        #Format: dict with (keys) file path (value) Boolean for if seen
        #Example: (u'yuri', u'2m'): True
        if merge_previous is True:
            persistent._seen_images.update(old_persistent._seen_images)
        else:
            persistent._seen_images=old_persistent._seen_images
        
        #Renpy translates, not sure what this does, but likely works in concert with _seen_ever for renpy.seen_label()
        #Format: set with keys that look like renpy labels followed by some hash
        #Example: u'ch40_main_496daacd'
        if merge_previous is True:
            persistent._seen_translates.update(old_persistent._seen_translates)
        else:
            persistent._seen_translates=old_persistent._seen_translates
        
        #clear
        #A list of 10 booleans marking which CG's were unlocked in play
        #For reference order is the same as the numbering in images/cg
        old_persistent.clear
        
        #clearall
        #This boolean simply says if the "perfect endging" was unlocked
        old_persistent.clearall
        
        #deleted_saves
        #Deletes save files, set to True after Sayori hangs herself
        old_persistent.deleted_saves
        
        #ghost_menu & seen_ghost_menu
        #There's a 1 in 64 chance Easter Egg of a ghost menu showing up in act 2
        old_persistent.ghost_menu
        old_persistent.seen_ghost_menu
        
        #monika_kill
        #Has monika died? (Had her character file deleted in act 3)
        old_persistent.monika_kill
        
        #monika_reload
        #How many times have you restarted in chapter 30 (spaceroom scene)
        old_persistent.monika_reload
        
        #monikatopics
        #A list with numbers for the random topics in Act 3 that Monika can talk about
        #The numbers line up with the ch30_## labels at the end of ch30
        old_persistent.monikatopics
        
        #playername
        #What name did the player set for the main character at the start of the game
        old_persistent.playername
        
        #playthrough
        #Marks which act the game is on
        #0 = intro, 1 = Sayori was just deleted, 2 = Act 2 without Sayori, 3 = Spaceroom Act 3, 4 = Post spaceroom finale
        old_persistent.playthrough
        

        #seen_eyes
        #Marks if the player saw an easter egg in Act 2 poem game with eyes (1 in 6 chance)
        old_persistent.seen_eyes
        
        #seen_sticker
        #Marks if the player saw an easter egg in Act 2 poem game where Monika's sticker jumped off screen
        old_persistent.seen_sticker
        
        #special_poems
        #Which special poems did the player unlock
        old_persistent.special_poems
        
        #steam
        #Steam version of the DDLC?
        old_persistent.steam
        
        #tried_skip
        #Did the player try to skip Monika's dialogue in Act 3?
        old_persistent.tried_skip
        
        #yuri_kill
        #Did yuri stab herself?
        old_persistent.yuri_kill
        
        
        dumpPersistentToFile(persistent,basedir + '/merged_persistent.txt')
    return