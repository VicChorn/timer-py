import tkinter as tk
from tkinter import ttk
import pygame
import time

from tkinter import filedialog

#Sound playback settings
pygame.mixer.init()
config_file_path = "config.txt"

#Function to load audio file path from config file
def load_audio_file():
    try:
        with open(config_file_path, "r") as file:
            return file.readline().strip()
    except FileNotFoundError:
        return None

def save_audio_file(audio_file_path):
    with open(config_file_path, "w") as file: 
        file.write(audio_file_path)

#Default audio file
audio_file_path = load_audio_file()
if audio_file_path:
    pygame.mixer.music.load(audio_file_path)
else:
    audio_file_path = "/Users/Victor/Downloads/goggins.mp3"  # Default audio file
    pygame.mixer.music.load(audio_file_path)

pygame.mixer.music.set_volume(0.8)

#User needs to provide the path to the local .mp3 media file manually or choose one from PC in setting

# Sound playback settings
pygame.mixer.init()
pygame.mixer.music.load("/Users/Victor/Downloads/goggins.mp3")
pygame.mixer.music.set_volume(0.8)

# User needs to provide the path to the local .mp3 media file manually

length_in_s = int((pygame.mixer.Sound("/Users/Victor/Downloads/goggins.mp3")).get_length())
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


    #Function for checking if a timer is already running-stop it

    # Check if a timer is already running, stop it
 main
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
    pygame.mixer.music.stop()

def recreate_entry():
    entry.grid(row=2, column=3, sticky="nesw")

def always_on_top():
    root.attributes("-topmost", 1)
    root.update_idletasks()

#Window drag function
lastClickX = 0
lastClickY = 0

def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


# def Dragging(event):
#     x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
#     root.geometry(f"+{x}+{y}")
def Dragging(event):
    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry(f"+{x}+{y}")

root = tk.Tk()
root.title("Timer")
root.geometry("180x70")


def on_validate(text):
    if text.isdigit():
        return True
    else:
        return False

entry = tk.Entry(root, bg="#008000", width=3, validate="key")
entry['validatecommand'] = (entry.register(on_validate), '%S')
entry = tk.Entry(root, bg="#008000", width=3)
entry.grid(row=2, column=3, sticky="nesw")

progress_var = tk.IntVar()
style = ttk.Style()
style.theme_use('default')
style.configure("Custom.Horizontal.TProgressbar", troughcolor='#c0c0c0', background='#14b009', thickness=20)  # Set thickness here
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=60, style="Custom.Horizontal.TProgressbar")
progress_bar.grid(row=1, column=0, columnspan=4, sticky="nesw")

options_window = None 

def update_transparency(value):

    inverted_value = 1.2 - float(value)
    #Function to update transparency of main window and options window
    root.attributes('-alpha', inverted_value)
    if options_window:
        options_window.attributes('-alpha', inverted_value)

def show_options():
    global options_window
    #Creating a new TopLevel window, otherwise not working
    options_window = tk.Toplevel(root)
    options_window.title("Options")

    #Setting the size of the options window
    options_window.geometry("250x120")

    #Get the position of the main window
    main_window_x = root.winfo_x()
    main_window_y = root.winfo_y()

    # Setting the position of the options window relative to the main window
    options_window.geometry(f"+{main_window_x}+{main_window_y}")

    #Adding widgets to the options window
    transparency_frame = tk.Frame(options_window)
    transparency_frame.pack(pady=0)

    label = tk.Label(transparency_frame, text="Transparency:")
    label.pack(side="left", padx=(10, 5),pady=(5,0))
    
    #Transparency styling:
    style = ttk.Style()
    style.theme_use('aqua')
    style.configure('Custom.Horizontal.TScale', troughcolor='#c0c0c0', background='#14b009', thickness=20)

    #Creating the ttk.Scale widget with the custom style
    transparency_slider = ttk.Scale(transparency_frame, from_=0.2, to=1, command=update_transparency, orient="horizontal", style="Custom.Horizontal.TScale")
    transparency_slider.pack(side="left", fill="x", expand=True, padx=(0, 10),pady=(5,0))
    transparency_slider.set(0.2)

    audio_frame = tk.Frame(options_window)
    audio_frame.pack(pady=5)
    label = tk.Label(audio_frame, text="Select an audio file:")
    label.pack(side="left", padx=(10, 5))

    browse_button = tk.Button(audio_frame, text="Browse", command=select_audio_file)
    browse_button.pack(side="left", padx=(0, 10), pady=(0,0))

    #Adding a button to close the options window and go back to the main window
    back_button = tk.Button(options_window, text="Back", command=lambda: go_back(options_window))
    back_button.pack(fill=tk.X,pady=(3, 0), padx=(30,30))

    #Hide the main window while the options window is open
    root.withdraw()

