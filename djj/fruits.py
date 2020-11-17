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
#by  红鲤鱼绿鲤鱼与驴，学习与测试用


djj_sharecode=''
djj_bark_cookie=''
djj_sever_jiang=''
djj_djj_cookie=''
#以上参数需要远程设置，以下为默认参数
JD_API_HOST = 'https://api.m.jd.com/client.action'
urlSchema = 'openjd://virtual?params=%7B%20%22category%22:%20%22jump%22,%20%22des%22:%20%22m%22,%20%22url%'
headers={
      'UserAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
}
cookiesList=[]
result=''
isFruitFinished=False
jdFruitBeanCard='false'#您设置的是使用水滴换豆卡，且背包有水滴换豆卡, 跳过10次浇水任务
Defalt_ShareCode= ['8b4f04a07a21445a9a7da6ddb4159427',
'ae6488dc5f0c4669bfa432b9bc884191','268e797816f340bc9ad3656fa249d1a6']#读取参数djj_sharecode为空，开始读取默认参数
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
       ckresult= requests.get('https://wq.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New',headers=headers).json()
       print(ckresult)
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


def jdFruit():
   msg=''
   print('水果\n')
   farmInfo=initForFarm()
   try:
      if (farmInfo['farmUserPro']):
       msg+= f'''【水果名称】{farmInfo['farmUserPro']['name']}
【互助码】{farmInfo['farmUserPro']['shareCode']}
【已成功兑换水果】{str(farmInfo['farmUserPro']['winTimes'])}次'''
      loger(msg)
      #助力好友一下
      masterHelpShare(farmInfo)
      if (farmInfo['treeState'] ==2 or farmInfo['treeState'] == 3):
        	msg=f'''京东账号x,昵称x,用户名y,【提醒⏰】{farmInfo['farmUserPro']['name']}水果已可领取'''
        	print(msg)
        	return 
      elif (farmInfo['treeState'] ==1):
        	msg=f'''京东账号x,昵称x,用户名y,{farmInfo['farmUserPro']['name']}种植中...
        	'''
        	print(msg)
      elif (farmInfo['treeState'] ==0):
        	msg=f'''京东账号x,昵称x,用户名y,{farmInfo['farmUserPro']['name']}【提醒⏰】您忘了种植新的水果\n请去京东APP或微信小程序选购并种植新的水果'''
        	print(msg)
        	return 
        	
      print(f'''
   【被水滴砸中】{farmInfo['todayGotWaterGoalTask']['canPop']}'''
   )
      if (farmInfo['todayGotWaterGoalTask']['canPop']):
         goalResult=gotWaterGoalTaskForFarm()
         if (goalResult['code']=='0'):
             print(f'''
      【被水滴砸中】获得{goalResult['addEnergy']}g💧
      ''')
      doDailyTask(farmInfo)
      getAwardInviteFriend(farmInfo)
      
      duck()
      
   except Exception as e:
      msg=str(e)
      print(msg)





def masterHelpShare(farmInfo):
   msg='开始助力好友'
   print('\n'+msg)
   salveHelpAddWater = 0
   remainTimes = 4#今日剩余助力次数,默认4次（京东农场每人每天4次助力机会）。
   helpSuccessPeoples = ''
   newShareCodes=shareCodesFormat()
   for code in newShareCodes:
      print(f'''开始助力京东账号的好友: {code}''')
      if (not code):
      	continue;
      if (code ==farmInfo['farmUserPro']['shareCode']):
         print('不能为自己助力哦，跳过自己的shareCode\n')
         continue
      helpResult=masterHelp(code)
      #print('助力结果',helpResult)
      if (helpResult['code'] =='0'):
        if (helpResult['helpResult']['code'] == '0'):
            salveHelpAddWater +=helpResult['helpResult']['salveHelpAddWater']
        
            print(f'''【助力好友结果】: 已成功给【{helpResult['helpResult']['masterUserInfo']['nickName']}】助力''')
        
            print(f'''给好友【${helpResult['helpResult']['masterUserInfo']['nickName']}】助力获得${helpResult['helpResult']['salveHelpAddWater']}g水滴''')
        
            helpSuccessPeoples += helpResult['helpResult']['masterUserInfo']['nickName'] + ','
        elif (helpResult['helpResult']['code'] == '8'):
            print(f'''【助力好友结果】: 助力【{helpResult['helpResult']['masterUserInfo.nickName']}】失败，您今天助力次数已耗尽''');
        elif helpResult['helpResult']['code'] =='9':
            print(f'''【助力好友结果】: 之前给【{helpResult['helpResult']['masterUserInfo']['nickName']}】助力过了''');
        elif helpResult['helpResult']['code'] =='10':
            print(f'''【助力好友结果】: 好友【{helpResult['helpResult']['masterUserInfo']['nickName']}】已满五人助力''')
        else:
            print(f'''助力其他情况：{helpResult['helpResult']}''')
        print(f'''【今日助力次数还剩】{helpResult['helpResult']['remainTimes']}次\n''')
      
        remainTimes = helpResult['helpResult']['remainTimes']
        if (helpResult['helpResult']['remainTimes']== 0):
           print('您当前助力次数已耗尽，跳出助力')
           break
      else:
         print(f'''助力失败:{helpResult}''')
    
  
    
    
