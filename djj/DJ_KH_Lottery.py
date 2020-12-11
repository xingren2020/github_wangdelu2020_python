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

osenviron={}
header={}
sharecode=''
djj_bark_cookie=''
djj_sever_jiang=''
djj_sharecode=''



JD_API_HOST = 'https://api.m.jd.com/client.action'



Defalt_ShareCode=['P04z54XCjVUm4aW5m9cZzurqQcz_VTZgpY8fQ','P04z54XCjVUm4aW5m9cZxGxqCoc3VQ9q9wdfQ']

cookiesList=[]
result=''

def myhd(hd):
   hd=eval(hd)
   hd['Origin']='https://h5.m.jd.com'
   hd['Referer']='https://h5.m.jd.com/babelDiy/Zeus/2zwQnu4WHRNfqMSdv69UPgpZMnE2/index.html?babelChannel=ttt1&utm_campaign=&utm_source=&utm_term=&utm_medium='
   return hd
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
          pushmsg('京东',msg)
   except Exception as e:
      signmd5=False
      msg=str(e)
      print(msg)
      pushmsg('京东cookie',msg)
   return signmd5


def JD_healthyDay():
   try:
      print('\n  healthyDay')
      global sharecode
      body='functionId=healthyDay_getHomeData&body={"appId":"1EFRTxw","taskToken":""}&client=wh5&clientVersion=1.0.0'
      res=json.loads(iosrule(body))
      #print(res)
      if(not res['code']==0):
         print('request error')
         return 
      res=res['data']
      endTime=stamptm(res['result']['activityInfo']['endTime'])
      nowTime=stamptm(res['result']['activityInfo']['nowTime'])
      startTime=stamptm(res['result']['activityInfo']['startTime'])
      money=res['result']['userInfo']['userScore']
      status=res['result']['userInfo']['wholeTaskStatus']
      sharecode=res['result']['taskVos'][3]['assistTaskDetailVo']['taskToken']
      print(f'''活动信息:
      【startTime】{startTime}
      【endTime】  {endTime}
      【money】    {money}
      【sharecode】{sharecode}
      ''')
      if(int(money)>500):
        for i in range(int(int(money)/500)):
         Lottery(i+1)
         time.sleep(5)
      for item in res['result']['taskVos']:
        print(f'''开始任务:{item['taskName']}--{item['subTitleName']}''')
        taskId=item['taskId']
        if 'followShopVo' in item.keys():
          print('\n  followShopVo')
          i=0
          for item_ in item['followShopVo']:
           i+=1
           taskToken=item_['taskToken']
           shopName=f'''任务【{len(item['followShopVo'])}---{i}】-{item_['shopName']}'''
           if(item_['status']==2):
              print(shopName+'==已经完成....')
              continue
           dotask(taskToken,taskId,shopName,'1')
           time.sleep(6)
           dotask(taskToken,taskId,shopName,'0')
        if 'shoppingActivityVos' in item.keys():
          print('\n  shoppingActivityVos')
          i=0
          for item_ in item['shoppingActivityVos']:
           i+=1
           taskToken=item_['taskToken']
           shopName=f'''任务【{len(item['shoppingActivityVos'])}---{i}】-{item_['title']}'''
           if(item_['status']==2):
              print(shopName+'==已经完成....')
              continue
           dotask(taskToken,taskId,shopName,'1')
           time.sleep(6)
           dotask(taskToken,taskId,shopName,'0')
        if 'productInfoVos' in item.keys():
          print('\n  productInfoVos')
          i=0
          for item_ in item['productInfoVos']:
           i+=1
           taskToken=item_['taskToken']
           shopName=f'''任务【{len(item['productInfoVos'])}---{i}】-{item_['skuName']}'''
           if(item_['status']==2):
              print(shopName+'==已经完成....')
              continue
           dotask(taskToken,taskId,shopName,'1')
           time.sleep(6)
           dotask(taskToken,taskId,shopName,'0')
        if 'assistTaskDetailVo' in item.keys():
          print('\n  assistTaskDetailVo')
          sharecode=item['assistTaskDetailVo']['taskToken']
          shopName=f'''任务【{item['taskName']},{item['subTitleName']}'''
          if(item['status']==2):
             print(shopName+'==已经完成....')
          else:
              doHelp()
          
   except Exception as e:
      msg=str(e)
      print(msg)

