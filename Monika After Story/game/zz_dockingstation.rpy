# Module that provides an interface for loading / saving files that we interact with
#
# NOTE: this is meant purely for reading / writing files into base64 with 
#   checksums. If you want readable text files for users, DO NOT USE THIS.
#
# NOTE: some clarifications:
#   - packed files are considered files encoding in base64, but particularly
#       encoded using the mas_packShipment() function. This function will
#       encode files into sized chunks that will work nicely with file io
#   - unpacked files are raw files, not encoded


init -900 python in mas_ics:
    import os
    # Image CheckSums

    ########################## ISLANDS ########################################
    # islands folder
    islands_folder = os.path.normcase(
        renpy.config.basedir + "/game/mod_assets/location/special/"
    )

    # Night With Frame
    islands_nwf = (
        "0ea361ef4c501c15a23eb36b1c47bf1a8eac1b4c2a1bc214e30db9e4f154dbdc"
    )

    # night without frame
    islands_nwof = (
        "fff96da27e029d5bab839bde8b2a00f8d484ad81880522b0e828c8a2cd0a7c97"
    )

    # day with frame
    islands_dwf = (
        "791f379866edf72dc6fd72ae8d7b26af43dd8278b725a0bf2aeb5c72ba04a672"
    )

    # day withotu frame
    islands_dwof = (
        "83963cf273e9f1939ad2fa604d8dfa1912a8cba38ede7f762d53090783ae8ca4"
    )

    # islands dict to map filenames to checksums and real filenames
    # key: filename of b64 encode
    # value: tuple:
    #   [0] - filename to save the image as
    #   [1] - checksum for that image
    islands_map = {
        "nwf": ("night_with_frame.png", islands_nwf),
        "nwof": ("night_without_frame.png", islands_nwof),
        "dwf": ("with_frame.png", islands_dwf),
        "dwof": ("without_frame.png", islands_dwof)
    }
        
    ###########################################################################


