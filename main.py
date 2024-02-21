import ipaddress
import requests
import threading
from tqdm import tqdm

EU_url = "https://suip.biz/?act=all-country-ip&continent=EU&all-download"
EU_filename = "EU.txt"
AF_url = "https://suip.biz/?act=all-country-ip&continent=AF&all-download"
AF_filename = "AF.txt"
AS_url = "https://suip.biz/?act=all-country-ip&continent=AS&all-download"
AS_filename = "AS.txt"
NA_url = "https://suip.biz/?act=all-country-ip&continent=NA&all-download"
NA_filename = "NA.txt"
SA_url = "https://suip.biz/?act=all-country-ip&continent=SA&all-download"
SA_filename = "SA.txt"
OC_url = "https://suip.biz/?act=all-country-ip&continent=OC&all-download"
OC_filename = "OC.txt"

total_files = 6
total_lines = 0

# 锁用于确保输出的稳定性
output_lock = threading.Lock()


def downloadIPRange(url, filename, pbar):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        pbar.update(1)  # 更新下载进度条
    else:
        print("下载失败，状态码:", response.status_code)


def calculation(ip_range):
    first, last = ip_range.split('-')
    start_ip = ipaddress.IPv4Address(first)
    end_ip = ipaddress.IPv4Address(last)
    ip_network = ipaddress.summarize_address_range(start_ip, end_ip)
    for network in ip_network:
        return str(network)


