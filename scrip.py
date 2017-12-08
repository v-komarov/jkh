#coding: utf-8

import pandas as pd
import requests
import os.path
import os
import random
import time


### Скрайпинг сайта (реформа ЖКХ)

HOUSE = 'html/house/'
SOURCE_FILE = 'source/krasnoyarsk.xlsm'
LIST_IP = ['80.240.33.209/29', '80.240.33.210/29', '80.240.33.211/29', '80.240.33.212/29', '80.240.33.213/29',]
#LIST_IP = ['80.240.33.210/29', '80.240.33.211/29', '80.240.33.212/29', '80.240.33.213/29',]



class ScripeHouse():

    def __init__(self):
        self.ip = "begin"
        self.new = "begin"
        self.list_ip = LIST_IP
        self.df = pd.read_excel(SOURCE_FILE, sheet_name=0, index_col=None)
        self.request_ip = 0


    ### Смена ip адреса
    def change_ip(self):

        if self.request_ip >= 11:

            while self.new == self.ip:
                self.ip = random.choice(self.list_ip)

            self.new = self.ip

            self.ip = random.choice(self.list_ip)
            os.system("/sbin/ifconfig ens160 %s" % self.ip)
            os.system("/usr/sbin/route add default gw 80.240.33.214")
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





if __name__ == '__main__':
    sc = ScripeHouse()
    sc.getdata()