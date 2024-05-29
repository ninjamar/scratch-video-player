from PIL import Image, ImageSequence
import numpy as np


def rgba_to_hex(rgba):
    return f"#{rgba[0]:02x}{rgba[1]:02x}{rgba[2]:02x}{rgba[3]:02x}"

def load_frames(image: Image, mode='RGBA'):
    # I got this fromn stack overflow
    return np.array([
        np.array(frame.convert(mode))
        for frame in ImageSequence.Iterator(image)
    ])

with Image.open('small.gif') as im:
    frames = load_frames(im)

frames = [[
    rgba_to_hex(frame[i, j])
    for i in range(24)
    for j in range(32)
] for frame in frames]

with open("output.txt", "w") as f:
    for pixel in [x[1:] for xs in frames for x in xs]: # skip the # because it isn't needed in scratch
        f.write(f"{pixel}\n")

    # frames * width * height