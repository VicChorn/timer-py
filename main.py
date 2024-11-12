import tkinter as tk
from tkinter import ttk
import pygame
import time
import os
from tkinter import filedialog
import json
import sys
from tkinter import messagebox
import keyboard

# Getting the application path
def resource_path():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return application_path

# Updating paths to be relative to the application directory
config_file_path = os.path.join(resource_path(), "config.txt")
settings_file_path = os.path.join(resource_path(), "settings.json")

# Initialize pygame mixer with error handling
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Failed to initialize pygame mixer: {e}")
    messagebox.showerror("Error", f"Failed to initialize audio system: {e}")

def load_settings():
    try:
        if os.path.exists(settings_file_path):
            with open(settings_file_path, "r") as file:
                return json.load(file)
    except Exception as e:
        print(f"Error loading settings: {e}")
    return {"transparency": 0.2, "volume": 0.8}

def save_settings(settings):
    try:
        settings_dir = os.path.dirname(settings_file_path)
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)
        with open(settings_file_path, "w") as file:
            json.dump(settings, file)
    except Exception as e:
        print(f"Error saving settings: {e}")
        messagebox.showerror("Error", f"Failed to save settings: {e}")

#Function to load audio file path from config file
def load_audio_file():
    try:
        if os.path.exists(config_file_path):
            with open(config_file_path, "r") as file:
                return file.readline().strip()
    except Exception as e:
        print(f"Error loading audio file: {e}")
    return None

def save_audio_file(audio_file_path):
    try:
        config_dir = os.path.dirname(config_file_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(config_file_path, "w") as file:
            file.write(audio_file_path)
    except Exception as e:
        print(f"Error saving audio file path: {e}")
        messagebox.showerror("Error", f"Failed to save audio file path: {e}")

#Load and initialize audio
audio_file_path = load_audio_file()
try:
    if audio_file_path and os.path.exists(audio_file_path):
        pygame.mixer.music.load(audio_file_path)
    else:
        audio_file_path = filedialog.askopenfilename(
            title="Select an Audio File",
            filetypes=[("MP3 Files", "*.mp3")]
        )
        if audio_file_path:
            pygame.mixer.music.load(audio_file_path)
            save_audio_file(audio_file_path)
        else:
            print("No audio file selected.")
            messagebox.showwarning("Warning", "No audio file selected. Some features may not work.")
except Exception as e:
    print(f"Error loading audio file: {e}")
    messagebox.showerror("Error", f"Failed to load audio file: {e}")

pygame.mixer.music.set_volume(0.8)

try:
    if audio_file_path:
        length_in_s = int(pygame.mixer.Sound(audio_file_path).get_length())
        length_in_ms = length_in_s * 1000
        print(f"Song length in seconds: {length_in_s}")
except Exception as e:
    length_in_s = 0
    print(f"Could not load song length: {e}")

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
        try:
            pygame.mixer.music.play(start=0.0)
        except Exception as e:
            print(f"Error playing sound: {e}")
            messagebox.showerror("Error", f"Failed to play sound: {e}")
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

    try:
        # Function for checking if a timer is already running-stop it
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
    except Exception as e:
        print(f"Error starting timer: {e}")
        messagebox.showerror("Error", f"Failed to start timer: {e}")

def click_stop():
    global current_state, current_timer
    try:
        current_state = False
        if current_timer is not None:
            root.after_cancel(current_timer)
        root.after(0, recreate_entry)
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"Error stopping timer: {e}")
        messagebox.showerror("Error", f"Failed to stop timer: {e}")

def recreate_entry():
    entry.grid(row=2, column=3, sticky="nesw")

def always_on_top():
    root.attributes("-topmost", 1)
    root.update_idletasks()

# Window drag function
lastClickX = 0
lastClickY = 0

def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y

# Create main window
root = tk.Tk()
root.title("Timer")
root.geometry("180x70")

def on_validate(text):
    if text.isdigit() or text == "":
        return True
    return False

# Create UI elements
entry = tk.Entry(root, bg="#008000", width=3, validate="key")
entry['validatecommand'] = (entry.register(on_validate), '%S')
entry.grid(row=2, column=3, sticky="nesw")

progress_var = tk.IntVar()
style = ttk.Style()
style.theme_use('default')
style.configure("Custom.Horizontal.TProgressbar", 
                troughcolor='#c0c0c0', 
                background='#14b009', 
                thickness=20)

progress_bar = ttk.Progressbar(root, 
                              variable=progress_var, 
                              maximum=60, 
                              style="Custom.Horizontal.TProgressbar")
progress_bar.grid(row=1, column=0, columnspan=4, sticky="nesw")

options_window = None

def update_transparency(value):
    try:
        inverted_value = 1.2 - float(value)
        root.attributes('-alpha', inverted_value)
        if options_window:
            options_window.attributes('-alpha', inverted_value)
        settings = load_settings()
        settings["transparency"] = float(value)
        save_settings(settings)
    except Exception as e:
        print(f"Error updating transparency: {e}")
        messagebox.showerror("Error", f"Failed to update transparency: {e}")

