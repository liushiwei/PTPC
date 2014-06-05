#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from wx import Icon
from autoid import AutoId
import itertools, glob  
from Device import Device

   
########################################################################
class SystemTray(wx.TaskBarIcon):
    #TBMENU_RESTORE = wx.NewId()
    #TBMENU_CLOSE   = wx.NewId()
    #TBMENU_CHANGE  = wx.NewId()
    #TBMENU_REMOVE  = wx.NewId()
    ANDROID = 0;
    
    devices = []
    
    #----------------------------------------------------------------------
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.id = AutoId()
        # Set the image
        self.icons = itertools.cycle(glob.glob('*.ico'))  
        self.tbIcon = Icon(self.icons.next())
             
        self.SetIcon(self.tbIcon, "PhoneToPc ")
        
        # bind some evts
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.id.TBMENU_CLOSE)
        self.Bind(wx.EVT_MENU, self.OnChangeIcon, id=self.id.SUBMENU_CHANGE_ICON)
        self.Bind(wx.EVT_MENU, self.OnShowFrame, id=self.id.TBMENU_RESTORE)
        self.Bind(wx.EVT_MENU, self.OnBatteryChange, id=self.id.SUBMENU_CHANGE_BATTERY)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)
        
    #----------------------------------------------------------------------
    def CreatePopupMenu(self, evt=None):
        """
        This method is called by the base class when it needs to popup
        the menu for the default EVT_RIGHT_DOWN evt.  Just create
        the menu how you want it and return it from this function,
        the base class takes care of the rest.
        """
        print("CreatePopupMenu ",self.devices)
        menu = wx.Menu()
        menu.Append(self.id.TBMENU_RESTORE, "Open Program")
        menu.Append(self.id.TBMENU_CHANGE, "Show all the Items")
        for device in self.devices:
            print("device :",device.Name,device.Battery,device.UnReadMessages,device.PhoneCall)
            sub_menu = wx.Menu()
            sub_menu.Append(self.id.SUBMENU_BATTER,"Battery: "+str(device.Battery)+"%")
            #sub_menu.Append(self.id.SUBMENU_CHANGE_ICON,"Change Icon")
            sub_menu.Append(self.id.SUBMENU_MESSAGE,"Message: "+str(device.UnReadMessages))
            sub_menu.Append(self.id.SUBMENU_PHONECALL,"Missed Call: "+str(device.PhoneCall))
            menu.AppendSubMenu(sub_menu,device.Name)
        menu.AppendSeparator()
        menu.Append(self.id.TBMENU_CLOSE,   "Exit Program")
        return menu
        
    def addDevice(self,device):
        print("addDevice ",device)
        if len(self.devices)==0:
            self.devices.append(device)
            return
        
        for i in range(len(self.devices)):
            if device.Mac == self.devices[i].Mac:
                print("device mac equse ",self.devices[i].Mac)
                self.devices[i] = device
                print("device mac equse ",self.devices[i].Mac,self.devices[i].UnReadMessages,self.devices[i].PhoneCall)
        if i== len(self.devices):
            print("device append ",device)
            self.devices.append(device)
    #----------------------------------------------------------------------
    def OnTaskBarActivate(self, evt):
        """"""
        pass
     #----------------------------------------------------------------------
    def OnChangeIcon(self, evt):  
        self.tbIcon = Icon(self.icons.next())
        self.SetIcon(self.tbIcon, "Icon changed")
        self.ShowBalloon("Test","Icon changed",5,wx.ICON_WARNING);
    #----------------------------------------------------------------------
    def OnTaskBarClose(self, evt):
        """
        Destroy the taskbar icon and frame from the taskbar icon itself
        """
        self.frame.Close()
        
    #----------------------------------------------------------------------
    def OnTaskBarLeftClick(self, evt):
        """
        Create the right-click menu
        """
        self.menu = self.CreatePopupMenu()
        self.PopupMenu(self.menu)
        self.menu.Destroy()
        
    def OnShowFrame(self, evt):
        """
        Show Frame
        """
        self.frame.Show(True)
        
    def OnBatteryChange(self,evt):
        """
        change battery
        """
        print "Can't find icon file - using default." ,self.better.GetText(); 
        self.better.SetText("60%")
        self.better.SetItemLabel("60%")
        print "Can't find icon file - using default." ,self.menu.FindItemById(self.id.SUBMENU_BETTER).GetText(); 
        self.menu.SetLabel(self.id.SUBMENU_BETTER,"60%")
        self.menu.UpdateUI()
########################################################################
class MyForm(wx.Frame):
    
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial", size=(500,500))
        self.panel = wx.Panel(self)
        self.tbIcon = SystemTray(self)
        device = Device()
        self.tbIcon.addDevice(device)
        self.tbIcon.ShowBalloon("Test","Test",5,wx.ICON_WARNING);
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
    #----------------------------------------------------------------------
    def onClose(self, evt):
        """
        Destroy the taskbar icon and the frame
        """
        self.tbIcon.RemoveIcon()
        self.tbIcon.Destroy()
        self.Destroy()

#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm().Show(False)
    app.MainLoop()