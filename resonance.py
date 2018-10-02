import airtable # airtable-python wrapper that allow to connect with remote airtable bases
import webbrowser

import kivy # Cross-Platform python framework for multi-OS compatible applications 
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

from functools import partial

# Variables
tab_headers = [] # List of strings of all headers (main-menu) fields within the database
tab_menus = [] # List of dictionaries of all menu options (sub-menu) and their url data (name and url reference) within the database

# Airtable API variable that connects to and fetches databases
connection = airtable.Airtable(
	base_key='appdqzfZoeTcXC7VD', # Serial number to identify the correct database
	table_name='Config', # Name of the table that host al needed data
	api_key='keyeNCirYgYK9YhOd') # Personal api key for authentification and access. PLEASE PROVIDE YOUR OWN 

# Function for data retrieval from Airtable via api connection
# {'id': 'recyBT9LyhJ7a1KJP', 
# 'fields': {'Link Type': 'All Brands', 
# 				'URL': 'https://www.google.com/', 
#				'View Type': 'Form', 
#				'Main Menu': 'Design', 
#				'Link Name': 'Upload Color', 
#				'Sub-menu': 'Develop Colors', 
#				'Live': True, 'Name': 
#				'Upload Color'}, 
# 'createdTime': '2018-04-16T16:47:52.000Z'}
def fetch_airtable_data():
	# Loop to cycle entirity of retireved data
	for obj in connection.get_all():
		# Isolating the dictionary with all essential data with obj["fields"]
		main_menu = str(obj["fields"]["Main Menu"]) # extracting data that will become the headers of the GUI TabbedPanel

		try:
			sub_menu = str(obj["fields"]["Sub-menu"]) # extracting data that will become the menu option en each Tab
		except Exception as e:
			sub_menu = "N/A" # data may be empty ("") or missing (NONE)

		try:
			link_name = str(obj["fields"]["Link Name"]) # extracting data that will become the button text
		except Exception as e:
			link_name = "N/A" # data may be empty ("") or missing (NONE)

		try:
			url = str(obj["fields"]["URL"]) # extrating data that will provide the url refrences for their respective button
		except Exception as e:
			url = "N/A" # data may be empty ("") or missing (NONE)
		
		try:
			is_live = obj["fields"]["Live"] # extracting data that will determine if the above will be included in the GUI
		except Exception as e:
			is_live = False	# data may be missing (NONE)

		# Only data that is Live (TRUE) and posess a valid url link will be saved for later use
		if is_live and (url != "N/A" or url != None):
			if main_menu not in tab_headers:
				tab_headers.append(main_menu) # Registering all headers to create the tabs
				tab_menus.append({'id': main_menu, 'menu': sub_menu, 'link': [link_name+"!"+url]}) # Registering the first menu option and link for a new header 
			else:
				unreg = True
				for i in range(len(tab_menus)):
					if tab_menus[i]["id"] == main_menu and tab_menus[i]["menu"] == sub_menu:
						tab_menus[i]["link"].append(link_name+"!"+url) # Adding a new link to an existing menu option for an existing header
						unreg = False
						break

				# Registering a new menu option and link to an existing header
				if unreg:
					tab_menus.append({'id': main_menu, 'menu': sub_menu, 'link': [link_name+"!"+url]})

# Proxy class to validate the existance the dynamic menu with both .py and .kv files
# No code is necessary within this context
class Sanbox(BoxLayout):
	pass

# TabbedPanel to organized all airtable data in an organized page format
# It will host the Headers, Menu Options and URL Buttons 
# Will remain empty until updated
airtable_content = TabbedPanel()

