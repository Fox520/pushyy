from jnius import autoclass, java_method, PythonJavaClass

from kivy.app import App
from kivy.uix.button import Button
import utils
from kivy.lang.builder import Builder
from kivy.properties import DictProperty
from kivy.properties import ObjectProperty
from pushyy import Pushyy

KV = '''
#:import utils utils
BoxLayout:
    orientation: "vertical"
    ScrollableLabel:
        text: str(app.recent_notification_data)
        font_size: 50
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
    Button:
        text: "get token"
        on_release: app.get_token()
<ScrollableLabel@Label+ScrollView>
'''

class TestApp(App):
    recent_notification_data = DictProperty(rebind=True)
    # Maintain reference to prevent Python gc the object. Without it we get something like
    # AttributeError: 'list' object has no attribute 'invoke'
    # alpha = ObjectProperty(utils.NewIntentListener())

    def on_start(self):
        # utils.register_notification_click(self.alpha)
        Pushyy().foreground_message_handler(my_foreground_callback)
        Pushyy().notification_click_handler(my_notification_click_callback)

    def get_token(self):
        Pushyy().get_device_token(my_token_callback)
        
    def build(self):
        return Builder.load_string(KV)

def my_token_callback(token):
    print(token)

def my_foreground_callback(data):
    print(data)
    App.get_running_app().recent_notification_data = data

def my_notification_click_callback(data):
    print(data)
    App.get_running_app().recent_notification_data = data

TestApp().run()
