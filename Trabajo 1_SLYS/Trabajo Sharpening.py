from PIL import Image # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt

# Cargar la imagen en formato BMP

image = Image.open("imagen.bmp").convert("L")  # Convertir a escala de grises
image_array = np.array(image)  # Convertir la imagen a un array de NumPy para manipular sus píxeles

# Definir el kernel de sharpening
sharpening_kernel = np.array([[0, -1, 0],
                              [-1, 5, -1],
                              [0, -1, 0]])

# Crear una imagen de salida vacía (con el mismo tamaño que la imagen original)
output_image = np.zeros_like(image_array)

# Obtener las dimensiones de la imagen y del kernel
image_height, image_width = image_array.shape  # Incluimos el canal de color
kernel_size = sharpening_kernel.shape[0]  # Suponemos un kernel cuadrado
offset = kernel_size // 2  # Para evitar los bordes (donde no cabe el kernel)

# Aplicar la convolución solo a la imagen ByN (un solo canal)
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

# Guardar la imagen procesada en formato BMP
output_image.save("imagen_sharpened_color_manual.bmp")

# Mostrar la imagen original
axes[0].imshow(image)
axes[0].set_title("Imagen Original")
axes[0].axis("off")

# Mostrar la imagen con sharpening
axes[1].imshow(output_image)
axes[1].set_title("Imagen con Sharpening")
axes[1].axis("off")

plt.show()

input()
