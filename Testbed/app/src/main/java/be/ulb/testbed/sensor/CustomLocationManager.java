package be.ulb.testbed.sensor;

import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.HandlerThread;
import android.os.Looper;
import android.util.Log;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;

/**
 * Interface to manage Location system
 */
public class CustomLocationManager implements SensorManager {

    private static final String TAG = "LocationManager";

    private static Location lastLocation = null;

    private final LocationManager locationManager;
    private final Context context;
    private LocationListener listener;
    private HandlerThread thread;
    private final FusedLocationProviderClient fusedLocationClient;

    public CustomLocationManager(final Context context, final AppCompatActivity activity) {
        this.context = context;

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

            thread = new HandlerThread("LoggerThread");
            thread.start();
            final Looper looper = thread.getLooper();
            listener = new mLocationListener();

            requestProviderUpdates(LocationManager.GPS_PROVIDER, listener, looper);

        }
    }

    private void requestProviderUpdates(String provider, LocationListener listener, Looper looper) {
        try {
            if (locationManager.isProviderEnabled(provider)) {
//                locationManager.requestSingleUpdate(provider, listener, looper);
                long minTimeMillis = 1000; // 1 second
                int minDistance = 1;
                locationManager.requestLocationUpdates(provider, minTimeMillis, minDistance, listener, looper);
                Log.d(TAG, "[requestProviderUpdates success: " + provider + "]");
            } else {
                Log.d(TAG, "[requestProviderUpdates disabled: " + provider + "]");
            }
        } catch (SecurityException e) {
            Log.d(TAG, "[requestProviderUpdates permission denied: " + provider + "]");
        }
    }

    @Override
    public void disable() {
        // Could not disable location with application

        // Display latest location
        new Handler(Looper.getMainLooper()).post(new Runnable() {
             @Override
             public void run() {
                 Toast.makeText(context, "Location [0]: " + lastLocation, Toast.LENGTH_SHORT).show();
             }
         });

        // Disable the update
        locationManager.removeUpdates(listener);

        if (thread != null) {
            thread.interrupt();
            thread = null;
        }
    }

    private class mLocationListener implements LocationListener {

        @Override
        public void onLocationChanged(Location location) {
            Log.d(TAG, "[location changed: " + location + "]");
            lastLocation = location;
            Toast.makeText(context, "Location [1]: " + location, Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onProviderDisabled(String provider) {
            Log.d(TAG, "[location provider " + provider + " disabled]");
            Log.d(TAG, "Latest location: " + lastLocation);
            Toast.makeText(context, "Location [2]: " + lastLocation, Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onProviderEnabled(String provider) {
            Log.d(TAG, "[location provider " + provider + " enabled]");
            Log.d(TAG, "Latest location: " + lastLocation);
            Toast.makeText(context, "Location [3]: " + lastLocation, Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {
            Log.d(TAG, "Latest location: " + lastLocation);
            Toast.makeText(context, "Location [4]: " + lastLocation, Toast.LENGTH_SHORT).show();
        }

    }

}
