package be.ulb.testbed.sensor;

import android.bluetooth.BluetoothAdapter;
import android.content.Context;
import android.content.pm.PackageManager;
import android.util.Log;

/**
 * Interface to manage Bluetooth
 */
public class CustomBluetoothManager implements SensorManager {

    private static final String TAG = "BluetoothManager";
    private final BluetoothAdapter bluetoothManager;

    public CustomBluetoothManager(final Context context) {
        final boolean bluetoothAvailable = context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH);
        if (bluetoothAvailable) {
            Log.d(TAG, "Bluetooth available on this device");
            bluetoothManager = BluetoothAdapter.getDefaultAdapter();
        } else {
            Log.w(TAG, "No Bluetooth on this device");
            bluetoothManager = null;
        }
    }

    @Override
    public void enable() {
        if(bluetoothManager != null) {
            bluetoothManager.enable();
        }
    }

    @Override
    public void disable() {
        if(bluetoothManager != null) {
            bluetoothManager.disable();
        }
    }
}