init -45 python:
    import os # this thing is super crucial everywhere so we should just
        # keep it open

    class MASDockingStation(object):
        """
        Docking station class designed to help with file reading / writing of
        certain files.
        """
        import hashlib  # sha256 signatures
        import base64   # "packing" shipments involve base64
        from StringIO import StringIO as slowIO
        from cStringIO import StringIO as fastIO

        import store.mas_utils as mas_utils # logging

        # The default docking station is the characters folder
        DEF_STATION = "/characters/"
        DEF_STATION_PATH = os.path.normcase(renpy.config.basedir + DEF_STATION)

        # default read size in bytes
        # NOTE: we use 4095 here since 3 divides evenly into 4095
        READ_SIZE = 4095
        B64_READ_SIZE = 5460

        ## docking station error format
        # 0 - message
        # 1 - docking station as str
        # 2 - exception (if applicable)
        ERR = "[ERROR] {0} | {1} | {2}\n"
        ERR_GET = "Failure getting package '{0}'."
        ERR_OPEN = "Failure opening package '{0}'."
        ERR_READ = "Failure reading package '{0}'."
        ERR_SEND = "Failure sending package '{0}'."
        ERR_SIGN = "Failure to request signature for package '{0}'."
        ERR_SIGNP = "Package '{0}' does not match checksum."

        ## constants returned from smartUnpack (status constants)
        ## these are bit-based
        # errored when we were tryingto red package
        PKG_E = 1

        # if we found the package
        PKG_F = 2

        # did not find package at all
        PKG_N = 4

        # package had bad checksum (corrupted)
        PKG_C = 8


        def __init__(self, station=None):
            """
            Constructor

            IN:
                station - the path to the folder this docking station interacts
                    with. (absolute path) 
                    NOTE: END WITH '/' please
                    (Default: DEF_STATION_PATH)
            """
            if station is None:
                station = self.DEF_STATION_PATH

            if not station.endswith("/"):
                station += "/"

            self.station = os.path.normcase(station)


        def __str__(self):
            """
            toString
            """
            return "DS: [{0}]".format(self.station)

       
        def checkForPackage(self, package_name, check_read=True):
            """
            Checks if a package exists in the docking station

            NOTE: will log exceptions

            NOTE: no signature checking

            IN:
                package_name - the filename we are lookiung for
                check_read - If False, then only check for existence
                    (Default: True)

            RETURNS:
                True if the package exists
                    If check_read is true, then package must also be readable
                False otherwise
            """
            return self.__check_access(
                self._trackPackage(package_name),
                check_read
            )


        def createPackageSlip(self, package, bs=None):
            """
            Generates a checksum for a package (which is a file descriptor)

            NOTE: may throw exceptions

            NOTE: when checking packages, we read by B64_READ_SIZE always

            IN:
                package - file descriptor of the package we want
                    NOTE: is seek(0)'d after reading
                bs - blocksize to use. IF None, the default blocksize is ued
                    (Default: None)

            RETURNS:
                sha256 checksum (hexadec) of the given package, or None
                if error occured
            """
            pkg_slip = self._unpack(package, None, False, True, bs)

            # reset the package when done
            package.seek(0)

            return pkg_slip


        def getPackage(self, package_name):
            """
            Gets a package from the docking station

            NOTE: will log exceptions

            IN:
                package_name - The filename we are looking for

            RETURNS:
                open file descriptor to the package (READ BYTES mode)
                    if package is readable and no errors occurred
                None otherwise
            """
            ### Check access
            if not self.checkForPackage(package_name):
                return None

            ### open the package
            package_path = self._trackPackage(package_name)
            package = None
            try:
                package = open(package_path, "rb")

            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_OPEN.format(package_name),
                    str(self),
                    str(e)
                ))
                if package is not None:
                    package.close()
                return None

            # otherwise, return the opened package
            return package


        def packPackage(self, contents, pkg_slip=False):
            """
            Packs a package so it can be sent
            (encodes a data buffer into base64)

            NOTE: may throw exceptions

            IN:
                contents - the bytes buffer we want to pack. Recommened to use
                    StringIO here, but any buffer that supports read(bytes)
                    will work fine.
                    NOTE: is CLOSED after reading
                pkg_slip - True will generate a checksum for the data buffer
                    and return that as well
                    (Default: False)

            RETURNS:
                tuple of the following format:
                [0] - base64 version of the given data, in a cStringIO buffer
                [1] - sha256 checksum if pkg_slip is True, None otherwise
            """
            box = None
            try:
                box = self.fastIO()

                return (box, self._pack(contents, box, True, pkg_slip))

            except Exception as e:
                # if an error occured, close the box buffer and raise
                if box is not None:
                    box.close()
                raise e

            finally:
                # always close teh data buffer
                contents.close()


        def sendPackage(self, 
                package_name, 
                package, 
                unpacked=False, 
                pkg_slip=False
            ):
            """
            Sends a package into the docking station
            (Writes a file in this stations' folder)

            NOTE: exceptions are logged

            IN:
                package_name - name of the file to write
                package - the data to write as bytes
                unpacked - True means that package is not in base64
                    False means that it is in base64
                    (Default: False)
                pkg_slip - True means we should generate a sha256 checksum for
                    the package and return that 
                    (Default: False)

            RETURNS:
                sha256 checksum if pkg_slip is True
                True if package was sent successfully and pkg_slip is False
                False Otherwise
            """
            mailbox = None
            try:
                ### open the mailbox
                mailbox = open(self._trackPackage(package_name), "wb")

                ### now write to the mailbox
                _pkg_slip = self._pack(package, mailbox, unpacked, pkg_slip)

                ### return pkg slip if we want it
                if pkg_slip:
                    return _pkg_slip

                # otherwise we good
                return True

            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_SEND.format(package_name),
                    str(self),
                    str(e)
                ))
                return False
                
            finally:
                # always close the mailbox
                if mailbox is not None:
                    mailbox.close()

            return False


        def signForPackage(self, 
                package_name,
                pkg_slip,
                keep_contents=False,
                bs=None
            ):
            """
            Gets a package, checks if all the contents are there, and then
            deletes the packaging.
            (Check if a file exists, is readable, has the checksum of the
            passed in pkg_slip, then deletes the file on disk)

            NOTE: Exceptions are logged

            IN:
                package_name - name of the file to check
                pkg_slip - sha256 checksum the file should match
                keep_contents - if True, then we copy the data into a StringIO
                    buffer and return it.
                    (Defualt: False)
                bs - blocksize to use when reading the package
                    IF None, the default blocksize is used
                    (Default: None)

            RETURNS:
                if the package matches signature:
                    - if keep_contents is True
                        StringIO buffer containing decoded data
                    - otherwise, 1 is returned
                if package found but no sig match
                    - NOTE: if this happens, we NEVER delete teh package
                    - return -2
                if package not found
                    - return -1
                0 otherwise (like if error occured)
            """
            package = None
            contents = None
            try:
                ### get the package
                package = self.getPackage(package_name)
                if package is None:
                    return -1

                ### we have a package, lets unpack it
                if keep_contents:
                    # use slowIO since we dont know contents unpacked
                    contents = slowIO()

                # we always want a package slip in this case
                # we only want to unpack if we are keeping contents
                _pkg_slip = self._unpack(
                    package,
                    contents,
                    keep_contents,
                    True,
                    bs
                )

                ### check sigs
                if _pkg_slip != pkg_slip:
                    contents.close()
                    return -2

                ### otherwise we matched sigs, return result
                if keep_contents:
                    return contents

                ### or discard the results 
                if contents is not None:
                    contents.close()

                package.close()
                os.remove(self._trackPackage(package_name))
                return 1

            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_SIGNP.format(package_name),
                    str(self),
                    str(e)
                ))
                if contents is not None:
                    contents.close()
                return 0

            finally:
                # always close the package
                if package is not None:
                    package.close()

            return 0


        def smartUnpack(self, 
                    package_name, 
                    pkg_slip, 
                    contents=None, 
                    one_line=False,
                    b64=True,
                    bs=None
            ):
            """
            Combines parts of signForPackage and _unpack in a way that is very
            useful for us

            NOTE: all exceptions are logged

            NOTE: if contents was passed in an error occurred (PKG_E will be in
                the return bits), then the contents of contents is undefined.

            IN:
                package_name - name of the package to read in
                pkg_slip - chksum to check package with (considerd PRE b64 decode)
                contents - buffer to save contents of package.
                    If None, we save contents to a StringIO object and return
                    that
                    (Default: None)
                one_line - True means we only retrieve a single line from the
                    package
                    (Default: False)
                b64 - True means the package is encoded in base64
                    (Default: True)
                bs - blocksize to use. By default, we use B64_READ_SIZE
                    (Default: None)

            RETURNS: tuple of the following format
                [0]: PKG_* bits constants highlighting success/failure status
                [1]: buffer containing the contents of the package.
                    If contents is not None, this is the same reference as
                    contents.
            """
            # First, lets try and get the package
            package = self.getPackage(package_name)

            # no package? this should already have been logged, so lets just
            # return appropriate stuff
            if package is None:
                return (self.PKG_N, None)

            # otherwise we have the package. Lets setup buffers and blocksizes
            if bs is None:
                bs = self.B64_READ_SIZE

            # internalize contents so we can do proper file closing
            if contents is None:
                _contents = self.slowIO()
            else:
                _contents = contents

            # as well as the return bytes
            ret_val = self.PKG_F

            # and our pkgslip checker
            checklist = self.hashlib.sha256()

            # and attempt to decode package
            keep_saving = True
            try:
                # iterator for looping
                _box = MASDockingStation._blockiter(package, bs)

                # and now we look. However we only save what is asked of us
                for packed_item in _box:
                    checklist.update(packed_item)

                    if keep_saving:
                        # writing out contents to buffer
                        _contents.write(self.base64.b64decode(packed_item))

                        if one_line:
                            # stop saving contents if we only want 1 line
                            keep_saving = False

            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_READ.format(package_name),
                    str(self),
                    str(e)
                ))

                if contents is None:
                    # only close our internal contents if we made it
                    _contents.close()

                return (ret_val | self.PKG_E, None)

            finally:
                # always close package after this
                package.close()

            # now to check checksums
            if checklist.hexdigest() != pkg_slip:
                # no match? uh oh, lets return stuff anyway
                return (ret_val | self.PKG_C, _contents)

            # otherwise, we got a match so
            return (ret_val, _contents)


        def unpackPackage(self, package, pkg_slip=None):
            """
            Unpacks a package
            (decodes a base64 file into a regular StringIO buffer)

            NOTE: may throw exceptions

            IN:
                package - file descriptor of the file to decode / unpack
                    NOTE: is CLOSED after reading
                pkg_slip - sha256 hex checksum of what the package data should
                    be. If passed in, then we check this against the package
                    NOTE: generated checksum uses data BEFORE it is decoded
                    (Default: None)

            RETURNS:
                StringIO buffer containing the package decoded
                Or None if pkg_slip checksum was passed in and the given 
                    package failed the checksum
            """
            contents = None
            try:
                # NOTE: we use regular StringIO in case of unicode
                contents = self.slowIO()

                _pkg_slip = self._unpack(
                    package,
                    contents,
                    True,
                    pkg_slip is not None
                )

                if pkg_slip is not None and _pkg_slip != pkg_slip:
                    # checksum checking
                    contents.close()
                    return None

                return contents

            except Exception as e:
                # if we get an exception, close the contents buffer and raise
                # the exception 
                if contents is not None:
                    contents.close()
                raise e

            finally:
                # Always close the package when we're done
                package.close()


        @staticmethod
        def _blockiter(fd, blocksize):
            """
            Creates an itererator of a file using the given blocksize

            NOTE: May throw exceptions

            IN:
                fd - file descriptor
                    NOTE: seeks this to 0 before starting
                blocksize - size to use for blocks

            YIELDS:
                blocks until a block read attempt gave us nothing

            ASSUMES:
                given file descriptor is open
            """
            fd.seek(0)
            block = fd.read(blocksize)
            while len(block) > 0:
                yield block
                block = fd.read(blocksize)


        def _trackPackage(self, package_name):
            """
            Adds this docking station's path tot he package_name so we can
            access it and stuff

            IN:
                package_name - name of the package

            RETURNS:
                package_name in a valid package_path ready for checking
            """
            return os.path.normcase(self.station + package_name)


        def _pack(self, contents, box, pack=True, pkg_slip=True, bs=None):
            """
            Runs the packing algorithm for given file descriptors
            Supports:
                1. encoding and checksumming data
                    this will encode the input, checksum it, then write to
                    output
                2. encoding data
                    this will encode the input, then write to output
                3. checksumming data
                    this will checksum the input. DOES NOT WRITE to output

            NOTE: may throw exceptions
            NOTE: if both pack and pkg_slip are False, this does absoultely
                nothing

            IN:
                contents - file descriptor to read data from
                box - file descriptor to write data to
                pack - if True, encode the input data into base64 prior to
                    writing to output data
                    (Default: True)
                pkg_slip - if True, generate a checksum of the data.
                    NOTE: if pack is True, this is done using data AFTER
                        encoding
                    (Default: True)
                bs - blocksize to use. If None, we use READ_SIZE
                    (Default: None)

            RETURNS:
                generated sha256 checksum if pkg_slip is True
                Otherwise, None
            """
            if not (pkg_slip or pack):
                return None

            if bs is None:
                bs = self.READ_SIZE

            _contents = MASDockingStation._blockiter(contents, bs)

            if pkg_slip and pack:
                # encode the data, then checksum the base64, then write to 
                # output
                checklist = self.hashlib.sha256()

                for item in _contents:
                    packed_item = self.base64.b64encode(item)
                    checklist.update(packed_item)
                    box.write(packed_item)

                return checklist.hexdigest()

            elif pack:
                # encode the data, write to output
                for item in _contents:
                    box.write(self.base64.b64encode(item))

            else:
                # checksum the data
                checklist = self.hashlib.sha256()

                for item in _contents:
                    checklist.update(self.base64.b64encode(item))

                return checklist.hexdigest()

            return None


        def _unpack(self, box, contents, unpack=True, pkg_slip=True, bs=None):
            """
            Runs the unpacking algorithm for given file descriptors
            Supports:
                1. checksumming and decoding data
                    this will checksum input, decode it, then write to output
                2. decoding data
                    this will decode the input, then write to ouput
                3. checksumming data
                    this will checksum the input. DOES NOT WRITE to output

            NOTE: may throw exceptions
            NOTE: if both unpack and pkg_slip are False, this does absolutely
                nothing

            IN:
                box - file descriptor to read data from
                contents - file descriptor to write data to
                unpack - if True, decode input data from base64 prior to 
                    writing output data
                    (Default: True)
                pkg_slip - if True, genereate a checksum of the data.
                    NOTE: if unpack is True, this is done using data BEFORE
                        decoding
                    (Default: True)
                bs - blocksize to use. If None, use B64_READ_SIZE
                    (Default: None)

            RETURNS:
                generated sha256 checksum if pkg_slip is True
                Otherwise, None
            """
            if not (pkg_slip or unpack):
                return None

            if bs is None:
                bs = self.B64_READ_SIZE

            _box = MASDockingStation._blockiter(box, bs)

            if pkg_slip and unpack:
                # checksum data, decode it, write to output
                checklist = self.hashlib.sha256()

                for packed_item in _box:
                    checklist.update(packed_item)
                    contents.write(self.base64.b64decode(packed_item))

                return checklist.hexdigest()

            elif pkg_slip:
                # checksum data
                checklist = self.hashlib.sha256()

                for packed_item in _box:
                    checklist.update(packed_item)

                return checklist.hexdigest()

            else:
                # decode the data
                for packed_item in _box:
                    contents.write(self.base64.b64decode(packed_item))

            return None


        def __check_access(self, package_path, check_read):
            """
            Checks access of the file at package_path

            NOTE:
                will log exceptions

            IN:
                package_path - path to the file we want to check access to
                check_read - If True, check for read access in addition to
                    file existence

            RETURNS:
                True if package exists / is readable.
                Otherwise:
                    if check_read is True, returns None
                    otherwise, returns False
            """
            try:
                file_ok = os.access(package_path, os.F_OK)
                read_ok = os.access(package_path, os.R_OK)

            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_GET.format(package_path),
                    str(self),
                    str(e)
                ))

                # in error case, assume failure
                return self.__bad_check_read(check_read)

            if check_read:
                if not (file_ok and read_ok):
                    return None

            else:
                if not file_ok:
                    return False

            return True


        def __bad_check_read(check_read):
            """
            Returns an appropriate failure value givne the check_read value

            IN:
                check_read - the value of check_read

            RETURNS:
                None if check_read is True, False otherwise
            """
            if check_read:
                return None

            return False


    mas_docking_station = MASDockingStation()


