import cv2
class video_analysis():


    def __init__(self,bot,top):
        '''
        analysis of a video frame to find 4 paws
        '''

        self.bot = bot
        self.top = top

    def segment_rat(self):
        pass











import trial_video

vidi = "GOPR0167.MP4"

def nothing():
    pass


def debug(vid):

        import cv2

        #get attribute values
        TRIAL_HORISON = 19
        TRIAL_SIDE_THRESH = 20
        TRIAL_BOT_THRESH = 21

        cv2.namedWindow("test")

        cv2.namedWindow("bottom mask")

        #trackbars
        cv2.createTrackbar('horizon','test',0,720,nothing)
        cv2.createTrackbar('top thresh','test',0,100,nothing)
        cv2.createTrackbar('bot thresh','test',0,100,nothing)

        trial = trial_video.trial_video(vid)

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
                        if (trial.get(TRIAL_SIDE_THRESH) != t or
                                        trial.get(TRIAL_BOT_THRESH) != b or
                                                trial.get(TRIAL_HORISON) != h):
                                trial.set_thresh_vals(t, b, 10)
                                trial.set_horizon(h)

                        cv2.line(frame, (0, h), (2000, h), (0, 255, 0))
                        cv2.imshow("test", frame)
                        cv2.imshow("bottom mask", trial.get_bottom_mask())
                        if cv2.waitKey(60) & 0xFF == ord('q'):
                                break

        trial.release()
        cv2.destroyAllWindows()

debug(vidi)