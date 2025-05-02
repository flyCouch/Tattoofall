import cv2
import os
import tkinter as tk
from tkinter import filedialog
import sys

def create_movie_from_images(image_paths, output_movie_path, display_delay_ms, fps=2, target_size=(640, 480)):
    """
    Creates a movie from a sequence of images given their file paths, with scaling.

    Args:
        image_paths (list): A list of paths to the image files.
        output_movie_path (str): Path to save the output movie file.
        display_delay_ms (int): The delay in milliseconds each image is displayed.
        fps (int, optional): Frames per second of the output movie. Defaults to 2.
        target_size (tuple, optional): The (width, height) to which all images will be scaled.
            Defaults to (640, 480).
    """
    if not image_paths:
        print("Error: No images selected.")
        return

    # Determine the frame size from the target size
    frame_width, frame_height = target_size
    size = (frame_width, frame_height)

    # Define the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_movie_path, fourcc, fps, size)

    print(
        f"Creating movie: {output_movie_path} from selected images at {fps} FPS, with display delay {display_delay_ms} ms, scaled to {target_size}."
    )
    # Iterate through the images, display, and write to the video
    for img_path in image_paths:
        frame = cv2.imread(img_path)
        if frame is None:
            print(f"Error reading image: {img_path}. Skipping...")
            continue
        frame = cv2.resize(frame, target_size)  # Scale the image
        cv2.imshow('Image Sequence', frame)
        cv2.waitKey(display_delay_ms)
        out.write(frame)

    out.release()
    cv2.destroyAllWindows()
    print(f"Movie successfully created at: {output_movie_path}")



def main():
    """
    Main function to get user input and call the movie creation function.
    Uses a file dialog for selecting the image files and save location.
    Allows user to exit program.
    """
    root = tk.Tk()
    root.withdraw()

    # Open the file dialog to select multiple image files
    image_paths = filedialog.askopenfilenames(
        title="Select the image files",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("All files", "*.*")],
    )

    if not image_paths:
        print("Error: No image files selected. Exiting.")
        sys.exit()

    # Sort the image paths to maintain order from file dialog selection (shift-click)
    image_paths = sorted(image_paths)


    output_movie_path = filedialog.asksaveasfilename(
        title="Save the movie as...",
        defaultextension=".mp4",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")],
    )
    if not output_movie_path:
        print("Error: No output movie path selected. Exiting.")
        sys.exit()

    delay_input = input(
        "Enter the display delay in milliseconds (e.g., 500 for half a second) or type 'exit' to quit: "
    )
    if delay_input.lower() == 'exit':
        print("Exiting program.")
        sys.exit()

    fps_input = input("Enter the frames per second for the movie (default is 2) or type 'exit' to quit: ")
    if fps_input.lower() == 'exit':
        print("Exiting program.")
        sys.exit()

    scale_input = input(
        "Enter the target resolution as W,H (e.g., 640,480) or leave blank for default (640x480): "
    )
    if scale_input.lower() == 'exit':
        print("Exiting program.")
        sys.exit()

    target_size = (640, 480)  # Default
    if scale_input:
        try:
            width, height = map(int, scale_input.split(','))
            if width <= 0 or height <= 0:
                raise ValueError("Width and height must be positive integers.")
            target_size = (width, height)
        except ValueError:
            print("Invalid resolution format. Using default resolution (640x480).")



    # Validate the delay input
    if delay_input:
        try:
            display_delay_ms = int(delay_input)
            if display_delay_ms <= 0:
                raise ValueError("Display delay must be a positive integer.")
        except ValueError:
            print("Invalid display delay value. Exiting.")
            sys.exit()

    # Validate the fps input
    if fps_input:
        try:
            fps = int(fps_input)
            if fps <= 0:
                raise ValueError("FPS must be a positive integer.")
        except ValueError:
            print("Invalid FPS value. Using default FPS (2).")
            fps = 2
    else:
        fps = 2  # Default FPS



    create_movie_from_images(image_paths, output_movie_path, display_delay_ms, fps, target_size)



if __name__ == "__main__":
    main()

