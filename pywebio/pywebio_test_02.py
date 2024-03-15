from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *


def main():
    import json
    from pywebio.session import info as session_info

    put_code(json.dumps({
        k: str(getattr(session_info, k))
        for k in ['user_agent', 'user_language', 'server_host',
                  'origin', 'user_ip', 'backend', 'protocol', 'request']
    }, indent=4), 'json')


start_server(main, port=8080, debug=True)
