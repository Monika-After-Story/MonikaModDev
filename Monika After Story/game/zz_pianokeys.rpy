# Module that lets you play the piano
#

# we need one persistent for data saving
# each list item is a tuple of the following format:
#   See PianoNoteMatchList._loadTuple
default persistent.pnml_data = []

# TRANSFORMS
transform piano_quit_label:
    xanchor 0.5 xpos 275 yanchor 0 ypos 332

transform piano_lyric_label:
    xalign 0.5 yalign 0.5

# super xp for playing well
define xp.ZZPK_FULLCOMBO = 40
#define xp.ZZPK_WIN = 30
define xp.ZZPK_PRACTICE = 15

# label that calls this creen
label zz_play_piano:

    # initial setup
    $ import store.zzpianokeys as zzpianokeys
    $ quit_label = Text("Press 'Z' to quit", size=36)
    $ pnmlLoadTuples()

    # Intro to piano dialogue here
    m 1j "You want to play the piano?"

label zz_play_piano_loopstart:

    # get song list
    $ song_list = zzpianokeys.getSongChoices()
    $ pnml = None
    $ play_mode = PianoDisplayable.MODE_FREE

label zz_play_piano_songchoice:

    if len(song_list) > 1:
        show monika 1a

        menu:
            m "Did you want to play a song or play on your own, [player]?"
            "Play a song":
                m "Which song?"
                $ pnml = renpy.display_menu(song_list)

                # song selected
                if pnml != "None":

                    # reaction in picking a song
                    m 1j "I'm so excited to hear you play, [player]!"

                    # launch label - if it exists, we can call this label to
                    # provide extra dialogue before playing this song
                    # not used atm
                    if pnml.launch_label:
                        call expression pnml.launch_label from _zzpk_ssll

                    # regardless, set mode
                    $ play_mode = PianoDisplayable.MODE_SONG

                    jump zz_play_piano_setupstart

                # nvermind selected
                else:
                    jump zz_play_piano_songchoice

            "On my own":
                pass

            "Nevermind":
                jump zz_play_piano_loopend

    # otherwise, we default to freestyle mode
    m 1a "Then play for me, [player]~"

label zz_play_piano_setupstart:

    show monika 1a at t22

    # pre call setup
    python:
        disable_esc()
        store.songs.enabled = False
        store.hkb_button.enabled = False
    stop music
    show text quit_label zorder 10 at piano_quit_label

    # call the display
    $ ui.add(PianoDisplayable(play_mode, pnml=pnml))
    $ full_combo,is_win,is_practice,post_piano = ui.interact()

    # post call cleanup
    hide text quit_label
    $ store.songs.enabled = True
    $ store.hkb_button.enabled = True
    $ enable_esc()
    $ play_song(store.songs.selected_track)
    $ pnmlSaveTuples()

    show monika 1j at t11

    # granting XP:
    # you are good player
    if full_combo and not persistent.ever_won['piano']:
        $persistent.ever_won['piano']=True
        $ grant_xp(xp.WIN_GAME)

    # call the post label
    call expression post_piano from _zzpk_ppel

    # No-hits dont get to try again
    if post_piano != "zz_piano_none":
        show monika 1a
        menu:
            m "Would you like to play again?"
            "Yes":
                jump zz_play_piano_loopstart
            "No":
                pass

label zz_play_piano_loopend:
    return

### labels for piano states ===================================================

# default. post game, freestyle mode
label zz_piano_default:
    m 1a "All done, [player]?"
    return

# Shown if player does not hit any notes
label zz_piano_none:
    m 1m "Uhhh [player]..."
    m 1l "I thought you wanted to play the piano?"
    m 1e "I really enjoy hearing you play."
    m 1j "Promise to play for me next time?"
    return

### YOUR REALITY

# shown if player completes the song but does not FC
label zz_piano_yr_win:
    m 1m "That was nice, [player]."
    m "But..."
    m 1n "You could do better with some more practice..."
    m 1l "Ehehe~"
    return

# shown if player FCs
label zz_piano_yr_fc:
    m 1b "That was wonderful, [player]!"
    m 1j "I didn't know you can play the piano so well."
    m 1a "Maybe we should play together sometime!"
    return

# shown if player did not complete song and had more fails than passes
label zz_piano_yr_fail:
    m 1o "..."
    m 1e "That's okay, [player]."
    m 1j "At least you tried your best."
    return

# shown if player did not complete song but had more passes than fails
label zz_piano_yr_prac:
    m 1a "That was really cool, [player]!"
    m 3b "With some more practice, you'll be able to play my song perfectly."
    m 1j "Make sure to practice everyday for me, okay~?"
    return

#abel zz_piano_yr_launch:
#   m

#### HOW TO FULL COMBO:
# (Everday, I can imagine a future...)
# o o o oiu uio u y t y u t w
# opo opo ] ] p[ op [ o
#
# (In my hands, is a pen...)
# o p o uio iuy e w q e w u t
# opo opo ] ] p[ op [ o
#
# (The ink flows down...)
# o o o i u t t y u o
#
# (Just move your hands ...)
# p o u y  w e t  e t y t
#
# (but in this world..)
# o o o i  u t t y u o
#
# (What will it take..)
# p o u y   w e t   e t y t
#
# (What will it take)
# p o u y  w e t
#
# (that special day)
# e t y t
#
# [break]
#
# (Have i found, everybody....)
# o o o oiu uio u y t y u t w
# opo opo ] ] p[ op [ o
#
# (When you're here....)
# o p o uio iuy e w q e w u t
# opo opo ] ] p[ op [ o
#
# (when i cant even read...)
# o o o i u t t y u o
#
# (What good are words)
# p o u y
#
# (when a smile says it all)
# w e t  e t y t
#
# (and if this world...)
# o o o i  u t t y u o
#
# (what will it take, just for me...)
# p o u y   w e t   e t y t
#
# [break]
#
# (does my pen, only write...)
# o o o oiu uio u y t y u t w
#
# (is it love...)
# o p o uio iuy e w q e w u t
#
# (The ink flows down...)
# o o o i u t t y u o
#
# (how can i write...)
# p o u y  w e t  e t y t
#
# (if i cant hear...)
# o o o i  u t t y u o
#
# (what do you call...)
# p o u y   w e t   e t y t
#
# (and in your reality, if i dont know how to love you
# w e t  e t y t u i i u t e t o
# o u i t p o
#
# (I'll leave you be)
# w e t t
#
# Extra post:
# o o o oiu iop [ o [ o (chord: t u o)

# keep the above for reference
# DISPLAYABLE:

