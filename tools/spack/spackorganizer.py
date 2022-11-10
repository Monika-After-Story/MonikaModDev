# organizes spritepacks (or regular sprites)
#
# VER: python 3.9.10

import os

from typing import Optional

import menutils3 as menutils
import toolscache


from spack.spack import Spack, SpackType, MOD_ASSETS,\
    SpackStructureType, SpackConversion
from spack.spackio import SpackLoader, SpackWriter
from spack.spackdb import SpackDB, SpackDBFilterCriteria


CACHE_PATH = "spackorganizer-last-path"


def conv_new(loaded_spacks: SpackLoader):
    """
    Convert spack to new version
    """
    conv(
        loaded_spacks,
        SpackDBFilterCriteria(
            types=[SpackType.ACS, SpackType.HAIR],
            struct_types=[SpackStructureType.FILES]
        ),
        "Folder"
    )


def conv_old(loaded_spacks: SpackLoader):
    """
    Convert spack to old version
    """
    conv(
        loaded_spacks,
        SpackDBFilterCriteria(
            types=[SpackType.ACS, SpackType.HAIR],
            struct_types=[SpackStructureType.FOLDER]
        ),
        "Files"
    )


def conv(
        loaded_spacks: SpackLoader,
        filter_criteria: SpackDBFilterCriteria,
        conv_name: str
):
    """
    Shared conversion code
    :param loaded_spacks: loaded spacks
    :param filter_criteria: filter criteria
    :param conv_name: name for conversion (display)
    """
    spacks = spack_select(loaded_spacks, False, filter_criteria=filter_criteria)
    if not spacks:
        return

    # generate conversions
    conv_data = []

    for spack in spacks:

        spack_conv = SpackConversion(spack)

        if not spack_conv.is_valid:
            print("unable to convert spack: {0}".format(spack_conv.exception))
            menutils.e_pause()
            return

        json_file = loaded_spacks.spack_db.spacks_json.get_file(spack.as_img_sit_type())

        conv_data.append((spack_conv, json_file))

    # ask to use git or not
    print()
    use_git = menutils.ask("Use git mv instead of move", def_no=True)

    # final confirmation
    menutils.clear_screen()
    print("Converting following spacks to {0}".format(conv_name))
    for spack_conv, json_file in conv_data:

        if json_file:
            json_desc = os.path.split(json_file)[1]
        else:
            json_desc = "No JSON to update"

        print("\t{0} | JSON: {1}".format(spack_conv.src_spack.img_sit, json_desc))

    print()
    print("Using git mv to move: {0}".format(use_git))
    print()
    if not menutils.ask_continue():
        print("Aborting...")
        menutils.e_pause()
        return

    # apply conversion
    print("Converting...")
    for spack_conv, json_file in conv_data:
        print("\t{0}...".format(spack_conv.src_spack.img_sit), end="")
        SpackWriter.apply_conversion(
            loaded_spacks.ma_folder_path,
            spack_conv,
            use_git,
            loaded_spacks.spack_db.spacks_json
        )
        print("done!")

    print("if no error occured, conversion probably complete!")
    loaded_spacks.reload()
    menutils.e_pause()


def show_list(loaded_spacks: SpackLoader):
    """
    Shows list of spacks
    """
    # check for types
    spack_types_with_data = loaded_spacks.spack_db.get_types()

    if not spack_types_with_data:
        print("no spritepacks found!")
        menutils.e_pause()
        return

    # request user to pick a type
    spack_type_menu = [
        ("Show Spacks", "Spack Type: "),
        ("Show All", loaded_spacks.spack_db.get_types()),
    ]
    for spack_type in spack_types_with_data:
        spack_type_menu.append((spack_type.display_name, [spack_type]))

    choice = True
    while choice is not None:
        choice = menutils.menu(spack_type_menu, defindex=1)

        if choice is not None:
            spack_select_list(
                loaded_spacks,
                SpackDBFilterCriteria(types=choice)
            )
            return


def show_files(loaded_spacks: SpackLoader):
    """
    Shows files assocaited with spack
    """
    # ask for spack
    spack = spack_select(loaded_spacks, True)
    if not spack:
        return

    # show files for the spack
    spack = spack[0]
    menutils.paginate(
        "Files for {0}".format(spack.img_sit),
        spack.menu_file_list()
    )


