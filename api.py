import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

#from cakechat.config import DEFAULT_CONDITION

global _HOST_FQDN
global _SERVER_PORT
_HOST_FQDN = '127.0.0.1'
_SERVER_PORT = '8080'

def get_response(context=['blank'], emotion='neutral'):
    url = 'http://{}:{}/cakechat_api/v1/actions/get_response'.format(_HOST_FQDN, _SERVER_PORT)
    body = {'context': context, 'emotion': emotion}

    response = requests.post(url, json=body)
    r_response = response.json()
    print(r_response)
    return r_response

