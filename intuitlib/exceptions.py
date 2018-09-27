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

import requests

class AuthClientError(Exception):
    """AuthClient Error object in case API response status != 200
    """

    def __init__(self, response):
        """Constructor for AuthClientError
        
        :param response: API response
        :type response: `requests` object
        """

        self.response = response
        self.status_code = response.status_code
        self.content = response.content 
        self.headers = response.headers
        self.intuit_tid = response.headers.get('intuit_tid', None) 
        self.timestamp = response.headers.get('Date', None) 

        Exception.__init__(self, 'HTTP status {0}, error message: {1}, intuit_tid {2} at time {3}'.format(self.status_code, self.content, self.intuit_tid, self.timestamp)) 
