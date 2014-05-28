#!/usr/bin/python
# -*- coding: utf-8 -*-

class Device():
    """设备类，用来定义每个连接到服务器的设备
    
       类中包括设备的类型，当前状态等信息"""
    DEVICE_TYPE_ANDROID_PHONE = 0x00;
    DEVICE_TYPE_ANDROID_PAD = 0x01;
    DEVICE_TYPE_ANDROID_DEVICE = 0x02;
    DEVICE_TYPE_IOS_PHONE = 0x10;
    DEVICE_TYPE_IOS_PAD = 0x11;
    DEVICE_TYPE_IOS_DEVICE = 0x12;
    DEVICE_TYPE_WIN_PHONE = 0x20;
    DEVICE_TYPE_WIN_PAD = 0x21;
    DEVICE_TYPE_WIN_DEVICE = 0x22;
    
    DeviceType = DEVICE_TYPE_ANDROID_PHONE
    Battery = 0
    UnReadMessages = 0
    PhoneCall = 0
    Name = "Unknown"
    