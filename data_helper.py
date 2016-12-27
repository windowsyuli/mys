# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import urllib.request as ur
import urllib.parse as up

class data_helper():
    
    def __init__(self, sid, store_path):
        appkey = "66b521828eb944d75985042355a56e32"
        params = {
            "gid" : sid,
            "key" : appkey
        }
        self._params = up.urlencode(params)
        self._sid = sid
        self._store_path = store_path
        self._base_url = "http://web.juhe.cn:8080/finance/stock/hs"
        # attribute
        #['sellOne', 'sellThreePri', 'sellFourPri', 'gid', 'time', 
        #'traNumber', 'date', 'sellOnePri', 'buyThree', 'buyTwo', 
        #'reservePri', 'increase', 'buyOne', 'sellFive', 'sellTwoPri', 
        #'increPer', 'competitivePri', 'todayMax', 'todayStartPri', 
        #'buyFour', 'buyFivePri', 'sellTwo', 'traAmount', 'sellFivePri', 
        #'sellFour', 'buyThreePri', 'buyFive', 'sellThree', 'nowPri', 
        #'buyOnePri', 'buyFourPri', 'name', 'yestodEndPri', 'todayMin', 'buyTwoPri']
        #9:30-11:30, 13:00-15:00


    def run(self, time_gap = 0.2):
        dir_path = "/".join([self._store_path, self._sid])
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        prev_dt = ""
        prev_file_path = ""
        fw = None
        while True:
            flag, dic = self.get_data()
            if flag == 0:
                now_dt = dic['date'] + "-" + dic['time']
                if now_dt == prev_dt:
                    if fw:
                        fw.flush()
                    time.sleep(time_gap)
                    continue
                prev_dt = now_dt
                file_path = "/".join([dir_path, dic['date'] + "-" + dic['time'].split(":")[0]])
                if file_path != prev_file_path:
                    if fw:
                        fw.flush()
                        fw.close()
                    fw = open(file_path, "w")
                    prev_file_path = file_path
                write_data = "\t".join([x for _, x in dic.items()])
                print(write_data, file = fw)
                print(write_data)
            else:
                print(content)
            time.sleep(time_gap)

    def get_data(self, method = "GET", encoding = "UTF-8"):
        if method == "GET":
            f = ur.urlopen("%s?%s" % (self._base_url, self._params))
        else:
            f = ur.urlopen(self._base_url, params)
        content = f.read().decode(encoding)
        res = json.loads(content)
        if res:
            error_code = res["error_code"]
            if error_code == 0:
                return 0, res["result"][0]['data']
            else:
                return 1, "Error: %s:%s." % (res["error_code"], res["reason"])
        else:
            return 2, "Error: unknown request api."
        

if __name__ == "__main__":
    dh = data_helper(sys.argv[1], sys.argv[2])
    dh.run()
