import numpy as np
import matplotlib.pyplot as plt

class steps():
    """
    analyze paw data retrived from 
    frame class
    """



    def __init__(self,paw_list,list_size,fps):
        """
        initialize list of paws, size of list and 
        frame per second
        """

        self.FRONT = 1
        self.BACK = 0
        self.RIGHT = 1
        self.LEFT = 0

        #plot value of paw
        self.FR = 1
        self.FL = 2
        self.BR = 3
        self.BL = 4

        self.list_size = list_size
        self.paw_list = paw_list
        self.seconds = list_size/fps


        #number of steps per each paw
        self.front_right_steps = 0
        self.front_left_steps = 0
        self.back_right_steps = 0
        self.back_left_steps = 0

        
        #create graph per foot and stride lenght
        print "starting ....."
       
        self.FR_list = list()
        self.FL_list = list()
        self.BR_list = list()
        self.BL_list = list()

        #list of stride lenghts
        self.FR_stride  = list()
        self.FL_stride = list()
        self.BR_stride = list()
        self.BL_stride = list()


        #variability
        self.FR_var = list()
        self.FL_var = list()    
        self.BR_var = list()
        self.BL_var = list()

        #cadence
        self.cadence = None

        self.analyze()

    def  analyze_front_right(self):
        """
        count the amount of  paw present 
        following right paw absence
        """

        paw_found = False
        previous_paw = 0
        current_paw = 0

        for i in xrange(self.list_size):

            try:
                
                if( self.paw_list[i][self.FRONT][self.RIGHT] 
                   and not self.paw_list[i-1][self.FRONT][self.RIGHT]):
                    #if the paw was previously in the air and in now down 
                    #increment the number of steps
                    self.front_right_steps +=1
                    paw_found = True


                    #add value to stride lenght
                    paw = self.paw_list[i][self.FRONT][self.RIGHT]
                    previous_paw = current_paw
                    current_paw = paw[0]
                    s_value = current_paw -  previous_paw
                    self.FR_stride.append(s_value)

                    
                if(self.paw_list[i][self.FRONT][self.RIGHT]):
                    #if there is a paw present add to graph array
                    value = self.FR
                    self.FR_list.append(value)

                if( not self.paw_list[i][self.FRONT][self.RIGHT]):
                    #if there was a paw in previous frame and its no longer there
                    paw_found = False
                    value = None
                    self.FR_list.append(value)

            except:
                pass

    def analyze_front_left(self):
        """
        count the amount of  paw present 
        following left paw absence
        """

        paw_found = False
        previous_paw = 0
        current_paw = 0
       
        for i in xrange(self.list_size):

            try:

                if( self.paw_list[i][self.FRONT][self.LEFT] 
                   and not self.paw_list[i-1][self.FRONT][self.LEFT]):
                    #if the paw was previously in the air and in now down 
                    #increment the number of steps
                    self.front_left_steps +=1
                    paw_found = True
                    
                    

                    #add value to stride lenght
                    paw = self.paw_list[i][self.FRONT][self.LEFT]
                    previous_paw = current_paw
                    current_paw = paw[0]
                    s_value = current_paw - previous_paw
                    self.FL_stride.append(s_value)

                if(self.paw_list[i][self.FRONT][self.LEFT] ):
                    #if there is paw present add to the graph list
                    value = self.FL
                    self.FL_list.append(value)


                if( not self.paw_list[i][self.FRONT][self.LEFT]):
                    #if there was a paw in previous frame and its no longer there
                    paw_found = False
                    value = None
                    self.FL_list.append(value)


            except:
                pass

    def analyze_back_right(self):
        """
        count the amount of  paw present 
        following right paw absence
        """

        paw_found = False
        previous_paw = 0
        current_paw = 0

        for i in xrange(self.list_size):

            try:

                if( self.paw_list[i][self.BACK][self.RIGHT] 
                   and not self.paw_list[i-1][self.BACK][self.RIGHT]):
                    #if the paw was previously in the air and in now down 
                    #increment the number of steps
                    self.back_right_steps +=1
                    paw_found = True

                    

                    #add value to stride lenght
                    paw = self.paw_list[i][self.BACK][self.RIGHT] 
                    previous_paw = current_paw
                    current_paw = paw[0]
                    s_value = current_paw - previous_paw
                    self.BR_stride.append(s_value)

                if(self.paw_list[i][self.BACK][self.RIGHT] ):
                    #if there is a paw present add to the paw graph
                    value = self.BR
                    self.BR_list.append(value)



                if( not self.paw_list[i][self.BACK][self.RIGHT]):
                    #if there was a paw in previous frame and its no longer there
                    paw_found = False
                    value = None
                    self.BR_list.append(value)

            except:
                pass

    def analyze_back_left(self):
        """
        count the amount of  paw present 
        following left paw absence
        """

        paw_found = False
        previous_paw = 0
        current_paw = 0

        for i in xrange(self.list_size):

            try:

                if( self.paw_list[i][self.BACK][self.LEFT]
                   and not self.paw_list[i-1][self.BACK][self.LEFT]):
                    #if the paw was previously in the air and in now down 
                    #increment the number of steps
                    self.back_left_steps +=1
                    paw_found = True


                    #add value to stride lenght
                    paw = self.paw_list[i][self.BACK][self.LEFT]
                    previous_paw = current_paw
                    current_paw = paw[0]
                    s_value = current_paw - previous_paw
                    self.BL_stride.append(s_value)

                if(self.paw_list[i][self.BACK][self.LEFT]):
                    #if there is a paw present add to paw graph
                    value = self.BL
                    self.BL_list.append(value)


                if( not self.paw_list[i][self.BACK][self.LEFT]):
                    #if there was a paw in previous frame and its no longer there
                    paw_found = False
                    value = None
                    self.BL_list.append(value)

            except:
                pass

    def plot_paw(self,linewidth=10):
        #draw a line on a plane representing the paw
        FR = np.array(self.FR_list)
        FL = np.array(self.FL_list)
        BR = np.array(self.BR_list)
        BL = np.array(self.BL_list)
        s_fr = FR.shape[0]
        s_fl = FL.shape[0]
        s_br = BR.shape[0]
        s_bl = BL.shape[0]
        i_fr = float(self.seconds)/float(s_fr)
        i_fl = float(self.seconds)/float(s_fl)
        i_br = float(self.seconds)/float(s_br)
        i_bl = float(self.seconds)/float(s_bl)
        x_fr = np.arange(0,self.seconds,i_fr)
        x_fl = np.arange(0,self.seconds,i_fl)
        x_br = np.arange(0,self.seconds,i_br)
        x_bl = np.arange(0,self.seconds,i_bl)


        fig, ax = plt.subplots()
        
        ax.plot(x_fr,FR,'-',label='FR',linewidth = linewidth)
        ax.plot(x_fl,FL,'-',label='FL',linewidth = linewidth)  
        ax.plot(x_br,BR,'-',label='BR',linewidth = linewidth)  
        ax.plot(x_bl,BL,'-',label='BL',linewidth = linewidth)
        
        legend = ax.legend(loc='upper right',shadow=True)
        axis = ax.axis([0,self.seconds,0,5])
        
        plt.show()
        
    def analyze(self):
        #initialize analysis of paw frame data 

        self.analyze_front_right()
        self.analyze_front_left()
        self.analyze_back_right()
        self.analyze_back_left()
   

        self.set_cadence()

        self.set_variability()
    
    def set_cadence(self):
        #total number of steps per sec
        total_steps = (self.front_left_steps + self.front_right_steps +
                      self.back_left_steps + self.back_right_steps)

        self.cadence = total_steps / self.seconds

    def set_variability(self):
        #standard div of stride lenght
        FR = np.array(self.FR_stride)
        FL = np.array(self.FL_stride)
        BR = np.array(self.BR_stride)
        BL = np.array(self.BL_stride)
        FR= np.delete(FR,0)
        FL = np.delete(FL,0)
        BR = np.delete(BR,0)
        BL = np.delete(BL,0)

        self.FR_var = np.std(FR)
        self.FL_var = np.std(FL)
        self.BR_var = np.std(BR)
        self.BL_var = np.std(BL)

    def printInfo(self):

                
        print" Cadence: %02d " % self.cadence

        print "Variability"
        print self.FR_var
        print self.FL_var
        print self.BR_var
        print self.BL_var