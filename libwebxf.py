#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random,time
import json,os,sys,re,hashlib
import getopt

from utils import _print
from utils import _
from utils import hexchar2bin

class webxf:
    __cookiepath = '%s/cookie'%module_path
    __verifyimg  = '%s/verify.jpg'%module_path
    __RE=re.compile("(\d+) *([^\d ]+)?")
    def __preprocess(self,password=None,verifycode=None,hashpasswd=None):

        if not hashpasswd:
            self.hashpasswd=self.__md5(password)

        I=hexchar2bin(self.hashpasswd)
        if sys.version_info >= (3,0):
          H = self.__md5(I + bytes(verifycode[2],encoding="ISO-8859-1"))
        else:
          H = self.__md5(I + verifycode[2])
        G = self.__md5(H + verifycode[1].upper())

        return G

    def __getverifycode(self):

        urlv = 'http://check.ptlogin2.qq.com/check?uin=%s&appid=567008010&r=%s'%(self.__qq,random.Random().random())

        str = self.__request(url = urlv, savecookie=False)
        verify=eval(str.split("(")[1].split(")")[0])
        verify=list(verify)
        if verify[0]=='1':
            imgurl="http://captcha.qq.com/getimage?aid=567008010&r=%s&uin=%s"%(random.Random().random(),self.__qq)
            f=open(self.__verifyimg,"wb")
            fp = request.urlopen(imgurl)
            f.write(fp.read())
            f.close()
            try:
                subprocess.Popen(['xdg-open', self.__verifyimg])
            except:
                _print("请打开%s查看验证码"%self.__verifyimg)
            print("请输入验证码：")
            vf=raw_input("vf # ").strip()
            verify[1]=vf

        return verify

    def __request_login(self):

        urlv="http://ptlogin2.qq.com/login?u=%s&p=%s&verifycode=%s"%(self.__qq,self.passwd,self.__verifycode[1])+"&aid=567008010&u1=http%3A%2F%2Flixian.qq.com%2Fmain.html&h=1&ptredirect=1&ptlang=2052&from_ui=1&dumy=&fp=loginerroralert&action=2-10-&mibao_css=&t=1&g=1"
        str = self.__request(url = urlv,savecookie=True)
        if str.find(_('登录成功')) != -1:
            self.__getlogin()
            self.main()
        elif str.find(_('验证码不正确')) != -1:
            self.__getverifycode()
            self.__Login(False,True)
        elif str.find(_('不正确')) != -1:
            _print('你输入的帐号或者密码不正确，请重新输入。')
            self.__Login(True)
        else:
            #print('登录失败')
            _print(str)
            self.__Login(True)

    def getfilename_url(self,url):
        url=url.strip()
        filename=""
        if url.startswith("ed2k"):
            arr=url.split("|")
            if len(arr)>=4:
                filename=parse.unquote(arr[2])
        else:
            filename=url.split("/")[-1]
        return filename.split("?")[0]
    def __getlogin(self):
        urlv = 'http://lixian.qq.com/handler/lixian/do_lixian_login.php'
        str = self.__request(url =urlv,data={},savecookie=True)
        return str

    def __getlist(self):
            """
            得到任务名与hash值
            """
            urlv = 'http://lixian.qq.com/handler/lixian/get_lixian_list.php'
            res = self.__request(urlv,{},savecookie=False)
            res = json.JSONDecoder().decode(res)
            if res["msg"]==_('未登录!'):
                res=json.JSONDecoder().decode(self.__getlogin())
                if res["msg"]==_('未登录!'):
                    self.__Login()

                else:
                    self.main()
            elif not res["data"]:
                print (_('无离线任务!'))
                self.__addtask()
                self.main()
            else:
                self.filename = []
                self.filehash = []
                self.filemid = []
                res['data'].sort(key=lambda x: x["file_name"])
                for num in range(len(res['data'])):
                    index=res['data'][num]
                    self.filename.append(index['file_name'].encode("u8"))
                    self.filehash.append(index['code'])
                    size=index['file_size']
                    self.filemid.append(index['mid'])
                    if size==0:
                        percent="-0"
                    else:
                        percent=str(index['comp_size']/size*100).split(".")[0]

    def __gethttp(self,filelist):
            """
            获取任务下载连接以及FTN5K值
            """
            urlv = 'http://lixian.qq.com/handler/lixian/get_http_url.php'
            self.filehttp = [''] * len(self.filehash)
            self.filecom = [''] * len(self.filehash)
            for num in filelist:
                num=int(num[0])-1
                data = {'hash':self.filehash[num],'filename':self.filename[num],'browser':'other'}
                str = self.__request(urlv,data)
                self.filehttp[num]=(re.search(r'\"com_url\":\"(.+?)\"\,\"',str).group(1))
                self.filecom[num]=(re.search(r'\"com_cookie":\"(.+?)\"\,\"',str).group(1))
                _print(self.filehttp[num])
                _print(self.filecom[num])

    def __getdownload(self):
            target=raw_input("dl # ").strip()
            if target.upper()=="A":
                lists=zip(range(1,len(self.filehash)+1) , ['']* len(self.filehash))
            else:
                lists=self.__RE.findall(target)
            if lists==[]:
                _print ("选择为空.")
                self.__chosetask()
                return
            _print (lists)

            self.__gethttp(lists)
            self.__download(lists)

    def __deltask(self):
        target=raw_input("dt # ").strip()
        if target.upper()=="A":
            lists=zip(range(1,len(self.filehash)+1) , ['']* len(self.filehash))
        else:
            lists=self.__RE.findall(target)
        if lists==[]:
            _print ("选择为空.")
            self.__chosetask()
        urlv = 'http://lixian.qq.com/handler/lixian/del_lixian_task.php'

        for i in lists:
            num=int(i[0])-1
            data={'mids':self.filemid[num]}
            self.__request(urlv,data)
                    
    def __addtask(self):
        url=raw_input()
        filename=self.getfilename_url(url)
        data={"down_link":url,\
                "filename":filename,\
                "filesize":0,\
                }
        urlv="http://lixian.qq.com/handler/lixian/add_to_lixian.php"
        str = self.__request(urlv,data)

    def __download(self,lists):
        cmds=[]
        for num in lists:
            num=int(num[0])-1
            cmd="aria2c -c -s10 -x10 --header 'Cookie:ptisp=edu; FTN5K=%s' '%s'"%(self.filecom[num],self.filehttp[num])

            if sys.version_info >= (3,0):
                pass
            else:
                cmd=cmd.encode("u8")

            cmds.append(cmd)

        """
        调用aria2进行下载

        """
        _print(cmds)
        for i in cmds:
            os.system("cd %s && %s"%(self._downpath,i))
        try:
            subprocess.Popen(["notify-send","xfdown: 下载完成!"])
        except:
            _print("notify-send error,you should have libnotify-bin installed.")
                    
    def __Login(self,needInput=False,verify=False):
        """
        登录
        """
        if not needInput and not verify:
            try:
                f=open(self.__cookiepath)
                line=f.readlines()[1].strip()
                lists=line.split("#")
                self.__qq=lists[1]
                self.hashpasswd=lists[2]
            finally:
                f.close()
        if not hasattr(self,"hashpasswd") or needInput:
            self.__qq = raw_input('QQ：')
            import getpass
            self.pswd= getpass.getpass('PASSWD: ')
            self.pswd = self.pswd.strip()
        self.__qq = self.__qq.strip()
        self.__verifycode = self.__getverifycode()
        if not hasattr(self,"hashpasswd") or needInput:
            self.passwd = self.__preprocess(
                self.pswd,
                self.__verifycode
            )
        else:
            self.passwd = self.__preprocess(
                verifycode=self.__verifycode ,
                hashpasswd=self.hashpasswd
            )
        _print ("登录中...")
        self.__request_login()
