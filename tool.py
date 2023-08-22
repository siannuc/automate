import tkinter as tk
import glob
import playsound

class Tool(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Test Application")
        self.minsize(1080, 720)

        self.grid_columnconfigure(3, minsize=200) 
        self.resizable = False

        self.timer = tk.Label(self, 
                              text = '8:00',
                              font = ('Arial',180),
                              justify='center')
        self.timer.grid(row = 0, column = 0, columnspan=4)

        self.seconds = 8*60
        self.timer_flag:bool = True

        self.start_btn = tk.Button(self, text = 'START', 
                                   command=self.start_btn_cb, 
                                   bg = 'green', 
                                   font = ('Arial',80), 
                                   width = 10)
        self.start_btn.grid(row = 1, column = 0)

        self.task_label = tk.Label(self, text = "INVESTING CYCLE", font = ('Arial',80), justify='center')
        self.task_label.grid(row = 1, column = 1, columnspan = 3)

        self.tasks = {479:{'Text':'Mixing', 'fg':'Yellow', 'Sound':None},
                      460:{'Text':'END Mixing', 'fg':'red', 'Sound':None},
                      440:{'Text':'Vacuum', 'fg':'green', 'Sound':None},
                      430:{'Text':'END', 'fg':'red', 'Sound':None}}
        
        # look for sounds
        paths = __file__.split('/')
        dir = paths[:-1].join('/') + '/sounds/'
        for file in glob.glob(dir + '*.mp3'):
            # isolate exact name
            keyword = file[len(dir):-3]

            for tk, td in self.tasks.items():
                # check if names match
                if td['Name'] == keyword:
                    td['Sound'] = file

        return

    def start_btn_cb(self,):
        # is timer running
        if self.timer_flag:
            # Start Countdown timer
            self.timer_flag = False
            self.timer_cb()
            # Change Button to stop
            self.start_btn.configure(text = 'STOP', bg = 'red')
        else:
            # reset timer
            self.timer_flag = True
            # reset button
            self.seconds = 480
            self.start_btn.configure(text = 'START', bg = 'green')
            self.task_label.configure(text = 'INVESTING CYCLE', fg = 'White')
        return
    
    def timer_cb(self):
        self.tasker()
        # convert seconds to mins and seconds
        mins = int(self.seconds / 60)
        secs = int(self.seconds % 60)
        self.timer.configure(text = '{}:{:02d}'.format(mins,secs))
        self.seconds -= 1
        if not self.timer_flag:
            self.after(1000, self.timer_cb)
        return
    
    def tasker(self):
        if not self.timer_flag:
            print('Checking, {}'.format(self.seconds))
            for key in self.tasks.keys():
                if self.seconds == key:
                    # set the task to show correctly
                    self.task_label.configure(text = self.tasks[key]['Text'],
                                            fg = self.tasks[key]['fg'])
                    # Play Sounds
                    sound = self.tasks[key]['Sound']
                    if sound is not None:
                        playsound.playsound(sound)
                    break
        else:
            self.task_label.configure(text = 'INVESTING CYCLE')

if __name__ == "__main__":
    app = Tool()
    app.mainloop()