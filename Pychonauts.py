import keyboard
import tkinter as tk
import pygame
import pymem.exception
import time
import webbrowser
from threading import Thread
from pymem import *
from pymem.process import *
from pymem.ptypes import RemotePointer
from time import sleep

while True:
    password = input("Enter password ")
    if password == "115":
        print("Welcome")
        break
    else:
        print("Try again retard")


mem = Pymem("Psychonauts2-Win64-Shipping")

module = module_from_name(mem.process_handle, "Psychonauts2-Win64-Shipping.exe").lpBaseOfDll

laser_offsets = [0x8, 0x8, 0x270, 0xE0, 0x8, 0x104]
health_offsets = [0x0, 0x20, 0x568, 0xD0, 0x0, 0x30]
speed_offsets = [0xE0, 0x90, 0xD0, 0x500, 0x0, 0x0, 0xAC]
cash_offsets = [0x490, 0x140, 0x68, 0x3E8, 0x230]
pspops_offsets = [0x490, 0x140,  0x128, 0x3E8, 0x180]
player_speed = [0x20, 0x120, 0x98]
gravity_offsets = [0x90, 0x360, 0x2b8, 0xb50]

endInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class input_i(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", input_i)]


# Actuals Functions
def presskey(hexkeycode):
    extra = ctypes.c_ulong(0)
    ii_ = input_i()
    ii_.ki = KeyBdInput(0, hexkeycode, 0x0008, 0, ctypes.pointer(extra))
    x = input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def releasekey(hexkeycode):
    extra = ctypes.c_ulong(0)
    ii_ = input_i()
    ii_.ki = KeyBdInput(0, hexkeycode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def getpointeraddress(base, offsets):
    remote_pointer = RemotePointer(mem.process_handle, base)
    for offset in offsets:
        if offset != offsets[-1]:
            remote_pointer = RemotePointer(mem.process_handle, remote_pointer.value + offset)
        else:
            return remote_pointer.value + offset


def multi_run_god():
    new_thread = Thread(target=god_hack, daemon=True)
    new_thread.start()


def multi_run_meth():
    new_thread = Thread(target=meth, daemon=True)
    new_thread.start()


def multi_run_fuck_gravity():
    new_thread = Thread(target=fuck_gravity, daemon=True)
    new_thread.start()


def multi_run_spam():
    new_thread = Thread(target=spam, daemon=True)
    new_thread.start()


def god_hack():
    addr1 = getpointeraddress(module + 0x05549500, laser_offsets)
    addr2 = getpointeraddress(module + 0x05540360, health_offsets)
    addr3 = getpointeraddress(module + 0x0533DD00, cash_offsets)
    while 1:
        try:
            mem.write_int(addr1, 0x57550000)
            mem.write_int(addr2, 0x47960000)
            mem.write_int(addr3, 0x5000)

            sleep(0.02)
            if keyboard.is_pressed("space"):
                keyboard.press_and_release("space")
                sleep(0.07)
                continue
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            break


def spam():
    while 1:
        try:
            # spam e key
            presskey(18)
            time.sleep(0.01)
            releasekey(18)

        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            print("Bot shutting down...")
            break


def meth():
    addr = getpointeraddress(module + 0x054B9258, player_speed)
    while 1:
        try:
            mem.write_int(addr, 0x40a00000)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            mem.write_int(addr, 0x3f800000)
            break


def fuck_gravity():
    addr = getpointeraddress(module + 0x054B9258, gravity_offsets)
    while 1:
        try:
            mem.write_int(addr, 0x00000000)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            mem.write_int(addr, 0x3f800000)
            break


pygame.init()
pygame.mixer_music.load("music/mod.mp3")
pygame.mixer_music.play(1)
root = tk.Tk()
photo = tk.PhotoImage(file="back/155.png")
root.wm_iconphoto(False, photo)
root.title("Fragging Terminal")
root.configure(background='dark red')
root.geometry("265x145")


def callback(url):
    webbrowser.open_new(url)


def show():
    root.deiconify()


def hide():
    root.withdraw()


button1 = tk.Button(root, text="God Mode", bg='black', fg='white', command=multi_run_god)
button1.grid(row=0, column=0)
button2 = tk.Button(root, text="Meth", bg='black', fg='white', command=multi_run_meth)
button2.grid(row=1, column=0)
button3 = tk.Button(root, text="Fuck Gravity", bg='black', fg='white', command=multi_run_fuck_gravity)
button3.grid(row=2, column=0)
button4 = tk.Button(root, text="Exit", bg='white', fg='black', command=root.destroy)
button4.grid(row=4, column=0)
label4 = tk.Label(master=root, text='C Show GUI', bg='red', fg='black')
label4.grid(row=0, column=3)
label5 = tk.Label(master=root, text='V Hide GUI', bg='red', fg='black')
label5.grid(row=1, column=3)
label6 = tk.Label(master=root, text='F1 KILLS LOOPS', bg='red', fg='black')
label6.grid(row=2, column=3)
label7 = tk.Label(master=root, text='L Spam E key', bg='red', fg='black')
label7.grid(row=3, column=3)
label8 = tk.Label(master=root, text='K KILL EXE', bg='red', fg='black')
link1 = tk.Label(root, text="Your Sleep Paralysis Demon", bg="black", fg="red", cursor="hand2")
link1.grid(row=7, column=0)
link1.bind("<Button-1>", lambda e: callback("https://steamcommunity.com/profiles/76561198259829950/"))

keyboard.add_hotkey("c", show)
keyboard.add_hotkey("v", hide)
keyboard.add_hotkey("l", multi_run_spam)
keyboard.add_hotkey("k", root.destroy)
root.mainloop()
