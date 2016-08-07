# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


# 注意：random.randint（）：含头且含尾
# 随机大写字母
def __rnduppercase():
    return chr(random.randint(65, 90))


# 随机大小写字母&阿拉伯数字
def __rndchar():
    charlist = range(48, 58) + range(65, 91) + range(97, 122)
    return chr(random.choice(charlist))


# 随机底图颜色
def __rndcolor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机字体颜色
def __rndcolor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


# 生成任意位数的验证码，但范围仅限大写字母
# 来源：廖雪峰python教程-pil
# 仅为纪念而保存
def rnduppercase(fignum, font, fontsize, unitsize):
    width = unitsize * fignum
    image = Image.new('RGB', (width, unitsize), (255, 255, 255))  # 创建底图白板
    font = ImageFont.truetype(font, fontsize)
    draw = ImageDraw.Draw(image)
    # 再次绘制底图
    for x in range(width):
        for y in range(unitsize):
            draw.point((x, y), fill=__rndcolor())
    # 输出文字
    for t in range(fignum):
        draw.text((60 * t + 10, 10), __rnduppercase(), font=font, fill=__rndcolor2())
    # 模糊
    image = image.filter(ImageFilter.BLUR)
    return image


'''
生成任意位数的验证码，字符包括大小写字母和阿拉伯数字，且字体有倾斜
特点：
    字体有倾斜，但无交叉
    字体大小不确定，但一定在图中
    底图为白色
返回值：生成的图（image）与对应值（string）
参数
    figNum:验证码中字符个数，int
    unitsize:每个字符所占空间pixel,int
    font:字体所在位置,string
'''
# todo:旋转后的字体可能相互覆盖
# todo:干扰底纹，背后随意曲线*1
# todo:字体如用透镜扭曲
# todo:排除1，i，I等干扰字体
def rndchar(fignum, unitsize, font="C:/Windows/Fonts/Arial.ttf", rotmaxangle=50, bgcolor=False):
    thetext = ""  # 存储随机产生的字符串
    theimage = Image.new('RGB', (unitsize * fignum, unitsize), (255, 255, 255))  # 创建底图白板
    # 输出文字
    if bgcolor:
        draw = ImageDraw.Draw(theimage)
        for x in range(unitsize * fignum):
            for y in range(unitsize):
                draw.point((x, y), fill=__rndcolor())
    for t in range(fignum):
        newtext = __rndchar()
        thetext += newtext.lower()
        fontsize = random.randint(int(unitsize * 0.2), int(unitsize * 0.4)) * 2  # 最小0.4，最大0.8倍外框
        thefont = ImageFont.truetype(font, fontsize)
        image = Image.new('RGBA', (unitsize, unitsize), (255, 255, 255, 0))  # 创建底图白板
        draw = ImageDraw.Draw(image)
        draw.text((random.randint(0, (unitsize - fontsize) / 2),
                   random.randint(0, (unitsize - fontsize) / 2)), newtext, font=thefont, fill=__rndcolor2())
        image = image.rotate(random.randint(-rotmaxangle, rotmaxangle))
        # image.show()
        theimage.paste(image, (t * unitsize, 0), image)
    return (theimage, thetext)


if __name__ == '__main__':
    defaultSize = 60  # 默认每个字符60*60（与字号相配）
    for i in range(5):
        newImage, newText = rndchar(5, defaultSize, bgcolor=True)
        newImage.save('code_' + str(i) + '.jpg', 'jpeg')
        print(newText)
