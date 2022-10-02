# NOTE: this is a dummy package so consumers think we exist.

import platform

if (
        platform.system() in ("Windows", "Linux")
        or (platform.system() == "Darwin" and platform.machine() == "x86_64") # 64-bit mac
):
    pass
else:
    raise ImportError
