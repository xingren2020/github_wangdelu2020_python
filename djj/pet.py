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


djj_djj_cookie=''
djj_sharecode=''
djj_bark_cookie=''
djj_sever_jiang=''










#以上参数需要远程设置，以下为默认参数
JD_API_HOST = 'https://api.m.jd.com/client.action'
headers={
      'UserAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
}
cookiesList=[]
Defalt_ShareCode= ['MTAxODExNDYxMTEwMDAwMDAwMzk4NzYxOTc=','MTAxODExNDYxMTEwMDAwMDAwNDA1NDQwNzE=']#读取参数djj_sharecode为空，开始读取默认参数

codeurl='http://api.turinglabs.net/api/v1/jd/pet/read/'
randomCount = 20
newShareCodes=[]

index=0
def jfPey():
   initPetTownRes=iosrule('initPetTown')
   print(initPetTownRes)
   if (initPetTownRes['code']== '0' and initPetTownRes['resultCode'] == '0' and initPetTownRes['message'] == 'success'):
      petInfo = initPetTownRes['result']
      if (petInfo['userStatus'] ==0):
         print('【提示】此账号萌宠活动未开始，请手动去京东APP开启活动\n入口：我的->游戏与互动->查看更多')
         return
      if (petInfo['petStatus'] == 5 and petInfo['showHongBaoExchangePop']):

          slaveHelp()#可以兑换而没有去兑换,也能继续助力好友
          print(f'''【提醒⏰】{petInfo['goodsInfo']['goodsName']}已可领取, 请去京东APP或微信小程序查看''')
        # print(f'''账号${index} - {nickName||UserName}奖品{petInfo['goodsInfo']['goodsName']'}已可领取''')
          return
      print(f'''\n【您的互助码shareCode】 {petInfo['shareCode']}\n''')
      taskInitRes=taskInit()
      print(taskInitRes)
      if (taskInitRes['resultCode'] == '9999') or (not taskInitRes['result']):
           print('初始化任务异常, 请稍后再试')
           return
      taskInfo = taskInitRes['result']
      petSport()#遛弯
      slaveHelp()#助力好友
      masterHelpInit()#获取助力的信息
      doTask(taskInfo,petInfo)#做日常任务
      feedPetsAgain()#再次投食
      energyCollect(petInfo)#收集好感度

   elif (initPetTownRes['code'] =='0'):
        print(f'''初始化萌宠失败:{initPetTownRes['message']}''')
 

'''
 * 助力好友, 暂时支持一个好友, 需要拿到shareCode
 * shareCode为你要助力的好友的
 * 运行脚本时你自己的shareCode会在控制台输出, 可以将其分享给他人
 '''
# 收取所有好感度
def energyCollect(petInfo):
   print('开始收取任务奖励好感度')
   response =iosrule(sys._getframe().f_code.co_name)
   print(response)
   if (response['code'] == '0'):
      message = f'''【第{response['result']['medalNum'] + 1}块勋章完成进度】{response['result']['medalPercent']}%，还需收集{response['result']['needCollectEnergy']}好感\n'''
      message += f'''【已获得勋章】{response['result']['medalNum']}块，还需收集{response['result']['needCollectMedalNum']}块即可兑换奖品{petInfo['goodsInfo']['goodsName']}\n'''
      print(message)
      pushmsg('jdpet',message)
#再次投食
def feedPetsAgain():
   #再次初始化萌宠
   response =iosrule('initPetTown')
   if (response['code'] == '0' and response['resultCode'] == '0' and response['message'] == 'success'):
      petInfo = response['result']
      foodAmount = petInfo['foodAmount']#剩余狗粮
      if (foodAmount - 100 >= 10):
         for  i in range(int((foodAmount - 100) / 10)):
              feedPetRes = iosrule('feedPets')
              print(f'''`投食{feedPetRes}''')
              if (feedPetRes['resultCode']== 0 and feedPetRes['code'] == 0):
                 print('投食成功')
        
                 response2=iosrule('initPetTown')
                 petInfo = response2['result']
                 subTitle = petInfo['goodsInfo']['goodsName']
      else :
          print(f'''目前剩余狗粮：【{foodAmount}】g,不再继续投食,保留部分狗粮用于完成第二天任务''')
          subTitle = petInfo['goodsInfo']['goodsName']

   else:
       print(f'''初始化萌宠失败:  {petInfo}''')

 
# 遛狗, 每天次数上限10次, 随机给狗粮, 每次遛狗结束需调用getSportReward领取奖励, 才能进行下一次遛狗
def petSport():
  print('开始遛弯')
  times = 1
  code = 0
  resultCode = 0
  for times in range(1,11):
    if (resultCode == 0 and code == 0):
      response=iosrule(sys._getframe().f_code.co_name)
      print(f'''第{times}次遛狗完成: {response}''')
      resultCode = response['resultCode']
      if (resultCode == 0):
         sportRevardResult = iosrule('getSportReward')
         print(f'''领取遛狗奖励完成: {sportRevardResult}''')
         times+=1
  
  if (times > 1):
      print('【十次遛狗】已完成\n')

