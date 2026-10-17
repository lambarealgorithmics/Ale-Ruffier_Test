from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex

from instructions import txt_instruction, txt_test1, txt_test2, txt_test3, txt_sits
from ruffier import test, get_result_details
from seconds import Seconds, CircularTimer
from sits import Sits
from runner import Runner
from sounds import sound_manager, play_click, play_start, play_complete, play_phase_change, play_count, play_error, play_success, play_timer_warning, create_default_sounds

# Importar tema de colores
from theme import (
    CELESTE, CELESTE_LIGHT, CELESTE_DARK, CELESTE_VERY_LIGHT,
    VERDE, VERDE_LIGHT, VERDE_DARK, VERDE_VERY_LIGHT,
    NARANJA, NARANJA_LIGHT, NARANJA_DARK, NARANJA_VERY_LIGHT,
    TURQUESA, TURQUESA_LIGHT, TURQUESA_DARK, TURQUESA_VERY_LIGHT,
    BLANCO, GRIS_OSCURO, GRIS_MEDIO, GRIS_CLARO, GRIS_MUY_CLARO, GRIS_FONDO,
    EXITO, ADVERTENCIA, ERROR,
    TEXT_STYLES, BUTTON_STYLES, INPUT_STYLES,
    SPACING, BUTTON_HEIGHT, INPUT_HEIGHT, CARD_RADIUS, BUTTON_RADIUS,
    hex_to_rgba, get_result_color, get_result_label, GRADIENTES
)


# ============================================================
# Utilidades de validación
# ============================================================

def parse_int(text: str) -> int | None:
    """Convierte texto a entero, retorna None si inválido"""
    try:
        val = int(text.strip())
        return val if val > 0 else None
    except (ValueError, AttributeError):
        return None


# ============================================================
# Pantalla 1: Instrucciones + Datos del usuario
# ============================================================

