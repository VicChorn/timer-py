import tkinter as tk
from tkinter import ttk
import pygame
import time
import os
from tkinter import filedialog
import json
import sys
from tkinter import messagebox

# Getting the base application path for resources 
def resource_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(resource_path(), "config.txt")
SETTINGS_FILE = os.path.join(resource_path(), "settings.json")
DEFAULT_SETTINGS = {"transparency": 0.2, "volume": 0.8}

class TimerApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Timer")
        self.geometry("180x70")

        self._current_state = False   # True when timer is counting down
        self._current_timer = None    # ID returned by self.after()
        self._on_top = False          # Current always-on-top state
        self._options_window = None   # Reference to the options Toplevel
        self._audio_file_path = None  # Path to the alarm MP3
        self._save_job = None         # Debounce job ID for settings write

        # Settings are loaded once into memory; updated in-place and get written only when slider stop moving
        self._settings = self._load_settings()

        # Initialize pygame mixer with error handling
        self._pygame_ok = False
        try:
            pygame.mixer.init()
            self._pygame_ok = True
        except pygame.error as e:
            print(f"Pygame mixer init failed: {e}")
        
        self._build_ui()
        self._apply_initial_settings()

        self.after(100, self._setup_audio)
    #Load and initialize audio
    def _setup_audio(self):
        if not self._pygame_ok:
            messagebox.showerror("Error", "Audio system failed to initialize.")
            return

        saved = self._load_audio_path()
        if saved and os.path.exists(saved):
            self._load_audio(saved)
        else:
            self._prompt_audio_file()

    def _load_audio(self, path):
        try:
            pygame.mixer.music.load(path)
            self._audio_file_path = path
        except Exception as e:
            print(f"Error loading audio: {e}")
            messagebox.showerror("Error", f"Failed to load audio file: {e}")

    def _prompt_audio_file(self):
        path = filedialog.askopenfilename(
            title="Select an Audio File",
            filetypes=[("MP3 Files", "*.mp3")]
        )
        if path:
            self._load_audio(path)
            self._save_audio_path(path)
        else:
            messagebox.showwarning(
                "Warning",
                "No audio file selected. Timer sound won't play."
            )

    def _load_audio_path(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    return f.readline().strip() or None
        except Exception as e:
            print(f"Error reading config: {e}")
        return None
    # Load selected audio file into pygame
    def _save_audio_path(self, path):
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE) or ".", exist_ok=True)
            with open(CONFIG_FILE, "w") as f:
                f.write(path)
        except Exception as e:
            print(f"Error saving config: {e}")
            messagebox.showerror("Error", f"Failed to save audio path: {e}")

    #Load saved settings from json file
    def _load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
        return dict(DEFAULT_SETTINGS)
    
    # Saving current settings to disk
    def _save_settings(self):
        try:
            os.makedirs(os.path.dirname(SETTINGS_FILE) or ".", exist_ok=True)
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self._settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    # Delaying saving whle user is moving sliders
    def _schedule_save(self):
        if self._save_job:
            self.after_cancel(self._save_job)
        self._save_job = self.after(500, self._save_settings)

    def _apply_initial_settings(self):
        try:
            self.attributes('-alpha', 1.2 - self._settings["transparency"])
            if self._pygame_ok:
                pygame.mixer.music.set_volume(self._settings["volume"])
        except Exception as e:
            print(f"Error applying initial settings: {e}")
    # Create UI elements
    def _build_ui(self):
        self.rowconfigure([0, 1, 2], minsize=10, weight=1)
        self.columnconfigure([0, 1, 2, 3], minsize=10, weight=1)

        vcmd = (self.register(self._validate_input), '%S')

        # Input field (minutes)
        self._entry = tk.Entry(
            self, bg="#008000", width=3,
            validate="key", validatecommand=vcmd
        )
        self._entry.grid(row=2, column=3, sticky="nesw")

        # Progress bar
        self._progress_var = tk.IntVar()
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor='#c0c0c0', background='#14b009', thickness=20
        )
        self._progress_bar = ttk.Progressbar(
            self, variable=self._progress_var, maximum=60,
            style="Custom.Horizontal.TProgressbar"
        )
        self._progress_bar.grid(row=1, column=0, columnspan=4, sticky="nesw")

        # Counter label
        self._counter_label = tk.Label(self, text="Set timer to start")
        self._counter_label.grid(row=0, column=0, columnspan=4, sticky="nesw")

        # Buttons
        tk.Button(self, text="Start", command=self._click_start).grid(
            row=2, column=0, sticky="nesw")
        tk.Button(self, text="Stop", command=self._click_stop).grid(
            row=2, column=1, sticky="nesw")

        self._aot_button = tk.Button(self, text="→", command=self._toggle_on_top)
        self._aot_button.grid(row=2, column=2, sticky="nesw")

        tk.Button(self, text="⚙️", command=self._show_options).grid(
            row=0, column=3, sticky="nesw")

    def _validate_input(self, char):
        """Allow only digit characters in the entry field."""
        return char.isdigit()

    def _tick(self, seconds):
        if self._current_state and seconds > 0:
            seconds -= 1
            self._counter_label.config(text=self._format_time(seconds))
            self._progress_var.set(seconds)
            self._current_timer = self.after(1000, self._tick, seconds)
        elif seconds == 0:
            self._on_time_up()
        else:
            # Timer was stopped externally
            self._show_entry()

    # Called when countdown reaches zero
    def _on_time_up(self):
        self._progress_var.set(0)
        self._show_entry()
        if not self._pygame_ok or not self._audio_file_path:
            return
        try:
            pygame.mixer.music.play(start=0.0)
        except Exception as e:
            print(f"Error playing sound: {e}")
            messagebox.showerror("Error", f"Failed to play sound: {e}")

    # Converting seconds into HH:MM:SS format
    def _format_time(self, seconds):
        h, remainder = divmod(seconds, 3600)
        m, s = divmod(remainder, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    
    # Starting countdown using entered minutes
    def _click_start(self):
        raw = self._entry.get().strip()
        if not raw:
            messagebox.showwarning(
                "Input required",
                "Please enter the number of minutes."
            )
            return

        try:
            # Cancel any running timer before starting a new one
            if self._current_timer is not None:
                self.after_cancel(self._current_timer)
                if self._pygame_ok:
                    pygame.mixer.music.stop()

            self._current_state = True
            seconds = int(raw) * 60
            self._progress_var.set(seconds)
            self._progress_bar.config(maximum=seconds)
            self._entry.grid_forget()
            self._tick(seconds)
        except Exception as e:
            print(f"Error starting timer: {e}")
            messagebox.showerror("Error", f"Failed to start timer: {e}")

    # Stops current timer and reset UI
    def _click_stop(self):
        try:
            self._current_state = False
            if self._current_timer is not None:
                self.after_cancel(self._current_timer)
                self._current_timer = None
            if self._pygame_ok:
                pygame.mixer.music.stop()
            self.after(0, self._show_entry)
        except Exception as e:
            print(f"Error stopping timer: {e}")
            messagebox.showerror("Error", f"Failed to stop timer: {e}")

    def _show_entry(self):
        self._entry.grid(row=2, column=3, sticky="nesw")

    # Enabling/disabling always-on-top mode, now fully toggleable 
    def _toggle_on_top(self):
        """Toggle the always-on-top state and update the button label."""
        self._on_top = not self._on_top
        self.attributes("-topmost", self._on_top)
        self._aot_button.config(text="✓→" if self._on_top else "→")

    # Open settings window
    def _show_options(self):
        if self._options_window and self._options_window.winfo_exists():
            self._options_window.lift()
            return

        x, y = self.winfo_x(), self.winfo_y()
        win = tk.Toplevel(self)
        win.title("Options")
        win.geometry(f"250x160+{x}+{y}")
        win.protocol("WM_DELETE_WINDOW", lambda: self._close_options(win))
        self._options_window = win

        opt_style = ttk.Style()
        opt_style.theme_use('aqua')
        opt_style.configure(
            'Custom.Horizontal.TScale',
            troughcolor='#c0c0c0', background='#14b009', thickness=20
        )

        # Transparency row
        t_frame = tk.Frame(win)
        t_frame.pack(pady=(5, 0))
        tk.Label(t_frame, text="Transparency:").pack(side="left", padx=(10, 5))
        t_slider = ttk.Scale(
            t_frame, from_=0.2, to=1, orient="horizontal",
            style="Custom.Horizontal.TScale",
            command=self._update_transparency
        )
        t_slider.set(self._settings["transparency"])
        t_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Volume row
        v_frame = tk.Frame(win)
        v_frame.pack(pady=5)
        tk.Label(v_frame, text="Volume:").pack(side="left", padx=(10, 5))
        v_slider = ttk.Scale(
            v_frame, from_=0, to=1, orient="horizontal",
            style="Custom.Horizontal.TScale",
            command=self._update_volume
        )
        v_slider.set(self._settings["volume"])
        v_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Audio file row
        a_frame = tk.Frame(win)
        a_frame.pack(pady=5)
        tk.Label(a_frame, text="Audio file:").pack(side="left", padx=(10, 5))
        tk.Button(
            a_frame, text="Browse", command=self._select_audio_file
        ).pack(side="left", padx=(0, 10))

        # Back button
        tk.Button(
            win, text="Back",
            command=lambda: self._close_options(win)
        ).pack(fill=tk.X, pady=(3, 0), padx=30)

        self.withdraw()

    # Updating window transparency and saving setting
    def _update_transparency(self, value):
        try:
            alpha = 1.2 - float(value)
            self.attributes('-alpha', alpha)
            if self._options_window and self._options_window.winfo_exists():
                self._options_window.attributes('-alpha', alpha)
            self._settings["transparency"] = float(value)
            self._schedule_save()
        except Exception as e:
            print(f"Error updating transparency: {e}")

    # Updating alarm volume and saving setting
    def _update_volume(self, value):
        try:
            vol = float(value)
            if self._pygame_ok:
                pygame.mixer.music.set_volume(vol)
            self._settings["volume"] = vol
            self._schedule_save()
        except Exception as e:
            print(f"Error updating volume: {e}")

    # Let user choose a new alarm sound
    def _select_audio_file(self):
        path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("MP3 Files", "*.mp3")]
        )
        if path:
            self._load_audio(path)
            self._save_audio_path(path)

    def _close_options(self, window):
        try:
            window.destroy()
            self._options_window = None
            self.deiconify()
            # Restore the style used by the main window
            ttk.Style().theme_use('default')
        except Exception as e:
            print(f"Error closing options: {e}")

# Application entry point
if __name__ == "__main__":
    app = TimerApp()
    app.mainloop()