# special store to contain a rdiciulous amount of constants
init -3 python in zzpianokeys:
    import pygame # we need this for keymaps

    # this is our threshold for determining how many notes the player needs to
    # play before we check for dialogue
    NOTE_SIZE = 6

    # keys
    QUIT = pygame.K_z
    F4 = pygame.K_q
    F4SH = pygame.K_2
    G4 = pygame.K_w
    G4SH = pygame.K_3
    A4 = pygame.K_e
    A4SH = pygame.K_4
    B4 = pygame.K_r
    C5 = pygame.K_t
    C5SH = pygame.K_6
    D5 = pygame.K_y
    D5SH = pygame.K_7
    E5 = pygame.K_u
    F5 = pygame.K_i
    F5SH = pygame.K_9
    G5 = pygame.K_o
    G5SH = pygame.K_0
    A5 = pygame.K_p
    A5SH = pygame.K_MINUS
    B5 = pygame.K_LEFTBRACKET
    C6 = pygame.K_RIGHTBRACKET

    # keyorder, for reference
    KEYORDER = [
        F4,
        F4SH,
        G4,
        G4SH,
        A4,
        A4SH,
        B4,
        C5,
        C5SH,
        D5,
        D5SH,
        E5,
        F5,
        F5SH,
        G5,
        G5SH,
        A5,
        A5SH,
        B5,
        C6
    ]


    # Exception class for piano failures
    class PianoException(Exception):
        def __init__(self, msg):
            self.msg = msg
        def __str__(self):
            return "PianoException: " + self.msg


    # this class matches particular sets of notes to some dialogue that
    # Monika can say.
    # NOTE: only one line of dialogue per set of notes, because brevity is
    #   important
    #
    # PROPERTIES:
    #   say - the line of dialogue to say (as a Text object)
    #   notes - list of notes (keys) that we need to hear to show the dialogue
    #       this is ORDER match only. also chords are NOT supported
    #       NOTE: This is expected as a list of ZZPK constants.
    #   notestr - string version of the list of notes, for matching
    #   express - the expression we want monika to show (prefixed with monika)
    #   matched - True if we were matched this session, False otherwise
    #   matchdex - Basically an index that says where the last matched note is
    #       in notestr (and notes, by extension)
    #   ev_timeout - time we wait for input to start this note match
    #   vis_timeout - visual timeout that should be used when this match is
    #       running. This value should be less than ev_timeout
    #   fails - number of failed attempts to play this
    #   passes - number of succesful attempts to play this
    #   postnotes - list of notes (keys) that are considered post match.
    #       NOTE: so if this is played after the match, monika will continue
    #           her expression until a miss or the set is complete.
    #           in both cases, we should expect a clearing of played
    #   postexpress - expression monika should have during post mode
    #   verse - verse index this phrases belongs to. 0 means first verse,
    #       other values will be the starting index of that verse
    #   copynotes - if not None, this is the index of the pnm whose notes
    #       this matches
    #   misses - number of misses we got
    #   posttext - True if we should keep the text up for post expression,
    #       False if not
    #
    class PianoNoteMatch(object):
        def __init__(self,
                say,
                notes=None,
                postnotes=None,
                express="1b",
                postexpress="1a",
                ev_timeout=None,
                vis_timeout=None,
                verse=0,
                copynotes=None,
                posttext=False
            ):
            #
            # IN:
            #   say - line of dialogue to say (as a Text object)
            #   notes - list of notes (keys) to match
            #   postnotes - list of notes (keys) that are considered post
            #       match
            #       (Default: None)
            #   express - the monika expression we want to show
            #       (Default: 1b)
            #   postexpress - the monika expression to show during post
            #       (Default: 1a)
            #   ev_timeout - number of seconds we wait for input
            #       NOTE: THIS means how long we wait BEFORE this note match
            #           before assuming event timeout
            #       (Default: None)
            #   vis_timeout - number of second we wait for visual change
            #       NOTE: THIS means how long we wait AFTER this note match
            #           before cleaning visual
            #       (Default: None)
            #   verse - the verse dex the phrase belongs to
            #       (Default: 0)
            #   copynotes - the index that this pnm note matches with
            #       (Default: None)
            #   posttext - True if we keep the text up during post, False
            #       otherwise
            #       (Default: False)

            # sanity checks
            if notes is None or len(notes) == 0:
                raise PianoException("Notes list must exist")
            if verse < 0:
                raise PianoException("Verse must be positive number")
            if copynotes is not None and copynotes < 0:
                raise PianoException("copyntoes must be positive number")
            if type(say) is not renpy.text.text.Text:
                raise PianoException("say must be of type Text")
            if not renpy.image_exists("monika " + express):
                raise PianoException("Given expression does not exist")
            if not renpy.image_exists("monika " + postexpress):
                raise PianoException("Given post expression does not exist")
#            if (
#                    ev_timeout is not None
#                    and vis_timeout is not None
#                    and vis_timeout > ev_timeout
#                ):
#                raise PianoException(
#                    "Visual timeout cannot be greater than event timeout"
#                )

            self.say = say
            self.notes = notes
            self.notestr = "".join([chr(x) for x in notes])
            self.express = "monika " + express
            self.ev_timeout = ev_timeout
            self.vis_timeout = vis_timeout
            self.postnotes = postnotes
            self.postexpress = "monika " + postexpress
            self.verse = verse
            self.copynotes = copynotes
            self.posttext = posttext

            # set resettables
            self.reset()

        def isNoteMatch(self, new_key, index=None):
            #
            # Checks if the new key continous a notes match
            #
            # IN:
            #   new_key - the key we want to check (pygame key)
            #   index - current index we need to look at
            #       (Default: self.matchdex)
            #
            # OUT:
            #   returns 1 or larger if we have a match
            #       -1 if no match
            #       -2 if index out of range

            return self._is_match(new_key, self.notes, index=index)

        def isPostMatch(self, new_key, index=None):
            #
            # Checks if the new key continous a post match
            #
            # IN:
            #   new_key - the key we want to check (pygame key)
            #   index - current index we need to look at
            #       (Default: self.matchdex)
            #
            # OUT:
            #   returns 1 or large if we have a match
            #       -1 if no match
            #       -2 if index out of range

            return self._is_match(new_key, self.postnotes, index=index)

        def _is_match(self, new_key, notes, index=None):
            #
            # checks if the new key continous the match that we are expecting
            #
            # IN:
            #   new_key - the key we want to check (pygame key)
            #   notes - the notes list we want to look at
            #   index - current index we need to look at
            #       (Default: self.matchdex)
            #
            # OUT:
            #   returns 1 or larger if we have a match
            #       -1 if no match
            #       -2 if index out of range

            if index is None:
                index = self.matchdex

            if index >= len(notes):
                return -2

            if new_key == notes[index]:
                self.matchdex = index + 1
                return 1

            return -1


        def reset(self):
            """
            Resets this piano note match to its default values.

            NOTE: this only clears the following values:
                misses - 0
                fails - 0
                passes - 0
                matchdex - 0
                matched - False
            """
            self.misses = 0
            self.matchdex = 0
            self.fails = 0
            self.passes = 0
            self.matched = False


    class PianoNoteMatchList(object):
        """
        This a wrapper for a list of note matches. WE do this so we can
        easily group note matches with other information.

        PROPERTIES:
            pnm_list - list of piano note matches
            verse_list - list of verse indexes (must be in order)
            name - song name (displayed to user in song selection mode)
            full_combos - number of times the song has been played with no
                no mistakes
            wins - number of times the song has been completed
            losses - number of the times the song has been attempted but not
                completed
            win_label - labelt o call to if we played the song well
            fc_label - label to call to if we full comboed
            fail_label - label to call to if we failed the song
            prac_label - label to call if we are practicing
            end_wait - seconds to wait before continuing to quit phase
            launch_label - label to call to prepare song launch
        """

        def __init__(self,
                pnm_list,
                verse_list,
                name,
                win_label,
                fc_label,
                fail_label,
                prac_label,
                end_wait=0,
                launch_label=None
                ):
            """
            Creates a PianoNoteMatchList

            IN:
                pnm_list - list of piano note matches
                verse_list - list of verse indexes (must be in order)
                name - song name (displayed to user in song selection mode)
                win_label - label to call to if we played the song well
                fc_label - label to call to if we full comboed the song
                fail_label - label to call to if we failed the song
                prac_label - label to call if we are practicing
                end_wait - number of seoncds to wait before actually quitting
                    (Integers pleaes)
                    (Default: 0)
                launch_label - label to call to prepare this song for play
                    (Default: None)
            """
            if not renpy.has_label(win_label):
                raise PianoException(
                    "label '" + win_label + "' does not exist"
                )
            if not renpy.has_label(fc_label):
                raise PianoException(
                    "label '" + fc_label + "' does not exist"
                )
            if not renpy.has_label(fail_label):
                raise PianoException(
                    "label '" + fail_label + "' does not exist"
                )
            if not renpy.has_label(prac_label):
                raise PianoException(
                    "label '" + prac_label + "' does not exist"
                )
            if launch_label and not renpy.has_label(launch_label):
                raise PianoException(
                    "label '" + launch_label + "' does not exist"
                )

            self.pnm_list = pnm_list
            self.verse_list = verse_list
            self.name = name
            self.win_label = win_label
            self.fc_label = fc_label
            self.fail_label = fail_label
            self.prac_label = prac_label
            self.launch_label = launch_label
            self.end_wait = end_wait
            self.full_combos = 0
            self.wins = 0
            self.losses = 0

        def resetPNM(self):
            """
            Resets the piano note matches in this Piano Note Match List
            """
            for pnm in self.pnm_list:
                pnm.reset()

        def _loadTuple(self, data_tup):
            """
            Fills in the data of this PianoNoteMatchList using the given data
            tup. (which was probably pickeled)

            IN:
                data_tup - tuple of the following format:
                    [0] -> name
                    [1] -> full_combos
                    [2] -> wins
                    [3] -> losses
            """
            if len(data_tup) == 4:
                # we only accept this data tup if it has the appropriate length
                self.name, self.full_combos, self.wins, self.losses = data_tup

        def _saveTuple(self):
            """
            Generates a tuple of key data in this PianoNoteMatchList for
            pickling

            RETURNS:
                a tuple of the following format:
                    See _loadTuple
            """
            return (self.name, self.full_combos, self.wins, self.losses)

