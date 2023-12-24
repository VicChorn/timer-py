import tkinter as tk
from tkinter import ttk
import pygame
import time

# Sound playback settings
pygame.mixer.init()
pygame.mixer.music.load("C:\\Users\\chorn\\Downloads\\goggins.mp3")
pygame.mixer.music.set_volume(0.8)

# User needs to provide the path to the local .mp3 media file manually
length_in_s = int((pygame.mixer.Sound("C:\\Users\\chorn\\Downloads\\goggins.mp3")).get_length())
length_in_ms = length_in_s * 1000
print(f"Song length in seconds {length_in_s}")

# Global variables
current_state = False
current_timer = None
start_x, start_y = 0, 0

def timer(seconds):
    global current_state, current_timer

    if current_state and seconds > 0:
        seconds -= 1
        converted_time = time_display_converter(seconds)
        counter_label.config(text=f"{converted_time}")
        progress_var.set(seconds)
        current_timer = root.after(1000, timer, seconds)
    elif seconds == 0:
        pygame.mixer.music.play(start=0.0)
        print("Time is up")
        progress_var.set(0)
        entry.grid(row=2, column=3, sticky="nesw")
    else:
        print("Timer stopped")
        progress_var.set(0)
        entry.grid(row=2, column=3, sticky="nesw")

def time_display_converter(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def click_start():
    global current_state, current_timer

    # Check if a timer is already running, stop it
    if current_timer is not None:
        root.after_cancel(current_timer)
        current_state = False
        pygame.mixer.music.stop()

    current_state = True
    seconds = int(entry.get()) * 60
    progress_var.set(seconds)
    progress_bar.config(maximum=seconds)
    entry.grid_forget()
    timer(seconds)

def click_stop():
    global current_state, current_timer
    current_state = False
    root.after(0, recreate_entry)

def recreate_entry():
    entry.grid(row=2, column=3, sticky="nesw")

def always_on_top():
    root.attributes("-topmost", 1)
    root.update_idletasks()

def on_drag_start(event):
    global start_x, start_y
    start_x = event.x_root - root.winfo_rootx()
    start_y = event.y_root - root.winfo_rooty()

def on_drag_motion(event):
    root.geometry(f"+{event.x_root - start_x}+{event.y_root - start_y}")

root = tk.Tk()
root.title("Timer")

entry = tk.Entry(root, bg="#008000", width=3)
entry.grid(row=2, column=3, sticky="nesw")

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=60)
progress_bar.grid(row=1, column=0, columnspan=4, sticky="nesw")

current_state = False

# Buttons and other widgets
start_button = tk.Button(root, text="Start", command=click_start)
stop_button = tk.Button(root, text="Stop", command=click_stop)
aot_button = tk.Button(root, text="->", command=always_on_top)
counter_label = tk.Label(root, text="Set timer to start")

# Placing all of them on the grid, final layout of the app
root.rowconfigure([0, 1, 2], minsize=10, weight=1)
root.columnconfigure([0, 1, 2, 3], minsize=10, weight=1)

entry.grid(row=2, column=3, sticky="nesw")
progress_bar.grid(row=1, column=0, columnspan=4, sticky="nesw")
stop_button.grid(row=2, column=1, sticky="nesw")
start_button.grid(row=2, column=0, sticky="nesw")
aot_button.grid(row=2, column=2, sticky="nesw")
counter_label.grid(row=0, column=0, columnspan=4, sticky="nesw")

root.attributes('-alpha', 0.5)
root.bind("<ButtonPress-1>", on_drag_start)
root.bind("<B1-Motion>", on_drag_motion)

root.mainloop()
