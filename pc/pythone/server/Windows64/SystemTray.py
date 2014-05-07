#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from wx import Icon
from autoid import AutoId
import itertools, glob  
     
   
########################################################################
class SystemTray(wx.TaskBarIcon):
    #TBMENU_RESTORE = wx.NewId()
    #TBMENU_CLOSE   = wx.NewId()
    #TBMENU_CHANGE  = wx.NewId()
    #TBMENU_REMOVE  = wx.NewId()
    
    
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
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)
        
    #----------------------------------------------------------------------
    def CreatePopupMenu(self, evt=None):
        """
        This method is called by the base class when it needs to popup
        the menu for the default EVT_RIGHT_DOWN evt.  Just create
        the menu how you want it and return it from this function,
        the base class takes care of the rest.
        """
        menu = wx.Menu()
        menu.Append(self.id.TBMENU_RESTORE, "Open Program")
        menu.Append(self.id.TBMENU_CHANGE, "Show all the Items")
        sub_menu = wx.Menu()
        sub_menu.Append(self.id.SUBMENU_BETTER,"50%")
        sub_menu.Append(self.id.SUBMENU_CHANGE_ICON,"Change Icon")
        menu.AppendSubMenu(sub_menu,"Device1")
        menu.AppendSeparator()
        menu.Append(self.id.TBMENU_CLOSE,   "Exit Program")
        return menu
        
    #----------------------------------------------------------------------
    def OnTaskBarActivate(self, evt):
        """"""
        pass
     #----------------------------------------------------------------------
    def OnChangeIcon(self, evt):
        self.icons = itertools.cycle(glob.glob('../*.ico'))  
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
        menu = self.tbIcon.CreatePopupMenu()
        self.PopupMenu(menu)
        menu.Destroy()
        
########################################################################
class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial", size=(500,500))
        panel = wx.Panel(self)
        self.tbIcon = SystemTray(self)
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
    frame = MyForm().Show()
    app.MainLoop()