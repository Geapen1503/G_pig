import tkinter as tk
import pyautogui
import random
import math
import pynput
import ctypes

ctypes.windll.kernel32.SetConsoleTitleW("System_Process")

root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes("-topmost", True)
root.attributes("-transparentcolor", "white")

cochon_x, cochon_y = 100, 100
cochon_size = 60
animation_step = 13
pattes_deplacees = False

canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="white",
                   highlightthickness=0)
canvas.pack()

def dessiner_cochon(x, y, eating=False):
    global pattes_deplacees
    canvas.delete("cochon")
    canvas.create_oval(x, y, x + cochon_size, y + cochon_size, fill="pink", outline="", tags="cochon")
    canvas.create_oval(x + 20, y + 20, x + 40, y + 40, fill="hot pink", outline="", tags="cochon")
    canvas.create_oval(x + 10, y + 10, x + 15, y + 15, fill="black", outline="", tags="cochon")
    canvas.create_oval(x + 45, y + 10, x + 50, y + 15, fill="black", outline="", tags="cochon")
    canvas.create_polygon(x + 10, y - 10, x + 20, y, x + 30, y - 10, fill="pink", outline="", tags="cochon")
    canvas.create_polygon(x + 30, y - 10, x + 40, y, x + 50, y - 10, fill="pink", outline="", tags="cochon")

    if pattes_deplacees:
        canvas.create_oval(x + 5, y + 45, x + 15, y + 55, fill="pink", outline="", tags="cochon")
        canvas.create_oval(x + 35, y + 55, x + 45, y + 65, fill="pink", outline="", tags="cochon")
    else:
        canvas.create_oval(x + 5, y + 55, x + 15, y + 65, fill="pink", outline="", tags="cochon")
        canvas.create_oval(x + 45, y + 55, x + 55, y + 65, fill="pink", outline="", tags="cochon")

    if eating:
        canvas.create_oval(x + 20, y + 20, x + 40, y + 40, fill="orange", outline="", tags="cochon")

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def bouger_vers_souris():
    global cochon_x, cochon_y, pattes_deplacees
    souris_x, souris_y = pyautogui.position()

    if distance(cochon_x, cochon_y, souris_x, souris_y) < 50:
        cacher_souris()
        dessiner_cochon(cochon_x, cochon_y, eating=True)
        root.after(1000, deplacer_aleatoirement)
    else:
        angle = math.atan2(souris_y - cochon_y, souris_x - cochon_x)
        cochon_x += animation_step * math.cos(angle)
        cochon_y += animation_step * math.sin(angle)

        pattes_deplacees = not pattes_deplacees
        dessiner_cochon(cochon_x, cochon_y)
        root.after(50, bouger_vers_souris)

def cacher_souris():
    mouse_listener = pynput.mouse.Listener(suppress=True)
    mouse_listener.start()
    keyboard_listener = pynput.keyboard.Listener(suppress=True)
    keyboard_listener.start()

def deplacer_aleatoirement():
    global cochon_x, cochon_y, pattes_deplacees
    direction = random.choice(["haut", "bas", "gauche", "droite"])

    if direction == "haut":
        cochon_y -= 20
    elif direction == "bas":
        cochon_y += 20
    elif direction == "gauche":
        cochon_x -= 20
    elif direction == "droite":
        cochon_x += 20

    cochon_x = max(0, min(cochon_x, root.winfo_screenwidth() - cochon_size))
    cochon_y = max(0, min(cochon_y, root.winfo_screenheight() - cochon_size))

    pattes_deplacees = not pattes_deplacees
    dessiner_cochon(cochon_x, cochon_y)
    root.after(300, deplacer_aleatoirement)

def stop_program(event=None):
    root.destroy()

bouger_vers_souris()
root.bind('<Control-Alt-Shift-KeyPress-G>', stop_program)

root.mainloop()
