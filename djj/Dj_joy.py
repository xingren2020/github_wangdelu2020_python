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


osenviron={}
djj_sharecode=''
djj_bark_cookie=''
djj_sever_jiang=''
djj_djj_cookie=''

Defalt_ShareCode=['xtnbyfDdKhSLK7XZdi1nOw==','fpSTmcR0VqB-sAOQ8vLCeQ==','tV8syjVsEKT4sCfEWngba6t9zd5YaBeE']

JD_API_HOST = 'https://api.m.jd.com'
headers={}
joyIds=[]
BUY_JOY_LEVEL = ''

cookiesList=[]
result=''
jd_name=''
mycode=''
info={}


def myhd(hd):
   hd=eval(hd)
   hd['Referer']='https://crazy-joy.jd.com/'
   return hd
   
   
def JD_Joy():
   gameState()
   getTaskState()
   doSign()
   Assist()
   LUCKY_BOX_Award()
   produce()
   checkAndMerge()




   
def checkAndMerge():
   print('checkAndMerge')
   try:
     print('joy列表',joyIds)
     buyid=1
     joyIds.sort()
     for i in joyIds:
       if i==0:
         continue
       else:
         buyid=i
         break
     for i in range(len(joyIds)):
        joy = joyIds[i]
        if (joy ==0):
           trade(buyid)
           time.sleep(2)
     for m in range(len(joyIds)):
        m+=1
        joyList()
        for i in range(len(joyIds)):
           if(i+m)<len(joyIds):
              if joyIds[i]==joyIds[i+m]:
                  moveOrMerge(i+m,i)
                  time.sleep(3)
         
     
   except Exception as e:
      msg=str(e)
      print(msg)


   

def gameState():
   try:
     print('gameState')
     global joyIds,mycode,BUY_JOY_LEVEL
     body = {'paramData': {'inviter':'DBwF_65db1jIoHqBDEMk8at9zd5YaBeE'}}
     data=json.loads(iosrule('crazyJoy_user_gameState',body).text)
     print(data)
     if (data['success']):
       mycode=data['data']['userInviteCode']
       print('邀请码'+data['data']['userInviteCode'])
       print('当前joy币'+str(data['data']['totalCoinAmount']))
       print('离线收益'+ str(data['data']['offlineCoinAmount']))
       BUY_JOY_LEVEL=data['data']['userTopLevelJoyId']
       print('最高级别的joy'+ str(data['data']['userTopLevelJoyId'])+'级')
       joyIds = data['data']['joyIds']
       print('joyIds',joyIds)
       
       hopen=data['data']['hourCoinCountDown']/60
       print('时段宝箱剩余'+str(hopen)+'分开启')
       if data['data']['hourCoinCountDown']==0:
         hourAward()
   except Exception as e:
       print(str(e))
       
{"body":"{\"paramData\":{\"typeId\":3}}","functionId":"crazyJoy_user_getSpecialJoy","appid":"crazy_joy","uts":"e7fed5f58a508ea3b6b081237be9afa95fe18409","t":"1608614921002"}


def joyList():
   global joyIds
   print('joyList')
   try:
     body = {'paramData': {'inviter': 'DBwF_65db1jIoHqBDEMk8at9zd5YaBeE'}}
     data=json.loads(iosrule('crazyJoy_user_gameState',body).text)
     #print(data)
     if (data['success'] and data['data']['joyIds']):
          joyIds = data['data']['joyIds']
          joyIds.sort()
          print(joyIds)
   except Exception as e:
       print(str(e))
       
       
       
       




def LUCKY_BOX_Award():
   print('LUCKY_BOX_Award')
   try:
     print('开始幸运宝箱任务')
     data=json.loads(iosrule('crazyJoy_joy_produce').text)
     print(data)
     eventRecordId=data['data']['luckyBoxRecordId']
     body = {'eventType': "LUCKY_BOX_DROP","eventRecordId":eventRecordId}
     tm=data['data']['advertViewTimes']
     if(tm==0):
       print('幸运宝箱任务完成....总金币:'+str(data['data']['totalCoinAmount']))
       return
     print('第'+str(tm)+'次浏览广告,当前金币'+str(data['data']['totalCoinAmount']))
     data=json.loads(iosrule('crazyJoy_event_getVideoAdvert',body).text)
     print(data)
     
     time.sleep(30)
     print('获取奖励')
     data=json.loads(iosrule('crazyJoy_event_obtainAward',body).text)
     print(data)
     if (data['success'] and data['data']['coins']):
       print(f'''模拟挂机中获得{data['data']['coins']}个币''')
       
   except Exception as e:
       print(str(e))


def hourAward():
   print('hourAward')
   try:
     body = {'eventType': "HOUR_BENEFIT"}
     data=json.loads(iosrule('crazyJoy_event_obtainAward',body).text)
     print(data)
   except Exception as e:
       print(str(e))



       

def doSign():
   try:
     print('doSign')
     Res=iosrule('crazyJoy_task_doSign').text
     print(Res)
   except Exception as e:
       print(str(e))
       
def getTaskState():
   try:
     print('getTaskState')
     body = {"paramData": {"taskType": "DAY_TASK"}}
     flag=''
     data=json.loads(iosrule('crazyJoy_task_getTaskState',body).text)
     #print(data)
     for i in data['data']:
       if i['status']==0:
         flag='没完成'
       else:
          flag='完成'
       print(i['taskTitle']+'===进度'+str(i['doneTimes'])+'/'+str(i['ext']['count'])+'==状态:'+flag)
     	
     for i in data['data']:
       if i['taskId']==50:
         continue
       if i['status']==0:
         print(i['taskTitle']+'===进度'+str(i['doneTimes'])+'/'+str(i['ext']['count'])+'进行中.....')
         Task_view(i['taskId'])
       else:
          print(i['taskTitle']+'===进度'+str(i['doneTimes'])+'/'+str(i['ext']['count'])+'完成.....')
   except Exception as e:
       print(str(e))