def doDailyTask(farmInfo):
   msg='日常任务'
   print('\n'+msg)
   
   farmTask=taskInitForFarm()
   try:
      if (not farmTask['signInit']['todaySigned']):
        print(f'''
           ✍️🏻还没有签到,开始签到''')

        signResult=signForFarm()
        if (signResult['code']=="0"):
           print(f'''
           【签到成功】获得{signResult['amount']}g💧
           ''')
      else:
         print(f'''
         今天已签到,连续签到{str(farmTask['signInit']['totalSigned'])}天,下次签到可得{farmTask['signInit']['signEnergyEachAmount']}g
         ''')
         
      print(f'签到结束,开始广告浏览任务')
      if (not farmTask['gotBrowseTaskAdInit']['f']) :
         adverts =farmTask['gotBrowseTaskAdInit']['userBrowseTaskAds']
         for advert in adverts:
              if (advert['limit']<=advert['hadFinishedTimes']):
                 print(f'''{advert['mainTitle']} 已完成''')
                 continue
               
              print(f'''正在进行广告浏览任务:{advert['mainTitle']}''')
              browseResult = browseAdTaskForFarm(advert['advertId'],0)
              if (browseResult['code'] =='0'):
                 print(f'''{advert['mainTitle']}浏览任务完成''')
                 browseRwardResult = browseAdTaskForFarm(advert['advertId'],1)
                 if (browseRwardResult['code']=='0'):
                     print(f'''领取浏览{advert['mainTitle']}广告奖励成功,获得{browseRwardResult['amount']}g''')
                 else:
                    print(f'''领取浏览广告奖励结果: {json.dumps(browseRwardResult)}''')
              else:
                   print(f'''领取浏览广告奖励结果: {json.dumps(browseResult)}''')
         
      else:
          print('今天已经做过浏览广告任务\n')
          
      print(f'浏览广告结束,开始定时领水任务')
      if (not farmTask['gotThreeMealInit']['f']) :
         gotThreeMealForFarm()
      else:  
          print('当前不在定时领水时间断或者已经领过')
      print(farmTask['waterFriendTaskInit'])
      
      if (not farmTask['waterFriendTaskInit']['f']):
       if (farmTask['waterFriendTaskInit']['waterFriendCountKey']<farmTask['waterFriendTaskInit']['waterFriendMax']):
       	   doFriendsWater(farmTask['waterFriendTaskInit']);
    
       else:
           print(f'''给{farmTask['waterFriendTaskInit']['waterFriendMax']}个好友浇水任务已完成''')
      clockIn()
      executeWaterRains(farmTask)
      getExtraAward()
      doTenWater(farmTask,farmInfo)
      doTenWaterAgain(farmInfo)#再次浇水
      getFirstWaterAward(farmTask)#领取首次浇水奖励
      getTenWaterAward(farmTask)#领取10浇水奖励
      getWaterFriendGotAward(farmTask)#领取为2好友浇水奖励
      turntableFarm(farmInfo)#天天抽奖得好礼
   except Exception as e:
      msg+=str(e)
      print(msg)
      
 
 #def getFirstWaterAward():
 	
