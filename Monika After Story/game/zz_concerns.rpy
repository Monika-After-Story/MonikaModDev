default persistent._mas_concerns = dict()

init python:
    def _mas_getConcern(_type, _new=False):
        return persistent._mas_concerns.get(_type, {
            '_type': _type,
            'occurences': list(),
            'expieres': datetime.datetime()
        } if _new else None)


    def _mas_persistConcern(_dict):
        persistent._mas_concerns[_dict['_type']] = _dict


    def _mas_unsetConcern(_type):
        if _type in persistent._mas_concerns:
            del persistent._mas_concerns[_type]


    def mas_addToConcern(_type, pts, tags=None, duration=None):
        if tags is None:
            tags = list()

        concern = _mas_getConcern(_type, True)
        concern['occurences'].append({
            'tags': tags,
            'value': pts
        })
        if duration is not None:
            concern['expires'] += duration


    def mas_getConcernPoints(_type, tags=None):
        concern = _mas_getConcern(_type)
        if concern is None:
            return 0

        if tags is None:
            return sum(map(lambda it: it['value'], occ for occ in concern['occurences']))
        else:
            def contains_all(src, check):
                return all(map(lambda it: it in src, check))

            return sum(map(lambda it: it['value'], occ for occ in concern['occurences'] if contains_all(occ['tags'], tags)))


    def mas_clearConcern(_type, tags=None):
        concern = _mas_getConcern(_type)
        if concern is not None:
            if tags is None:
                _mas_unsetConcern(_type)
            else:
                def contains_all(src, check):
                    return all(map(lambda it: it in src, check))

                for i in range(len(concern['occurences']), -1, -1):
                    occ = concern['occurences'][i]
                    if contains_all(occ['tags'], tags):
                        del concern['occurences'][i]


    def mas_hasConcernExpired(_type):
        concern = _mas_getConcern(_type)
        if concern is not None:
            return datetime.datetime.now() > concern['expires']
