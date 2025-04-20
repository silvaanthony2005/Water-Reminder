# Water Reminder App

¡Bienvenido a la aplicación **Water Reminder**! Esta aplicación te ayuda a recordar beber agua regularmente, mostrando notificaciones en tu sistema y un reloj visual que cuenta el tiempo restante hasta el próximo recordatorio.

## Características

- **Notificaciones del sistema**: Recibe notificaciones en tu escritorio cuando es hora de beber agua.
- **Reloj visual**: Un reloj circular muestra el tiempo restante hasta el próximo recordatorio.
- **Minimizar a la bandeja del sistema**: La aplicación se puede minimizar a la bandeja del sistema para que no ocupe espacio en la barra de tareas.
- **Configurable**: Puedes establecer el intervalo de tiempo entre recordatorios.

## Requisitos

- Python 3.7 o superior
- Bibliotecas necesarias: `tkinter`, `Pillow`, `pystray`, `plyer`

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/water-reminder.git
   cd water-reminder
   ```

2. **Crear un entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**:
   - En Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Para ejecutar la aplicación, simplemente ejecuta el archivo `app.py`:

```bash
python app.py
```

## Empaquetado con PyInstaller

Para hacer que la aplicación sea portable, puedes empaquetarla usando `PyInstaller`. Sigue estos pasos:

1. **Instalar PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Generar el archivo `.spec`**:
   ```bash
   pyi-makespec --onefile --windowed --icon=water.ico app.py
   ```

3. **Modificar el archivo `.spec`** (si es necesario):
   Asegúrate de que el archivo `.spec` incluya todas las dependencias necesarias. Aquí tienes un ejemplo de archivo `.spec`:

   ```python
    # -*- mode: python ; coding: utf-8 -*-


    a = Analysis(
        ['app.py'],
        pathex=[],
        binaries=[],
        datas=[('water.ico', '.')],
        hiddenimports=[
            'tkinter',
            'tkinter.messagebox',
            'threading',
            'time',
            'PIL',
            'PIL.Image',
            'PIL.ImageTk',
            'pystray',
            'plyer',
            'plyer.platforms.win.notification',
            'os',
            'sys'
        ],
        hookspath=[],
        hooksconfig={},
        runtime_hooks=[],
        excludes=[],
        noarchive=False,
        optimize=0,
    )
    pyz = PYZ(a.pure)

    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name='app',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=['water.ico'],
    )
   ```

4. **Empaquetar la aplicación**:
   ```bash
   pyinstaller app.spec
   ```

5. **Mover la carpeta completa**:
   Después de empaquetar, `PyInstaller` generará una carpeta llamada `dist` que contiene el ejecutable y todos los archivos dependientes. Mueve esta **carpeta completa** a cualquier ubicación, y la aplicación seguirá funcionando.

## Uso

1. **Establecer el intervalo de tiempo**:
   - Ingresa el intervalo de tiempo en minutos en el campo de entrada y haz clic en "Iniciar Recordatorios".

2. **Minimizar a la bandeja del sistema**:
   - Puedes minimizar la aplicación a la bandeja del sistema haciendo clic en la "X" de la ventana principal.

3. **Restaurar desde la bandeja del sistema**:
   - Haz clic derecho en el ícono de la aplicación en la bandeja del sistema y selecciona "Abrir" para restaurar la ventana principal.

4. **Salir de la aplicación**:
   - Haz clic derecho en el ícono de la aplicación en la bandeja del sistema y selecciona "Salir" para cerrar la aplicación.

## Contribución

Si deseas contribuir a este proyecto, ¡eres bienvenido! Por favor, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

---

¡Gracias por usar **Water Reminder**! Esperamos que esta aplicación te ayude a mantenerte hidratado y saludable. 😊
