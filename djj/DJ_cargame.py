import re
import requests
import json
import urllib
import time
import timeit
import math
import sys
from datetime import datetime
from dateutil import tz
import os
import dateutil.parser

cookiesList=[]
result=''
djj_bark_cookie=''
djj_sever_jiang=''
djj_djj_cookie=''


JD_API_HOST = 'https://car-member.jd.com/api/'
headers={
      'Accept': '*/*',
      'User-Agent': 'jdapp;iPhone;9.2.4;12.4;3c6b06b6a8d9cc763215d2db748273edc4e02512;network/4g;ADID/B38160D2-DC94-4414-905B-D15F395FD787;supportApplePay/0;hasUPPay/0;hasOCPay/0;model/iPhone11,8;addressid/3529080897;supportBestPay/0;appBuild/167432;pushNoticeIsOpen/0;jdSupportDarkMode/0;pv/117.4;apprpd/Search_ProductList;ref/FinalSearchListViewController;psq/3;ads/;psn/3c6b06b6a8d9cc763215d2db748273edc4e02512|275;jdv/0|kong|t_1001848278_|jingfen|dcdae1aff03e4544a2abe5b1fea7ff3b|1606876124750|1606876163;adk/;app_device/IOS;pap/JA2015_311210|9.2.4|IOS 12.4;Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1','Accept-Language': 'zh-cn',"Referer": "https://h5.m.jd.com/babelDiy/Zeus/44bjzCpzH9GpspWeBzYSqBA7jEtP/index.html",'Accept-Encoding': 'gzip, deflate, br',"activityid": "39443aee3ff74fcb806a6f755240d127",      "Content-Type": "application/json;charset=UTF-8",
    }

      
   
 
    
    
    
    


def JD_car():
   Sign()
   time.sleep(1)
   all_mission('user')
   time.sleep(2)
   all_mission('game')
   time.sleep(1)
   Gamestart()
   getPoint()

   
def Sign():
   print('\n Sign')
   try:
     data=json.loads(iosrule('v1/user/sign',1))
     #print(data)
     if (data['status']):
       print(f'''签到成功，获得{data['data']['point']}，已签到{data['data']['signDays']}天''')
     else:
        print(f'''{data['error']['msg']}.....''')
   except Exception as e:
      msg=str(e)
      print(msg)
      
      

def doMission(missionId):
   print('\n doMission')
   try:
     #print('missionId',missionId)
     data=json.loads(iosrulex('v1/game/mission', {"missionId": missionId}))
     #print(data)
     if (data['status']):
        print('success.....')
        receiveMission(missionId)
     else:
        print(f'''{data['error']['msg']}.....''')
   except Exception as e:
      msg=str(e)
      print(msg)
      
def receiveMission(missionId,fun):
   print('\n receiveMission')
   try:
     data=json.loads(iosrulex(fun+'/receive', {"missionId": missionId}))
    # print(data)
     if (data['status']):
        print('success.....')
     else:
       print(f'''{data['error']['msg']}.....''')
   except Exception as e:
      msg=str(e)
      print(msg)
      
      
def all_mission(flag):
   if(flag=='game'):
     fun='v1/game/mission'
     print('\n game_mission')
   elif(flag=='user'):
     fun='v1/user/mission'
     print('\n user_mission')
   try:
     data=json.loads(iosrule(fun))
    # print(data)
     if (data['status']):
       print('success.....')
       missions = data['data']['missionList']
       for i in range(len(missions)):
         mission = missions[i]
         if(mission['missionStatus']==0 and mission['missionType'] ==1 or mission['missionType'] == 5):
           print(f'''去做任务：{mission['missionName']}''')
           doMission(mission['missionId'])
           time.sleep(1)
         if mission['missionStatus']==1:
            print(f'''领取：{mission['missionName']}奖励''')
            receiveMission(mission['missionId'],fun)
         if mission['missionStatus']==2:
            print(f'''任务:{mission['missionName']}已完成''')
   except Exception as e:
      msg=str(e)
      print(msg)


def Gamestart():
   print('\n Gamestart')
   try:
     data=json.loads(iosrule('/v1/game/start/check'))
     #print(data)
     if (data['status']):
        if (data['data']['hasPower']):
          print('success.....,start')
          Gostart()
        else:
          print('have not enough power.....')
   except Exception as e:
      msg=str(e)
      print(msg)
def Gostart():
   print('\n Gostart')
   try:
     data=json.loads(iosrule('v1/game/start'))
    # print(data)
     if (data['status']):
        print(f'''success.....,get{data['data']['value']}赛点,currentSiteNum:{data['data']['currentSiteNum']}''')
     else:
       print(f'''have not enough power.....{data['error']['msg']}''')
   except Exception as e:
      msg=str(e)
      print(msg)
      
