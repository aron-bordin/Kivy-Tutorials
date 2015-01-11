__version__ = 1.0

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


class RootWidget(FloatLayout):
	def __init__(self): #init the obj
		super(RootWidget, self).__init__()
		self.max_id = 1
		
	def btn_close_on_press(self):#callback. Close the current tab
		panel = self.ids.tab_panel #get the tab_panel by id
		tab = panel.current_tab #get the current tab
		panel.remove_widget(tab) #remove tab from tablist
		
	def btn_new_on_press(self):# callback; Add a new Tab
		panel = self.ids.tab_panel
		#create a tab by KV string
		tab_str = '''
TabbedPanelItem:
	id: tab_%d
	text: 'Tab %d'
	BoxLayout:
		Button:
			id: btn_new
            text: 'New Tab'
        Button:
            id: btn_close
            text: 'Close tab'
		'''
		self.max_id += 1 #max tab id
		tab = Builder.load_string(tab_str %(self.max_id, self.max_id)) #create a widget by string
		tab.ids.btn_new.on_press = self.btn_new_on_press #set events
		tab.ids.btn_close.on_press = self.btn_close_on_press
		panel.add_widget(tab) # add the tab
    
    
class MainApp(App):		
	def build(self):
		return RootWidget()
		
if __name__=='__main__':
    MainApp().run()