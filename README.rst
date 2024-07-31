Intuit's OAuth2 and OpenID Connect Python Client
=================================================

|coverage| |docs|

.. |coverage| image:: https://coveralls.io/repos/github/intuit/oauth-pythonclient/badge.svg?branch=master
    :target: https://coveralls.io/github/intuit/oauth-pythonclient?branch=master

.. |docs| image:: https://readthedocs.org/projects/oauth-pythonclient/badge/?version=latest
    :target: https://oauth-pythonclient.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

The official Python client library for working with Intuit APIs. 
The `AuthClient` object response can be used for the 
`Intuit UserInfo API <https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/openid-connect#obtaining-user-profile-information>`_, 
`QuickBooks Accounting API <https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api>`_, 
and `QuickBooks Payments API <https://developer.intuit.com/app/developer/qbpayments/docs/learn/explore-the-quickbooks-payments-api>`_. 

This library supports:

- Raising authorization requests
- Requesting OAuth2 bearer (access) tokens
- Refreshing OAuth2 tokens
- Revoking OAuth2 tokens
- Validating ID tokens
- Fetching profile attributes from UserInfo
- Various utility methods
- Migrating tokens from OAuth1.0 to OAuth2

Install
-------

Using `pip <https://pypi.org/project/pip/>`_: ::
    
    $ pip install intuit-oauth

Documentation
-------------

Usage and reference documentation can be found at `oauth-pythonclient.readthedocs.io <https://oauth-pythonclient.readthedocs.io/en/latest/>`_.

Sample App
----------

A sample app for this library can be found on the `IntuitDeveloper GitHub Org <https://github.com/IntuitDeveloper/SampleOAuth2_UsingPythonClient>`_.

Issues and Contributions
------------------------

Please open an `issue <https://github.com/intuit/oauth-pythonclient/issues>`_ on GitHub if you have anything to report, a suggestion, or comment.

Pull requests are welcomed and encouraged! Any contributions should include new or updated unit tests as necessary to maintain thorough test coverage.

License
-------

This library is provided under Apache 2.0 which is found `here <https://github.com/intuit/oauth-pythonclient/blob/master/LICENSE>`_
