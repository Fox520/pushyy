package org.kivy.plugins.messaging;


import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

import com.google.firebase.messaging.RemoteMessage;
import com.google.gson.Gson;

import java.util.HashMap;

import static org.kivy.plugins.messaging.PlatformIntermediate.backgroundMessages;

public class KivyFirebaseMessagingReceiver extends BroadcastReceiver {
    private static final String TAG = "FLTFireMsgReceiver";
    static HashMap<String, RemoteMessage> notifications = new HashMap<>();

    @Override
    public void onReceive(Context context, Intent intent) {
        Log.d(TAG, "broadcast received for message");
        if (ContextHolder.getApplicationContext() == null) {
            ContextHolder.setApplicationContext(context.getApplicationContext());
        }

        RemoteMessage remoteMessage = new RemoteMessage(intent.getExtras());

        // Store the RemoteMessage if the message contains a notification payload.
        if (remoteMessage.getNotification() != null) {
            notifications.put(remoteMessage.getMessageId(), remoteMessage);
            KivyFirebaseMessagingStore.getInstance().storeFirebaseMessage(remoteMessage);
        }

        //  |-> ---------------------
        //      App in Foreground
        //   ------------------------
        if (KivyFirebaseMessagingUtils.isApplicationForeground(context)) {
            Log.d(TAG, "Setting the foreground. BTW, title is " + remoteMessage.getNotification().getTitle());
            PlatformIntermediate.setForegroundMessage(KivyFirebaseMessagingUtils.remoteMessageToMap(remoteMessage));
            return;
        }

        //  |-> ---------------------
        //    App in Background/Quit
        //   ------------------------
        Log.d(TAG, "App in Background/Quit " + remoteMessage.getNotification().getTitle());
//        HashMap<String, Object> payload = new HashMap<>();
//        payload.put("unique_key", Math.random());
//        payload.put("payload_type", "BACKGROUND_MSG");
//        payload.put("data", KivyFirebaseMessagingUtils.remoteMessageToMap(remoteMessage));
//        Gson gson = new Gson();
//        String json = gson.toJson(payload);
//        backgroundMessages.put(Math.random()+"",json);
//        com.waterfall.youtube.ServicePythonnotificationhandler.start(org.kivy.android.PythonActivity.mActivity, json);
        // Issue with above is that Python service does not start when app is killed
        Intent onBackgroundMessageIntent =
                new Intent(context, org.kivy.plugins.messaging.KivyFirebaseMessagingBackgroundService.class);
        onBackgroundMessageIntent.putExtra(
                KivyFirebaseMessagingUtils.EXTRA_REMOTE_MESSAGE, remoteMessage);
        org.kivy.plugins.messaging.KivyFirebaseMessagingBackgroundService.enqueueMessageProcessing(
                context, onBackgroundMessageIntent);
    }
}