def update_volume(value):
    try:
        volume = float(value)
        pygame.mixer.music.set_volume(volume)
        settings = load_settings()
        settings["volume"] = volume
        save_settings(settings)
    except Exception as e:
        print(f"Error updating volume: {e}")
        messagebox.showerror("Error", f"Failed to update volume: {e}")

def show_options():
    global options_window
    
    try:
        # Coordinates of current position of the main window
        x = root.winfo_x()
        y = root.winfo_y()
        
        options_window = tk.Toplevel(root)
        options_window.title("Options")
        options_window.geometry("250x160")
        
        # Position the options window at the same coordinates as the main window
        options_window.geometry(f"+{x}+{y}")

        settings = load_settings()

        transparency_frame = tk.Frame(options_window)
        transparency_frame.pack(pady=0)

        label = tk.Label(transparency_frame, text="Transparency:")
        label.pack(side="left", padx=(10, 5), pady=(5,0))
        
        style = ttk.Style()
        style.theme_use('aqua')
        style.configure('Custom.Horizontal.TScale', 
                       troughcolor='#c0c0c0', 
                       background='#14b009', 
                       thickness=20)

        transparency_slider = ttk.Scale(
            transparency_frame, 
            from_=0.2, 
            to=1, 
            command=update_transparency, 
            orient="horizontal", 
            style="Custom.Horizontal.TScale"
        )
        transparency_slider.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=(5,0))
        transparency_slider.set(settings["transparency"])

        volume_frame = tk.Frame(options_window)
        volume_frame.pack(pady=5)

        volume_label = tk.Label(volume_frame, text="Volume:")
        volume_label.pack(side="left", padx=(10, 5))

        volume_slider = ttk.Scale(
            volume_frame,
            from_=0,
            to=1,
            command=update_volume,
            orient="horizontal",
            style="Custom.Horizontal.TScale"
        )
        volume_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        volume_slider.set(settings["volume"])

        audio_frame = tk.Frame(options_window)
        audio_frame.pack(pady=5)
        label = tk.Label(audio_frame, text="Select an audio file:")
        label.pack(side="left", padx=(10, 5))

        browse_button = tk.Button(audio_frame, text="Browse", command=select_audio_file)
        browse_button.pack(side="left", padx=(0, 10), pady=(0,0))

        back_button = tk.Button(options_window, text="Back", command=lambda: go_back(options_window))
        back_button.pack(fill=tk.X, pady=(3, 0), padx=(30,30))

        root.withdraw()
    except Exception as e:
        print(f"Error showing options: {e}")
        messagebox.showerror("Error", f"Failed to show options window: {e}")

def select_audio_file():
    global audio_file_path
    try:
        file_path = filedialog.askopenfilename(
            title="Select Audio File", 
            filetypes=[("MP3 Files", "*.mp3")]
        )
        if file_path:
            audio_file_path = file_path
            pygame.mixer.music.load(audio_file_path)
            save_audio_file(audio_file_path)
    except Exception as e:
        print(f"Error selecting audio file: {e}")
        messagebox.showerror("Error", f"Failed to select audio file: {e}")

def go_back(window):
    try:
        window.destroy()
        root.deiconify()
        style.theme_use('default')
    except Exception as e:
        print(f"Error closing options window: {e}")
        messagebox.showerror("Error", f"Failed to close options window: {e}")

# Create buttons and widgets
start_button = tk.Button(root, text="Start", command=click_start)
stop_button = tk.Button(root, text="Stop", command=click_stop)
aot_button = tk.Button(root, text="->", command=always_on_top)
counter_label = tk.Label(root, text="Set timer to start")
options_button = tk.Button(root, text="⚙️", command=show_options)

# Configure grid
root.rowconfigure([0, 1, 2], minsize=10, weight=1)
root.columnconfigure([0, 1, 2, 3], minsize=10, weight=1)

# Place widgets in grid
entry.grid(row=2, column=3, sticky="nesw")
progress_bar.grid(row=1, column=0, columnspan=4, sticky="nesw")
stop_button.grid(row=2, column=1, sticky="nesw")
start_button.grid(row=2, column=0, sticky="nesw")
aot_button.grid(row=2, column=2, sticky="nesw")
counter_label.grid(row=0, column=0, columnspan=4, sticky="nesw")
options_button.grid(row=0, column=3, sticky="nesw")

# Load initial settings
try:
    initial_settings = load_settings()
    root.attributes('-alpha', 1.2 - initial_settings["transparency"])
    pygame.mixer.music.set_volume(initial_settings["volume"])
except Exception as e:
    print(f"Error loading initial settings: {e}")
    messagebox.showerror("Error", f"Failed to load initial settings: {e}")

# Bind events
root.bind('<Button-1>', SaveLastClickPos)
root.mainloop()