# I got rickroll.gif from the internet, then I trimmed the length
convert rickroll.gif -coalesce small.gif
convert -size 320x240 small.gif -resize 32x24 small.gif
# convert small.gif -colors 26 small.gif
