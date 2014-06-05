#!/usr/bin/env python
#-*- coding:gbk -*-
import time
import wx
import socket
from jsonParse import JsonParse
from SystemTray import SystemTray
from Device import Device
from Commands import Commands
#import sys
import threading
import struct
#import logging
#logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%d/%b/%Y %H:%M:%S]')

#Receive message

PORT = 1224

class Receiver(threading.Thread):
    def __init__(self,threadName,window):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.host = ''
        #���ӷ�����
        # Create a socket (SOCK_STREAM means a TCP socket)
#        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         ipList = socket.gethostbyname_ex(socket.gethostname())
#         ips = ipList[2]
#         for i in ips:
#             print "external IP:%s"%i
#             
#         try:
#             # Connect to server and send data
#             self.window.LogMessage(u"IP: "+self.host+" port:"+str(PORT)+"...\n")
#             self.sock.bind((self.host, PORT))
#             self.sock.settimeout(10)
#             #self.window.LogMessage(u"���ӷ������ɹ�...\n")
#             self.runT = True
#         except Exception,data:
#             print Exception,":",data
#             self.window.LogMessage(u"���ӷ�����ʧ��...\n")
#             self.sock.close()

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
        self.runT = True
        while self.runT:
            while self.runT:
                ipList = socket.gethostbyname_ex(socket.gethostname())
                ips = ipList[2]
                for i in ips:
                    print "external IP:%s"%i
                    try:
                        # Connect to server and send data
                        self.window.LogMessage(u"IP: "+i+" port:"+str(PORT)+"...\n")
                        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        self.sock.bind((i, PORT))
                        self.sock.settimeout(2)
                        udpT4Data, udpT4ServerInfo = self.sock.recvfrom(1024)
                        if udpT4Data:
                            self.host = i
                            break;
                    except Exception,data:
                        print Exception,":",data
                        self.window.LogMessage(u"���ӷ�����ʧ��...\n")
                        self.sock.close()
                if self.host:
                    self.sock.settimeout(30)
                    self.window.systemTray.ShowBalloon("Connecting Success","^_^",2,wx.ICON_WARNING);
                    break;
            try:
                while self.runT:
                    udpT4Data, udpT4ServerInfo = self.sock.recvfrom(1024)
                    if udpT4Data:
                        #dataLen, = struct.unpack_from("i",data)
                        #wx.CallAfter(self.window.LogMessage,(u"�������ݳ���:%s\n" % (dataLen)))
                        cmd = JsonParse.parseCmd(udpT4Data)
                        if cmd ==  Commands.CMD_PTD_PHSTATUS:
                            device_t = JsonParse.parseDevice(udpT4Data)
                            print "device mac:%s"%device_t.Mac
                            self.window.systemTray.addDevice(device_t)
        #                     if self.device:
        #                         if self.device.Mac == device_t.Mac:
        #                             self.device = device_t
        #                         else :
        #                             self.window.systemTray.addDevice(device_t)
        #                     else :
        #                         self.device = device_t
        
                            wx.CallAfter(self.window.LogMessage,(u"��������:%s\n" % udpT4Data))
                        elif cmd ==  Commands.CMD_PTD_MISSEDCALL:
                            wx.CallAfter(self.window.LogMessage,(u"��������:%s\n" % udpT4Data))
                            self.window.systemTray.ShowBalloon("Missed Call",JsonParse.getMissedCall(udpT4Data),2,wx.ICON_WARNING)
                        elif cmd ==  Commands.CMD_PTD_MISSEDMMS:
                            wx.CallAfter(self.window.LogMessage,(u"��������:%s\n" % udpT4Data))
                            self.window.systemTray.ShowBalloon("Missed MMS","*o*",2,wx.ICON_WARNING);
            except Exception,data:
                print Exception,":",data
                #self.window.systemTray.ShowBalloon("Connection is disconnected","*o*",2,wx.ICON_WARNING);
                self.window.LogMessage(u"���ӷ�����ʧ��...\n")
                self.sock.close()
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
        
        #����ϵͳ����
        self.systemTray = SystemTray(self)
        device = Device()
        #self.systemTray.addDevice(device)
        self.systemTray.ShowBalloon("Connecting","...",10,wx.ICON_WARNING);
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
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
        self.systemTray.RemoveIcon()
        self.systemTray.Destroy()
        if 'thread' in locals().keys():
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
