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

default persistent._mas_pm_taken_monika_out = False
# True if the user has taken monika out of the spaceroom

init -900 python in mas_ics:
    import os
    # Image CheckSums

    ########################## ISLANDS ########################################
    # islands folder
    islands_folder = os.path.normcase(
        renpy.config.basedir + "/game/mod_assets/location/special/"
    )

    # NOTE: these checksums are BEFORE b64 encoding

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

    # rain with frame
    islands_rwf = (
        "5854576632f76d9a99c8c69c8b4a6c2053241c0cb7550c31aa49ab0454635e36"
    )

    # rain without frame
    islands_rwof = (
        "e78eaf99bc56f22f16579c3a22f336db838d36c84ac055f193aec343deb5c9dc"
    )

    # night rain with frame
    islands_nrwf = (
        "68610912a463d267d4bd74400909204b5efe2249e71b348f2cc911b79fea3693"
    )

    # night rain without frame
    islands_nrwof = (
        "37e01bb69418ebb825c2955b645391a1fb99e13c76b1adb47483d6cc02c1d8e3"
    )

    # overcast with frame
    islands_owf = (
        "4917416ab2c390846bdc59fa25a995d2a5be1be0ddbc3860048aef4fe670fa70"
    )

    # overcast without frame
    islands_owof = (
        "4b4dc5ccfa81de15e09ee01ea7ee7ff3a5c498a5a4d660e8579dd5556599ae1b"
    )

    # night overcast with frame
    islands_nowf = (
        "21e8b98faafb24778df5cce17876e0caf822f314c9f80c6d63e7d2a3d68ab54a"
    )

    # night overcast without frame
    islands_nowof = (
        "ac6e6d09cd18aa30a8dd2e33879b0669590f303fe98c9dba8ce1b5dd0c8212ba"
    )

    # snow with frame
    islands_swf = (
        "510a7fc62321f3105c99c74fd53d06f4e20f6e4cc20d794327e3094da7a5d168"
    )

    # snow without frame
    islands_swof = (
        "262242dd67ae539bae0c7022d615696d19acb85fc7723f545a00b65aeb13be24"
    )

    # night snow with frame
    islands_nswf = (
        "c426957bda7740b361bc010a2f6ddb0a8fa2a1a983da9c40249a0648117f45a9"
    )

    # night snow without frame
    islands_nswof = (
        "822ed24c0250a273f6e614790a439473f638ce782e505507e617e56e85ffc17f"
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
        "dwof": ("without_frame.png", islands_dwof),
        "rwf": ("rain_with_frame.png", islands_rwf),
        "rwof": ("rain_without_frame.png", islands_rwof),
        "nrwf": ("night_rain_with_frame.png", islands_nrwf),
        "nrwof": ("night_rain_without_frame.png", islands_nrwof),
        "owf": ("overcast_with_frame.png", islands_owf),
        "owof": ("overcast_without_frame.png", islands_owof),
        "nowf": ("night_overcast_with_frame.png", islands_nowf),
        "nowof": ("night_overcast_without_frame.png", islands_nowof),
        "swf": ("snow_with_frame.png", islands_swf),
        "swof": ("snow_without_frame.png", islands_swof),
        "nswf": ("night_snow_with_frame.png", islands_nswf),
        "nswof": ("night_snow_without_frame.png", islands_nswof)
    }

    #################################### O31 ##################################
    # cg folder
    o31_cg_folder = os.path.normcase(
        renpy.config.basedir + "/game/mod_assets/monika/cg/"
    )

    # marisa cg
    o31_marisa = (
        "6a05463e8200af9846e7f70f4c03e6feddb6c5a93395d7b17a91a6fd23da29af"
    )

    # rin cg
    o31_rin = (
        "c8fb05e801e0eb1f234b4af99d910e561a9afbbd1a5df6bee6edd602c94adb81"
    )

    # cg dict to map filenames to checksums and real filenames
    # key: filename of b64 encode
    # value: tuple:
    #   [0] - filename to save the image as
    #   [1] - checksum for that image
    o31_map = {
        "o31mcg": ("o31_marisa_cg.png", o31_marisa),
        "o31rcg": ("o31_rin_cg.png", o31_rin)
    }

    #################################### RPY ##################################
    #game folder
    game_folder = os.path.normcase(
        renpy.config.basedir + "/game/"
    )
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
        ERR_DEL = "Failure removing package '{0}'."
        ERR_GET = "Failure getting package '{0}'."
        ERR_OPEN = "Failure opening package '{0}'."
        ERR_READ = "Failure reading package '{0}'."
        ERR_SEND = "Failure sending package '{0}'."
        ERR_SIGN = "Failure to request signature for package '{0}'."
        ERR_SIGNP = "Package '{0}' does not match checksum."
        ERR_CREATE = "Failed to create directory '{0}'"

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
                    with. (absolute path), will try to create the folder if it
                    doesn't exist. Exceptions will be logged.
                    NOTE: END WITH '/' please
                    (Default: DEF_STATION_PATH)
            """
            if station is None:
                station = self.DEF_STATION_PATH

#            if not station.endswith("/"):
#                station += "/"

            self.station = os.path.normcase(station)
            self.enabled = True

            if not os.path.isdir(self.station):
                try:
                    os.makedirs(self.station)
                except Exception as e:
                   store.mas_utils.writelog(self.ERR.format(
                       self.ERR_CREATE.format(self.station),
                       str(self),
                       repr(e)
                   ))
                   self.enabled = False

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
            if not self.enabled:
                return False

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
            if not self.enabled:
                return None

            pkg_slip = self._unpack(package, None, False, True, bs)

            # reset the package when done
            package.seek(0)

            return pkg_slip


        def destroyPackage(self, package_name):
            """
            Attempts to destroy the given package in the docking station.

            NOTE: exceptions are logged

            IN:
                package_name - name of the package to delete

            RETURNS:
                True if package no exist or was deleted. False otherwise
            """
            if not self.enabled:
                return False

            if not self.checkForPackage(package_name, False):
                return True

            # otherwise we have a package
            try:
                os.remove(self._trackPackage(package_name))
                return True

            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_DEL.format(package_name),
                    str(self),
                    repr(e)
                ))
                return False


        def getPackageList(self, ext_filter=""):
            """
            Gets a list of the packages in the docking station.
            We also ensure that the item retrieved is not a folder.

            IN:
                ext_filter - extension filter to use when getting list.
                    the '.' is added if not already given.
                    If not given, we get all the packages
                    (Default: "")

            RETURNS: list of packages
            """
            if not self.enabled:
                return []

            # correct filter if needed
            if len(ext_filter) > 0 and not ext_filter.startswith("."):
                ext_filter = "." + ext_filter

            return [
                package
                for package in os.listdir(self.station)
                if package.endswith(ext_filter)
                and not os.path.isdir(self._trackPackage(package))
            ]


        def getPackage(self, package_name, log=None):
            """
            Gets a package from the docking station

            NOTE: will log exceptions

            IN:
                package_name - The filename we are looking for
                log - log to write messages to, if needed
                    If None, we use mas_log
                    (Default: None)

            RETURNS:
                open file descriptor to the package (READ BYTES mode)
                    if package is readable and no errors occurred
                None otherwise
            """
            if not self.enabled:
                return None

            ### Check access
            if not self.checkForPackage(package_name):
                return None

            ### open the package
            package_path = self._trackPackage(package_name)
            package = None
            try:
                package = open(package_path, "rb")

            except Exception as e:
                msg = self.ERR.format(
                    self.ERR_OPEN.format(package_name),
                    str(self),
                    repr(e)
                )

                if log is None:
                    mas_utils.writelog(msg)
                else:
                    log.write(msg)

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


        def safeRandom(self, amount):
            """
            Generates a random amount of unicode-safe bytes.

            IN:
                amount - number of bytes to generate
            """
            return self.base64.b64encode(os.urandom(amount))[:amount]


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
            if not self.enabled:
                return False

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
            if not self.enabled:
                return 0

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
                    lines=0,
                    b64=True,
                    bs=None,
                    log=None
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
                lines - number of lines to retrieve when reading data.
                    If less than 0, then we scan the file itself to tell us
                    how many lines to read.
                    If "all", then we read ALL LINES
                    (Default: 0)
                b64 - True means the package is encoded in base64
                    (Default: True)
                bs - blocksize to use. By default, we use B64_READ_SIZE
                    (Default: None)
                log - log to write messages to, if needed.
                    If None, we use mas_log
                    (Default: None)

            RETURNS: tuple of the following format
                [0]: PKG_* bits constants highlighting success/failure status
                [1]: buffer containing the contents of the package.
                    If contents is not None, this is the same reference as
                    contents.
            """
            NUM_DELIM = "|num|"

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
            if lines == "all":
                # nothing we read should be 200 million lines of 4MB
                lines = 20000000

            try:
                # iterator for looping
                _box = MASDockingStation._blockiter(package, bs)

                # no lines means we need to look for them instead
                if lines < 0:
                    first_item = next(_box, None)

                    if first_item is None:
                        raise Exception("EMPTY PACKAGE")

                    checklist.update(first_item)
                    first_unpacked = self.base64.b64decode(first_item)

                    # parse the line for the first NUM_DELIM
                    raw_num, sep, remain = first_unpacked.partition(NUM_DELIM)
                    if len(sep) == 0:
                        raise Exception(
                            "did not find sep. size of first {0}".format(
                                len(raw_num)
                            )
                        )

                    num = mas_utils.tryparseint(raw_num, -1)

                    if num < 0:
                        # this is a problem. Raise an exception
                        raise Exception(
                            "did not find lines. found {0}".format(raw_num)
                        )

                    # otherwise, set lines to num
                    lines = num

                    if lines > 0:
                        # do we save the first line?
                        _contents.write(remain)
                        lines -= 1

                # and now to look at the rest.
                # only save what we need though
                for packed_item in _box:

                    checklist.update(packed_item)

                    if lines > 0:
                        # writing out contents to buffer
                        _contents.write(self.base64.b64decode(packed_item))
                        lines -= 1


            except Exception as e:
                msg = self.ERR.format(
                    self.ERR_READ.format(package_name),
                    str(self),
                    repr(e)
                )

                if log is None:
                    mas_utils.writelog(msg)
                else:
                    log.write(msg)

                if contents is None:
                    # only close our internal contents if we made it
                    _contents.close()

                return (ret_val | self.PKG_E, None)

            finally:
                # always close package after this
                package.close()

            # get checksum and log
            chk = checklist.hexdigest()
            msg = "chk: {0}\n".format(chk)
            if log is None:
                mas_utils.writelog(msg)
            else:
                log.write(msg)

            # now check checksum
            if chk != pkg_slip:
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
            if not self.enabled:
                return None

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
            if not self.enabled:
                return None

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
            if not self.enabled:
                return None

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
            Checks access of the file at package_path.
            Also ensures that the file is not actually is folder.

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
            if not self.enabled:
                return False

            try:
                file_ok = os.access(package_path, os.F_OK)
                read_ok = os.access(package_path, os.R_OK)
                not_dir = not os.path.isdir(package_path)

            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_GET.format(package_path),
                    str(self),
                    repr(e)
                ))

                # in error case, assume failure
                return self.__bad_check_read(check_read)

            if check_read:
                if not (file_ok and read_ok and not_dir):
                    return None

            return file_ok and not_dir

        def __bad_check_read(self, check_read):
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

