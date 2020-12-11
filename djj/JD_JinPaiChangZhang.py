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



djj_sharecode=''
djj_bark_cookie=''
djj_sever_jiang=''
djj_djj_cookie=''

Defalt_ShareCode=['x7WCky9PesrFuc-4Q_7ZNy53iayjI4M9nB9i4TsSDvU=','5Rys-86k-gdnFNTINn-8mfat98gKuYUg85xqkRm8PPc=']

JD_API_HOST = 'https://m.jingxi.com'
codeurl='http://api.turinglabs.net/api/v1/jd/jxstory/read/'
headers={
      'Host': 'm.jingxi.com',
      'Accept': '*/*',
       'User-Agent': "jdpingou;iPhone;3.15.2;13.5.1;90bab9217f465a83a99c0b554a946b0b0d5c2f7a;network/wifi;model/iPhone12,1;appBuild/100365;ADID/696F8BD2-0820-405C-AFC0-3C6D028040E5;supportApplePay/1;hasUPPay/0;pushNoticeIsOpen/1;hasOCPay/0;supportBestPay/0;session/14;pap/JA2015_311210;brand/apple;supportJDSHWK/1;",
      'Accept-Language': 'zh-cn',
      'Referer': 'https://st.jingxi.com/pingou/jx_factory_story/index.html',
      'Accept-Encoding': 'gzip, deflate, br',
    }

      
    
cookiesList=[]
result=''
ele=0
randomCount=5
click=True
currentMoneyNum=0
def JX_Jinpaichangzhang():
   userInfo()
   SignIn()
   doHelp()
   taskList()
   for i in range(round(currentMoneyNum/20000)):
    upgrade()
    cardList()
    if(click):
      increase()

def userInfo():
   print('\n userInfo')
   global currentMoneyNum
   currentMoneyNum=0
   
   try:
     dt=datetime.today().strftime('%Y%m%d')
     data=json.loads(iosrule('GetUserInfo'))
     #print(data)
     if (data['ret'] == 0):
       data = data['data']
       shareId = data['shareId']
       print(f'''分享码:{data['shareId']}''')
       currentMoneyNum = data['currentMoneyNum']
   except Exception as e:
      msg=str(e)
      print(msg)

def SignIn():
   print('\n sign')
   try:
     dt=datetime.today().strftime('%Y%m%d')
     data=json.loads(iosrule('SignIn','date='+dt+'&type=0'))
     print(data)
     if (data['ret'] == 0):
       print(f'''签到钞票：收取成功，获得 {data['data']['rewardMoneyToday']}''')
     else:
       print(f'''签到钞票：收取失败，{data['msg']}''')
   except Exception as e:
      msg=str(e)
      print(msg)


def cardList():
   for i in range(10):
     readyCard(i)
     time.sleep(1)
def readyCard(index):
   try:
     print('💎准备机会')
     data=json.loads(iosrule('ReadyCard'))
     #print(data)
     if(data['ret']==0 and data['data']['flopFinishNumber']<data['data']['flopNumber']):
       cardInfo_ = data['data']['cardInfo']
       cardInfo=[]
       for i in range(len(cardInfo_)):
         temp= {
                  "cardId" : cardInfo_[i]['cardId'],
                  "cardPosition" : i+1,
                  "cardStatus" :0
                }
         
         cardInfo.append(temp)

       cardInfo[0]['cardStatus'] = 1
       print(cardInfo)
       selectCard(cardInfo)
   except Exception as e:
      msg=str(e)
      print(msg)


def selectCard(cardInfo):
   try:
     print('🍋🍋🍋🍋开始选择')
     data=json.loads(iosrule('SelectCard','cardInfo='+urllib.parse.quote(json.dumps({"cardInfo":cardInfo}))))
     #print(data)
     if(data['ret']==0):
       finishCard(cardInfo[0]['cardId'])
   except Exception as e:
      msg=str(e)
      print(msg)
def finishCard(cardId):
   print('🍋🍋🍋🍋完成卡片')
   try:
     data=json.loads(iosrule('FinishCard','cardInfo='+str(cardId)))
     print(data)
     if(data['ret']==0):
        ratio = data['data']['cardInfo']
        print(f'''翻倍成功，获得{ratio}%，共计获得{data['data']['earnRatio']}%''')
   except Exception as e:
      msg=str(e)
      print(msg)
def upgrade():
   try:
     dt=datetime.today().strftime('%Y%m%d')
     data=json.loads(iosrule('UpgradeUserLevelDraw','date='+dt+'&type=0'))
     #print(data)
     if (data['ret'] ==0 and data['data']['active']):
        print(f'''升级成功，获得{data['data']}''')
   except Exception as e:
      msg=str(e)
      print(msg)
def increase():
   global click
   try:
     data=json.loads(iosrule('IncreaseUserMoney'))
     print(data)
     if (data['ret'] == 0):
        print(f'''点击厂长成功，获得 {data['data']['moneyNum']} 钞票''')
     elif(data['ret'] == 2005):
          click = false
     else:
          print('点击厂长过快，休息25秒')
          time.sleep(25)
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


