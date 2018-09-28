from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.clock import mainthread

NUMBER_OF_BUTTONS = 5


class MapScreen(Screen):

    @mainthread
    def on_enter(self):
        for i in xrange(NUMBER_OF_BUTTONS):
            button = Button(text="B_" + str(i))
            self.ids.grid.add_widget(button)


class RessonanceApp(App):
    pass


RessonanceApp().run()