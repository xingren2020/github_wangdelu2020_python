import requests
import json
import time
import os
import re
import urllib
from datetime import datetime
from dateutil import tz
#by 红鲤鱼绿鲤鱼与驴 2020.11
mins = int(time.time())
date_stamp = (mins-57600) % 86400
print(datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
_datatime = datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y%m%d", )
start=datetime.now().minute%10
result=''
djj_bark_cookie=''
djj_sever_jiang=''
airplay_count_cookie=''
cookiesList=[]
def airplay_sign(ck):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1','Host':'glados.rocks','Cookie':ck}
    body={"token":"glados_network"}
    response = requests.post('https://glados.rocks/api/user/checkin',headers=headers,data=body)
    #print(response.text)
    obj=response.json()
    x=re.findall('\d+',obj['list'][0]['balance'])
    msg=f"""打卡成功✅{obj['message']}打卡时间:{obj['list'][0]['detail']}剩余{x[0]}天"""
    loger(msg)
    
def checkio():
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   global djj_bark_cookie
   global djj_sever_jiang
   if "DJJ_BARK_COOKIE" in os.environ:
     djj_bark_cookie = os.environ["DJJ_BARK_COOKIE"]

   if "DJJ_SEVER_JIANG" in os.environ:
      djj_sever_jiang = os.environ["DJJ_SEVER_JIANG"]
      
def checklocal():
   global airplay_count_cookie
   if "AIRPLAY_COUNT_COOKIE" in os.environ:
      airplay_count_cookie = os.environ["AIRPLAY_COUNT_COOKIE"]
      for line in airplay_count_cookie.split('\n'):
        if not line:
          continue 
        cookiesList.append(line.strip())
   elif airplay_count_cookie:
       for line in airplay_count_cookie.split('\n'):
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
    #print(response.text)
def loger(m):
   print(m)
   global result
   result +=m+'\n'
def start():
   checkio()
   checklocal()
   j=0
   for count in cookiesList:
     j+=1
     print(f'''>>>>>>>>>【账号{str(j)}开始】''')
     airplay_sign(count)
     time.sleep(2)
   pushmsg('鸡场',result)
def main_handler(event, context):
    return start()
if __name__ == '__main__':
       start()
