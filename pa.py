# -*- coding: utf-8 -*-

__author__ = 'Administrator'

'''
我记得在家里存过这个算法，不知道为什么没找到
先写个自己的，在参考大神写法

在写时修正的想法
1. 取消设置因重量而无法添加的项
* 原因：第二轮是在第一轮的基础上此时第一轮的排除项无意义

'''


class item:
    def __init__(self, weight, price):
        self.weight = weight
        self.price = price


class bag:
    def __init__(self, weight, itemnum):
        self.totalweight = weight
        self.totalprice = 0
        self.weight = 0
        self.items = []  # 选出的物品

    def additem(self, itemidx, items):
        self.weight += items[itemidx].weight
        self.totalprice += items[itemidx].price
        self.items.append(itemidx)




if __name__ == '__main__':
    # todo：转为控制台输入
    iWeight = (35, 30, 60, 50, 40, 10, 25)
    iPrice = (10, 40, 30, 50, 35, 40, 30)
    # todo:验证iWeight与iPrice 个数一致
    bagWeight = 150

    # todo:考虑必要性
    minWeight = min(iWeight)
    # python帮我省掉的代码
    # deltaWeight=iWeight[0]
    # for ii in range(len(iWeight)-1):
    #     if iWeight[ii]>iWeight[ii+1]:
    #         deltaWeight=iWeight[ii+1]

    # todo: 计算最小的Δw
    # deltaWeight=min(iWeight) #如果10，12，20，21，22会有影响?
    deltaWeight = 5

    # 生成系列item
    items = []
    for ii in range(len(iWeight)):
        items.append(item(iWeight[ii], iPrice[ii]))
    # 生成系列bag
    bags = []
    for ii in range(deltaWeight, bagWeight, deltaWeight):
        tempBag = bag(ii, len(iWeight))

    # 包内的第ii件物品(第ii轮)
    for ii in range(1,len(items)):
        tempIdx = -1  # 存储待选项
        tempPrice=0
        # 第一轮，不需要和前一轮做比较
        # todo:去啰嗦？
        if ii == 1:
            for bg in bags:
                # todo:这里没写完
                for jj in range(len(items)):
                    if bg.weight+items[jj]<bg.totalweight:
                        if tempIdx == -1:
                            tempIdx = jj
                            tempPrice=items[jj].price
                        else:
                            if tempPrice < items[jj].price:
                                tempIdx = jj
                                tempPrice=items[jj].price
                if tempIdx != -1:
                    bg.additem(tempIdx,items)
        else:
