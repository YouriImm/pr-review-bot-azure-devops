from dataclasses import dataclass

from starlette.requests import Request


@dataclass
class PullRequestAgentDeps:
    pull_request_id: int
    request: Request | None = None


@dataclass
class FallbackAgentDeps:
    pull_request_id: int
    error_message: str
