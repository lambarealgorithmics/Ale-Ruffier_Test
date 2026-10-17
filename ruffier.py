''' Módulo para calcular los resultados de las pruebas de Ruffier.

La suma de los tres intentos de medición del pulso (antes del esfuerzo, justo después del esfuerzo y después de un breve descanso)
idealmente no debería superar los 200 latidos por minuto.
Se propone que los niños midan su pulso durante 15 segundos,
y encuentren el resultado en latidos por minuto multiplicando por 4:
   S = 4 * (P1 + P2 + P3)
Cuanto más se aleje el resultado del ideal de 200 latidos, peor será.
Tradicionalmente, se presentan tablas con los valores divididos por 10.

Índice de Ruffier  
   IR = (S - 200) / 10
se evalúa según la edad de acuerdo con la tabla:
        7-8             9-10                11-12               13-14               15+ (solo para adolescentes!)

perfecto     < 6.5           < 5                 < 3.5               < 2                 < 0.5  
bueno    >= 6.5 y < 12   >= 5 y < 10.5       >= 3.5 y < 9        >= 2 y < 7.5        >= 0.5 y < 6
satisfactorio  >= 12 y < 17    >= 10.5 y < 15.5    >= 9 y < 14         >= 7.5 y < 12.5     >= 6 y < 11
débil  >= 17 y < 21    >= 15.5 y < 19.5    >= 14 y < 18        >= 12.5 y < 16.5    >= 11 y < 15
insatisfactorio   >= 21           >= 19.5             >= 18               >= 16.5             >= 15

El resultado "insatisfactorio" está 4 puntos por encima del resultado "débil" para todas las edades,
"débil" se separa de "satisfactorio" por 5, y "bueno" se separa de "satisfactorio" por 5.5.

Por lo tanto, escribiremos una función ruffier_result(r_index, level) que producirá
el índice de Ruffier calculado y el nivel "insatisfactorio" para la edad evaluada, y producirá un resultado.

'''

# Textos de resultado (índice 0 = peor, 4 = mejor)
txt_index = "Índice de Ruffier: "
txt_workheart = "Eficiencia cardíaca: "
txt_nodata = "No hay datos para esa edad"

txt_res = [
    '''bajo.
¡Consulta a tu médico lo antes posible!''',           # 0: insatisfactorio
    '''satisfactorio.
Se recomienda consultar a tu médico.''',               # 1: débil
    '''promedio.
Podría valer la pena realizar pruebas adicionales con el médico.''',  # 2: satisfactorio
    '''superior al promedio.''',                        # 3: bueno
    '''alto.'''                                         # 4: perfecto
]

# Colores para cada nivel (para UI) - Usando la paleta del tema
RESULT_COLORS = {
    0: '#E74C3C',  # Rojo - insatisfactorio
    1: '#F39C12',  # Naranja - débil
    2: '#00B4D8',  # Celeste - satisfactorio
    3: '#00CED1',  # Turquesa - bueno
    4: '#2ECC71',  # Verde - perfecto
}

RESULT_LABELS = {
    0: 'INSATISFACTORIO',
    1: 'DÉBIL',
    2: 'SATISFACTORIO',
    3: 'BUENO',
    4: 'EXCELENTE',
}


def ruffier_index(P1: int, P2: int, P3: int) -> float:
    """Calcula el índice de Ruffier a partir de las 3 mediciones (en latidos/15seg)"""
    return (4 * (P1 + P2 + P3) - 200) / 10


def neud_level(age: int) -> float:
    """
    Calcula el nivel umbral 'insatisfactorio' para la edad dada.
    Para edad < 7 retorna valor muy alto (siempre insatisfactorio).
    """
    if age < 7:
        return 100  # Fuera de rango
    norm_age = (min(age, 15) - 7) // 2
    return 21 - norm_age * 1.5


def ruffier_result(r_index: float, level: float) -> int:
    """
    Evalúa el índice contra los umbrales por edad.
    Retorna 0-4 (0=peor, 4=mejor).
    """
    if r_index >= level:
        return 0  # insatisfactorio
    level -= 4
    if r_index >= level:
        return 1  # débil
    level -= 5
    if r_index >= level:
        return 2  # satisfactorio
    level -= 5.5
    if r_index >= level:
        return 3  # bueno
    return 4  # excelente


def test(P1: int, P2: int, P3: int, age: int) -> str:
    """
    Función principal que retorna el resultado formateado.
    
    Args:
        P1: Pulso en reposo (latidos en 15 seg)
        P2: Pulso justo después del esfuerzo (latidos en 15 seg)
        P3: Pulso después de descanso (latidos en 15 seg)
        age: Edad del usuario
        
    Returns:
        String formateado con índice y evaluación
    """
    if age < 7:
        return f"{txt_index}0\n{txt_nodata}"
    
    ruff_index = ruffier_index(P1, P2, P3)
    result_idx = ruffier_result(ruff_index, neud_level(age))
    result_text = txt_res[result_idx]
    
    return f"{txt_index}{ruff_index:.1f}\n{txt_workheart}{result_text}"


def get_result_details(P1: int, P2: int, P3: int, age: int) -> dict:
    """Retorna diccionario con detalles completos para UI avanzada"""
    if age < 7:
        return {
            'index': 0,
            'level': 'N/A',
            'label': 'SIN DATOS',
            'description': txt_nodata,
            'color': '#6B7280',
            'valid': False
        }
    
    ruff_index = ruffier_index(P1, P2, P3)
    result_idx = ruffier_result(ruff_index, neud_level(age))
    
    return {
        'index': round(ruff_index, 1),
        'level_idx': result_idx,
        'label': RESULT_LABELS[result_idx],
        'description': txt_res[result_idx],
        'color': RESULT_COLORS[result_idx],
        'valid': True
    }