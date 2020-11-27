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


currentRoundId =''#本期活动id
lastRoundId = ''#上期id
roundList = [];
awardState = ''#上期活动的京豆是否收取
newShareCodes=[]
shareCodes=[]
#以上参数需要远程设置，以下为默认参数
JD_API_HOST = ''
codeurl='http://api.turinglabs.net/api/v1/jd/bean/read/'
randomCount = 5
headers={
         'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'JD4iPhone/167283 (iPhone;iOS 13.6.1;Scale/3.00)',
        'Accept-Language': 'zh-Hans-CN;q=1,en-CN;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': "application/x-www-form-urlencoded"
}
cookiesList=[]
result=''

Defalt_ShareCode= ['7oivz2mjbmnx4bddymkpj42u75jmba2c6ga6eba','2vgtxj43q3jqzr2i5ac4uj2h6wxl66n4i326u3i']#读取参数djj_sharecode为空，开始读取默认参数
if "JD_API_HOST" in os.environ:
      JD_API_HOST = os.environ["JD_API_HOST"]
      if not JD_API_HOST:
         print('over')
         exit()
def TotalBean(cookies,checkck):
   print('检验过期')
   signmd5=False
   global iosrule
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


def jdPlantBean():
   msg=''
   print('京东种豆\n')
   
   plantBeanIndexResult=json.loads(plantBeanIndex())
   #print(plantBeanIndexResult)
   try:
      #print(plantBeanIndexResult['data']['taskList'])
      if (plantBeanIndexResult['code'] == '0'):
          shareUrl = plantBeanIndexResult['data']['jwordShareInfo']['shareUrl']
          myPlantUuid = re.compile('plantUuid=(.*)').findall(shareUrl)[0]
          print(f'''\n【您的互助码】{myPlantUuid}\n''')
          roundList=plantBeanIndexResult['data']['roundList']
          currentRoundId = roundList[1]['roundId']#本期的roundId
          lastRoundId = roundList[0]['roundId']#上期的roundId
          awardState = roundList[0]['awardState']
          taskList = plantBeanIndexResult['data']['taskList']
          subTitle = f'''【京东昵称】{plantBeanIndexResult['data']['plantUserInfo']['plantNickName']}'''
          msg += f'''【上期时间】{roundList[0]['dateDesc']}\n'''
          msg += f'''【上期成长值】{roundList[0]['growth']}\n'''
      receiveNutrients(currentRoundId)#定时领取营养液
      doHelp(myPlantUuid)#助力
      doTask(taskList)#做日常任务
      doEgg()
      stealFriendWater(currentRoundId)
      doCultureBean(plantBeanIndexResult)
      doGetReward(awardState,roundList,lastRoundId)
      showTaskProcess()
      plantShareSupportList()
   except Exception as e:
      msg=str(e)
   print(msg)






