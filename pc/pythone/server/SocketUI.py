#!/usr/bin/env python
#-*- coding:gbk -*-
import time
import wx
import socket

#import sys
import threading
import struct
#import logging
#logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%d/%b/%Y %H:%M:%S]')

#Receive message
class Receiver(threading.Thread):
    def __init__(self,threadName,window):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        #���ӷ�����
        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Connect to server and send data
            self.window.LogMessage(u"IP: "+self.window.host+" port:"+str(self.window.port)+"...\n")
            self.sock.bind((self.window.host, self.window.port))
            #self.window.LogMessage(u"���ӷ������ɹ�...\n")
            self.runT = True
        except Exception,data:
            print Exception,":",data
            self.window.LogMessage(u"���ӷ�����ʧ��...\n")
            self.sock.close()

    def stop(self):
        self.window.LogMessage(u"�ر�Socket����...\n")
        self.sock.close()
        self.runT = False
        self.timeToQuit.set()

    def sendMsg(self,msg):
        logMsg = (u"���ͣ�%s\n" % (msg))
        self.window.LogMessage(logMsg)
        self.sock.sendall(msg)

    def run(self):
        try:
            while self.runT:
                udpT4Data, udpT4ServerInfo = self.sock.recvfrom(1024)
                if udpT4Data:
                    #dataLen, = struct.unpack_from("i",data)
                    #wx.CallAfter(self.window.LogMessage,(u"�������ݳ���:%s\n" % (dataLen)))
                    wx.CallAfter(self.window.LogMessage,(u"��������:%s\n" % udpT4Data))
        except Exception:
            pass
class InsertFrame(wx.Frame):

    def __init__(self, parent, id):

        #��������
        wx.Frame.__init__(self, parent, id, 'Socket Client', size=(640, 450))
        #��������
        self.panel = wx.Panel(self,-1)
        self.panel.SetBackgroundColour("White")
        #������ť
        self.createButtonBar(self.panel)
        #������̬�ı�
        self.createTextFields(self.panel)
        #�����ı���
        self.creatTextInput(self.panel)

        #Socket ��ַ
        self.host, self.port = "localhost", 12340
        self.runT = True
###############################
    #�����ı�
    def createTextFields(self, panel):
        for eachLabel, eachPos in self.textFieldData():
            self.createCaptionedText(panel, eachLabel, eachPos)

    def createCaptionedText(self, panel, label, pos):
        static = wx.StaticText(panel, wx.NewId(), label, pos)
        static.SetBackgroundColour("White")
#########################
    #������ť
    def createButtonBar(self, panel):
        for eachLabel,eachSize,eachPos, eachHandler in self.buttonData():
            self.buildOneButton(panel, eachLabel,eachSize,eachHandler,eachPos)
    def buildOneButton(self, parent, label,buttonsize,handler, pos=(0,0)):
        button = wx.Button(parent, -1, label, pos,buttonsize)
        #�󶨰�ť�ĵ����¼�
        self.Bind(wx.EVT_BUTTON, handler, button)
#########################
    #��ť������
    def buttonData(self):#(��ť���ƣ���ť��С����ť���꣬��ť�¼���
        return ((u"�� ��",(50, 25),(310, 30),self.OnConnection),
                (u"�� ��", (50, 25),(370, 30),self.OnCloseSocket),
                (u"�� ��", (50, 25),(430, 30),self.OnClearLog),
                (u"�� ��", (50, 25),(540, 400),self.OnSend))
    #�ı�����
    def textFieldData(self):
        return (("Please Input socket address AND port��", (10, 10)),
                (u"������Ϣ��", (10, 380)))
########################
    #�����ı���
    def creatTextInput(self,panel):
        #��������ַ�����
        self.socketHostText = wx.TextCtrl(self.panel, wx.NewId(), "", size=(230, 25),pos=(10, 30))
        #�������˿������
        self.socketPortText = wx.TextCtrl(self.panel, wx.NewId(), "", size=(50, 25),pos=(250, 30))
        #��Ϣ��ʾ
        self.log = wx.TextCtrl(self.panel, -1, "",size=(620, 310),pos=(10, 60),style=wx.TE_RICH|wx.TE_MULTILINE|wx.TE_READONLY)
        #��Ϣ����
        self.inputMessage = wx.TextCtrl(self.panel, wx.NewId(), size=(520, 25),style=wx.TE_PROCESS_ENTER,pos=(10, 400))
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSend, self.inputMessage)
########################

    #�¼�������(�رմ��ڣ�
    def OnCloseWindow(self, event):
        self.thread.stop()
        self.Destroy()

    #�¼�������(�ر�Socket��
    def OnCloseSocket(self, event):
        self.thread.stop()

    #�¼�������(���ӵ�SOCKET��
    def OnConnection(self,event):
        if self.socketHostText.GetValue()!='' and self.socketPortText.GetValue()!='':
            self.host, self.port = str(self.socketHostText.GetValue()),int(self.socketPortText.GetValue())
        threadName = "socketclient"
        self.thread = Receiver(threadName, self)#����һ���߳�
        self.thread.setDaemon(True)
        self.thread.start()#�����߳�

    #�¼�������(��ʾLOG��
    def LogMessage(self, msg):#ע��һ����Ϣ
        self.log.AppendText(msg)

    #�¼�������(���LOG��
    def OnClearLog(self,event):#ע��һ����Ϣ
        self.log.Clear()

    #�¼�������(��SOCKET������Ϣ,����������
    def OnSend(self, event):
        self.thread.sendMsg(self.inputMessage.GetValue())
        self.inputMessage.Clear()

import uuid
def get_mac_address(): 
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = InsertFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
    localIP = socket.gethostbyname(socket.gethostname())#�õ�����ip
    print "local ip:%s "%localIP
    ipList = socket.gethostbyname_ex(socket.gethostname())
    for i in ipList:
        print "external IP:%s"%i
    print get_mac_address()
