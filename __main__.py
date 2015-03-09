#!/usr/bin/env python
import lib.frame as f
import lib.video_analysis as va
import cv2
import Tkinter as tk
from lib.testGUI import testGUI


video = "flipped3.mp4" 
#f.debug(video)

root = tk.Tk()
root.wm_title("Gaitor")
x = testGUI.GUI(video,98.1,98.7,245,root)
root.after(0,x.update_main)
x.dostuff()
root.mainloop()



if __name__ == "__main__":

        pass