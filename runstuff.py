import tkinter as tk
import subprocess
import random
import os

import threading, time
from tkinter import ttk

def run_script():
    """
    Function to run the convert.py script.
    It constructs the full path from a base path and the relative path input by the user,
    and then executes the script using subprocess.
    """
    # Disable the entry widgets and button while running the script
    entry1.configure(state="disabled")
    entry2.configure(state="disabled")
    run_button.configure(state="disabled")

    # Start the spinner
    start_spinner()

   # Retrieve the relative path entered by the user in the entry widget
    relative_path = entry1.get()
    relative_path = relative_path.replace("/", "\\")
    if not relative_path.endswith(".md"):
        relative_path += ".md"

    # Retrieve the path context entered by the user in the entry widget
    base_path = entry2.get()

    # Create a function to run the script in a separate thread
    def run_convert_script():
        subprocess.run(["python", "C:\\...\\testvault\\.llmjsons\\scripts\\convert.py", relative_path, base_path])

        # Re-enable the entry widgets and button after the script is done
        entry1.configure(state="normal")
        entry2.configure(state="normal")
        run_button.configure(state="normal")

        # Stop the spinner
        stop_spinner()

    # Start the script in a separate thread
    script_thread = threading.Thread(target=run_convert_script)
    script_thread.start()

def start_spinner():
    def animate_spinner():
        symbol_set = "⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿"
        while spinning:
            num = 12
            left_symbols = [symbol_set[random.randint(0, len(symbol_set) - 1)] for _ in range(num)]
            right_symbols = [symbol_set[random.randint(0, len(symbol_set) - 1)] for _ in range(num)]
            label_str = "".join(left_symbols) + " 🤖 " + "".join(right_symbols)
            spinner_label.configure(text=label_str, font="SegoeUIEmoji")
            time.sleep(0.1)

    global spinning
    spinning = True
    spinner_thread = threading.Thread(target=animate_spinner)
    spinner_thread.start()

def stop_spinner():
    global spinning
    spinning = False
    spinner_label.configure(text="")

def on_enter(event):
    run_script()

def exit_app():
    os._exit(0)  # Forcefully exit the application

# Initialize the main window for the application
root = tk.Tk()
root.title("Run Convert Script")

# Make the window always stay on top
root.attributes('-topmost', True)

# Disable window resizing
root.resizable(False, False)

# Remove minimize and maximize buttons (title bar)
root.overrideredirect(True)

# Create a frame to hold the label and entry widgets
frame1 = tk.Frame(root)
frame1.pack(padx=5, pady=5)
frame2 = tk.Frame(root)
frame2.pack(padx=5, pady=5)

# Set a fixed size for the window (width x height)
xpos = 250 #1280 - 162
ypos = 250 #720 - 65
root.geometry(f"324x130+{xpos}+{ypos}")  # Adjust the width and height as needed

# Disable window resizing (both horizontally and vertically)
root.resizable(False, False)

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# Create a "Run" button
run_button = tk.Button(button_frame, text="Run", command=run_script)
run_button.pack(side="left", padx=5)

# Create an "Exit" button
exit_button = tk.Button(button_frame, text="Exit", command=exit_app)
exit_button.pack(side="left", padx=5)

# Create and pack a label for the relative path entry widget
label1 = tk.Label(frame1, text="Note path:")
label1.pack(side=tk.LEFT)

# Create and pack an entry widget for inputting the relative file path
entry1 = tk.Entry(frame1, width=45)
entry1.pack(side=tk.LEFT)
entry1.bind('<Return>', on_enter)  # Bind Enter key to run_script function

# Create and pack a label for the path context entry widget
label2 = tk.Label(frame2, text="Path Context:")
label2.pack(side=tk.LEFT)

# Create and pack an entry widget for inputting the file path context
entry2 = tk.Entry(frame2, width=40)
entry2.pack(side=tk.LEFT)
entry2.insert(0, "C:\\...\\testvault\\") # Default text on start
entry2.bind('<Return>', on_enter)  # Bind Enter key to run_script function

# Create a label for the spinner
spinner_label = ttk.Label(root, text="", font=("Helvetica", 12))
spinner_label.pack(pady=5)

# Initialize the spinner state
spinning = False

# Function to handle mouse press event
def on_mouse_press(event):
    global mouse_x, mouse_y, dragging
    mouse_x, mouse_y = event.x, event.y
    dragging = True

# Function to handle mouse release event
def on_mouse_release(event):
    global dragging
    dragging = False

# Function to handle mouse motion (dragging) event
def on_mouse_motion(event):
    if dragging:
        x, y = event.x_root - mouse_x, event.y_root - mouse_y
        root.geometry(f"+{x}+{y}")

# Bind mouse events to their respective handlers
root.bind("<ButtonPress-1>", on_mouse_press)
root.bind("<ButtonRelease-1>", on_mouse_release)
root.bind("<B1-Motion>", on_mouse_motion)

# Start the Tkinter event loop to keep the window open and responsive
root.mainloop()