def TaskAward(id):
   print('TaskAward',str(id))
   try:
     body = {'taskId': id}
     data=json.loads(iosrule('crazyJoy_task_obtainAward',body).text)
     print(data)
   except Exception as e:
       print(str(e))

def Task_view(id):
   print('Task_view',str(id))
   try:
     body = {"action":"MARK","taskId":id}
     data=json.loads(iosrule('crazyJoy_task_viewPage',body).text)
     print(data)
     taskRecordId=data['data']['taskRecordId']
     time.sleep(30)
     Taskdo(id,taskRecordId)
     time.sleep(2)
     TaskAward(id)
   except Exception as e:
       print(str(e))

       
def Taskdo(id,taskRecordId):
   print('Taskdo',str(id),taskRecordId)
   try:
     body={"action":"INCREASE","taskId":id,"taskRecordId":taskRecordId}
     data=json.loads(iosrule('crazyJoy_task_viewPage',body).text)
     print(data)
     
     
     
   except Exception as e:
       print(str(e))
       
def Assist():
   for code in Defalt_ShareCode:
      if code==mycode:
        print('跳过自己')
        continue
      recordAssist(code)
def recordAssist(code):
   try:
     print('recordAssist助力',code)
     body = {"paramData": {"inviter": code}}
     Res=iosrule('crazyJoy_task_recordAssist',body).text
     print(Res)
   except Exception as e:
     print(str(e))
       
       

   
def produce():
#模拟国际
   print('produce')
   try:
     data=json.loads(iosrule('crazyJoy_joy_produce').text)
     print(data)
     if (data['success'] and data['data']['coins']):
       print(f'''模拟挂机中 获得{data['data']['coins']}个币，当前拥有{data['data']['totalCoinAmount']}''')
   except Exception as e:
       print(str(e))
       
def moveOrMerge(f,t):
#等待5s再合并，不然会操作过于频繁
   print('moveOrMerge')
   try:
     body = {
    "operateType": "MERGE",
    "fromBoxIndex": f,
    "targetBoxIndex": t
  }
     Res=iosrule('crazyJoy_joy_moveOrMerge',body).text
     print(Res)
   except Exception as e:
       print(str(e))

def trade(joyLevel):
   print('trade')
   try:
     body = {"action": "BUY", "joyId": joyLevel, "boxId": ""}
     data=json.loads(iosrule('crazyJoy_joy_trade',body).text)
     print(data)
     if (data['success']):
       print(f'''购买{joyLevel}级joy成功， 花费{data['data']['coins']}，下次购买费用 --> {data['data']['nextBuyPrice']}， 剩余joy币 --> ${data['data']['totalCoins']}''')
   except Exception as e:
       print(str(e))
       

def trade1(joyId, boxId):
   print('trade1')
   try:
     body = {"action": "SELL", "joyId": joyId, "boxId": boxId}
     data=json.loads(iosrule('crazyJoy_joy_trade',body).text)
     print(data)
     if (data['success'] and data['data']['coins']):
       print(f'''模拟挂机中 获得{data['data']['coins']}个币，当前拥有{data['data']['totalCoinAmount']}''')
   except Exception as e:
       print(str(e))

       
def iosrule(functionId,body={}):
   url=JD_API_HOST+f'''/?body={urllib.parse.quote(json.dumps(body))}&appid=crazy_joy&functionId={functionId}&uts=b8bf8319bc0e120e166849cb7e957d335fe01979'''

   #print(url)
   try:
      response=requests.get(url,headers=headers)
      return response
   except Exception as e:
     print(f'''初始化{functionId}任务:''', str(e))


def iosrulex(functionId,body):
   url=JD_API_HOST+f'''/client.action?functionId={functionId}'''
   print(url)
   try:
      response=requests.post(url,headers=headers,data=body)
      return response
   except Exception as e:
     print(f'''初始化{functionId}任务:''', str(e))
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
       #print(ckresult)
       if ckresult['retcode']==0:
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

def check(flag,list):
   vip=''
   global djj_bark_cookie
   global djj_sever_jiang
   if "DJJ_BARK_COOKIE" in os.environ:
     djj_bark_cookie = os.environ["DJJ_BARK_COOKIE"]
   if "DJJ_SEVER_JIANG" in os.environ:
      djj_sever_jiang = os.environ["DJJ_SEVER_JIANG"]
   if flag in os.environ:
      vip = os.environ[flag]
   if flag in osenviron:
      vip = osenviron[flag]
   if vip:
       for line in vip.split('\n'):
         if not line:
            continue 
         list.append(line.strip())
       return list
   else:
       print(f'''【{flag}】 is empty,DTask is over.''')
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
   cookiesList=[]
   xfj_hdlist=[]
   global headers
   global djj_djj_cookie
   check('DJJ_XFJ_HEADERS',xfj_hdlist)
   check('DJJ_DJJ_COOKIE',cookiesList)
   j=0
   for i in range(6):
     for count in cookiesList:
        j+=1
        headers=myhd(xfj_hdlist[0])
        headers['Cookie']=count
    
        if(islogon(j,count)):
            JD_Joy()

if __name__ == '__main__':
       start()
