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
define mas_diary.moods = list()

# list of special custom diary entry strings. Each string is considered a
# "line". These are placed after main diary entry but before the PS section
define mas_diary.custom_entry_lines = list()

# list of PS diary entry lines. Each string is considered a "line"
# each line gets an extra P (PS, PPS, PPPS...)
define mas_diary.ps_entry_lines = list()

#### persistents we need
# True if we've written a diary entry today, False otherwise.
# this should reset every day. and after a day has been written
default persistent._mas_diary_written = False

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

    # diary entry keywords dict
    # these kwargs are treated as format specifier names in diary templates
    # TODO
    # we might replace some of this with renpy.substitute
#    diary_keywords = {
#        "player": None,
#        "currentuser": None,
#        "mcname": None,
#        "his": None

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
# go over the formats for the tempaltes
