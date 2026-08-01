import pickle

from intuitlib.exceptions import AuthClientError
from tests.helper import MockResponse


class TestExceptions:
    def mock_request(self, status=200, content=None):
        return MockResponse(status=status, content=content)

    def test_authclienterror_is_pickleable(self):
        error = AuthClientError(self.mock_request(404))
        pickle.dumps(error)