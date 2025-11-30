import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from fastmcp.utilities.tests import run_server_in_process

from app.auth import AzureDevOpsSettings, AzureDevOpsAuth
from app.main import app
from app.mcp.azure_devops_server import AZDO_MCP
from tests.evals.dataset_loader import load_dataset_from_yaml


@pytest.fixture(scope="function")
def auth_instance() -> AzureDevOpsAuth:
    settings = AzureDevOpsSettings(
        ORGANIZATION="test-org",
        PROJECT="test-project",
        AZURE_TENANT_ID="tenant-123",
        AZURE_CLIENT_ID="client-123",
        AZURE_CLIENT_SECRET="secret-123",
        JWT_SECRET_STRING="1234567890abcdefghij1234567890abcdefghij",
    )
    return AzureDevOpsAuth(settings)


@pytest.fixture(scope="function")
def temp_storage_dir() -> Generator[Path, None, None]:
    base_path = Path(os.path.dirname(os.path.realpath(__file__)))
    with tempfile.TemporaryDirectory(dir=base_path) as temp_dir:
        yield Path(temp_dir)


@pytest.fixture(scope="session")
def unawaited_mcp_http_server():
    async def mcp_http_server():
        def run_server(host: str, port: int) -> None:
            AZDO_MCP.run(host=host, port=port)

        with run_server_in_process(run_server, transport="http") as url:
            yield f"{url}/azure-devops"

    return mcp_http_server()


@pytest.fixture(scope="session")
def client(unawaited_mcp_http_server) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def python_rule_eval_dataset():
    return load_dataset_from_yaml(Path("datasets/python_rules.yaml"))


@pytest.fixture
def python_review_comment_eval_dataset():
    return load_dataset_from_yaml(Path("datasets/review_tone_accuracy.yaml"))
