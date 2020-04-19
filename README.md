# GIF-Snake-Generator
A satisfying GIF generator that performs a Snake game

-------------------------------------------------------------------------------

## Example : 
![](render/renderGIF-Example.gif)

-------------------------------------------------------------------------------

## Installation

To run the generator, you need to install the following on your device:

* Python 3
* `imageio`
* `tkinter`

-------------------------------------------------------------------------------

## Execution

Just clone the folder and run `main.py` the main directory.

A window will open inviting you to start the generation. You will be able to follow the progress of the generation on this window. Each image will be saved in the `data` folder. When the game is finish, the window will close and the GIF generation will start. Do not kill the execution before the end of the execution. The GIF will be available in the `render` folder.

-------------------------------------------------------------------------------

### Modify the execution

It is possible to modify variables before the execution, in the `variables.py` file.

* `NBCOLUMN` and `NBROW` represent the size of the grid.
* `NBPIXELS` is the size o one element of the grid matrix.
* `COLORBACKGROUND`, `COLORFOOD`, `COLORHEAD` and `COLORTAIL` are the RGB valuies for the colors of the different obkects. (Give the same value to `COLORHEAD` and `COLORTAIL` to have a snake of the same color)