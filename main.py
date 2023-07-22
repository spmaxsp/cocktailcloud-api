import flask_server

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import webbrowser

import threading

def start_flask_thread(app):
    flask_thread = threading.Thread(target=flask_server.start_flask_server, args=(app,))
    flask_thread.daemon = True
    flask_thread.start()
    return flask_thread

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.console_output_label = None
        self.flask_thread = None


    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Title at the top
        title_label = Label(text='Cocktailcloud Backend', size_hint=(1, 0.1))
        layout.add_widget(title_label)

        # Scrollable container with a label
        scroll_container = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=10, padding=10)
        scroll_container.bind(minimum_height=scroll_container.setter('height'))

        self.console_output_label = Label(text="", halign='left', valign='top', markup=True, size_hint_y=None, size_hint_x=1)
        scroll_container.add_widget(self.console_output_label)

        scroll_view = ScrollView(size_hint=(1, 0.8), do_scroll_x=False)
        scroll_view.add_widget(scroll_container)
        layout.add_widget(scroll_view)

        # Button at the bottom
        button = Button(text='Open Browser', size_hint=(1, 0.1))
        button.bind(on_press=self.open_browser)
        layout.add_widget(button)

        return layout

    def open_browser(self, instance):
        url = 'http://localhost:43560'  # Replace with the desired URL
        try:
            webbrowser.open(url)
        except Exception as e:
            # Show a popup if there's an error opening the browser
            popup = Popup(title='Error', content=Label(text=f'Error: {e}'), size_hint=(0.7, 0.3))
            popup.open()

    def on_start(self):
        # Start Flask server in a separate thread
        self.flask_thread = start_flask_thread(self)

if __name__ == '__main__':
    MyApp().run()
