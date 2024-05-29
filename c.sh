# I got rickroll.gif from the internet, then I trimmed the length
convert rickroll.gif -coalesce small.gif
convert -size 320x240 small.gif -resize 80x60 small.gif

# This converts the each of the gif's frame to a pallete, but it isn't unified across all frames
# convert small.gif -colors 26 small.gif

# Extract all frames
convert small.gif frame_%03d.png
# Convert all the frames to a single pallete
convert frame_*.png -coalesce -append -colors 26 palette.png
# Reapply
convert frame_*.png -map palette.png small.gif
