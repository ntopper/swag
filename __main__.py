#!/usr/bin/env python
import lib.frame as f
import lib.video_analysis as va


video = "flipped3.mp4" 
#f.debug(video)
v = va.video_analysis(video,98.1,98.7,245)
v.dostuff()



if __name__ == "__main__":

        pass