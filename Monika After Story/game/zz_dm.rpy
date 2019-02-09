# data migration module

init -915 python:
    # before verification

    persistent._mas_dm_data_version = 1
    # this should be updated whenever we do a data version migration

init -905 python:
    # between verification and backup
    pass 

init -895 python:
    # after backup
    pass
