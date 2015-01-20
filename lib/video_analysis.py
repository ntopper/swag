import cv2

def ImageResize(frame):
    #maintaing aspec ratio... keeps image from distorting

    r = 1000.0 / frame.shape[1]
    dim = (1000, int(frame.shape[0]*r))

    #resizing of the image
    resized = cv2.resize(frame,dim,interpolation = cv2.INTER_AREA)



         

vid = "GOPR0167.MP4"

video = trial_video.debug(vid)


