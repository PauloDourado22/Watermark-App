# Watermark App
Watermark App (Tkinter)

This project is a desktop application built with Python, Tkinter, and Pillow (PIL).
It allows users to load one or multiple images, preview them, and apply either a text watermark or a logo watermark before exporting the final watermarked images.

Features
✔️ Image Upload

Upload single or multiple images

Automatically previews the first selected image

Displays a thumbnail strip with a stacked preview effect for multiple images

✔️ Watermark Options

You can choose between two watermark modes:

Text Watermark

Custom text input

Text positioning: Center, corners, or edges

Adjustable via a centered dropdown selection

Logo Watermark

Upload a PNG logo with transparency

Logo automatically scaled

Optionally combined with a semi-transparent white overlay

Positionable just like the text watermark

✔️ Live Preview

The selected image with watermark is previewed on a dedicated canvas

Thumbnails are shown on a separate strip

Preview always updates when applying a watermark

✔️ Batch Processing

When multiple images are uploaded, the watermark is applied to all of them and saved as individual files.

Requirements

Python 3.x

Pillow (pip install pillow)

Tkinter (bundled with most Python installations)

How to Run
python watermark_app.py

File Output

All exported images are saved as PNG to preserve transparency and watermark quality.