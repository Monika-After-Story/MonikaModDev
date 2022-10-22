
#NOTE: This is done during init because exceptions are suppressed in early, singleton needs to raise an exception
init -1500 python:
    import os
    import singleton
    me = singleton.SingleInstance()


init -1500 python in mas_utils:
    # ssl/https usage checks


    def can_use_https():
        """
        Checks if we can safely use https in general - this combines several
        checks, mainly:
            - ssl
            - a cert

        NOTE: https can still be used with sites that do not require SSL verify
        even if no cert is found.

        RETURNS: True if https can be used.
        """
        return (
            store.mas_can_import.ssl()
            and store.mas_can_import.certifi.cert_available
        )


python early in mas_logging:
    import datetime
    import logging
    import os
    import platform
    import store
    import re

    #Thanks python...
    from logging import handlers as loghandlers

    # log tags
    LT_INFO = "info"
    LT_WARN = "Warning! ;_;"
    LT_ERROR = "!ERROR! T_T"

    LT_MAP = {
        logging.INFO: LT_INFO,
        logging.WARN: LT_WARN,
        logging.ERROR: LT_ERROR,
    }

    #Consts
    DEF_FMT = "[%(asctime)s] [%(levelname)s]: %(message)s"
    DEF_DATEFMT = "%Y-%m-%d %H:%M:%S"

    #Map for filename : Logger
    LOG_MAP = dict()

    class MASLogFormatter(logging.Formatter):
        """
        log formatter all other mas logs should extend if they want
        custom functionality.

        Features:
            - uses our own log tags
            - defaults format with time and level name
        """
        NEWLINE_MATCHER = re.compile(r"(?<!\r)\n")
        LINE_TERMINATOR = "\r\n"

        def __init__(self, fmt=None, datefmt=None):
            if fmt is None:
                fmt = DEF_FMT
            if datefmt is None:
                datefmt = DEF_DATEFMT

            super(MASLogFormatter, self).__init__(fmt=fmt, datefmt=datefmt)

        def format(self, record):
            """
            Override of format - mainly replaces the levelname prop
            """
            self.update_levelname(record)
            return self.replace_lf(
                super(MASLogFormatter, self).format(record)
            )

        def update_levelname(self, record):
            """
            Updates the levelname of the record. Use in custom formatter
            functions.
            """
            record.levelname = LT_MAP.get(record.levelno, record.levelname)

        @classmethod
        def replace_lf(cls, msg):
            """
            Replaces all line feeds with carriage returns and a line feed
            """
            return re.sub(cls.NEWLINE_MATCHER, cls.LINE_TERMINATOR, msg)

    class MASNewlineLogFormatter(MASLogFormatter):
        """
        log formatter with newline prefix support.
        """

        def apply_newline_prefix(self, record, msg):
            """
            Applies newline to a msg if the record supports it.
            The newline is prefixed to the start of the message.

            IN:
                record - LogRecord to generate format for
                msg - the currently formatted message

            RETURNS: msg with newline if appropriate
            """
            try:
                if record.pfx_newline:
                    return "\n" + msg
            except:
                pass
            return msg

        def format(self, record):
            """
            Applies a prefix newline if appropriate.
            """
            return self.replace_lf(
                self.apply_newline_prefix(
                    record,
                    super(MASNewlineLogFormatter, self).format(record)
                )
            )


    class MASExtraPropLogAdapter(logging.LoggerAdapter):
        """
        Log adapter_ctor that enables defaulting of props on LogRecord objects.
        Use this if you need extra props.

        PROPERTES:
            extra_props - dictionary of extra props and their default values
        """

        def __init__(self, logger, extra_props):
            """
            IN:
                logger - the logger to adapt
                extra_props - dict of props to default on LogRecord objects.
                    key: name of prop
                    value: default value
            """
            super(MASExtraPropLogAdapter, self).__init__(logger, extra_props)

        def _add_extra_prop(self, prop_name, kwargs):
            """
            Adds a prop from the kwargs to the extra kwargs.
            Assumes extra is set.

            IN:
                prop_name - name of the prop to get from kwargs
                kwargs - should contain the prop data (if exists)

            OUT:
                kwargs - prop data moved to extra if found.
            """
            if prop_name not in kwargs:
                return

            kwargs["extra"][prop_name] = kwargs.pop(prop_name)

        def process(self, msg, kwargs):
            """
            Override of process.

            Main difference is to update existing extra dict if it exists
            """
            self.set_extra(kwargs)
            return msg, kwargs

        def set_extra(self, kwargs):
            """
            Sets the extra kwarg with our extra data, updating existing if
            found. Also pulls extra props directly from the kwargs if
            those props are found.

            OUT:
                kwargs - the kwargs to set extra in
            """
            if "extra" in kwargs:
                new_extra = dict(self.extra)
                new_extra.update(kwargs["extra"])
                kwargs["extra"] = new_extra
            else:
                kwargs["extra"] = dict(self.extra)

            for prop_name in self.extra:
                self._add_extra_prop(prop_name, kwargs)


    class MASNewlineLogAdapter(MASExtraPropLogAdapter):
        """
        Log adapter_ctor with an option for newline kwargs.
        The newline kwarg is pfx_newline.
        """

        def __init__(self, logger, extra_props=None, newline_def=False):
            """
            IN:
                logger - the logger to adapt
                extra_props - additional props, other than the newline one.
                    Optional.
                    (Default: None)
                newline_def - the default value for the newline prop
                    (Default: False)
            """
            if extra_props is None:
                extra_props = {}

            extra_props["pfx_newline"] = newline_def
            super(MASNewlineLogAdapter, self).__init__(logger, extra_props)


    #We always log to renpy.config.basedir/log
    LOG_PATH = os.path.join(renpy.config.basedir, "log")

    LOG_MAXSIZE_B = 5242880 #5 mb

    #Add the header to each log, including OS info + MAS version number
    #NOTE: python logging does not auto handle CRLF, so we need to explicitly manage that for the header
    LOG_HEADER = "\r\n\r\n{_date}\r\n{system_info}\r\n{renpy_ver}\r\n\r\nVERSION: {game_ver}\r\n{separator}"

    #Unformatted logs use these consts (spj/pnm)
    MSG_INFO = "[" + LT_INFO + "]: {0}"
    MSG_WARN = "[" + LT_WARN + "]: {0}"
    MSG_ERR = "[" + LT_ERROR + "]: {0}"

    MSG_INFO_ID = "    " + MSG_INFO
    MSG_WARN_ID = "    " + MSG_WARN
    MSG_ERR_ID = "    " + MSG_ERR

    #Load strs for files
    LOAD_TRY = "Attempting to load '{0}'..."
    LOAD_SUCC = "'{0}' loaded successfully."
    LOAD_FAILED = "Load failed."

    JSON_LOAD_FAILED = "Failed to load json at '{0}'."
    FILE_LOAD_FAILED = "Failed to load file at '{0}'. | {1}"
    NAME_BAD = "name must be unique."

    #Ensure log path exists
    try:
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
    except Exception as e:
        raise Exception("Failed to create log folder because: {}".format(e))

    #Full logging info
    def init_log(name, append=True, formatter=None, adapter_ctor=None, header=None, rotations=5):
        """
        Initializes a logger with a handler with the name and files given.

        IN:
            name - name of the logger, this will be the same as the file, with the file appending '.txt'
            append - Whether or not we're appending this log or clearing it on load
                (Default: True)
            formatter - custom logging.Formatter to be used.
                If None is provided, the default MASLogFormatter is used.
                NOTE: IF YOU ARE USING YOUR OWN FORMATTER, YOU SHOULD CALL THE `replace_lf` METHOD TO ENSURE YOUR LOGS ARE USING CRLF
                (Default: None)
            adapter_ctor - Constructor reference to the adapter we want to use. If None, no adapter is used
                (Default: None)
            header - Header block for logs to use. If None, the default header printing version info is used. If False, no header is used.
                (Default: None)
            rotations - Integer representing the amount of log rotations we should have. If 0, no rotations are used.
                (Default: 5)

        NOTE: ALL LOGS ARE IN renpy.config.basedir/log/
        All logs flush and rotate once they're 5 mb in size.
        """
        _kwargs = {
            "filename": os.path.join(LOG_PATH, name + '.log'),
            "mode": ("a" if append else "w"),
            "encoding": "utf-8",
            "delay": header is False #We auto delay here if no header to only gen the file once we need to
        }

        #Setup header
        if header is None:
            header = LOG_HEADER

        if append:
            handler = loghandlers.RotatingFileHandler(
                maxBytes=LOG_MAXSIZE_B,
                backupCount=rotations,
                **_kwargs
            )
        else:
            handler = logging.FileHandler(**_kwargs)

        log = logging.getLogger(name)

        #Allow all severities to be logged
        log.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)

        #Add the handler so we can print log header info
        log.addHandler(handler)

        #Write as this has no formatting yet
        if header is not False:
            log.info(
                header.format(
                    _date=datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
                    system_info="{0} {1} - build: {2}".format(platform.system(), platform.release(), platform.version()),
                    renpy_ver=renpy.version(),
                    game_ver=renpy.config.version,
                    separator="=" * 50
                )
            )

        if formatter is None:
            handler.setFormatter(MASLogFormatter())

        else:
            #Now apply formatting to all further uses
            handler.setFormatter(formatter)

        if adapter_ctor is not None:
            log = adapter_ctor(log)

        #Add it to the map
        LOG_MAP[name] = log

        return log


    def get_log(name):
        """
        Gets a log from the log map

        IN:
            name - log name

        RETURNS: log, or None if no log
        """
        return LOG_MAP.get(name)


    def is_inited(name):
        """
        Checks if a log has been inited

        IN:
            name - log name
        """
        return name in LOG_MAP


