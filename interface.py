#!/bin/python

import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from Prediction import Prediction
import sys

LARGE_FONT= ("Verdana", 12)

pred = Prediction()

#setting stock to be fetched if no argument is given
Stock = "GOOGL"
#reading the argument the interface is created with and setting this as the stock to be fetched using tiingo client
if (len(sys.argv) > 1):
    Stock = sys.argv[1]
#fetching the data using the client
stock_prices = pred.stockprices(Stock, 35)
#Training the models and generating the predictions
svm_array, lr_array, svm_confidence, lr_confidence, volume = pred.inference(Stock, 15000, 30, 3)

#creating a container for a TkInterface, initializing the app and all its pages
class StockDSS(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #create a tk frame which will hold the current page being displayed
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #list holding the different frames 
        self.frames = {}
        #initializing the frames/pages we are going to display
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        #bring up the startpage
        self.show_frame(StartPage)

    #bring given frame to front
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#This is how we make the actual pages. They are classes which inherit from tk.Frame.
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Title of page 
        label = tk.Label(self, text="Stock Predicting Decision Support System", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        #button which brings you to the svm prediction page
        button = tk.Button(self, text="SVM Prediction", command=lambda: controller.show_frame(PageOne))
        button.pack()
        #button which brings you to the lvr prediction page 
        button2 = tk.Button(self, text="LVR Prediction", command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        #button showing graph of past 30 days stock prices
        button3 = tk.Button(self, text="Stock prices", command=lambda: controller.show_frame(PageThree))
        button3.pack()        
        #link to page showing our generated prediction
        button4 = tk.Button(self, text="Our recommendation", command=lambda: controller.show_frame(PageFour))
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
        label = tk.Label(self, text=Stock + " Past 30 days", font=LARGE_FONT)
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
        text = tk.Text(self, height = 10, width = 50, font = LARGE_FONT)
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        text.pack(pady = 10, padx = 10, side = "top", fill = "both", expand = True)
        scrollbar.config(command = text.yview)
        text.config(yscrollcommand = scrollbar.set)
        quote = predictionText()
        text.insert(tk.END, quote)
        
def predictionText():
    if(svm_array[5]/svm_array[0] > 1):
     svmIncreasing = True
     momentum1 = svm_array[5]/svm_array[0] - 1
    else:
     svmIncreasing = False
     momentum1 = 1 - svm_array[5]/svm_array[0]
   
    if(lr_array[5]/lr_array[0] > 1):
     lrIncreasing = True
     momentum2 = svm_array[5]/svm_array[0] - 1
    else: 
     lrIncreasing = False
     momentum2 = 1 - lr_array[5]/lr_array[0]

    if (lrIncreasing == True and svmIncreasing == True):
        text1 = "Both our predictions show that the stock price is increasing over the coming five days." + " The price is expected to increase by " +  str(round((momentum1 + momentum2)/2 * 100, 2)) + "%. \n"
   
    elif lrIncreasing != svmIncreasing:
      text1 = "Our predictions do not match each other. \n"
    
    else:
        text1 = "Both our predictions show that the stock price is decreasing over the coming five days. The price is expected to decrease  by " +  str(round((momentum1 + momentum2)/2 * 100, 2)) + "%. \n"
        
    if volume > 1:
      text2 = "The recent volume of transactions is high, we recommend you take action! \n"
    else:
      text2 = "There has been low mobility in the market recently, not taking action may be the best current course of action. \n"

    text3 = "Our confidence in the Linear Regression models prediction is " + str(round(lr_confidence * 100, 2)) + "%. Our confidence in the Support Vector models prediction is " + str(round(svm_confidence * 100, 2)) +"%."
    return text1 + text2 + text3

app = StockDSS()
app.mainloop()
