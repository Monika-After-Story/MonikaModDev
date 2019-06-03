#### IMAGE START (IMG030)
# Image are created using a DynamicDisplayable to allow for runtime changes
# to sprites without having to remake everything. This saves us on image
# costs.
#
# To create a new image, these parts are required:
#   eyebrows, eyes, nose, mouth (for sitting)
#   head, left, right OR a single image (for standing)
#
# Optional parts for sitting is:
#   sweat, tears, blush, emote, eyebags
#
# Non-leaning poses require an ARMS part.
# leaning poses require a LEAN part.
#
# For more information see mas_drawmonika function
#
#### FOLDER IMAGE RULES: (IMG031)
# To ensure that the images are created correctly, all images must be placed in
# a specific folder heirarchy.
#
# mod_assets/monika/f/<facial expressions>
# mod_assets/monika/c/<clothing types>/<body/arms/poses>
# mod_assets/monika/h/<hair types>
# mod_assets/monika/a/<accessories>
#
# All layers must have a night version, which is denoted using the -n suffix.
# All leaning layers must have a non-leaning fallback
#
## FACIAL EXPRESSIONS:
# Non leaning filenames:
#   face-{face part type}-{face part name}{-n}.png
#   (ie: face-mouth-big.png / face-mouth-big-n.png)
# leaning filenames:
#   face-leaning-{lean type}-{face part type}-{face part name}{-n}.png
#   (ie: face-leaning-eyes-sparkle.png / face-leaning-eyes-sparkle-n.png)
#
## BODY / POSE:
# NEW
# Non leaning:
#   body-def{-n}.png
#   arms-{arms name}{-n}.png
# Leaning:
#   body-leaning-{lean type}{-n}.png
#   arms-leaning-{lean type}-{arms pose}{-n}.png
#
# OLD:
# Non leaning filenames / parts:
#   torso-{hair type}{-n}.png
#   arms-{arms name}{-n}.png
#   (ie: torso-def.png / torso-def-n.png)
#   (ie: arms-def-steepling.png / arms-def-steepling-n.png)
# Leaning filenames:
#   torso-leaning-{hair type}-{lean name}{-n}.png
#   (ie: torso-leaning-def-def.png / torso-leaning-def-def-n.png)
#
## HAIR:
# hair-{hair type}-{front/back}{-n}.png
#

image monika 1cua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="crazy",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfo_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="gasp",
    head="d",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dfp_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="pout",
    head="h",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dft_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="triangle",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dftdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling",
    tears="dried"
)

image monika 1dftsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streamingclosedsad"
)

image monika 1dftsu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="smug",
    tears="streaming",
    head="j",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="wide",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="disgust",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dka_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dkb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dkbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1dkbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="q",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1dkbfsdlb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    blush="full",
    sweat="def",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dkbfu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smug",
    blush="full",
    head="j",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dkbla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines"
)

image monika 1dkbltda_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    blush="lines",
    tears="dried",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dkbltpa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="pooled"
)

image monika 1dkbltpb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="pooled"
)

image monika 1dkbltua_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    blush="lines",
    tears="up",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dkbltuu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="upclosedsad"
)

image monika 1dkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1dkbsb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    blush="shade",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dkbsc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    blush="shade",
    head="h",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dkbsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1dkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)


image monika 1dkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dksdla_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    sweat="def",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    sweat="def",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    sweat="def",
    head="h",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dksdld_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="small",
    sweat="def",
    head="i",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dksdlw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="wide",
    sweat="def",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dksdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    sweat="right",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dkt_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="triangle",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dktda_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="dried"
)

image monika 1dktdc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    tears="dried",
    head="h",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dktdd_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="small",
    tears="dried",
    head="i",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dktpa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    tears="pooled",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dktpc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="pooled"
)

image monika 1dktpu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smug",
    tears="pooled",
    head="j",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dktsc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    tears="streaming",
    head="h",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dktsd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streamingclosedsad"
)

image monika 1dktua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    tears="upclosedsad"
)

image monika 1dktub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    tears="upclosedsad"
)

