import pyautogui as pyg
import keyboard, json, time

BIND_KEY = "b"

print(f"Hover your mouse above the download button, then press '{BIND_KEY}' to assign it")

try:
    pos = None
    while True:
        if keyboard.is_pressed(BIND_KEY):
            pos = pyg.position()
            print(f"{pos} as download button. (Ctrl + C to confirm)")
        time.sleep(.1)

except KeyboardInterrupt:
    if pos == None:
        print("No position set!")
        quit(1)
    
    print(f"Set to {pos}")
    json.dump({"dl_btn_pos":[pos.x,pos.y]}, open("config.json", "w"))
    quit(0)