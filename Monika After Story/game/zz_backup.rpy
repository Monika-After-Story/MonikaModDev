# module that does some file backup work

python early:
    # sometimes we have persistent issues. Why? /shrug.
    # but we do know is that we might be able to tell if a persistent got
    # screwed by attempting to read it in now, before renpy actually does so.
    mas_corrupted_per = False
    mas_no_backups_found = False
    mas_backup_copy_failed = False
    mas_backup_copy_filename = None
    mas_bad_backups = list()
    
    def _mas_earlyCheck():
        """
        attempts to read in the persistent and load it. if an error occurs
        during loading, we'll log it in a dumped file in basedir.

        NOTE: we don't have many functions available here. However, we can
        import __main__ and gain access to core functions.
        """
        import __main__
        import cPickle
        import os
        import datetime
        import shutil
        global mas_corrupted_per, mas_no_backups_found, mas_backup_copy_failed
        global mas_backup_copy_filename, mas_bad_backups
        early_log_path = os.path.normcase(renpy.config.basedir + "/early.log")

        per_dir = __main__.path_to_saves(renpy.config.gamedir)

        # first, check if we even have a persistent
        if not os.access(os.path.normcase(per_dir + "/persistent"), os.F_OK):
            # NO ERROR TO REPORT!
            return

        def trywrite(_path, msg, first=False):
            # attempt to write, no worries if no worko
            if first:
                mode = "w"
            else:
                mode = "a"

            _fileobj = None
            try:
                _fileobj = open(_path, mode)
                _fileobj.write("[{0}]: {1}\n".format(
                    datetime.datetime.now(),
                    msg
                ))
            except:
                pass
            finally:
                if _fileobj is not None:
                    _fileobj.close()


        def tryper(_tp_persistent):
            # tryies a persistent and checks if it is decoded succesfully
            # returns True on success. raises errors if failure
            per_file = None
            try:
                per_file = file(_tp_persistent, "rb")
                per_data = per_file.read().decode("zlib")
                per_file.close()
                actual_data = cPickle.loads(per_data)
                return True

            except Exception as e:
                raise e

            finally:
                if per_file is not None:
                    per_file.close()

        
        # okay, now let's attempt to read the persistent.
        try:
            if tryper(per_dir + "/persistent"):
                return

        except Exception as e:
            mas_corrupted_per = True
            trywrite(early_log_path, "persistent was corrupted!: " + repr(e))
        
        # if we got here, we had an exception. Let's attempt to restore from
        # an eariler persistent backup.

        # lets get all the persistent files here.
        per_files = os.listdir(per_dir)
        per_files = [x for x in per_files if x.startswith("persistent")]

        if len(per_files) == 0:
            trywrite(early_log_path, "no backups available")
            mas_no_backups_found = True
            return

        # now lets map them by number and also generate a list of the numbers
        file_nums = list()
        file_map = dict()
        for p_file in per_files:
            pname, dot, bakext = p_file.partition(".")
            try:
                num = int(pname[-2:])
            except:
                num = -1

            if 0 <= num < 100:
                file_nums.append(num)
                file_map[num] = p_file

        if len(file_nums) == 0:
            trywrite(early_log_path, "no backups available")
            mas_no_backups_found = True
            return

        # sort number list
        def wraparound_sort(_numlist):
            """
            Sorts a list of numbers using a special wraparound sort.
            Basically if all the numbers are between 0 and 98, then we sort
            normally. If we have 99 in there, then we need to make the wrap
            around numbers (the single digit ints in the list) be sorted
            as larger than 99.
            """
            if 99 in _numlist:
                for index in range(0, len(_numlist)):
                    if _numlist[index] < 10:
                        _numlist[index] += 100

            _numlist.sort()

        # using the special sort function
        wraparound_sort(file_nums)

        # okay, now to iteratively test backups and pick the good one
        sel_back = None
        while sel_back is None and len(file_nums) > 0:
            _this_num = file_nums.pop() % 100
            _this_file = file_map.get(_this_num, None)
            if _this_file is not None:
                try:
                    if tryper(per_dir + "/" + _this_file):
                        sel_back = _this_file
                except Exception as e:
                    trywrite(
                        early_log_path,
                        "'{0}' was corrupted: {1}".format(_this_file, repr(e))
                    )
                    sel_back = None
                    mas_bad_backups.append(_this_file)

        # did we get any?
        if sel_back is None:
            trywrite(early_log_path, "no working backups found")
            mas_no_backups_found = True
            return

        # otherwise, lets rename the existence persistent to bad and copy the
        # good persistent into the system
        # also let the log know we found a good one
        trywrite(early_log_path, "working backup found: " + sel_back)
        _bad_per = os.path.normcase(per_dir + "/persistent_bad")
        _cur_per = os.path.normcase(per_dir + "/persistent")
        _god_per = os.path.normcase(per_dir + "/" + sel_back)

        # we should at least try to keep a copy of the current persistent
        try:
            # copy current persistent
            shutil.copy(_cur_per, _bad_per)

        except Exception as e:
            trywrite(
                early_log_path, 
                "Failed to rename existing persistent: " + repr(e)
            )

        # regardless, we should try to copy over the good backup
        try:
            # copy the good one
            shutil.copy(_god_per, _cur_per)

        except Exception as e:
            mas_backup_copy_failed = True
            mas_backup_copy_filename = sel_back
            trywrite(
                early_log_path, 
                "Failed to copy backup persistent: " + repr(e)
            )
           
        # well, hopefully we were successful!
    
    # now call this
    _mas_earlyCheck()


