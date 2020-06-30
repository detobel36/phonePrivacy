package be.ulb.testbed;

import android.content.Context;
import android.content.pm.PackageManager;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;

public class CheckConfigurationActivity extends AppCompatActivity {

    private static final String TAG = "CheckConfigActivity";

    private WifiManager wifiManager = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_check_config);
    }

    private void checkWifi() {
        final Context context = getApplicationContext();

        final boolean wifiAvailable = context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_WIFI);
        if (wifiAvailable) {
            Log.d(TAG, "Wifi on this device");
            wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
        } else {
            Log.w(TAG, "No Wifi on this device");
        }
    }

}