python early in mas_utils:
    import codecs
    import os
    import sys
    import platform
    import shutil
    import store
    import time
    import traceback
    import functools

    from store import mas_logging

    
    def init_mas_log():
        """
        Initializes the MAS log, or gets it if its already init.

        RETURNS: the init'd mas_log
        """
        global mas_log

        if mas_logging.is_inited("mas_log"):
            return mas_logging.get_log("mas_log")

        mas_log = mas_logging.init_log("mas_log")
        return mas_log


    mas_log = init_mas_log()


    def deprecated(use_instead=None, should_raise=False):
        """
        Decorator that marks functions and classes as deprecated

        During LINT every UNIQUE EXECUTION (during the init phase) of a deprecated object
            will be reported to stdout using lint hooks
        During RUNTIME every EXECUTION of a deprecated object
            will be reported in the main log (mas_log.txt) and stderr
        NOTE: if we were allowed to raise, we RAISE a DeprecationWarning intead

        You can access all the reports via __all_warnings__

        IN:
            use_instead - string with the name of the function/class to use instead
            should_raise - whether we raise an exception or just log the error
        """
        def decorator(callable_):
            """
            The actual decorator

            IN:
                callable_ - the func/class to decorate
            """
            # FIXME: We have to do this 'til we finally get py3
            DEF_ATTR = ("__module__", "__name__", "__doc__")
            assigned = [attr for attr in DEF_ATTR if hasattr(callable_, attr)]

            @functools.wraps(callable_, assigned=assigned)
            def wrapper(*args, **kwargs):
                """
                Wrapper around the deprecated function/class
                """
                msg = "'{module}{name}' is deprecated.{use_instead_text}"

                if hasattr(callable_, "__module__") and callable_.__module__:
                    module = callable_.__module__ + "."
                else:
                    module = ""

                name = callable_.__name__

                if not use_instead:
                    use_instead_text = ""
                else:
                    use_instead_text = " Use '{0}' instead.".format(use_instead)

                msg = msg.format(
                    module=module,
                    name=name,
                    use_instead_text=use_instead_text
                )

                deprecated.__all_warnings__.add(msg)

                if should_raise:
                    raise DeprecationWarning(msg)

                else:
                    print("[WARNING]: " + msg, file=sys.stderr)
                    mas_log.warning(msg)

                return callable_(*args, **kwargs)

            return wrapper

        return decorator

    # Keep all warnings
    deprecated.__all_warnings__ = set()

    # mac logging
    class MASMacLog(renpy.renpy.log.LogFile):
        def __init__(self, name, append=False, developer=False, flush=True):
            """
            `name`
                The name of the logfile, without the .txt extension.
            `append`
                If true, we will append to the logfile. If false, we will truncate
                it to an empty file the first time we write to it.
            `developer`
                If true, nothing happens if config.developer is not set to True.
            `flush`
                Determines if the file is flushed after each write.
            """
            super(MASMacLog, self).__init__(name, append=append, developer=developer, flush=flush)


        def open(self):  # @ReservedAssignment
            if self.file:
                return True

            if self.file is False:
                return False

            if self.developer and not renpy.config.developer:
                return False

            if not renpy.config.log_enable:
                return False

            try:

                home = os.path.expanduser("~")
                base = os.path.join(home,".MonikaAfterStory/" )

                if base is None:
                    return False

                fn = os.path.join(base, self.name + ".txt")

                path, filename = os.path.split(fn)
                if not os.path.exists(path):
                    os.makedirs(path)

                if self.append:
                    mode = "a"
                else:
                    mode = "w"

                if renpy.config.log_to_stdout:
                    self.file = real_stdout

                else:

                    try:
                        self.file = codecs.open(fn, mode, "utf-8")
                    except:
                        pass

                if self.append:
                    self.write('')
                    self.write('=' * 78)
                    self.write('')

                self.write("%s", time.ctime())
                try:
                    self.write("%s", platform.platform())
                except:
                    self.write("Unknown platform.")
                self.write("%s", renpy.version())
                self.write("%s %s", renpy.config.name, renpy.config.version)
                self.write("")

                return True

            except:
                self.file = False
                return False

    # A map from the log name to a log object.
    mas_mac_log_cache = { }

    @deprecated(use_instead="mas_logging.init_log")
    def macLogOpen(name, append=False, developer=False, flush=False):  # @ReservedAssignment
        rv = mas_mac_log_cache.get(name, None)

        if rv is None:
            rv = MASMacLog(name, append=append, developer=developer, flush=flush)
            mas_mac_log_cache[name] = rv

        return rv

    @deprecated(use_instead="mas_logging.init_log")
    def getMASLog(name, append=False, developer=False, flush=False):
        if renpy.macapp or renpy.macintosh:
            return macLogOpen(name, append=append, developer=developer, flush=flush)
        return renpy.renpy.log.open(name, append=append, developer=developer, flush=flush)

    @deprecated(use_instead="mas_logging.init_log")
    def logcreate(filepath, append=False, flush=False, addversion=False):
        """
        Creates a log at the given filepath.
        This also opens the log and sets raw_write to True.
        This also adds per version number if desired

        IN:
            filepath - filepath of the log to create (extension is added)
            append - True will append to the log. False will overwrite
                (Default: False)
            flush - True will flush every operation, False will not
                (Default: False)
            addversion - True will add the version, False will not
                You dont need this if you create the log in runtime,
                (Default: False)

        RETURNS: created log object.
        """
        new_log = getMASLog(filepath, append=append, flush=flush)
        new_log.open()
        new_log.raw_write = True
        if addversion:
            new_log.write("VERSION: {0}\n".format(
                store.persistent.version_number
            ))
        return new_log

    @deprecated(use_instead="mas_utils.mas_log.info")
    def writelog(msg):
        """
        Writes to the mas log if it is open

        IN:
            msg - message to write to log
        """
        mas_log.info(msg)
        #if mas_log_open:
        #    mas_log.write(msg)

    @deprecated(use_instead="mas_utils.mas_log.critical")
    def wtf(msg):
        """
        Wow That Failed
        For logging stuff that should never happen

        IN:
            msg - message to log
        """
        mas_log.critical(msg)

    @deprecated(use_instead="mas_utils.mas_log.debug('', exc_info=True)")
    def writestack():
        """
        Prints current stack to log
        """
        mas_log.debug("".join(traceback.format_stack()))

    #"No longer necessary as all logs have builtin rotation"
    @deprecated()
    def logrotate(logpath, filename):
        """
        Does a log rotation. Log rotations contstantly increase. We defualt
        to about 2 decimal places, but let the limit go past that

        NOTE: exceptions are logged

        IN:
            logpath - path to the folder containing logs
                NOTE: this is assumed to have the trailing slash
            filename - filename of the log to rotate
        """
        try:
            filelist = os.listdir(logpath)
        except Exception as e:
            mas_log.error(str(e))
            return

        # log rotation constants
        __numformat = "{:02d}"
        __numdelim = "."

        # parse filelist for valid filenames,
        # also sort them so the largest number is last
        filelist = sorted([
            x
            for x in filelist
            if x.startswith(filename)
        ])

        # now extract only the largest number in this list.
        # NOTE: this is only possible if we have more than one file in the list
        if len(filelist) > 1:
            fname, dot, largest_num = filelist.pop().rpartition(__numdelim)
            largest_num = tryparseint(largest_num, -1)

        else:
            # otherwise
            largest_num = -1

        # now increaese largest num to get the next number we should write out
        largest_num += 1

        # delete whatever file that is if it exists
        new_path = os.path.normcase("".join([
            logpath,
            filename,
            __numdelim,
            __numformat.format(largest_num)
        ]))
        trydel(new_path)

        # and copy our main file over
        old_path = os.path.normcase(logpath + filename)
        copyfile(old_path, new_path)

        # and delete the current file
        trydel(old_path)


    class IsolatedFlexProp(object):
        """
        class that supports flexible attributes.
        all attributes that are set are stored in a 
        separate internal structure. Supports a few additional behaviors
        because of this.

        Supports:
            - extracting the vars that were manually set into a dict format
                - _to_dict/_from_dict
            - clearing all vars that were manually set
                - _clear
            - direct attribute get/set (obj.attribute)
            - key-based get/set (obj[key])
                Don't use this to access built-ins.
            - attribute existence ("attribute" in obj)
        """
        __slots__ = ("_default_val", "_set_vars")

        def __init__(self, default_val=None):
            """
            Constructor

            IN:
                default_val - the value to return as default when retrieving
                    a prop that does not exist.
                    (Default: None)
            """
            self._default_val = default_val
            self._set_vars = {}

        def __repr__(self):
            return "<{}: (def value: {}, data: {})>".format(
                type(self).__name__,
                self._default_val,
                self._set_vars
            )

        def __contains__(self, item):
            return item in self._set_vars

        def __getattr__(self, name):
            if name.startswith("_"):
                return super(IsolatedFlexProp, self).__getattribute__(name)
            return self._set_vars.get(name, self._default_val)

        def __setattr__(self, name, value):
            if name.startswith("_"):
                super(IsolatedFlexProp, self).__setattr__(name, value)
            else:
                self._set_vars[name] = value

        def __getitem__(self, key):
            return self.__getattr__(key)

        def __setitem__(self, key, value):
            self.__setattr__(key, value)

        def _clear(self):
            """
            Clears manually set attributes
            """
            self._set_vars.clear()

        def _from_dict(self, data):
            """
            sets internal data using a dict

            IN:
                data - dictionary to load from
            """
            for key in data:
                self[key] = data[key]

        def _to_dict(self):
            """
            Returns manually set data in raw format for persistent

            RETURNS: dict of the manually set data (shallow copy)
            """
            return dict(self._set_vars)


    def compareVersionLists(curr_vers, comparative_vers):
        """
        Generic version number checker

        IN:
            curr_vers - current version number as a list (eg. 1.2.5 -> [1, 2, 5])
            comparative_vers - the version we're comparing to as a list, same format as above

            NOTE: The version numbers can be different lengths

        OUT:
            integer:
                - (-1) if the current version number is less than the comparitive version
                - 0 if the current version is the same as the comparitive version
                - 1 if the current version is greater than the comparitive version
        """
        #Define a local function to use to fix up the version lists if need be
        def fixVersionListLen(smaller_vers_list, larger_vers_list):
            """
            Adjusts the smaller version list to be the same length as the larger version list for easy comparison

            IN:
                smaller_vers_list - the smol list to adjust
                larger_vers_list - the list we will adjust the smol list to

            OUT:
                adjusted version list

            NOTE: fills missing indeces with 0's
            """
            for missing_ind in range(len(larger_vers_list) - len(smaller_vers_list)):
                smaller_vers_list.append(0)
            return smaller_vers_list

        #Let's verify that the lists are the same length
        if len(curr_vers) < len(comparative_vers):
            curr_vers = fixVersionListLen(curr_vers, comparative_vers)

        elif len(curr_vers) > len(comparative_vers):
            comparative_vers = fixVersionListLen(comparative_vers, curr_vers)

        #Check if the lists are the same. If so, we're the same version and can return 0
        if comparative_vers == curr_vers:
            return 0

        #Now we iterate and check the version numbers sequentially from left to right
        for index in range(len(curr_vers)):
            if curr_vers[index] > comparative_vers[index]:
                #The current version is greater here, let's return 1 as the rest of the version is irrelevant
                return 1

            elif curr_vers[index] < comparative_vers[index]:
                #Comparative version is greater, the rest of this is irrelevant
                return -1


    def copyfile(oldpath, newpath):
        """
        Copies the file at oldpath into a file at newpath
        Paths assumed to include the filename (like an mv command)

        NOTE:
            if a copy fails, the error is logged

        IN:
            oldpath - path to old file, including filename
            newpath - path to new file, including filename

        RETURNS:
            True if copy succeeded, False otherwise
        """
        try:
            shutil.copyfile(oldpath, newpath)
            return True
        except Exception as e:
            mas_log.error(_mas__failcp.format(oldpath, newpath, str(e)))
        return False


    def _get_version_nums(ver_str):
        """
        Gets version numbers from a version string

        IN:
            ver_str - version string to get version from

        RETURNS: version numbers as a list of ints
        """
        return list(map(int, ver_str.partition("-")[0].split(".")))


    def is_ver_stable(ver_str):
        """
        Checks if a version number is stable or not.
        A stable version is generally a 3-tiered version number.

        IN:
            ver_str - version number string to check

        RETURNS: true if version is stable, False if not.
        """
        return len(_get_version_nums(ver_str)) == 3


    def _is_downgrade(from_ver_str, to_ver_str):
        """
        Checks if the version transition given is a downgrade

        IN:
            from_ver_str - starting version (as ver str)
            to_ver_str - ending version (as ver str)

        RETURNS: true if downgrade, False if not
        """
        return compareVersionLists(
            _get_version_nums(from_ver_str),
            _get_version_nums(to_ver_str)
        ) > 0


    def trydel(f_path, log=False):
        """
        Attempts to delete something at the given path

        NOTE: completely hides exceptions, unless log is True
        """
        try:
            os.remove(f_path)
        except Exception as e:
            if log:
                mas_log.error("[exp] {0}".format(repr(e)))

    def trywrite(f_path, msg, log=False, mode="w"):
        """
        Attempts to write out a file at the given path

        Exceptions are hidden

        IN:
            f_path - path to write file
            msg - text to write
            log - True means we log exceptions
                (Default: False)
            mode - write mode to use
                (Defaut: w)
        """
        outfile = None
        try:
            outfile = open(f_path, mode)
            outfile.write(msg)
        except Exception as e:
            if log:
                mas_log.error("[exp] {0}".format(repr(e)))
        finally:
            if outfile is not None:
                outfile.close()

    def tryparseint(value, default=0):
        """
        Attempts to parse the given value into an int. Returns the default if
        that parse failed.

        IN:
            value - value to parse
            default - value to return if parse fails
            (Default: 0)

        RETURNS: an integer representation of the given value, or default if
            the given value could not be parsed into an int
        """
        try:
            return int(value)
        except:
            return default

