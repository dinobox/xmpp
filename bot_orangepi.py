#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from os import popen
from os import system
from time import time
import sys
import base64
from os import getcwd

from pyA20.gpio import gpio
from pyA20.gpio import port

gpio.init()
##设置 PA7 为输出
gpio.setcfg(port.PA7, gpio.OUTPUT)

class EchoBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)


    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        print("msg:%s\n" % msg)
        if str(msg['from']).split('/')[0] in ('gpiopi@sure.im', 'sunny@sure.im','morgan@sure.im','gpiopi@semantic.semioe.com','snailpi@semantic.semioe.com'):
        #if msg['type'] in ('chat', 'normal'):
            txt="%(body)s" % (msg)
            retxt=txt
            if(txt=="拍照"):
                retxt="正在拍照"
                timestamp=int(time())
                pic_file_name="/home/pi/pics/%s.jpg" % (timestamp)
                system("fswebcam %s" % (pic_file_name))
                #base64_content=base64.b64encode(open(pic_file_name).read())
                img_url=popen("curl -F 'file=@%s;filename=%s.jpg;type=image/jpeg' http://47.52.16.64:3000/upload" %(pic_file_name,timestamp)).read()
                #img_url="data:image/x-icon;base64,%s" % (base64_content)
                #retxt="<image xmlns='http://mangga.me/protocol/image' type='image/jpeg'>%s</image>" % (base64_content)
                retxt="http://47.52.16.64:3000%s" % (img_url)
            if(txt=="关机"):
                retxt="正在关机"
            if(txt=="开灯"):
                gpio.output(port.PA7, gpio.HIGH)
                retxt="已开启"
            if(txt=="关灯"):
                gpio.output(port.PA7, gpio.LOW)
                retxt="已关闭"
            if(txt[0:1]=="#"):
                #cmd=txt[1:len(txt)]
                cmd=txt.split("#")[1]
                retxt=popen(cmd).read()
            msg.reply("\n%s" % retxt).send()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    if(len(sys.argv)<3):
        print("use:%s jid passwd" % (sys.argv[0]))
        sys.exit(1)
    xmpp = EchoBot(sys.argv[1],sys.argv[2])
    xmpp.connect()
    xmpp.process(block=True)
