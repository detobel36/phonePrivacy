package be.ulb.testbed.sensor;

import android.content.Context;
import android.content.pm.PackageManager;
import android.net.wifi.WifiManager;
import android.util.Log;

import java.math.BigInteger;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.nio.ByteOrder;

/**
 * Interface to manage Wifi
 */
public class CustomWifiManager implements SensorManager {

    private static final String TAG = "WifiManager";

    private final WifiManager wifiManager;

    public CustomWifiManager(final Context context) {
        final boolean wifiAvailable = context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_WIFI);
        if (wifiAvailable) {
            Log.d(TAG, "Wifi available on this device");
            wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
        } else {
            Log.w(TAG, "No Wifi on this device");
            wifiManager = null;
        }
    }

    @Override
    public void enable() {
        if(wifiManager != null) {
            wifiManager.setWifiEnabled(true);
        }
    }

    @Override
    public void disable() {
        if(wifiManager != null) {
            wifiManager.setWifiEnabled(false);
        }
    }

    public InetAddress getWifiIpAddress() {
        InetAddress ipAddressInet = null;

        if(wifiManager != null) {
            int ipAddress = wifiManager.getDhcpInfo().serverAddress;

            // Convert little-endian to big-endianif needed
            if (ByteOrder.nativeOrder().equals(ByteOrder.LITTLE_ENDIAN)) {
                ipAddress = Integer.reverseBytes(ipAddress);
            }

            final byte[] ipByteArray = BigInteger.valueOf(ipAddress).toByteArray();

            try {
                ipAddressInet = InetAddress.getByAddress(ipByteArray);
            } catch (UnknownHostException ex) {
                // TODO print message
            }
        }

        return ipAddressInet;
    }

}
