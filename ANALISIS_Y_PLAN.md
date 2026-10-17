# Análisis del Proyecto Ruffier Test - Kivy

## 📋 Resumen del Proyecto
Aplicación móvil para test de Ruffier (evaluación de eficiencia cardíaca) con 5 pantallas:
1. **InstrScr** - Ingreso de nombre y edad
2. **PulseScr** - Medición de pulso en reposo (15 seg)
3. **CheckSits** - Sentadillas (30 en 45 seg)
4. **PulseScr2** - Medición de pulso post-esfuerzo (15 seg + 30 seg descanso + 15 seg)
5. **Result** - Resultado del índice de Ruffier

---

## 🐛 Errores Encontrados

### main_app.py - ERRORES CRÍTICOS

| Línea | Error | Tipo | Descripción |
|-------|-------|------|-------------|
| 13-16 | Variables globales | Arquitectura | Uso de `global name, age, p1, p2, p3` - mala práctica, causa bugs en navegación |
| 33, 75, 107, 143, 173 | `btn.on_press =` | Sintaxis Kivy | **Incorrecto**. En Kivy se usa `btn.bind(on_press=callback)` |
| 70, 85, 136, 137, 161, 167 | `set_disabled()` | Sintaxis Kivy | **No existe**. Se usa `widget.disabled = True/False` |
| 86, 91, 168, 175 | `btn.set_disabled()` | Sintaxis Kivy | **No existe**. Botones usan `disabled` property |
| 106 | `txt_test1` | Lógica | Instrucción incorrecta para pantalla de sentadillas (debe ser `txt_test2` o `txt_sits`) |
| 185 | `self.in_result2 = str(p3)` | Bug | Debe ser `self.in_result2.text = str(p3)` |
| 196 | `self.on_enter = self.before` | Sintaxis Kivy | **Incorrecto**. Se usa `self.bind(on_enter=self.before)` o sobrescribir `on_enter` |
| 207 | **Falta CheckSits** | **CRÍTICO** | La pantalla de sentadillas **nunca se agrega al ScreenManager** |
| 52, 95, 178, 179 | `check_int()` retorna `False` | Lógica | Mezcla tipos `int` y `bool` - usar `None` o excepciones |

### seconds.py - ERRORES

| Línea | Error | Tipo | Descripción |
|-------|-------|------|-------------|
| 15-20 | `restart()` llama `start()` sin cancelar previo | Bug | `Clock.schedule_interval` se acumula → múltiples timers corriendo |
| 8-13 | `done` no es `BooleanProperty` | Kivy | No notifica cambios automáticamente al UI |

### sits.py - ERRORES CRÍTICOS

| Línea | Error | Tipo | Descripción |
|-------|-------|------|-------------|
| 3 | `class Sits(L'abel):` | **Sintaxis** | **Error de sintaxis Python** - comilla mal colocada |
| 5-9 | Clase vacía | Funcionalidad | No implementada - solo placeholder |

### runner.py - ERRORES

| Línea | Error | Tipo | Descripción |
|-------|-------|------|-------------|
| 3 | Hereda de `BoxLayout` no importado | Import | Falta `from kivy.uix.boxlayout import BoxLayout` |
| 5-12 | Clase vacía | Funcionalidad | No implementada - solo placeholder |

### ruffier.py - OBSERVACIONES

- ✅ Lógica matemática correcta
- ⚠️ `txt_res` índices invertidos: 0="bajo" (peor) → 4="alto" (mejor), pero `ruffier_result` retorna 0 para peor caso. **Coherente pero confuso**.
- ⚠️ Sin type hints ni docstrings formales

---

## 🎯 Plan de Corrección

### Fase 1: Correcciones Críticas (Bloqueantes)
1. ✅ Arreglar sintaxis en `sits.py` (`L'abel` → `Label`)
2. ✅ Implementar `CheckSits` en `ScreenManager` (main_app.py línea 207)
3. ✅ Corregir todos los `bind(on_press=)` y `disabled` properties
4. ✅ Arreglar `Clock` en `seconds.py` (cancelar intervalo previo)
5. ✅ Corregir `on_enter` binding en `Result` screen

