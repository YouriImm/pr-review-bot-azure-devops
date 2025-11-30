"""
This class is used only by the MCP tools and not by other parts of the app.

Choosing not to unit test this class now: Would lead to a lot of mocks. In an enterprise setting I'd go for it because
of the higher impact of even small issues.

The self.auth methods are bespoke and more vulnerable to issues, so they are tested.
"""

from typing import Any

import httpx
import logfire
from fastapi import HTTPException

from app.auth import get_azure_devops_auth, AzureDevOpsAuth


class AzureDevOpsClient:
    """Client for making Azure DevOps API requests with standardized error handling."""

    def __init__(self):
        self.auth: AzureDevOpsAuth = get_azure_devops_auth()
        self.timeout = 30.0  # No reason yet to make dynamic
        self.api_version = "7.1"  # No reason yet to make dynamic

    async def make_get_request(self, endpoint: str, extra_params: dict | None = None) -> dict[str, Any]:
        """
        Make a GET request to Azure DevOps API with standardized error handling.

        Args:
            endpoint: The API endpoint (e.g., "git/repositories")
            extra_params: additional query parameters to provide to the API endpoint (e,g.,"baseVersion")

        Returns:
            dict: json response from the api

        Raises:
            HTTPException: Standardized HTTP exceptions for various 40X and 50X error codes
        """
        url = self.auth.build_api_url(endpoint)
        headers: dict[str, str] = self.auth.get_auth_headers()
        default_params = {"api-version": self.api_version}
        params = {**default_params, **extra_params} if extra_params else default_params

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                logfire.info(
                    f"GET request made by MCP to {endpoint}", url=url, header_keys=headers.keys(), query_params=params
                )
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()

                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type:
                    return response.json()
                else:
                    return {"content": response.text}

            except httpx.HTTPStatusError as e:
                error_detail = f"Azure DevOps API error ({endpoint}): {e.response.status_code}"
                if e.response.status_code == 404:
                    error_detail = f"{endpoint} not found"
                elif e.response.status_code == 401:
                    error_detail = "Authentication failed - check service principal credentials"
                elif e.response.status_code == 403:
                    error_detail = "Access denied - check service principal permissions"

                raise HTTPException(status_code=e.response.status_code, detail=error_detail)
            except httpx.TimeoutException:
                raise HTTPException(status_code=504, detail=f"Azure DevOps API timeout for {endpoint}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error with {endpoint}: {str(e)}")

    async def make_post_request(self, endpoint: str, body: dict | None = None) -> dict[str, Any]:
        """
        Make a POST request to Azure DevOps API with standardized error handling.

        Args:
            endpoint: API endpoint (e.g., "git/repositories/{repositoryId}/pullrequests/{pullRequestId}/threads")
            body: Request body data to send as JSON

        Returns:
            dict: JSON response from API

        Raises:
            HTTPException: Standardized HTTP exceptions for various 40X and 50X error codes
        """
        url = self.auth.build_api_url(endpoint)
        headers = self.auth.get_auth_headers()
        headers["Content-Type"] = "application/json"
        params = {"api-version": self.api_version}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                logfire.info(
                    f"POST request made by MCP to {endpoint}",
                    url=url,
                    header_keys=headers.keys(),
                    query_params=params,
                    body=body,
                )
                response = await client.post(url, headers=headers, params=params, json=body)
                response.raise_for_status()

                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type:
                    return response.json()
                else:
                    return {"content": response.text}

            except httpx.HTTPStatusError as e:
                error_detail = f"Azure DevOps API error ({endpoint}): {e.response.status_code}"
                print(f"Error response: {e.response.text}")
                if e.response.status_code == 404:
                    error_detail = f"{endpoint} not found"
                elif e.response.status_code == 401:
                    error_detail = "Authentication failed - check service principal credentials"
                elif e.response.status_code == 403:
                    error_detail = "Access denied - check service principal permissions"

                raise HTTPException(status_code=e.response.status_code, detail=error_detail)

            except httpx.TimeoutException:
                raise HTTPException(status_code=504, detail=f"Azure DevOps API timeout for {endpoint}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error with {endpoint}: {str(e)}")
