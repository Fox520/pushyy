// Copyright 2020 The Chromium Authors. All rights reserved.
package org.kivy.plugins.messaging;

import android.content.Context;
import android.util.Log;

public class ContextHolder {
    private static Context applicationContext;

    public static Context getApplicationContext() {
        return applicationContext;
    }

    public static void setApplicationContext(Context applicationContext) {
        Log.d("KVFireContextHolder", "received application context.");
        ContextHolder.applicationContext = applicationContext;
    }
}