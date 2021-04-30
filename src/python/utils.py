from jnius import autoclass, java_method, PythonJavaClass

# Sidenote: No longer using this approach but commiting in case someone runs into it
# Issue I had with this is, it gets called when the app is resumed from background state
# but not after the app has been killed.
# Reason might be that the listener is registered after the app has finished initialising,
# thereby missing out the intent sent earlier. idk if that makes sense but :)
# Register NewIntentListener
class NewIntentListener(PythonJavaClass):
    __javainterfaces__ = ["org.kivy.android.PythonActivity$NewIntentListener"]
    __javacontext__ = "app"

    def __init__(self, **kwargs):
        super(NewIntentListener, self).__init__(**kwargs)

    @java_method("(Landroid/content/Intent;)V")
    def onNewIntent(self, intent):
        bundle = intent.getExtras()
        if bundle is not None:
            notification_data = {}
            for key in bundle.keySet():
                notification_data[key] = bundle.get(key)
            print(notification_data)
        else:
            print("onNewIntent: bundle is None")


def register_notification_click(aa):
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    PythonActivity.mActivity.registerNewIntentListener(aa)

