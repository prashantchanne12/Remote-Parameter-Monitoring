from rpm import app
from rpm.utils import *

from flask import send_file, request, render_template
import os


@app.route('/')
def home():
    data = getDF(15)

    plot = getPlot(data)
    data = formatTime(data)

    return render_template(
        'home.html',
        rows=data.to_dict(orient='records'),
        cols=data.columns.values)


@app.route('/download')
def download_csv():
    limit = request.args.get('limit', 0, type=int)
    data = getDF(limit)
    data = formatTime(data)
    data.to_csv(os.path.join(app.root_path, 'data.csv'), index=False)
    return send_file(
        os.path.join(app.root_path, 'data.csv'),
        mimetype='application/x-csv')
