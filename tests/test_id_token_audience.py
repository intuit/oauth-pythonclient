"""Exercise audience handling with real RS256 signatures."""

import time
from types import SimpleNamespace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from intuitlib.utils import validate_id_token


@pytest.fixture(scope='module')
def signing_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.mark.parametrize('audience, expected', [
    ('client-id', True),
    (['client-id'], True),
    ('other-client', False),
    ('client-id-suffix', False),
    (['other-client'], False),
])
def test_id_token_audience(signing_key, monkeypatch, audience, expected):
    monkeypatch.setattr('intuitlib.utils.get_jwk',
                        lambda *_: SimpleNamespace(key=signing_key.public_key()))
    token = jwt.encode(
        {'iss': 'https://issuer.example', 'aud': audience,
         'exp': int(time.time()) + 3600},
        signing_key, algorithm='RS256', headers={'kid': 'test-key'},
    )
    assert validate_id_token(token, 'client-id', 'https://issuer.example',
                             'https://issuer.example/keys') is expected


def test_string_audience_still_requires_valid_signature(signing_key, monkeypatch):
    other_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    monkeypatch.setattr('intuitlib.utils.get_jwk',
                        lambda *_: SimpleNamespace(key=other_key.public_key()))
    token = jwt.encode(
        {'iss': 'https://issuer.example', 'aud': 'client-id',
         'exp': int(time.time()) + 3600},
        signing_key, algorithm='RS256', headers={'kid': 'test-key'},
    )
    assert not validate_id_token(token, 'client-id', 'https://issuer.example',
                                 'https://issuer.example/keys')
