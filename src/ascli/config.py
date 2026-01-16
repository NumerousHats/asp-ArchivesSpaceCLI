import shelve

from asnake.client import ASnakeClient

shelf = shelve.open("test")

if 'token' in shelf:
    client = ASnakeClient(username=None, password=None, session_token=shelf['token'])
    client.authorize()
else:
    client = ASnakeClient()
    client.authorize()
    shelf['token'] = client.session.headers[client.config['session_header_name']]

shelf.close()


