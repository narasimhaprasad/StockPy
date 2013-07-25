import pandas.io.data as web
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wd


def plot_data(stkname, fig, topplt, botplt, sidplt):
    #Get data from yahoo
    #Calculate olling mean, mean and current value of stock
    #Also calculate length of data
    startdate = dt.date(2007, 1, 1)
    stkdata = web.DataReader(stkname, 'yahoo', startdate)
    stklen = len(stkdata.index)
    enddate = dt.datetime.date(stkdata.index[stklen-1])
    stkrolmean = pd.ewma(stkdata['Close'], 60)
    stkmean = stkdata['Close'].mean(1).round(2)
    stkcur = stkdata['Close'][stklen-1]
    stkmax = stkdata['Close'].max(1)
    stkmin = stkdata['Close'].min(1)

    #Decoration for annotation of latest trading value
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    #Clear all axes
    topplt.cla()
    botplt.cla()
    sidplt.cla()

    #Top plot: Closing data, mean and rolling mean
    topplt.plot(stkdata.index, stkdata['Close'], stkdata.index,
                stkmean*np.ones(stklen), stkdata.index, stkrolmean,)
    topplt.set_title('{} Stock Price from {} to {}'.format(stkname,
                     startdate, enddate))
    topplt.grid(True)
    topymin, topymax = topplt.get_ylim()
    topplt.text(0.05, 0.95, 'Trading price on {}: ${}'.format(enddate,
                stkcur), transform=topplt.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)
    topplt.fill_between(stkdata.index, stkdata['Close'],
                        (topymin+0.01)*np.ones(stklen), alpha=0.5)
    topplt.legend(('Close', 'Mean', 'EWMA'), 'lower right', shadow=True,
                  fancybox=True, fontsize=8)

    #Bottom plot: Bar Graph, trading volume
    botplt.bar(stkdata.index, stkdata['Volume'])
    botplt.set_title('{} Trading Volume'.format(stkname))

    #Side plot: histogram of 'high-low'
    sidplt.hist(stkdata['High']-stkdata['Low'], bins=50, normed=True)
    sidplt.set_title('Stock Value Variation')
    sidplt.grid(True)
    sidplt.text(0.70, 0.50, '{} Trading Value Stats\nMean:${}\nHighest:${}'
                '\nLowest:${}'.format(stkname, stkmean, stkmax, stkmin),
                transform=sidplt.transAxes, fontsize=12,
                verticalalignment='top', horizontalalignment='center',
                bbox=props)

    #Remove xticklabels on top plot
    plt.setp(topplt.get_xticklabels(), visible=False)
    plt.tight_layout()
    return fig


def setup():
    #Setup figure
    #Top, Bottom, Side with top and bottom plot sharing x axis
    fig = plt.figure()
    top = plt.subplot(221)
    bot = plt.subplot(223, sharex=top)
    sid = plt.subplot(122)

    stklst = sorted(('AMZN', 'GE', 'GOOG', 'MSFT', 'YHOO', 'EBAY'))
    fig = plot_data(stklst[0], fig, top, bot, sid)

    #Setup for radio bottoms
    axcolor = 'lightgoldenrodyellow'
    ylen = len(stklst)/50.0
    prop_radio = plt.axes([0.95, 1-ylen, 0.048, ylen], axisbg=axcolor)
    radio = wd.RadioButtons(prop_radio, stklst)

    return [fig, top, bot, sid, radio]

if __name__ == "__main__":
    fig, top, bot, sid, radio = setup()

    #Setup multicursor between top and bottom plot
    multi = wd.MultiCursor(fig.canvas, (top, bot), color='r', lw=2)

    def stocksel(label):
        plot_data(label, fig, top, bot, sid)

    radio.on_clicked(stocksel)

    #Show plot
    plt.show()
