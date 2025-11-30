from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict

from .base_models import IdentityRef, ReferenceLinks
from .enums import CommentType, CommentThreadStatus


class CommentPosition(BaseModel):
    """Comment position within a file.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-request-threads/create?view=azure-devops-rest-7.1&tabs=HTTP#commentposition
    """

    line: int = Field(ge=1, description="The line number of a thread's position. Starts at 1.")
    offset: int = Field(
        ge=1,
        description="Position of first character of the thread's span in file. The line number of a thread's position. The character offset of a thread's position inside of a line. Starts at 1. Must only be set if <left/right>StartLine is also specified for that file. ",
    )

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True, extra="forbid")


class CommentThreadContext(BaseModel):
    """Context for where the comment thread is positioned within a file.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-request-threads/create?view=azure-devops-rest-7.1&tabs=HTTP#commentthreadcontext
    """

    file_path: str = Field(
        alias="filePath",
        pattern=r"^/.*",
        description="File path relative to the root of the repository. Must start with a slash.",
    )
    left_file_end: Optional[CommentPosition] = Field(
        None,
        alias="leftFileEnd",
        description="Position of last character of the thread's span in left file. The line number of a thread's position. Must only be set if leftFileStart is also specified.",
    )
    left_file_start: Optional[CommentPosition] = Field(
        None,
        alias="leftFileStart",
        description="Position of first character of the thread's span in left file. The line number of a thread's position.",
    )
    right_file_end: Optional[CommentPosition] = Field(
        None,
        alias="rightFileEnd",
        description="Position of last character of the thread's span in right file. The line number of a thread's position. Must only be set if rightFileStart is also specified.",
    )
    right_file_start: Optional[CommentPosition] = Field(
        None,
        alias="rightFileStart",
        description="Position of first character of the thread's span in right file. The line number of a thread's position.",
    )

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True, extra="forbid")


class CommentIterationContext(BaseModel):
    """Iteration context for pull request comments.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-request-threads/create?view=azure-devops-rest-7.1&tabs=HTTP#commentiterationcontext
    """

    first_comparing_iteration: Optional[int] = Field(
        None,
        alias="firstComparingIteration",
        description="The iteration of the file on the left side of the diff when the thread was created.",
    )
    second_comparing_iteration: Optional[int] = Field(
        None,
        alias="secondComparingIteration",
        description="The iteration of the file on the right side of the diff when the thread was created.",
    )

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True, extra="forbid")


class CommentTrackingCriteria(BaseModel):
    """Tracking criteria for comments.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-request-threads/create?view=azure-devops-rest-7.1&tabs=HTTP#commenttrackingcriteria
    """

    first_comparing_iteration: Optional[int] = Field(
        None,
        alias="firstComparingIteration",
        description="The iteration of the file on the left side of the diff that the thread will be tracked to.",
    )
    orig_file_path: Optional[str] = Field(
        None, alias="origFilePath", description="Original filepath the thread was created on before tracking."
    )
    orig_left_file_end: Optional[CommentPosition] = Field(
        None,
        alias="origLeftFileEnd",
        description="Original position of last character of the thread's span in left file.",
    )
    orig_left_file_start: Optional[CommentPosition] = Field(
        None,
        alias="origLeftFileStart",
        description="Original position of first character of the thread's span in left file.",
    )
    orig_right_file_end: Optional[CommentPosition] = Field(
        None,
        alias="origRightFileEnd",
        description="Original position of last character of the thread's span in right file.",
    )
    orig_right_file_start: Optional[CommentPosition] = Field(
        None,
        alias="origRightFileStart",
        description="Original position of first character of the thread's span in right file.",
    )
    second_comparing_iteration: Optional[int] = Field(
        None,
        alias="secondComparingIteration",
        description="The iteration of the file on the right side of the diff that the thread will be tracked to.",
    )

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True, extra="forbid")


class GitPullRequestCommentThreadContext(BaseModel):
    """Pull request comment thread context.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-request-threads/create?view=azure-devops-rest-7.1&tabs=HTTP#gitpullrequestcommentthreadcontext
    """

    change_tracking_id: Optional[int] = Field(
        None, alias="changeTrackingId", description="Used to track a comment across iterations."
    )
    iteration_context: Optional[CommentIterationContext] = Field(
        None, alias="iterationContext", description="The iteration context being viewed when the thread was created."
    )
    tracking_criteria: Optional[CommentTrackingCriteria] = Field(
        None, alias="trackingCriteria", description="The criteria used to track this thread."
    )

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True, extra="forbid")


class Comment(BaseModel):
    """Comment model for pull request threads.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-request-threads/create?view=azure-devops-rest-7.1&tabs=HTTP#comment
    """

    # Required field for creation
    content: str = Field(description="The comment content.")

    # Optional fields for creation
    comment_type: Optional[CommentType] = Field(
        None, alias="commentType", description="The comment type at the time of creation."
    )
    parent_comment_id: Optional[int] = Field(
        None,
        alias="parentCommentId",
        description="The ID of the parent comment. Do not use this unless you are replying to an existing comment.",
    )

    # Response-only fields (will be populated by Azure DevOps)
    id: Optional[int] = Field(None, description="The ID of the comment.")
    author: Optional[IdentityRef] = Field(None, description="The author of the comment.")
    published_date: Optional[datetime] = Field(
        None, alias="publishedDate", description="The date the comment was first published."
    )
    last_updated_date: Optional[datetime] = Field(
        None, alias="lastUpdatedDate", description="The date the comment was last updated."
    )
    last_content_updated_date: Optional[datetime] = Field(
        None, alias="lastContentUpdatedDate", description="The date the comment's content was last updated."
    )
    is_deleted: Optional[bool] = Field(
        None, alias="isDeleted", description="Whether or not this comment was soft-deleted."
    )
    users_liked: Optional[List[IdentityRef]] = Field(
        None, alias="usersLiked", description="A list of the users who have liked this comment."
    )
    links: Optional[ReferenceLinks] = Field(None, alias="_links", description="Links to other related objects.")

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True, extra="forbid")


class GitPullRequestCommentThread(BaseModel):
    """Pull request comment thread response model.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-request-threads/create?view=azure-devops-rest-7.1&tabs=HTTP#gitpullrequestcommentthread
    """

    # Response fields populated by Azure DevOps
    id: Optional[int] = Field(None, description="The comment thread id.")
    published_date: Optional[datetime] = Field(
        None, alias="publishedDate", description="The time this thread was published."
    )
    last_updated_date: Optional[datetime] = Field(
        None, alias="lastUpdatedDate", description="The time this thread was last updated."
    )
    comments: Optional[List[Comment]] = Field(None, description="A list of the comments.")
    status: Optional[CommentThreadStatus] = Field(None, description="The status of the comment thread.")
    thread_context: Optional[CommentThreadContext] = Field(
        None, alias="threadContext", description="Specify thread context such as position in left/right file."
    )
    pull_request_thread_context: Optional[GitPullRequestCommentThreadContext] = Field(
        None, alias="pullRequestThreadContext", description="Extended context information unique to pull requests"
    )
    is_deleted: Optional[bool] = Field(
        None,
        alias="isDeleted",
        description="Specify if the thread is deleted which happens when all comments are deleted.",
    )
    identities: Optional[Dict[str, Any]] = Field(None, description="Set of identities related to this thread")
    properties: Optional[Dict[str, Any]] = Field(
        None, description="Optional properties associated with the thread as a collection of key-value pairs."
    )
    links: Optional[ReferenceLinks] = Field(None, alias="_links", description="Links to other related objects.")

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )
