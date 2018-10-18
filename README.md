# 电影天堂爬取

## 注意
1. requests.text结果出现乱码
    * 原因：requests库默认会用自己猜测的编码方式将抓取的网页解码，存储到text属性
    在电影天堂里，网页不规范，编码方式不对，查看meta charset 为gb2312，产生乱码
2. test.py用来测试，发现第三页出现问题
3. 解决方法：我们不用管乱码部分，要的是详情页的链接，所以直接写request.text就好了
4. 问题：演员和简介栏都有问题，不规范，需要再次整理数据
5. 部分电影没有截图screenshot，需要if判断
## 英文
* zoom 放大
