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

result=''
osenviron={}
headers={}
djj_bark_cookie=''
djj_sever_jiang=''
djj_djj_cookie=''
djj_tele_cookie=''
cookiesList=[]
hdList=[]
shopid=''
info={}
Taskinfo={}






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
       if ckresult['retcode']==0:
           signmd5=True
           print(f'''【京东{checkck}】''')
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
   family_info()
   family_query()
   family_taskdone()
   family_query(True)

def family_taskdone():
    try:
     for ts in info['config']['tasks']:
          print(ts['_id'])
          doTask(ts['_id'])
          time.sleep(2)
    except Exception as e:
      print(f'''family_info''', str(e))

def family_info():
    global info
    try:
     url='https://anmp.jd.com/babelDiy/Zeus/2ZpHzZdUuvWxMJT4KXuRdK6NPj3D/index.html?'
     rs=requests.get(url,headers=headers)
     rs.encoding=rs.apparent_encoding
     rs=rs.text
     txt=re.compile('var snsConfig = (.*)').findall(rs)
     tmp=txt[0]
     info=json.loads(tmp)
     print('startTime:',info['startTime'])
     print('endTime:',info['endTime'])
     #print(info)
    except Exception as e:
      print(f'''family_info''', str(e))
    


def doTask(taskId):
   try:
     url='https://wq.jd.com/activep3/family/family_task?activeid='+info['activeId']+'&token='+info['actToken']+'&sceneval=2&t='+tm13()+'&taskid='+taskId+'&callback=CheckParamsk&_='+tm13()
     headers['Referer']='https://anmp.jd.com/babelDiy/Zeus/2ZpHzZdUuvWxMJT4KXuRdK6NPj3D/index.html?sid=48f799c83f7c55bfc3eedd9882a20c8w&'
     rs=requests.get(url,headers=headers)
     rs.encoding=rs.apparent_encoding
     rs=rs.text
     txt=rs[rs.find('({')+1:rs.find(');')]
     shop=json.loads(txt)
     #print(shop)
   except Exception as e:
      print(f'''doTask''', str(e))

def family_query(X=False):
    global info,Taskinfo
    try:
     url='https://wq.jd.com/activep3/family/family_query?activeid='+info['activeId']+'&token='+info['actToken']+'&sceneval=2&t=&callback=CheckParamsl&_='
     headers['Referer']='https://anmp.jd.com/babelDiy/Zeus/2ZpHzZdUuvWxMJT4KXuRdK6NPj3D/index.html?'
     rs=requests.get(url,headers=headers)
     rs.encoding=rs.apparent_encoding
     rs=rs.text
     txt=re.compile('CheckParamsl\((.*)').findall(rs)
     #print(txt)
     tmp=txt[0]
     Taskinfo=json.loads(tmp)
     msg='幸福值:'+Taskinfo['tatalprofits']
     if X==True:
       loger(msg)
    except Exception as e:
      print(f'''family_query''', str(e))
    

def check(flag,list):
   vip=''
   global djj_bark_cookie
   global djj_sever_jiang
   global djj_tele_cookie
   if "DJJ_BARK_COOKIE" in os.environ:
      djj_bark_cookie = os.environ["DJJ_BARK_COOKIE"]
   if "DJJ_TELE_COOKIE" in os.environ:
      djj_tele_cookie = os.environ["DJJ_TELE_COOKIE"]
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
       
def pushmsg(title,txt,bflag=1,wflag=1,tflag=1):
  try:
   txt=urllib.parse.quote(txt)
   title=urllib.parse.quote(title)
   if bflag==1 and djj_bark_cookie.strip():
      print("\n【通知汇总】")
      purl = f'''https://api.day.app/{djj_bark_cookie}/{title}/{txt}'''
      response = requests.post(purl)
      #print(response.text)
   if tflag==1 and djj_tele_cookie.strip():
      print("\n【Telegram消息】")
      id=djj_tele_cookie[djj_tele_cookie.find('@')+1:len(djj_tele_cookie)]
      botid=djj_tele_cookie[0:djj_tele_cookie.find('@')]

      turl=f'''https://api.telegram.org/bot{botid}/sendMessage?chat_id={id}&text={title}\n{txt}'''

      response = requests.get(turl)
      #print(response.text)
   if wflag==1 and djj_sever_jiang.strip():
      print("\n【微信消息】")
      purl = f'''http://sc.ftqq.com/{djj_sever_jiang}.send'''
      headers={
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
    }
      body=f'''text={txt})&desp={title}'''
      response = requests.post(purl,headers=headers,data=body)
    #print(response.text)
  except Exception as e:
      msg=str(e)
      print(msg)
    
def loger(m):
   #print(m)
   global result
   result +=m
def tm13():
   Localtime=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f", )
   timeArray = datetime.strptime(Localtime, "%Y-%m-%d %H:%M:%S.%f")
   timeStamp = int(time.mktime(timeArray.timetuple())*1000+timeArray.microsecond/1000)
   return str(timeStamp)   
    
def islogon(j,count):
    JD_islogn=False 
    for i in count.split(';'):
       if i.find('pin=')>=0:
          newstr=i.strip()[i.find('pin=')+4:len(i)]
          
          msg=f'''【账号{str(j)}】{newstr}|'''
          print('>>>>>>>>>'+msg)
          loger(msg)
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
   global cookiesList,hdList
   global headers,result
   check('DJJ_DJJ_COOKIE',cookiesList)
   check('DJJ_XFJ_NEWHEADERS',hdList)
   j=0
   for count in cookiesList:
     j+=1
     headers=eval(hdList[0])
     headers['Cookie']=count
     if(islogon(j,count)):
         JD_family()
     time.sleep(10)
     result+='\n'
   pushmsg('主库-XFJ',result)
if __name__ == '__main__':
       start()
