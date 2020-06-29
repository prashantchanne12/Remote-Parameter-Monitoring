from rpm import app
from rpm.utils import *

from flask import send_file, request
import os


@app.route('/')
def home():
    limit = request.args.get('limit', 0, type=int)
    data = getCSV(limit)
    return data.to_html(index=False)


@app.route('/download')
def download_csv():
    limit = request.args.get('limit', 0, type=int)
    data = getCSV(limit)
    data.to_csv(os.path.join(app.root_path, 'data.csv'), index=False)
    return send_file(os.path.join(app.root_path, 'data.csv'), mimetype='application/x-csv', attachment_filename='data.csv', as_attachment=True))
