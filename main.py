import tkinter as tk
import random
import time

class CounterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Blinking Timer")
        
        self.counter = 0
        self.timer_interval = 0
        self.timer_id = None
        self.running = False
        self.paused = False
        
        self.counter_label = tk.Label(self.master, text="Contador: 0")
        self.counter_label.grid(row=0, column=0, pady=10)

        self.timer_label = tk.Label(self.master, text="Tempo restante: -")
        self.timer_label.grid(row=1, column=0, pady=10)

        self.canvas = tk.Canvas(self.master, width=400, height=300)
        self.canvas.grid(row=2, column=0, pady=10)
        self.canvas.bind("<Configure>", self.center_circle)  # Chamar center_circle quando o tamanho da tela mudar
        self.circle = self.canvas.create_oval(10, 10, 90, 90, 
                                              fill="red", state="hidden")

        self.start_button = tk.Button(self.master, text="Iniciar", 
                                      command=self.start_process)
        self.start_button.grid(row=3, column=0, pady=10)

        self.pause_button = tk.Button(self.master, text="Pausar", 
                                      command=self.pause_process, state="disabled")
        self.pause_button.grid(row=4, column=0, pady=10)

        self.restart_button = tk.Button(self.master, text="Reiniciar", 
                                        command=self.restart_process, state="disabled")
        self.restart_button.grid(row=5, column=0, pady=10)

        self.stop_button = tk.Button(self.master, text="Parar", 
                                     command=self.stop_process, state="disabled")
        self.stop_button.grid(row=6, column=0, pady=10)

    def center_circle(self, event=None):
        # Obter as dimensões do canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        # Calcular as coordenadas para centralizar o círculo
        x0 = (canvas_width - 100) / 2
        y0 = (canvas_height - 100) / 2
        x1 = x0 + 100
        y1 = y0 + 100
        # Atualizar as coordenadas do círculo
        self.canvas.coords(self.circle, x0, y0, x1, y1)
        
    def start_process(self):
        self.counter = 0
        self.update_counter_label()
        self.canvas.itemconfig(self.circle, state="hidden") 
        self.running = True
        self.update_button_state("disabled","normal","normal","normal")
        self.schedule_counter_increment()
    
    def pause_process(self):
        if self.running and not self.paused:
            self.master.after_cancel(self.timer_id)
            self.paused_time = time.time()
            self.update_time = self.paused_time - self.executing_timer
            #print(self.update_time)
            self.paused = True
            self.pause_button.config(text="Continuar")
        else:
            self.pause_button.config(text="Pausar")
            #self.timer_interval = self.update_time
            self.schedule_counter_increment()
            self.paused = False
    
    def restart_process(self):
        self.master.after_cancel(self.timer_id)
        self.counter = 0
        self.update_counter_label()
        self.timer_label.config(text="Tempo restante: -")
        self.schedule_counter_increment()
    
    def stop_process(self):
        self.master.after_cancel(self.timer_id)
        self.running = False
        self.update_button_state("normal","disabled","disabled","disabled")

    def increment_counter(self):
        self.counter += 1
        self.update_counter_label()
        self.flash_circle()
        self.schedule_counter_increment()

    def update_counter_label(self):
        self.counter_label.config(text=f"Contador: {self.counter}")

    def flash_circle(self):
        self.canvas.itemconfig(self.circle, state="normal")
        self.master.after(300, self.hide_circle)

    def hide_circle(self):
        self.canvas.itemconfig(self.circle, state="hidden")
    
    def schedule_counter_increment(self):
        if self.running and self.counter < 25:
            self.executing_timer = time.time()
            if not self.paused:
                self.timer_interval = random.randint(5, 10)
            self.timer_label.config(text=f"Tempo restante: {self.timer_interval} segundos")
            self.timer_id = self.master.after(self.timer_interval * 1000, self.increment_counter)
        else:
            self.update_button_state("normal","disabled","disabled","disabled")
    
    def update_button_state(self, start, pause, restart, stop):
        self.start_button.config(state=start)
        self.pause_button.config(state=pause)
        self.restart_button.config(state=restart)
        self.stop_button.config(state=stop)

root = tk.Tk()
app = CounterApp(root)
root.mainloop()