# this containst the actual songs
# we need it to be high init level so we have images
# TODO: considre making this readable from TEXt files.
# NOTE: if we do the above, we need to reconsider how we handle post game
# labels. Storing them in text files would be better organized but bad
# for finding errors
init 1000 python in zzpianokeys:

    # all piano note matches should follow this layout:
    # pnm_<song name inital>_v#l#
    # v#l# -> verse #, line #

### YOUR REALITY ##############################################################

    # your reality, piano note setup
    pnm_yr_v1l1 = PianoNoteMatch(
        renpy.text.text.Text(
            "Everyday, I imagine a future where I can be with you",
            style="monika_credits_text"
        ),
        [
            G5,
            G5,
            G5,
            G5,
            F5,
            E5,
            E5,
            F5,
            G5,
            E5,
            D5,
            C5,
            D5,
            E5,
            C5,
            G4
        ],
        postnotes=[
            G5,
            A5,
            G5,
            G5,
            A5,
            G5,
            C6,
            C6,
            A5,
            B5,
            G5,
            A5,
            B5,
            G5
        ],
        express="1k",
        postexpress="1j",
        verse=0
    )
    pnm_yr_v1l2 = PianoNoteMatch(
        renpy.text.text.Text(
            ("In my hands, is a pen that will write a poem of me" +
            " and you"),
            style="monika_credits_text"
        ),
        [
            G5,
            A5,
            G5,
            E5,
            F5,
            G5,
            F5,
            E5,
            D5,
            A4,
            G4,
            F4,
            A4,
            G4,
            E5,
            C5
        ],
        postnotes=pnm_yr_v1l1.postnotes,
        express="1b",
        postexpress="1a",
        verse=0,
    )
    pnm_yr_v1l3 = PianoNoteMatch(
        renpy.text.text.Text(
            "The ink flows down into a dark puddle",
            style="monika_credits_text"
        ),
        [
            G5,
            G5,
            G5,
            F5,
            E5,
            C5,
            C5,
            D5,
            E5,
            G5
        ],
        express="1b",
        postexpress="1a",
        verse=0
    )
    pnm_yr_v1l4 = PianoNoteMatch(
        renpy.text.text.Text(
            "Just move your hand, write the way into his heart",
            style="monika_credits_text"
        ),
        [
            A5,
            G5,
            E5,
            D5,
            G4,
            A4,
            C5,
            A4,
            C5,
            D5,
            C5
        ],
        express="1k",
        postexpress="1j",
        verse=0
    )
    pnm_yr_v1l5 = PianoNoteMatch(
        renpy.text.text.Text(
            "But in this world of infinite choices",
            style="monika_credits_text"
        ),
        pnm_yr_v1l3.notes,
        express="1b",
        postexpress="1a",
        verse=0
    )
    pnm_yr_v1l6 = PianoNoteMatch(
        renpy.text.text.Text(
            "What will it take just to find that special day?",
            style="monika_credits_text"
        ),
        pnm_yr_v1l4.notes,
        express="1b",
        postexpress="1a",
        verse=0
    )
    pnm_yr_v1l7 = PianoNoteMatch(
        renpy.text.text.Text(
            "What will it take just to find",
            style="monika_credits_text"
        ),
        [
            A5,
            G5,
            E5,
            D5,
            G4,
            A4,
            C5
        ],
        express="1b",
        postexpress="1a",
        verse=0,
        posttext=True
    )
    pnm_yr_v1l8 = PianoNoteMatch(
        renpy.text.text.Text(
            "that special day",
            style="monika_credits_text"
        ),
        [
            A4,
            C5,
            D5,
            C5
        ],
        express="1k",
        postexpress="1j",
        verse=0,
        ev_timeout=5.0,
        vis_timeout=3.0,
        posttext=True
    )

    # verse 2
    pnm_yr_v2l1 = PianoNoteMatch(
        renpy.text.text.Text(
            "Have I found everybody a fun assignment to do today?",
            style="monika_credits_text"
        ),
        pnm_yr_v1l1.notes,
        postnotes=pnm_yr_v1l1.postnotes,
        express="1b",
        postexpress="1a",
        verse=8,
        copynotes=0,
        ev_timeout=15.0
    )
    pnm_yr_v2l2 = PianoNoteMatch(
        renpy.text.text.Text(
            ("When you're here, everything that we do is fun for them"+
            " anyway"),
            style="monika_credits_text"
        ),
        pnm_yr_v1l2.notes,
        postnotes=pnm_yr_v1l2.postnotes,
        express="1k",
        postexpress="1j",
        verse=8,
        copynotes=1
    )
    pnm_yr_v2l3 = PianoNoteMatch(
        renpy.text.text.Text(
            "When I can't even read my own feelings",
            style="monika_credits_text"
        ),
        pnm_yr_v1l3.notes,
        express="1g",
        postexpress="1f",
        verse=8,
        copynotes=2
    )
    pnm_yr_v2l4 = PianoNoteMatch(
        renpy.text.text.Text(
            "What good are words",
            style="monika_credits_text"
        ),
        [
            A5,
            G5,
            E5,
            D5
        ],
        express="1g",
        postexpress="1f",
        vis_timeout=2.0,
        verse=8,
        posttext=True
    )
    pnm_yr_v2l5 = PianoNoteMatch(
        renpy.text.text.Text(
            "when a smile says it all?",
            style="monika_credits_text"
        ),
        [
            G4,
            A4,
            C5,
            A4,
            C5,
            D5,
            C5
        ],
        express="1k",
        postexpress="1j",
        vis_timeout=3.0,
        verse=8,
        posttext=True
    )
    pnm_yr_v2l6 = PianoNoteMatch(
        renpy.text.text.Text(
            "And if this world won't write me an ending",
            style="monika_credits_text"
        ),
        pnm_yr_v1l5.notes,
        express="1g",
        postexpress="1f",
        verse=8,
        copynotes=4
    )
    pnm_yr_v2l7 = PianoNoteMatch(
        renpy.text.text.Text(
            "What will it take just for me to have it all?",
            style="monika_credits_text"
        ),
        pnm_yr_v1l6.notes,
        express="1g",
        postexpress="1e",
        vis_timeout=3.0,
        verse=8,
        copynotes=5,
        posttext=True
    )

    # verse 3
    pnm_yr_v3l1 = PianoNoteMatch(
        renpy.text.text.Text(
            ("Does my pen only write bitter words for those who are "+
            "dear to me?"),
            style="monika_credits_text"
        ),
        pnm_yr_v1l1.notes,
#                [
#                    G5,
#                    G5,
#                    G5,
#                    F5,
#                    E5,
#                    E5,
#                    F5,
#                    G5,
#                    E5,
#                    D5,
#                    C5,
#                    D5,
#                    E5,
#                    C5,
#                    G4
#                ],
        express="1g",
        postexpress="1e",
        verse=15,
        copynotes=0,
        ev_timeout=25.0,
        vis_timeout=2.0
    )
    pnm_yr_v3l2 = PianoNoteMatch(
        renpy.text.text.Text(
            ("Is it love if I take you, or is it love if I set you " +
            "free?"),
            style="monika_credits_text"
        ),
        pnm_yr_v1l2.notes,
        express="1g",
        postexpress="1e",
        verse=15,
        copynotes=1,
        ev_timeout=7.0,
        vis_timeout=2.0
    )
    pnm_yr_v3l3 = PianoNoteMatch(
        pnm_yr_v1l3.say,
        pnm_yr_v1l3.notes,
        express="1b",
        postexpress="1a",
        verse=15,
        copynotes=2,
        ev_timeout=10.0
    )
    pnm_yr_v3l4 = PianoNoteMatch(
        renpy.text.text.Text(
            "How can I write love into reality?",
            style="monika_credits_text"
        ),
        pnm_yr_v1l4.notes,
        express="1g",
        postexpress="1e",
        verse=15,
        copynotes=3
    )
    pnm_yr_v3l5 = PianoNoteMatch(
        renpy.text.text.Text(
            "If I can't hear the sound of your heartbeat",
            style="monika_credits_text"
        ),
        pnm_yr_v1l5.notes,
        express="1p",
        postexpress="1o",
        verse=15,
        copynotes=4
    )
    pnm_yr_v3l6 = PianoNoteMatch(
        renpy.text.text.Text(
            "What do you call love in your reality?",
            style="monika_credits_text"
        ),
        pnm_yr_v1l6.notes,
        express="1g",
        postexpress="1e",
        verse=15,
        copynotes=5
    )
    pnm_yr_v3l7 = PianoNoteMatch(
        renpy.text.text.Text(
            "And in your reality, if I don't know how to love you",
            style="monika_credits_text"
        ),
        [
            G4,
            A4,
            C5,
            A4,
            C5,
            D5,
            C5,
            E5,
            F5,
            F5,
            E5,
            C5,
            A4,
            C5,
            G5
        ],
        postnotes=[
            G5,
            E5,
            F5,
            C5,
            A5,
            G5
        ],
        express="1p",
        postexpress="1m",
        verse=15
    )
    pnm_yr_v3l8 = PianoNoteMatch(
        renpy.text.text.Text(
            "I'll leave you be",
            style="monika_credits_text"
        ),
        [
            G4,
            A4,
            C5,
            C5
        ],
        postnotes=[
            G5,
            G5,
            G5,
            G5,
            F5,
            E5,
            F5,
            G5,
            A5,
            B5,
            G5,
            B5,
            G5
        ],
        express="1b",
        postexpress="1a",
        ev_timeout=5.0,
        vis_timeout=5.0,
        posttext=True
    )

    # your reality, pnml
    pnml_yourreality = PianoNoteMatchList(
        [
            pnm_yr_v1l1,
            pnm_yr_v1l2,
            pnm_yr_v1l3,
            pnm_yr_v1l4,
            pnm_yr_v1l5,
            pnm_yr_v1l6,
            pnm_yr_v1l7,
            pnm_yr_v1l8,
            pnm_yr_v2l1,
            pnm_yr_v2l2,
            pnm_yr_v2l3,
            pnm_yr_v2l4,
            pnm_yr_v2l5,
            pnm_yr_v2l6,
            pnm_yr_v2l7,
            pnm_yr_v3l1,
            pnm_yr_v3l2,
            pnm_yr_v3l3,
            pnm_yr_v3l4,
            pnm_yr_v3l5,
            pnm_yr_v3l6,
            pnm_yr_v3l7,
            pnm_yr_v3l8
        ],
        [0, 8, 15, 23],
        "Your Reality",
        "zz_piano_yr_win",
        "zz_piano_yr_fc",
        "zz_piano_yr_fail",
        "zz_piano_yr_prac",
        5.0
#        "zz_piano_yr_launch"
    )


