import asyncio
import os

import pytest

from app.agents.sub_agents import python_code_reviewer
from app.auth import get_azure_devops_settings
from app.models.review_models import ReviewRequest, ReviewOutcomeItem
from tests.base import BaseTestCase


@pytest.mark.skipif(os.getenv("CI", 0) == 0, reason="Evals are Skipped outside CI/CD")
class TestEvals(BaseTestCase):
    def _python_review_wrapper(self, inputs: dict) -> list[ReviewOutcomeItem] | None:
        """Wrapper to convert eval inputs to ReviewRequest format."""
        review_request = ReviewRequest(filePath=inputs["file_path"], fileContent=inputs["file_content"])

        return asyncio.run(python_code_reviewer(None, review_request))

    def test_python_rules_are_evaluated(self, python_rule_eval_dataset):
        eval_report = python_rule_eval_dataset.evaluate_sync(self._python_review_wrapper)
        print(eval_report.print(include_output=True, include_reasons=True))
        avg = eval_report.averages()

        assert avg is not None
        assert avg.assertions >= 0.9

    def test_python_rule_violations_receive_fair_comments(self, python_review_comment_eval_dataset):
        # Set env var like this because it is the exact expected name for LLMJudge to use, but elsewhere I don't use it.
        os.environ["ANTHROPIC_API_KEY"] = get_azure_devops_settings().AGENT_API_KEY

        eval_report = python_review_comment_eval_dataset.evaluate_sync(self._python_review_wrapper)
        print(eval_report.print(include_output=True, include_reasons=True))
        avg = eval_report.averages()

        assert avg is not None
        assert avg.assertions >= 0.75
