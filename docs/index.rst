.. intuit-oauth documentation master file, created by
   sphinx-quickstart on Thu Aug 30 15:56:04 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Intuit's OAuth2 and OpenID Connect Client
==========================================

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

`View this library on GitHub <https://github.com/intuit/oauth-pythonclient>`_

Install Client 
--------------
This library can be installed using `pip <https://pypi.org/project/pip/>`_::

    $ pip install intuit-oauth

Docs
----

.. toctree::
    :maxdepth: 2

    user-guide
    Reference <reference/index>

Note
----

The API endpoints in this library only work with TLS 1.2

License
-------

This library is provided under Apache 2.0 which is found `here <https://github.com/intuit/oauth-pythonclient/blob/master/LICENSE>`_

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


