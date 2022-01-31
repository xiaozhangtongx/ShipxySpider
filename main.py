import random  # 导入requests库
import time
import csv  # 导出为csv文档
import requests
from fake_useragent import UserAgent  # 导入随机获取UA的库

# 船讯网系统主页，用来获得cookie
main_url = 'http://www.shipxy.com/'
# 获取船舶MMSI的url
mmsi_url = 'http://www.shipxy.com/Advert/JinGangJingShips'
# 获取船舶数据的url
data_url = 'http://www.shipxy.com/ship/GetShip'
# 随机生成一个谷歌浏览器的UA
ua = UserAgent()
# 定义header
header = {'User-Agent': ua.chrome}


class ShipxySpider(object):
    def __init__(self):
        # 船讯网系统主页，用来获得cookie
        self.main_url = 'http://www.shipxy.com/'
        # 获取船舶MMSI的url
        self.mmsi_url = 'http://www.shipxy.com/Advert/JinGangJingShips'
        # 获取船舶数据的url
        self.data_url = 'http://www.shipxy.com/ship/GetShip'
        # 随机生成一个谷歌浏览器的UA
        self.ua = UserAgent()
        # 定义header
        self.header = {'User-Agent': self.ua.chrome}

    # 获取船舶数据
    def getData(self):
        session = requests.Session()
        session.get(self.main_url, headers=self.header)
        # 获取船舶的MMSI
        mmsi_res = session.post(self.mmsi_url, headers=self.header)
        MMSI = mmsi_res.json()['data']
        # 根据MMSI获取船舶的数据
        alldata = []
        for mmsi in MMSI:
            data = {"mmsi": mmsi}
            data_res = session.post(self.data_url, headers=self.header, data=data)
            print(data_res.json()['data'])
            alldata.append(data_res.json()['data'])
        session.close()
        return alldata

    # 把爬取的数据保存到本地
    def saveData(self, filename):
        with open(filename, mode='w', newline='') as csv_file:
            # 构建字段名称，也就是key
            fieldnames = ['mmsi', 'lat', 'lon', 'tradetype', 'callsign', 'hdg', 'trail', 'laststa', 'lastdyn', 'imo',
                          'satelliteutc', 'type', 'left', 'length', 'matchtype', 'draught', 'dest', 'width', 'name',
                          'cog', 'rot', 'navistatus', 'cnname', 'source', 'sog', 'eta', 'shipid']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # 写入字段名，当做表头
            writer.writeheader()
            for item in self.getData():
                # 多行写入
                writer.writerows(item)

    # 入口函数
    def run(self):
        self.saveData('data.csv')
        # 每爬取一个页面随机休眠1-2秒钟的时间
        time.sleep(random.randint(1, 2))


# 主函数，用来控制整体逻辑
if __name__ == '__main__':
    # 程序开始运行时间
    start = time.time()
    # 实例化一个对象spider
    spider = ShipxySpider()
    # 调用入口函数
    spider.run()
    end = time.time()
    # 爬虫执行时间
    print('执行时间:%.2f' % (end - start))
