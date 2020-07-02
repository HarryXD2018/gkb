~~~python
class LocationNotFound(Exception):
    def __init__(self, location):
        err = '未找到{}'.format(location)
        Exception.__init__(self, err)


class GeoGenerator:
    def __init__(self):
        pass

    def parse_location(self, location):
        return parsed_location, location_catalog
	    # catalog = -1 没有修改
        # catalog 与 place_enum 的index相同 

    def is_capital(self, location):
        return True, capitals[0]
        return False, None
    	# 返回是否是capital与capital类型

    def check_location(self, location):
        return location_type, location_index

    def single_location_generator(self, single_location, list_count=3):
        pass
        return single_location_list

    def multi_location_generator(self, multi_location):
        multi_location_list = []
        pass
        return multi_location_list

    def run(self, location):
        # 无需在函数的形参中引入类型，在内部般判断即可
        input_type = type(location)
        if input_type == "str":
            location_set = self.single_location_generator(location)
        else:
            location_set = self.multi_location_generator(location)
        return location_set


if __name__ == '__main__':
    geo = GeoGenerator()
    print(geo.check_location("华盛顿特区"))
    print(geo.check_location("香港特别行政区"))
    print(geo.check_location("北京"))
    print(geo.check_location("海淀"))
    # print(geo.single_location_generator("马萨诸塞州"))
    # print(geo.single_location_generator("福岛"))
    # print(geo.single_location_generator("美利坚合众国"))
    # print(geo.single_location_generator("海淀区"))
    # print(geo.single_location_generator("中国"))
    # print(geo.multi_location_generator(["马萨诸塞州", "福岛", "美利坚合众国", "海淀区", "中国"]))
    # print(geo.multi_location_generator(["马萨诸塞州", "加利福尼亚州", "幻想乡", "曲阳县"]))
    # 这个世界上当然是没有幻想乡啦

~~~

