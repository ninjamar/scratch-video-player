# Usage: bash conv.sh input.gif inputDimensions output.gif outputDimensions
# Replace rickroll.gif with whatever gif you want to use
convert $1 -coalesce $3

# Change 1280x720 to the size of the gif that you have
# Change 96x54 to the target size
convert -size $2 $3 -resize $4 $3

# Extract all frames
convert small.gif frame_%03d.png

# Convert all the frames to a single pallete
# I know GIFs can only support 256 colors, but rickroll.gif seems to have more
# If you know the input gif has 256 colors, you don't need to extract all frames
# and convert the color palette
convert frame_*.png -coalesce -append -colors 36 palette.png

# Reapply
convert frame_*.png -map palette.png small.gif

# Remove all generated files
rm frame_*.png
rm palette.png