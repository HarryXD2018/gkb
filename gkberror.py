class LocationNotFound(Exception):
    def __init__(self, location: str):
        err = '未找到{}'.format(location)
        Exception.__init__(self, err)


class LessThanExpectError(Exception):
    def __init__(self, exist_num):
        err = 'only find {} satisfied item(s) '.format(exist_num)
        Exception.__init__(self, err)