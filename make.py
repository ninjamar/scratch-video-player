# Usage: python3 make.py output.gif WIDTHxHEIGHT output.txt

from PIL import Image, ImageSequence
import numpy as np
import sys

CHARS = """abcdefghijklmnopqrstuvwxyz!"#$%&'()*"""

def rgb_to_hex(rgba):
    # I have removed the hashtag for compatibility
    return f"{rgba[0]:02x}{rgba[1]:02x}{rgba[2]:02x}"

def load_frames(image: Image, mode='RGBA'):
    # I got this fromn stack overflow
    return np.array([
        np.array(frame.convert(mode))
        for frame in ImageSequence.Iterator(image)
    ])

def rle_compress(data):
    #result = []
    #for frame in data:
    current_char = data[0]
    total = 0
    new = ""
    for char in data[1:]: # current_char is already data[0]
        if char == current_char:
            total += 1
        else:
            # TODO: If total = 1, then add current char twice (doesn't save any characters by encoding)
            if total > 0:
                new = new + current_char + str(total) # we have already current char is already added (part of total)
            else:
                new = new + current_char
            total = 0
            current_char = char

def make(fpath, width, height, output_path):
    with Image.open(fpath) as im:
        frames = load_frames(im)

    frames = [[
        rgb_to_hex(frame[i, j])
        for i in range(height) # Height
        for j in range(width) # Width
    ] for frame in frames]

    colors = set()
    for frame in frames:
        colors.update(frame)

    colors = sorted(colors)
    if len(colors) > len(CHARS):
        raise Exception(f"The GIF needs less than {len(CHARS)} colors")

    # Remember to remove the #
    colorLookup = {color: letter for color, letter in zip(colors, CHARS)}
    colorEncoded = [
        [colorLookup[pixel] for pixel in frame]
        for frame in frames
    ]

    with open(output_path, "w") as f:
        # Scratch treats semicolons and commas as CSV delimeters
        f.write(f"{width}x{height}\n")
        f.write(f"{CHARS}\n")
        f.write(f"{'-'.join(colors)}\n") # colors
        # 3 lines for headers
        for frame in "".join([rle_compress(frame) for frame in colorEncoded]):
            f.write(f"{''.join(frame)}\n")

if __name__ == "__main__":
    FPATH = sys.argv[1]
    WIDTH, HEIGHT = sys.argv[2].split("x")
    OUTPUT_PATH = sys.argv[3]

    WIDTH = int(WIDTH)
    HEIGHT = int(HEIGHT)

    make(FPATH, WIDTH, HEIGHT, OUTPUT_PATH)