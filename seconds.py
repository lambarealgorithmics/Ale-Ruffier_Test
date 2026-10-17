# Módulo para cronómetro / timer
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.graphics import Color, Line
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

# Importar sonidos
from sounds import play_timer_warning

# Colores del tema (inline para evitar import circular) - Modo oscuro
CELESTE = '#00B4D8'
CELESTE_LIGHT = '#67E8F9'
GRIS_CLARO_CIRCLE = '#374151'


class Seconds(Label):
    """
    Widget de cuenta regresiva/progresiva en segundos.
    Emite evento 'done' cuando termina.
    """
    
    __events__ = ('on_done',)
    
    done = BooleanProperty(False)
    current = NumericProperty(0)
    total = NumericProperty(0)
    auto_start = BooleanProperty(False)
    text = StringProperty('')
    
    def __init__(self, total=15, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_done')
        self.total = total
        self.current = 0
        self.done = False
        self._clock_event = None
        self._update_text()
        
        if self.auto_start:
            self.start()
    
    def _update_text(self):
        self.text = f'Segundos: {self.current} / {self.total}'
    
    def start(self):
        """Inicia el timer"""
        self.stop()  # Cancelar cualquier timer previo
        self.done = False
        self.current = 0
        self._update_text()
        self._clock_event = Clock.schedule_interval(self._tick, 1)
    
    def restart(self, total=None, **kwargs):
        """Reinicia el timer con nuevo total opcional"""
        if total is not None:
            self.total = total
        self.start()
    
    def stop(self):
        """Detiene el timer"""
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None
    
    def _tick(self, dt):
        """Callback cada segundo"""
        self.current += 1
        self._update_text()
        
        if self.current >= self.total:
            self.done = True
            self.stop()
            self.dispatch('on_done')
            return False  # Detener el intervalo
        return True
    
    def on_done(self, *args):
        """Evento disparado al terminar - puede ser sobrescrito o bindeado"""
        pass


class CircularTimer(Label):
    """
    Timer visual circular para UI moderna.
    Muestra progreso en arco circular.
    """
    
    __events__ = ('on_done',)
    
    progress = NumericProperty(0)  # 0.0 a 1.0
    total = NumericProperty(15)
    current = NumericProperty(0)
    done = BooleanProperty(False)
    time_text = StringProperty('00:15')
    
    def __init__(self, total=15, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_done')
        self.total = total
        self.current = 0
        self.done = False
        self.progress = 0
        self._clock_event = None
        # Radio inicial por defecto (se actualizará cuando el widget tenga tamaño)
        self._circle_radius = dp(80)
        self._update_time_text()
        
        # Dibujar círculo base
        self._draw_circle()
    
    def _update_time_text(self):
        remaining = max(self.total - self.current, 0)
        mins = remaining // 60
        secs = remaining % 60
        self.time_text = f'{mins:02d}:{secs:02d}'
    
    def _draw_circle(self):
        """Dibuja el círculo de progreso con canvas"""
        self.canvas.clear()
        with self.canvas:
            # Fondo del círculo
            Color(*get_color_from_hex(GRIS_CLARO_CIRCLE))
            self.bg_circle = Line(
                circle=(self.center_x, self.center_y, self._circle_radius, 0, 360),
                width=dp(8),
                cap='round'
            )
            # Progreso - color celeste
            Color(*get_color_from_hex(CELESTE))
            self.progress_circle = Line(
                circle=(self.center_x, self.center_y, self._circle_radius, 90, 90),
                width=dp(8),
                cap='round'
            )
        
        self.bind(pos=self._update_circles, size=self._update_circles)
    
    def _update_circles(self, *args):
        # Calcular radio basado en el tamaño menor del widget (menos padding)
        padding = dp(20)
        available_w = max(self.width - padding * 2, dp(10))
        available_h = max(self.height - padding * 2, dp(10))
        self._circle_radius = min(available_w, available_h) / 2
        
        self.bg_circle.circle = (self.center_x, self.center_y, self._circle_radius, 0, 360)
        angle = 360 * self.progress
        self.progress_circle.circle = (self.center_x, self.center_y, self._circle_radius, 90, 90 + angle)
    
    def start(self):
        self.stop()
        self.done = False
        self.current = 0
        self.progress = 0
        self._update_time_text()
        self._update_circles()
        self._clock_event = Clock.schedule_interval(self._tick, 1)
    
    def restart(self, total=None):
        if total is not None:
            self.total = total
        self.start()
    
    def stop(self):
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None
    
    def _tick(self, dt):
        self.current += 1
        self.progress = self.current / self.total
        self._update_time_text()
        self._update_circles()
        
        # Sonido de advertencia en los últimos 3 segundos
        remaining = self.total - self.current
        if remaining == 3:
            play_timer_warning()
        
        if self.current >= self.total:
            self.done = True
            self.stop()
            self.dispatch('on_done')
            return False
        return True
    
    def on_done(self, *args):
        pass