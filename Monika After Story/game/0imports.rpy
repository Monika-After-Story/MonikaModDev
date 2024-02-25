# mas can import paradigm.
# see python-packages/mas/can_import/masimport.py for details
init -1500 python in mas_can_import:

    import renpy
    import store.mas_utils as mas_utils
    import mas.can_import.masimport as masimport
    from mas.can_import import MASImport_ssl, MASImport_certifi

    # set importables

    certifi = MASImport_certifi()
    certifi._set_log(mas_utils.mas_log)

    ssl = MASImport_ssl()
    ssl._set_log(mas_utils.mas_log)

    # run checks

    masimport.check_imports(renpy)


init -1510 python in mas_can_import:

    from mas.can_import import MASImport