def turntableFarm(farmInfo):
   print('抽奖中')
   initForTurntableFarmRes=initForTurntableFarm()
   print('初始化集卡抽奖活动数据API')
   if (initForTurntableFarmRes['code']== '0'):
    #领取定时奖励 //4小时一次
      timingIntervalHours=initForTurntableFarmRes['timingIntervalHours']
      timingLastSysTime=initForTurntableFarmRes['timingLastSysTime']
      sysTime=initForTurntableFarmRes['sysTime']
      timingGotStatus=initForTurntableFarmRes['timingGotStatus']
      remainLotteryTimes=initForTurntableFarmRes['remainLotteryTimes']
      turntableInfos=initForTurntableFarmRes['turntableInfos']

      if (not timingGotStatus):
          print(f'''是否到了领取免费赠送的抽奖机会--{sysTime > (timingLastSysTime + 60*60*timingIntervalHours*1000)}''')
          if (sysTime > (timingLastSysTime + 60*60*timingIntervalHours*1000)):
             print('timingAwardForTurntableFarm')
             timingAwardRes=timingAwardForTurntableFarm()
             print(f'''领取定时奖励结果{timingAwardRes}''')
             initForTurntableFarmRes=initForTurntableFarm()
             remainLotteryTimes=initForTurntableFarmRes['remainLotteryTimes']
          else:
              print('免费赠送的抽奖机会未到时间')
      print('4小时候免费赠送的抽奖机会已领取')
      print(initForTurntableFarmRes['turntableBrowserAds'])
      if initForTurntableFarmRes['turntableBrowserAds'] and len(initForTurntableFarmRes['turntableBrowserAds'])> 0:
         for index in range(len(initForTurntableFarmRes['turntableBrowserAds'])):
            if (not initForTurntableFarmRes['turntableBrowserAds'][index]['status']) :
                print(f'''开始浏览天天抽奖的第{index + 1}个逛会场任务''')
                browserForTurntableFarmRes=browserForTurntableFarm(1, initForTurntableFarmRes['turntableBrowserAds'][index]['adId'])
                if (browserForTurntableFarmRes['code'] =='0' and browserForTurntableFarmRes['status']):
                   print(f'''第{index + 1}个逛会场任务完成，开始领取水滴奖励\n''')
                   browserForTurntableFarmRes= browserForTurntableFarm(2,initForTurntableFarmRes['turntableBrowserAds'][index]['adId']);
                   if (browserForTurntableFarmRes['code'] == '0'):
                       print(f'''第{index + 1}个逛会场任务领取水滴奖励完成\n''')
                       initForTurntableFarmRes=initForTurntableFarm()
                       remainLotteryTimes = initForTurntableFarmRes['remainLotteryTimes']
          
         else:
            print(f'''浏览天天抽奖的第{index + 1}个逛会场任务已完成''')
        
    #天天抽奖助力
      print('开始天天抽奖--好友助力--每人每天只有三次助力机会.')
      newShareCodes=shareCodesFormat()
      for code in newShareCodes:
         if (code ==farmInfo['farmUserPro']['shareCode']):
            print('天天抽奖-不能自己给自己助力\n')
            continue
         lotteryMasterHelpRes=lotteryMasterHelp(code)
         print('天天抽奖助力结果',lotteryMasterHelpRes['helpResult'])
         if  json.dumps(lotteryMasterHelpRes['helpResult']).find('nickName')>0:
             pout=lotteryMasterHelpRes['helpResult']['masterUserInfo']['nickName']
         else:
         		 pout=lotteryMasterHelpRes['helpResult']['masterUserInfo']['shareCode']
         if (lotteryMasterHelpRes['helpResult']['code'] == '0' ):
            print(f'''天天抽奖-助力{pout}成功\n''')
         elif (lotteryMasterHelpRes['helpResult']['code']== '11'):
            print(f'''天天抽奖-不要重复助力{pout}\n''')
         elif (lotteryMasterHelpRes['helpResult']['code']== '13'):
           print(f'''天天抽奖-助力{pout}失败,助力次数耗尽\n''');
           break
      print(f'''--天天抽奖次数remainLotteryTimes----{remainLotteryTimes}次''')
   #抽奖
      if (remainLotteryTimes > 0):
         print('开始抽奖')
         lotteryResult = ''
         lotteryRes=lotteryForTurntableFarm()
         if (lotteryRes['code'] == '0'):
            if(json.dumps(lotteryRes).find('bean')>0):
              print(f'''获得{lotteryRes['beanCount']}个豆子,剩余{lotteryRes['remainLotteryTimes']}次机会''')
            elif (json.dumps(lotteryRes).find('water')>0):
               print(f'''获得{lotteryRes['addWater']}滴水,剩余{lotteryRes['remainLotteryTimes']}次机会''')
            else:
              print(f'''获得{lotteryRes['type']},剩余{lotteryRes['remainLotteryTimes']}次机会''')
      else:
         print('天天抽奖--抽奖机会为0次')
  
   else:
      print('初始化天天抽奖得好礼失败')
  
 	
 	
 	
def doTenWater(farmTask,farmInfo):
   print('\n准备浇水十次')
   myCardInfoRes=myCardInfoForFarm()
   print(myCardInfoRes)
   if ({jdFruitBeanCard}== 'true' and json.dumps(myCardInfoRes).encode('ascii').decode('unicode_escape').find('限时翻倍')>0 and myCardInfoRes['beanCard'] > 0):
       print(f'''您设置的是使用水滴换豆卡，且背包有水滴换豆卡{myCardInfoRes['beanCard']}张, 跳过10次浇水任务''')
       return
   print('没换豆开始浇水十次')
   if farmTask['totalWaterTaskInit']['totalWaterTaskTimes'] < farmTask['totalWaterTaskInit']['totalWaterTaskLimit'] :
       waterCount = 0
       isFruitFinished = False
       for waterCount in range(farmTask['totalWaterTaskInit']['totalWaterTaskLimit'] -farmTask['totalWaterTaskInit']['totalWaterTaskTimes']):
           print(f'''第{waterCount + 1}次浇水''')
           waterResult=waterGoodForFarm()
           print(f'''本次浇水结果:{waterResult}''')
           if (waterResult['code']=='0'):
               print(f'''剩余水滴{waterResult['totalEnergy']}g''')
               if (waterResult['finished']):
          #已证实，waterResult.finished为true，表示水果可以去领取兑换了
                  isFruitFinished =True
                  break
               else:
                   if (waterResult['totalEnergy'] < 10):
                       print('水滴不够，结束浇水')
                       break
               gotStageAward(waterResult)#领取阶段性水滴奖励
           else:
                 print('浇水出现失败异常,跳出不在继续浇水')
                 break
       if isFruitFinished:
            print(f'''【提醒⏰】{farmInfo['farmUserPro']['name']}已可领取`, '请去京东APP或微信小程序查看\n点击弹窗即达''')
            
            
