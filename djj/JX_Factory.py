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



djj_sharecode=''
djj_bark_cookie=''
djj_sever_jiang=''
djj_djj_cookie=''

Defalt_ShareCode=['Q0VdTSuur3SLeSSfOW2A2Q==','v6859vuzm0wJDBqu2J9Shg==']

JD_API_HOST = 'https://m.jingxi.com'
codeurl='http://api.turinglabs.net/api/v1/jd/jxfactory/read/'
headers={
      'Host': 'm.jingxi.com',
      'Accept': '*/*',
      'User-Agent': 'jdpingou;iPhone;3.14.4;14.0;ae75259f6ca8378672006fc41079cd8c90c53be8;network/wifi;model/iPhone10,2;appBuild/100351;ADID/00000000-0000-0000-0000-000000000000;supportApplePay/1;hasUPPay/0;pushNoticeIsOpen/1;hasOCPay/0;supportBestPay/0;session/62;pap/JA2015_311210;brand/apple;supportJDSHWK/1;Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
      'Accept-Language': 'zh-cn',
      'Referer': 'https://wqsd.jd.com/pingou/dream_factory/index.html',
      'Accept-Encoding': 'gzip, deflate, br',
    }

      
    
cookiesList=[]
result=''
factoryId=''
productionId=''
ele=0
randomCount=5
encryptPin=''
unActive=False
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



def JX_DreamFactory():
   userInfo()
   
   doHelp()
   if(not unActive):
      return 
   getUserElectricity()
   DrawProductionStagePrize()
   taskList()
   investElectric()
   QueryHireReward()
   PickUp()
   stealFriend()
   
def taskList():
   print('\n taskList')
   try:
     data=json.loads(iosrulex('GetUserTaskStatusList'))
     #print(data)
     userTaskStatusList = data['data']['userTaskStatusList']
     for i in range(len(userTaskStatusList)):
         vo = userTaskStatusList[i];
         #print(vo)
         if (not vo['awardStatus']== 1):
           if (vo['completedTimes']>= vo['targetTimes']):
             print(f'''任务:{vo['description']}可完成''')
             completeTask(vo['taskId'],vo['taskName'])
             time.sleep(1)
           else:
             if(vo['taskType']==2 or vo['taskType']==6 or vo['taskType']==9):
                 print(f'''去做任务:{vo['taskName']}''')
                 doTask(vo['taskId'])
                 completeTask(vo['taskId'],vo['taskName'])
                 time.sleep(1)
             

   except Exception as e:
      msg=str(e)
      print(msg)
	
def completeTask(taskId, taskName):
   print('\n taskName taskId',taskName,taskId)
   global ele
   try:
     data=json.loads(iosrulex('Award', taskId))
     #print(data)
     sw=data['data']['awardStatus']
     if(sw==1):
        ele += int(data['data']['prizeInfo'].replace('\\n', ''))
        print(f'''领取{taskName}任务奖励成功，收获：{data['data']['prizeInfo']}电力''')
     else:
        print(f'''领取{taskName}任务奖励失败''')
   except Exception as e:
      msg=str(e)
      print(msg)
def doTask(taskId):
   print('\n taskId',taskId)
   try:
     data=json.loads(iosrulex('DoTask', taskId))
     #print(data)
     sw=data['ret']
     if(sw==0):
        print(f'''任务完成''')
     else:
        print(f'''任务失败{data['msg']}''')
   except Exception as e:
      msg=str(e)
      print(msg)
	
	
	
	
def getUserElectricity():
   print('\n getUserElectricity')
   flag=''
   try:
     print('factoryId',factoryId)
     data=json.loads(iosrule('generator/QueryCurrentElectricityQuantity','factoryid='+str(factoryId)))
     #print(data)
     if (data['ret'] == 0):
        if (data['data']['nextCollectDoubleFlag']==1):
          flag='可'
        else:
          flag='不可'
        print(f'''
     nextCollectDoubleFlag:{data['data']['nextCollectDoubleFlag']}
     nextCollectDoubleType:{data['data']['nextCollectDoubleType']}
     下次集满收取{flag}双倍电力
     发电机：当前 {data['data']['currentElectricityQuantity']} 
     电力，最大值 {data['data']['maxElectricityQuantity']} 电力''')
        if (data['data']['nextCollectDoubleFlag'] ==1):
           if (data['data']['currentElectricityQuantity'] == data['data']['maxElectricityQuantity'] and data['data']['doubleElectricityFlag']):
              print('发电机：电力可翻倍并收获')
              CollectCurrentElectricity()
           else:
              print(f'''【发电机电力】当前{data['data']['currentElectricityQuantity']} 电力，未达到收获标准\n''')
        else:
             print('再收取双倍电力达到上限时，直接收取，不再等到满级')
             
   except Exception as e:
      msg=str(e)
      print(msg)
