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
''''微信小程序入口：
来客有礼 - > 首页 -> 东东小窝
网页入口（注：进入后不能再此刷新，否则会有问题，需重新输入此链接进入）
https://h5.m.jd.com/babelDiy/Zeus/2HFSytEAN99VPmMGZ6V4EYWus1x/index.html'''



djj_bark_cookie=''
djj_sever_jiang=''
djj_small_headers=''
Defalt_ShareCode=[]






    
    
    
    
cookiesList=[]
result=''
mypin=''
mytoken=''
mywoB=''
numm=0
createAssistUserID=''
isPurchaseShops=True

def JD_homesmall():
   ssjj_rooms()
   queryByUserId()
   getTaskList()
   createInviteUser()
   queryDraw()
   queryByUserId()
   queryFurnituresCenterList()
   helpFriends()
def ssjj_rooms():
   print('\n ssjj-rooms')
   try:
      url='https://lkyl.dianpusoft.cn/api/ssjj-rooms/info/%E5%AE%A2%E5%8E%85?body=%7B%7D'
      data=json.loads(requests.get(url,headers=headers).text)
      #print(data)
   except Exception as e:
      msg=str(e)
      print(msg)

def queryByUserId():
   print('\n queryByUserId')
   try:
      global mywoB
      url='https://lkyl.dianpusoft.cn/api/ssjj-wo-home-info/queryByUserId/2?body=%7B%7D'
      data=json.loads(requests.get(url,headers=headers).text)
      #print(data)
      msg=f'''{data['body']['name']}|{data['body']['name']}|{data['body']['woB']}|{data['body']['nick']}|{data['body']['userId']}'''
      mywoB=data['body']['woB']
      loger(msg)
   except Exception as e:
      msg=str(e)
      print(msg)

def createInviteUser():
   print('\n createInviteUser')
   if numm>len(cookiesList)+1:
         print('收集助力id完毕✌🏻️✌🏻️✌🏻️✌🏻️....') 
         return 
   global Defalt_ShareCode
   try:
      url='https://lkyl.dianpusoft.cn/api/ssjj-task-record/createInviteUser?body=%7B%7D'
      data=json.loads(requests.get(url,headers=headers).text)
      #print(data)
      msg=data['body']['id']
      print('Sharecode='+str(msg))
      Defalt_ShareCode.append(msg)
      print(Defalt_ShareCode)
   except Exception as e:
      msg=str(e)
      print(msg)
      
def createAssistUser(inviteId, taskId):
   print('\n createAssistUser')
   global Defalt_ShareCode
   if numm<=len(cookiesList):
         print('收集助力id中....')
         return 
   try:
      url='https://lkyl.dianpusoft.cn/api/ssjj-task-record/createAssistUser/'+inviteId+'/'+taskId+'?body=%7B%7D'
      data=json.loads(requests.get(url,headers=headers).text)
      print(data)
    
   except Exception as e:
      msg=str(e)
      print(msg)
      
      
def helpFriends():
   try:
      if numm<=len(cookiesList):
         print('收集助力id中....')
         return 
      print('\n helpFriends')
      print(Defalt_ShareCode)
      for id in Defalt_ShareCode:
        createAssistUser(id, createAssistUserID)

   except Exception as e:
      msg=str(e)
      print(msg)
      




