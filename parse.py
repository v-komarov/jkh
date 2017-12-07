#coding: utf-8

import os.path
import os
from bs4 import BeautifulSoup as bs
import pandas as pd

HOUSE = 'html/house/'
MANAGES = 'data/manages.xls'

data = []


class ParseHouse():

    def __init__(self):
        self.files = os.listdir(HOUSE)

    def getmanageid(self):

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

        df = pd.DataFrame(data)
        df.to_excel(MANAGES, index=None)
        print df.head()


if __name__ == '__main__':
    ph = ParseHouse()
    ph.getmanageid()

