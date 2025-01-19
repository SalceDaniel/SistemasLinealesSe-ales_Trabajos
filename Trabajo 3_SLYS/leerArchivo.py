import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from tkinter import filedialog, Tk

def seleccionar_archivo_wav():
    print("Seleccionar el archivo WAV...")
    return filedialog.askopenfilename(title="Selecciona un archivo .wav", filetypes=[("Archivos WAV", "*.wav")])

def graficar_audio_tiempo(file_path):
    # Leer el archivo de audio usando soundfile
    data, sample_rate = sf.read(file_path)
    
    # Si el archivo es estéreo, convertir a mono
    if data.ndim == 2:
        data = data.mean(axis=1)
    
    times = np.arange(len(data)) / float(sample_rate)
    
    plt.figure(figsize=(10, 6))
    plt.plot(times, data, label="Señal de audio")
    plt.title(f"Forma de onda de '{file_path.split('/')[-1]}'")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    archivo = seleccionar_archivo_wav()
    if archivo:
        print(f"Archivo seleccionado: {archivo.split('/')[-1]}")
        graficar_audio_tiempo(archivo)
    else:
        print("No se seleccionó ningún archivo.")
