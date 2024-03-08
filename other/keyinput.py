try:
    import keyboard
except:
    import os
    os.system("pip install keyboard")
    import keyboard
import time


def get_input():
    press = False
    release = False
    allowed = ["down", "up", "right", "left", "enter"]
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name in allowed:
            press = True
            pressed = event.name
        if event.event_type == keyboard.KEY_UP and press and event.name == pressed:
            return pressed


can_press = ["down", "up", "left", "right", "enter", "+", "-"]


def get_press():
    p = []
    for i in can_press:
        if keyboard.is_pressed(i):
            p.append(i)
    return p

def write_eqn(s):
    keyboard.write(s)

if __name__ == "__main__":
    while True:
        time.sleep(0.5)
        print(get_press())
