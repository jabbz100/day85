from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

edit_image = None
original_image = None
watermarked_picture = None

# Window Setup
root = Tk()
root.geometry('1280x780')
root.resizable(False, False)
root.configure(background="#2E2E2E", borderwidth=0)
root.title("Watermark App")

canvas = Canvas(root, width=1280, height=720, bg="#3B3B3B")
canvas.grid(row=0, columnspan=4)

label = Label(root, text="Upload Your Image", font=("Roboto", 14), bg="#3B3B3B", foreground="white")
label.grid(row=0, columnspan=4)

# Button Style
style = ttk.Style()
style.configure(
    "Apple.TButton",
    background="#444",
    foreground="black",
    font=("San Francisco", 14), padding=5
)
# Entry Style
style.configure(
    "Custom.TEntry",
    fieldbackground="white",
    background="white",
    bordercolor="#D1D1D1",
    focuscolor="#007AFF",
    padding=5,
    relief="flat"
)
# Label Style
style.configure(
    "Custom.TLabel",
    foreground="white",
    font=("San Francisco", 14),
    background="#2E2E2E",
    bordercolor="black",
    padding=5,
    relief="flat"
)
style.map(
    "Apple.TButton",
    background=[("active", "#D4D4D4")],
)
style.configure(
    "Dark.TFrame",
    background="#2E2E2E"
)


# Watermark Text
def add_text_btn():

    def watermark_image(input_img, watermark_text, opacity, text_size):
        width, height = input_img.size

        overlay = Image.new('RGBA', input_img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        watermark_color_pattern = (255, 255, 255, 30)
        for n in range(0, width + height, 50):
            draw.line([(0, height - n), (n, height)], fill=watermark_color_pattern, width=5)

        font_size = text_size
        font = ImageFont.truetype('arial.ttf', font_size)

        bbox = draw.textbbox((0, 0), watermark_text, font=font)

        text_width = bbox[2] - bbox[0]  # bbox[2] is the right side, bbox[0] is the left side
        text_height = bbox[3] - bbox[1]

        x = (width - text_width) // 2
        y = (height - text_height) // 2

        watermark_color_text = (255, 255, 255, opacity)

        draw.text((x, y), watermark_text, fill=watermark_color_text, font=font)

        watermarked_image = Image.alpha_composite(input_img, overlay)

        return watermarked_image

    def apply_watermark():
        global watermarked_picture
        try:
            input_image = edit_image
        except AttributeError:
            print("No image to watermark.")
        else:
            input_text = entries[0].get()
            text_size = int(entries[1].get())
            opacity = int(entries[2].get())
            if input_image and input_text:
                marked_img = watermark_image(input_image, input_text, opacity, text_size)
                watermarked_picture = marked_img

                display_image = marked_img.copy()
                display_image.thumbnail((1280, 720))

                photo = ImageTk.PhotoImage(display_image)
                label.config(image=photo)
                label.image = photo

                label.img = marked_img

                pane.destroy()

    pane = Toplevel(root)
    pane.title("Watermark Settings")
    pane.geometry("400x200")
    pane.configure(background="#2E2E2E")
    pane.resizable(False, False)

    pane.grid_columnconfigure(0, weight=0)  # Label column
    pane.grid_columnconfigure(1, weight=1)  # Entry column expands
    pane.grid_rowconfigure(5, weight=1)  # Pushes buttons to bottom

    entries = []
    labels = [("Text:", "Hello World"), ("Text Size:", 120), ("Opacity:", 60)]
    for i, (text, default_value) in enumerate(labels):
        this_label = ttk.Label(pane, text=text, style="Custom.TLabel")
        this_label.grid(row=i, column=0, pady=5, padx=10, sticky="w")

        this_entry = ttk.Entry(pane, style="Custom.TEntry", font=("San Francisco", 16), width=14)
        this_entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")
        this_entry.insert(0, default_value)

        entries.append(this_entry)

    # Centering buttons
    button_frame = ttk.Frame(pane, style="Dark.TFrame")
    button_frame.grid(row=4, column=0, columnspan=2, pady=10)

    ttk.Button(button_frame, text="Save", command=apply_watermark, style="Apple.TButton").grid(row=0, column=0, padx=10)
    ttk.Button(button_frame, text="Cancel", command=pane.destroy, style="Apple.TButton").grid(row=0, column=1, padx=10)


def remove_watermark():
    label.config(image=original_image)


def open_image():
    global original_image
    global edit_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        input_img = Image.open(file_path).convert('RGBA')

        edit_image = input_img  # Keep full-size image

        # Create a copy for display and resize it
        display_image = input_img.copy()
        display_image.thumbnail((1280, 720))

        photo = ImageTk.PhotoImage(display_image)

        label.config(image=photo)
        label.image = photo

        original_image = photo


def save_image():
    if watermarked_picture:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        if file_path:
            watermarked_picture.save(file_path)


ttk.Button(root, text="Open Image", command=open_image, style="Apple.TButton").grid(row=1, column=0, pady=5)
ttk.Button(root, text="Add Text", command=add_text_btn, style="Apple.TButton").grid(row=1, column=1)
ttk.Button(root, text="Revert Image", command=remove_watermark, style="Apple.TButton").grid(row=1, column=2)
ttk.Button(root, text="Save Image", command=save_image, style="Apple.TButton").grid(row=1, column=3)

root.mainloop()