default persistent._mas_moni_chksum = None

# these should have the same size
# these are also datetimes
default persistent._mas_dockstat_checkout_log = list()
default persistent._mas_dockstat_checkin_log = list()

# this value should be in bytes
# NOTE: do NOT set this directly. Use the helper functions
default persistent._mas_dockstat_moni_size = 0

init -500 python in mas_dockstat:
    # blocksize is relatively constant
    blocksize = 4 * (1024**2)
    b64_blocksize = 5592408 # (above size converted to base64)

    ## package constants for the state of monika
    # Monika not found
    MAS_PKG_NF = 1

    # Monika found
    MAS_PKG_F = 2

    # Not our monika was found
    MAS_PKG_FO = 3

init python in mas_dockstat:
    import store

    # blocksize is relatively constant
    blocksize = 4 * (1024**2)

    # previous vars dict
    previous_vars = dict()

    def setMoniSize(tdelta):
        """
        Sets the appropriate persistent size for monika

        IN:
            tdelta - timedelta to use
        """
        # get hours
        days = tdelta.days
        secs = tdelta.seconds
        hours = (days * 24) + (secs / 3600.0)

        # our rates
        first100 = 0.54
        post100 = 0.06

        # megabytes
        mbs = 0

        if hours > 100:
            mbs = 100 * first100
            hours -= 100
            mbs += hours * post100

        else:
            mbs = hours * first100

        # now we can set the final size (in MiB)
        store.persistent._mas_dockstat_moni_size = int(mbs * (1024**2))



