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
osenviron={}

djj_djj_cookie=''
djj_xfj_headers=''
djj_bark_cookie=''
djj_sever_jiang=''
#删除
result=''
JD_API_HOST = 'https://wq.jd.com/activep3/family/'

def JD_lotteryTask():
   print('family_query\n')
   try:
      url='https://api.m.jd.com/client.action?appid=vip_h5&functionId=vvipclub_lotteryTask&body=%7B%22info%22%3A%22browseTask%22%2C%22withItem%22%3Atrue%7D&_=1606749660668'
      response=requests.get(url,headers=djj_xfj_headers)
      print(response.text)
   except Exception as e:
      print(f'''shaking:''', str(e))

def JD_doTask():
   print('doTask\n')
   try:
      JD_TaSkall()
      JR_TaSkall()
      TotalSubsidy()
      TotalSteel()
      TotalRed()
      TotalMoney()
   except Exception as e:
      print(str(e))
      
     
def JR_TaSkall():
   JR_Rebates()
   JR_Steel()
   JR_DoubleSign()
   JRJT_Checkin()
   JRJT_DoubleSign()
   JR_LuckyLottery()



def JD_TaSkall():
   JD_BeanSign()
   JD_Turn()
   JD_shaking()
   JD_Overseas()
   JD_GetCash()
   JD_Webcasts()
   JD_TakeaLook()
   JD_supermarket()
   JD_SecKilling()



     



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


def JD_shaking():
   print('shaking check!\n')
   try:
      Boxurl='https://api.m.jd.com/client.action?appid=vip_h5&functionId=vvipclub_luckyBox&body=%7B%22info%22%3A%22freeTimes%2Ctitle%2CbeanNum%2CuseBeanNum%2CimgUrl%22%7D&_=1606750872421'
      Skurl='https://api.m.jd.com/client.action?appid=vip_h5&functionId=vvipclub_shaking&body=%7B%22type%22%3A%220%22%2C%22riskInfo%22%3A%7B%22platform%22%3A1%2C%22pageClickKey%22%3A%22MJDVip_Shake%22%2C%22eid%22%3A%22VZQF7EIYQYJKPQIU74AIOBJKF22UDNSMT2QQQIVURYAKF2YBHTAU5JRQZUGGQPWAF4LTR3A2MZBK4OXQOZXHLJF4IM%22%2C%22fp%22%3A%227d1fc40cdff80d605c1d405f78d83777%22%2C%22shshshfp%22%3A%223b1613341e6ac359c7338792b3676ed4%22%2C%22shshshfpa%22%3A%22b21c2188-a9ee-0c7a-96bb-bffd77e6f997-1605501503%22%2C%22shshshfpb%22%3A%22lMdmIvIIK9Nt7SkcQGnFQ9Q%3D%3D%22%7D%7D&_=1606748482455'
      response=requests.get(Boxurl,headers=djj_xfj_headers)
      print(response.text)
      Boxres=json.loads(response.text)
      print(Boxres['data']['freeTimes'])
      if(Boxres['success']==True):
         
         if(Boxres['data']['freeTimes']>0):
            print('shaking go')
            response=requests.get(Skurl,headers=djj_xfj_headers)
            print(response.text)
            Shakres=json.loads(response.text)
            if(Shakres['success']==True):
                LFtimes=f'''剩余免费{Shakres['data']['luckyBox']['freeTimes']}次----总京豆{Shakres['data']['luckyBox']['totalBeanCount']}'''
                print(LFtimes)
         else:
             print('免费次数用完')
      else:
          print('摇豆子获取数据错误')
   except Exception as e:
      print(f'''shaking:''', str(e))


#====================================================
    
def JD_BeanSign():
   try:
     print('\n京东商城-京豆签到')
     body='functionId=signBeanIndex&appid=ld'
     response=requests.post('https://api.m.jd.com/client.action',headers=djj_xfj_headers,data=body)
     res=response.text
     print(res)
     return res
   except Exception as e:
      print(str(e))

def JD_Turn():
   try:
     print('\n京东商城-转盘查询')
     response=requests.post('https://api.m.jd.com/client.action?functionId=wheelSurfIndex&body=%7B%22actId%22%3A%22jgpqtzjhvaoym%22%2C%22appSource%22%3A%22jdhome%22%7D&appid=ld',headers=djj_xfj_headers)
     res=json.loads(response.text)
     #print(res)
     if res['code']=='0':
       if int(res['data']['lotteryCount'])>0:
          code=res['data']['lotteryCode']
          time.sleep(2)
          JD_TurnSign(code)
       else:
       	print('次数为0')
   except Exception as e:
      print(str(e))