def taskList():
   try:
     data=json.loads(iosrulex('GetUserTaskStatusList'))
     #print(data)
     userTaskStatusList = data['data']['userTaskStatusList']
     for i in range(len(userTaskStatusList)):
       vo = userTaskStatusList[i];
       if (not vo['awardStatus']==1):
          if (vo['completedTimes'] >= vo['targetTimes']):
              print(f'''任务:{vo['description']}可完成''')
              completeTask(vo['taskId'], vo['taskName'])
              time.sleep(1)
          else:
            if(vo["taskType"]==2 or vo["taskType"]==6 or vo["taskType"]==9):
               for i in range(vo['configTargetTimes']-vo['completedTimes']):
                  print(f'''去做任务：{vo['taskName']}''')
                  doTask(vo['taskId'])
                  completeTask(vo['taskId'], vo['taskName'])
                  time.sleep(1)
   except Exception as e:
      msg=str(e)
      print(msg)
      
    
      
      
      
def completeTask(taskId, taskName):
   try:
     global ele
     data=json.loads(iosrulex('Award',taskId))
     #print(data)
     sw=data['data']['awardStatus']
     if (sw==1):
       ele += int(data['data']['prizeInfo'].replace('\\n', ''))
       print(f'''领取{taskName}任务奖励成功，收获：{data['data']['prizeInfo']}钞票''')
     elif(sw==0 or sw==1013):
        print(f'''领取{taskName}任务奖励失败，任务已领奖''')
     else:
        print(f'''领取{taskName}任务奖励失败，任务已领奖''')
   except Exception as e:
      msg=str(e)
      print(msg)
      

def doTask(taskId):
   try:
     data=json.loads(iosrulex('DoTask',taskId))
     print(data)
     if (data['ret'] == 0):
         print("做任务完成！")
     else:
        print('做任务失败')
   except Exception as e:
      msg=str(e)
      print(msg)
      




def doHelp():
   try:
      newShareCodes=shareCodesFormat()
      for code in newShareCodes:
          print(f'''开始助力京东账号{code}''')
          if (not code):
    	        continue
          if (code ==encryptPin):
             print('\n跳过自己的code \n')
             continue
          print(f'''\n开始助力好友: {code}''')
          helpResult= helpShare(code)
          if (helpResult and helpResult['ret'] == 0):
               print(f'''助力朋友：{code}成功，因一次只能助力一个，故跳出助力''')
               break
          elif (helpResult and helpResult['ret'] == 11009):
             print(f'''助力朋友[{code}]失败：{helpResult.msg}，跳出助力''')
             break
          else:
            print(f'''`助力朋友[{code}]失败:{helpResult.msg}''')
   except Exception as e:
       pass
def helpShare(code):
   try:
     data=iosrule('AssistFriend','shareId='+code)
     print(data)
     if (data['ret'] == 0):
        print(f'''助力朋友：{shareId}成功''')
     else:
        print(f'''助力朋友[{shareId}]失败:{data['msg']}''')
   except Exception as e:
    	print(str(e))
def readShareCode():
   url=f'''{codeurl}{randomCount}/'''
   try:
      readShareCodeRes=json.loads(requests.get(url).text)
      print(f'''随机取个{randomCount}码放到您固定的互助码后面''')
      return readShareCodeRes
   except Exception as e:
    	pass

def shareCodesFormat():
   newShareCodes = []
  # print(ShareCode)
   #ShareCode=''
   if(djj_sharecode):
      for line in djj_sharecode.split('\n'):
         if not line:
          continue 
         newShareCodes.append(line)
   else:
        print('Github助力码参数读取空，开始读取默认助力码')
        readShareCodeRes = readShareCode()
        print(readShareCodeRes)
        if (readShareCodeRes and readShareCodeRes['code'] == 200):
          newShareCodes=Defalt_ShareCode+readShareCodeRes['data']
        else:
            newShareCodes=Defalt_ShareCode
   print(f'''京东账号将要助力的好友{newShareCodes}''')
   return newShareCodes





    
def iosrule(functionId,body=''):
   url=JD_API_HOST+f'''/jxstory/userinfo/{functionId}?bizcode=jxstory&{body}&sceneval=2&g_login_type=1&_time={round(time.time()*1000)}&={round(time.time()*1000)+6}'''
   #print(url)
   try:
     response=requests.get(url,headers=headers).text
     return response
   except Exception as e:
      print(f'''初始化{functionId}任务:''', str(e))
def iosrulex(functionId,taskId=''):
   url=JD_API_HOST+f'''/newtasksys/newtasksys_front/{functionId}?source=jxstory&bizCode=jxstory&sceneval=2&g_login_type=1&&_time={round(time.time()*1000)}&={round(time.time()*1000)+1}'''
   #print(url)
   if (taskId):
      url += f'''&taskId={taskId}'''
   try:
     response=requests.get(url,headers=headers).text
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
    for i in count.split(';'):
       if i.find('pin=')>=0:
          newstr=i.strip()[i.find('pin=')+4:len(i)]
          print(f'''>>>>>>>>>【账号{str(j)}开始】{newstr}''')
    if(TotalBean(count,newstr)):
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
   global djj_shop_headers
   check()
   j=0
   for count in cookiesList:
     j+=1
     headers['Cookie']=count
     if(islogon(j,count)):
         JX_Jinpaichangzhang()

if __name__ == '__main__':
       start()