init 200 python in mas_dockstat:
    # special store 
    # lets use this store to handle generation of docking station files
    import store
    import store.mas_utils as mas_utils
    import store.mas_sprites as mas_sprites
    import store.mas_greetings as mas_greetings
    import store.evhand as evhand
    from cStringIO import StringIO as fastIO
    import os
    import random

    def generateMonika(dockstat):
        """
        Generates / writes a monika blob file.

        NOTE: This does both generation and integretiy checking
        NOTE: exceptions are logged

        IN:
            dockstat - the docking station to generate Monika in

        RETURNS:
            checksum of monika
            -1 if checksums didnt match (and we cant verify data integrity of
                the generated moinika file)
            None otherwise

        ASSUMES:
            blocksize - this is a constant in this store
        """
        ### other stuff we need
        # inital buffer
        moni_buffer = fastIO()

        ### metadata elements
        END_DELIM = "|||"
        num_5 = "{:05d}"
        num_2 = "{:02d}"
        num_f = "{:6f}"
        first_sesh = ""
        affection_val = ""
       
        # metadata parsing
        if store.persistent.sessions is not None:
            first_sesh_dt = store.persistent.sessions.get("first_session",None)

            if first_sesh_dt is not None:
                first_sesh = str(first_sesh_dt)
#                first_sesh = "".join([
#                    num_5.format(first_sesh_dt.year),
#                    num_2.format(first_sesh_dt.month),
#                    num_2.format(first_sesh_dt.day)
#                ])

        if store.persistent._mas_affection is not None:
            _affection = store.persistent._mas_affection.get("affection", None)
            
            if _affection is not None:
                affection_val = num_f.format(_affection)

        # build metadata list
        moni_buffer.write("|".join([
            first_sesh,
            store.persistent.playername,
            store.persistent._mas_monika_nickname,
            affection_val,
            store.monika_chr.hair,
            store.monika_chr.clothes
        ]) + END_DELIM)

        ### monikachr
        moni_chr = None
        try:
            moni_chr = open(os.path.normcase(
                renpy.config.basedir + "/game/mod_assets/monika/mbase"
            ), "rb")

            # NOTE: moin_chr is going to be less than 200KB, this be fine
            moni_buffer.write(moni_chr.read())

        except Exception as e:
            mas_utils.writelog("[ERROR] mbase copy failed | {0}".format(
                str(e)
            ))
            moni_buffer.close()
            return None
            
        finally:
            # always close moni_chr
            if moni_chr is not None:
                moni_chr.close()

        ### now we must do the streamlined write system to file
        moni_path = dockstat._trackPackage("monika")
        moni_fbuffer = None
        moni_sum = None
        try:
            # first, lets open up the moni file buffer
            moni_fbuffer = open(moni_path, "wb")

            # now open up the checklist and encoders
            checklist = dockstat.hashlib.sha256()
            encoder = dockstat.base64.b64encode

            # and write out the metadata / monika
            # NOTE: we can do this because its under our 4MB block size
            data = encoder(moni_buffer.getvalue())
            checklist.update(data)
            moni_fbuffer.write(data)

            # and now for the random data generation
            # NOTE: this should represent number of bytes
            moni_size = store.persistent._mas_dockstat_moni_size
            moni_size_limit = moni_size - blocksize
            curr_size = 0

            while curr_size < moni_size_limit:
                data = encoder(os.urandom(blocksize))
                checklist.update(data)
                moni_fbuffer.write(data)
                curr_size += blocksize

            # we should have some leftovers
            leftovers = moni_size - curr_size
            if leftovers > 0:
                data = encoder(os.urandom(leftovers))
                checklist.update(data)
                moni_fbuffer.write(data)

            # great! lets go ahead and save the digest
            moni_sum = checklist.hexdigest()

        except Exception as e:
            mas_utils.writelog("[ERROR] monibuffer write failed | {0}".format(
                str(e)
            ))

            # attempt to delete existing file if its there
            # NOTE: dont care if it fails, we just want to try it 
            try:
                # NOTE: we do buffer closing here because we need to try
                # file deletion in here too
                if moni_fbuffer is not None:
                    moni_fbuffer.close()

                moni_fbuffer = None
                os.remove(moni_path)
            except:
                pass

            return None

        finally:
            # always close the fbuffer
            if moni_fbuffer is not None:
                moni_fbuffer.close()

            # we dont need this buffer after here
            moni_buffer.close()

        ### Now to verify that we output the file correctly
        moni_pkg = dockstat.getPackage("monika")
        if moni_pkg is None:
            # ALERT ALERT HOW DID WE FAIL
            mas_utils.writelog("[ERROR] monika not found.")
            mas_utils.trydel(moni_path)
            return None

        # we should have a file descriptor, lets attempt a pkg slip
        moni_slip = dockstat.createPackageSlip(moni_pkg, blocksize)
        if moni_slip is None:
            # ALERT ALERT WE FAILED AGAIN
            mas_utils.writelog("[ERROR] monika could not be validated.")
            mas_utils.trydel(moni_path)
            return None

        if moni_slip != moni_sum:
            # WOW SRS THIS IS BAD
            mas_utils.writelog(
                "[ERROR] monisums didn't match, did we have write failure?"
            )
            mas_utils.trydel(moni_path)
            return -1

        # otherwise, we managed to create a monika! Congrats!
        return moni_sum


    def findMonika(dockstat):
        """
        Attempts to find monika in the giving docking station

        RETURNS: tuple of the following format:
            [0]: MAS_PKG_* constants depending on the state of monika
            [1]: string of important data, if we found a monika. Will be empty
                if no monika or data found
        """
        END_DELIM = "|||"

        status, first_line = dockstat.smartUnpack(
            "monika",
            store.persistent._mas_moni_chksum,
            one_line=True,
            bs=b64_blocksize
        )

        if (status & (dockstat.PKG_E | dockstat.PKG_N)) > 0:
            # we had an error in reading, therefore we cant trust the data.
            # OR, we didnt find the package.
            # in either case, just say we didnt find monika
            return (MAS_PKG_NF, "")

        # otherwise, we certainly found monika
        # lets parse monika's data

        # reset this buffer
        first_line.seek(0)

        # we only want the data portion that's likely to contain our stuff
        real_data = first_line.read(dockstat.READ_SIZE)
        first_line.close()

        # and see if this does contain our stuff
        real_data, sep, garbage = real_data.partition(END_DELIM)

        # and return results
        if len(sep) == 0:
            # no data found, assume a missing monika
            return (MAS_PKG_NF, "")

        if (status & dockstat.PKG_C) > 0:
            # we found a different monika (or corrupted monika)
            return (MAS_PKG_FO, real_data)

        # otherwise, we have a matching monika!
        return (MAS_PKG_F, real_data)


    def parseMoniData(data_line):
        """
        Parses monika data into its components

        NOTE: all exceptions are logged

        IN:
            data_line - PIPE delimeted data line

        RETURNS: list of the following format:
            [0]: datetime of first sessin
            [1]: playername
            [2]: monika's nickname (could be Monika)
            [3]: affection, integer value (dont really rely on this for much)
            [4]: monika's hair setting
            [5]: monika's clothes setting
            
            OR None if general (not item-specific) parse errors occurs)
        """
        try:
            data_list = data_line.split("|")
            
            # now parse what needs to be parsed
            data_list[0] = mas_utils.tryparsedt(data_list[0])
            data_list[3] = mas_utils.tryparseint(data_list[3], 0)
            data_list[4] = mas_sprites.tryparsehair(data_list[4])
            data_list[5] = mas_sprites.tryparseclothes(data_list[5])

            # and return only the parts we want
            return data_list[:6]

        except Exception as e:
            mas_utils.writelog("[ERROR]: Moni Data parse fail: {0}\n".format(
                str(e)
            ))
            return None


    def selectReturnHomeGreeting(_type=None):
        """
        Selects the correct Return Home greeting.
        Return Home-style greetings must have TYPE_GO_SOMEWHERE in the category

        NOTE: this calls mas_getEV, so do NOT run this function prior to 
            runtime
        
        IN:
            _type - list of additoinal mas_greetings types to search on

        RETURNS:
            Event object representing the selected greeting
        """
        if _type is not None:
            greeting_types = list(_type)
        else:
            greeting_types = list()

        # add the return home type
        greeting_types.append(mas_greetings.TYPE_GO_SOMEWHERE)

        # and now we need to find greetings that fit
        rethome_greetings = store.Event.filterEvents(
            evhand.greeting_database,
            unlocked=True,
            category=(False, greeting_types)
        )

        if len(rethome_greetings) > 0:
            # if we have at least one from this list, random select
            return rethome_greetings[random.choice(rethome_greetings.keys())]

        # otherwise, always return the generic random event
        return store.mas_getEV("greeting_returned_home")