# these should have the same size during runtime (except for empty desk mode)
# NOTE: this is only for OUR monika. Rogue monikas are not added here.
# these should basically consist of tuples:
#   [0]: datetime of event
#   [1]: checksum of Monika during this event
default persistent._mas_dockstat_checkout_log = list()
default persistent._mas_dockstat_checkin_log = list()

# dict matching monika checksums to some monika state.
# basically, if a rogue monika appears, we save her checksum to this dict
# and store some additional data.
# NOTE: to prevent collisions, if a monika file generated by this MAS has the
#   same checksum as one in this dict, we pop that checksum off this dict.
#   Yes, we basically forget a monika, but there's no use in trying to make
#   this perfect. For the majority of people, checksums will never collide.
# key: checksum of the rogue monika
# value: TODO: not sure of this yet, probably giong to be a dict so we can
#   make the values malleable
default persistent._mas_dockstat_moni_log = dict()

# set this if we are on the path to leave.
default persistent._mas_dockstat_going_to_leave = False

# this value should be in bytes
# NOTE: do NOT set this directly. Use the helper functions
default persistent._mas_dockstat_moni_size = 0

default persistent._mas_bday_sbp_reacted = False
# True means we have reacted to the surprise birthday party.
# NOTE: we need to consider how we want to do this in future bdays. probably
# may do historical when we can


init -500 python in mas_dockstat:
    # blocksize is relatively constant
    blocksize = 4 * (1024**2)
    b64_blocksize = 5592408 # (above size converted to base64)

    ## package constants for the state of monika
    # bit-based
    # Monika not found
    MAS_PKG_NF = 1

    # Monika found
    MAS_PKG_F = 2

    # Not our monika was found
    MAS_PKG_FO = 4

    # Monika data is in list form
    MAS_PKG_DL = 8

    # Monika data is in persitent form
    MAS_PKG_DP = 16

    ## surprise party constants for the state of the surprise party
    # bit based

    MAS_SBP_NONE = 1
    # no surprise party files

    MAS_SBP_CAKE = 2
    # cake was found

    MAS_SBP_BANR = 4
    # banner was found

    MAS_SBP_BLON = 8
    # balloon was found

