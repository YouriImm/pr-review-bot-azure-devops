from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict

from .base_models import IdentityRef, ReferenceLinks, ResourceRef, GitRepositoryRef
from .enums import GitStatusState, VersionControlChangeType, ItemContentType


class GitUserDate(BaseModel):
    """User info and date for Git operations.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#gituserdate
    """

    name: str = Field(description="The name of the user.")
    email: str = Field(description="The email of the user.")
    date: datetime = Field(description="The date associated with the user information.")
    image_url: Optional[str] = Field(default=None, alias="imageUrl", description="URL for the user's avatar image.")


class GitPushRef(BaseModel):
    """Git push reference.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#gitpushref
    """

    push_id: int = Field(alias="pushId", description="Unique ID of the push.")
    date: datetime = Field(description="Date of the push.")
    pushed_by: Optional[IdentityRef] = Field(
        default=None, alias="pushedBy", description="Identity of the user who performed the push."
    )
    url: Optional[str] = Field(default=None, description="URL to retrieve information about this push.")
    links: Optional[ReferenceLinks] = Field(
        default=None, alias="_links", description="Links to related REST resources."
    )


class GitStatusContext(BaseModel):
    """Status context that uniquely identifies the status.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#gitstatuscontext
    """

    genre: Optional[str] = Field(default=None, description="Genre of the status.")
    name: str = Field(description="Name of the status context.")


class GitStatus(BaseModel):
    """Status metadata from services and extensions.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#gitstatus
    """

    id: Optional[int] = Field(default=None, description="ID of the status.")
    context: GitStatusContext = Field(description="Status context that uniquely identifies the status.")
    created_by: Optional[IdentityRef] = Field(
        default=None, alias="createdBy", description="Identity that created the status."
    )
    creation_date: Optional[datetime] = Field(
        default=None, alias="creationDate", description="Date the status was created."
    )
    updated_date: Optional[datetime] = Field(
        default=None, alias="updatedDate", description="Date the status was last updated."
    )
    state: GitStatusState = Field(description="State of the status.")
    description: Optional[str] = Field(default=None, description="Description of the status.")
    target_url: Optional[str] = Field(
        default=None, alias="targetUrl", description="Target URL associated with the status."
    )
    links: Optional[ReferenceLinks] = Field(
        default=None, alias="_links", description="Links to related REST resources."
    )


class ItemContent(BaseModel):
    """Item content.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#itemcontent
    """

    content: Optional[str] = Field(default=None, description="Content of the item.")
    content_type: Optional[ItemContentType] = Field(default=None, alias="contentType", description="Type of content.")


class GitTemplate(BaseModel):
    """Git template.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#gittemplate
    """

    name: str = Field(description="Name of the template.")
    type: str = Field(description="Type of the template.")


class GitChange(BaseModel):
    """Git change information.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#gitchange
    """

    change_id: Optional[int] = Field(default=None, alias="changeId", description="ID of the change.")
    change_type: Optional[VersionControlChangeType] = Field(
        default=None, alias="changeType", description="Type of change made to the item."
    )
    item: Optional[str] = Field(default=None, description="Item that was changed.")
    new_content: Optional[ItemContent] = Field(
        default=None, alias="newContent", description="Content of the item after the change."
    )
    new_content_template: Optional[GitTemplate] = Field(
        default=None, alias="newContentTemplate", description="Template used for new content."
    )
    original_path: Optional[str] = Field(default=None, alias="originalPath", description="Original path of the item.")
    source_server_item: Optional[str] = Field(
        default=None, alias="sourceServerItem", description="Path of the item on the server."
    )
    url: Optional[str] = Field(default=None, description="URL to retrieve the item.")