def CollectCurrentElectricity():
   print('\n   CollectCurrentElectricity',factoryId)
   try:
        body = 'factoryid='+str(factoryId)+'&apptoken=&pgtimestamp=&phoneID=&doubleflag=1'
        data=json.loads(iosrule('generator/CollectCurrentElectricity', body))
        print(data)
        if (data['ret'] == 0):
          print(f'''【收取发电站】收取成功，获得{data['data']['CollectElectricity']} 电力''')
        else:
          print(f'''{data['msg']}''')
   except Exception as e:
      msg=str(e)
      print(msg)
def investElectric():
   print('\n   investElectric')
   try:
       data=json.loads(iosrule('userinfo/InvestElectric', 'productionId='+str(productionId)))
       print(data)
       if (data['ret'] == 0):
         print(f'''成功投入电力{data['data']['investElectric']}电力''')
       else:
          print(f'''投入失败{data['msg']}''')
   except Exception as e:
      msg=str(e)
      print(msg)
def QueryHireReward():
   print('\n  QueryHireReward')
   try:
       data=json.loads(iosrule('friend/QueryHireReward'))
       print(data)
       if (data['ret'] == 0):
         for item in data['data']['hireReward']:
                print(item['date'])
                hireAward(item['date'])
       else:
          print(f'''{data['msg']}''')
   except Exception as e:
      msg=str(e)
      print(msg)
def hireAward(date):
   print('\n   hireAward')
   try:
       data=json.loads(iosrule('friend/HireAward', 'date='+date+'&type=0'))
       #print(data)
       if (data['ret'] == 0):
         print(f'''打工电力,收取成功''')
       else:
          print(f'''打工电力,收取失败{data['msg']}''')
   except Exception as e:
      msg=str(e)
      print(msg)
def PickUp(Pin=encryptPin,help=False):
   print('\n   PickUp')
   try:
     for index in range(5):
       index+=1
       data=json.loads(iosrule('usermaterial/PickUpComponent', 'placeId='+str(index)+'&pin='+str(Pin)))
       #print(data)
       if (data['ret'] == 0):
         epower=data['data']['increaseElectric']
         if(help):
           print(f'''收取好友[{Pin}]零件成功:获得{epower}电力''')
         else:
           print(f'''收取自家零件成功:获得{epower}电力''')
       else:
         if(help):
           print(f'''收取好友[{Pin}]:{data['msg']}''')
         else:
           print(f'''收取自家零件失败:{data['msg']}''')
       time.sleep(1)
   except Exception as e:
      msg=str(e)
      print(msg)
      
def stealFriend():
   print('\n   stealFriend')
   try:
       data=json.loads(iosrule('friend/QueryFactoryManagerList', 'sort=0'))
       #print(data)
       if (data['ret'] == 0):
         el=data['data']['list']
         for i in el:
           Pin=i['encryptPin']
           if(Pin==Defalt_ShareCode[0] or Pin==Defalt_ShareCode[1]):
              continue
           PickUp(Pin,True)
           time.sleep(1)
       else:
           print(f'''{data['msg']}''')
   except Exception as e:
      msg=str(e)
      print(msg)
      

    
    
    
      
      
      
      
def userInfo():
   msg='userInfo'
   global factoryId,encryptPin,productionId,unActive
   factoryId=''
   encryptPin=''
   productionId=''
   unActive=False
   print(msg+'\n')
   try:
      taskData=json.loads(iosrule('userinfo/GetUserInfo', 'pin=&sharePin=&shareType=&materialTuanPin=&materialTuanId='))
      if(taskData['ret'] == 0):
        data = taskData['data']
        unActive = True
        encryptPin = ''
        if (data['factoryList'] and data['productionList']):
            production = data['productionList'][0]
            factory = data['factoryList'][0]
            factoryId = factory['factoryId']
            productionId = production['productionId']
            commodityDimId = production['commodityDimId'];
            encryptPin = data['user']['encryptPin']
            print('factoryId:💎',factoryId)
            print('encryptPin💎:',encryptPin)
            print('productionId💎:',productionId)
            productName=GetCommodityDetails(commodityDimId)
            Res=f'''【生产商品】{productName}
            当前电力:{data['user']['electric']}
            当前等级：{data['user']['currentLevel']}
            分享码: {data['user']['encryptPin']}
            生产进度：{round((production['investedElectric'] / production['needElectric']),2) * 100}%'''
            print(Res)
            msg +=Res
            
         
            if (production['investedElectric'] >= production['needElectric']):
              msg+=f'''【生产商品】{productName}已生产完,请速去兑换'''
        else:
             unActive=False
             print('【提示】此账号京喜工厂活动未开始\n请手动去京东APP->游戏与互动->查看更多->京喜工厂 开启活动\n')
      else:
          return
   except Exception as e:
      msg=str(e)
   loger(msg)

def GetCommodityDetails(commodityDimId):
   print('\n  GetCommodityDetails')
   try:
      data=json.loads(iosrule('diminfo/GetCommodityDetails', 'commodityId='+str(commodityDimId)))
      if (data['ret'] == 0):
         productName = data['data']['commodityList'][0]['name']
         return productName
      else:
        print('Data  err')
   except Exception as e:
      msg=str(e)
      print(msg)
