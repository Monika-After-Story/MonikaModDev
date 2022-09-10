# parses renpy_output and removes missing dynamic image lines. 
# (and other known things)

import re
import os


# regex parsing

IMG_NOT_FOUND = re.compile(
    "\w+/(\w+/)*.+\.rpy:\d+ (Could not find image \(monika |The image named 'monika )(\d\w\w\w+|\d\w|1|5|4|g1|g2)"
)

# file load

IN_FILENAME = "renpy_output"
OUT_FILENAME = "renpy_output_clean"

# load files
INFILE = open(IN_FILENAME, "r")
OUTFILE = open(OUT_FILENAME, "w")

if not INFILE or not OUTFILE:
    print("file load failed")
    exit(1)

# loop and clean
for line in INFILE:
    if (
            len(line.strip()) > 0
            and not IMG_NOT_FOUND.match(line)
    ):
        OUTFILE.write(line)

INFILE.close()
OUTFILE.close()
exit(0)
