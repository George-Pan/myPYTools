# -*- coding: utf-8 -*-
import numpy as np

__author__ = 'Administrator'

'''
我记得在家里存过这个算法，不知道为什么没找到
先写个自己的，在参考大神写法

在写时修正的想法
1. 取消设置因重量而无法添加的项
* 原因：第二轮是在第一轮的基础上此时第一轮的排除项无意义
2. 再次评估selectable的位置
* 功能分析
# 保留ownStatus
# 再次内移selectable：每个
3.新增bgIdx
8/17
* 重新调整变量名等，以符合python规范
* 去除所有private变量：算法，装什么OO逼！
* bag在更换垫脚石时重新计算selectable：all-items(放大范围，靠下一次循环缩小)
* 经验：作为循环范围的列表不能在循环内发生变化
* 经验：python内一层冒号一个作用域
* 修正173行开始的tempIdxArray错误：应在循环内找到最大值再赋值，而不是直接赋值
* 修正每一行内包有满足的条件就立即放入：之后的包循环时，包内物品数量超过轮数（改为轮最后统一加）
* 修正compare_items_in_bag函数内由于无待选项，而误认“toselect=None”的状态，改为直接返回-1（否决权交给循环完所有可能垫脚石包之后）
* 现在结果：4,2,6,5,total price 165 → 错误！
* 经验：条件断点：查找多重循环中的bug的唯一捷径（限制到某一循环）
'''
# todo:问题推测：并未在最优结果的基础之上
# todo:尝试垫脚包只能是满了的包
# todo:对装不满的包，新增状态排除出循环（且不能作为垫脚包）

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

    def get_by_order(self, index):
        """
        :param index: 第n项
        :return:按重量排序后的第n项
        此处的order指依据重量从小到大排序
        """
        return self.idx[index]


class Bag:
    def __init__(self, weight, itemnum, bgidx):
        self.total_weight = weight
        self.total_price = 0
        self.weight = 0
        self.bag_idx = bgidx
        self.items = []  # 选出的物品
        self.is_full = False
        self.max_item = itemnum
        # 注意：这个范围一定大于最精确的筛选范围，且一直在减小
        self.selectable = range(itemnum)
        self.bag_selectable = range(self.bag_idx)  # 可能作为垫脚石的包的序号

    def add_item(self, item_idx, weight, price, changed_bag=None):
        if not self.is_full:
            if type(changed_bag) == "bag":
                self.weight = changed_bag.weight
                self.items = changed_bag.items
                self.total_price = changed_bag.totalPrice
                self.selectable = range(self.max_item)
                # 重新放大到除已选中项之外的最大范围
                # todo:待测试
                for x in self.items:
                    self.selectable.remove(x)
            self.weight += weight
            self.total_price += price
            self.items.append(item_idx)
            self.selectable.remove(item_idx)
            # 判断是否装满
            if self.weight == self.total_weight or len(self.selectable) == 0:
                self.selectable = []  # 统一清零，不然我也不太确定此时的状态
                self.is_full = True


def compare_items_in_bag(bag, items, toselect=None):
    """
    :param bag:bag类
    :param items: items类
    :return:满足重量要求的最贵的物品的编号
    注意：该方法只适用对当前包内的筛选
    """
    temp_index = -1
    # python 好像没有三元运算符（ext=toselect?toselect:items.idx）
    if type(toselect) == list:
        if len(toselect) == 0:  # 包没装满但无可选项状态
            return temp_index
        else:
            ext = toselect[:]  # 必须复制！！！！
    else:
        ext = items.idx
    for itemIdx in ext:
        if bag.weight + items.get_weight(itemIdx) <= bag.total_weight:
            if temp_index == -1:
                temp_index = itemIdx
            else:
                if items.get_price(temp_index) < items.get_price(itemIdx):  # 不取等号原因：同价值的东西尽量取轻的
                    temp_index = itemIdx
        else:
            bag.selectable.remove(itemIdx)
    return temp_index


def compare_items_among_bags(bag, items, target_bag):
    """
    :param bag:
    :param items:
    :param target_bag:
    :return:
    注意：该方法适用对垫脚石包的筛选
    """
    # todo:这里不能删元素
    # todo:这里
    temp_index = -1
    ext = target_bag.selectable[:]  # 必须复制！！！！
    for itemIdx in ext:
        if bag.weight + items.get_weight(itemIdx) <= target_bag.total_weight:
            if temp_index == -1:
                temp_index = itemIdx
            else:
                if items.get_price(temp_index) < items.get_price(itemIdx):  # 不取等号原因：同价值的东西尽量取轻的
                    temp_index = itemIdx
    return temp_index


if __name__ == '__main__':
    # todo：转为控制台输入
    iWeight = [35, 30, 60, 50, 40, 10, 25]
    iPrice = [10, 40, 30, 50, 35, 40, 30]
    bagWeight = 150

    # 生成items&系列bag
    objs = Items(iWeight, iPrice)
    bags = []
    bg_idx = 0
    for r in range(objs.get_weight(objs.get_by_order(0)), bagWeight + 1, objs.delta):
        bags.append(Bag(r, objs.sum, bg_idx))
        bg_idx += 1
    bg_idx = None

    # 包内的第ii件物品(第ii轮)
    for r in range(objs.sum):
        # 第一轮，不需要和前一轮做比较
        if r == 0:
            for bg in bags:
                temp_idx = compare_items_in_bag(bg, objs)
                bg.add_item(temp_idx, objs.get_weight(temp_idx), objs.get_price(temp_idx))
        else:
            item_to_add = []  # 记录每一轮要修改的所有包的值，格式为（包号，垫脚石包号，新增物品号）
            for bg in bags:
                tempIdxArray = []  # 存储待选项(背包号，物品号)
                if not bg.is_full:
                    # todo:直接在自己包内加东西
                    temp_idx = compare_items_in_bag(bg, objs, bg.selectable)
                    if temp_idx != -1:
                        tempIdxArray.append((bg.bag_idx, temp_idx))
                    # 其他包情况
                    if len(bg.bag_selectable) > 0:
                        ext_selectable = bg.bag_selectable[:]
                        for bag_index in ext_selectable:
                            temp_idx = compare_items_among_bags(bags[bag_index], objs, bg)
                            if temp_idx == -1:
                                bg.bag_selectable.remove(bag_index)
                            else:
                                tempIdxArray.append((bag_index, temp_idx))
                    if len(tempIdxArray) > 0:
                        temp_price = bg.total_price
                        temp_idx = -1
                        for temp in tempIdxArray:
                            if objs.get_price(temp[1]) + bags[temp[0]].total_price > temp_price:
                                temp_idx = temp  # 元组
                                temp_price = objs.get_price(temp[1]) + bags[temp[0]].total_price
                        if temp_idx != -1:
                            item_to_add.append((bg.bag_idx, temp_idx[0], temp_idx[1]))
                        else:
                            bg.is_full = True
            for record in item_to_add:
                if record[0] == record[1]:
                    bags[record[0]].add_item(record[2], objs.get_weight(record[2]), objs.get_price(record[2]))
                else:
                    bags[record[0]].add_item(record[2], objs.get_weight(record[2]), objs.get_price(record[2]),
                                             bags[record[1]])
    # 输出结果
    print "the bag of" + str(bagWeight) + " should contains:"
    string_out = ""
    for elm in bags[-1].items:
        string_out += str(elm + 1) + ","
    print string_out + "\n its total price is" + str(bags[-1].total_price) + "!\n"
