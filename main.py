#TimerExe
#Allows the following:
#To set timer for different periods of time - done
#To pause timer - to be implemented in next updates
#To reset timer - to be implemented in next updates

import tkinter as tk
import time
import pygame

root = tk.Tk()
label = tk.Label(text="Timer")
label.pack()

#Sound playback settings
pygame.mixer.init()
pygame.mixer.music.load("C:\\Users\\chorn\\Downloads\\runa_tone_trimmed.mp3")
pygame.mixer.music.set_volume(0.2)

#User needs to provide path to the local .mp3 media file manually
length_in_s = int((pygame.mixer.Sound("C:\\Users\\chorn\\Downloads\\goggins.mp3")).get_length())
length_in_ms = length_in_s * 1000
print(f"Song length in seconds {length_in_s}")


entry = tk.Entry(fg = "white",bg = "#008080")
entry.pack()

#User input for timer
def ask_for_entry():
    set_timer_to = int(entry.get())
    print(f"Timer is set to: {set_timer_to}")
    return set_timer_to
    

def timer ():       
    set_timer_to = int(entry.get())
    seconds = (set_timer_to * 60)
    while seconds != 0:
            time.sleep(1)
            seconds = seconds - 1
            print(f"{(seconds)} seconds remaining")

    pygame.mixer.music.play(start=0.0)
    pygame.time.wait(length_in_ms)


button = tk.Button(root, text="Set Timer", command=ask_for_entry)
button.pack()

button= tk.Button(root, text="Start timer", command=timer)
button.pack()

root.mainloop()
