import tkinter as tk
from tkinter import ttk, messagebox
from math import pi
import pygame
import threading
import sys
import os
import sqlite3
from datetime import datetime

if getattr(sys, 'frozen', False):
    # Empaquetado por PyInstaller
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

icon_path = os.path.join(base_path, "img", "tomato.png")
sound_path = os.path.join(base_path, "sound", "alarm.wav")
db_path = os.path.join(base_path, "pomodoro.db")

# Inicializar la base de datos
def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS configuraciones
                 (id INTEGER PRIMARY KEY, work_min INTEGER, short_break_min INTEGER, 
                  long_break_min INTEGER, tarea TEXT, created_at TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tareas_completadas
                 (id INTEGER PRIMARY KEY, tarea TEXT, duracion INTEGER, 
                  completada_at TIMESTAMP)''')
    conn.commit()
    conn.close()

# Cargar última configuración
def load_last_config():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT work_min, short_break_min, long_break_min, tarea FROM configuraciones ORDER BY created_at DESC LIMIT 1')
    result = c.fetchone()
    conn.close()
    if result:
        return result
    return (25, 5, 15, "Trabajo")  # Valores por defecto

# Guardar configuración
def save_config(work_min, short_break_min, long_break_min, tarea):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''INSERT INTO configuraciones (work_min, short_break_min, long_break_min, tarea, created_at)
                 VALUES (?, ?, ?, ?, ?)''', 
                 (work_min, short_break_min, long_break_min, tarea, datetime.now()))
    conn.commit()
    conn.close()

# Guardar tarea completada
def save_completed_task(tarea, duracion):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''INSERT INTO tareas_completadas (tarea, duracion, completada_at)
                 VALUES (?, ?, ?)''', 
                 (tarea, duracion, datetime.now()))
    conn.commit()
    conn.close()

# Inicializar la base de datos al inicio
init_db()

# Cargar la última configuración
WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN, TAREA = load_last_config()

# Variables de tiempo (ahora son globales para poder modificarlas)
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
TAREA = "Trabajo"
DESCANSO = "Descanso"
DESCANSO_LARGO = "Descanso Largo"

reps = 0
timer = None
dark_mode = False
total_seconds = 0
current_seconds = 0
timer_running = False
is_paused = False
paused_time = 0

# functions
def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
    pygame.time.wait(1000)  # Espera 1 segundo entre cada sonido

threading.Thread(target=play_sound).start()

def start_pause_timer():
    global reps, total_seconds, current_seconds, paused_time, is_paused, timer_running

    if timer_running and not is_paused:
        # PAUSA
        window.after_cancel(timer)
        is_paused = True
        paused_time = current_seconds
        start_btn.config(text="🔁")  # Reanudar
        return

    if is_paused:
        # REANUDA
        is_paused = False
        start_btn.config(text="⏸")  # Pausar
        countdown(paused_time)
        return

    # START
    timer_running = True
    start_btn.config(text="⏸")  # Cambia a Pausar
    reps += 1

    if reps % 8 == 0:
        total_seconds = LONG_BREAK_MIN * 60
        title_label.config(text=DESCANSO_LARGO, fg="#e17055")
        canvas.itemconfig(progress_arc, outline="#e17055")
    elif reps % 2 == 0:
        total_seconds = SHORT_BREAK_MIN * 60
        title_label.config(text=DESCANSO, fg="#74b9ff")
        canvas.itemconfig(progress_arc, outline="#74b9ff")
    else:
        total_seconds = WORK_MIN * 60
        title_label.config(text=TAREA, fg="#00b894")
        canvas.itemconfig(progress_arc, outline="#00b894")

    current_seconds = total_seconds
    countdown(current_seconds)

def reset_timer():
    global reps, timer, current_seconds, paused_time, timer_running, is_paused
    if timer:
        window.after_cancel(timer)
    reps = 0
    current_seconds = 0
    paused_time = 0
    timer_running = False
    is_paused = False
    start_btn.config(text="▶")  # Vuelve a Start
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Pomodoro", fg="green")
    checkmarks.config(text="")
    canvas.itemconfig(progress_arc, extent=0)

def countdown(count):
    global current_seconds, timer, timer_running
    current_seconds = count
    minutes = count // 60
    seconds = count % 60
    canvas.itemconfig(timer_text, text=f"{minutes:02}:{seconds:02}")

    extent = (1 - count / total_seconds) * 360
    canvas.itemconfig(progress_arc, extent=extent)

    if count > 0:
        timer = window.after(1000, countdown, count - 1)
    else:
        play_sound()
        play_sound()
        play_sound()
        marks = "✔" * (reps // 2)
        checkmarks.config(text=marks)
        timer_running = False
        is_paused = False
        start_btn.config(text="▶")
        
        # Guardar la tarea completada si era un período de trabajo
        if reps % 2 == 1:  # Si era un período de trabajo
            save_completed_task(TAREA, WORK_MIN)

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#2d3436" if dark_mode else "white"
    fg = "white" if dark_mode else "green"

    window.config(bg=bg)
    canvas.config(bg=bg)
    title_label.config(bg=bg, fg=fg)
    checkmarks.config(bg=bg, fg=fg)
    buttons_frame.config(bg=bg)

def open_settings():
    settings_window = tk.Toplevel(window)
    settings_window.title("Configuración")
    settings_window.geometry("300x220")
    settings_window.resizable(False, False)
    
    settings_window.transient(window)
    settings_window.grab_set()
    
    input_frame = tk.Frame(settings_window, padx=10, pady=10)
    input_frame.pack(fill="both", expand=True)
    
    work_var = tk.StringVar(value=str(WORK_MIN))
    short_break_var = tk.StringVar(value=str(SHORT_BREAK_MIN))
    long_break_var = tk.StringVar(value=str(LONG_BREAK_MIN))
    tarea_var = tk.StringVar(value=str(TAREA))
    
    tk.Label(input_frame, text="Tiempo de trabajo (min):").grid(row=0, column=0, sticky="w", pady=2)
    tk.Entry(input_frame, textvariable=work_var, width=10).grid(row=0, column=1, padx=5)
    
    tk.Label(input_frame, text="Descanso corto (min):").grid(row=1, column=0, sticky="w", pady=2)
    tk.Entry(input_frame, textvariable=short_break_var, width=10).grid(row=1, column=1, padx=5)
    
    tk.Label(input_frame, text="Descanso largo (min):").grid(row=2, column=0, sticky="w", pady=2)
    tk.Entry(input_frame, textvariable=long_break_var, width=10).grid(row=2, column=1, padx=5)

    tk.Label(input_frame, text="Tarea a realizar:").grid(row=3, column=0, sticky="w", pady=2)
    tk.Entry(input_frame, textvariable=tarea_var, width=20).grid(row=3, column=1, padx=5)
    
    def save_settings():
        global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN, TAREA
        try:
            work_min = int(work_var.get())
            short_break_min = int(short_break_var.get())
            long_break_min = int(long_break_var.get())
            tarea = str(tarea_var.get())
            
            # Guardar en la base de datos
            save_config(work_min, short_break_min, long_break_min, tarea)
            
            # Actualizar variables globales
            WORK_MIN = work_min
            SHORT_BREAK_MIN = short_break_min
            LONG_BREAK_MIN = long_break_min
            TAREA = tarea
            
            settings_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese números válidos")
    
    tk.Button(settings_window, text="Guardar", command=save_settings).pack(pady=10)

def show_history():
    history_window = tk.Toplevel(window)
    history_window.title("Historial de Tareas")
    history_window.geometry("400x300")
    history_window.resizable(False, False)
    
    history_window.transient(window)
    history_window.grab_set()
    
    # Frame principal
    main_frame = tk.Frame(history_window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Crear Treeview para mostrar las tareas
    columns = ('tarea', 'duracion', 'fecha')
    tree = ttk.Treeview(main_frame, columns=columns, show='headings')
    
    # Definir encabezados
    tree.heading('tarea', text='Tarea')
    tree.heading('duracion', text='Duración (min)')
    tree.heading('fecha', text='Fecha y Hora')
    
    # Configurar columnas
    tree.column('tarea', width=150)
    tree.column('duracion', width=100)
    tree.column('fecha', width=150)
    
    # Agregar scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Posicionar elementos
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Cargar datos de la base de datos
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''SELECT tarea, duracion, completada_at 
                 FROM tareas_completadas 
                 ORDER BY completada_at DESC''')
    
    for row in c.fetchall():
        # Formatear la fecha para mejor visualización
        fecha = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
        fecha_formateada = fecha.strftime('%d/%m/%Y %H:%M')
        tree.insert('', 'end', values=(row[0], row[1], fecha_formateada))
    
    conn.close()
    
    # Botón para cerrar
    tk.Button(history_window, text="Cerrar", command=history_window.destroy).pack(pady=10)

