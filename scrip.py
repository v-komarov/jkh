#coding: utf-8

import pandas as pd
import requests
import os.path
import os
import random
import time
import argparse
import config


### Скрайпинг сайта (реформа ЖКХ)

HOUSE = config.HOUSE
SOURCE_DIR = config.SOURCE_DIR
LIST_IP = config.LIST_IP
GW = config.GW
INTERFACE = config.INTERFACE


class ScripeHouse():

    def __init__(self,args):

        self.source = SOURCE_DIR+args.source
        self.ip = "begin"
        self.new = "begin"
        self.list_ip = LIST_IP
        self.df = pd.read_excel(self.source, sheet_name=args.sheet, index_col=None)
        self.request_ip = 0


    ### Смена ip адреса
    def change_ip(self):

        if self.request_ip >= 11:

            while self.new == self.ip:
                self.ip = random.choice(self.list_ip)

            self.new = self.ip

            os.system("/sbin/ifconfig %s %s" % (INTERFACE,self.ip))
            os.system("/usr/sbin/route add default gw %s" % GW)
            print "sleep"
            time.sleep(60)
            self.request_ip = 0





    def getdata(self):

        list_id = self.df[u'Дом_id'].tolist()
        while len(list_id)>len(os.listdir(HOUSE)):

            for id in list_id:
                print id, len(os.listdir(HOUSE)), self.ip, self.request_ip

                if not os.path.exists("%s%s" % (HOUSE,id)):

                    ### Смена ip адреса
                    self.change_ip()

                    r = requests.get('https://www.reformagkh.ru/myhouse/profile/view/%s' % id)
                    f = open("%s%s" % (HOUSE,id),'a')
                    if len(r.text.encode("utf-8")) >=1024:
                        f.write(r.text.encode("utf-8"))
                        f.close()
                        self.request_ip = self.request_ip + 1
                        time.sleep(5)
                    else:
                        print "They have caught us!!!"
                        exit()




def parse_args():
    parser = argparse.ArgumentParser(description='Сбор данных в формате html')
    parser.add_argument('data', choices=['house','manager'], help='Вид данных, которые будут собираться')
    parser.add_argument('source', help='Файл - источник данных')
    parser.add_argument('sheet', type=int, help='Номер листа в таблице')


    return parser.parse_args()





if __name__ == '__main__':

    args = parse_args()

    if args.data == "house":
        sc = ScripeHouse(args)
        sc.getdata()

