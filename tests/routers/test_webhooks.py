from datetime import datetime, UTC, timedelta
from unittest.mock import patch

import jwt

from app.models.webhooks import TokenValidationResponse
from tests.base import BaseTestCase


class TestWebhookTokens(BaseTestCase):
    @patch("app.routers.webhooks.get_azure_devops_settings")
    def test_can_generate_new_token(self, mock_settings):
        mock_settings.return_value.JWT_SECRET_STRING = "123"

        response = self.client.post("/webhooks/register", json={"client_name": "test"})

        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @patch("app.routers.webhooks.get_azure_devops_settings")
    def test_authorization_header_with_valid_token_is_accepted(self, mock_settings):
        payload = {"sub": "youri", "iat": datetime.now(UTC), "exp": datetime.now(UTC) + timedelta(days=90)}

        secret_key = "234"
        mock_settings.return_value.JWT_SECRET_STRING = secret_key
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        result = self.client.get("/webhooks/validate", headers={"Authorization": f"Bearer {token}"})

        validation_response = TokenValidationResponse(**result.json())
        assert validation_response.valid
        assert validation_response.expires_at is not None

    @patch("app.routers.webhooks.get_azure_devops_settings")
    def test_authorization_header_with_invalid_token_is_rejected(self, mock_settings):
        secret_key = "234"
        mock_settings.return_value.JWT_SECRET_STRING = secret_key
        result = self.client.get("/webhooks/validate", headers={"Authorization": "Bearer nonsense"})

        validation_response = TokenValidationResponse(**result.json())
        assert not validation_response.valid
        assert "invalid" in validation_response.reason.lower()

    @patch("app.routers.webhooks.get_azure_devops_settings")
    def test_authorization_header_with_expired_token_is_rejected(self, mock_settings):
        payload = {"sub": "youri", "iat": datetime.now(UTC), "exp": datetime.now(UTC) - timedelta(days=1)}

        secret_key = "234"
        mock_settings.return_value.JWT_SECRET_STRING = secret_key
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        result = self.client.get("/webhooks/validate", headers={"Authorization": f"Bearer {token}"})

        validation_response = TokenValidationResponse(**result.json())
        assert not validation_response.valid
        assert "expired" in validation_response.reason.lower()
