"""
Sistema de sonidos para la app Test de Ruffier
Genera archivos WAV programáticamente SIN numpy
"""

from kivy.core.audio import SoundLoader
from kivy.logger import Logger
import math
import wave
import io
import struct


class SoundManager:
    """Gestor centralizado de sonidos"""
    
    _instance = None
    _sounds = {}
    _enabled = True
    _volume = 0.7
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_sounds()
        return cls._instance
    
    def _generate_wav(self, frequency: int, duration: float, volume: float = 0.5) -> bytes:
        """Genera un archivo WAV en memoria SIN numpy"""
        sample_rate = 44100
        num_samples = int(sample_rate * duration)
        
        # Generar onda senoidal
        wave_data = []
        for i in range(num_samples):
            t = i / sample_rate
            # Envelope para evitar clicks
            envelope = 1.0
            if i < sample_rate * 0.01:  # Fade in 10ms
                envelope = i / (sample_rate * 0.01)
            elif i > num_samples - sample_rate * 0.01:  # Fade out 10ms
                envelope = (num_samples - i) / (sample_rate * 0.01)
            
            sample = math.sin(2 * math.pi * frequency * t) * volume * envelope
            # Convertir a 16-bit signed integer
            wave_data.append(int(max(-32768, min(32767, sample * 32767))))
        
        # Crear archivo WAV en memoria
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)      # Mono
            wav_file.setsampwidth(2)      # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(struct.pack('<' + 'h' * len(wave_data), *wave_data))
        
        buffer.seek(0)
        return buffer.read()
    
    def _load_sounds(self):
        """Carga todos los sonidos generándolos programáticamente"""
        import tempfile
        import os
        
        sounds_to_create = {
            'click': (800, 0.05, 0.3),
            'start': (523, 0.2, 0.5),      # Do5
            'complete': (784, 0.3, 0.6),   # Sol5
            'phase_change': (659, 0.15, 0.4), # Mi5
            'count': (440, 0.08, 0.3),     # La4
            'error': (220, 0.2, 0.5),      # La3
            'success': (1047, 0.4, 0.6),   # Do6
            'timer_warning': (880, 0.1, 0.5), # La5
        }
        
        for name, (freq, dur, vol) in sounds_to_create.items():
            try:
                wav_data = self._generate_wav(freq, dur, vol)
                # Escribir a archivo temporal
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                    tmp.write(wav_data)
                    tmp_path = tmp.name
                
                sound = SoundLoader.load(tmp_path)
                # Limpiar archivo temporal
                os.unlink(tmp_path)
                
                if sound:
                    sound.volume = self._volume
                    self._sounds[name] = sound
                    Logger.info(f'SoundManager: Generado "{name}" ({freq}Hz, {dur}s)')
                else:
                    Logger.warning(f'SoundManager: No se pudo crear sonido "{name}"')
            except Exception as e:
                Logger.warning(f'SoundManager: Error generando "{name}": {e}')
    
    def play(self, name: str, volume: float = None):
        """Reproduce un sonido por nombre"""
        if not self._enabled:
            return
        
        sound = self._sounds.get(name)
        if sound:
            if volume is not None:
                original_volume = sound.volume
                sound.volume = volume
                sound.play()
                sound.volume = original_volume
            else:
                sound.play()
        else:
            Logger.debug(f'SoundManager: Sonido "{name}" no disponible')
    
    def stop(self, name: str):
        """Detiene un sonido"""
        sound = self._sounds.get(name)
        if sound:
            sound.stop()
    
    def set_enabled(self, enabled: bool):
        """Activa/desactiva todos los sonidos"""
        self._enabled = enabled
    
    def set_volume(self, volume: float):
        """Establece volumen global (0.0 a 1.0)"""
        self._volume = max(0.0, min(1.0, volume))
        for sound in self._sounds.values():
            sound.volume = self._volume
    
    def is_enabled(self):
        return self._enabled


# Instancia global
sound_manager = SoundManager()


# Funciones de conveniencia
def play_click():
    sound_manager.play('click')

def play_start():
    sound_manager.play('start')

def play_complete():
    sound_manager.play('complete')

def play_phase_change():
    sound_manager.play('phase_change')

def play_count():
    sound_manager.play('count', volume=0.5)

def play_error():
    sound_manager.play('error')

def play_success():
    sound_manager.play('success')

def play_timer_warning():
    sound_manager.play('timer_warning')


def create_default_sounds():
    """Función de compatibilidad - los sonidos ya se crean en _load_sounds"""
    return sound_manager._sounds