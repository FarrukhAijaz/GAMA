import tkinter as tk
from tkinter import Canvas, Entry, OptionMenu, StringVar, messagebox
from PIL import Image, ImageTk
from GUI.helper import blur_image
from GUI.helper import create_rounded_rectangle


class DynamicInputPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(width=800, height=600)
        num_sc = 3
        num_unit = 4
        io_incl = 0
        #io_incl = random.randint(0,1)
        def InitaliseFrame():
            self.bg_image = Image.open("/home/saijaz/Desktop/GAMA/GAMA/assets/images/bg.png")
            self.bg_image = self.bg_image.resize((800, 600), Image.ANTIALIAS)
            self.bg_photo = ImageTk.PhotoImage(blur_image(self.bg_image, 1))

            self.canvas = Canvas(self, width=800, height=600, bg="white", bd=0, highlightthickness=0)
            self.canvas.place(x=0, y=0)

            self.canvas.create_image(400, 0, image=self.bg_photo, anchor="nw")

            label_text = "Next Step! Providing Information"
            label_font = ("Times New Roman", 14, "bold italic")
            self.canvas.create_text(148, 20, text=label_text, font=label_font, fill="#000FFF", anchor="center")

            label_text = f"You have selected to create {num_sc} subcomponents and {num_unit} units." 
            label_font = ("Times New Roman", 10, "italic")
            self.canvas.create_text(175, 40, text=label_text, font=label_font, fill="#0036FF")

            if io_incl == 1:
                label_text = "You have also opted to include I/O ports and would like to"
                label_font = ("Times New Roman", 10, "italic")
                self.canvas.create_text(178, 55, text=label_text, font=label_font, fill="#0036FF")

                label_text = "define their names"
                label_font = ("Times New Roman", 10, "italic")
                self.canvas.create_text(70, 70, text=label_text, font=label_font, fill="#0036FF")
            else: 
                label_text = "You have also opted to not include I/O ports and would like"
                label_font = ("Times New Roman", 10, "italic")
                self.canvas.create_text(181, 55, text=label_text, font=label_font, fill="red")

                label_text = "to not define their names"
                label_font = ("Times New Roman", 10, "italic")
                self.canvas.create_text(90, 70, text=label_text, font=label_font, fill="red")

                    

            # label_text = "You have selected to create {num_sc} subcomponents"
            # label_font = ("Times New Roman", 10, "italic")
            # self.canvas.create_text(150, 40, text=label_text, font=label_font, fill="#0036FF")

            # label_text = "You have selected to create {num_sc} subcomponents"
            # label_font = ("Times New Roman", 10, "italic")
            # self.canvas.create_text(150, 40, text=label_text, font=label_font, fill="#0036FF")

            # label_text = "Please fill in the following:"
            # label_font = ("Times New Roman", 12, "bold italic")
            # self.canvas.create_text(100, 80, text=label_text, font=label_font, fill="#17202A")

        InitaliseFrame()
        # InitialiseRadioButtonSet1()
        # InitialiseRadioButtonSet2()
        # create_swc_name_input()
        # create_subcomponents_question()
        # create_units_question()
        # Question1()
        # Question2()
        # NextButton()
        # PrevButton()    
