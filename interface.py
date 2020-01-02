#!/bin/python

import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from Prediction import Prediction


LARGE_FONT= ("Verdana", 12)
SMALL_FONT= ("Verdana", 8)
pred = Prediction()
svm_array, lr_array, svm_confidence, lr_confidence, volume = pred.inference("GOOGL", 15000, 30, 3)
stock_prices = pred.stockprices("GOOGL", 35)

class StockDSS(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
       
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
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
        button4 = tk.Button(self, text="Visit Page 4", command=lambda: controller.show_frame(PageFour))
        button4.pack()
 

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Support Vector Prediction", font=LARGE_FONT)
        label.pack(padx=10, pady=10)
        button1 = tk.Button(self, text = "home", command = lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize = (5, 5), dpi = 100)
        a = f.add_subplot(111)
        a.plot(range(1, 31), svm_array)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand = True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Linear Regression Prediction", font=LARGE_FONT)
        label.pack(padx=10, pady=10)
        button1 = tk.Button(self, text = "home", command = lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize = (5, 5), dpi = 100)
        a = f.add_subplot(111)
        a.plot(range(1, 31), lr_array)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand = True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Three", font=LARGE_FONT)
        label.pack(padx=10, pady=10)
        button1 = tk.Button(self, text = "home", command = lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize = (5, 5), dpi = 100)
        a = f.add_subplot(111)
        a.plot(range(1, stock_prices.size + 1), stock_prices)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand = True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text= "Our Recommendation", font = LARGE_FONT)
        label.pack(padx = 10, pady = 10)
        button1 = tk.Button(self, text = "home", command = lambda: controller.show_frame(StartPage))
        button1.pack()


app = StockDSS()
app.mainloop()
