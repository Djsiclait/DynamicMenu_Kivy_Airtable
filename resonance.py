import airtable
import webbrowser

import kivy
kivy.require("1.10.0")

from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView 
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

def fetch_airtable_data():
	for obj in connection.get_all():
		main_menu = str(obj["fields"]["Main Menu"])

		try:
			sub_menu = str(obj["fields"]["Sub-menu"])
		except Exception as e:
			sub_menu = "N/A"

		try:
			link_name = str(obj["fields"]["Link Name"])
		except Exception as e:
			link_name = "N/A"

		try:
			url = str(obj["fields"]["URL"])
		except Exception as e:
			url = "N/A"
		
		try:
			is_live = obj["fields"]["Live"]
		except Exception as e:
			is_live = False

		if is_live and url != "N/A":
			if main_menu not in tab_headers:
				tab_headers.append(main_menu)
				tab_menus.append({'id': main_menu, 'menu': sub_menu, 'link': [link_name+"."+url]})
			else:
				unreg = True
				for i in range(len(tab_menus)):
					if tab_menus[i]["id"] == main_menu and tab_menus[i]["menu"] == sub_menu:
						tab_menus[i]["link"].append(link_name+"."+url)
						unreg = False
						break

				if unreg:
					tab_menus.append({'id': main_menu, 'menu': sub_menu, 'link': [link_name+"."+url]})

# Proxy class to validate the existance the dynamic menu with both .py and .kv files
# No code is necessary within this context
class Sanbox(BoxLayout):
	pass

# TabbedPanel to organized all airtable data in an organized page format
# Will remain empty until updated
airtable_content = TabbedPanel()
scrollview = ScrollView()
scrollview.scroll_type = ['bars', 'content']
gridlayout = GridLayout(cols=1, spacing=10, size_hint_y=None)

def fill_menu_with_data():
	airtable_content.clear_tabs()
	airtable_content.do_default_tab = False
	airtable_content.background_color = (0, 0, 1, .5) #50% translucent red
	airtable_content.tab_width = 150

	# Trigger airtable connection and data retrieval
	fetch_airtable_data()

	for header in tab_headers:
		tab = TabbedPanelHeader(text=header)

		#tab.content = format_airtable_data(i)
		#tab.content.minimum_height= 100
		
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
	
	def present_airtable_data(self):
		 # Height and any other dimension attributes for sandbox
		 # must (higly recommended) be defined here given that .kv code superceed and 
		 # .py attribute definitions override
		self.sandbox.minimum_height= 100

		# Essential to clear the Sanbox of the previous menu
		gridlayout.remove_widget(airtable_content)
		scrollview.remove_widget(gridlayout)
		self.sandbox.remove_widget(scrollview)
		
		# Updating the menu with new data
		fill_menu_with_data()

		# Publishing updated data
		gridlayout.add_widget(airtable_content)
		scrollview.add_widget(gridlayout)
		self.sandbox.add_widget(scrollview)
		print("This funcition works!") 

		
# creating the Application class that joins both the python and kivy ui file
class ResonanceApp(App):
	def build(self):
		return Resonance()

# instantiating and running the resonance app
main = ResonanceApp()
main.run()