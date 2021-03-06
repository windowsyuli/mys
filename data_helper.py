# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import urllib.request as ur

class data_helper():
    
    def __init__(self, sid, store_path):
        self._sid = sid
        self._store_path = store_path
        self._url = "http://yunhq.sse.com.cn:32041/v1/sh1/snap/" + sid + "?select=name,last,chg_rate,change,amount,volume,open,prev_close,ask,bid,high,low,tradephase"
        self._dir_path = "/".join([self._store_path, self._sid])
        if not os.path.exists(self._dir_path):
            os.mkdir(self._dir_path)


    def __call__(self, time_gap = 1):
        prev_dt = ""
        prev_file_path = ""
        fw = None
        while True:
            flag, dic = self.get_data()
            if flag == 0:
                if (int(dic['time']) < 093000) or (int(dic['time']) > 113000 and int(dic['time']) < 130000) or (int(dic['time']) > 150000):
                    continue
                now_dt = str(dic['date']) + str(dic['time'])
                if now_dt and prev_dt and int(now_dt) <= int(prev_dt):
                    if int(now_dt) == int(prev_dt):
                        print(self.get_time() + " : " + "time error ==.")
                    else:
                        print(self.get_time() + " : " + "time error <.")
                    time.sleep(time_gap)
                    continue
                prev_dt = now_dt
                file_path = "/".join([self._dir_path, str(now_dt[:-4])])
                if file_path != prev_file_path:
                    if fw:
                        fw.flush()
                        fw.close()
                    fw = open(file_path, "a")
                    prev_file_path = file_path
                write_data = self.parse_data(dic)
                print(self.get_time() + " : " + write_data, file = fw)
                print(self.get_time() + " : " + write_data)
            else:
                print(self.get_time() + " : " + dic)
            time.sleep(time_gap)
   
    def parse_data(self, dic):
        t = str(dic['time'])
        d = str(dic['date'])
        data = dic['snap']
        res = [d, t] + data[1:8] + data[8] + data[9] + data[10:]
        return "\t".join([str(x) for x in res])
 
    def get_data(self, encoding = "GBK"):
        b_content = b""
        try:
            req = ur.Request(self._url)
            response = ur.urlopen(req)
            b_content = response.read()
        except Exception as e:
            return -1, str(e)
        content = b_content.decode(encoding)
        content = json.loads(content)
        return 0, content

    def get_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))


if __name__ == "__main__":
    dh = data_helper(sys.argv[1], sys.argv[2])
    dh()
