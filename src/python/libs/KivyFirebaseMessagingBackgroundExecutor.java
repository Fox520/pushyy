package org.kivy.plugins.messaging;

import android.util.Log;

import java.util.concurrent.atomic.AtomicBoolean;

public class KivyFirebaseMessagingBackgroundExecutor {
private static AtomicBoolean started = new AtomicBoolean(false);
    public static void startBackgroundPythonService() {

        Log.d("BackgroundExecutor", "Starting background service");
        com.waterfall.youtube.ServicePythonnotificationhandler.start(ContextHolder.getApplicationContext(), "");
        Log.d("BackgroundExecutor", "Background service started");

    }

}
