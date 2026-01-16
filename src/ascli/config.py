import pickle
from pathlib import Path

from asnake.client import ASnakeClient
from asnake.aspace import ASpace


if Path("asnakeclient.pkl").exists():
    print("auth cache hit")
    with open('asnakeclient.pkl', 'rb') as file:
        client = pickle.load(file)
else:
    print("auth cache miss")
    client = ASnakeClient()
    client.authorize()

    with open('asnakeclient.pkl', 'wb') as file:
        pickle.dump(client, file)
