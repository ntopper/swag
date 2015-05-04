import cv2
import numpy as np
from arch import get_arch_data

class frame():

        """
        represents a singe frame of video
        collects and stores relevant data
        """

        def __init__(self, top, bot, mask, use_profile=True):

                """
                initalized with a top frame, bottom frame,
                and bottom mask array
                
                if not "use_profile", then the frame is always valid
                """
                self.use_profile = use_profile
                
                #empty 2x2 array to hold feet positions as they are found
                self.foot_geom = np.empty([2, 2])

                #calalculate the critical points
                self.valid_flag = self.calc_critical_points(top) or not use_profile

                #calculate the foot positions if valid
                if self.valid_flag:
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
                #unless not use_profile
                if self.use_profile:
                    h, w = mask.shape
                    cv2.rectangle(mask, (0, 0), (rear_limit, h), 0, -1)

                #blur, to merge adjsent toes and footpads
                #TODO: for each footpad on grid, make grid mean of cirrent
                #centroid and new centroid
                mask = cv2.blur(mask, (10,10))

                #is this still a valid frame?
                if not mask.any():
                        return

                else: #find all the contours
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

                        #Is there already a foot here?
                        old_foot = self.foot_geom[x][y]

                        if old_foot:
                                #if so, this value becomes the mean of
                                #the old and new feet
                                new_x = np.mean([c[0], old_foot[0]])
                                new_y = np.mean([c[1], old_foot[1]])
                        else: new_x , new_y = c

                        self.foot_geom[x][y] = [new_x, new_y]

        def calc_arch_data(self, top_mask):

            """
            calculates the 2nd degree polinomial coefficents
            and the curviture of the rat's back
            coeffs are an empty array and cuveiture is null if there is no data
            """

            self.arch_polyfit, self.arch_K = get_arch_data(self, top_mask)
            

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

        def get_valid_flag(self):
            #return if frame is valid
            return self.valid_flag

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
        import itertools

        trial = trial_video.trial_video(video)
        trial.set_horizon(255)
        trial.set_thresh_vals(98.1,98.7)

        frame_list  = list()


        while 1:
            ret, raw = trial.get_raw_frame()

            if not ret:
                break

            this_frame = get_next_frame(trial)
            feet = this_frame.get_foot_positions()
            #frame_list.append(feet)
            top = trial.get_top_mask()
            bot= trial.get_bottom_mask()
            for foot in list(itertools.chain(*feet)):
                if foot:
                        try:
                                cv2.circle(raw, (foot[0], foot[1] + 245), 20, (0, 255, 0), 5)
                        except:
                                pass

            cv2.imshow("frame",raw)

            if cv2.waitKey(60) & 0xFF == ord('q'):
                break

        trial.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":

        import sys

        video = sys.argv[1]
        debug(video)
