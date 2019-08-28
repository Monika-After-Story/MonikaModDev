## this is for travis to run

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
bad_codes = spc.check_sprites(False)

if len(bad_codes) > 0:
    for bad_code in bad_codes:
        print(
            spc.BAD_CODE_LN.format(
                bad_code.line,
                bad_code.code,
                bad_code.filename
            )
        )

    raise Exception("Invalid sprites found. **Did you forget to generate sprites?**")
