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
# this should reset every day.
# i think a cutoff of about 7am is a good cutoff for what constitutes a day
# TODO: review this a little more
default persistent._mas_diary_written = False

init python in mas_diary:

    # folder path to diary templates (from game)
    DIARY_TEMPLATES_FOLDER = "mod_assets/templates/diary/"

    # game folder
    # we only need this until we create a mod_assets.rpa (probably)
    GAME_FOLDER = "/game/"

    # template file template
    # probalby use this with startswith
    DIARY_TEMPLATE_NAME = "template_" 

    # template file extensions
    DIARY_TEMPLATE_EXT = "mde" # Monika Diary Entry

    # list of the scanned valid templates
    template_paths = list()

    # diary entry keywords dict
    # these kwargs are treated as format specifier names in diary templates
    # TODO
#    diary_keywords = {
#        "player": None

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


    def _scanTemplates():
        """
        Scans the template folder for valid templates.

        RETURNS: list of valid template filepaths
        """
        # TODO:
        pass


# TODO:
# go over the formats for the tempaltes
