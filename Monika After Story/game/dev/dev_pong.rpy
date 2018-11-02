## here we run some test cases

<<<<<<< HEAD
init 2017 python:
=======
init 999 python:
>>>>>>> be423abed5eb988f07d48c189406ae8a9bccd9f5
    import store.mas_pong as mas_pong

    for dlg_label in mas_pong.DLG_BLOCKS:
        if not renpy.has_label(dlg_label):
            raise Exception("missing label {0}".format(dlg_label))
