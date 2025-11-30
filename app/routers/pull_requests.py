from urllib.parse import urljoin

import logfire
from fastapi import APIRouter, Request, Depends, BackgroundTasks
from pydantic_ai import Agent, RunContext, UsageLimits, UsageLimitExceeded, UnexpectedModelBehavior, AgentRunError
from pydantic_ai.mcp import MCPServerStreamableHTTP

from app.agents.models import coordinator_agent_model
from app.agents.sub_agents import python_code_reviewer, sql_code_reviewer, markdown_docs_reviewer
from app.dependencies import validate_authorization_header, limiter
from app.models.agents import PullRequestAgentDeps, FallbackAgentDeps
from app.prompts.core import PR_REVIEWER_PROMPT
from app.prompts.errors import ERROR_PROMPT

router = APIRouter(
    prefix="/pull-requests",
    tags=["pull_requests"],
    dependencies=[Depends(validate_authorization_header), Depends(limiter)],
)


@router.post("/{pull_request_id}/tmpwrap")
async def tmpwrap(pull_request_id: int, request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(review_created_pull_request, pull_request_id, request)
    return {"status": "success"}


# Currently defined this as route, but later we may conclude this can be a plain function
# At least this way we have the router-wide dependency execution which is nice
@router.post("/{pull_request_id}/created")
async def review_created_pull_request(pull_request_id: int, request: Request):
    logfire.info("Starting PR Review", pull_request_id=pull_request_id)

    # We don't pre-define the MCP toolset but instantiate it live, so we can refer to the URL of the mounted FastMCP app
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    mcp_tool = MCPServerStreamableHTTP(url=urljoin(base_url, "/mcp/azure-devops"))

    # We instantiate the agent class here for the same reason, we want dynamic parts resolved at init time
    # If we later have a stand-alone MCP server ten we can pre-instantiate this and call it here like normal!
    agent = Agent(
        model=coordinator_agent_model,
        deps_type=PullRequestAgentDeps,
        toolsets=[mcp_tool],
        tools=[python_code_reviewer, sql_code_reviewer, markdown_docs_reviewer],
        system_prompt=PR_REVIEWER_PROMPT,
    )

    # Dynamic part of the sys prompt, keep it here because we want the PR ID which is sourced from the POST call itself
    @agent.system_prompt
    def get_the_pull_request_id(ctx: RunContext[PullRequestAgentDeps]) -> str:
        return f"The pull request id is {ctx.deps.pull_request_id}."

    try:
        output = await agent.run(
            "Please review the pull request that is provided to you.",
            deps=PullRequestAgentDeps(pull_request_id=pull_request_id, request=request),
            usage_limits=UsageLimits(tool_calls_limit=40, output_tokens_limit=20000, input_tokens_limit=250000),
        )
        return {output.output}

    except (UsageLimitExceeded, UnexpectedModelBehavior, AgentRunError) as e:
        # Again, instantiate here to dynamically allow the MCP tool. We use it to post a PR comment about the error.
        fallback_agent = Agent(
            model=coordinator_agent_model, toolsets=[mcp_tool], deps_type=FallbackAgentDeps, system_prompt=ERROR_PROMPT
        )

        @fallback_agent.system_prompt
        def add_the_error_message_and_pr_id(ctx: RunContext[FallbackAgentDeps]) -> str:
            return (
                f"The pull request id is {ctx.deps.pull_request_id}. \n The error message is: {ctx.deps.error_message}"
            )

        logfire.error(
            f"Abandoning PR review for pull request with ID {pull_request_id} due to an error. Error message: {e}"
        )
        output = await fallback_agent.run(
            "Please handle the error that is provided to you.",
            deps=FallbackAgentDeps(pull_request_id=pull_request_id, error_message=str(e)),
            usage_limits=UsageLimits(output_tokens_limit=1000),
        )
        return {output.output}
