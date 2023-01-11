import tkinter as tk
from tkinter.messagebox import YES
import obd

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class TabbedUserInterface:
    background_colour = '#FFFFFF'
    label_color = '#000000'
    value_color = '#000000'

    frames = []
    current_frame = 0

    def __init__(self, data_connector, live_data):
        self.data_connector = data_connector
        self.live_data = live_data

        self.window = tk.Tk()
        #self.window.geometry("480x320")
        self.window.attributes('-fullscreen', True)
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.setup_ui()

    def start_ui(self):
        self.window.mainloop()

    def setup_ui(self):
        self.window.configure(background=self.background_colour)
        self.frame_container = tk.Frame(bg=self.background_colour)
        self.frame_container.pack(side=tk.TOP, fill=tk.BOTH, expand=YES)

        self.add_frame(obd.commands.SPEED.name, 'Speed', 'km/h')
        self.add_frame(obd.commands.RPM.name, 'RPM', None)
        self.add_frame(obd.commands.COOLANT_TEMP.name, 'Coolant', '°C')
        self.add_frame(obd.commands.INTAKE_TEMP.name, 'Intake', '°C')
        self.add_frame(obd.commands.FUEL_LEVEL.name, 'Fuel', '%')
        self.add_frame(obd.commands.ENGINE_LOAD.name, 'Load', '%')

        self.frames[0].lift()

    def add_frame(self, data_key, data_name, data_unit):
        frame = tk.Frame(self.frame_container, bg=self.background_colour)

        title_label = tk.Label(frame, text=data_name, bg=self.background_colour, fg=self.label_color, font=("Arial", 30))
        title_label.place(relx=0.5, rely=0.22, anchor=tk.CENTER)
        title_label.bind("<Button-1>", self.increment_frame)

        var = tk.StringVar()
        value_label = tk.Label(frame, textvariable=var, bg=self.background_colour, fg=self.value_color, font=("Arial", 60))
        value_label.place(relx=0.5, rely=0.58, anchor=tk.CENTER)
        value_label.bind("<Button-1>", self.increment_frame)
        self.update_widget(value_label, var, data_key, data_name, data_unit)

        frame.place(relheight=1, relwidth=1)
        frame.bind("<Button-1>", self.increment_frame)
        self.frames.append(frame)

    def update_widget(self, label, var, data_key, data_name, data_unit):
        widget_text = f'{str(self.live_data[data_key])} {data_unit if data_unit is not None else ""}'

        var.set(widget_text)

        label.after(100, self.update_widget, label, var, data_key, data_name, data_unit)

    def increment_frame(self, event):
        self.current_frame = 0 if self.current_frame == len(self.frames)-1 else self.current_frame + 1

        self.frames[self.current_frame].lift()

    def close(self):
        self.window.destroy()
        self.data_connector.stop()