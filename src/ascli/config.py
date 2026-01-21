import sys
from pathlib import Path
import json
import atexit

import platformdirs
from asnake.client import ASnakeClient


class AppConfig(object):
    def __init__(self):
        self.datadir = Path(platformdirs.user_data_dir('ascli'))
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
            print("token cache miss", file=sys.stderr)
            self.client = ASnakeClient()
            self.client.authorize()
            self.state['token'] = self.client.session.headers[self.client.config['session_header_name']]

        # Save state at application exit without using file locking.
        #
        # This, of course, could result in a race condition if more than one application process is running. However, the
        # possibilities of that are so remote and of such low consequence that it's not worth dealing with.
        #
        # A race condition could arise in only two scenarios: 1) a user (or user shell script, perhaps) runs more than one
        # simultaneous and contradictory instances of 'repository set' or 'resource set', or 2) the session token expires while
        # more than one process of the app is running.
        #
        # The first situation is practically impossible to happen in normal operation by a normal user, so it can be discounted.
        # The second situation is slightly more plausible, but any invalid/expired key will be cleared at the next invocation of
        # the application.

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

    def get_default(self, key, value):
        if value is None:
            value = self.state[key]
            if value is None:
                print(f"No {key} specified", file=sys.stderr)
                sys.exit(1)
        return value

    # Wrapper functions that call client.get() and client.post(), saving the token on the chance that it has been
    # refreshed due to expiration

    def get(self, endpoint):
        response = self.client.get(endpoint)
        if response.status_code == 412: # cached token has expired
            self.client = ASnakeClient()
            self.client.authorize()
            self.state['token'] = self.client.session.headers[self.client.config['session_header_name']]
            response = self.client.get(endpoint)
        # in case the token changed due to a 403
        self.state['token'] = self.client.session.headers[self.client.config['session_header_name']]
        return response

    def post(self, endpoint, json_file=None):
        response = self.client.post(endpoint, json=json_file)
        if response.status_code == 412: # cached token has expired
            self.client = ASnakeClient()
            self.client.authorize()
            self.state['token'] =  self.client.session.headers[self.client.config['session_header_name']]
            response = self.client.get(endpoint)
        self.state['token'] = self.client.session.headers[self.client.config['session_header_name']]
        return response

config = AppConfig()