def dotask(taskToken,taskId,shopName,actionType):
   try:
      print('\n'+shopName)
      body='functionId=harmony_collectScore&body={"appId":"1EFRTxw","taskToken":"'+taskToken+'","taskId":'+str(taskId)+',"actionType":'+actionType+'}&client=wh5&clientVersion=1.0.0'
      #print(body)
      res=json.loads(iosrule(body))
      print(res)
      print(res['data']['bizMsg'])
   except Exception as e:
      msg=str(e)
      print(msg)
      
      
def Lottery(i):
   try:
      print(f'''\nLottery【{i}】''')
      body='functionId=interact_template_getLotteryResult&body={"appId":"1EFRTxw"}&client=wh5&clientVersion=1.0.0'
      #print(body)
      res=json.loads(iosrule(body))
      #print(res)
      res=res['data']
      print(f'''抽奖{res['result']['haveLotteryNum']}次,奖品{res['result']['userAwardsCacheDto']['jBeanAwardVo']['prizeName']},剩余{res['result']['userScore']}金币''')
   except Exception as e:
      msg=str(e)
      print(msg)

def doHelp():
   try:
      newShareCodes=shareCodesFormat()
      index=0
      for code in newShareCodes:
          index+=1
          print(f'''【{index}】,开始助力京东账号{code}''')
          if (not code):
    	        continue
          if (code ==sharecode):
             print(f'''\n跳过自己的{code} \n''')
             continue
          print(f'''\n开始助力好友: ''')
          helpResult= json.loads(helpShare(code))
          if (helpResult and helpResult['code'] ==0):
             print(f'''助力朋友:{helpResult['data']['bizMsg']}''')
   except Exception as e:
       print(str(e))
def helpShare(code):
   print('助力请求::::::::::')
   try:
      body='functionId=harmony_collectScore&body={"appId":"1EFRTxw","taskToken":"'+code+'","taskId":6,"actionType":0}&client=wh5&clientVersion=1.0.0'
      data=iosrule(body)
      #print(data)
      return data
   except Exception as e:
    	print(str(e))
def readShareCode():
   print('\n  readShareCode')
   url='http://api.turinglabs.net/api/v1/jd/jdapple/read/20/'
   try:
      readShareCodeRes=requests.get(url).json()
      #print(readShareCodeRes)
      return readShareCodeRes
   except Exception as e:
    	pass

def shareCodesFormat():
   newShareCodes = []
  # print(ShareCode)
   #ShareCode=''
   print('开始读取默认助力码')
   readShareCodeRes = readShareCode()
   #print(readShareCodeRes)
   if (readShareCodeRes and readShareCodeRes['code'] == 200):
        #print(readShareCodeRes['data']['value'])
        newShareCodes.append(readShareCodeRes['data']['value'])
        newShareCodes=Defalt_ShareCode+newShareCodes
        print('添加完毕:',newShareCodes)
   else:
        newShareCodes=Defalt_ShareCode
   print(f'''京东账号将要助力的好友{newShareCodes}''')
   return newShareCodes

def submitShareCode():
   print('\n提交验证码')
   try:
      url=f'''https://api.ninesix.cc/api/jx-cfd/{info['strMyShareId']}/{jd_name}'''
      response=requests.post(url).json()
      #print(response)
      if(response['data']['value']):
      	print('邀请码提交成功')
   except Exception as e:
    	print(str(e))



    
def iosrule(body={}):
   url=JD_API_HOST
   try:
     response=requests.post(url,headers=header,data=body).text
     return response
   except Exception as e:
      print(f'''初始化任务:''', str(e))
      
def tmstamp(tr):
   tm = dateutil.parser.parse(tr).timestamp()
   return tm

def stamptm(tm,frm='%Y-%m-%d %H:%M:%S'):
   #frm=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
   tr = datetime.fromtimestamp(tm/1000).strftime(frm)
   return tr


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
   xfj_hdlist=[]
   global header
   global djj_djj_cookie
   check('DJJ_XFJ_HEADERS',xfj_hdlist)
   check('DJJ_DJJ_COOKIE',cookiesList)
   j=0
   for count in cookiesList:
     j+=1
     header=myhd(xfj_hdlist[0])
     header['Cookie']=count
     if(islogon(j,count)):
         JD_healthyDay()

if __name__ == '__main__':
       start()