def getTaskList():
   try:
     global createAssistUserID
     print('💎getTaskList')
     url='https://lkyl.dianpusoft.cn/api/ssjj-task-info/queryAllTaskInfo/2'
     m=''
     data=json.loads(requests.get(url,headers=headers).text)
     tasklist=data['body']
     for item in tasklist:
       if not item['ssjjTaskInfo']['type']==1 and not item['ssjjTaskInfo']['type']==2:
         m=item['ssjjTaskInfo']['awardOfDayNum']
       else:
         m=1
       print(f'''{item['ssjjTaskInfo']['name']}----{item['doneNum']}/{m}---{item['ssjjTaskInfo']['type']}''')
     for item in tasklist:
       if (item['ssjjTaskInfo']['type'] == 1):
         createAssistUserID = item['ssjjTaskInfo']['id']
         
         print(f'''createAssistUserID:{item['ssjjTaskInfo']['id']}''')
         print(f'''\n\n助力您的好友:{item['doneNum']}人''')
       if (item['ssjjTaskInfo']['type'] ==2):
         
         if (item['doneNum'] ==1):
            print(f'''{item['ssjjTaskInfo']['name']}已完成[{item['doneNum']}/1]''')
            continue
         print(item['ssjjTaskInfo']['id'])
         signclock(item['ssjjTaskInfo']['id'])

       if (item['ssjjTaskInfo']['type'] ==3):
        if (item['doneNum'] ==item['ssjjTaskInfo']['awardOfDayNum']):
           print(f'''{item['ssjjTaskInfo']['name']}已完成[{item['doneNum']}/{item['ssjjTaskInfo']['awardOfDayNum']}]''')
           continue
          
        for ii in range(item['ssjjTaskInfo']['awardOfDayNum']):
           game(item['ssjjTaskInfo']['id'], item['doneNum'],ii)

       if (item['ssjjTaskInfo']['type'] == 4):
      #关注店铺
         if (item['doneNum'] ==item['ssjjTaskInfo']['awardOfDayNum']):
           print(f'''{item['ssjjTaskInfo']['name']}已完成[{item['doneNum']}/{item['ssjjTaskInfo']['awardOfDayNum']}]''')
           continue
         for ii in range(item['ssjjTaskInfo']['awardOfDayNum']):
           followShops('followShops', item['ssjjTaskInfo']['id'])#一键关注店铺
           queryDoneTaskRecord(item['ssjjTaskInfo']['id'], item['ssjjTaskInfo']['type'])
     
   
       if (item['ssjjTaskInfo']['type'] == 5):
      #浏览店铺
         if (item['doneNum'] ==item['ssjjTaskInfo']['awardOfDayNum']):
           print(f'''{item['ssjjTaskInfo']['name']}已完成[{item['doneNum']}/{item['ssjjTaskInfo']['awardOfDayNum']}]''')
           continue
         for ii in range(item['ssjjTaskInfo']['awardOfDayNum']):
           browseChannels('browseShops', item['ssjjTaskInfo']['id'], item['browseId'])
     
   
       if (item['ssjjTaskInfo']['type'] == 6):
      #关注4个频道
         if (item['doneNum'] ==item['ssjjTaskInfo']['awardOfDayNum']):
            print(f'''{item['ssjjTaskInfo']['name']}已完成[{item['doneNum']}/{item['ssjjTaskInfo']['awardOfDayNum']}]''')
            continue
         doChannelsListTask(item['ssjjTaskInfo']['id'], item['ssjjTaskInfo']['type'])
        
        
       if (item['ssjjTaskInfo']['type'] == 7):
     #浏览3个频道
         if (item['doneNum'] ==item['ssjjTaskInfo']['awardOfDayNum']):
           print(f'''{item['ssjjTaskInfo']['name']}已完成[{item['doneNum']}/{item['ssjjTaskInfo']['awardOfDayNum']}]''')
           continue
         for ii in range(item['ssjjTaskInfo']['awardOfDayNum']):
           browseChannels('browseChannels', item['ssjjTaskInfo']['id'], item['browseId'])
       if (isPurchaseShops and item['ssjjTaskInfo']['type'] == 9):
      #加购商品
          if (item['doneNum'] ==item['ssjjTaskInfo']['awardOfDayNum']):
             print(f'''{item['ssjjTaskInfo']['name']}已完成[{item['doneNum']}/{item['ssjjTaskInfo']['awardOfDayNum']}]''')
             continue
          for ii in range(item['ssjjTaskInfo']['awardOfDayNum']):
            followShops('purchaseCommodities', item['ssjjTaskInfo']['id'])#一键加购商品
            queryDoneTaskRecord(item['ssjjTaskInfo']['id'], item['ssjjTaskInfo']['type'])
     
    
       if (item['ssjjTaskInfo']['type'] ==10):
      #浏览商品
          if (item['doneNum'] ==item['ssjjTaskInfo']['awardOfDayNum']):
             print(f'''{item['ssjjTaskInfo']['name']}已完成[{item['doneNum']}/{item['ssjjTaskInfo']['awardOfDayNum']}]''')
             continue
          for ii in range(item['ssjjTaskInfo']['awardOfDayNum']):
           browseChannels('browseCommodities', item['ssjjTaskInfo']['id'], item['browseId']);
  
       if (item['ssjjTaskInfo']['type'] == 11):
      #浏览会场
          if (item['doneNum'] ==item['ssjjTaskInfo']['awardOfDayNum']):
              print(f'''{item['ssjjTaskInfo']['name']}已完成[{item['doneNum']}/{item['ssjjTaskInfo']['awardOfDayNum']}]''')
              continue
          for ii in range(item['ssjjTaskInfo']['awardOfDayNum']):
              browseChannels('browseMeetings',item['ssjjTaskInfo']['id'], item['browseId'])
      
      

          
          
          
   except Exception as e:
      msg=str(e)
      print(msg)
      
      
      
      
      
      
      
      
