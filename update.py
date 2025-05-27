import keyboard
import pyautogui
import time
import threading
import tkinter as tk
import pystray
from PIL import Image

clicking = False
root = None  # Global variable to hold the Tkinter root window

def clicker():
    """
    The core clicking logic. Continuously presses F6 with specified delays
    when the 'clicking' flag is True.
    """
    global clicking
    while True:
        while clicking:
            print("Clicked F6 - start")
            pyautogui.press('f6')
            time.sleep(10)  # Clicks F6, waits 10 seconds
            print("Clicked F6 - end")
            pyautogui.press('f6') # Clicks F6 again
            print("Waiting 5 seconds before next cycle...")
            time.sleep(5)  # Waits 5 seconds before the next cycle starts
        time.sleep(0.1) # Small delay when not clicking to prevent high CPU usage

def toggle_clicker():
    """
    Toggles the 'clicking' flag and updates the GUI label.
    """
    global clicking
    clicking = not clicking
    print("Auto clicker started" if clicking else "Auto clicker stopped")
    if root and hasattr(root, 'label'): # Ensure the label exists before updating
        update_label()

def update_label():
    """
    Updates the text and color of the Tkinter label based on the 'clicking' status.
    This function is called periodically by Tkinter's after method.
    """
    if root and hasattr(root, 'label'):
        status = "Running" if clicking else "Stopped"
        color = "lime" if clicking else "red"
        root.label.config(text=status, fg=color)
        root.after(500, update_label) # Schedule itself to run again after 500ms

def setup_gui():
    """
    Sets up the Tkinter GUI window, including its appearance,
    label, and hotkey binding.
    """
    global root
    root = tk.Tk()
    root.overrideredirect(True) # Removes window decorations (title bar, borders)
    root.attributes("-topmost", True) # Keeps the window on top of others
    root.attributes("-alpha", 0.8) # Sets window transparency
    root.configure(bg='black') # Sets background color to black

    # Create and pack the status label
    root.label = tk.Label(root, text="Stopped", fg="red", bg="black", font=("Arial", 14, "bold"))
    root.label.pack(padx=10, pady=5)

    # Position the window in the top-right corner of the screen
    screen_width = root.winfo_screenwidth()
    root.geometry(f"+{screen_width - 150}+50")

    # Start the clicker thread when the GUI is set up
    threading.Thread(target=clicker, daemon=True).start()

    # Bind F9 to toggle the clicker
    keyboard.add_hotkey('f9', toggle_clicker)
    print("Press F9 to start/stop the auto clicker. Press ESC to exit.")

    # Periodically check for the ESC key press to exit the application
    def check_esc():
        if keyboard.is_pressed('esc'):
            if root:
                root.destroy()
            return
        root.after(100, check_esc)

    root.after(100, check_esc) # Start checking for ESC key

    root.after(0, update_label) # Start updating the label immediately

    root.mainloop() # Start the Tkinter event loop

# --- System Tray Icon Functions ---

def exit_application(icon, item):
    """Exits the application from the system tray menu."""
    icon.stop() # Stop the tray icon
    if root:
        root.quit() # Properly quit the Tkinter main loop

def show_window(icon, item):
    """Shows the Tkinter window when selected from the system tray menu."""
    if root:
        root.deiconify() # Restore the window if it was minimized/hidden

def hide_window(icon, item):
    """Hides the Tkinter window to the system tray."""
    if root:
        root.withdraw() # Hide the window without destroying it

def on_tray_icon_click(icon, item):
    """Handles clicks on the system tray menu items."""
    if str(item) == "Toggle Clicker":
        toggle_clicker()
    elif str(item) == "Show Window":
        show_window(icon, item)
    elif str(item) == "Hide Window":
        hide_window(icon, item)
    elif str(item) == "Exit":
        exit_application(icon, item)

if __name__ == "__main__":
    # Create a simple red image for the tray icon
    image = Image.new('RGB', (64, 64), color = 'red')

    # Define the system tray menu items
    menu = (
        pystray.MenuItem("Toggle Clicker", on_tray_icon_click),
        pystray.MenuItem("Show Window", show_window),
        pystray.MenuItem("Hide Window", hide_window),
        pystray.Menu.SEPARATOR, # Adds a separator line
        pystray.MenuItem("Exit", exit_application)
    )

    # Create and run the system tray icon in a separate thread
    icon = pystray.Icon("my_clicker", image, "Auto Clicker", menu)

    # Start the GUI in a separate thread so it doesn't block the tray icon
    threading.Thread(target=setup_gui, daemon=True).start()

    # Run the system tray icon (this will block until the icon is stopped)
    icon.run()