def slaveHelp():
   helpPeoples = ''
   message=''
   print(f'''开始助力京东账号{newShareCodes}''')
   for code in newShareCodes:
      if (not code):
         continue
      response=iosrule(sys._getframe().f_code.co_name,{'shareCode': code})
      if (response['code']== '0' and response['resultCode'] == '0'):
         if (response['result']['helpStatus'] == 0):
            print(f'''已给好友: 【{response['result']['masterNickName']} 】助力''');
            helpPeoples += response['result']['masterNickName']+','
         elif (response['result']['helpStatus'] == 1):
        #您今日已无助力机会
            print(f'''助力好友{response['result']['masterNickName']}失败，您今日已无助力机会''')
            break
         elif (response['result']['helpStatus'] == 2):
        #该好友已满5人助力，无需您再次助力
           print(f'''该好友{response['result']['masterNickName']}已满5人助力，无需您再次助力''')
         else:
           print(f'''助力其他情况：{response}''')
      else:
          print(f'''助理好友结果: {response['message']}''')
   if (helpPeoples and len(helpPeoples)> 0):
       message += f'''【您助力的好友】{helpPeoples[0:len(helpPeoples)]}\n'''
       
def masterHelpInit():
   res = iosrule(sys._getframe().f_code.co_name)
   message=''
   print(f'''助力信息: {res}''');
   if (res['code'] == '0' and res['resultCode'] == '0'):
      if res['result']['masterHelpPeoples'] and len(res['result']['masterHelpPeoples'])>= 5:
         if(not res['result']['addedBonusFlag']):
            print("开始领取额外奖励")
            getHelpAddedBonusResult =iosrule('getHelpAddedBonus')
            print(getHelpAddedBonusResult)
            print(f'''领取30g额外奖励结果：【{getHelpAddedBonusResult['message']}】''')
            message += f'''【额外奖励{getHelpAddedBonusResult['result']['reward']}领取】{getHelpAddedBonusResult['message']}'''
         else:
           print("已经领取过5好友助力额外奖励")
           message += '【额外奖励】已领取\n'
      else:
        print("助力好友未达到5个")
        message += '【额外奖励】领取失败，原因：给您助力的人未达5个\n'
      if (res['result']['masterHelpPeoples'] and len(res['result']['masterHelpPeoples']) > 0):
          print('帮您助力的好友的名单开始')
          str = ''
          for index in res['result']['masterHelpPeoples']:
              str += index['nickName']+','

          message += f'''【助力您的好友】{str}'''
          print(message)
def doTask(taskInfo,petInfo):
   print('做任务')
   print(taskInfo)
   taskListobj=['signInit', 'threeMealInit', 'firstFeedInit', 'feedReachInit', 'inviteFriendsInit','browseSingleShopInit','browseSingleShopInit1']
   print(taskListobj)
   for  item in taskListobj:
      if (taskInfo[item]['finished']):
          print(f'''任务 {item} 已完成✅''')
      else:
          print(f'''任务 {item} 未完成❎''')
   if (taskInfo[taskListobj[0]] and not taskInfo[taskListobj[0]]['finished']):
       getSignReward()

   if (taskInfo[taskListobj[2]] and not taskInfo[taskListobj[2]]['finished']):
       firstFeedInitFun()
     #投食10次
   if (taskInfo[taskListobj[3]] and not taskInfo[taskListobj[3]]['finished']):
      feedReachInitFun(taskInfo)
   if (taskInfo[taskListobj[1]] and not taskInfo[taskListobj[1]]['finished']):
      if (taskInfo[taskListobj[1]]['timeRange']== -1) :
          print('未到三餐时间')
          return 
      getThreeMealReward()
   if (taskInfo[taskListobj[5]] and not taskInfo[taskListobj[5]]['finished']):
       browseShopsInitFun()
   browseSingleShopInitList = [];
   for item in taskListobj:
      if (json.dumps(taskInfo[item]).find('browseSingleShopInit') >0):
          browseSingleShopInitList.append(item)
    
  # 去逛逛好货会场
   for item in browseSingleShopInitList:
      browseSingleShopInitTask = taskInfo[item]
      if (browseSingleShopInitTask and not browseSingleShopInitTask['finished']):
        browseSingleShopInit(browseSingleShopInitTask)

   if (taskInfo[taskListobj[4]] and not taskInfo[taskListobj[4]]['finished']):
        inviteFriendsInitFun(taskInfo)
 
  

  
def getSignReward():
   print('准备每日签到')
   response=iosrule(sys._getframe().f_code.co_name)
   print(f'''每日签到结果: {response}''')
   if (response['code']== '0' and response['resultCode']== '0'):
       print(f'''【每日签到成功】奖励{response['result']['signReward']}g狗粮\n''')
   else:
        print(f'''【每日签到】{response['message']}\n''')
 