def signclock(taskId):
   try:
     print('💎signclock')
     url='https://lkyl.dianpusoft.cn/api/ssjj-task-record/clock/'+taskId+'?body=%7B%7D'
     data=json.loads(requests.get(url,headers=headers).text)
     print(data)
   
   except Exception as e:
      msg=str(e)
      print(msg)
def game(taskId,index,k):
   try:
     print('💎game======'+str(k))
     url='https://lkyl.dianpusoft.cn/api/ssjj-task-record/game/'+str(index)+'/'+taskId+'?body=%7B%7D'
     data=json.loads(requests.get(url,headers=headers).text)
     print(data)
   
   except Exception as e:
      msg=str(e)
      print(msg)
def followShops(functionID,taskId):
   try:
     print('💎followShops======')
     url='https://lkyl.dianpusoft.cn/api/ssjj-task-record/'+functionID+'/'+taskId+'?body=%7B%7D'
     data=json.loads(requests.get(url,headers=headers).text)
     print(data)
   
   except Exception as e:
      msg=str(e)
      print(msg)
def queryDoneTaskRecord(taskId, taskType):
   try:
     print('💎queryDoneTaskRecord======')
     url='https://lkyl.dianpusoft.cn/api/ssjj-task-record/queryDoneTaskRecord/'+str(taskType)+'/'+taskId+'?body=%7B%7D'
     data=json.loads(requests.get(url,headers=headers).text)
     print(data['head']['msg'])
   except Exception as e:
      msg=str(e)
      print(msg)
      
      
      
def browseChannels(functionID,taskId, browseId):
   try:
     print('💎browseChannels======')
     url='https://lkyl.dianpusoft.cn/api/ssjj-task-record/'+functionID+'/'+taskId+'/'+str(browseId)+'?body=%7B%7D'
     data=json.loads(requests.get(url,headers=headers).text)
     print(data)
   except Exception as e:
      msg=str(e)
      print(msg)
def doChannelsListTask(taskId,taskType):
   try:
     print('💎doChannelsListTask======')
     url='https://lkyl.dianpusoft.cn/api/ssjj-task-channels/queryChannelsList/'+taskId+'?body=%7B%7D'
     data=json.loads(requests.get(url,headers=headers).text)['body']
     for item in data:
          time.sleep(1)
          followChannel(taskId, item['id'])
          queryDoneTaskRecord(taskId, taskType)
   except Exception as e:
      msg=str(e)
      print(msg)