### Docking station labels regarding monika leaving the station

# call this label when monika is ready to leave the station
# RETURNS:
#   true if moni can leave
#   false otherwise
label mas_dockstat_ready_to_go:
    show monika 2dsc

    # generate the monika file
    $ moni_chksum = store.mas_dockstat.generateMonika(mas_docking_station)
    $ can_moni_leave = moni_chksum is not None and moni_chksum != -1
     
    if can_moni_leave:
        # file successfully made
        # monika can leave
        if len(persistent._mas_dockstat_checkout_log) == 0:
            call mas_dockstat_first_time_goers

        else:
            m 1eua "Alright."

        m 1eua "I'm ready to go."

        $ persistent._mas_moni_chksum = moni_chksum

    else:
        # we failed to generate file somehow
        m 1ekc "Oh no..."
        m 1lksdlb "I wasn't able to turn myself into a file."
        m "I think you'll have to go on without me this time."
        m 1ekc "Sorry, [player]."

    return can_moni_leave


label mas_dockstat_first_time_goers:
    m 3eua "I'm now in the file 'monika' in your characters folder."
    m "After I shutdown the game, you can move me wherever you like."
    m 3eub "But make sure to bring me back to the characters folder before turning the game on again, okay?"

    m 1eua "And lastly..."
    m 1ekc "Please be careful with me. It's so easy to delete files after all..."
    m 1eua "Anyway..."
    return

