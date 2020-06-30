package be.ulb.testbed;

import android.content.Context;
import android.content.pm.PackageManager;
import android.net.wifi.WifiManager;
import android.util.Log;

/**
 * @singleton
 */
public class SensorManager {

    private static SensorManager instance = null;
    private static String TAG = "SensorManager";

    private final WifiManager wifiManager;

    private SensorManager(final Context context) {

        final boolean wifiAvailable = wifiFeatureExist(context);
        if (wifiAvailable) {
            Log.d(TAG, "Wifi on this device");
            wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
        } else {
            Log.w(TAG, "No Wifi on this device");
            wifiManager = null;
        }

    }

    private boolean wifiFeatureExist(final Context context) {
        return context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_WIFI);
    }

    public boolean isWifiEnable() {
        return wifiManager != null && wifiManager.isWifiEnabled();
    }

    public

    public static SensorManager getSensorManager(final Context context) {
        if(instance == null) {
            instance = new SensorManager(context);
        }
        return instance;
    }

}