def doTask(taskList):
   if (taskList and len(taskList) > 0):
    for item in taskList:
      print('次数','类型')
      print(item['dailyTimes'],item['taskType'])
      if (item['isFinished'] == 1):
         print(f'''{item['taskName']} 任务已完成\n''')
         continue
      else:
        if (item['taskType'] == 8):
          print(f'''\n【{item['taskName']}】任务未完成,需自行手动去京东APP完成，{item['desc']}营养液\n''')
        else:
          print(f'''\n【{item['taskName']}】任务未完成,{item['desc']}营养液\n''')
      if (item['dailyTimes'] == 1 and not item['taskType']== 8):
          print(f'''\n开始 {item['taskName']}任务,任务类型{item['taskType']}''')
          receiveNutrientsTaskRes=receiveNutrientsTask(str(item['taskType']))
          print(f'''做 {item['taskName']}任务结果:{receiveNutrientsTaskRes}\n''')
      if (item['taskType'] == 1):
          print('京东app签到')
          print(f'''\n开始做 {item['taskName']}任务''')
          signRes=signBeanIndex()
          print(signRes)
          if(signRes['code']=='0'):
             Bs=signRes['data']['dailyAward']
             print(f'''{Bs['title']}{Be['subTitle']}{Be['beanAward']['beanCount']}京豆''')
          receiveNutrientsTaskRes=receiveNutrientsTask(str(item['taskType']))
          print(f'''做 {item['taskName']}任务结果:{receiveNutrientsTaskRes}\n''')
         
      if (item['taskType'] == 3):
          print('浏览店铺')
          unFinishedShopNum = int(item['totalNum'])-int(item['gainedNum'])
          print(f'''\n开始做 {item['taskName']}任务,剩余店铺{unFinishedShopNum}个''')
          
          if (unFinishedShopNum == 0):
             continue
          
          shopTaskListRes= json.loads(shopTaskList())
          
          goodShopListARR = []
          moreShopListARR = []
          shopList = []
          for i in shopTaskListRes['data']['goodShopList']:

             if (i['taskState'] == '2'):
                goodShopListARR.append(i)
          for j in shopTaskListRes['data']['moreShopList']:
             if (j['taskState'] == '2'):
               moreShopListARR.append(j)
          shopList = goodShopListARR+moreShopListARR
          for shop in shopList:
             shopId=shop['shopId']
             shopTaskId=shop['shopTaskId']
             shopRes=json.loads(shopNutrientsTask(shopId,shopTaskId))
             print(f'''shopRes结果:{shopRes}''')
             if (shopRes['code'] == '0' and json.dumps(shopRes).find('errorMessage')<0):
                if (shopRes['data'] and shopRes['data']['nutrState'] and shopRes['data']['nutrState'] =='1'):
                   unFinishedShopNum-=1
             time.sleep(2)
             if (unFinishedShopNum <= 0):
                print(f'''{item['taskName']}任务已做完\n''')
                break
      if (item['taskType'] ==5):
        print('挑选商品')
        unFinishedProductNum = int(item['totalNum'])-int(item['gainedNum'])
        print(f'''开始做{item['taskName']}任务,剩余{unFinishedProductNum}个''')
        
        if (unFinishedProductNum == 0):
          continue
        productTaskListRes= json.loads(productTaskList())
        productListARR = []
        productList = []
        productInfoList= productTaskListRes['data']['productInfoList']
        for i in range(len(productInfoList)):
          for j in range(len(productInfoList[i])):
            productListARR.append(productInfoList[i][j])
        for i in productListARR:
          if (i['taskState'] == '2'):
             productList.append(i)
        for product in productList:
          productTaskId=product['productTaskId']
          skuId=product['skuId']
          productRes=json.loads(productNutrientsTask(productTaskId,skuId))
          print(productRes)
          if (productRes['code']=='0'and json.dumps(productRes).find('errorMessage')<0):
            #这里添加多重判断,有时候会出现活动太火爆的问题,导致nutrState没有
            if (productRes['data'] and productRes['data']['nutrState'] and productRes['data']['nutrState'] =='1'):
              unFinishedProductNum -=1
          time.sleep(2)
          if (unFinishedProductNum <= 0):
            print(f'''{item['taskName']}任务已做完\n''')
            break
      if (item['taskType'] ==10):
        print('关注频道')
        unFinishedChannelNum = int(item['totalNum'])-int(item['gainedNum'])
        print(f'''开始做 {item['taskName']}任务,剩余{unFinishedChannelNum}个''')

        if (unFinishedChannelNum == 0):
            continue
        pctlRes= json.loads(plantChannelTaskList())
        goodChannelListARR = []
        normalChannelListARR = []
        channelList = []
        for i in pctlRes['data']['goodChannelList']:
          if (i['taskState'] == '2'):
            goodChannelListARR.append(i);
        for j in pctlRes['data']['normalChannelList']:
          if (j['taskState'] == '2'):
            normalChannelListARR.append(j)
        channelList = goodChannelListARR+normalChannelListARR
        for channelItem in channelList:
          channelId=channelItem['channelId']
          channelTaskId=channelItem['channelTaskId']
          print(channelId,channelTaskId)
          channelRes=json.loads(plantChannelNutrientsTask(channelId,channelTaskId))
          print(f'''channelRes结果:{channelRes}''')
          if (channelRes['code'] == '0' and json.dumps(channelRes).find('errorMessage')<0):
            if (channelRes['data'] and channelRes['data']['nutrState'] and channelRes['data']['nutrState']== '1'):
              unFinishedChannelNum -=1
          time.sleep(2)
          if (unFinishedChannelNum <= 0):
            print(f'''{item['taskName']}任务已做完\n''')
            break
   
      
