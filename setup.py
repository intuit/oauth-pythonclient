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

from setuptools import setup
from setuptools import find_packages

version = {}
with open("./intuitlib/version.py") as fp:
    exec(fp.read(), version)

setup(
    name='intuit-oauth',
    version=version['__version__'],
    description='Intuit OAuth Client',
    long_description=open('README.rst').read().strip(),
    author='Intuit Inc',
    author_email='IDGSDK@intuit.com',
    url='https://github.com/intuit/oauth-pythonclient',
    packages=find_packages(exclude=('tests*',)),
    namespace_packages=('intuitlib',),
    install_requires=[
        'python_jose>=2.0.2',
        'requests>=2.13.0',
        'requests_oauthlib>=1.0.0',
        'six>=1.10.0',
        'enum-compat',
    ],
    license='Apache 2.0',
    keywords='intuit quickbooks oauth auth openid client'
)
