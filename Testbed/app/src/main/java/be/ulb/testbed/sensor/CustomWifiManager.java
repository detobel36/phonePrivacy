package be.ulb.testbed.sensor;

import android.content.Context;
import android.content.pm.PackageManager;
import android.net.wifi.WifiManager;
import android.util.Log;

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

}