def doEgg():
   plantEggLotteryRes=json.loads(egg())
   #print(plantEggLotteryRes)
   if (plantEggLotteryRes['code'] == '0'):
      if (plantEggLotteryRes['data']['restLotteryNum'] > 0):
          eggL=plantEggLotteryRes['data']['restLotteryNum']
          print(f'''目前共有{eggL}次扭蛋的机会''')
          for i in range(eggL):
              print(f'''开始第{i + 1}次扭蛋''')
              plantEggDoLotteryResult= plantEggDoLottery()
              print(f'''天天扭蛋成功：{plantEggDoLotteryResult}''')
      else:
         print('暂无扭蛋机会')
   else:
       print('查询天天扭蛋的机会失败')
def stealFriendWater(currentRoundId):
  sFriendList=json.loads(stealFriendList())
  print(sFriendList)
  if (sFriendList['code'] == '0'):
    if (json.dumps(sFriendList).find('tips'))>0:
       print('偷取好友营养液今日已达上限')
       return
    if (sFriendList['data'] and sFriendList['data']['friendInfoList'] and len(sFriendList['data']['friendInfoList']) > 0):
      for item in sFriendList['data']['friendInfoList']:
        if (json.dumps(item).find('nutrCount'))<0:
          print('好友暂无营养液可以偷')
          continue
        if int(item['nutrCount']) >= 1:
          stealFriendRes=json.loads(collectUserNutr(currentRoundId,item['paradiseUuid']))
          #print(f'''偷取好友营养液情况:{stealFriendRes}''')
          if (stealFriendRes['code']== '0'):
            print('偷取好友营养液成功')
          time.sleep(3)
def doCultureBean(plantBeanIndexResult):
   if (plantBeanIndexResult['code'] == '0'):
      plantBeanRound=plantBeanIndexResult['data']['roundList'][1]
      if (plantBeanRound['roundState'] == '2'):
         print('开始收取营养液')
         for bubbleInfo in plantBeanRound['bubbleInfos']:
           print(f'''收取-{bubbleInfo['name']}-的营养液''')
           cultureBeanRes=cultureBean(plantBeanRound['roundId'], bubbleInfo['nutrientsType'])
           print(f'''收取营养液结果:{cultureBeanRes}''')
           time.sleep(2)
   else:
      print(f'''plantBeanIndexResult:{plantBeanIndexResult}''')
  
def doGetReward(awardState,roundList,lastRoundId):
   print('上期兑换京豆')
   msg=''
   if (awardState == '4'):
      print('京豆采摘中...')
      msg +=f''' 【上期状态】{roundList[0]['tipBeanEndTitle']}\n''';
   elif (awardState =='5'):
       print('收获')
       getReward= json.loads(getReward(lastRoundId))
       print('开始领取京豆');
       if(getReward['code'] =='0'):
           print('京豆领取成功');
           msg += f'''【上期兑换京豆】{getReward['data']['awardBean']}个\n`'''
 
   elif (awardState == '6'):
        print('京豆已领取')
        msg += f'''【上期兑换京豆】{roundList[0]['awardBeans']}个\n'''
        dDs=roundList[1]['dateDesc']
        if (dDs.find('本期')>=0):
            dDs = dDs[dDs.find('本期')+3:len(roundList[1].dateDesc)]
        msg += f'''【本期时间】{ds}\n'''
        msg += f'''【本期成长值】{roundList[1]['growth']}\n'''
   print(msg)
