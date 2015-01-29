from lib.frame import *

class steps():

    FRONT = 1
    BACK = 0
    RIGHT = 1
    LEFT = 0

    def __init__(self,list_size,fps,paw_list):
        """
        initialize list of paws, size of list and 
        frame per second
        """
        #number of steps per each paw
        self.front_right_steps = 0
        self.front_left_steps = 0
        self.back_right_steps = 0
        self.back_left_steps = 0


    def set_front_right():
        """
        count the amount of  paw present 
        following right paw absence
        """
        for i in xrange(self.list_size):

            try:

                if( self.paw_list[i][FRONT][RIGHT] 
                   and not self.paw_list[i-1][FRONT][RIGHT]):
                    #if the paw was previously in the air and in now down 
                    #increment the number of steps
                    self.front_right_steps +=1

            except:
                pass

    def set_front_left():
        """
        count the amount of  paw present 
        following right paw absence
        """
        for i in xrange(self.list_size):

            try:

                if( self.paw_list[i][FRONT][LEFT] 
                   and not self.paw_list[i-1][FRONT][LEFT]):
                    #if the paw was previously in the air and in now down 
                    #increment the number of steps
                    self.front_left_steps +=1

            except:
                pass

    def set_back_right():
        """
        count the amount of  paw present 
        following right paw absence
        """
        for i in xrange(self.list_size):

            try:

                if( self.paw_list[i][BACK][RIGHT] 
                   and not self.paw_list[i-1][BACK][RIGHT]):
                    #if the paw was previously in the air and in now down 
                    #increment the number of steps
                    self.back_right_steps +=1

            except:
                pass

    def set_back_left():
        """
        count the amount of  paw present 
        following right paw absence
        """
        for i in xrange(self.list_size):

            try:

                if( not self.paw_list[i][BACK][LEFT]
                   and not self.paw_list[i-1][BACK][LEFT]):
                    #if the paw was previously in the air and in now down 
                    #increment the number of steps
                    self.back_left_steps +=1

            except:
                pass