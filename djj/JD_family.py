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




djj_bark_cookie=''
djj_sever_jiang=''
djj_xfj_token=''
djj_xfj_headers=''
djj_djj_cookie=''
#删除





#删除
result=''
JD_API_HOST = 'https://wq.jd.com/activep3/family/'
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


def JD_family():
   print('family_query\n')
   try:
      queryRes=family_query()
      queryRes=json.loads(queryRes[18:-14].strip())
      Tasklst=queryRes['tasklist']
      print(Tasklst)
      for item in Tasklst:
        doTask(item['taskid'])
        time.sleep(2)
        queryRes=family_query()
      queryRes=json.loads(queryRes[18:-14].strip())
      Tasklst=queryRes['tasklist']
      print(Tasklst)
   except Exception as e:
      msg=str(e)
      print(msg)






def doTask(taskId):
    TaskRes=iosrule('family_task',f'''taskid={taskId}&''')
    print(TaskRes)
    return TaskRes

def family_query():
    getTaskRes=iosrule('family_query')
    print(getTaskRes)
    return getTaskRes
    
def iosrule(mod,task=''):
   tm=round(time.time()*1000)
   url=JD_API_HOST+f'''{mod}?activeid=10073670&token={djj_xfj_token}&sceneval=2&{task}callback=CheckParamsf&_={tm}'''
   try:
     response=requests.get(url,headers=djj_xfj_headers).text
     return response
   except Exception as e:
      print(f'''初始化{mode}任务:''', str(e))
      
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
   cookiesList=[]
   xfj_hdlist=[]
   xfj_tklist=[]
   global djj_xfj_token
   global djj_xfj_headers
   global djj_djj_cookie
   check('djj_xfj_token',xfj_tklist)
   check('djj_xfj_headers',xfj_hdlist)
   check('djj_djj_cookie',cookiesList)
   
   j=0
   for count in cookiesList:
     j+=1
     if j!=1:
       continue
     djj_xfj_headers=eval(xfj_hdlist[j-1])
     djj_xfj_headers['Cookie']=count
     djj_xfj_token=xfj_tklist[j-1]
     if(islogon(j,count)):
         JD_family()

if __name__ == '__main__':
       start()
