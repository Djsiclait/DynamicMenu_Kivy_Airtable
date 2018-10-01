import airtable
import webbrowser
import kivy
kivy.require("1.10.0")

import kivy.uix
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader 
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.properties import ObjectProperty

# Variables
tab_headers = []
tab_menus = []

# Airtable API variable that connects to and fetches databases
connection = airtable.Airtable(base_key='appdqzfZoeTcXC7VD', 
	table_name='Config', 
	api_key='keyeNCirYgYK9YhOd')

# Proxy class to validate the existance the dynamic menu with both .py and .kv files
# No code is necessary within this context
class Sanbox(BoxLayout):
	pass

# TabbedPanel to organized all airtable data in an organized page format
# Will remain empty until updated
airtable_content = TabbedPanel()

def fill_menu_with_data():
	airtable_content.clear_tabs()
	airtable_content.do_default_tab = False
	airtable_content.background_color = (0, 0, 1, .5) #50% translucent red
	airtable_content.minimum_height = 100

	for i in range(1, 5):
		tab = TabbedPanelHeader(text='Tab ' + str(i))

		tab.content = format_airtable_data(i)
		tab.content.minimum_height= 100
		
		airtable_content.add_widget(tab)

def format_airtable_data(num):
		formated_data = BoxLayout() # container for converted air table data
		formated_data.orientation = "vertical"
		formated_data.padding = 10
		formated_data.spacing = 10
		formated_data.add_widget(Label(text="Menu option " + str(num),size_hint=(.7,.5)))
		formated_data.add_widget(Button(text="Link " + str(num),size_hint=(.7,.5), on_press=open_link))

		return formated_data

def open_link(instance):
	webbrowser.open("http://kivy.org/")
		

# Class containing all objects and functions of the UI
class Resonance(BoxLayout):
	sandbox = ObjectProperty() # represents the Box layout that houses the dynamic menu
	
	def fetch_airtable_data(self):
		 # Height and any other dimension attributes for sandbox
		 # must (higly recommended) be defined here given that .kv code superceed and 
		 # .py attribute definitions override
		self.sandbox.minimum_height= 100

		# Essential to clear the Sanbox of the previous menu
		self.sandbox.remove_widget(airtable_content)
		
		# Updating the menu with new data
		fill_menu_with_data()

		# Publishing updated data
		self.sandbox.add_widget(airtable_content)
		print("This funcition works!") 

		
# creating the Application class that joins both the python and kivy ui file
class ResonanceApp(App):
	def build(self):
		return Resonance()

# instantiating and running the resonance app
main = ResonanceApp()
main.run()