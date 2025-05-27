import keyboard
import pyautogui
import time
import threading
import tkinter as tk

clicking = False

def clicker():
    global clicking
    while True:
        if clicking:
            print("Clicked F6 - start")
            pyautogui.press('f6')
            time.sleep(10)
            print("Clicked F6 - end")
            pyautogui.press('f6')
            clicking = False
        time.sleep(0.1)

def toggle_clicker():
    global clicking
    clicking = not clicking
    print("Auto clicker started" if clicking else "Auto clicker stopped")

def run_gui():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.8)
    root.configure(bg='black')

    label = tk.Label(root, text="Stopped", fg="red", bg="black", font=("Arial", 14, "bold"))
    label.pack(padx=10, pady=5)

    screen_width = root.winfo_screenwidth()
    root.geometry(f"+{screen_width - 150}+50")

    def update_label():
        status = "Running" if clicking else "Stopped"
        color = "lime" if clicking else "red"
        label.config(text=status, fg=color)
        root.after(500, update_label)

    root.after(0, update_label)

    threading.Thread(target=clicker, daemon=True).start()

    keyboard.add_hotkey('f9', toggle_clicker)
    print("Press F9 to start/stop the auto clicker. Press ESC to exit.")

    def check_esc():
        if keyboard.is_pressed('esc'):
            root.destroy()
            return
        root.after(100, check_esc)

    root.after(100, check_esc)

    root.mainloop()

run_gui()
