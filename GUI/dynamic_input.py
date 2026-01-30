import tkinter as tk
from tkinter import ttk
from config_swc import ConfigPage


class DynamicInputPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Number of Subcomponents:").grid(row=0, column=0)
        self.combo_subcomponents = ttk.Combobox(self, values=[1, 2, 3, 4, 5], state="readonly")
        self.combo_subcomponents.grid(row=0, column=1)
        self.combo_subcomponents.bind("<<ComboboxSelected>>", self.update_dynamic_fields)

        self.dynamic_frame = tk.Frame(self)
        self.dynamic_frame.grid(row=2, column=0, columnspan=2)

        tk.Button(self, text="Next", command=lambda: controller.show_frame(ConfigPage)).grid(row=3, column=0, columnspan=2, pady=10)

    def update_dynamic_fields(self, event):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        num_subcomponents = int(self.combo_subcomponents.get())
        for i in range(num_subcomponents):
            tk.Label(self.dynamic_frame, text=f"Subcomponent {i + 1}:").grid(row=i, column=0)
            tk.Entry(self.dynamic_frame).grid(row=i, column=1)
