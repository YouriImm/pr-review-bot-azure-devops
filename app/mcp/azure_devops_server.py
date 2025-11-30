"""
Note that these MCP tools purposefully contain very little logic of their own.
They just call the underlying APIs with strict input & output model validation. Note that the LLM will make use of
the docstrings as well as the metadata in the Pydantic models, so it was worth taking extra effort detailing that out.

The amount of incorrect MCP tool calls made by the coordinator agent notably decreased after adding extra descriptions
to Pydantic models and more inline return specification in the docstrings here.


"""

from fastmcp import FastMCP

from app.mcp import AzureDevOpsClient
from app.models.azure_devops.base_models import GitRepositoryListResponse
from app.models.azure_devops.comment_thread_models import Comment, CommentThreadContext, GitPullRequestCommentThread
from app.models.azure_devops.enums import GitVersionType, CommentThreadStatus
from app.models.azure_devops.git_models import GitCommitDiffs, GitItem
from app.models.azure_devops.pull_request_models import GitPullRequest

AZDO_MCP = FastMCP("Azure DevOps Tools")
AZDO_REST_CLIENT = AzureDevOpsClient()


@AZDO_MCP.tool
async def repo_get_pull_request_by_id(pull_request_id: int) -> GitPullRequest:
    """
    Get information about a pull request by its ID from Azure DevOps.

    Args:
        pull_request_id: The ID of the pull request to retrieve

    Returns:
        GitPullRequest. Complete pull request model with fields from the Azure DevOps API, i.e.:
        - pullRequestId, status, title, description
        - source and target branch ref information
        - createdBy, creationDate, sourceRefName, targetRefName
        - repository, reviewers, commits, mergeStatus
        - completion options, labels, and other metadata

    Raises:
        HTTPException: If the Azure DevOps API GET request fails
    """
    endpoint = f"git/pullrequests/{pull_request_id}"

    body = await AZDO_REST_CLIENT.make_get_request(endpoint)
    return GitPullRequest.model_validate(body)


@AZDO_MCP.tool
async def list_repos() -> GitRepositoryListResponse:
    """
    List all repositories from the authenticated Azure DevOps project.
    The make_get_request() method is already authenticated against the Azure DevOps Project.

    Returns:
        GitRepositoryListResponse. Complete list of GitRepository model objects with fields from the Azure DevOps API, i.e.:
        - count: Total number of repositories
        - value: List of GitRepository objects with fields like:
          - id, name, url, defaultBranch, size
          - project information, remoteUrl, webUrl
          - repository state and maintenance flags

    Raises:
        HTTPException: If the Azure DevOps API GET request fails
    """
    endpoint = "git/repositories"

    body = await AZDO_REST_CLIENT.make_get_request(endpoint)
    return GitRepositoryListResponse.model_validate(body)


@AZDO_MCP.tool
async def get_diffs(repository_id: str, base_version: str, target_version: str) -> GitCommitDiffs:
    """
    Get diffs between two versions in a Git repository.

    Args:
        repository_id: The ID of the repository
        base_version: Base version (branch name)
        target_version: Target version (branch name)

    Returns:
        GitCommitDiffs. Differences between the versions containing:
        - aheadCount, behindCount: Commit count differences
        - changeCounts: Summary of change types (Add, Edit, Delete, etc.)
        - changes: Detailed list of file changes following the GitChangesChange model with change types and items
        - commonCommit: Common ancestor commit ID
        - baseCommit, targetCommit: Optional commit identifiers

    Raises:
        HTTPException: If the Azure DevOps API GET request fails
    """
    endpoint = f"git/repositories/{repository_id}/diffs/commits"
    params = {
        # "api-version": AZDO_REST_CLIENT.api_version,
        "baseVersion": base_version,
        "targetVersion": target_version,
    }

    body = await AZDO_REST_CLIENT.make_get_request(endpoint, params)
    return GitCommitDiffs.model_validate(body)


