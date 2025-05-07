import tkinter as tk
from tkinter import Frame, Canvas, filedialog, messagebox
from PIL import Image, ImageTk
from GUI.helper import blur_image
from GUI.helper import create_rounded_rectangle

from SWC.parser import parse_swc_file

class XmlPreview(Frame):
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

        def GIF():
            self.gif_frames = []
            gif_path = "/home/saijaz/Desktop/GAMA/GAMA/assets/images/final.gif"
            gif = Image.open(gif_path)

            try:
                while True:
                    frame = ImageTk.PhotoImage(gif.copy())
                    self.gif_frames.append(frame)
                    gif.seek(len(self.gif_frames))
            except EOFError:
                pass

            self.gif_index = 0
            self.gif_image = self.canvas.create_image(0, 150, image=self.gif_frames[0], anchor="nw")

            def animate():
                if hasattr(self, "gif_running") and not self.gif_running:
                    return
                self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
                self.canvas.itemconfig(self.gif_image, image=self.gif_frames[self.gif_index])
                self.after(100, animate)

            # Flag to control animation
            self.gif_running = True
            animate()

            def stop_animation():
                self.gif_running = False
                self.canvas.delete(self.gif_image)
                self.gif_frames.clear()

            self.after(4500, stop_animation)
        self.var = tk.IntVar(value=0)

        def navigate_next(event=None):
            # Proceed to the respective page
            self.controller.show_frame("XmlData")

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
        
        # Function to display and remove text sequentially
        def Text_Animation(self):
        
            def show_text_and_remove(text, position, delay_show, delay_remove):
                label_id = self.canvas.create_text(position[0], position[1], text=text, font=("Times New Roman", 12, "bold italic"), fill="#17202A")
                
                # After delay_show (time in ms), make the text visible
                self.after(delay_show, lambda: self.canvas.itemconfig(label_id, state="normal"))
                
                # After delay_remove (time in ms), remove the text
                self.after(delay_remove, lambda: self.canvas.delete(label_id))

                return label_id
            
            # Show and remove text in sequence
            show_text_and_remove("Parsing the XML ....", (185, 450), 0, 1000)
            self.after(1000, lambda: show_text_and_remove("Extracting the Software Component Information ....", (185, 450), 0, 1500))
            self.after(2500, lambda: show_text_and_remove("Finalizing ....", (185, 450), 0, 2000))
        InitaliseFrame()
        GIF()
        NextButton()
        Text_Animation(self)