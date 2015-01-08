from random import sample
from cv2 import VideoCapture , fillConvexPoly, cvtColor
from cv2.cv import CV_CAP_PROP_FRAME_HEIGHT, CV_CAP_PROP_FRAME_WIDTH
from cv2.cv import CV_CAP_PROP_POS_FRAMES, CV_CAP_PROP_FRAME_COUNT
from cv2 import COLOR_BGR2GRAY
from numpy import array, int32, mean, percentile, linspace, where, zeros

"""
#usage example

#read in green_bg.mp4 with horizon 200 pixles down
trial = trial_video.trial_video("green_bg.mp4", horizon=200)

#read status, top, and bottom of frame
ret, bot, top = trial.read()
"""

#get attribute values
TRIAL_HORISON = 19
TRIAL_SIDE_THRESH = 20
TRIAL_BOT_THRESH = 21

class trial_video():

        """represents an instance of a gait tracking trial from a given video
        stream"""
        def __init__ (self, video_stream, horizon = None,
                        side_thresh = 95, bot_thresh = 95):

                """
                Initalize with a video stream (filename or device number),
                and a "horison line" tupple

                top and bottom thresholds are percentile brightness thresholds
                """

                #to store last read value and unmodified video frame
                self.ret = None
                self.raw_frame = None


                #initalize capture with video_stream (filename or device number)
                self.video_capture = VideoCapture(video_stream)

                """
                horison is a tupple of two points, who when connected devide
                the mirror from the side view

                If no horison is given, horison line will partition image
                horisonaly in half
                """

                self.horizon = horizon
                if not horizon:
                        #create points from left to right at half of the height
                        self.horizon = self.video_capture.get(CV_CAP_PROP_FRAME_HEIGHT) / 2

                #set brightness threshold based on random samples
                self.set_thresh_vals(side_thresh, bot_thresh)

        def read(self):

                """
                returns a retval, the top half of the image, and the bottom
                half of the image according to the hoirson value
                """

                #read the next frame
                ret, frame = self.video_capture.read()

                #untouched frame and read status
                self.ret = ret
                self.raw_frame = frame

                if not ret:#nothing to read, end of file or error
                        return ret, None, None

                height = self.video_capture.get(CV_CAP_PROP_FRAME_HEIGHT)
                width =  self.video_capture.get(CV_CAP_PROP_FRAME_WIDTH)

                #top half of image
                top_mat = frame.copy()[0:self.horizon, 0:width]

                #bottom half of image
                bottom_mat = frame[self.horizon:height, 0:width]

                return ret, bottom_mat, top_mat

        def set_thresh_vals(self, top_thresh_percent, bot_thresh_percent, n = None):

                """
                sets the value of the top and bottom threshold values based on
                given persentiles, using a random sample of video frames

                calling this function resets the video caputre to frame zero

                n specifies sample size (frames), 
                default size is 8% of total frame count
                custom n-value is used for testing
                """

                #get current frame number, to reset
                current_frame = int(self.video_capture.get(CV_CAP_PROP_POS_FRAMES))

                #get sample frame counts
                frame_count = int(self.video_capture.get(CV_CAP_PROP_FRAME_COUNT))
                if not n:#then use default size
                        n = int(frame_count * .08) #8 percent of total frames
                sample_index = linspace(1, frame_count - 1, n)

                #calculate mean percentile over n frames
                bot_vals = []
                top_vals = []

                for i in sample_index:
                        #set caputre to frame i
                        self.video_capture.set(CV_CAP_PROP_POS_FRAMES, int(i))
                        #read top and bottom frame
                        ret, top, bot = self.read()

                        #attempt to calculate percentile from top and bottom
                        #append persentile to list
                        if ret:
                                #to catch the condition where the horizon is at
                                #the top or bottom of the frame
                                try:
                                        top_val = percentile(top, top_thresh_percent)
                                except:
                                        top_val = 0
                                try:
                                        bot_val = percentile(bot, bot_thresh_percent)
                                except:
                                        bot_val = 0

                                bot_vals.append(bot_val)
                                top_vals.append(top_val)

                #set instance variables for refrence
                self.top_thresh_percent = top_thresh_percent
                self.bot_thresh_percent = bot_thresh_percent

                #set thresh values to mean persentile
                self.side_thresh_val = int(mean(top_vals))
                self.bot_thresh_val = int(mean(bot_vals))

                #"rewind" video
                self.video_capture.set(CV_CAP_PROP_POS_FRAMES, current_frame)

        def set_horizon(self, h):
                """
                used to set horison line after initalizaton
                """
                self.horizon = h

        def get_raw_frame(self):

                """
                gets lated read value and unmodified frame
                """
                return self.ret, self.raw_frame

        def apply_brightness_mask(self, top, bottom):
                """
                uses brightness threshold and returns a mask of points who 
                exceed threshold for the top and bottom
                """

                return


        def get(self, prop):
                """
                used to retireve properties of this trial
                or properties of the VideoCaputre instance
                """
                if prop == TRIAL_HORISON:
                        return self.horizon
                if prop == TRIAL_SIDE_THRESH:
                        return self.top_thresh_percent
                if prop == TRIAL_BOT_THRESH:
                        return self.bot_thresh_percent

                #otherwise, return property of video capture
                return self.video_capture.get(prop)

        def release(self):
                """
                closes all open files
                """
                self.video_capture.release()

#tests beyond this point
def nothing(*k):
        #GIVEN ANYTHING EVER DOES ABSOLUTLY NOTHING
        pass

if __name__ == "__main__":

        import sys, cv2

        vid = sys.argv[1]
        cv2.namedWindow("test")

        #trackbars
        cv2.createTrackbar('horizon','test',0,720,nothing)
        cv2.createTrackbar('top thresh','test',0,100,nothing)
        cv2.createTrackbar('bot thresh','test',0,100,nothing)

        trial = trial_video(vid)

        while(1):

                h = cv2.getTrackbarPos('horizon','test')
                t = cv2.getTrackbarPos('top thresh','test')
                b = cv2.getTrackbarPos('bot thresh','test')

                ret, top, bot = trial.read()
                if not ret:#start over
                        #cheating
                        #python does not believe in private properties
                        #python is a left wing anarchist
                        trial.video_capture.set(CV_CAP_PROP_POS_FRAMES,0)
                        print "Resetting video"

                else:
                        ret, frame = trial.get_raw_frame()
                        if trial.get(TRIAL_HORISON) != h:
                                trial.set_horizon(h)
                        if (trial.get(TRIAL_SIDE_THRESH) != t or
                                        trial.get(TRIAL_BOT_THRESH) != b):
                                trial.set_thresh_vals(t, b, 10)

                        cv2.line(frame, (0, h), (2000, h), (0, 255, 0))
                        cv2.imshow("test", frame)
                        if cv2.waitKey(60) & 0xFF == ord('q'):
                                break

        trial.release()
        cv2.destroyAllWindows()
