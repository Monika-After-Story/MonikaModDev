## TODO
## we need a neato menu for everything

import spritepuller

sp_list = spritepuller.pull_sprite_list()

sp_list = [
    code
    for code in sp_list
    if ":" not in code
]

spritepuller.write_spritecodes(sp_list)
spritepuller.write_zz_sprite_opt(sp_list)
