import requests
import json
import time
import os
import re
import urllib
from datetime import datetime
from dateutil import tz


print(datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
_datatime = datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y%m%d", )
result=''
djj_bark_cookie=''
djj_sever_jiang=''
wetcard_tian_cookie = ''
wetcard_tianlist=[]
wetcard_wei_cookie = ''
wetcard_weilist=[]


def wetcard_sign(j,ck):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.14(0x17000e2e) NetType/4G Language/zh_CN'}

    response = requests.get(ck,headers=headers)
    #print(response.text)
    obj=response.json()
    msg='[账号'+str(j)+']'
    if obj['status']==1:
       msg+='打卡成功✅'
    elif obj['status']==2:
       msg+='打卡上限✅✅'
    loger(msg)
    
def wetcard_cash(j,ck):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.14(0x17000e2e) NetType/4G Language/zh_CN'}
    cck = ck.replace('action=sign&contr=clock','action=cash&contr=my')
    response = requests.get(cck,headers=headers)
    #print(response.text)
    obj=response.json()
    
    if obj['status']==1:
       if obj['info']['least_money']=='':
          sb='0'
       else:
          sb=obj['info']['least_money']
       msg=f"""{obj['info']['member']['nickname']}"""+',最低提现额度:'+sb+'.现金:'+f"""{obj['info']['member']['money']}"""
       loger(msg)
       wetcard_withdraw(sb,ck)
       
    elif obj['status']==2:
       msg=f"""{obj['info']}"""
       loger(msg)
       
def wetcard_withdraw(ca,ck):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.14(0x17000e2e) NetType/4G Language/zh_CN'}
    cck = ck.replace('action=sign&contr=clock','action=withdrawals&contr=my')+'&money='+ca+'&payment_code='
    response = requests.get(cck,headers=headers)
    #print(response.text)
    obj=response.json()
    if obj['status']==1:
      msg='提现成功✅'
    else:
      msg=f"""{obj['info']}\n"""
    loger(msg)
    
    
def check(st,flag,list,tt):
   result=''
   if "DJJ_BARK_COOKIE" in os.environ:
     djj_bark_cookie = os.environ["DJJ_BARK_COOKIE"]
   if "DJJ_SEVER_JIANG" in os.environ:
      djj_sever_jiang = os.environ["DJJ_SEVER_JIANG"]
   if flag in os.environ:
      st = os.environ[flag]
   if st:
       for line in st.split('\n'):
         if not line:
            continue 
         list.append(line.strip())
   else:
       print('DTask is over.')
       return 
   j=0
   for count in list:
      j+=1
      print(f'''>>>>>>>>>【账号{str(j)}开始】''')
      if count:
         wetcard_sign(j,count)
         wetcard_cash(j,count)
   pushmsg(tt,result)
     
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
   print(m)
   global result
   result +=m
   




print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))

check(wetcard_tian_cookie,'WETCARD_TIAN_COOKIE',wetcard_tianlist,'tiancard')
check(wetcard_wei_cookie,'WETCARD_WEI_COOKIE',wetcard_weilist,'weicard')
