import tkinter as tk
import obd

class UserInterface:
    def __init__(self, data_connector, live_data):
        self.data_connector = data_connector
        self.live_data = live_data

        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.setup_ui()

    def start_ui(self):
        self.window.mainloop()

    def setup_ui(self):
        self.add_widget(obd.commands.SPEED.name, 'Speed', 0, 0)
        self.add_widget(obd.commands.RPM.name, 'RPM', 0, 1)
        self.add_widget(obd.commands.COOLANT_TEMP.name, 'Coolant Temp', 0, 2)
        self.add_widget(obd.commands.INTAKE_TEMP.name, 'Intake Temp', 1, 0)
        self.add_widget(obd.commands.FUEL_LEVEL.name, 'Fuel Level', 1, 1)
        self.add_widget(obd.commands.ENGINE_LOAD.name, 'Engine Load', 1, 2)

        col_count, row_count = self.window.grid_size()

        for col in range(col_count):
            self.window.grid_columnconfigure(col, minsize=200)

        for row in range(row_count):
            self.window.grid_rowconfigure(row, minsize=200)

        self.window.configure(background='#002B36')

    def add_widget(self, data_key, data_name, row, col):
        frame = tk.Frame(bg='#002B36')

        thing = tk.Label(frame, text=data_name, bg='#002B36', fg='#FFF', font=("Arial", 20))
        thing.pack()

        var = tk.StringVar()
        label = tk.Label(frame, textvariable=var, bg='#002B36', fg='#746A31', font=("Arial", 25))
        label.pack()
        self.update_widget(label, var, data_key, data_name)

        frame.grid(row=row, column=col)

    def close(self):
        self.window.destroy()
        self.data_connector.stop()

    def update_widget(self, label, var, data_key, data_name):
        var.set(str(self.live_data[data_key]))
        label.after(100, self.update_widget, label, var, data_key, data_name)