### END =======================================================================

## setup dict of pnmls: #------------------------------------------------------

    pnml_db = dict()
    pnml_db[pnml_yourreality.name] = pnml_yourreality

    def getSongChoices():
        """
        Creates a list of tuples appropriate to display as a piano song
        selection menu.

        RETURNS:
            list of tuples for song selection. The returned list will for sure
            have at least one item (the nevermind)

        ASSUMES:
            pnml_db
        """
        song_list = list()

        for k in pnml_db:
            pnml = pnml_db.get(k)
            if pnml.wins > 0:
                song_list.append((pnml.name, pnml))

        song_list.append(("Nevermind", "None"))
        return song_list

# make this later than zzpianokeys
init 1001 python:
    import pygame # because we need them keyups
    import store.zzpianokeys as zzpianokeys

    # setup named tuple dicts
    def pnmlLoadTuples():
        """
        Loads piano note match lists from the saved data, wich is assumed to
        be in the proper format. No checking is done.

        ASSUMES:
            persistent.pnml_data
            zzpianokeys.pnml_db
        """
        for data_row in persistent.pnml_data:
            db_data = zzpianokeys.pnml_db.get(data_row[0], None)
            if db_data:
                db_data._loadTuple(data_row)

    def pnmlSaveTuples():
        """
        Saves piano not match list into a pickleable format.

        ASSUMES:
            persistent.pnml_data
            zzpianokeys.pnml_db
        """
        persistent.pnml_data = [
            zzpianokeys.pnml_db[k]._saveTuple() for k in zzpianokeys.pnml_db
        ]

    # the displayable
    class PianoDisplayable(renpy.Displayable):

        # CONSTANTS
        # timeout
        TIMEOUT = 1.0 # seconds
        SONG_TIMEOUT = 3.0 # seconds
        SONG_VIS_TIMEOUT = 4.0 # seconds
