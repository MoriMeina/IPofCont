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
CN_url = "https://suip.biz/?act=all-country-ip&country=CN&all-download"
CN_filename = "CN.txt"

total_files = 7
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


def process_files(input_file, output_file, pbar):
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

def main():
    download_threads = []

    # 创建总下载进度条
    with tqdm(total=total_files, desc="Downloading files") as pbar:
        urls_filenames = [
            (EU_url, EU_filename),
            (AF_url, AF_filename),
            (AS_url, AS_filename),
            (NA_url, NA_filename),
            (SA_url, SA_filename),
            (OC_url, OC_filename),
            (CN_url, CN_filename)
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
            thread = threading.Thread(target=process_files, args=(filename, filename, pbar))
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

    # 等待所有线程完成后执行exp_cn_as()
    for thread in process_threads + aggregate_threads:
        thread.join()



if __name__ == '__main__':
    main()
