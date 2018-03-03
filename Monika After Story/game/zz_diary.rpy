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
# list of category tags shown today
define mas_diary.category_tags = list()

# list of games played today 
define mas_diary.games_played = list()

# list of game outcomes
# NOTE match-style games (pong, chess) are here.
# key: game
# value: (player wins, draws, player losses)
define mas_diary.game_outcomes = dict()

# list of player moods (can also manage mood swings)
# TODO: waiting on moods pr
define mas_diary.moods = list()

# list of special custom diary entry strings. Each string is considered a
# "line". These are placed after main diary entry but before the PS section
define mas_diary.custom_entry_lines = list()

# list of PS diary entry lines. Each string is considered a "line"
# each line gets an extra P (PS, PPS, PPPS...)
define mas_diary.ps_entry_lines = list()

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

    # list of the scanned valid templates
    templates = list()

    ########################## diary entry keywords dicts
    # these kwargs are treated as format specifier names in diary templates
    # TODO
    # NOTE: for all DATES, look into strftime() and strptime() behavior
    #   that has stuff for using abbrv names
    # we might replace some of this with renpy.substitute
    # these are initliazed outside of this store at startup
    # and are probably reinitalized 

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

    # diary keywords for games
    diary_keywords_games = {
        "gamesCSV": None # games played, comma separated # TODO: framework for this?

        # TODO: we need to figure out the framework for thesee 
#        "game_chess": None, # result of chess game (if it was played)
#        "game_piano": None, # result of piano (if it was played)
#        "game_hangman": None, # results of hangman (if it was played)
#        "game_pong": None # results of pong (if it was played)
    }

    # diary keywords for topics
    diary_keywords_topics = {
        "topicsCSV": None # category tags for topics shown, comma separated # TODO: framework for this?
    }

    # diary keywords general
    # consists of other diary-related things
    diary_keywords_gen = {
        "greeting": None, # like the Dear Diary stuff. this should be 
            # customizable by adding a file with lines
        "closing": None # sincerely, love, from. This also should be 
            # customizable by aadding a fiel with lines
    }

    ################## functions ############################
    def addCategories(cat_list):
        """
        Adds the given list of category tags to the category tags diary entry
        list

        IN:
            cat_list - list of category tags to add to the diary entry list

        ASSUMES:
            category_tags
        """
        for cat in cat_list:
            if cat not in category_tags:
                category_tags.append(cat)

    
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


    def _initDiaryKeywordsGames():
        """
        Fills the diary replcaement keywords for games dict
        """
        # starting with the games CSV
        if len(games_played) > 0:
            if len(games_played) > 1:
                games_played_str = ", ".join(games_played[:-1])
                games_played_str += " and {0}".format(games_played[-1:])
            else:
                games_played_str = games_played[0]
            diary_keywords_games["gamesCSV"] = games_played_str


    def _initDiaryKeywordsTopics():
        """
        Fills the diary replacement keywords for topics dict
        """
        # starting with topics CSV
        if len(category_tags) > 0:
            if len(category_tags) > 1:
                category_tags_str = ", ".join(category_tags[:-1])
                category_tags_str += " and {0}".format(category_tags[-1:])
            else:
                category_tags_str = category_tags[0]
            diary_keywords_topics["topicsCSV"] = category_tags_str


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


# post startup stuff
init 2018 python:
    import store.mas_diary as mas_diary

    mas_diary.diary_basedir = (
        config.basedir +
        mas_diary.GAME_FOLDER +
        mas_diary.DIARY_TEMPLATE_FOLDER
    ).replace("\\", "/")
    

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
