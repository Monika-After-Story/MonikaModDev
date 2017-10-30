label import_ddlc_persistent:

    #Open the persistent save file as old_persistent
    python:
        from renpy.loadsave import dump, loads
        
        #open the persistent save file at save_path
        f=file(save_path,"rb")
        s=f.read().decode("zlib")
        f.close()
        
        old_persistent=loads(s)
        old_persistent=vars(old_persistent)
        
        #Bring old_persistent data up to date with current version
        
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
            
            
    return