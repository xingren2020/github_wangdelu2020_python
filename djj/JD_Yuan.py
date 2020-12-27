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

djj_bark_cookie=''
djj_sever_jiang=''


JD_API_HOST = 'https://daojia.jd.com/client?_jdrandom=1609034402844'

yuanck=''
cookiesList=[]
yuanckList=[]
result=''

def JD_XIANDOU():
   tasklist()
 
   signin_carveUp()
   plantBeans_getWater()
   
   loop_wartering()
   

  
 

 
 

       
       
       
def plantBeans_getActivityInfo():
   print('\n  plantBeans_getActivityInfo')
   try:
     body ={}
     body=urllib.parse.quote(json.dumps(body))
     data=json.loads(iosrulex('functionId=plantBeans%2FgetActivityInfo&isNeedDealError=true&method=POST&body='+body).text)
     #print(data)

     return data

   except Exception as e:
       print(str(e))
       
       
       
       
def ttmsg():
   print('\n  ttmsg')
   try:
      data=plantBeans_getActivityInfo()
      msg=f'''{data['result']['cur']['activityDay']}|{data['result']['cur']['level']}|{data['result']['cur']['water']}|{data['result']['cur']['levelProgress']}-{data['result']['cur']['totalProgress']}'''
      #print(msg)
      loger(msg)
   except Exception as e:
         print(str(e))
def loop_wartering():
     print('\n  loop_wartering')
     try:
         data=plantBeans_getActivityInfo()
         print(f'''
   【activityDay】{data['result']['cur']['activityDay']}
   【level】{data['result']['cur']['level']}
   【water】{data['result']['cur']['water']}
   【waterCart】{data['result']['cur']['waterCart']}/300
   【dailyWater】{data['result']['cur']['dailyWater']}
   【levelProgress/totalProgress】{data['result']['cur']['levelProgress']}/{data['result']['cur']['totalProgress']}''')
         water_=data['result']['cur']['totalProgress']-data['result']['cur']['levelProgress']
         if data['result']['cur']['water']>=water_:
           for i in range(int(water_/100)+1):
              print('第'+str(int(water_/100)+1)+'-'+str(i+1)+'次浇水')
              plantBeans_watering()
              time.sleep(1)
           print('\n  完成循环浇水任务++++')
         ttmsg()
     except Exception as e:
         print(str(e))
def tasklist():
   print('\n tasklist')
   try:
     body = {"modelId":"M10003","plateCode":1}
     data=json.loads(iosrule('task%2Flist',body).text)
     #print(data)
     print('任务列表')
     for itm in data['result']['taskInfoList']:
       if itm['status']==3:
          m='【完成】'
       elif itm['status']==2:
          m='【领奖】'
       else:
          m='【未完成】'
       print(f'''{itm['taskName']}={itm['taskType']}=={m}''')
     print('\n-----------------------')
     for itm in data['result']['taskInfoList']:
       if itm['status']!=3:
         print(f'''开始任务: {itm['taskType']} -{itm['taskName']}-{itm['status']}''')
         if itm['status']==1 or itm['status']==0:
           if itm['taskType']!=506:
            task_received(itm['modelId'],itm['taskId'],itm['taskType'])
            time.sleep(2)
            task_finished(itm['modelId'],itm['taskId'],itm['taskType'])
            if itm['taskType']==502:
               task_do(502)
         if itm['status']==2:
           if itm['taskType']==513:
              task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'],1)
              task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'],2)
              task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'],3)
           else:
           	  task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'])
           time.sleep(2)
   except Exception as e:
       print(str(e))
       



def task_do(taskType):
   print('\n task_do___'+str(taskType))
   try:
      if taskType==401:
         fun='xapp%2FfriendHelp%2Flist'
         body={}
      if taskType==502:
         fun='signin%2FifClickedCouponButton'
         body={}
         
      data=json.loads(iosrule(fun,body).text)
      print(data)
      print(data['msg'])
   except Exception as e:
       print(str(e))
         
         
         
def task_received(modelId,taskId,taskType):
   print('\n task_received')
   try:
     body = {"modelId":modelId,"taskId":taskId,"taskType":taskType,"plateCode":1}
     data=json.loads(iosrule('task%2Freceived',body).text)
     print(data['msg'])
   except Exception as e:
       print(str(e))
       
def task_sendPrize(modelId,taskId,taskType,subNode=1):
   print('\n task_sendPrize')
   try:
     body = {"modelId":modelId,"taskId":taskId,"taskType":taskType,"plateCode":1}
     if taskType==513:
       body = {"modelId":modelId,"taskId":taskId,"taskType":taskType,"plateCode":1,"subNode":subNode}
     
     data=json.loads(iosrule('task%2FsendPrize',body).text)
     print(data['msg'])
   except Exception as e:
       print(str(e))
       
       
def task_finished(modelId,taskId,taskType):
   print('\n task_finished')
   try:
     body = {"modelId":modelId,"taskId":taskId,"taskType":taskType,"plateCode":1}
     data=json.loads(iosrule('task%2Ffinished',body).text)
     print(data['msg'])
   except Exception as e:
       print(str(e))
def signin_carveUp():
   print('\n signin_carveUp')
   try:
     body = {"groupId":"","type":2}
     data=json.loads(iosrule('signin%2FcarveUp%2FcarveUpInfo',body).text)
     print(data)

    
   except Exception as e:
       print(str(e))
       

       
def plantBeans_watering():
   print('\n  plantBeans_watering')
   try:
     body ={"activityId":"23ad8d84d6addad"}
     body=urllib.parse.quote(json.dumps(body))
     data=json.loads(iosrulex('functionId=plantBeans%2Fwatering&isNeedDealError=true&method=POST&body='+body).text)
     print(data)

    
   except Exception as e:
       print(str(e))
       
       
       
def plantBeans_getWater():
   print('\n  plantBeans_getWater')
   try:
     body ={"activityId":"23ad8d84d6addad"}
     body=urllib.parse.quote(json.dumps(body))
     data=json.loads(iosrulex('functionId=plantBeans%2FgetWater&isNeedDealError=true&method=POST&body='+body).text)
     print(data)

    
   except Exception as e:
       print(str(e))




       
def iosrule(functionId,body={}):
   url=JD_API_HOST+f'''&functionId={functionId}&isNeedDealError=true&body={urllib.parse.quote(json.dumps(body))}&channel=ios&platform=6.6.0&platCode=h5&appVersion=6.6.0&appName=paidaojia&deviceModel=appmodel'''

   #print(url)
   try:
      response=requests.get(url,headers=djheaders)
      return response
   except Exception as e:
     print(f'''初始化{functionId}任务:''', str(e))


def iosrulex(body):
   url=JD_API_HOST
   try:
      response=requests.post(url,headers=djheaders,data=body)
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
 

   global djheaders,zyheaders,yuanck,result
   check('DJJ_DAOJIA_COOKIE',cookiesList)
   check('DJJ_YUAN_CK',yuanckList)
   j=0
   #for i in range(2):
   for count in cookiesList:
        djheaders['Cookie']=count
        yuanck=yuanckList[j-1]
        zyheaders['Cookie']=yuanck

        #if(islogon(j,count)):
        JD_XIANDOU()
     #time.sleep(30)
   pushmsg('JD_Xiandou',result)
if __name__ == '__main__':
       start()
