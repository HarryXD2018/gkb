# -*- coding: utf-8 -*-
# 这个程序需要制作一个包含全球地点名词的详细信息，结构为洲——>国家——>省——>市——>县 以及五大洋，通过这个数据结构完成相似地点名词集合的生成

import csv
import random
import gkberror
'''
Version 2.0

Date: 2020年1月13日

更新要求：
    一.在输入省 市 县 的时候 输出的结果我们希望有一定的相似相关性，比如说： 
    输入的是北京市，那么结果最好是中国的城市，例如上海，杭州，广州一类的，
    或者因为北京是首都 那么对应的输出也可以是各个国家的首都，比如华盛顿、伦敦、东京。
    这里的优化可以从两个方面进行，
    1.对数据库进行改进，例如对首都，省府进行分类标注。
    2. 在提取地名的时候在数据库中尽量提取相邻的地名 或者有相同父节点的地名，比如说输入是石家庄 
    那么石家庄的父节点是河北，那么结果最好是从河北省中的其他城市构成，如果不够数量就在河北省的相邻节点中继续寻找。

版本日志：
    1. capital_data.csv
    补充了capital_data.csv文件，增加了世界各国的首都、中国省份的省会和美国各州首府的信息
    2. 完成了对single_location附近周围的查找和生成，但是在拼音上是相邻近的
'''