### Fase 2: Implementar Funcionalidad Faltante
6. ✅ Implementar `Sits` class completa (contador de sentadillas con animación)
7. ✅ Implementar `Runner` class (animación de sentadilla)
8. ✅ Integrar `Sits` y `Runner` en `CheckSits` screen

### Fase 3: Mejoras de Arquitectura
8. ✅ Eliminar variables globales → usar `App.get_running_app()` o propiedades del `ScreenManager`
9. ✅ Añadir type hints
10. ✅ Validación robusta de inputs

### Fase 4: Modernización UI/UX (Frontend Plan)
11. ✅ Crear archivo `.kv` para separación UI/Logic
12. ✅ Diseño Material Design 3 / Moderno
13. ✅ Colores, tipografía, espaciado consistentes
14. ✅ Feedback visual (loading, transiciones, animaciones)
15. ✅ Responsive para móvil
16. ✅ Accesibilidad básica

---

## 🎨 Frontend Plan - Diseño Moderno Móvil

### Paleta de Colores (Material Design 3)
```python
# Colores principales
PRIMARY = "#2563EB"      # Blue 600 - Confianza médica
PRIMARY_CONTAINER = "#DBEAFE"  # Blue 100
SECONDARY = "#059669"    # Emerald 600 - Salud/Éxito
SURFACE = "#FFFFFF"      # White
SURFACE_VARIANT = "#F3F4F6"  # Gray 100
BACKGROUND = "#FAFAFA"   # Gray 50
ON_PRIMARY = "#FFFFFF"
ON_SURFACE = "#1F2937"   # Gray 800
ON_SURFACE_VARIANT = "#4B5563"  # Gray 600
ERROR = "#DC2626"        # Red 600
OUTLINE = "#D1D5DB"      # Gray 300

# Estados
SUCCESS = "#16A34A"      # Green 600
WARNING = "#F59E0B"      # Amber 500
```

### Tipografía
- **Display/Large**: Roboto 32sp / Bold - Títulos principales
- **Headline/Medium**: Roboto 24sp / SemiBold - Títulos de pantalla
- **Title/Large**: Roboto 20sp / Medium - Subtítulos
- **Body/Large**: Roboto 16sp / Regular - Texto principal
- **Body/Medium**: Roboto 14sp / Regular - Texto secundario
- **Label/Large**: Roboto 14sp / Medium - Botones
- **Numbers/Timer**: Roboto Mono 48sp / Bold - Cronómetros

### Espaciado (8px base)
- `xs`: 4px, `sm`: 8px, `md`: 16px, `lg`: 24px, `xl`: 32px, `2xl`: 48px

### Componentes UI

#### 1. Pantalla Inicio (InstrScr)
```
┌─────────────────────────┐
│  🫀  Test de Ruffier    │  ← Header con icono
├─────────────────────────┤
│                         │
│  [Ilustración SVG]      │  ← Ilustración médica decorativa
│                         │
├─────────────────────────┤
│  Nombre          [____] │  ← Input con label flotante
│  Edad            [____] │  ← Input numérico
├─────────────────────────┤
│      [  COMENZAR  ]     │  ← Botón primario full-width
│                         │
│  ℹ️  Para mayores de 7 │  ← Texto informativo
└─────────────────────────┘
```

#### 2. Pantalla Pulso 1 (PulseScr)
```
┌─────────────────────────┐
│  ←  Pulso en Reposo     │  ← Header con back
├─────────────────────────┤
│                         │
│      ⏱  00:15          │  ← Timer grande circular
│    ●──────────────●    │  ← Progreso circular animado
│                         │
│  "Mide tu pulso durante│
│   15 segundos"         │
├─────────────────────────┤
│  Resultado:  [____]    │  ← Input (disabled hasta fin)
├─────────────────────────┤
│    [  INICIAR  ]       │  ← Botón primario
└─────────────────────────┘
```

#### 3. Pantalla Sentadillas (CheckSits)
```
┌─────────────────────────┐
│  ←  Ejercicio           │
├─────────────────────────┤
│                         │
│     🏃  Sentadilla 15/30│  ← Contador + avatar animado
│                         │
│    ⏱  00:45            │  ← Timer regresivo
│    ●──────────────●    │
│                         │
│  "Mantén el ritmo"     │
├─────────────────────────┤
│    [  PAUSAR  ]        │  ← Botón secundario
└─────────────────────────┘
```

