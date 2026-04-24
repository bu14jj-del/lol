import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class ClickerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='Tiles Bot', font_size='24sp', size_hint_y=None, height=50)
        layout.add_widget(title)
        
        self.status = Label(text='Готов', font_size='18sp')
        layout.add_widget(self.status)
        
        # TilesSurvive locations
        btn1 = Button(text='Village (404, 47)', size_hint_y=None, height=60)
        btn1.bind(on_press=lambda x: self.do_click(x, 404, 47))
        layout.add_widget(btn1)
        
        btn2 = Button(text='Wild Lands (318, 51)', size_hint_y=None, height=60)
        btn2.bind(on_press=lambda x: self.do_click(x, 318, 51))
        layout.add_widget(btn2)
        
        btn3 = Button(text='Search (289, 837)', size_hint_y=None, height=60)
        btn3.bind(on_press=lambda x: self.do_click(x, 289, 837))
        layout.add_widget(btn3)
        
        btn4 = Button(text='Attack (542, 835)', size_hint_y=None, height=60)
        btn4.bind(on_press=lambda x: self.do_click(x, 542, 835))
        layout.add_widget(btn4)
        
        return layout
    
    def do_click(self, instance, x, y):
        self.status.text = f'Клик {x}, {y}'
        
        # Try using platform-specific method
        try:
            from plyer import tts
            tts.speak(text=f'click {x} {y}')
        except:
            pass

if __name__ == '__main__':
    ClickerApp().run()