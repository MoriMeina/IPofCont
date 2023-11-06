from country_code import *
import requests
import threading

Asia_IP = []
Europe_IP = []
Africa_IP = []
NorthAmerica_IP = []
SouthAmerica_IP = []
Oceana_IP = []
Antarctica_IP = []


def datalist():
    # 创建一个空列表，用于存储线程对象
    threads = []
    # 遍历需要请求的数据列表和结果列表
    for data, res_list in zip(
            [AsiaList, EuropeList, AfricaList, NorthAmericaList, SouthAmericaList, OceanaList, AntarcticaList],
            [Asia_IP, Europe_IP, Africa_IP, NorthAmerica_IP, SouthAmerica_IP, Oceana_IP, Antarctica_IP]):
        # 为每一对创建一个线程对象，并将其添加到线程列表中
        t = threading.Thread(target=request, args=(data, res_list))
        threads.append(t)
    # 遍历线程列表，启动每个线程
    for t in threads:
        t.start()
    # 遍历线程列表，等待每个线程结束
    for t in threads:
        t.join()


def request(data, res_list):
    for url in data:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            res_list.append(response.text)
        else:
            print(f"请求失败，链接：{url}")
