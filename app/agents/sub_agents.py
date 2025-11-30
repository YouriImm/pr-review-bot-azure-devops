"""
Functions which get added to the coordinator agent as tools. The tools themselves are/contain agents.

There is a fair bit of code repetition in this file but for now I am okay with it. Of course we could generalize but
I like how easy to read each individual sub-agent's code is.
"""

import logfire
from pydantic_ai import RunContext, Agent

from app.agents.models import sub_agent_model
from app.models.review_models import ReviewOutcomeItem, ReviewInput, ReviewRuleLanguage, ReviewRequest
from app.prompts.markdown_reviewer import MD_REVIEWER_PROMPT
from app.prompts.python_reviewer import PYTHON_REVIEWER_PROMPT
from app.prompts.sql_reviewer import SQL_REVIEWER_PROMPT
from app.rules import get_review_rules


# Keeping RunContext in even though it's not strictly used as most future extensions would be sure to require it.
async def python_code_reviewer(ctx: RunContext, review_request: ReviewRequest):
    """
    Tool for reviewing Python code.

    Args:
        ctx: The run context for this review run
        review_request: The input data for this review run, featuring:
            review_rules: The list of review rules to use when reviewing this function.
            file_path: The file path for the content you are asked to review. This must always be formatted as relative path.
            file_content: The file content that needs to be reviewed

    """
    logfire.info("Starting Python code reviewer agent.", file_path=review_request.file_path)

    python_rules = await get_review_rules(language=ReviewRuleLanguage.PYTHON)

    review_input = ReviewInput(
        reviewRules=python_rules, filePath=review_request.file_path, fileContent=review_request.file_content
    )

    agent = Agent(
        model=sub_agent_model,
        deps_type=ReviewInput,
        output_type=list[ReviewOutcomeItem] | None,
        system_prompt=PYTHON_REVIEWER_PROMPT,
    )

    @agent.system_prompt
    def get_review_specification(ctx: RunContext[ReviewInput]) -> str:
        return (
            f"The list of review rules is: {ctx.deps.review_rules}. \n\n "
            f"The file content is: {ctx.deps.file_content}. \n\n "
            f"The file path is: {ctx.deps.file_path}."
        )

    response = await agent.run("Complete the review with the specification provided.", deps=review_input)
    return response.output


async def sql_code_reviewer(ctx: RunContext, review_request: ReviewRequest):
    """
    Tool for reviewing SQL code.

    Args:
        ctx: The run context for this review run
        review_request: The input data for this review run, featuring:
            review_rules: The list of review rules to use when reviewing this function.
            file_path: The file path for the content you are asked to review. This must always be formatted as relative path.
            file_content: The file content that needs to be reviewed

    """
    logfire.info("Starting SQL code reviewer agent.", file_path=review_request.file_path)

    sql_rules = await get_review_rules(language=ReviewRuleLanguage.SQL)

    review_input = ReviewInput(
        reviewRules=sql_rules, filePath=review_request.file_path, fileContent=review_request.file_content
    )

    agent = Agent(
        model=sub_agent_model,
        deps_type=ReviewInput,
        output_type=list[ReviewOutcomeItem] | None,
        system_prompt=SQL_REVIEWER_PROMPT,
    )

    @agent.system_prompt
    def get_review_specification(ctx: RunContext[ReviewInput]) -> str:
        return (
            f"The list of review rules is: {ctx.deps.review_rules}. \n\n "
            f"The file content is: {ctx.deps.file_content}. \n\n "
            f"The file path is: {ctx.deps.file_path}."
        )

    response = await agent.run("Complete the review with the specification provided.", deps=review_input)
    return response.output


async def markdown_docs_reviewer(ctx: RunContext, review_request: ReviewRequest):
    """
    Tool for reviewing Markdown docs.

    Args:
        ctx: The run context for this review run
        review_request: The input data for this review run, featuring:
            review_rules: The list of review rules to use when reviewing this function.
            file_path: The file path for the content you are asked to review. This must always be formatted as relative path.
            file_content: The file content that needs to be reviewed

    """
    logfire.info("Starting Markdown docs reviewer agent.", file_path=review_request.file_path)

    md_rules = await get_review_rules(language=ReviewRuleLanguage.MD)

    review_input = ReviewInput(
        reviewRules=md_rules, filePath=review_request.file_path, fileContent=review_request.file_content
    )

    agent = Agent(
        model=sub_agent_model,
        deps_type=ReviewInput,
        output_type=list[ReviewOutcomeItem] | None,
        system_prompt=MD_REVIEWER_PROMPT,
    )

    @agent.system_prompt
    def get_review_specification(ctx: RunContext[ReviewInput]) -> str:
        return (
            f"The list of review rules is: {ctx.deps.review_rules}. \n\n "
            f"The file content is: {ctx.deps.file_content}. \n\n "
            f"The file path is: {ctx.deps.file_path}."
        )

    response = await agent.run("Complete the review with the specification provided.", deps=review_input)
    return response.output
