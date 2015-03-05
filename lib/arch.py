import numpy as np
import cv2

def fit(arch):

    """
    returns the 3 coefficents of a 2nd degree polinomial fit to the points given in arch
    returns an empty array if there is no data in arch
    """

    if not arch:
        return np.array([])

    y, x = arch
    if not x.any():
        return np.array([])

    poly = np.polyfit(x, y, 2)
    return poly

def K(poly, x):
    
    """
    returns the crviture at point x given binomial coeeficents poly
    returns null if there is no data in poly
    """
    
    if not poly.any():
        return

    y_prime = lambda x: 2 * poly[0] * x + poly[1]
    y_prime2 = 2 * poly[0]

    return abs(y_prime2) / (1 + y_prime(x) ** 2) ** (3.0/2)

def isolate_back(frame, mask):

    """
    given a frame object and a top mask (rat profile)
    returns the isolated points along the curve of the rats back
    returns null if there is no data
    """

    
    if not frame:
        return

    copy = mask.copy()
    
    #get crititcal points
    back, apex, front = frame.critical_points
    
    if not (back and front and apex):
        return 

    #get shortest distance to apex from critical points
    dist = int(min(abs(back - apex), abs(front - apex)) * 1.5)

    #min and max x value
    min_x = apex - dist
    max_x = apex + dist

    #calculate min y value
    points = np.where(copy != 0)
    if not points[0].any():
          return
    min_y = int(np.min(points[0]) * 1.5)

    #bound with rectangles
    cv2.rectangle(copy, (0, min_y), (2000, 2000), 0, -1)
    cv2.rectangle(copy, (0, 0), (min_x, 2000), 0, -1)
    cv2.rectangle(copy, (max_x, 0), (2000, 2000), 0, -1)

    #return indexable array using canny edge finder to isolate the edge of the rat
    return np.where(cv2.Canny(copy, 100, 200) != 0)

def get_arch_data(frame, mask):

    """
    returns the polynomial coeffecients and curviture of the arch of the
    back of the rat detected, given a frame object and a top mask (rat profile)
    returns null if there is no data
    """

    #get isolated vector using calcualted limits
    arch = isolate_back(frame, mask)
    poly = fit(arch)
    
    if not poly.any():
        return np.array([]), None
    
    return poly, K(poly, frame.critical_points[1]) 
        
""" example usage
if __name__ == "__main__":

        import trial_video
        import numpy as np
        import itertools
        import frame

        trial = trial_video.trial_video("/home/nick/Desktop/gait_pics_1-5/green_bg_flipped.mp4")
        trial.set_horizon(255)
        trial.set_thresh_vals(98.1,98.7)

        frame_list  = list()

        while 1:

            ret, raw = trial.get_raw_frame()

            if not ret:
                break

            this_frame = frame.get_next_frame(trial)

            if not this_frame:
                break

            #peak of arch, for plotting
            peak = this_frame.critical_points[1]

            #isolated back, for plotting
            back = isolate_back(this_frame, trial.get_top_mask())

            #this data quantifies the arch of the rat's back
            poly, k = get_arch_data(this_frame, trial.get_top_mask())
            
            #draw the back
            if back:
                raw[back] = (100, 0, 0)

            #if there is any polinomial data
            if poly.any():
            
                #fit data to curve
                f = np.poly1d(poly) #function fits polinomial curve
                x = back[1].astype(int) #x-values of the arch
                curve = (f(x).astype(int), x) #y-values of the fitted arch
                
                #line drawn representing the inverse of the curviture, longer line = flatter back
                cv2.line(raw, (peak, int(f(peak))), (peak, int(f(peak - (k ** -1)))), (100, 0, 100),  5 )
                
                #highlight fitted curve
                raw[curve] = (0, 255, 0)

            cv2.imshow('', raw)
            if cv2.waitKey(60) & 0xFF == ord('q'):
                break
"""