def DrawProductionStagePrize():
   print('\n  DrawProductionStagePrize',productionId)
   try:
      data=iosrule('userinfo/DrawProductionStagePrize', 'productionId='+str(productionId))
      #print(data)
      if(data['ret']==0):
         print('成功======')
      else:
        print(f'''失败:{data['msg']}''')
   except Exception as e:
      msg=str(e)
      print(msg)
      

def doHelp():
   try:
      newShareCodes=shareCodesFormat()
      for code in newShareCodes:
          print(f'''开始助力京东账号{code}''')
          if (not code):
    	        continue
          if (code ==encryptPin):
             print('\n跳过自己的code \n')
             continue
          print(f'''\n开始助力好友: {code}''')
          helpResult= helpShare(code)
          if (helpResult and helpResult['ret'] == 0):
               print(f'''助力朋友：{code}成功，因一次只能助力一个，故跳出助力''')
               break
          elif (helpResult and helpResult['ret'] == 11009):
             print(f'''助力朋友[{code}]失败：{helpResult.msg}，跳出助力''')
             break
          else:
            print(f'''`助力朋友[{code}]失败:{helpResult.msg}''')
   except Exception as e:
       pass
def helpShare(code):
   try:
      #data=iosrule('')
     url=JD_API_HOST+f'''/dreamfactory/friend/AssistFriend?zone=dream_factory&sharepin='+{code}+'&sceneval=2&g_login_type=1'''
     header=headers
     header['Referer']='https://st.jingxi.com/pingou/dream_factory/index.html'
    
     header["User-Agent"]: "jdpingou;iPhone;3.15.2;14.2;f803928b71d2fcd51c7eae549f7bc3062d17f63f;network/4g;model/iPhone11,8;appBuild/100365;ADID/0E38E9F1-4B4C-40A4-A479-DD15E58A5623;supportApplePay/1;hasUPPay/0;pushNoticeIsOpen/1;hasOCPay/0;supportBestPay/0;session/2;pap/JA2015_311210;brand/apple;supportJDSHWK/1;"
     data=requests.get(url,headers=header).text
     print(data)
   except Exception as e:
    	print(str(e))
def readShareCode():
   url=f'''{codeurl}{randomCount}/'''
   try:
      readShareCodeRes=json.loads(requests.get(url).text)
      print(f'''随机取个{randomCount}码放到您固定的互助码后面''')
      return readShareCodeRes
   except Exception as e:
    	pass

def shareCodesFormat():
   newShareCodes = []
  # print(ShareCode)
   #ShareCode=''
   if(djj_sharecode):
      for line in djj_sharecode.split('\n'):
         if not line:
          continue 
         newShareCodes.append(line)
   else:
        print('Github助力码参数读取空，开始读取默认助力码')
        readShareCodeRes = readShareCode()
        print(readShareCodeRes)
        if (readShareCodeRes and readShareCodeRes['code'] == 200):
          newShareCodes=Defalt_ShareCode+readShareCodeRes['data']
        else:
            newShareCodes=Defalt_ShareCode
   print(f'''京东账号将要助力的好友{newShareCodes}''')
   return newShareCodes





    
def iosrule(functionId,body=''):
   url=JD_API_HOST+f'''/dreamfactory/{functionId}?zone=dream_factory&{body}&sceneval=2&g_login_type=1&_time={round(time.time()*1000)}&={round(time.time()*1000)+1}'''
   #print(url)
   try:
     response=requests.get(url,headers=headers).text
     return response
   except Exception as e:
      print(f'''初始化{functionId}任务:''', str(e))
def iosrulex(functionId,taskId=''):
   url=JD_API_HOST+f'''/newtasksys/newtasksys_front/{functionId}?source=dream_factory&bizCode=dream_factory&sceneval=2&g_login_type=1&&_time={round(time.time()*1000)}&={round(time.time()*1000)+1}'''
   #print(url)
   if (taskId):
      url += f'''&taskId={taskId}'''
   try:
     response=requests.get(url,headers=headers).text
     return response
   except Exception as e:
      print(f'''初始化{functionId}任务:''', str(e))

      
def check():
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   global djj_djj_cookie
   global djj_bark_cookie
   global djj_sever_jiang
   if "DJJ_BARK_COOKIE" in os.environ:
     djj_bark_cookie = os.environ["DJJ_BARK_COOKIE"]
   if "DJJ_SEVER_JIANG" in os.environ:
      djj_sever_jiang = os.environ["DJJ_SEVER_JIANG"]
   if "DJJ_DJJ_COOKIE" in os.environ:
      djj_djj_cookie = os.environ["DJJ_DJJ_COOKIE"]
      for line in djj_djj_cookie.split('\n'):
        if not line:
          continue 
        cookiesList.append(line.strip())
   elif djj_djj_cookie:
       for line in djj_djj_cookie.split('\n'):
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
   global djj_shop_headers
   check()
   j=0
   for count in cookiesList:
     j+=1
     #if j!=1:
       #continue
     headers['Cookie']=count
     if(islogon(j,count)):
         JX_DreamFactory()
   pushmsg('jx_factory',result)
if __name__ == '__main__':
       start()