def followChannel(taskId, channelId):
   try:
     print('💎followChannel======')
     url='https://lkyl.dianpusoft.cn/api/ssjj-task-record/followChannel/'+channelId+'/'+taskId+'?body=%7B%7D'
     data=json.loads(requests.get(url,headers=headers).text)
     print(data)
   except Exception as e:
      msg=str(e)
      print(msg)

def queryDraw():
   try:
     print('💎queryDraw======')
     url='https://lkyl.dianpusoft.cn/api/ssjj-draw-center/queryDraw?body=%7B%7D'
     data=json.loads(requests.get(url,headers=headers).text)
     print(data['head']['msg'])
     freeDrawCount = data['body']['freeDrawCount']
     lotteryId = data['body']['center']['id']
     if(freeDrawCount>0):
        drawRecord(lotteryId)
     else:
        print('抽奖次数用完......')
   except Exception as e:
      msg=str(e)
      print(msg)
def drawRecord(Id):
   try:
     print('💎drawRecord======')
     url='https://lkyl.dianpusoft.cn/api/ssjj-draw-record/draw/'+Id+'?body=%7B%7D'
     data=json.loads(requests.get(url,headers=headers).text)
     print(data['head']['msg'])
   except Exception as e:
      msg=str(e)
      print(msg)
   
   
def queryFurnituresCenterList():
   try:
     print('💎queryFurnituresCenterList======')
     url='https://lkyl.dianpusoft.cn/api/ssjj-furnitures-center/queryFurnituresCenterList?body=%7B%7D'
     data=json.loads(requests.get(url,headers=headers).text)
     print(data['head']['msg'])
     #print(data['body'])
     canBuyList = []
     l={}
     for item in data['body']['list']:
       l.update({'id':item['id'],'needWoB':item['needWoB'],'jdBeanNum':item['jdBeanNum']})
       canBuyList.append(l)
     print(canBuyList)
     for item in canBuyList:
       if(item['needWoB']<=mywoB):
         furnituresCenterPurchase(item['id'],item['jdBeanNum'])
        
   except Exception as e:
      msg=str(e)
      print(msg)
   
def furnituresCenterPurchase(id,bnum):
   try:
     print('💎furnituresCenterPurchase======')
     url='https://lkyl.dianpusoft.cn/api/ssjj-furnitures-center/furnituresCenterPurchase/'+id++'body=%7B%7D'
     data=json.loads(requests.get(url,headers=headers).text)
     print(data['head']['msg'])
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





def check():
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   global djj_small_headers
   global djj_bark_cookie
   global djj_sever_jiang
   if "DJJ_BARK_COOKIE" in os.environ:
     djj_bark_cookie = os.environ["DJJ_BARK_COOKIE"]
   if "DJJ_SEVER_JIANG" in os.environ:
      djj_sever_jiang = os.environ["DJJ_SEVER_JIANG"]
   if 'DJJ_SMALL_HEADERS' in os.environ:
      djj_small_headers =os.environ["DJJ_SMALL_HEADERS"]
      for line in djj_small_headers.split('\n'):
        if not line:
          continue 
        cookiesList.append(line.strip())
   elif djj_small_headers:
       for line in djj_small_headers.split('\n'):
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
def gettoken(hd):
   hd=json.dumps(hd)
   t=hd.split(',')
   for i in t:
      ii=i.find('&token=')
      if ii>0:
        return i[ii+8:len(i)-1]
        
        
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
   global headers,mypin,mytoken,numm
   check()
   numm=0
   iii=0
   for i in range(2):
     for count in cookiesList:
       numm+=1
       iii+=1
       print('【账号'+str(iii)+'】运行中'+'🔔'*iii)
     #if j!=1:
       #continue
       headers=eval(count)
       mytoken=gettoken(headers)
     #headers['Cookie']=count
     #if(islogon(j,count)):
       JD_homesmall()
     print('=====:💎:第'+str(i+1)+'💎次::::=::::::')
     if(i<1):
       time.sleep(10)
if __name__ == '__main__':
       start()
