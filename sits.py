# Módulo para contar sentadillas con animación
from kivy.uix.label import Label
from kivy.properties import NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from runner import Runner


class Sits(BoxLayout):
    """Widget que muestra el contador de sentadillas y la animación del personaje"""
    
    counter = NumericProperty(0)
    total = NumericProperty(30)
    finished = BooleanProperty(False)
    
    def __init__(self, total=30, **kwargs):
        super().__init__(**kwargs)
        self.total = total
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(20)
        
        # Label del contador
        self.lbl_counter = Label(
            text=f'Sentadillas: 0 / {self.total}',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40),
            color='#1F2937'
        )
        
        # Runner (personaje animado) - usa la clase de runner.py
        self.runner = Runner(
            total=self.total,
            steptime=1.5,
            size_hint=(1, 0.6)
        )
        
        self.add_widget(self.lbl_counter)
        self.add_widget(self.runner)
        
        # Bind para actualizar contador
        self.runner.bind(value=self._update_counter)
        self.runner.bind(finished=self._on_finished)
    
    def _update_counter(self, instance, value):
        self.counter = value
        self.lbl_counter.text = f'Sentadillas: {self.counter} / {self.total}'
    
    def _on_finished(self, instance, value):
        if value:
            self.finished = True
    
    def start(self):
        self.counter = 0
        self.finished = False
        self.lbl_counter.text = f'Sentadillas: 0 / {self.total}'
        self.runner.start()
    
    def reset(self):
        self.runner.reset()
        self.counter = 0
        self.finished = False
        self.lbl_counter.text = f'Sentadillas: 0 / {self.total}'