#        FAIL_TIMEOUT = 4.0 # number of seconds to display awkward face on fail
#        MISS_TIMEOUT = 4.0 # number of seconds to display awkard face on miss
#        MATCH_TIMEOUT = 4.0 # number of seconds to wait for match notes
        VIS_TIMEOUT = 2.5 # number of seconds to wait before changing face

        # DETECTION_LIST

        # AT_LIST
        AT_LIST = [i22]
        TEXT_AT_LIST = [piano_lyric_label]

        # expressions
        DEFAULT = "monika 1a"
        AWKWARD = "monika 1l"
        HAPPY = "monika 1j"
        FAILED = "monika 1m"

        # Text related
        TEXT_TAG = "piano_text"

        # STATEMACHINE STUFF

        # Default state. In this state, we run the detection algorithm.
        # No rendering adjustment is done in this state
        STATE_LISTEN = 0

        # Just MATCH state. Here, we just matched a phrase/note and want to
        # render the appropriate expression and text.
        # NOTE: CALLS REDRAW
        STATE_JMATCH = 1

        # currently MATCHing state. Here, we are matching a phrase, and only
        # care if we miss something. No rendering adjustment is done in this
        # state
        # NOTE: CALLS REDRAW
        STATE_MATCH = 2

        # MISS state. Here, the user misses a note once. That is okay, but
        # we need to change monika's expression accoridngly.
        # NOTE: CALLS REDRAW
        STATE_MISS = 3

        # FAIL state. Here, the user fails a phrase. In this case, we need
        # to abort matching and head to the CLEAN state, which will fix up
        # Monika's expressions. We also render an expression for Monika
        # NOTE: failure means 2 misses in a row
        # NOTE: CALLS REDRAW
        STATE_FAIL = 4

        # Just POST state. Here, the user just finished a phrase and is now
        # playing the post section of that phrase. POST sections are optional
        # for passing the phrase, but playing them allows smooth transition to
        # the next note phrase.
        # Rendering of the post expression is done here
        # NOTE: CALLS REDRAW
        STATE_JPOST = 5

        # POST state. Here, the user is currently playing the POST note phrase
        # We are matching the POST phrase.
        # No rendering is done here
        # NOTE: CALLS REDRAW
        STATE_POST = 6

        # Visual POST state. This is similiar to the JPOST state, except we
        # only care about visual adjustments. The main difference between this
        # and JPOST is that VPOST leads into the WPOST state, while JPOST leads
        # into the POST state. VPOST also does not handle postnotes.
        # Post expression rendering is done here
        # NOTE: CALLS REDRAW
        STATE_VPOST = 7

        # Clean POST state. This is a special cleanup state that only does
        # visual cleanup instead of total cleanup. Meant to be used with a
        # WPOST that has a visual timeout.
        # Rendering cleanup is done here
        # NOTE: CALLS REDRAW
        STATE_CPOST = 8

        # Wait POST state. This state is a transitional state between note
        # phrases. Here, we wait for user input, and if its appropriate,
        # move to a JMATCH state. This state also calls a redraw using visual
        # redraw_time if available.
        # No Rendering is done here
        # NOTE: CALLS REDRAW
        STATE_WPOST = 9

        # CLEAN state. This state resets the display back to Default state as
        # well as resetting the timeouts. This leads into the LISTEN state,
        # so we should only do this if we want to reset.
        # Rendering cleanup is done here
        STATE_CLEAN = 10 # reset things

        # DONE state. This state is entered when we are done with the song
        # and we should wait for some time then quit.
        # NOTE: CALLS REDRAW
        STATE_DONE = 11

        # Just Done POST state. This is simliar to the JPOST state except
        # we can timeout visually and quit the game.
        # NOTE: CALLS REDRAW
        STATE_DJPOST = 12

        # Done POST state. This is similiar to the POST state except we can
        # timeout visually and quit hte game.
        # NOTE: CALLS REDRAW
        STATE_DPOST = 13

        # Wait DONE state. This is for allowing a wait period after the song
        # is completed. Leads into DONE state.
        # NOTE: CALLS REDRAW
        STATE_WDONE = 14

        # TUPLE state groups. This for easier checking of states
        # States related to Done flow
        DONE_STATES = (
            STATE_DPOST,
            STATE_WDONE,
            STATE_DJPOST,
            STATE_DONE
        )

        # States related to post flow
        POST_STATES = (
            STATE_POST,
            STATE_JPOST,
            STATE_DPOST,
            STATE_DJPOST
        )

        # states related to transitional post flow
        TRANS_POST_STATES = (
            STATE_WPOST,
            STATE_CPOST,
            STATE_VPOST
        )

        # states related to matches
        MATCH_STATES = (
            STATE_MATCH,
            STATE_MISS,
            STATE_JMATCH
        )

        # timeout states for matches
        TOUT_MATCH_STATES = (
            STATE_MATCH,
            STATE_MISS,
            STATE_JMATCH,
            STATE_FAIL
        )

        # timeout states for posts
        TOUT_POST_STATES = (
            STATE_POST,
            STATE_JPOST
        )

        # render states for done
        REND_DONE_STATES = (
            STATE_WDONE,
            STATE_DPOST,
            STATE_DONE
        )

        # done states that mean we should quit
        FINAL_DONE_STATES = (
            STATE_DONE,
            STATE_WDONE
        )

        # key limit for matching
        KEY_LIMIT = 100

        # filenames
        ZZFP_F4 =  "mod_assets/sounds/piano_keys/F4.ogg"
        ZZFP_F4SH = "mod_assets/sounds/piano_keys/F4sh.ogg"
        ZZFP_G4 = "mod_assets/sounds/piano_keys/G4.ogg"
        ZZFP_G4SH = "mod_assets/sounds/piano_keys/G4sh.ogg"
        ZZFP_A4 = "mod_assets/sounds/piano_keys/A4.ogg"
        ZZFP_A4SH = "mod_assets/sounds/piano_keys/A4sh.ogg"
        ZZFP_B4 = "mod_assets/sounds/piano_keys/B4.ogg"
        ZZFP_C5 = "mod_assets/sounds/piano_keys/C5.ogg"
        ZZFP_C5SH = "mod_assets/sounds/piano_keys/C5sh.ogg"
        ZZFP_D5 = "mod_assets/sounds/piano_keys/D5.ogg"
        ZZFP_D5SH = "mod_assets/sounds/piano_keys/D5sh.ogg"
        ZZFP_E5 = "mod_assets/sounds/piano_keys/E5.ogg"
        ZZFP_F5 = "mod_assets/sounds/piano_keys/F5.ogg"
        ZZFP_F5SH = "mod_assets/sounds/piano_keys/F5sh.ogg"
        ZZFP_G5 = "mod_assets/sounds/piano_keys/G5.ogg"
        ZZFP_G5SH = "mod_assets/sounds/piano_keys/G5sh.ogg"
        ZZFP_A5 = "mod_assets/sounds/piano_keys/A5.ogg"
        ZZFP_A5SH = "mod_assets/sounds/piano_keys/A5sh.ogg"
        ZZFP_B5 = "mod_assets/sounds/piano_keys/B5.ogg"
        ZZFP_C6 = "mod_assets/sounds/piano_keys/C6.ogg"

        # piano images
        ZZPK_IMG_BACK = "mod_assets/piano/board.png"
        ZZPK_IMG_KEYS = "mod_assets/piano/piano.png"

        # lyrical bar
        ZZPK_LYR_BAR = "mod_assets/piano/lyrical_bar.png"

        # overlay, white
        ZZPK_W_OVL_LEFT = "mod_assets/piano/ovl/ivory_left.png"
        ZZPK_W_OVL_RIGHT = "mod_assets/piano/ovl/ivory_right.png"
        ZZPK_W_OVL_CENTER = "mod_assets/piano/ovl/ivory_center.png"
        ZZPK_W_OVL_PLAIN = "mod_assets/piano/ovl/ivory_plain.png"

        # overlay black
        ZZPK_B_OVL_PLAIN = "mod_assets/piano/ovl/ebony.png"

        # offsets for rendering
        ZZPK_IMG_BACK_X = 5
        ZZPK_IMG_BACK_Y = 10
        ZZPK_IMG_KEYS_X = 51
        ZZPK_IMG_KEYS_Y = 50
        ZZPK_LYR_BAR_YOFF = -50

        # other sizes
        ZZPK_IMG_IKEY_WIDTH = 36
        ZZPK_IMG_IKEY_HEIGHT = 214
        ZZPK_IMG_EKEY_WIDTH = 29
        ZZPK_IMG_EKEY_HEIGHT = 152

        # MODES
        MODE_FREE = 0
        MODE_SONG = 1 # song mode means we are trying to play a song

        def __init__(self, mode, pnml=None):
            """
            Creates the piano displablable

            IN:
                mode - the mode we want to be in
                pnml - the piano note match list we want to use
                    (Default: None)
            """
            super(renpy.Displayable,self).__init__()

            # current mode
            self.mode = mode

            # setup images

            # background piano
            self.piano_back = Image(self.ZZPK_IMG_BACK)
            self.piano_keys = Image(self.ZZPK_IMG_KEYS)
            self.PIANO_BACK_WIDTH = 437
            self.PIANO_BACK_HEIGHT = 214

            # lyric bar
            self.lyrical_bar = Image(self.ZZPK_LYR_BAR)

            # setup sounds
            # sound dict:
            self.pkeys = {
                zzpianokeys.F4: self.ZZFP_F4,
                zzpianokeys.F4SH: self.ZZFP_F4SH,
                zzpianokeys.G4: self.ZZFP_G4,
                zzpianokeys.G4SH: self.ZZFP_G4SH,
                zzpianokeys.A4: self.ZZFP_A4,
                zzpianokeys.A4SH: self.ZZFP_A4SH,
                zzpianokeys.B4: self.ZZFP_B4,
                zzpianokeys.C5: self.ZZFP_C5,
                zzpianokeys.C5SH: self.ZZFP_C5SH,
                zzpianokeys.D5: self.ZZFP_D5,
                zzpianokeys.D5SH: self.ZZFP_D5SH,
                zzpianokeys.E5: self.ZZFP_E5,
                zzpianokeys.F5: self.ZZFP_F5,
                zzpianokeys.F5SH: self.ZZFP_F5SH,
                zzpianokeys.G5: self.ZZFP_G5,
                zzpianokeys.G5SH: self.ZZFP_G5SH,
                zzpianokeys.A5: self.ZZFP_A5,
                zzpianokeys.A5SH: self.ZZFP_A5SH,
                zzpianokeys.B5: self.ZZFP_B5,
                zzpianokeys.C6: self.ZZFP_C6
            }

            # pressed dict
            self.pressed = {
                zzpianokeys.F4: False,
                zzpianokeys.F4SH: False,
                zzpianokeys.G4: False,
                zzpianokeys.G4SH: False,
                zzpianokeys.A4: False,
                zzpianokeys.A4SH: False,
                zzpianokeys.B4: False,
                zzpianokeys.C5: False,
                zzpianokeys.C5SH: False,
                zzpianokeys.D5: False,
                zzpianokeys.D5SH: False,
                zzpianokeys.E5: False,
                zzpianokeys.F5: False,
                zzpianokeys.F5SH: False,
                zzpianokeys.G5: False,
                zzpianokeys.G5SH: False,
                zzpianokeys.A5: False,
                zzpianokeys.A5SH: False,
                zzpianokeys.B5: False,
                zzpianokeys.C6: False
            }

            # overlay setup
            left = Image(self.ZZPK_W_OVL_LEFT)
            right = Image(self.ZZPK_W_OVL_RIGHT)
            center = Image(self.ZZPK_W_OVL_CENTER)
            w_plain = Image(self.ZZPK_W_OVL_PLAIN)
            whites = [
                (zzpianokeys.F4, left),
                (zzpianokeys.G4, center),
                (zzpianokeys.A4, center),
                (zzpianokeys.B4, right),
                (zzpianokeys.C5, left),
                (zzpianokeys.D5, center),
                (zzpianokeys.E5, right),
                (zzpianokeys.F5, left),
                (zzpianokeys.G5, center),
                (zzpianokeys.A5, center),
                (zzpianokeys.B5, right),
                (zzpianokeys.C6, w_plain),
            ]

            # key, x coord
            # NOTE: this is differente because black keys are not separated
            # equally
            b_plain = Image(self.ZZPK_B_OVL_PLAIN)
            blacks = [
                (zzpianokeys.F4SH, 73),
                (zzpianokeys.G4SH, 110),
                (zzpianokeys.A4SH, 147),
                (zzpianokeys.C5SH, 221),
                (zzpianokeys.D5SH, 258),
                (zzpianokeys.F5SH, 332),
                (zzpianokeys.G5SH, 369),
                (zzpianokeys.A5SH, 406)
            ]

            # overlay dict
            # NOTE: x and y are assumed to be relative to the top let of
            #   the piano_back image
            # (overlay image, x coord, y coord)
            self.overlays = dict()

            # white overlay processing
            for i in range(0,len(whites)):
                k,img = whites[i]
                self.overlays[k] = (
                    img,
                    self.ZZPK_IMG_KEYS_X + (i * (self.ZZPK_IMG_IKEY_WIDTH + 1)),
                    self.ZZPK_IMG_KEYS_Y
                )

            # blacks overlay processing
            for k,x in blacks:
                self.overlays[k] = (
                    b_plain,
                    x,
                    self.ZZPK_IMG_KEYS_Y
                )


            # list containing lists of matches.
            # NOTE: highly recommend not adding too many detections
            self.pnml_list = []
            if self.mode == self.MODE_FREE:
                self.pnml_list = [
                    zzpianokeys.pnml_db[k] for k in zzpianokeys.pnml_db
                    if zzpianokeys.pnml_db[k].wins == 0
                ]

            # list of notes we have played
            self.played = list()
            self.prev_time = 0
            self.drawn_time = 0

            # currently matched dialogue
            self.match = None

            # True if we literally just matched, False if not
            self.justmatched = False

            # true only if we had a missed match, after a match
            self.missed_one = False

            # contains the previously matched pnm
            self.lastmatch = None

            # true if we failed the last match
            # NOTE: this should be reset by timeout, also when match is found
            self.failed = False

            # NOTE: the current state
            self.state = self.STATE_LISTEN

            # currently visible text
            self.lyric = None

            # what index of piano matching should we be looking at
            self.pnm_index = 0

            # timeouts
            self.ev_timeout = self.TIMEOUT
            self.vis_timeout = self.VIS_TIMEOUT

            # current verse
            self.versedex = 0

            # current note match list
            self.pnml = pnml

            # song mode has a lot of things
            if self.mode == self.MODE_SONG:
                self.pnml.resetPNM()
                self.match = self.pnml.pnm_list[0]
                self.setsongmode(True)

            # did player hit a note
            self.note_hit = False

            # integer to handle redraw calls.
            # NOTE: when we want to redraw, we add to this value. Render
            # decrements the value by 1 whenever it runs.
            # NOTE: Render cannot call redraws unless this value is 0.
            # NOTE: similar to semaphores, but not entirely the same.
            # Semaphores are about locking the access of something to a certain
            # number of threads (usually 1) by subracting/adding a value.
            # here we use that concept to limit the amount of rescursive redraw
            # calls
            # NOTE: we actually dont need this becaues of how renpy handles
            # its own custom events
