import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, messagebox, ttk
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
tk_thumbnails = None
tk_thumbnails = []

# GUI Setup

root = tk.Tk()
root.title("Watermark App")

default_font = tkFont.Font(family="Helvetica", size=12)
root.option_add("*Font", default_font)

watermark_mode = tk.StringVar(value="text")  # default mode


# Mode Selection

mode_frame = ttk.Frame(root)
mode_frame.pack(pady=5)

ttk.Radiobutton(mode_frame, text="Text Watermark", variable=watermark_mode, value="text").pack(side="left", padx=10)
ttk.Radiobutton(mode_frame, text="Logo Watermark", variable=watermark_mode, value="logo").pack(side="left", padx=10)


# Upload Logo

def upload_logo():
    global logo_img, logo_path
    logo_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    if logo_path:
        logo_img = Image.open(logo_path).convert("RGBA")
        messagebox.showinfo("Logo Loaded", "Logo loaded successfully.")

# Canvas for Preview

preview_frame = ttk.Frame(root)
preview_frame.pack(pady=10, padx=10)

preview_label = ttk.Label(preview_frame, text="Preview")
preview_label.pack()

canvas = tk.Canvas(
    preview_frame, 
    width=PREVIEW_WIDTH + 2 * PREVIEW_PADDING, 
    height=PREVIEW_HEIGHT + 2 * PREVIEW_PADDING, 
    bg="lightgray", 
    relief="flat", 
    bd=2
)
canvas.pack(anchor="center")

thumb_strip = tk.Canvas(
    root,
    height=80,
    bg="lightgray",
    highlightthickness=0
)

thumb_strip.pack()

# Upload Images (single or multiple)

def upload_image():
    global img, img_path, tk_img, multiple_images, tk_thumbnails, thumb_strip
    paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png *.jpeg *.jpg")])
    if not paths:
        return

    multiple_images = list(paths)

    # Always preview the first image
    img_path = multiple_images[0]
    img = Image.open(img_path)

    # Update upload count label
    upload_count_label.config(text=f"Images uploaded: {len(multiple_images)}")

    # Main Preview
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

    canvas.delete("all")

    # Center main preview
    x_offset = PREVIEW_PADDING + (PREVIEW_WIDTH - new_width) // 2
    y_offset = PREVIEW_PADDING + (PREVIEW_HEIGHT - new_height) // 2

    canvas.create_image(x_offset, y_offset, anchor="nw", image=tk_img)

    print("Single image loaded.")
    
    # ---- Thumbnail strip for multiple images ----
    thumb_strip.delete("all")
    tk_thumbnails = []

    if len(multiple_images) > 1:
        thumbnail_size = 70
        overlap = 45

        x_offset_thumbs = 10
        y_offset_thumbs = 5

        for path in multiple_images[:10]: # Show up to 10 stacked thumbnails
            thumb_img = Image.open(path)
            thumb_img.thumbnail((thumbnail_size, thumbnail_size), Image.Resampling.LANCZOS)
            tk_thumb = ImageTk.PhotoImage(thumb_img)
            tk_thumbnails.append(tk_thumb)

            thumb_strip.create_image(x_offset_thumbs, y_offset_thumbs, anchor="nw", image=tk_thumb)
            x_offset_thumbs += overlap


        messagebox.showinfo("Images Loaded", f"{len(multiple_images)} images selected.")
        print(f"Loaded {len(multiple_images)} images.")

upload_button = ttk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

# Label to show upload count
upload_count_label = ttk.Label(root, text="Images uploaded: 0", foreground="white")
upload_count_label.pack(pady=5)

upload_logo_button = ttk.Button(root, text="Upload Logo", command=upload_logo)
upload_logo_button.pack(pady=5)


# Watermark Input with Placeholder

placeholder_text = "Enter your watermark text"
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

# Watermark Position Selection
position_label = ttk.Label(root, text="Watermark Position: ")
position_label.pack(pady=(5, 0))

# Centered Combobox Style
style = ttk.Style()
style.configure("Centered.TCombobox", justify="center")

position_var = tk.StringVar()
position_combination = ttk.Combobox(
    root,
    textvariable= position_var,
    state="readonly",
    width=20,
    values= [
        "Center",
        "Top-Left",
        "Top-Center",
        "Top-Right",
        "Bottom-Left",
        "Bottom-Center",
        "Bottom-Right"
    ],
    style="Centered.TCombobox",
    justify="center" 
)
position_combination.current(0)
position_combination.pack(pady=10)

# Center the text in the entry field
position_combination.configure(justify="center")

# Center items in the dropdown list (Combobox's internal Listbox)
root.option_add("*TCombobox*Listbox.justify", "center")

# Hover cursor effect
def on_combo_enter(event):
    position_combination.config(cursor="hand2")

def on_combo_leave(event):
    position_combination.config(cursor="arrow")

def on_combo_motion(event):
    position_combination.config(cursor="hand2")

position_combination.bind("<Enter>", on_combo_enter)
position_combination.bind("<Leave>", on_combo_leave)
position_combination.bind("<Motion>", on_combo_motion)

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

        pos = position_var.get()
        padding = 40

        if pos == "Center":
            x = (watermarked.width - text_width) // 2
            y = (watermarked.height - text_height) // 2
        elif pos == "Top-Left":
            x, y = 20, 20
        elif pos == "Top-Center":
            x = (watermarked.width - text_width) // 2
            y = 20
        elif pos == "Top-Right":
            x = watermarked.width - text_width - 20
            y = 20
        elif pos == "Bottom-Left":
            x = 20
            y = watermarked.height - text_height - 20
        elif pos == "Bottom-Center":
            x = (watermarked.width - text_width) // 2
            y = watermarked.height - text_height - 20
        elif pos == "Bottom-Right":
            x = watermarked.width - text_width - 20
            y = watermarked.height - text_height - 20
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

        pos = position_var.get()
        if pos == "Center":
            x = (watermarked.width - tinted.width) // 2
            y = (watermarked.height - tinted.width) // 2
        elif pos == "Top-Left":
            x, y = 20, 20
        elif pos == "Top-Center":
            x = (watermarked.width - tinted.width) // 2
            y = 20
        elif pos == "Top-Right":
            x = watermarked.width - tinted.width - 20
            y = 20
        elif pos == "Bottom-Left":
            x = 20
            y = watermarked.height - tinted.height - 20
        elif pos == "Bottom-Center":
            x = (watermarked.width - tinted.width) // 2
            y = watermarked.height - tinted.height - 20
        elif pos == "Bottom-Right":
            x = watermarked.width - tinted.width - 20
            y = watermarked.height - tinted.height - 20
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


watermark_button = ttk.Button(root, text="Add Watermark", command=add_watermark)
watermark_button.pack(pady=10)


# Run App

root.mainloop()
