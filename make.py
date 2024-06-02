from PIL import Image, ImageSequence
import numpy as np
import sys

WIDTH, HEIGHT = sys.argv[1].split("x")
WIDTH = int(WIDTH)
HEIGHT = int(HEIGHT)
CHARS = """abcdefghijklmnopqrstuvwxyz0123456789!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

def rgb_to_hex(rgba):
    # I have removed the hashtag for compatibility
    return f"{rgba[0]:02x}{rgba[1]:02x}{rgba[2]:02x}"

def load_frames(image: Image, mode='RGBA'):
    # I got this fromn stack overflow
    return np.array([
        np.array(frame.convert(mode))
        for frame in ImageSequence.Iterator(image)
    ])

with Image.open('small.gif') as im:
    frames = load_frames(im)

TOTAL_LENGTH = len(frames)

frames = [[
    rgb_to_hex(frame[i, j])
    for i in range(HEIGHT) # Height
    for j in range(WIDTH) # Width
] for frame in frames]

colors = set()
for frame in frames:
    colors.update(frame)

colors = sorted(colors)
if len(colors) > len(CHARS):
    raise Exception(f"The GIF needs less than {len(CHARS)} colors")

# Remember to remove the #
encoder = {color: letter for color, letter in zip(colors, CHARS)}

header = "-".join(colors)
encoded = [
    [encoder[pixel] for pixel in frame]
    for frame in frames
]

with open("output.txt", "w") as f:
    # Scratch treats semicolons and commas as CSV delimeters
    f.write(f"{TOTAL_LENGTH}\n")
    f.write(f"{WIDTH}x{HEIGHT}\n")
    f.write(f"{header}\n")
    for frame in encoded:
        f.write(f"{''.join(frame)}\n")
    #for pixel in [x[1:] for xs in frames for x in xs]: # skip the # because it isn't needed in scratch
    #    f.write(f"{pixel}\n")

    # frames * width * height