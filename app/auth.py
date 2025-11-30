"""
Azure DevOps authentication and configuration management.
"""

import os
from datetime import datetime
from functools import lru_cache
from typing import Optional
from urllib.parse import urljoin

import logfire
from azure.core.credentials import AccessToken
from azure.identity import EnvironmentCredential
from fastapi import HTTPException
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AzureDevOpsSettings(BaseSettings):
    """General application settings, primarily for Azure DevOps.
    pydantic-settings will give priority to environment variables and will refer to .env if those can't be found.
    Refer to the docs: https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support."""

    ORGANIZATION: str = Field(default="", description="Name of the Azure DevOps organization.")
    PROJECT: str = Field(default="", description="Name of the Azure DevOps project.")
    AZURE_TENANT_ID: str = Field(default="", description="Tenant ID for the Azure Entra ID App Registration.")
    AZURE_CLIENT_ID: str = Field(default="", description="Client ID for the Azure Entra ID App Registration.")
    AZURE_CLIENT_SECRET: str = Field(default="", description="Client Secret for the Azure Entra ID App Registration.")
    AGENT_API_KEY: str = Field(default="", description="API key to authenticate the LLM Agent.")
    LOGFIRE_DEPLOYMENT_ENV: str = Field(default="", description="Deployment environment for observability.")
    JWT_SECRET_STRING: str = Field(default="", description="Secret key for JWT encoding.")

    model_config = SettingsConfigDict(env_prefix="PR_APP_", env_file=".env", extra="ignore")


@lru_cache(maxsize=1)
def get_azure_devops_settings() -> AzureDevOpsSettings:
    """Instantiate a settings object or return a cached one."""
    return AzureDevOpsSettings()


class CachedToken:
    def __init__(self, token: AccessToken):
        self.token = token

    def is_expired(self, buffer_minutes: int = 5) -> bool:
        """Buffer to protect against a token that would expire mid-review."""
        import time

        return time.time() >= (self.token.expires_on - (buffer_minutes * 60))


class AzureDevOpsAuth:
    """Azure DevOps authentication handler using service principal."""

    def __init__(self, settings: AzureDevOpsSettings):
        self.settings = settings
        self._credential: Optional[EnvironmentCredential] = None
        self._cached_token: Optional[CachedToken] = None

    def _refresh_token(self) -> CachedToken:
        """Get a fresh auth token for Azure DevOps."""

        if not self._credential:
            self._credential = EnvironmentCredential()

        # That string is the permissions scope for the Azure DevOps REST API. Not dynamic, so fine to hardcode.
        # Very sneakily hidden in the docs!
        # https://learn.microsoft.com/en-us/rest/api/azure/devops/tokens/?view=azure-devops-rest-7.1
        token_response: AccessToken = self._credential.get_token("499b84ac-1321-427f-aa17-267ca6975798/.default")
        logfire.info(
            "Azure DevOps Token retrieved.", expiry_timestamp=datetime.fromtimestamp(token_response.expires_on)
        )

        return CachedToken(token_response)

    def _get_token(self) -> str:
        """Get a valid auth token using cached token if available"""

        if self._cached_token and not self._cached_token.is_expired():
            logfire.info("Using cached Azure DevOps access token")
            return self._cached_token.token.token

        logfire.info("Cached token missing or expired, fetching new token")
        self._cached_token = self._refresh_token()
        return self._cached_token.token.token

    def _set_environment_variables(self) -> None:
        """Takes the variables needed for spn-based authentication and sets them with the names azure mandates.
        This ensures our variable names within AzureDevOpsSettings are decoupled from mandatory variable names."""

        os.environ["AZURE_TENANT_ID"] = self.settings.AZURE_TENANT_ID
        os.environ["AZURE_CLIENT_ID"] = self.settings.AZURE_CLIENT_ID
        os.environ["AZURE_CLIENT_SECRET"] = self.settings.AZURE_CLIENT_SECRET

    def get_auth_headers(self) -> dict[str, str]:
        """Generate and format Authorization bearer token for Azure DevOps REST API."""
        try:
            self._set_environment_variables()
            token = self._get_token()
            return {
                "Authorization": f"Bearer {token}"
                # "Content-Type": "application/json"
            }

        except Exception as e:
            logfire.error(f"Failed to get auth headers: {e}")
            raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

    def build_api_url(self, endpoint: str) -> str:
        """Return the full API url for a given endpoint."""
        return urljoin(
            f"https://dev.azure.com/{self.settings.ORGANIZATION}/{self.settings.PROJECT}/_apis/", endpoint.lstrip("/")
        )


@lru_cache(maxsize=1)
def get_azure_devops_auth() -> AzureDevOpsAuth:
    """Instantiate an AzureDevOpsAuth object or return a cached one.
    Because it is entirely possible we will use AzureDevOpsSettings objects independently of the AzureDevOpsAuth class
    in which it is embedded, we keep the methods to instantiate them separate."""

    settings = get_azure_devops_settings()
    return AzureDevOpsAuth(settings)
