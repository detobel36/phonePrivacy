package be.ulb.testbed;

import android.bluetooth.BluetoothAdapter;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.LocationManager;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Handler;
import android.provider.Settings;
import android.util.Log;
import android.widget.ProgressBar;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";

    private WifiManager wifiManager = null;
    private BluetoothAdapter bluetoothManager = null;
    private LocationManager locationManager = null;

    private Handler handler = new Handler();

    private int totalStep = 6;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final Context context = getApplicationContext();

        // Check Wifi
        final boolean wifiAvailable = context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_WIFI);
        if (wifiAvailable) {
            Log.d(TAG, "Wifi on this device");
            wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
        } else {
            Log.w(TAG, "No Wifi on this device");
        }

        // Check bluetooth
        final boolean bluetoothAvailable = context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH);
        if (bluetoothAvailable) {
            Log.d(TAG, "Bluetooth on this device");
        } else {
            Log.w(TAG, "No Bluetooth on this device");
        }
        bluetoothManager = BluetoothAdapter.getDefaultAdapter();

        // Check location
        final boolean locationAvailable = context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_LOCATION);
        if (locationAvailable) {
            Log.d(TAG, "Location system on this device");
        } else {
            Log.w(TAG, "No Location system on this device");
        }
        locationManager = (LocationManager) context.getSystemService(Context.LOCATION_SERVICE);

        launchTimer();
    }

    private void launchTimer() {
        final int maxTiming = 30;
        new Thread(new Runnable() {
            float currentTiming = 0;
            int currentStep = 0;

            public void run() {
                // First wait
                try {
                    Thread.sleep(2000); // 2 seconds
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                while(currentStep < totalStep) {
                    executeAction(currentStep);

                    // Wait a defined time
                    while (currentTiming < maxTiming) {
                        currentTiming += 1;
                        // Update the progress bar and display the
                        //current value in the text view
                        handler.post(new Runnable() {
                            public void run() {
                                final int timingToPercent = Math.round((currentTiming / maxTiming) * 100);
                                getCurrentProgressBar(currentStep).setProgress(timingToPercent);
                                Log.d(TAG, "Counter: " + timingToPercent);
                            }
                        });
                        try {
                            Thread.sleep(1000); // 1 second
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }

                    currentTiming = 0;
                    ++currentStep;
                }
            }
        }).start();
    }

    /**
     * Allow to change the Wifi Status
     *
     * @param activate True to enable, False to disable wifi
     */
    private void setWifiStatus(final boolean activate) {
        wifiManager.setWifiEnabled(activate);
    }

    private void setBluetoothStatus(final boolean activate) {
        if(activate) {
            bluetoothManager.enable();
        } else {
            bluetoothManager.disable();
        }
    }

    private void setLocationOn() {
        final Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
        startActivity(intent);
    }

    private ProgressBar getCurrentProgressBar(final int curentStep) {
        switch (curentStep) {
            case 0:
                return findViewById(R.id.progressBarWifiON);

            case 1:
                return findViewById(R.id.progressBarBluetoothON);

            case 2:
                return findViewById(R.id.progressBarBluetoothOFF);

            case 3:
                return findViewById(R.id.progressBarLocationON);

            case 4:
                return findViewById(R.id.progressBarWifiOFF);

            case 5:
                return findViewById(R.id.progressBarWifiON2);
        }

        return null;
    }

    private void executeAction(final int currentStep) {
        switch (currentStep) {
            case 0: // Enable wifi
                setWifiStatus(true);
                break;

            case 1: // Bluetooth on
                setBluetoothStatus(true);
                break;

            case 2: // Bluetooth off
                setBluetoothStatus(false);
                break;

            case 3: // Location on
                setLocationOn();
                break;

            case 4: // Disable wifi
                setWifiStatus(false);
                break;

            case 5: // Enable wifi
                setWifiStatus(true);
                break;
        }
    }

}