class InstrScr(Screen):
    name_input = ObjectProperty(None)
    age_input = ObjectProperty(None)
    btn_start = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        # Fondo de pantalla
        with self.canvas.before:
            Color(*hex_to_rgba(GRIS_FONDO))
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        main = BoxLayout(orientation='vertical', padding=SPACING['lg'], spacing=SPACING['md'])
        
        # Header con icono
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(110), spacing=SPACING['xs'])
        header.add_widget(Label(
            text='🫀  Test de Ruffier',
            font_size=TEXT_STYLES['display']['font_size'],
            bold=True,
            color=CELESTE_DARK,
            size_hint_y=None,
            height=dp(50),
            halign='center',
            valign='middle'
        ))
        header.add_widget(Label(
            text='Evaluación de eficiencia cardíaca',
            font_size=TEXT_STYLES['subtitle']['font_size'],
            color=GRIS_MEDIO,
            halign='center',
            valign='middle'
        ))
        main.add_widget(header)
        
        # Card de instrucciones - ocupa más espacio para mostrar todos los pasos
        instr_card = BoxLayout(
            orientation='vertical',
            padding=SPACING['md'],
            size_hint=(1, 0.55)
        )
        with instr_card.canvas.before:
            Color(*hex_to_rgba(CELESTE_VERY_LIGHT))
            instr_card.bg_rect = RoundedRectangle(radius=[CARD_RADIUS])
        instr_card.bind(pos=self._update_instr_bg, size=self._update_instr_bg)
        self.instr_card = instr_card
        
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        instr_label = Label(
            text=txt_instruction,
            font_size=TEXT_STYLES['body']['font_size'],
            color=GRIS_MEDIO,
            halign='left',
            valign='top',
            text_size=(None, None),
            padding=(SPACING['md'], SPACING['md']),
            markup=True
        )
        # Configurar el text_size para que el label se expanda horizontalmente
        # y la altura se ajuste al contenido
        def update_text_size(instance, value):
            instance.text_size = (instance.width, None)
        def update_height(instance, value):
            instance.height = instance.texture_size[1]
        instr_label.bind(width=update_text_size, texture_size=update_height)
        scroll.add_widget(instr_label)
        instr_card.add_widget(scroll)
        main.add_widget(instr_card)
        
        # Formulario
        form = BoxLayout(orientation='vertical', spacing=SPACING['md'], size_hint_y=None, height=dp(150))
        
        # Nombre
        name_row = BoxLayout(orientation='vertical', spacing=SPACING['xs'])
        name_row.add_widget(Label(
            text='Nombre completo',
            font_size=TEXT_STYLES['input_label']['font_size'],
            bold=True,
            color=GRIS_OSCURO,
            halign='left',
            size_hint_y=None,
            height=dp(22)
        ))
        self.name_input = TextInput(
            hint_text='Ej: Juan Pérez',
            multiline=False,
            font_size=TEXT_STYLES['input_hint']['font_size'],
            size_hint_y=None,
            height=INPUT_HEIGHT,
            padding=INPUT_STYLES['default']['padding'],
            background_color=INPUT_STYLES['default']['background_color'],
            foreground_color=INPUT_STYLES['default']['foreground_color'],
            cursor_color=INPUT_STYLES['default']['cursor_color']
        )
        name_row.add_widget(self.name_input)
        form.add_widget(name_row)
        
        # Edad
        age_row = BoxLayout(orientation='vertical', spacing=SPACING['xs'])
        age_row.add_widget(Label(
            text='Edad (años)',
            font_size=TEXT_STYLES['input_label']['font_size'],
            bold=True,
            color=GRIS_OSCURO,
            halign='left',
            size_hint_y=None,
            height=dp(22)
        ))
        self.age_input = TextInput(
            hint_text='Ej: 25',
            multiline=False,
            input_filter='int',
            font_size=TEXT_STYLES['input_hint']['font_size'],
            size_hint_y=None,
            height=INPUT_HEIGHT,
            padding=INPUT_STYLES['default']['padding'],
            background_color=INPUT_STYLES['default']['background_color'],
            foreground_color=INPUT_STYLES['default']['foreground_color'],
            cursor_color=INPUT_STYLES['default']['cursor_color']
        )
        age_row.add_widget(self.age_input)
        form.add_widget(age_row)
        
        main.add_widget(form)
        
        # Botón principal
        self.btn_start = Button(
            text='COMENZAR',
            font_size=BUTTON_STYLES['primary']['font_size'] if 'font_size' in BUTTON_STYLES['primary'] else TEXT_STYLES['button']['font_size'],
            bold=TEXT_STYLES['button']['bold'],
            size_hint_y=None,
            height=BUTTON_HEIGHT,
            **{k: v for k, v in BUTTON_STYLES['primary'].items() if k != 'font_size'}
        )
        self.btn_start.bind(on_press=self.on_start)
        main.add_widget(self.btn_start)
        
        # Nota
        main.add_widget(Label(
            text='ℹ️  Para mayores de 7 años',
            font_size=TEXT_STYLES['body_small']['font_size'],
            color=GRIS_CLARO,
            halign='center',
            size_hint_y=None,
            height=dp(28)
        ))
        
        self.add_widget(main)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def _update_instr_bg(self, *args):
        if hasattr(self, 'instr_card') and self.instr_card:
            if hasattr(self.instr_card, 'bg_rect') and self.instr_card.bg_rect:
                self.instr_card.bg_rect.pos = self.instr_card.pos
                self.instr_card.bg_rect.size = self.instr_card.size
    
    def on_start(self, instance):
        play_click()
        name = self.name_input.text.strip()
        age = parse_int(self.age_input.text)
        
        if not name:
            play_error()
            self._show_error('Por favor ingresa tu nombre')
            return
        
        if age is None or age < 7:
            play_error()
            self._show_error('La edad debe ser 7 años o más')
            self.age_input.text = '7'
            return
        
        # Guardar en la app
        app = App.get_running_app()
        app.user_name = name
        app.user_age = age
        
        play_start()
        # Navegar
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'pulse1'
    
    def _show_error(self, msg):
        play_error()
        self.btn_start.text = msg
        self.btn_start.background_color = '#DC2626'
        Clock.schedule_once(lambda dt: self._reset_button(), 2)
    
    def _reset_button(self):
        self.btn_start.text = 'COMENZAR'
        self.btn_start.background_color = '#2563EB'


