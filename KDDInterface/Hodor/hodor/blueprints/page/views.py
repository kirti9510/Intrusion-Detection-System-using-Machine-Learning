import os
from flask import Blueprint, send_file

page = Blueprint('page', __name__)
prefix = 'webapp'

@page.route('/', defaults={'path': 'index.html'})
@page.route('/<path:path>')
def home(path):
        return send_file(os.path.join(prefix, path))

