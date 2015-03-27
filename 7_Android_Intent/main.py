__version__ = '1.0'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

if platform() == "android":
	from jnius import cast
	from jnius import autoclass

class RootWidget(BoxLayout):
    
    def share(self):
        if platform() == 'android': #check if the app is on Android
            # read more here: http://developer.android.com/training/sharing/send.html
           
            PythonActivity = autoclass('org.renpy.android.PythonActivity') #request the Kivy activity instance
            Intent = autoclass('android.content.Intent') # get the Android Intend class

            String = autoclass('java.lang.String') # get the Java object

            intent = Intent() # create a new Android Intent
            intent.setAction(Intent.ACTION_SEND) #set the action

            # to send a message, it need to be a Java char array. So we use the cast to convert and Java String to a Java Char array
            intent.putExtra(Intent.EXTRA_SUBJECT, cast('java.lang.CharSequence', String('Byte::Debugger() Tutorial #7')))
            intent.putExtra(Intent.EXTRA_TEXT, cast('java.lang.CharSequence', String("Testing Byte::Debugger() Tutorial #7, with Python for Android")))

            intent.setType('text/plain') #text message

            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            currentActivity.startActivity(intent) # show the intent in the game activity

class MainApp(App):
    def build(self):
        return RootWidget()

    def on_pause(self):
        return True

if __name__ == '__main__':
    MainApp().run()