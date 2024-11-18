import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageColor
import os
from tkinter.filedialog import askopenfilename
from tkinter import colorchooser

im = None
selected_color = (255, 255, 255)

def browse():
    global im
    file_path = askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        link_entry.delete(0, 'end')
        link_entry.insert(0, file_path)
        im = Image.open(file_path)
        im.thumbnail((800, 800))
        im_display = ImageTk.PhotoImage(im)

        preview_label.config(image=im_display)
        preview_label.image = im_display

def choose_color():
    global selected_color
    color = colorchooser.askcolor(title="Tkinter Color Chooser")[0]
    selected_color = color
    update_preview()

def update_preview():
    global im
    file_path = link_entry.get()
    if file_path:
        im = Image.open(file_path)
        width, height = im.size

        draw = ImageDraw.Draw(im)
        text = "Poco Loco"
        font = ImageFont.truetype('arial.ttf', size_scale.get())
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = width - text_width - 10
        y = height - text_height - 10
        draw.text((x, y), text, font=font, fill=selected_color + (128,))

        im.thumbnail((800, 800))
        im_display = ImageTk.PhotoImage(im)

        preview_label.config(image=im_display)
        preview_label.image = im_display

def save_image():
    global im
    if im:
        file_path = link_entry.get()
        file_name = os.path.basename(file_path)
        im.save(f'watermarked-{file_name}')
        print("Image saved")
    else:
        print("No image to save")

window = tk.Tk()
window.title("Watermark adder")
window.config(padx=50, pady=50)

text_label = tk.Label(window, text="Insert the link of the image you want to add watermark:", font=('Arial', 12, "bold"))
text_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), padx=(20, 20))

link_entry = tk.Entry(window, width=45)
link_entry.grid(row=1, column=0, pady=(10, 10))

browse_button = tk.Button(window,text="Browse",font=('Arial', 12), width=10, command=browse)
browse_button.grid(row=1, column=1)

add_watermark_button = tk.Button(window, text="Add Watermark", font=('Arial', 12), width=14, height=1, command=update_preview)
add_watermark_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))

size_scale = tk.Scale(window, from_=8, to=80, orient="horizontal", label="Watermark size", command=lambda val: update_preview())
size_scale.set(36)
size_scale.grid(row=3, column=0, columnspan=2)

color_button = tk.Button(window, text="Choose color", font=('Arial', 12), width=14, height=1, command=choose_color)
color_button.grid(row=4, column=0, columnspan=2)

save_button = tk.Button(window, text="Save", font=('Arial', 12), width=14, height=1, bg="green2", command=save_image)
save_button.grid(row=5, column=0, columnspan=2, pady=(10, 0))

preview_label = tk.Label(window)
preview_label.grid(row=0, column=2, rowspan=100)

window.mainloop()