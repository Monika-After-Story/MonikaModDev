# Diary entries FOR MONIKA
#

# FUCK TAXABLE INCOME

# Diary entries whitepaper:
# 
# Diary entries are effectively little snippets into the everyday life of
# monika from her point of view. WE use a combination of metric data gathering
# and templating to somewhat achieve relasitic diary entries.
#
# Also, we checksum the diary for changes and also use access time to check if
# the user has played around with the diary, Monika will get mad if you touch
# it without her asking, ya know.
#
# Diaries should be written once per day, with multiple diary entries being 
# written if the player stopped visiting her. We'll cap this at like 3-5 days
# so we dont get too many bland entries.
#
# we'll use a persistet to keep track if a diary entry has been made today.
# i thjink that should be good for this.
#
# diary templates are scanned via the startswith keyword and extension

# TODO: we're not gonna do this yet, but at some point, add a property to Event
# for diary lines. Basically if an event will trigger a specific diary entry
# we should display it in the diary.

#### metric datas. These should NOT be persisetent.
# list of tuples of event entries:
#   [0]: event_database of this entry
#   [1]: key of this entry
# NOTE: these are assumed in chronological-like order
define mas_diary.event_entries = list()

# list of games played today 
define mas_diary.games_played = list()

# list of game outcomes
# NOTE match-style games (pong, chess) are here.
# key: game
# value: (player wins, draws, player losses)
define mas_diary.game_outcomes = dict()

# list of player moods (can also manage mood swings)
# TODO: waiting on moods pr
define mas_diary.player_moods = list()

# list of special custom diary entry strings. Each string is considered a
# "line". These are placed after main diary entry but before the PS section
define mas_diary.custom_entries = list()

# list of PS diary entry lines. Each string is considered a "line"
# each line gets an extra P (PS, PPS, PPPS...)
define mas_diary.ps_entries = list()

# diary been touched today? (by the player)
# this value should be set at start in the same location session time
# is handled.
define mas_diary.diary_opened = False

#### persistents we need
# True if we've written a diary entry today, False otherwise.
# this should reset every day. and after a day has been written
default persistent._mas_diary_written = False

# checksum of the diary
# if this None, we assume no diary exists
default persistent._mas_diary_checksum = None

init python in mas_diary:
    # global stuff
    import os
    import math # yuck

    # store stuff
    import store.mas_utils as mas_utils

    # specific stuff
    from cStringIO import StringIO # we do alot of string work here

    # folder path to diary templates (from game)
    DIARY_TEMPLATES_FOLDER = "mod_assets/templates/diary/"

    # game folder
    # we only need this until we create a mod_assets.rpa (probably)
    GAME_FOLDER = "/game/"

    # internally stored folder, generated at start of game
    diary_basedir = ""

    # template file template
    # probalby use this with startswith
    DIARY_TEMPLATE_NAME = "template_" 

    # template file extensions
    DIARY_TEMPLATE_EXT = "mdet" # Monika Diary Entry Template
