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

"""Test module for intuitlib.utils
"""

import pytest
import mock
import requests

from intuitlib.utils import (
    get_discovery_doc,
    scopes_to_string,
    set_attributes,
    send_request,
    generate_token,
    get_jwk,
    validate_id_token,
)
from intuitlib.enums import Scopes
from intuitlib.client import AuthClient
from intuitlib.exceptions import AuthClientError
from tests.helper import MockResponse

class TestUtils():

    auth_client = AuthClient('client_id','client_secret','redirect_uri','sandbox')

    def mock_request(self, status=200, content=None):
        return MockResponse(status=status, content=content)

    def test_get_discovery_doc_sandbox(self):
        discovery_doc = get_discovery_doc('sandbox')
        
        assert discovery_doc['issuer'] == 'https://oauth.platform.intuit.com/op/v1'
        assert discovery_doc['userinfo_endpoint'] == 'https://sandbox-accounts.platform.intuit.com/v1/openid_connect/userinfo'

    def test_get_discovery_doc_production(self):
        discovery_doc = get_discovery_doc('production')
        
        assert discovery_doc['issuer'] == 'https://oauth.platform.intuit.com/op/v1'
        assert discovery_doc['userinfo_endpoint'] == 'https://accounts.platform.intuit.com/v1/openid_connect/userinfo'

    def test_get_discovery_doc_custom_url_input(self):
        discovery_doc = get_discovery_doc('https://developer.intuit.com/.well-known/openid_sandbox_configuration/')
        
        assert discovery_doc['issuer'] =='https://oauth.platform.intuit.com/op/v1'
        assert discovery_doc['userinfo_endpoint'] == 'https://sandbox-accounts.platform.intuit.com/v1/openid_connect/userinfo'
    
    @mock.patch('intuitlib.utils.requests.get')
    def test_get_discovery_doc_bad_response(self, mock_get):
        mock_resp = self.mock_request(status=400)
        mock_get.return_value = mock_resp

        with pytest.raises(AuthClientError):
            get_discovery_doc('sandbox')

    def test_scopes_to_string_input_string(self):
        with pytest.raises(TypeError):
            scopes_to_string('openid')

    def test_scopes_to_string_input_list(self):
        with pytest.raises(TypeError):
            scopes_to_string(['openid'])

    def test_scopes_to_string_input_correct(self):
        scope = scopes_to_string([Scopes.OPENID, Scopes.EMAIL])  
        
        assert scope == 'openid email'

    def test_set_attributes(self):
        response = {
            'refresh_token': 'testrefresh',
            'access_token': 'testaccess',
            'test': 'testing',
            'id_token': 'token'
        }
        set_attributes(self.auth_client, response)
        
        assert self.auth_client.refresh_token == response['refresh_token']
        assert self.auth_client.access_token == response['access_token']
        assert not self.auth_client.id_token
    
    @mock.patch('intuitlib.utils.requests.request')
    def test_send_request_bad_request(self, mock_post):
        mock_resp = self.mock_request(status=400)
        mock_post.return_value = mock_resp

        with pytest.raises(AuthClientError):
            send_request('POST', 'url', {}, '', body={})

    @mock.patch('intuitlib.utils.requests.request')
    def test_send_request_ok(self, mock_post):
        mock_resp = self.mock_request(status=200, content={'access_token': 'testaccess'})
        mock_post.return_value = mock_resp

        send_request('POST', 'url', {}, self.auth_client, body={})
        assert self.auth_client.access_token == 'testaccess'
    
    @mock.patch('intuitlib.utils.Session.request')
    def test_send_request_session_ok(self, mock_post):
        mock_resp = self.mock_request(status=200, content={'access_token': 'testaccess'})
        mock_post.return_value = mock_resp
        session = requests.Session()

        send_request('POST', 'url', {}, self.auth_client, body={}, session=session)
        assert self.auth_client.access_token == 'testaccess'

    @mock.patch('intuitlib.utils.Session.request')
    def test_send_request_session_bad(self, mock_post):
        mock_resp = self.mock_request(status=400, content={'access_token': 'testaccess'})
        mock_post.return_value = mock_resp
        session = requests.Session()

        with pytest.raises(AuthClientError):
            send_request('POST', 'url', {}, self.auth_client, body={}, session=session)

    def test_generate_token(self):
        token = generate_token()

        assert len(token) == 30

    @mock.patch('intuitlib.utils.requests.get')
    def test_get_jwk_bad_request(self, mock_get):
        mock_resp = self.mock_request(status=400)
        mock_get.return_value = mock_resp

        with pytest.raises(AuthClientError):
            get_jwk('', 'test_uri')
    
    def test_validate_id_token_bad_idtoken(self):
        id_token = 'firstcomp.secondcomp'
        client_id = 'test'
        intuit_issuer = 'test'
        jwk_uri = 'test_uri'

        is_valid = validate_id_token(id_token, client_id, intuit_issuer, jwk_uri)
        assert not is_valid

    def test_validate_id_token_bad_issuer(self):
        sample_id_token = 'eyJraWQiOiJyNHA1U2JMMnFhRmVoRnpoajhnSSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJiMDUzZDk5NC0wN2Q1LTQ2OGQtYjdlZS0yMmUzNDlkMmU3MzkiLCJhdWQiOlsiTDM5ZWxTdWJGeGpQT1NwZFpvWVdSS2lDQ0U2VElOanY2N1JvYUU4ekJxYkl4eGI0bEsiXSwicmVhbG1pZCI6IjExMDgwMzM0NzEiLCJhdXRoX3RpbWUiOjE0NjI1NTQ0NzUsImlzcyI6Imh0dHBzOlwvXC9vYXV0aC1lMmUucGxhdGZvcm0uaW50dWl0LmNvbVwvb2F1dGgyXC92MVwvb3BcL3YxIiwiZXhwIjoxNDYyNTYxMzI4LCJpYXQiOjE0NjI1NTc3Mjh9.BIJ9x_WPEOZsLJfQE3mGji_Q15j_rdlTyFYELiJM-W92fWSLC-TLEwCp5IrRhDWMvyvrLSMZCEdQALYQpbVy8uKI22JgGWYvkwNEDweOjbYzyt33F4xtn3GGcW9nAwRtA3M19qquWyi7G0kcCZUDN8RfUXz2qKMJ6KPOfLVe2UQ'
        client_id = 'test'
        intuit_issuer = 'test'
        jwk_uri = 'test_uri'

        is_valid = validate_id_token(sample_id_token, client_id, intuit_issuer, jwk_uri)
        assert not is_valid 

if __name__ == '__main__':
    pytest.main()