#            self.redraw_count = 0

            # DEBUG: NOTE:
#            self.testing = open("piano", "w+")


#        def customRedraw(self, timeout, from_render=False):
#            """
#            Custom redraw function that wraps around the actual redraw call.
#            This version increments the redraw_count value appropraitelyl
#            as well as call redraw itself.
#            In addition, if we are calling fromt he render function, we check
#            if redraw_count is 0 before calling redraw
#
#            IN:
#                timeout - the amount of time to pass into the redraw call.
#                from_render - True if this is called from the render function,
#                    False otherwise
#                    (Default: False)
#            """
#            self.testing.write(str(self.redraw_count) + "\n")
#            if from_render:
#                if self.redraw_count == 0:
#                    self.redraw_count += 1
#                    renpy.redraw(self, timeout)
#            else:
#                self.redraw_count += 1
#                renpy.redraw(self, timeout)


        def findnotematch(self, notes):
            #
            # Finds a PianoNoteMatch object that matches the given set of
            # notes.
            # Also sets the pnml to the piano note match list that is
            # appropriate
            # NOTE: only the first notematch phrase is checked per note match
            #   list.
            #
            # IN:
            #   notes - list of notes to match
            #
            # RETURNS:
            #   PianoNoteMatch object that matches, or None if no match

            # convert to string for ease of us
            notestr = "".join([chr(x) for x in notes])

            # go through the pnm_list
            for pnml in self.pnml_list:
                pnm = pnml.pnm_list[0]

                # use string finding to match stuff
                findex = pnm.notestr.find(notestr)
                if findex >= 0:
                    pnm.matchdex = findex + len(notestr)
                    pnm.matched = True
                    self.pnm_index = 0
                    self.pnml = pnml # curreent song
                    self.mode = self.MODE_SONG # we are locked into song mode
                    return pnm

            return None

        def getnotematch(self, index=None):
            #
            # returns the notematch object at the given index
            #
            # IN:
            #   index - the index to retrieve notematch.
            #       If None, the self.pnm_index is incremeneted and used as
            #       the index
            #
            # OUT:
            #   returns PianoNoteMatch object at index, or None if index is
            #   beyond the grave

            if index is None:
                self.pnm_index += 1
                index = self.pnm_index

            if index >= len(self.pnml.pnm_list):
                return None

            new_pnm = self.pnml.pnm_list[index]

            # settting up the proper next verse