# ============================================================
# Pantalla 2: Pulso en reposo (15 seg)
# ============================================================

class PulseScr(Screen):
    timer = ObjectProperty(None)
    result_input = ObjectProperty(None)
    btn_action = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._stage = 'ready'  # ready, running, done
        self.build_ui()
    
    def build_ui(self):
        with self.canvas.before:
            Color(*hex_to_rgba(GRIS_FONDO))
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        main = BoxLayout(orientation='vertical', padding=SPACING['lg'], spacing=SPACING['md'])
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(50))
        header.add_widget(Label(
            text='←',
            font_size=sp(28),
            color=GRIS_MEDIO,
            size_hint_x=None,
            width=dp(48),
            halign='left'
        ))
        header.add_widget(Label(
            text='Pulso en Reposo',
            font_size=TEXT_STYLES['headline']['font_size'],
            bold=True,
            color=GRIS_OSCURO,
            halign='center'
        ))
        main.add_widget(header)
        
        # Instrucción en card
        instr_card = BoxLayout(orientation='vertical', padding=SPACING['md'], size_hint_y=None, height=dp(100))
        with instr_card.canvas.before:
            Color(*hex_to_rgba(CELESTE_VERY_LIGHT))
            self.instr_bg = RoundedRectangle(radius=[CARD_RADIUS])
        instr_card.bind(pos=self._update_instr_bg, size=self._update_instr_bg)
        
        instr_card.add_widget(Label(
            text=txt_test1,
            font_size=TEXT_STYLES['body']['font_size'],
            color=GRIS_MEDIO,
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(70),
            text_size=(None, None)
        ))
        main.add_widget(instr_card)
        
        # Timer circular
        self.timer = CircularTimer(total=15, size_hint=(1, 0.35))
        self.timer.bind(on_done=self.on_timer_done)
        main.add_widget(self.timer)
        
        # Input resultado
        input_row = BoxLayout(orientation='vertical', spacing=SPACING['xs'], size_hint_y=None, height=dp(100))
        input_row.add_widget(Label(
            text='Tu resultado (latidos en 15 seg)',
            font_size=TEXT_STYLES['input_label']['font_size'],
            bold=True,
            color=GRIS_OSCURO,
            halign='left',
            size_hint_y=None,
            height=dp(24)
        ))
        self.result_input = TextInput(
            hint_text='Ej: 18',
            multiline=False,
            input_filter='int',
            font_size=sp(28),
            halign='center',
            size_hint_y=None,
            height=dp(60),
            padding=(dp(16), dp(12)),
            disabled=True,
            background_color=INPUT_STYLES['disabled']['background_color'],
            foreground_color=INPUT_STYLES['disabled']['foreground_color'],
            cursor_color=CELESTE
        )
        input_row.add_widget(self.result_input)
        main.add_widget(input_row)
        
        # Botón
        self.btn_action = Button(
            text='INICIAR',
            font_size=TEXT_STYLES['button']['font_size'],
            bold=TEXT_STYLES['button']['bold'],
            size_hint_y=None,
            height=BUTTON_HEIGHT,
            **{k: v for k, v in BUTTON_STYLES['primary'].items() if k != 'font_size'}
        )
        self.btn_action.bind(on_press=self.on_action)
        main.add_widget(self.btn_action)
        
        self.add_widget(main)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def _update_instr_bg(self, *args):
        if hasattr(self, 'instr_card') and self.instr_card:
            if hasattr(self.instr_card, 'bg_rect') and self.instr_card.bg_rect:
                self.instr_card.bg_rect.pos = self.instr_card.pos
                self.instr_card.bg_rect.size = self.instr_card.size
    
    def on_timer_done(self, *args):
        play_phase_change()
        self._stage = 'done'
        self.result_input.disabled = False
        self.result_input.background_color = INPUT_STYLES['default']['background_color']
        self.result_input.foreground_color = INPUT_STYLES['default']['foreground_color']
        self.result_input.focus = True
        self.btn_action.text = 'CONTINUAR'
        self.btn_action.background_color = VERDE
        self.btn_action.disabled = False
    
    def on_action(self, instance):
        play_click()
        if self._stage == 'ready':
            play_start()
            self._stage = 'running'
            self.btn_action.text = 'ESPERA...'
            self.btn_action.disabled = True
            self.btn_action.background_color = GRIS_CLARO
            self.timer.start()
        elif self._stage == 'done':
            p1 = parse_int(self.result_input.text)
            if p1 is None:
                self.result_input.text = '1'
                p1 = 1
            
            app = App.get_running_app()
            app.p1 = p1
            
            play_success()
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'sits'
    
    def on_enter(self, *args):
        self._stage = 'ready'
        self.result_input.disabled = True
        self.result_input.background_color = INPUT_STYLES['disabled']['background_color']
        self.result_input.foreground_color = INPUT_STYLES['disabled']['foreground_color']
        self.result_input.text = ''
        self.btn_action.text = 'INICIAR'
        self.btn_action.disabled = False
        self.btn_action.background_color = CELESTE
        # Detener timer previo y resetear
        self.timer.stop()
        self.timer.current = 0
        self.timer.progress = 0
        self.timer.done = False
        self.timer._update_time_text()
        self.timer._update_circles()


