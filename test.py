# -*- coding: utf-8 -*-
import sys, urllib.request as ur, json
import time

def req_url():
    try:
        url = 'http://apis.baidu.com/apistore/stockservice/stock?stockid=sh601988&list=1'
        req = ur.Request(url)
        req.add_header("apikey", "d5dfd9fbaab089b49d8cc0ec123db340")
        resp = ur.urlopen(req)
        content = resp.read()
        content = content.decode("gbk") 
        dic = json.loads(content)
        data = dic["retData"]["stockinfo"][0]
        print("\t".join([str(x) for x in [data["name"], data["time"], data["currentPrice"], data["totalNumber"]]]))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    while True:
        req_url()
        time.sleep(0.2)


