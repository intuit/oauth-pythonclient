User Guide
==========

Authorize your app
------------------

Step 1: Instantiate AuthClient object 
+++++++++++++++++++++++++++++++++++++
::

    auth_client = AuthClient(
        client_id, 
        client_secret, 
        redirect_uri, 
        environment,
    )

Valid values for environment include `sandbox` and `production`. `redirect_uri` should be set in your Intuit Developer app's Keys tab under the right environment.

Step 2: Get Authorization URL
+++++++++++++++++++++++++++++

Get authorization url by specifying list of `intuitlib.enums.Scopes` ::

    url = auth_client.get_authorization_url([Scopes.ACCOUNTING])

After user connects to the app, the callback URL has params for `state`, `auth_code` and `realm_id` (`realm_id` for Accounting and Payments scopes only)

Step 3: Get Tokens and Expiry details
++++++++++++++++++++++++

The `auth_code` from URL params from Step 2 is used to get bearer tokens. Optionally, `realm_id` is passed to set this property for `auth_client` object. ::
        
    auth_client.get_bearer_token(auth_code, realm_id=realm_id)

After successful response, `access_token`, `refresh_token`, etc properties of `auth_client` object are set.
    
Step 4 (OAuth): Sample API Call
+++++++++++++++++++++++++++++++

Here's a sample API call to show how to use `access_token` to get CompanyInfo for Accounting API. ::

    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    url = '{0}/v3/company/{1}/companyinfo/{1}'.format(base_url, auth_client.realm_id)
    auth_header = 'Bearer {0}'.format(auth_client.access_token)
    headers = {
        'Authorization': auth_header, 
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)

Step 4 (OpenID): User Info API call
+++++++++++++++++++++++++++++++++++

User Info is returned by this method for OpenID scope only: ::
    
    response = auth_client.get_user_info()

Or by passing the `access_token` as a parameter: ::

    response = auth_client.get_user_info(access_token='EnterAccessTokenHere')

Refresh Tokens
--------------

Validity for Intuit's `access_token` is 60 min and `refresh_token` is 24 hours. A fresh `access_token` and `refresh_token` can be retrieved by calling the refresh token endpoint. If `auth_client.refresh_token` property is already set, this can be done by: ::

    auth_client.refresh()

Or by passing the `refresh_token` as a parameter: ::

    auth_client.refresh(refresh_token='EnterRefreshTokenHere')

Revoke Tokens
-------------

If `auth_client.refresh_token` or `auth_client.access_token` property is already set, this can be done by: ::
        
    auth_client.revoke()

Alternatively, pass the `refresh_token` or `access_token` as a parameter: ::

    auth_client.revoke(token='EnterAccessOrRefreshTokenHere')
    
If successfully revoked, this method returns `True`

Migrate OAuth 1.0a Tokens
-------------------------

`Migration` module migrates OAuth 1.0a token to OAuth2 tokens. The method takes in valid OAuth 1.0a tokens (consumer_key, consumer_secret, access_key, access_secret), `auth_client` object from `intuitlib.client.AuthClient` object as well as list of `intuitlib.enum.Scopes` ::

    migrate(
        consumer_key, 
        consumer_secret, 
        access_key, 
        access_secret, 
        auth_client, 
        [Scopes.ACCOUNTING]
    )

Error Handling
--------------

In case of HTTP Errors, the client raises `intuitlib.exceptions.AuthClientError` which has properties `status_code`, `intuit_tid`, `timestamp`, etc which can used for troubleshooting or while contacting `Support <https://help.developer.intuit.com/s/contactsupport/>`_ ::

    try:
        auth_client.get_bearer_token(auth_code, realm_id=realm_id)
    except AuthClientError as e:
        # just printing here but it can be used for retry workflows, logging, etc
        print(e.status_code)
        print(e.content)
        print(e.intuit_tid)




