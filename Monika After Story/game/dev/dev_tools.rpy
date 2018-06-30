# basic dev tool stuff

init 2018 python:
    
    def mas_remove_event(label):
        """
        Removes an event from the persistent database and lock DB
        NOTE: runtime only

        Use this if you need to reseat an Event
        """
        if label in persistent.event_database:
            persistent.event_database.pop(label)

        if label in Event.INIT_LOCKDB:
            Event.INIT_LOCKDB.pop(label)
