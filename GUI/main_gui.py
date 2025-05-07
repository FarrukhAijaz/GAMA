import tkinter as tk
from GUI.intro import IntroPage
from GUI.swc_setup import SWCSetupPage
from GUI.dynamic_input import DynamicInputPage
from GUI.config_swc import ConfigPage
from GUI.confirmation import ConfirmationPage
from GUI.xml_output import  XmlData
from GUI.xml_preview import  XmlPreview

class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title("SMG-F1")

        # Lock window size to 800x600
        self.root.geometry("800x600")
        self.root.resizable(False, False)  # Disable resizing

        # Set window icon
        self.root.iconphoto(False, tk.PhotoImage(file='/home/saijaz/Desktop/GAMA/GAMA/assets/icons/ico.png'))

        self.frames = {}

        container = tk.Frame(root)
        container.pack(fill="both", expand=True)

        # Store frames with their class names as strings
        for F in (IntroPage, SWCSetupPage, DynamicInputPage, ConfigPage, ConfirmationPage, XmlData, XmlPreview):
            page_name = F.__name__  # Get class name as string
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame  # Store by name
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("IntroPage")  # Use string instead of class reference

    def show_frame(self, page_name):
        """Switch to the given frame using its class name as a string."""
        if page_name not in self.frames:
            print(f"Error: {page_name} not found in self.frames")
        else:
            frame = self.frames[page_name]
            frame.tkraise()
            # If the frame has a 'start' method, call it (used for XmlData or other animated pages)
            if hasattr(frame, 'start'):
                frame.start()
