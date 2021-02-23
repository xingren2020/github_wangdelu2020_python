import requests
import os
import re
import json
import time
import random
import timeit
import urllib
from datetime import datetime
from dateutil import tz


result=''
osenviron={}
hd={}
body1={}
body2={}
body3={}
body4={}
urllist=[]
hdlist=[]
bdlist=[]
alllist=[]
liveIdList=[]
tkbdlist=[]
tklist=[]
actId1=''
actId2=''
actId3=''
acount=2

def Av(i,hd,k,key=''):
   try:
      print(str(k)+'go===='+i)
      userRes=''
      if k>1 and k<13 or k==15 or k==16:
        
        response = requests.get(i,headers=hd,timeout=10)
        userRes=json.loads(response.text)
      if k==1 or k==13 or k==14 or k==17:
         
  
         response = requests.post(i,headers=hd,data=key,timeout=10)
     
         userRes=json.loads(response.text)
     # print(userRes)
      hand(userRes,k)
   except Exception as e:
      print(str(e))


def hand(userRes,k):
   global actId1,liveIdList,actId2,actId3,hd
   msg=''
   try:
     
    if k==1:
      #print(userRes)
      
      if(userRes['resultCode']==1):
        hd['token']=userRes['data']['accessToken']
    if k==11:
          for data in userRes['data']['everyDayActivityList']:
           if data['actName'].find('直播')>0:
              actId2=data['actId']
           elif data['actName'].find('视频')>0:
             	actId1=data['actId']
           elif data['actName'].find('红包')>0:
             	actId3=data['actId']
    if k==12:
       if userRes['resultCode']==1:
          liveIdList= userRes['data']['liveIdList']
          #print(liveIdList)
          
    if k==13:
       if userRes['resultCode']== 1:
         print(str(userRes['data']['goldCoinNumber']))
         
       else:
          print(userRes['errorCode']+userRes['errorDesc'])
       time.sleep(random.randint(15,30))
    if k==14:
      if userRes['resultCode']== 1:
         print(str(userRes['data']['goldCoinAmt']))
         time.sleep(random.randint(15,30))
      else:
          print(userRes['errorCode']+userRes['errorDesc'])
          
    
      
     
     
    
    if(k==15):
       if userRes['resultCode']== 1:
         msg=userRes['data']['customerInfo']['nickname'][0:2]+'|'
         loger(msg)
       else:
          print(userRes['errorCode']+userRes['errorDesc'])
         
    if(k==16):
      if userRes['resultCode']== 1:
        msg=str(userRes['data']['balanceSum']/100)+'|'+str(userRes['data']['coinSum'])
        loger(msg)
        if userRes['data']['coinSum']/10000>15:
          body4['amount']=1500
          print(body4)
          Av(urllist[k],hd,(k+1),json.dumps(body4))
      else:
          print(userRes['errorCode']+userRes['errorDesc'])
    if(k==17):
          print('wtok(1/2):::::'+str(userRes['data']['withdrawRes']))
       
   except Exception as e:
      #print(str(e))
      pass
      

def watch(flag,list):
   vip=''
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
    
  
def tm13():
   Localtime=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f", )
   timeArray = datetime.strptime(Localtime, "%Y-%m-%d %H:%M:%S.%f")
   timeStamp = int(time.mktime(timeArray.timetuple())*1000+timeArray.microsecond/1000)
   return timeStamp   
  


def allinone(i):
   global alllist
   try:
     response = requests.get(i,timeout=10)
     response.raise_for_status()
     response.close()
     userRes=json.loads(response.text)
     if userRes['resultCode']==1:
      for l in userRes['data']['records']:
        alllist.append(l['videoPublishId'])
   except Exception as e:
      print(str(e))
      



def allinbd(alllist,liveId):
      global body1,body2,body3,body4
      
      body1=json.loads(body1)
      body2=json.loads(body2)
      body3=json.loads(body3)
      tf=[1,1,2]
      body1['videoList'][0]['videoId']=random.choice(alllist)
      body1['videoList'][0]['type']=random.choice(tf)
      body1['videoList'][1]['videoId']=random.choice(alllist)
      body1['videoList'][1]['type']=body1['videoList'][0]['type']
      body1['actId']=str(actId1)
      
     # body2['liveId']=random.choice(liveIdList)
      body2['liveId']=liveId
      body2['actId']=str(actId2)
      body3['actId']=str(actId3)
      body1=json.dumps(body1)
      body2=json.dumps(body2)
      
      body3=json.dumps(body3,separators=(':',':'))
      #print(body3)
      print(str(actId1),str(actId2),str(actId3))
   
def pushmsg(title,txt,bflag=1,wflag=1,tflag=1):
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
      print(response.text)





def loger(m):
   global result
   #print(result)
   result +=m
@clock
def start():
   global result,hd,body1,body2,body3,body4,alllist,hdlist,urllist,tkbdlist,tklist
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   try:
      watch('xb_main_url',urllist)
      watch('xb_main_hd',hdlist)
      watch('xb_main_bd',bdlist)
      watch('xb_tk_bd',tkbdlist)
      watch('xb_tk',tklist)
      allcode=[]
      
       
      for i in range(1,10):
        allcode.append(urllist[i])
      allinone(random.choice(allcode))
      
      for ac in range(accont):
        result=''
        for k in range(0,len(tklist)):
          body1=bdlist[0]
          body2=bdlist[1]
          body3=bdlist[2]
          body4=bdlist[3]

          hd=eval(hdlist[0])
          
          hd['token']=tklist[k].split('@')[0]
          st=tklist[k].split('@')[1]
          hd['traceid']=st.replace(st[20:33],str(tm13()))
          print(str(ac+1)+'_loop__【C】'+str(k+1))
          Av(urllist[0],hd,(1),tkbdlist[k])
          #Av(urllist[14],hd,(15),body3)
         
          Av(urllist[10],hd,(11))
          Av(urllist[11],hd,(12))
          Av(urllist[12],hd,(13),body1)
          if len(alllist)>10:
             for ii in range(len(liveIdList)):
                 print(str(ii+1)+'=go='+str(len(liveIdList)))
                 allinbd(alllist,liveIdList[ii])
                 Av(urllist[13],hd,(14),body2)
                 time.sleep(random.randint(15,30))
          
          
          
          
          if ac!=acount-1:
              del hd['signature']
              del hd['User-Agent']
              del hd["X-User-Agent"]
              del hd['random']
          
          if ac==acount-1:
              print('acount')
              Av(urllist[14],hd,(15))
              Av(urllist[15],hd,(16))
      
              time.sleep(1)
              result+='\n'
      

        print('<<<<<<<'+str(ac+1)+'>>>>>>>>>')
      #print(result)
      pushmsg('主库',result)
      print('🏆🏆🏆🏆运行完毕')
   except Exception as e:
      print(str(e))
   print('🏆🏆🏆🏆运行完毕')
    
    
   
     
if __name__ == '__main__':
       start()
    
