import ipaddress
import requests
import threading

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


def downloadIPRange(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("文件已成功下载并保存为:", filename)
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
    # 判断文件是否有带有:的行，如果有则删除，无则直接返回
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
            print(output_file + ':' + cidr)


def process_files(input_file, output_file):
    lines = read_file(input_file)
    ip2cidr(lines, output_file)


def main():
    threads = []

    urls_filenames = [
        (EU_url, EU_filename, 'CIDR-EU.txt'),
        (AF_url, AF_filename, 'CIDR-AF.txt'),
        (AS_url, AS_filename, 'CIDR-AS.txt'),
        (NA_url, NA_filename, 'CIDR-NA.txt'),
        (SA_url, SA_filename, 'CIDR-SA.txt'),
        (OC_url, OC_filename, 'CIDR-OC.txt')
    ]

    for url, filename, output_file in urls_filenames:
        thread = threading.Thread(target=downloadIPRange, args=(url, filename))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # 使用多线程处理文件
    file_threads = []
    for _, filename, output_file in urls_filenames:
        thread = threading.Thread(target=process_files, args=(filename, output_file))
        thread.start()
        file_threads.append(thread)

    for thread in file_threads:
        thread.join()


if __name__ == '__main__':
    main()
