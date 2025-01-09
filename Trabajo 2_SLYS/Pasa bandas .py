import subprocess
import sys
import os
import threading

# Verificar si las librerías están instaladas
try:
    import numpy as np
    import scipy.signal as signal
    import soundfile as sf
    from scipy.io import wavfile
    import sounddevice as sd
    import matplotlib.pyplot as plt
    from tkinter import Tk, Button, filedialog, Scale, HORIZONTAL, Label, messagebox, StringVar,Canvas, Frame, Scrollbar,VERTICAL
    from concurrent.futures import ThreadPoolExecutor
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'numpy', 'scipy', 'soundfile', 'matplotlib', 'sounddevice', 'tkinter'])
    import numpy as np
    import scipy.signal as signal
    import soundfile as sf
    from scipy.io import wavfile
    import sounddevice as sd
    import matplotlib.pyplot as plt
    from tkinter import Tk, Button, filedialog, Scale, HORIZONTAL, Label, messagebox, StringVar, Canvas, Frame, Scrollbar,VERTICAL
    from concurrent.futures import ThreadPoolExecutor


def seleccionar_archivo_wav():
    Tk().withdraw()
    return filedialog.askopenfilename(title="Selecciona un archivo .wav", filetypes=[("Archivos WAV", "*.wav")])

def filtro_pasa_bandas_convolucion(audio_signal, fs, f_min, f_max):
    nyquist = 0.5 * fs
    fir_filter = signal.firwin(101, [f_min / nyquist, f_max / nyquist], pass_zero=False)
    if audio_signal.ndim > 1:
        return np.apply_along_axis(lambda m: np.convolve(m, fir_filter, mode='same'), axis=0, arr=audio_signal)
    return np.convolve(audio_signal, fir_filter, mode='same')













def plot_waveform_and_spectrum(file_path,f_min,f_max, sample_interval=1):
    # Lee el archivo de audio original
    sample_rate, data = wavfile.read(file_path)
    
    # Si el archivo es estéreo, convierte a mono
    if len(data.shape) == 2:
        data = data.mean(axis=1)
    
    # Subsamplear los datos
    data = data[::sample_interval]
    times = np.arange(len(data)) / float(sample_rate / sample_interval)

    # Generar la ruta del archivo filtrado
    filtered_file_path = file_path.replace('.wav', '_filtrado.wav')

    # Leer el archivo de audio filtrado
    sample_rate_f, data_filtered = wavfile.read(filtered_file_path)
    
    # Si el archivo filtrado es estéreo, convierte a mono
    if len(data_filtered.shape) == 2:
        data_filtered = data_filtered.mean(axis=1)
    
    # Subsamplear los datos del archivo filtrado
    data_filtered = data_filtered[::sample_interval]
    times_filtered = np.arange(len(data_filtered)) / float(sample_rate_f / sample_interval)

    # Graficar las 6 gráficas en una cuadrícula 3x2
    plt.figure(figsize=(10, 8))

    # Gráfica 1: Forma de onda del archivo original
    plt.subplot(3, 2, 1)
    plt.plot(times, data, label='_nolegend_')  
    plt.title('Señal en Tiempo de "' + file_path.split('/')[-1] + '"')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')

    # Gráfica 2: Espectro de frecuencia del archivo original
    frequencies = np.fft.rfftfreq(len(data), d=1/sample_rate)
    magnitude = np.abs(np.fft.rfft(data))
    plt.subplot(3, 2, 2)
    plt.plot(frequencies, magnitude, label='_nolegend_')  
    plt.title('Señal en Frecuencia de "' + file_path.split('/')[-1] + '"')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')

    # Gráfica 3: Forma de onda del archivo filtrado
    plt.subplot(3, 2, 3)
    plt.plot(times_filtered, data_filtered, label='_nolegend_') 
    plt.title('Señal en Tiempo de "' + filtered_file_path.split('/')[-1] + '"')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')

    # Gráfica 4: Espectro de frecuencia del archivo filtrado
    frequencies_filtered = np.fft.rfftfreq(len(data_filtered), d=1/sample_rate_f)
    magnitude_filtered = np.abs(np.fft.rfft(data_filtered))
    plt.subplot(3, 2, 4)
    plt.plot(frequencies_filtered, magnitude_filtered, label='_nolegend_')  
    plt.title('Señal en Frecuencia de "' + filtered_file_path.split('/')[-1] + '"')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')

    # Gráfica 5: Respuesta Impulsional h(t)
    nyquist = 0.5 * sample_rate
    fir_filter = signal.firwin(101, [f_min / nyquist, f_max / nyquist], pass_zero=False)
    plt.subplot(3, 2, 5)
    plt.title('Respuesta al impulso h(t)')
    plt.plot(fir_filter)
    plt.xlabel('Muestra')
    plt.ylabel('Amplitud')

    # Gráfica 6: Respuesta en Frecuencia H(f)
    fft_filter = np.fft.fft(fir_filter, 2048)  # FFT de la respuesta impulsional, con padding para mayor resolución
    frequencies_hf = np.fft.fftfreq(len(fft_filter), 1/sample_rate)
    plt.subplot(3, 2, 6)
    plt.title('Respuesta en al impulso en frecuencia H(f)')
    plt.plot(frequencies_hf[:len(frequencies_hf)//2], np.abs(fft_filter)[:len(frequencies_hf)//2])
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True)

    # Ajuste más preciso del espacio entre las subgráficas
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.7, wspace=0.3)


    plt.show()











