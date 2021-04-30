package org.kivy.plugins.messaging;


import android.util.Log;

import androidx.annotation.NonNull;

import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;
import com.google.gson.Gson;

import java.util.HashMap;

public class KivyFirebaseMessagingService extends FirebaseMessagingService {
    @Override
    public void onNewToken(@NonNull String token) {
        HashMap<String, Object> payload = new HashMap<>();
        payload.put("unique_key", Math.random());
        payload.put("payload_type", "NEW_TOKEN");
        payload.put("data", token);
        Gson gson = new Gson();
        String json = gson.toJson(payload);
        com.waterfall.youtube.ServicePythonnotificationhandler.start(ContextHolder.getApplicationContext(), json);
        Log.d("python","------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------from onNewToken: "+token);
    }

    @Override
    public void onMessageReceived(@NonNull RemoteMessage remoteMessage) {
        // Added for commenting purposes;
        // We don't handle the message here as we already handle it in the receiver and don't want to duplicate.
    }
}