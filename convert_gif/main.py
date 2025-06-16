import os
from PIL import Image, ImageSequence
import numpy as np

TEMP_DIR = "temp"

def clear_temp_folder(folder=TEMP_DIR):
    """
    Clears or creates a temporary folder for storing extracted GIF frames.
    """
    if os.path.exists(folder):
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))
    else:
        os.makedirs(folder)

def extract_gif_frames(gif_path, output_folder=TEMP_DIR):
    """
    Extracts frames from an animated GIF and saves them as PNG files.
    
    Returns:
        List of file paths to the saved PNG frames.
    """
    img = Image.open(gif_path)
    frames = []
    for i, frame in enumerate(ImageSequence.Iterator(img)):
        frame = frame.convert("RGB")
        frame_path = os.path.join(output_folder, f"frame_{i}.png")
        frame.save(frame_path)
        frames.append(frame_path)
    return frames

def image_to_rgb565_array(image_path, size=(320, 240)):
    """
    Converts an RGB image to a 2D array in RGB565 format.

    Args:
        image_path (str): Path to the image file.
        size (tuple): Desired resolution (width, height).

    Returns:
        Numpy array of shape (height, width) with uint16 values in RGB565 format.
    """
    img = Image.open(image_path).convert("RGB").resize(size, Image.BILINEAR)
    data = np.array(img)
    r = (data[..., 0] >> 3).astype(np.uint16)
    g = (data[..., 1] >> 2).astype(np.uint16)
    b = (data[..., 2] >> 3).astype(np.uint16)
    rgb565 = ((r << 11) | (g << 5) | b).astype(np.uint16)
    return rgb565

def save_frames_to_header(frames, output_path="output.h", var_name="gifdata", size=(320, 240)):
    """
    Saves multiple image frames as a single C header file in RGB565 format.

    Args:
        frames (list): List of image file paths (frames).
        output_path (str): Output .h file path.
        var_name (str): Name of the variable to be used in the header.
        size (tuple): Frame resolution (width, height).
    """
    width, height = size
    with open(output_path, "w") as f:
        f.write(f"#define {var_name.upper()}_WIDTH {width}\n")
        f.write(f"#define {var_name.upper()}_HEIGHT {height}\n")
        f.write(f"#define {var_name.upper()}_FRAMES {len(frames)}\n\n")
        f.write(f"const uint16_t {var_name}[] PROGMEM = {{\n")

        for frame_path in frames:
            rgb565 = image_to_rgb565_array(frame_path, size=size)
            for y in range(height):
                for x in range(width):
                    val = rgb565[y, x]
                    f.write(f"0x{val:04X},")
                f.write("\n")
            f.write("\n")

        f.write("};\n")

def convert_gif_to_header(gif_path, output_path="output.h", var_name="gifdata", size=(320, 240)):
    """
    Main function to convert a GIF animation into a C header file containing RGB565 image data.
    
    Args:
        gif_path (str): Path to the input GIF file.
        output_path (str): Output .h file path.
        var_name (str): Variable name to be used in the header.
        size (tuple): Desired frame resolution (width, height).
    """
    clear_temp_folder()
    frames = extract_gif_frames(gif_path)
    save_frames_to_header(frames, output_path, var_name, size)

# Example usage
if __name__ == "__main__":
    convert_gif_to_header("test.gif", "test.h", "test")
