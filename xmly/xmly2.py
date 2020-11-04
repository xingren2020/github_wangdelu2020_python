import requests
import json
import rsa
import base64
import time
from itertools import groupby
from functools import reduce
from random import choice
import hashlib
from datetime import datetime
from dateutil import tz
import os

# 喜马拉雅极速版加了bark通知，作者github https://github.com/Zero-S1/xmly_speed
# 使用参考 xmly_speed.md
# cookies填写

cookies1 = ""  # 字符串形式 都可以识别
cookies2 = {
}  # 字典形式




cookiesList = [cookies1, ]  # 多账号准备

xmly_speed_cookie ='''_xmLog=xm_kfyn5itg692198; 1&_device=iPhone&C5D8B777-201A-479C-B7AC-B8BA5ADC9229&1.1.10; 1&_token=191084372&E05BBB60240NED25CD0345B7C50CAE4B946D667E164BB71A6945E03336FCAEEFB790BAEBE184130M329312FD3546968_; NSUP=42E33F03%2C41BA403A%2C1602028306432; XUM=C5D8B777-201A-479C-B7AC-B8BA5ADC9229; ainr=0; c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1; device_model=iPhone XR; idfa=6EF3E645-FAD6-4B47-BDDD-978DA2F2D216; impl=com.ximalaya.tingLite; ip=192.168.31.104; net-mode=WIFI; res=828%2C1792
 _xmLog=xm_kg39l8wpkqknzj; 1&_device=iPhone&414C68E7-715F-475E-9776-2D89C4595066&1.1.10; 1&_token=260149230&ECEAD9D0240N6495943F0C58479D3E5257D56E082609E807B6255BE96E2672CDA8204559F19613M0349775CAAB9335_; NSUP=42E33EDE%2C41BA3F9B%2C1602309062656; XUM=414C68E7-715F-475E-9776-2D89C4595066; ainr=0; c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1; device_model=iPhone 6s Plus; idfa=414C68E7-715F-475E-9776-2D89C4595066; impl=com.ximalaya.tingLite; ip=240e:57d:1418:4599:da:408:100:0; net-mode=WIFI; res=1242%2C2208
_xmLog=xm_kg3p14uihd7aqi;1&_device=iPad&653F94B8-410E-4C69-B4C0-41611C41B4D2&1.1.10;1&_token=260235678&E6CB9350340C69B013D876ED1BC00FEDA4BBF6DEF61B6D7159D5857895D82666839F109197D8130M38E411DCAD6CC22_;NSUP=42E33ED5%2C41BA3FBB%2C1602334359552;XUM=653F94B8-410E-4C69-B4C0-41611C41B4D2;ainr=0;c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1;device_model=iPad 4; idfa=E4B9A2E5-5B7D-4A8B-959F-120B6D8B8A2C;impl=com.ximalaya.tingLite;ip=192.168.31.68;net-mode=WIFI;res=640%2C960
_xmLog=xm_kgdvp6hrdrrzo9; 1&_device=iPhone&C8077270-DEA9-4D94-940B-D6203F1383C5&1.1.10; 1&_token=261793732&2D1DB430340N91220D343D863B9A6338B888C3B12D932567B042D3701381A02EEE753D9193F1174M7F15A0B45D1E595_; NSUP=; XUM=C8077270-DEA9-4D94-940B-D6203F1383C5; ainr=0; c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1; device_model=iPhone 5; idfa=00000000-0000-0000-0000-000000000000; impl=com.ximalaya.tingLite; ip=240e:3b9:1435:e380:f0:503:8046:ea14; net-mode=WIFI; res=640%2C1136
_xmLog=xm_kh098gxnxu4gjn; 1&_device=iPhone&C5D8B777-201A-479C-B7AC-B8BA5ADC9229&1.1.10; 1&_token=264729242&16311620340N750C68CA608ED5A65C224C59E93F67F16EA13C98A16004312CB647E758628B9E139MD1DE12B448EFA0F_; NSUP=42E289B8%2C41B8CE3E%2C1604303978496; XUM=C5D8B777-201A-479C-B7AC-B8BA5ADC9229; ainr=0; c-oper=%E8%81%94%E9%80%9A; channel=ios-b1; device_model=iPhone XR; idfa=00000000-0000-0000-0000-000000000000; impl=com.ximalaya.tingLite; ip=240e:57d:2139:14dc:76:8307:100::; net-mode=4G; res=828%2C1792
_xmLog=xm_kh0nj2wk5kzirm; 1&_device=iPhone&414C68E7-715F-475E-9776-2D89C4595066&1.1.11; 1&_token=80150810&BE9F5F90240N020DE4ABD372DBE9A8EB1A2609E94785C0B9CA1ED9C475AF543B08AC2532C6A9161MF14A764E27F1420_; NSUP=42E33EDB%2C41BA3FA4%2C1602332786688; XUM=414C68E7-715F-475E-9776-2D89C4595066; ainr=0; c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1; device_model=iPhone 6s Plus; idfa=EB8686CB-8DC7-463A-95F4-93F8A9F3FD13; impl=com.ximalaya.tingLite; ip=172.16.209.2; net-mode=4G; res=1242%2C2208
'''


