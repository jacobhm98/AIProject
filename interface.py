#!/bin/python

import tkinter as tk

LARGE_FONT= ("Verdana", 12)
SMALL_FONT= ("Verdana", 8)

class StockDSS(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
       
        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the startpage", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button = tk.Button(self, text="Visit Page 1", command=lambda: controller.show_frame(PageOne))
        button.pack()
        
        button2 = tk.Button(self, text="Visit Page 2", command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        button3 = tk.Button(self, text="Visit Page 3", command=lambda: controller.show_frame(PageThree))
        button3.pack()        

 

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(padx=10, pady=10)
        button1 = tk.Button(self, text = "home", command = lambda: controller.show_frame(StartPage))
        button1.pack()

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two", font=LARGE_FONT)
        label.pack(padx=10, pady=10)
        button1 = tk.Button(self, text = "home", command = lambda: controller.show_frame(StartPage))
        button1.pack()

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Three", font=LARGE_FONT)
        label.pack(padx=10, pady=10)
        button1 = tk.Button(self, text = "home", command = lambda: controller.show_frame(StartPage))
        button1.pack()

app = StockDSS()
app.mainloop()