# ============================================================
# Pantalla 3: Sentadillas (30 en 45 seg)
# ============================================================

class CheckSits(Screen):
    sits_widget = ObjectProperty(None)
    btn_next = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        with self.canvas.before:
            Color(*hex_to_rgba(GRIS_FONDO))
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        main = BoxLayout(orientation='vertical', padding=SPACING['lg'], spacing=SPACING['md'])
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(50))
        header.add_widget(Label(
            text='←',
            font_size=sp(28),
            color=GRIS_MEDIO,
            size_hint_x=None,
            width=dp(48),
            halign='left'
        ))
        header.add_widget(Label(
            text='Ejercicio: Sentadillas',
            font_size=TEXT_STYLES['headline']['font_size'],
            bold=True,
            color=GRIS_OSCURO,
            halign='center'
        ))
        main.add_widget(header)
        
        # Instrucción breve en card
        instr_card = BoxLayout(orientation='vertical', padding=SPACING['md'], size_hint_y=None, height=dp(80))
        with instr_card.canvas.before:
            Color(*hex_to_rgba(NARANJA_VERY_LIGHT))
            self.instr_bg = RoundedRectangle(radius=[CARD_RADIUS])
        instr_card.bind(pos=self._update_instr_bg, size=self._update_instr_bg)
        
        instr_card.add_widget(Label(
            text=txt_sits,
            font_size=TEXT_STYLES['body']['font_size'],
            color=NARANJA_DARK,
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(50)
        ))
        main.add_widget(instr_card)
        
        # Widget de sentadillas (Sits contiene Runner + contador)
        self.sits_widget = Sits(total=30)
        self.sits_widget.bind(finished=self.on_sits_finished)
        main.add_widget(self.sits_widget)
        
        # Botón siguiente (inicialmente oculto/deshabilitado)
        self.btn_next = Button(
            text='CONTINUAR',
            font_size=TEXT_STYLES['button']['font_size'],
            bold=TEXT_STYLES['button']['bold'],
            size_hint_y=None,
            height=BUTTON_HEIGHT,
            **{k: v for k, v in BUTTON_STYLES['success'].items() if k != 'font_size'},
            disabled=True,
            opacity=0.5
        )
        self.btn_next.bind(on_press=self.on_next)
        main.add_widget(self.btn_next)
        
        self.add_widget(main)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def _update_instr_bg(self, *args):
        if hasattr(self, 'instr_card') and self.instr_card:
            if hasattr(self.instr_card, 'bg_rect') and self.instr_card.bg_rect:
                self.instr_card.bg_rect.pos = self.instr_card.pos
                self.instr_card.bg_rect.size = self.instr_card.size
    
    def on_enter(self, *args):
        # Iniciar automáticamente al entrar
        Clock.schedule_once(lambda dt: self.sits_widget.start(), 0.5)
    
    def on_sits_finished(self, instance, finished):
        if finished:
            play_complete()
            self.btn_next.disabled = False
            self.btn_next.opacity = 1
            self.sits_widget.runner.lbl_status.text = '¡Completado! Presiona Continuar'
    
    def on_next(self, instance):
        play_click()
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'pulse2'


