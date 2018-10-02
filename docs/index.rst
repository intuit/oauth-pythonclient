.. intuit-oauth documentation master file, created by
   sphinx-quickstart on Thu Aug 30 15:56:04 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

   
Intuit's OAuth2 and OpenID Client 
=================================

`View on GitHub <https://github.com/intuit/oauth-pythonclient>`_

This client library is meant to work with Intuit's OAuth and OpenID implementation. The `bearer_token` response can be used for User Info API, Accounting API and Payments API. It supports:

- Generating Authorization URL
- Getting OAuth2 Bearer Token 
- Getting User Info 
- Validating OpenID token
- Refreshing OAuth2 Token
- Revoking OAuth2 Token
- Migrating tokens from OAuth1.0 to OAuth2

Install Client 
--------------
This library can be installed using `pip <https://pypi.org/project/pip/>`_::

    $ pip install intuit-oauth

View it on GitHub `here <https://github.com/intuit/oauth-pythonclient>`_

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


