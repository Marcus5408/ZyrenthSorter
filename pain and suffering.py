import tkinter as tk

def set_text_widget_height(widget):
    # Get number of lines in widget
    num_lines = int(widget.index('end-1c').split('.')[0])
    
    # Get height of one line
    line_height = root.font.measure('linespace')
    
    # Set height of widget
    widget.config(height=num_lines * line_height)

root = tk.Tk()
root.font = tk.font.Font(font=root['font'])

text_widget = tk.Text(root, wrap='word')
text_widget.pack(expand=True, fill='both')

text_widget.insert('end', 'This is some long text that will be wrapped when it reaches the edge of the text widget.')
set_text_widget_height(text_widget)

root.mainloop()