import shelve
from pathlib import Path

import platformdirs
from asnake.client import ASnakeClient

datadir = Path(platformdirs.user_data_dir('ascli'))
shelf_file = datadir / 'persistence.dat'

if not datadir.is_dir():
    Path(datadir).mkdir(parents=True, exist_ok=True)

shelf = shelve.open(shelf_file)
if 'token' in shelf:
    client = ASnakeClient(username=None, password=None, session_token=shelf['token'])
    client.authorize()
else:
    print("token cache miss")
    client = ASnakeClient()
    client.authorize()
    shelf['token'] = client.session.headers[client.config['session_header_name']]
shelf.close()


# Wrapper functions that call client.get() and client.post(), saving the token on the chance that it has been
# refreshed due to expiration

def get(endpoint):
    response = client.get(endpoint)
    new_token = client.session.headers[client.config['session_header_name']]
    shelf = shelve.open(shelf_file)
    shelf['token'] = new_token
    shelf.close()
    return response

def post(endpoint):
    response = client.post(endpoint)
    new_token = client.session.headers[client.config['session_header_name']]
    shelf = shelve.open(shelf_file)
    shelf['token'] = new_token
    shelf.close()
    return response


