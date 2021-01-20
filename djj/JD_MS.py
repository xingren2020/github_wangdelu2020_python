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


encryptProjectId=''
cookiesList=[]
xfj_hdlist=[]


















JD_API_HOST = 'https://api.m.jd.com/client.action'
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
       else:
       	  signmd5=False
       	  msg=f'''【京东账号{checkck}】cookie已失效,请重新登录京东获取'''
          pushmsg('主库_更新数据',msg)
   except Exception as e:
      signmd5=False
      msg=str(e)
      print(msg)
      pushmsg('京东cookie',msg)
   return signmd5


def JD_miaosha():
     JD_getActInfo()
     if not encryptProjectId:
        print('no result,next===========')
        return 
     
     JD_getTaskList()
     JD_getUserInfo()
     time.sleep(10)
def JD_getActInfo():
   print('getActInfo\n')
   try:
      global encryptProjectId
      bd={}
      headers['Content-Type']='application/x-www-form-urlencoded'
      body=f'''functionId=assignmentList&body={urllib.parse.quote(json.dumps(bd))}&client=wh5&clientVersion=9.3.2&appid=jwsp'''
      rs= requests.post(JD_API_HOST,headers=headers,data=body,timeout=10).json()
      if (rs['code'] == 200):
         encryptProjectId = rs['result']['assignmentResult']['encryptProjectId']
         print('活动名称:'+rs['result']['assignmentResult']['projectName'])
         
   except Exception as e:
      msg=str(e)
      print(msg)
def JD_getUserInfo():
   print('getUserInfo\n')
   try:
      
      bd={}
      msg=''
      body=f'''functionId=homePageV2&body={urllib.parse.quote(json.dumps(bd))}&client=wh5&clientVersion=9.3.2&appid=SecKill2020'''
      headers['Content-Type']='application/x-www-form-urlencoded'
      rs= requests.post(JD_API_HOST,data=body,headers=headers,timeout=10).json()
      if (rs['code'] == 2041):
        score = rs['result']['assignment']['assignmentPoints']
        msg+='|当前秒秒币'+str(score)
      else:
         msg+='无秒币'
         print('无秒币')
      loger(msg)
   except Exception as e:
      msg=str(e)
      print(msg)
      
      
      
def JD_getTaskList():
   print('getTaskList\n')

   try:
      bd = {"encryptProjectId": encryptProjectId, "sourceCode": "wh5"}
      body=f'''functionId=queryInteractiveInfo&body={urllib.parse.quote(json.dumps(bd))}&client=wh5&clientVersion=9.3.2'''
      headers['Content-Type']='application/x-www-form-urlencoded'
      rs= requests.post(JD_API_HOST,headers=headers,data=body,timeout=10).text
      rs=rs.replace('false','False')
      rs=rs.replace('true','True')
      rs=eval(rs)
      bb=0
      if rs['code'] == '0':
        for so in rs['assignmentList']:
          if (so['completionCnt'] < so['assignmentTimesLimit']):
            print('【'+str(bb+1)+'】')
            if so['assignmentType'] == 1:
               for i in range(so['assignmentTimesLimit']-so['completionCnt']):
                 print('去做'+so['assignmentName']+'任务：'+str(i+1)+'/'+str(so['assignmentTimesLimit']))
                 body={"encryptAssignmentId": so['encryptAssignmentId'],"itemId": so['ext'][so['ext']['extraType']][i]['itemId'],"actionType": 1,"completionFlag": ""}
                 doTask(body)
                 time.sleep(so['ext']['waitDuration'] * 1 + 1)
                 body['actionType'] = 0
                 doTask(body)
                  
            elif so['assignmentType'] ==0:
              print(str(so['assignmentTimesLimit']-so['completionCnt']))
              for i in range(so['assignmentTimesLimit']-so['completionCnt']):
                 print('去做'+so['assignmentName']+'任务：'+str(i+1)+'/'+str(so['assignmentTimesLimit']))
                 body = {"encryptAssignmentId":so['encryptAssignmentId'],"itemId": "","actionType": "0","completionFlag": True}
                 doTask(body)
                 time.sleep(1)
            elif (so['assignmentType'] ==3):
              for i in range(so['assignmentTimesLimit']-so['completionCnt']):
                print('去做'+so['assignmentName']+'任务：'+str(i+1)+'/'+str(so['assignmentTimesLimit']))
                body = {"encryptAssignmentId": so['encryptAssignmentId'],"itemId": so['ext'][so['ext']['extraType']][i]['itemId'],"actionType": 0,"completionFlag": ""}
                doTask(body)
                time.sleep(1)
   except Exception as e:
      msg=str(e)
      print(msg)
      
    
      


def doTask(body):
   print('doTask\n')
   try:
      
      bd = {"encryptProjectId": encryptProjectId, "sourceCode": "wh5", "ext": {}}
      bd.update(body)
      body=f'''functionId=doInteractiveAssignment&body={urllib.parse.quote(json.dumps(bd))}&client=wh5&clientVersion=9.3.2&'''
      headers['Content-Type']='application/x-www-form-urlencoded'
      rs= requests.post(JD_API_HOST,headers=headers,data=body,timeout=10).text
      print(rs)
   except Exception as e:
      msg=str(e)
      print(msg)


    


      
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
   global result
   result +=m

def islogon(j,count):
    JD_islogn=False 
    for i in count.split(';'):
       if i.find('pin=')>=0:
          newstr=i[(i.find('pt_pin=')+7):len(i)]
          print(f'''【账号{str(j)}】''')
          msg=f'''【账号{str(j)}】{urllib.parse.unquote(newstr)}|'''
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
   global headers,result,xfj_hdlist,cookiesList
   check('DJJ_XFJ_NEWHEADERS',xfj_hdlist)
   check('DJJ_DJJ_COOKIE',cookiesList)
   j=0
   for count in cookiesList:
     j+=1
     headers=eval(xfj_hdlist[0])
     headers['Cookie']=count
     headers['Origin']='https://h5.m.jd.com'
     if(islogon(j,count)):
         JD_miaosha()
     result+='\n'
   pushmsg('JD_ms',result)
if __name__ == '__main__':
       start()
