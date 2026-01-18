import shelve
import sys
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


def from_shelf(item: str):
    shelf = shelve.open(shelf_file)
    if item in shelf:
        value = shelf[item]
        shelf.close()
        return value
    else:
        shelf.close()
        return None


def to_shelf(item: str, value):
    shelf = shelve.open(shelf_file)
    shelf[item] = value
    shelf.close()

def get_default_repo(repo: int):
    if repo is None:
        repo = from_shelf("repo")
        if repo is None:
            print("No repo specified", file=sys.stderr)
            sys.exit(1)

    return repo


# Wrapper functions that call client.get() and client.post(), saving the token on the chance that it has been
# refreshed due to expiration

def get(endpoint):
    global client
    response = client.get(endpoint)
    if response.status_code == 412: # cached token has expired
        client = ASnakeClient()
        client.authorize()
        to_shelf('token', client.session.headers[client.config['session_header_name']])
        response = client.get(endpoint)
    new_token = client.session.headers[client.config['session_header_name']] # in case the token changed due to a 403
    shelf = shelve.open(shelf_file)
    shelf['token'] = new_token
    shelf.close()
    return response

def post(endpoint, json=None):
    global client
    response = client.post(endpoint, json=json)
    if response.status_code == 412: # cached token has expired
        client = ASnakeClient()
        client.authorize()
        to_shelf('token', client.session.headers[client.config['session_header_name']])
        response = client.get(endpoint)
    new_token = client.session.headers[client.config['session_header_name']]
    shelf = shelve.open(shelf_file)
    shelf['token'] = new_token
    shelf.close()
    return response