@AZDO_MCP.tool
async def get_item(
    repository_id: str, path: str, version: str, version_type: GitVersionType, include_content: bool = True
) -> GitItem:
    """
    Get a single item (file or folder) from a Git repository.

    Args:
        repository_id: The ID of the repository
        path: Path to the item (e.g., "/src/main.py")
        version: Version specifier (commit SHA, branch name, or tag)
        version_type: Version type (commit, branch, tag)
        include_content: Whether to include file content in the response (default: True)

    Returns:
        GitItem. Item information containing:
        - objectId: Git object identifier
        - gitObjectType: Object type (blob, tree, commit)
        - commitId: Commit SHA where this item exists
        - path: Item path
        - content: File content (if includeContent=true and item is a file)
        - url: API resource URL
        - isFolder: Whether the item is a folder
        - size: Size of the item in bytes

    Raises:
        HTTPException: If the Azure DevOps API GET request fails
    """
    endpoint = f"git/repositories/{repository_id}/items"
    params = {
        "path": path,
        "versionDescriptor.version": version,
        "versionDescriptor.versionType": version_type.value,
        "includeContent": str(include_content).lower(),
    }

    body = await AZDO_REST_CLIENT.make_get_request(endpoint, params)
    retrieved_item = GitItem.model_validate(body)

    return retrieved_item


# Left PR context and status in the code but commented out for now. A future extension would almost certainly need them!
@AZDO_MCP.tool
async def create_pull_request_thread(
    repository_id: str,
    pull_request_id: int,
    comments: list[Comment],
    thread_context: CommentThreadContext | None = None,
    # pull_request_thread_context: GitPullRequestCommentThreadContext | None = None
    # status: CommentThreadStatus | None = None,
) -> GitPullRequestCommentThread:
    """
    Create a new comment thread on a pull request.

    Args:
        repository_id: The ID of the repository containing the pull request
        pull_request_id: The ID of the pull request to comment on
        comments: List of Comment objects to add to the thread. Each comment must have 'content' field.
             Optional fields: 'parent_comment_id', 'comment_type'
        # status: Optional status for the thread (active, fixed, wontFix, closed, byDesign, pending)
        thread_context: Optional context specifying file path and position for the comment. When creating a comment for a
        specific file, this argument becomes mandatory.
                   Relevant Fields: filePath, leftFileStart, leftFileEnd, rightFileStart, rightFileEnd
        # pull_request_thread_context: Optional iteration context for the pull request.
                   Relevant Fields: changeTrackingId, iterationContext, trackingCriteria

    Returns:
        GitPullRequestCommentThread: Created comment thread with populated fields including:
        - id: Thread identifier
        - publishedDate, lastUpdatedDate: Timestamp information
        - comments: List of comments in the thread
        # - status: Thread status
        - threadContext: File location context (if applicable)
        - pullRequestThreadContext: Iteration context (if applicable)

    Raises:
        HTTPException: If the Azure DevOps API POST request fails
    """
    endpoint = f"git/repositories/{repository_id}/pullrequests/{pull_request_id}/threads"

    request_body = {
        "comments": [comment.model_dump(by_alias=True, exclude_none=True) for comment in comments],
        "status": CommentThreadStatus.ACTIVE.value,
    }

    # if status is not None:
    #     request_body["status"] = status.value

    if thread_context is not None:
        request_body["threadContext"] = thread_context.model_dump(by_alias=True, exclude_none=True)

    # if pull_request_thread_context is not None:
    #     request_body["pullRequestThreadContext"] = pull_request_thread_context.model_dump(by_alias=True, exclude_none=True)

    body = await AZDO_REST_CLIENT.make_post_request(endpoint, request_body)
    return GitPullRequestCommentThread.model_validate(body)


azure_devops_mcp_app = AZDO_MCP.http_app(path="/azure-devops")