def JD_TurnSign(code):
   try:
     print('\n京东商城-转盘签到')
     response=requests.post(f'''https://api.m.jd.com/client.action?functionId=lotteryDraw&body=%7B%22actId%22%3A%22jgpqtzjhvaoym%22%2C%22appSource%22%3A%22jdhome%22%2C%22lotteryCode%22%3A%22{code}%22%7D&appid=ld''',headers=djj_xfj_headers)
     res=response.text
     print(res)
   except Exception as e:
      print(str(e))

def JD_Overseas():
   try:
     print('\n京东商城-国际签到')
     body="body=%7B%7D&build=167237&client=apple&clientVersion=9.0.0&openudid=1fce88cd05c42fe2b054e846f11bdf33f016d676&partner=apple&scope=11&sign=e27f8b904040a0e3c99b87fc27e09c87&st=1591730990449&sv=101"
     response=requests.post('https://api.m.jd.com/client.action?functionId=checkin',headers=djj_xfj_headers,data=body)
     res=response.text
     print(res)
   except Exception as e:
      print(str(e))
      
      
def JD_GetCash():
   try:
     print('\n京东商城-现金签到')
     response=requests.post('https://api.m.jd.com/client.action?functionId=cash_sign&body=%7B%22remind%22%3A0%2C%22inviteCode%22%3A%22%22%2C%22type%22%3A0%2C%22breakReward%22%3A0%7D&client=apple&clientVersion=9.0.8&openudid=1fce88cd05c42fe2b054e846f11bdf33f016d676&sign=7e2f8bcec13978a691567257af4fdce9&st=1596954745073&sv=111',headers=djj_xfj_headers)
     res=response.text
     print(res)
   except Exception as e:
      print(str(e))
def JD_Webcasts():
   try:
     print('\n京东商城-直播签到')
     headers=djj_xfj_headers
     headers['Origin']='https://h.m.jd.com'
     response=requests.get('https://api.m.jd.com/api?functionId=getChannelTaskRewardToM&appid=h5-live&body=%7B%22type%22%3A%22signTask%22%2C%22itemId%22%3A%221%22%7D',headers=headers)
     res=response.text
     print(res)
   except Exception as e:
      print(str(e))
def JD_TakeaLook():
   try:
     print('\n京东发现-看看签到')
     response=requests.get('https://api.m.jd.com/client.action?functionId=discTaskList&body=%7B%22bizType%22%3A1%2C%22referPageId%22%3A%22discRecommend%22%7D&client=apple&clientVersion=9.1.6&openudid=1fce88cd05c42fe2b054e846f11bdf33f016d676&sign=17061147fe8e0eb10edfe8d9968b6d66&st=1601138337675&sv=102',headers=djj_xfj_headers)
     res=response.text
     print(res)
   except Exception as e:
      print(str(e))
def JD_supermarket():
   try:
     print('\n京东-超市签到')
     response=requests.get('https://api.m.jd.com/api?appid=jdsupermarket&functionId=smtg_sign&clientVersion=8.0.0&client=m&body=%7B%7D',headers=djj_xfj_headers)
     res=response.text
     print(res)
   except Exception as e:
      print(str(e))
def JD_SecKilling():
   try:
     print('\n京东秒杀-红包查询')
     headers={}
     headers['Origin']='https://h5.m.jd.com'
     headers['Content-Type']='application/x-www-form-urlencoded'
     headers['Cookie'] =djj_xfj_headers['Cookie']
     body='functionId=freshManHomePage&body=%7B%7D&client=wh5&appid=SecKill2020'
     response=requests.post('https://api.m.jd.com/client.action',headers=headers,data=body)
     res=json.loads(response.text)
     print(res)
     if not (res['code'] == 203 or res['code'] == 3 or res['code'] == 101):
       projectId=res['result']['projectId']
       taskId=res['result']['taskId']
       print('\n京东秒杀-红包签到')
       body=f'''functionId=doInteractiveAssignment&body=%7B%22encryptProjectId%22%3A%22{projectId}%22%2C%22encryptAssignmentId%22%3A%22{taskId}%22%2C%22completionFlag%22%3Atrue%7D&client=wh5&appid=SecKill2020'''
       print(body)
       response=requests.post('https://api.m.jd.com/client.action',headers=headers,data=body)
       res=response.text
       print(res)
   except Exception as e:
      print(str(e))



