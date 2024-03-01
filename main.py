import tkinter as tk
import random

class CounterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Blinking Timer")

        # Centralizar os elementos vertical e horizontalmente
        window_width = 400
        window_height = 300
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        self.counter = 0
        self.timer_interval = 0
        self.timer_id = None
        self.running = False
        
        self.counter_label = tk.Label(self.master, text="Contador: 0")
        self.counter_label.pack(anchor="center")

        self.timer_label = tk.Label(self.master, text="Tempo restante: -")
        self.timer_label.pack(anchor="center")

        self.canvas = tk.Canvas(self.master, width=window_width, height=window_height)
        self.canvas.pack(anchor="center")
        self.circle = self.canvas.create_oval(10, 10, 90, 90, fill="red", state="hidden")

        self.start_button = tk.Button(self.master, text="Iniciar", command=self.start_process)
        self.start_button.pack(anchor="center")

        self.pause_button = tk.Button(self.master, text="Pausar", command=self.pause_process, state="disabled")
        self.pause_button.pack(anchor="center")

        self.resume_button = tk.Button(self.master, text="Retomar", command=self.resume_process, state="disabled")
        self.resume_button.pack(anchor="center")

        self.restart_button = tk.Button(self.master, text="Reiniciar", command=self.restart_process, state="disabled")
        self.restart_button.pack(anchor="center")

        self.stop_button = tk.Button(self.master, text="Parar", command=self.stop_process, state="disabled")
        self.stop_button.pack(anchor="center")

    def start_process(self):
        if not self.running:
            self.counter = 0
            self.update_counter_label()
            self.canvas.itemconfig(self.circle, state="hidden") 
            self.running = True
            self.start_button.config(state="disabled")
            self.restart_button.config(state="normal")
            self.stop_button.config(state="normal")
            self.schedule_counter_increment()

    def pause_process(self):
        if self.running:
            self.start_button.config(state="disable")
            self.pause_button.config(state="disable")
            self.resume_button.config(state="normal")
            self.restart_button.config(state="normal")
            self.stop_button.config(state="normal")
    
    def resume_process(self):
        if self.running:
            self.start_button.config(state="disable")
            self.pause_button.config(state="normal")
            self.resume_button.config(state="disable")
            self.restart_button.config(state="normal")
            self.stop_button.config(state="normal")
    
    def restart_process(self):
        if self.running:
            self.master.after_cancel(self.timer_id)
            self.counter = 0
            self.update_counter_label()
            self.timer_label.config(text="Tempo restante: -")
            self.schedule_counter_increment()
    
    def stop_process(self):
        if self.running:
            self.master.after_cancel(self.timer_id)
            self.running = False
            self.start_button.config(state="normal")
            self.restart_button.config(state="disabled")
            self.stop_button.config(state="disabled")

    def schedule_counter_increment(self):
        if self.running and self.counter < 25:
            self.timer_interval = random.randint(5, 10)
            self.timer_label.config(text=f"Tempo restante: {self.timer_interval} segundos")
            self.timer_id = self.master.after(self.timer_interval * 1000, self.increment_counter)
        else:
            self.running = False
            self.start_button.config(state="normal")
            self.restart_button.config(state="disabled")
            self.stop_button.config(state="disabled")

    def increment_counter(self):
        if self.running and self.counter < 25:
            self.counter += 1
            self.update_counter_label()
            self.flash_circle()
            self.schedule_counter_increment()

    def update_counter_label(self):
        self.counter_label.config(text=f"Contador: {self.counter}")

    def flash_circle(self):
        if self.running:
            self.canvas.itemconfig(self.circle, state="normal")
            self.master.after(3000, self.hide_circle)

    def hide_circle(self):
        if self.running:
            self.canvas.itemconfig(self.circle, state="hidden")

root = tk.Tk()
app = CounterApp(root)
root.mainloop()