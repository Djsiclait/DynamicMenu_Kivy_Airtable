import kivy 

from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

# Class containing all objects and functions of the UI
class Resonance(BoxLayout):
	pass

# creating the Application class that joins both the python and kivy ui file
class ResonanceApp(App):
	def build(self):
		return Resonance()

# instantiating and running the resonance app
main = ResonanceApp()
main.run()