#====================================================
def JR_Rebates():
   try:
     print('\n金融金币乐园')
     headers=djj_xfj_headers
     headers['Referer']= 'https://member.jr.jd.com/gcmall/?channel=01-qddlq-201010'
     response=requests.get('https://ms.jr.jd.com/gw/generic/hy/h5/m/receiveRebates?reqData=%7B%22version%22:%221.0%22,%22channel%22:%22%22,%22timeStamp%22:1606817564072%7D',headers=headers)
     res=response.text
     print(res)
     return res
   except Exception as e:
      print(str(e))
def JRJT_Checkin():
   try:
     print('\n京东金融-金贴签到')
     body='reqData=%7B%22channelCode%22%3A%22ZHUANQIAN%22%2C%22clientType%22%3A%22sms%22%2C%22clientVersion%22%3A%2211.0%22%7D'
     response=requests.post('https://ms.jr.jd.com/gw/generic/zc/h5/m/openScreenReward',headers=djj_xfj_headers,data=body)
     res=response.text
     print(res)
   except Exception as e:
      print(str(e))
def JR_Steel():
   try:
     print('\n京东金融-钢镚签到')
     body='reqData=%7B%22channelSource%22%3A%22JRAPP%22%2C%22riskDeviceParam%22%3A%22%7B%7D%22%7D'
     response=requests.post('https://ms.jr.jd.com/gw/generic/gry/h5/m/signIn',headers=djj_xfj_headers,data=body)
     res=response.text
     print(res)
   except Exception as e:
      print(str(e))
def JR_DoubleSign():
   try:
     print('\n京东金融-双签')
     body='reqData=%7B%22actCode%22%3A%22FBBFEC496C%22%2C%22type%22%3A3%2C%22riskDeviceParam%22%3A%22%22%7D'
     response=requests.post('https://nu.jr.jd.com/gw/generic/jrm/h5/m/process?',headers=djj_xfj_headers,data=body)
     res=response.text
     print(res)
   except Exception as e:
      print(str(e))
      
      


def JR_Redsign():
   try:
     print('\n京东金融-红包签到')
     body='body=%7B%22pageClickKey%22%3A%22CouponCenter%22%2C%22eid%22%3A%22O5X6JYMZTXIEX4VBCBWEM5PTIZV6HXH7M3AI75EABM5GBZYVQKRGQJ5A2PPO5PSELSRMI72SYF4KTCB4NIU6AZQ3O6C3J7ZVEP3RVDFEBKVN2RER2GTQ%22%2C%22shshshfpb%22%3A%22v1%5C%2FzMYRjEWKgYe%2BUiNwEvaVlrHBQGVwqLx4CsS9PH1s0s0Vs9AWk%2B7vr9KSHh3BQd5NTukznDTZnd75xHzonHnw%3D%3D%22%2C%22childActivityUrl%22%3A%22openapp.jdmobile%253a%252f%252fvirtual%253fparams%253d%257b%255c%2522category%255c%2522%253a%255c%2522jump%255c%2522%252c%255c%2522des%255c%2522%253a%255c%2522couponCenter%255c%2522%257d%22%2C%22monitorSource%22%3A%22cc_sign_ios_index_config%22%7D&client=apple&clientVersion=8.5.0&d_brand=apple&d_model=iPhone8%2C2&openudid=1fce88cd05c42fe2b054e846f11bdf33f016d676&scope=11&screen=1242%2A2208&sign=1cce8f76d53fc6093b45a466e93044da&st=1581084035269&sv=102'
     response=requests.post('https://api.m.jd.com/client.action?functionId=ccSignInNew',headers=djj_xfj_headers,data=body)
     res=response.text
     
     print(res)
   except Exception as e:
      print(str(e))


def JRJT_DoubleSign():
   try:
     print('\n京东金融金贴双签')
     body='reqData='+urllib.parse.quote(json.dumps({"type":3,"frontParam":{"channel":"JR","belong":4},"actCode":"1DF13833F7"}))
     response=requests.post('https://nu.jr.jd.com/gw/generic/jrm/h5/m/process',headers=djj_xfj_headers,data=body)
     res=response.text
     print(res)
   except Exception as e:
      print(str(e))
def JR_LuckyLottery():
   try:
     print('\金融抽奖顶部签到')
     body='reqData='+urllib.parse.quote(json.dumps({"activityNo":"e2d1b240d5674def8178be6b4faac5b6","signType":"1","encryptSign":""}))
     response=requests.post('https://ms.jr.jd.com/gw/generic/syh_yxmx/h5/m/handleSign',headers=djj_xfj_headers,data=body)
     res=response.text
     print(res)
   except Exception as e:
      print(str(e))
      

      

      
      
