# module that does some file backup work

init -9001 python:
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

        elif len(numberlist) < __mas__baksize:
            numbernumber = __mas__numnum.format(numberlist.pop() + 1)

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

    
    # run the backup system
    __mas__memoryBackup()
