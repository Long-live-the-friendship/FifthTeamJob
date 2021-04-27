#!/usr/bin/env python
# coding: utf-8

# In[15]:


import csv
from selenium import webdriver
import time
import requests


# In[16]:


def getUrl(driver):
    urlList=[]
    for link in driver.find_elements_by_xpath('//a[contains(@class, "house-title")]'):
        #print(link)
        url=link.get_attribute('href')
        #print(url)
        urlList.append(url)
    #print(urlList)
    return urlList


# In[17]:


def get_data(driver):#提取数据

    infoDic = {}

    housingEstate = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[3]/ul/li[1]/div[2]/a').text # 小区
    infoDic["小区"] = housingEstate

    houseType = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/ul/li[1]/p').text# 户型
    infoDic["户型"] = houseType

    area = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/ul/li[2]/p').text # 面积
    infoDic["面积"] = area

    region = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[3]/ul/li[4]/div[2]/div/a[1]').text # 区域
    infoDic["区域"] = region

    totalPrice = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[1]/div[1]/span').text  # 总价
    infoDic["总价"] = totalPrice
    # print(total)

    unitPrice = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[1]/div[2]/p[1]').text  # 单价
    infoDic["单价"] = unitPrice

    school = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[3]/ul/li[3]/div[2]/a').text # 学校
    infoDic["学校"] = school

    ageLimit = driver.find_element_by_xpath('//*[@id="scrollto-1"]/div[3]/ul/li[3]/div[2]').text   # 年限
    infoDic["年限"] = ageLimit

    mortgage = driver.find_element_by_xpath('//*[@id="scrollto-1"]/div[3]/ul/li[5]/div[2]').text   # 抵押信息
    infoDic["抵押信息"] = mortgage

    houseID = driver.find_element_by_xpath('//*[@id="scrollto-1"]/div[3]/ul/li[7]/div[2]').text  # 房源编号
    infoDic["房源编号"] = houseID

    name = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[4]/div[1]/p/a').text   # 中介姓名
    infoDic["中介姓名"] = name

    telphone = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[4]/div[1]/div[4]/div[1]/span').text  # 中介电话
    infoDic["中介电话"] = telphone.replace(' ', '')
    
    saveImg(driver,housingEstate,houseType)
    
    return infoDic


# In[22]:


def saveImg(driver,title,houseType):

    img=driver.find_element_by_xpath('//*[@id="housePhotoWrap"]/ul/li[1]/a/img')
    img=img.get_attribute('data-src')
    #print(img)
    data = requests.get(img)
    #print(img)
    with open('./qfang/{}{}.jpg'.format(title,houseType), 'wb') as f:
        f.write(data.content)


# In[23]:


def saveData(infoList):
    header=['小区','户型','面积','区域','总价','单价','学校','年限','抵押信息','房源编号','中介姓名','中介电话']
    with open('211806229_qfang_selenium.csv', 'w', newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(infoList)


# In[26]:


if __name__ == '__main__':
    infoList = []
    url = 'https://shenzhen.qfang.com/sale'
    driver=webdriver.Chrome()#创建浏览器
    driver.get(url)#打开浏览器

    time.sleep(10)

    urlList=getUrl(driver)
    
    time.sleep(3)
    
    for url in urlList:
        driver.get(url)  # 打开浏览器
        time.sleep(5)
        infoList.append(get_data(driver))

    saveData(infoList)

