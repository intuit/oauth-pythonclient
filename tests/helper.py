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
"""Helper module with MockResponse object
"""

class MockResponse():
    
    def __init__(self, status=200, content=None):
        self.status_code = status
        self.content = content
        self.headers = {
            'intuit_tid': 'mock_tid',
            'Date': 'mock_date',
        }
    
    def json(self):
        return self.content