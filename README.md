# Watermark App

This is my first desktop app using Python and Tkinter. It lets you upload one or multiple images and add a watermark automatically.

I made this in the context of a course I'm attending. It's an easy way to watermark photos before posting them online.

Features

Upload any image (PNG, JPG, JPEG).

Upload multiple images at once and apply the same watermark to all of them.

Add a text watermark.

Add a logo watermark with automatic semi-transparent white overlay.

Center the watermark or place it at the bottom with padding.

Preview the image before saving (for single images).

Save watermarked images as PNG to preserve transparency. JPEG is only supported for images without transparency.

How to Use

Open the app:

python3 watermark.py


Click Upload Image to select one or more pictures.

(Optional) Click Upload Logo to use a logo as a watermark. Ensure the logo is a PNG with transparency.

Type your watermark text in the input box (if using text).

Click Add Watermark to apply it.

For a single image: a save dialog will appear.

For multiple images: select a folder to save all watermarked images.

All watermarked images are saved as PNG by default to preserve transparency.

Notes

The text input has placeholder text that disappears when you click on it.

The watermark is semi-transparent by default, so it doesn’t cover the image completely.

Logo watermarks are automatically converted to semi-transparent white to ensure visibility on any image.

Single-image previews are displayed in the app; multiple-image uploads skip previews for efficiency.

Requirements

Python 3.14+

Pillow (install via pip install Pillow)