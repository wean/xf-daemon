#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import subprocess
import os, re
from utils import _print

class XF:
    __RE=re.compile("(\d+) *([^\d ]+)?")

    def __download(self,lists):
        cmds=[]
        _print(dir(lists))
        _print ("开始下载。。。")
        for num in lists:
            num=int(num[0])-1
            cmd="aria2c -c -s10 -x10 --header 'Cookie:ptisp=edu; FTN5K=%s' '%s'"%(self.filecom[num],self.filehttp[num])
            _print (cmd)

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
                    
