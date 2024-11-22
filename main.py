import psutil
import os
import ctypes
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

NVML_AVAILABLE = False

try:
    import pynvml
    nvml_path = os.path.join(os.getenv("ProgramFiles", "C:/Program Files"), "NVIDIA Corporation/NVSMI/nvml.dll")
    if os.path.exists(nvml_path):
        ctypes.CDLL(nvml_path)
        pynvml.nvmlInit()
        NVML_AVAILABLE = True
except ImportError:
    pass

def get_cpu_info():
    return psutil.cpu_percent(interval=0.1)

def get_memory_info():
    return psutil.virtual_memory().percent

def get_disk_info():
    return psutil.disk_usage('/').percent

def get_gpu_info():
    if not NVML_AVAILABLE:
        return 0  # Default to 0 if no GPU is detected
    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Use the first GPU
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        return utilization.gpu
    except:
        return 0

class TaskManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Real-Time System Monitor")
        self.geometry("900x800")
        self.configure(bg='#2b2b2b')

        # CPU Usage Chart
        self.cpu_fig, self.cpu_ax = plt.subplots(figsize=(5, 2))
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, self)
        self.cpu_canvas.get_tk_widget().pack(fill="both", expand=True)
        self.cpu_usage_data = [0] * 60

        # Memory Usage Chart
        self.memory_fig, self.memory_ax = plt.subplots(figsize=(5, 2))
        self.memory_canvas = FigureCanvasTkAgg(self.memory_fig, self)
        self.memory_canvas.get_tk_widget().pack(fill="both", expand=True)
        self.memory_usage_data = [0] * 60

        # GPU Usage Chart
        self.gpu_fig, self.gpu_ax = plt.subplots(figsize=(5, 2))
        self.gpu_canvas = FigureCanvasTkAgg(self.gpu_fig, self)
        self.gpu_canvas.get_tk_widget().pack(fill="both", expand=True)
        self.gpu_usage_data = [0] * 60

        # Disk Usage Chart
        self.disk_fig, self.disk_ax = plt.subplots(figsize=(5, 2))
        self.disk_canvas = FigureCanvasTkAgg(self.disk_fig, self)
        self.disk_canvas.get_tk_widget().pack(fill="both", expand=True)
        self.disk_usage_data = [0] * 60

        self.update_info()

    def update_info(self):
        # Update CPU Usage Chart
        self.cpu_usage_data.append(get_cpu_info())
        self.cpu_usage_data = self.cpu_usage_data[-60:]
        self.cpu_ax.clear()
        self.cpu_ax.plot(self.cpu_usage_data, color="cyan")
        self.cpu_ax.set_title("CPU Usage (%)", color="white")
        self.cpu_ax.set_facecolor("#2b2b2b")
        self.cpu_fig.patch.set_facecolor('#2b2b2b')
        self.cpu_ax.tick_params(axis='x', colors='white')
        self.cpu_ax.tick_params(axis='y', colors='white')
        self.cpu_canvas.draw()

        # Update Memory Usage Chart
        self.memory_usage_data.append(get_memory_info())
        self.memory_usage_data = self.memory_usage_data[-60:]
        self.memory_ax.clear()
        self.memory_ax.plot(self.memory_usage_data, color="green")
        self.memory_ax.set_title("Memory Usage (%)", color="white")
        self.memory_ax.set_facecolor("#2b2b2b")
        self.memory_fig.patch.set_facecolor('#2b2b2b')
        self.memory_ax.tick_params(axis='x', colors='white')
        self.memory_ax.tick_params(axis='y', colors='white')
        self.memory_canvas.draw()

        # Update GPU Usage Chart
        self.gpu_usage_data.append(get_gpu_info())
        self.gpu_usage_data = self.gpu_usage_data[-60:]
        self.gpu_ax.clear()
        self.gpu_ax.plot(self.gpu_usage_data, color="magenta")
        self.gpu_ax.set_title("GPU Usage (%)", color="white")
        self.gpu_ax.set_facecolor("#2b2b2b")
        self.gpu_fig.patch.set_facecolor('#2b2b2b')
        self.gpu_ax.tick_params(axis='x', colors='white')
        self.gpu_ax.tick_params(axis='y', colors='white')
        self.gpu_canvas.draw()

        # Update Disk Usage Chart
        self.disk_usage_data.append(get_disk_info())
        self.disk_usage_data = self.disk_usage_data[-60:]
        self.disk_ax.clear()
        self.disk_ax.plot(self.disk_usage_data, color="orange")
        self.disk_ax.set_title("Disk Usage (%)", color="white")
        self.disk_ax.set_facecolor("#2b2b2b")
        self.disk_fig.patch.set_facecolor('#2b2b2b')
        self.disk_ax.tick_params(axis='x', colors='white')
        self.disk_ax.tick_params(axis='y', colors='white')
        self.disk_canvas.draw()

        self.after(1000, self.update_info)

if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()