def gotStageAward(waterResult):
   print('领取阶段性水滴奖励')
   if (waterResult['waterStatus'] == 0 and waterResult['treeEnergy'] == 10):
      print('果树发芽了,奖励30g水滴')
      gotStageAwardForFarmRes= gotStageAwardForFarm('1')
      print(f'''浇水阶段奖励1领取结果{gotStageAwardForFarmRes}''')
      if (gotStageAwardForFarmRes['code']=='0'):
         print(f'''【果树发芽了】奖励{gotStageAwardForFarmRes['addEnergy']}\n''')
      
      elif (waterResult['waterStatus'] ==1):
         print('果树开花了,奖励40g水滴')
         gotStageAwardForFarmRes=gotStageAwardForFarm('2')
         print(f'''浇水阶段奖励2领取结果{gotStageAwardForFarmRes}''')
         if (gotStageAwardForFarmRes['code'] =='0'):
             print(f'''【果树开花了】奖励{gotStageAwardForFarmRes['addEnergy']}g💧\n''')
         elif (waterResult['waterStatus']== 2):
             print('果树长出小果子啦, 奖励50g水滴');
             gotStageAwardForFarmRes=gotStageAwardForFarm('3')
             print(f'''浇水阶段奖励3领取结果{gotStageAwardForFarmRes}''')
             if (gotStageAwardForFarmRes['code'] =='0'):
                 print(f'''【果树结果了】奖励{gotStageAwardForFarmRes['addEnergy']}g💧\n''');
     
      
      

def getFirstWaterAward(farmTask):
   print('领取首次浇水奖励')
   if (not farmTask['firstWaterInit']['f'] and farmTask['firstWaterInit']['totalWaterTimes'] > 0):
       firstWaterReward= firstWaterTaskForFarm()
       if (firstWaterReward['code']== '0'):
           print(f'''【首次浇水奖励】获得{firstWaterReward['amount']}g💧\n''')

       else:
          print(f'''领取首次浇水奖励结果:{firstWaterReward}''')
   else:
      print('首次浇水奖励已领取\n')
	
def getTenWaterAward(farmTask):
   print('领取10次浇水奖励')
   if (not farmTask['totalWaterTaskInit']['f'] and farmTask['totalWaterTaskInit']['totalWaterTaskTimes'] >= farmTask['totalWaterTaskInit']['totalWaterTaskLimit']):
       totalWaterReward= totalWaterTaskForFarm()
       if (totalWaterReward['code'] == '0'):
            print(f'''【十次浇水奖励】获得{totalWaterReward['totalWaterTaskEnergy']}g💧\n''')
       else:
           print(f'''领取10次浇水奖励结果:{totalWaterReward}''')
    
   elif (farmTask['totalWaterTaskInit']['totalWaterTaskTimes'] < farmTask['totalWaterTaskInit']['totalWaterTaskLimit']):
       print(f'''【十次浇水奖励】任务未完成，今日浇水{farmTask['totalWaterTaskInit']['totalWaterTaskTimes']}次\n''')
   print('finished 水果任务完成!');

def doTenWaterAgain(farmInfo):
   #再次浇水
   print('开始检查剩余水滴能否再次浇水再次浇水\n')
   totalEnergy= farmInfo['farmUserPro']['totalEnergy']
   print(f'''剩余水滴{totalEnergy}g\n''')
   myCardInfoRes= myCardInfoForFarm()
   print(f'''背包已有道具:\n快速浇水卡:未解锁{myCardInfoRes['fastCard']}张\n水滴翻倍卡:未解锁': {myCardInfoRes['doubleCard']}张\n水滴换京豆卡:未解锁':{myCardInfoRes['beanCard']} 张\n加签卡:未解锁' : {myCardInfoRes['signCard']} 张\n''')
   if (totalEnergy >= 100 and myCardInfoRes['doubleCard'] > 0):
    #使用翻倍水滴卡
     userMyCardForFarm=userMyCardForFarm('doubleCard');
     print(f'''使用翻倍水滴卡结果:{userMyCardRes}''')
   
	
#def gotStageAward():
	
	
#def getExtraAward():
	
	
	
	
def clockIn():
   print('开始打卡领水活动（签到，关注，领券)🐶')
   print('打卡领水')
   clockInInit = clockInInitForFarm()
   if (clockInInit['code'] == "0"):
     if (not clockInInit['todaySigned']):
        print('开始今日签到领水滴')
        clockInForFarmRes=clockInForFarm()
        if (clockInForFarmRes['code'] ==0):
          print('''【第{clockInForFarmRes['signDay']}天签到】获得{clockInForFarmRes['amount']💧''')
          if (clockInForFarmRes['signDay'] ==7):
              print('开始领取--惊喜礼包38g水滴')
              gotClockInGiftRes=gotClockInGift()
              if (gotClockInGiftRes['code'] == "0"):
                 print(f'''【惊喜礼包】获得{gotClockInGiftRes['amount']}g💧''');
     if (clockInInit['themes'] and len(clockInInit['themes'])>0 ):
        print('开始今日签到领水滴')
        for item in clockInInit['themes']:
           if (item['hadGot']):
              print(f'''关注ID{item['id']}''')
              themeStep1=clockInFollowForFarm(item['id'],'theme',1)
              print(f'''themeStep1--结果{json.dumps(themeStep1)}''')
              
              if (themeStep1['code'] == "0"):
                 themeStep2=clockInFollowForFarm(item['id'],'theme',1)
                 print(f'''themeStep2--结果{json.dumps(themeStep2)}''')
                 if (themeStep2['code'] == "0"):
                    print(f'''关注{item['name']}，获得水滴{themeStep2['amount']}g''')
     
     if (clockInInit['venderCoupons'] and len(clockInInit['venderCoupons'])>0 ):
        print('限时领券领水滴')
        for item in clockInInit['venderCoupons']:
           if (item['hadGot']):
              print(f'''领券的ID{item['id']}''')
              venderCouponStep1=clockInFollowForFarm(item['id'],'venderCoupons',1)
              print(f'''venderCouponStep1--结果{json.dumps(venderCouponStep1)}''')
              
              if (venderCouponStep1['code'] == "0"):
                venderCouponStep2=clockInFollowForFarm(item['id'],'venderCoupons',2)
                venderCouponStep2=json.loads(requests.post(url,headers=headers).text)
                print(f'''venderCouponStep2--结果{json.dumps(venderCouponStep2)}''')
                if (venderCouponStep2['code'] == "0"):
                   print(f'''从${item['name']}领券，获得水滴${venderCouponStep2['amount']}g''')
   print('打卡领水活动（签到，关注，领券）结束✅\n')
       	
