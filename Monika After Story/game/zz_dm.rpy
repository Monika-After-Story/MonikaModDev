# data migration module

init -899 python:
    # NOTE: THIS should happen after persistent backup algorithm

    persistent._mas_dm_data_version = 1
    # this should be updated whenever we do a data version migration