class GitCommitRef(BaseModel):
    """Git commit reference with metadata.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#gitcommitref
    """

    commit_id: str = Field(alias="commitId", description="SHA1 ID of the commit.")
    url: str = Field(description="URL to retrieve information about the commit.")
    author: Optional[GitUserDate] = Field(default=None, description="Author information and timestamp.")
    committer: Optional[GitUserDate] = Field(default=None, description="Committer information and timestamp.")
    comment: Optional[str] = Field(default=None, description="Comment associated with the commit.")
    comment_truncated: Optional[bool] = Field(
        default=None, alias="commentTruncated", description="True if the comment was truncated."
    )
    change_counts: Optional[Dict[str, int]] = Field(
        default=None, alias="changeCounts", description="Counts of changes by change type."
    )
    changes: Optional[List[GitChange]] = Field(default=None, description="List of changes made in the commit.")
    parents: Optional[List[str]] = Field(default=None, description="Parent commit IDs.")
    push: Optional[GitPushRef] = Field(default=None, description="Push reference associated with the commit.")
    remote_url: Optional[str] = Field(default=None, alias="remoteUrl", description="Remote URL of the repository.")
    statuses: Optional[List[GitStatus]] = Field(default=None, description="Statuses associated with the commit.")
    work_items: Optional[List[ResourceRef]] = Field(
        default=None, alias="workItems", description="Work items linked to the commit."
    )
    commit_too_many_changes: Optional[bool] = Field(
        default=None, alias="commitTooManyChanges", description="True if the commit has too many changes to list."
    )
    links: Optional[ReferenceLinks] = Field(
        default=None, alias="_links", description="Links to related REST resources."
    )


class GitForkRef(BaseModel):
    """Information about a fork ref.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#gitforkref
    """

    name: str = Field(description="Name of the ref.")
    object_id: str = Field(alias="objectId", description="ID of the Git object.")
    creator: Optional[IdentityRef] = Field(default=None, description="Identity that created the ref.")
    url: Optional[str] = Field(default=None, description="URL to retrieve information about the ref.")
    is_locked: Optional[bool] = Field(default=None, alias="isLocked", description="True if the ref is locked.")
    is_locked_by: Optional[IdentityRef] = Field(
        default=None, alias="isLockedBy", description="Identity that locked the ref."
    )
    peeled_object_id: Optional[str] = Field(
        default=None, alias="peeledObjectId", description="Peeled object ID if the ref is a tag."
    )
    repository: Optional[GitRepositoryRef] = Field(default=None, description="Repository associated with the ref.")
    statuses: Optional[List[GitStatus]] = Field(default=None, description="Statuses associated with the ref.")
    links: Optional[ReferenceLinks] = Field(
        default=None, alias="_links", description="Links to related REST resources."
    )


class GitItem(BaseModel):
    """Git item information for diffs and items API.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/diffs/get?view=azure-devops-rest-7.1&tabs=HTTP
    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/items/get?view=azure-devops-rest-7.1&tabs=HTTP
    """

    git_object_type: Optional[str] = Field(default=None, alias="gitObjectType", description="Type of Git object.")
    commit_id: Optional[str] = Field(
        default=None, alias="commitId", description="ID of the commit the item was fetched at."
    )
    path: Optional[str] = Field(default=None, description="Path of the item in the repository.")
    url: Optional[str] = Field(default=None, description="URL to retrieve the item.")
    # Additional fields for Items Get API
    object_id: Optional[str] = Field(default=None, alias="objectId", description="ID of the Git object.")
    content: Optional[str] = Field(default=None, description="Content of the item.")
    is_folder: Optional[bool] = Field(default=None, alias="isFolder", description="True if the item is a folder.")
    size: Optional[int] = Field(default=None, description="Size of the item in bytes.")


class GitChangesChange(BaseModel):
    """Git change information for diffs.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/diffs/get?view=azure-devops-rest-7.1&tabs=HTTP#gitchange
    """

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    change_id: Optional[int] = Field(default=None, alias="changeId", description="ID of the change.")
    change_type: Optional[VersionControlChangeType] = Field(
        default=None, alias="changeType", description="Type of change made to the item."
    )
    item: Optional[GitItem] = Field(default=None, description="Item that was changed.")


class GitCommitDiffs(BaseModel):
    """Git commit differences response.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/diffs/get?view=azure-devops-rest-7.1&tabs=HTTP#gitcommitdiffs
    """

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    ahead_count: int = Field(alias="aheadCount", description="Number of commits in the target ahead of the base.")
    behind_count: int = Field(alias="behindCount", description="Number of commits in the target behind the base.")
    change_counts: Dict[str, int] = Field(alias="changeCounts", description="Counts of changes by change type.")
    changes: List[GitChangesChange] = Field(description="List of changes between the specified commits.")
    common_commit: str = Field(alias="commonCommit", description="The common ancestor commit ID.")

    all_changes_included: Optional[bool] = Field(
        default=None, alias="allChangesIncluded", description="True if all changes are included in this response."
    )
    base_commit: Optional[str] = Field(default=None, alias="baseCommit", description="The base commit ID.")
    target_commit: Optional[str] = Field(default=None, alias="targetCommit", description="The target commit ID.")
