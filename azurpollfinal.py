# -*- coding:utf-8 -*-
# 碧蓝航线决赛投票网页端API查询
# xhr source:https://qcloud-sdkact-api.biligame.com/bilan/vote/show?activity_id=33&model_id=145
import requests
import time
import prettytable
import os

url = 'https://qcloud-sdkact-api.biligame.com/bilan/vote/show?activity_id=33&model_id=145'
response = None
# API
# 开机先执行一次API拉取

if os.path.exists("./result.csv"):
    pass
else:
    with open("./result.csv","w") as out:
        out.writelines("舰船名,游戏内投票,网页端投票\n")
        out.close()
response = requests.get(url)
rjson = response.json()
rid = rjson['request_id']
print('启动后首次拉取数据成功，本次请求ID为:'+str(rid))
kansen = rjson['data']
# print(kansen)
tab = prettytable.PrettyTable()
tab.field_names = ["船舰名", "游戏内投票", "网页投票"]
with open("./result.csv","a") as res:
    res.writelines("抓取ID: "+rid+"\n")
    res.close()
for id in kansen:
    # print(id)
    name = id['target_name']
    gcount = id['game_count']
    wcount = id['web_count']
    tab.add_row([name,gcount,wcount])
    with open("./result.csv","a") as res:
        res.writelines(str(name)+","+str(gcount)+","+str(wcount)+"\n")
        res.close()
print(tab)

while(True and response.status_code == 200):
    time.sleep(60)
    # 每隔 1min 拉取一次
    response = requests.get(url)
    rjson = response.json()
    rid = rjson['request_id']
    print('拉取数据成功，本次请求ID为:'+str(rid))
    kansen = rjson['data']
    # print(kansen)
    tab = prettytable.PrettyTable()
    with open("./result.csv","a") as res:
        res.writelines("抓取ID: "+rid+"\n")
        res.close()
    tab.field_names = ["船舰名", "游戏内投票", "网页投票"]
    for id in kansen:
        # print(id)
        name = id['target_name']
        gcount = id['game_count']
        wcount = id['web_count']
        tab.add_row([name,gcount,wcount])
        with open("./result.csv","a") as res:
            res.writelines(str(name)+","+str(gcount)+","+str(wcount)+"\n")
    print(tab)

