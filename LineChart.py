import matplotlib.pyplot as plt
import array

def showChart(prediction, days, predictedPrice):
    plt.plot(days, predictedPrice)
    plt.xlabel('Days')
    plt.ylabel('Predicted Price')
    plt.title(prediction)
    plt.show()



