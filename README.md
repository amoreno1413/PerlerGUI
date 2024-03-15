Original Python script done by [dylan-lawrence](https://github.com/dylan-lawrence)

# Perler GUI
This is a python app that takes in a pixel art image, and converts the pixel colors to perler colors. The GUI displays the converted image as well as a key of the colors and number of perler beads needed.

![alt text](https://github.com/amoreno1413/PerlerGUI/blob/main/example.png "GUI example")

# How To Use
  1. Make a pixel art image [here](https://www.pixilart.com/draw)
  2. Open the GUI and select the proper pixel size

# TODO
  1. Make color key larger
  2. Currently, displaying the images requires converting from PIL to PyQT image, PIL has a PyQT fork, but I wasn't able to get the fork to work.

# Limitations
Uploading a pixel image from the web to the GUI will not convert it properly, so the user has to make a pixel art image for the [pixel2perler](https://github.com/dylan-lawrence/pixel2perler) script to work properly.
