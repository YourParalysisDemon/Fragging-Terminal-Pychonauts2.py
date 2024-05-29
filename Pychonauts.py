
import keyboard
import tkinter as tk
import pygame
import pymem.exception
from threading import Thread
from pymem import *
from pymem.process import *
from pymem.ptypes import RemotePointer
from time import sleep

mem = Pymem("Psychonauts2-Win64-Shipping")

module = module_from_name(mem.process_handle, "Psychonauts2-Win64-Shipping.exe").lpBaseOfDll

laser_offsets = [0x8, 0x8, 0x270, 0xE0, 0x8, 0x104]
health_offsets = [0x0, 0x20, 0x568, 0xD0, 0x0, 0x30]
speed_offsets = [0xE0, 0x90, 0xD0, 0x500, 0x0, 0x0, 0xAC]
cash_offsets = [0x490, 0x140, 0x68, 0x3E8, 0x230]
pspops_offsets = [0x490, 0x140,  0x128, 0x3E8, 0x180]
player_speed = [0x20, 0x120, 0x98]


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


pygame.init()
pygame.mixer_music.load("music/mod.mp3")
pygame.mixer_music.play(1)

root = tk.Tk()
root.title("Fragging Terminal")
root.geometry("200x180")
root.configure(background='dark red')
root.attributes("-topmost", True)


def show():
    root.deiconify()


def hide():
    root.withdraw()


button1 = tk.Button(root, text="God Mode", bg='black', fg='white', command=multi_run_god)
button1.grid(row=0, column=0)
button2 = tk.Button(root, text="Meth", bg='black', fg='white', command=multi_run_meth)
button2.grid(row=1, column=0)
button4 = tk.Button(root, text="Exit", bg='white', fg='black', command=root.destroy)
button4.grid(row=3, column=0)
label4 = tk.Label(master=root, text='C Show GUI', bg='red', fg='black')
label4.grid(row=0, column=3)
label5 = tk.Label(master=root, text='V Hide GUI', bg='red', fg='black')
label5.grid(row=1, column=3)
label6 = tk.Label(master=root, text='F1 KILLS LOOPS', bg='red', fg='black')
label6.grid(row=2, column=3)

keyboard.add_hotkey("c", show)
keyboard.add_hotkey("v", hide)
root.mainloop()
