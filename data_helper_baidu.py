# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import urllib.request as ur

class data_helper_baidu():
    
    def __init__(self, sid, store_path):
        self._sid = sid
        self._store_path = store_path
        self._url = "http://apis.baidu.com/apistore/stockservice/stock?stockid=" + sid + "&list=1"
        self._dir_path ="/".join([store_path, sid])
        if not os.path.exists(self._dir_path):
            os.mkdir(self._dir_path)


    def __call__(self, time_gap = 1):
        prev_dt = ""
        prev_file_path = ""
        fw = None
        while True:
            flag, dic = self.get_data()
            if flag == 0:
                dic['date'] = dic['date'].replace("-", "")
                dic['time'] = dic['time'].replace(":", "")
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
        key = ["date", "time", "OpenningPrice", "closingPrice", "currentPrice", "currentPrice", "hPrice",
                "lPrice", "competitivePrice", "auctionPrice", "totalNumber", "turnover", "increase", 
                "buyOne", "buyOnePrice", "buyTwo", "buyTwoPrice", "buyThree", "buyThreePrice",
                "buyFour", "buyFourPrice", "buyFive", "buyFivePrice", "sellOne", "sellOnePrice",
                "sellTwo", "sellTwoPrice", "sellThree", "sellThreePrice", "sellFour", "sellFourPrice",
                "sellFive", "sellFivePrice"]
        data = [dic[x] for x in key]
        return "\t".join([str(x) for x in data])
 
    def get_data(self, encoding = "GBK", api_key = "d5dfd9fbaab089b49d8cc0ec123db340"):
        b_content = b""
        try:
            req = ur.Request(self._url)
            req.add_header("apikey", api_key)
            response = ur.urlopen(req)
            b_content = response.read()
        except Exception as e:
            return -1, str(e)
        content = b_content.decode(encoding)
        content = json.loads(content)
        if "retData" not in content or "stockinfo" not in content["retData"]:
            return -2, "empty response."
        content = content["retData"]["stockinfo"][0]
        if content:
            return 0, content
        else:
            return -2, "empty response."

    def get_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))


if __name__ == "__main__":
    dh = data_helper_baidu(sys.argv[1], sys.argv[2])
    dh()
