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

#### metric datas. These should NOT be persisetent.
# list of tuples of event entries:
#   [0]: event_database of this entry
#   [1]: key of this entry
# NOTE: these are assumed in chronological-like order
define mas_diary.event_entries = list()

# list of games played today 
# TODO: change this to include stats on how many times we've played these games
define mas_diary.games_played = list()

# list of game outcomes
# NOTE match-style games (pong, chess) are here.
# key: game
# value: (player wins, draws, player losses)
define mas_diary.game_outcomes = dict()

# list of player moods (can also manage mood swings)
# TODO: waiting on moods pr
define mas_diary.player_moods = list()

# list of story-based entries.  These are written in list order.
# each entry is a tuple of the following format:
#   [0]: unique_id - unique ID for this entry
#   [1]: entry - actual string entry
define mas_diary.story_entries = list()

# lock to prevent story entires from being added
define mas_diary.story_lock = False

# list of special custom diary entry strings. Each string is considered a
# "line". These are placed after main diary entry but before the PS section
#define mas_diary.custom_entries = list()

# list of PS diary entry lines. Each string is considered a "line"
# each line gets an extra P (PS, PPS, PPPS...)
define mas_diary.ps_entries = list()

# set to closed self upon start
define mas_diary.closed_self = False 

# diary been touched today? (by the player)
# this value should be set at start in the same location session time
# is handled.
define mas_diary.diary_opened = False

# modifiers for diary entries (based on ingame stuff)
# refer to the specific functions for what modifiers should be
define mas_diary.diary_modifiers = dict()

### UNIQUE IDS for story events
define mas_diary.opendoor_knock = 1
define mas_diary.opendoor_open_one = 2
define mas_diary.opendoor_open_two = 3
define mas_diary.opendoor_open_three = 4
define mas_diary.opendoor_listen_rmrf = 11
define mas_diary.opendoor_listen_surprise = 12

#### persistents we need
# True if we've written a diary entry today, False otherwise.
# this should reset every day. and after a day has been written
default persistent._mas_diary_written = False

# list of dicts of the following format:
#   "filepath": file path to diary
#   "checksum": checksum of the file
#   "entries": number of entries written to this file
#
# NOTE: we assume that the first entry in this list is the latest diary.
# NOTE: we doing this historically so we can:
#   a - not use the same place/name twice
#   b - see if the player modded any of these diaries
#   c - kind of give us an idea of how many times player has intruded privacy
default persistent._mas_diary_files = list()

# list of unique ids that have been written out already
# clear this on new day
#default persistent._mas_diary_stories_written = list()