#### 4. Pantalla Pulso 2 (PulseScr2) - 3 Fases
```
Fase 1: Pulso post-esfuerzo (15s)
Fase 2: Descanso (30s) - pantalla relajada, color suave
Fase 3: Pulso recuperación (15s)

┌─────────────────────────┐
│  ←  Recuperación        │
├─────────────────────────┤
│                         │
│     📍 FASE 1/3         │  ← Indicador de paso
│      ⏱  00:15          │
│    ●──────────────●    │
│                         │
│  "Cuenta tu pulso"     │
├─────────────────────────┤
│  Pulso 1:     [____]   │  ← Se habilita al terminar fase
│  Pulso 2:     [____]   │  ← Se habilita al terminar fase 3
├─────────────────────────┤
│    [  CONTINUAR  ]     │  ← Solo al final
└─────────────────────────┘
```

#### 5. Pantalla Resultado (Result)
```
┌─────────────────────────┐
│  ←  Resultado           │
├─────────────────────────┤
│                         │
│     🎉  Juan Pérez      │
│                         │
│     Índice:  8.5        │  ← Número grande, color según resultado
│                         │
│  ┌─────────────────┐   │
│  │  BUENO          │   │  ← Card con color semántico
│  │  Eficiencia     │   │
│  │  cardíaca       │   │
│  └─────────────────┘   │
│                         │
│  [Recomendaciones]     │  ← Expandible
│                         │
│    [  REINICIAR  ]     │  ← Botón outline
└─────────────────────────┘
```

### Animaciones y Transiciones
- **Screen transitions**: `SlideTransition` (direction='left' para avance, 'right' para retroceso)
- **Timer circular**: `AnimatedWidget` con `canvas` drawing
- **Botones**: `ripple` effect, `scale` on press (0.95x)
- **Inputs**: Label flotante (float label pattern)
- **Resultado**: Fade-in + slide-up para cards

### Responsive
- `size_hint` y `pos_hint` para layouts fluidos
- `dp()` para unidades densidas-independent
- `Window.size` detection para tablet vs phone
- Landscape support opcional

### Accesibilidad
- Contraste WCAG AA (4.5:1 mínimo)
- Tamaños touch target mínimos 48dp
- Semántica de navegación clara
- Soporte para TalkBack/VoiceOver básico

---

## 📁 Estructura Final Propuesta

```
Test de ruffier/
├── main.py                 # Entry point (renombrado de main_app.py)
├── ruffier.py             # Lógica de cálculo (mejorado)
├── instructions.py        # Textos (mejorado)
├── screens/
│   ├── __init__.py
│   ├── base.py            # BaseScreen con navegación shared
│   ├── instr.py           # InstrScr
│   ├── pulse1.py          # PulseScr
│   ├── sits.py            # CheckSits (con Sits + Runner)
│   ├── pulse2.py          # PulseScr2
│   └── result.py          # Result
├── widgets/
│   ├── __init__.py
│   ├── timer.py           # Seconds (mejorado)
│   ├── sit_counter.py     # Sits + Runner (implementado)
│   ├── animated_button.py # Botón con ripple/scale
│   ├── circular_timer.py  # Timer visual circular
│   └── input_field.py     # Input con label flotante
├── utils/
│   ├── __init__.py
│   ├── validation.py      # check_int mejorado
│   └── navigation.py      # Helper navegación
├── theme/
│   ├── __init__.py
│   ├── colors.py          # Paleta
│   ├── typography.py      # Estilos texto
│   └── spacing.py         # Espaciado
├── ruffier.kv             # UI declarativo principal
└── assets/
    ├── icons/
    └── illustrations/
```

---

## ✅ Checklist de Implementación

- [ ] Corregir todos los bugs sintácticos y lógicos
- [ ] Implementar `Sits` y `Runner` completos
- [ ] Eliminar variables globales
- [ ] Crear `theme/` system
- [ ] Crear `widgets/` reutilizables
- [ ] Refactorizar pantallas a archivos separados
- [ ] Crear `ruffier.kv` con diseño moderno
- [ ] Implementar transiciones suaves
- [ ] Añadir validación robusta
- [ ] Testing en móvil (buildozer)
- [ ] Documentar en README.md