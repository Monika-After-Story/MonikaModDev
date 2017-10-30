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
    
    menu:
        "Previous Monika After Story save data has also been found.\nReplace or merge with DDLC save data?"
        "Merge save data.":
            #Time to merge data
            pass
        "Delete After Story data.":
            #Replace
            pass
        "Cancel.":
            #Go back to previous question
            pass
            
    return