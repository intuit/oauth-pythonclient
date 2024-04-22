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

import json
import requests

try:
  from urllib.parse import urlencode
except (ModuleNotFoundError, ImportError):
  from future.moves.urllib.parse import urlencode

from intuitlib.utils import (
    get_discovery_doc,
    generate_token,
    scopes_to_string,
    get_auth_header,
    send_request,
)

class AuthClient(requests.Session):
    """Handles OAuth 2.0 and OpenID Connect flows to get access to User Info API, Accounting APIs and Payments APIs
    """

    def __init__(self, client_id, client_secret, redirect_uri, environment, state_token=None, access_token=None, refresh_token=None, id_token=None, realm_id=None):
        """Constructor for AuthClient

        :param client_id: Client ID found in developer account Keys tab
        :param client_secret: Client Secret found in developer account Keys tab
        :param redirect_uri: Redirect URI, handles callback from provider
        :param environment: App Environment, accepted values: 'sandbox','production','prod'
        :param state_token: CSRF token, generated if not provided, defaults to None
        :param access_token: Access Token for refresh or revoke functionality, defaults to None
        :param refresh_token: Refresh Token for refresh or revoke functionality, defaults to None
        :param id_token: ID Token for OpenID flow, defaults to None
        :param realm_id: QBO Realm/Company ID, defaults to None
        """

        super(AuthClient, self).__init__()

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.environment = environment
        self.state_token = state_token

        # Discovery doc contains endpoints based on environment specified
        discovery_doc = get_discovery_doc(self.environment, session=self)
        self.auth_endpoint = discovery_doc['authorization_endpoint']
        self.token_endpoint = discovery_doc['token_endpoint']
        self.revoke_endpoint = discovery_doc['revocation_endpoint']
        self.issuer_uri = discovery_doc['issuer']
        self.jwks_uri = discovery_doc['jwks_uri']
        self.user_info_url = discovery_doc['userinfo_endpoint']

        # response values
        self.realm_id = realm_id
        self.access_token = access_token
        self.expires_in = None
        self.refresh_token = refresh_token
        self.x_refresh_token_expires_in = None
        self.id_token = id_token

    def setAuthorizeURLs(self, urlObject):
        """Set authorization url using custom values passed in the data dict
        :param **data: data dict for custom authorizationURLS
        :return: self
        """
        if urlObject is not None:
            self.auth_endpoint = urlObject['auth_endpoint']
            self.token_endpoint = urlObject['token_endpoint']
            self.revoke_endpoint = urlObject['revoke_endpoint']
            self.user_info_url = urlObject['user_info_url']
        return None

    def get_authorization_url(self, scopes, state_token=None):
        """Generates authorization url using scopes specified where user is redirected to

        :param scopes: Scopes for OAuth/OpenId flow
        :type scopes: list of enum, `intuitlib.enums.Scopes`
        :param state_token: CSRF token, defaults to None
        :return: Authorization url
        """

        state = state_token or self.state_token
        if state is None:
            state = generate_token()
        self.state_token = state

        url_params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'scope': scopes_to_string(scopes),
            'redirect_uri': self.redirect_uri,
            'state': self.state_token
        }

        return '?'.join([self.auth_endpoint, urlencode(url_params)])

    def get_bearer_token(self, auth_code, realm_id=None):
        """Gets access_token and refresh_token using authorization code

        :param auth_code: Authorization code received from redirect_uri
        :param realm_id: Realm ID/Company ID of the QBO company
        :raises `intuitlib.exceptions.AuthClientError`: if response status != 200
        """

        realm = realm_id or self.realm_id
        if realm is not None:
            self.realm_id = realm

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': get_auth_header(self.client_id, self.client_secret)
        }

        body = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }

        send_request('POST', self.token_endpoint, headers, self, body=urlencode(body), session=self)

    def refresh(self, refresh_token=None):
        """Gets fresh access_token and refresh_token

        :param refresh_token: Refresh Token
        :raises ValueError: if Refresh Token value not specified
        :raises `intuitlib.exceptions.AuthClientError`: if response status != 200
        """

        token = refresh_token or self.refresh_token
        if token is None:
            raise ValueError('Refresh token not specified')

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': get_auth_header(self.client_id, self.client_secret)
        }

        body = {
            'grant_type': 'refresh_token',
            'refresh_token': token
        }

        send_request('POST', self.token_endpoint, headers, self, body=urlencode(body), session=self)

    def revoke(self, token=None):
        """Revokes access to QBO company/User Info using either valid Refresh Token or Access Token

        :param token: Refresh Token or Access Token to revoke
        :raises ValueError: if Refresh Token or Access Token value not specified
        :raises `intuitlib.exceptions.AuthClientError`: if response status != 200
        :return: True if token successfully revoked
        """

        token_to_revoke = token or self.refresh_token or self.access_token
        if token_to_revoke is None:
            raise ValueError('Token to revoke not specified')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': get_auth_header(self.client_id, self.client_secret)
        }

        body = {
            'token': token_to_revoke
        }

        send_request('POST', self.revoke_endpoint, headers, self, body=json.dumps(body), session=self)
        return True

    def get_user_info(self, access_token=None):
        """Gets User Info based on OpenID scopes specified

        :param access_token: Access token
        :raises ValueError: if Refresh Token or Access Token value not specified
        :raises `intuitlib.exceptions.AuthClientError`: if response status != 200
        :return: Requests object
        """

        token = access_token or self.access_token
        if token is None:
            raise ValueError('Acceess token not specified')

        headers = {
            'Authorization': 'Bearer {0}'.format(token)
        }

        return send_request('GET', self.user_info_url, headers, self, session=self)