image monika 1dku_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dkx_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="disgust",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dsb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dsbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1dsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smile",
    blush="shade",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dsbso_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1dsbssdlu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smug",
    blush="shade",
    sweat="def",
    head="j",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dsbssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    blush="shade",
    sweat="right",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dsd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dso_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dssdlb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    sweat="def",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    sweat="right",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dssdrc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smirk",
    sweat="right",
    head="h",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dsu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dtc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="think",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dtsdlc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="think",
    nose="def",
    mouth="smirk",
    sweat="def",
    head="h",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dtu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="think",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dub_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dubfa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    blush="full",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dubfb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    blush="full",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dubfsdld_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="small",
    blush="full",
    sweat="def",
    head="i",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dubftsb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    blush="full",
    tears="streaming",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dubfu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smug",
    blush="full",
    head="j",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dublo_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="gasp",
    blush="lines",
    head="d",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dubsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    blush="shade",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dubso_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="gasp",
    blush="shade",
    head="d",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dubssdru_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade",
    sweat="right"
)

image monika 1dubsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1dubsw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="wide",
    blush="shade",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1duc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dud_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1duo_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="gasp",
    head="d",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dusdlb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    sweat="def",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1dutsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    tears="streaming",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1duu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1duw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="wide",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1efb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="gasp",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efp_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="pout",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1eft_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="triangle",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)


image monika 1eftsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="i",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1efu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1eka_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="e",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1ekb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1ekbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1ekbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1ekbfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1ekbla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines"
)

image monika 1ekbltua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="up"
)

image monika 1ekbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1ekbsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1ekc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1ekd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1eksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1eksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1eksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1eksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1ekt_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="triangle",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1ektda_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    tears="dried"
)

image monika 1ektdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="dried"
)

image monika 1ektdd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="dried"
)

image monika 1ektpa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="pooled"
)

image monika 1ektpu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="pooled"
)

image monika 1ektsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1ektsd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1ektua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    tears="up"
)

image monika 1esa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1esb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1esc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1esd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1eua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1eub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1eubfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1eubfu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="normal",
    eyebrows="up",
    nose="def",
    mouth="smug",
    blush="full",
    head="j",
    left="1l",
    right="1r",
    arms="steepling",
)

image monika 1euc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="c",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1eud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="wide",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="disgust",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hka_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="l",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hkbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1hkbfsdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="1r",
    blush="full",
    arms="steepling",
    sweat="def"
)

image monika 1hkbla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines"
)

image monika 1hkbltpa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="pooled"
)

image monika 1hksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="l",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1hksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1hksdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="right"
)

image monika 1hsb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hubfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1hubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1huu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1kua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="winkleft",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1kubfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="winkleft",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1lfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lftsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1lfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lkbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1lkbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1lkbltpa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="pooled"
)

image monika 1lkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="e",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1lkbsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1lksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="small",
    head="p",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lksdlw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="wide",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lksdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="right"
)

image monika 1lktsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1lsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1lsbssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="right",
    blush="shade"
)

image monika 1lsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="right"
)

image monika 1lssdrc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="right"
)

image monika 1ltsdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="think",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1lud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rkbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="q",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1rkbfsdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="q",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full",
    sweat="def"
)

image monika 1rkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="e",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1rkbsb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="q",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1rkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="o",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1rksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1rksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1rksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="p",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1rktsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1rsbssdlu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smug",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def",
    blush="shade"
)

image monika 1rsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rssdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1ruc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="d",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rusdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="big",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1sfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1skbla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines"
)

image monika 1skbltda_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="dried"
)

image monika 1skbltpa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="pooled"
)

image monika 1sua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1sub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1subfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1subfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1subftsb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full",
    tears="streaming"
)

image monika 1sublo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines"
)

image monika 1subsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1suo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1sutsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1tfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tkbfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1tkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tku_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tkx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tsb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tsbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1tsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1tsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1ttu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="think",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="k",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tubfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1tubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1tubfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="k",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1tubsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1tuu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="k",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="smile",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wka_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wkb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="big",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wkbltpa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="pooled"
)

