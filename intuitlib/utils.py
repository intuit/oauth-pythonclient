 # Copyright (c) 2018 Intuit
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 #  http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.

"""This module contains utility methods used by this library
"""

import json
from base64 import b64encode, b64decode, urlsafe_b64decode
from datetime import datetime
import random
import string
from jose import jwk
import requests
from requests.sessions import Session
import six
from requests_oauthlib import OAuth1


from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError
from intuitlib.config import DISCOVERY_URL, ACCEPT_HEADER

def get_discovery_doc(environment, session=None):
    """Gets discovery doc based on environment specified.
    :param environment: App environment, accepted values: 'sandbox','production','prod','e2e'
    :param session: `requests.Session` object if a session is already being used, defaults to None
    :return: Discovery doc response 
    :raises HTTPError: if response status != 200
    """
    if environment.lower() in ['production', 'prod']:
        discovery_url = DISCOVERY_URL['production']
    elif environment.lower() in ['sandbox', 'sand']:
        discovery_url = DISCOVERY_URL['sandbox']
    else:
        discovery_url = environment
        
    if session is not None and isinstance(session, Session):
        response = session.get(url=discovery_url)
    else:
        response = requests.get(url=discovery_url)
    if response.status_code != 200:
        raise AuthClientError(response)
    return response.json()

def set_attributes(obj, response_json):
    """Sets attribute to an object from a dict
    
    :param obj: Object to set the attributes to
    :param response_json: dict with key names same as object attributes
    """

    for key in response_json:
        if key not in ['token_type', 'id_token']:
            setattr(obj, key, response_json[key])
    
    if 'id_token' in response_json:
        if response_json['id_token'] is not None:
            is_valid = validate_id_token(response_json['id_token'], obj.client_id, obj.issuer_uri, obj.jwks_uri)
            if is_valid:
                obj.id_token = response_json['id_token']  

def send_request(method, url, header, obj, body=None, session=None, oauth1_header=None):
    """Makes API request using requests library, raises `intuitlib.exceptions.AuthClientError` if request not successful and sets specified object attributes from API response if request successful
    
    :param method: HTTP method type
    :param url: request URL
    :param header: request headers
    :param obj: object to set the attributes to
    :param body: request body, defaults to None
    :param session: requests session, defaults to None
    :param oauth1_header: OAuth1 auth header, defaults to None
    :raises AuthClientError: In case response != 200
    :return: requests object
    """

    headers = ACCEPT_HEADER
    header.update(headers)

    if session is not None and isinstance(session, Session):
        response = session.request(method, url, headers=header, data=body, auth=oauth1_header)
    else:
        response = requests.request(method, url, headers=header, data=body, auth=oauth1_header) 

    if response.status_code != 200:
        raise AuthClientError(response)

    if response.content:
        set_attributes(obj, response.json())

    return response

def get_auth_header(client_id, client_secret):
    """Gets authorization header 
    
    :param client_id: Client ID
    :param client_secret: Client Secret
    :return: Authorization header
    """

    auth_header = '{0}:{1}'.format(client_id, client_secret)
    if six.PY3:
        auth_header = auth_header.encode('utf-8')
    return ' '.join(['Basic', b64encode(auth_header).decode('utf-8')])

def scopes_to_string(scopes):
    """Converts list of enum to string
    
    :param scopes: Scopes specified for OAuth/OpenID flow  
    :type scopes: list of `intuitlib.enums.Scopes`
    :raises TypeError: for invalid input for scope 
    :return: Scopes string
    """
    
    for scope in scopes:
        if not isinstance(scope, Scopes) or not isinstance(scopes, list):
            raise TypeError('Please use enum of type Scopes in list for scopes.')
    return ' '.join(scope.value for scope in scopes).strip()

def generate_token(length=30, allowed_chars=''.join([string.ascii_letters, string.digits])):
    """Generates random CSRF token
    
    :param length: Length of CSRF token, defaults to 30
    :param allowed_chars: Characters to use, defaults to 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    :return: Token string
    """

    return ''.join(random.choice(allowed_chars) for i in range(length))

def validate_id_token(id_token, client_id, intuit_issuer, jwk_uri):
    """Validates ID Token returned by Intuit
    
    :param id_token: ID Token
    :param client_id: Client ID
    :param intuit_issuer: Intuit Issuer
    :param jwk_uri: JWK URI
    :return: True/False
    """

    id_token_parts = id_token.split('.')
    if len(id_token_parts) < 3:
        return False

    id_token_header = json.loads(b64decode(_correct_padding(id_token_parts[0])).decode('ascii'))
    id_token_payload = json.loads(b64decode(_correct_padding(id_token_parts[1])).decode('ascii'))
    id_token_signature = urlsafe_b64decode(((_correct_padding(id_token_parts[2])).encode('ascii')))

    if id_token_payload['iss'] != intuit_issuer:
        return False
    elif id_token_payload['aud'][0] != client_id:
        return False

    current_time = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
    if id_token_payload['exp'] < current_time:
        return False

    message = id_token_parts[0] + '.' + id_token_parts[1]
    keys_dict = get_jwk(id_token_header['kid'], jwk_uri)

    public_key = jwk.construct(keys_dict)
    is_signature_valid = public_key.verify(message.encode('utf-8'), id_token_signature)
    return is_signature_valid

def get_jwk(kid, jwk_uri):
    """Get JWK for public key information
    
    :param kid: KID
    :param jwk_uri: JWK URI

    :raises HTTPError: if response status != 200
    :return: dict containing keys
    """

    response = requests.get(jwk_uri)
    if response.status_code != 200:
        raise AuthClientError(response)
    data = response.json()
    keys = next(key for key in data["keys"] if key['kid'] == kid)
    return keys

def _correct_padding(val):
    """Correct padding for JWT
    
    :param val: value to correct
    """

    return val + '=' * (4 - len(val) % 4)
