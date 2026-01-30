import tkinter as tk
from intro import IntroPage
from swc_setup import SWCSetupPage
from dynamic_input import DynamicInputPage
from config_swc import ConfigPage
from confirmation import ConfirmationPage

class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title("SMG-F1")
        
        # Lock window size to 800x600
        self.root.geometry("800x600")
        self.root.resizable(False, False)  # Disable resizing
        
        # Set window icon (use PNG file with iconphoto)
        self.root.iconphoto(False, tk.PhotoImage(file='/home/saijaz/Desktop/GAMA/GAMA/assets/icons/ico.png'))  # Replace with your PNG icon path

        self.frames = {}

        container = tk.Frame(root)
        container.pack(fill="both", expand=True)

        for F in (IntroPage, SWCSetupPage, DynamicInputPage, ConfigPage, ConfirmationPage):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(IntroPage)

    def show_frame(self, page_class):
        """Switch to the given frame by class reference."""
        if page_class not in self.frames:
            print(f"Error: {page_class} not found in self.frames")  # Debugging
        else:
            frame = self.frames[page_class]
            frame.tkraise()