#            if self.versedex != new_pnm.verse:
#                self.versedex = new_pnm.verse

            return new_pnm

        def quitflow(self):
            """
            Quits the game and does the appropriate processing.

            RETURNS:
                tuple of the following format:
                    [0]: true if full_combo, False if not
                    [1]: true if won, false if not
                    [2]: true if both passes and misses are greater than 0
                        (which is like practicing)
                    [3]: label to call next (like post game dialogue)
            """
            # process this game
            passes = 0
            fails = 0
            misses = 0
            full_combo = False
            is_win = False
            is_prac = False
            end_label = None
            completed_pnms = 0

            if not self.note_hit:
                end_label = "zz_piano_none"

            elif self.pnml:
                full_combo = True

                # grab all this data
                for pnm  in self.pnml.pnm_list:
                    passes += pnm.passes
                    fails += pnm.fails
                    misses += pnm.misses

                    if pnm.passes > 0:
                        completed_pnms += 1

                    if pnm.misses > 0 or pnm.fails > 0 or pnm.passes == 0:
                        full_combo = False

                if full_combo:
                    end_label = self.pnml.fc_label
                    self.pnml.full_combos += 1
                    self.pnml.wins += 1
                    is_win = True

                # fail case
                elif (completed_pnms != len(self.pnml.pnm_list)
                        and fails > passes
                    ):
                    end_label = self.pnml.fail_label
                    self.pnml.losses += 1

                # compelted everything, nut a ful combo though
                elif completed_pnms == len(self.pnml.pnm_list):
                    end_label = self.pnml.win_label
                    self.pnml.wins += 1
                    is_win = True

                # otherwise, assume practice mode
                else:
                    end_label = self.pnml.prac_label
                    is_prac = True

            else:
                end_label = "zz_piano_default"

            # finally return the tuple
            return (
                full_combo,
                is_win,
                is_prac,
                end_label
            )


        def resetVerse(self):
            """
            Resets the current match back to its verse start.
            """
            # we can only reset if we have a match
            if self.match:
                self.pnm_index = self.match.verse
                self.match = self.getnotematch(self.pnm_index)


        def setsongmode(self, songmode=True, ev_tout=None, vis_tout=None):
            #
            # sets our timeout vars into song mode
            #
            # IN:
            #   songmode - True means set into song mode, False means get out
            #       (Default: True)
            #   ev_tout - use a custom ev timeout for song mode
            #       (Default: None)
            #   vis_tout - use a custom vis timeout for song mode
            #       (Default: None)

            if songmode:

                if ev_tout:
                    self.ev_timeout = ev_tout
                else:
                    self.ev_timeout = self.SONG_TIMEOUT

                if vis_tout:
                    self.vis_timeout = vis_tout
                else:
                    self.vis_timeout = self.SONG_VIS_TIMEOUT
            else:
                self.ev_timeout = self.TIMEOUT
                self.vis_timeout = self.VIS_TIMEOUT


        def stateListen(self, ev):
            """
            Flow that occurs when we in listen state

            IN:
                ev - pygame event that occured

            STATES:
                STATE_LISTEN
            """
            # check if we are in song mode
            if self.mode == self.MODE_SONG:

                # find a match
                findex = self.match.isNoteMatch(ev.key, 0)

                if findex >= 0:
                    self.state = self.STATE_JMATCH

            # not in song mode, check for correct number of
            # notes
            elif len(self.played) >= zzpianokeys.NOTE_SIZE:

                # find a match
                self.match = self.findnotematch(self.played)

                # check if match
                if self.match:
                    self.state = self.STATE_JMATCH


        def stateMatch(self, ev):
            """
            Flow that occurs when we are matching notes

            IN:
                ev - pygame event that occured

            STATES:
                STATE_MATCH
                STATE_MISS
                STATE_JMATCH
            """
            # we have a match, check to ensure that this key
            # follows the pattern
            findex = self.match.isNoteMatch(ev.key)

            # failed match
            if findex < 0:

                # -1 is a non match
                if findex == -1:

                    # check for a double failure, which means
                    # we failed entirely on playing this piece
                    if self.state == self.STATE_MISS:
                        self.match.fails += 1
                        self.state = self.STATE_FAIL

                        # incase of a double failure, we zero
                        # the list and the prev time
                        # self.played = [ev.key]
                        self.played = list()

                        # clear the match
#                                       self.lastmatch = None
#                                       self.match = None

                    # this is our first failure, just take note
                    else:
                        self.match.misses += 1
                        self.state = self.STATE_MISS

            # otherwise, we matched, but need to clear fails
            else:

                # check for finished notes
                if self.match.matchdex == len(self.match.notes):

                    # you passed
                    self.match.passes += 1

                    # post notes flow
                    if self.match.postnotes:

                        # check if we have anymore notes
                        if self.getnotematch(self.pnm_index+1):
                            self.state = self.STATE_JPOST
                        else:
                            self.state = self.STATE_DJPOST

                        self.match.matchdex = 0
                        self.played = list()

                    # next pnm match
                    else:
                        next_pnm = self.getnotematch()

                        if next_pnm:

                            self.lastmatch = self.match
                            self.match = next_pnm
                            self.state = self.STATE_VPOST
                            self.setsongmode(
                                ev_tout=next_pnm.ev_timeout,
                                vis_tout=self.lastmatch.vis_timeout
                            )
                            self.match.matchdex = 0
                            self.played = list()

                        # no more matches, we are done
                        else:
                            self.state = self.STATE_WDONE

                else:
                    self.state = self.STATE_MATCH


        def statePost(self, ev):
            """
            Flow that occurs when we are post matching notes

            IN:
                ev - pygame event that occured

            STATES:
                STATE_POST
                STATE_JPOST
                STATE_DPOST
                STATE_DJPOST
            """
            # post match means we abort on the first miss
            findex = self.match.isPostMatch(ev.key)

            # check for a match
            if findex == -1:

                next_pnm = self.getnotematch()

                # check next set of notes
                if next_pnm:

                    if next_pnm.isNoteMatch(ev.key, 0) >= 0:
                        # match found
                        self.state = self.STATE_JMATCH

                    else:
                        # not a match, but move to next
                        # pnm anyway
                        self.state = self.STATE_WPOST
                        next_pnm.matchdex = 0
                        self.setsongmode(
                            ev_tout=next_pnm.ev_timeout,
                            vis_tout=self.match.vis_timeout
                        )

                    self.match = next_pnm
                    self.played = [ev.key]

                # completed this song
                else:
                    self.state = self.STATE_WDONE

            # finished post complete
            elif self.match.matchdex == len(self.match.postnotes):

                next_pnm = self.getnotematch()

                # check next set of notes
                if next_pnm:

                    self.played = list()
                    next_pnm.matchdex = 0
                    self.setsongmode(
                        ev_tout=next_pnm.ev_timeout,
                        vis_tout=self.match.vis_timeout
                    )
                    self.match = next_pnm
                    self.state = self.STATE_WPOST

                # no next set of notes, you've played this
                # song completel
                else:
                    self.state = self.STATE_WDONE


        def stateWaitPost(self, ev):
            """
            Flow that occurs when we are in a transitional phase from a note
            match to another

            IN:
                ev - pygame event that occured

            STATES:
                STATE_WPOST
                STATE_CPOST
                STATE_VPOST
            """
            # here we check the just hit note for matching
            findex = self.match.isNoteMatch(ev.key, index=0)

            if findex > 0:
                self.state = self.STATE_JMATCH

            else:
                # missed the note, so take us back to verse
                # start
                self.state = self.STATE_CLEAN
                self.played = [ev.key]


        def render(self, width, height, st, at):
            # renpy render function
            # NOTE: Displayables are EVENT-DRIVEN

            r = renpy.Render(width, height)

            # prepare piano back as render
            back = renpy.render(self.piano_back, 1280, 720, st, at)
            piano = renpy.render(self.piano_keys, 1280, 720, st, at)


            # now prepare overlays to render
            overlays = list()
            for k in self.pressed:
                if self.pressed[k]:
                    overlays.append(
                        (
                            renpy.render(self.overlays[k][0], 1280, 720, st, at),
                            self.overlays[k][1],
                            self.overlays[k][2]
                        )
                    )

            # Draw the piano
            r.blit(
                back,
                (
                    self.ZZPK_IMG_BACK_X,
                    self.ZZPK_IMG_BACK_Y
                )
            )
            r.blit(
                piano,
                (
                    self.ZZPK_IMG_KEYS_X + self.ZZPK_IMG_BACK_X,
                    self.ZZPK_IMG_KEYS_Y + self.ZZPK_IMG_BACK_Y
                )
            )

            # and now the overlays
            for ovl in overlays:
                r.blit(
                    ovl[0],
                    (
                        self.ZZPK_IMG_BACK_X + ovl[1],
                        self.ZZPK_IMG_BACK_Y + ovl[2]
                    )
                )

            # True if we need to do an interaction restart
            restart_int = False

            # True if we already called a redraw
            redrawn = False

            # subtract a redraw count for every render
#            if self.redraw_count > 0:
#                self.redraw_count -= 1

            # check if we are currently matching something
            # NOTE: the following utilizies renpy.show, which means we need
            #   to use renpy.restart_interaction(). This also means that the
            #   changes that occur here shouldnt be rendered
            # STATE MACHINE
            if self.state in self.DONE_STATES:

                if self.state == self.STATE_DJPOST:
                    # display monikas post expression
                    renpy.show(self.match.postexpress)

                    # hide text
                    if not self.match.posttext:
                        self.lyric = None

                    restart_int = True

                    # we go to DPOST instead of POST
                    self.state = self.STATE_DPOST

                    # force a redraw
                    renpy.redraw(self, self.vis_timeout)

                # check for visual timeout
                elif st-self.prev_time >= self.vis_timeout:

                    # force event call
                    self.state = self.STATE_DONE
                    renpy.timeout(1.0)
