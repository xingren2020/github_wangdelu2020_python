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
cookiesList=[]
result=''
wx_dawang_body=''
djj_bark_cookie=''
djj_sever_jiang=''


header={"Accept": "*/*","Accept-Encoding": "br, gzip, deflate","Accept-Language": "zh-cn","Content-Type": "application/json","Host": "www.dawang-goon.cn","Referer": "https://servicewechat.com/wxd9e27d81d505e3b4/49/page-frame.html","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.14(0x17000e2e) NetType/WIFI Language/zh_CN",}
Mit = 'https://www.dawang-goon.cn/api/jbs/'
def Wx_dawang(j,id):
   sign(j,id)
   getinfos(j,id)
def sign(j,id):
   print('\sign')
   try:
     body = {}
     body['id']=id
     response = requests.post(Mit+sys._getframe().f_code.co_name,headers=header,data=json.dumps(body))
     Res=response.json()
     #print(Res)
   except Exception as e:
      msg=str(e)
      print(msg)

def getinfos(j,id):
   print('\score')
   msg='🔔🔔【Count】'+str(j)+':🔔🔔\n'
   try:
     body = {}
     body['id']=id
     response = requests.post(Mit+sys._getframe().f_code.co_name,headers=header,data=json.dumps(body))
     Res=response.json()
     if(Res['error']==0):
       sg=Res['infos']['1']
       if(json.dumps(sg).find(r'\u7b7e\u5230\u9001\u91d1\u5e01')>0):
         tm=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d")
         if(sg[0]['created'].find(tm)>=0):
            msg+='【sign】today✌🏻️success.\n'
            msg+=f'''【score】:{sg[0]['score']}💰,signtime:{sg[0]['created']}⏰\n'''
            if(len(sg)>2):
               msg+=f'''【score】:{sg[1]['score']}💰,signtime:{sg[1]['created']}⏰'''
            
          
         else:
            msg+='【sign】today failed❌\n'
            msg+=f'''【score】:{sg[0]['score']}💰,signtime:{sg[0]['created']}⏰'''
       msg+=Res['score']
     else:
     	msg+='cookies need update❌'
   except Exception as e:
      msg+=str(e)
   loger(msg)
    


      

def check():
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   global wx_dawang_body
   global djj_bark_cookie
   global djj_sever_jiang
   if "DJJ_BARK_COOKIE" in os.environ:
     djj_bark_cookie = os.environ["DJJ_BARK_COOKIE"]
   if "DJJ_SEVER_JIANG" in os.environ:
      djj_sever_jiang = os.environ["DJJ_SEVER_JIANG"]
   if "WX_DAWANG_BODY" in os.environ:
      wx_dawang_body = os.environ["WX_DAWANG_BODY"]
   if "WX_DAWANG_BODY" in osenviron:
      wx_dawang_body = osenviron["WX_DAWANG_BODY"]
      for line in wx_dawang_body.split('\n'):
        if not line:
          continue 
        cookiesList.append(line.strip())
   elif wx_dawang_body:
       for line in wx_dawang_body.split('\n'):
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
    

   
   
def clock(func):
    def clocked(*args, **kwargs):
        t0 = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[🔔speed time:%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
    
@clock
def start():
   check()
   j=0
   for count in cookiesList:
     j+=1
     Wx_dawang(j,count)
   pushmsg('wx_dawang_sign',result)
def main_handler(event, context):
    return start()

if __name__ == '__main__':
       start()
