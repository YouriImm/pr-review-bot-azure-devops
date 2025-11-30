from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .enums import ProjectState, ProjectVisibility


class ReferenceLinks(BaseModel):
    """The class to represent a collection of REST reference links.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#referencelinks
    """

    links: Optional[Dict[str, Any]] = Field(default=None, description="The set of links relevant to the REST resource.")


class IdentityRef(BaseModel):
    """Identity reference model.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#identityref
    """

    id: str = Field(description="The identifier of the identity.")
    display_name: Optional[str] = Field(
        default=None, alias="displayName", description="The non-unique display name of the identity."
    )
    unique_name: Optional[str] = Field(
        default=None, alias="uniqueName", description="DEPRECATED - The unique name of the identity."
    )
    url: Optional[str] = Field(default=None, description="The URL to retrieve information about this identity.")
    image_url: Optional[str] = Field(
        default=None, alias="imageUrl", description="DEPRECATED - The URL of the image associated with this identity."
    )
    descriptor: Optional[str] = Field(
        default=None, description="The field that uniquely identifies this identity across accounts and organizations."
    )
    directory_alias: Optional[str] = Field(
        default=None, alias="directoryAlias", description="DEPRECATED - The Active Directory alias of the identity."
    )
    inactive: Optional[bool] = Field(
        default=None, description="DEPRECATED - True if the identity is inactive; otherwise, false."
    )
    is_aad_identity: Optional[bool] = Field(
        default=None,
        alias="isAadIdentity",
        description="DEPRECATED -True if the identity is an Azure Active Directory identity; otherwise, false.",
    )
    is_container: Optional[bool] = Field(
        default=None,
        alias="isContainer",
        description="DEPRECATED - True if the identity is a container (such as a group); otherwise, false.",
    )
    is_deleted_in_origin: Optional[bool] = Field(
        default=None,
        alias="isDeletedInOrigin",
        description="True if the identity has been deleted in the origin provider; otherwise, false.",
    )
    profile_url: Optional[str] = Field(
        default=None, alias="profileUrl", description="DEPRECATED - The URL to the profile of the identity."
    )
    links: Optional[ReferenceLinks] = Field(
        default=None, alias="_links", description="Interesting links about the graph subject."
    )


class IdentityRefWithVote(IdentityRef):
    """Identity information including a vote on a pull request.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#identityrefwithvote
    """

    vote: Optional[int] = Field(
        default=None,
        description="Vote on a pull request: 10 - approved, 5 - approved with suggestions, 0 - no vote, -5 - waiting for author, -10 - rejected.",
    )
    has_declined: Optional[bool] = Field(
        default=None,
        alias="hasDeclined",
        description="Indicates if the reviewer has declined to review the pull request.",
    )
    is_flagged: Optional[bool] = Field(
        default=None, alias="isFlagged", description="Indicates if this is a flagged reviewer."
    )
    is_reapprove: Optional[bool] = Field(
        default=None, alias="isReapprove", description="Indicates if the reviewer is flagged for reapproval."
    )
    is_required: Optional[bool] = Field(
        default=None,
        alias="isRequired",
        description="Indicates if the reviewer is required for the pull request to be completed.",
    )
    reviewer_url: Optional[str] = Field(
        default=None, alias="reviewerUrl", description="URL to retrieve information about this reviewer."
    )
    voted_for: Optional[List[IdentityRef]] = Field(
        default=None, alias="votedFor", description="List of other reviewers that this reviewer voted for."
    )


