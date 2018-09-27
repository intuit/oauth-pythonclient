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

import os
import re 
import setuptools

def get_version():
    init_file_path = os.path.join('intuitlib', '__init__.py')
    init_file_lines = open(init_file_path, 'rt').readlines()
    version = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in init_file_lines:
        match = re.search(version, line, re.M)
        if match:
            return match.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (init_file_path,))

setuptools.setup(
    name='intuit-oauth',
    version=get_version(),
    description='Intuit OAuth Client',
    long_description=open('README.rst').read().strip(),
    author='Intuit Inc',
    author_email='IDGSDK@intuit.com',
    url='https://github.com/intuit/oauth-pythonclient',
    install_requires=[
        'python_jose>=2.0.2',
        'future>=0.16.0',
        'requests>=2.13.0',
        'mock>=2.0.0',
        'requests_oauthlib>=1.0.0',
        'pytest>=3.8.0',
        'six>=1.10.0',
        'enum34',
        'python-coveralls',
    ],
    license='Apache 2.0',
    keywords='intuit quickbooks oauth auth openid client'
)
