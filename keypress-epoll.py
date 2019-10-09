#!/usr/bin/env python3
import time
import select
import sys

NULL_CHAR = chr(0)

special1='-=[]\;\'`,./'

def release_key():
    return NULL_CHAR*8


def write_letter(x):
    if x=='\t':
        return NULL_CHAR*2+chr(43)+NULL_CHAR*5 + release_key()
    if x=='0':
        return NULL_CHAR*2+chr(39)+NULL_CHAR*5 + release_key()
    if x>='1' and x<='9':
        keyCode = 30 + ord(x)-ord('1')
        return NULL_CHAR*2+chr(keyCode)+NULL_CHAR*5 + release_key()
    if x>='A' and x<='Z':
        keyCode = 4 + ord(x)-ord('A')
        return chr(32)+NULL_CHAR+chr(keyCode)+NULL_CHAR*5 + release_key()
    if x>='a' and x<='z':
        keyCode = 4 + ord(x)-ord('a')
        return NULL_CHAR*2+chr(keyCode)+NULL_CHAR*5  + release_key()
    if x==' ':
        return NULL_CHAR*2+chr(44)+NULL_CHAR*5 + release_key()
    if ord(x)==10:
        return NULL_CHAR*2+chr(40)+NULL_CHAR*5 + release_key()
    if special1.find(x)>=0:
        return NULL_CHAR*2+chr(46+special1.find(x))+NULL_CHAR*5 + release_key()


def convert_text(txt):
    out = ""
    for x in txt:
        out += write_letter(x)
    return out


def writeKey(key):
    usbSeq = convert_text(key)
    print(usbSeq.encode())
    count = 0
    e = select.poll()
    fd=open('/dev/hidg0', 'rb+')
    print("FD={}".format(fd.fileno()))
    print("Len={}".format(len(usbSeq)))
    keyCode = 0
    nbytes = 0
    try:
        e.register(fd.fileno(), select.POLLOUT | select.POLLHUP |  select.POLLIN | select.POLLNVAL | select.POLLPRI | select.EPOLLWRNORM | select.EPOLLRDBAND | select.EPOLLWRBAND )
        while count<len(usbSeq):
            events = e.poll(1)
        #print(events)
        #print(len(events))
            for fno, event_type in events:
                if ( event_type & select.POLLERR) != 0:
                    print("ERRR")
                if ( event_type & select.POLLHUP) != 0:
                    print("HUP")
                if ( event_type & select.POLLNVAL) != 0:
                    print("NVAL")
                if ( event_type & select.POLLPRI) != 0:
                    print("PRI")
                if ( event_type & select.POLLIN ) != 0:
                    print("CAN READ")
                if ( event_type & select.EPOLLRDBAND ) != 0:
                    print("CAN EPOLLRDBAND")
                if ( event_type & select.EPOLLWRBAND ) != 0:
                    print("CAN EPOLLWRBAND")
                if ( event_type & select.EPOLLET ) != 0:
                    print("CAN EPOLLET")
                if ( event_type & select.EPOLLONESHOT) != 0:
                    print("CAN EPOLLSHNOT")
                if ( event_type & select.POLLOUT ) != 0:
                    #print("CAN WRITE")
                    x=usbSeq[count]
                    nbytes = fd.write(x.encode())
                    count += nbytes
    except Exception as err:
        print(err)
    finally:
        print("DONE.")
        e.unregister(fd.fileno())
        #e.close()
        fd.flush()
        fd.close()



writeKey("abcdefghij")