def aplicar_filtro():
    global archivo, estado
    if not archivo:
        messagebox.showerror("Error", "No se ha seleccionado un archivo de audio.")
        return
    f_min = slider_min.get()
    f_max = slider_max.get()
    if f_min >= f_max:
        messagebox.showerror("Error", "La frecuencia mínima debe ser menor que la máxima.")
        return
    estado.set("Cargando...")
    ventana.update_idletasks()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(filtrar_y_guardar_audio, archivo, f_min, f_max)
        result = future.result()
    estado.set("")
    if result:
        archivo_salida = result
        plot_waveform_and_spectrum(archivo,f_min,f_max)  # Graficar el archivo original
        
        messagebox.showinfo("Guardado", f"Archivo filtrado guardado como {archivo_salida}")

def filtrar_y_guardar_audio(archivo, f_min, f_max):
    try:
        audio_signal, fs = sf.read(archivo)
        audio_signal_filtrada = filtro_pasa_bandas_convolucion(audio_signal, fs, f_min, f_max)
        archivo_salida = os.path.join(os.path.dirname(archivo), os.path.basename(archivo).replace(".wav", "_filtrado.wav"))
        sf.write(archivo_salida, audio_signal_filtrada, fs)
        return archivo_salida
    except Exception as e:
        messagebox.showerror("Error", f"Error al aplicar el filtro: {e}")
        return None

def cargar_y_filtrar(archivo_seleccionado=None):
    
    global archivo
    archivo = archivo_seleccionado or seleccionar_archivo_wav()
    if archivo:
        boton_cargar.config(text= 'seleccionado: ' + archivo.split('/')[-1])
        boton_filtrar.config(state="normal")
        boton_reproducir_original.config(state="normal")
        boton_reproducir_filtrada.config(state="normal")

def reproducir_audio(archivo, es_filtrado=False):
    if es_filtrado:
        archivo = archivo.replace(".wav", "_filtrado.wav")  # Cambiar a archivo filtrado
    audio_signal, fs = sf.read(archivo)
    sd.play(audio_signal, fs)
    sd.wait()

def reproducir_audio_original():
    # Crear un hilo para reproducir el audio sin bloquear la UI
    threading.Thread(target=reproducir_audio, args=(archivo, False), daemon=True).start()

def reproducir_audio_filtrado():
    # Crear un hilo para reproducir el audio sin bloquear la UI
    threading.Thread(target=reproducir_audio, args=(archivo, True), daemon=True).start()
def detener_audio():
    sd.stop()


ventana = Tk()
ventana.title("Filtro Pasa Bandas y Reproductor de Audio")
ventana.geometry("600x500")  # Ajustar el tamaño de la ventana

archivo = None
estado = StringVar()

# Botón para seleccionar archivo de audio
boton_cargar = Button(ventana, text="Seleccionar archivo .wav", command=cargar_y_filtrar, font=("Arial", 12), bg="#4CAF50", fg="white")
boton_cargar.pack(pady=10)

# Sliders para la frecuencia mínima y máxima
slider_min = Scale(ventana, from_=1, to=20000, orient=HORIZONTAL, label="Frecuencia mínima (Hz)", font=("Arial", 10), length=400)  # Hacer más anchos los sliders
slider_min.set(500)
slider_min.pack(pady=5)

slider_max = Scale(ventana, from_=1, to=20000, orient=HORIZONTAL, label="Frecuencia máxima (Hz)", font=("Arial", 10), length=400)  # Hacer más anchos los sliders
slider_max.set(5000)
slider_max.pack(pady=5)

# Botón para aplicar el filtro
boton_filtrar = Button(ventana, text="Filtrar", state="disabled", command=aplicar_filtro, font=("Arial", 12), bg="#FF5722", fg="white")
boton_filtrar.pack(pady=10)

# Botones para reproducir los audios original y filtrado
boton_reproducir_original = Button(ventana, text="Reproducir Canción Original", state="disabled", command=reproducir_audio_original, font=("Arial", 12), bg="#2196F3", fg="white")
boton_reproducir_original.pack(pady=5)

boton_reproducir_filtrada = Button(ventana, text="Reproducir Canción Filtrada", state="disabled", command=reproducir_audio_filtrado, font=("Arial", 12), bg="#2196F3", fg="white")
boton_reproducir_filtrada.pack(pady=5)

boton_detener = Button(ventana, text="Detener",  command=detener_audio, font=("Arial", 12), bg="#2196F3", fg="red")
boton_detener.pack(pady=5)

# Estado de la aplicación
label_estado = Label(ventana, textvariable=estado, font=("Arial", 12), fg="black")
label_estado.pack(pady=10)

def cerrar_ventana():
    sd.stop()  # Detener todas las reproducciones de audio
    ventana.destroy()
ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)



ventana.mainloop()
