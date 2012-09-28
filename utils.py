#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,hashlib

def _(string):
    try:
        return string.decode("u8")
    except:
        return string

def _print(str):
    print (_(str))

def get_module_path():
        if hasattr(sys, "frozen"):
            module_path = os.path.dirname(sys.executable)
        else:
            module_path = os.path.dirname(os.path.abspath(__file__))
        return module_path

def hexchar2bin(hex):
    arry= bytearray()
    for i in range(0, len(hex), 2):
        arry.append(int(hex[i:i+2],16))
    return arry

def __md5(self,item):
    if sys.version_info >= (3,0):
        try:
          item=item.encode("u8")
        except:
          pass
    return hashlib.md5(item).hexdigest().upper()
