import requests
import json

zdUrl = 'http://api.turinglabs.net/api/v1/jd/bean/create/'
ncUrl = 'http://api.turinglabs.net/api/v1/jd/farm/create/'
mcUrl = 'http://api.turinglabs.net/api/v1/jd/pet/create/'

Defalt_ncShareCode= ['ae6488dc5f0c4669bfa432b9bc884191','268e797816f340bc9ad3656fa249d1a6']#读取参数djj_sharecode为空，开始读取默认参数
Defalt_mcShareCode= ['MTAxODExNDYxMTEwMDAwMDAwMzk4NzYxOTc=','MTAxODExNDYxMTEwMDAwMDAwNDA1NDQwNzE=']#读取参数djj_sharecode为空，开始读取默认参数
Defalt_zdShareCode= ['']#读取参数djj_sharecode为空，开始读取默认参数
#学习与测试  by 红鲤鱼绿鲤鱼与驴 2020.1
def AddhelpCode(Url,Defalt_ShareCode):
   for code in Defalt_ShareCode:
      try:
         AddcodeRes=hongliyu(Url+code+'/')
         print(AddcodeRes)
      
         if AddcodeRes['code']==200:
           print("互助码添加成功✅")
         elif AddcodeRes['code']==400:
           print("互助码已存在")
         else:
           print('互助码添加异常')
      except Exception as e:
          	pass
def hongliyu(url):
   try:
     return json.loads(requests.get(url).text)
   except Exception as e:
      print(f'''初始化函数:''', str(e))
      
AddhelpCode(mcUrl,Defalt_mcShareCode)
AddhelpCode(ncUrl,Defalt_ncShareCode)