init python in mas_diary:
    # global stuff
    import os
    import math # yuck
    import datetime

    # store stuff
    import store.mas_utils as mas_utils

    # specific stuff
    from cStringIO import StringIO # we do alot of string work here

    # folder path to diary templates (from game)
    DIARY_TEMPLATE_FOLDER = "mod_assets/templates/diary"

    # main templates folder
    MAIN_FOLDER = "/main/"

    # PS entry folder
    PS_FOLDER = "/ps/"

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

    # section delimiter
    DLMTR_S = "@"

    # keyword delimeter
    DLMTR_KW_S = "{"
    DLMTR_KW_E = "}"

    # renpy sub delimiters
    DLMTR_RS_S = "["
    DLMTR_RS_E = "]"

    # modifier delimiters
    DLMTR_MOD = "|"

    # diary entry size limits
    # 80 sheets - 160 entries
    # 100 sheets - 200 entries
    # TODO: decide this

    # internal value copies because of issues with scope
    _internal_twitter = None

    # list of the scanned valid templates
    templates = list()

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

    # this is the dict that we actually use when parsing.
    # make sure to fill it before use using the init functions
    diary_keywords = dict()

    ################## functions ############################
    def addGamePlayed(game):
        """
        Adds the game played to the games played list, if it has not been
        added already
        """
        # TODO:
        # NOTE i think we need to rethink this
        # TODO: chess
        if game not in games_played:
            games_played.append(game)


    def addStoryEntry(entry, override_lock=False, replace=False):
        """
        Adds a story entry to the story_entries
        If the story entries is locked, this will not do anything unless
        override_lock is True

        IN:
            entry - the entry to add. tuple of the following format:
                [0]: unique id of this entry
                [1]: the entry itself
            override_lock - True means we bypass story locks, False means we
                do not
                (Default: False)
            replace - True means we replace the first instance of an entyr with
                the same unique ID. False means we append as usual
                (Default: False)

        ASSUMES:
            story_entries
        """
        if override_lock or not story_lock:
            if replace:
                loc = indexStoryEntry(entry[0], story_entries)
                if loc >= 0:
                    story_entries.pop(loc)

            # entries are always appended
            story_entries.append(entry)


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


    def indexStoryEntry(entry_id, entry_list):
        """
        Returns index of the story entry with the same id

        IN:
            entry_id - id the entry to find
            entry_list - the list of entries to search through

        RETURNS: index of this story entry, or -1 if not found
        """
        for index in range(0, len(entry_list)):
            if entry_id == entry_list[index][0]:
                return index

        return -1


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


    def _chooseEventEntries(count=None, chrono=True, use_nl=True):
        """
        Picks entries from the event_entries list according to the given params
        NOTE: will return a generic for no entries, if applicable

        IN:
            count - number of entries to pick. If None, then we pick all
                (Default: None)
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
        output = StringIO() # cStringIO version

        # minor optimization? maybe
        entry_length = len(event_entries)

        # inital check if we even have entries to grab
        if entry_length == 0:
            return renpy.random.choice([
                "We didn't talk about much today."
            ])

        if entry_length < count:
            # this means the amount of options available is less than what we
            # wanted. make this flow select all then.
            count = None

        # otherwise, normal operation

        # first, generate a range for us to use
        if count is None:
            selected = range(0, entry_length)
        else:
            selected = mas_utils.randrange(count, 0, entry_length-1, True)

        # the first entry is special!
        # (we dont add a newline prior to the entry
        ev_db, ev_key = event_entries[selected[0]]
        if ev_db[ev_key].diary_entry[0] is not None:
            output.write(ev_db[ev_key].diary_entry[0])

        # now iterate over that range
        for index in selected[1:]:
            ev_db, ev_key = event_entries[index]

            output.write("\n\n")
            output.write(ev_db[ev_key].diary_entry[0])

        # split line check
        body_str = output.getvalue()
        output.close()

        if not use_nl:
            return body_str.splitlines()

        return body_str


    def _scanEntryTemplates():
        """
        Scans the template folder for valid entry templates.

        RETURNS:
            list of template filepaths we found
        """
        return _scanTemplates(MAIN_FOLDER)


    def _scanPSTemplates():
        """
        Scans the template folder for valid PS templates.

        RETURNS:
            list of template filepaths we found
        """
        return _scanTemplates(PS_FOLDER)


    def _scanTemplates(folder):
        """
        Scans the template folder for valid templates.

        IN:
            folder - the folder we are getting templates from

        RETURNS:
            list of template filepaths we found
        """
        templates = list()
        t_files = os.listdir(diary_basedir + folder)
        for t_filename in t_files:
            t_filepath = diary_basedir + folder + t_filename
            
            if (
                    isValidTemplateFilename(t_filename) 
                    and isValidTemplateFile(t_filepath)
                ):
                # TODO, this really should be a dict with ## as the keys
                templates.append(t_filepath)

        return templates


############## diary keyword functions ######################
    # these functions will be set to values in some of the dicts 
    def _dk_body(modifier, curr_mods):
        """
        Generates the body

        IN:
            modifier - modifier as a string (SEE the dict for rules)
            curr_mods - UNUSED

        RETURNS:
            body string

        ASSUMES:
            event_entries
        """
        if len(modifier) > 0:
            # the modifier is a real value

            if modifier.startswith("a"):
                # use all entries
                return _chooseEventEntries()

            elif modifier.startswith("%"):
                # use a percentage of entires
                sel_pct = mas_utils.tryparseint(modifier[1:], -1)

                # they decided to negative us? use the default
                if sel_pct < 0:
                    sel_count = DEFAULT_BODY_COUNT

                elif sel_pct >= 100:
                    # wait, they wanted all? why u gotta trick me
                    return _chooseEventEntries()

                else:
                    # otherwise, we need to get an integer value out of this
                    # percetnage
                    sel_count = int(math.ceil(
                        len(event_entries) * (sel_pct / 100.0)
                    ))

                    if sel_count >= len(event_entries):
                        # again, if you got all of them, lets make this easy
                        return _chooseEventEntries()

                # now that we have a number, countinue

            else:
                # modifier is a number probably
                sel_count = mas_utils.tryparseint(modifier, DEFAULT_BODY_COUNT)

        else:
            # otherwise, assume default number of entries
            sel_count = DEFAULT_BODY_COUNT

        # otherwise, we are using a numerical value
        return _chooseEventEntries(sel_count)


    def _dk_closing(modifier, curr_mods):
        """
        Generates the closing

        IN:
            modifier - UNUSED
            curr_mods - dict of modifications to apply because of in-game 
                events

        RETURNS:
            closing string
        """
        # if the curr_mods includes a key for mood, then we pick a closing
        # that is appropriate. The mood can be:
        #   "good" - good mood
        #   "bad" - bad mood
        #   None (or anything else) - neutral mood
        if curr_mods is not None:
            mood_mod = curr_mods.get("mood", None)
        else:
            mood_mod = None

        # create list of closings available
        # NOTE: we do this because we don't need closings all the time
        # NOTE: if you have repeats, put them in the lists they repeat in
        if mood_mod == "good":
            # good closings
            greetings_list = [
                "With love,",
                "Love,",
                "Happily in love,", # TODO: probably should be separated when we do friends
                "Until next time,",
                ":)"
            ]

        elif mood_mod == "bad":
            # bad closings
            greetings_list = [
                "Unhappily,",
                ":(",
                "Whatever,",
                "Bye."
            ]

        else:
            # neutral closings
            greetings_list = [
                "Sincerely,",
                "From,",
                "Love,",
                "Until next time,"
            ]

        # pick a greetings
        return renpy.random.choice(greetings_list)
   

    def _dk_day(modifier, curr_mods):
        """
        Gets the current day as a string

        IN:
            modifier - modifier as a string (SEE the dict for rules)
            curr_mods - UNUSED

        RETURNS: current day as a string
        """
        if modifier == "f":
            # full word day
            return datetime.date.today().strftime("%A")

        elif modifier == "2u":
            # 2 digit day, unpadded
            return str(datetime.date.today().day)

        elif modifier == "s":
            # short word day
            return datetime.date.today().strftime("%a")

        # 2 digit day
        return datetime.date.today().strftime("%d")


    def _dk_gamesCSV(modifier, curr_mods):
        """
        Sets up the games CSV string

        IN:
            modifier - modifier as a string (SEE the dict for rules)
            curr_mods - UNUSED

        RETURNS:
            games CSV string
        """       
        if len(games_played) > 0:

            if len(games_played) > 1:
                # more than one game played
                games_played_str = (
                    ", ".join(games_played[:-1]) +
                    " and {0}".format(games_played.pop())
                )

            else:
                # otherwise only one game played today
                games_played_str = games_played[0]

        else:
            # otherwise no games played today
            games_played_str = ""

        if "i" in modifier:
            # intro text was requested

            if len(games_played_str) == 0:
                # no games played
                return "We didn't play any games today."

            # games were played
            games_played_str = "Today we played {0}.".format(games_played_str)

        if "b" in modifier:
            # break lines was requested
            return breakLines(games_played_str)

        # othrwise as is
        return games_played_str

    
    def _dk_greeting(modifier, curr_mods):
        """
        Generates a greeting

        IN:
            modifier - UNUSED 
            curr_mods - dict of mods to apply because of in-game events

        RETURNS:
            greeting string
        """
        # if the curr_mods includes a key for mood, then we pick a 
        # greeting that is appropraite. The mood can be:
        #   "good" - good mood
        #   "bad" - bad mood
        #   None (or anything else) - neutral mood
        if curr_mods is not None:
            mood_mod = curr_mods.get("mood", None)
        else:
            mood_mod = None

        # create the list of greetings available
        # NOTE: we do this because we don't need greetings all the time
        # NOTE: if you have repeats, put them in the lists that they repeat in
        if mood_mod == "good":
            # good greetings
            greetings_list = [
                "Dear diary,",
                "Dear diary:",
                "Hey diary,",
                "Hello there."
            ]


        elif mood_mod == "bad":
            # bad greetings
            greetings_list = [
                "Dear diary:",
                "Sigh,"
            ]

        else:
            # neutral greetings
            greetings_list = [
                "Dear diary,",
                "Dear diary:",
                "Hey diary,",
                "Hello there."
            ]

        # pick a greeting
        return renpy.random.choice(greetings_list)


    def _dk_m_name(modifier, curr_mods):
        """
        Generates monika's name

        IN:
            modifier - modifier as a string (SEE the dict for rules)
            curr_mods - UNUSED

        RETURNS: monika's name
        """
        if modifier == "t":
            return _internal_twitter

        # otherwise
        # NOTE: not a constant because YOU CANT CHANGE THIS
        # TODO this needs to be changed because of the new nickname thing
        # probably another modifier
        return "Monika"


    def _dk_month(modifier, curr_mods):
        """
        Gets current month as a string

        IN:
            modifier - modifier as a string (SEE the dict for rules)
            curr_mods - UNUSED

        RETURNS: current month as a string
        """
        if modifier == "f":
            # full word month
            return datetime.date.today().strftime("%B")

        elif modifier == "s":
            # short word month
            return datetime.date.today().strftime("%b")

        elif modifier == "2u":
            # 2 digit month, unpadded
            return str(datetime.date.today().month)

        # 2 digit month
        return datetime.date.today().strftime("%m")


    def _dk_ps(modifier, curr_mods):
        """
        Generates PS entries.
        Breaklines is automatically assumed

        IN:
            modifier - UNUSED
            curr_mods - UNUSED

        RETURNS:
            PS entry string

        ASSUMES:
            ps_entries
        """
        if len(ps_entries) > 0:
            # at least one PS entry

            output = StringIO() # from cStringIO
            
            # setup base values
            ps_base = "P.S: "
            ps_part = "P."
            entry_count = 0

            for entry in ps_entries:

                # build PS string
                ps_str = (ps_part * entry_count) + ps_base + entry

                # write breaklines version of ps string
                output.write(breakLines(ps_str))
                output.write("\n")

                # increase the P
                entry_count + =1

            # return PS entries
            outstr = output.getvalue()
            output.close()
            return outstr

        # otherwise no PS entries
        return None

    
    def _dk_story(modifier, curr_mods):
        """
        Generates story event entries.

        IN:
            modifier - UNUSED
            curr_mods - UNUSED

        RETURNS:
            story event string

        ASSUMES:
            story_entries
        """
        if len(story_entries) > 0:
            # at least one story entry
            return "\n\n".join([entry[1] for entry in story_entries])

        # otherwise no story entries
        return None


    def _dk_topicsCSV(modifier, curr_mods):
        """
        Generates CSV of topics discussed today. this uses the short diary
        entries

        IN:
            modifier - modifier as a string (SEE the dict for rules)
            curr_mods - UNUSED

        RETURN: CSV of topics discussed today.

        ASSUMES:
            event_entries 
        """
        if len(event_entries) > 0:

            # we only want short entries that exist
            short_entry_list = [
                ev_db[ev_key].diary_entry[1]
                for ev_db,ev_key in event_entries
                if ev_db[ev_key].diary_entry[1] is not None
            ]

            if len(short_entry_list) > 1:
                # more than one topic
                topics_str = (
                    ", ".join(short_entry_list[:-1]) + 
                    " and {0}".format(short_entry_list.pop())
                )

            else:
                # otherwise only one topic
                topics_str = short_entry_list[0]

        else:
            # otherwise no topics discussed today
            topics_str = ""

        if "i" in modifier:
            # intro text was requested

            if len(topics_str) == 0:
                # no topics discussed
                return "We didn't talk about much today."

            # topics were discussed
            topics_str = "Today we talked about {0}.".format(topics_str)

        if "b" in modifier:
            # break lines was requested
            return breakLines(topics_str)

        # otherwise as is
        return topics_str


    def _dk_year(modifier, curr_mods):
        """
        Gets current year as a string.

        IN:
            modifier - modifier as a string (SEE the dict for rules)
            curr_mods - UNUSED

        RETURNS: current year as a string
        """
        if modifier == "2":
            # 2 digit year
            return datetime.date.today().strftime("%y")

        # default is 4 digit year
        return datetime.date.today().strftime("%Y")


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

    # diary keywords general
    # consists of other diary-related things
    # all functions accept a curr_mods dict of modifiers.
    #   (not all of them use it though)
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
        "m_name": _dk_m_name,

        # games played, comma separated
        # gamesCSV|<modifier>
        # modifier rules:
        #   b - break the lines into multiple ones
        #   i - include intro text
        # combinable: b, i
        "gamesCSV": _dk_gamesCSV,

        # topics discussed, comma separated
        # topicsCSV|<modifier>
        # modifier rules:
        #   b - break the lines into multiple ones
        #   i - include intro text
        # combinable: b, i
        "topicsCSV": _dk_topicsCSV,

        # story entries. These will only be populated if we have any story
        # events, like changing name, knocking on the door, stuff like that
        # Each story event is written in its own separate block, like a
        # paragraph
        # NOTE: disabled for now
#        "story": _dk_story,

        # PS entries. 
        # no modifier
        # NOTE: ps entry is no longer used. Instead PS entries are considerd
        # multiple sessions
#        "ps": _dk_ps,

        # current year
        # Y|<modifier>
        # modifier rules:
        #   4 - 4 digit current year (Default)
        #   2 - 2 digit current year
        "Y": _dk_year,

        # current month
        # M|<modifier>
        # modifier rules:
        #   2 - 2 digit current month (Default)
        #   2u - 2 digit current month, unpadded
        #   f - full word current month
        #   s - short/abbreviated word current month
        "M": _dk_month,

        # current day
        # D|<modifier>
        # modifier rules:
        #   2 - 2 digit current day (date) (Default)
        #   2u - 2 digit current day, unpadded (date)
        #   f - full word current day
        #   s - short/abbrv word current day
        "D": _dk_day

        # TODO: times

        # 
        "h": _dk_hour,
    }


#### functions for parsing #####################
    def parseLine(line, diary_kws, curr_mods):
        """
        Parses the given line appropriately. This function applies replacements
        in the following order:

        1. Sections 
        2. renpy subs

        Note that a "line" in the diary template can expand to multiple lines
        in the actual diary.

        NOTE: breaklines isnt used here. I'm not sure how/when we really 
            should apply breaklines because of custom formatting for entires

        IN:
            line - the line to parse
            diary_kws - dict of diary keywords to apply to line
            curr_mods - dict of current modifiers to apply to section
                generation functions

        RETURNS:
            string to write being parsed, or NONE if this line should be
            ignored
        """
        # if the line is empty or just a newline, return it
        if len(line) == 0 or line.isspace():
            return line

        # if the line starts with a comment, return None, which means we 
        # shouldn't write anything out for this line
        if line[0] == DIARY_COMMENT:
            return None

        # start with section parsing
        line = _parseSections(line, curr_mods)

        # now keyword parsing
#        line = line.format(**diary_kws)

        # now renpy sub
        # NOTE: this can also be adjusted for scope and translation by kw:
        #   scope - scope to substitute, i think its a dict
        #       (Default: use default store, which is probably global)
        #   translate - True means to translate, false to not
        #       (Defaullt: True)
        line = renpy.substitute(line)

        return line


    def _parseSection(section, curr_mods):
        """
        Parses the given section for modifiers and stuff.
        Does NOT resolve {keywords} or [subs]

        IN:
            section - section string. assumes modifiers are attached
            curr_mods - dict of current modifiers to apply to section
                generation functions

        RETURNS:
            the result of the parsed section. If the section was invalid, the
            string is not changed.

        ASSUMES:
            diary_keywords_gen
        """
        if len(section) == 0:
            # this means template did an @@
            return DMLTR_S

        # now parse modifiers
        section_kw, dlmtr, modifier = section.partition(DLMTR_MOD)

        generator = diary_keywords_gen.get(section_kw, None)

        if generator is None:
            # no generator function means we have an invalid keyword. Just
            # return the given string.
            return section

        # otherwise we can process the generator
        return generator(modifier, curr_mods)


    def _parseSections(line, curr_mods):
        """
        Parses the given line for sections, and fills them out. 
        Does NOT resolve {keywords} or [subs]

        IN:
            line - the line we are parsing
            curr_mods - dict of curent modifiers to apply to section 
                generation functions

        RETURNS:
            the line after filling in sections. If no sections are found, the
            line will be returned as is.
        """
        if DLMTR_S not in line:
            return line

        # we have confirmed the presence of section delimiters
        outline = StringIO() # lots of string building here
        curr_line = line
        while DLMTR_S in curr_line:
        
            # the first parition call sets up the start of the section keyword
            first, dlmtr, curr_line = curr_line.partition(DLMTR_S)

            if len(first) > 0:
                # stuff before the first delimiter should be written
                outline.write(first)

            # the 2nd partition call retrieves the value of the section and
            # sets up the next part of the line to parse
            section_kw, dlmtr, curr_line = curr_line.partition(DLMTR_S)

            if len(dlmtr) == 0:
                # if dlmtr is an empty string, then we have a dangling 
                # delimiter.For the sake of not having runtime exceptions, 
                # just treat the remainder of this string as a comment and 
                # ignore it.
                # NOTE: this is NOT what DLMTR_S should be used for. Comments
                #   should start at the beginning of the line with a #
                outline.write("\n")
                curr_line = ""

            else:
                # dlmtr non empty string, we have a section keyword
                outline.write(_parseSection(section_kw, curr_mods))

        # now write the remainder of curr_line
        outline.write(curr_line)

        # alright, we've finished parsing sections for this string.
        outstr = outline.getvalue()
        outline.close()
        return outstr


# post startup stuff
init 2018 python:
    import store.mas_diary as mas_diary

    mas_diary.diary_basedir = (
        config.basedir +
        mas_diary.GAME_FOLDER +
        mas_diary.DIARY_TEMPLATE_FOLDER
    ).replace("\\", "/")
   
    mas_diary._internal_twitter = mas_monika_twitter_handle

    def mas_writeDiary(template_choice):
        """
        Writes a diary entry to file.
        """

        # TODO: determining what file to write.
        # TODO: determining which template to pick

        # NOTE: debug stuff right now
        entry_templates = mas_diary._scanEntryTemplates()

        # NOTE: debug
        # template_choice should be an int
        sel_template = entry_templates[template_choice]
    
        # TODO,if the file doesnt exist, use "w"
        # otherwise, use "a"
        with open(basedir + "/test.bin", "a") as diary:
            with open(sel_template, "r") as diary_template:
                for line in diary_template:
                    out_line = mas_diary.parseLine(line, diary_kws, None)
                    if out_line is not None:
                        diary.write(out_line)

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
# Sections use: @keyword|modifier@
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
#
# BODY (missing)
# these are lines to display if you didn't talk with the player at all
# - no modifieres for now
#
# GREETINGS:
# these are like the Dear Diary starters.
# - no modifiers for now
#
# CLOSINGS: 
# like, Love, sincerely, and so on
# - no modifiers for now

# keywords process:
# {keyword} - these are for direct string-string replacements
# @section|mod@ - these are for section replacements. these may also include
#   modifiers
# [player] - these are handled by renpy.substitute
# ``` <text> ``` - anything in 3 backticks is considered literal text and will
#   appear as is in the diary (minus the ticks) TODO

# order of operations:
# 1. @section@
# 2. {keyword}
# 3. [player]

