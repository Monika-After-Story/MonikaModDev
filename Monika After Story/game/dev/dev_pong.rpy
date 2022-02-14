## here we run some test cases

init 999 python:
    import store.mas_pong as mas_pong

    for dlg_label in mas_pong.DLG_BLOCKS:
        if not renpy.has_label(dlg_label):
            raise Exception("missing label {0}".format(dlg_label))