def duck():
   print('鸭子')
   for i in range(10):
       duckRes = getFullCollectionReward()
       if (duckRes['code'] == "0"):
          if (duckRes['hasLimit']):
              print(f'''【小鸭子游戏】{duckRes['title']}''')
          else:
              print(f'''{duckRes['title']}''')
              break
       elif (duckRes['code'] == "10"):
            print(f'''【小鸭子游戏】达到上限.''')
            break
      
      
def getAwardInviteFriend(farmInfo):
   print('获取邀请好友奖励')
   friendList= friendListInitForFarm()
   receiveFriendInvite(farmInfo)
   print(f'''\n今日已邀请好友{friendList['inviteFriendCount']}个 / 每日邀请上限${friendList['inviteFriendMax']}个''')
   if (friendList['inviteFriendCount'] > 0):
      if (friendList['inviteFriendCount']>friendList['inviteFriendGotAwardCount']):
         print('开始领取邀请好友的奖励');
         awardInviteFriendRes=awardInviteFriendForFarm()
         print(f'''领取邀请好友的奖励结果:{awardInviteFriendRes}''')
   else:
      print('今日未邀请过好友')
  
#领取额外奖励水滴
def getExtraAward():
   print('领取额外奖励水滴')
   masterHelpResult=masterHelpTaskInitForFarm()
   print(masterHelpResult)
   if (masterHelpResult['code'] == '0'):
      if (masterHelpResult['masterHelpPeoples'] and len(masterHelpResult['masterHelpPeoples']) >= 5):
      #已有五人助力。领取助力后的奖励
         if (masterHelpResult['masterGotFinal']):
            masterGotFinished=masterGotFinishedTaskForFarm()
            print(masterGotFinished)
            if (masterGotFinished['code'] == '0'):
              print(f'''已成功领取好友助力奖励：【{masterGotFinished['amount']}】g水''')

         else:
             print("已经领取过5好友助力额外奖励")

   else:
       print("【额外奖励】领取失败,原因：给您助力的人未达5个")

   if (masterHelpResult['masterHelpPeoples'] and len(masterHelpResult['masterHelpPeoples']) >= 0):
         str = ''
         jsonout=masterHelpResult['masterHelpPeoples']
         print(jsonout)
         #print(f'''京东昵称【${item.nickName || "匿名用户"}】 在 ${time} 给您助过力\n''')

   print('领取额外奖励水滴结束\n')
  

 
def doFriendsWater(waterFriendTaskInit):
   print(f'''开始给好友浇水...''')
   farmTask=taskInitForFarm()
   
   
   waterFriendCountKey=farmTask['waterFriendTaskInit']['waterFriendCountKey']
   waterFriendMax=farmTask['waterFriendTaskInit']['waterFriendMax']
   print(f'''今日已给{waterFriendCountKey}个好友浇水''')
   
   if (waterFriendCountKey < waterFriendMax):
      needWaterFriends = [];
      friendList = friendListInitForFarm()
      if (friendList['friends'] and len(friendList['friends'])> 0):
         #print('好友列表浇水',friendList)
         for item in friendList['friends']:
             if (item['friendState']== 1):
                if (len(needWaterFriends) < (waterFriendMax - waterFriendCountKey)):
                    needWaterFriends.append(item['shareCode'])
         print(f'''需要浇水的好友列表shareCodes:{needWaterFriends}''')
         waterFriendsCount = 0
         cardInfoStr = ''
         for index in range(len(needWaterFriends)):
            waterFriendForFarmRes=waterFriendForFarm(needWaterFriends[index])
            print(f'''为第{index+1}个好友浇水结果:{waterFriendForFarmRes}\n''')
            if (waterFriendForFarmRes['code']== '0'):
               waterFriendsCount +=1
               if json.dumps(waterFriendForFarmRes).find('cardInfo')>0:
                   print('为好友浇水获得道具了')
               if (waterFriendForFarmRes['cardInfo']['type']== 'beanCard'):
                   print(f'''获取道具卡:{waterFriendForFarmRes['cardInfo']['rule']}''');
                   cardInfoStr += '水滴换豆卡,'
               elif (waterFriendForFarmRes['cardInfo']['type'] =='fastCard'):
                   print(f'''获取道具卡:${waterFriendForFarmRes['cardInfo']['rule']}''')
                   cardInfoStr += '快速浇水卡,'
               elif (waterFriendForFarmRes['cardInfo']['type']== 'doubleCard'):
                   print(f'''获取道具卡:{waterFriendForFarmRes['cardInfo']['rule']}''')
                   cardInfoStr += '水滴翻倍卡,'
               elif (waterFriendForFarmRes['cardInfo']['type'] == 'signCard'):
                   print(f'''获取道具卡:{waterFriendForFarmRes['cardInfo']['rule']}''')
                   cardInfoStr += '加签卡,'
            elif (waterFriendForFarmRes['code']=='11'):
              print('水滴不够,跳出浇水')
       
      
         print(f'''【好友浇水】已给{waterFriendsCount}个好友浇水,消耗{waterFriendsCount * 10}g水\n''')
         if (cardInfoStr and len(cardInfoStr)> 0):
            print(f'''【好友浇水奖励】{cardInfoStr[0: len(cardInfoStr)-1]}\n''')
      else:
   	      print('您的好友列表暂无好友,快去邀请您的好友吧!')
   else:
       print(f'''今日已为好友浇水量已达{waterFriendMax}个''')
   
