import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

def select_directory():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select a folder containing images")

def select_images_from_dir(directory, max_files=5):
    root = tk.Tk()
    root.withdraw()
    filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    return filedialog.askopenfilenames(
        title=f"Select up to {max_files} images",
        initialdir=directory,
        filetypes=filetypes
    )[:max_files]

def ask_output_filename():
    root = tk.Tk()
    root.withdraw()
    return filedialog.asksaveasfilename(
        title="Save combined image as",
        defaultextension=".png",
        filetypes=[("PNG image", "*.png"), ("JPEG image", "*.jpg"), ("All files", "*.*")]
    )

def combine_images_side_by_side(image_paths, output_path):
    if not image_paths:
        print("No images selected.")
        return

    images = [Image.open(path) for path in image_paths]
    min_height = min(img.height for img in images)

    resized_images = [
        img.resize((int(img.width * min_height / img.height), min_height)) for img in images
    ]

    total_width = sum(img.width for img in resized_images)
    combined_img = Image.new("RGB", (total_width, min_height))

    x_offset = 0
    for img in resized_images:
        combined_img.paste(img, (x_offset, 0))
        x_offset += img.width

    combined_img.save(output_path)
    print(f"Combined image saved to: {output_path}")

if __name__ == "__main__":
    dir_path = select_directory()
    if not dir_path:
        print("No directory selected.")
        exit()

    selected_images = select_images_from_dir(dir_path)
    if not selected_images:
        messagebox.showinfo("No images selected", "No images were selected. Exiting.")
        exit()

    output_filename = ask_output_filename()
    if not output_filename:
        print("No output filename given.")
        exit()

    combine_images_side_by_side(selected_images, output_filename)