def TotalSteel():
   try:
     print('\n总钢镚查询')
     msg='总钢镚查询:'
     response=requests.get('https://coin.jd.com/m/gb/getBaseInfo.html',headers=djj_xfj_headers)
     res=json.loads(response.text)
     msg+=str(res['gbBalance'])
   except Exception as e:
   	  msg+=str(e)
   loger(msg)
      

def TotalRed():
   try:
     print('\n总红包查询')
     msg='红包:'
     body='body=%7B%22fp%22%3A%22-1%22%2C%22appToken%22%3A%22apphongbao_token%22%2C%22childActivityUrl%22%3A%22-1%22%2C%22country%22%3A%22cn%22%2C%22openId%22%3A%22-1%22%2C%22childActivityId%22%3A%22-1%22%2C%22applicantErp%22%3A%22-1%22%2C%22platformId%22%3A%22appHongBao%22%2C%22isRvc%22%3A%22-1%22%2C%22orgType%22%3A%222%22%2C%22activityType%22%3A%221%22%2C%22shshshfpb%22%3A%22-1%22%2C%22platformToken%22%3A%22apphongbao_token%22%2C%22organization%22%3A%22JD%22%2C%22pageClickKey%22%3A%22-1%22%2C%22platform%22%3A%221%22%2C%22eid%22%3A%22-1%22%2C%22appId%22%3A%22appHongBao%22%2C%22childActiveName%22%3A%22-1%22%2C%22shshshfp%22%3A%22-1%22%2C%22jda%22%3A%22-1%22%2C%22extend%22%3A%22-1%22%2C%22shshshfpa%22%3A%22-1%22%2C%22activityArea%22%3A%22-1%22%2C%22childActivityTime%22%3A%22-1%22%7D&client=apple&clientVersion=8.5.0&d_brand=apple&networklibtype=JDNetworkBaseAF&openudid=1fce88cd05c42fe2b054e846f11bdf33f016d676&sign=fdc04c3ab0ee9148f947d24fb087b55d&st=1581245397648&sv=120'
     response=requests.post('https://api.m.jd.com/client.action?functionId=myhongbao_balance',headers=djj_xfj_headers,data=body)
     res=json.loads(response.text)
     print(res)
     msg+=f'''{res['balanceMap']['totalUsableBalance']}/{res['totalBalance']}'''
   except Exception as e:
      msg+=str(e)
   loger(msg)

def TotalSubsidy():
   try:
     print('\n总金贴查询')
     msg='总金贴查询'
     headers=djj_xfj_headers
     headers['Referer']='https://active.jd.com/forever/cashback/index?channellv=wojingqb'
     response=requests.get('https://ms.jr.jd.com/gw/generic/uc/h5/m/mySubsidyBalance',headers=headers)
     res=json.loads(response.text)
     print(res)
     msg+=str(res['resultData']['data']['balance'])
   except Exception as e:
      msg+=str(e)
   loger(msg)
def TotalMoney():
   try:
     print('\n总现金查询')
     msg='总现金:'
     response=requests.get('https://api.m.jd.com/client.action?functionId=cash_exchangePage&body=%7B%7D&build=167398&client=apple&clientVersion=9.1.9&openudid=1fce88cd05c42fe2b054e846f11bdf33f016d676&sign=762a8e894dea8cbfd91cce4dd5714bc5&st=1602179446935&sv=102',headers=djj_xfj_headers)
     res=json.loads(response.text)
     print(res)
     msg+=str(res['data']['result']['totalMoney'])
   except Exception as e:
     msg+=str(e)
   loger(msg)
      
      
      
      
def iosrule(mod,body={}):
   try:
     url=f'''https://api.m.jd.com/client.action?functionId={mod}'''
     response=requests.post(url,headers=djj_xfj_headers,data=json.dumps(body))
     res=response.text
     print(res)
     return res
   except Exception as e:
      print(f'''初始化{mode}任务:''', str(e))
      
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
   print('over💎',result)
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
   global djj_xfj_headers
   global djj_djj_cookie
   check('DJJ_XFJ_HEADERS',xfj_hdlist)
   check('DJJ_DJJ_COOKIE',cookiesList)
   j=0
   for count in cookiesList:
     j+=1
     #if j!=2:
       #continue
     djj_xfj_headers=eval(xfj_hdlist[0])
     djj_xfj_headers['Cookie']=count
     if(islogon(j,count)):
         JD_doTask()

   pushmsg('jd_bean',result)
if __name__ == '__main__':
       start()
