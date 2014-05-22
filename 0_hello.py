''' Python and Kivy Hello World.
You can run this project where do you prefer, including mobile platforms.
Read more: http://bytedebugger.wordpress.com/2014/05/21/tutorial-android-development-with-python-and-kivy-introduction/

'''

from kivy.app import App
from kivy.uix.button import Button
 
class Hello(App):
    def build(self):
        btn = Button(text='Hello World')
        return  btn
 
Hello().run()