# ---------------- UI ----------------
window = tk.Tk()
window.title("pomodoro")
window.geometry("200x180")
window.resizable(False, False)
window.config(padx=0, pady=0, bg="white")

# Título
title_label = tk.Label(window, text="pomodoro-app", fg="green", bg="white", font=("Courier", 10, "bold"))
title_label.pack(pady=(5, 2))

# Canvas
canvas = tk.Canvas(window, width=100, height=100, bg="white", highlightthickness=0)
tomato_img = tk.PhotoImage(file=icon_path)
canvas.create_image(50, 42, image=tomato_img)
canvas.pack()

# Barra de progreso circular
progress_arc = canvas.create_arc(5, 5, 95, 95, start=90, extent=0, style="arc", outline="green", width=3)

# Fondo blanco redondo
canvas.create_oval(15, 15, 85, 80, fill="white", outline="")

# Texto del cronómetro
timer_text = canvas.create_text(50, 50, text="00:00", fill="black", font=("Courier", 14, "bold"))

# Checkmarks ✔
checkmarks = tk.Label(window, fg="green", bg="white", font=("Arial", 10))
checkmarks.pack(pady=(0, 2))

# Botones en frame
buttons_frame = tk.Frame(window, bg="white", highlightthickness=0)
buttons_frame.pack()

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 8), padding=(1, 1), relief="flat")

start_btn = ttk.Button(buttons_frame, text="▶", command=start_pause_timer, width=3)
start_btn.grid(row=0, column=0, padx=1)

reset_btn = ttk.Button(buttons_frame, text="🔄", command=reset_timer, width=3)
reset_btn.grid(row=0, column=1, padx=1)

theme_btn = ttk.Button(buttons_frame, text="🌙", command=toggle_theme, width=3)
theme_btn.grid(row=0, column=2, padx=1)

settings_btn = ttk.Button(buttons_frame, text="⚙️", command=open_settings, width=3)
settings_btn.grid(row=0, column=3, padx=1)

history_btn = ttk.Button(buttons_frame, text="📋", command=show_history, width=3)
history_btn.grid(row=0, column=4, padx=1)

window.mainloop()
