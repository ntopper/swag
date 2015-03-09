import lib.frame as f
from lib.trial_video import trial_video
from lib.trial_video import TRIAL_SIDE_THRESH, TRIAL_BOT_THRESH , TRIAL_HORISON , BLUR_SIGMA
from lib.steps import steps as s
from PIL import Image, ImageTk
import Tkinter as tk
import ttk as ttk
from cv2.cv import CV_CAP_PROP_POS_FRAMES, CV_CAP_PROP_FRAME_COUNT
import cv2
import tkFileDialog as tkFile
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import time
import numpy as np

class GUI():

    def __init__(self,video,top,bot,hor, parent):

        #boolean variables
        self.play_video = True
        self.show_data = False
        self.trial_ready = tk.BooleanVar()


        #some important words
        self.root = parent
        self.n = ttk.Notebook(parent,)
        self.n.pack(fill="both",expand="yes")

        self.f1 = tk.LabelFrame(self.n,text="Main") # first page with main 
        #self.f1.grid(column=0,row=0,columnspan=1,rowspan=1,padx=5, pady=5, ipadx=5, ipady=5)
        self.f1.pack(fill="both",expand="yes")
        self.canvas = tk.Canvas(self.f1)#, width=640,height=480)
        self.canvas.grid(column=0,row=0, columnspan=1,rowspan=5)

        self.f2 = tk.Frame(self.n) # second page with advanced options
        self.f2.pack()

        self.f3 = tk.Frame(self.n) #frame for graph canvas
        self.f3.pack()

        self.n.add(self.f1, text='Main')
        self.n.add(self.f2, text='Advanced')
        self.n.add(self.f3, text='Graph')


        #create menu and menu items
        self.menu = tk.Menu(self.n)
        parent.config(menu=self.menu)
        self.submenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="file", menu=self.submenu)
        self.submenu.add_command(label="Open", command = self.set_filename)
        self.submenu.add_command(label="Quit", command=parent.destroy)

        #file dialog options
        self.file_opt = options = {}
        options['defaultextension'] = ' .MP4'
        options['filetypes'] = [('all files', '.*'),('text files','.MP4')]
        options['initialdir'] = 'c:\Users\Rod\Source\Repos\swag\\'
        options['initialfile'] = 'flipped3.mp4'
        options['parent'] = self.submenu

        #file name
        self.file_name = file_name = tkFile.askopenfilename(**self.file_opt)

        #labels for 1st frame
        self.cadence_label = tk.Label(text="Cadence: ", master= self.f1)
        self.cadence_label.grid(column=1, row=1)
        self.cadence_value = tk.Label(text='0', master=self.f1)
        self.cadence_value.grid(column=2, row=1)
        self.cadence_label.columnconfigure(1,weight=1)
        self.cadence_value.columnconfigure(1,weight=1)

        self.FR_label = tk.Label(text="FR Var: ", master= self.f1)
        self.FR_label.grid(column=1, row=2)
        self.FR_value = tk.Label(text='0', master=self.f1)
        self.FR_value.grid(column=2, row=2)
        self.FR_label.columnconfigure(1,weight=1)
        self.FR_value.columnconfigure(1,weight=1)

        self.FL_label = tk.Label(text="FL Var: ", master= self.f1)
        self.FL_label.grid(column=1, row=2)
        self.FL_value = tk.Label(text='0', master=self.f1)
        self.FL_value.grid(column=2, row=2)
        self.FL_label.columnconfigure(1,weight=1)
        self.FL_value.columnconfigure(1,weight=1)

        self.BR_label = tk.Label(text="BR Var: ", master= self.f1)
        self.BR_label.grid(column=1, row=3)
        self.BR_value = tk.Label(text='0', master=self.f1)
        self.BR_value.grid(column=2, row=3)
        self.BR_label.columnconfigure(1,weight=1)
        self.BR_value.columnconfigure(1,weight=1)

        self.BL_label = tk.Label(text="BL Var: ", master= self.f1)
        self.BL_label.grid(column=1, row=4)
        self.BL_value = tk.Label(text='0', master=self.f1)
        self.BL_value.grid(column=2, row=4)
        self.BL_label.columnconfigure(1,weight=1)
        self.BL_label.columnconfigure(1,weight=1)



        #trialvideo
        self.increment = 0

        self.trial = trial_video(self.file_name)
        self.count = self.trial.get(CV_CAP_PROP_FRAME_COUNT)
        print "Count %02d" % self.count
        self.trial.set_horizon(hor)
        self.trial.set_thresh_vals(top,bot)
        self.frame_list = list()

        #get height ratio needed for horizon line
        self.trial.set(CV_CAP_PROP_POS_FRAMES,self.count/2)
        self.top = self.trial.get_top_mask()
        self.height_i = self.top.shape[0]
        self.top = self.trial.resize_frame(self.top, 300)
        self.height_f = self.top.shape[0]
        self.h_ratio = self.height_f / self.height_i


        self.side_thresh = self.trial.get(TRIAL_SIDE_THRESH)
        self.bot_thresh = self.trial.get(TRIAL_BOT_THRESH)
        self.hor_value = hor
        self.blur_thresh = self.trial.get(BLUR_SIGMA)

        self.advance_settings()


    def update_video(self):
        #do more stuff
        raw = self.trial.get_raw_frame()
        raw=self.trial.resize_frame(raw[1],500)
        self.canvas.config(width=raw.shape[1],height=raw.shape[0])
        self.bgr = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
        self.a = Image.fromarray(self.bgr)
        self.b = ImageTk.PhotoImage(image= self.a)
        self.canvas.create_image(0,0,image=self.b,anchor=tk.NW)
        self.increment += 1
        self.root.update()
        self.this_frame = f.get_next_frame(self.trial)
        try:
            if(self.this_frame.get_valid_flag()):
                self.feet = self.this_frame.get_foot_positions()
                self.frame_list.append(self.feet)

            
        except:
            pass
        self.dostuff()
        self.root.after(33,self.update_video)

    def update_main(self):
        #update main tab

        if self.play_video and self.trial_ready.get():
            print " i am playing video"
            self.update_video()

        if not self.trial_ready.get():
            print " i am looping main"
            self.visual_threshold()
            
    def dostuff(self):

        if (self.increment  >= self.count) and (self.show_data == False):
            list_size = len(self.frame_list)
            print " i got past this"
            self.steps = s(self.frame_list,list_size,29)
            #steps.get_FR()
            
            c,fr,fl,br,bl = self.steps.get_variable()
            self.cadence_value['text'] = str(c)
            self.FR_value['text'] = str(fr)
            self.FL_value['text'] = str(fl)
            self.BR_value['text'] = str(br)
            self.BL_value['text'] = str(bl)
            figure =self.steps.plot_paw()
            self.graph(figure)
            self.show_data = True
            self.play_video = False

    def do_nothing(self):
        pass

    def set_filename(self):
        #return name of the open file

        file_name = tkFile.askopenfilename(**self.file_opt)

        self.file_name = file_name

        self.reset_video()
        self.play_video = True

    def graph(self,figure):
        """embed matplot graph to tkinter canvas"""
        self.graph_canvas = tk.Canvas(self.f3,width=640,height=480)
        self.graph_canvas.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
        

        self.canvas2 = FigureCanvasTkAgg(figure,self.graph_canvas)
        self.canvas2.show()
        self.canvas2.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)
        
        self.toolbar = NavigationToolbar2TkAgg(self.canvas2,self.f3)
        self.toolbar.update()
        self.canvas2._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)    

    def reset_video(self):
        '''
        set frame current frame to 0
        reset all data variables
        '''
        self.trial.set(CV_CAP_PROP_POS_FRAMES,0)
        self.increment = 0
        self.frame_list[:] = []
        self.show_data = False

        #reset labels
        self.cadence_value['text'] = ""
        self.FR_value['text'] = ""
        self.FL_value['text'] = ""
        self.BR_value['text'] = ""
        self.BL_value['text'] = ""

        #reset graph canvas
        try:
            self.graph_canvas.destroy()
            self.toolbar.destroy()
        except:
            pass


        

    def advance_settings(self):
        """
        GUI for user setting, contains
        canvas for horizon , top and bot thresh
        also slider and lable buttton to set trial_ready
        """
        t_var = tk.StringVar(self.root)
        t_var.set(str(self.side_thresh))

        b_var = tk.StringVar(self.root)
        b_var.set(str(self.bot_thresh))

        h_var = tk.StringVar(self.root)
        h_var.set(str(self.hor_value))

        bl_var = tk.StringVar(self.root)
        bl_var.set(str(self.blur_thresh))


        self.top_canvas = tk.Canvas(self.f2,width=100,height=100)
        self.bot_canvas = tk.Canvas(self.f2,width=100,height=100)


        self.horizon_label = tk.Label(text="Horizon Value: ", master= self.f2)
        self.top_label = tk.Label(text= "Top_Thresh Value: ", master= self.f2)
        self.bot_label = tk.Label(text= "Bot_Thresh Value: ", master= self.f2)
        self.blur_label = tk.Label(text=" Blur : ", master=self.f2)

        self.horizon_value = tk.Spinbox(self.f2)
        self.horizon_value.configure(from_=0,to =1000, increment = 1, width=5, textvariable=h_var)
        self.horizon_value.configure(font = ('San', '18', 'bold'))


        self.top_value = tk.Spinbox(self.f2)
        self.top_value.configure(from_ =0,to = 100, increment=0.1, width=5,textvariable=t_var)
        self.top_value.configure(font = ('San', '18', 'bold'))

        self.bot_value = tk.Spinbox(self.f2)
        self.bot_value.configure(from_ =0, to=100, increment=0.1, width=5,textvariable=b_var)
        self.bot_value.configure(font = ('San', '18', 'bold'))

        self.blur_value = tk.Spinbox(self.f2)
        self.blur_value.configure(from_ =0, to=100, increment=1, width=5, textvariable=bl_var)
        self.blur_value.configure(font = ('San', '18', 'bold'))


        self.top_canvas.grid(column=0, row=1, columnspan=2)
        self.bot_canvas.grid(column=0, row=2, columnspan=2)


        self.horizon_label.grid(column=2, row=0, pady=30)
        self.top_label.grid(column=2, row=1)
        self.bot_label.grid(column=2, row=2)
        self.blur_label.grid(column=0, row=0, pady=30)

        self.trial_ready_checkbox = tk.Checkbutton(self.f2,text="Trial Ready",variable=self.trial_ready, command=self.set_trial_ready)
        self.trial_ready_checkbox.grid(column=0,row=3)

        self.horizon_value.grid(column=3, row=0, pady=30)
        self.top_value.grid(column=3, row=1)
        self.bot_value.grid(column=3, row=2)
        self.blur_value.grid(column=1, row=0, pady=30)

    def visual_threshold(self):
        '''
        visual for advanced setting 
        '''
        
        #set top threshold 
        top = self.trial.get_top_mask()
        top =self.trial.resize_frame(top,300)
        self.top_canvas.config(width=top.shape[1],height=top.shape[0])
        self.a = Image.fromarray(top)
        self.b = ImageTk.PhotoImage(image= self.a)
        self.top_canvas.create_image(0,0,image=self.b,anchor=tk.NW)

        #set bot threshold
        bot = self.trial.get_bottom_mask()
        bot =self.trial.resize_frame(bot,300)
        self.bot_canvas.config(width=bot.shape[1],height=bot.shape[0])
        self.a_b = Image.fromarray(bot)
        self.b_b = ImageTk.PhotoImage(image= self.a_b)
        self.bot_canvas.create_image(0,0,image=self.b_b,anchor=tk.NW)

        #update cavas
        self.root.update()
        self.trial.set(TRIAL_SIDE_THRESH,float(self.top_value.get()))
        self.trial.set(TRIAL_BOT_THRESH,float(self.bot_value.get()))
        self.trial.set(TRIAL_HORISON,float(self.horizon_value.get()))
        self.trial.set(BLUR_SIGMA,float(self.blur_value.get()))
        self.this_frame = f.get_next_frame(self.trial)
        #self.root.after(33,self.visual_threshold)

        if not self.trial_ready.get():
            self.root.after(33 ,self.visual_threshold)     
        else:
            self.root.after(33,self.update_main)



    def set_trial_ready(self):
        #change the state of  trial ready

        if self.trial_ready.get() == False:
            self.top_value.configure(state ="normal")
            self.bot_value.configure(state="normal")
        else:
            self.top_value.configure(state ="disabled")
            self.bot_value.configure(state="disabled")
            self.reset_video()