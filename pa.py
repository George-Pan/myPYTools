# -*- coding: utf-8 -*-
import numpy as np

__author__ = 'Administrator'

'''
问题描述
    有N件物品和一个承重为C的背包，每件物品的重量是wi,价值是pi
    求解将哪几件物品装入背包可使这些物品在重量总和不超过C的情况下价值总和最大
问题核心要点
    在选中的这k个元素里拿掉最后那个元素，前面剩下的元素依然构成一个最佳解
我的算法中犯错过的点
    1.最佳子解的确定：必要条件是该子包恰好被装满
        不然依据我优先依据重量排序的前提，等价于“重量轻优先的贪婪算法”
    2.装满时的处理：装满也要继续循环+垫脚包的必要条件是包内件数与轮数相同的最佳子解
        典型点：现在案例中的50包（第1轮时最优50（第4件），第2轮时最优80（第6，2件））
        无法装满的判定：无论自身还是垫脚包都无法找到能再装入的项
        无法装满的处理：废弃
    3.实际放入包的时间：所有包在该轮都确定方案以后
        不然，2包可能用1包垫脚，3包再用2包垫脚（3包就会有+2物品数）
    4.去除计算量设计
        频繁修改的设计：bag.selectable
            for:去除因重量超过总重而不可能放入的选项
            against:第二轮是在第一轮的基础上此时第一轮的排除项无意义
            for：在更换垫脚石时重新计算selectable：all-items(放大范围，靠下一次循环缩小)
            for: 第二轮的范围一定比第一轮小（那在第二轮时继续减少就好）
            final against:即使装满（selectable=[]）,垫脚包也仍有可选项→selectable只能为自己服务→不如用总数-bag.items

我的算法特点
    1.去除所有private变量：算法，装什么OO逼！
    2.该方法能输出所有最优子解

待优化项
* 能否在程序开始时就明确能装满的包（或者比当前方法更好的方法）
* 能否用数组/矩阵的概念优化算法
'''


class Items:
    def __init__(self, weight, price):
        if len(weight) != len(price):
            return
        self.weights = weight
        self.prices = price
        self.idx = np.argsort(weight)
        self.sum = len(weight)  # 数据个数
        # todo:合理性？
        temp_weight = np.array(self.weights)[self.idx]
        self.delta = min(temp_weight[1:] - temp_weight[:-1])

    def get_weight(self, index):
        return self.weights[index]

    def get_price(self, index):
        return self.prices[index]


class Bag:
    def __init__(self, weight, bgidx):
        self.total_weight = weight
        self.total_price = 0
        self.weight = 0
        self.bag_idx = bgidx
        self.items = []  # 选出的物品
        self.is_full = False
        self.is_useful = True  # 不能被装满的包为False

    def add_item(self, item_idx, item_collection, changed_bag=None):
        if isinstance(changed_bag, Bag):
            self.weight = changed_bag.weight
            self.items = changed_bag.items[:]
            self.total_price = changed_bag.total_price
        self.weight += item_collection.get_weight(item_idx)
        self.total_price += item_collection.get_price(item_idx)
        self.items.append(item_idx)
        # 判断是否装满
        if self.weight == self.total_weight:
            self.is_full = True  # 唯一修改is_full的地方


def compare_items(bag, items, target_bag=None):
    """
    :param bag:bag类
    :param items: items类
    :return:满足重量要求的最贵的物品的编号
    注意：该方法只适用对当前包内的筛选
    """
    if isinstance(target_bag, Bag):
        target = target_bag
    else:
        target = bag
    temp_index = -1
    for itemIdx in items.idx:
        if itemIdx not in bag.items:
            if bag.weight + items.get_weight(itemIdx) <= target.total_weight:
                if temp_index == -1:
                    temp_index = itemIdx
                else:
                    if items.get_price(temp_index) < items.get_price(itemIdx):  # 不取等号原因：同价值的东西尽量取轻的
                        temp_index = itemIdx
            else:
                break  # 已经排序，超过的话后面都没可能
    return temp_index


def solve(weight_array, value_array, bag_weight):
    """
    :param weight_array:重量列表
    :param value_array: 价值列表
    :param bag_weight: 包重
    :return:包列表
    """
    # 生成items&系列bag
    objs = Items(weight_array, value_array)
    bgs = []
    bg_idx = 0
    for r in range(objs.get_weight(objs.idx[0]), bag_weight + 1, objs.delta):
        bgs.append(Bag(r, bg_idx))
        bg_idx += 1
    bg_idx = None

    # 包内的第ii件物品(第ii轮)
    for r in range(objs.sum + 1):
        item_to_add = []  # 记录每一轮要修改的所有包的值，格式为（包号，垫脚石包号，新增物品号）
        for bg in bgs:
            temp_idx_array = []  # 存储待选项(背包号，物品号)
            if bg.is_useful:
                # 直接在自己包内加东西
                temp_idx = compare_items(bg, objs)
                if temp_idx != -1:
                    temp_idx_array.append((bg.bag_idx, temp_idx))
                if r != 0:  # 其他包情况
                    for ii in range(bg.bag_idx):
                        if bgs[ii].is_full and len(bgs[ii].items) == r:
                            temp_idx = compare_items(bgs[ii], objs, bg)
                            if temp_idx != -1:
                                temp_idx_array.append((ii, temp_idx))
                if len(temp_idx_array) > 0:
                    temp_price = bg.total_price
                    temp_idx = -1
                    for temp in temp_idx_array:
                        if objs.get_price(temp[1]) + bgs[temp[0]].total_price > temp_price:
                            temp_idx = temp  # 元组
                            temp_price = objs.get_price(temp[1]) + bgs[temp[0]].total_price
                    if temp_idx != -1:
                        item_to_add.append((bg.bag_idx, temp_idx[0], temp_idx[1]))
                elif not bg.is_full:
                    bg.is_useful = False
        for record in item_to_add:
            if record[0] == record[1]:
                bgs[record[0]].add_item(record[2], objs)
            else:
                bgs[record[0]].add_item(record[2], objs, bgs[record[1]])
    return bgs


if __name__ == '__main__':

    # todo：转为控制台输入
    iWeight = [35, 30, 60, 50, 40, 10, 25]
    iPrice = [10, 40, 30, 50, 35, 40, 30]
    bagWeight = 150
    # iWeight = [10,20,30]
    # iPrice = [60,100,120]
    # bagWeight = 50

    bags = solve(iWeight, iPrice, bagWeight)
    # 输出结果
    print "The useful bags I have: "
    string_out = ""
    for bag in bags:
        if bag.is_useful:
            string_out += "Bag" + str(bag.total_weight) + ":"
            for i in bag\
                    .items:
                string_out += str(i + 1) + ","
            string_out += "\nits total price is " + str(bag.total_price) + "!\n"
    print string_out
