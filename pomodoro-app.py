import tkinter as tk
from tkinter import ttk
from math import pi
import pygame
import threading

# Variables de tiempo (ahora son globales para poder modificarlas)
WORK_MIN = 1
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
    pygame.mixer.music.load("sound/alarm.wav")
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
    
    # Hacer que la ventana de configuración sea modal
    settings_window.transient(window)
    settings_window.grab_set()
    
    # Frame para los inputs
    input_frame = tk.Frame(settings_window, padx=10, pady=10)
    input_frame.pack(fill="both", expand=True)
    
    # Variables para los inputs
    work_var = tk.StringVar(value=str(WORK_MIN))
    short_break_var = tk.StringVar(value=str(SHORT_BREAK_MIN))
    long_break_var = tk.StringVar(value=str(LONG_BREAK_MIN))
    tarea_var = tk.StringVar(value=str(TAREA))
    
    # Labels y inputs

    tk.Label(input_frame, text="Tiempo de trabajo (min):").grid(row=0, column=0, sticky="w", pady=2)
    tk.Entry(input_frame, textvariable=work_var, width=10).grid(row=0, column=1, padx=5)
    
    tk.Label(input_frame, text="Descanso corto (min):").grid(row=1, column=0, sticky="w", pady=2)
    tk.Entry(input_frame, textvariable=short_break_var, width=10).grid(row=1, column=1, padx=5)
    
    tk.Label(input_frame, text="Descanso largo (min):").grid(row=2, column=0, sticky="w", pady=2)
    tk.Entry(input_frame, textvariable=long_break_var, width=10).grid(row=2, column=1, padx=5)

    tk.Label(input_frame, text="Tarea a realizar:").grid(row=3, column=0, sticky="w", pady=2)
    tk.Entry(input_frame, textvariable=tarea_var, width=10).grid(row=3, column=1, padx=5)
    
    def save_settings():
        global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN, TAREA
        try:
            WORK_MIN = int(work_var.get())
            SHORT_BREAK_MIN = int(short_break_var.get())
            LONG_BREAK_MIN = int(long_break_var.get())
            TAREA = str(tarea_var.get())
            settings_window.destroy()
        except ValueError:
            tk.messagebox.showerror("Error", "Por favor ingrese números válidos")
    
    # Botón de guardar
    tk.Button(settings_window, text="Guardar", command=save_settings).pack(pady=10)

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
tomato_img = tk.PhotoImage(file="img/tomato.png")  # Usa una imagen tipo tomate si tienes
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
buttons_frame = tk.Frame(window, bg="white")
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

window.mainloop()
