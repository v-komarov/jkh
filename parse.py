#coding: utf-8

import os.path
import os
from bs4 import BeautifulSoup as bs
import pandas as pd
import argparse

HOUSE = 'html/house/'
MANAGES = 'data/'

data = []


class ParseHouse():

    def __init__(self,args):
        self.files = os.listdir(HOUSE)
        self.outfile = MANAGES+args.outfile
        self.html = HOUSE+args.dir

    def getmanageid(self):

        ###
        row = 1

        for file in self.files:
            f = open("%s%s" % (HOUSE,file),"r")
            bsobj = bs(f.read(),"lxml")
            f.close()

            if bsobj.find("td"):
                manage = bsobj("td",limit=2)[1].a
                if manage:
                    address = bsobj.findAll("span", {"class": "float-left loc_name_ohl width650 word-wrap-break-word"})[0].get_text().strip(" \n").replace("\n", "").replace(u"ВР", u"").strip()
                    id = manage['href'].strip("\n").split("/")[3]
                    name = manage.string.strip(" \n")

                    #print file,id,name
                    data.append({
                        'house_id':file,
                        'manage_id':id,
                        'manage_name': name,
                        'address':address
                    })

                    print "row : %s" % row

                    row+=1


        df = pd.DataFrame(data)
        df.to_excel(self.outfile, index=None)
        print df.head()



def parse_args():
    parser = argparse.ArgumentParser(description='Извлечение информации управляющей компании из html формата')
    parser.add_argument('outfile', help='Название файла результата')
    parser.add_argument('dir', help='Подкаталог html файлов')

    return parser.parse_args()



if __name__ == '__main__':

    args = parse_args()

    ph = ParseHouse(args)
    ph.getmanageid()