def showTaskProcess():
   print('任务进度')
   plantBeanIndexResult=json.loads(plantBeanIndex())
   print(plantBeanIndexResult)
   taskList = plantBeanIndexResult['data']['taskList']
   if (taskList and len(taskList) > 0):
      print('任务           进度')
      for item in taskList:
        print(f'''[{item["taskName"]}]  {item["gainedNum"]}/{item["totalNum"]}   {item["isFinished"]}''')
	

def plantShareSupportList():
   msg='【助力您的好友】'
   print(msg)
   shareSupportList =json.loads(iosrule(sys._getframe().f_code.co_name,{"roundId": ""}))
   print(shareSupportList)
   if (shareSupportList and shareSupportList['code']== '0'):
       data= shareSupportList['data']
       msg+= f'''共{len(data)}人'''
       print(msg)
   else:
       print(f'''异常情况：{shareSupportList}''')
    
	
def stealFriendList():
   body = {
    'pageNum': '1'
  }
   stealFriendList = iosrule('plantFriendList', body);
   return stealFriendList


def collectUserNutr(currentRoundId,paradiseUuid):
   print('开始偷好友')
   body = {
    "paradiseUuid": paradiseUuid,
    "roundId": currentRoundId
  }
   stealFriendRes = iosrule('collectUserNutr', body);
   return stealFriendRes

def  getReward(lastRoundId):
   body = {
    "roundId": lastRoundId
  }
   getReward = iosrule('receivedBean', body)

def cultureBean(currentRoundId, nutrientsType):
   body = {
    "roundId": currentRoundId,
    "nutrientsType": nutrientsType,
  }
   cultureBeanRes=iosrule(sys._getframe().f_code.co_name,body)
   return cultureBeanRes
def signBeanIndex():
   body={"jda":"-1","monitor_source":"bean_app_bean_index","shshshfpb":"","fp":"-1","eid":"","shshshfp":"-1","monitor_refer":"","userAgent":"-1","rnVersion":"4.0","shshshfpa":"-1","referUrl":"-1"}
   TaskRes=json.loads(iosrule('signBeanIndex',body))
   return TaskRes
   
def plantChannelTaskList():
   pctlres=iosrule(sys._getframe().f_code.co_name)
   return pctlres

def shopTaskList():
   body={"monitor_refer": "plant_receiveNutrients"}
   shopTaskListRes=iosrule(sys._getframe().f_code.co_name)
   return shopTaskListRes
def plantEggDoLottery():
   plantEggDoLotteryResult=iosrule(sys._getframe().f_code.co_name)
   return plantEggDoLotteryResult

def receiveNutrientsTask(awardType):
   body = {
    "monitor_refer": "receiveNutrientsTask",
    "awardType": awardType,
    "monitor_source":"plant_app_plant_index"
        }
   receiveNutrientsTaskRes=json.loads(iosrule(sys._getframe().f_code.co_name,body))
   return receiveNutrientsTaskRes
#查询天天扭蛋的机会
def egg():
   plantEggLotteryRes =iosrule('plantEggLotteryIndex')
   return  plantEggLotteryRes
def productTaskList():
   body = {"monitor_refer": "plant_productTaskList"}
   ptlistres=iosrule(sys._getframe().f_code.co_name,body)
   return ptlistres
def plantChannelNutrientsTask(id1,id2):
   body = {
            "channelId": id1,
            "channelTaskId":id2
            }
   channelRes=iosrule(sys._getframe().f_code.co_name,body)
   return channelRes
def productNutrientsTask(id1,id2):
   body = {
            "monitor_refer": "plant_productNutrientsTask",
            "productTaskId": id1,
            "skuId": id2
            }
   TiaoRes=iosrule(sys._getframe().f_code.co_name,body)
   return TiaoRes
def shopNutrientsTask(shopId,shopTaskId):
   body = {
            "monitor_refer":"plant_shopNutrientsTask",
            "shopId": shopId,
            "shopTaskId": shopTaskId
               }
   shopRes =iosrule(sys._getframe().f_code.co_name,body)
   return shopRes
   
def receiveNutrients(currentRoundId):
   body={"roundId": currentRoundId, "monitor_refer": "plant_receiveNutrients"}
   receiveNutrientsRes=iosrule(sys._getframe().f_code.co_name,body)
