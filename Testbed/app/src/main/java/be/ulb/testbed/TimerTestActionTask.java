package be.ulb.testbed;

import android.os.Handler;
import android.util.Log;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.ArrayList;

import be.ulb.testbed.sensor.CustomWifiManager;

/**
 * Manager timer to execute action
 */
public class TimerTestActionTask extends Thread {

    private static final String TAG = "TimerTask";

    private final ArrayList<TestAction> listAction;
    private final CustomWifiManager customWifiManager;
    private final Handler handler;
    private int currentActionId;
    private float currentTiming;

    public TimerTestActionTask(final ArrayList<TestAction> listAction, final CustomWifiManager customWifiManager) {
        this.listAction = listAction;
        this.customWifiManager = customWifiManager;
        currentActionId = 0;

        handler = new Handler();

        start();
    }

    @Override
    public void run() {
        // First wait
        try {
            Thread.sleep(2000); // 2 seconds
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        while(currentActionId < listAction.size()) {
            final TestAction currentAction = listAction.get(currentActionId);
            Log.d(TAG, "Try to send packet");
            sendUdpPacket();
            currentAction.executeAction();

            // Wait a defined time
            currentTiming = 0; // In half second
            while (currentTiming < (currentAction.getTimer() * 2)) {
                currentTiming += 1;

                // Update the progress bar and display the
                //current value in the text view
                handler.post(new Runnable() {
                    public void run() {
                        final int timingToPercent = Math.round((currentTiming / (currentAction.getTimer()*2)) * 100);
                        currentAction.getProgressBar().setProgress(timingToPercent);
                    }
                });

                try {
                    Thread.sleep(500); // 0.5 second
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            ++currentActionId; // Get next action
        }
    }

    private void sendUdpPacket() {
        String messageStr = "Ping " + currentActionId;
        int server_port = 12345;
        try {
            final DatagramSocket socket = new DatagramSocket();

            final InetAddress wifiRouter = customWifiManager.getWifiIpAddress();

            final int msg_length = messageStr.length();
            final byte[] message = messageStr.getBytes();

            final DatagramPacket packet = new DatagramPacket(message, msg_length,wifiRouter,server_port);

            socket.send(packet);
            Log.i(TAG, "Send packet to " + wifiRouter.getHostAddress());

        } catch (IOException e) {
            Log.w(TAG, "Problem to send packet", e);
            // e.printStackTrace();
            // TODO add message
        }
    }

}