init -900 python:
    import os
    import store.mas_utils as mas_utils

    __mas__bakext = ".bak"
    __mas__baksize = 5
    __mas__bakmin = 0
    __mas__bakmax = 100
    __mas__numnum = "{:02d}"
    __mas__latestnum = None

    # needs to be pretty damn early, but we require savedir here so 
    # we cant use python early

    def __mas__extractNumbers(partname, filelist):
        """
        Extracts a list of the number parts of the given file list

        Also sorts them nicely

        IN:
            partname - part of the filename prior to the numbers
            filelist - list of filenames
        """
        filenumbers = list()
        for filename in filelist:
            pname, dot, bakext = filename.rpartition(".")
            num = mas_utils.tryparseint(pname[len(partname):], -1)
            if __mas__bakmin <= num <= __mas__bakmax:
                # we only accept persistents with the correct number scheme
                filenumbers.append(num)

        if len(filenumbers) > 0:
            return sorted(filenumbers)

        return []


    def __mas__backupAndDelete(loaddir, org_fname, savedir=None, numnum=None):
        """
        Does a file backup / and iterative deletion.

        NOTE: Steps:
            1. make a backup copy of the existing file (org_fname)
            2. delete the oldest copy of the orgfilename schema if we already
                have __mas__baksize number of files

        Will log some exceptions
        May raise other exceptions

        Both dir args assume the trailing slash is already added

        IN:
            loaddir - directory we are copying files from
            org_fname - filename of the original file / aka file to copy
            savedir - directory we are copying files to (and deleting old files)
                If None, we use loaddir instead
                (Default: None)
            numnum - if passed in, use this number instead of figuring out the
                next numbernumber.
                (Default: None)

        RETURNS:
            tuple of the following format:
            [0]: numbernumber we just made
            [1]: numbernumber we delted (None means no deltion)
        """
        if savedir is None:
            savedir = loaddir

        filelist = os.listdir(savedir)
        loadpath = loaddir + org_fname

        # check for access of the org file
        if not os.access(loadpath, os.F_OK):
            return

        # parse the filelist to only get the import files
        filelist = [
            x
            for x in filelist
            if x.startswith(org_fname)
        ]

        # if we have the origin name in the filelist, remove it
        if org_fname in filelist:
            filelist.remove(org_fname)

        # get the number parts of the backup
        numberlist = __mas__extractNumbers(org_fname, filelist)

        # now do the iterative backup system
        numbernumber_del = None
        if len(numberlist) <= 0:
            numbernumber = __mas__numnum.format(0)

        elif 99 in numberlist:
            # some notes:
            # if 99 is in the list, it MUST be the last one in the list.
            # if we wrapped around, then the first parts of the list MUST be
            # less than __mas__baksize.
            # at min, the list will look like: [95, 96, 97, 98, 99]
            # At max, the list will look like: [0, 1, 2, 3, 99]
            # so we loop until the num at the current index is larger than or
            # equal to __mas__baksize - 1, then we know our split point between
            # new and old files
            curr_dex = 0
            while numberlist[curr_dex] < (__mas__baksize - 1):
                curr_dex += 1

            if curr_dex <= 0:
                numbernumber = __mas__numnum.format(0)
            else:
                numbernumber = __mas__numnum.format(numberlist[curr_dex-1] + 1)

            numbernumber_del = __mas__numnum.format(numberlist[curr_dex])

        elif len(numberlist) < __mas__baksize:
            numbernumber = __mas__numnum.format(numberlist.pop() + 1)

        else:
            # otherwise the usual, set up next number and deletion number
            numbernumber = __mas__numnum.format(numberlist.pop() + 1)
            numbernumber_del = __mas__numnum.format(numberlist[0])

        # numnum override
        if numnum is not None:
            numbernumber = numnum

        # copy the current file
        mas_utils.copyfile(
            loaddir + org_fname,
            "".join([savedir, org_fname, numbernumber, __mas__bakext])
        )

        # delete a backup
        if numbernumber_del is not None:
            numnum_del_path = "".join(
                [savedir, org_fname, numbernumber_del, __mas__bakext]
            )
            try:
                os.remove(numnum_del_path)
            except Exception as e:
                mas_utils.writelog(mas_utils._mas_failrm.format(
                    numnum_del_path,
                    str(e)
                ))

        return (numbernumber, numbernumber_del)


    def __mas__memoryBackup():
        """
        Backs up both persistent and calendar info
        """
        try:
            p_savedir = os.path.normcase(renpy.config.savedir + "/")
            p_name = "persistent"
            numnum, numnum_del = __mas__backupAndDelete(p_savedir, p_name)
            cal_name = "db.mcal"
            __mas__backupAndDelete(p_savedir, cal_name, numnum=numnum)

        except Exception as e:
            mas_utils.writelog("[ERROR]: {0}".format(str(e)))

    
    # run the backup system if persistents arent screwd
    if not mas_corrupted_per and persistent._mas_moni_chksum is None:
        __mas__memoryBackup()


