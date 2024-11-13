try:
    from PIL import Image
    import numpy as np
    import matplotlib.pyplot as plt
    import tkinter as tk
    from tkinter import filedialog
    import os
except ImportError:
    import subprocess
    import sys
    print("Instalando las librerías necesarias...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "numpy", "matplotlib"])
    from PIL import Image
    import numpy as np
    import matplotlib.pyplot as plt
    import tkinter as tk
    from tkinter import filedialog
    import os

def sharpening(image):
    image_array = np.array(image)  # Convertir la imagen a un array de NumPy para manipular sus píxeles

    # Definir el kernel de sharpening
    sharpening_kernel = np.array([[0, -1, 0],
                                  [-1, 5, -1],
                                  [0, -1, 0]])

    # Crear una imagen de salida vacía (con el mismo tamaño que la imagen original)
    output_image = np.zeros_like(image_array)

    # Obtener las dimensiones de la imagen y del kernel
    image_height, image_width = image_array.shape
    kernel_size = sharpening_kernel.shape[0]  # Suponemos un kernel cuadrado
    offset = kernel_size // 2  # Para evitar los bordes (donde no cabe el kernel)

    # Aplicar la convolución a la imagen ByN (un solo canal)
    for i in range(offset, image_height - offset):
        for j in range(offset, image_width - offset):
            # Extraer la región 3x3 alrededor del píxel (i, j)
            region = image_array[i - offset:i + offset + 1, j - offset:j + offset + 1]

            # Realizar el producto elemento a elemento y sumar los resultados
            result = np.sum(region * sharpening_kernel)

            # Asegurarse de que el valor resultante esté en el rango [0, 255]
            output_image[i, j] = min(max(result, 0), 255)

    # Convertir la matriz de salida en una imagen
    output_image = Image.fromarray(output_image)
    return output_image

def ingresar_imagen():
    # Obtener el directorio en el que se encuentra el archivo Python
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Abrir un cuadro de diálogo para seleccionar un archivo
    file_path = filedialog.askopenfilename(
        initialdir=current_directory,
        title="Seleccione una imagen BMP",
        filetypes=[("Archivos BMP", "*.bmp")]
    )

    # Comprobar si el usuario seleccionó un archivo
    if file_path:
        print(f"Archivo seleccionado: {file_path}")
        
        # Cargar la imagen en formato BMP
        image = Image.open(file_path).convert("L")  # Convertir a escala de grises si es necesario
        # Obtener el nombre base sin extensión
        original_name = os.path.splitext(os.path.basename(file_path))[0]
        return image, original_name
        
    else:
        print("No se seleccionó ningún archivo.")
        return None, None

def mostrar_imagenes(image, output_image):
    # Mostrar la imagen original y la imagen con sharpening lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Crear una figura con 1 fila y 2 columnas

    # Mostrar la imagen original
    axes[0].imshow(image, cmap="gray")
    axes[0].set_title("Imagen Original")
    axes[0].axis("off")

    # Mostrar la imagen con sharpening
    axes[1].imshow(output_image, cmap="gray")
    axes[1].set_title("Imagen con Sharpening")
    axes[1].axis("off")

    plt.show()


image, image_name = ingresar_imagen()

if image:
    print("\nRealizando sharpening...")
    output_image = sharpening(image)
    # Guardar la imagen procesada en formato BMP
    output_path = "Resultados/" + str(image_name) + "_sharpened.bmp"
    output_image.save(output_path)
    print("\nLa imagen modificada se guardó en el directorio Resultados")

    mostrar_imagenes(image, output_image)
