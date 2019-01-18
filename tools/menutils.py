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

MENU_TITLE = "    {0}"
MENU_ENTRY = "    {0}) {1}"
MENU_END = """
    0) Exit
"""

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
        print("\n" + MENU_TITLE.format(title) + "\n")

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


def e_pause():
    """
    Generic enter to continue
    """
    abc = raw_input("\n\n (Press Enter to continue)")
