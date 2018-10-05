.. image:: views/SDK.png 
   :target: https://help.developer.intuit.com/s/samplefeedback?cid=1110&repoName=oauth-pythonclient

Intuit's OAuth2 and OpenID Python Client
========================================

|build| |coverage| |docs|

.. |build| image:: https://travis-ci.com/intuit/oauth-pythonclient.svg?branch=master
    :target: https://travis-ci.com/intuit/oauth-pythonclient

.. |coverage| image:: https://coveralls.io/repos/github/intuit/oauth-pythonclient/badge.svg?branch=master
    :target: https://coveralls.io/github/intuit/oauth-pythonclient?branch=master

.. |docs| image:: https://readthedocs.org/projects/oauth-pythonclient/badge/?version=latest
    :target: https://oauth-pythonclient.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

This client library is meant to work with Intuit's OAuth and OpenID implementation. The `AuthClient` object response can be used for User Info API, Accounting API and Payments API. This library supports:

- Generating Authorization URL
- Getting OAuth2 Bearer Token 
- Getting User Info 
- Validating OpenID token
- Refreshing OAuth2 Token
- Revoking OAuth2 Token
- Migrating tokens from OAuth1.0 to OAuth2

Install
-------

Using `pip <https://pypi.org/project/pip/>`_: ::
    
    $ pip install intuit-oauth

Documentation
-------------

Usage and Reference Documentation can be found at `oauth-pythonclient.readthedocs.io <https://oauth-pythonclient.readthedocs.io/en/latest/>`_ 

Sample App
----------

Sample app for this library can be found at `IntuitDeveloper GitHub Org <https://github.com/IntuitDeveloper/SampleOAuth2_UsingPythonClient>`_

Issues and Contributions
------------------------

Please open an `issue <https://github.com/intuit/oauth-pythonclient/issues>`_ on GitHub if you have a problem, suggestion, or other comment.

Pull requests are welcome and encouraged! Any contributions should include new or updated unit tests as necessary to maintain thorough test coverage.

License
-------

This library is provided under Apache 2.0 which is found `here <https://github.com/intuit/oauth-pythonclient/blob/master/LICENSE>`__
