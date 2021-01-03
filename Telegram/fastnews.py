import requests
import json
import time
import timeit
import os
import re
import urllib
from datetime import datetime
from dateutil import tz


djj_tele_group=''
osenviron={}
result=''




headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1'}



def getzhuti():
   msg1='【2-1新干快线公众号iosrule】'
   msg2='【2-2新干快线公众号iosrule】'
   try:
      response=requests.get('http://www.788511.com/forum-43-1.html',headers=headers,timeout=10)
      #print(response.text)
      st=response.text
      pt1=re.compile('<title>(.*)</title>')
      tt=pt1.findall(st)
     #print(tt)
      msg1+=tt[0]+'\n'
      msg2+=tt[0]+'\n'
      pt0=re.compile('<span>(.*)</span><span class=')
      tm=pt0.findall(st)
      
      pt1=re.compile('class="">\n(.*)<span class')
      tt=pt1.findall(st)
      pt2=re.compile('class="text">([\s\S]*?)</dl>')
      ct=pt2.findall(st)
      adurl=re.compile('<div class="threaditem">([\s\S]*?)<h3 class="">').findall(st)
      #print('填空',adurl)
      index=0
      for zt in tt:
        index+=1
        if index<7:
          msg1+=str(index)+'.'+zt.strip()
          msg1+='>>'+tm[index-1]+'\n'
          msg1+=('--'+ct[index-1].strip()).replace('\n','')+'\n'
          cttemp=re.compile('<a href=(.*)class="c"').findall(adurl[index-1])[0].strip()
          cttemp=eval(cttemp)
          msg1+=cttemp+'\n'
        if index>=7:
          msg2+=str(index)+'.'+zt.strip()
          msg2+='>>'+tm[index-1]+'\n'
          msg2+=('--'+ct[index-1].strip()).replace('\n','')+'\n'
          cttemp=re.compile('<a href=(.*)class="c"').findall(adurl[index-1])[0].strip()
          cttemp=eval(cttemp)
          msg2+=cttemp+'\n'
      
   except Exception as e:
      msg=str(e)
      print(msg)
   #loger(msg1)
   pushmsg('news',msg1)
   #loger(msg2)
   pushmsg('news',msg2)

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
    

def telegroup():
   global djj_tele_group

   if "DJJ_TELE_GROUP" in os.environ:
      djj_tele_group = os.environ["DJJ_TELE_GROUP"]
   if "DJJ_TELE_GROUP" in osenviron:
      djj_tele_group = osenviron["DJJ_TELE_GROUP"]
   if not djj_tele_group:
       print(f'''【通知参数】 is empty,DTask is over.''')
       exit()
def all():
   telegroup()
   getzhuti()
   print('its over')





def pushmsg(title,txt):
   txt=urllib.parse.quote(txt)
   title=urllib.parse.quote(title)
   print("\n【Telegram消息】")
   id=djj_tele_group[djj_tele_group.find('@')+1:len(djj_tele_group)]
   botid=djj_tele_group[0:djj_tele_group.find('@')]

   turl=f'''https://api.telegram.org/bot{botid}/sendMessage?chat_id={id}&text={title}\n{txt}'''

   response = requests.get(turl)
    
    
def loger(m):
   #print(m)
   global result
   result =m
   
@clock
def start():
   
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   all()


if __name__ == '__main__':
       start()
