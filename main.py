import os
import sys
from tkinter import *
class tkButton(Button): pass # keep access to the normal tk button class, reason is later
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
import requests
import openai
import secrets
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from svglib.svglib import SvgRenderer
import webbrowser
from time import sleep, time
import textwrap
import asyncio

# imports the environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

# set the openai api key
openai.api_key = os.getenv("OPENAI_API_KEY")

def import_image(image_relative_path, size=(24, 24)):
    # this stupid function is here because tkinter is stupid and doesn"t like relative paths for images
    # note: this function breaks if fed svg files. i tried with svglib but it didn"t work.
    #       i don"t know why, i don"t care, and i"m not going to fix it. too bad.
    # also note: all images fed must be square in dimensions or else they will be stretched
    #            this is because i"m too lazy to fix it
    # this is just a terrible function in general but it works well enough so i"m not going to fix it
    script_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    # print(script_dir)
    image_path = script_dir + image_relative_path
    # print(image_relative_path)
    image = Image.open(image_path)
    # get the image"s dimensions
    width, height = image.size
    # scale the smaller dimension to the size passed in, if none passed in use 24x24
    if width > height:
        scale = size[0] / width
        width = size[0]
        height = height * scale
    else:
        scale = size[1] / height
        height = size[1]
        width = width * scale
    # resize the image
    size = (int(width), int(height))
    image = image.resize(size)
    imported = ImageTk.PhotoImage(image)
    # print(imported)
    return image, imported


