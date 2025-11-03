# mas can import paradigm.
# see python-packages/mas/can_import/masimport.py for details
init -1500 python in mas_can_import:

    import renpy
    import mas.can_import.masimport as masimport

    # set importables


    # run checks

    masimport.check_imports(renpy)