class GeoGenerator:
    def __init__(self):
        # 将包含地点信息的文件载入
        location_data_cvs = csv.reader(open(r".\gkb_cn\location_data.csv",
                                            'r', encoding='UTF8'))
        self.location_data = [row for row in location_data_cvs]
        # [州，国家，省（州），市（郡），县（区）]

        nation_equi_cvs = csv.reader(open(r".\gkb_cn\nation_abbr_data.csv",
                                          'r', encoding='UTF8'))
        self.nation_abbr_data = [row for row in nation_equi_cvs]
        # [0] short term; [1] long term

        capital_data = csv.reader(open(r".\gkb_cn\capital_data.csv",
                                       'r', encoding='UTF8'))
        self.capital_data = [row for row in capital_data]
        # [亚洲,欧洲,非洲,美洲,澳洲,中国省会,美国首府]^T

    def parse_location(self, location):
        """
        :param location:
        :return parsed_location, location_catalog
        国家名称转化为缩写形式， 中华人民共和国  ->  中国
        Example 1：
            Input:  中华人民共和国
            Output: 中国，1
        Example 2:
            Input:  北京市
            Output: 北京，3
        Example 3:
            Input:  纽约州
            Output: 纽约，2
        """
        dic_2 = {"中华台北": "台湾",                      # 对个别情况进行处理
                 "中国台湾": "台湾",
                 "哥伦比亚特区": "哥伦比亚特区"}
        dic_3 = {"香港特别行政区": "香港",
                 "澳门特别行政区": "澳门",
                 "纽约": "纽约",
                 "华盛顿哥伦比亚特区": "华盛顿哥伦比亚特区",
                 "华盛顿特区": "华盛顿哥伦比亚特区"}
        if location in dic_2.keys():
            return dic_2[location], 2
        elif location in dic_3.keys():
            return dic_3[location], 3

        enum = [['省', 2], ['州', 2],
                ['市', 3], ['郡', 3],
                ['区', 4], ['县', 4]]
        for catalog in enum:                                # 对非国家名称进行处理
            p_type = catalog[0]
            if p_type in location:
                loc = location.replace(p_type, '')
                return loc, catalog[1]
        # ["洲", "国家", "省（州）", "市（郡）", "区（县）"]
        # [0,      1,      2,          3,         4]

        for nation_term in self.nation_abbr_data:               # 对国家缩写进行处理
            if location == nation_term[1]:
                return nation_term[0], 1
        return location, -1             # 没有修改

    def is_capital(self, location):
        for capitals in self.capital_data:
            if location in capitals:
                return True, self.capital_data.index(capitals)
        else:
            return False, None

    def check_location(self, location):
        """
        :param location:
        :return location_type, index_in_file:
        如果是通过遍历获得，index_in_file是其在location_data.csv的下表
        如果是通过parse_location()直接获得，或是洲、洋则返回 -1
        """
        continents = ["亚洲", "欧洲", "北美洲", "南美洲", "非洲", "大洋洲", "南极洲"]
        oceans = ["太平洋", "大西洋", "印度洋", "北冰洋", "南冰洋"]
        location_type = []
        index_in_file = -1
        if location in continents:
            print("洲 - {}".format(location))
            location_type.append("洲")
        elif location in oceans:
            print("海洋 - {}".format(location))
            location_type.append("海洋")
        else:
            (parsed_location, location_catalog) = self.parse_location(location)
            place_type_enum = ["洲", "国家", "省（州）", "市（郡）", "区（县）"]
            # if location_catalog != -1:
            #     print(place_type_enum[location_catalog], " - {}".format(location))
            #     location_type.append(place_type_enum[location_catalog])
            #     return parsed_location, location_type, -1
            # else:
            #     for location_item in self.location_data:
            #         if parsed_location not in location_item and location not in location_item:
            #             continue
            #         else:
            #             parsed_index = -1
            #             nature_index = -1
            #             for parsed_index in range(0, 5):
            #                 if location_item[parsed_index] == parsed_location:
            #                     break
            #             for nature_index in range(0, 5):
            #                 if location_item[nature_index] == location:
            #                     break
            #             location_type.append(place_type_enum[min(parsed_index, nature_index)])
            #             index_in_file = self.location_data.index(location_item)
            #             return parsed_location, location_type, index_in_file
            #     else:       # 无法查找该位置
            #         raise LocationNotFound(location)
            # if location_catalog != -1:
            #     print(place_type_enum[location_catalog], " - {}".format(location))
            #     location_type.append(place_type_enum[location_catalog])
            #     return parsed_location, location_type, -1

            for location_item in self.location_data:
                if parsed_location not in location_item and location not in location_item:
                    continue
                else:
                    parsed_index = -1
                    nature_index = -1
                    for parsed_index in range(0, 5):
                        if location_item[parsed_index] == parsed_location:
                            break
                    for nature_index in range(0, 5):
                        if location_item[nature_index] == location:
                            break
                    location_type.append(place_type_enum[min(parsed_index, nature_index)])
                    index_in_file = self.location_data.index(location_item)
                    return parsed_location, location_type, index_in_file
            else:       # 无法查找该位置
                raise gkberror.LocationNotFound(location)
        return location, location_type, index_in_file

    '''
    input：单个地点名词
    output：和该地点属于一类的名词list
    list中的元素可以包括input中的部分地点，但是都应该是同一个类型的地点名词，均为国家或者城市
    example：input 北京 output ["上海","深圳","广州"] 该词同类的词均为城市
            input  广东省 output ["福建省","河北省","山东省"] 该词同类的词均为省级行政区
            input  美国  output ["英国","中国","俄罗斯"]
    '''

    def single_location_generator(self, single_location, list_len=3):
        single_location_list = []
        parsed_location, location_type, location_file_index = self.check_location(single_location)
        location_type = location_type[0]
        if location_type == "洲":
            continents = ["亚洲", "欧洲", "北美洲", "南美洲", "非洲", "大洋洲", "南极洲"]
            single_location_list = random.sample(continents, 3)
        elif location_type == "海洋":
            oceans = ["太平洋", "大西洋", "印度洋", "北冰洋", "南冰洋"]
            single_location_list = random.sample(oceans, 3)
        else:
            # 对首都、省会、首府进行判断
            is_capital_args = self.is_capital(single_location)
            if is_capital_args[0]:
                aim_capitals = self.capital_data[is_capital_args[1]]
                while len(single_location_list) < list_len:
                    item = random.choice(aim_capitals)
                    if item in single_location_list \
                            or item == single_location \
                            or item == '':
                        continue
                    else:
                        single_location_list.append(item)
                print("Should finish", single_location_list)

            # 其它情况
            else:
                place_type_enum = ["洲", "国家", "省（州）", "市（郡）", "区（县）"]
                location_index = place_type_enum.index(location_type)       # location类型
                if location_file_index != -1:               # 通过遍历查找所得
                    while True:     # 向前搜索
                        neighbor = location_file_index - 1
                        if self.location_data[neighbor][location_index - 1] \
                                == self.location_data[location_file_index][location_index - 1]\
                                and self.location_data[neighbor][location_index - 1] != ''\
                                and self.location_data[neighbor][location_index] not in single_location_list\
                                and self.location_data[neighbor][location_index] \
                                != self.location_data[location_file_index][location_index]:
                            # 1. 父亲节点相同
                            # 2. 子节点不相同
                            # 3. 子节点不为空
                            # 4. 不可以重复
                            single_location_list.append(self.location_data[neighbor][location_index])
                            neighbor -= 1
                        else:
                            neighbor = location_file_index + 1
                            break
                        if len(single_location_list) == list_len:
                            break
                    while True:    # 向后搜索
                        if len(single_location_list) == list_len:
                            break
                        else:
                            # 父亲节点下的孩子不足，使用堂表兄弟节点补充
                            try:
                                item = self.location_data[neighbor]
                                if item[location_index] != self.location_data[location_file_index][location_index] \
                                        and item[location_index] not in single_location_list:
                                    single_location_list.append(item[location_index])
                                neighbor += 1
                            except IndexError:
                                item = random.choice(self.location_data)[location_index]
                                if item != '' and item not in single_location_list:
                                    single_location_list.append(item)
                else:               # 通过parse_location()得到 location_file_index == -1
                    pass

                while len(single_location_list) < list_len:
                    choice = random.choice(self.location_data)
                    if choice[location_index] is not "" and choice[location_index] not in single_location_list:
                        single_location_list.append(choice[location_index])
        return single_location_list

    '''
        input：多个地点的list  ["上海","深圳","广州"]
        output：和该地点属于一类的多个list组成的list [ ["北京","西安","兰州"] ["福州","深圳","广州"] ["南京","深圳","杭州"] ]
        这里output包括的三个list中 每个list都不相同，可以包括input中的部分地点，但是都应该是同一个类型的地点名词，均为国家或者城市
        example：input 北京 output ["上海","深圳","广州"] 该词同类的词均为城市
    '''

    def multi_location_generator(self, multi_location):
        multi_location_list = []
        functional_multi_location_list = []
        for location in multi_location:
            try:
                self.check_location(location)
            except gkberror.LocationNotFound as lnf_except:
                print(lnf_except.args)
            else:
                functional_multi_location_list.append(location)
        if len(functional_multi_location_list) == 0:                # input没有一个满足要求的地址元素
            raise gkberror.LocationNotFound("输入列表中满足要求的地址元素")
        else:
            for location in functional_multi_location_list:
                multi_location_list.append(self.single_location_generator(location, list_len=len(multi_location)))
            if len(functional_multi_location_list) != len(multi_location):
                diff = len(multi_location) - len(functional_multi_location_list)
                print("根据符合要求的地址，补充{}项地址元素".format(diff))
                for i in range(0, diff):
                    location = random.choice(functional_multi_location_list)
                    multi_location_list.append(self.single_location_generator(location, list_len=len(multi_location)))
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
    # print(geo.check_location("海淀"))
    # print(geo.is_capital("北京"))
    # print(geo.single_location_generator("马萨诸塞州"))
    # print(geo.single_location_generator("福岛"))
    # print(geo.single_location_generator("美利坚合众国"))
    print(geo.single_location_generator("上海市"))
    print(geo.single_location_generator("邢台"))
    print(geo.single_location_generator("中国"))
    print(geo.multi_location_generator(["马萨诸塞州", "福岛", "美利坚合众国", "海淀区", "中国"]))
    # print(geo.multi_location_generator(["马萨诸塞州", "加利福尼亚州", "幻想乡", "曲阳县"]))
    # 这个世界上当然是没有幻想乡啦
