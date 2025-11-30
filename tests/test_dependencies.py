from datetime import datetime, UTC, timedelta
from unittest.mock import patch, Mock

import jwt
import pytest
from fastapi import HTTPException, Request

from app.dependencies import validate_authorization_header, _extract_auth_header
from tests.base import BaseTestCase


class TestDependencies(BaseTestCase):
    @pytest.mark.asyncio
    async def test_authorization_header_must_start_with_bearer(self):
        with pytest.raises(HTTPException):
            await validate_authorization_header(authorization="Nonsense")

    @pytest.mark.asyncio
    @patch("app.dependencies.get_azure_devops_settings")
    async def test_authorization_header_with_valid_token_is_accepted(self, mock_settings):
        payload = {"sub": "youri", "iat": datetime.now(UTC), "exp": datetime.now(UTC) + timedelta(days=90)}

        secret_key = "234"
        mock_settings.return_value.JWT_SECRET_STRING = secret_key
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        result = await validate_authorization_header(authorization=f"Bearer {token}")

        assert result == f"Bearer {token}"

    @pytest.mark.asyncio
    @patch("app.dependencies.get_azure_devops_settings")
    async def test_authorization_header_with_invalid_token_is_rejected(self, mock_settings):
        mock_settings.return_value.JWT_SECRET_STRING = "123"
        with pytest.raises(HTTPException) as exc_info:
            await validate_authorization_header(authorization="Bearer madness")

        assert "invalid" in exc_info.value.detail.lower()

    @pytest.mark.asyncio
    @patch("app.dependencies.get_azure_devops_settings")
    async def test_authorization_header_with_expired_token_is_rejected(self, mock_settings):
        payload = {"sub": "youri", "iat": datetime.now(UTC), "exp": datetime.now(UTC) - timedelta(days=1)}

        secret_key = "234"
        mock_settings.return_value.JWT_SECRET_STRING = secret_key
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        with pytest.raises(HTTPException) as exc_info:
            await validate_authorization_header(authorization=f"Bearer {token}")

        assert "expired" in exc_info.value.detail.lower()

    def test_get_auth_headers_succesfully(self):
        mock = Mock(spec=Request)
        mock.headers = {"Authorization": "Bearer test_bearer_token"}

        assert _extract_auth_header(mock) == "test_bearer_token"

    def test_invalid_auth_header_returns_default(self):
        mock = Mock(spec=Request)
        mock.headers = {}

        assert _extract_auth_header(mock) == "unknown"