def gotThreeMealForFarm():
   print('正在进行定时领水任务')
   url=JD_API_HOST+f'''?functionId=gotThreeMealForFarm&appid=wh5&'''
   print('领水',url)
   response=requests.post(url,headers=headers)
   print(response.text)
   threeMeal = json.loads(response.text)
   if (threeMeal['code'] == "0"):
      print(f'''【定时领水】获得{threeMeal['amount']}g💧''');
   else:
      print(f'''【定时领水】结果:{json.dumps(threeMeal)}g''');





         
def getWaterFriendGotAward(farmTask):
   print('领取给3个好友浇水后的奖励水滴.....')
   
   waterFriendMax=farmTask['waterFriendTaskInit']['waterFriendMax']
   waterFriendSendWater=farmTask['waterFriendTaskInit']['waterFriendSendWater']
   waterFriendGotAward=farmTask['waterFriendTaskInit']['waterFriendGotAward']
   waterFriendCountKey=farmTask['waterFriendTaskInit']['waterFriendCountKey']
   print('最大浇水',waterFriendCountKey,waterFriendMax)
   if (waterFriendCountKey >= waterFriendMax):
     if (not waterFriendGotAward):
        waterFriendGotAwardRes=waterFriendGotAwardForFarm()
        print(f'''领取给{waterFriendMax}个好友浇水后的奖励水滴::{waterFriendGotAwardRes}''')
        if (waterFriendGotAwardRes['code']== '0'):
           print(f'''【给{waterFriendMax}好友浇水】奖励{waterFriendGotAwardRes['addWater']}g水滴\n''')
     else:
        print(f'''给好友浇水的{waterFriendSendWater}g水滴奖励已领取\n''')

   else:
      print(f'''暂未给{waterFriendMax}个好友浇水\n''')
  



def predictionFruit():
   msg='预测水果成熟时间\n'
   print(msg)
   
   farmTask=taskInitForFarm()
   farmInfo=initForFarm()
   #print(farmInfo)
   if (farmInfo['code']!='0'):
     print('获取农场数据错误')
     return 
   
   waterEveryDayT =farmTask['totalWaterTaskInit']['totalWaterTaskTimes'];
    #今天到到目前为止，浇了多少次水
   msg += f'''【今日共浇水】{waterEveryDayT}次\n'''
   msg += f'''【剩余 水滴】{farmInfo['farmUserPro']['totalEnergy']}g💧\n'''
   msg += f'''【水果🍉进度】{round(((farmInfo['farmUserPro']['treeEnergy'] / farmInfo['farmUserPro']['treeTotalEnergy']) * 100),2)}%，果树已获取{farmInfo['farmUserPro']['treeEnergy']}能量,还需{(farmInfo['farmUserPro']['treeTotalEnergy'] - farmInfo['farmUserPro']['treeEnergy'])}能量\n'''
   
   
   

   
   
   if (farmInfo['toFlowTimes'] > (farmInfo['farmUserPro']['treeEnergy']/10)):
       msg += f'''【开花进度】再浇水{farmInfo['toFlowTimes'] - farmInfo['farmUserPro']['treeEnergy'] / 10}次开花\n'''
   elif (farmInfo['toFruitTimes'] > (farmInfo['farmUserPro']['treeEnergy']/ 10)):
        msg +=f'''【结果进度】再浇水{farmInfo['toFruitTimes'] -farmInfo['farmUserPro']['treeEnergy'] / 10}次结果\n'''
  
  #预测n天后水果课可兑换功能
   waterTotalT = (farmInfo['farmUserPro']['treeTotalEnergy'] - farmInfo['farmUserPro']['treeEnergy']- farmInfo['farmUserPro']['totalEnergy']) / 10
      #一共还需浇多少次水
   if (waterEveryDayT>0):
      waterD = math.ceil(waterTotalT / waterEveryDayT)
   else:
    	 waterD=0
   if waterD == 1:
  	  tm='明天'
   elif waterD == 2:
  	  tm='后天'
   else:
  	  tm=waterD
   seconds = 24 * 60 * 60  * waterD + time.time()
   timeArray = time.localtime(seconds)
   pretime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
   msg += f'''【预测】{tm}天之后({pretime}日)可兑换水果🍉'''
   loger(msg)



