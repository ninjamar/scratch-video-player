from PIL import Image, ImageSequence
import numpy as np
import sys

WIDTH, HEIGHT = sys.argv[1].split("x")
WIDTH = int(WIDTH)
HEIGHT = int(HEIGHT)
CHARS = """abcdefghijklmnopqrstuvwxyz!"#$%&\'()*"""

def rgb_to_hex(rgba):
    # I have removed the hashtag for compatibility
    return f"{rgba[0]:02x}{rgba[1]:02x}{rgba[2]:02x}"

def load_frames(image: Image, mode='RGBA'):
    # I got this fromn stack overflow
    return np.array([
        np.array(frame.convert(mode))
        for frame in ImageSequence.Iterator(image)
    ])

def compress(data):
    result = []
    for frame in data:
        current_char = frame[0]
        total = 0
        new = ""
        for char in frame[1:]: # current-char is already frame[0]
            if char == current_char:
                total += 1
            else:
                if total - 1 > 1:
                    new = new + current_char + str(total - 1) # we have already current char is already added (part of total)
                else:
                    new = new + current_char
                total = 0
                current_char = char
        result.append(new)
    return result

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
colorLookup = {color: letter for color, letter in zip(colors, CHARS)}

header = "-".join(colors)
colorEncoded = [
    [colorLookup[pixel] for pixel in frame]
    for frame in frames
]

compressed = compress(colorEncoded)

with open("output.txt", "w") as f:
    # Scratch treats semicolons and commas as CSV delimeters
    f.write(f"{TOTAL_LENGTH}\n")
    f.write(f"{WIDTH}x{HEIGHT}\n")
    f.write(f"{header}\n")
    for frame in compressed:
        f.write(f"{''.join(frame)}\n")
    # TODO: Remove last newline of file since it might mess stuff up in scratch
    #for pixel in [x[1:] for xs in frames for x in xs]: # skip the # because it isn't needed in scratch
    #    f.write(f"{pixel}\n")

    # frames * width * height