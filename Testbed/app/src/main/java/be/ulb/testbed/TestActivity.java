package be.ulb.testbed;

import android.content.Context;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;

import be.ulb.testbed.sensor.CustomBluetoothManager;
import be.ulb.testbed.sensor.CustomLocationManager;
import be.ulb.testbed.sensor.CustomWifiManager;

public class TestActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";
    private static TestActivity instance;  // TODO remove

    private int currentActionId = 0;
    private final ArrayList<TestAction> listAction = new ArrayList<TestAction>();

    private Handler handler = new Handler();

    private int totalStep = 6;

    private CustomWifiManager customWifiManager;
    private CustomBluetoothManager customBluetoothManager;
    private CustomLocationManager customLocationManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        initSensor();

        setContentView(R.layout.activity_test);

        listAction.add(new TestAction(R.id.progressBarWifiON) {
            @Override
            public void executeAction() {
                customWifiManager.enable();
            }
        });

        listAction.add(new TestAction(R.id.progressBarBluetoothON) {
            @Override
            public void executeAction() {
                customBluetoothManager.enable();
            }
        });

        listAction.add(new TestAction(R.id.progressBarBluetoothOFF) {
            @Override
            public void executeAction() {
                customBluetoothManager.disable();
            }
        });

        listAction.add(new TestAction(R.id.progressBarLocationON) {
            @Override
            public void executeAction() {
                customLocationManager.enable();
            }
        });

        listAction.add(new TestAction(R.id.progressBarWifiOFF) {
            @Override
            public void executeAction() {
                customWifiManager.disable();
            }
        });

        listAction.add(new TestAction(R.id.progressBarWifiON2) {
            @Override
            public void executeAction() {
                customWifiManager.enable();
            }
        });


        // Check Wifi
//        final boolean wifiAvailable = context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_WIFI);
//        if (wifiAvailable) {
//            Log.d(TAG, "Wifi on this device");
//            wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
//        } else {
//            Log.w(TAG, "No Wifi on this device");
//        }

        // Check bluetooth
//        final boolean bluetoothAvailable = context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH);
//        if (bluetoothAvailable) {
//            Log.d(TAG, "Bluetooth on this device");
//        } else {
//            Log.w(TAG, "No Bluetooth on this device");
//        }
//        bluetoothManager = BluetoothAdapter.getDefaultAdapter();

        // Check location
//        final boolean locationAvailable = context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_LOCATION);
//        if (locationAvailable) {
//            Log.d(TAG, "Location system on this device");
//        } else {
//            Log.w(TAG, "No Location system on this device");
//        }
//        locationManager = (LocationManager) context.getSystemService(Context.LOCATION_SERVICE);

        launchTimer();
    }

    private void initSensor() {
        final Context appContext = getApplicationContext();
        customWifiManager = new CustomWifiManager(appContext);
        customBluetoothManager = new CustomBluetoothManager(appContext);
        customLocationManager = new CustomLocationManager(appContext, this);
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
//                    executeAction(currentStep);

                    // Wait a defined time
                    while (currentTiming < maxTiming) {
                        currentTiming += 1;
                        // Update the progress bar and display the
                        //current value in the text view
                        handler.post(new Runnable() {
                            public void run() {
                                final int timingToPercent = Math.round((currentTiming / maxTiming) * 100);
//                                getCurrentProgressBar(currentStep).setProgress(timingToPercent);
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

//    private void setBluetoothStatus(final boolean activate) {
//        if(activate) {
//            bluetoothManager.enable();
//        } else {
//            bluetoothManager.disable();
//        }
//    }

//    private void setLocationOn() {
//        final Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
//        startActivity(intent);
//    }

//    private ProgressBar getCurrentProgressBar(final int curentStep) {
//        switch (curentStep) {
//            case 0:
//                return findViewById(R.id.progressBarWifiON);
//
//            case 1:
//                return findViewById(R.id.progressBarBluetoothON);
//
//            case 2:
//                return findViewById(R.id.progressBarBluetoothOFF);
//
//            case 3:
//                return findViewById(R.id.progressBarLocationON);
//
//            case 4:
//                return findViewById(R.id.progressBarWifiOFF);
//
//            case 5:
//                return findViewById(R.id.progressBarWifiON2);
//        }
//
//        return null;
//    }

//    private void executeAction(final int currentStep) {
//        switch (currentStep) {
//            case 0: // Enable wifi
//                setWifiStatus(true);
//                break;
//
//            case 1: // Bluetooth on
//                setBluetoothStatus(true);
//                break;
//
//            case 2: // Bluetooth off
//                setBluetoothStatus(false);
//                break;
//
//            case 3: // Location on
//                setLocationOn();
//                break;
//
//            case 4: // Disable wifi
//                setWifiStatus(false);
//                break;
//
//            case 5: // Enable wifi
//                setWifiStatus(true);
//                break;
//        }
//    }

}
