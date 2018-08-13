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

init -45 python:

    class MASDockingStation(object):
        """
        Docking station class designed to help with file reading / writing of
        certain files.
        """
        import os
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
        ERR = "[ERROR] {0} | {1} | {2}"
        ERR_GET = "Failure getting package '{0}'."
        ERR_OPEN = "Failure opening package '{0}'."
        ERR_SIGN = "Failure to request signature for package '{0}'."


        def __init__(self, station=MASDockingStation.DEF_STATION_PATH):
            """
            Constructor

            IN:
                station - the path to the folder this docking station interacts
                    with. (absolute path) 
                    NOTE: END WITH '/' please
                    (Default: DEF_STATION_PATH)
            """
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


        def createPackageSlip(self, package):
            """
            Generates a checksum for a package (which is a file descriptor)

            NOTE: may throw exceptions

            NOTE: when checking packages, we read by B64_READ_SIZE always

            IN:
                package - file descriptor of the package we want
                    NOTE: is seek(0)'d after reading

            RETURNS:
                sha256 checksum (hexadec) of the given package, or empty string
                if error occured
            """
            _package = MASDockingStation._blockiter(
                package, self.B64_READ_SIZE
            )

            pkg_slip = self._unpack(_package, None, False, True)

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
            if not self.checkForPackage(package_name)

            ### open the package
            package_path = self._trackPackage(package_name)
            try:
                package = open(package_path, "rb")

            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_OPEN.format(package_name),
                    str(self),
                    str(e)
                ))
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
            try:
                _contents = MASDockingStation._blockiter(
                    contents, self.READ_SIZE
                )
                box = self.fastIO()

                return (box, self._pack(_contents, box, True, pkg_slip))

            except Exception as e:
                # if an error occured, close the box buffer and raise
                box.close()
                raise e

            finally:
                # always close teh data buffer
                contents.close()


        def sendPackage(self, 
                package_name, 
                package, 
                unpacked=False, 
                req_sign=False
            ):
            """
            Sends a package into the docking station
            (Writes a file in this stations' folder)

            IN:
                package_name - name of the file to write
                package - the b64 encoded data to write as bytes
                unpacked - True means that package is actually data that hasnt
                    been encoded yet and should be encoded as we write it out
                    (Default: False)
                req_sign - True means we should generate a sha256 checksum for
                    the package and return that 
                    (Default: False)

            RETURNS:
                True if package was sent successfully
            """
            pass


        def signForPackage(self, 
                package_name,
                pkg_slip,
                keep_contents=False
                unpack=False
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
                unpack - if True, decodes that base64 in addition to copying
                    it
                    NOTE: only functions if keep_contents is True
                    (Default: False)

            RETURNS:
                if the package matches signature:
                    - if keep_contents and unpack is True:
                        StringIO buffer containing decoded data
                    - elif only keep_contents is True:
                        StringIO buffer containing base64 encoded data
                    - otherwise, True is returned
                None Otherwise (or if an error occured along the way
            """
            ### get the package
            package = self.getPackage(package_name)
            if package is None:
                return None

            ### 



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
            try:
                _package = MASDockingStation._blockiter(
                    package, self.B64_READ_SIZE
                )
                # NOTE: we use regular StringIO in case of unicode
                contents = self.slowIO()

                _pkg_slip = self._unpack(
                    _package,
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
                blocksize - size to use for blocks

            YIELDS:
                blocks until a block read attempt gave us nothing

            ASSUMES:
                given file descriptor is open
            """
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


        def _pack(self, contents, box, pack=True, pkg_slip=True):
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

            RETURNS:
                generated sha256 checksum if pkg_slip is True
                Otherwise, None
            """
            if not (pkg_slip or pack):
                return None

            _contents = MASDockingStation._blockiter(contents, self.READ_SIZE)

            if pkg_slip and pack:
                # encode the data, then checksum the base64, then write to 
                # output
                checklist = hashlib.sha256()

                for item in _contents
                    packed_item = base64.b64encode(item)
                    checklist.update(packed_item)
                    box.write(packed_item)

                return checklist.hexdigest()

            elif pack:
                # encode the data, write to output
                for item in _contents:
                    box.write(base64.b64encode(item))

            else:
                # checksum the data
                checklist = hashlib.sha256()

                for item in _contents:
                    checklist.update(base64.b64encode(item))

                return checklist.hexdigest()

            return None


        def _unpack(self, box, contents, unpack=True, pkg_slip=True):
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

            RETURNS:
                generated sha256 checksum if pkg_slip is True
                Otherwise, None
            """
            if not (pkg_slip or unpack):
                return None

            _box = MASDockingStation._blockiter(box, self.B64_READ_SIZE)

            if pkg_slip and unpack:
                # checksum data, decode it, write to output
                checklist = hashlib.sha256()

                for packed_item in _box:
                    checklist.update(packed_item)
                    contents.write(base64.b64decode(packed_item))

                return checklist.hexdigest()

            elif pkg_slip:
                # checksum data
                checklist = hashlib.sha256()

                for packed_item in _box:
                    checklist.update(packed_item)

                return checklist.hexdigest()

            else:
                # decode the data
                for packed_item in _box:
                    contents.write(base64.b64decode(packed_item))

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