#    DIARY_GAME_LINES_EXT = "mdgl" # Monika Diary Game Lines

    # diary comment character
    DIARY_COMMENT = "#"

    # default count for entires (for a body)
    DEFAULT_BODY_COUNT = 3

    # internal value copies because of issues with scope
    _internal_twitter = None

    # list of the scanned valid templates
    templates = list()

    # literal diary keyword dicts
    # these ones dont call into functions
    # diary keywords for dates
    diary_keywords_dates_auto = {
        "YYYY": "%Y", # 4 digit current year
        "YY": "%y", # 2 digit current year
        "MM": "%m", # 2 digit current month
        "Mfull": "%B", # full word current month
        "Mshort": "%b", # abbv/3char current month
        "DD": "%d", # 2 digit current day
        "Dfull": "%A", # full word current day
        "Dshort": "%a" # abbv current day 
    }

    # diary keywords for dates (custom)
    diary_keywords_dates_custom = {
        "mm": "{0}", # 2 digit current month, unpadded
        "dd": "{0}" # 2 digit current day, unpadded
    }

    # diary keywords for times
    # TODO: do we really need this
    # NOTE: we would also need session start times as well
    diary_keywords_times_ls_auto = {
        # time ones
        "lsHH": "%H", # 24 hour time, last session
        "lshh": "%I", # 12 hour time, last session
        "lsAP": "%p", # am,pm thing, last session
        "lsMI": "%M", # minute, last session
        "lsSS": "%S" # second, last session
    }

    ################## functions ############################
    def breakLines(string, min_length=100, max_length=120, use_nl=True):
        """
        Breaks the given string into multiple lines that follow the min/max
        line length rule.

        IN:
            string - the string we want to break up
            min_length - the minimum length per line
                (Default: 100)
            max_length - the maximum length per line
                (Default: 120)
            use_nl - True means use newlines to identify line breaks.
                False will add each line to a list
                (Default: True)

        RETURNS:
            if use_nl is True, then a single string with newlines for handling
            line breaks.
            If use_nl is False, then a list of strings where each string 
            represents a line.
        """
        output = StringIO() # cStringIO version

        curr_line = string
        while len(curr_line) > max_length:

            # limit this line and continue
            new_line, curr_line = limitLine(curr_line, min_length, max_length)
            output.write(new_line)
            output.write("\n")

        # at this point, curr_line will contain either the last line or 
        # nothing if theres no more lines
        if len(curr_line) > 0:
            output.write(curr_line)

        outstring = output.getvalue()
        output.close()

        # if we're not using newlines, better split by them
        if not use_nl:
            return outstring.splitlines()

        # otherwise we're done
        return outstring
        

    def indexLeftSpace(string, loc, end_loc=0):
        """
        Returns the index of the nearest space on the left of the string

        IN:
            string - the string to check
            loc - the index to begin check
            end_loc - the index to stop check
                NOTE: the check INCLUDES this index
                (Default: 0)

        RETURNS: the index of the nearest space, or -1 if no spcae found
        """
        index = loc
        while index >= end_loc and not string[index].isspace():
            index -= 1

        return index


    def indexRightNonSpace(string, loc, end_loc=None):
        """
        Returns the index of the nearest nonspcae character on the right of
        the string

        IN:
            string - string to check
            loc - the index to begin check
            end_loc the index to stop check
                NOTE: the check does NOT include this index
                (Defualt: None - the length of hte string)

        RETURNS: the index of the nearest nonspace, -1 if no nonspace found
        """
        if end_loc is None:
            end_loc = len(string)

        index = loc
        while index < end_loc and string[index].isspace():
            index += 1

        if index >= len(string):
            return -1

        return index
       

    def indexRightSpace(string, loc, end_loc=None):
        """
        Returns the index of the nearest space on the right of the string

        IN:
            string - the string to check
            loc - the index to begin check
            end_loc - the index to stop check
                NOTE: the check does NOT include this index
                (Default: None - the length of the string)

        RETURNS: the index of the nearest space, or -1 if no space found
        """
        if end_loc is None:
            end_loc = len(string)

        index = loc
        while index < end_loc and not string[index].isspace():
            index += 1

        if index >= len(string):
            return -1

        return index


    def isValidTemplateFile(filepath):
        """
        Checks if the file at the given filepath is a valid template file

        Valid template files start with a DIARY_COMMENT.
        TODO: more on this later?

        IN:
            filepath - path to the file to check

        RETURNS: True if the file at filepath is a valid template file,
            false otherwise
        """
        with open(filepath, "r") as t_file:
            return t_file.readline().startswith(DIARY_COMMENT)

        return False

    
    def isValidTemplateFilename(filename):
        """
        Checks if the given filename is a valid template filename

        IN:
            filename - the filename to check

        RETURNS: True if filename is a valid template filename, false otherwise
        """
        return (
            filename.startswith(DIARY_TEMPLATE_NAME) and 
            filename.endswith("." + DIARY_TEMPLATE_EXT)
        )


    def limitLine(line, min_length=100, max_length=120):
        """
        Limits the length of the given line so it is within a particular length
        range.
        Lines are broken by whitespace

        IN:
            line - the string to limit
            min_length - the minimum length this string should be
                (Default: 100)
            max_length - the maximum length this string should be

        RETURNS:
            tuple of the following format:
                [0]: the length-limited line
                [1]: the rest of the string 
        """
        # first, check if the min_length/max_length numbers are valid
        if min_length > max_length:
            return ("", line)

        # check if we have to do any changes
        if len(line) <= max_length:
            return (line, "")

        # otherwise, we need to do some limiting
        limit_dex = indexLeftSpace(line, max_length - 1, min_length)
        found_right = False

        # if we didn't find a length smaller, try slightly bigger, using 
        # difference between max and min
        if limit_dex < 0:
            limit_dex = indexRightSpace(
                line, 
                max_length -1, 
                max_length + (max_length - min_length)
            )

            # still not found, try any space left
            if limit_dex < 0:
                limit_dex = indexLeftSpace(line, min_length - 1)

                # still not found? try any space right
                if limit_dex < 0:
                    limit_dex = indexRightSpace(
                        line, 
                        max_length + (max_length - min_length) - 1
                    )

                    # still not found? forget limiting, this string is too long
                    if limit_dex < 0:
                        return (line, "")

                    # found white spcae by moving right
                    else:
                        found_right = True

            # found white spcae by moving right
            else:
                found_right = True

        # if our limit dex was found via a right-space check, then we
        # should find the first nonspace index
        if found_right:
            nonspace_dex = indexRightNonSpace(line, limit_dex+1)

            if nonspace_dex < 0:
                nonspace_dex = len(line)

        # otherwise, just use limit dex
        else:
            nonspace_dex = limit_dex
                
        return (line[:limit_dex], line[nonspace_dex:])


    def _chooseEventEntries(count=None, random=True, chrono=True, use_nl=True):
        """
        Picks entries from the event_entries list according to the given params
        NOTE: will return a generic for no entries, if applicable

        IN:
            count - number of entries to pick. If None, then we pick all
                (Default: None)
            random - True means we pick randomly, False means in order.
                NOTE: this only applies if count is not None
                (Default: True)
            chrono - True means respect chronological adding order, False
                means do not.
                (Default: True)
            use_nl - True means return the output as a string with newlines.
                False means return the output as a list of strings, with each
                string being a line
                (Default: True)

        RETURNS:
            If use_nl - one giant string with newlines
            if not use_nl - list of strings, each string being a line

        ASSUMES:
            event_entries
        """
        output - StringIO() # cStringIO version

        # minor optimization? maybe
        entry_length = len(event_entries)

        # inital check if we even have entries to grab
        if entry_length == 0:
            # TODO: we want to select from a predeteremined list of lines
            return "nothing here for now"

        if entry_length < count:
            # this means the amount of options available is less than what we
            # wanted. make this flow select all then.
            count = None

        # otherwise, normal operation

        # first, generate a range for us to use
        if count is None:
            selected = range(0, entry_length)
        else:
            selected = mas_utils.randrange(count, 0, entry_length, True)

        # the first entry is special!
        # (we dont add a newline prior to the entry
        ev_db, ev_key = selected[0]
        output.write(ev_db[ev_key].diary_entry)

        # now iterate over that range
        for index in selected[1:]:
            ev_db, ev_key = selected[index]

            output.write("\n")
            output.write(ev_db[ev_key].diary_entry)

        # split line check
        body_str = output.getvalue()
        output.close()

        if not use_nl:
            return body_str.splitlines()

        return body_str


    def _fillDiaryKeywordsDates(using_date=None):
        """
        Fills the diary replacement keywords for dates dict

        IN:
            using_date - if not None, we use this date to populate the
                dates dict. otherwise we use current date
        """
        import datetime

        # check for ussing date
        if using_date is None:
            using_date = datetime.date.today()

        # process keyword replacements
        for date_kw in diary_keywords_dates_auto:
            diary_keywords_dates_auto[date_kw] = (
                using_date.strftime(diary_keywords_dates_auto[date_kw])
            )

        # and custom ones
        diary_keywords_dates_custom["mm"] = (
            diary_keywords_dates_custom["mm"].format(using_date.month)
        )
        diary_keywords_dates_custom["dd"] = (
            diary_keywords_dates_custom["dd"].format(using_date.day)
        )


    def _scanTemplates():
        """
        Scans the template folder for valid templates.

        RETURNS: list of valid template filepaths
        """
        t_files = os.listdir(diary_basedir)
        for t_filename in t_files:
            t_filepath = diary_basedir + t_filename
            
            if (
                    isValidTemplateFilename(t_filename) 
                    and isValidTemplateFile(t_filepath)
                ):
                templates.append(t_filepath)


