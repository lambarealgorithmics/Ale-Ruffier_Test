"""
Sistema de colores y tema visual para la app Test de Ruffier
Paleta: Celeste, Verde, Naranja, Turquesa
"""

from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex

# ============================================================
# PALETA PRINCIPAL
# ============================================================

# Celeste - Color principal de la app (confianza, salud)
CELESTE = '#00B4D8'
CELESTE_LIGHT = '#67E8F9'
CELESTE_DARK = '#0096C7'
CELESTE_VERY_LIGHT = '#0C4A6E'  # Fondo card oscuro

# Verde - Éxito, completado, salud buena
VERDE = '#2ECC71'
VERDE_LIGHT = '#86EFAC'
VERDE_DARK = '#27AE60'
VERDE_VERY_LIGHT = '#052E16'  # Fondo card oscuro

# Naranja - Advertencia, fase intermedia, energía
NARANJA = '#F39C12'
NARANJA_LIGHT = '#FDE047'
NARANJA_DARK = '#E67E22'
NARANJA_VERY_LIGHT = '#451A03'  # Fondo card oscuro

# Turquesa - Acento secundario, recuperación, fresco
TURQUESA = '#00CED1'
TURQUESA_LIGHT = '#5EEAD4'
TURQUESA_DARK = '#008B8B'
TURQUESA_VERY_LIGHT = '#134E4A'  # Fondo card oscuro

# ============================================================
# COLORES NEUTROS
# ============================================================

BLANCO = '#FFFFFF'
GRIS_OSCURO = '#E5E7EB'      # Texto principal en fondo negro
GRIS_MEDIO = '#9CA3AF'       # Texto secundario
GRIS_CLARO = '#6B7280'       # Texto muted
GRIS_MUY_CLARO = '#374151'   # Inputs fondo
GRIS_FONDO = '#000000'       # FONDO NEGRO
NEGRO = '#000000'

# ============================================================
# COLORES SEMÁNTICOS (para estados)
# ============================================================

EXITO = VERDE
ADVERTENCIA = NARANJA
ERROR = '#E74C3C'
INFO = CELESTE

# Colores para resultados de Ruffier (usando la paleta)
RESULTADO_COLORES = {
    0: ERROR,           # Insatisfactorio - Rojo
    1: NARANJA,         # Débil - Naranja
    2: CELESTE,         # Satisfactorio - Celeste
    3: TURQUESA,        # Bueno - Turquesa
    4: VERDE,           # Excelente - Verde
}

RESULTADO_ETIQUETAS = {
    0: 'INSATISFACTORIO',
    1: 'DÉBIL',
    2: 'SATISFACTORIO',
    3: 'BUENO',
    4: 'EXCELENTE',
}

# ============================================================
# ESTILOS DE TEXTO
# ============================================================

TEXT_STYLES = {
    'display': {
        'font_size': sp(32),
        'bold': True,
        'color': GRIS_OSCURO,
    },
    'headline': {
        'font_size': sp(24),
        'bold': True,
        'color': GRIS_OSCURO,
    },
    'title': {
        'font_size': sp(20),
        'bold': True,
        'color': GRIS_OSCURO,
    },
    'subtitle': {
        'font_size': sp(16),
        'bold': True,
        'color': GRIS_MEDIO,
    },
    'body': {
        'font_size': sp(15),
        'color': GRIS_MEDIO,
    },
    'body_small': {
        'font_size': sp(13),
        'color': GRIS_CLARO,
    },
    'button': {
        'font_size': sp(16),
        'bold': True,
        'color': BLANCO,
    },
    'button_outline': {
        'font_size': sp(15),
        'bold': True,
        'color': CELESTE,
    },
    'number_large': {
        'font_size': sp(48),
        'bold': True,
        'color': GRIS_OSCURO,
    },
    'number_timer': {
        'font_size': sp(36),
        'bold': True,
        'color': CELESTE,
    },
    'input_label': {
        'font_size': sp(14),
        'bold': True,
        'color': GRIS_OSCURO,
    },
    'input_hint': {
        'font_size': sp(16),
        'color': GRIS_CLARO,
    },
}

# ============================================================
# ESTILOS DE BOTONES
# ============================================================

