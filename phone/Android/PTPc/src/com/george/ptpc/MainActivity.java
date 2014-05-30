package com.george.ptpc;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;


public class MainActivity extends Activity {
	MyBatteryReceiver mbr = null;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main_layout);
		Button button = (Button) findViewById(R.id.button1);
		mbr = new MyBatteryReceiver();
		button.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View v) {
				new Thread(){

					@Override
					public void run() {
						send("Hello UDP");
						super.run();
					}
					
				}.start();;
				
			}
		});
		
		IntentFilter filter = new IntentFilter(Intent.ACTION_BATTERY_CHANGED);	//还有3个Action说说得
		registerReceiver(mbr, filter);		
	}
	
	public static void send(String message) {  
        message = (message == null ? "Hello IdeasAndroid!" : message);  
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
        int msg_length = message.length();  
        byte[] messageByte = message.getBytes();  
        DatagramPacket p = new DatagramPacket(messageByte, msg_length, local,  
                server_port);  
        try {  
            s.send(p); 
            Log.e("UDP", "Send :"+message);
        } catch (IOException e) {  
            e.printStackTrace();  
        }  
    } 
	
	private class MyBatteryReceiver extends BroadcastReceiver{
		@Override
		public void onReceive(Context context, Intent intent) {		//重写onReceiver方法
			int current = intent.getExtras().getInt("level");		//获得当前电量
			int total = intent.getExtras().getInt("scale");			//获得总电量
			int percent = current*100/total;		//计算百分比
			TextView tv = (TextView)findViewById(R.id.battery);			//获得TextView对象
			tv.setText("现在的电量是："+percent+"%。");				//设置TextView显示的内容
			Log.e("MyBatteryReceiver", "现在的电量是："+percent+"%。");
		}
    }

}
