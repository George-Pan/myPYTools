# -*- coding: utf-8 -*-
import numpy as np

__author__ = 'Administrator'

'''
我记得在家里存过这个算法，不知道为什么没找到
先写个自己的，在参考大神写法

在写时修正的想法
1. 取消设置因重量而无法添加的项
* 原因：第二轮是在第一轮的基础上此时第一轮的排除项无意义
# 保留ownStatus
#

'''


class items:
    def __init__(self, weight, price):
        if len(weight) != len(price):
            print "输入数据个数不匹配"
            return
        self.weights = weight
        self.prices = price
        self.idx = np.argsort(weight)
        self.sum = len(weight)  # 数据个数
        # todo:合理性？
        tWeight = np.array(self.weights)[self.idx]
        self.delta=min(tWeight[1:]-tWeight[:-1])

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
    def __init__(self, weight, itemnum):
        self.totalWeight = weight
        self.totalPrice = 0
        self.weight = 0
        self.items = []  # 选出的物品
        self._ownStatus = True
        # 注意：这个范围一定大于最精确的筛选范围，且一直在减小
        self._selectable = range(itemnum)

    def addItem(self, itemidx, weight, price):
        if self._ownStatus:
            self.weight += weight
            self.totalPrice += price
            self.items.append(itemidx)
            self.deleteselectable(itemidx)
            # 判断是否装满
            if self.weight == self.totalWeight or len(self._selectable) == 0:
                self._ownStatus = False

    def deleteselectable(self, index):
        self._selectable.remove(index)


def comapreitems(bag, items):
    '''
    :param bags:bag类的集合
    :param items: items类
    :return:满足重量要求的最贵的物品的编号
    '''
    tIdx = -1
    for itemIdx in items.idx:
        if bag.weight + items.getWeight(itemIdx) <= bag.totalWeight:
            if tIdx == -1:
                tIdx = itemIdx
            else:
                if items.getPrice(tIdx) < items.getPrice(itemIdx):
                    tIdx = itemIdx
        else:
            bag.deleteselectable(itemIdx)
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
        bags.append(bag(r, objs.sum))

    # 包内的第ii件物品(第ii轮)
    for r in range(0, objs.sum):
        # 第一轮，不需要和前一轮做比较
        if r == 0:
            for bg in bags:
                tempIdx = comapreitems(bg, objs)
                if tempIdx != -1:
                    bg.addItem(tempIdx, objs.getWeight(tempIdx), objs.getPrice(tempIdx))
        else:
            bagToFill = range(len(bags))  # 还未装满的
            bagForFill = range(len(bags))  # 可能成为装满其他包的解决方案的包
            for bg in bags:
                tempIdx = []

                tempIdx = [(-1, -1)]  # 存储待选项(背包号，物品号)
