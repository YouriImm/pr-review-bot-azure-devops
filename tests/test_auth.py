import time
from unittest.mock import patch

import pytest
from azure.core.credentials import AccessToken
from fastapi import HTTPException

from app.auth import AzureDevOpsAuth, CachedToken
from tests.base import BaseTestCase


class TestCachedToken(BaseTestCase):
    def test_is_expired_not_expired(self):
        future_timestamp = int(time.time()) + 3600  # 1 hour from now
        token = AccessToken(token="test_token", expires_on=future_timestamp)
        cached_token = CachedToken(token)

        assert not cached_token.is_expired()

    def test_is_expired_with_buffer(self):
        near_future_timestamp = int(time.time()) + 240  # 4 minutes from now
        token = AccessToken(token="test_token", expires_on=near_future_timestamp)
        cached_token = CachedToken(token)

        # Should be expired due to 5-minute buffer
        assert cached_token.is_expired()

    def test_is_expired_custom_buffer(self):
        near_future_timestamp = int(time.time()) + 240  # 4 minutes from now
        token = AccessToken(token="test_token", expires_on=near_future_timestamp)
        cached_token = CachedToken(token)

        # Should not be expired with 2-minute buffer
        assert not cached_token.is_expired(buffer_minutes=2)

    def test_is_expired_past_timestamp(self):
        past_timestamp = int(time.time()) - 100  # 100 seconds ago
        token = AccessToken(token="test_token", expires_on=past_timestamp)
        cached_token = CachedToken(token)

        assert cached_token.is_expired()


class TestAzureDevOpsAuth(BaseTestCase):
    def test_build_api_url_simple_endpoint(self, auth_instance):
        url = auth_instance.build_api_url("pullrequests")
        expected = "https://dev.azure.com/test-org/test-project/_apis/pullrequests"
        assert url == expected

    def test_build_api_url_with_leading_slash(self, auth_instance):
        url = auth_instance.build_api_url("/pullrequests")
        expected = "https://dev.azure.com/test-org/test-project/_apis/pullrequests"
        assert url == expected

    def test_get_token_caching(self, auth_instance):
        future_timestamp = int(time.time()) + 3600
        mock_token = AccessToken(token="cached_token", expires_on=future_timestamp)

        auth_instance._cached_token = CachedToken(mock_token)

        with patch.object(auth_instance, "_refresh_token") as mock_refresh:
            token = auth_instance._get_token()

            assert token == "cached_token"
            mock_refresh.assert_not_called()

    def test_get_token_refresh_when_expired(self, auth_instance):
        past_timestamp = int(time.time()) - 100
        expired_token = AccessToken(token="expired_token", expires_on=past_timestamp)
        new_token = AccessToken(token="new_token", expires_on=int(time.time()) + 3600)

        # Set up an expired cached token
        auth_instance._cached_token = CachedToken(expired_token)

        with patch.object(auth_instance, "_refresh_token", return_value=CachedToken(new_token)) as mock_refresh:
            token = auth_instance._get_token()

            assert token == "new_token"
            mock_refresh.assert_called_once()

    def test_get_token_no_cached_token(self, auth_instance):
        new_token = AccessToken(token="fresh_token", expires_on=int(time.time()) + 3600)

        with patch.object(auth_instance, "_refresh_token", return_value=CachedToken(new_token)) as mock_refresh:
            token = auth_instance._get_token()

            assert token == "fresh_token"
            mock_refresh.assert_called_once()

    @patch.object(AzureDevOpsAuth, "_get_token")
    @patch.object(AzureDevOpsAuth, "_set_environment_variables")
    def test_get_auth_headers_success(self, mock_set_env, mock_get_token, auth_instance):
        mock_get_token.return_value = "test_bearer_token"

        headers = auth_instance.get_auth_headers()

        expected_headers = {"Authorization": "Bearer test_bearer_token"}
        assert headers == expected_headers
        mock_set_env.assert_called_once()
        mock_get_token.assert_called_once()

    @patch.object(AzureDevOpsAuth, "_get_token")
    @patch.object(AzureDevOpsAuth, "_set_environment_variables")
    def test_get_auth_headers_failure(self, mock_set_env, mock_get_token, auth_instance):
        mock_get_token.side_effect = Exception("Auth failed")

        with pytest.raises(HTTPException) as exc_info:
            auth_instance.get_auth_headers()

        assert exc_info.value.status_code == 401
        assert "Authentication failed: Auth failed" in str(exc_info.value.detail)
