import sys
from pathlib import Path
import json
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
                self.state = json.load(f)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
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
                    json.dump(self.state, f, indent=2)
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


config = AppConfig()


def construct_url(endpoint, id, repo, needs_repo):
    repo = config.get_default("repository", repo)
    if endpoint == "resources":
        id = config.get_default("resource", id)
    url = f'{endpoint}/{id}'
    if needs_repo:
        url = f'repositories/{repo}/' + url
    return url


def simple_get(endpoint, id, repo, needs_repo=True):
    out = config.client.get(construct_url(endpoint, id, repo, needs_repo))
    out_json = json.loads(out.text)
    print(json.dumps(out_json, indent=2))


def simple_update(new_json, endpoint, id, repo, needs_repo=True):
    out = config.client.post(construct_url(endpoint, id, repo, needs_repo), json=new_json)
    out_json = json.loads(out.text)
    print(json.dumps(out_json, indent=2))
