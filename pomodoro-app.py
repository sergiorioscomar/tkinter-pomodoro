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
        reset_btn.config(text="⏸")
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
    title_label.config(text="Pomodoro-app", fg="green")
    checkmarks.config(text="")
    canvas.itemconfig(progress_arc, extent=0)

def pause_or_reset():
    global timer, is_paused, paused_time

    if not is_paused:
        window.after_cancel(timer)
        is_paused = True
        paused_time = current_seconds
        reset_btn.config(text="🔄")
    else:
        reset_timer()
        is_paused = False
        paused_time = 0
        reset_btn.config(text="⏸")

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
canvas.pack()

# Barra de progreso circular
progress_arc = canvas.create_arc(5, 5, 95, 95, start=90, extent=0, style="arc", outline="green", width=3)

# Fondo blanco redondo
canvas.create_oval(15, 15, 85, 85, fill="white", outline="")

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

start_btn = ttk.Button(buttons_frame, text="▶", command=start_timer, width=3)
start_btn.grid(row=0, column=0, padx=1)

reset_btn = ttk.Button(buttons_frame, text="⏸", command=pause_or_reset, width=3)
reset_btn.grid(row=0, column=1, padx=1)

theme_btn = ttk.Button(buttons_frame, text="🌙", command=toggle_theme, width=3)
theme_btn.grid(row=0, column=2, padx=1)

window.mainloop()
