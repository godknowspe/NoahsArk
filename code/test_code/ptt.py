# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:56:07 2017

@author: Gary
"""

import telnetlib
import time

HOST = "ptt.cc"
user = "blueweak"
password = "736173"

tn = telnetlib.Telnet(HOST)

#outstr = tn.read_very_eager()
outstr = tn.read_until("new")
print outstr
print len(outstr)

#tn.read_until("註冊: ")
tn.write(user + "\r")

time.sleep(1)
print tn.read_very_eager()

if password:
    #tn.read_until("密碼: ")
    tn.write(password + "\r")

time.sleep(1)
print tn.read_very_eager()

tn.write("\r")

time.sleep(1)
print tn.read_very_eager()

tn.write("\r")
print tn.read_very_eager()
time.sleep(1)
tn.write("\r")
print tn.read_very_eager()
time.sleep(1)
tn.write("f")
print tn.read_very_eager()
time.sleep(1)
tn.write("\r")
print tn.read_very_eager()
time.sleep(1)
tn.write("29")
print tn.read_very_eager()
time.sleep(1)
tn.write("\r")
print tn.read_very_eager()
time.sleep(1)

tn.write("\r")
print tn.read_very_eager()
time.sleep(1)
tn.write("\r")
print tn.read_very_eager()
time.sleep(1)

tn.write("f")
time.sleep(1)
print tn.read_very_eager()
time.sleep(1)