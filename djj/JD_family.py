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
djj_xfj_token=''
djj_xfj_headers=''
djj_djj_cookie=''





headers={"Accept": "*/*","Accept-Encoding": "br, gzip, deflate","Accept-Language": "zh-cn","Host": "wq.jd.com","Referer": "https://lgame.jd.com/babelDiy/Zeus/2dJDkTg31SrzZDAS74ozoKArg7hu/index.html?lng=113.627812&lat=23.278284&sid=632429371578e01154b220fb71e84a0w&un_area=19_1601_50284_50451","User-Agent": "jdapp;iPhone;9.2.4;12.4;3c6b06b6a8d9cc763215d2db748273edc4e02512;network/wifi;ADID/B38160D2-DC94-4414-905B-D15F395FD787;supportApplePay/0;hasUPPay/0;hasOCPay/0;model/iPhone11,8;addressid/3529080897;supportBestPay/0;appBuild/167432;pushNoticeIsOpen/0;jdSupportDarkMode/0;pv/111.4;apprpd/JingDou_Detail;ref/JingDou_Detail_Contrller;psq/3;ads/;psn/3c6b06b6a8d9cc763215d2db748273edc4e02512|259;jdv/0|kong|t_1001848278_|jingfen|dcdae1aff03e4544a2abe5b1fea7ff3b|1606876124750|1606876163;adk/;app_device/IOS;pap/JA2015_311210|9.2.4|IOS 12.4;Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",}












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
   url=JD_API_HOST+f'''{mod}?activeid=10073670&token=92602dfb7b63776469a06deef1a45021&sceneval=2&{task}&callback=CheckParamsf&_={tm}'''
   try:
     response=requests.get(url,headers=headers).text
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
   global headers
   check('DJJ_DJJ_COOKIE',cookiesList)
   
   j=0
   for count in cookiesList:
     j+=1
     headers['Cookie']=count
 
     if(islogon(j,count)):
         JD_family()

if __name__ == '__main__':
       start()
