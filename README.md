# pushyy
A Python module meant to simplify working with push notifications in Kivy

**Video tutorial**: https://youtu.be/8nrXsWeRG8I

Features
--------------
- Receive push notifications when your app is in the **foreground**
- Receive push notifications when your app is in the **background** or not running
- Run a background function when notification is received when app is not running
- Get a device token
- Listen for device token changes

Credits
--------------
- [Flutter Firebase Messaging](https://github.com/FirebaseExtended/flutterfire/tree/master/packages/firebase_messaging/firebase_messaging): The Java classes are from there

        - Kindly create a PR correcting the copyright if it's wrong :)
- [Electrum](https://github.com/spesmilo/electrum/tree/master/electrum) for the [onNewIntent](https://github.com/spesmilo/electrum/blob/6650e6bbae12a79e12667857ee039f1b1f30c7e3/electrum/gui/kivy/main_window.py#L620)

Usage Overview
--------------
```python
from pushyy import Pushyy

# Get device token
def my_token_callback(token: str) -> None:
    send_to_server(token)

Pushyy().get_device_token(my_token_callback)

# Listen for new device token
def new_token_callback(token: str) -> None:
    print(token)

Pushyy().token_change_listener(new_token_callback)

# Get notification data when app is in foreground
def my_foreground_message_callback(notification_data: RemoteMessage) -> None:
    print(notification_data)

Pushyy().foreground_message_handler(my_foreground_message_callback)

# Get notification data when user taps on notification from tray
def my_notification_click_callback(notification_data: RemoteMessage) -> None:
    print(notification_data)

Pushyy().notification_click_handler(my_notification_click_callback)

```
> See `src/python/main.py` on how the UI is being updated

##### Background function
To run custom code in the background when a notification is received and your application is not running, write your code in the ```my_background_callback``` function in [python_notification_handler.py](src/python/python_notification_handler.py)
```python
def my_background_callback(notification_data: RemoteMessage) -> None:
    """
    Note: Application is not visible to the user here
    One of the things you can do here: Mark a chat message
    as delivered by making a request to your server.
    """
    try:
        # connect to server
        pass
    except:
        pass
```

Set up
--------------
##### Part 1
1. Clone [python-for-android](https://github.com/kivy/python-for-android)
2. Open the file `pythonforandroid/bootstraps/common/build/templates/build.tmpl.gradle`
3. Add the following:
    - Under `buildscript->dependencies` add `classpath 'com.google.gms:google-services:4.3.4'`
    - Below `apply plugin: 'com.android.application'` add `apply plugin: 'com.google.gms.google-services'`
    - Under `dependencies` add `implementation platform('com.google.firebase:firebase-bom:X.Y.Z')` (replace XYZ with the latest version from [here](https://firebase.google.com/docs/android/learn-more#bom))
4. Open the file `pythonforandroid/bootstraps/sdl2/build/templates/AndroidManifest.tmpl.xml`
5. Before the `</application>` tag, add
```xml
<service
    android:name="org.kivy.plugins.messaging.KivyFirebaseMessagingBackgroundService"
    android:permission="android.permission.BIND_JOB_SERVICE"
    android:exported="false"/>
<service android:name="org.kivy.plugins.messaging.KivyFirebaseMessagingService"
    android:exported="false">
    <intent-filter>
        <action android:name="com.google.firebase.MESSAGING_EVENT"/>
    </intent-filter>
</service>
<receiver
    android:name="org.kivy.plugins.messaging.KivyFirebaseMessagingReceiver"
    android:exported="true"
    android:permission="com.google.android.c2dm.permission.SEND">
    <intent-filter>
        <action android:name="com.google.android.c2dm.intent.RECEIVE" />
    </intent-filter>
</receiver>
```
6. Create a Firebase project [here](https://console.firebase.google.com/)
    - Add an Android app and skip the steps since we already did that at
    - Download the `google-services.json`
    - Move it to `pythonforandroid/bo -> Noneotstraps/common/build/` folder
##### Part 2
1. Place [pushyy.py](src/python/pushyy.py) and [python_notification_handler.py](src/python/python_notification_handler.py) next to your `main.py`
2. Place [libs/](src/python/libs) in the same folder as `buildozer.spec`
3. In your `buildozer.spec` find and set:
```bash
android.add_src = libs/
android.gradle_dependencies = com.google.firebase:firebase-messaging,com.google.firebase:firebase-analytics,com.google.code.gson:gson:2.8.6
p4a.source_dir = /path/to/cloned/python-for-android

services = PythonNotificationHandler:python_notification_handler.py
# NB: File name must be python_notification_handler.py
```
5. Open `PlatformIntermediate.java` from your `libs/` folder and replace `com.waterfall.youtube` with `your.app.packagename`

6. Open `KivyFirebaseMessagingBackgroundExecutor.java` from your `libs/` folder and replace `com.waterfall.youtube` with `your.app.packagename`

Notes
---------
- This module is aimed for Android. For iOS, you may consider [this](https://youtu.be/mONyhxt2KV8) video
- Just to clarify, with [Plyer](https://github.com/kivy/plyer) you get to show local notifications, not push notifications. [Which notifications should i use, Push notification or local notification?](https://stackoverflow.com/questions/45343427/which-notifications-should-i-use-push-notification-or-local-notification)
- Why Pushyy? First thing that came to mind `¯\_(ツ)_/¯`
