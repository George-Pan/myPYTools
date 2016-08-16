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
'''


class items:
    def __init__(self, weight, price):
        if len(weight) != len(price):
            return
        self.weights = weight
        self.prices = price
        self.idx = np.argsort(weight)
        self.sum = len(weight)  # 数据个数
        # todo:合理性？
        tWeight = np.array(self.weights)[self.idx]
        self.delta = min(tWeight[1:] - tWeight[:-1])

    def getWeight(self, index):
        return self.weights[index]

    def getPrice(self, index):
        return self.prices[index]

    # todo:换个合适的名称？
    def getNext(self, index):
        '''
        :param index: 第n项
        :return:按重量排序后的第n项
        '''
        return self.idx[index]


class bag:
    def __init__(self, weight, itemnum, bgidx):
        self.totalWeight = weight
        self.totalPrice = 0
        self.weight = 0
        self.bgidx = bgidx
        self.items = []  # 选出的物品
        self._ownStatus = True
        # 注意：这个范围一定大于最精确的筛选范围，且一直在减小
        self._selectable = range(itemnum)
        self.bgselectable = range(self.bgidx)  # 可能作为垫脚石的包的序号

    def addItem(self, itemidx, weight, price, changedbag=None):
        if self._ownStatus:
            if type(changedbag) == "bag":
                self.weight = changedbag.weight
                self.items = changedbag.items
                self.totalPrice = changedbag.totalPrice
            self.weight += weight
            self.totalPrice += price
            self.items.append(itemidx)
            self.deleteselectable(itemidx)
            # 判断是否装满
            if self.weight == self.totalWeight or len(self._selectable) == 0:
                self._selectable = []  # 统一清零，不然我也不太确定此时的状态
                self._ownStatus = False

    def deleteselectable(self, index):
        self._selectable.remove(index)

    def isFull(self):
        return not self._ownStatus

    def getSelectable(self):
        return self._selectable


def compareitems(bag, items, toselect=None):
    '''
    :param bags:bag类的集合
    :param items: items类
    :return:满足重量要求的最贵的物品的编号
    注意：该方法只适用第一次筛选
    下并未依据已有的bag.selectablelai
    '''
    tIdx = -1
    # python 好像没有三元运算符（ext=toselect?toselect:items.idx）
    if toselect:
        ext = toselect
    else:
        ext = items.idx
    for itemIdx in ext:
        if bag.weight + items.getWeight(itemIdx) <= bag.totalWeight:
            if tIdx == -1:
                tIdx = itemIdx
            else:
                if items.getPrice(tIdx) < items.getPrice(itemIdx):  # 不取等号原因：同价值的东西尽量取轻的
                    tIdx = itemIdx
        else:
            bag.deleteselectable(itemIdx)
    return tIdx


def compareitems2(bag, items, targetbag):
    '''

    :param bag:
    :param items:
    :param targetbag:
    :return:
    '''
    # todo:这里不能删元素
    # todo:这里
    tIdx = -1
    for itemIdx in targetbag.getSelectable():
        if bag.weight + items.getWeight(itemIdx) <= targetbag.totalWeight:
            if tIdx == -1:
                tIdx = itemIdx
            else:
                if items.getPrice(tIdx) < items.getPrice(itemIdx):  # 不取等号原因：同价值的东西尽量取轻的
                    tIdx = itemIdx
    return tIdx


if __name__ == '__main__':
    # todo：转为控制台输入
    iWeight = [35, 30, 60, 50, 40, 10, 25]
    iPrice = [10, 40, 30, 50, 35, 40, 30]
    bagWeight = 150

    # 生成items&系列bag
    objs = items(iWeight, iPrice)
    bags = []
    for r in range(objs.getWeight(objs.getNext(0)), bagWeight + 1, objs.delta):
        bgIdx = (r - objs.getWeight(objs.getNext(0))) / objs.delta  # todo:待测试
        bags.append(bag(r, objs.sum, bgIdx))  # todo:待测试

    # 包内的第ii件物品(第ii轮)
    for r in range(objs.sum):
        # 第一轮，不需要和前一轮做比较
        if r == 0:
            for bg in bags:
                tempIdx = compareitems(bg, objs)
                if tempIdx != -1:
                    bg.addItem(tempIdx, objs.getWeight(tempIdx), objs.getPrice(tempIdx))
        else:
            # bagToFill = range(len(bags))  # 还未装满的
            # bagForFill = range(len(bags))  # 可能成为装满其他包的解决方案的包
            for bg in bags:
                if not bg.isFull():
                    tempIdxArray = []  # 存储待选项(背包号，物品号)
                    # todo:直接在自己包内加东西
                    tempIdx = compareitems(bg, objs, bg.getSelectable())
                    if tempIdx != -1:
                        tempIdxArray.append((bg.bgidx, tempIdx))
                # 其他包情况
                for bgIdx in bg.bgselectable:
                    tempIdx = compareitems2(bags[bgIdx], objs, bg)
                    if tempIdx == -1:
                        bg.bgSelectable.remove(bgIdx)
                    else:
                        tempIdxArray.append((bgIdx, tempIdx))
                if len(tempIdxArray) > 0:
                    tempPrice = bg.totalPrice
                    for temp in tempIdxArray:
                        if objs.getPrice(temp[1]) + bags[temp[0]].totalPrice > tempPrice:
                            if bg is bags[temp[0]]:
                                bg.addItem(temp[1], objs.getWeight(temp[1]), objs.getPrice(temp[1]))
                            else:
                                bg.addItem(temp[1], objs.getWeight(temp[1]), objs.getPrice(temp[1]), bags[temp[0]])
    # 输出结果
    print "the bag of" + str(bagWeight) + " should contains:"
    for elm in bags[-1].items:
        print str(elm + 1) + ","
    print "\n its total price is" + str(bags[-1].totalPrice) + "!\n"
