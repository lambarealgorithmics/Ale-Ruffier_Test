from kivy.clock import Clock
from kivy.base import EventLoop
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from seconds import CircularTimer

class TestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.timer = CircularTimer(total=3, size_hint=(1, 0.5))
        self.btn = Button(text='Start', size_hint=(1, 0.1))
        self.btn.bind(on_press=self.on_start)
        layout.add_widget(self.timer)
        layout.add_widget(self.btn)
        self.add_widget(layout)
        self.timer.bind(on_done=self.on_done)
        
    def on_start(self, *args):
        print('Starting timer...')
        self.timer.start()
        self.btn.disabled = True
        
    def on_done(self, *args):
        print('Timer DONE! Enabling button...')
        self.btn.disabled = False
        self.btn.text = 'DONE!'

class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TestScreen(name='test'))
        return sm

if __name__ == '__main__':
    TestApp().run()