// Copyright 2020 The Chromium Authors. All rights reserved.
package org.kivy.plugins.messaging;


import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.core.app.JobIntentService;

import com.google.firebase.messaging.RemoteMessage;

import java.util.Map;
import java.util.concurrent.CountDownLatch;

public class KivyFirebaseMessagingBackgroundService extends JobIntentService {
    private static final String TAG = "KVFireMsgService";

    /**
     * Schedule the message to be handled by the {@link KivyFirebaseMessagingBackgroundService}.
     */
    public static void enqueueMessageProcessing(Context context, Intent messageIntent) {
        enqueueWork(
                context,
                KivyFirebaseMessagingBackgroundService.class,
                KivyFirebaseMessagingUtils.JOB_ID,
                messageIntent);
    }

    @Override
    public void onCreate() {
        super.onCreate();
        KivyFirebaseMessagingBackgroundExecutor.startBackgroundPythonService();
    }

    @Override
    protected void onHandleWork(@NonNull final Intent intent) {


        // There were no pre-existing callback requests. Execute the callback
        // specified by the incoming intent.
        final CountDownLatch latch = new CountDownLatch(1);

        new Handler(getMainLooper())
                .post(new Runnable() {
                          @Override
                          public void run() {
                              RemoteMessage remoteMessage =
                                      intent.getParcelableExtra(KivyFirebaseMessagingUtils.EXTRA_REMOTE_MESSAGE);
                              if (remoteMessage != null) {
                                  Map<String, Object> remoteMessageMap =
                                          KivyFirebaseMessagingUtils.remoteMessageToMap(remoteMessage);
                                  remoteMessageMap.put("unique_key", Math.random() + "");
                                  PlatformIntermediate.addbackroundMessage(remoteMessageMap, ContextHolder.getApplicationContext());
                              }
                              // End
                              latch.countDown();
                          }
                      }
                );

        try {
            latch.await();
        } catch (InterruptedException ex) {
            Log.i(TAG, "Exception waiting to execute Python callback", ex);
        }
    }
}