############## diary keyword functions ######################
    # these functions will be set to values in some of the dicts 
    def _dk_body(modifier)
        """
        Generates the body

        IN:
            modifier - modifier as a string (SEE the dict for rules)

        RETURNS:
            body string

        ASSUMES:
            event_entries
        """
        if len(modifier) > 0:
            # the modifier is a real value

            if modifier.startswith("a"):
                # use all entries
                #TODO
                # this should return

            elif modifier.startswith("%"):
                # use a percentage of entires
                sel_pct = tryparseint(modifier[1:], -1)

                # they decided to negative us? use the default
                if sel_pct < 0:
                    sel_count = DEFAULT_BODY_COUNT

                elif sel_pct >= 100:
                    # wait, they wanted all? why u gotta trick me
                    return _dk_body("a")

                else:
                    # otherwise, we need to ceil this
                    sel_count = math.ceil(
                        len(event_entries) * (sel_pct / 100.0)
                    )

                    if sel_count >= len(event_entries):
                        # again, if you got all of them, lets make this easy
                        return _dk_body(modifier)



            else:
                # modifier is a number probably
                try:
                    sel_count = int(modifier)
                except:
                    # it wasnt a string, but thats okay, use the default
                    sel_count = DEFAULT_BODY_COUNT

            # take

        # otherwise, we are using a numerical value
            

        return ""


    def _dk_closing(modifier):
        """
        Generates the closing

        IN:
            modifier - modifier as a string (SEE the dict for rules)

        RETURNS:
            closing string
        """
        # TODO
        return ""
    

    def _dk_gamesCSV(modifier):
        """
        Sets up the games CSV string

        IN:
            modifier - modifier as a string (SEE the dict for rules)

        RETURNS:
            games CSV string
        """       
        if len(games_played) > 0:

            if len(games_played) > 1:
                games_played_str = (
                    ", ".join(games_played[:-1]) +
                    " and {0}".format(games_played[-1:])
                )

                # break up the lines
                if modifier == "b":
                    return breakLines(games_played_str)

                # otherwise as is
                return games_played_str

            # otherwise only one game played today
            return games_played[0]

        # otherwise no games played today
        return ""

    
    def _dk_greeting():
        """
        Generates a greeting

        RETURNS:
            greeting string
        """
        # TODO:
        return ""


    def _dk_m_name(modifier):
        """
        Generates monika's name

        IN:
            modifier - modifier as a string (SEE the dict for rules)
        """
        if modifier == "t":
            return _internal_twitter

        # otherwise
        return "Monika"


