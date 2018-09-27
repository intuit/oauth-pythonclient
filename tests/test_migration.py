
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

"""Test module for intuitlib.client
"""
from __future__ import unicode_literals
import six
import pytest
import mock

try:
    from urllib.parse import urlparse, parse_qs, urlsplit
except ImportError:
    from urlparse import urlparse, parse_qs, urlsplit

from intuitlib.enums import Scopes
from intuitlib.client import AuthClient
from intuitlib.exceptions import AuthClientError
from intuitlib.migration import migrate
from tests.helper import MockResponse

class TestMigration():
    
    auth_client = AuthClient('clientId','secret','https://www.mydemoapp.com/oauth-redirect','sandbox')

    client_mock_discovery_urls = {
        'authorization_endpoint': 'test',
        'token_endpoint': 'test',
        'revocation_endpoint': 'test',
        'issuer': 'test',
        'jwks_uri': 'test',
        'userinfo_endpoint': 'test',
    }

    def mock_request(self, status=200, content=None):
        return MockResponse(status=status, content=content)

    @mock.patch('intuitlib.utils.requests.request')
    def test_migrate_bad_request(self, mock_post):
        mock_resp = self.mock_request(status=400)
        mock_post.return_value = mock_resp

        with pytest.raises(AuthClientError):
            migrate('consumer_key', 'consumer_secret', 'access_token', 'access_secret', self.auth_client, [Scopes.ACCOUNTING])

    @mock.patch('intuitlib.utils.requests.request')
    def test_migrate_200(self, mock_post):
        mock_resp = self.mock_request(status=200, content={
            'access_token': 'testaccess'
        })
        mock_post.return_value = mock_resp

        migrate('consumer_key', 'consumer_secret', 'access_token', 'access_secret', self.auth_client, [Scopes.ACCOUNTING])

        assert self.auth_client.access_token == 'testaccess'

    @mock.patch('intuitlib.utils.requests.request')
    def test_migrate_prod(self, mock_post):
        mock_resp = self.mock_request(status=400)
        mock_post.return_value = mock_resp
        self.auth_client.environment = 'production'

        with pytest.raises(AuthClientError):
            migrate('consumer_key', 'consumer_secret', 'access_token', 'access_secret', self.auth_client, [Scopes.ACCOUNTING])

if __name__ == '__main__':
    pytest.main()