class ChatUI:
    def __init__(self, master):
        self.master = master
        master.title("ZyrenthSorter")

        self.current_row = 0

        scrollbar_style = Style()
        scrollbar_style.configure("Vertical.TScrollbar", background="#372549", troughcolor="#372549", borderwidth=0, gripcount=0, arrowsize=0, highlightthickness=0, width=0, relief="flat")

        # create scrolled text widget for chat window
        self.chat_window = ScrolledText(master)
        self.chat_window.grid(row = 4, column = 0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.chat_window.config(background="#372549", foreground="#EACDC2", borderwidth=0, highlightthickness=0, width=0, relief="flat", font=("FOT-Rodin Pro M", 12))
        self.chat_window.columnconfigure(0, weight=1)
        # if self.chat_window.yview()[1] == 1.0:
        #     self.chat_window.configure(yscrollcommand=None)

        # create input box
        self.input_box = Text(master, height=3, width=2)
        self.input_box.grid(row=5, column=0, columnspan=1, padx=5, pady=5, sticky="nsew")
        self.input_box.config(background="#372549", foreground="#EACDC2", borderwidth=0, font=("FOT-Rodin Pro DB", 12))
        
        # this code is no longer needed cuz i just gave up on trying to get ttk buttons to work but im too lazy to delete it
        ## stupid workaround b/c ttk buttons don"t have background or foreground properties
        # button_style = Style()
        ## button_style.map("TButton", background=[("active", "#372549"), ("pressed", "#372549")], foreground=[("active", "#372549"), ("pressed", "#774C60")], font=[("active", ("FOT-Rodin Pro DB", 10)), ("pressed", ("FOT-Rodin Pro DB", 10))])
        # button_style.configure("TButton", background="#1A1423", highlightbackground="#372549", foreground="blue", highlightcolor="#774C60", font=("FOT-Rodin Pro DB", 10))
        ## set the button color to the same as the background
        ## button_style.configure("TButton", background="#372549", foreground="#372549", font=("FOT-Rodin Pro DB", 10))

        # another stupid workaround b/c ttk buttons are picky with images
        # no longer using ttk but this workaround is still somehow needed
        script_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
        # print(script_dir)
        image_path = script_dir + "/assets/images/send.png"
        # print(image_path)
        image = Image.open(image_path)
        image = image.resize((24, 24))
        ChatUI.photo = ImageTk.PhotoImage(image)

        # create send button. uses tkButton class (og Button class) cause the ttk buttons just werent working on windows 11
        # self.send_button = Button(master, style="TButton", text="Send", image=ChatUI.photo, command=self.send_message)
        self.image, self.button_image = import_image("/assets/images/send.png")
        self.send_button = tkButton(master, text="Send", image=self.button_image, command=self.send_message, background="#372549", highlightbackground="#372549", foreground="blue", activeforeground="#774C60", borderwidth=0, highlightcolor="#774C60", font=("FOT-Rodin Pro DB", 10))
        self.send_button.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

        # initialize message count
        self.message_count = 0

        master.columnconfigure(0, weight=4)
        master.columnconfigure(1, weight=1)
        master.rowconfigure(4, weight=1)
        
        # bind enter key to send message
        master.bind("<Return>", self.send_message)

    def send_message(self, type="normal"):
        if type != "resend":
            message = self.input_box.get("1.0", "end-1c").strip()
            # check if message is empty or is just whitespace, exit function if it is
            if message == "" or message.isspace():
                return
            
            def print_directory_contents(path, indent=0):
                output = ''
                for child in os.listdir(path):
                    child_path = os.path.join(path, child)
                    if os.path.isdir(child_path):
                        output += ' ' * indent + child + '/' + '\n'
                        output += print_directory_contents(child_path, indent + 4)
                    else:
                        output += ' ' * indent + child + '\n'
                return output

            # see if message contains a directory path
            if os.path.isdir(message):
                # create a text file tree of the directory
                sent_message = print_directory_contents(r'' + message)
                self.create_message("user", "You", message.strip(), False)
                messages.append({"role": "user", "content": sent_message})
                # print(sent_message)
                # update message count
                self.message_count += 1

                self.input_box.delete("1.0", END)

                # print(messages)
                # send message to openai api
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens = 100,
                    temperature = 0.9,
                    stop=[" Human:", " Zyrenth:"],
                    timeout=100
                )

                self.create_message("assistant", "Zyrenth", r''+ response["choices"][0]["message"]["content"])
                print(response.choices[0].message)
            else: 
                self.create_message("user", "You", message.strip())

                # update message count
                self.message_count += 1

                self.input_box.delete("1.0", END)

                # print(messages)
                # send message to openai api
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens = 100,
                    temperature = 0.9,
                    stop=[" Human:", " Zyrenth:"],
                    timeout=100
                )

                self.create_message("assistant", "Zyrenth", r''+response["choices"][0]["message"]["content"])
                print(response.choices[0].message)
                print(response.choices[0])
        else:
            # delete the last text widget in the chat window
            self.chat_window.delete("end-2l", "end-1l")
            # delete the last message in the messages list
            messages.pop(len(messages) - 1)
            # print(messages)
            # send message to openai api
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                n = 1,
                max_tokens = 100,
                temperature = 0.9,
                stop=[" Human:", " Zyrenth:",],
                timeout=100
            )
            self.create_message("assistant", "Zyrenth", response["choices"][0]["message"]["content"].strip())

    def resend_message(self):
        # print("resending message")
        self.send_message("resend")
        # webbrowser.open("https://openai.com")
    

    def create_message(self, role, person, message, save_to_history=True):
        # make sure the role provided is "system" or "user" or "assistant" or the openai api will throw an error
        if role not in ["system", "user", "assistant"]:
            raise ValueError("Invalid role provided")

        message_box = Text(self.chat_window, height=(round((len(message)//30)+1)), wrap="word")
        message_box.insert(END, f"{person}: {message.strip()}")
        message_box.config(
            background="#372549",
            foreground="#EACDC2",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            font=("FOT-Rodin Pro M", 12),
            wrap="word",
        )
        if role == "assistant":
            message_box.config(background="#774C60")

        message_box.grid(column=0, columnspan=1, row=self.current_row, sticky="nsew")
        self.current_row += 1

        self.chat_window.columnconfigure(0, weight=1)

        # add message to message history in {"role": "user", "content": "message"} format
        if save_to_history:
            messages.append({"role": role, "content": message.strip()})

        # add a divider to the chat window
        self.chat_window.insert(END, "----------------------------------------\n", "divider")



def about_window():
    # create a popup window
    info_window = Toplevel()
    info_window.title("About ZyrenthSorter")
    info_window.geometry("400x600")

    # create a image label
    logo, imported_logo = import_image("/assets/images/ZyrenthSorter_Logo.png", (150, 150))
    image_label = Label(info_window, image=imported_logo)
    image_label.grid(row=0, column=0, columnspan=3, sticky="nsew")
    image_label.configure(anchor="center")
    image_label.config(background="#1A1423")

    title_and_version_frame = Frame(info_window, padding=10)
    title_label = Label(title_and_version_frame, text="ZyrenthSorter", font=("FOT-Rodin Pro UB", 28), foreground="#EACDC2")
    title_label.grid(row=0, rowspan=2, column=0)
    title_label.configure(anchor="e")
    title_label.config(background="#1A1423", padding=(0, 0), width=11)
    version_label = Label(title_and_version_frame, text="v1.0.0", font=("FOT-Rodin Pro M", 12), foreground="#D19596")
    version_label.grid(row=1, column=1)
    version_label.configure(anchor="w")
    version_label.config(background="#1A1423", padding=(0,0), width=5)
    title_and_version_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
    title_and_version_frame.config(style="TFrame")

    title_and_version_frame.grid_columnconfigure(0, weight=0)
    title_and_version_frame.grid_columnconfigure(1, weight=3)
    title_and_version_frame.grid_rowconfigure(0, weight=1)
    title_and_version_frame.grid_rowconfigure(1, weight=1)

    TFrame = Style()
    TFrame.configure("TFrame", background="#1A1423", borderwidth=0, highlightthickness=0, relief="flat")
    
    # ignore all of this, it's just my failed attempts at making a text widget with multiple styles
    # # Create a Text widget
    # title_and_version_text = Text(info_window, height=1, wrap='none', font=('FOT-Rodin Pro UB', 24), borderwidth=0, highlightthickness=0, relief="flat")
    # title_and_version_text.insert(END, 'ZyrenthSorter ', 'title')
    # title_and_version_text.insert(END, 'v1.0.0', 'version')
    # title_and_version_text.tag_configure("title", foreground='#EACDC2', font=("FOT-Rodin Pro UB", 24))
    # title_and_version_text.tag_configure("version", foreground='#D19596', font=("FOT-Rodin Pro M", 12))
    # # Grid the widgets
    # title_and_version_text.grid(row=1, column=0)
    # title_and_version_text.config(background="#1A1423")

    # title_and_version_label = Label(info_window, text=title_and_version_text.get("1.0", "end-1c"))
    # title_and_version_label.grid(row=5, column=0, columnspan=3, sticky="nsew")
    
    # version_label = Label(info_window, text="v1.0.0")
    # version_label.grid(row=3, column=0, columnspan=3, sticky="nsew")
    # version_label.config(background="#1A1423", foreground="#EACDC2", font=("FOT-Rodin Pro M", 12))
    # version_label.configure(anchor="center")

    subtitle_label = Label(info_window, text="by Issac Liu")
    subtitle_label.grid(row=3, column=0, columnspan=3, sticky="nsew")
    subtitle_label.config(background="#1A1423", foreground="#EACDC2", font=("FOT-Rodin Pro DB", 14))
    subtitle_label.configure(anchor="center")

    code_mark, imported_code_mark = import_image("/assets/images/code_overflow_mark.png", (350, 140)) # ratio is 2.5:1 
    code_overflow_image = tkButton(info_window, text="Code Overflow 2023", image=imported_code_mark, command=lambda: webbrowser.open("https://codeoverflow.devpost.com"))
    code_overflow_image.grid(row=4, column=0, columnspan=3, sticky="nsew")
    code_overflow_image.config(background="#1A1423", foreground="#EACDC2", borderwidth=0, font=("FOT-Rodin Pro DB", 12), width=350, height=140)
    code_overflow_image.configure(anchor="center")

    ok_button = tkButton(info_window, text="OK", command=info_window.destroy)
    ok_button.grid(row=6, column=1, sticky="nsew")
    ok_button.config(background="#372549", foreground="#EACDC2", borderwidth=0, font=("FOT-Rodin Pro DB", 12))

    info_window.columnconfigure(0, weight=1)
    info_window.columnconfigure(1, weight=1)
    info_window.columnconfigure(2, weight=1)
    info_window.rowconfigure(0, weight=1)
    info_window.rowconfigure(1, weight=1)
    info_window.rowconfigure(2, weight=1)
    info_window.rowconfigure(3, weight=1)
    info_window.rowconfigure(4, weight=1)
    info_window.rowconfigure(5, weight=4)
    info_window.rowconfigure(6, weight=1)

    image_label.grid_configure(padx=10, pady=(10,0))
    title_and_version_frame.grid_configure(padx=10, pady=(0,0))
    subtitle_label.grid_configure(padx=10, pady=(0,0))
    code_overflow_image.grid_configure(padx=10, pady=(0,10))

    ok_button.grid_configure(padx=10, pady=(10,10))

    info_window.config(background="#1A1423")

    info_window.mainloop()

def resend_message():
    # call send_message() again from the chat_ui class defined earlier
    chat_ui.resend_message()

if __name__ == "__main__":
    # create the tkinter window and set tkinter to be a thread
    global messages
    messages = []

    window = Tk()
    window.title("ZyrenthSorter")
    window.geometry("400x630")

    messages.append({"role": "system", "content": "You are Zyrenth, a helpful and friendly chatbot that is still in development. You will help the user sort the files on their computer. You first ask them for their name, then ask for the location of the files they want to sort. They will give you You then ask them if they want to sort more files, and if they say yes, you ask them for the location of the files they want to sort. If they say no, you thank them for using ZyrenthSorter and wish them a good day. Do not use any code snippets, only use plain text."})

    title_label = Label(window, text="ZyrenthSorter")
    title_label.grid(row=0, column=0, columnspan=2, sticky="ew")
    title_label.config(background="#1A1423", foreground="#EACDC2", font=("FOT-Rodin Pro UB", 24))
    subtitle_label = Label(window, text="Made for CodeOverflow 2023")
    subtitle_label.grid(row=1, column=0, columnspan=2, sticky="ew")
    subtitle_label.config(background="#1A1423", foreground="#EACDC2", font=("FOT-Rodin Pro M", 12))

    about_image, about_imported = import_image("/assets/images/info.png", (24, 24))
    about_button = tkButton(window, text="About", image=about_imported, command=about_window, background="#1A1423", highlightbackground="#372549", foreground="blue",   activeforeground="#774C60", borderwidth=0, highlightcolor="#774C60", font=("FOT-Rodin Pro DB", 10))
    about_button.grid(row=0, column=1, sticky="e", padx=(0,10), pady=(10,0))

    regenerate_image, regenerate_imported = import_image("/assets/images/regenerate_message.png", (24, 24))
    regenerate_button = tkButton(window, text="Regenerate", image=regenerate_imported, background="#1A1423", command=resend_message, highlightbackground="#372549", foreground="blue", activeforeground="#774C60", borderwidth=0, highlightcolor="#774C60", font=("FOT-Rodin Pro DB", 10))
    regenerate_button.grid(row=1, column=1, sticky="e", padx=(0,10), pady=(0,10))
    regenerate_button.grid_configure(padx=10, pady=(0,10))

    chat_ui = ChatUI(window)

    title_label.grid_configure(padx=10, pady=(10,0))
    subtitle_label.grid_configure(padx=10, pady=(0,10))
    about_button.grid_configure(padx=10, pady=(10,0))

    chat_ui.create_message("assistant", "Zyrenth", "Hello! I'm Zyrenth, here to help you sort your files. What is your name?")
        
    window.configure(background="#1A1423")

    window.mainloop()