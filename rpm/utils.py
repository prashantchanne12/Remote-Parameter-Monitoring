from firebase_admin import firestore
import pandas as pd
from datetime import datetime
from pytz import timezone

from rpm import db


def getCSV(limit=None):
    data = db.collection('Sensor-Data')\
        .order_by('timestamp', direction=firestore.Query.DESCENDING)

    if limit:
        data = data.limit(limit)

    df = pd.DataFrame\
        .from_dict(
            [d.to_dict() for d in data.stream()])\
        .sort_values(['timestamp'])

    df['timestamp'] = [datetime
                       .fromtimestamp(time, timezone('Asia/Kolkata'))
                       .strftime("%d/%m/%Y %H:%M:%S") for time in df.timestamp]

    return df
