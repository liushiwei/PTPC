package com.george.ptpc;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.HashMap;
import java.util.Map;

import android.app.Application;
import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.database.ContentObserver;
import android.database.Cursor;
import android.net.Uri;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Handler;
import android.os.IBinder;
import android.os.Message;
import android.provider.CallLog;
import android.provider.CallLog.Calls;
import android.telephony.PhoneStateListener;
import android.telephony.TelephonyManager;
import android.util.Log;

import com.george.ptpc.json.Device;
import com.google.gson.Gson;

public class PTPCService extends Service {

	MyBatteryReceiver mbr = null;
	private String mac;
	private int percent;
	private Handler mHandler = new Handler() {

		@Override
		public void handleMessage(Message msg) {
			super.handleMessage(msg);
			Gson gson = new Gson();
			Map<String, Object> map = new HashMap<String, Object>();
			switch (msg.what) {
			case 0:
				Device device = new Device();
				device.setMac(mac);
				device.setBattery(percent);
				device.setPhoneCall(readMissCall());
				device.setUnReadMessages(getNewSmsCount());
				map.put("cmd", Commands.CMD_PTD_PHSTATUS);
				map.put("device", device);
				send(gson.toJson(map));
				mHandler.sendEmptyMessageDelayed(0, 5000);
				break;
				
			case 1:
				map.put("cmd", Commands.CMD_PTD_MISSEDCALL);
				map.put("phone_number", msg.obj);
				send(gson.toJson(map));
				mHandler.sendEmptyMessageDelayed(0, 5000);
				break;

			default:
				break;
			}
		}

	};

	@Override
	public void onCreate() {
		mbr = new MyBatteryReceiver();
		IntentFilter filter = new IntentFilter(Intent.ACTION_BATTERY_CHANGED); // 还有3个Action说说得
		registerReceiver(mbr, filter);

		final IntentFilter missed_call_filter = new IntentFilter();
		missed_call_filter
				.addAction("com.android.phone.NotificationMgr.MissedCall_intent");
		final Application application = getApplication();
		application.registerReceiver(new BroadcastReceiver() {
			@Override
			public void onReceive(Context context, Intent intent) {
				String action = intent.getAction();

				if (action != null
						&& "com.android.phone.NotificationMgr.MissedCall_intent"
								.equals(action)) {
					int mMissCallCount = intent.getExtras().getInt(
							"MissedCallNumber");
				}
			}
		}, missed_call_filter);
		registerObserver();
		mHandler.sendEmptyMessage(0);

		WifiManager manager = (WifiManager) getSystemService(Context.WIFI_SERVICE);
		WifiInfo info = manager.getConnectionInfo();
		mac = info.getMacAddress();
		TelephonyManager telManager = (TelephonyManager) this
				.getSystemService(TELEPHONY_SERVICE);
		// 手动注册对PhoneStateListener中的listen_call_state状态进行监听
		telManager.listen(new MyPhoneStateListener(),
				PhoneStateListener.LISTEN_CALL_STATE);
		super.onCreate();
	}
	
	private int phoneState  = TelephonyManager.CALL_STATE_IDLE;
	private String phoneNumber  ;

	/***
	 * 继承PhoneStateListener类，我们可以重新其内部的各种监听方法 然后通过手机状态改变时，系统自动触发这些方法来实现我们想要的功能
	 */
	class MyPhoneStateListener extends PhoneStateListener {

