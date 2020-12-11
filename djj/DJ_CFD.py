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

Defalt_ShareCode=['B8CB4F09962CFB8F35187ADF71D4F522F5CCA648B7EFAA05C0C77DB56CCD6317','2F8FC80C8A065332B368DBB9401F1F93F5CCA648B7EFAA05C0C77DB56CCD6317']

JD_API_HOST = 'https://m.jingxi.com'
headers={}

      


cookiesList=[]
result=''
jd_name=''
info={}


def myhd(hd):
   hd=eval(hd)
   hd['Referer']='https://st.jingxi.com/fortune_island/index.html?'
   return hd
   
   
def JX_CaiFuDao():
   userInfo()
   querySignList()
   submitShareCode()
   doHelp()
   getTaskList_daily()
   getTaskList_achiv()
   treasureHunt()
   
   
def userInfo():
   print('\n userInfo')
   global info
   info={}
   try:
     data=json.loads(iosrule('user/QueryUserInfo'))
     #print(data)
     if (data['iRet'] == 0):
       info={
          'SceneList':data['SceneList'],
          'ddwMoney':data['ddwMoney'],
          'strMyShareId':data['strMyShareId'],
          'strPin':data['strPin']}
       print(info)
   except Exception as e:
      msg=str(e)
      print(msg)

def querySignList():
   print('\n querySignList')
   try:
     data=json.loads(iosrule('task/QuerySignListV2'))
     #print(data)
     if (data['iRet'] == 0):
       for i in data['sData']['Sign']:
          if(i['dwStatus']==0):
             userSignReward(i['ddwMoney'])
   except Exception as e:
      msg=str(e)
      print(msg)
def userSignReward(ddwMoney):
   print('\n userSignReward')
   try:
     data=json.loads(iosrule('task/UserSignRewardV2','dwReqUserFlag=1&ddwMoney='+str(ddwMoney)))
     print(data)
     if (data['iRet'] == 0):
        print(f'''获得财富 {data['sData']['dwMoney']}''')
   except Exception as e:
      msg=str(e)
      print(msg)




def getTaskList_daily():
   try:
     print('💎getTaskList_daily')
     data=json.loads(iosrulex('GetUserTaskStatusList'))
     #print(data)
     tsl=data['data']['userTaskStatusList']
     print(f'''\n获取【日常任务】列表tsl，总共{len(tsl)}个任务！\n''')
     j=0
     for item in tsl:
      if(not item['awardStatus']==1):
        j+=1
        print(f'''开始第【{j}】个任务中......''')
        if(item['completedTimes']<item['configTargetTimes']):
           dailyres=dotask_daily(item['taskId'])
          
           if(dailyres['ret']==0):
              print(f'''成功做任务''')
           else:
              print(f'''{dailyres['msg']}''')
              #break
           time.sleep(2)
        else:
         awardTask_daily(item['taskId'])
          
   except Exception as e:
      msg=str(e)
      print(msg)
def dotask_daily(taskId):
   try:
     print('💎dotask_daily')
     data=json.loads(iosrulex('DoTask','taskId='+str(taskId)))
     #print(data)
     return data
   except Exception as e:
      msg=str(e)
      print(msg)
def awardTask_daily(taskId):
   try:
     print('awardTask_daily')
     data=json.loads(iosrulex('Award','taskId='+str(taskId)))
     #print(data)
     if(data['ret']==0):
       print(f'''奖励{data['data']['prizeInfo']['RedPack']}''')
     else:
       print(f'''{data['msg']}''')
   except Exception as e:
      msg=str(e)
      print(msg)
      
      
      
def getTaskList_achiv():
   try:
     print('💎getTaskList_achiv')
     data=json.loads(iosrule('consume/AchieveInfo'))
     #print(data)
     tsl=data['taskinfo']
     print(f'''\n获取【成就任务】列表tsl，总共{len(tsl)}个任务！\n''')
     for item in tsl:
      if(item['dwAwardStatus']==0):
         print(f'''{item['strTaskDescr']}【领成就奖励】：该成就任务未达到门槛''')
      else:
         awardTask_achive(item)
   except Exception as e:
      msg=str(e)
      print(msg)
      
      
      
def awardTask_achive(taskinfo):
   try:
     print('awardTask_achive')
     data=json.loads(iosrule('consume/AchieveAward','strTaskIndex='+taskinfo['strTaskIndex']))
     #print(data)
     print(f'''{data['strTaskDescr']}【领成就奖励】： success,领获得财富值{data['dwExpericnce']}''')
     time.sleep(2)
   except Exception as e:
      msg=str(e)
      print(msg)
      
