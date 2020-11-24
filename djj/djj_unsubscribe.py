'''
脚本：取关京东店铺和商品
'''
import requests
import json
import time
import timeit
import os
import re
import urllib
from datetime import datetime
from dateutil import tz



result=''
djj_sharecode=''
djj_bark_cookie=''
djj_sever_jiang=''
djj_djj_cookie=''


cookiesList=[]
#以上参数需要远程设置，以下为默认参数

shopPageSize=20
goodPageSize=20
stopShop=''
stopGoods=''
JD_API_HOST = 'https://wq.jd.com/fav'
headers={
      'UserAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}


def getFollowGoods():
   print('\getFollowGoods')
   msg='【getFollowGoods】'
   try:
       url=f'''{JD_API_HOST}/comm/FavCommQueryFilter?cp=1&pageSize={goodPageSize}&category=0&promote=0&cutPrice=0&coupon=0&stock=0&areaNo=1_72_4139_0&sceneval=2&g_login_type=1&callback=jsonpCBKB&g_ty=ls'''
       hd=headers
       hd['Referer']='https://wqs.jd.com/my/fav/goods_fav.shtml?ptag=37146.4.1&sceneval=2&jxsid=16060273094135053167'

       login=requests.get(url,headers=hd).text
       print(login)
       obj=json.loads(login[14:-13])
       
       return obj
   except Exception as e:
      msg+=str(e)
      #print(msg)
      loger(msg+'\n')
def getFollowShops():
   print('\getFollowShops')
   msg='【getFollowShops】'
   try:
       url=f'''{JD_API_HOST}/shop/QueryShopFavList?cp=1&pageSize={shopPageSize}&sceneval=2&g_login_type=1&callback=jsonpCBKA&g_ty=ls'''
       hd=headers
       hd['Referer']='https://wqs.jd.com/my/fav/shop_fav.shtml?sceneval=2&jxsid=16060273094135053167&ptag=7155.1.9'
       login=requests.get(url,headers=hd)
       print(login.text)
       obj=json.loads(login.text[14:-13])
       return obj
   except Exception as e:
      msg+=str(e)
      #print(msg)
      loger(msg+'\n')
   
   
   
def unsubscribeGoodsFun(commId):
   print('\n unsubscribeGoodsFun')
   msg='【unsubscribeGoodsFun】'
   try:
       url=f'''{JD_API_HOST}/comm/FavCommDel?commId={commId}&_={time.time()}&sceneval=2&g_login_type=1&callback=jsonpCBKP&g_ty=ls'''
       hd=headers
       hd['Referer']='https://wqs.jd.com/my/fav/goods_fav.shtml?ptag=37146.4.1&sceneval=2&jxsid=16060273094135053167'

       login=requests.get(url,headers=hd)
       print(login.text)
       obj=json.loads(login.text[14:-13])
       return obj
   except Exception as e:
      msg+=str(e)
      #print(msg)
      loger(msg+'\n')
def unsubscribeShopsFun(shopId,venderId):
   print('\n unsubscribeShopsFun')
   msg='【unsubscribeShopsFun】'
   try:
       url=f'''{JD_API_HOST}/shop/DelShopFav?shopId={shopId}&venderId={venderId}&_={time.time()}&sceneval=2&g_login_type=1&callback=jsonpCBKG&g_ty=ls'''
       hd=headers
       hd['Referer']=f'''https://shop.m.jd.com/?shopId={shopId}'''
       login=requests.get(url,headers=hd)
       print(login.text)
       obj=json.loads(login.text[14:-13])
       return obj
   except Exception as e:
      msg+=str(e)
      #print(msg)
      loger(msg+'\n')
   
def unsubscribeShops():
   print('\n unsubscribeShops')
   msg='【unsubscribeShops】'
   followShops = getFollowShops()
   if followShops['iRet']=='0':
      count = 0
      unsubscribeShopsCount = count
      if ((shopPageSize * 1) !=0):
        if (int(followShops['totalNum'])> 0):
          for item in followShops['data']:
            res =unsubscribeShopsFun(item['shopId'],item['venderId'])
            print('取消关注店铺结果', res)
            if (res['iRet'] == '0') :
               print(f'''取消已关注店铺---{item['shopName']}----成功\n''')
               count +=1
            else:
               print(f'''取消已关注店铺---{item['shopName']}----失败\n''')
          unsubscribeShopsCount = count;

def unsubscribeGoods():
   print('\n unsubscribeGoods')
   msg='【unsubscribeGoods】'
   followGoods = getFollowGoods()
   print(followGoods)
   if followGoods['iRet']=='0':
      count = 0
      unsubscribeGoodsCount = count
      if ((shopPageSize * 1) !=0):
        if (int(followGoods['totalNum'])> 0):
          for item in followGoods['data']:
            res =unsubscribeGoodsFun(item['commId'])
            print('取消关注店铺结果', res)
            if (res['iRet'] == 0 and res['errMsg']== 'success') :
               print(f'''取消已关注商品---{item['commTitle'][0:20]}----成功\n''')
               count +=1
            else:
               print(f'''取消已关注商品---{item['commTitle'][0:20]}----失败\n''')
          unsubscribeGoodsCount = count;

      
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


    

def check(st,flag,list):
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
       return list
   else:
       print('DTask is over.')
       exit()
def DJJ_main():
   print('开始')
   unsubscribeGoods()
   unsubscribeShops()
   getFollowShops()
   getFollowGoods()
      	
      	

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
   check(djj_djj_cookie,'DJJ_DJJ_COOKIE',cookiesList)
   j=0
   for count in cookiesList:
     j+=1
     if j!=1:
       continue
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