# empty desk. This one includes file checking every 1 seconds for monika
label mas_dockstat_empty_desk:
    call spaceroom(hide_monika=True)

    # empty desk should be a zorder lower so we can pop monika over it
    $ ed_zorder = MAS_MONIKA_Z - 1
    show emptydesk zorder ed_zorder at i11

label mas_dockstat_empty_desk_loop:

    python:
        # setup ui hiding
        import store.mas_dockstat as mas_dockstat
        mas_OVLHide()
        mas_calRaiseOverlayShield()
        disable_esc()
        mas_enable_quit()

        # now just check for monika
        moni_found = False
        while not moni_found:
            # wait a second
            renpy.pause(1.0, hard=True)

            moni_status, moni_data = mas_dockstat.findMonika(
                mas_docking_station
            )

            if moni_status == mas_dockstat.MAS_PKG_FO:
                # found a different monika, jump to the different monika
                # greeting
                moni_found = True

                # with a different monika, she won't care if you quit, but
                # if you do, it's game over for this monika

                renpy.jump("mas_dockstat_different_monika")

            if moni_status = mas_dockstat.MAS_PKG_F:
                # found our monika, jump to the found monika greeting
                moni_found = True

                # but we gotta clear some of the ui hiding stuff
                enable_esc()
                mas_disable_quit()

                renpy.jump("mas_dockstat_found_monika")

            # otherwise we still havent' found monika, so lets just continue
            # the loop

    # we should never, ever reach here. If we do, just do a straight quit
    jump _quit

