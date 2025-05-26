import tkinter as tk
import math

# ---------------- CONSTANTES ---------------- #
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15

reps = 0
timer = None

# ---------------- FUNCIONES ---------------- #
def reset_timer():
    global reps
    window.after_cancel(timer)
    reps = 0
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Pomodoro", fg="green")
    check_marks.config(text="")


def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Descanso largo", fg="red")
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Descanso corto", fg="pink")
    else:
        count_down(work_sec)
        title_label.config(text="Trabajo", fg="green")


def count_down(count):
    global timer
    minutes = math.floor(count / 60)
    seconds = count % 60
    if seconds < 10:
        seconds = f"0{seconds}"
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)


# ---------------- UI CONFIG ---------------- #
window = tk.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg="white")

title_label = tk.Label(text="Pomodoro", fg="green", bg="white", font=("Courier", 35, "bold"))
title_label.grid(column=1, row=0)

canvas = tk.Canvas(width=200, height=224, bg="white", highlightthickness=0)
tomato_img = tk.PhotoImage(file="img/tomato.png") 
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="black", font=("Courier", 30, "bold"))
canvas.grid(column=1, row=1)

start_button = tk.Button(text="Inicio", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = tk.Button(text="Reiniciar", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = tk.Label(fg="green", bg="white", font=("Courier", 20))
check_marks.grid(column=1, row=3)

window.mainloop()
