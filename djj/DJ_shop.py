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




djj_djj_cookie=''

JD_API_HOST = 'https://api.m.jd.com/client.action'

headers={"Host": "api.m.jd.com","User-Agent": "JD4iPhone/167151 (iPhone; iOS 12.4; Scale/2.00)",}
cookiesList=[]
result=''


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


def JD_SHOP():
      print('进店\n')
      beanCount = 0
 
      taskData=json.loads(getTask())
      if(taskData['code'] == '0'):
        if (json.dumps(taskData).find('taskErrorTips')>0):
           print(f'''{taskData['data']['taskErrorTips']}\n''')
        else:
           
           taskList  = taskData['data']['taskList']
           for item in taskList:
             if (item['taskStatus']== 3):
                print(f'''{item['shopName']} 已拿到2京豆\n''')
             else:
                print(f'''taskId:{item['taskId']}''')
                doTaskRes =json.loads(doTask(item['taskId']))
                if(doTaskRes['code'] =='0'):
                   beanCount += 2
          
        print(f'''beanCount::{beanCount}''')
        if(beanCount > 0):
           print(f'''成功领取{beanCount}京豆''')





def doTask(taskId):
    body = {'taskId': str(taskId)};
    takeTaskRes=iosrule('takeTask',body)
    print(takeTaskRes)
    return takeTaskRes

def getTask():
    getTaskRes=iosrule('queryTaskIndex')
    #print(getTaskRes)
    return getTaskRes
    
def iosrule(mod,body={}):
   url=JD_API_HOST+f'''?functionId={mod}&appid=ld&body={urllib.parse.quote(json.dumps(body))}'''
   try:
     response=requests.get(url,headers=headers).text
     return response
   except Exception as e:
      print(f'''初始化{mode}任务:''', str(e))
      

      
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
         JD_SHOP()

if __name__ == '__main__':
       start()
