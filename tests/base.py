import pytest
from fastapi.testclient import TestClient


class BaseTestCase:
    client: TestClient = None

    @pytest.fixture(autouse=True)
    def setup_fixtures(self, client):
        """Setup pytest fixtures for unittest class."""
        self.client = client