xmly_bark_cookie='azjFQzUeTG5hVYx7cRJRTU'
UserAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 iting/1.0.12 kdtunion_iting/1.0 iting(main)/1.0.12/ios_1"
# 非iOS设备的需要的自行修改,自己抓包 与cookie形式类似

iosrule=''
def str2dict(str_cookie):
    if type(str_cookie) == dict:
        return str_cookie
        
    tmp = str_cookie.split(";")
    dict_cookie = {}
    for i in tmp:
        j = i.split("=")
        if not j[0]:
            continue
        dict_cookie[j[0].strip()] = j[1].strip()
    return dict_cookie




'''if "XMLY_SPEED_COOKIE" in os.environ:
    """
    判断是否运行自GitHub action,"XMLY_SPEED_COOKIE" 该参数与 repo里的Secrets的名称保持一致
    """
    print("执行自GitHub action")
    xmly_speed_cookie = os.environ["XMLY_SPEED_COOKIE"]
    '''
 
cookiesList = []  # 重置cookiesList
for line in xmly_speed_cookie.split('\n'):
    if not line:
       continue 
    cookiesList.append(line)

if not cookiesList[0]:
    print("cookie为空 跳出X")
    exit()
mins = int(time.time())
date_stamp = (mins-57600) % 86400
#print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print(datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
_datatime = datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y%m%d", )
print(_datatime)
print("今日已过秒数: ", date_stamp)
print("当前时间戳", mins)

if "XMLY_BARK_COOKIE" in os.environ:
    xmly_bark_cookie = os.environ["XMLY_BARK_COOKIE"]

