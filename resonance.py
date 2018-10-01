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

		if is_live and (url != "N/A" or url != None):
			if main_menu not in tab_headers:
				tab_headers.append(main_menu)
				tab_menus.append({'id': main_menu, 'menu': sub_menu, 'link': [link_name+"!"+url]})
			else:
				unreg = True
				for i in range(len(tab_menus)):
					if tab_menus[i]["id"] == main_menu and tab_menus[i]["menu"] == sub_menu:
						tab_menus[i]["link"].append(link_name+"!"+url)
						unreg = False
						break

				if unreg:
					tab_menus.append({'id': main_menu, 'menu': sub_menu, 'link': [link_name+"!"+url]})

# Proxy class to validate the existance the dynamic menu with both .py and .kv files
# No code is necessary within this context
class Sanbox(BoxLayout):
	pass

# TabbedPanel to organized all airtable data in an organized page format
# Will remain empty until updated
airtable_content = TabbedPanel()
#scrollview = ScrollView()
#scrollview.scroll_type = ['bars', 'content']
#scrollview.minimum_height = 500
#scrollview.orientation = "vertical"
#scrollview.minimum_width = 500
#gridlayout = GridLayout(cols=1, spacing=10, size_hint_y=None)
#gridlayout.minimum_height = 500
#gridlayout.orientation = "vertical"
#gridlayout.minimum_width = 500

def fill_menu_with_data():
	airtable_content.clear_tabs()
	#airtable_content.size_hint_y =0.5
	airtable_content.orientation = "vertical"
	airtable_content.do_default_tab = False
	airtable_content.background_color = (0, 0, 1, .5) #50% translucent
	airtable_content.tab_width = 150
	#airtable_content.minimum_height = 1000
	#airtable_content.minimum_width = 500

	# Trigger airtable connection and data retrieval
	fetch_airtable_data()

	for header in tab_headers:
		tab = TabbedPanelHeader(text=header)

		#grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
		#grid.add_widget(format_airtable_data(header))
		#grid.minimum_height = 500

		scroll = ScrollView()
		scroll.bar_margin = 10
		#scroll.size_hint = (1, 0.1)
		#scroll.pos_hint = (1, 1)
		scroll.scroll_type = ['bars', 'content']
		scroll.bar_pos_y = 'left'
		scroll.bar_width = 20
		scroll.bar_color = (5, 10, 15, 0.8)
		scroll.bar_inactive_color = (5, 20, 15, 0.8)
		scroll.do_scroll_y = True
		scroll.do_scroll_x = False
		scroll.scroll_y = 1
		#scroll.minimun_height = 400
		scroll.add_widget(format_airtable_data(header))

		tab.content = scroll
		#tab.content = format_airtable_data(header)
		tab.content.orientation = "vertical"
		#tab.content.minimum_height = 1000
		#tab.content.minimum_width = 500
		
		airtable_content.add_widget(tab)


def open_link(url):
	webbrowser.open(url)	

def format_airtable_data(header):
		formated_data = GridLayout(cols=1, spacing=10, size_hint_y=None) # container for converted air table data
		formated_data.orientation = "vertical"
		formated_data.padding = 10
		formated_data.spacing = 20
		#formated_data.minimum_height = 1000
		#formated_data.minimum_width = 250

		for item in tab_menus:
			if item["id"] == header:
				if str(item["menu"]) != "N/A":
					formated_data.add_widget(Label(text=item["menu"],size_hint=(.7,.5)))
					formated_data.add_widget(Label())
				else:
					formated_data.add_widget(Label(text="Menu name pending",size_hint=(.7,.5)))
					formated_data.add_widget(Label())

				for link in item["link"]:
					print(link)
					url_name = str(link).split('!')[0]	
					url = str(link).split('!')[1]
					#print(url_name + "---" + url)
					button = Button(text=url_name, size_hint=(.7,.5))
					#print("Ping 1!")
					#button.bind(on_press=open_link(url))
					#print("Ping 2!")
					formated_data.add_widget(button)
					formated_data.add_widget(Label())
					formated_data.add_widget(Label())
					#print("Ping 3!")

		#formated_data.add_widget(Button(text="Link " + str(num),size_hint=(.7,.5), on_press=open_link))

		return formated_data

		

# Class containing all objects and functions of the UI
class Resonance(BoxLayout):
	sandbox = ObjectProperty() # represents the Box layout that houses the dynamic menu
	
	def present_airtable_data(self):
		# Height and any other dimension attributes for sandbox
		# must (higly recommended) be defined here given that .kv code superceed and 
		# .py attribute definitions override
		#self.sandbox.minimum_height = 500
		#self.sandbox.minimum_width = 500
		#self.sandbox.size_hint_y =0.5
		# Essential to clear the Sanbox of the previous menu
		#gridlayout.remove_widget(airtable_content)
		#scrollview.remove_widget(gridlayout)
		self.sandbox.remove_widget(airtable_content)
		
		# Updating the menu with new data
		fill_menu_with_data()

		# Publishing updated data
		#airtable_content.minimum_height = 500
		#gridlayout.add_widget(airtable_content)
		#gridlayout.minimum_height = 500
		#scrollview.add_widget(gridlayout)
		#gridlayout.minimum_height = 500
		self.sandbox.add_widget(airtable_content)
		print("This funcition works!") 

		
# creating the Application class that joins both the python and kivy ui file
class ResonanceApp(App):
	def build(self):
		return Resonance()

# instantiating and running the resonance app
main = ResonanceApp()
main.run()