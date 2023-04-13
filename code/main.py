import os
import sys
from tkinter import *
from tkinter import ttk
import requests

window = Tk()
window.title('File Sorter')
window.geometry("400x630")

titleLabel = ttk.Label(window, text='File Sorter')
titleLabel.grid(column=0, row=0, sticky='ew')
titleLabel.config(font=("FOT-Rodin Pro EB", 14))
subtitleLabel = ttk.Label(window, text='with Zyrenth, your personal assistant')
subtitleLabel.grid(column=0, row=1, sticky='ew')
subtitleLabel.config(font=("FOT-Rodin Pro DB", 10))

titleLabel.grid_configure(padx=10, pady=10)
subtitleLabel.grid_configure(padx=10, pady=10)

window.mainloop()