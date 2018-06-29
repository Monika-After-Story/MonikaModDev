## this is for travis to run

import gamedir as GDIR
GDIR.REL_PATH_GAME = "MonikaModDev/Monika After Story/game/"

import spritechecker as spc

bad_codes = spc.check_sprites(False)

if len(bad_codes) > 0:
    for bad_code in bad_list:
        print(
            spc.BAD_CODE_LN.format(
                bad_code.line,
                bad_code.code,
                bad_code.filename
            )
        )

    raise Exception("Invalid sprites found. Run the sprite checker for more info.")
