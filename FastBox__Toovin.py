import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


scale_factor = 1  # Initialize the scale factor.
box_size = 512
max_box_size = 1024
min_box_size = 64
increment = 8
box_size_text = None

def force_canvas_focus(event=None):
    canvas.focus_force()

def on_focus_in(event):
    print("Canvas gained focus!")

def on_focus_out(event):
    print("Canvas lost focus!")

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        root.focus_set()  # Return focus to the main window after the dialog is closed
        return os.path.abspath(file_path)
    return None



def rescale_image_to_fit_window(image, max_width, max_height):
    """
    Rescale the PIL image to fit within max_width and max_height while maintaining the aspect ratio.
    """
    width_ratio = max_width / image.width
    height_ratio = canvas_max_height / image.height  # use canvas_max_height here
    scale_factor = min(width_ratio, height_ratio)

    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)

    return image.resize((new_width, new_height), Image.Resampling.LANCZOS), scale_factor

def update_canvas(event=None):
    global image, tk_image, scale_factor, rect
    if not image:
        return
    image_rescaled, scale_factor = rescale_image_to_fit_window(image, canvas.winfo_width(), canvas.winfo_height())
    tk_image = ImageTk.PhotoImage(image_rescaled)
    canvas.config(scrollregion=canvas.bbox(tk.ALL))
    canvas.delete(tk.ALL)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    rect_size = 512 * scale_factor
    rect = canvas.create_rectangle(0, 0, rect_size, rect_size, outline="red")
    canvas.tag_raise(box_size_text)

def adjust_box_size(event):
    global box_size, box_size_text
    if event.delta > 0:
        box_size = min(max_box_size, box_size + increment)
    else:
        box_size = max(min_box_size, box_size - increment)

    # Update text content
    canvas.itemconfigure(box_size_text, text=f"{box_size}x{box_size}")

    on_mouse_move(event)  # Refresh the box's position and text after resizing

def save_region(image, x, y):
    print("save_region function entered")
    half_box_size = (box_size * scale_factor) / 2  # Adjust for scale factor
    left = (x / scale_factor) - half_box_size  # Adjust for scale factor
    top = (y / scale_factor) - half_box_size  # Adjust for scale factor
    right = (x / scale_factor) + half_box_size  # Adjust for scale factor
    bottom = (y / scale_factor) + half_box_size  # Adjust for scale factor

    region = image.crop((left, top, right, bottom))
    print("Attempting to open save dialog...")
    save_path = filedialog.asksaveasfilename(
    defaultextension=".jpg",
    filetypes=(
        ("JPEG files", "*.jpg"),
        ("PNG files", "*.png"),
        ("BMP files", "*.bmp"),
        ("WEBP files", "*.webp"),
        ("GIF files", "*.gif"),
        ("ICO files", "*.ico"),
        (
            "TIFF files",
            "*.tif;*.tiff",
        ),  # Note that you can use a semicolon to support multiple patterns in a single tuple.
    ),
)
    if save_path:
        print("Saving image to:", save_path)
        region.save(save_path)

def on_mouse_move(event):
    global scale_factor, box_size, box_size_text
    x, y = event.x, event.y

    half_box_size = box_size * scale_factor / 2
    x1 = max(0, x - half_box_size)
    y1 = max(0, y - half_box_size)
    x2 = min(canvas.winfo_width(), x + half_box_size)
    y2 = min(canvas.winfo_height(), y + half_box_size)

    canvas.coords(rect, x1, y1, x2, y2)
    
    # Update the position of the text to be right below the rectangle
    canvas.coords(box_size_text, x, y2 + 10)
    print("Text coords updated to:", x, y2 + 10)


def capture_image(event=None):
    if event:
        x, y = event.x, event.y
    else:
        # Use the center of the canvas as the default position
        x = canvas.winfo_width() / 2
        y = canvas.winfo_height() / 2

    print("capture_image called")
    save_region(image, x, y)

def on_mouse_click(event):
    x, y = event.x, event.y
    save_region(image, x, y)

def navigate(event):
    global image_files, current_image_index, image, tk_image

    if event.keysym == "Right":
        current_image_index += 1
    elif event.keysym == "Left":
        current_image_index -= 1

    current_image_index %= len(image_files)
    image_path = image_files[current_image_index]
    image = Image.open(image_path)
    image, scale_factor = rescale_image_to_fit_window(image, canvas.winfo_width(), canvas.winfo_height())  # rescale image
    tk_image = ImageTk.PhotoImage(image)

    update_canvas()

root = tk.Tk()
screen_height = root.winfo_screenheight()
canvas_max_height = screen_height - 100
root.title("Image Box Extractor")

image_path = open_image()

btn = tk.Button(root, text="Capture", command=capture_image)
btn.pack()
##root.focus_set()  # Set focus to the main window
if image_path:
    root.focus_force()
    dir_path = os.path.dirname(image_path)
    image_files = [os.path.abspath(os.path.join(dir_path, f)) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]
    current_image_index = image_files.index(image_path)
    image = Image.open(image_path)
    tk_image = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(root, width=image.width, height=min(image.height, canvas_max_height)) # this gotta change
    canvas.pack()
    canvas.focus_force()  # forcefully set the focus on the canvas
    canvas.bind("<FocusIn>", on_focus_in)
    canvas.bind("<FocusOut>", on_focus_out)
    canvas.focus_set()
    # Create a rectangle that's 512x512. Neat.
    rect = canvas.create_rectangle(0, 0, 512, 512, outline="red")
    box_size_text = canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        anchor=tk.CENTER,
        text=f"{box_size}x{box_size}",
        fill="red",
            )
    print("Text created with coords:", canvas.coords(box_size_text))
    canvas.tag_raise(box_size_text)
    #canvas.bind("<Button-1>", force_canvas_focus)
    canvas.bind("<Configure>", update_canvas)
    canvas.bind("<MouseWheel>", adjust_box_size)  # For Windows and MacOS with a mouse
    canvas.bind("<Button-4>", adjust_box_size)  # For Linux scroll up
    canvas.bind("<Button-5>", adjust_box_size)  # For Linux scroll down
    canvas.bind("<Motion>", on_mouse_move)
    canvas.bind("<KeyPress-c>", capture_image)
    root.bind("<Left>", navigate)
    root.bind("<Right>", navigate)

canvas.after(100, canvas.focus_set)  # Wait 100ms and then set the focus.
root.mainloop()
