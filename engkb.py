import cngkb
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
            raise cngkb.LocationNotFound(location=location)

    def single_location_generator(self, single_location, list_len=3):
        try:
            location_index, row_index = self.check_location(location=single_location)
        except cngkb.LocationNotFound as error:
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
            raise cngkb.LessThanExpectError(existnum=neighbors.shape[0])


if __name__ == "__main__":
    geo = GeoGeneratorEn()
    # print(geo.city_usa)
    # print(geo.check_location('Boston'))
    # print(geo.check_location('Alabama'))
    print(geo.single_location_generator('Boston'))      # ['Billerica', 'Acton', 'Belmont']
    print(geo.single_location_generator('Alabama'))     # ['New Jersey', 'Florida', 'California']
