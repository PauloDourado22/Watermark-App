# Watermark App

This is my first desktop app using Python and Tkinter. It lets you upload an image and add a watermark automatically.

I made this in the context of a course I'm attending. It's an easy way to watermark photos before posting them online.



Features

Upload any image (PNG, JPG, JPEG).

Add a text watermark.

Center the watermark or put it at the bottom-right with some padding.

Preview the image before saving.

Save the watermarked image as PNG or JPEG.



How to Use

Open the app (python3 watermark.py).

Click Upload Image to select your picture.

Type your watermark in the input box.

Click Add Watermark to apply it.

Choose where to save the watermarked image.



Notes

The text input has placeholder text that disappears when you click on it.

The watermark is semi-transparent by default, so it doesn’t cover the image completely.

Make sure the logo file has transparency (PNG) so it looks good on your images.

I used Pillow for image processing and Tkinter for the GUI.



Requirements

Python 3.14+

Pillow (pip install Pillow)



Future Improvements

Let users choose font size, color, and opacity.

Add drag-and-drop to position watermark manually.

Batch process multiple images at once.

Make the app look nicer with better styling.
