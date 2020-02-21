import tkinter as tk
from BaseFunctions.ETF2lBase import dateHourToUnix, getCompList, getTeamIDs, getTransfers, getTeamDiv
from BaseFunctions.HijackAndSkillContribBase import transferCheck, getPlayerSkillHS, teamSkillHS, activeLineup

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
        self.label_date_prov = tk.Label(self.input_frame, text='Input the date of provisional release', bd='3', fg='black',
                                        font='Helvetica 9 bold')
        self.label_hour_prov = tk.Label(self.input_frame, text='Input the hour of provisional release', bd='3', fg='black',
                                        font='Helvetica 9 bold')
        self.label_days_to_check = tk.Label(self.input_frame, text='Input the amount of days to backcheck', bd='3',fg='black',
                                        font='Helvetica 9 bold')

        self.maincompID = tk.IntVar()
        self.maincompID.set(668)
        self.topcompID = tk.IntVar()
        self.topcompID.set(670)
        self.oldcompID = tk.IntVar()
        self.oldcompID.set(605)
        self.provdate = tk.StringVar()
        self.provdate.set('24/01/2020')
        self.provhour = tk.StringVar()
        self.provhour.set('23:59:00')
        self.daystocheck = tk.IntVar()
        self.daystocheck.set(7)
        self.activejoinlimit = tk.IntVar()
        self.activejoinlimit.set(3)
        self.skillcontriblimit = tk.IntVar()
        self.skillcontriblimit.set(2)
        self.gametype = tk.StringVar()
        self.gametype.set('6v6')

        self.entry_main_comp = tk.Entry(self.input_frame, bd='3', justify="center",textvariable=self.maincompID)
        self.entry_top_comp = tk.Entry(self.input_frame, bd='3', justify="center",textvariable=self.topcompID)
        self.entry_old_comp = tk.Entry(self.input_frame, bd='3', justify="center", textvariable=self.oldcompID)
        self.entry_date_prov = tk.Entry(self.input_frame, bd='3', justify="center",textvariable=self.provdate)
        self.entry_hour_prov = tk.Entry(self.input_frame, bd='3', justify="center",textvariable=self.provhour)
        self.entry_days_to_check = tk.Entry(self.input_frame, bd='3', justify="center",textvariable=self.daystocheck)


        self.confirm_input = tk.Button(self.input_frame, text='Confirm Input', bd='2', fg='black',
                                       activebackground='grey',
                                       bg='white', padx='10', pady='10', font='Helvetica 12 bold',
                                       command=self.get_input)

        self.label_main_comp.place(relx=0.0, rely=0, relheight=0.25)
        self.entry_main_comp.place(relx=0.01, rely=0.2, relwidth=0.2, relheight=0.1)
        self.label_top_comp.place(relx=0.0, rely=0.25, relheight=0.25)
        self.entry_top_comp.place(relx=0.01, rely=0.45, relwidth=0.2, relheight=0.1)
        self.label_old_comp.place(relx=0.00, rely=0.50, relheight=0.25)
        self.entry_old_comp.place(relx=0.01, rely=0.70, relwidth=0.2, relheight=0.1)
        self.label_date_prov.place(relx=0.5, rely=0, relheight=0.25)
        self.entry_date_prov.place(relx=0.51, rely=0.2, relwidth=0.2, relheight=0.1)
        self.label_hour_prov.place(relx=0.5, rely=0.25, relheight=0.25)
        self.entry_hour_prov.place(relx=0.51, rely=0.45, relwidth=0.2, relheight=0.1)
        self.label_days_to_check.place(relx=0.50, rely=0.50, relheight=0.25)
        self.entry_days_to_check.place(relx=0.51, rely=0.70, relwidth=0.2, relheight=0.1)

        self.confirm_input.place(relx=0.02, rely=0.85, relheight=0.15)

        self.input_frame.place(relx=0.005, rely=0.5, relwidth=0.99, relheight=0.5)
        self.frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def HL_Hijack_Skillcontrib(self):
        print('Hello')

    def get_input(self):
        try:
            self.setupmaincompID = self.maincompID.get()
            self.setuptopcompID = self.topcompID.get()
            self.setupoldcompID = self.oldcompID.get()
            self.setupprovdate = self.provdate.get()
            self.setupprovhour = self.provhour.get()
            self.setupdaystocheck = self.daystocheck.get()
            self.correct_input_text = tk.Label(self.input_frame, text='All inputs were correct. \n Running the script!',bd='3', fg='green', font='Helvetica 9 bold')
            self.correct_input_text.place(relx=0.5, rely=0.78, relheight=0.3)
            self.confirm_input.config(state='disabled')

            self.confirm_input.destroy()
            self.button_rerun = tk.Button(self.input_frame, text='Re-run the script', bd='2', fg='black', activebackground='grey',
                                       bg='white', padx='10', pady='10', font='Helvetica 12 bold')
            self.button_rerun.place(relx=0.02, rely=0.85, relheight=0.15)
            self.main()

        except tk.TclError:
            self.wrong_input_text = tk.Label(self.input_frame, text='One of the inputs was not in the correct format', bd='3', fg='red',
                                        font='Helvetica 9 bold')
            self.wrong_input_text.place(relx=0.35, rely=0.85, relheight=0.15)
            self.wrong_input_text.after(2000, self.wrong_input_text.destroy)

    def main(self):
        self.provisionalsRelease = dateHourToUnix(self.setupprovdate, self.setupprovhour)
        self.compList6v6, self.compListHL = getCompList(self.setupoldcompID, self.setuptopcompID)
        self.fullCompList6v6, self.fullCompListHL = getCompList(1, self.setupmaincompID)
        self.teamIDList = getTeamIDs(self.setupmaincompID, self.setuptopcompID)
        self.previousFMC = 0
        allowedPlayerIDlist = []

        outputFile = open('output.txt','w')
        outputFile.close()

        for teamID in self.teamIDList:
            self.activePlayerIDlist = []
            self.teamHL = dict(prem=0, div1=0, high=0, mid=0, low=0, open=0, none=0)
            self.team6s = dict(prem=0, div1=0, div2=0, mid=0, low=0, open=0, none=0)
            self.activePlayer = 0
            self.totalJoins = 0
            self.playerScore = 0
            self.skillContribTotal6s = 0
            self.skillContribTotalHL = 0
            self.waterfall = []
            outputList = []

            self.transfers = getTransfers(teamID, self.provisionalsRelease)
            if self.transfers is None:
                totalJoins = 0
            else:
                self.playerIDList, totalJoins = transferCheck(self.transfers, teamID, allowedPlayerIDlist, self.setupdaystocheck, self.provisionalsRelease)
                if len(self.playerIDList) == 0:
                    continue
                else:
                    self.teamDiv = getTeamDiv(teamID, self.setupmaincompID, self.setuptopcompID)
                    for playerID in self.playerIDList:
                        self.isActivePlayer = activeLineup(teamID, playerID, self.setupdaystocheck)
                        if self.isActivePlayer > 0:
                            self.activePlayer = self.activePlayer + 1
                            if playerID not in self.activePlayerIDlist:
                                self.activePlayerIDlist.append(playerID)
                        self.playerHL, self.player6s, self.HLMatchCount, self.SMatchCount, self.previousFMC = getPlayerSkillHS(playerID, self.teamDiv,
                                self.fullCompList6v6, self.fullCompListHL, self.compList6v6, self.compListHL,self.previousFMC)
                        self.team6s, self.teamHl, self.skillContribTotal6s, self.skillContribTotalHL, self.waterfall = teamSkillHS(self.player6s,
                                self.playerHL, self.team6s, self.teamHL, self.skillContribTotal6s, self.skillContribTotalHL,
                                self.HLMatchCount, self.SMatchCount, playerID, teamID, self.activePlayerIDlist,
                                self.waterfall, self.setupmaincompID, self.setuptopcompID)

            # Log output to the cosole for each team
            self.Sseperate = 'Prem: ' + str(self.team6s['prem']) + ', Div1: ' + str(self.team6s['div1']) + ', Div2: ' + str(
                self.team6s['div2']) + ', Mid: ' + str(self.team6s['mid']) + ', Low: ' + str(
                self.team6s['low']) + ', Open: ' + str(self.team6s['open']) + ', None: ' + str(self.team6s['none'])
            self.Hlseperate = 'Prem: ' + str(self.teamHL['prem']) + ', Div1: ' + str(self.team6s['div1']) + ', High: ' + str(
                self.teamHL['high']) + ', Mid: ' + str(self.teamHL['mid']) + ', Low: ' + str(
                self.teamHL['low']) + ', Open: ' + str(self.teamHL['open']) + ', None:' + str(self.teamHL['none'])
            if ((self.activePlayer >= self.activejoinlimit.get() or (
                    self.skillContribTotal6s >= self.skillcontriblimit.get())) and self.gametype.get() == "6v6") or (
                    (self.activePlayer >= self.activejoinlimit.get() or (
                            self.skillContribTotalHL >= self.skillcontriblimit.get())) and self.gametype.get() == "9v9") or (
                    self.teamDiv == 'Open' and self.skillContribTotalHL >= self.skillcontriblimit.get() and self.gametype.get() == "6v6"):
                outputList.append("[team id = " + str(teamID) + "], this team is a " + self.teamDiv + " team")
                outputList.append("Number of joins since provisionals released: " + str(self.totalJoins))
                outputList.append("PlayerID of the joiners:")
                for playerID in self.playerIDList:
                    outputList.append("[player id = " + str(playerID) + "]")
                outputList.append("Number of late joiners actively playing for the team: " + str(self.activePlayer))
                outputList.append("PlayerID of active late joiners: ")
                for activePlayerID in self.activePlayerIDlist:
                    outputList.append("[player id = " + str(activePlayerID) + "]")
                outputList.append("6S skill of joiners: " + str(self.Sseperate))
                outputList.append("6S skill  contribution of joiners cumulative " + str(self.skillContribTotal6s))
                outputList.append("HL skill of joiners: " + str(self.Hlseperate))
                outputList.append("HL skill contribution of joiners cumulative: " + str(self.skillContribTotalHL) + "\n")
                for waterfallID in self.waterfall:
                    outputList.append("[player id = " + str(
                        waterfallID) + "], has three or more games played in different divisions, check his profile")
            if len(self.waterfall) >= self.activejoinlimit.get():
                outputList.append(
                    "\n -------------------------------- \n Team Detected by waterfall \n -------------------------------- \n")
                outputList.append("[team id = " + str(teamID) + "], this team is a " + self.teamDiv + " team")
                outputList.append("Number of joins since provisionals released: " + str(self.totalJoins))
                for waterfallID in self.waterfall:
                    outputList.append("[player id = " + str(
                        waterfallID) + "], has three or more games played in different divisions, check his profile")
            outputFile = open('output.txt','a')
            for line in outputList:
                if line != []:
                    outputFile.write(line + '\n')
            outputFile.close()
            self.displayOutput()

    def displayOutput(self):
        self.button_frame.destroy()
        self.input_frame.destroy()
        self.output_frame = tk.Frame(self.frame, bd='10', padx=3, pady=3)
        self.output_frame.place(relx=0.005, rely=0.005, relwidth=0.99, relheight=1)
        with open("output.txt", "r") as f:
            self.outputtext = tk.Label(self.output_frame, text=f.read(),bd='3', fg='black', font='Helvetica 9 bold',justify='left')
            self.outputtext.place(relx=0.0, rely=0.005, relheight=1)




window = tk.Tk()
window.title("ETF2L Scripts")
c = MainApplication(window)
window.mainloop()  # keeps the application open