#                    renpy.redraw(self, 1.0)
#                    redrawn = True

                # do a redraw for the next timeout
                else:
                    renpy.redraw(self, self.vis_timeout)
#                    redrawn = True

            elif (
                    self.state == self.STATE_CLEAN
                    or st-self.prev_time >= self.ev_timeout
                ):

                # default monika
                renpy.show(self.DEFAULT)

                # hide text
                self.lyric = None

                restart_int = True

                if self.state not in self.DONE_STATES:
                    self.state = self.STATE_LISTEN
                    self.resetVerse()
                self.setsongmode(False)

            elif self.state != self.STATE_LISTEN:

                if self.state == self.STATE_JMATCH:

                    # display monika's expression
                    renpy.show(self.match.express)

                    # display text
                    self.lyric = self.match.say

                    # set song mode
                    self.setsongmode(vis_tout=self.match.vis_timeout)

                    restart_int = True
                    self.state = self.STATE_MATCH

                elif self.state == self.STATE_MISS:

                    # display an awkward expresseion monika
                    renpy.show(self.AWKWARD)
                    restart_int = True

                elif self.state == self.STATE_VPOST:

                    # display the post expression
                    renpy.show(self.lastmatch.postexpress)
                    restart_int = True

                    # hide text
                    if not self.lastmatch.posttext:
                        self.lyric = None

                    # setup visual timeout
                    if self.lastmatch.vis_timeout:
#                        self.customRedraw(
#                            self.lastmatch.redraw_time,
#                            from_render=True
#                        )
                        renpy.redraw(self, self.lastmatch.vis_timeout)
                        self.drawn_time = st
                        self.state = self.STATE_CPOST
                        redrawn = True

                    else:
                        self.state = self.STATE_WPOST

                elif self.state == self.STATE_CPOST:

                    # check if timeout
                    if st-self.drawn_time >= self.lastmatch.vis_timeout:

                        # display default monika
                        renpy.show(self.DEFAULT)

                        # hide text
                        self.lyric = None

                        restart_int = True
                        self.state = self.STATE_WPOST

                    # force a redraw in a second
                    else:
#                        self.customRedraw(1.0, from_render=True)
                        renpy.redraw(self, 1.0)
                        redrawn = True

                elif self.state == self.STATE_JPOST:

                    # display monikas post expression
                    renpy.show(self.match.postexpress)

                    # hide text
                    if not self.match.posttext:
                        self.lyric = None

                    restart_int = True
                    self.state = self.STATE_POST

                elif self.state == self.STATE_FAIL:

                    # display failed monika
                    renpy.show(self.FAILED)

                    # hide text
                    self.lyric = None

                    restart_int = True
                    self.state = self.STATE_CLEAN

                # redraw timeout
                if not redrawn:
                    renpy.redraw(self, self.vis_timeout)
#                    self.customRedraw(self.vis_timeout, from_render=True)

            if self.lyric:
                lyric_bar = renpy.render(self.lyrical_bar, 1280, 720, st, at)
                lyric = renpy.render(self.lyric, 1280, 720, st, at)
                pw, ph = lyric.get_size()

                # the lyric bar should be slightly below y-center
                r.blit(
                    lyric_bar,
                    (
                        0,
                        int((height - 50) /2) - self.ZZPK_LYR_BAR_YOFF
                    )
                )
                r.blit(
                    lyric,
                    (
                        int((width - pw) / 2),
                        int((height - ph) / 2) - self.ZZPK_LYR_BAR_YOFF
                    )
                )

#                    renpy.show(
#                        "monika " + match.express,
#                        at_list=self.AT_LIST,
#                        zorder=10,
#                        layer="transient"
#                    )
#                    renpy.force_full_redraw()
#                    r.blit(
#                        renpy.render(match.img, 1280, 720, st, at),
#                        (0, 0)
#                    )
#                    renpy.say(m, match.say, interact=False)
#                    renpy.force_full_redraw()

            if restart_int:
                renpy.restart_interaction()

            # rerender redrawing thing
            # renpy.redraw(self, 0)

            # and apparenly we return the render object
            return r

        def event(self, ev, x, y, st):
            # renpy event handler
            # NOTE: Renpy is EVENT-DRIVEN

            # DONE state means you immediate quit
            if self.state in self.FINAL_DONE_STATES:
                return self.quitflow()

            # when you press down a key, we launch a sound
            if ev.type == pygame.KEYDOWN:

                if len(self.played) > self.KEY_LIMIT:
                    self.played = list()

                # we only care about keydown events regarding timeout
                elif st-self.prev_time >= self.ev_timeout:

#                    self.testing.write("".join([chr(x) for x in self.played])+ "\n")
                    self.played = list()

                    # NOTE: in the listen state,  timeout means restart
                    # the played list (which is what handles the note
                    # matchin). Keep state.

                    # NOTE: in transitional post states, timeout means
                    # continue waiting.
                    # Keep state.

                    # NOTE: in done related states, timeout means quit
                    # the game.
                    if self.state in self.DONE_STATES:
                        return self.quitflow()

                    # NOTE: in the match-related states, timeout means
                    # they failed the expression.
                    elif self.state in self.TOUT_MATCH_STATES:
                        self.resetVerse()
                        self.state = self.STATE_LISTEN

                    # NOTE: in post-match related states, timeout means
                    # move onto the next expression.
                    elif self.state in self.TOUT_POST_STATES:
                        next_pnm = self.getnotematch()

                        if next_pnm:
                            self.setsongmode(
                                ev_tout=next_pnm.ev_timeout,
                                vis_tout=self.match.vis_timeout
                            )
                            self.state = self.STATE_WPOST
                            self.match = next_pnm
                            self.match.matchdex = 0

                        # no more matches, we are done
                        else:
                            self.state = self.STATE_WDONE

                    # NOTE: in clean state, chnage state to listen.
                    elif self.state == self.STATE_CLEAN:
                        self.state = self.STATE_LISTEN

#   DEBUG: NOTE:
#                if self.match:
#                    self.testing.write(
#                        chr(ev.key) + " : " + str(self.state) + " : " +
#                        str(self.match.matchdex) + "\n")
#                else:
#                    self.testing.write(chr(ev.key) + " : " + str(self.state) + "\n")

                # setup previous time thing
                self.prev_time = st

                # but first, check for quit ("Z")
                if ev.key == zzpianokeys.QUIT:
                    return self.quitflow()
                else:

                    # only play a sound if we've lifted the finger
                    if not self.pressed.get(ev.key, True):

                        # note has been hit
                        self.note_hit = True

                        # add to played
                        self.played.append(ev.key)

                        # set appropriate value
                        self.pressed[ev.key] = True

                        # check if we have enough played notes
                        if self.state == self.STATE_LISTEN:
                            self.stateListen(ev)

                        # post match checking
                        elif self.state in self.POST_STATES:
                            self.statePost(ev)

                        # waiting post
                        elif self.state in self.TRANS_POST_STATES:
                            self.stateWaitPost(ev)

                        # match
                        elif self.state in self.MATCH_STATES:
                            self.stateMatch(ev)

                        # get a sound to play
                        renpy.play(self.pkeys[ev.key], channel="audio")

                        # now rerender
#                        self.customRedraw(0)
                        renpy.redraw(self, 0)

            # keyup, means we should stop render
            elif ev.type == pygame.KEYUP:

                # only do this if we keyup a key we care about
                if self.pressed.get(ev.key, False):

                    # set appropriate value
                    self.pressed[ev.key] = False

                    # now rerender
#                    self.customRedraw(0)
                    renpy.redraw(self, 0)

            # time event, rerender
            elif ev.type == renpy.display.core.TIMEEVENT:
#                self.customRedraw(0)
                renpy.redraw(self, 0)

            # the default so we can keep going
            raise renpy.IgnoreEvent()
