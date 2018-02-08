# 1) Configure below
# 2) pip install esipy Flask
# 3) FLASK_APP=tokenfetcher.py flask run
# 4) Wait a couple of seconds for the browser to open

import webbrowser

from esipy import App
from esipy import EsiClient
from esipy import EsiSecurity

from flask import Flask, request

CLIENT_ID = ''
SECRET_KEY = ''
SCOPES = ['esi-universe.read_structures.v1', 'esi-markets.structure_markets.v1']

app = Flask(__name__)
esi_app = App.create(url="https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility")

security = EsiSecurity(
    app=esi_app,
    redirect_uri='http://127.0.0.1:5000/ESICallback',
    client_id=CLIENT_ID,
    secret_key=SECRET_KEY
)

client = EsiClient(
    retry_requests=True,
    header={'User-Agent': 'ESI Token Fetcher'},
    security=security
)

webbrowser.open_new(security.get_auth_uri(scopes=SCOPES))

@app.route('/ESICallback')
def esi_callback():
    code = request.args.get('code', '')
    
    if code:
        tokens = security.auth(code)
        return str(tokens)
    else:
        return 'No code returned!'

