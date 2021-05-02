// Copyright 2020 The Chromium Authors. All rights reserved.
package org.kivy.plugins.messaging;



import androidx.annotation.NonNull;

import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

public class KivyFirebaseMessagingService extends FirebaseMessagingService {
    @Override
    public void onNewToken(@NonNull String token) {
        PlatformIntermediate.token = token;
    }

    @Override
    public void onMessageReceived(@NonNull RemoteMessage remoteMessage) {
        // Added for commenting purposes;
        // We don't handle the message here as we already handle it in the receiver and don't want to duplicate.
    }
}