from typing import Any

import logfire
from fastapi import FastAPI

from app.auth import get_azure_devops_settings


def _match_filepath_in_comment(attr_path: tuple) -> bool:
    """The third item in the tuple can be any arbitrary int, so this is an ugly yet effective way to"""
    return (
        len(attr_path) == 4
        and attr_path[0] == "attributes"
        and attr_path[1] == "tool_response"
        and isinstance(attr_path[2], int)
        and attr_path[3] == "file_path"
    )


def scrubbing_callback(match: logfire.ScrubMatch) -> Any | None:
    """Handles exceptions in logfire scrubbing. In certain contexts, override the confidential data scrubbing
    and simply return the plain values anyway."""
    if match.path == ("attributes", "tool_arguments", "thread_context", "filePath") or _match_filepath_in_comment(
        match.path
    ):
        return match.value
    return None


def setup_logfire(app: FastAPI) -> None:
    """Handles configuration and setup for logfire for a certain FastAPI app.
    This function isn't set up like this for reusability but just to keep main.py a little cleaner and to have all
    observability-related setup in one script here.
    """
    logfire.configure(
        environment=get_azure_devops_settings().LOGFIRE_DEPLOYMENT_ENV,
        distributed_tracing=False,
        scrubbing=logfire.ScrubbingOptions(callback=scrubbing_callback),
    )
    logfire.instrument_fastapi(app, excluded_urls=r"^.*\/mcp\/azure-devops$")
    logfire.instrument_pydantic_ai()
