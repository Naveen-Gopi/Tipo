#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib3 import PoolManager  # added by naveen
from bs4 import BeautifulSoup  # added by naveen

import urllib3
import json
import os
import sys
import logging

from flask import Flask, render_template
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


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

# out_str = []
# data = []
urls = [
    'https://app.tipotapp.com/docs/introduction/',
    'https://app.tipotapp.com/docs/quickstart/',
    'https://app.tipotapp.com/docs/advanced_concepts/',
    'https://app.tipotapp.com/docs/developer_documentation/',
    'https://app.tipotapp.com/docs/client_side_actions/',
    'https://app.tipotapp.com/docs/server_side_actions/',
    'https://app.tipotapp.com/docs/expressions_and_filters_syntax/',
    ]


def processRequest(req):
    data=[]
    if req.get('result').get('action') == 'getTipoTapp':
        out_str = []
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        manager = PoolManager(num_pools=3)
        tipo_req = makeWebhookParameters(req)
        if tipo_req is None:
            return {}
        for url in urls:
            page = manager.request('GET', url)
            soup = BeautifulSoup(page.data, 'html.parser')

            print('After Parameter function', tipo_req)

            if soup.find(id=tipo_req) is not None:
                print('Inside the find function', tipo_req)
                for sibling in soup.find(id=tipo_req).next_siblings:
                    if sibling.name is None:
                        continue
                    elif sibling.name != 'h2':
                        out = sibling.getText()
                        out_str.append(out)
                        if sibling.img is not None:
                            url=sibling.img['src']
                            name=sibling.img['alt']
                            hyperlink_format = '<a href="{link}">{text}</a>'
                            link_text = hyperlink_format.format
                            out_1=link_text(link=url, text=name)
                            out_str.append(out_1)
                        else:
                            continue
                    else:
                        break
                    data = '\n'.join(out_str)
                 print('before printing data', data)
            else:
                continue
            print('after printing data', data)
        res = makeWebhookResultForTipoTapp(data)
    else:

       # print('Else Loop ')

        speechText = 'Introduction Not available'
        return {'speech': speechText}

    return res


def makeWebhookResultForTipoTapp(data):
    speechText = data
    displayText = data
    print('Response:')
    print(speechText)
    return {'speech': speechText, 'displayText': displayText,
            'source': 'apiai-weather-webhook-sample'}  # "data": data,


                                                       # "contextOut": [],

def makeWebhookParameters(req):
    result = req.get('result')
    parameters = result.get('parameters')

    # tipo_id = parameters.get('any')  # commented on 19th Feb
    # tipo_id = list(parameters)[0]    # as API.AI is including all the entity in the intent we have changing the value based on length

    for (entity_name, entity_value) in parameters.items():
        if len(entity_value) > 0:
            tipo_id = entity_name
            print('Inside the funtion makeWebhookParameters', tipo_id)
            break

    # if tipo_id is None:
        # return None

   # print('Inside the funtion makeWebhookParameters')

    return tipo_id


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print('Starting app on port %d' % port)

    app.run(debug=False, port=port, host='0.0.0.0')