image monika 1wkbsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="e",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1wkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="small",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wktpa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smile",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="pooled"
)

image monika 1wktsd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="small",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1wua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="smile",
    head="d",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1wubfsdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full",
    sweat="def"
)

image monika 1wubso_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1wubsw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1wud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wuo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wuw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 2dfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dfo_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="gasp",
    head="d",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dfp_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="pout",
    head="h",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dfsdld_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="small",
    sweat="def",
    head="i",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dft_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="triangle",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dftdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="2r",
    arms="crossed",
    tears="dried"
)

image monika 2dftsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streamingclosedsad"
)

image monika 2dftsu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="smug",
    tears="streaming",
    head="j",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="wide",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="disgust",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dka_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dkb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dkbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2dkbfb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    blush="full",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dkbfsdlb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    blush="full",
    sweat="def",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dkbfsdld_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="small",
    blush="full",
    sweat="def",
    head="i",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dkbfsdlu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smug",
    blush="full",
    sweat="def",
    head="j",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    blush="shade",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dkbsc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    blush="shade",
    head="h",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dkbsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2dkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dkp_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="pout",
    head="h",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dksdla_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    sweat="def",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    sweat="def",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2dksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2dksdlw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="wide",
    sweat="def",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dksdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    sweat="right",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dkt_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="triangle",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dktdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="2r",
    arms="crossed",
    tears="dried"
)

image monika 2dktpc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="r",
    left="1l",
    right="2r",
    arms="crossed",
    tears="pooled"
)

image monika 2dktsc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    tears="streaming",
    head="h",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dktsd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streamingclosedsad"
)

image monika 2dktuc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="r",
    left="1l",
    right="2r",
    arms="crossed",
    tears="upclosedsad"
)

image monika 2dku_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dkx_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="disgust",
    head="f",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dsb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smile",
    blush="shade",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dsbso_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2dsbssdlb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    blush="shade",
    sweat="def",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dsbssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    blush="shade",
    sweat="right",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dsd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dso_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dssdlb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    sweat="def",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    sweat="right",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dssdrc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smirk",
    sweat="right",
    head="h",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dsu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dtc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="think",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dtu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="think",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dub_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dubfa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    blush="full",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dubfb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    blush="full",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dubfsdld_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="small",
    blush="full",
    sweat="def",
    head="i",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dubftsb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    blush="full",
    tears="streaming",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dubfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2dubso_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="gasp",
    blush="shade",
    head="d",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dubssdru_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade",
    sweat="right"
)

image monika 2dubsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2dubsw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="wide",
    blush="shade",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2duc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dud_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2duo_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="gasp",
    head="d",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2dutsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    tears="streaming",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2duu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2duw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="wide",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
)

image monika 2efb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2efc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2efd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2efo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="gasp",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2eft_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="triangle",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)


image monika 2eftsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="i",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2efu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2efw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2efx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2eka_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="e",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2ekb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="e",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2ekbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2ekbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2ekc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2ekd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2ekp_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="pout",
    head="a",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2eksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="i",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2eksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2eksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2ekt_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="triangle",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2ektsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="r",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2eku_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2esa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2esb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2esc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2esd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2etc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="think",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2eua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2eub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2euc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="c",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2eud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hfsdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2hfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="wide",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="disgust",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hkbfsdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="2r",
    blush="full",
    arms="crossed",
    sweat="def"
)

image monika 2hksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2hksdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="right"
)

image monika 2hua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hubfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2hubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2lfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lfp_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="pout",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lftsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2lfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lkbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2lkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="e",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2lkbsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2lksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="small",
    head="p",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lksdlw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="wide",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lksdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="right"
)

image monika 2lktsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2lsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2lsbssdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def",
    blush="shade"
)

image monika 2lsbssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="right",
    blush="shade"
)

image monika 2lsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lssdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="right"
)

image monika 2lssdrc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="right"
)

image monika 2lubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2lud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rka_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rkbfsdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def",
    blush="full"
)

image monika 2rkbfsdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="p",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full",
    sweat="def"
)