BUTTON_STYLES = {
    'primary': {
        'background_color': CELESTE,
        'color': BLANCO,
        'background_normal': '',
        'background_down': '',
    },
    'success': {
        'background_color': VERDE,
        'color': BLANCO,
        'background_normal': '',
        'background_down': '',
    },
    'warning': {
        'background_color': NARANJA,
        'color': BLANCO,
        'background_normal': '',
        'background_down': '',
    },
    'accent': {
        'background_color': TURQUESA,
        'color': BLANCO,
        'background_normal': '',
        'background_down': '',
    },
    'disabled': {
        'background_color': GRIS_CLARO,
        'color': GRIS_MUY_CLARO,
        'background_normal': '',
        'background_down': '',
    },
    'outline_primary': {
        'background_color': (0, 0, 0, 0),
        'color': CELESTE,
        'background_normal': '',
        'background_down': '',
    },
    'outline_success': {
        'background_color': (0, 0, 0, 0),
        'color': VERDE,
        'background_normal': '',
        'background_down': '',
    },
}

# ============================================================
# ESTILOS DE INPUTS (Modo oscuro)
# ============================================================

INPUT_STYLES = {
    'default': {
        'background_color': '#1F2937',  # Gris oscuro para inputs
        'foreground_color': BLANCO,
        'cursor_color': CELESTE,
        'padding': (dp(12), dp(12)),
    },
    'disabled': {
        'background_color': GRIS_MUY_CLARO,
        'foreground_color': GRIS_CLARO,
        'cursor_color': CELESTE,
        'padding': (dp(12), dp(12)),
    },
    'focused': {
        'background_color': '#1F2937',
        'foreground_color': BLANCO,
        'cursor_color': CELESTE,
        'padding': (dp(12), dp(12)),
    },
}

# ============================================================
# ESPACIADO Y DIMENSIONES
# ============================================================

SPACING = {
    'xs': dp(4),
    'sm': dp(8),
    'md': dp(16),
    'lg': dp(24),
    'xl': dp(32),
    'xxl': dp(48),
}

BUTTON_HEIGHT = dp(56)
BUTTON_HEIGHT_SM = dp(48)
INPUT_HEIGHT = dp(56)
INPUT_HEIGHT_LG = dp(64)

CARD_RADIUS = dp(16)
BUTTON_RADIUS = dp(12)
INPUT_RADIUS = dp(8)

# ============================================================
# GRADIENTES Y EFECTOS (para canvas)
# ============================================================

def get_gradient_colors(start_hex, end_hex):
    """Retorna tupla de colores RGBA para gradiente"""
    return (get_color_from_hex(start_hex), get_color_from_hex(end_hex))

GRADIENTES = {
    'primary': (CELESTE, CELESTE_DARK),
    'success': (VERDE, VERDE_DARK),
    'warning': (NARANJA, NARANJA_DARK),
    'accent': (TURQUESA, TURQUESA_DARK),
    'card_primary': (CELESTE_VERY_LIGHT, '#1E3A5F'),
    'card_success': (VERDE_VERY_LIGHT, '#166534'),
    'card_warning': (NARANJA_VERY_LIGHT, '#92400E'),
    'card_accent': (TURQUESA_VERY_LIGHT, '#0F766E'),
}

# ============================================================
# FUNCIONES DE UTILIDAD
# ============================================================

def hex_to_rgba(hex_color: str, alpha: float = 1.0):
    """Convierte hex a tupla RGBA (0-1)"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return (r, g, b, alpha)

def get_result_color(level_idx: int):
    """Obtiene color para nivel de resultado"""
    return RESULTADO_COLORES.get(level_idx, GRIS_MEDIO)

def get_result_label(level_idx: int):
    """Obtiene etiqueta para nivel de resultado"""
    return RESULTADO_ETIQUETAS.get(level_idx, '—')

def apply_button_style(button: 'Button', style_name: str):
    """Aplica estilo predefinido a un botón"""
    if style_name in BUTTON_STYLES:
        style = BUTTON_STYLES[style_name]
        for key, value in style.items():
            setattr(button, key, value)

def apply_text_style(label: 'Label', style_name: str):
    """Aplica estilo predefinido a un label"""
    if style_name in TEXT_STYLES:
        style = TEXT_STYLES[style_name]
        for key, value in style.items():
            setattr(label, key, value)