# Main function in charge of accurately organizing ALL contents into a correct Kivy UI layout format 
def fill_menu_with_data():
	# Necesary to flush old data 
	airtable_content.clear_tabs()

	# Layout metadata to specify dimension and style
	airtable_content.orientation = "vertical"
	airtable_content.do_default_tab = False # Necesary to disable Default Tab that TabbedPanel generate automatically
	airtable_content.background_color = (0, 0, 1, .5) #50% translucent
	airtable_content.tab_width = 150

	# Trigger airtable connection and data retrieval
	# tab_headers and tab_menus have all data needed to fill airtable_content
	fetch_airtable_data()

	# Creation of each Tab and their respective items 
	for header in tab_headers:

		tab = TabbedPanelHeader(text=header)

		# Scrollview required to adequatly contain items without window or objec distortion
		# Effectively scroll through the menu effortlessly
		scroll = ScrollView()
		scroll.bar_margin = 10
		scroll.size_hint = (1, 1) # Needed to allow scrollview to fit the window regarless od size
		scroll.scroll_type = ['bars', 'content'] # allow scrolling via the bar or by draging content 
		scroll.bar_pos_y = 'left'
		scroll.bar_width = 20
		scroll.bar_color = (5, 10, 15, 0.8)
		scroll.bar_inactive_color = (5, 20, 15, 0.8)
		scroll.do_scroll_y = True # Needed for vertical scrolling
		scroll.do_scroll_x = False
		scroll.scroll_y = 1 # Scrolling speed
		
		# Adding item specifically fitted for the current tab
		scroll.add_widget(format_airtable_data(header))

		tab.content = scroll # adding scrollview with fitted items as content of the tab
		tab.content.orientation = "vertical"
		
		airtable_content.add_widget(tab) # adding the entirity of a tab page to the TabbedPanel

# Function to organize the content of a SINGLE tab/header
def format_airtable_data(header):
		# Gridlayout to host menu options and URL buttons
		formated_data = GridLayout(cols=1, spacing=10, size_hint_y=None)
		formated_data.orientation = "vertical"
		formated_data.padding = 10
		formated_data.row_default_height = 1

		rows = 0 # needed to track the number of items inside the gridlayout
		
		# Converting airtable data into usable Kivy GUI labels and Buttons
		for item in tab_menus:
			if item["id"] == header:
				# Creating the Labels
				if str(item["menu"]) != "N/A":
					formated_data.add_widget(Label(text=item["menu"],size_hint=(.7,.5))) # Creating a menu option as a Label
					rows += 1
				else: # For menu options that have yet to be given a name
					formated_data.add_widget(Label(text="Menu name pending",size_hint=(.7,.5)))
					rows += 1

				# Creating the URL Buttons that belong bellow each Label
				for link in item["link"]:
					url_name = str(link).split('!')[0]	
					url = str(link).split('!')[1]

					# Creaing the Button without refrences
					if  url_name != "N/A":
						button = Button(text=url_name, size_hint=(None, None))
					else: # For URL links with no assigned names
						button = Button(text="Unknown Link", size_hint=(None, None))

					button.width = 250
					button.height = 50

					# Assign each Button a refrence to a created function with their respective URL links
					# This is equivalent to Kivy script: 	on_press: root.open_link('www.your_url_link.com')
					button.bind(on_press=lambda x:Resonance().open_link(url))

					formated_data.add_widget(button)
					rows += 1
					
				formated_data.add_widget(Label())
				rows += 1

		# Formating the gridlayout to fit the sum of items created
		# Necessary to indicate to Scrollview if scroll is needed 
		# if grid size > window size allow scroll 
		formated_data.height = rows * 50  
		
		return formated_data

# Class that unite Kivy objects and Python functions and variables 
class Resonance(BoxLayout):
	# Represents the boxlayout that houses the dynamic menu
	# United by Kivy id and python class with matching names (REQUIRED)
	sandbox = ObjectProperty() 

	# Function that responds to User initiated event (on_press) via Link Buttons
	# Recieves a URL link to initiate browsing session
	def open_link(self, url):
		webbrowser.open(url) 

	# Function that responds to User initiated event (on_press) via Fetch Updated Airtable Data Button
	# Fetches and present the interactive menu based on available Airtable data
	def present_airtable_data(self):
		# Clearing the boxlayout of any old data
		self.sandbox.remove_widget(airtable_content)
		
		# Updating the menu with new data
		fill_menu_with_data()

		# Publishing updated data
		self.sandbox.add_widget(airtable_content)
	
# Creating the Application class that joins both the python and kivy file
class ResonanceApp(App):
	def build(self):
		return Resonance()

# Instantiating and running the resonance app
main = ResonanceApp()
main.run()