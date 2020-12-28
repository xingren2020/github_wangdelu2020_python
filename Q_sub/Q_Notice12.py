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
djj_bark_cookie=''
djj_sever_jiang=''
osenviron={}
msg=''
hd=''
urllist=[]
hdlist=[]
btlist=[]
pn=1
bx=0
bxfb=0
bxn=0
bxfbn=0
nome=False


def Av(i,hd,k,key=''):
   print(str(k)+'=🔔='*k)
   try:
     if(k==5):
         response = requests.post(f'''{i}{key}''',headers=hd,data={},timeout=10)
     else:
         response = requests.get(f'''{i}{key}''',headers=hd,timeout=10)

     userRes=json.loads(response.text)
     hand(userRes,k)
   except Exception as e:
      print(str(e))

def watch(flag,list):
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
def hand(userRes,k):
   msg=''
   global bx,bxfb,bxn,bxfbn,pn,nome
   tm=''
   
   try:
     if(userRes['code']==0):
       if(k==1):
           msg+=f'''{userRes['data']['user']['nickName'][0:2]}'''
           print(msg)
       elif(k==2):
            msg+=f'''|{userRes['data']['treasureBox']['count']}'''
       
       
       elif(k==3):
         tm=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d", )
         
         
         for tdata in userRes['data']['list']:
           if tdata['content'][0:10]==tm:
              if tdata['type']==240:
                bx+=tdata['amount']
                bxn+=1
          
         
              elif tdata['type']==250:
                bxfb+=tdata['amount']
                bxfbn+=1
              
              
           else:
               nome=True
               msg+='|'+str(bxn)+'-'+str(bx)+'|'+str(bxfbn)+'-'+str(bxfb)+'|'
               break
         
         if (not nome):
            pn+=1
            Av(urllist[2]+str(pn),hd,3)
        
         
         
         
         
         print(msg)
       elif(k==4):
         msg+=f'''|{userRes['data']['amount']/10000}|{userRes['data']['expiringAmount']}|{userRes['data']['expiringDate']}|'''
         if userRes['data']['amount']>100000:
            Av(urllist[k],hd,(k+1))
         ttm=0
         for wdata in userRes['data']['withdrawList']:
            ttm+=abs(wdata['amount'])/10000
         msg+=str(ttm)+'|'
       elif(k==5):
         print(userRes['msg'])
       loger(msg)
   except Exception as e:
      print(str(e))
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
    #print(response.text)
def loger(m):
   #print(m)
   global result
   result +=m     
def getid(id):
   lll=id.split(';')
   for l in lll:
     if l.find('ywguid=')>=0:
      return l[(l.find('ywguid=')+7):len(l)]
   
      
    
def notice(b,e):
    ll=False
    start_time = datetime.strptime(str(datetime.now().date())+b, '%Y-%m-%d%H:%M')
    end_time =  datetime.strptime(str(datetime.now().date())+e, '%Y-%m-%d%H:%M')
    now_time = datetime.now()
    if now_time > start_time and now_time<end_time:
       ll=True
    else:
    	ll=False
    return ll
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
   global result,hd
   global bx,bxfb,bxn,bxfbn,pn,nome
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   watch('ios_wturl',urllist)
   watch('ios_newhd',hdlist)
   watch('ios_newbt',btlist)
   for j in range(2):
       bx=0
       bxfb=0
       bxn=0
       bxfbn=0
       pn=1
       nome=False
       print(f'''===={str(j+1)}({len(btlist)})''')
       result+='['+str(len(btlist))+'-'+str(j+1)+']'
       hd=eval(hdlist[0])
       hd['Cookie']=btlist[j]
       for k in range(len(urllist)-1):
         Av(urllist[k],hd,(k+1))
       result+=getid(btlist[j])+'\n'
       print('🏆🏆🏆🏆运行完毕')
   pushmsg('公众号iosrule',result)
     
     
    
   
     
if __name__ == '__main__':
       start()
    
