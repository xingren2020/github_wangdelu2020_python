# encoding:utf-8
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
headers={}
info={}
userInfo={}
djj_bark_cookie=''
djj_sever_jiang=''
djj_tele_cookie=''
djj_djj_cookie=''

encryptProjectId=''
'''
抽奖可获得京豆和快递优惠券
活动时间：2021年1月15日至2021年2月19日
活动入口：https://snsdesign.jd.com/babelDiy/Zeus/4N5phvUAqZsGWBNGVJWmufXoBzpt/index.html?channel=lingsns003&scope=0&sceneid=9001&btnTips=&hideApp=0

'''


headers={'Accept': 'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5'}









#删除
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


def JD_Geziyaya():
     JD_getInfo()
     JD_getUserInfo()
     while (userInfo['bless'] >= userInfo['cost_bless_one_time']):
       JD_draw()
       JD_getUserInfo()
       time.sleep(2)
def JD_getInfo():
   print('getInfo\n')
   global info
   try:
      rs= requests.get('https://snsdesign.jd.com/babelDiy/Zeus/4N5phvUAqZsGWBNGVJWmufXoBzpt/index.html?channel=lingsns003&scope=0&sceneid=9001&btnTips=&hideApp=0',headers=headers,timeout=10)
      rs.encoding=rs.apparent_encoding
      rs=rs.text
      txt=re.compile('var snsConfig = (.*)').findall(rs)
      tmp=txt[0]
      
      info=json.loads(tmp)
      #print(info)
    
   except Exception as e:
      msg=str(e)
      print(msg)
def JD_getUserInfo():
   print('getUserInfo\n')
   try:
      global userInfo
      body = 'activeid='+info['activeId']+'&token='+info['actToken']+'&sceneval=2&shareid=&_=&callback=query&'
      url='https://wq.jd.com/activet2/piggybank/query?'+body
      headers['Referer']='https://anmp.jd.com/babelDiy/Zeus/xKACpgVjVJM7zPKbd5AGCij5yV9/index.html?wxAppName=jd'
      
      rs= requests.get(url,headers=headers,timeout=10)
      rs.encoding=rs.apparent_encoding
      rs=rs.text
      #print(rs)
      txt=re.compile('query\((.*)').findall(rs)
      tmp=txt[0]
      userInfo=json.loads(tmp)
      userInfo=userInfo['data']
      print('当前幸运值：'+str(userInfo['bless']))
      print(userInfo['complete_task_list'])
      for task in info['config']['tasks']:
       if len(userInfo['complete_task_list'])==0:
          print('去做任务'+task['_id'])
          doTask(task['_id'])
       else:
          if task['_id'] not in userInfo['complete_task_list']:
             print('去做任务'+task['_id'])
             doTask(task['_id'])
   except Exception as e:
      msg=str(e)
      print(msg)
      
      
      



def doTask(taskId):
   print('doTask\n')
   global userInfo
   try:
      body = 'activeid='+info['activeId']+'&token='+info['actToken']+'&sceneval=2&shareid=&_=&callback=query&'+'task_bless=10&taskid='+taskId
      url='https://wq.jd.com/activet2/piggybank/completeTask?'+body
      headers['Referer']='https://anmp.jd.com/babelDiy/Zeus/xKACpgVjVJM7zPKbd5AGCij5yV9/index.html?wxAppName=jd'
      
      rs= requests.get(url,headers=headers,timeout=10)
      rs.encoding=rs.apparent_encoding
      rs=rs.text
      txt=re.compile('query\((.*)').findall(rs)
      tmp=txt[0]
      if tmp.find('curbless')>0:
         tmp=json.loads(tmp)
         userInfo['bless'] = tmp['data']['curbless']
         print('任务完成成功，当前幸运值:'+str(tmp['data']['curbless']))
         
      else:
         print('任务重复======')
      
      

      time.sleep(1)
            

   except Exception as e:
      msg=str(e)
      print(msg)


def JD_draw():
   print('draw\n')
   try:
      body = 'activeid='+info['activeId']+'&token='+info['actToken']+'&sceneval=2&shareid=&_=&callback=query&'
      url='https://wq.jd.com/activet2/piggybank/draw?'+body
      headers['Referer']='https://anmp.jd.com/babelDiy/Zeus/xKACpgVjVJM7zPKbd5AGCij5yV9/index.html?wxAppName=jd'
      rs= requests.get(url,headers=headers,timeout=10)
      rs.encoding=rs.apparent_encoding
      rs=rs.text
      txt=re.compile('query\((.*)').findall(rs)
      tmp=txt[0]
      if tmp.find('drawflag')>0:
         tmp=json.loads(tmp)['data']
         print('转盘bless:'+str(tmp['bless']))
      else:
         print('结束======')
       	 return 
   except Exception as e:
      msg=str(e)
      print(msg)


      
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
   print(m)
   global result
   result +=m+'\n'
def getid(st):
   for k in st.split(';'):
      if k.strip().find('pt_pin=')==0:
        nm=k[(k.find('pt_pin=')+7):len(k)]
        nm=urllib.parse.unquote(nm)
        return nm
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
   global headers,result
   global djj_djj_cookie
   check('DJJ_DJJ_COOKIE',cookiesList)
   j=0
   for count in cookiesList:
     j+=1
     #if j!=3:
        #continue
     headers['Cookie']=count
     result+='【count】'+getid(count)
     if(islogon(j,count)):
         JD_Geziyaya()
   print('任务执行结束........+')
if __name__ == '__main__':
       start()
