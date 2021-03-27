# -*- coding: UTF-8 -*-
# Desc: 和彩云自动打卡签到 gen: SCF-GENERATE
# Time: 2020/02/20 12:53:28
# Auth: xuthus
# SIG: QQ Group(824187964)

import json
from urllib import parse

import requests


class Account():
    def __init__(self):
        self.OpenLuckDraw = False  # 是否开启自动幸运抽奖(首次免费, 第二次5积分/次) 不建议开启 否则会导致多次执行时消耗积分
        self.Skey = ""  # 酷推 skey
        self.Cookie = ""  # 抓包Cookie 存在引号时 请使用 \ 转义
        self.Referer = ""  # 抓包referer
        self.UA = "Mozilla/5.0 (Linux; Android 10; M2007J3SC Build/QKQ1.191222.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 MCloudApp/7.6.0"
        self.session = requests.session()
        self.session.headers = {
            "Host": "caiyun.feixin.10086.cn:7070",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": self.UA,
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "http://caiyun.feixin.10086.cn:7070",
            "Referer": self.Referer,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie": self.Cookie,
        }

    def push(self, title, content):
        url = "https://push.xuthus.cc/send/" + self.Skey
        data = title + "\n" + content
        # 发送请求
        res = requests.post(url=url, data=data.encode('utf-8')).text
        # 输出发送结果
        print(res)

    def getEncryptTime(self):
        target = "http://caiyun.feixin.10086.cn:7070/portal/ajax/tools/opRequest.action"
        payload = parse.urlencode({
            "op": "currentTimeMillis"
        })
        resp = json.loads(self.session.post(target, data=payload).text)
        if resp['code'] != 10000:
            print('获取时间戳失败: ', resp['msg'])
            return 0
        return resp['result']

    def getTicket(self):
        target = "https://proxy.xuthus.cc/api/10086_calc_sign"
        payload = {
            "sourceId": 1003,
            "type": 1,
            "encryptTime": self.getEncryptTime()
        }
        resp = json.loads(requests.post(target, data=payload).text)
        if resp['code'] != 200:
            print('加密失败: ', resp['msg'])
        return resp['data']

    def luckDraw(self):
        target = "http://caiyun.feixin.10086.cn:7070/portal/ajax/common/caiYunSignIn.action"
        payload = parse.urlencode({
            "op": "luckDraw",
            "data": self.getTicket()
        })
        resp = json.loads(self.session.post(target, data=payload).text)

        if resp['code'] != 10000:
            print('自动抽奖失败: ', resp['msg'])
            return '自动抽奖失败: ' + resp['msg']
        else:
            if resp['result']['type'] == '40160':
                return '自动抽奖成功: 小狗电器小型手持床铺除螨仪'
            elif resp['result']['type'] == '40175':
                return '自动抽奖成功: 飞科男士剃须刀'
            elif resp['result']['type'] == '40120':
                return '自动抽奖成功: 京东京造电动牙刷'
            elif resp['result']['type'] == '40140':
                return '自动抽奖成功: 10-100M随机长期存储空间'
            elif resp['result']['type'] == '40165':
                return '自动抽奖成功: 夏新蓝牙耳机'
            elif resp['result']['type'] == '40170':
                return '自动抽奖成功: 欧莱雅葡萄籽护肤套餐'
            else:
                return '自动抽奖成功: 谢谢参与'

    def run(self):
        target = "http://caiyun.feixin.10086.cn:7070/portal/ajax/common/caiYunSignIn.action"

        ticket = self.getTicket()
        payload = parse.urlencode({
            "op": "receive",
            "data": ticket,
        })

        resp = json.loads(self.session.post(target, data=payload).text)
        if resp['code'] != 10000:
            self.push('和彩云签到', '失败:' + resp['msg'])
        else:
            content = '签到成功\n月签到天数:' + str(resp['result']['monthDays']) + '\n总积分:' + str(
                resp['result']['totalPoints'])
            if self.OpenLuckDraw:
                content += '\n\n' + self.luckDraw()
            self.push('和彩云签到', content)


def run():
    pass


def main_handler(event, context):
    run()


# 本地测试
if __name__ == '__main__':
    run()
