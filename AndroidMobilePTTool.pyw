import os
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import requests
import zipfile
import io

def download_and_extract_tools():
    url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
    try:
        response = requests.get(url)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall()
        platform_tools_path = os.path.join(os.getcwd(), "platform-tools")
        if os.path.exists(platform_tools_path):
            os.environ["PATH"] += os.pathsep + platform_tools_path
            messagebox.showinfo("Success", f"Platform tools downloaded and set up successfully!\nPath set: {platform_tools_path}")
        else:
            messagebox.showerror("Error", "Failed to locate platform-tools folder.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download tools: {e}")

def detect_devices():
    try:
        result = subprocess.check_output(["adb", "devices"], universal_newlines=True)
        devices = [line.split("\t")[0] for line in result.splitlines() if "\tdevice" in line]
        device_dropdown["values"] = devices
        if devices:
            device_dropdown.current(0)
            messagebox.showinfo("Success", "Devices detected.")
        else:
            messagebox.showwarning("Warning", "No devices detected.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to detect devices: {e}")

def run_adb_command():
    device = device_dropdown.get()
    command = command_dropdown.get()
    arguments = args_entry.get()
    if not command:
        messagebox.showerror("Error", "Please select a command.")
        return
    try:
        cmd = ["adb"]
        if device:
            cmd += ["-s", device]
        cmd += command.split() + arguments.split()
        result = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)
    except subprocess.CalledProcessError as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, e.output)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run command: {e}")

def load_commands():
    try:
        with open("adbcommand.txt", "r") as file:
            commands = [line.strip() for line in file if line.strip()]
        command_dropdown["values"] = commands
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load commands: {e}")

def show_about():
    about_message = (
        "ADB GUI Tool\n"
        "Version: 1.0\n"
        "Author: Your Name\n"
        "This tool provides a graphical interface for managing ADB commands and devices."
    )
    messagebox.showinfo("About Us", about_message)

# GUI Setup
root = tk.Tk()
root.title("ADB GUI Tool")
root.geometry("600x400")

# Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

config_menu = tk.Menu(menu_bar, tearoff=0)
config_menu.add_command(label="Set up Platform Tools", command=download_and_extract_tools)
menu_bar.add_cascade(label="Config", menu=config_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About Us", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

frame = tk.Frame(root)
frame.pack(pady=10)

# Device Detection Row
device_frame = tk.Frame(frame)
device_frame.grid(row=0, column=0, columnspan=2, pady=5)

device_label = tk.Label(device_frame, text="Select Device:")
device_label.pack(side=tk.LEFT, padx=5)

device_dropdown = ttk.Combobox(device_frame, state="readonly")
device_dropdown.pack(side=tk.LEFT, padx=5)

btn_detect = tk.Button(device_frame, text="Detect Devices", command=detect_devices)
btn_detect.pack(side=tk.LEFT, padx=5)

# Command Dropdown
command_label = tk.Label(frame, text="Select Command:")
command_label.grid(row=1, column=0, padx=10, pady=5)
command_dropdown = ttk.Combobox(frame, state="readonly")
command_dropdown.grid(row=1, column=1, padx=10, pady=5)

# Load commands from file
load_commands()

# Arguments Entry
args_label = tk.Label(frame, text="Arguments:")
args_label.grid(row=2, column=0, padx=10, pady=5)
args_entry = tk.Entry(frame, width=40)
args_entry.grid(row=2, column=1, padx=10, pady=5)

# Run Button
btn_run = tk.Button(frame, text="Run Command", command=run_adb_command)
btn_run.grid(row=3, column=0, columnspan=2, pady=10)

# Output Text
output_text = tk.Text(root, height=10, width=70)
output_text.pack(pady=10)

root.mainloop()