def getThreeMealReward():
   print('准备三餐签到')
   response=response=iosrule(sys._getframe().f_code.co_name)
   print(f'''三餐签到结果: {response}''');
   if (response['code'] == '0' and response['resultCode'] == '0'):
      print(f'''【定时领狗粮】获得{response['result']['threeMealReward']}g\n''')
   else:
      print(f'''【定时领狗粮】{response['message']}\n''');


#浏览指定店铺 任务
def browseSingleShopInit(item):
   print(f'''开始做 {item['title']} 任务， {item['desc']}''')
   body1 = {"index": item['index'], "version":1, "type":1};
   body2 = {"index": item['index'], "version":1, "type":2};
   response1= iosrule("getSingleShopReward", body1);
   print(f'''点击进去response1:{response1}''')
   if (response1['code'] == '0' and response1['resultCode'] == '0'):
      response2 = iosrule("getSingleShopReward", body2);
      if (response2['code'] == '0' and response2['resultCode'] == '0'):
          print(f'''【浏览指定店铺】获取{response2['result']['reward']}g\n''')
   

#浏览店铺任务, 任务可能为多个? 目前只有一个
def browseShopsInitFun():
   print('开始浏览店铺任务')
   times = 0
   resultCode = 0
   code = 0
   for times in range(5):
     if (resultCode == 0 and code == 0 and times < 5):
       response=iosrule("getBrowseShopsReward")
       print(f'''第{times}次浏览店铺结果: {response}''')
       code = response['code']
       resultCode = response['resultCode']
       times+=1
   print('浏览店铺任务结束')

#首次投食 任务
def firstFeedInitFun():
  print('首次投食任务合并到10次喂食任务中\n')
#邀请新用户
def inviteFriendsInitFun(taskInfo):
   print('邀请新用户功能未实现')
   if (taskInfo['inviteFriendsInit']['status'] == 1 and taskInfo['inviteFriendsInit']['inviteFriendsNum']> 0):
    #如果有邀请过新用户,自动领取60gg奖励
      res = iosrule('getInviteFriendsReward')
      if (res['code'] == 0 and res['resultCode'] == 0):
          print(f'''领取邀请新用户奖励成功,获得狗粮现有狗粮{taskInfo['inviteFriendsInit']['reward']}g，{res['result']['foodAmount']}g''')
          message = f'''【邀请新用户】获取狗粮{taskInfo['inviteFriendsInit']['reward']}g\n'''

def feedReachInitFun(taskInfo):
   print('投食任务开始...')
   finishedTimes = taskInfo['feedReachInit']['hadFeedAmount']/10 #已经喂养了几次
   needFeedTimes = 10 - finishedTimes#//还需要几次
   tryTimes = 20#尝试次数
   for needFeedTimes in range(20):
      if (needFeedTimes > 0 and tryTimes > 0):
          response = iosrule('feedPets')
          print(f'''本次投食结果: {response}''')
          time.sleep(3)
          if (response['resultCode'] == 0 and response['code'] == 0):
              needFeedTimes-=1
          print(f'''`还需要投食{needFeedTimes}次''')
          if (response['resultCode'] == 3003 and response['code'] == 0):
              print('剩余狗粮不足, 投食结束');
              needFeedTimes = 0
              break
          tryTimes-=1
   print('投食任务结束...\n')




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
   readShareCodeRes = readShareCode();
   #print(readShareCodeRes)
   if (readShareCodeRes and readShareCodeRes['code'] == 200):
            #print(readShareCodeRes['data'])
        newShareCodes=Defalt_ShareCode+readShareCodeRes['data']
            
   print(f'''京东账号将要助力的好友{newShareCodes}''')
   return newShareCodes
   
def taskInit():
   taskInitRes=iosrule(sys._getframe().f_code.co_name,{"version":1})
   return taskInitRes
	
def iosrule(mod,body={}):
   url=f'''{JD_API_HOST}?functionId={mod}&appid=wh5&loginWQBiz=pet-town&body={urllib.parse.quote(json.dumps(body))}'''
   try:
     return json.loads(requests.get(url,headers=headers).text)
   except Exception as e:
      print(f'''初始化{mode}任务:''', st(e))

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
    #print(response.text)
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
       #print(ckresult)
       if json.dumps(ckresult).find(checkck)>0:
           signmd5=True
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
   
def Pet_main():
   global newShareCodes
   newShareCodes= shareCodesFormat()
   jfPey()
   
   
   
   
   
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
   index=0
   for count in cookiesList:
     index+=1
     #if index!=1:
       #continue
     oldstr = count.split(';')
     for i in oldstr:
       if i.find('pin=')>=0:
          newstr=i.strip()[i.find('pin=')+4:len(i)]
          print(f'''>>>>>>>>>【账号{str(index)}开始】{newstr}''')
     headers['Cookie']=count
     if(TotalBean(count,newstr)):
         Pet_main()
def main_handler(event, context):
    return start()
    

if __name__ == '__main__':
       start()
