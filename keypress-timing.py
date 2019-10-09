#!/usr/bin/env python3
import time

NULL_CHAR = chr(0)

special1='-=[]\;\'`,./'

def write_report(report, timeout=0.05):
    with open('/dev/hidg0', 'rb+') as fd:
        for x in report:
            if ord(x)==0:
                time.sleep(0.01)
            else:
                time.sleep(0.05)
            fd.write(x.encode())
        #fd.write(report.encode())

def release_key():
    write_report(NULL_CHAR*8, 0.01)


def write_letter(x):
    if x=='\t':
        write_report(NULL_CHAR*2+chr(43)+NULL_CHAR*5)
        release_key()
        return
    if x=='0':
        write_report(NULL_CHAR*2+chr(39)+NULL_CHAR*5)
        release_key()
        return
    if x>='1' and x<='9':
        keyCode = 30 + ord(x)-ord('1')
        write_report(NULL_CHAR*2+chr(keyCode)+NULL_CHAR*5)
        release_key()
        return
    if x>='A' and x<='Z':
        keyCode = 4 + ord(x)-ord('A')
        write_report(chr(32)+NULL_CHAR+chr(keyCode)+NULL_CHAR*5)
        release_key()
        return
    if x>='a' and x<='z':
        keyCode = 4 + ord(x)-ord('a')
        write_report(NULL_CHAR*2+chr(keyCode)+NULL_CHAR*5)
        release_key()
        return
    if x==' ':
        write_report(NULL_CHAR*2+chr(44)+NULL_CHAR*5)
        release_key()
        return
    if ord(x)==10:
        write_report(NULL_CHAR*2+chr(40)+NULL_CHAR*5)
        release_key()
        return
    if special1.find(x)>=0:
        write_report(NULL_CHAR*2+chr(46+special1.find(x))+NULL_CHAR*5)
        release_key()
    

doc="""
Ahoj, jak se mas?
Ja se mam dobre.
Je mi 1234567890 let
"""
for x in doc:
    write_letter(x)