		@Override
		public void onCallStateChanged(int state, String incomingNumber) {
			switch (state) {
			case TelephonyManager.CALL_STATE_IDLE:
				// result+=" 手机空闲起来了  ";
				if(phoneState==TelephonyManager.CALL_STATE_RINGING){
					Log.e("Service", "有未接电话  ");
					mHandler.obtainMessage(1, phoneNumber).sendToTarget();
				}
				Log.e("Service", "手机空闲起来了  ");
				phoneState = TelephonyManager.CALL_STATE_IDLE;
				break;
			case TelephonyManager.CALL_STATE_RINGING:
				// result+="  手机铃声响了，来电号码:"+incomingNumber;
				Log.e("Service", "  手机铃声响了，来电号码:" + incomingNumber);
				phoneNumber = incomingNumber;
				phoneState = TelephonyManager.CALL_STATE_RINGING;
				break;
			case TelephonyManager.CALL_STATE_OFFHOOK:
				// result+=" 电话被挂起了 ";
				Log.e("Service", "电话被挂起了");
				phoneState = TelephonyManager.CALL_STATE_OFFHOOK;
			default:
				break;
			}
			super.onCallStateChanged(state, incomingNumber);
		}

	}

	@Override
	public IBinder onBind(Intent arg0) {
		// TODO Auto-generated method stub
		return null;
	}

	public static void send(String message) {
		final String msg = message;
		Thread sendThread = new Thread() {

			@Override
			public void run() {
				int server_port = 1224;
				DatagramSocket s = null;
				try {
					s = new DatagramSocket();
				} catch (SocketException e) {
					e.printStackTrace();
				}
				InetAddress local = null;
				try {
					// 换成服务器端IP
					local = InetAddress.getByName("255.255.255.255");
				} catch (UnknownHostException e) {
					e.printStackTrace();
				}
				int msg_length = msg.length();
				byte[] messageByte = msg.getBytes();
				DatagramPacket p = new DatagramPacket(messageByte, msg_length,
						local, server_port);
				try {
					s.send(p);
					Log.e("UDP", "Send :" + msg);
				} catch (IOException e) {
					e.printStackTrace();
				}
				super.run();
			}

		};
		sendThread.start();

	}

	private class MyBatteryReceiver extends BroadcastReceiver {
		@Override
		public void onReceive(Context context, Intent intent) { // 重写onReceiver方法
			int current = intent.getExtras().getInt("level"); // 获得当前电量
			int total = intent.getExtras().getInt("scale"); // 获得总电量
			percent = current * 100 / total; // 计算百分比
			Log.e("MyBatteryReceiver", "现在的电量是：" + percent + "%。");
		}
	}

	private ContentObserver newMmsContentObserver = new ContentObserver(
			new Handler()) {
		public void onChange(boolean selfChange) {
			int mNewSmsCount = getNewSmsCount() + getNewMmsCount();
		}
	};

	private void registerObserver() {
		unregisterObserver();
		getContentResolver().registerContentObserver(
				Uri.parse("content://sms"), true, newMmsContentObserver);
		getContentResolver().registerContentObserver(
				Uri.parse("content://mms-sms"), true, newMmsContentObserver);
	}

	private synchronized void unregisterObserver() {
		try {
			if (newMmsContentObserver != null) {
				getContentResolver().unregisterContentObserver(
						newMmsContentObserver);
			}
			if (newMmsContentObserver != null) {
				getContentResolver().unregisterContentObserver(
						newMmsContentObserver);
			}
		} catch (Exception e) {
			Log.e("MainActivity", "unregisterObserver fail");
		}
	}

	private int getNewSmsCount() {
		int result = 0;
		Cursor csr = getContentResolver().query(Uri.parse("content://sms"),
				null, "type = 1 and read = 0", null, null);
		if (csr != null) {
			result = csr.getCount();
			csr.close();
		}
		return result;
	}

	private int getNewMmsCount() {
		int result = 0;
		Cursor csr = getContentResolver().query(
				Uri.parse("content://mms/inbox"), null, "read = 0", null, null);
		if (csr != null) {
			result = csr.getCount();
			csr.close();
		}
		return result;
	}

	private int readMissCall() {
		int result = 0;
		Cursor cursor = getContentResolver().query(CallLog.Calls.CONTENT_URI,
				new String[] { Calls.TYPE }, " type=? and new=?",
				new String[] { Calls.MISSED_TYPE + "", "1" }, "date desc");

		if (cursor != null) {
			result = cursor.getCount();
			cursor.close();
		}
		return result;
	}

}