### now for some dialogue bits courtesy of chibika

label mas_backups_you_have_corrupted_persistent:
    $ quick_menu = False
    scene black
    window show
    show chibika smile at mas_chdropin(300, travel_time=1.5)
    pause 1.5

    show chibika 3 at sticker_hop
    "Hello there!"
    show chibika sad
    "I hate to be the bringer of bad news..."
    "But unfortunately, your persistent file is corrupt."

    if mas_no_backups_found:
        "And what's even worse is..."
        show chibika at sticker_move_n
        "I was unable to find a working backup persistent."

        menu:
            "Do you have your own backups?"
            "Yes":
                jump mas_backups_have_some
            "No":
                jump mas_backups_have_none

    # otherwise we culd not copy
    jump mas_backups_could_not_copy


label mas_backups_have_some:

    show chibika smile at sticker_hop
    "That's a relief!"
    "Please copy them into '[renpy.config.savedir]' to restore your Monika's memories."

    call mas_backups_dont_tell
    show chibika smile at mas_chflip_s(-1)
    "Good luck!"

    jump _quit


label mas_backups_have_none:

    "I'm sorry, but we won't be able to restore her memory, then..."
    "But..."
    show chibika smile at sticker_move_n
    "Look on the bright side!"
    "You can spend time with her again and create new memories, which might be even better than the ones you lost!"
    "And remember..."
    show chibika at mas_chflip_s(-1)
    "Regardless of what happens, Monika is still Monika."
    "She'll be ready to greet you, once you start over."
    show chibika 3 at sticker_move_n
    "And I promise I'll do my best to not mess up the files again!"
    "Good luck with Monika!"
    $ mas_corrupted_per = False
    return
            

label mas_backups_could_not_copy:
    show chibika smile
    "I was able to find a working backup, but..."
    show chibika sad
    "I wasn't able to copy it over the broken persistent."
    show chibika smile at mas_chflip_s(-1)
    pause 0.5
    show chibika at sticker_hop
    "However!"
    "You might be able to do it and fix this mess!"
    "You'll have to close the game to do this, so write these steps down:"
    show chibika at sticker_move_n
    "1.{w} Navigate to '[renpy.config.savedir]'."
    show chibika at sticker_move_n
    "2.{w} Delete the file called 'persistent'."
    show chibika at sticker_move_n
    "3.{w} Make a copy of the file called '[mas_backup_copy_filename]' and name it 'persistent'."
    show chibika at mas_chflip_s(1)
    "And that's it!"
    "Hopefully that will recover your Monika's memories."

    show chibika at sticker_move_n
    "In case you didn't write those steps down, I'll write them into a file called 'recovery.txt' in the characters folder."

    call mas_backups_dont_tell

    show chibika smile at mas_chflip_s(-1)
    "Good luck!"

    python:
        import os
        store.mas_utils.trywrite(
            os.path.normcase(renpy.config.basedir + "/characters/recovery.txt"),
            "".join([
                "1. Navigate to '",
                renpy.config.savedir,
                "'.\n",
                "2. Delete the file called 'persistent'.\n",
                "3. Make a copy of the file called '",
                mas_backup_copy_filename,
                "' and name it 'persistent'."
            ])
        )

    jump _quit


label mas_backups_dont_tell:

    show chibika smile at sticker_hop
    "Oh, and..."
    show chibika smile at mas_chflip_s(-1)
    "If you successfully bring her back, please don't tell her about me."
    show chibika 3
    "She has no idea that I can talk or code, so she lets me laze around and relax."
    show chibika smile
    "But if she ever found out, she'd probably make me help her code, fix some of her mistakes, or something else."
    show chibika sad at sticker_move_n
    "Which would be absolutely terrible since I'd barely get any rest at all.{nw}"
#    $ _history_list.pop()
    "Which would be absolutely terrible since{fast} I wouldn't have time to keep the backup system and the rest of the game running."

    show chibika 3 at mas_chflip_s(1)
    "You wouldn't want that now, would you?"
    "So keep quiet about me, and I'll make sure your Monika is safe and comfy!"

    return