def getPoint():
   try:
     print('\n 💎getPoint')
     msg='【getPoint】'
     data=json.loads(iosrule('v1/user/point'))
     #print(data)
     if (data['status']):
        if (data['data']['remainPoint'] >= data['data']['oncePoint']):
          print(f'''当前赛点:{data['data']['remainPoint']}/{data['data']['oncePoint']}，可以兑换京豆，请打开APP兑换''')
          msg += f'''当前赛点:{data['data']['remainPoint']}/{data['data']['oncePoint']}，可以兑换京豆，请打开APP兑换'''
        else:
          print(f'''当前赛点：{data['data']['remainPoint']}/{data['data']['oncePoint']}无法兑换京豆''')
          msg+=f'''当前赛点：{data['data']['remainPoint']}/{data['data']['oncePoint']}无法兑换京豆'''
          loger(msg)
   except Exception as e:
      msg=str(e)
      print(msg)


def TotalBean(cookies,checkck):
   print('检验过期')
   signmd5=False
   headers= {
        "Cookie": cookies,
        "Referer": 'https://home.m.jd.com/myJd/newhome.action?',
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1'
      }
   try:
       ckresult= requests.get('https://wq.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New',headers=headers,timeout=10).json()
       if json.dumps(ckresult).find(checkck)>0:
           signmd5=True
           loger(f'''【京东{checkck}】''')
       else:
       	  signmd5=False
       	  msg=f'''【京东账号{checkck}】cookie已失效,请重新登录京东获取'''
       	  print(msg)
          pushmsg(msg)
   except Exception as e:
      signmd5=False
      msg=str(e)
      print(msg)
      pushmsg('京东cookie',msg)
   return signmd5






    
def iosrule(functionId,f=0):
   frm=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
   print(frm)
   url=JD_API_HOST+f'''{functionId}?timestamp={tmstamp(frm)}'''
   #print(url)
   try:
     if(f==0):
       response=requests.get(url,headers=headers).text
     else:
       response=requests.post(url,headers=headers).text
     return response
   except Exception as e:
      print(f'''初始化{functionId}任务:''', str(e))
def iosrulex(functionId,body={}):
   frm=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
   print(frm)
   url=JD_API_HOST+f'''{functionId}?timestamp={tmstamp(frm)}'''
   #print(url)
   try:
     response=requests.post(url,headers=headers,data=json.dumps(body)).text
     return response
   except Exception as e:
      print(f'''初始化{functionId}任务:''', str(e))

      
def check():
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   global djj_djj_cookie
   global djj_bark_cookie
   global djj_sever_jiang
   if "DJJ_BARK_COOKIE" in os.environ:
     djj_bark_cookie = os.environ["DJJ_BARK_COOKIE"]
   if "DJJ_SEVER_JIANG" in os.environ:
      djj_sever_jiang = os.environ["DJJ_SEVER_JIANG"]
   if "DJJ_DJJ_COOKIE" in os.environ:
      djj_djj_cookie = os.environ["DJJ_DJJ_COOKIE"]
      for line in djj_djj_cookie.split('\n'):
        if not line:
          continue 
        cookiesList.append(line.strip())
   elif djj_djj_cookie:
       for line in djj_djj_cookie.split('\n'):
         if not line:
            continue 
         cookiesList.append(line.strip())
   else:
     print('DTask is over.')
     exit()

def pushmsg(title,txt,bflag=1,wflag=1):
   txt=urllib.parse.quote(txt)
   title=urllib.parse.quote(title)
   if bflag==1 and djj_bark_cookie.strip():
      print("\n【通知汇总】")
      purl = f'''https://api.day.app/{djj_bark_cookie}/{title}/{txt}'''
      response = requests.post(purl)
      #print(response.text)
   if wflag==1 and djj_sever_jiang.strip():
      print("\n【微信消息】")
      purl = f'''http://sc.ftqq.com/{djj_sever_jiang}.send'''
      headers={
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
    }
      body=f'''text={txt})&desp={title}'''
      response = requests.post(purl,headers=headers,data=body)
   global result
   print(result)
   result =''
    
def loger(m):
   print(m)
   global result
   result +=m+'\n'
    
def islogon(j,count):
    JD_islogn=False
    global jd_name
    for i in count.split(';'):
       if i.find('pin=')>=0:
          jd_name=i.strip()[i.find('pin=')+4:len(i)]
          print(f'''>>>>>>>>>【账号{str(j)}开始】{jd_name}''')
    if(TotalBean(count,jd_name)):
        JD_islogn=True
    return JD_islogn





def tmstamp(tr):
   tm = dateutil.parser.parse(tr).timestamp()
   return tm

def stamptm(tm,frm='%Y-%m-%d %H:%M:%S'):
   #frm=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
   tr = datetime.datetime.fromtimestamp(tm).strftime(frm)
   return tr
def clock(func):
    def clocked(*args, **kwargs):
        t0 = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[🔔运行完毕用时%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
    
@clock
def start():
   check()
   j=0
   for count in cookiesList:
     j+=1
     headers['Cookie']=count
     if(islogon(j,count)):
         JD_car()
   pushmsg('jd_cargame',result)
if __name__ == '__main__':
       start()
