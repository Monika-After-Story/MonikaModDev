default persistent._mas_concerns = dict()

init python:
    class Concern:
        def __init__(self, *args):
            """
            Constructs a new instance of Concern.

            IN:
                _dict - dictionary or dict-like object containing object field values.

                ... or ...

                value - value of this concern object.
                expire - datetime object representing the instant of this concern object expiration.

            OUT:
                Instance of Concern.
            """
            if len(args) == 0:
                self._value = None
                self._expire = None
                self._tags = list()
            elif len(args) == 1:
                if hasattr(args[0], "__getitem__"):
                    self._value = args[0]["value"]
                    self._expire = args[0]["expire"]
                else:
                    raise ValueError("__init__() expected positional argument to be dict or dict-like but argument of type " + args[0].__class__.__name__ + " was given")
            elif len(args) == 2:
                self._value = args[0]
                self._expire = args[1]
            else:
                raise ValueError("__init__() takes 2 positional arguments but " + str(len(args)) + " were given")


        def has_expired(self):
            """
            Performs a concern expiration check.

            OUT:
                True if this concern object has expired, False otherwise.
            """
            if self._expire is not None:
                return datetime.datetime.now() >= self._expire
            else:
                return False


        def is_concerned(self, threshold):
            """
            Performs a concern value check.

            IN:
                threshold - concern value greater than or equal to this value
                    will make this concern object 'concerning.'

            OUT:
                True if this concern object has value greather than
                    or equal to threshold, False otherwise.
            """
            if self._value is not None:
                return self._value >= threshold
            else:
                return False


        def to_dict(self):
            """
            Converts this object into a dictionary.

            OUT:
                Dictionary representation of this concern object.
            """
            return dict(value=self._value, expire=self._expire)


    def mas_setConcern(_type, concern):
        """
        Saves concern object to persistent storage.

        IN:
            _type - concern type (name.)
            concern - concern object.
        """
        if concern is not None:
            persistent._mas_concerns[_type] = concern
        else:
            del persistent._mas_concerns[_type]


    def mas_getConcern(_type):
        """
        Retrieves concern object from persistent storage.

        IN:
            _type - concern type (name.)

        OUT:
            Concern object with the given type.
        """
        concern_dict = persistent._mas_concerns.get(_type)
        if concern_dict is not None:
            return Concern(concern_dict)
        else:
            return Concern()


    def mas_clearConcern(_type):
        """
        Removed concern object from persistent storage.

        IN:
            _type - concern type (name.)
        """
        mas_setConcern(_type, None)


    def mas_isConcerned(_type, threshold):
        """
        Checks if concern is 'concerning.'

        IN:
            _type - concern type (name.)
            threshold - value to compare concern value with.

        OUT:
            True if concern with the given type has value greather or equal
                to the specified threshold, False otherwise.
        """
        return mas_getConcern(_type).is_concerned(threshold)


    def mas_hasConcernExpired(_type):
        """
        Checks if concern has expired.

        IN:
            _type - concern type (name.)

        OUT:
            True if concern with the given type has expired, False otherwise.
        """
        return mas_getConcern(_type).has_expired()


    def mas_concern(_type, add=None, prolong=None):
        """
        Adds value to concern and/or prolongs it.

        IN:
            _type - concern type (name.)
            add - value to add to this concern.
            prolong - timedelta to prolong this concern by.
        """
        concern = mas_getConcern(_type)

        if prolong is not None:
            concern._expire = (concern._expire or datetime.datetime.now()) + prolong

        if add is not None:
            concern._value = (concern._value or 0) + add
