import kivy 

from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label 
from kivy.uix.tabbedpanel import TabbedPanel 
from kivy.properties import ObjectProperty

# Proxy class to validate the existance the dynamic menu with both .py and .kv files
# No code is necessary within this context
class Sanbox(BoxLayout):
	pass

test = Label()
# TabbedPanel to organized all airtable data in an organized page format
# Will remain empty until updated
airtable_content = TabbedPanel()

# Class containing all objects and functions of the UI
class Resonance(BoxLayout):
	sandbox = ObjectProperty() # represents the Box layout that houses the dynamic menu
	
	def fetch_airtable_data(self):
		# Essential to clear the Sanbox of the previous menu
		self.sandbox.remove_widget(test)
		
		# Updating the menu with new data
		test.text= "Hello"
		
		# Publishing updated data
		self.sandbox.add_widget(test)
		print("This funcition works!") 

		
# creating the Application class that joins both the python and kivy ui file
class ResonanceApp(App):
	def build(self):
		return Resonance()

# instantiating and running the resonance app
main = ResonanceApp()
main.run()