image monika 2rkbfsdlu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smug",
    head="e",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full",
    sweat="def"
)

image monika 2rkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="2r",
    blush="shade",
    arms="crossed"
)

image monika 2rkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2rksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2rksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2rksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="p",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2rktpc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed",
    tears="pooled"
)

image monika 2rktsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2rktsd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="f",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2rsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2rsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rubfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="smug",
    head="q",
    left="1l",
    right="2r",
    blush="full",
    arms="crossed"
)

image monika 2sub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2subfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2subftsb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full",
    tears="streaming"
)

image monika 2sutsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2tfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tfp_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="pout",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tkb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="big",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tku_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tkx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tsb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2tsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2ttu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="think",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2tubfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="k",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2tuu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="k",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="c",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="small",
    head="c",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wkbsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="l",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2wkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="l",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="small",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wktsd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="small",
    head="f",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2wub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2wubfsdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full",
    sweat="def"
)

image monika 2wubso_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2wubsw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2wuc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="d",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wuo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wuw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 3dfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dfo_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="gasp",
    head="d",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dft_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="triangle",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dftdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="dried"
)

image monika 3dftsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streamingclosedsad"
)

image monika 3dftsu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="smug",
    tears="streaming",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="disgust",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dka_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dkb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dkbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3dkbfb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    blush="full",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dkbfsdla_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    blush="full",
    sweat="def",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dkbla_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    blush="lines",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dkbltda_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    blush="lines",
    tears="dried",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dkbltpa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="lines",
    tears="pooled"
)

image monika 3dkbltub_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    blush="lines",
    tears="up",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    blush="shade",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dkbsc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    blush="shade",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dkbsu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smug",
    blush="shade",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright"
)


image monika 3dkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dksdla_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    sweat="def",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    sweat="def",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    sweat="def",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dksdld_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="small",
    sweat="def",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dksdlw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="wide",
    sweat="def",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dksdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    sweat="right",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dktda_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    tears="dried",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dktsc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    tears="streaming",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dku_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dkx_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="disgust",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dsb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smile",
    blush="shade",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dsbso_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3dsbssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    blush="shade",
    sweat="right",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dsd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dso_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dssdlb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    sweat="def",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dssdlc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smirk",
    sweat="def",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    sweat="right",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dssdrc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smirk",
    sweat="right",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dsu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dtc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="think",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dtd_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="think",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dua_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dub_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dubfa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    blush="full",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dubfb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    blush="full",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dubfsdld_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="small",
    blush="full",
    sweat="def",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dubfsdlo_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="gasp",
    blush="full",
    sweat="def",
    head="d",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dubftsb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    blush="full",
    tears="streaming",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dubsb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    blush="shade",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dubso_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="gasp",
    blush="shade",
    head="d",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dubssdru_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade",
    sweat="right"
)

image monika 3dubsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3dubsw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="wide",
    blush="shade",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3duc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dud_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3duo_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="gasp",
    head="d",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3dutsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    tears="streaming",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3duu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3duw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="wide",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
)

image monika 3efb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3efc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3efd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3efo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="gasp",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3eft_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="triangle",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)


image monika 3eftsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3efu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3efw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3efx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3eka_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="e",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3ekb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3ekbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3ekbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3ekbla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="lines"
)

image monika 3ekbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3ekc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3ekd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3eksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3eksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3eksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3ektda_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="dried"
)

image monika 3ektsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3esa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3esb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3esc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3esd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3etc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="think",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3etd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="think",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3eua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3eub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3euc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="c",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3eud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="disgust",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hkbltpa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="lines",
    tears="pooled"
)

image monika 3hkbltub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="lines",
    tears="upclosedhappy"
)

image monika 3hksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3hksdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="right"
)

image monika 3hua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hubfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3hubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3hubsb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3lfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lftsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3lfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lkbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3lkbltpa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="lines",
    tears="pooled"
)

image monika 3lkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="e",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3lkbsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3lksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="m",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3lksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3lksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3lksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="small",
    head="p",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3lksdlw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="wide",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3lksdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="right"
)

