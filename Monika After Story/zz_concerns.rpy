default persistent._mas_concerns = dict()

init python:
    class Concern:
        def __init__(self, *args):
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
            if self._expire is not None:
                return datetime.datetime.now() >= self._expire
            else:
                return False


        def is_concerned(self, threshold):
            if self._value is not None:
                return self._value >= threshold
            else:
                return False


        def to_dict(self):
            return dict(value=self._value, expire=self._expire)


    def mas_setConcern(_type, concern):
        if concern is not None:
            persistent._mas_concerns[_type] = concern
        else:
            del persistent._mas_concerns[_type]


    def mas_getConcern(_type):
        concern_dict = persistent._mas_concerns.get(_type)
        if concern_dict is not None:
            return Concern(concern_dict)
        else:
            return Concern()


    def mas_clearConcern(_type):
        mas_setConcern(_type, None)


    def mas_isConcerned(_type, threshold):
        return mas_getConcern(_type).is_concerned(threshold)


    def mas_hasConcernExpired(_type):
        return mas_getConcern(_type).has_expired()


    def mas_concern(_type, add=None, prolong=None):
        concern = mas_getConcern(_type)

        if prolong is not None:
            concern._expire = (concern._expire or datetime.datetime.now()) + prolong

        if add is not None:
            concern._value = (concern._value or 0) + add
