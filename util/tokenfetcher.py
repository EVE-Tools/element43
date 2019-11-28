# Works on Python 3.6+
#
# 1) Configure below
# 2) pip install esipy Flask
# 3) FLASK_APP=tokenfetcher.py flask run
# 4) Wait a couple of seconds for the browser to open

import random
import string
import webbrowser

from esipy import App
from esipy import EsiClient
from esipy import EsiSecurity

from flask import Flask, request

CLIENT_ID = ''
SECRET_KEY = ''
SCOPES = ['esi-universe.read_structures.v1', 'esi-markets.structure_markets.v1']

app = Flask(__name__)
esi_app = App.create(url="https://esi.evetech.net/latest/swagger.json?datasource=tranquility")

security = EsiSecurity(
    app=esi_app,
    redirect_uri='http://127.0.0.1:5000/ESICallback',
    headers={'User-Agent': 'ESI Token Fetcher'},
    client_id=CLIENT_ID,
    secret_key=SECRET_KEY
)

client = EsiClient(
    retry_requests=True,
    headers={'User-Agent': 'ESI Token Fetcher'},
    security=security
)

state = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
webbrowser.open_new(security.get_auth_uri(scopes=SCOPES, state=state))

@app.route('/ESICallback')
def esi_callback():
    url_state = request.args.get('state', '')
    
    if url_state != state:
        return 'Invalid state token returned!'
    
    code = request.args.get('code', '')
    
    if code:
        tokens = security.auth(code)
        return str(tokens)
    else:
        return 'No code returned!'

