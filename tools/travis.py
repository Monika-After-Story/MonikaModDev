## this is for travis to run

# set to True if we are checking sprites for dynamically generated sprites
# False will be standard sprite check behavior
is_dynamic = True

import gamedir as GDIR
GDIR.REL_PATH_GAME = "MonikaModDev/Monika After Story/game/"

import spritechecker as spc
#import spritemaker as spm

# load sprites
#sprite_db = spm._load_sprites()
#sprite_db_keys = sorted(sprite_db.keys())

# generate sprites
#spm.run_gss(sprite_db, sprite_db_keys, quiet=True)

# now check sprites
bad_codes = spc.check_sprites(False, is_dynamic)

if len(bad_codes) > 0:
    for bad_code in bad_codes:
        print(
            spc.BAD_CODE_LN.format(
                bad_code.line,
                bad_code.code,
                bad_code.filename
            )
        )

    if is_dynamic:
        raise Exception(
            "Invalid sprites found. Run sprite checker manually "
            "to find invalid sprites."
        )
    else:
        raise Exception(
            "Invalid sprites found. **Did you forget to generate sprites?**"
        )
