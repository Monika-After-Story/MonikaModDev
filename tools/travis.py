## this is for travis to run

import spritechecker as spc

bad_codes = spc.check_sprites(False)

if len(bad_codes) > 0:
    raise Exception("Invalid sprites found. Run the sprite checker for more info.")
