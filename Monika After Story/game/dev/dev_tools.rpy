# basic dev tool stuff

init 2018 python:
    
    def mas_remove_event(*labels):
        """
        Removes an event from the persistent database and lock DB
        NOTE: runtime only

        Use this if you need to reseat an Event
        will quit the game once you have done this
        """
        for label in labels:
            if label in persistent.event_database:
                persistent.event_database.pop(label)

            if label in Event.INIT_LOCKDB:
                Event.INIT_LOCKDB.pop(label)
           
        persistent.closed_self = True
        persistent._mas_game_crashed = False
        renpy.save_persistent()
        renpy.jump("_quit")
