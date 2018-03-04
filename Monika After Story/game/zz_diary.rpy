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
    import os

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
    DIARY_TEMPLATE_EXT = "mde" # Monika Diary Entry

    # diary comment character
    DIARY_COMMENT = "#"

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

    ################## functions ############################
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
                nonspace_dex = limit_dex    

        # otherwise, just use limit dex
        else:
            nonspace_dex = limit_dex
                
        return (line[:limit_dex], line[nonspace_dex:])


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
    def _dk_body(modifier):
        """
        Generates the body

        IN:
            modifier - modifier as a string (SEE the dict for rules)

        RETURNS:
            body string
        """
        # TODO
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
        # TODO: use modifier name to limit lenght of string
        if len(games_played) > 0:
            if len(games_played) > 1:
                return (
                    ", ".join(games_played[:-1]) +
                    " and {0}".format(games_played[-1:])
                )

            # otherwise
            return games_played[0]

        # otherwise
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
        "body": _dk_body,

        # monika's name
        # name|<modifier>
        # modifier rules:
        #   t - use twitter name
        "m_name": _dk_gen_monikaName

    }



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

# Topics?: that might be too variable