def read_file(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
        if any(':' in line for line in lines):
            lines = [line.strip() for line in lines if ':' not in line]
            return lines
        else:
            return lines


def ip2cidr(lines, output_file):
    with open(output_file, 'w') as f:
        for line in lines:
            cidr = calculation(line)
            f.write(cidr + '\n')


def process_files(input_file, output_file, total_lines, pbar):
    lines = read_file(input_file)
    with open(output_file, 'w') as f:
        for line in lines:
            cidr = calculation(line)
            f.write(cidr + '\n')
            with output_lock:
                pbar.update(1)  # 更新处理文件进度条


def aggregate_cidr(cidr_list):
    networks = [ipaddress.ip_network(cidr) for cidr in cidr_list]
    aggregated_networks = ipaddress.collapse_addresses(networks)
    return aggregated_networks


def estimate_aggregate_cidr(cidr_list):
    # 估算聚合后的CIDR数量
    total_cidr = sum(1 for _ in aggregate_cidr(cidr_list))
    return total_cidr


def aggregate_cidr_in_file(output_file, pbar):
    cidr_list = []
    with open(output_file, 'r') as f:
        for line in f:
            cidr_list.append(line.strip())

    # 估算聚合后的CIDR数量并创建进度条
    total_cidr = estimate_aggregate_cidr(cidr_list)
    with tqdm(total=total_cidr, desc="Aggregating CIDR") as pbar_inner:
        # 聚合CIDR地址
        aggregated_cidr = aggregate_cidr(cidr_list)

        # 写入聚合后的CIDR地址到文件
        with open("CIDR-" + output_file, 'w') as f:
            for cidr in aggregated_cidr:
                f.write(str(cidr) + '\n')
                with output_lock:
                    pbar_inner.update(1)  # 更新聚合进度条
                    pbar.update(1)  # 更新总进度条


def fetch_cn():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryMKSYlBiByPoqUhJg',
        'Cookie': '_ga=GA1.2.1943133153.1705676070; _ym_uid=1705676072852181160; _ym_d=1705676072; __gsas=ID=4269853c9fd6d356:T=1705676073:RT=1705676073:S=ALNI_Mbq5OPpoibF3EIt1SmL4MHXUsZb4A; _gid=GA1.2.472741953.1708436372; _ym_isad=2; _ym_visorc=w; _ga_ZG4GV8W6PZ=GS1.2.1708483046.4.1.1708483782.0.0.0; __gads=ID=10748fc03b08c6e6:T=1705676070:RT=1708483783:S=ALNI_MYkgwmpEaGmFJQk_0pfFL2E57Ipzg; __gpi=UID=00000cead34d5f4c:T=1705676070:RT=1708483783:S=ALNI_MZhXn2QJqLtHWSZbkEEPxw7Pu2eUg; __eoi=ID=d84d6c39983bb961:T=1708436371:RT=1708483783:S=AA-AfjbiL-wgkyUGsXijR6J-KboB; FCNEC=%5B%5B%22AKsRol8pPFE0gNAXkqxFrAM9I6UJr4ZSyuF6n1cO74pTD6cH01ruzRYmUOrJUXpQGT7r0OR1e-KXi0NenyybO_I9tVRqZrSbCpdJ9v1NzS2lDJZGUB9PGA455aSbqo0D2dd31C1XXc5He1WicM-wuvW0pO42RG3gdg%3D%3D%22%5D%5D',
        'Origin': 'https://suip.biz',
        'Referer': 'https://suip.biz/?act=ipcountry',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = '------WebKitFormBoundaryMKSYlBiByPoqUhJg\r\nContent-Disposition: form-data; name="location"\r\n\r\nCN\r\n------WebKitFormBoundaryMKSYlBiByPoqUhJg\r\nContent-Disposition: form-data; name="only_open"\r\n\r\n1\r\n------WebKitFormBoundaryMKSYlBiByPoqUhJg\r\nContent-Disposition: form-data; name="sure_online"\r\n\r\n1\r\n------WebKitFormBoundaryMKSYlBiByPoqUhJg\r\nContent-Disposition: form-data; name="Submit1"\r\n\r\nSubmit\r\n------WebKitFormBoundaryMKSYlBiByPoqUhJg--\r\n'

    response = requests.post('https://suip.biz/?act=ipcountry', headers=headers, data=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Assuming the response content is a file, you can save it
        with open('CN.txt', 'wb') as f:
            f.write(response.content)
    else:
        print("Request was not successful. Status code:", response.status_code)


def exp_cn_as():
    # 读取CN.txt中的内容，用于后续匹配
    with open('CN.txt', 'r', encoding='utf-8') as cn_file:
        cn_lines = cn_file.readlines()

    # 读取AS.txt中的内容，并过滤掉含有CN.txt中内容的行
    with open('CIDR-AS.txt', 'r', encoding='utf-8') as as_file:
        as_lines = as_file.readlines()

    # 过滤后的内容将存储在filtered_lines列表中
    filtered_lines = [line for line in as_lines if not any(cn_line.strip() in line.strip() for cn_line in cn_lines)]

    # 将过滤后的内容写入新文件AS_filtered.txt中
    with open('CIDR-AS_filtered_CN.txt', 'w', encoding='utf-8') as filtered_file:
        filtered_file.writelines(filtered_lines)


def main():
    threads = []
    download_threads = []

    # 创建总下载进度条
    with tqdm(total=total_files, desc="Downloading files") as pbar:
        urls_filenames = [
            (EU_url, EU_filename),
            (AF_url, AF_filename),
            (AS_url, AS_filename),
            (NA_url, NA_filename),
            (SA_url, SA_filename),
            (OC_url, OC_filename)
        ]

        for url, filename in urls_filenames:
            thread = threading.Thread(target=downloadIPRange, args=(url, filename, pbar))
            thread.start()
            download_threads.append(thread)

        for thread in download_threads:
            thread.join()  # 等待下载线程完成

    # 获取总行数
    global total_lines
    total_lines = sum(len(read_file(filename)) for _, filename in urls_filenames)

    # 创建总处理文件进度条
    with tqdm(total=total_lines, desc="Processing files") as pbar:
        process_threads = []

        for _, filename in urls_filenames:
            thread = threading.Thread(target=process_files, args=(filename, filename, total_lines, pbar))
            thread.start()
            process_threads.append(thread)

        for thread in process_threads:
            thread.join()  # 等待处理文件线程完成

    # 创建总聚合进度条
    aggregate_threads = []
    for _, filename in urls_filenames:
        thread = threading.Thread(target=aggregate_cidr_in_file, args=(filename, pbar))
        thread.start()
        aggregate_threads.append(thread)

    for thread in aggregate_threads:
        thread.join()  # 等待聚合线程完成

    fetch_cn()
    exp_cn_as()


if __name__ == '__main__':
    main()
