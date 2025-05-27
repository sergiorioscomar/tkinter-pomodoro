import tkinter as tk
from tkinter import ttk
from math import pi

# Constantes de tiempo
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15

reps = 0
timer = None
dark_mode = False
total_seconds = 0
current_seconds = 0
is_paused = False
paused_time = 0


def start_timer():
    global reps, total_seconds, current_seconds, paused_time, is_paused

    if is_paused:
        is_paused = False
        countdown(paused_time)
        reset_btn.config(text="Pausar")
        return

    reps += 1

    if reps % 8 == 0:
        total_seconds = LONG_BREAK_MIN * 60
        title_label.config(text="Descanso Largo", fg="#e17055")
        canvas.itemconfig(progress_arc, outline="#e17055")
    elif reps % 2 == 0:
        total_seconds = SHORT_BREAK_MIN * 60
        title_label.config(text="Descanso", fg="#74b9ff")
        canvas.itemconfig(progress_arc, outline="#74b9ff")
    else:
        total_seconds = WORK_MIN * 60
        title_label.config(text="Trabajo", fg="#00b894")
        canvas.itemconfig(progress_arc, outline="#00b894")

    current_seconds = total_seconds
    countdown(current_seconds)

def reset_timer():
    global reps, timer, current_seconds, paused_time
    if timer:
        window.after_cancel(timer)
    reps = 0
    current_seconds = 0
    paused_time = 0
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Pomodoro")
    checkmarks.config(text="")
    canvas.itemconfig(progress_arc, extent=0)


def pause_or_reset():
    global timer, is_paused, paused_time

    if not is_paused:
        window.after_cancel(timer)
        is_paused = True
        paused_time = current_seconds
        reset_btn.config(text="Reiniciar")
    else:
        reset_timer()
        is_paused = False
        paused_time = 0
        reset_btn.config(text="Pausar")

def countdown(count):
    global current_seconds, timer
    current_seconds = count
    minutes = count // 60
    seconds = count % 60
    canvas.itemconfig(timer_text, text=f"{minutes:02}:{seconds:02}")

    extent = (1 - count / total_seconds) * 360
    canvas.itemconfig(progress_arc, extent=extent)

    if count > 0:
        timer = window.after(1000, countdown, count - 1)
    else:
        marks = "✔" * (reps // 2)
        checkmarks.config(text=marks)
        start_timer()

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

# --------------------- UI ---------------------
window = tk.Tk()
window.title("Pomodoro")
window.geometry("400x500")
window.iconphoto(False, tk.PhotoImage(file="img/icono.png"))
window.resizable(False, False)
window.config(padx=20, pady=20, bg="white")

# Título
title_label = tk.Label(text="Pomodoro-app", fg="green", bg="white",
                       font=("Courier", 32, "bold"))
title_label.pack(pady=(10, 0))

# Canvas principal
canvas = tk.Canvas(width=300, height=300, bg="white", highlightthickness=0)
canvas.pack()

# Barra de progreso exterior
progress_arc = canvas.create_arc(10, 10, 290, 290, start=90,
                                 extent=0, style="arc", outline="green", width=6)

# Imagen redonda con círculo blanco debajo
canvas.create_oval(70, 70, 230, 230, fill="white", outline="")  # círculo base blanco
tomato_img = tk.PhotoImage(file="img/tomato.png")
canvas.create_image(150, 150, image=tomato_img)

# Tiempo encima de la imagen
timer_text = canvas.create_text(150, 150, text="00:00",
                                fill="black", font=("Courier", 28, "bold"))

# Frame de botones
buttons_frame = tk.Frame(bg="white")
buttons_frame.pack(pady=10)

# Estilo de botones mejorado
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton",
                font=("Segoe UI", 11),
                padding=5,
                relief="flat",
                background="#dfe6e9",
                foreground="black")

start_btn = ttk.Button(buttons_frame, text="Inicio", command=start_timer)
start_btn.grid(row=0, column=0, padx=10)

reset_btn = ttk.Button(buttons_frame, text="Pausar", command=pause_or_reset)
reset_btn.grid(row=0, column=1, padx=10)

theme_btn = ttk.Button(buttons_frame, text="🌓", command=toggle_theme)
theme_btn.grid(row=0, column=2, padx=10)

# Checkmarks
checkmarks = tk.Label(fg="green", bg="white", font=("Arial", 18))
checkmarks.pack()

window.mainloop()
