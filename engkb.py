import cngkb, gkberror
import pandas as pd
import csv


class GeoGeneratorEn:
    def __init__(self):
        self.city_usa = pd.read_csv("./gkb_en/city_usa.csv", sep=',', header=None)

    def check_location(self, location):
        # for row in range(0, self.city_usa.shape[1]):
        for row in list(self.city_usa.columns):
            if self.city_usa[self.city_usa[row] == location].empty:
                pass
            else:
                return self.city_usa[self.city_usa[row] == location], row
        else:
            raise gkberror.LocationNotFound(location=location)

    def single_location_generator(self, single_location, list_len=3):
        try:
            location_index, row_index = self.check_location(location=single_location)
        except gkberror.LocationNotFound as error:
            raise error
        # print(location_index)   已找到！
        if row_index != 0:          # 不是第一列的数据
            neighbors = self.city_usa[(self.city_usa[row_index-1] == location_index.iloc[0, row_index-1])
                                      & (self.city_usa[row_index] != location_index.iloc[0, row_index])]
        else:                   # 是第一列的数据
            neighbors = self.city_usa[self.city_usa[0] != location_index.iloc[0, 0]]
        try:            # 检测相似元素是否多于需要元素
            sample = neighbors.sample(n=list_len, replace=False)
            return list(sample[row_index])
        except ValueError:
            raise gkberror.LessThanExpectError(exist_num=neighbors.shape[0])

    def multi_location_generator(self, location_list):
        return_list = []
        for location in location_list:
            return_list.append(self.single_location_generator(single_location=location, list_len=len(location_list)))
        return return_list

    def run(self, location):
        # 无需在函数的形参中引入类型，在内部般判断即可
        input_type = type(location)
        if input_type == "str":
            location_set = self.single_location_generator(location)
        else:
            location_set = self.multi_location_generator(location)
        return location_set


if __name__ == "__main__":
    geo = GeoGeneratorEn()
    # print(geo.city_usa)
    # print(geo.check_location('Boston'))
    # print(geo.check_location('Alabama'))
    print(geo.single_location_generator('Boston'))      # ['Billerica', 'Acton', 'Belmont']
    print(geo.single_location_generator('Alabama'))     # ['New Jersey', 'Florida', 'California']
    print(geo.multi_location_generator(['Boston', 'New York City', 'Texas']))
    # [['Billerica', 'Pittsfield', 'Lynnfield'], ['Norwich', 'Cornwall', 'Ithaca'], ['Indiana', 'Oregon', 'Ohio']]
