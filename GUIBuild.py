import tkinter as tk
from functools import partial

class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)

class MainApplication:

    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=500, height=400)
        # to make a frame
        self.frame = tk.Frame(master, bg='white')

        # to place a menu item in the window
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)

        ############################################################################################

        self.button_frame = tk.Frame(self.frame, bd='10', padx=3, pady=3)
        self.button_info = tk.Label(self.button_frame, text='Choose a gamemode', bd='3', fg='black',font='Helvetica 9 bold')
        self.gamemode_button_6v6 = tk.Button(self.button_frame, text='6v6', bd='2', fg='black', activebackground='grey',
                                             bg='white', padx='10', pady='10', font='Helvetica 15 bold',
                                             command=self.Classic_Hijack_Skillcontrib)
        self.gamemode_button_9v9 = tk.Button(self.button_frame, text='9v9', bd='2', fg='black', activebackground='grey',
                                             bg='white', padx='10', pady='10', font='Helvetica 15 bold',
                                             command=self.HL_Hijack_Skillcontrib)

        self.button_info.place(relx=0.38, rely=0.05, relheight=0.25)
        self.gamemode_button_6v6.place(relx=0.2, rely=0.5, relheight=0.25)
        self.gamemode_button_9v9.place(relx=0.7, rely=0.5, relheight=0.25)

        ###############################################################################################
        # all the frames are placed in their respective positions
        self.button_frame.place(relx=0.005, rely=0.005, relwidth=0.99,relheight=0.5)

        self.frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        self.canvas.pack()
        ##############################################################################################

    def Classic_Hijack_Skillcontrib(self):
        self.gamemode_button_6v6.config(state='disabled')
        self.gamemode_button_9v9.config(state='disabled')
        self.input_frame = tk.Frame(self.frame, bd='10', padx=3, pady=3)
        self.label_main_comp = tk.Label(self.input_frame, text='Input the Main competition ID', bd='3', fg='black',
                                        font='Helvetica 9 bold')
        self.label_top_comp = tk.Label(self.input_frame, text='Input the Top competition ID', bd='3', fg='black',
                                       font='Helvetica 9 bold')
        self.label_old_comp = tk.Label(self.input_frame, text='Input the Old competition ID', bd='3', fg='black',
                                       font='Helvetica 9 bold')
        self.label_date_prov = tk.Label(self.input_frame, text='Input the Main competition ID', bd='3', fg='black',
                                        font='Helvetica 9 bold')
        self.maincompID = tk.IntVar()
        self.topcompID = tk.IntVar()
        self.oldcompID = tk.IntVar()
        self.entry_main_comp = tk.Entry(self.input_frame, bd='3', justify="center",textvariable=self.maincompID)
        self.entry_top_comp = tk.Entry(self.input_frame, bd='3', justify="center",textvariable=self.topcompID)
        self.entry_old_comp = tk.Entry(self.input_frame, bd='3', justify="center", textvariable=self.oldcompID)

        #getinput = partial(self.get_input, self.entry_main_comp, self.entry_top_comp, self.entry_old_comp)
        self.confirm_input = tk.Button(self.input_frame, text='Confirm Input', bd='2', fg='black',
                                       activebackground='grey',
                                       bg='white', padx='10', pady='10', font='Helvetica 12 bold',
                                       command=self.get_input)

        self.label_main_comp.place(relx=0.08, rely=0, relheight=0.25)
        self.entry_main_comp.place(relx=0.22, rely=0.2, relwidth=0.2, relheight=0.1)
        self.label_top_comp.place(relx=0.08, rely=0.25, relheight=0.25)
        self.entry_top_comp.place(relx=0.22, rely=0.45, relwidth=0.2, relheight=0.1)
        self.label_old_comp.place(relx=0.08, rely=0.50, relheight=0.25)
        self.entry_old_comp.place(relx=0.22, rely=0.70, relwidth=0.2, relheight=0.1)
        self.confirm_input.place(relx=0.02, rely=0.85, relheight=0.15)

        self.input_frame.place(relx=0.005, rely=0.5, relwidth=0.99, relheight=0.5)
        self.frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def HL_Hijack_Skillcontrib(self):
        print('Hello')

    def get_input(self):
        try:
            currentmaincompID = self.maincompID.get()
            currenttopcompID = self.topcompID.get()
            currentoldcompID = self.oldcompID.get()
            self.correct_input_text = tk.Label(self.input_frame, text='All inputs were correct. \n Running the script!',bd='3', fg='green', font='Helvetica 9 bold')
            self.correct_input_text.place(relx=0.5, rely=0.78, relheight=0.3)
            self.confirm_input.config(state='disabled')
            print(currentmaincompID, currenttopcompID, currentoldcompID)
        except tk.TclError:
            self.wrong_input_text = tk.Label(self.input_frame, text='One of the inputs was not in the correct format', bd='3', fg='red',
                                        font='Helvetica 9 bold')
            self.wrong_input_text.place(relx=0.35, rely=0.85, relheight=0.15)
            self.wrong_input_text.after(2000, self.wrong_input_text.destroy)



window = tk.Tk()
window.title("ETF2L Scripts")
c = MainApplication(window)
window.mainloop()  # keeps the application open