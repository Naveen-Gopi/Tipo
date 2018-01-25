#!/usr/bin/python
# -*- coding: utf-8 -*-

# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib3 import PoolManager  # added by naveen
from bs4 import BeautifulSoup  # added by naveen

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout

app = Flask(__name__)


                                         # naveen

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print('Request:')
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)

    # print(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get('result').get('action') == 'getTipoTapp':
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        manager = PoolManager(num_pools=3)
        tipo_req = makeWebhookParameters(req)
        if tipo_req is None:
            return {}
        base_url = 'https://app.tipotapp.com/docs/quickstart/'
        page = manager.request('GET', base_url)
        soup = BeautifulSoup(page.data, 'html.parser')
        print('After Parameter function')
        for sibling in soup.find(id=tipo_req).next_siblings:
            if sibling.name is None:
                continue
            elif sibling.name == 'p':
                out = sibling.getText()
                out_str.append(out)
            else:
                break
            data = '\n'.join(out_str)
            res = makeWebhookResultForTipoTapp(data)
        print('After the result function')
    else:
        return {}

    return res


def makeWebhookResultForTipoTapp(data):
    speechText = data
    displayText = data
    print('Response:')
    print(speechText)
    return {'speech': speechText, 
            'displayText': displayText,
            'source': 'apiai-weather-webhook-sample'}  # "data": data,
                                                       # "contextOut": [],


def makeWebhookParameters():
    result = req.get('result')
    parameters = result.get('parameters')
    tipo_id = parameters.get('any')
    if tipo_id is None:
        return None
    print('Inside the funtion makeWebhookParameters')
    return tipo_id


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print('Starting app on port %d' % port)

    app.run(debug=False, port=port, host='0.0.0.0')


			
