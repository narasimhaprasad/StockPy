import matplotlib.pyplot as plt
import numpy as np
from pandas import rolling_mean
from pandas.io.data import DataReader
from datetime import date
from datetime import datetime
from matplotlib.widgets import MultiCursor
from matplotlib.widgets import RadioButtons

#Setup figure. 3 plots. Top: Closing Share Values. Bottom(Bot): Trading Volumes
#Side(Sid): Histogram of day to day variation in stock prices
fig = plt.figure()
top = plt.subplot(221)
bot = plt.subplot(223,sharex=top)
sid = plt.subplot(122)

#Default: GOOG(Google)
stockname = "GOOG"
stock = DataReader(stockname,"yahoo",date(2007,1,1))

#Prop for showing the latest price    
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

#Top plot. Contains closing price, the mean and running mean
top.plot(stock.index,stock['Close'],stock.index,
         stock['Close'].mean(1)*np.ones(len(stock.index)),stock.index,
            rolling_mean(stock['Close'],60))
top.set_title('%s Stock Price from %s to %s' %(stockname,date(2007,1,1),
    datetime.date(stock.index[len(stock.index)-1])))
top.grid(True)
top.text(0.05, 0.95, 'Trading Price on %s : $%s' 
    %(stock.index[len(stock.index)-1], stock['Close'][len(stock.index)-1]),
    transform=top.transAxes,fontsize=14,verticalalignment='top',bbox=props)
ymin,ymax = top.get_ylim()
top.fill_between(stock.index,stock['Close'],
                 (ymin+0.05)*np.ones(len(stock.index)),alpha=0.5)

#Bottom plot contains the trading volumes of the stock  
bot.bar(stock.index,stock['Volume'])
bot.set_title('%s Trading Volume in Millions' %(stockname))

#Side plot contains the histogram of stock value variation
n,bins,patches = sid.hist(stock['High']-stock['Low'],bins=50,normed=True)
sid.set_title('Stock Value Variation')
sid.grid(True)

#Remove x axis tick on top plot
#Set tight layout
#Setup multicursor on top and bottom plot
plt.setp(top.get_xticklabels(),visible=False)
plt.tight_layout()
multi = MultiCursor(fig.canvas,(top,bot),color='r',lw=2)

#Setup for radio bottoms
axcolor = 'lightgoldenrodyellow'
prop_radio = plt.axes([0.85, 0.85, 0.1, 0.1], axisbg=axcolor)
radio = RadioButtons(prop_radio,('GOOG','MSFT','YHOO','GE'))
def stocksel(label):
    top.cla()
    bot.cla()
    sid.cla()

    stockname = label
    stock = DataReader(stockname,"yahoo",date(2007,1,1))
        
    top.plot(stock.index,stock['Close'],stock.index,
         stock['Close'].mean(1)*np.ones(len(stock.index)),stock.index,
            rolling_mean(stock['Close'],60))
    top.set_title('%s Stock Price from %s to %s' %(stockname,date(2007,1,1),
        datetime.date(stock.index[len(stock.index)-1])))
    top.grid(True)
    top.text(0.05, 0.95, 'Trading Price on %s : $%s' 
        %(stock.index[len(stock.index)-1], stock['Close'][len(stock.index)-1]),
        transform=top.transAxes,fontsize=14,verticalalignment='top',bbox=props)
    ymin,ymax = top.get_ylim()
    top.fill_between(stock.index,stock['Close'],
                     (ymin+0.05)*np.ones(len(stock.index)),alpha=0.5)
      
    bot.bar(stock.index,stock['Volume'])
    bot.set_title('%s Trading Volume in Millions' %(stockname))
    
    n,bins,patches = sid.hist(stock['High']-stock['Low'],bins=50,normed=True)
    sid.set_title('Stock Value Variation')
    sid.grid(True)
    
    plt.setp(top.get_xticklabels(),visible=False)
    plt.tight_layout()
radio.on_clicked(stocksel)

plt.show()