# ============================================================
# Pantalla 4: Pulso post-esfuerzo (3 fases)
# ============================================================

class PulseScr2(Screen):
    timer = ObjectProperty(None)
    lbl_phase = ObjectProperty(None)
    input1 = ObjectProperty(None)
    input2 = ObjectProperty(None)
    btn_action = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._phase = 0  # 0=ready, 1=phase1, 2=rest, 3=phase3, 4=done
        self.build_ui()
    
    def build_ui(self):
        with self.canvas.before:
            Color(*hex_to_rgba(GRIS_FONDO))
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        main = BoxLayout(orientation='vertical', padding=SPACING['lg'], spacing=SPACING['md'])
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(50))
        header.add_widget(Label(
            text='←',
            font_size=sp(28),
            color=GRIS_MEDIO,
            size_hint_x=None,
            width=dp(48),
            halign='left'
        ))
        header.add_widget(Label(
            text='Recuperación',
            font_size=TEXT_STYLES['headline']['font_size'],
            bold=True,
            color=GRIS_OSCURO,
            halign='center'
        ))
        main.add_widget(header)
        
        # Indicador de fase
        self.lbl_phase = Label(
            text='FASE 1/3: Pulso post-esfuerzo',
            font_size=TEXT_STYLES['subtitle']['font_size'],
            bold=True,
            color=CELESTE,
            size_hint_y=None,
            height=dp(36),
            halign='center'
        )
        main.add_widget(self.lbl_phase)
        
        # Instrucción en card
        instr_card = BoxLayout(orientation='vertical', padding=SPACING['md'], size_hint_y=None, height=dp(100))
        with instr_card.canvas.before:
            Color(*hex_to_rgba(TURQUESA_VERY_LIGHT))
            self.instr_bg = RoundedRectangle(radius=[CARD_RADIUS])
        instr_card.bind(pos=self._update_instr_bg, size=self._update_instr_bg)
        
        instr_card.add_widget(Label(
            text=txt_test3,
            font_size=TEXT_STYLES['body']['font_size'],
            color=TURQUESA_DARK,
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(70)
        ))
        main.add_widget(instr_card)
        
        # Timer circular - más espacio vertical para evitar superposición
        self.timer = CircularTimer(total=15, size_hint=(1, 0.4))
        self.timer.bind(on_done=self.on_timer_done)
        main.add_widget(self.timer)
        
        # Inputs de resultados
        inputs_box = BoxLayout(orientation='vertical', spacing=SPACING['sm'], size_hint_y=None, height=dp(160))
        
        # Pulso 1
        row1 = BoxLayout(orientation='vertical', spacing=SPACING['xs'])
        row1.add_widget(Label(
            text='Pulso 1 (inmediato post-esfuerzo)',
            font_size=sp(12),
            color=GRIS_CLARO,
            halign='left',
            size_hint_y=None,
            height=dp(20)
        ))
        self.input1 = TextInput(
            hint_text='—',
            multiline=False,
            input_filter='int',
            font_size=sp(22),
            halign='center',
            size_hint_y=None,
            height=dp(56),
            disabled=True,
            background_color=INPUT_STYLES['disabled']['background_color'],
            foreground_color=INPUT_STYLES['disabled']['foreground_color']
        )
        row1.add_widget(self.input1)
        inputs_box.add_widget(row1)
        
        # Pulso 2
        row2 = BoxLayout(orientation='vertical', spacing=SPACING['xs'])
        row2.add_widget(Label(
            text='Pulso 2 (tras 30 seg descanso)',
            font_size=sp(12),
            color=GRIS_CLARO,
            halign='left',
            size_hint_y=None,
            height=dp(20)
        ))
        self.input2 = TextInput(
            hint_text='—',
            multiline=False,
            input_filter='int',
            font_size=sp(22),
            halign='center',
            size_hint_y=None,
            height=dp(56),
            disabled=True,
            background_color=INPUT_STYLES['disabled']['background_color'],
            foreground_color=INPUT_STYLES['disabled']['foreground_color']
        )
        row2.add_widget(self.input2)
        inputs_box.add_widget(row2)
        
        main.add_widget(inputs_box)
        
        # Botón
        self.btn_action = Button(
            text='INICIAR',
            font_size=TEXT_STYLES['button']['font_size'],
            bold=TEXT_STYLES['button']['bold'],
            size_hint_y=None,
            height=BUTTON_HEIGHT,
            **{k: v for k, v in BUTTON_STYLES['primary'].items() if k != 'font_size'}
        )
        self.btn_action.bind(on_press=self.on_action)
        main.add_widget(self.btn_action)
        
        self.add_widget(main)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def _update_instr_bg(self, *args):
        if hasattr(self, 'instr_card') and self.instr_card:
            if hasattr(self.instr_card, 'bg_rect') and self.instr_card.bg_rect:
                self.instr_card.bg_rect.pos = self.instr_card.pos
                self.instr_card.bg_rect.size = self.instr_card.size
    
    def on_timer_done(self, *args):
        if self._phase == 1:
            # Fase 1 terminada -> habilitar input1, iniciar descanso
            self._phase = 2
            self.input1.disabled = False
            self.input1.background_color = INPUT_STYLES['default']['background_color']
            self.input1.foreground_color = INPUT_STYLES['default']['foreground_color']
            self.input1.focus = True
            self.lbl_phase.text = 'FASE 2/3: Descanso (30 seg)'
            self.lbl_phase.color = VERDE
            self.timer.restart(total=30)
            self.timer.start()
            play_phase_change()
            
        elif self._phase == 2:
            # Descanso terminado -> iniciar fase 3
            self._phase = 3
            self.lbl_phase.text = 'FASE 3/3: Pulso recuperación'
            self.lbl_phase.color = NARANJA
            self.timer.restart(total=15)
            self.timer.start()
            play_phase_change()
            
        elif self._phase == 3:
            # Fase 3 terminada -> habilitar input2, finalizar
            self._phase = 4
            self.input2.disabled = False
            self.input2.background_color = INPUT_STYLES['default']['background_color']
            self.input2.foreground_color = INPUT_STYLES['default']['foreground_color']
            self.input2.focus = True
            self.lbl_phase.text = '¡Completado!'
            self.lbl_phase.color = VERDE
            self.btn_action.text = 'VER RESULTADO'
            self.btn_action.background_color = VERDE
            self.btn_action.disabled = False
            play_complete()
    
    def on_action(self, instance):
        play_click()
        if self._phase == 0:
            # Iniciar fase 1
            self._phase = 1
            self.btn_action.text = 'ESPERA...'
            self.btn_action.disabled = True
            self.btn_action.background_color = GRIS_CLARO
            self.timer.start()
            play_start()
        elif self._phase == 4:
            # Navegar a resultados
            play_success()
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'result'
    
    def on_enter(self, *args):
        self._phase = 0
        self.input1.disabled = True
        self.input1.background_color = INPUT_STYLES['disabled']['background_color']
        self.input1.foreground_color = INPUT_STYLES['disabled']['foreground_color']
        self.input1.text = ''
        self.input2.disabled = True
        self.input2.background_color = INPUT_STYLES['disabled']['background_color']
        self.input2.foreground_color = INPUT_STYLES['disabled']['foreground_color']
        self.input2.text = ''
        self.btn_action.text = 'INICIAR'
        self.btn_action.disabled = False
        self.btn_action.background_color = CELESTE
        self.lbl_phase.text = 'FASE 1/3: Pulso post-esfuerzo'
        self.lbl_phase.color = CELESTE
        self.timer.current = 0
        self.timer.progress = 0
        self.timer.done = False
        self.timer._update_time_text()
        self.timer._update_circles()
    
    def on_leave(self, *args):
        # Guardar resultados al salir
        if self._phase == 4:
            p2 = parse_int(self.input1.text)
            p3 = parse_int(self.input2.text)
            
            if p2 is None:
                p2 = 1
                self.input1.text = '1'
            if p3 is None:
                p3 = 1
                self.input2.text = '1'
            
            app = App.get_running_app()
            app.p2 = p2
            app.p3 = p3


