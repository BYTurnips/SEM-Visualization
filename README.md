# Awe-SEM Visualization
Brion Ye for Professor Pease 2018

Python application intended to be run on a Raspberry Pi Model 3B+ that
controls the driving coils and reads and displays data from a low-cost
scanning electron microscope. Requires inclusion of several libraries.
Files currently in use for the product:
ProjectConstants.py [Storage of Constant Variables],
Main.py [Main controller], Gui.py [Creates GUI], 
Display.py [Processes data], Data.py [Takes data], 
WaveGen.py [Controls coils], QTD_Window.py [Helper to GUI.py],
UniversalPiAPI.py [Library for use with the Universal Pi board],
grid.png [Background Image Resource].

The application starts from Main.py.