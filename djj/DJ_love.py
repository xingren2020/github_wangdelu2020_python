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

djj_djj_cookie=''
djj_sharecode=''
djj_bark_cookie=''
djj_sever_jiang=''


JD_API_HOST = 'https://api.m.jd.com/client.action'
headers={
       "origin": "https://h5.m.jd.com",
      "referer": "https://h5.m.jd.com/",
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'jdpingou;iPhone;3.15.2;12.4;fccee6e5e9f146fcedd9be68ef5807568f000c12;network/4g;model/iPhone11,8;appBuild/100365;ADID/B38160D2-DC94-4414-905B-D15F395FD787;supportApplePay/1;hasUPPay/0;pushNoticeIsOpen/1;hasOCPay/0;supportBestPay/0;session/11;pap/JA2015_311210;brand/apple;supportJDSHWK/1;Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    }

      
   
 
    
    
    
    
cookiesList=[]
result=''



#=================================================
def JD_live():
   getTaskList()
   time.sleep(1)
   shareTask()
   time.sleep(2)
   awardTask()
   viewTask()
   time.sleep(2)
   awardViewTask()

def getTaskList():
   print('\n getTaskList')
   try:
     frm=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
     #print(frm)
     body={'timestamp':tmstamp(frm)}
     data=iosrule('liveChannelTaskListToM',body)
     print(data)
   except Exception as e:
      msg=str(e)
      print(msg)
def shareTask():
   print('\n shareTask')
   try:
     body ='body=%7B%22liveId%22%3A%222995233%22%2C%22type%22%3A%22shareTask%22%2C%22authorId%22%3A%22682780%22%2C%22extra%22%3A%7B%22num%22%3A1%7D%7D&build=167408&client=apple&clientVersion=9.2.0&eid=eidIF3CF0112RTIyQTVGQTEtRDVCQy00Qg%3D%3D6HAJa9%2B/4Vedgo62xKQRoAb47%2Bpyu1EQs/6971aUvk0BQAsZLyQAYeid%2BPgbJ9BQoY1RFtkLCLP5OMqU&isBackground=Y&joycious=194&lang=zh_CN&networkType=wifi&networklibtype=JDNetworkBaseAF&openudid=53f4d9c70c1c81f1c8769d2fe2fef0190a3f60d2&osVersion=14.2&partner=TF&rfs=0000&scope=01&screen=1242%2A2208&sign=457d557a0902f43cbdf9fb735d2bcd64&st=1607559819969&sv=110&uts=0f31TVRjBSsxGLJHVBkddxFxBqY/8qFkrfEYLL0gkhB/JVGyEYIoD8r5rLvootZziQYAUyvIPogdJpesEuOMmvlisDx6AR2SEsfp381xPoggwvq8XaMYlOnHUV66TZiSfC%2BSgcLpB2v9cy/0Z41tT%2BuLheoEwBwDDYzANkZjncUI9PDCWpCg5/i0A14XfnsUTfQHbMqa3vwsY6QtsbNsgA%3D%3D&uuid=hjudwgohxzVu96krv/T6Hg%3D%3D'

     res=iosrulex("liveChannelReportDataV912", body)
     print(res)
   except Exception as e:
      msg=str(e)
      print(msg)
      

   
def awardTask():
   print('\n awardTask')
   try:
      frm=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
      body = f'''?functionId=getChannelTaskRewardToM&appid=h5-live&body=%7B%22type%22%3A%22shareTask%22%2C%22liveId%22%3A%222942545%22%7D&v={tmstamp(frm)}'''
      data= response=requests.get('https://api.m.jd.com/api'+body,headers=headers).text
      print(data)
   except Exception as e:
      msg=str(e)
      print(msg)
      
def viewTask():
   print('\n viewTask')
   try:
     body ='body=%7B%22liveId%22%3A%223008300%22%2C%22type%22%3A%22viewTask%22%2C%22authorId%22%3A%22644894%22%2C%22extra%22%3A%7B%22time%22%3A120%7D%7D&build=167408&client=apple&clientVersion=9.2.0&eid=eidIF3CF0112RTIyQTVGQTEtRDVCQy00Qg%3D%3D6HAJa9%2B/4Vedgo62xKQRoAb47%2Bpyu1EQs/6971aUvk0BQAsZLyQAYeid%2BPgbJ9BQoY1RFtkLCLP5OMqU&isBackground=N&joycious=194&openudid=53f4d9c70c1c81f1c8769d2fe2fef0190a3f60d2&osVersion=14.2&partner=TF&rfs=0000&scope=01&sign=90e14adc21c4bf31232a1ded5f4ba40e&st=1607561111999&sv=111&uts=0f31TVRjBSsxGLJHVBkddxFxBqY/8qFkrfEYLL0gkhB/JVGyEYIoD8r5rLvootZziQYAUyvIPogdJpesEuOMmvlisDx6AR2SEsfp381xPoggwvq8XaMYlOnHUV66TZiSfC%2BSgcLpB2v9cy/0Z41tT%2BuLheoEwBwDDYzANkZjncUI9PDCWpCg5/i0A14XfnsUTfQHbMqa3vwsY6QtsbNsgA%3D%3D&uuid=hjudwgohxzVu96krv/T6Hg%3D%3D'

     res=iosrulex("liveChannelReportDataV912", body)
     print(res)
   except Exception as e:
      msg=str(e)
      print(msg)
      

   
def awardViewTask():
   print('\n awardViewTask')
   try:
      frm=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
      body = f'''?functionId=getChannelTaskRewardToM&appid=h5-live&body=%7B%22type%22%3A%22commonViewTask%22%2C%22liveId%22%3A%222942545%22%7D&v={tmstamp(frm)}'''
      data= response=requests.get('https://api.m.jd.com/api'+body,headers=headers).text
      print(data)
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



    
def iosrule(functionId,body=''):
   frm=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
   #print(frm)
   url=JD_API_HOST+f'''?functionId={functionId}&appid=h5-live&body={body}&timestamp={tmstamp(frm)}'''
   #print(url)
   try:
     response=requests.get(url,headers=headers).text
     return response
   except Exception as e:
      print(f'''初始化{functionId}任务:''', str(e))
def iosrulex(functionId,body={}):
   frm=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
   #print(frm)
   url=JD_API_HOST+f'''?functionId={functionId}'''
   #print(url)
   try:
     response=requests.post(url,headers=headers,data=body).text
     return response
   except Exception as e:
      print(f'''初始化{functionId}任务:''', str(e))

#=================================================
def tmstamp(tr):
   tm = dateutil.parser.parse(tr).timestamp()
   return tm

def stamptm(tm,frm='%Y-%m-%d %H:%M:%S'):
   #frm=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
   tr = datetime.datetime.fromtimestamp(tm).strftime(frm)
   return tr



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
         JD_live()

if __name__ == '__main__':
       start()