image monika 3lktsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3lsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3lsbssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="right",
    blush="shade"
)

image monika 3lsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="right"
)

image monika 3lssdrc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="right"
)

image monika 3lubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3lud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rka_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rkbfsdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="m",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def",
    blush="full"
)

image monika 3rkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="e",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3rkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="m",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3rksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3rksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3rksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="p",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3rktsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3rsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smile",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rssdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="big",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3rssdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3rssdrc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="right"
)

image monika 3rubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="big",
    head="d",
    left="1l",
    right="1r",
    blush="full",
    arms="restleftpointright"
)

image monika 3rud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="1r",
    arms="restleftpointright"
)

image monika 3skbltda_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="lines",
    tears="dried"
)

image monika 3sua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3sub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3subfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3subftsb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full",
    tears="streaming"
)

image monika 3sutsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3tfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tkbsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3tkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="1r",
    arms="restleftpointright"
)
image monika 3tku_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tkx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tsb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3tsd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="small",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="k",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3tuu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="k",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wkbsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="p",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)


image monika 3wkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="small",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3wubfsdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full",
    sweat="def"
)

image monika 3wubfsdlo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full",
    sweat="def"
)

image monika 3wubso_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3wubsw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3wud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wuo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wuw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 4dfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dfo_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="gasp",
    head="d",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dft_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="triangle",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dftdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="2r",
    arms="pointright",
    tears="dried"
)

image monika 4dftsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streamingclosedsad"
)

image monika 4dftsu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="smug",
    tears="streaming",
    head="j",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="disgust",
    head="q",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dka_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dkbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4dkbfb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    blush="full",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    blush="shade",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dkbsc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    blush="shade",
    head="h",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="2r",
    arms="pointright"
)
image monika 4dksdla_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    sweat="def",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    sweat="def",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    sweat="def",
    head="h",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dksdld_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="small",
    sweat="def",
    head="i",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dksdlw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="wide",
    sweat="def",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dksdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    sweat="right",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dktdc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    tears="dried",
    head="h",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dktpc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    tears="pooled",
    head="h",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dktsc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    tears="streaming",
    head="h",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dktsw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="wide",
    tears="streaming",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dku_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dkx_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="disgust",
    head="f",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dsb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smile",
    blush="shade",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dsbso_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4dsbssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    blush="shade",
    sweat="right",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dsd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dso_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="big",
    sweat="right",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dssdrc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smirk",
    sweat="right",
    head="h",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dua_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dub_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dubfa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    blush="full",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dubfb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    blush="full",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dubfsdld_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="small",
    blush="full",
    sweat="def",
    head="i",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dubftsb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    blush="full",
    tears="streaming",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dubso_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="gasp",
    blush="shade",
    head="d",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dubssdru_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade",
    sweat="right"
)

image monika 4dubsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4dubsw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="wide",
    blush="shade",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4duc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dud_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4duo_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="gasp",
    head="d",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4dutsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    tears="streaming",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4duu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4duw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="wide",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
)

image monika 4efb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4efc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4efd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4efo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="gasp",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4eft_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="triangle",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4eftsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="i",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4efu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4efw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4efx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4eka_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="e",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4ekbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4ekbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4ekbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="k",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4ekc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4ekd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4eksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="m",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4eksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4eksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4ektdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="r",
    left="2l",
    right="2r",
    arms="pointright",
    tears="dried"
)

image monika 4ektsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="r",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4esa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4esb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="big",
    head="d",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4esc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4esd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4eua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4eub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4euc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="c",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4eud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="disgust",
    head="q",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4hksdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right"
)

image monika 4hua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="j",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hubfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4hubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4huu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smug",
    head="k",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lftsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4lfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lkbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4lkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="e",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4lkbsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4lksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="m",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4lksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4lksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4lksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="small",
    head="p",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4lksdlw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="wide",
    head="n",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4lksdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right"
)

image monika 4lktsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4lsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4lsbssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right",
    blush="shade"
)

image monika 4lsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right"
)

image monika 4lssdrc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right"
)