init -11 python in mas_dockstat:
    import store.mas_utils as mas_utils

    def decodeImages(dockstat, image_dict, selective=[]):
        """
        Attempts to decode the iamges

        IN:
            dockstat - docking station to use
            image_dict - image map to use
            selective - list of images keys to decode
                If not passed in, we decode EVERYTHINg
                (DEfault: [])

        Returns TRUE upon success, False otherwise
        """
        if len(selective) == 0:
            selective = image_dict.keys()

        for b64_name in selective:
            real_name, chksum = image_dict[b64_name]

            # read in the base64 versions, output an image
            b64_pkg = dockstat.getPackage(b64_name)

            if b64_pkg is None:
                # if we didnt find the image, we in big trouble
                return False

            # setup the outfile
            real_pkg = None
            real_chksum = None
            real_path = dockstat._trackPackage(real_name)

            # now try to decode image
            try:
                real_pkg = open(real_path, "wb")

                # unpack this package
                dockstat._unpack(
                    b64_pkg,
                    real_pkg,
                    True,
                    False,
                    bs=b64_blocksize
                )

                # close and reopen as read
                real_pkg.close()
                real_pkg = open(real_path, "rb")

                # check pkg slip
                real_chksum = dockstat.createPackageSlip(
                    real_pkg,
                    bs=blocksize
                )

            except Exception as e:
                mas_utils.writelog(
                    "[ERROR] failed to decode '{0}' | {1}\n".format(
                        b64_name,
                        str(e)
                    )
                )
                return False

            finally:
                # always close the base64 package
                b64_pkg.close()

                if real_pkg is not None:
                    real_pkg.close()

            # now to check this image for chksum correctness
            if real_chksum is None:
                # bad shit happened here somehow
                mas_utils.trydel(real_path)
                return False

            if real_chksum != chksum:
                # decoded was wrong somehow
                mas_utils.trydel(real_path)
                return False

        # otherwise success somehow
        return True


    def removeImages(dockstat, image_dict, selective=[], log=False):
        """
        Removes the decoded images at the end of their lifecycle

        IN:
            dockstat - docking station
            image_dict - image map to use
            selective - list of image keys to delete
                If not passed in, we delete everything in the image dict
                (Default: [])
            log - should we log a delete failure?
                (Default: False)

        AKA quitting
        """
        if len(selective) == 0:
            selective = image_dict.keys()

        for b64_name in selective:
            real_name, chksum = image_dict[b64_name]
            mas_utils.trydel(dockstat._trackPackage(real_name), log=log)


