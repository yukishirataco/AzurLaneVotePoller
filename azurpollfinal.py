# -*- coding:utf-8 -*-
# 碧蓝航线决赛投票网页端API查询
# xhr source:https://qcloud-sdkact-api.biligame.com/bilan/vote/show?activity_id=33&model_id=145
import requests
import time
import prettytable
import os
import pyautogui as pyag
import pyperclip as pycl

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
print('启动后首次拉取数据成功，本次请求ID为:' + str(rid))
kansen = rjson['data']
# print(kansen)
tab = prettytable.PrettyTable()
tab.field_names = ["船舰名", "游戏内投票", "网页投票"]
with open("./result.csv", "a") as res:
    res.writelines("抓取ID: " + rid + "\n")
    res.close()

kansen.sort(key=lambda k: k['game_count'],reverse=True)
for id in kansen:
    # print(id)
    name = id['target_name']
    gcount = id['game_count']
    wcount = id['web_count']
    tab.add_row([name, gcount, wcount])
    with open("./result.csv", "a") as res:
        res.writelines(
            str(name) + "," + str(gcount) + "," + str(wcount) + "\n")
        res.close()
print(tab)

"""
time.sleep(0)
laffey = str(kansen[0]['target_name']) + "酱的游戏内票量: " + str(
    kansen[0]['game_count']) + ", 网页票量: " + str(
        kansen[0]['web_count']) + " 指挥官们还要再加把劲"

pycl.copy(laffey)
pyag.hotkey("ctrl", "v")
pyag.typewrite("\n")
"""

while (True and response.status_code == 200):
    time.sleep(60 * 5)
    # 每隔 1min 拉取一次
    response = requests.get(url)
    rjson = response.json()
    rid = rjson['request_id']
    print('拉取数据成功，本次请求ID为:' + str(rid))
    kansen = rjson['data']
    # print(kansen)
    tab = prettytable.PrettyTable()
    with open("./result.csv", "a") as res:
        res.writelines("抓取ID: " + rid + "\n")
        res.close()
    tab.field_names = ["船舰名", "游戏内投票", "网页投票"]
    for id in kansen:
        # print(id)
        name = id['target_name']
        gcount = id['game_count']
        wcount = id['web_count']
        tab.add_row([name, gcount, wcount])
        with open("./result.csv", "a") as res:
            res.writelines(
                str(name) + "," + str(gcount) + "," + str(wcount) + "\n")
    print(tab)
    """
    laffey = str(kansen[0]['target_name']) + "酱的游戏内票量: " + str(
        kansen[0]['game_count']) + ", 网页投票数量: " + str(
            kansen[0]['web_count']) + " 指挥官们还要再加把劲"
    pycl.copy(laffey)
    pyag.hotkey("ctrl", "v")
    pyag.typewrite("\n")
    """
