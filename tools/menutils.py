## module containing constants for menu creation
#
#
# to run a menu, prepare a list of menu entries. Each entry should consist of
# a tuple of the following format:
# [0]: Text to display for this entry
# [1]: return value 
#
# NOTE: the first item of the list should be a tuple of thef ollowing format:
# [0]: Title / header to display
# [1]: Prompt text
#
# the menu generator function (menu) will add an exit / back option 
# automatically. this option always returns None

import os
import platform

HEADER = """\n\n\
#=============================================================================#
#   {: <74}#
#=============================================================================#
"""


MENU_TITLE = "    {0}"
MENU_ENTRY = "    {0}) {1}"
MENU_END = """
   [0] Exit
"""

PAGE_ENTRY = MENU_TITLE
PAGE_GOTO = "(G)oto ): "
PAGE_NEXT = "[N]ext Page"
PAGE_PREV = "(P)revious Page"
PAGE_QUIT = "\n  ( (Q)uit"
PAGE_QUIT_DEF = "\n  ( [Q]uit"
PAGE_BAR = " | "
PAGE_PROG = " - [Page {0}/{1}]"

PAGE_GOTO_PROMPT = "\nEnter a page number [1-{0}]: "

__GOTO = "g"
__NEXT = "n"
__PREV = "p"
__QUIT = "q"


def menu(menu_opts):
    """
    Generates a menu and returns the desired menu action

    IN:
        menu_opts - See above for menu formatting

    RETURNS:
        the selected menu action
    """
    if len(menu_opts) < 2:
        # a menu must consist of header + prompt entry and at least one
        # menu option
        return None

    no_sel = True
    while no_sel:

        # print title
        title, prompt = menu_opts[0]
        #print("\n" + MENU_TITLE.format(title) + "\n")
        #print("\033[H\033[J")
        clear_screen()
        print(HEADER.format(title))

        # print entries
        entries = menu_opts[1:]
        entry_count = 1
        for entry in entries:
            print(MENU_ENTRY.format(entry_count, entry[0]))
            entry_count += 1

        # print footer
        print(MENU_END + "\n")

        # and then prompt!
        user_input = raw_input(prompt)

        # NOTE: if blank, we just quit
        if len(user_input) <= 0:
            return None

        try:
            user_input = int(user_input)

            # okay so userinput is an int
            if 1 <= user_input <= len(entries):
                # and user input is valid, return the result
                return menu_opts[user_input][1]

            elif user_input == 0:
                # user wants to go back
                return None

        except:
            # bad user input
            pass


def paginate(title, items, per_page=20, str_func=str):
    """
    Paginates a list of items. Each item is shown with a tab 4 indent.
    Also runs the paginatation. This returns when the user hits q (quit)

    IN:
        title - title to show at the top of each page
        items - list of items to show
        per_page - number of items to show per page 
            Only accepts values between 10 - 50
            (Default: 20)
        str_func - function to use to convert an item into a string
            (Default: str)
    """
    if len(items) < 1:
        # if there are no items, to show, mention this and then abort
        clear_screen()
        print(header(title))
        print("\nThere are no items to show.\n")
        e_pause()
        return

    def restrict(page_value):
        return max(10, min(page_value, 50))

    # otherwise, we have items
    per_page = restrict(per_page)
    show_pages = True
    page = 0
    last_page = len(items) / per_page
    while show_pages:
        # determine items to show this page
        items_to_show = items[(page*per_page):((page+1) * per_page)]

        # build action bar
        action_bar = []

        # quit can be default
        if page < last_page:
            action_bar.append(PAGE_QUIT)
        else:
            action_bar.append(PAGE_QUIT_DEF)

        if page > 0:
            action_bar.append(PAGE_PREV)

        if page < last_page:
            action_bar.append(PAGE_NEXT)

        action_bar.append(PAGE_GOTO)

        # title
        clear_screen()
        print(header(title + PAGE_PROG.format(page+1, last_page+1)))

        # items
        for item in items_to_show:
            print(PAGE_ENTRY.format(str_func(item)))

        # action string and user input
        user_input = raw_input(PAGE_BAR.join(action_bar)).lower()

        # process user input
        if user_input == __QUIT:
            return

        elif user_input == __PREV:
            if page > 0:
                page -= 1

        elif user_input == __NEXT:
            if page < last_page:
                page += 1

        elif user_input == __GOTO:
            page_input = raw_input(PAGE_GOTO_PROMPT.format(last_page+1))
            try:
                page = int(page_input)-1

            except:
                # bad page input
                pass

        else:
            # otherwise, we do a default action
            if page < last_page:
                # default to next page
                page += 1
            
            else:
                # otherwise, quit
                return


def e_pause():
    """
    Generic enter to continue
    """
    abc = raw_input("\n\n (Press Enter to continue)")


def header(title):
    """
    Returns headerized title
    """
    return HEADER.format(title)


def clear_screen():
    """
    Clears screen.
    NOTE: this is not the recommended way of clearing a screen. Bad results may
    occur on unsupported terminals.
    """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
