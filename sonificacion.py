import numpy as np
import sounddevice as sd

# Frecuencias de las notas musicales (escala de Do mayor)
note_frequencies = {
    "C": 261.63,  # Do
    "D": 293.66,  # Re
    "E": 329.63,  # Mi
    "F": 349.23,  # Fa
    "G": 392.00,  # Sol
    "A": 440.00,  # La
    "B": 493.88   # Si
}

# Función para mapear valores del vector a notas
def map_to_notes(vector):
    """
    Mapea valores de un vector a notas musicales.
    
    Parámetros:
    vector (list): Lista de valores numéricos
    
    Retorna:
    list: Lista de notas musicales correspondientes
    """
    # Verificar que el vector no esté vacío
    if not vector or len(vector) == 0:
        return []
    
    # Asegurarse de que el vector sea una lista plana de números
    try:
        # Convertir a array numpy para asegurar que es un array plano
        flat_vector = np.array(vector).flatten()
        
        # Obtener min y max para normalizar
        min_val = np.min(flat_vector)
        max_val = np.max(flat_vector)
        
        # Si todos los valores son iguales, evitar división por cero
        if min_val == max_val:
            # Asignar la nota del medio
            notes = list(note_frequencies.keys())
            middle_note = notes[len(notes)//2]
            return [middle_note] * len(flat_vector)
        
        notes = list(note_frequencies.keys())
        normalized = np.interp(flat_vector, (min_val, max_val), (0, len(notes)-1))
        return [notes[int(round(n))] for n in normalized]
    
    except Exception as e:
        print(f"❌ Error al mapear valores a notas: {e}")
        return []

# Generar una onda sonora para una frecuencia y un instrumento
def generate_tone(frequency, duration=0.5, sample_rate=44100, instrument="piano"):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    if instrument == "piano":
        # Piano: Onda sinusoidal con atenuación
        wave = 0.5 * np.sin(2 * np.pi * frequency * t) * np.exp(-3 * t)
    elif instrument == "trumpet":
        # Trompeta: Onda cuadrada enriquecida con armónicos
        wave = 0.5 * (np.sin(2 * np.pi * frequency * t) +
                      0.3 * np.sin(2 * np.pi * frequency * 2 * t) +
                      0.1 * np.sin(2 * np.pi * frequency * 3 * t))
    elif instrument == "both":
        # Combinar piano y trompeta
        piano_wave = 0.5 * np.sin(2 * np.pi * frequency * t) * np.exp(-3 * t)
        trumpet_wave = 0.5 * (np.sin(2 * np.pi * frequency * t) +
                              0.3 * np.sin(2 * np.pi * frequency * 2 * t) +
                              0.1 * np.sin(2 * np.pi * frequency * 3 * t))
        wave = piano_wave + trumpet_wave
    else:
        raise ValueError("Instrument must be 'piano', 'trumpet', or 'both'.")
    
    # Normalizar la onda para evitar distorsión
    wave = np.clip(wave, -1, 1)
    return wave

# Reproducir las notas generadas
def play_notes(notes, instrument="piano", duration=0.5):
    sample_rate = 44100  # Frecuencia de muestreo
    for note in notes:
        freq = note_frequencies[note]
        wave = generate_tone(freq, duration, sample_rate, instrument)
        sd.play(wave, samplerate=sample_rate)
        sd.wait()  # Esperar a que termine de reproducir antes de pasar a la siguiente nota
