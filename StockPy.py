import pandas.io.data as web
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wd

if __name__ == "__main__":
    #Setup figure
    #Top, Bottom, Side with top and bottom plot sharing x axis
    fig = plt.figure()
    top = plt.subplot(221)
    bot = plt.subplot(223, sharex=top)
    sid = plt.subplot(122)

    def plot_data(stkname, fig, topplt, botplt, sidplt):
        #Get data from yahoo
        #Calculate olling mean, mean and current value of stock
        #Also calculate length of data
        startdate = dt.date(2007, 1, 1)
        stkdata = web.DataReader(stkname, 'yahoo', startdate)
        stklen = len(stkdata.index)
        enddate = dt.datetime.date(stkdata.index[stklen-1])
        stkrolmean = pd.rolling_mean(stkdata['Close'], 60)
        stkmean = stkdata['Close'].mean(1)
        stkcur = stkdata['Close'][stklen-1]

        #Decoration for annotation of latest trading value
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        #Top plot: Closing data, mean and rolling mean
        topplt.plot(stkdata.index, stkdata['Close'], stkdata.index,
                    stkmean*np.ones(stklen), stkdata.index, stkrolmean)
        topplt.set_title('{} Stock Price from {} to {}'.format(stkname,
                         startdate, enddate))
        topplt.grid(True)
        topymin, topymax = topplt.get_ylim()
        topplt.text(0.05, 0.95, 'Trading price on {}: ${}'.format(enddate,
                    stkcur), transform=top.transAxes, fontsize=14,
                    verticalalignment='top', bbox=props)
        topplt.fill_between(stkdata.index, stkdata['Close'],
                            (topymin+0.01)*np.ones(stklen), alpha=0.5)

        #Bottom plot: Bar Graph, trading volume
        botplt.bar(stkdata.index, stkdata['Volume'])
        botplt.set_title('{} Trading Volume'.format(stkname))

        #Side plot: histogram of 'high-low'
        sidplt.hist(stkdata['High']-stkdata['Low'], bins=50, normed=True)
        sidplt.set_title('Stock Value Variation')
        sidplt.grid(True)

        #Remove xticklabels on top plot
        plt.setp(top.get_xticklabels(), visible=False)
        plt.tight_layout()
        return fig

    fig = plot_data('GOOG', fig, top, bot, sid)
    multi = wd.MultiCursor(fig.canvas, (top, bot), color='r', lw=2)

    #Setup for radio bottoms
    axcolor = 'lightgoldenrodyellow'
    prop_radio = plt.axes([0.95, 0.9, 0.05, 0.1], axisbg=axcolor)
    radio = wd.RadioButtons(prop_radio, ('GOOG', 'MSFT', 'YHOO', 'GE'))

    def stocksel(label):
        #Clear all axes
        top.cla()
        bot.cla()
        sid.cla()

        plot_data(label, fig, top, bot, sid)
    radio.on_clicked(stocksel)

    #Show plot
    plt.show()
