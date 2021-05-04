package org.kivy.plugins.messaging;

import android.content.Context;
import android.util.Log;

import com.google.gson.Gson;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.io.Writer;
import java.util.HashMap;
import java.util.Map;

public class PlatformIntermediate {
    private static HashMap<String, Object> _foregroundMessage = new HashMap<String, Object>();
    final public static HashMap<String, Object> backgroundMessages = new HashMap<String, Object>();
    public static String token = "";
    private static final String BACKGROUND_MSG_FILE_NAME = "/background_messages.json";

    public static String getForegroundMessage() {
        return new Gson().toJson(_foregroundMessage);
    }

    public static void setForegroundMessage(Map<String, Object> msg) {
        HashMap<String, Object> copy = new HashMap<String, Object>(msg);
        _foregroundMessage = copy;

        _foregroundMessage.put("unique_key", Math.random());
        Log.d("PlatformIntermediate", "setForegroundMessage worked " + _foregroundMessage.toString());
    }

    public static void addbackroundMessage(Map<String, Object> remoteMessageMap, Context context) {
        try {
            com.waterfall.youtube.ServicePythonnotificationhandler.start(org.kivy.android.PythonActivity.mActivity, "");
        } catch (Exception e) {
            Log.d("PlatformIntermediate", "Exception occurred while trying to start service: " + e.getMessage());
        }
        backgroundMessages.put(remoteMessageMap.get("unique_key").toString(), remoteMessageMap);

        // Read stored json
        String jsonText = readBackgroundFile(context);

        Map<String, Object> map = new HashMap<String, Object>();
        if (jsonText.length() > 0) {
            map = (Map<String, Object>) new Gson().fromJson(jsonText, map.getClass());
        }
        boolean shouldRecreateFile = false;
        // Merge with map where key does not exist or create file if map size is 0
        if (map.size() == 0) {
            shouldRecreateFile = true;
        } else {
            for (String key : map.keySet()) {
                if (backgroundMessages.get(key) == null) {
                    backgroundMessages.put(key, map.get(key));
                    shouldRecreateFile = true;
                }
            }
        }
        // Write to file
        if (shouldRecreateFile) {
//            deleteBackgroundFile(context);
            writeBackgroundFile(new Gson().toJson(backgroundMessages), context);

        }
        Log.d("PlatformIntermediate", "New message added, recreated: "+shouldRecreateFile +" "+context.getFilesDir().getPath());
        if(shouldRecreateFile == false){
            Log.d("PlatformIntermediate", map.toString());

        }
    }

    public static void writeBackgroundFile(String data, Context context) {
        try (Writer writer = new BufferedWriter(new OutputStreamWriter(
                new FileOutputStream(context.getFilesDir().getPath()+BACKGROUND_MSG_FILE_NAME), "utf-8"))) {
            writer.write(data);
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static String readBackgroundFile(Context context) {
        String ret = "";
        try (BufferedReader br = new BufferedReader(new FileReader(context.getFilesDir().getPath()+BACKGROUND_MSG_FILE_NAME))) {
            StringBuilder sb = new StringBuilder();
            String line = br.readLine();
            while (line != null) {
                sb.append(line);
                sb.append("\n");
                line = br.readLine();
            }
            ret = sb.toString();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return ret;
    }
}
