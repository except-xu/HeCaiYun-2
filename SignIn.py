# -*- coding: UTF-8 -*-
# Desc: 和彩云自动打卡签到 gen: SCF-GENERATE
# Time: 2020/02/20 12:53:28
# Auth: xuthus
# SIG: QQ Group(824187964)

import json
from urllib import parse
import time
import os, sys
import requests


def get_datetime():
    local_time = time.localtime()
    dt = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    return dt


def log(text):
    print("{} - {}".format(get_datetime(), text))


class Account():
    def __init__(self):
        self.OpenLuckDraw = False  # 是否开启自动幸运抽奖(首次免费, 第二次5积分/次) 不建议开启 否则会导致多次执行时消耗积分
        self.Skey = ""  # 酷推 skey
        self.Cookie = ""  # 抓包Cookie 存在引号时 请使用 \ 转义
        self.Referer = "https://caiyun.feixin.10086.cn:7071/portal/newsignin/index.jsp"  # 抓包referer
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
        log(res)

    def getEncryptTime(self):
        target = "http://caiyun.feixin.10086.cn:7070/portal/ajax/tools/opRequest.action"
        payload = parse.urlencode({
            "op": "currentTimeMillis"
        })
        resp = json.loads(self.session.post(target, data=payload).text)
        if resp['code'] != 10000:
            log('获取时间戳失败: ', resp['msg'])
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
            log('加密失败: ', resp['msg'])
        return resp['data']

    def luckDraw(self):
        target = "http://caiyun.feixin.10086.cn:7070/portal/ajax/common/caiYunSignIn.action"
        payload = parse.urlencode({
            "op": "luckDraw",
            "data": self.getTicket()
        })
        resp = json.loads(self.session.post(target, data=payload).text)

        if resp['code'] != 10000:
            log('自动抽奖失败: ', resp['msg'])
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

    def sign_in(self):
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


def run(Cookie: str, OpenLuckDraw: bool):
    account = Account()
    account.Cookie = Cookie
    account.OpenLuckDraw = OpenLuckDraw
    account.sign_in()


def conf_file_run(account_conf_file):
    with open(account_conf_file) as f:
        account_conf = json.loads(f.read())
    for account in account_conf:
        log("开始账号")
        run(account["Cookie"], account["OpenLuckDraw"])


def cli_arg_run(argv):
    '''
    命令行参数启动
    :return:
    '''
    Cookie_list = argv[1].split("#")
    OpenLuckDraw_list = argv[2].split("#")
    if len(Cookie_list) != len(OpenLuckDraw_list):
        log("请确保<Cookie>和<是否开启抽奖的设置>数量一致")
    for i in range(0, len(Cookie_list)):
        Cookie = Cookie_list[i]
        OpenLuckDraw = False  # 默认不开启抽奖
        if "ture" == OpenLuckDraw_list[i]:  # 如果设置了ture才开启
            OpenLuckDraw = True
        # elif "false" == OpenLuckDraw_list[i]:
        #     OpenLuckDraw = False
        log("开始账号")
        run(Cookie, OpenLuckDraw)


def tencent_SCF_run(event, context):
    environment = eval(context["environment"])
    cli_arg_run([environment["SCF_NAMESPACE"], environment["Cookie"], environment["OpenLuckDraw"]])


# 本地测试
if __name__ == '__main__':
    if len(sys.argv) > 1:
        log("命令行参数启动")
        log("因cookie过于长，暂不支持命令行输入cookie等参数")
        exit(1)
        cli_arg_run(sys.argv)
    else:
        log("账号配置文件启动")
        account_conf_file = "account_conf.json"
        if not os.path.exists(account_conf_file) or not os.path.isfile(account_conf_file):
            log("不存在账号配置文件{}".format(account_conf_file))
            exit(1)
        else:
            conf_file_run(account_conf_file)
