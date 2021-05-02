package org.kivy.plugins.messaging;

import android.util.Log;

import com.google.gson.Gson;

import java.util.HashMap;
import java.util.Map;

public class PlatformIntermediate {
    private static HashMap<String, Object> _foregroundMessage = new HashMap<String, Object>();
    final public static HashMap<String, Object> backgroundMessages = new HashMap<String, Object>();
    public static String token = "";

    public static String getForegroundMessage() {
        return new Gson().toJson(_foregroundMessage);
    }

    public static void setForegroundMessage(Map<String, Object> msg) {
        HashMap<String, Object> copy = new HashMap<String, Object>(msg);
        _foregroundMessage = copy;

        _foregroundMessage.put("unique_key", Math.random());
        Log.d("PlatformIntermediate", "setForegroundMessage worked " + _foregroundMessage.toString());
    }

    public static void addbackroundMessage(Map<String, Object> remoteMessageMap) {
        try{
            com.waterfall.youtube.ServicePythonnotificationhandler.start(org.kivy.android.PythonActivity.mActivity, "");
        }catch (Exception e){
            Log.d("PlatformIntermediate","Exception occurred while trying to start service: "+e.getMessage());
        }
        backgroundMessages.put(remoteMessageMap.get("unique_key").toString(), remoteMessageMap);
        Log.d("PlatformIntermediate", "New message added, new map -> "+new Gson().toJson(backgroundMessages));
    }

    public static String getBackgroundMessages() {
        return new Gson().toJson(backgroundMessages);
    }
}
