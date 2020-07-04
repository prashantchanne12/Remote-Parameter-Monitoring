from firebase_admin import firestore
import pandas as pd
from datetime import datetime
from pytz import timezone
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
import os

from rpm import db, app


def getDF(limit=None):
    data = db.collection('Sensor-Data')\
        .order_by('timestamp', direction=firestore.Query.DESCENDING)

    if limit:
        data = data.limit(limit)

    df = pd.DataFrame\
        .from_dict(
            [d.to_dict() for d in data.stream()])\
        .sort_values(['timestamp'])

    return df


def formatTime(df):
    df['timestamp'] = [datetime
                       .fromtimestamp(time, timezone('Asia/Kolkata'))
                       .strftime("%d/%m/%Y %H:%M:%S") for time in df.timestamp]

    return df


def getPlot(df):
    dates = [datetime.fromtimestamp(time, timezone(
        'Asia/Kolkata')) for time in df.timestamp]
    date_format = mpl_dates.DateFormatter("%d/%m/%Y\n%H:%M:%S")

    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)

    ax[0].plot_date(dates, df.temp, ls='-', c='red')
    ax[1].plot_date(dates, df.humidity, ls='-', c='green')

    ax[0].set(ylabel='Temperature')
    ax[1].set(ylabel='Humidity')

    fig.gca().xaxis.set_major_formatter(date_format)
    plt.setp(ax[1].get_xticklabels(), rotation=270)

    fig.savefig(os.path.join(app.root_path, 'static',
                             'plot.png'),
                bbox_inches='tight', transparent=True)
