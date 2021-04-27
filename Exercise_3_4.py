#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pymysql
from selenium import webdriver
import time
import json

infoList = []
urlList = []

connectPool = pymysql.connect(  # 连接数据库
    host="115.159.41.241",
    user="user211806229",
    password="211806229",
    database="db211806229",
    charset="utf8")
cursor = connectPool.cursor()


def opmysql(data):  # 插入数据库
    # print(".............")
    table = 'lianjia'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
        cursor.execute(sql, tuple(data.values()))
        connectPool.commit()
    except:
        connectPool.ping(True)


def search():
    urlList = []
    driver = webdriver.Chrome()  # 创建浏览器
    driver.get("https://fz.lianjia.com/chengjiao/")  # 打开浏览器
    time.sleep(2)
    #driver.find_element_by_xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div[1]/a[7]').click()  # 点击连江
    #time.sleep(2)
    totalPage = json.loads(driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[5]/div[2]/div').get_attribute('page-data')).get('totalPage')
    print(totalPage)
    print("开始爬取")
    for page in range(totalPage + 1):
        print('https://fz.lianjia.com/chengjiao/pg/' + str(page))
        for link in driver.find_elements_by_xpath('//ul[@class="listContent"]/li/a'):
            url = link.get_attribute('href')
            #print(url)
            urlList.append(url)
            
    print(len(urlList))
    
    i = 1
    for url in urlList:
        print("正在爬取第" + str(i) + "条")
        driver.get(url)  # 打开浏览器
        time.sleep(5)
        get_data(driver)
        i = i + 1


def getUrl(driver):
    for link in driver.find_elements_by_xpath('//ul[@class="listContent"]/li/a'):
        # print(link)
        url = link.get_attribute('href')
        #print(url)
        urlList.append(url)
    # print(urlList)


def get_data(driver):  # 提前数据

    infoDic = {}
    house = driver.find_element_by_xpath('/html/body/div[4]/div').text.split()  # 房子信息
    # print(house)

    infoDic["小区"] = house[0]

    infoDic["户型"] = house[1]

    infoDic["面积"] = house[2].split('米')[0] + "米"

    totalPrice = driver.find_element_by_xpath('/html/body/section[1]/div[2]/div[2]/div[1]/span/i').text  # 总价
    infoDic["总价"] = totalPrice + "万"
    # print(total)

    unitPrice = driver.find_element_by_xpath('/html/body/section[1]/div[2]/div[2]/div[1]/b').text  # 单价
    infoDic["单价"] = unitPrice + "元/平"

    transactionTime = driver.find_element_by_xpath('/html/body/div[4]/div/span').text.split()  # 成交日期
    infoDic["成交时间"] = transactionTime[0]

    period = driver.find_element_by_xpath('/html/body/section[1]/div[2]/div[2]/div[3]/span[2]/label').text  # 成交周期
    infoDic["成交周期"] = period + "天"

    price = driver.find_element_by_xpath('/html/body/section[1]/div[2]/div[2]/div[3]/span[1]/label').text  # 挂牌价格
    infoDic["挂牌价格"] = price + "万"

    orientation = driver.find_element_by_xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[7]').text  # 朝向
    infoDic["房屋朝向"] = orientation.split('向')[1].replace(' ', '')

    floor = driver.find_element_by_xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[2]').text  # 所在楼层
    infoDic["所在楼层"] = floor.split('所在楼层')[1]

    years = driver.find_element_by_xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[8]').text  # 建成年代
    infoDic["建成年代"] = years.split('代')[1]

    structure = driver.find_element_by_xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[10]').text  # 建筑结构
    infoDic["建筑结构"] = structure.split('建筑结构')[1]

    lift = driver.find_element_by_xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[13]').text  # 配备电梯
    infoDic["配备电梯"] = lift.split('梯')[1]

    proportion = driver.find_element_by_xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li[12]').text  # 梯户比例
    infoDic["梯户比例"] = proportion.split('例')[1]

    listingTime = driver.find_element_by_xpath('//*[@id="introduction"]/div[1]/div[2]/div[2]/ul/li[3]').text  # 挂牌时间
    infoDic["挂牌时间"] = listingTime.split('间')[1]

    power = driver.find_element_by_xpath('//*[@id="introduction"]/div[1]/div[2]/div[2]/ul/li[2]').text  # 交易权属
    infoDic["交易权属"] = power.split('属')[1]

    infoList.append(infoDic)
    print(infoDic)
    opmysql(infoDic)
 

if __name__ == '__main__':  # 当程序执行时调用函数
    search()
    connectPool.close()
    print("爬取完成")


# In[ ]:




