import sys
from pathlib import Path
import json as jsonmod
import atexit

import asnake.client.web_client
import platformdirs
from asnake.client import ASnakeClient


class AppConfig(object):
    def __init__(self):
        self.datadir = Path(platformdirs.user_data_dir('asp'))
        self.state_file = self.datadir / 'cache.json'
        if not self.datadir.is_dir():
            Path(self.datadir).mkdir(parents=True, exist_ok=True)

        # Read stored state once at initialization and assume it doesn't change for the duration of the process.
        # This may not be the case if there is more than one concurrent process of this application, but it is a rather
        # minimal risk.

        self.state = {}
        try:
            with open(self.state_file, 'r') as f:
                self.state = jsonmod.load(f)
        except FileNotFoundError:
            pass
        except jsonmod.JSONDecodeError:
            print("Error decoding JSON from file. File might be corrupted.", file=sys.stderr)

        if 'token' in self.state:
            self.client = ASnakeClient(username=None, password=None, session_token=self.state['token'])
            self.client.authorize()
        else:
            asnake_file = Path.home() / '.archivessnake.yml'
            if not asnake_file.is_file():
                print("You are missing the '.achivessnake.yml' file in your home directory. "
                      "This is required for authentication.", file=sys.stderr)
                sys.exit(1)
            try:
                self.client = ASnakeClient()
                self.client.authorize()
                self.state['token'] = self.client.session.headers[self.client.config['session_header_name']]
            except asnake.client.web_client.ASnakeAuthError:
                print("Failed to authenticate with the ArchivesSpace API. Please check your '.achivessnake.yml' file.",
                      file=sys.stderr)
                sys.exit(1)

        # Save state at application exit without using file locking.
        #
        # This, of course, could result in a race condition if more than one application process is running. However,
        # the possibilities of that are so remote and of such low consequence that it's not worth dealing with.
        #
        # A race condition could arise in only two scenarios: 1) a user (or a shell script, perhaps) runs more than
        # one simultaneous and contradictory instances of 'repository set' or 'resource set', or 2) the session token
        # expires while more than one process of the app is running.
        #
        # The first situation is practically impossible to happen in normal operation by a normal user, so it can be
        # discounted. The second situation is slightly more plausible, but any invalid/expired key will be cleared at
        # the next time the application is run.

        def save_state():
            try:
                with open(self.state_file, 'w') as f:
                    jsonmod.dump(self.state, f, indent=2)
            except IOError as e:
                print(f"Error saving state: {e}", file=sys.stderr)

        atexit.register(save_state)

    def clear_state(self, items):
        for item in items:
            if item in self.state:
                del self.state[item]

    def set_default(self, key, value):
        self.state[key] = value

    def get_default(self, key, value):
        if value is None:
            value = self.state.get(key)
            if value is None:
                print(f"No {key} specified", file=sys.stderr)
                sys.exit(1)
        return value

    def _redo(self, api_out):
        if api_out.status_code == 412:
            try:
                self.client = ASnakeClient()
                self.client.authorize()
            except asnake.client.web_client.ASnakeAuthError:
                print("Failed to authenticate with the ArchivesSpace API. Please check your '.achivessnake.yml' file.",
                      file=sys.stderr)
                sys.exit(1)
            self.state['token'] = self.client.session.headers[self.client.config['session_header_name']]
            return True
        elif api_out.status_code >= 400:
            print(f'API call failed: {api_out.text}', file=sys.stderr)
            exit(1)

        if api_out.status_code != 200:
            print(f'API problem: {api_out.text}', file=sys.stderr)
            exit(1)

        if api_out.status_code == 200:
            return False

    def safe_get(self, endpoint):
        out = self.client.get(endpoint)
        if self._redo(out):
            out = self.client.get(endpoint)
        return out

    def safe_post(self, endpoint, json):
        out = self.client.post(endpoint, json=json)
        if self._redo(out):
            out = self.client.post(endpoint, json=json)
        return out


config = AppConfig()


def simple_get(endpoint, id, repo):
    if '{repo}' in endpoint:
        repo = config.get_default("repository", repo)
    if 'resource' in endpoint:
        id = config.get_default("resource", id)
    out = config.safe_get(endpoint.format(id=id, repo=repo))
    return jsonmod.loads(out.text)


def simple_post(new_json, endpoint, id, repo):
    if '{repo}' in endpoint:
        repo = config.get_default("repository", repo)
    if 'resource' in endpoint:
        id = config.get_default("resource", id)

    if new_json is None or new_json == '-':
        new_json = jsonmod.load(sys.stdin)
    else:
        try:
            with open(new_json, 'r') as f:
                new_json = jsonmod.load(f)
        except FileNotFoundError:
            print("Note JSON file not found", file=sys.stderr)
            exit(1)
        except jsonmod.JSONDecodeError:
            print("Error decoding JSON from file. File might be corrupted.", file=sys.stderr)
            exit(1)
    if 'repository' in endpoint:
        repo = config.get_default("repository", repo)
    if 'resource' in endpoint:
        id = config.get_default("resource", id)
    out = config.safe_post(endpoint.format(id=id, repo=repo), json=new_json)
    return jsonmod.loads(out.text)
