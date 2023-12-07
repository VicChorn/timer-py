#TimerExe
#Allows the following:
#To set timer for different periods of time
#To pause timer
#To reset timer

import tkinter as tk
import time
import pygame

from datetime import datetime, timedelta

#Sound playback settings
pygame.mixer.init()
pygame.mixer.music.load("C:\\Users\\chorn\\Downloads\\runa_tone_trimmed.mp3")
pygame.mixer.music.set_volume(0.2)

length_in_s = int((pygame.mixer.Sound("C:\\Users\\chorn\\Downloads\\goggins.mp3")).get_length())
length_in_ms = length_in_s * 1000
print(f"Song length in seconds {length_in_s}")

def timer (set_timer_to ):
        set_timer_to = float(input("Set timer to: "))
        current_time = datetime.now()

        timer_time = current_time + timedelta(seconds=set_timer_to)
        seconds = (timer_time) - (current_time)
        difference = int((seconds.total_seconds()))

        print (f'Timer in: {difference} seconds')
        print (f'Current time: {current_time}')
        print (f'Timer set to: {timer_time}')

        while current_time < timer_time:
                time.sleep(1)
                current_time = datetime.now()
                difference = difference - 1
                print(f"{(difference)} seconds remaining")

        print("Breaking from the loop")
        pygame.mixer.music.play(start=0.0)
        pygame.time.wait(length_in_ms)
timer(0.12)

