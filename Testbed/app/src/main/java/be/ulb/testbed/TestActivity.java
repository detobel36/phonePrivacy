package be.ulb.testbed;

import android.content.Context;
import android.os.Bundle;
import android.view.WindowManager;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;

import be.ulb.testbed.sensor.CustomBluetoothManager;
import be.ulb.testbed.sensor.CustomLocationManager;
import be.ulb.testbed.sensor.CustomWifiManager;

public class TestActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";


    private final ArrayList<TestAction> listAction = new ArrayList<TestAction>();

    private CustomWifiManager customWifiManager;
    private CustomBluetoothManager customBluetoothManager;
    private CustomLocationManager customLocationManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        initSensor();

        /*
        TextView myAwesomeTextView = (TextView)findViewById(R.id.textViewBlueetoothOFF);
        myAwesomeTextView.setText("Test");

        https://stackoverflow.com/a/6661379
        */

        setContentView(R.layout.activity_test);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        listAction.add(new TestAction(this, R.id.progressBarWifiON, 30) {
            @Override
            public void executeAction() {
                customWifiManager.enable();
            }
        });

        listAction.add(new TestAction(this, R.id.progressBarBluetoothON, 30) {
            @Override
            public void executeAction() {
                customBluetoothManager.enable();
            }
        });

        listAction.add(new TestAction(this, R.id.progressBarBluetoothOFF, 30) {
            @Override
            public void executeAction() {
                customBluetoothManager.disable();
            }
        });

        listAction.add(new TestAction(this, R.id.progressBarLocationON, 30) {
            @Override
            public void executeAction() {
                customLocationManager.enable();
            }
        });

        listAction.add(new TestAction(this, R.id.progressBarLocationOFF, 30) {
            @Override
            public void executeAction() {
                customLocationManager.disable();
            }
        });


        listAction.add(new TestAction(this, R.id.progressBarWifiOFF, 30) {
            @Override
            public void executeAction() {
                customWifiManager.disable();
            }
        });

        listAction.add(new TestAction(this, R.id.progressBarWifiON2, 30) {
            @Override
            public void executeAction() {
                customWifiManager.enable();
            }
        });

        new TimerTestActionTask(listAction, customWifiManager);
    }

    private void initSensor() {
        final Context appContext = getApplicationContext();
        customWifiManager = new CustomWifiManager(appContext);
        customBluetoothManager = new CustomBluetoothManager(appContext);
        customLocationManager = new CustomLocationManager(appContext, this);
    }

}
