import pprint

import requests

payload = {
    'action': 'list_customer',
}

response = requests.get('http://127.0.0.1/api/mgr/customers', params=payload)

pprint.pprint(response.json())
