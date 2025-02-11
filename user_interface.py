from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

edit_image = None
original_image = None
watermarked_picture = None
logo_img = None

# Window Setup
root = Tk()
root.geometry('1280x780')
root.resizable(False, False)
root.configure(background="#2E2E2E", borderwidth=0)
root.title("Watermark App")

canvas = Canvas(root, width=1280, height=720, bg="#3B3B3B")
canvas.grid(row=0, columnspan=5)

label = Label(root, text="Upload Your Image", font=("Roboto", 14), bg="#3B3B3B", foreground="white")
label.grid(row=0, columnspan=5)

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
# Button Frame
style.configure(
    "Dark.TFrame",
    background="#2E2E2E"
)


# Watermark Functionality
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


def add_logo_btn():
    global logo_img
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        def watermark_image_w_logo(input_img, logo_path, opacity=100, scale=0.3):
            width, height = input_img.size

            logo = logo_path

            # Scale
            logo_width = int(width * scale)
            logo_height = int(logo.height * (logo_width / logo.width))  # Keep aspect ratio
            logo = logo.resize((logo_width, logo_height), Image.LANCZOS)

            # Opacity
            alpha = logo.split()[3].point(lambda p: p * (opacity / 100))
            logo.putalpha(alpha)

            x = (width - logo_width) // 2
            y = (height - logo_height) // 2

            overlay = Image.new("RGBA", input_img.size, (255, 255, 255, 0))
            overlay.paste(logo, (x, y), logo)

            watermarked_image = Image.alpha_composite(input_img.convert("RGBA"), overlay)

            return watermarked_image

        def apply_logo_watermark():
            global watermarked_picture
            try:
                input_image = edit_image
            except AttributeError:
                print("No image to watermark.")
            else:
                input_logo = logo_img
                logo_scale = float(entries[0].get())
                opacity = int(entries[1].get())
                if input_image and input_logo:
                    marked_img = watermark_image_w_logo(input_image, input_logo, scale=logo_scale, opacity=opacity)
                    watermarked_picture = marked_img

                    display_image = marked_img.copy()
                    display_image.thumbnail((1280, 720))

                    photo = ImageTk.PhotoImage(display_image)
                    label.config(image=photo)
                    label.image = photo

                    label.img = marked_img

                    pane.destroy()

        logo_img = Image.open(file_path).convert('RGBA')

        pane = Toplevel(root)
        pane.title("Watermark Settings")
        pane.geometry("400x150")
        pane.configure(background="#2E2E2E")
        pane.resizable(False, False)

        pane.grid_columnconfigure(0, weight=0)  # Label column
        pane.grid_columnconfigure(1, weight=1)  # Entry column expands
        pane.grid_rowconfigure(5, weight=1)  # Pushes buttons to bottom

        entries = []
        labels = [("Scale:", 0.3), ("Opacity:", 60)]
        for i, (text, default_value) in enumerate(labels):
            this_label = ttk.Label(pane, text=text, style="Custom.TLabel")
            this_label.grid(row=i, column=0, pady=5, padx=10, sticky="w")

            this_entry = ttk.Entry(pane, style="Custom.TEntry", font=("San Francisco", 16), width=14)
            this_entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")
            this_entry.insert(0, default_value)

            entries.append(this_entry)

        button_frame = ttk.Frame(pane, style="Dark.TFrame")
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save", command=apply_logo_watermark,
                   style="Apple.TButton").grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Cancel", command=pane.destroy,
                   style="Apple.TButton").grid(row=0, column=1, padx=10)


def remove_watermark():
    global logo_img
    label.config(image=original_image)
    logo_img = None


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
ttk.Button(root, text="Add Logo", command=add_logo_btn, style="Apple.TButton").grid(row=1, column=2)
ttk.Button(root, text="Revert Image", command=remove_watermark, style="Apple.TButton").grid(row=1, column=3)
ttk.Button(root, text="Save Image", command=save_image, style="Apple.TButton").grid(row=1, column=4)

root.mainloop()
