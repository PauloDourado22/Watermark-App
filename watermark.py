import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

PREVIEW_WIDTH = 300
PREVIEW_HEIGHT = 300
PREVIEW_PADDING = 20


# GUI setup
root = tk.Tk()
root.title("Watermark App")
watermark_mode = tk.StringVar(value="text") # this is the default mode
logo_img = None
logo_path = None

mode_frame = tk.Frame(root)
mode_frame.pack(pady=5)

tk.Radiobutton(mode_frame, text="Text Watermark", variable=watermark_mode, value="text").pack(side="left")
tk.Radiobutton(mode_frame, text="Logo Watermark", variable=watermark_mode, value="logo").pack(side="left")

# Button to upload logo
def upload_logo():
    global logo_img, logo_path
    logo_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    if logo_path:
        logo_img = Image.open(logo_path).convert("RGBA")
        messagebox.showinfo("Logo Loaded", "Logo loaded successfully.")

upload_logo_button = tk.Button(root, text="Upload Logo", command=upload_logo)
upload_logo_button.pack(pady=5)

# Canvas to show image
canvas = tk.Canvas(root, width=PREVIEW_WIDTH + 2*PREVIEW_PADDING, height=PREVIEW_HEIGHT + 2*PREVIEW_PADDING)
canvas.pack()

# Upload image to the app
def upload_image():
    global img, img_path, tk_img
    img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpeg *.jpg")])
    if img_path:
        img = Image.open(img_path)
        
        # Resize for preview inside padded canvas
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

        # Center image inside the canvas with padding
        x_offset = PREVIEW_PADDING + (PREVIEW_WIDTH - new_width)//2
        y_offset = PREVIEW_PADDING + (PREVIEW_HEIGHT - new_height)//2

        canvas.delete("all")
        canvas.create_image(x_offset, y_offset, anchor="nw", image=tk_img)

        print("Button clicked")  # debugging

# Function to add watermark
def add_watermark():
    global img, logo_img

    if not img:
        messagebox.showerror("Error", "No image uploaded")
        return

    mode = watermark_mode.get()
    watermarked = img.copy()

    if mode == "text":
        text = watermark_entry.get()
        if not text.strip() or text == "Enter your watermark here":
            messagebox.showerror("Error", "Please enter watermark text")
            return 

        draw = ImageDraw.Draw(watermarked)
        
        # Choose font and size
        font = ImageFont.truetype("Arial.ttf", 200)
    
    
        # Text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Center bottom position
        x = (watermarked.width - text_width) // 2
        y = watermarked.height - text_height - 40  # 40px padding from bottom

        # Draw the text
        draw.text((x, y), text, font=font, fill=(255,255,255,128)) # white with transparency

    elif mode == "logo":
        if logo_img is None:
            messagebox.showerror("Error", "No logo uploaded.")
            return
        
        # Resize logo (10% of image width)
        scale_w = watermarked.width // 6
        ratio = scale_w / logo_img.width
        resized = logo_img.resize((scale_w, int(logo_img.height * ratio)))

        # ---- Apply white transparency to the logo ----
        # Convert the logo to RGBA 
        tinted = Image.new("RGBA", resized.size, (255, 255, 255, 0))
        white_overlay = Image.new("RGBA", resized.size, (255, 255, 255, 128)) # 50% opacity

        # Keep the shape by using its alpha channel as a mask
        tinted = Image.composite(white_overlay, tinted, resized.split()[3])

        # Position centered bottom
        logo_width, logo_height = tinted.size
        bottom_padding = 200

        x = (watermarked.width - logo_width) // 2
        y = watermarked.height - logo_height - bottom_padding
        
        watermarked.paste(tinted, (x, y), tinted)
    
    # Save the watermarked final image
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])

    if save_path:
        watermarked.save(save_path)
        messagebox.showinfo("Success", f"Watermarked image saved to {save_path}.")
    

# Upload button
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

# Watermark input
placeholder_text = "Enter your watermark here"
placeholder_color = "grey"

watermark_entry = tk.Entry(root, fg=placeholder_color)
watermark_entry.pack(pady=10)

# Insert placeholder
watermark_entry.insert(0, placeholder_text)

# Focus-in: remove placeholder
def on_entry_click(event):
    if watermark_entry.get() == placeholder_text:
        watermark_entry.delete(0, "end")
        watermark_entry.config(fg="black") # normal text color

# Focus-out: restore placeholder
def on_focusout(event):
    if watermark_entry.get() == "":
        watermark_entry.insert(0, placeholder_text)
        watermark_entry.config(fg=placeholder_color)

# Bind events
watermark_entry.bind("<FocusIn>", on_entry_click)
watermark_entry.bind("<FocusOut>", on_focusout)

# Watermark button
watermark_button = tk.Button(root, text="Add Watermark", command=add_watermark)
watermark_button.pack(pady=10)

img = None
img_path = None
tk_img = None

root.mainloop()