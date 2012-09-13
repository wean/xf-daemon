#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import urllib as parse
    import urllib2 as request
    import cookielib as cookiejar
except:
    from urllib import parse,request
    from http import cookiejar
import os

class LWPCookieJar(cookiejar.LWPCookieJar):
    def save(self, filename=None, ignore_discard=False, ignore_expires=False,userinfo=None):
        if filename is None:
            if self.filename is not None: filename = self.filename
            else: raise ValueError(MISSING_FILENAME_TEXT)

        f = open(filename, "a+")
        try:
            if userinfo:
                f.seek(0)
                f.write("#LWP-Cookies-2.0\n")
                f.write("#%s\n"%userinfo)
            else:
                f.seek(len(''.join(f.readlines()[:2])))
            f.write(self.as_lwp_str(ignore_discard, ignore_expires))
            truncate_pos = f.tell()
            f.truncate(truncate_pos)
        finally:
            f.close()

class httpwrapper:

    def start(self):
        self.cookieJar=LWPCookieJar(self.__cookiepath)

        cookieload=False

        if os.path.isfile(self.__cookiepath):
            try:
                self.cookieJar.load(ignore_discard=True, ignore_expires=True)
                cookieload=True
            except:
                pass

        opener = request.build_opener(request.HTTPCookieProcessor(self.cookieJar))
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        request.install_opener(opener)

    def request(self,url,data=None,savecookie=False):
        """
            请求url
        """
        if data:
            data = parse.urlencode(data).encode('utf-8')
            fp=request.urlopen(url,data)
        else:
            fp=request.urlopen(url)
        try:
            str = fp.read().decode('utf-8')
        except UnicodeDecodeError:
            str = fp.read()
        if savecookie == True:
            if hasattr(self,"pswd"):
                self.cookieJar.save(ignore_discard=True, ignore_expires=True,userinfo="%s#%s"%(self.__qq,self.hashpasswd))
            else:
                self.cookieJar.save(ignore_discard=True, ignore_expires=True)

        fp.close()
        return str
