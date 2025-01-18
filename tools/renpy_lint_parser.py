# parses renpy_output and removes missing dynamic image lines.
# (and other known things)

import re
# import os
import sys


# regex parsing

IMG_NOT_FOUND = re.compile(
    r"\w+/(\w+/)*.+\.rpy:\d+ (Could not find image \(monika |The image named 'monika )(\d\w\w\w+|\d\w|1|5|4|g1|g2)"
)

# file load

IN_FILENAME = "renpy_output"
OUT_FILENAME = "renpy_output_clean"

# load files
try:
    with open(IN_FILENAME, "r") as infile, open(OUT_FILENAME, "w") as outfile:
        # loop and clean
        for line in infile:
            if (
                len(line.strip()) > 0
                and not IMG_NOT_FOUND.match(line)
            ):
                outfile.write(line)

except Exception as e:
    print(f"File load failed: {e}")
    sys.exit(1)

else:
    sys.exit(0)
