# -*- coding:utf-8 -*-
# 碧蓝航线决赛投票网页端API查询
# xhr source:https://qcloud-sdkact-api.biligame.com/bilan/vote/show?activity_id=33&model_id=145
import requests
import time
import prettytable
import os
import pyautogui as pyag
import pyperclip as pycl
import plotly.graph_objects as go

oldkansen = dict()
url = 'https://qcloud-sdkact-api.biligame.com/bilan/vote/show?activity_id=33&model_id=145'
response = None
# API
# 开机先执行一次API拉取
if os.path.exists("./result.csv"):
    pass
else:
    with open("./result.csv", "w") as out:
        out.writelines("舰船名,游戏内投票,网页端投票\n")
        out.close()
response = requests.get(url)
rjson = response.json()
rid = rjson['request_id']
print('启动后首次拉取数据成功，本次请求ID为: ' + str(rid))
kansen = rjson['data']
# print(kansen)
tab = prettytable.PrettyTable()
tab.field_names = ["舰船名", "游戏内投票", "网页投票"]
with open("./result.csv", "a") as res:
    res.writelines("抓取ID: " + rid + "\n")
    res.close()

kansen.sort(key=lambda k: k['game_count'], reverse=True)
"""
kname = []
kpollg = []
kpollw = []
for id in kansen:
    kname.append(id['target_name'])
    kpollg.append(id['game_count'])
    kpollw.append(id['web_count'])
fig = go.Figure(data=[
    go.Table(header=dict(values=['舰船名称', '游戏投票', '网页投票']),
             cells=dict(values=[kname, kpollg, kpollw]))
])
fig.show()
"""
lastcount = kansen[0]['game_count']
for id in kansen:
    # print(id)
    name = id['target_name']
    gcount = id['game_count']
    wcount = id['web_count']
    tab.add_row([name, gcount, wcount])
    with open("./result.csv", "a") as res:
        res.writelines(
            str(name).replace("·"," ") + "," + str(gcount) + "," + str(wcount) + "\n")
        res.close()
print(tab)
oldkansen = kansen
"""
time.sleep(0)
laffey = str(kansen[1]['target_name']) + "酱的游戏内票量: " + str(
    kansen[1]['game_count']) + ", 网页票量: " + str(
        kansen[1]['web_count']) + " 指挥官们还要再加把劲"


pycl.copy(laffey)
pyag.hotkey("ctrl", "v")
pyag.typewrite("\n")
"""

while (True and response.status_code == 200):
    time.sleep(5)
    # 每隔 1min 拉取一次
    response = requests.get(url)
    rjson = response.json()
    rid = rjson['request_id']
    kansen = rjson['data']
    kansen.sort(key=lambda k: k['game_count'], reverse=True)
    # print(kansen)
    tab = prettytable.PrettyTable()
    if kansen[0]['game_count'] == lastcount:
        # print("本次数据与上次数据一致，故不显示与记录。")
        pass
    else:
        print('拉取数据成功，本次请求ID为:' + str(rid))
        with open("./result.csv", "a") as res:
            res.writelines("抓取ID: " + rid + "\n")
            res.close()
        tab.field_names = ["舰船名", "游戏内投票", "网页投票","上轮增量"]
        for i in range(len(kansen)):
            # print(id)
            name = kansen[i]['target_name']
            gcount = kansen[i]['game_count']
            wcount = kansen[i]['web_count']
            distance = kansen[i]['game_count'] - oldkansen[i]['game_count'] 
            tab.add_row([name, gcount, wcount,distance])
            with open("./result.csv", "a") as res:
                res.writelines(
                    str(name).replace("·"," ") + "," + str(gcount) + "," + str(wcount) + "\n")
        lastcount = kansen[0]['game_count']
        print(tab)
        oldkansen=kansen
        """
        laffey = str(kansen[1]['target_name']) + "酱的游戏内票量: " + str(
            kansen[1]['game_count']) + ", 网页投票数量: " + str(
                kansen[1]['web_count']) + " 指挥官们还要再加把劲"
        pycl.copy(laffey)
        pyag.hotkey("ctrl", "v")
        pyag.typewrite("\n")
        """
