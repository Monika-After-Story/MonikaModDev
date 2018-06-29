## this is for travis to run

import gamedir as GDIR
GDIR.REL_PATH_GAME = "MonikaModDev/Monika After Story/game/"

import spritechecker as spc

bad_codes = spc.check_sprites(False)

if len(bad_codes) > 0:
    raise Exception("Invalid sprites found. Run the sprite checker for more info.")
