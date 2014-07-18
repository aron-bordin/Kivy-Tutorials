'''
	First tutorial of Mobile development with Python. This code is compatible with Android and iOS.
	Check the full tutorial at: ###########################
	Check Mobile Development with Python Course at: http://bytedebugger.wordpress.com/
	
	Created by Aron Bordin <aron.bordin@gmail.com>
	
	Released into GPL2	
'''

__version__ = '1.0' #declare the app version. Will be used by buildozer


from kivy.app import App #for the main app
from kivy.uix.floatlayout import FloatLayout #the UI layout
from kivy.uix.label import Label #a label to show information
from plyer import accelerometer #object to read the accelerometer
from kivy.clock import Clock #clock to schedule a method

class UI(FloatLayout):#the app ui
	def __init__(self, **kwargs):
		super(UI, self).__init__(**kwargs)
		self.lblAcce = Label(text="\t\t\tAccelerometer: ") #create a label at the center
		self.add_widget(self.lblAcce) #add the label at the screen
		try:
			accelerometer.enable() #enable the accelerometer
			#if you want do disable it, just run: accelerometer.disable()
		except:
			self.lblAcce.text = "Failed to start accelerometer" #error
		
		Clock.schedule_interval(self.update, 1.0/24) #24 calls per second
		
	def update(self, dt):
		txt = ""
		try:
			txt = "Accelerometer:\nX = %.2f\nY = %.2f\nZ = %2.f " %(
				accelerometer.acceleration[0], #read the X value
				accelerometer.acceleration[1], # Y
				accelerometer.acceleration[2]) # Z
		except:
			txt = "Cannot read accelerometer!" #error
		self.lblAcce.text = txt #add the correct text 

class Accelerometer(App): #our app
	def build(self):
		ui = UI()# create the UI
		return ui #show it

Accelerometer().run() #start our app
