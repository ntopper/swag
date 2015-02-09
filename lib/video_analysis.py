import frame
from trial_video import trial_video
from steps import steps as s
import itertools
import numpy as np
import cv2

class video_analysis():
    """
    analyze video using frame and steps classes
    """
    def __init__(self,video,top,bot,hor):
        
        trial = trial_video(video)
        trial.set_horizon(hor)
        trial.set_thresh_vals(top,bot)

        print "i made it past trial_video"

        frame_list = []
        

        while 1:
            ret, raw = trial.get_raw_frame()
        
            cv2.imshow("frame",raw[1])
            if not ret:
                break

            this_frame = frame.get_next_frame(trial)
            try:

                if this_frame.get_valid_flag() :
                    feet = this_frame.get_foot_positions()
                    frame_list.append(feet)
            except:
                break

            

        list_size = len(frame_list)
        print " i got past this"
        self.steps = s(frame_list,list_size,29)
    def dostuff(self):

        #steps.get_FR()
        self.steps.printInfo()
        #self.steps.plot_paw()







        