def doHelp(myPlantUuid):
   newShareCodes=shareCodesFormat()
   for plantUuid in newShareCodes:
       print(f'''开始助力京东账号{plantUuid}''')
       if (not plantUuid):
    	    continue
       if (plantUuid ==myPlantUuid):
          print('\n跳过自己的plantUuid \n')
          continue
       print(f'''\n开始助力好友: {plantUuid}''')
       helpResult= helpShare(plantUuid)
       if (helpResult['code'] == '0'):
          if (helpResult['data']['helpShareRes']):
             if (helpResult['data']['helpShareRes']['state']=='1'):
                 print(f'''助力好友{plantUuid}成功''')
                 print(f'''{helpResult['data']['helpShareRes']['promptText']}\n''')
             elif (helpResult['data']['helpShareRes']['state'] == '2'):
                 print('您今日助力的机会已耗尽，已不能再帮助好友助力了\n')
                 break
             elif (helpResult['data']['helpShareRes']['state'] == '3'):
                 print('该好友今日已满9人助力/20瓶营养液,明天再来为Ta助力吧\n')
             elif (helpResult['data']['helpShareRes']['state'] =='4'):
                  print(f'''{helpResult['data']['helpShareRes']['promptText']}\n''')
             else:
              print(f'''助力其他情况：{helpResult['data']['helpShareRes']}''')
       else:
           print(f'''助力好友失败: {helpResult}''')

def helpShare(plantUuid):
   body = {
    "plantUuid": plantUuid,
    "wxHeadImgUrl": "",
    "shareUuid": "",
    "followType": "1",
  }
   try:
     helpResult=json.loads(iosrule('plantBeanIndex',body))
     return helpResult
   except Exception as e:
       print(str(e))
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
        if (readShareCodeRes and readShareCodeRes['code'] == 200):
           newShareCodes=Defalt_ShareCode+readShareCodeRes['data']
            
   print(f'''京东账号将要助力的好友{newShareCodes}''')
   return newShareCodes
   
   
def plantBeanIndex():
   try:   
     body={"monitor_source":"plant_app_plant_index","monitor_refer":"","version":"9.0.0.4"}
     plantBeanIndexResult=iosrule(sys._getframe().f_code.co_name,body)
     return plantBeanIndexResult
   except Exception as e:
      print("初始化种豆任务:", str(e))
      time.sleep(2)
      
      


def inviteFriend(code):
   body={
    'imageUrl': "",
    'nickName': "",
    'shareCode': code + '-inviteFriend',
    'version': 4,
    'channel': 2
  }
   inviteFriendRes=iosrule('initForFarm',body)
   return inviteFriendRes


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
        if (readShareCodeRes and readShareCodeRes['code'] == 200):
          newShareCodes=Defalt_ShareCode+readShareCodeRes['data']
            
            
   print(f'''京东账号将要助力的好友{newShareCodes}''')
   return newShareCodes
     
def iosrule(mod,body={}):
   url=JD_API_HOST+f'''?functionId={mod}&appid=ld&body={urllib.parse.quote(json.dumps(body))}'''
   try:
     response=requests.get(url,headers=headers).text
     return response
   except Exception as e:
      print(f'''初始化{mode}任务:''', str(e))
      
      
def check():
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   global djj_djj_cookie
   global djj_bark_cookie
   global djj_sever_jiang
   global JD_API_HOST
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
    
def DJJ_main():
   jdPlantBean()
  # pushmsg('种豆',result)
   
   
   
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
   check()
   #print(cookiesList)
   j=0
   for count in cookiesList:
     j+=1
     #if j!=1:
       #continue
     oldstr = count.split(';')
     for i in oldstr:
       if i.find('pin=')>=0:
          newstr=i.strip()[i.find('pin=')+4:len(i)]
          print(f'''>>>>>>>>>【账号{str(j)}开始】{newstr}''')
     headers['Cookie']=count
     if(TotalBean(count,newstr)):
         DJJ_main()
def main_handler(event, context):
    return start()

if __name__ == '__main__':
       start()
