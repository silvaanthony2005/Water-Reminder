import tkinter as tk
from tkinter import messagebox
import threading
import time
from PIL import Image, ImageTk
import pystray
from plyer import notification
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class WaterReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recordatorio de Agua")
        self.root.geometry("500x600")  # Aumentar la altura de la ventana
        self.root.configure(bg="#E0F7FA")  # Color de fondo relacionado con el agua

        # Establecer el ícono de la ventana principal
        icon_path = resource_path("water.ico")
        self.root.iconbitmap(icon_path)  # Usar el archivo .ico como ícono de la ventana

        # Inicializar el tiempo restante antes de dibujar el reloj
        self.remaining_time = 0

        # Marco principal para organizar los elementos
        self.main_frame = tk.Frame(root, bg="#E0F7FA")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Etiqueta principal
        self.label = tk.Label(self.main_frame, text="¡Es hora de beber agua!", bg="#E0F7FA", fg="#00796B", font=("Arial", 18, "bold"))
        self.label.pack(pady=10)

        # Cargar y mostrar la imagen
        image_path = resource_path("water.ico")
        self.image = Image.open(image_path)
        self.image = self.image.resize((100, 100), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self.main_frame, image=self.photo, bg="#E0F7FA")
        self.image_label.pack(pady=10)

        # Canvas para el reloj circular
        self.canvas = tk.Canvas(self.main_frame, width=200, height=200, bg="#E0F7FA", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Dibujar el reloj con tiempo 00:00 al iniciar
        self.draw_clock(0)

        # Marco para el campo de entrada y los botones
        self.control_frame = tk.Frame(self.main_frame, bg="#E0F7FA")
        self.control_frame.pack(pady=10)

        # Campo de entrada para el tiempo
        self.time_entry = tk.Entry(self.control_frame, font=("Arial", 12), bd=2, relief="flat", bg="#FFFFFF", fg="#00796B", insertbackground="#00796B")
        self.time_entry.insert(0, "60")  # Valor predeterminado de 60 minutos
        self.time_entry.pack(pady=10, padx=10, ipady=5, fill="x")

        # Marco para los botones
        self.button_frame = tk.Frame(self.control_frame, bg="#E0F7FA")
        self.button_frame.pack(pady=10)

        # Botón para iniciar recordatorios
        self.start_button = tk.Button(self.button_frame, text="Iniciar Recordatorios", command=self.start_reminders, bg="#00796B", fg="white", bd=0, relief="flat", font=("Arial", 12), padx=20, pady=10, borderwidth=0, highlightthickness=0, activebackground="#004D40", activeforeground="white")
        self.start_button.pack(side="left", padx=5)

        # Botón para detener recordatorios
        self.stop_button = tk.Button(self.button_frame, text="Detener Recordatorios", command=self.stop_reminders, bg="#00796B", fg="white", bd=0, relief="flat", font=("Arial", 12), padx=20, pady=10, borderwidth=0, highlightthickness=0, activebackground="#004D40", activeforeground="white")
        self.stop_button.pack(side="left", padx=5)

        # Configurar el comportamiento al cerrar la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

        # Inicializar la bandeja del sistema
        self.tray_icon = None
        self.init_tray_icon()

        self.reminder_active = False

    def start_reminders(self):
        if not self.reminder_active:
            try:
                self.reminder_interval = int(self.time_entry.get()) * 60  # Convertir minutos a segundos
                self.remaining_time = self.reminder_interval
                self.reminder_active = True
                threading.Thread(target=self.reminder_loop, daemon=True).start()
                self.update_timer()
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa un número válido.")

    def stop_reminders(self):
        self.reminder_active = False
        self.remaining_time = 0
        self.draw_clock(0)

    def reminder_loop(self):
        while self.reminder_active:
            time.sleep(1)
            if self.reminder_active:
                self.remaining_time -= 1
                if self.remaining_time <= 0:
                    self.show_notification()
                    self.remaining_time = self.reminder_interval

    def show_notification(self):
        notification.notify(
            title="Recordatorio de Agua",
            message="¡Es hora de beber agua!",
            app_name="Water Reminder",
            timeout=10
        )

    def update_timer(self):
        if self.reminder_active:
            minutes, seconds = divmod(self.remaining_time, 60)
            self.draw_clock(self.remaining_time / self.reminder_interval)
            self.root.after(1000, self.update_timer)

    def draw_clock(self, progress):
        self.canvas.delete("all")
        center_x, center_y = 100, 100
        radius = 80
        start_angle = 90
        extent = -360 * progress

        # Dibujar el círculo de fondo
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="#00796B", width=5)

        # Dibujar la barra de progreso
        self.canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius, start=start_angle, extent=extent, outline="#00BCD4", width=5, style=tk.ARC)

        # Mostrar el tiempo restante en el centro
        minutes, seconds = divmod(self.remaining_time, 60)
        self.canvas.create_text(center_x, center_y, text=f"{minutes:02}:{seconds:02}", font=("Arial", 16, "bold"), fill="#00796B")

    def minimize_to_tray(self):
        try:
            self.root.withdraw()  # Ocultar la ventana principal
            if self.tray_icon is not None:
                self.tray_icon.stop()  # Detener el ícono de la bandeja si ya está en ejecución
            self.init_tray_icon()  # Reinicializar el ícono de la bandeja
            self.tray_icon.run()  # Ejecutar el ícono en la bandeja del sistema
        except Exception as e:
            print(f"Error al minimizar a la bandeja: {e}")
            self.root.deiconify()  # Mostrar la ventana principal si hay un error

    def init_tray_icon(self):
        menu = (
            pystray.MenuItem("Abrir", self.restore_from_tray),
            pystray.MenuItem("Salir", self.exit_app)
        )
        image = Image.open("water.ico")  # Usar la misma imagen para el ícono de la bandeja
        self.tray_icon = pystray.Icon("Water Reminder", image, "Water Reminder", menu)

    def restore_from_tray(self):
        if self.tray_icon is not None:
            self.tray_icon.stop()  # Detener el ícono de la bandeja
        self.root.deiconify()  # Mostrar la ventana principal

    def exit_app(self):
        if self.tray_icon is not None:
            self.tray_icon.stop()  # Detener el ícono de la bandeja
        self.root.destroy()  # Cerrar la aplicación

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterReminderApp(root)
    root.mainloop()