init python in mas_dockstat:
    import store
    import cPickle

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
    import store.mas_sprites as mas_sprites
    import store.mas_greetings as mas_greetings
    import store.mas_ics as mas_ics
    import store.evhand as evhand
    from cStringIO import StringIO as fastIO
    import codecs
    import re
    import os
    import random
    import datetime

    cr_log_path = "log/mfgen"
    rd_log_path = "log/mfread"

    # we set these during init phase if we found a monika
    retmoni_status = None
    retmoni_data = None


    def _buildMetaDataList(_outbuffer):
        """
        Writes out a pipe-delimeted metadata list to the given buffer

        OUT:
            _outbuffer - buffer to write metadata to
        """
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
        _outbuffer.write("|".join([
            first_sesh,
            store.persistent.playername,
            store.persistent._mas_monika_nickname,
            affection_val,
            store.monika_chr.hair,
            store.monika_chr.clothes
        ]) + END_DELIM)


    def _buildMetaDataPer(_outbuffer, log):
        """
        Writes out the persistent's data into the given buffer

        Exceptions are logged

        OUT:
            _outbuffer - buffer to write persistent data to
            log - log to write messages to, if needed

        RETURNS:
            True on success, False if failed
        """
        ### metadata elements
        END_DELIM = "|||per|"

        try:
            _outbuffer.write(codecs.encode(cPickle.dumps(store.persistent), "base64"))
            _outbuffer.write(END_DELIM)
            return True

        except Exception as e:
            log.write(
                "[ERROR]: failed to pickle data: {0}\n".format(repr(e))
            )
            return False


    def checkMonika(status, moni_data):
        """
        Parses if a given set of monika data is a rogue monika, our monika,
        and so on, and does checkins and more for the appropriate case.

        IN:
            status - findMonika's return status
            moni_data - findMonika's return data

        RETURNS:
            TBD
        """
        # TODO
        return


    def checkinMonika():
        """
        Adds entry to checkin log that monika has returned to the spaceroom.
        Also clears the global checksum var.
        """
        mas_utils.log_entry(
            store.persistent._mas_dockstat_checkin_log,
            store.persistent._mas_moni_chksum
        )
        store.persistent._mas_moni_chksum = None


    def checkoutMonika(chksum):
        """
        Adds entry to checkout log that monika has left the spaceroom.
        Also sets the chk to the global checksum var.
        Also removes monikas that had the same checksum

        IN:
            chksum - monika's checksum when checking her out.
        """
        # sanity checks
        if chksum is None or chksum == -1 or len(chksum) == 0:
            return

        mas_utils.log_entry(
            store.persistent._mas_dockstat_checkout_log,
            chksum
        )
        store.persistent._mas_moni_chksum = chksum

        if chksum in store.persistent._mas_dockstat_moni_log:
            store.persistent._mas_dockstat_moni_log.pop(chksum)


    def triageMonika(from_empty):
        """
        Jumps to an appropriate label based on retmoni_status and retmoni_data.
        If retmoni_status is None, we dont do anything.

        IN:
            from_empty - True if we should assume from empty desk, False
                otherwise.
        """
        if retmoni_status is None:
            return

        # otherwise, parse the status
        if (retmoni_status & MAS_PKG_FO) > 0:
            # TODO: jump to mas_dockstat_different_monika label
            label_jump = "mas_dockstat_empty_desk"

        elif (retmoni_status & MAS_PKG_F) > 0:
            # found monika
            label_jump = "mas_dockstat_found_monika"

        else:
            # none of the above
            label_jump = "mas_dockstat_empty_desk"

        if from_empty:
            label_jump += "_from_empty"

        renpy.jump(label_jump)


    def packageCheck(
            dockstat,
            pkg_name,
            pkg_slip,
            on_succ,
            on_fail,
            sign=True
        ):
        """
        Checks for existence of a package that matches the pkg name and slip.

        This acts as a wrapper around the signForPackage that can encapsulate
        return values with different values.

        Success is when signForPackage returns 1. All other values are
        considered failures.

        NOTE: if sign is False, then we use createPackageSlip + getPackage
        instead. use this if you don't want to delete the package once you
        have checked them in.

        IN:
            dockstat - docking station to check packag ein
            pkg_name - name of the package to check
            pkg_slip - checksum of this package
            on_succ - value to return on successful package check
            on_fail - value to return on failed package check
            sign - True to use signForPackage (aka delete after checking),
                False uses getPackage + createPackageSlip (aka no delete after
                checking)
                (Default: True)
        """
        if sign:
            if dockstat.signForPackage(pkg_name, pkg_slip, bs=b64_blocksize) == 1:
                return on_succ

        else:
            # use getPackage and createPackageSlip
            package = dockstat.getPackage(pkg_name)
            if package is None:
                return on_fail

            try:
                read_slip = dockstat.createPackageSlip(package, b64_blocksize)

                if read_slip == pkg_slip:
                    return on_succ

            except Exception as e:
                mas_utils.writelog(
                    "[WARN]: package slip fail? {0} | {1}\n".format(
                        pkg_name,
                        repr(e)
                    )
                )

            finally:
                if package is not None:
                    package.close()

        return on_fail

    def generateMonika(dockstat, logpath):
        """
        Generates / writes a monika blob file.

        NOTE: This does both generation and integretiy checking
        NOTE: exceptions are logged

        IN:
            dockstat - the docking station to generate Monika in
            logpath - path of log to write messagse to

        RETURNS:
            checksum of monika
            -1 if checksums didnt match (and we cant verify data integrity of
                the generated moinika file)
            None otherwise

        ASSUMES:
            blocksize - this is a constant in this store
        """
        cr_log = store.mas_utils.logcreate(logpath, flush=True)

        cr_log.write("\n\nCreating Monika in: {0}\n".format(dockstat.station))

        # sanity check regarding the filepath
        if "temp" in dockstat.station.lower():
            cr_log.write("[ERROR] temp directory found, aborting.\n")
            return False

        ### other stuff we need
        # inital buffer
        moni_buffer = fastIO()
        moni_buffer = codecs.getwriter("utf8")(moni_buffer)

        # number deliemter
        NUM_DELIM = "|num|"

        ### write metadata
        if not _buildMetaDataPer(moni_buffer, cr_log):
            # if we failed to do this via persistent, then we'll use the old
            # style instead
            _buildMetaDataList(moni_buffer)

        ### monikachr
        moni_chr = None
        try:
            moni_chr = open(os.path.normcase(
                renpy.config.basedir + "/game/mod_assets/monika/mbase"
            ), "rb")

            # NOTE: moin_chr is going to be less than 200KB, this be fine
            moni_buffer.write(moni_chr.read())

        except Exception as e:
            cr_log.write("[ERROR] mbase copy failed | {0}\n".format(
                repr(e)
            ))
            moni_buffer.close()
            return False

        finally:
            # always close moni_chr
            if moni_chr is not None:
                moni_chr.close()

        ### now we must do the streamlined write system to file
        moni_path = dockstat._trackPackage("monika")
        moni_fbuffer = None
        moni_tbuffer = None
        moni_sum = None
        try:

            # First, lets iterate over the data to figure out how many lines
            # we will need, as well as how large this thing will be
            moni_buffer_iter = store.MASDockingStation._blockiter(
                moni_buffer,
                blocksize
            )
            lines = 0
            last_line_size = 0
            for _line in moni_buffer_iter:
                lines += 1
                last_line_size = len(_line)

            # check if adding the line data would go over the line size
            line_str_size = len(str(lines) + NUM_DELIM)
            if (last_line_size + line_str_size) > blocksize:
                lines += 1

            # fill a new buffer with the number of lines and reset it for
            # blocksize iterating
            moni_buffer_iter = store.MASDockingStation._blockiter(
                moni_buffer,
                blocksize
            )
            moni_tbuffer = fastIO()
            moni_tbuffer = codecs.getwriter("utf8")(moni_tbuffer)
            moni_tbuffer.write(str(lines) + NUM_DELIM)
            for _line in moni_buffer_iter:
                moni_tbuffer.write(_line)
            moni_buffer.close()

            # now we can prepare to write
            moni_fbuffer = codecs.open(moni_path, "wb", "utf-8")

            # now open up the checklist and encoders
            checklist = dockstat.hashlib.sha256()
            def safe_encoder(data):
                return dockstat.base64.b64encode(dockstat.safeRandom(data))
            encoder = dockstat.base64.b64encode

            # now write this buffer out, keeping track of the last buffer
            # size
            moni_tbuffer.seek(0)
            _line = moni_tbuffer.read(blocksize)
            total_buffer_size = 0
            while len(_line) == blocksize:
                total_buffer_size += blocksize
                data = encoder(_line)
                checklist.update(data)
                moni_fbuffer.write(data)
                _line = moni_tbuffer.read(blocksize)
            moni_tbuffer.close()

            # when we reach here, we either have no more lines or leftovers
            last_buffer_size = len(_line)
            total_buffer_size += last_buffer_size

            # calculate extra padding for last line and the remaining buffer
            # size we need to write out
            moni_size_left = (
                store.persistent._mas_dockstat_moni_size
                - total_buffer_size
            )
            if moni_size_left > 0:
                # we should do some padding and additional data writes

                # what padding do we even have
                if (moni_size_left + last_buffer_size) <= blocksize:
                    extra_padding = moni_size_left
                    moni_size_left = 0
                else:
                    extra_padding = blocksize - last_buffer_size
                    moni_size_left -= extra_padding

                # and write out the metadata / monika
                data = encoder(_line + dockstat.safeRandom(extra_padding))
                checklist.update(data)
                moni_fbuffer.write(data)

                # and now for the random data generation
                # NOTE: this should represent number of bytes
                moni_size_limit = moni_size_left - blocksize
                curr_size = 0

                while curr_size < moni_size_limit:
                    data = safe_encoder(blocksize)
                    checklist.update(data)
                    moni_fbuffer.write(data)
                    curr_size += blocksize

                # we should have some leftovers
                leftovers = moni_size_left - curr_size
                if leftovers > 0:
                    data = safe_encoder(leftovers)
                    checklist.update(data)
                    moni_fbuffer.write(data)

            else:
                # otherwise, we shoudl just write out the last line and
                # be done with it
                data = encoder(_line)
                checklist.update(data)
                moni_fbuffer.write(data)

            # great! lets go ahead and save the digest
            moni_sum = checklist.hexdigest()

        except Exception as e:
            cr_log.write("[ERROR] monibuffer write failed | {0}\n".format(
                repr(e)
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

            return False

        finally:
            # always close the fbuffer
            if moni_fbuffer is not None:
                moni_fbuffer.close()

            # always close the temp buffer
            if moni_tbuffer is not None:
                moni_tbuffer.close()

            # we dont need this buffer after here
            moni_buffer.close()

        ### Now to verify that we output the file correctly
        moni_pkg = dockstat.getPackage("monika")
        if moni_pkg is None:
            # ALERT ALERT HOW DID WE FAIL
            cr_log.write("[ERROR] monika not found.\n")
            mas_utils.trydel(moni_path)
            return False

        # we should have a file descriptor, lets attempt a pkg slip
        moni_slip = dockstat.createPackageSlip(moni_pkg, blocksize)
        if moni_slip is None:
            # ALERT ALERT WE FAILED AGAIN
            cr_log.write("[ERROR] monika could not be validated.\n")
            mas_utils.trydel(moni_path)
            return False

        if moni_slip != moni_sum:
            # WOW SRS THIS IS BAD
            cr_log.write(
                "[ERROR] monisums didn't match, did we have write failure?\n"
            )
            mas_utils.trydel(moni_path)
            return -1

        # otherwise, we managed to create a monika! Congrats!
        cr_log.write("chk: {0}\n".format(moni_sum))
        return moni_sum


    def init_findMonika(dockstat):
        """
        findMonika variation that is meant to be run at init time.

        IN:
            dockstat - MASDockingStation to use
        """
        global retmoni_status, retmoni_data

        # try to find this monika
        retmoni_status, retmoni_data = findMonika(dockstat, rd_log_path, True)


    def findMonika(dockstat, logpath, at_init):
        """
        Attempts to find monika in the giving docking station

        IN:
            dockstat - MASDockingStation to use
            logpath - path of log to write messages to
            at_init - True if we are in init, False if not

        RETURNS: tuple of the following format:
            [0]: MAS_PKG_* constants depending on the state of monika
            [1]: either list of data or persistent object of data. Will be
                None if no data or errors occured
        """
        rd_log = store.mas_utils.logcreate(
            logpath,
            append=not at_init,
            flush=True
        )

        rd_log.write("\n\nFinding Monika in: {0}\n".format(dockstat.station))

        END_DELIM = "|||"
        PER_DELIM = "per|"
        ret_code = 0

        status, first_line = dockstat.smartUnpack(
            "monika",
            store.persistent._mas_moni_chksum,
            lines=-1,
            bs=b64_blocksize,
            log=rd_log
        )

        if (status & (dockstat.PKG_E | dockstat.PKG_N)) > 0:
            # we had an error in reading, therefore we cant trust the data.
            # OR, we didnt find the package.
            # in either case, just say we didnt find monika
            return (MAS_PKG_NF, None)

        # otherwise, we certainly found monika
        # lets parse monika's data

        # reset this buffer
        first_line.seek(0)

        # we only want the data portion that's likely to contain our stuff
        # TODO: we do NOT have a system in place to handle persistents above
        #   4 MB. we need to consider this when we do long term
        real_data = first_line.read()
        first_line.close()

        # because the console may have shit, we should just attempt to parse
        # the data as persistent first, and then as a backup, try non-persist.
        per_data = parseMoniDataPer(real_data, rd_log)

        if per_data is None:
            # this isn't a persistent. Let's try backup strats

            # and see if this does contain our stuff
            real_data, sep, garbage = real_data.partition(END_DELIM)

            # and return results
            if len(sep) == 0:
                # no data found, assume a missing monika
                return (MAS_PKG_NF, None)

            real_data = parseMoniData(real_data, rd_log)
            ret_code = MAS_PKG_DL

        else:
            real_data = per_data
            ret_code = MAS_PKG_DP

        if real_data is None:
            # we failed to parse data. Please return an error
            # in this case, we should assume monika was not found
            return (MAS_PKG_NF, real_data)

        if (status & dockstat.PKG_C) > 0:
            # we found a different monika (or corrupted monika)
            rd_log.write(
                "[!] I found a corrupt monika! {0}\n".format(status)
            )
            return (ret_code | MAS_PKG_FO, real_data)

        # otherwise, we have a matching monika!
        return (ret_code | MAS_PKG_F, real_data)


    def parseMoniData(data_line, log):
        """
        Parses monika data into its components

        NOTE: all exceptions are logged

        IN:
            data_line - PIPE delimeted data line
            log - log to write messages to, if needed

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
            log.write("[ERROR]: Moni Data parse fail: {0}\n".format(
                repr(e)
            ))
            return None


    def parseMoniDataPer(data_line, log):
        """
        Parses persitent data into a persitent object.

        NOTE: all exceptions are loggeed

        IN:
            data_line - the data portion that may contain a persitent
            log - log to write messages to, if needed

        RETURNS: a persistent object, or None if failure
        """
        try:
            #pers = re.match(r"^(.*?)\|\|\|per\|",str(data_line)).group()
            # TODO: change separator to a very large delimeter so we can handle persistents larger than 4MB
            splitted = data_line.split("|||per|")
            if(len(splitted)>0):
                return cPickle.loads(codecs.decode(splitted[0] + b'='*4, "base64"))
            return cPickle.loads(codecs.decode(data_line + b'='*4, "base64"))

        except Exception as e:
            log.write(
                "[ERROR]: persistent unpickle failed: {0}\n".format(repr(e))
            )
            return None


    def selectReturnHomeGreeting(gre_type=None):
        """
        Selects the correct Return Home greeting.

        If None was selected, we return the default returned home gre

        We also default type to TYPE_GENERIC_RET if no type is given

        IN:
            gre_type - greeting type to find
                If None, we use TYPE_GENERIC_RET
                (Default: None)

        RETURNS:
            Event object representing the selected greeting
        """
        if gre_type is None:
            gre_type = mas_greetings.TYPE_GENERIC_RET

        sel_gre_ev = mas_greetings.selectGreeting(gre_type)

        if sel_gre_ev is None:
            # no selection? return the generic random
            return store.mas_getEV("greeting_returned_home")

        # otherwise, return this ev
        return sel_gre_ev


    def getCheckTimes(chksum=None):
        """
        Gets the corresponding checkin/out times for the given chksum.

        IN:
            chksum - chksum to retrieve checkin/checkout times.
                If None, then we simply get the latest checkin/checkout,
                regardless if they match or not.
                (Default: None)

        RETURNS tuple of the following format:
            [0] - checkout time
            [1] - checkin time
        If any param is None, then we couldn't find the matching chksum or
        there were no entries
        """
        checkin_log = store.persistent._mas_dockstat_checkin_log
        checkout_log = store.persistent._mas_dockstat_checkout_log
        checkin_time = None
        checkout_time = None
        checkin_len = len(checkin_log)
        checkout_len = len(checkout_log)

        # quick function to find a time based on checksum
        def find_time(check_log, check_sum):
            for _time, _chksum in check_log:
                if _chksum == check_sum:
                    return _time

            return None

        if checkin_len > 0:
            if chksum is None:
                checkin_time = checkin_log[checkin_len-1][0]

            else:
                checkin_time = find_time(checkin_log, chksum)

        if checkout_len > 0:
            if chksum is None:
                checkout_time = checkout_log[checkout_len-1][0]

            else:
                checkout_time = find_time(checkout_log, chksum)

        return (checkout_time, checkin_time)


    def diffCheckTimes(index=None):
        """
        Returns the difference between the latest checkout and check in times
        We do checkin - checkout.

        IN:
            index - the index of checkout/checkin to use when diffing
                If None, we use the latest one
                (Default: None)

        RETURNS: timedelta of the difference between checkin and checkout
        """
        checkin_log = store.persistent._mas_dockstat_checkin_log
        checkout_log = store.persistent._mas_dockstat_checkout_log
        checkin_len = len(checkin_log)
        checkout_len = len(checkout_log)

        if checkin_len == 0 or checkout_len == 0:
            return datetime.timedelta(0)

        if checkin_len != checkout_len:
            # mis match logs, please log this.
            mas_utils.writelog(
                (
                    "[WARNING]: checkin is {0}, checkout is {1}. "
                    "Going to pop.\n"
                ).format(checkin_len, checkout_len)
            )

            # and we will pop extras as well
            if checkin_len > checkout_len:
                larger_log = checkin_log
                goal_size = checkout_len

            else:
                larger_log = checkout_log
                goal_size = checkin_len

            while len(larger_log) > goal_size:
                larger_log.pop()

        if index is None or index >= len(checkout_log):
            index = len(checkout_log)-1

        return checkin_log[index][0] - checkout_log[index][0]


    def timeOut(_date):
        """
        Given a date, return how long monika has been out

        We assume that checkout logs are the source of truth

        IN:
            _date - date to check
        """
        checkout_log = store.persistent._mas_dockstat_checkout_log

        if len(checkout_log) == 0:
            return datetime.timedelta(0)

        # we only want the checkout dates for today
        checkout_indexes = [
            index
            for index in range(0, len(checkout_log))
            if checkout_log[index][0].date() == _date
        ]

        if len(checkout_indexes) == 0:
            return datetime.timedelta(0)

        # otherwise we have checkouts today, lets calculat time
        time_out = datetime.timedelta(0)

        for index in checkout_indexes:
            time_out += diffCheckTimes(index)

        return time_out


    def _ds_aff_for_tout(
            _time_out,
            max_hour_out,
            max_aff_gain,
            min_aff_gain,
            aff_mult=1
            ):
        """
        Grants an amount of affection based on time out. This is designed for
        use ONLY with the returned home greeting.

        NOTE: this also sets the monika_returned_home persistent

        IN:
            _time_out - timedelta we want to treat as monika being out
            max_hour_out - how many hours is considered max
                (anthing OVER this will be maxxed)
            max_aff_gain - amount of aff to be gained when max+
            min_aff_gain - smallest amount of aff gain
            aff_mult - multipler to hours to use as aff gain when between min
                and max
                (Default: 1)
        """
        if store.persistent._mas_monika_returned_home is None:
            hours_out = int(_time_out.total_seconds() / 3600)

            # you gain 1 per hour, max 5, min 1
            if hours_out > max_hour_out:
                aff_gain = max_aff_gain
            elif hours_out == 0:
                aff_gain = min_aff_gain
            else:
                aff_gain = hours_out * aff_mult

            store.mas_gainAffection(aff_gain, bypass=True)
            store.persistent._mas_monika_returned_home = (
                datetime.datetime.now()
            )


init 205 python in mas_dockstat:
    import store.mas_threading as mas_threading
    # thread classes for monika files

    # runs monika file generation
    monikagen_promise = mas_threading.MASAsyncWrapper(
        generateMonika,
        [store.mas_docking_station, cr_log_path]
    )

    # runs monika file check
    monikafind_promise = mas_threading.MASAsyncWrapper(
        findMonika,
        [store.mas_docking_station, rd_log_path, False]
    )

    # other important vars for this

    abort_gen_promise = False
    # if True, we aborted monika generation, but since its an async call,
    # ch30_loop needs to handle this

    def abortGenPromise():
        """
        Attempts to about the monikagen promise and properly delete the
        monika package.
        """
        global abort_gen_promise

        if not abort_gen_promise:
            return

        # otherwise we need to abourt this.
        if not monikagen_promise.done():
            return

        # promise is done! lets abort
        monikagen_promise.end()
        store.mas_docking_station.destroyPackage("monika")
        abort_gen_promise = False


### Docking station labels regarding monika leaving the station

# call this label when monika is ready to leave the station
# RETURNS:
#   true if moni can leave
#   false otherwise
label mas_dockstat_ready_to_go(moni_chksum):
    # generate the monika file
#    $ moni_chksum = store.mas_dockstat.generateMonika(mas_docking_station)
    $ can_moni_leave = moni_chksum and moni_chksum != -1

    if can_moni_leave:
        # file successfully made
        # monika can leave

        #We'll do our actual getting ready here since this saves us needing to do it multiple times later
        python:
            #If we should take drink with, we do that now
            mas_useThermos()

            #NOTE: Do clothes changes here once we want to have Monika change as she's getting ready
            renpy.pause(1.0, hard=True)

        #If bday + aff+, we use this fare
        if (
            mas_isMoniAff(higher=True) and mas_isMonikaBirthday()
            and not persistent._mas_bday_has_done_bd_outro
        ):
            if len(persistent._mas_dockstat_checkout_log) == 0:
                #We change Moni's outfit here because she just got ready
                $ monika_chr.change_clothes(mas_clothes_blackdress)
                call mas_dockstat_first_time_goers
            call mas_bday_bd_outro

        elif len(persistent._mas_dockstat_checkout_log) == 0:
            call mas_dockstat_first_time_goers

        else:
            m "Alright."

        # setup check and log this file checkout
        $ store.mas_dockstat.checkoutMonika(moni_chksum)
        # NOTE: callers must handle dialogue for this

    else:
        #Let's handle potential date var issues
        call mas_dockstat_decrement_date_counts
        # we failed to generate file somehow
        # NOTE: callers must handle the dialogue for this

    return can_moni_leave


label mas_dockstat_first_time_goers:
    call mas_transition_from_emptydesk("monika 3eua")
    m 3eua "I'm now in the file 'monika' in your characters folder."
    m "After I shut down the game, you can move me wherever you like."
    m 3eub "But make sure to bring me back to the characters folder before turning the game on again, okay?"
    m 1eua "And lastly..."
    m 1ekc "Please be careful with me. It's so easy to delete files after all..."
    m 1eua "Anyway..."
    return

label mas_dockstat_abort_post_show:
    #Call this label to re-set anything needed when aborting dockstat farewells (error or by user)
    #After Monika has returned to her desk
    python:
        #Restore the drink and make sure it's kept on desk again
        _curr_drink = MASConsumable._getCurrentDrink()
        if _curr_drink and _curr_drink.portable:
            _curr_drink.acs.keep_on_desk = True

    return

label mas_dockstat_abort_gen:
    # call this label to abort monika gen promise
    # we should abort the promise (this lets spaceroom idle abort, as well)
    python:
        store.mas_dockstat.abort_gen_promise = True

        #Attempt to abort the promise
        store.mas_dockstat.abortGenPromise()

    #FALL THROUGH

#Call this label to reset the date vars
label mas_dockstat_decrement_date_counts:
    python:
        #We are not leaving
        persistent._mas_dockstat_going_to_leave = False

        # we are not leaving and need to reset these
        if persistent._mas_player_bday_left_on_bday:
            persistent._mas_player_bday_left_on_bday = False
            persistent._mas_player_bday_date -= 1

        if persistent._mas_f14_on_date:
            persistent._mas_f14_on_date = False
            persistent._mas_f14_date_count -= 1

        if persistent._mas_bday_on_date:
            persistent._mas_bday_on_date = False
            persistent._mas_bday_date_count -= 1
    return


# empty desk. This one includes file checking every 1 second
label mas_dockstat_empty_desk:
    python:
        #Make sure O31 effects show
        if persistent._mas_o31_in_o31_mode:
            mas_globals.show_vignette = True
            #If weather isn't thunder, we need to make it so (done so we don't have needless sets)
            if mas_current_weather != mas_weather_thunder:
                mas_changeWeather(mas_weather_thunder, True)

        else:
            #Now setup weather
            mas_startupWeather()
            skip_setting_weather = True

        mas_from_empty = True

        checkout_time = store.mas_dockstat.getCheckTimes()[0]

        if mas_isD25Season() and persistent._mas_d25_deco_active:
            store.mas_d25ShowVisuals()

        #NOTE: Player bday and Moni bday do a zoom reset so deco is shown properly
        if mas_confirmedParty() and mas_isMonikaBirthday():
            persistent._mas_bday_visuals = True
            store.mas_sprites.reset_zoom()
            store.mas_surpriseBdayShowVisuals(cake=not persistent._mas_bday_sbp_reacted)

        #NOTE: elif'd so we don't try and show two types of visuals here
        elif persistent._mas_player_bday_decor:
            store.mas_sprites.reset_zoom()
            store.mas_surpriseBdayShowVisuals()

    call spaceroom(hide_monika=True, scene_change=True)

    #FALL THROUGH

label mas_dockstat_empty_desk_preloop:
    python:
        import store.mas_dockstat as mas_dockstat

        #Setup ui hiding
        mas_OVLHide()
        mas_calRaiseOverlayShield()
        mas_calShowOverlay()
        disable_esc()
        mas_enable_quit()
        promise = mas_dockstat.monikafind_promise

label mas_dockstat_empty_desk_from_empty:

    python:
        #Begin the find thread
        if promise.ready:
            promise.start()

        #wait 1 seconds before checking again
        renpy.pause(1.0, hard=True)

        #Check for surprise visuals
        if mas_confirmedParty() and mas_isMonikaBirthday():
            persistent._mas_bday_visuals = True
            store.mas_surpriseBdayShowVisuals(cake=not persistent._mas_bday_sbp_reacted)

        #Check for monika
        if promise.done():
            # we have a result! lets get and then check if we found anything.
            _status, _data_line = promise.get()
            mas_dockstat.retmoni_status = _status
            mas_dockstat.retmoni_data = _data_line
            mas_dockstat.triageMonika(True)

    # otherwise we still havent' found monika, so lets just continue
    # the loop
    jump mas_dockstat_empty_desk_from_empty

define mas_dockstat.different_moni_flow = False

# different monika found
label mas_dockstat_different_monika:
    # ASSUMES:
    # mas_dockstat.retmoni_data - should be the data portion of monika

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
    $ moni_data = mas_dockstat.parseMoniData(mas_dockstat.retmoni_data)

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
    $ monika_chr.change_outfit(moni_clothes, moni_hair, False)

    # and then we can begin talking
    call mas_transition_from_emptydesk("monika 1ekd")

    m "[player]?"

    m "Wait, you're not [player]."

    # TODO: more dialogue

    $ mas_dockstat.retmoni_data = None
    $ startup_check = False

    jump ch30_post_exp_check


# found our monika, but we coming from empty desk
label mas_dockstat_found_monika_from_empty:
    if checkout_time is not None and checkout_time.date() == persistent._date_last_given_roses:
        $ monika_chr.wear_acs(mas_acs_roses)

    # dont want users using our promises
    $ promise = None

    # FALL THROUGH

# found our monika
label mas_dockstat_found_monika:
    $ store.mas_dockstat.retmoni_status = None
    $ store.mas_dockstat.retmoni_data = None
    $ store.mas_dockstat.checkinMonika()
    $ persistent._mas_pm_taken_monika_out = True
    $ checkout_time = store.mas_dockstat.getCheckTimes()[0]

    if checkout_time is not None and checkout_time.date() == persistent._date_last_given_roses:
        $ monika_chr.wear_acs(mas_acs_roses)
    # select the greeting we want
    python:
        selected_greeting = store.mas_dockstat.selectReturnHomeGreeting(
            persistent._mas_greeting_type
        ).eventlabel

        # TODO: consider running the greeting setup label?

        # reset greeting type
        persistent._mas_greeting_type = None

        # removee the monika
        mas_docking_station.destroyPackage("monika")

        # reenabel a bunch of things
        mas_OVLShow()
        mas_disable_quit()
        enable_esc()
        startup_check = False

    if persistent._mas_o31_in_o31_mode:
        $ store.mas_globals.show_vignette = True
        #Force progressive to disabled for o31
        $ mas_changeWeather(mas_weather_thunder, True)

    elif mas_run_d25s_exit and not mas_lastSeenInYear("mas_d25_monika_d25_mode_exit"):
        call mas_d25_season_exit

    elif mas_isD25Season() and persistent._mas_d25_deco_active:
        $ store.mas_d25ShowVisuals()

    jump ch30_post_exp_check

#START: GENERALIZED MONIKA IO LABELS

#IOSTART LABEL
#Use this to begin monika file generation
#REQUIRES THE FOLLOWING GLOBAL VARIABLE TO BE SET TO ALLOW CUSTOM FLOWS
# - mas_farewells.dockstat_iowait_label
#   If not set, the generic iowait label is assumed
label mas_dockstat_iostart:
    show monika 2dsc
    python:
        persistent._mas_dockstat_going_to_leave = True
        first_pass = True

        # launch I/O thread
        promise = store.mas_dockstat.monikagen_promise
        promise.start()

    #Jump to the iowait label
    if renpy.has_label(mas_farewells.dockstat_iowait_label):
        jump expression mas_farewells.dockstat_iowait_label
    #If the one passed in wasn't valid, then we'll use the generic iowait
    jump mas_dockstat_generic_iowait


#GENERIC IOWAIT LABEL
##NOTE: REQUIRES THE FOLLOWING GLOBAL VARIABLES FOR CUSTOM FLOWS
# - mas_farewells.dockstat_rtg_label
# - mas_farewells.dockstat_cancel_dlg_label
# - mas_farewells.dockstat_wait_menu_label
#NOTE: If any of these are None (as they default), generic labels are assumed
label mas_dockstat_generic_iowait:
    hide screen mas_background_timed_jump

    # we want to display the menu first to give users a chance to quit
    if first_pass:
        $ first_pass = False
        m 1eua "Give me a second to get ready.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

        #Prepare the current drink to be removed if needed
        python:
            current_drink = MASConsumable._getCurrentDrink()
            if current_drink and current_drink.portable:
                current_drink.acs.keep_on_desk = False

        #Get Moni off screen
        call mas_transition_to_emptydesk

    elif promise.done():
        # i/o thread is done!
        #We're ready to go. Let's jump to the rtg label
        if renpy.has_label(mas_farewells.dockstat_rtg_label):
            jump expression mas_farewells.dockstat_rtg_label
        #Otherwise, we don't have a valid label and need to jump to a generic ready to go
        jump mas_dockstat_generic_rtg

    # display menu options
    # 4 seconds seems decent enough for waiting.
    show screen mas_background_timed_jump(4, "mas_dockstat_generic_iowait")
    menu:
        "Hold on a second!":
            hide screen mas_background_timed_jump
            $ persistent._mas_dockstat_cm_wait_count += 1

    # fall thru to the wait wait flow
    if renpy.has_label(mas_farewells.dockstat_wait_menu_label):
        call expression mas_farewells.dockstat_wait_menu_label
    else:
        #Otherwise fallback to this label
        call mas_dockstat_generic_wait_label

    #If we returned True, that means we cancelled
    if _return:
        #We need to clear all the vars in case we go dockstat again
        $ mas_farewells.resetDockstatFlowVars()

        #And now, we return what the generic label would have returned, that is if it's a string.
        if isinstance(_return, basestring):
            return _return
        #This means we got a boolean and we can't return it because the event handler requires strings
        return

    # by default, continue looping
    jump mas_dockstat_generic_iowait


#GENERIC WAIT LABEL
label mas_dockstat_generic_wait_label:
    menu:
        m "What is it?"
        "Actually, I can't take you right now.":
            call mas_dockstat_abort_gen

            #Show Monika again
            call mas_transition_from_emptydesk("monika 1ekc")
            call mas_dockstat_abort_post_show

            if renpy.has_label(mas_farewells.dockstat_cancel_dlg_label):
                jump expression mas_farewells.dockstat_cancel_dlg_label

            #Fallback to generic cancel
            jump mas_dockstat_generic_cancel

        "Nothing.":
            # if we get here, we should jump back to the top so we can
            # continue waiting
            m 2hub "Oh, good! Let me finish getting ready."
            return


#GENERIC RTG LABEL
#FOR CUSTOM FLOWS, REQUIRES THE FOLLOWING GLOBAL VARIABLE:
# - mas_farewells.dockstat_failed_io_still_going_ask_label
#If not set, the generic label will be used
label mas_dockstat_generic_rtg:
    # io thread should be done by now
    $ moni_chksum = promise.get()
    $ promise = None # clear promise so we dont have any issues elsewhere
    call mas_dockstat_ready_to_go(moni_chksum)
    if _return:
        python:
            persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
                store.mas_greetings.TYPE_GENERIC_RET
            )

        call mas_transition_from_emptydesk("monika 1eua")

        #Otherwise we just use the normal outro
        m 1eua "I'm ready to go."
        return "quit"
    call mas_transition_from_emptydesk("monika 1ekc")
    call mas_dockstat_abort_post_show
    # otherwise, we failed, so monika should tell player
    m 1ekc "Oh no..."
    m 1lksdlb "I wasn't able to turn myself into a file."
    m "I think you'll have to go on without me this time."
    m 1ekc "Sorry, [player]."

    if renpy.has_label(mas_farewells.dockstat_failed_io_still_going_ask_label):
        # NOTE: we assume that this label will reset the docstat vars
        jump expression mas_farewells.dockstat_failed_io_still_going_ask_label
    #Use generic to fallback
    jump mas_dockstat_generic_failed_io_still_going_ask


#GENERIC DOCKSTAT CANCEL LABEL
#Used when the player tells Monika they can't take her out
#REQUIRES THE FOLLOWING GLOBAL VARIABLE TO BE ASSIGNED IF YOU WANT CUSTOM FLOWS:
# - mas_farewells.dockstat_cancelled_still_going_ask_label
label mas_dockstat_generic_cancel:
    if mas_isMoniDis(lower=True):
        m 1tkc "..."
        m 1tkd "I knew it.{nw}"
        $ _history_list.pop()
        m 1lksdld "That's okay, I guess."

    elif mas_isMoniHappy(lower=True):
        m 1ekd "Oh,{w=0.3} all right. Maybe next time?"

    else:
        # otherwise affection and higher:
        m 2ekp "Aw..."
        m 1hub "Fine, but you better take me next time!"

    if renpy.has_label(mas_farewells.dockstat_cancelled_still_going_ask_label):
        jump expression mas_farewells.dockstat_cancelled_still_going_ask_label
    #Otherwise we use the generic still going ask as a fallback
    jump mas_dockstat_generic_cancelled_still_going_ask

#GENERIC CANCELLED STILL GOING ASK
#Used when we cancel dockstat, this is where Monika asks you if you're still going
label mas_dockstat_generic_cancelled_still_going_ask:
    m 1euc "Are you still going to go?{nw}"
    $ _history_list.pop()
    menu:
        m "Are you still going to go?{fast}"
        "Yes.":
            if mas_isMoniNormal(higher=True):
                m 2eka "All right. I'll be right here waiting for you, as usual..."
                m 2hub "So hurry back! I love you, [player]!"

            else:
                # otherwise, upset and below
                m 2tfd "...Fine."

            return "quit"

        "No.":
            if mas_isMoniNormal(higher=True):
                m 2eka "...Thank you."
                m "It means a lot that you're going to spend more time with me since I can't come along."
                m 3ekb "Please just go about your day whenever you need to, though. I wouldn't want to make you late!"

            else:
                # otherwise, upset and below
                m 2lud "All right, then..."
            return True

#GENERIC FAILED IO STILL GOING ASK
#Used when Monika fails to turn herself into a file. This is where Monika asks you if you're still going
label mas_dockstat_generic_failed_io_still_going_ask:
    #We need to clear all the vars in case we go dockstat again
    $ mas_farewells.resetDockstatFlowVars()
    m "Are you still going to go?{nw}"
    $ _history_list.pop()
    menu:
        m "Are you still going to go?{fast}"
        "Yes.":
            m 2eka "I understand. You have things to do, after all..."
            m 2hub "Be safe out there! I'll be right here waiting for you!"
            return "quit"

        "No.":
            m 2wub "Really? Are you sure? Even though it's my own fault I can't go with you..."
            m 1eka "...Thank you, [player]. That means more to me than you could possibly understand."
            $ mas_gainAffection()
            return
