import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import requests
import secrets

class ChatUI:
    def __init__(self, master):
        self.master = master
        master.title("ChatGPT Application")

        # create frame to hold chat window
        chat_frame = ttk.Frame(master)
        chat_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # create scrolled text widget for chat window
        self.chat_window = ScrolledText(chat_frame)
        self.chat_window.grid(row = 4, column = 0, columnspan=2, padx=5, pady=5, sticky="nsew")
        # set width to window width

        # create input box
        self.input_box = ttk.Entry(master)
        self.input_box.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        # create send button
        self.send_button = ttk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

        # initialize message count
        self.message_count = 0

        master.columnconfigure(0, weight=3)
        master.columnconfigure(1, weight=1)

    def send_message(self):
        message = self.input_box.get()
        # send message to ChatGPT API and get response
        response = "Response from ChatGPT API"

        # create new text box for message and response
        message_box = Text(self.chat_window, height=1, width=50)
        message_box.insert(END, "You: " + message + "\nChatGPT: " + response)
        message_box.configure(state=DISABLED)
        self.chat_window.window_create(END, window=message_box)

        # update message count
        self.message_count += 1

        self.input_box.delete(0, END)

if __name__ == '__main__':
    window = Tk()
    window.title('File Sorter')
    window.geometry("400x630")

    titleLabel = ttk.Label(window, text='File Sorter')
    titleLabel.grid(row=0, column=0, columnspan=2, sticky='ew')
    titleLabel.config(font=("FOT-Rodin Pro EB", 14))
    subtitleLabel = ttk.Label(window, text='with Zyrenth, your personal assistant')
    subtitleLabel.grid( row=1, column=0, columnspan=2, sticky='ew')
    subtitleLabel.config(font=("FOT-Rodin Pro DB", 10))

    titleLabel.grid_configure(padx=10, pady=10)
    subtitleLabel.grid_configure(padx=10, pady=10)

    chat_ui = ChatUI(window)
    window.mainloop()