image monika 4lubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4lud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rkbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4rkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="m",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4rksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4rksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4rksdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="p",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4rktpc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright",
    tears="pooled"
)

image monika 4rktsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4rsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rssdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right"
)

image monika 4rssdrc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right"
)

image monika 4sub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4subfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)


image monika 4subftsb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full",
    tears="streaming"
)

image monika 4sutsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4tfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="2r",
    arms="pointright"
)
image monika 4tku_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="f",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tkx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="f",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tsb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4tub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4wfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wfx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wkbsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4wkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wkd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="small",
    head="b",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wktsw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4wua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="smile",
    head="d",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4wubfsdld_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full",
    sweat="def"
)

image monika 4wubso_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4wubsw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4wuc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="d",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wuo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wuw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 5dfa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dfc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dka_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dkbfa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    blush="full",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dkbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    blush="full",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dkbla_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    blush="lines",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    blush="shade",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dkc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dsbfa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smile",
    blush="full",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dsbfu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smug",
    blush="full",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dsc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dsu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dtu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="think",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dua_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dub_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dubfa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    blush="full",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dubfb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    blush="full",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dubfsdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    blush="full",
    sweat="right",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dubfsdru_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smug",
    blush="full",
    sweat="right",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dubfu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smug",
    blush="full",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dubfw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="wide",
    blush="full",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dubla_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    blush="lines",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dubsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smile",
    blush="shade",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5duc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dusdrb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    sweat="right",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5dusdru_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smug",
    sweat="right",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5duu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5duw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="wide",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5efa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5eka_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3e"
)

image monika 5ekbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="full",
    single="3b"
)

image monika 5ekbla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="lines",
    single="3b"
)

image monika 5ekbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="shade",
    single="3b"
)

image monika 5esbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="full",
    single="3b"
)

image monika 5esu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3a"
)

image monika 5eua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3a"
)

image monika 5eub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5eubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    blush="full",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5eubfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    blush="full",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5eubla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="lines",
    single="3b"
)

image monika 5euc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5hkbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="full",
    single="3b"
)

image monika 5hkbfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="full",
    single="3b"
)

image monika 5hua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5hub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5hubfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="full",
    single="3b"
)

image monika 5hubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="full",
    single="3b"
)

image monika 5hubfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="full",
    single="3b"
)

image monika 5lfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5lkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5lsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5lubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    blush="full",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5lubfsdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    blush="full",
    sweat="right",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5lubfsdru_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    blush="full",
    sweat="right",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5lubfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    blush="full",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5lubsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    blush="shade",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5lusdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    sweat="right",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5lusdru_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    sweat="right",
    arms="def",
    lean="def",
    single="3b"
)

# bored
image monika 5luu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5rfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5rkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5rsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5rub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5rubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    blush="full",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5rubfsdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    blush="full",
    sweat="right",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5rubfsdru_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    blush="full",
    sweat="right",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5rubfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    blush="full",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5rusdrb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    sweat="right",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5rusdru_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    sweat="right",
    arms="def",
    lean="def",
    single="3b"
)


image monika 5ruu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5tsbfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="full",
    single="3a"
)

image monika 5tsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5tsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3a"
)

image monika 5ttu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="think",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3a"
)

image monika 5tubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="full",
    single="3a"
)

image monika 5tubfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    blush="full",
    single="3a"
)

image monika 5wubfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="",
    left="",
    right="",
    blush="full",
    arms="def",
    lean="def",
    single="3b"
)

image monika 5wuw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="",
    left="",
    right="",
    arms="def",
    lean="def",
    single="3b"
)

image monika 6cfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="crazy",
    nose="def",
    mouth="wide",
    head="c",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6ckc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="crazy",
    nose="def",
    mouth="smirk",
    head="c",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6dfc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6dfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6dft_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="triangle",
    head="a",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dftdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6dftdx_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="disgust",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6dftpc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="smirk",
    tears="pooled",
    head="h",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dftsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="streamingclosedsad"
)

