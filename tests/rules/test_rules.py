import json
from unittest import mock

import pytest

from app.models.review_models import ReviewRuleLanguage
from app.rules import get_review_rules
from tests.base import BaseTestCase


class TestReviewRuleRetrieval(BaseTestCase):
    @pytest.mark.asyncio
    async def test_can_retrieve_rules_for_valid_language(self, temp_storage_dir):
        dummy_rules = [
            {
                "id": "SEC001",
                "title": "Avoid hardcoded secrets",
                "description": "Never hardcode passwords, API keys, or other sensitive information directly in source code",
                "severity": "critical",
                "code_smells": [
                    "Hardcoded strings that look like passwords or API keys",
                    "Direct assignment of sensitive values",
                ],
            },
            {
                "id": "SEC002",
                "title": "SQL injection prevention",
                "description": "Use parameterized queries to prevent SQL injection attacks",
                "severity": "critical",
                "code_smells": ["String concatenation in SQL queries", "f-strings used to build SQL statements"],
            },
        ]

        rules_file = temp_storage_dir.joinpath("python_rules.json")
        rules_file.write_text(json.dumps(dummy_rules))

        with mock.patch("app.rules.__file__", str(temp_storage_dir.joinpath("__init__.py"))):
            result = await get_review_rules(ReviewRuleLanguage.PYTHON)
            assert len(result) == 2

    @pytest.mark.asyncio
    async def test_raises_value_error_for_missing_language(self, temp_storage_dir):
        with mock.patch("app.rules.__file__", str(temp_storage_dir.joinpath("__init__.py"))):
            with pytest.raises(ValueError):
                await get_review_rules(ReviewRuleLanguage.PYTHON)

    @pytest.mark.asyncio
    async def test_raises_value_error_if_load_fails(self, temp_storage_dir):
        dummy_rules = [
            {
                "id": "SEC001",
                "title": "Avoid hardcoded secrets",
                "description": "Never hardcode passwords, API keys, or other sensitive information directly in source code",
                "severity": "critical",
                "code_smells": [
                    "Hardcoded strings that look like passwords or API keys",
                    "Direct assignment of sensitive values",
                ],
            },
            {
                "id": "SEC002",
                "title": "SQL injection prevention",
                "description": "Use parameterized queries to prevent SQL injection attacks",
                "severity": "critical",
                "code_smells": ["String concatenation in SQL queries", "f-strings used to build SQL statements"],
            },
        ]

        rules_file = temp_storage_dir.joinpath("python_rules.json")
        rules_file.write_text(json.dumps(dummy_rules))

        with (
            mock.patch("app.rules.__file__", str(temp_storage_dir.joinpath("__init__.py"))),
            mock.patch("app.rules.json.load", side_effect=Exception("Something went wrong")),
        ):
            with pytest.raises(ValueError):
                await get_review_rules(ReviewRuleLanguage.PYTHON)
