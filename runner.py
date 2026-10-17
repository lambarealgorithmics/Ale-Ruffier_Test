# Módulo para animación de sentadillas (Runner)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

# Importar sonidos
from sounds import play_count

# Colores del tema (inline) - Modo oscuro
CELESTE = '#00B4D8'
CELESTE_LIGHT = '#67E8F9'
TURQUESA = '#00CED1'
NARANJA = '#F39C12'
VERDE = '#2ECC71'
GRIS_MEDIO = '#9CA3AF'
GRIS_OSCURO = '#E5E7EB'


class Runner(BoxLayout):
    """Widget animado que muestra un personaje haciendo sentadillas"""
    
    value = NumericProperty(0)      # Contador actual
    total = NumericProperty(30)     # Total de sentadillas
    finished = BooleanProperty(False)
    steptime = NumericProperty(1.5) # Tiempo por sentadilla (segundos)
    
    def __init__(self, total=30, steptime=1.5, **kwargs):
        super().__init__(**kwargs)
        self.total = total
        self.steptime = steptime
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(15)
        
        # Área de dibujo del avatar
        self.avatar_area = Widget(size_hint=(1, 0.7))
        self._draw_avatar()
        self.add_widget(self.avatar_area)
        
        # Label de estado
        self.lbl_status = Label(
            text='Presiona "Iniciar" para comenzar',
            font_size='16sp',
            size_hint_y=None,
            height=dp(40),
            color=GRIS_MEDIO,
            halign='center',
            valign='middle'
        )
        self.lbl_status.bind(size=self.lbl_status.setter('text_size'))
        self.add_widget(self.lbl_status)
        
        # Contador grande
        self.lbl_counter = Label(
            text='0 / 30',
            font_size='36sp',
            bold=True,
            size_hint_y=None,
            height=dp(60),
            color=CELESTE,
            halign='center',
            valign='middle'
        )
        self.lbl_counter.bind(size=self.lbl_counter.setter('text_size'))
        self.add_widget(self.lbl_counter)
        
        self._current_step = 0
        self._anim_event = None
        self._is_animating = False
    
    def _draw_avatar(self):
        """Dibuja el avatar simple con gráficos de Kivy"""
        self.avatar_area.canvas.clear()
        with self.avatar_area.canvas:
            # Color principal - Turquesa para el avatar
            Color(*get_color_from_hex(TURQUESA))
            
            # Guardamos referencias para animar
            # Cabeza
            self.head = Ellipse(size=(dp(60), dp(60)))
            # Cuerpo
            self.body = RoundedRectangle(size=(dp(80), dp(70)), radius=[dp(10)])
            # Piernas
            self.leg_left = RoundedRectangle(size=(dp(25), dp(50)), radius=[dp(5)])
            self.leg_right = RoundedRectangle(size=(dp(25), dp(50)), radius=[dp(5)])
            # Brazos
            self.arm_left = RoundedRectangle(size=(dp(20), dp(60)), radius=[dp(5)])
            self.arm_right = RoundedRectangle(size=(dp(20), dp(60)), radius=[dp(5)])
        
        # Posicionar inicialmente
        self._update_avatar_pos(standing=True)
        self.avatar_area.bind(pos=self._update_avatar_pos, size=self._update_avatar_pos)
    
    def _update_avatar_pos(self, *args, standing=True):
        """Actualiza posiciones de las partes del avatar"""
        cx = self.avatar_area.center_x
        cy = self.avatar_area.center_y
        
        # Posiciones base (de pie)
        head_y = cy + dp(40)
        body_y = cy - dp(10)
        leg_y = cy - dp(70)
        arm_y = cy + dp(5)
        
        if not standing:
            # Posiciones agachado
            head_y = cy + dp(10)
            body_y = cy - dp(40)
            leg_y = cy - dp(60)  # Piernas flexionadas
            arm_y = cy - dp(20)
        
        self.head.pos = (cx - dp(30), head_y)
        self.body.pos = (cx - dp(40), body_y)
        self.leg_left.pos = (cx - dp(30), leg_y)
        self.leg_right.pos = (cx + dp(5), leg_y)
        self.arm_left.pos = (cx - dp(55), arm_y)
        self.arm_right.pos = (cx + dp(35), arm_y)
    
    def start(self):
        """Inicia la secuencia de sentadillas"""
        self.value = 0
        self.finished = False
        self._current_step = 0
        self._is_animating = True
        self.lbl_counter.text = f'0 / {self.total}'
        self.lbl_status.text = '¡Comienza!'
        self.lbl_status.color = NARANJA
        self._do_squat()
    
    def _do_squat(self):
        """Ejecuta una animación de sentadilla completa"""
        if not self._is_animating or self._current_step >= self.total:
            self._finish()
            return
        
        self._current_step += 1
        self.value = self._current_step
        self.lbl_counter.text = f'{self._current_step} / {self.total}'
        self.lbl_status.text = f'Sentadilla {self._current_step} de {self.total}'
        
        # Animación: bajar (0.5 * steptime) + subir (0.5 * steptime)
        half_time = self.steptime * 0.5
        
        # Animar a posición agachado
        anim_down = Animation(duration=half_time, t='out_quad')
        anim_down.bind(on_complete=lambda *a: self._animate_up(half_time))
        
        # Animamos las propiedades gráficas directamente
        # Para simplificar, usamos un callback con Clock
        self._animate_down(half_time)
    
    def _animate_down(self, duration):
        """Anima bajada"""
        # Animación simple usando Clock para interpolar
        start_time = Clock.get_time()
        target_leg_y = self.leg_left.pos[1] + dp(20)  # Suben las piernas al agacharse
        
        def update_down(dt):
            elapsed = Clock.get_time() - start_time
            progress = min(elapsed / duration, 1.0)
            eased = 1 - (1 - progress) ** 2  # out_quad
            
            # Interpolar piernas
            leg_y = self.leg_left.pos[1] + (target_leg_y - self.leg_left.pos[1]) * eased
            self.leg_left.pos = (self.leg_left.pos[0], leg_y)
            self.leg_right.pos = (self.leg_right.pos[0], leg_y)
            
            # Cuerpo y cabeza bajan
            body_y = self.body.pos[1] - dp(30) * eased
            self.body.pos = (self.body.pos[0], body_y)
            head_y = self.head.pos[1] - dp(30) * eased
            self.head.pos = (self.head.pos[0], head_y)
            
            # Brazos bajan
            arm_y = self.arm_left.pos[1] - dp(25) * eased
            self.arm_left.pos = (self.arm_left.pos[0], arm_y)
            self.arm_right.pos = (self.arm_right.pos[0], arm_y)
            
            if progress >= 1.0:
                return False  # Detener Clock
            return True
        
        Clock.schedule_interval(update_down, 1/60)
        Clock.schedule_once(lambda dt: self._animate_up(duration), duration)
    
    def _animate_up(self, duration):
        """Anima subida"""
        start_time = Clock.get_time()
        
        # Posiciones objetivo (de pie)
        cx = self.avatar_area.center_x
        cy = self.avatar_area.center_y
        target_leg_y = cy - dp(70)
        target_body_y = cy - dp(10)
        target_head_y = cy + dp(40)
        target_arm_y = cy + dp(5)
        
        start_leg_y = self.leg_left.pos[1]
        start_body_y = self.body.pos[1]
        start_head_y = self.head.pos[1]
        start_arm_y = self.arm_left.pos[1]
        
        def update_up(dt):
            elapsed = Clock.get_time() - start_time
            progress = min(elapsed / duration, 1.0)
            eased = progress ** 2  # in_quad
            
            leg_y = start_leg_y + (target_leg_y - start_leg_y) * eased
            self.leg_left.pos = (self.leg_left.pos[0], leg_y)
            self.leg_right.pos = (self.leg_right.pos[0], leg_y)
            
            body_y = start_body_y + (target_body_y - start_body_y) * eased
            self.body.pos = (self.body.pos[0], body_y)
            
            head_y = start_head_y + (target_head_y - start_head_y) * eased
            self.head.pos = (self.head.pos[0], head_y)
            
            arm_y = start_arm_y + (target_arm_y - start_arm_y) * eased
            self.arm_left.pos = (self.arm_left.pos[0], arm_y)
            self.arm_right.pos = (self.arm_right.pos[0], arm_y)
            
            if progress >= 1.0:
                # Sonido al completar la sentadilla (al subir)
                play_count()
                # Programar siguiente sentadilla
                Clock.schedule_once(lambda dt: self._do_squat(), 0.1)
                return False
            return True
        
        Clock.schedule_interval(update_up, 1/60)
    
    def _finish(self):
        """Termina la rutina"""
        self._is_animating = False
        self.finished = True
        self.lbl_status.text = '¡Completado! Bien hecho'
        self.lbl_status.color = VERDE
    
    def reset(self):
        """Reinicia el runner"""
        self._is_animating = False
        if self._anim_event:
            self._anim_event.cancel()
        self.value = 0
        self.finished = False
        self._current_step = 0
        self.lbl_counter.text = f'0 / {self.total}'
        self.lbl_status.text = 'Presiona "Iniciar" para comenzar'
        self.lbl_status.color = GRIS_MEDIO
        self._update_avatar_pos(standing=True)
    
    def stop(self):
        """Detiene la animación actual"""
        self._is_animating = False