def executeWaterRains(farmTask):
   print('水滴鱼任务')
   executeWaterRain =not farmTask['waterRainInit']['f']
   print(f'''水滴雨任务，每天两次，最多可得10g水滴,完成?{executeWaterRain}''')
   if (executeWaterRain) :
      
      if (farmTask['waterRainInit']['lastTime']):
         if (time.time() < (farmTask['waterRainInit']['lastTime']+ 3 * 60 * 60 * 1000)) :
            executeWaterRain = False;
            ft=float(farmTask['waterRainInit']['lastTime']/1000)
            timeArray=time.localtime(ft + 3 * 60 * 60 * 1000)
            hopetime=time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            print(f'''【第{farmTask['waterRainInit']['winTimes']+ 1}次水滴雨】未到时间，请{hopetime}再试\n''')
      if (executeWaterRain):
          print(f'''开始水滴雨任务,这是第{farmTask['waterRainInit']['winTimes'] + 1}次，剩余{2 - (farmTask['waterRainInit']['winTimes']+ 1)}次''')
          waterRain= waterRainForFarm()
          print('水滴雨waterRain')
          if (waterRain['code'] == '0'):
             print(f'''水滴雨任务执行成功，获得水滴： {waterRain['addEnergy']} g''')
        
             print(f'''【第{farmTask['waterRainInit']['winTimes'] + 1}次水滴雨】获得{waterRain['addEnergy']}g水滴\n''')






def taskInitForFarm():
   try:   
     farmTask=iosrule(sys._getframe().f_code.co_name)
     #print('初始化农场',farmTask)
     return farmTask
   except Exception as e:
      print("初始化农场任务:", str(e))
      time.sleep(5)
      taskInitForFarm()
      
def initForFarm():
   url=JD_API_HOST+'?functionId=initForFarm&appid=wh5'
   body=f'&body={urllib.parse.quote(json.dumps({"version":4}))}&appid=wh5&clientVersion=9.1.0'
   sheaders= headers
   sheaders["Content-Type"]= "application/x-www-form-urlencoded"
   try:
      farmInfo=json.loads(requests.post(url,headers=headers).text)
      #print('初始化农场🐮',farmInfo)
      return farmInfo
   except Exception as e:
      print("初始化农场错误:", str(e))
      time.sleep(5)
      initForFarm()
      
def clockInInitForFarm():
   clockInInit=iosrule(sys._getframe().f_code.co_name)
     #print('打卡领水API',farmTask)
   return clockInInit
def clockInForFarm():
   clockInForFarmRes=iosrule(sys._getframe().f_code.co_name,{"type": 1})
     #print('连续签到API',farmTask)
   return clockInForFarmRes
   
def gotClockInGift():
   gotClockInGiftRes=iosrule(sys._getframe().f_code.co_name,{"type": 2})
     #print('领取连续签到7天的惊喜礼包API',farmTask)
   return gotClockInGiftRes
def masterGotFinishedTaskForFarm():
   masterGotFinished=iosrule(sys._getframe().f_code.co_name)
     #print('领取连续签到7天的惊喜礼包API',farmTask)
   return masterGotFinished
   
   
def browseAdTaskForFarm(advertId, type):
   body={'advertId':advertId, 'type':type}
   browseResult=iosrule(sys._getframe().f_code.co_name,body)
     #print('签到API',farmTask)
   return browseResult
   
   
def signForFarm():
   signResult=iosrule(sys._getframe().f_code.co_name)
     #print('签到API',farmTask)
   return signResult
def waterFriendForFarm(shareCode):
   body ={"shareCode": shareCode, "version": 6, "channel": 1}
   waterFriendForFarmRes=iosrule(sys._getframe().f_code.co_name,body)
     #print('初始化waterFriendForFarm任务',farmTask)
   return waterFriendForFarmRes
   
def gotWaterGoalTaskForFarm():
   goalResult=iosrule(sys._getframe().f_code.co_name,body,{'type': 3})
     #print('初始化任务',farmTask)
   return goalResult
	
def waterRainForFarm():
   body = {"type": 1, "hongBaoTimes": 100, "version": 3}
   waterRain=iosrule(sys._getframe().f_code.co_name,body)
     #print('初始化任务',farmTask)
   return waterRain

def waterGoodForFarm():
   waterResult=iosrule(sys._getframe().f_code.co_name)
     #print('初始化任务',farmTask)
   return waterResult

def myCardInfoForFarm():
   body={"version": 5, "channel": 1}
   myCardInfoRes=iosrule(sys._getframe().f_code.co_name,body)
   return myCardInfoRes

def totalWaterTaskForFarm():
   totalWaterReward=iosrule(sys._getframe().f_code.co_name)
     #print('初始化任务',farmTask)
   return totalWaterReward

def firstWaterTaskForFarm():
   firstWaterReward=iosrule(sys._getframe().f_code.co_name)
   return firstWaterReward

