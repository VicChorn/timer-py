
# Timer App with Sound Playback

This simple timer application, built using the Tkinter GUI toolkit in Python, provides users with a convenient way to set a timer and receive an audible alert when the countdown reaches zero. 
The app utilizes the pygame library for sound playback, allowing users to customize the audio alert by providing a local path to an MP3 file.


Added simple UI using the Tkinter library including the time for which the timer is set, and buttons for better control over the app.
![timer_exe](https://github.com/VicChorn/timer-py/assets/153026489/20261839-b299-47eb-a5d2-24cfe2fc8dcc)
According to timeit: average execution time: 0.08 seconds

## Features:
 - **Timer Input**: Users can set the timer duration by entering the desired time in minutes via the provided input field.

 - **Sound Playback**: The app supports customizable sound alerts. The user needs to provide the local path to an MP3 media file manually. The sound will play when the timer reaches zero.

## How to Use:
1. Run the application.
2. Enter the desired timer duration in minutes using the "Set Timer" button.
3. Click the "Start Timer" button to initiate the countdown.
## Requirements:
- Python with Tkinter and pygame libraries.
## Usage:
Copy & run code:
```bash
python timer_app.py
```

## Notes:
Make sure to provide the correct path to your desired MP3 file for sound playback.
The app displays the remaining seconds during the countdown in the console.