def listenData(cookies):
    headers = {
        'User-Agent': UserAgent,
        'Host': 'm.ximalaya.com',
        'Content-Type': 'application/json',
    }
    listentime = date_stamp
    print(listentime//60)
    currentTimeMillis = int(time.time()*1000)-2
    sign = hashlib.md5(
        f'currenttimemillis={currentTimeMillis}&listentime={listentime}&uid={uid}&23627d1451047b8d257a96af5db359538f081d651df75b4aa169508547208159'.encode()).hexdigest()
    data = {
        # 'activtyId': 'listenAward',
        'currentTimeMillis': currentTimeMillis,
        'listenTime': str(listentime),
        # 'nativeListenTime': str(listentime),
        'signature': sign,
        'uid': uid
    }

    response = requests.post('http://m.ximalaya.com/speed/web-earn/listen/client/data',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def ans_receive(cookies, paperId, lastTopicId, receiveType):

    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
    }
    _checkData = f"""lastTopicId={lastTopicId}&numOfAnswers=3&receiveType={receiveType}"""
    checkData = rsa_encrypt(str(_checkData), pubkey_str)

    data = {
        "paperId": paperId,
        "checkData": checkData,
        "lastTopicId": lastTopicId,
        "numOfAnswers": 3,
        "receiveType": receiveType
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/topic/receive',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def ans_restore(cookies):
    """
    看视频回复体力，type=2
    """
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
    }
    checkData = rsa_encrypt("restoreType=2", pubkey_str)

    data = {
        "restoreType": 2,
        "checkData": checkData,
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/topic/restore',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def ans_getTimes(cookies):

    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/topic/user', headers=headers, cookies=cookies)
    result = json.loads(response.text)
    stamina = result["data"]["stamina"]  # 答题次数
    remainingTimes = result["data"]["remainingTimes"]  # 可回复次数
    print(f"answer_stamina答题次数: {stamina}")
    print(f"answer_remainingTimes可回复次数: {remainingTimes}\n")
    return {"stamina": stamina,
            "remainingTimes": remainingTimes}


def ans_start(cookies):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/topic/start', headers=headers, cookies=cookies)
    result = json.loads(response.text)
    paperId = result["data"]["paperId"]
    dateStr = result["data"]["dateStr"]
    lastTopicId = result["data"]["topics"][2]["topicId"]
    print(paperId, dateStr, lastTopicId)
    return paperId, dateStr, lastTopicId

def ans_main(cookies):
    print("\n【答题】")
    ans_times = ans_getTimes(cookies)

    for i in range(ans_times["stamina"]):
        paperId, dateStr, lastTopicId = ans_start(cookies)
        ans_receive(cookies, paperId, lastTopicId, 1)
        time.sleep(2)
        ans_receive(cookies, paperId, lastTopicId, 2)
        time.sleep(2)

    if ans_times["remainingTimes"] > 0:
        print("[看视频回复体力]")
        ans_restore(cookies)
        for i in range(5):
            paperId, dateStr, lastTopicId = ans_start(cookies)
            ans_receive(cookies, paperId, lastTopicId, 1)
            time.sleep(1)
            ans_receive(cookies, paperId, lastTopicId, 2)
            time.sleep(1)


def _str2key(s):
    b_str = base64.b64decode(s)
    if len(b_str) < 162:
        return False
    hex_str = ''
    for x in b_str:
        h = hex(x)[2:]
        h = h.rjust(2, '0')
        hex_str += h
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2
    modulus = hex_str[m_start:m_start + m_len]
    exponent = hex_str[e_start:e_start + e_len]
    return modulus, exponent


def rsa_encrypt(s, pubkey_str):
    key = _str2key(pubkey_str)
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    pubkey = rsa.PublicKey(modulus, exponent)
    return base64.b64encode(rsa.encrypt(s.encode(), pubkey)).decode()


pubkey_str = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVhaR3Or7suUlwHUl2Ly36uVmboZ3+HhovogDjLgRE9CbaUokS2eqGaVFfbxAUxFThNDuXq/fBD+SdUgppmcZrIw4HMMP4AtE2qJJQH/KxPWmbXH7Lv+9CisNtPYOlvWJ/GHRqf9x3TBKjjeJ2CjuVxlPBDX63+Ecil2JR9klVawIDAQAB"

def lottery_info(cookies):
  print("\n【幸运大转盘】")
  headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-ad-sweepstake-h5/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    # 查询信息
  response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/inspire/lottery/info', headers=headers, cookies=cookies)
  try:
    result = json.loads(response.text)
    print(result)

    remainingTimes = result["data"]["remainingTimes"]
    print(f'lottery_remainingTimes转盘剩余次数: {remainingTimes}\n')
    if result["data"]["chanceId"] != 0 and result["data"]["remainingTimes"] == 1:
        print("免费抽奖次数")
        return
        data = {
            "sign": rsa_encrypt(str(result["data"]["chanceId"]), pubkey_str),
        }
        response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/action',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
        print(response.text)
        return
    if result["data"]["remainingTimes"] in [0, 1]:
        return
    data = {
        "sign": rsa_encrypt(str(result["data"]["chanceId"]), pubkey_str),
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/action',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)
    # for i in range(3):
    # 获取token
    # exit()
    if remainingTimes > 0:
        headers = {
            'Host': 'm.ximalaya.com',
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive',
            'User-Agent': UserAgent,
            'Accept-Language': 'zh-cn',
            'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-ad-sweepstake-h5/home',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/inspire/lottery/token', headers=headers, cookies=cookies)
        print("token", response.text)
        result = json.loads(response.text)
        _id = result["data"]["id"]
        data = {
            "token": _id,
            "sign": rsa_encrypt(f"token={_id}&userId={uid}", pubkey_str),
        }
        headers = {
            'User-Agent': UserAgent,
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'm.ximalaya.com',
            'Origin': 'https://m.ximalaya.com',
            'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-ad-sweepstake-h5/home',
        }
        response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/chance',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
        result = json.loads(response.text)
        print("chance", result)
        data = {
            "sign": rsa_encrypt(str(result["data"]["chanceId"]), pubkey_str),
        }
        
        response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/action',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
        print("action", response.text)
  except Exception as e:
        print("action", str(e))


def task_label(cookies):
    print("\n【收听时长 30 60 90 】")
    """
    任务查看
    """
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('taskLabels', '1,2'),
    )

    response = requests.get('https://m.ximalaya.com/speed/task-center/task/record',
                            headers=headers, params=params, cookies=cookies)
    try:
      result = json.loads(response.text)
      taskList = result["taskList"]
      print(taskList)
      for i in taskList:
        if i["taskId"] in [79, 80, 81]:  # 收听时长
            if i["status"] == 1:  # 可以领取
                print(i)
                taskRecordId = i["taskRecordId"]
                headers = {
                    'User-Agent': UserAgent,
                    'Host': 'm.ximalaya.com',
                    'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
                    'Origin': 'https://m.ximalaya.com',
                }

                response = requests.post(
                    f'https://m.ximalaya.com/speed/task-center/task/receive/{taskRecordId}', headers=headers, cookies=cookies)
                print(response.text)
                time.sleep(1)
    except Exception as e:
        msg=str(e)
        print(msg)
    print("\n")











def ad_score(cookies, businessType, taskId):
    print("\n【听书点击广告收益】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain ,*/*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/json;charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/task-center/ad/token', headers=headers, cookies=cookies)
    try:
      result = response.json()
      token = result["id"]
      data = {
        "taskId": taskId,
        "businessType": businessType,
        "rsaSign": rsa_encrypt(f"""businessType={businessType}&token={token}&uid={uid}""", pubkey_str),
    }
      response = requests.post(f'https://m.ximalaya.com/speed/task-center/ad/score',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    
      print(response.text)
    except Exception as e:
        msg=str(e)
        print(msg)
    print("\n")




def bubble(cookies):
    print("\n【听书收集气泡】")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-open-components/bubble',
    }

    data = {"listenTime": "41246", "signature": "2b1cc9ee020db596d28831cff8874d9c",
            "currentTimeMillis": "1596695606145", "uid": uid, "expire": False}

    response = requests.post('https://m.ximalaya.com/speed/web-earn/listen/bubbles',
                             headers=headers, cookies=cookies, data=json.dumps(data))
  
    try:
      result = response.json()
      print(result)
      for i in result["data"]["effectiveBubbles"]:
         print(i["id"])
         receive(cookies, i["id"])
         time.sleep(1)
         ad_score(cookies, 7, i["id"])
      for i in result["data"]["expiredBubbles"]:
         ad_score(cookies, 6, i["id"])
    except Exception as e:
        msg=str(e)
        print(msg)

def receive(cookies, taskId):
    print("\n【听书获取奖励】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-open-components/bubble',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        f'https://m.ximalaya.com/speed/web-earn/listen/receive/{taskId}', headers=headers, cookies=cookies)
    try:
      print("receive: ", response.text)
    except Exception as e:
        msg=str(e)
        print(msg)

def card_draw2(cookies, drawRecordIdList):
    print("\n【每天30次抽奖获取卡】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    token = requests.get('https://m.ximalaya.com/speed/web-earn/card/token/1',
                         headers=headers, cookies=cookies,).json()["data"]["id"]
   
    data = {
        "drawType": 1,
        "drawRecordIdList": drawRecordIdList
    }
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/draw',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    try:
      print('抽奖',response.text)
    except Exception as e:
        msg=str(e)
        print(msg)



def get_card_coin(cookies, themeId, cardIdList):
    print("\n【普通卡集卡齐全兑换】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    token = requests.get('https://m.ximalaya.com/speed/web-earn/card/token/3',
                         headers=headers, cookies=cookies,).json()["data"]["id"]
    data = {
        "cardIdList": cardIdList,
        "themeId": themeId,
        "signData": rsa_encrypt(f"{_datatime}{token}{uid}", pubkey_str),
        "token": token
    }
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/exchangeCoin',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    try:
       print('集卡兑换金币',response.text)
    except Exception as e:
        msg=str(e)
        print(msg)


def exchangeCard(cookies, toCardAwardId, fromId):
    print("\n【万能卡兑换普通卡】")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    fromRecordIdList=[]
    fromRecordIdList+=[fromId]
    print(fromRecordIdList)
    data = {
        "toCardAwardId": toCardAwardId,
        "fromRecordIdList":fromRecordIdList,
        "exchangeType": 1
    }
    print('兑换卡片toCardAwardId',toCardAwardId)
    
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/exchangeCard',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    try:
       print('万能卡兑换',response.text)
    except Exception as e:
        msg=str(e)
        print(msg)


def card(cookies):
    print("\n【开始集卡】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/card/userCardInfo', headers=headers, cookies=cookies)
    try:
      print(response.text)
      userCardsList = response.json()["data"]["userCardsList"]
      drawRecordIdList = response.json()["data"]["drawRecordIdList"]
      if drawRecordIdList:
         drawRecordIdList=drawRecordIdList[0:1]
         card_draw2(cookies,drawRecordIdList)
    
      allIds = set([i["id"] for i in userCardsList if i["id"] != 1])
      print('自己的非万能卡',allIds)
      delt = set(range(2, 19))-allIds
      print('自己没有获取的卡',delt)
      OmnipotentCard = [i for i in userCardsList if i["id"] == 1]
      print('自己万能卡',OmnipotentCard)
      if delt and OmnipotentCard:
         exchangeCard(cookies, choice(list(delt)),
                     OmnipotentCard[0]["recordId"])

      jixiangwu2 = [i for i in userCardsList if i["id"] in [2, 3]]
      shangsiji4 = [i for i in userCardsList if i["id"] in [4, 5, 6, 7]]
      shuiguolao5 = [i for i in userCardsList if i["id"] in [8, 9, 10, 11, 12]]
      minghuahui6 = [i for i in userCardsList if i["id"] in [13, 14, 15, 16, 17, 18]]
      _map = {
        2: [2, 3],
        3: [4, 5, 6, 7],
        4: [8, 9, 10, 11, 12],
        5: [13, 14, 15, 16, 17, 18]
        }
      for i in [jixiangwu2,shangsiji4,shuiguolao5,minghuahui6]:
        if not i:
            continue
        card_theme = i
        themeId = card_theme[0]["themeId"]
        print(f""">>>>当前集卡所在类型{themeId} {_map[themeId]}""")
        recordIdList = []
        for _, v in groupby(card_theme, key=lambda x: x["id"]):
            recordIdList.append(list(v)[0])
        if len(recordIdList) == len(_map[themeId]):
            print("卡片凑齐满足兑换金币")
            cardIdList = [i["recordId"] for i in recordIdList]
            print('卡片类型'+str(themeId), cardIdList)
            get_card_coin(cookies, themeId, cardIdList)
    except Exception as e:
          msg=str(e)
          print(msg)

def getOmnipotentCard(cookies):
   print("\n 【获得万能卡信息】")
   headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
   result = requests.get('https://m.ximalaya.com/speed/web-earn/card/omnipotentCardInfo',
                         headers=headers, cookies=cookies,).json()
   try:
     print(result)
     count=result["data"]["count"]
     if count == 5:
        print("万能卡获取今日已满")
        return
     token = requests.get('https://m.ximalaya.com/speed/web-earn/card/token/1',
                         headers=headers, cookies=cookies,).json()["data"]["id"]
     data = {
        "listenTime": mins-date_stamp,
        "signData": rsa_encrypt(f"{_datatime}{token}{uid}", pubkey_str),
        "token": token
     }

     response = requests.post('https://m.ximalaya.com/speed/web-earn/card/getOmnipotentCard',
                             headers=headers, cookies=cookies, data=json.dumps(data))
     print(response.text)
   except Exception as e:
        msg=str(e)
        print(msg)
    


def reportTime(cookies):
    print("提交服务器本地时长\n")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    listenTime = mins-date_stamp
    data = {"listenTime": listenTime,
            "signData": rsa_encrypt(f"{_datatime}{listenTime}{uid}", pubkey_str), }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/reportTime',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    try:
      print(response.text)
    except Exception as e:
        msg=str(e)
        print(msg)





def account(cookies):
    print("\n【打印账号收益】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': UserAgent,
        'Referer': 'https://m.ximalaya.com/speed/web-earn/wallet',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/account/coin', headers=headers, cookies=cookies)
    result = response.json()
    print(result)
    global iosrule
    global j
    iosrule+=f"""【账号{j}】当前剩余:{result["total"]/10000}今日获得:{result["todayTotal"]/10000}累计获得:{result["historyTotal"]/10000}"""+'\n'
    

    
def saveListenTime(cookies):
    print("\n【保存本地收听时长】")
    headers = {
        'User-Agent': UserAgent,
        'Host': 'mobile.ximalaya.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    listentime = date_stamp
    print(listentime//60)
    currentTimeMillis = int(time.time()*1000)-2
    sign = hashlib.md5(
        f'currenttimemillis={currentTimeMillis}&listentime={listentime}&uid={uid}&23627d1451047b8d257a96af5db359538f081d651df75b4aa169508547208159'.encode()).hexdigest()
    data = {
        'activtyId': 'listenAward',
        'currentTimeMillis': currentTimeMillis,
        'listenTime': str(listentime),
        'nativeListenTime': str(listentime),
        'signature': sign,
        'uid': uid
    }

    response = requests.post('http://mobile.ximalaya.com/pizza-category/ball/saveListenTime',
                             headers=headers, cookies=cookies, data=data)
    try:
      print(response.text)
    except Exception as e:
        msg=str(e)
        print(msg)

def dati_taskrecord(cookies):
    print("\n【领取答题任务各种奖励】")
    headers = {
        'User-Agent': UserAgent,

    }
    response = requests.get('https://m.ximalaya.com/speed/web-earn/task/record?taskLabels=4&showReceived=true',
                            headers=headers, cookies=cookies)
    result = response.json()
    #print(response.text)
    if len(result['taskList'])>0:
       for ls in result['taskList']:
         if ls['taskRecordId']>0:
           response = requests.post('https://m.ximalaya.com/speed/web-earn/task/receive/'+str(ls['taskRecordId']),
                           headers=headers, cookies=cookies)
           print(response.text)
           
def homehourred(cookies):
  print("\n【首页红包信息】")
  headers = {
        'User-Agent': UserAgent,}
  currentTimeMillis = int(time.time()*1000)-2
  response = requests.get(f'http://mobile.ximalaya.com/pizza-category/activity/getAward?activtyId=indexSegAward&ballKey={uid}&currentTimeMillis={currentTimeMillis}&sawVideoSignature={currentTimeMillis}+{uid}&version=2',
                            headers=headers, cookies=cookies)

    
  try:
    print(response.text)
    result = response.json()
    for num in range(1,7):
       xg=time.strftime("%Y%m%d", time.localtime())
       response = requests.get(f'http://mobile.ximalaya.com/pizza-category/activity/awardMultiple?activtyId=indexSegAward&awardReceiveId={uid}-{xg}-6-{num}',
                            headers=headers, cookies=cookies)
       result = response.json()
       print(response.text)
       time.sleep(1)
  except Exception as e:
        msg=str(e)
        print(msg)
        
def pushmsg():
  print("\n【通知汇总】")
  if xmly_bark_cookie.strip():
    purl = f'https://api.day.app/{xmly_bark_cookie}/喜马拉雅极速/{iosrule}'
    response = requests.post(purl)
    print(response.text)
 
    
	
	
	
	
	
	
	
def m():
    currentTimeMillis = int(time.time()*1000)-2
    sign = hashlib.md5(('2'+'a45421662ad74842a3f3118aa474ac6c').encode()).hexdigest()
    print(sign)
##################################################################

#http://113.96.156.166/pizza-category/activity/getAward?activtyId=gameTimeAward&currentTimeMillis=1602054131470&gameTime=6&signature=777203037112a37f8a4be0fb1b1cc592&uid=191084372

def main(cookies):
    print("#"*20)
    print("\n")
    homehourred(cookies)
    listenData(cookies)
    saveListenTime(cookies)
    reportTime(cookies)
    bubble(cookies)
    card(cookies)
    getOmnipotentCard(cookies)
    #dati_taskrecord(cookies)
    ans_main(cookies)
    lottery_info(cookies)

    print("\n")

j=0
for i in cookiesList:
    j+=1
   # if j!=6:
    	#continue
    	
    print(">>>>>>>>>【账号"+str(j)+"开始】")
    cookies = str2dict(i)
    uid = cookies["1&_token"].split("&")[0]
    uuid = cookies["XUM"]
    main(cookies)
    account(cookies)
pushmsg()

    
    
