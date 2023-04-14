import textwrap
from tkinter import Text, Tk, END

r = Tk()
r.geometry("400x400")

t = Text(r, height=20, width=40)
t.pack()

# Insert your text here
t.insert("end", "Your text here")

# def resize_text_widget(text_input):
#    num_lines = t.index("end").split(".")[0]
#    height = int(t.dlineinfo(num_lines).split()[3]) + 10
#    t.config(height=height)

num_lines = int(t.index("end-1c").split(".")[0])
height = int(t.dlineinfo(num_lines).split()[3]) + 10
t.config(height=height)

# t.bind("<Configure>", resize_text_widget)
r.mainloop()
# resize_text_widget("# Get the current text widget contents\n    text_contents = event.widget.get('1.0', tk.END)\n\n    # Calculate the desired height based on the contents\n    lines = text_contents.count('\n') + 1\n    height = lines * int(event.widget.index('end-1c').split('.')[0])\n\n    # Set the new height of the Text widget\n    event.widget.configure(height=height)")