def waterFriendGotAwardForFarm():
   firstWaterReward=iosrule(sys._getframe().f_code.co_name)
   return firstWaterReward
   
def userMyCardForFarm(cardType):
   body={"cardType": cardType}
   #使用道具卡API
   userMyCardRes=iosrule(sys._getframe().f_code.co_name,body)
   return userMyCardRes

def gotStageAwardForFarm(type):
   gotStageAwardForFarmRes=iosrule(sys._getframe().f_code.co_name, {'type': type})
   return gotStageAwardForFarmRes
   
def browserForTurntableFarm(type, adId):
   if (type ==1):
     print('浏览爆品会场')
   if (type == 2):
     print('天天抽奖浏览任务领取水滴');
   body = {"type": type,"adId": adId,"version":4,"channel":1};
   browserForTurntableFarmRes=iosrule(sys._getframe().f_code.co_name,body)
   return browserForTurntableFarmRes
  #浏览爆品会场8秒

#天天抽奖浏览任务领取水滴API
def browserForTurntableFarm2(type):
   body = {"type":2,"adId": type,"version":4,"channel":1};
   browserForTurntableFarm2Res=iosrule('browserForTurntableFarm',body)
   return browserForTurntableFarm2Res


def lotteryMasterHelp(code):
   body={
    'imageUrl': "",
    'nickName': "",
    'shareCode': code + '-3',
    'babelChannel': "3",
    'version': 4,
    'channel': 1
    }
   lotteryMasterHelpRes=iosrule('initForFarm',body)
   return lotteryMasterHelpRes
   

def clockInFollowForFarm(id, type, step):
   bd= {'id':id,'type':type,'step':step}
   res=iosrule(sys._getframe().f_code.co_name,body)
   return res
def getFullCollectionReward():
   body={"type": 2, "version": 6, "channel": 2}
   duckRes=iosrule(sys._getframe().f_code.co_name,body)
   return duckRes
#初始化集卡抽奖活动数据API
def initForTurntableFarm():
   body={'version': 4, 'channel': 1}
   initForTurntableFarmRes=iosrule(sys._getframe().f_code.co_name,body)
   return initForTurntableFarmRes
 

def lotteryForTurntableFarm() :
   time.sleep(5)
   print('等待了5秒')
   body={'type': 1, 'version': 4, 'channel': 1}
   lotteryRes =iosrule(sys._getframe().f_code.co_name,body)
   return lotteryRes
 

def timingAwardForTurntableFarm():
   body={'version': 4, 'channel': 1}
   timingAwardRes =iosrule(sys._getframe().f_code.co_name,body)
   return timingAwardRes



def receiveFriendInvite(farmInfo):
   print('接收好友邀请')
   newShareCodes=shareCodesFormat()
   for code in newShareCodes:
      if (code ==farmInfo['farmUserPro']['shareCode']) :
         print('自己不能邀请自己成为好友噢\n')
         continue
      inviteFriendRes= inviteFriend(code)
      print(f'''接收邀请成为好友结果:{inviteFriendRes['helpResult']}''')
      if inviteFriendRes['helpResult']['code'] == '0':
          print(f'''您已成为{inviteFriendRes['helpResult']['masterUserInfo']['nickName']}的好友''')
      elif (inviteFriendRes['helpResult']['code'] == '17') :
          print('对方已是您的好友')
      elif (inviteFriendRes['helpResult']['code'] == '5') :
      	  print('返回code=5，状态未知道')
    
  
	
def friendListInitForFarm():
   body={"version": 4, "channel": 1}
   friendList=iosrule(sys._getframe().f_code.co_name,body)
   return friendList
def awardInviteFriendForFarm():
   awardInviteFriendRes=iosrule(sys._getframe().f_code.co_name)
   return awardInviteFriendRes
   
def masterHelpTaskInitForFarm():
   masterHelpResult=iosrule(sys._getframe().f_code.co_name)
   return masterHelpResult
    
def masterHelp(code):
   body={
    'imageUrl': "",
    'nickName': "",
    'shareCode': code,
    'babelChannel': "3",
    'version': 2,
    'channel': 1
    }
   helpResult=iosrule('initForFarm',body)
   return helpResult


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
        newShareCodes =Defalt_ShareCode
            
   print(f'''京东账号将要助力的好友{newShareCodes}''')
   return newShareCodes
     
def iosrule(mod,body={}):
   url=JD_API_HOST+f'''?functionId={mod}&appid=wh5&body={urllib.parse.quote(json.dumps(body))}'''
   try:
     return json.loads(requests.get(url,headers=headers).text)
   except Exception as e:
      print(f'''初始化{mode}任务:''', str(e))
      
      
def check():
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   global djj_djj_cookie
   global djj_bark_cookie
   global djj_sharecode
   if "DJJ_SHARECODE" in os.environ:
     djj_sharecode = os.environ["DJJ_SHARECODE"]
   if "DJJ_BARK_COOKIE" in os.environ:
     djj_bark_cookie = os.environ["DJJ_BARK_COOKIE"]
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
   jdFruit()
   predictionFruit()
   pushmsg('京东农场',result)
   
   
   
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
     print(count)
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
