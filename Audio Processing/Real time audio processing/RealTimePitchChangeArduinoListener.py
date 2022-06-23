import pyaudio
import wave
import numpy as np
import time
import serial
import io
import keyboard

# ---------------------- #
"""ÆNDRE DETTE HVIS DU BRUGER Arduino MED KODEN TIL TRUE, OG FALSE UDEN"""
Arudino_Connect = False
# ---------------------- #

p = pyaudio.PyAudio()
file = wave.open('heartbeat.wav', 'rb')
n = 1
# Chunk nummere der kan bruges
#  0.25 0.5 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536 131072

chunk = 8192

"""Portaudio Sample Formats: paFloat32, paInt32, paInt24, paInt16, paInt8, paUInt8, paCustomFormat 
paInt16 is basically a signed 16-bit binary string. 15 bits for the number, and one for the sign, 
leaving your range options to be (-32768, 32767) if I'm not completely mistaken. 2^15, anyway. """
FORMAT = pyaudio.paInt16
RATE = 44100


def ChangePitch(sound_In_Array, n):
    new_sound_In_Array = np.array(np.arange(start=0, stop=len(sound_In_Array), step=n), dtype='int16')
    return sound_In_Array[new_sound_In_Array]

print(f'[STARING STREAMER]')
stream = p.open(format=FORMAT,
                channels=file.getnchannels(),
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=chunk)

if Arudino_Connect:
    print(f'[STARING Arduino]')
    PORT = 'COM3'
    arduino = serial.serial_for_url(PORT, 9600, timeout=.1)
    print(arduino)
    sio = io.TextIOWrapper(io.BufferedRWPair(arduino, arduino))
    print("[CONNECTED]")
    sio.flush()  # it is buffering. required to get the data out *now*
    time.sleep(1)

while True:
    if Arudino_Connect:
        send_data = sio.readline()[:-1]
        if send_data == "INTENSITY 1":
            print("Worked")
            n = 1
        if send_data == "INTENSITY 2":
            print("INTENSITY 2")
            n = 1.5
        if send_data == "INTENSITY 3":
            n = 2.0
            print("INTENSITY 3")

    if not Arudino_Connect:
        if keyboard.is_pressed('a'):  # if key 'q' is pressed
            n -= .5
            print("A have been pressed")
            print(f'Value of n is: {n}')
        if keyboard.is_pressed('s'):  # if key 'q' is pressed
            print("B have been pressed")
            n += .5
            print(f'Value of n is: {n}')

    data = file.readframes(chunk)
    data = np.array(wave.struct.unpack("%dh" % (len(data) / 2), data), dtype='int16')
    new_data = ChangePitch(data, n)
    dataout = np.array(new_data, dtype='int16')
    chunkout = wave.struct.pack("%dh" % (len(dataout)), *list(dataout))  # convert back to String Byte
    stream.write(chunkout)