def select_audio_file():
    global audio_file_path
    file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        audio_file_path = file_path
        # Update audio file used in the timer
        pygame.mixer.music.load(audio_file_path)
        # Save selected audio file path to config file
        save_audio_file(audio_file_path)
    # Function to update transparency of main window and options window
    root.attributes('-alpha', float(value))
    if options_window:
        options_window.attributes('-alpha', float(value))

def show_options():
    global options_window
    # Create a new TopLevel window, otherwise not working
    options_window = tk.Toplevel(root)
    options_window.title("Options")

    # Get the width and height of the main window
    main_window_width = root.winfo_width()
    main_window_height = root.winfo_height()

    # Set the size of the options window to match the main window
    options_window.geometry(f"{main_window_width}x{main_window_height}")

    # Set the position of the options window relative to the main window
    options_window.geometry(f"+{root.winfo_x()}+{root.winfo_y()}")

    # Add widgets to the options window
    transparency_slider = tk.Scale(options_window, from_=0.2, to=1, resolution=0.05, orient="horizontal", label="Transparency", font=("Arial", 11), command=update_transparency)
    transparency_slider.pack()

    # Add a button to close the options window and go back to the main window
    back_button = tk.Button(options_window, text="Back", command=lambda: go_back(options_window))
    back_button.pack()

    # Hide the main window while the options window is open
    root.withdraw()

def go_back(window):
    # Callback function to go back to the main window
    window.destroy()
    root.deiconify()

    style.theme_use('default')

#Buttons and other widgets

# Buttons and other widgets
start_button = tk.Button(root, text="Start", command=click_start)
stop_button = tk.Button(root, text="Stop", command=click_stop)
aot_button = tk.Button(root, text="->", command=always_on_top)
counter_label = tk.Label(root, text="Set timer to start")
options_button = tk.Button(root, text="⚙️",command=show_options)

#Placing all of them on the grid, final layout of the app
# Placing all of them on the grid, final layout of the app
root.rowconfigure([0, 1, 2], minsize=10, weight=1)
root.columnconfigure([0, 1, 2, 3], minsize=10, weight=1)

entry.grid(row=2, column=3, sticky="nesw")
progress_bar.grid(row=1, column=0, columnspan=4, sticky="nesw")
stop_button.grid(row=2, column=1, sticky="nesw")
start_button.grid(row=2, column=0, sticky="nesw")
aot_button.grid(row=2, column=2, sticky="nesw")
counter_label.grid(row=0, column=0, columnspan=4, sticky="nesw")
options_button.grid(row=0, column=3, sticky="nesw")

root.attributes('-alpha', 1)

#For debug purposes
#def debug_click(event):
#    print(f"Click event on {event.widget}")
#start_button.bind('<Button-1>', debug_click)
#stop_button.bind('<Button-1>', debug_click)
#aot_button.bind('<Button-1>', debug_click)

#Can be used in conjunction with dragging func in Windows machines:
#root.overrideredirect(True)  --removes windows outline and native window control buttons
root.bind('<Button-1>', SaveLastClickPos)
#root.bind('<B1-Motion>', Dragging) --used for dragging window without window control buttons

root.attributes('-alpha', 0.5)

#For debug purposes
# def debug_click(event):
#     print(f"Click event on {event.widget}")
# start_button.bind('<Button-1>', debug_click)
# stop_button.bind('<Button-1>', debug_click)
# aot_button.bind('<Button-1>', debug_click)

#root.overrideredirect(True)
root.bind('<Button-1>', SaveLastClickPos)
root.bind('<B1-Motion>', Dragging)

root.mainloop()
