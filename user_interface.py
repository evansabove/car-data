import tkinter as tk
import obd

class UserInterface:
    background_colour = '#FFFFFF'
    label_color = '#000000'
    value_color = '#000000'

    def __init__(self, data_connector, live_data):
        self.data_connector = data_connector
        self.live_data = live_data

        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.setup_ui()

    def start_ui(self):
        self.window.mainloop()

    def setup_ui(self):
        self.add_widget(obd.commands.SPEED.name, 'Speed', 'km/h', 0, 0)
        self.add_widget(obd.commands.RPM.name, 'RPM', None, 0, 1)
        self.add_widget(obd.commands.COOLANT_TEMP.name, 'Coolant', '°C', 0, 2)
        self.add_widget(obd.commands.INTAKE_TEMP.name, 'Intake', '°C', 1, 0)
        self.add_widget(obd.commands.FUEL_LEVEL.name, 'Fuel', '%', 1, 1)
        self.add_widget(obd.commands.ENGINE_LOAD.name, 'Load', '%', 1, 2)

        col_count, row_count = self.window.grid_size()

        for col in range(col_count):
            self.window.grid_columnconfigure(col, minsize=150, weight=1)

        for row in range(row_count):
            self.window.grid_rowconfigure(row, minsize=150, weight=1)

        self.window.configure(background=self.background_colour)

    def add_widget(self, data_key, data_name, data_unit, row, col):
        frame = tk.Frame(bg=self.background_colour)

        title_label = tk.Label(frame, text=data_name, bg=self.background_colour, fg=self.label_color, font=("Arial", 20))
        title_label.pack()

        var = tk.StringVar()
        value_label = tk.Label(frame, textvariable=var, bg=self.background_colour, fg=self.value_color, font=("Arial", 25))
        value_label.pack()
        self.update_widget(value_label, var, data_key, data_name, data_unit)

        frame.grid(row=row, column=col)

    def close(self):
        self.window.destroy()
        self.data_connector.stop()

    def update_widget(self, label, var, data_key, data_name, data_unit):
        widget_text = f'{str(self.live_data[data_key])} {data_unit if data_unit is not None else ""}'

        var.set(widget_text)

        label.after(100, self.update_widget, label, var, data_key, data_name, data_unit)