define mas_dockstat.different_moni_flow = False

# different monika found
label mas_dockstat_different_monika:
    # ASSUMES:
    #   moni_data - data line of the monika we read in. Would need parsing

    # NOTE: we also need to save current vars so we dont have issues
    $ mas_dockstat.previous_vars["m_name"] = persistent._mas_monika_nickname
    $ mas_dockstat.previous_vars["playername"] = persistent.playername
    $ mas_dockstat.previous_vars["hair"] = persistent._mas_monika_hair
    $ mas_dockstat.previous_vars["clothes"] = persistent._mas_monika_clothes

    # we set this to true so in QUIT we can delete monika if you quit before
    # resolving this monika situation (as well as reset some previous vars)
    $ mas_dockstat.different_moni_flow = True

    # NOTE: in this case, we need to completely avoid the traditional
    # spaceroom logic since we need to assume that this monika is different
    # this means the greeting is entirely held in here.

    # first, lets split the data and get some meaningful results
    $ moni_data = mas_dockstat.parseMoniData(moni_data)

    if moni_data is None:
        # bad data means we actually have a corrupted monika. Let's delete her
        # and return to empty desk
        $ store.mas_utils.trydel(mas_docking_station._trackPackage("monika"))
        $ mas_dockstat.different_moni_flow = False
        jump mas_dockstat_empty_desk

    # otherwise, we have a monika. Let's setup some vars and do some dialgoue
    # NOTE: some key vars have been overwritten here. Please watch out for the
    #   player - player's name
    #   m_name - monika's name
    $ moni_sesh, player, m_name, aff_val, moni_hair, moni_clothes = moni_data
    $ monika_chr.change_outfit(moni_clothes, moni_hair)

    # and then we can begin talking
    show monika 1ekd zorder MAS_MONIKA_Z at t11

    # 1 line of dialgoue before we remove the empty desk
    m "[player]?" 
    hide emptydesk

    m "Wait, you're not [player]."




    

    jump ch30_post_greeting_check

# found our monika
label mas_dockstat_found_monika:
    # ASSUMES:
    #   moni_data - data line of the monika we read in. Would need parsing


    jump ch30_post_greeting_check
