import tkinter as tk
from tkinter import Frame, Canvas, filedialog, messagebox
from PIL import Image, ImageTk
from GUI.helper import blur_image
from GUI.helper import create_rounded_rectangle


class XmlData(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(width=800, height=600)
        def InitaliseFrame():
            self.bg_image = Image.open("/home/saijaz/Desktop/GAMA/GAMA/assets/images/bg.png")
            self.bg_image = self.bg_image.resize((800, 600), Image.ANTIALIAS)
            self.bg_photo = ImageTk.PhotoImage(blur_image(self.bg_image, 1))

            self.canvas = Canvas(self, width=800, height=600, bg="white", bd=0, highlightthickness=0)
            self.canvas.place(x=0, y=0)

            self.canvas.create_image(400, 0, image=self.bg_photo, anchor="nw")

            label_text = "Welcome to SMG-F1"
            label_font = ("Times New Roman", 14, "bold italic")
            self.canvas.create_text(90, 20, text=label_text, font=label_font, fill="#000FFF", anchor="center")
            
            label_text = "(Simulink Model Generator - Ford v1.0)"
            label_font = ("Times New Roman", 14, "bold italic")
            self.canvas.create_text(160, 40, text=label_text, font=label_font, fill="#000FFF", anchor="center")

            label_text = "This application is an automation tool for creating Simulink Models"
            label_font = ("Times New Roman", 10, "italic")
            self.canvas.create_text(200, 60, text=label_text, font=label_font, fill="#0036FF")

            label_text = "for Software Components, feel free to use it and share any comments!"
            label_font = ("Times New Roman", 10, "italic")
            self.canvas.create_text(200, 75, text=label_text, font=label_font, fill="#0036FF")

            label_text = "Below you can find the data extracted from the XMl"
            label_font = ("Times New Roman", 12, "bold italic")
            self.canvas.create_text(185, 100, text=label_text, font=label_font, fill="#17202A")

            label_text = "to be used in Simulink Creation:"
            label_font = ("Times New Roman", 12, "bold italic")
            self.canvas.create_text(120, 115, text=label_text, font=label_font, fill="#17202A")

        self.var = tk.IntVar(value=0)
        
        # Button 1 Starts
        def InitialiseRadioButton1():
            label_text = "Generate Software Component in Simulink"
            label_font = ("Times New Roman", 12, "bold")
            self.canvas.create_text(190, 167, text=label_text, font=label_font, fill="#17202A")

            label_text = "using a XML import."
            label_font = ("Times New Roman", 12, "bold")
            self.canvas.create_text(118, 187, text=label_text, font=label_font, fill="#17202A")

            self.circle1 = self.canvas.create_oval(20, 160, 35, 175, fill="#CCD1D1", outline="#0036FF", width=2)
            self.canvas.tag_bind(self.circle1, "<Button-1>", lambda event: toggle_radio_button(1))

            self.inner_circle1 = self.canvas.create_oval(23, 163, 32, 172, fill="#28B463", outline="", state="hidden")

            self.canvas.create_oval(23, 163, 32, 172, fill="green", outline="", state="hidden", tags="inner1")

        # Button 2 Starts
        def InitialiseRadioButton2():
            label_text = "Generate Software Component in Simulink by"
            label_font = ("Times New Roman", 12, "bold")
            self.canvas.create_text(200, 227, text=label_text, font=label_font, fill="#17202A")

            label_text = "manually defining software components/units."
            label_font = ("Times New Roman", 12, "bold")
            self.canvas.create_text(200, 247, text=label_text, font=label_font, fill="#17202A")

            self.circle2 = self.canvas.create_oval(20, 220, 35, 235, fill="#CCD1D1", outline="#0036FF", width=2)
            self.canvas.tag_bind(self.circle2, "<Button-1>", lambda event: toggle_radio_button(2))

            self.inner_circle2 = self.canvas.create_oval(23, 223, 32, 232, fill="#28B463", outline="", state="hidden")

            self.canvas.create_oval(23, 223, 32, 232, fill="green", outline="", state="hidden", tags="inner2")
        

        def toggle_radio_button(selected_value):
            self.var.set(selected_value)

            self.canvas.itemconfig(self.inner_circle1, state="normal" if self.var.get() == 1 else "hidden")
            self.canvas.itemconfig(self.inner_circle2, state="normal" if self.var.get() == 2 else "hidden")

            # Clear previous UI elements before rendering new ones
            clear_previous_widgets()

            if self.var.get() == 1:
                DisplayRadioButton1()

            elif self.var.get() == 2:
                DisplayRadioButton2()


        # Function to clear previous UI elements
        def clear_previous_widgets():
            for widget in self.current_widgets:
                self.canvas.delete(widget)  # Remove previous elements
            self.current_widgets.clear()  # Reset list


        # Function to open directory dialog and update text
        def select_directory(text_id):
            folder_selected = filedialog.askdirectory(title="Select Folder")
            if folder_selected:
                self.canvas.itemconfig(text_id, text=folder_selected, fill="black")


        def DisplayRadioButton1():
            # Labels for text boxes
            label_font = ("Times New Roman", 12, "bold")
            label1 = self.canvas.create_text(80, 300, text="Save Location:", font=label_font, fill="#17202A")
            label2 = self.canvas.create_text(70, 400, text="XML File:", font=label_font, fill="#17202A")

            # Rectangular boxes
            rect1 = create_rounded_rectangle(self.canvas, 90, 325, 360, 355, radius=5, fill="white", outline="black")
            rect2 = create_rounded_rectangle(self.canvas, 90, 425, 360, 455, radius=5, fill="white", outline="black")

            # Text inside boxes
            self.text1_id = self.canvas.create_text(225, 340, text="Click to select directory for Simulink Model", font=("Arial", 10), fill="grey")
            self.text2_id = self.canvas.create_text(220, 440, text="Click to select XML file for Import", font=("Arial", 10), fill="grey")

            # Bind clicks to open dialogs
            self.canvas.tag_bind(rect1, "<Button-1>", lambda event: select_directory(self.text1_id))
            self.canvas.tag_bind(self.text1_id, "<Button-1>", lambda event: select_directory(self.text1_id))

            self.canvas.tag_bind(rect2, "<Button-1>", lambda event: select_directory(self.text2_id))
            self.canvas.tag_bind(self.text2_id, "<Button-1>", lambda event: select_directory(self.text2_id))

            # Store UI elements for removal later
            self.current_widgets.extend([label1, label2, rect1, rect2, self.text1_id, self.text2_id])


        def DisplayRadioButton2():
            # Labels for text boxes
            label_font = ("Times New Roman", 12, "bold")
            label1 = self.canvas.create_text(80, 300, text="Save Location:", font=label_font, fill="#17202A")

            # Rectangular box
            rect1 = create_rounded_rectangle(self.canvas, 90, 325, 360, 355, radius=5, fill="white", outline="black")

            # Text inside box
            self.text1_id = self.canvas.create_text(225, 340, text="Click to select directory for Simulink Model", font=("Arial", 10), fill="grey")

            # Bind clicks to open dialogs
            self.canvas.tag_bind(rect1, "<Button-1>", lambda event: select_directory(self.text1_id))
            self.canvas.tag_bind(self.text1_id, "<Button-1>", lambda event: select_directory(self.text1_id))

            # Store UI elements for removal later
            self.current_widgets.extend([label1, rect1, self.text1_id])

        def navigate_next(event=None):
            try:
                selected_option = self.var.get()

                if selected_option not in [1, 2]:
                    raise ValueError("Please select an option before proceeding.")

                # Get the actual text inside the text boxes
                save_location_text = self.canvas.itemcget(self.text1_id, "text")
                arxml_file_text = self.canvas.itemcget(self.text2_id, "text") if selected_option == 1 else None

                # Default placeholders (greyed-out text when unselected)
                default_save_text = "Click to select directory for Simulink Model"
                default_arxml_text = "Click to select XML file for Import"

                # Check if the required fields are filled
                if save_location_text == default_save_text or not save_location_text.strip():
                    raise ValueError("Please select a Save Location.")

                if selected_option == 1 and (arxml_file_text == default_arxml_text or not arxml_file_text.strip()):
                    raise ValueError("Please select a XML File.")

                # Proceed to the respective page
                if selected_option == 1:
                    self.controller.show_frame("SWCSetupPage")
                elif selected_option == 2:
                    self.controller.show_frame("DynamicInputPage")

            except ValueError as e:
                messagebox.showerror("Input Error", str(e))  # Show error pop-up

        # Hover effects for the 'Next' button
        def on_hover(event):
            self.canvas.itemconfig(self.start_button, fill="#A3E4D7")

        def on_leave(event):
            self.canvas.itemconfig(self.start_button, fill="#F0B27A")

        # Next button definition
        def NextButton():
            self.start_button = create_rounded_rectangle(self.canvas, 300, 550, 380, 580, radius=15, fill="#F0B27A", outline="", width=2)
            self.start_button_text = self.canvas.create_text(335, 565, text="Next", font=("Times New Roman", 14, "bold italic"), fill="#17202A")

            self.canvas.tag_bind(self.start_button, "<Button-1>", navigate_next)
            self.canvas.tag_bind(self.start_button_text, "<Button-1>", navigate_next)
            self.canvas.tag_bind(self.start_button, "<Enter>", on_hover)
            self.canvas.tag_bind(self.start_button_text, "<Enter>", on_hover)
            self.canvas.tag_bind(self.start_button, "<Leave>", on_leave)
            self.canvas.tag_bind(self.start_button_text, "<Leave>", on_leave)

        # Initialize list to track UI elements
        self.current_widgets = []
        InitaliseFrame()
        InitialiseRadioButton1()
        InitialiseRadioButton2()
        NextButton()