def treasureHunt():
   try:
     print('\n treasureHunt')
     for place in ["tree", "wood", "small_stone"]:
        data=json.loads(iosrule('consume/TreasureHunt','strIndex='+place+'&dwIsShare=0'))
        #print(data)
        if(data['iRet']==0):
          print(f'''【获取随机奖励】： success,领获得财富值{data['dwExpericnce']}''')
        else:
          print(data['sErrMsg'])
        time.sleep(2)
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
          pushmsg('JD_treasure',msg)
   except Exception as e:
      signmd5=False
      msg=str(e)
      print(msg)
      pushmsg('京东cookie',msg)
   return signmd5




def doHelp():
   try:
      newShareCodes=shareCodesFormat()
      index=0
      for code in newShareCodes:
          index+=1
          print(f'''【{index}】,开始助力京东账号{code}''')
          if (not code):
    	        continue
          if (code ==info['strMyShareId']):
             print(f'''\n跳过自己的{code} \n''')
             continue
          print(f'''\n开始助力好友: ''')
          helpResult= json.loads(helpShare(code))
          if (helpResult and helpResult['iRet'] ==0):
             print(f'''助力朋友：成功''')
          else:
             print(f'''助力朋友失败:{helpResult['sErrMsg']}''')
   except Exception as e:
       print(str(e))
def helpShare(code):
   print('助力请求::::::::::')
   try:
     data=iosrule('user/JoinScene','strShareId='+code+'&dwSceneId=1001')
     #print(data)
     return data
   except Exception as e:
    	print(str(e))
def readShareCode():
   print('\n  readShareCode')
   url='https://api.ninesix.cc/api/jx-cfd'
   try:
      readShareCodeRes=requests.get(url).json()
      return readShareCodeRes
   except Exception as e:
    	pass

def shareCodesFormat():
   newShareCodes = []
  # print(ShareCode)
   #ShareCode=''
   print('开始读取默认助力码')
   readShareCodeRes = readShareCode()
   #print(readShareCodeRes)
   if (readShareCodeRes and readShareCodeRes['code'] == 200):
        #print(readShareCodeRes['data']['value'])
        newShareCodes.append(readShareCodeRes['data']['value'])
        newShareCodes=Defalt_ShareCode+newShareCodes
        print('添加完毕:',newShareCodes)
   else:
        newShareCodes=Defalt_ShareCode
   print(f'''京东账号将要助力的好友{newShareCodes}''')
   return newShareCodes

def submitShareCode():
   print('\n提交验证码')
   try:
      url=f'''https://api.ninesix.cc/api/jx-cfd/{info['strMyShareId']}/{jd_name}'''
      response=requests.post(url).json()
      #print(response)
      if(response['data']['value']):
      	print('邀请码提交成功')
   except Exception as e:
    	print(str(e))




    
def iosrule(functionId,body=''):
   url=JD_API_HOST+f'''/jxcfd/{functionId}?strZone=jxcfd&bizCode=jxcfd&source=jxcfd&dwEnv=7&_cfd_t={round(time.time()*1000)}&ptag=138631.26.55&{body}&_ste=1&_={round(time.time()*1000)+5}&sceneval=2&g_login_type=1&g_ty=ls'''

   try:
      response=requests.get(url,headers=headers).text
      return response
   except Exception as e:
     print(f'''初始化{functionId}任务:''', str(e))
def iosrulex(functionId,body=''):
   url=JD_API_HOST+f'''/newtasksys/newtasksys_front/{functionId}?strZone=jxcfd&bizCode=jxcfd&source=jxcfd&dwEnv=7&_cfd_t={round(time.time()*1000)}&ptag=138631.26.55&{body}&_ste=1&_={round(time.time()*1000)+5}&sceneval=2&g_login_type=1&g_ty=ls'''
   #print(url)
   try:
     response=requests.get(url,headers=headers).text
     return response
   except Exception as e:
      print(f'''初始化{functionId}任务:''', str(e))

      
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
   for count in cookiesList:
     j+=1
     headers=myhd(xfj_hdlist[0])
     headers['Cookie']=count
    
     if(islogon(j,count)):
         JX_CaiFuDao()

if __name__ == '__main__':
       start()
