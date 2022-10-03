# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 22:19:53 2022

@author: sskky
"""
from tkinter import *
from tkinter import ttk
import tkinter as tk
import controller

class MainGUI(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.geometry("450x200")
        #self.configure(background="white")
        self.mainframe = ttk.Frame(self, padding="8 8 12 12")
        self.mainframe.grid(column=0, row=0)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.modeframe = tk.LabelFrame(self.mainframe, text = "mode")
        self.modeframe.grid(row=1, column=1, padx=10)
        self.modeVar = tk.IntVar()
        self.modeVar.set(-1)
        self.manuel_button = tk.Radiobutton(self.modeframe, text="manuel", command = self.disable_button , variable = self.modeVar, value = 1)
        self.manuel_button.grid(column=1, row=2, pady=10, padx=10)
        self.auto_button = tk.Radiobutton(self.modeframe, text="auto", command = self.disable_button,  variable = self.modeVar, value = 2)
        self.auto_button.grid(column=2, row=2, pady=10, padx=10)
        #start&stop
        self.start_button = tk.Button(self.mainframe, text = "start", command = self.scenario_run, height = 2, width = 10)
        self.start_button.grid(column=2, row=1, padx=10)
        #scenario
        self.scenarioVar = tk.IntVar()
        self.scenarioVar.set(-1)
        self.scenarioframe = tk.LabelFrame(self.mainframe, text = "scenario")
        self.scenarioframe.grid(row=3, column=1, sticky=tk.W, padx=10)
        self.scenario1 = tk.Radiobutton(self.scenarioframe, text="scenario1", variable = self.scenarioVar, value=1)
        self.scenario1.grid(column=1, row=1, padx=5, pady=5)
        self.scenario2 = tk.Radiobutton(self.scenarioframe, text="scenario2", variable = self.scenarioVar, value=2)
        self.scenario2.grid(column=1, row=2, padx=5, pady=5)
        self.scenario3 = tk.Radiobutton(self.scenarioframe, text="scenario3", variable = self.scenarioVar, value=3)
        self.scenario3.grid(column=1, row=3, padx=5, pady=5)
        #keyboard
        self.keyboardframe = tk.LabelFrame(self.mainframe, text = "keyboard")
        self.keyboardframe.grid(row=3, column=2, padx=10)
        self.button_up = tk.Button(self.keyboardframe, command = self.forward, text = 'up')
        self.button_up.grid(column=1, row=0, sticky=tk.N, padx=5, pady=5)
        self.button_down = tk.Button(self.keyboardframe, command = self.stop,  text = 'down')
        self.button_down.grid(column=1, row=1, sticky=tk.S, padx=5, pady=5)
        self.button_left = tk.Button(self.keyboardframe, text = 'left')
        self.button_left.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.button_right = tk.Button(self.keyboardframe, text = 'right')
        self.button_right.grid(column=2, row=1, sticky=tk.E, padx=5, pady=5)
        self.bind("<Key>",self.keyEvent)
        self.mainloop()
        
    def scenario_run(self):
        if(self.start_button['text'] == "start"):
            self.start_button['text'] = "stop"
        else:
            self.start_button['text'] = "start"
    
    def forward(self):
        controller.main.vorwaerts(self)
        
    def stop(self):
        controller.main.stop(self)
        
    def disable_button(self):
        if (self.modeVar.get() == 1):
            self.scenario1['state']  = tk.DISABLED
            self.scenario2['state']  = tk.DISABLED
            self.scenario3['state']  = tk.DISABLED
            self.button_up['state']  = tk.NORMAL
            self.button_down['state']  = tk.NORMAL
            self.button_left['state']  = tk.NORMAL
            self.button_right['state']  = tk.NORMAL
        else:
            self.scenario1['state']  = tk.NORMAL
            self.scenario2['state']  = tk.NORMAL
            self.scenario3['state']  = tk.NORMAL
            self.button_up['state']  = tk.DISABLED
            self.button_down['state']  = tk.DISABLED
            self.button_left['state']  = tk.DISABLED
            self.button_right['state']  = tk.DISABLED
      
    def keyEvent(self, event):
        print("key : " + chr(event.keycode))

if __name__ == '__main__':
    app = MainGUI()
