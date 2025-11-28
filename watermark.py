import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

PREVIEW_WIDTH = 300
PREVIEW_HEIGHT = 300
PREVIEW_PADDING = 20

# GUI setup
root = tk.Tk()
root.title("Watermark App")

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
    if not img_path:
        messagebox.showerror("Error", "No image uploaded")
        return

    water_text = watermark_entry.get()
    if not water_text:
        messagebox.showerror("Error", "Please enter watermark text")
        return
    
    # Convert image to RGBA
    watermarked = img.convert("RGBA")

    # Transparent layer the same size as the image
    txt_layer = Image.new("RGBA", watermarked.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Choose font and size
    font = ImageFont.truetype("Arial.ttf", 200)
    
    # Text width and height
    bbox = draw.textbbox((0, 0), water_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Right bottom corner position
    x = (watermarked.width - text_width) // 2

    bottom_padding = 200
    y = watermarked.height - text_height - bottom_padding

    # Draw the text
    draw.text((x, y), water_text, font=font, fill=(255,255,255,128)) # white with transparency

    # Merge layers 
    watermarked = Image.alpha_composite(watermarked, txt_layer)
    
    # Save the watermarked final image
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])

    if save_path:
        if save_path.lower().endswith(".jpg"):
            watermarked = watermarked.convert("RGB")
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