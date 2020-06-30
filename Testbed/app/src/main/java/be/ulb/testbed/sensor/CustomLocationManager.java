package be.ulb.testbed.sensor;

import android.content.Context;
import android.content.pm.PackageManager;
import android.location.LocationManager;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;

/**
 * Interface to manage Location system
 */
public class CustomLocationManager implements SensorManager {

    private static final String TAG = "LocationManager";
    private final LocationManager locationManager;
    private final FusedLocationProviderClient fusedLocationClient;

    public CustomLocationManager(final Context context, final AppCompatActivity activity) {
        final boolean locationAvailable = context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_LOCATION);
        if (locationAvailable) {
            Log.d(TAG, "Location system available on this device");
            locationManager = (LocationManager) context.getSystemService(Context.LOCATION_SERVICE);
        } else {
            Log.w(TAG, "No Location system on this device");
            locationManager = null;
        }

        fusedLocationClient = LocationServices.getFusedLocationProviderClient(activity);
    }

    @Override
    public void enable() {
        if(locationManager != null) {
            fusedLocationClient.getLastLocation();
        }
    }

    @Override
    public void disable() {
        // Could not disable location with application
    }

}
