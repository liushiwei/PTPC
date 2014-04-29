package com.george.ptpc;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;


public class MainActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main_layout);
		Button button = (Button) findViewById(R.id.button1);
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

}
