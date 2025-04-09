import tkinter as tk
import os
import sys
from PIL import Image, ImageTk
import time
import platform

# Función para obtener la ruta correcta de la imagen
def get_ruta_imagen():
    if getattr(sys, 'frozen', False):  # Si está en un exe
        base_path = sys._MEIPASS  # Carpeta temporal de PyInstaller
    else:
        base_path = os.path.abspath(".")  # Directorio normal del script
    return os.path.join(base_path, "PE.jpg")

imagen_nombre = get_ruta_imagen()  # Ruta correcta de la imagen

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")  # Centrar la ventana

def cuenta_atras():
    veces = 10
    root = tk.Tk()
    root.title("Pereira")

    # Configurar la ventana
    root.protocol("WM_DELETE_WINDOW", lambda: None)  # Bloquea el botón de cerrar
    root.resizable(False, False)  # No permite cambiar tamaño
    root.attributes('-topmost', True)  # Siempre en primer plano

    # Definir tamaño de la ventana de la cuenta atrás
    ancho_ventana, alto_ventana = 300, 200  # Ajusta el tamaño si lo necesitas
    centrar_ventana(root, ancho_ventana, alto_ventana)

    label = tk.Label(root, text="", font=("Arial", 48))
    label.pack(expand=True, padx=20, pady=20)

    def actualizar_contador(i):
        if i >= 0:
            label.config(text=f"{i}s")
            root.after(1000, actualizar_contador, i - 1)
        else:
            root.destroy()  # Cierra la ventana del contador
            mostrar_imagen()  # Abre la imagen a pantalla completa

    actualizar_contador(veces)
    root.mainloop()

def mostrar_imagen():
    ventana = tk.Tk()
    ventana.attributes('-fullscreen', True)  # Hace que la ventana sea de pantalla completa
    ventana.configure(bg="black")  # Fondo negro para evitar bordes visibles

    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()

    try:
        imagen = Image.open(imagen_nombre)  
        imagen = imagen.resize((pantalla_ancho, pantalla_alto), Image.Resampling.LANCZOS)  # Redimensionar la imagen
        imagen_tk = ImageTk.PhotoImage(imagen)
        
        label_imagen = tk.Label(ventana, image=imagen_tk)
        label_imagen.image = imagen_tk  
        label_imagen.place(x=0, y=0, relwidth=1, relheight=1)  # Ajustar la imagen a toda la pantalla

        ventana.bind("<Escape>", lambda e: ventana.destroy())  # Permitir salir con ESC

        ventana.after(2000, mostrar_texto)  # Esperar 2 segundos antes de mostrar el texto
        ventana.mainloop()

    except FileNotFoundError:
        print(f"Error: No se encontró la imagen en la ruta: {imagen_nombre}")
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

def mostrar_texto():
    ventana_texto = tk.Tk()
    ventana_texto.title("Mensaje")
    ventana_texto.configure(bg="black")

    # Mostrar el texto en pantalla completa
    label_texto = tk.Label(ventana_texto, text="QUE QUIERES QUE HAGA PEREIRA", font=("Arial", 36), fg="white", bg="black")
    label_texto.pack(expand=True, padx=20, pady=20)

    ventana_texto.attributes('-fullscreen', True)  # Pantalla completa

    # Reiniciar después de 5 segundos
    ventana_texto.after(5000, reiniciar_computadora)

    ventana_texto.mainloop()

def reiniciar_computadora():
    sistema = platform.system()
    if sistema == "Windows":
        os.system("shutdown /r /t 1")
    elif sistema == "Linux" or sistema == "Darwin":  # Linux o macOS
        os.system("sudo reboot")
    else:
        print("Sistema no soportado para reiniciar.")

cuenta_atras()