image monika 6dfw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="furrowed",
    nose="def",
    mouth="wide",
    head="b",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dka_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dkbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="o",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6dkbfd_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="small",
    blush="full",
    head="i",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dkbfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6dkbsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    blush="shade",
    head="a",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dkbsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    blush="shade"
)

image monika 6dkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="a",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6dkd_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="i",
    left="1l",
    right="1r",
    arms="down",
    sweat="def"
)

image monika 6dksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="big",
    sweat="def",
    head="b",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smirk",
    sweat="def",
    head="h",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dktda_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    tears="dried",
    head="a",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dktdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="a",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6dktpc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="pooled"
)

image monika 6dktrc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="rightclosedsad"
)

image monika 6dktrd_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="small",
    tears="right",
    head="i",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dktsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="knit",
    nose="def",
    mouth="smile",
    tears="streaming",
    head="a",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dktsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="a",
    left="1l",
    right="1r",
    arms="down",
    tears="streamingclosedsad"
)

image monika 6dktua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="upclosedsad"
)

image monika 6dktuc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="upclosedsad"
)

image monika 6dktuu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="upclosedsad"
)

image monika 6dku_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6dsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6dsbfa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smile",
    blush="full",
    head="a",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="smile",
    blush="shade",
    head="a",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6dst_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="mid",
    nose="def",
    mouth="triangle",
    head="a",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dstdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6dstsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="streamingclosedsad"
)

image monika 6dua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6dub_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dubfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6dubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6dubfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6dubfo_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="gasp",
    blush="full",
    head="d",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dubsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="1r",
    arms="down",
    blush="shade"
)

image monika 6dubsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="j",
    left="1l",
    right="1r",
    arms="down",
    blush="shade"
)

image monika 6dubsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="down",
    blush="shade"
)

image monika 6dubsw_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="wide",
    blush="shade",
    head="b",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6dud_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6duo_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="gasp",
    head="d",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6duu_static = DynamicDisplayable(
    mas_drawmonika,
    monika_chr,
    eyes="closedsad",
    eyebrows="up",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="down",
)

image monika 6eftsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6eka_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="e",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6ekbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="o",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6ekbfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="o",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6ekbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down",
    blush="shade"
)

image monika 6ekbsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    blush="shade"
)

image monika 6ekc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="a",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6ekd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6eksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="i",
    left="1l",
    right="1r",
    arms="down",
    sweat="def"
)

image monika 6ektda_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6ektdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6ektpc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="pooled"
)

image monika 6ektrd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="right"
)

image monika 6ektsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6ektsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6esa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="q",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6esbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6eua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6eud_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="small",
    head="a",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6hft_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="triangle",
    head="r",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6hkbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6hkbsu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down",
    blush="shade"
)

image monika 6hksdlb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="1r",
    arms="down",
    sweat="def"
)

image monika 6hua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6hub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6hubfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6hubfb_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6lftsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6lkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6lktdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6lktsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6rkbfd_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="o",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6rkc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6rksdla_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="1r",
    arms="down",
    sweat="def"
)


image monika 6rksdlc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="down",
    sweat="def"
)

image monika 6rktda_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6rktdc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="a",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6rktsc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6rktuc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="up"
)

image monika 6sua_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6sub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6suu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smug",
    head="b",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6tftpc_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="pooled"
)

image monika 6tkbfu_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    blush="full"
)

image monika 6tsbfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="q",
    left="1l",
    right="1r",
    blush="full",
    arms="down"
)

image monika 6tsbsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="q",
    left="1l",
    right="1r",
    blush="shade",
    arms="down"
)

image monika 6tst_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="triangle",
    head="q",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6tubfa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="q",
    left="1l",
    right="1r",
    blush="full",
    arms="down",
)

image monika 6tubsa_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="q",
    left="1l",
    right="1r",
    blush="shade",
    arms="down",
)

image monika 6wfw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6wka_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6wub_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6wubfo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="1r",
    blush="full",
    arms="down"
)

image monika 6wubsw_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="b",
    left="1l",
    right="1r",
    arms="down",
    blush="shade"
)

image monika 6wuo_static = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="1r",
    arms="down"
)


