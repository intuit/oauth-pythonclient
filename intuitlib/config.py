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

"""This module contains static URLs 
"""
import platform
from intuitlib import version

MIGRATION_URL = {
    'sandbox': 'https://developer-sandbox.api.intuit.com/v2/oauth2/tokens/migrate',
    'production': 'https://developer.api.intuit.com/v2/oauth2/tokens/migrate',
}

DISCOVERY_URL = {
    'sandbox': 'https://developer.intuit.com/.well-known/openid_sandbox_configuration/',
    'production': 'https://developer.intuit.com/.well-known/openid_configuration/',
}

OAUTH2_ISSUER = "https://oauth.platform.intuit.com/op/v1"
OAUTH2_AUTH_ENDPOINT = "https://appcenter.intuit.com/connect/oauth2"
OAUTH2_TOKEN_ENDPOINT = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
OAUTH2_REV_ENDPOINT = "https://developer.api.intuit.com/v2/oauth2/tokens/revoke"
OAUTH2_JWKS_URI = "https://oauth.platform.intuit.com/op/v1/jwks"
OAUTH2_SANDBOX = "https://sandbox-accounts.platform.intuit.com/v1/openid_connect/userinfo"
OAUTH2_PROD = "https://accounts.platform.intuit.com/v1/openid_connect/userinfo"

# info for user-agent
PYTHON_VERSION = platform.python_version()
OS_SYSTEM = platform.uname()[0]
OS_RELEASE_VER = platform.uname()[2]
OS_MACHINE = platform.uname()[4]

ACCEPT_HEADER = {
    'Accept': 'application/json',
    'User-Agent': '{0}-{1}-{2}-{3} {4} {5} {6}'.format('Intuit-OAuthClient', version.__version__,'Python', PYTHON_VERSION, OS_SYSTEM, OS_RELEASE_VER, OS_MACHINE)
}
