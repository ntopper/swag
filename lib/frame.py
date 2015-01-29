import cv2
import numpy as np

class frame():

        """
        represents a singe frame of video
        colects and stores relevant data
        """

        def __init__(self, top, bot, mask):

                """
                initalized with a top frame, bottom frame,
                and bottom mask array
                """
                #empty 2x2 array to hold feet positions as they are found
                self.foot_geom = np.empty([2, 2])

                self.top = top
                self.bot = bot
                self.mask = mask

                #calalculate the critical points
                valid_flag = self.calc_critical_points(top)

                #calculate the foot positions if valid
                if valid_flag:
                        self.calc_feet_positions(mask)


        def calc_critical_points(self, top):

                """
                finds the highest point on the rat's body
                returns True only if this is a valid frame

                frames are valid if the entire rat's body is on screen
                """

                #greyscale of top image, to find contours
                imgray = cv2.cvtColor(top,cv2.COLOR_BGR2GRAY)

                #find contours
                contours, hierarchy = cv2.findContours(imgray,
                        cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

                #valid frame will have contours
                if not contours:
                        self.critical_points = [None, None, None]
                        return False

                else:
                        #first, find the largest contour
                        #TODO sort and get first element for nlog(n) time
                        largest = contours[0]
                        for c in contours:
                                if len(c) > len(largest):
                                        largest = c

                        #find rightmost and topmost point

                        #TODO make this not as stupid looking
                        #rat's nose
                        rightmost =tuple(largest[largest[:,:,0].argmax()][0])[0]
                        #rat's hunch
                        topmost = tuple(largest[largest[:,:,1].argmin()][0])[0]

                        #2/7ths of the distance between the hunch and the nose
                        dist = int((rightmost - topmost) / 3.5)

                        #rear limit behind hunch
                        rear_limit = topmost - dist

                        #valid frame has the rat's full body visible
                        #and at least 10 pixles from the edges of the screen
                        h, w, d = top.shape

                        #is this frame valid?
                        valid = rightmost < w - 10 #right point must have 10px pad
                        valid = valid and rear_limit > 10        #so must rear limit

                        if not valid:
                                self.critical_points = [None, None, None]
                                return False

                        #save values and return
                        self.critical_points = [rear_limit, topmost, rightmost]
                        return True

        def calc_feet_positions(self,mask):

                """
                calculates the foot positions relitive to eachother
                by finding the extreem points of the detected feet in the given
                foot mask
                """

                #empty 2x2 array to hold feet positions as they are found
                self.foot_geom = [ [None,None] , [None,None] ]

                rear_limit, topmost, rightmost = self.critical_points

                #ignore detected values behind rear line by drawing over them
                h, w = mask.shape
                cv2.rectangle(mask, (0, 0), (rear_limit, h), 0, -1)

                #blur, to merge adjsent toes and footpads
                #TODO: for each footpad on grid, make grid mean of cirrent
                #centroid and new centroid
                mask = cv2.blur(mask, (10,10))

                if not mask.any():
                        return
                #get centroids of all contours
                if not mask.any():
                    self.foot_geom = 0
                    return

                else:
                    contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    center = lambda box: (box[0] + box[2]/2, box[1]+ box[3]/2)
                    centers = [center(cv2.boundingRect(cnt)) for cnt in contours]

                contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                center = lambda box: (box[0] + box[2]/2, box[1]+ box[3]/2)
                centers = [center(cv2.boundingRect(cnt)) for cnt in contours]

                #identify feet positions
                dstk = np.dstack(centers)[0]
                rear = np.min(dstk[0])          #rearmost x value
                front = np.max(dstk[0])         #frontmost x value
                left = np.min(dstk[1])          #leftmost y
                right = np.max(dstk[1])         #rightmost y

                for c in centers:

                        #distance to frontmost
                        front_dist = front - c[0]
                        #distance to rearmost
                        rear_dist = c[0] - rear

                        #distance to leftmost
                        left_dist = c[1] - left
                        #distance to rightmost foot
                        right_dist = right - c[1]

                        #is it closer to the front or the back?
                        x = int(front_dist <= rear_dist)

                        #is it closer to the left or the right?
                        y = int(left_dist <= right_dist)

                        #store in foot geommetry matrix
                        self.foot_geom[x][y] = c

        def get_critical_points(self):

                """returns rear_limit, topmost, rightmost"""
                return self.critical_points

        def get_foot_positions(self):

                """
                returns 2x2 array containing all detected foot positions
                element 0,0 corrispoinds to rear left foot
                missing feet are None
                """
                return self.foot_geom

def get_next_frame(trial):


        """
        pulls the next frame from a trial video instance
        and returns an instance of frame.

        retuns none if there is no data to read
        """

        ret, top, bot = trial.read()

        if not ret:
                return None

        mask = trial.get_bottom_mask()

        return frame(top, bot, mask)

#unit testing below
def debug(video):

        import trial_video
        import numpy as np


        trial = trial_video.trial_video(video)
        trial.set_horizon(245)
        trial.set_thresh_vals(98.1,98.7)

        raw =trial.get_raw_frame()[1]
        h = raw.shape[0]
        w = raw.shape[1]
        vid = np.zeros((h,w), np.uint8)

        frame_list  = list()

        while 1:
            this_frame = get_next_frame(trial)
            feet = this_frame.get_foot_positions()
            frame_list.append(feet)
            top = trial.get_top_mask()
            bot= trial.get_bottom_mask()


            print top.shape
            vid[:245,:w] = top
            vid[245:,:w] = bot
            cv2.imshow("name",vid)

            if cv2.waitKey(60) & 0xFF == ord('q'):
                break
            if not this_frame:
                    break
        trial.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":

        import sys

        video = sys.argv[1]
        debug(video)
