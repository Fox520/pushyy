import os
import json

from .remote_message import RemoteMessage
from typing import Callable
from typing import Any
from kivy.clock import Clock, mainthread
from jnius import autoclass, cast, java_method, PythonJavaClass


class Pushyy:
    __notification_click_callback = None
    __last_on_message_key = None
    __token = None

    def foreground_message_handler(
        self, callback: Callable[[RemoteMessage], None], interval: float = 0.5
    ) -> None:
        """Function to call when push notification is received
        and application is in the foreground

        Example
        def my_foreground_callback(data: RemoteMessage):
            print(data)

        Parameters:
        callback (function): Callback function reference
        interval (float): How often to check for message

        Returns:
        None

        """

        @mainthread
        def checker(*args):
            try:
                self.__on_message(callback)
            except Exception as e:
                print(e)

        Clock.schedule_interval(checker, interval)

    def __on_message(self, callback):
        PlatformIntermediate = autoclass(
            "org.kivy.plugins.messaging.PlatformIntermediate"
        )
        data = PlatformIntermediate.getForegroundMessage()
        msg = json.loads(data)
        # Avoid "processing" an already "processed" message
        if len(msg) == 0 or msg.get("unique_key") == self.__last_on_message_key:
            pass
        else:
            self.__last_on_message_key = msg.get("unique_key")
            msg.pop("unique_key")
            callback(RemoteMessage(msg))

    def notification_click_handler(self, callback: Callable[[RemoteMessage], None]):
        """Function to call when push notification is clicked

        Example
        def my_click_callback(data: RemoteMessage):
            print(data)

        Parameters:
        callback (function): Callback function reference

        Returns:
        None

        """
        self.__notification_click_callback = callback

        # gg https://github.com/spesmilo/electrum/blob/6650e6bbae12a79e12667857ee039f1b1f30c7e3/electrum/gui/kivy/main_window.py#L620
        from android import activity

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        mactivity = PythonActivity.mActivity
        # Bind to when application appears on the foreground
        self.__on_new_intent(mactivity.getIntent())
        activity.bind(on_new_intent=self.__on_new_intent)

    def __on_new_intent(self, intent):
        bundle = intent.getExtras()
        # Make sure it's a push notification
        if bundle is not None and (
            bundle.get("google.message_id") != None or bundle.get("message_id")
        ):
            # Go through Java HashMap copying over to Python dictionary
            notification_data = {}
            for key in bundle.keySet():
                notification_data[key] = bundle.get(key)
            self.__notification_click_callback(RemoteMessage(notification_data))

    def get_device_token(self, callback: Callable[[str], None]) -> None:
        """Function to call when device token is retrieved

        Example
        def my_token_callback(token: str):
            print(token)

        Parameters:
        callback (function): Callback function reference

        Returns:
        None

        """

        class MyTokenListener(PythonJavaClass):
            __javainterfaces__ = ["com/google/android/gms/tasks/OnSuccessListener"]
            __javacontext__ = "app"

            @java_method("(Ljava/lang/Object;)V")
            def onSuccess(self, s):
                callback(s)

        FirebaseMessaging = autoclass("com.google.firebase.messaging.FirebaseMessaging")
        FirebaseMessaging.getInstance().getToken().addOnSuccessListener(
            MyTokenListener()
        )

    def token_change_listener(
        self, callback: Callable[[dict], None], interval: float = 0.5
    ) -> None:
        """Function to call when device token changes

        Example
        def new_token_callback(data: str):
            print(data)

        Parameters:
        callback (function): Callback function reference
        interval (float): How often to check for message

        Returns:
        None

        """

        @mainthread
        def checker(*args):
            try:
                self.__on_new_token(callback)
            except Exception as e:
                print(e)

        Clock.schedule_interval(checker, interval)

    def __on_new_token(self, callback):
        PlatformIntermediate = autoclass(
            "org.kivy.plugins.messaging.PlatformIntermediate"
        )
        token = PlatformIntermediate.token
        # Overwriting an already read "token"
        if len(token) == 0 or token == self.__token:
            pass
        else:
            self.__token = token
            callback(token)


last_read_background_keys = None


def process_background_messages(callback: Callable[[dict], None]):
    global last_read_background_keys
    """Function to call when push notification is received and app is not running
    Possible use-case is marking message as delivered in a chat application
        
    Example
    def my_background_callback(data: dict):
        print(data)

    Parameters:
    callback (function): Callback function reference

    Returns:
    None

    """
    from jnius import autoclass
    import time

    try:
        PythonService = autoclass("org.kivy.android.PythonService")
    except Exception as e:
        # 'Request to get environment variables before JNI is ready'
        print(e)
        # Not sure if this is necessary, anyway
        import jnius
        reload(jnius)
        from jnius import autoclass
        import time
        time.sleep(3)
        PythonService = autoclass("org.kivy.android.PythonService")

    context = PythonService.mService.getApplicationContext()
    file_path = context.getFilesDir().getPath() + "/background_messages.json"
    if os.path.exists(file_path):
        """
        Reason to read from a file and not the backgroundMessages variable is that from my
        observation, over JNI, the backgroundMessages variable gets reset to empty. Almost as
        if a new version of a static class is created ¯\_(ツ)_/¯
        """
        use_callback = False
        with open(file_path) as f:
            content = json.loads(f.read())
            if last_read_background_keys != content.keys():
                last_read_background_keys = content.keys()
                use_callback = True
        
        # Delete file since notification data is read
        os.remove(file_path)
        # Ensure old data is not passed to callback
        for key, data in content.items():
            if use_callback:
                data.pop("unique_key")
                callback(RemoteMessage(data))
