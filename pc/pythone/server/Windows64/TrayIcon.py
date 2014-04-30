#!/usr/bin/python
# -*- coding: utf-8 -*-

from win32api import *
# Try and use XP features, so we get alpha-blending etc.
try:
     from winxpgui import *
except ImportError:
     from win32gui import *

import win32con
import sys, os
import struct
import time
from collections import namedtuple

PyNOTIFYICONDATA = namedtuple('PyNOTIFYICONDATA',
                              'hWnd ID Flags CallbackMessage '
                              'hIcon Tip Info Timeout InfoTitle '
                              'InfoFlags')

NIN_BALLOONSHOW = win32con.WM_USER + 2
NIN_BALLOONHIDE = win32con.WM_USER + 3
NIN_BALLOONTIMEOUT = win32con.WM_USER + 4
NIN_BALLOONUSERCLICK = win32con.WM_USER + 5

class TrayIconWin(object):
    def __init__(self, winname="Taskbar Demo", clsname="PythonTaskbarDemo",
                 iconpath="J:\\temp\\TBI_src\\carhome.ico"):
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_COMMAND: self.OnCommand,
            win32con.WM_USER+20: self.OnTaskbarNotify,
            }
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = clsname
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        hwnd = self.hwnd = CreateWindow( classAtom, winname, style,
                                         0, 0, win32con.CW_USEDEFAULT, 
                                         win32con.CW_USEDEFAULT, 
                                         0, 0, hinst, None)
        UpdateWindow(hwnd)
        # Load icon
        iconPathName = os.path.abspath(iconpath)
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        hicon = LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        # show tray icon
        nid = PyNOTIFYICONDATA(hwnd, 0, NIF_ICON | NIF_MESSAGE | NIF_TIP, 
                               win32con.WM_USER + 20,
                               hicon, winname, "", 0, "", 0)
        Shell_NotifyIcon(NIM_ADD, nid)

    def show_msg(self, title=u"测试", msg=u"测试消息正常", type="info"):
        type_dict = dict(info=NIIF_INFO, warn=NIIF_WARNING,
                         warning=NIIF_WARNING, error=NIIF_ERROR)
        title = title.encode('gb18030') if isinstance(title, unicode) else title
        msg = msg.encode('gb18030') if isinstance(msg, unicode) else msg
        nid = PyNOTIFYICONDATA(self.hwnd, 0, NIF_INFO, 0,
                               0, "", msg, 0, title, type_dict.get(type, NIIF_INFO))
        Shell_NotifyIcon(NIM_MODIFY, nid)
        
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        print "Exit"
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.        

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam==win32con.WM_LBUTTONUP or lparam==win32con.WM_RBUTTONUP:
            print "Click."
            menu = CreatePopupMenu()
            AppendMenu( menu, win32con.MF_STRING, 1024, u"测试".encode('gbk'))
            AppendMenu( menu, win32con.MF_STRING, 1026, u"今日预报".encode('gbk'))
            AppendMenu( menu, win32con.MF_STRING, 1025, u"退出".encode('gbk'))
            pos = GetCursorPos()
            SetForegroundWindow(self.hwnd)
            TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], 
                           pos[1],0, self.hwnd, None)
            PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
            return 1
        elif lparam == NIN_BALLOONUSERCLICK:
            print "You Clicked Balloon"

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = LOWORD(wparam)
        if id == 1024:
            self.show_msg()
        elif id == 1025:
            print "Goodbye"
            DestroyWindow(self.hwnd)
        elif id == 1026:
            self.update_weather()
        else:
            print "OnCommand for ID", id

    def update_weather(self):
        import urllib, json
        data = urllib.urlopen("http://www.weather.com.cn/data/cityinfo/101070101.html")
        data = json.load(data)
        info = data[u'weatherinfo']
        title = u"%(city)s 今日天气" % info
        msg =  u"%(weather)s\n气温: %(temp1)s / %(temp2)s" % info
        self.show_msg(title, msg)

if __name__ == '__main__':
    w = TrayIconWin()
    w.show_msg("Title", "Text here")
    import platform
    print(platform.architecture())
    PumpMessages()
