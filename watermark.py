import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk


# Constants

PREVIEW_WIDTH = 300
PREVIEW_HEIGHT = 300
PREVIEW_PADDING = 20


# Globals

img = None
img_path = None
tk_img = None
multiple_images = []
logo_img = None
logo_path = None


# GUI Setup

root = tk.Tk()
root.title("Watermark App")
watermark_mode = tk.StringVar(value="text")  # default mode


# Mode Selection

mode_frame = tk.Frame(root)
mode_frame.pack(pady=5)

tk.Radiobutton(mode_frame, text="Text Watermark", variable=watermark_mode, value="text").pack(side="left")
tk.Radiobutton(mode_frame, text="Logo Watermark", variable=watermark_mode, value="logo").pack(side="left")


# Upload Logo

def upload_logo():
    global logo_img, logo_path
    logo_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    if logo_path:
        logo_img = Image.open(logo_path).convert("RGBA")
        messagebox.showinfo("Logo Loaded", "Logo loaded successfully.")

upload_logo_button = tk.Button(root, text="Upload Logo", command=upload_logo)
upload_logo_button.pack(pady=5)


# Canvas for Preview

canvas = tk.Canvas(root, width=PREVIEW_WIDTH + 2*PREVIEW_PADDING,
                   height=PREVIEW_HEIGHT + 2*PREVIEW_PADDING)
canvas.pack()


# Upload Images (single or multiple)

def upload_image():
    global img, img_path, tk_img, multiple_images
    paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png *.jpeg *.jpg")])
    if not paths:
        return

    multiple_images = list(paths)

    # If single image, show preview
    if len(multiple_images) == 1:
        img_path = multiple_images[0]
        img = Image.open(img_path)

        # Resize for preview while keeping aspect ratio
        img_ratio = img.width / img.height
        preview_ratio = PREVIEW_WIDTH / PREVIEW_HEIGHT

        if img_ratio > preview_ratio:
            new_width = PREVIEW_WIDTH
            new_height = int(PREVIEW_WIDTH / img_ratio)
        else:
            new_height = PREVIEW_HEIGHT
            new_width = int(PREVIEW_HEIGHT * img_ratio)

        resized_img = img.resize((new_width, new_height))
        tk_img = ImageTk.PhotoImage(resized_img)

        # Center image
        x_offset = PREVIEW_PADDING + (PREVIEW_WIDTH - new_width)//2
        y_offset = PREVIEW_PADDING + (PREVIEW_HEIGHT - new_height)//2

        canvas.delete("all")
        canvas.create_image(x_offset, y_offset, anchor="nw", image=tk_img)

        print("Single image loaded.")
    else:
        img = None
        canvas.delete("all")
        messagebox.showinfo("Images Loaded", f"{len(multiple_images)} images selected.")
        print(f"Loaded {len(multiple_images)} images.")

upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)


# Watermark Input with Placeholder

placeholder_text = "Enter your watermark here"
placeholder_color = "grey"

watermark_entry = tk.Entry(root, fg=placeholder_color)
watermark_entry.pack(pady=10)
watermark_entry.insert(0, placeholder_text)

def on_entry_click(event):
    if watermark_entry.get() == placeholder_text:
        watermark_entry.delete(0, "end")
        watermark_entry.config(fg="black")

def on_focusout(event):
    if watermark_entry.get() == "":
        watermark_entry.insert(0, placeholder_text)
        watermark_entry.config(fg=placeholder_color)

watermark_entry.bind("<FocusIn>", on_entry_click)
watermark_entry.bind("<FocusOut>", on_focusout)


# Watermark Helper Function

def apply_watermark(input_img, show_preview=True):
    """
    Applies watermark (text or logo) to input_img.
    Returns a new Image object.
    """
    watermarked = input_img.copy()
    mode = watermark_mode.get()

    if mode == "text":
        text = watermark_entry.get()
        if not text.strip() or text == placeholder_text:
            messagebox.showerror("Error", "Please enter watermark text")
            return watermarked

        draw = ImageDraw.Draw(watermarked)
        try:
            font = ImageFont.truetype("Arial.ttf", 200)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0,0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (watermarked.width - text_width) // 2
        y = watermarked.height - text_height - 40  # bottom padding
        draw.text((x, y), text, font=font, fill=(255,255,255,128))

    elif mode == "logo":
        if logo_img is None:
            messagebox.showerror("Error", "No logo uploaded")
            return watermarked

        scale_w = watermarked.width // 6
        ratio = scale_w / logo_img.width
        resized = logo_img.resize((scale_w, int(logo_img.height * ratio)))

        # Apply white semi-transparent overlay
        tinted = Image.new("RGBA", resized.size, (255,255,255,0))
        white_overlay = Image.new("RGBA", resized.size, (255,255,255,128))
        tinted = Image.composite(white_overlay, tinted, resized.split()[3])

        x = (watermarked.width - tinted.width) // 2
        y = watermarked.height - tinted.height - 40
        watermarked.paste(tinted, (x, y), tinted)

    # If single image preview requested
    if show_preview:
        resized_preview = watermarked.copy()
        img_ratio = resized_preview.width / resized_preview.height
        preview_ratio = PREVIEW_WIDTH / PREVIEW_HEIGHT

        if img_ratio > preview_ratio:
            new_width = PREVIEW_WIDTH
            new_height = int(PREVIEW_WIDTH / img_ratio)
        else:
            new_height = PREVIEW_HEIGHT
            new_width = int(PREVIEW_HEIGHT * img_ratio)

        preview_img = resized_preview.resize((new_width, new_height))
        global tk_img
        tk_img = ImageTk.PhotoImage(preview_img)
        x_offset = PREVIEW_PADDING + (PREVIEW_WIDTH - new_width)//2
        y_offset = PREVIEW_PADDING + (PREVIEW_HEIGHT - new_height)//2
        canvas.delete("all")
        canvas.create_image(x_offset, y_offset, anchor="nw", image=tk_img)

    return watermarked


# Add Watermark Button

def add_watermark():
    global img

    if not img and not multiple_images:
        messagebox.showerror("Error", "No image uploaded")
        return

    # Single image
    if img:
        watermarked = apply_watermark(img)
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png")]
        )
        if save_path:
            if not save_path.lower().endswith(".png"):
                save_path += ".png"
            watermarked.save(save_path, format="PNG")
            messagebox.showinfo("Success", f"Watermarked image saved to {save_path}.")

    # Multiple images
    elif multiple_images:
        save_folder = filedialog.askdirectory(title="Select folder to save watermarked images")
        if not save_folder:
            return

        for path in multiple_images:
            current_img = Image.open(path).convert("RGBA")
            watermarked = apply_watermark(current_img, show_preview=False)

            # Force PNG extension
            filename = path.split("/")[-1].rsplit(".", 1)[0] + ".png"
            save_path = f"{save_folder}/{filename}"
            watermarked.save(save_path, format="PNG")

        messagebox.showinfo("Success", f"Watermarked {len(multiple_images)} images.")




watermark_button = tk.Button(root, text="Add Watermark", command=add_watermark)
watermark_button.pack(pady=10)


# Run App

root.mainloop()