class TeamProjectReference(BaseModel):
    """Represents a shallow reference to a TeamProject.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#teamprojectreference
    """

    id: UUID = Field(description="The project's unique identifier.")
    name: str = Field(description="The name of the project.")
    description: Optional[str] = Field(default=None, description="The description of the project.")
    url: str = Field(description="The full http URL to the project.")
    state: Optional[ProjectState] = Field(default=None, description="Indicates the current state of the project.")
    revision: Optional[int] = Field(default=None, description="The last update revision of the project.")
    visibility: Optional[ProjectVisibility] = Field(
        default=None, description="Indicates the visibility of the project."
    )
    last_update_time: Optional[datetime] = Field(
        default=None, alias="lastUpdateTime", description="The last time the project was updated."
    )
    abbreviation: Optional[str] = Field(default=None, description="The abbreviation of the project.")
    default_team_image_url: Optional[str] = Field(
        default=None, alias="defaultTeamImageUrl", description="The default team image URL for the project."
    )


class TeamProjectCollectionReference(BaseModel):
    """Reference object for a TeamProjectCollection.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#teamprojectcollectionreference
    """

    id: UUID = Field(description="The collection's unique identifier.")
    name: str = Field(description="The name of the collection.")
    url: str = Field(description="The full http URL to the collection.")
    avatar_url: Optional[str] = Field(default=None, alias="avatarUrl", description="The avatar URL for the collection.")


class GitRepositoryRef(BaseModel):
    """Git repository reference.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#gitrepositoryref
    """

    id: UUID = Field(description="The repository ID.")
    name: str = Field(description="The name of the repository.")
    url: str = Field(description="The full http URL to the repository.")
    project: Optional[TeamProjectReference] = Field(default=None, description="The project containing the repository.")
    remote_url: Optional[str] = Field(default=None, alias="remoteUrl", description="The remote URL of the repository.")
    ssh_url: Optional[str] = Field(default=None, alias="sshUrl", description="The SSH URL of the repository.")
    collection: Optional[TeamProjectCollectionReference] = Field(
        default=None, description="The collection containing the repository."
    )
    is_fork: Optional[bool] = Field(
        default=None, alias="isFork", description="True if the repository is a fork; otherwise, false."
    )


class GitRepository(GitRepositoryRef):
    """Full Git repository model.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#gitrepository
    """

    default_branch: Optional[str] = Field(
        default=None, alias="defaultBranch", description="The default branch of the repository."
    )
    size: Optional[int] = Field(default=None, description="The size of the repository.")
    is_disabled: Optional[bool] = Field(
        default=None, alias="isDisabled", description="True if the repository is disabled; otherwise, false."
    )
    is_in_maintenance: Optional[bool] = Field(
        default=None,
        alias="isInMaintenance",
        description="True if the repository is in maintenance mode; otherwise, false.",
    )
    parent_repository: Optional[GitRepositoryRef] = Field(
        default=None, alias="parentRepository", description="The parent repository if this is a fork."
    )
    valid_remote_urls: Optional[List[str]] = Field(
        default=None, alias="validRemoteUrls", description="A list of valid remote URLs for the repository."
    )
    web_url: Optional[str] = Field(default=None, alias="webUrl", description="The web URL of the repository.")
    links: Optional[ReferenceLinks] = Field(
        default=None, alias="_links", description="The links to related REST resources."
    )


class ResourceRef(BaseModel):
    """Resource reference.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#resourceref
    """

    id: Optional[str] = Field(default=None, description="The ID of the resource.")
    url: Optional[str] = Field(default=None, description="The full http URL to the resource.")


class WebApiTagDefinition(BaseModel):
    """Tag definition representation.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.1&tabs=HTTP#webapittagdefinition
    """

    id: UUID = Field(description="The unique ID of the tag definition.")
    name: str = Field(description="The name of the tag definition.")
    url: str = Field(description="Resource URL for the tag definition.")
    active: Optional[bool] = Field(
        default=None, description="Indicates whether the tag is active or not. True if the tag is active."
    )


class GitRepositoryListResponse(BaseModel):
    """Response model for listing Git repositories.

    See: https://learn.microsoft.com/en-us/rest/api/azure/devops/git/repositories/list?view=azure-devops-rest-7.1&tabs=HTTP
    """

    count: int = Field(description="The number of repositories returned.")
    value: List[GitRepository] = Field(description="The full list of repositories returned.")
