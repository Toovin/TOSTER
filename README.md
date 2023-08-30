# TOSTER
Toovins Open Source Tools EXTREME REPOSITORY

First script. 
Python 3.10.6
Uses: tkinter, PIL

Goal: Quick 512x512 (default) square image extractor. Red square box over mouse location indicating "selection" to "capture". 

Current state: Not as quick, and buggy, 512x512 (default - use mouse wheel to change box size in increments of 8) square image extractor. Current Issues: 
    - Focus is not going into the proper area when program first launched. You must open an image initially (expected), and then press the "Capture" button at the top to get focus into the correct area for ANY keyboard shortcuts to work (not expected). 
    - Before pressing "c", or using arrow keys to navigate, YOU MUST PRESS "CAPTURE" AT THE TOP. Current BUG, probably ez fix, focus issue in script. 
    - The red bounding box for the capture square *SHOULD* have small text displaying the current resolution being captured. But, it doesn't. Its probably hiding behind another element/thingy. 
    - Window resizing works, but, its wonky. It attempts to scale the image, and the red bounding box SHOULD stay within the window confines, but its having problems with that. Also, ideally, the resolution of the capture box should never change due to hitting boundary. Perhaps instead of removing this behavior, have a toggle for how edge behavior is actually handled (in cases where maybe you just want that portion even if its not correct size.) Maybe more so on this though, have multiple options for selection shape. 

What next? 
    - fix current bugz
    - Features! 
       -- Metadata creation with file save?
       -- Multiple file type output (currently only jpg. Probably ez implement)
       -- Copy to Clipboard function (as opposed to capture). Sometimes easier to paste into stable-diffusion, image program, whatever. 
       -- ??? There will be more probably. 
    - Good luck.
