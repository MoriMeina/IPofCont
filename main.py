import os
import shutil
import time
from request import *


def write_in():
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    AS = Asia_IP
    EU = Europe_IP
    AF = Africa_IP
    NA = NorthAmerica_IP
    SA = SouthAmerica_IP
    OC = Oceana_IP
    AN = Antarctica_IP
    AS_file = date + '/Asia_IP-' + date + '.txt'
    EU_file = date + '/Europe_IP-' + date + '.txt'
    AF_file = date + '/Africa_IP-' + date + '.txt'
    NA_file = date + '/NorthAmerica_IP-' + date + '.txt'
    SA_file = date + '/SouthAmerica_IP-' + date + '.txt'
    OC_file = date + '/Oceana_IP-' + date + '.txt'
    AN_file = date + '/Antarctica_IP-' + date + '.txt'

    write(AS_file, AS)
    write(EU_file, EU)
    write(AF_file, AF)
    write(NA_file, NA)
    write(SA_file, SA)
    write(OC_file, OC)
    write(AN_file, AN)


def main():
    datalist()
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if os.path.exists(date):
        shutil.rmtree(date)
        os.mkdir(date)
        write_in()
    else:
        os.mkdir(date)
        write_in()


def write(file_name, lists):
    lists.sort()
    with open(file_name, "a") as file:
        for item in lists:
            file.write(item)


if __name__ == '__main__':
    main()
