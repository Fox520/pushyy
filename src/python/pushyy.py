import json
from typing import Callable
from typing import Any
from kivy.clock import Clock, mainthread
from jnius import autoclass, java_method, PythonJavaClass

class Pushyy:
    # TODO: create listener for new device token
    __notification_click_callback = None
    __last_on_message_key = None

    def foreground_message_handler(self, callback: Callable[[dict], None], interval: float = 0.5) -> None:
        """Function to call when push notification is received
        and application is in the foreground
        
        Example
        def my_foreground_callback(data: dict):
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
        PlatformIntermediate = autoclass("org.kivy.plugins.messaging.PlatformIntermediate")
        data = PlatformIntermediate.getForegroundMessage()
        msg = json.loads(data)
        # Avoid "process" an already "processed" message
        if len(msg) == 0 or msg.get("unique_key") == self.__last_on_message_key:
            pass
        else:
            self.__last_on_message_key = msg.get("unique_key")
            msg.pop("unique_key")
            callback(msg)
    
    def notification_click_handler(self, callback: Callable[[dict], None]):
        """Function to call when push notification is clicked
        
        Example
        def my_click_callback(data: dict):
            print(data)

        Parameters:
        callback (function): Callback function reference

        Returns:
        None

        """
        self.__notification_click_callback = callback

        # gg https://github.com/spesmilo/electrum/blob/6650e6bbae12a79e12667857ee039f1b1f30c7e3/electrum/gui/kivy/main_window.py#L620
        from android import activity
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        mactivity = PythonActivity.mActivity
        self.__on_new_intent(mactivity.getIntent())
        activity.bind(on_new_intent=self.__on_new_intent)
    
    def __on_new_intent(self, intent):
        bundle = intent.getExtras()
        # Make sure it's a push notification
        if bundle is not None and (bundle.get("google.message_id") != None or bundle.get("message_id")):
            # Go through Java HashMap copying over to Python dictionary
            notification_data = {}
            for key in bundle.keySet():
                notification_data[key] = bundle.get(key)
            self.__notification_click_callback(notification_data)
    
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
            __javainterfaces__ = ['com/google/android/gms/tasks/OnSuccessListener']
            __javacontext__ = "app"

            @java_method("(Ljava/lang/Object;)V")
            def onSuccess(self, s):
                callback(s)
        FirebaseMessaging = autoclass('com.google.firebase.messaging.FirebaseMessaging')
        FirebaseMessaging.getInstance().getToken().addOnSuccessListener(MyTokenListener())


def process_background_messages(callback: Callable[[dict], None]):
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
    try:
        PlatformIntermediate = autoclass("org.kivy.plugins.messaging.PlatformIntermediate")
    except:
        # 'Request to get environment variables before JNI is ready'
        # didn't look up how to check if it's ready, anyway
        import time
        time.sleep(1)
        PlatformIntermediate = autoclass("org.kivy.plugins.messaging.PlatformIntermediate")
    # {"random_num_1": {"notification_one": "data"}, "random_num_2": {"notification_two": "data"}}
    # TODO: returns empty dictionary
    data = json.loads(PlatformIntermediate.getBackgroundMessages())
    print(data)
    # Go over HashMap
    for key, value in data.items():
        try:
            # Remove notification before callback as it may throw an exception
            PlatformIntermediate.backgroundMessages.remove(key)
            callback({"test": "value"})
            callback(value)
        except Exception as e:
            print(e)
