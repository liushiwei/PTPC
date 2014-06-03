package com.george.ptpc.json;


public class Device {
	public static final int DEVICE_TYPE_ANDROID_PHONE = 0x00;
	public static final int DEVICE_TYPE_ANDROID_PAD = 0x01;
	public static final int DEVICE_TYPE_ANDROID_DEVICE = 0x02;
	public static final int DEVICE_TYPE_IOS_PHONE = 0x10;
	public static final int DEVICE_TYPE_IOS_PAD = 0x11;
	public static final int DEVICE_TYPE_IOS_DEVICE = 0x12;
	public static final int DEVICE_TYPE_WIN_PHONE = 0x20;
	public static final int DEVICE_TYPE_WIN_PAD = 0x21;
	public static final int DEVICE_TYPE_WIN_DEVICE = 0x22;
	
	private int DeviceType = DEVICE_TYPE_ANDROID_PHONE;
	private int Battery = 0;
	private int UnReadMessages = 0;
	private String Mac ;
	private int PhoneCall = 0;
	private String Name = "Unknown";
	
	public int getDeviceType() {
		return DeviceType;
	}
	public void setDeviceType(int deviceType) {
		DeviceType = deviceType;
	}
	public int getBattery() {
		return Battery;
	}
	public void setBattery(int battery) {
		Battery = battery;
	}
	public int getUnReadMessages() {
		return UnReadMessages;
	}
	public void setUnReadMessages(int unReadMessages) {
		UnReadMessages = unReadMessages;
	}
	public String getMac() {
		return Mac;
	}
	public void setMac(String mac) {
		Mac = mac;
	}
	public int getPhoneCall() {
		return PhoneCall;
	}
	public void setPhoneCall(int phoneCall) {
		PhoneCall = phoneCall;
	}
	public String getName() {
		return Name;
	}
	public void setName(String name) {
		Name = name;
	}
	
	
	

}
