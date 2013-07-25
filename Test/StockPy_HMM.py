import pandas.io.data as web
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wd
import sklearn.hmm as lrn


def stkHMM(lrndata, n_components):
    model = lrn.GaussianHMM(n_components, covariance_type="tied", n_iter=20)
    model.fit([lrndata])

    hidden_states = model.predict(lrndata)
    return [model, hidden_states]


def plot_data(stkname, fig, topplt, botplt, mlrnplt, sidplt):
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
    stkmchnlrndata = np.column_stack([stkdata['Close'], stkdata['Volume']])
    ncomponents = 5
    lrnmodel, hiddenstates = stkHMM(stkmchnlrndata, ncomponents)
    nxtstateidx = lrnmodel.transmat_[hiddenstates[len(hiddenstates)-1], :]
    nxtstateprob = np.amax(nxtstateidx)
    nxtstate = np.argmax(nxtstateidx)

    #Decoration for annotation of latest trading value
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    #Clear all axes
    topplt.cla()
    botplt.cla()
    mlrnplt.cla()
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

    #Machine Learn plot
    for i in xrange(ncomponents):
        idx = (hiddenstates == i)
        mlrnplt.plot_date(stkdata.index[idx], stkdata['Close'][idx], 'o',
                          label='Hidden state: {}'.format(i))
    mlrnplt.legend(loc='best', fancybox=True, shadow=True, fontsize=8)
    mlrnplt.grid(True)
    mlrnplt.text(0.99, 0.1,
                 'Next State: {} with {:.2f}% probability'
                 .format(nxtstate, nxtstateprob*100),
                 transform=mlrnplt.transAxes, fontsize=10,
                 horizontalalignment='right', verticalalignment='center',
                 bbox=props)
    mlrnplt.set_title('Hidden Markov Model States')

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
    plt.setp(botplt.get_xticklabels(), visible=False)
    plt.tight_layout()
    return fig


def setup():
    stklst = sorted(('ABB', 'AMZN', 'GE', 'GOOG', 'MSFT', 'YHOO', 'EBAY'))

    #Setup figure
    #Top, Bottom, Side with top and bottom plot sharing x axis
    fig = plt.figure()
    top = plt.subplot2grid((3, 3), (0, 0), colspan=2)
    bot = plt.subplot2grid((3, 3), (1, 0), colspan=2, sharex=top)
    mlrn = plt.subplot2grid((3, 3), (2, 0), colspan=2, sharex=top)
    sid = plt.subplot2grid((3, 3), (0, 2), rowspan=3)

    fig = plot_data(stklst[0], fig, top, bot, mlrn, sid)

    #Setup for radio bottoms
    axcolor = 'lightgoldenrodyellow'
    ylen = len(stklst)/50.0
    prop_radio = plt.axes([0.95, 1-ylen, 0.048, ylen], axisbg=axcolor)
    radio = wd.RadioButtons(prop_radio, stklst)

    return [fig, top, bot, sid, mlrn, radio]

if __name__ == "__main__":
    fig, top, bot, sid, mlrn, radio = setup()

    #Setup multicursor between top and bottom plot
    multi = wd.MultiCursor(fig.canvas, (top, bot, mlrn), color='r', lw=2)

    def stocksel(label):
        plot_data(label, fig, top, bot, mlrn, sid)

    radio.on_clicked(stocksel)

    #Show plot
    plt.show()
