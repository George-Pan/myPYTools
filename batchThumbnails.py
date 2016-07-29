# -*- coding: utf-8 -*-
# 作用：批量生成不同的缩略图
__author__ = 'George Pan'
import os
from PIL import Image
# PIL version'1.1.7'== PILLOW_VERSION = '2.8.2'
# 缩略图撑满要求尺寸且且不变形
def thumbnailByFulfill(rootDir,sizeRatio,outDir):
    for pic in os.listdir(rootDir):
        if pic[pic.rfind('.'):].lower() == '.jpg':
            path = os.path.join(rootDir, pic)
            im = Image.open(path)
            #生成缩略图等比例放大框
            ratioWidth=1.0*im.size[0]/sizeRatio[0]
            ratioHeight=1.0*im.size[1]/sizeRatio[1]
            centerPoint=(im.size[0]/2,im.size[1]/2)
            ratioReal=min(ratioWidth,ratioHeight)
            newHalfWidth=int(ratioReal*sizeRatio[0]/2)
            newHalfHeight=int(ratioReal*sizeRatio[1]/2)
            box=(centerPoint[0]-newHalfWidth,centerPoint[1]-newHalfWidth,centerPoint[0]+newHalfWidth,centerPoint[1]+newHalfHeight)
            # 生成新图
            region = im.crop(box)#left, upper, right, and lower pixel
            thumb=region.resize(sizeRatio)
            thumb.save(os.path.join(outDir, pic))#默认以原格式保存

#原图最大高/宽满足要求尺寸（缩略图整图小于要求尺寸）
def thumbnailByMaxBorder(rootDir,sizeRatio,outDir):
    for pic in os.listdir(rootDir):
        if pic[pic.rfind('.'):].lower() == '.jpg':
            path = os.path.join(rootDir, pic)
            im = Image.open(path)
            im.thumbnail(sizeRatio) #自带算法
            im.save(os.path.join(outDir, pic))#默认以原格式保存

# 缩略图撑满要求尺寸且且不变形(正方形简化版)
def thumbnailToSqure(rootDir,sizeRatio,outDir):
    for pic in os.listdir(rootDir):
        if pic[pic.rfind('.'):].lower() == '.jpg':
            path = os.path.join(rootDir, pic)
            im = Image.open(path)
            #生成缩略图等比例放大框
            width = int(im.size[0])
            height = int(im.size[1])
            if (width > height):
                dx = width - height
                box = (dx / 2, 0, height + dx / 2,  height)
            else:
                dx = height - width
                box = (0, dx / 2, width, width + dx / 2)
            # 生成新图
            region = im.crop(box)#left, upper, right, and lower pixel
            thumb=region.resize(sizeRatio)
            thumb.save(os.path.join(outDir, pic))#默认以原格式保存

if __name__ == '__main__':
    '''这里输入的参数是图片文件的位置'''
    mySize=(90,92)
    thumbnailByFulfill("C:/temp/testJSP/web/images",mySize,"C:/temp/testJSP/web/thumbnails")