# some stuff should happen a bit later
init 1 python in mas_diary:
    ########################## diary entry keywords dicts
    # these kwargs are treated as format specifier names in diary templates
    # TODO
    # NOTE: for all DATES, look into strftime() and strptime() behavior
    #   that has stuff for using abbrv names
    # we might replace some of this with renpy.substitute
    # these are initliazed outside of this store at startup
    # and are probably reinitalized 

    # diary keywords for games
    diary_keywords_games = {
        # games played, comma separated
        # gamesCSV|<modifier>
        # modifier rules:
        #   b - break the line into multiple if needed
        "gamesCSV": _dk_gamesCSV

        # TODO: we need to figure out the framework for thesee 
#        "game_chess": None, # result of chess game (if it was played)
#        "game_piano": None, # result of piano (if it was played)
#        "game_hangman": None, # results of hangman (if it was played)
#        "game_pong": None # results of pong (if it was played)
    }

    # diary keywords general
    # consists of other diary-related things
    diary_keywords_gen = {
        # like the Dear Diary stuff. this should be 
        # customizable by adding a file with lines
        "greeting": _dk_greeting,

        # sincerely, love, from. This also should be 
        # customizable by aadding a fiel with lines
        "closing": _dk_closing,

        # body section is where paragraph diary entries from topics go
        # body|<modifier>
        # modifier rules:
        #   %## - percentage of main diary entries to use (randomized)
        #   ## - number of main diary entries to use (randomized)
        #   a - use all diary entries
        #   (Default option is to use mas_diary.DEFAULT_BODY_COUNT
        "body": _dk_body,

        # monika's name
        # name|<modifier>
        # modifier rules:
        #   t - use twitter name
        "m_name": _dk_gen_monikaName

    }


#### functions for parsing #####################
    def parseLine(line, use_nl=False):
        """
        Parses the given line appropriately
        """


# post startup stuff
init 2018 python:
    import store.mas_diary as mas_diary

    mas_diary.diary_basedir = (
        config.basedir +
        mas_diary.GAME_FOLDER +
        mas_diary.DIARY_TEMPLATE_FOLDER
    ).replace("\\", "/")
   
   mas_diary._internal_twitter = mas_monika_twitter_handle

# TODO:
# diary templates are nearly fully customizable. Using a {keyword} system, you
# can construct templates of varying setups and stuff. Couple of key things:
# - [player] variables work as well, they are treated using renpy.substitute.
# - date keywords are designed to work for current date. 
# - the CSV keywords generate comma separated lists of stuff.
# - the section keywords are used to pick out lines/section of text that are
#   related to one thing.

# SECTIONS:
# so sections are like text groups that are related to stuff
# They have properties associated with them that are important for classifying
# a section's availability, since sometimes we can't use templated sections
# if some criteria isn't available.
#
# lets say this is an example:
# NOTE: these are actually stored in a text file so we avoid storing execess
# strings in memory
#
# GAMES:
# @<game name>|<wlpn>@ (win, lost, played, not played)
#   if game isnt there, assume not played
    """
    # Lost Chess, won pong 
    # @chess|l@
    # @pong|w@
    [player] lost at chess today, but [he] beat me at pong!
    I was quite surprised.
    """

# keywords process:
# {keyword} - these are for direct string-string replacements
# @section|mod@ - these are for section replacements. these may also include
#   modifiers
# [player] - these are handled by renpy.substitute
# ``` <text> ``` - anything in 3 backticks is considered literal text and will
#   appear as is in the diary (minus the ticks)
