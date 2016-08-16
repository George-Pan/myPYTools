# -*- coding: utf-8 -*-
import numpy as np

__author__ = 'Administrator'

'''
我记得在家里存过这个算法，不知道为什么没找到
先写个自己的，在参考大神写法

在写时修正的想法
1. 取消设置因重量而无法添加的项
* 原因：第二轮是在第一轮的基础上此时第一轮的排除项无意义

'''


class items:
    def __init__(self, weight, price):
        if len(weight) != len(price):
            print "输入数据个数不匹配"
            return
        self.weights = weight
        self.prices = price
        self.idx = np.argsort(weight)

    def getWeight(self, index):
        return self.weights[index]

    def getPrice(self, index):
        return self.prices[index]
    def getNext(self,index):
        '''
        :param index: 第n项
        :return:按重量排序后的第n项
        '''
        return self.idx[index]

class bag:
    def __init__(self, weight, itemnum, mindelta, maxdelta):
        self.totalWeight = weight
        self.totalPrice = 0
        self.weight = 0
        self.items = []  # 选出的物品
        # self.minDelta = mindelta
        # self.maxDelta = maxdelta
        # self.ownStatus = True  # 是否还能装下任何其他东西
        # self.addStatus = True  # 是否还能为更大重量的包提供解决方案

    def addItem(self, itemidx, _items):
        if self.ownStatus:
            self.weight += _items.getWeight(itemidx)
            self.totalPrice += _items.getPrice(itemidx)
            self.items.append(itemidx)
            # if self.totalWeight-self.weight<self.minDelta:
            #     self.ownStatus=False


if __name__ == '__main__':
    # todo：转为控制台输入
    iWeight = [35, 30, 60, 50, 40, 10, 25]
    iPrice = [10, 40, 30, 50, 35, 40, 30]
    bagWeight = 150

    # todo:考虑必要性
    # minWeight = min(iWeight)
    # maxWeight = max(iWeight)
    # python帮我省掉的代码
    # deltaWeight=iWeight[0]
    # for ii in range(len(iWeight)-1):
    #     if iWeight[ii]>iWeight[ii+1]:
    #         deltaWeight=iWeight[ii+1]

    # todo: 计算最小的Δw
    # deltaWeight=min(iWeight) #如果10，12，20，21，22会有影响?
    deltaWeight = 5

    # 生成系列item
    objs = items(iWeight, iPrice)

    # 生成系列bag
    bags = []
    for round in range(deltaWeight, bagWeight + 1, deltaWeight):
        tempBag = bag(round, len(iWeight))

    # 包内的第ii件物品(第ii轮)
    for round in range(1, len(items)):
        # 第一轮，不需要和前一轮做比较
        # todo:去啰嗦？
        if round == 1:
            for bg in bags:
                tempIdx = -1
                # todo:这里没写完
                for itemIdx in range(len(items)):
                    if bg.weight + items[itemIdx] < bg.totalweight:
                        if tempIdx == -1:
                            tempIdx = itemIdx
                        else:
                            if objs.getPrice(tempIdx) < items[itemIdx].price:
                                tempIdx = itemIdx
                if tempIdx != -1:
                    bg.additem(tempIdx, items)
        else:
            for bgIdx in range(len(bags)):
                if not bg.bags[bgIdx].ownStatus:
                    tempIdx = [(-1, -1)]  # 存储待选项(背包号，物品号)
