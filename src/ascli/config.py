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
    client = ASnakeClient()
    client.authorize()
    shelf['token'] = client.session.headers[client.config['session_header_name']]

shelf.close()


