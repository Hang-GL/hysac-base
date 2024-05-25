import getopt
import sys
import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
class HysacException(Exception):
    def __init__(self,ErrorInfo,Line):
        super().__init__(self)
        self.ErrorInfo=ErrorInfo
        self.Line=Line
    def __str__(self):
        return self.ErrorInfo

stage0_agent={
        "Host": "cp.fjg360.cn",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
stage1_agent = {
        "Host": "api.fjg360.cn",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "*/*",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
stage2_agent = {
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Origin": "http://h5.cyol.com",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
stage3_agent = {
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/tpg,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.tencent.mm",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
stage4_agent = {
        "Host": "cp.fjg360.cn",
        "Connection": "keep-alive",
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer":"https://cp.fjg360.cn/wenda/18da/door.php"
    }
Rresult={
    "code":-1,
    "message":"undefined error",
    "OpenID":"",
    "course":"",
    "name":"",
    "section1":"",
    "section2":"",
    "section3":"",
    "class":"",
    "picUrl":"",
    "EmuUrl":"",
    "cid":""
}
version=(1,0,0,0)
urlWithCode=""
openid=""
okFlag=True

steps=[0,0,0,0,0]
step_preset=[-1,-1,-1,-1,-1]

#stage 0
def S0_UrlLogin():
    ssLogin=requests.session()
    try:
        replaced=urlWithCode.replace("rood","door.php")
    except:
        raise HysacException("Invalid URL",sys._getframe().f_lineno)
    try:
        replaced=replaced+"#wechat_redirect"
        resp=ssLogin.get(replaced,headers=stage0_agent)
        sstr=resp.content.decode("utf8")
        ssLogin.close()
        opidPosi=sstr.find("pre_loc='sessionId=&imgTextId=&ip=&username='+username+'&phone='+phone+'&city='+city+'&danwei2='+danwei2+'&danwei='+danwei+'&openid=")+132
        buildstr=""
        while(sstr[opidPosi]!="'"):
            buildstr+=sstr[opidPosi]
            opidPosi+=1
    except:
        raise HysacException("URL invalid or expired",sys._getframe().f_lineno)
    if(buildstr!=""):
        Rresult["OpenID"]=buildstr
    else:
        raise HysacException("OpenID generating failed",sys._getframe().f_lineno)
    
#stage 1
def S1_GetUser():
    try:
        ssTask=requests.session()
        url = "https://api.fjg360.cn/index.php?m=vote&c=index&a=get_members&openid="+ Rresult["OpenID"]
        resp = ssTask.get(url, headers=stage1_agent).json()
        ssTask.close()
    except:
        raise HysacException("Request Error",sys._getframe().f_lineno)
    if resp.get("code") == 1:
        user=resp.get("h5_ask_member")
        Rresult["name"]=user["name"]
        Rresult["section1"]=user["danwei1"]
        Rresult["section2"]=user["danwei2"]
        Rresult["section3"]=user["danwei3"]
        Rresult["class"]=user["class_name"]
    else:
        raise HysacException("Wrong OpenID",sys._getframe().f_lineno)

#stage 2
def S2_GetLatestCourse():
    try:
        ssTask=requests.session()
        url = "https://h5.cyol.com/special/weixin/sign.json"
        resp = ssTask.get(url,headers=stage2_agent).json()
        ssTask.close()
        Rresult["cid"]=list(resp)[-1]
    except:
        raise HysacException("Request Error",sys._getframe().f_lineno)

#stage 3
def S3_GetCourseProps():
    try:
        ssTask=requests.session()
        url = 'https://h5.cyol.com/special/daxuexi/'+ Rresult["cid"] +'/m.html'
        resp = ssTask.get(url,headers=stage3_agent)
        ssTask.close()
    except:
        raise HysacException("Request Error",sys._getframe().f_lineno)
    if(resp.status_code!=200):raise HysacException("Can not find course",sys._getframe().f_lineno)
    try:
        soup = BeautifulSoup(resp.content.decode("utf8"),"lxml")
        Rresult["course"] = soup.title.string[7:]
    except:
        raise HysacException("Can not parse course",sys._getframe().f_lineno)

def S4_SubmitRecord():
    try:
        ssTask=requests.session()
        url = "&username=" + Rresult["name"]
        url += "&phone=" + "未知"
        url += "&city=" + Rresult["section1"]
        url += "&danwei2=" + Rresult["section3"]
        url += "&danwei=" + Rresult["section2"]
        url += "&openid=" + Rresult["OpenID"]
        url += "&num=10"
        url += "&lesson_name=" + Rresult["course"]
        url="https://cp.fjg360.cn/index.php?m=vote&c=index&a=save_door&sessionId=&imgTextId=&ip="+url
        resp = ssTask.get(url,headers=stage4_agent).json()
        ssTask.close()
    except:
        raise HysacException("Request Error",sys._getframe().f_lineno)
    if resp.get("code") == 1:
        Rresult["picUrl"]="https://h5.cyol.com/special/daxuexi/"+Rresult["cid"]+"/images/end.jpg"
        Rresult["EmuUrl"]="https://hang-gl.github.io/Hysac-emu/web/door.html?id="+Rresult["cid"]
    else:
        raise HysacException("Submit record failed",sys._getframe().f_lineno)

def proc_run():
    global steps
    try:
        if(steps[0]):S0_UrlLogin()
        if(steps[1]):S1_GetUser()
        if(steps[2]):S2_GetLatestCourse()
        if(steps[3]):S3_GetCourseProps()
        if(steps[4]):S4_SubmitRecord()
        Rresult["code"]=0
        Rresult["message"]="Success"
    except HysacException as e:
        Rresult["code"]=e.Line
        Rresult["message"]=e.ErrorInfo
    except:pass

def parse_step(val):
    global steps
    if(len(val)!=5):raise HysacException("Invalid step info",sys._getframe().f_lineno)
    else:
        for num in range(0,5):
            if(val[num]=='0'):steps[num]=0
            else:steps[num]=1

def parse_data(val):
    global Rresult,urlWithCode,step_preset
    if(len(val)==0):raise HysacException("URL or OpenID is required",sys._getframe().f_lineno)
    if(val.find("://")==-1):
        step_preset[0]=0
        Rresult["OpenID"]=val
    else:
        step_preset[0]=1
        urlWithCode=val

def parse_course(val):
    global step_preset
    Rresult["cid"]=val
    step_preset[2]=0

def check_args():
    global steps,step_preset
    if(step_preset[0]==-1):raise HysacException("URL or OpenID is required",sys._getframe().f_lineno)
    for i in range(0,5):
        if(step_preset[i]!=-1):steps[i]=step_preset[i]

def command_proc():
    try:
        opts,args=getopt.getopt(sys.argv[1:],'d:s:t:hv',["help","version"])
    except:
        raise HysacException("Invalid arguments",sys._getframe().f_lineno)
    
    global steps
    steps=[1,1,1,1,1]
    for name,val in opts:
        if name in ("-h","--help"):
            print("[-h --help] help info [-v --version] version [-s <string>] steps(len=5) [-d <string>] Wechat url or OpenID")
            print("Open URL in Wechat:")
            print("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx26a2a915deb3df1c&redirect_uri=https%3A%2F%2Fcp.fjg360.cn%2Fwenda%2F18da%2Frood%3FsessionId%3D%26secret%3D60e9768b2c0ea4b99265237587416905%26tset%3D1&response_type=code&scope=snsapi_userinfo&state=STATE&connect_redirect=0#wechat_redirect")
            return
        if name in ("-v","--version"):
            print(version[0],".",version[1],".",version[2],".",version[3])
            return
        if name in ("-d"): 
            parse_data(val)
        if name in ("-s"):
            parse_step(val)
        if name in ("-t"):
            parse_course(val)
    check_args()
    proc_run()

def window_proc():
    global steps
    steps=[1,1,1,1,1]
    print("Hubei Youth Study Automatic Completer - HYSAC")
    print("----------------")
    print("Open in Wechat:")
    print("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx26a2a915deb3df1c&redirect_uri=https%3A%2F%2Fcp.fjg360.cn%2Fwenda%2F18da%2Frood%3FsessionId%3D%26secret%3D60e9768b2c0ea4b99265237587416905%26tset%3D1&response_type=code&scope=snsapi_userinfo&state=STATE&connect_redirect=0#wechat_redirect")
    print("----------------")
    print("Input URL or OpenID:")
    data=input()
    try:
        parse_data(data)
        check_args()
        proc_run()
    except:pass
    if(Rresult["code"]!=0):
        print()
        print("**Error**")
        print()
        print(Rresult["message"],":",Rresult["code"])
    else:
        print()
        print("**Success**")
        print()
        print(Rresult["name"]+"("+Rresult["class"]+")")
        print(Rresult["section1"],"-",Rresult["section2"],"-",Rresult["section3"])
        print(Rresult["course"]+"("+Rresult["cid"]+")")
        print("----------------")
        print("OpenID:"+Rresult["OpenID"])
        print("Emulation site:"+Rresult["EmuUrl"])
    print()
    input("press 'Enter' to exit")
    

def process():
    argc=len(sys.argv)
    if(argc<2):
        window_proc()
    else:
        command_proc()
        print(json.dumps(Rresult))


if __name__ == '__main__':
    try:
        process()
    except :
        pass