# ============================================================
# Pantalla 5: Resultado
# ============================================================

class ResultScr(Screen):
    result_label = ObjectProperty(None)
    details_label = ObjectProperty(None)
    btn_restart = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        with self.canvas.before:
            Color(*hex_to_rgba(GRIS_FONDO))
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        main = BoxLayout(orientation='vertical', padding=SPACING['lg'], spacing=SPACING['md'])
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(50))
        header.add_widget(Label(
            text='←',
            font_size=sp(28),
            color=GRIS_MEDIO,
            size_hint_x=None,
            width=dp(48),
            halign='left'
        ))
        header.add_widget(Label(
            text='Resultado',
            font_size=TEXT_STYLES['headline']['font_size'],
            bold=True,
            color=GRIS_OSCURO,
            halign='center'
        ))
        main.add_widget(header)
        
        # Nombre
        self.name_label = Label(
            text='',
            font_size=sp(22),
            bold=True,
            color=CELESTE_DARK,
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        main.add_widget(self.name_label)
        
        # Card de resultado principal
        self.result_card = BoxLayout(
            orientation='vertical',
            padding=SPACING['lg'],
            spacing=SPACING['sm'],
            size_hint_y=None,
            height=dp(200)
        )
        
        # Fondo de la card (usamos canvas)
        with self.result_card.canvas.before:
            self.card_bg_color = Color(*hex_to_rgba(CELESTE))
            self.card_bg = RoundedRectangle(radius=[CARD_RADIUS])
        self.result_card.bind(pos=self._update_card_bg, size=self._update_card_bg)
        
        self.result_index = Label(
            text='Índice: —',
            font_size=sp(42),
            bold=True,
            color=BLANCO,
            halign='center'
        )
        self.result_card.add_widget(self.result_index)
        
        self.result_level = Label(
            text='—',
            font_size=sp(24),
            bold=True,
            color=BLANCO,
            halign='center'
        )
        self.result_card.add_widget(self.result_level)
        
        self.result_desc = Label(
            text='',
            font_size=TEXT_STYLES['body']['font_size'],
            color=BLANCO,
            halign='center',
            text_size=(None, None)
        )
        self.result_card.add_widget(self.result_desc)
        
        main.add_widget(self.result_card)
        
        # Detalles
        self.details_label = Label(
            text='',
            font_size=TEXT_STYLES['body_small']['font_size'],
            color=GRIS_CLARO,
            halign='center',
            valign='top',
            size_hint_y=None,
            height=dp(90)
        )
        main.add_widget(self.details_label)
        
        # Botón reiniciar (outline)
        self.btn_restart = Button(
            text='REALIZAR OTRA PRUEBA',
            font_size=TEXT_STYLES['button_outline']['font_size'],
            bold=TEXT_STYLES['button_outline']['bold'],
            size_hint_y=None,
            height=BUTTON_HEIGHT,
            **{k: v for k, v in BUTTON_STYLES['outline_primary'].items() if k != 'font_size'}
        )
        with self.btn_restart.canvas.before:
            Color(*hex_to_rgba(CELESTE, 0.1))
            self.btn_border = RoundedRectangle(radius=[BUTTON_RADIUS])
        self.btn_restart.bind(pos=self._update_btn_border, size=self._update_btn_border)
        self.btn_restart.bind(on_press=self.on_restart)
        main.add_widget(self.btn_restart)
        
        self.add_widget(main)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def _update_card_bg(self, *args):
        self.card_bg.pos = self.result_card.pos
        self.card_bg.size = self.result_card.size
    
    def _update_btn_border(self, *args):
        self.btn_border.pos = (self.btn_restart.x, self.btn_restart.y)
        self.btn_border.size = (self.btn_restart.width, self.btn_restart.height)
    
    def on_enter(self, *args):
        play_success()
        app = App.get_running_app()
        
        name = getattr(app, 'user_name', 'Usuario')
        age = getattr(app, 'user_age', 25)
        p1 = getattr(app, 'p1', 0)
        p2 = getattr(app, 'p2', 0)
        p3 = getattr(app, 'p3', 0)
        
        self.name_label.text = name
        
        details = get_result_details(p1, p2, p3, age)
        
        if details['valid']:
            self.result_index.text = f"Índice: {details['index']}"
            self.result_level.text = get_result_label(details['level_idx'])
            self.result_desc.text = details['description']
            
            # Actualizar color de la card usando el tema
            self.card_bg_color.rgba = hex_to_rgba(get_result_color(details['level_idx']))
            
            self.details_label.text = (
                f"P1 (reposo): {p1}  |  "
                f"P2 (post-esfuerzo): {p2}  |  "
                f"P3 (recuperación): {p3}\n"
                f"Edad: {age} años"
            )
        else:
            self.result_index.text = 'Sin datos'
            self.result_level.text = 'EDAD NO VÁLIDA'
            self.result_desc.text = 'La prueba es para mayores de 7 años'
            self.card_bg_color.rgba = hex_to_rgba(GRIS_CLARO)
            self.details_label.text = ''
    
    def on_restart(self, instance):
        play_click()
        app = App.get_running_app()
        # Resetear datos
        app.user_name = ''
        app.user_age = 0
        app.p1 = app.p2 = app.p3 = 0
        
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'instr'


# ============================================================
# App Principal
# ============================================================

class HeartCheck(App):
    # Propiedades para almacenar datos del usuario (reemplazan variables globales)
    user_name = StringProperty('')
    user_age = NumericProperty(0)
    p1 = NumericProperty(0)
    p2 = NumericProperty(0)
    p3 = NumericProperty(0)
    
    def build(self):
        self.title = 'Test de Ruffier'
        
        # Crear sonidos por defecto si no existen archivos
        create_default_sounds()
        
        sm = ScreenManager()
        sm.transition = SlideTransition(duration=0.25)
        
        sm.add_widget(InstrScr(name='instr'))
        sm.add_widget(PulseScr(name='pulse1'))
        sm.add_widget(CheckSits(name='sits'))
        sm.add_widget(PulseScr2(name='pulse2'))
        sm.add_widget(ResultScr(name='result'))
        
        return sm
    
    def on_pause(self):
        return True
    
    def on_resume(self):
        pass


if __name__ == '__main__':
    HeartCheck().run()