def spack_select(
        loaded_spacks: SpackLoader,
        select_one: bool,
        filter_criteria: SpackDBFilterCriteria = None
) -> Optional[list[Spack]]:
    """
    Selects a spack, with options to use entry or page select
    :param loaded_spacks: spackloader data
    :param select_one: true to only select 1
    :param filter_criteria: filter criteria to use for the spacks
    :returns: list of selected Spacks or None if not selected
    """
    selected_spacks = []

    choice = True
    while choice is not None:
        menu = [
            ("Select Spack(s)", "Option: "),
            ("Enter Spack ID (img_sit)", 1),
            ("Select From List", 2),
            ("Select All Spacks", 3),
        ]

        if selected_spacks:
            menu.append(("Confirm Selections", 4))
            def_index = 4
        else:
            def_index = None

        choice = menutils.menu(menu, defindex=def_index, exit_value=-1)

        spack = None

        if choice == 1:
            spack =  spack_select_enter(
                loaded_spacks,
                filter_criteria=filter_criteria
            )

        elif choice == 2:
            spack = spack_select_list(
                loaded_spacks,
                filter_criteria=filter_criteria,
                mode=menutils.PaginateMode.SELECT
            )

        elif choice == 3:
            selected_spacks = loaded_spacks.spack_db.get(
                filter_criteria=filter_criteria
            )

        elif choice == 4:
            if menutils.paginate(
                "Selected Spacks",
                selected_spacks,
                str_func=Spack.menustr,
                mode=menutils.PaginateMode.CONFIRM
            ):
                return selected_spacks

        elif choice == -1:
            # exit clicked, confirm if we still have selected
            if selected_spacks:
                if menutils.ask("You have selected spacks, continue returning", def_no=True):
                    return None

            else:
                return None

        if spack:

            if select_one:
                return [spack]

            selected_spacks.append(spack)

    return None

def spack_select_enter(
        loaded_spacks: SpackLoader,
        filter_criteria: SpackDBFilterCriteria = None
) -> Optional[Spack]:
    """
    Select spack via ID
    """
    if filter_criteria:
        filter_criteria = SpackDBFilterCriteria.copy(filter_criteria)
    else:
        filter_criteria = SpackDBFilterCriteria()

    while True:
        spack_id = input("Enter ID (img_sit) of the spack: ")

        if not spack_id: # assume user wanted to quit
            return None

        filter_criteria.ids = [spack_id]
        matching_spacks = loaded_spacks.spack_db.get(filter_criteria=filter_criteria)

        if len(matching_spacks) > 1:
            # select from matching spacks
            selection: Spack = menutils.paginate(
                "Select Spack",
                matching_spacks,
                str_func=Spack.menustr,
                mode=menutils.PaginateMode.SELECT
            )
            if selection is not None:
                return selection

        elif len(matching_spacks) > 0:
            # only 1, default as selection
            return matching_spacks[0]

        else:
            # none found
            print("No Spacks with img_sit '{0}' found.".format(spack_id))


def spack_select_list(
        loaded_spacks: SpackLoader,
        filter_criteria: SpackDBFilterCriteria = None,
        mode: menutils.PaginateMode = menutils.PaginateMode.LIST
) -> Optional[Spack]:
    """
    Select a spack
    :param loaded_spacks: spack loader data to select from
    :param filter_criteria: spack filter criteria to use
    :param mode: paginate mode
    :returns: Spack or NOne if not selecting
    """
    if mode == menutils.PaginateMode.SELECT:
        title = "Select Spack"
    else:
        title = "Found Spacks"

    return menutils.paginate(
        title,
        loaded_spacks.spack_db.get(filter_criteria=filter_criteria),
        str_func=Spack.menustr,
        mode=mode
    )


def run():
    """
    Runs spack organizer
    """
    ma_folder = toolscache.get(CACHE_PATH, "")

    # use previous if possible
    if ma_folder:
        print("Previously entered path: {0}".format(ma_folder))
        new_ma_folder = input("enter new path or blank to reuse this path: ")
        if new_ma_folder:
            ma_folder = new_ma_folder

    else:
        ma_folder = input("enter path to mod assets folder: ")
        if not ma_folder:
            return


    # verify existence + mod assets
    ma_folder = os.path.normcase(ma_folder)

    if not os.access(ma_folder, os.F_OK):
        print("Could not find path: {0}".format(ma_folder))
        menutils.e_pause()
        return

    folders = os.listdir(ma_folder)
    if MOD_ASSETS not in folders:
        print("no mod_assets folder found in '{0}'!".format(ma_folder))
        menutils.e_pause()
        return


    # verify spacks
    loaded_spacks = SpackLoader(os.path.normcase(os.path.join(ma_folder, MOD_ASSETS)))
    toolscache.put(CACHE_PATH, ma_folder)

    if len(loaded_spacks) < 1:
        print("no spacks found in '{0}'!".format(ma_folder))
        menutils.e_pause()
        return


    # build menu
    menu_title = (
        "Spack Organizer ({0}){1}".format(
            ma_folder,
            " - JSONS loaded" if loaded_spacks.spack_db.has_jsons() else ""
        ),
        "Utility: "
    )
    menu_main = [
        menu_title,
        ("Show List of Spacks", show_list),
        ("Show Files in Spack", show_files),
        ("Convert to Folder Structure (New)", conv_new),
        ("Convert to File Structure (Old)", conv_old),
    ]

    choice = True

    while choice is not None:
        choice = menutils.menu(menu_main)

        if choice is not None:
            choice(loaded_spacks)


