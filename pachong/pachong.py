import requests
import re
import csv


def getHTML():
    name = input('请输入爬取商品的名字:')
    start_url = 'https://s.taobao.com/search?q={}&s='.format(name)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    }
    path = r'C:\Users\ZB\Desktop\新建文件夹\cookie.txt'
    with open(path, 'r')as f:
        mycookies = f.read()
    mycookies = mycookies.split(';')
    cookies = {}
    for cookie in mycookies:
        name, value = cookie.strip().split('=', 1)
        cookies[name] = value
    print(cookies)
    pages = input('请输入爬取的商品页数:')
    goods = ''
    for i in range(int(pages)):
        url = start_url + str(i * 44)
        r = requests.get(url, headers=header, cookies=cookies, timeout=60)
        r.encoding = r.apparent_encoding
        goods += r.text
    return goods

def findMS(html):
    print('=' * 20, '正在爬取商品信息', '=' * 20, '\n')
    marketnames = re.findall('"nick":"(.*?)"', html)
    titles = re.findall('"raw_title":"(.*?)"', html)
    prices = re.findall('"view_price":"(.*?)"', html)
    citys = re.findall('"item_loc":"(.*?)"', html)
    pays = re.findall('"view_sales":"(.*?)"', html)
    data = []

    try:
        for i in range(len(titles)):
            data.append([marketnames[i], titles[i], prices[i], citys[i], pays[i]])
        if data == '':
            print('=' * 20, '暂无此商品信息', '=' * 20, '\n')
            return data
        print('=' * 20, '爬取成功', '=' * 20, '\n')

    except:
        print('异常，爬取中断')
    return data


def download(data):
    print('=' * 20, '正在保存商品信息', '=' * 20, '\n')
    path = r'C:\Users\ZB\Desktop\新建文件夹\good.csv'
    try:
        f = open(path, "w", newline="")
        writer = csv.writer(f)
        writer.writerow(['name', 'good', 'price', 'local', 'people'])
        writer.writerows(data)
        print('=' * 20, '保存成功', '=' * 20, '\n')
    except:
        print('保存失败')
    f.close()

def saveSql(data):

    import pymysql  # 调用模块
    db = pymysql.connect(
        host="115.159.41.241",
        user="user211806159",
        password="211806159",
        database="db211806159",
        charset="utf8")  # 打开数据库连接
    cursor = db.cursor()  # 获取操作游标
    for da in data:
        print(da)
        sql = "INSERT INTO taobao (name,introduce,price,local,people) VALUES ('%s','%s','%s','%s','%s')" % (
        da[0], da[1], da[2], da[3], da[4])
        demo = cursor.execute(sql)
        db.commit()  # 提交mysql语句

    return 0



def main():
    html = getHTML()
    data = findMS(html)
    saveSql(data)
    download(data)


if __name__ == "__main__":
    main()