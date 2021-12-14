# NOTE: this is a dummy package so consumers think we exist.

import platform

if platform.system() == "Windows": # TODO- add all acceptable packages here
    pass
else:
    raise ImportError
