# Hubei Youth Study Automatic Completer (Hysac)
湖北青年大学习自动完成脚本
## 申明
- 本项目仅供学习，**`请勿`使用本脚本完成青年大学习**以及其他非法用途
- 本项目遵循`Apache 2.0`协议，请在遵顼本协议的条件下使用本项目
- 本项目的开发者**不会提供任何**关于使用该脚本完成青年大学习的帮助
- 使用本项目即表示您同意并遵循以上申明
- 直接拖视频进度条不是更方便吗（雾
## 使用方法
### **本节内容仅用于分享实现思路，再次声明`请勿使用本脚本完成青年大学习`**
### 获取链接
在微信中打开链接`https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx26a2a915deb3df1c&redirect_uri=https%3A%2F%2Fcp.fjg360.cn%2Fwenda%2F18da%2Frood%3FsessionId%3D%26secret%3D60e9768b2c0ea4b99265237587416905%26tset%3D1&response_type=code&scope=snsapi_userinfo&state=STATE&connect_redirect=0#wechat_redirect`待出现404页面后点击标题右上角的按钮使用浏览器打开，复制链接后运行本项目并输入链接，回车即可完成，此时输出的信息应与在青年大学习页面设置的个人信息相同，同时也会展示你的openID，下次可直接输入openID即可
### 命令行/其他应用调用
带参数运行该脚本，将会以JSON字符串作为输出，输出示例如下
```JSON
{
    "code": -1, 
    "message": "undefined error", 
    "OpenID": "", 
    "course": "", 
    "name": "", 
    "section1": "", 
    "section2": "", 
    "section3": "", 
    "picUrl": "", 
    "EmuUrl": "", 
    "cid": ""
}
```
从上到下各值的含义如下：
|键名|解释|
|-|-|
|code|运行结果，返回0为无错误，否则为抛出错误对应的行号|
|message|运行信息|
|OpenID|你的青春湖北OpenID|
|course|课程名| 
|name|姓名|
|section1|所属地区|
|section2|所属单位|
|section3|组织|
|class|班级|
|picUrl|本次课程的背景图|
|EmuUrl|打开本链接可以截图|
|cid|课程名对应的编号|

其中命令行可供使用的参数有
|参数|说明|
|-|-|
|-d|URL或openid|
|-s|长度为5的字符串，详见[运行过程](#运行过程)|
|-t|要完成的课程的编号（可能不会被统计）|
|-h/--help|获取帮助|
|-v/--version|版本号|
## 编译与运行
运行`build.sh`(Linux)或`build.bat`(Windows)即可在`./dist`下生成可执行文件
## 运行过程
本项目运行分为5步，在命令行中通过`-s`参数输入长度为5的字符串即可控制是否运行对应步骤，若步骤对应的字符为`0`则跳过该步，否则正常运行，通过使用该命令可完成其他功能，但也**可能会引发错误**

其中各个步骤的作用如下：
1. 解析输入的URL并获取OpenID
2. 通过OpenID获取用户信息
3. 获取最新课程的编号
4. 获取课程信息
5. 提交学习记录

