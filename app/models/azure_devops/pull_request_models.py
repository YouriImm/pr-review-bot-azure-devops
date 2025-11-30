from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from .base_models import (
    IdentityRef,
    IdentityRefWithVote,
    GitRepository,
    ReferenceLinks,
    ResourceRef,
    WebApiTagDefinition,
)
from .enums import PullRequestStatus, PullRequestAsyncStatus, PullRequestMergeFailureType, GitPullRequestMergeStrategy
from .git_models import GitCommitRef, GitForkRef


class GitPullRequestMergeOptions(BaseModel):
    """Options for pull request merge."""

    conflict_authorship_commits: Optional[bool] = Field(
        default=None,
        alias="conflictAuthorshipCommits",
        description="If true, conflict resolutions applied during the merge will be put in separate commits to preserve authorship info for git blame.",
    )
    detect_rename_false_positives: Optional[bool] = Field(
        default=None,
        alias="detectRenameFalsePositives",
        description="If true, ambiguous rename mappings will be treated as false positives and ignored during merge.",
    )
    disable_renames: Optional[bool] = Field(
        default=None,
        alias="disableRenames",
        description="If true, rename detection will not be performed during the merge.",
    )


class GitPullRequestCompletionOptions(BaseModel):
    """Preferences about how the pull request should be completed."""

    auto_complete_ignore_config_ids: Optional[List[int]] = Field(
        default=None,
        alias="autoCompleteIgnoreConfigIds",
        description="List of policy configuration IDs that auto-complete should not wait for. Applies only to optional policies.",
    )
    bypass_policy: Optional[bool] = Field(
        default=None,
        alias="bypassPolicy",
        description="If true, policies will be explicitly bypassed when completing the pull request.",
    )
    bypass_reason: Optional[str] = Field(
        default=None, alias="bypassReason", description="Reason provided when policies are bypassed during completion."
    )
    delete_source_branch: Optional[bool] = Field(
        default=None,
        alias="deleteSourceBranch",
        description="If true, the source branch will be deleted after the pull request is completed.",
    )
    merge_commit_message: Optional[str] = Field(
        default=None, alias="mergeCommitMessage", description="Custom commit message used for the merge commit."
    )
    merge_strategy: Optional[GitPullRequestMergeStrategy] = Field(
        default=None,
        alias="mergeStrategy",
        description="Specifies the strategy used to merge the pull request during completion.",
    )
    squash_merge: Optional[bool] = Field(
        default=None,
        alias="squashMerge",
        description="Deprecated. If true, commits will be squash-merged. Use mergeStrategy instead.",
    )
    transition_work_items: Optional[bool] = Field(
        default=None,
        alias="transitionWorkItems",
        description="If true, linked work items will be transitioned to the next logical state upon completion.",
    )
    triggered_by_auto_complete: Optional[bool] = Field(
        default=None,
        alias="triggeredByAutoComplete",
        description="Indicates if the current completion attempt was triggered via auto-complete.",
    )


class GitPullRequest(BaseModel):
    """Represents all the data associated with a pull request."""

    pull_request_id: int = Field(alias="pullRequestId", description="Unique ID of the pull request.")
    repository: GitRepository = Field(description="Repository associated with the pull request.")
    source_ref_name: str = Field(alias="sourceRefName", description="Source branch of the pull request.")
    target_ref_name: str = Field(alias="targetRefName", description="Target branch of the pull request.")
    status: PullRequestStatus = Field(description="Current status of the pull request.")
    created_by: IdentityRef = Field(alias="createdBy", description="Identity that created the pull request.")
    creation_date: datetime = Field(alias="creationDate", description="Date the pull request was created.")
    title: str = Field(description="Title of the pull request.")

    artifact_id: Optional[str] = Field(
        default=None, alias="artifactId", description="Artifact associated with the pull request."
    )
    auto_complete_set_by: Optional[IdentityRef] = Field(
        default=None, alias="autoCompleteSetBy", description="Identity that set the pull request to auto-complete."
    )
    closed_by: Optional[IdentityRef] = Field(
        default=None, alias="closedBy", description="Identity that closed the pull request."
    )
    closed_date: Optional[datetime] = Field(
        default=None, alias="closedDate", description="Date the pull request was closed."
    )
    code_review_id: Optional[int] = Field(
        default=None, alias="codeReviewId", description="Code review ID associated with the pull request."
    )
    commits: Optional[List[GitCommitRef]] = Field(
        default=None, description="List of commits associated with the pull request."
    )
    completion_options: Optional[GitPullRequestCompletionOptions] = Field(
        default=None, alias="completionOptions", description="Options for completing the pull request."
    )
    completion_queue_time: Optional[datetime] = Field(
        default=None, alias="completionQueueTime", description="Time the pull request was queued for completion."
    )
    description: Optional[str] = Field(default=None, description="Description of the pull request.")
    fork_source: Optional[GitForkRef] = Field(
        default=None, alias="forkSource", description="Source repository if the pull request is from a fork."
    )
    has_multiple_merge_bases: Optional[bool] = Field(
        default=None, alias="hasMultipleMergeBases", description="True if the pull request has multiple merge bases."
    )
    is_draft: Optional[bool] = Field(default=None, alias="isDraft", description="True if the pull request is a draft.")
    labels: Optional[List[WebApiTagDefinition]] = Field(
        default=None, description="List of labels associated with the pull request."
    )
    last_merge_commit: Optional[GitCommitRef] = Field(
        default=None, alias="lastMergeCommit", description="Last merge commit created during pull request completion."
    )
    last_merge_source_commit: Optional[GitCommitRef] = Field(
        default=None, alias="lastMergeSourceCommit", description="Last source commit used in the merge."
    )
    last_merge_target_commit: Optional[GitCommitRef] = Field(
        default=None, alias="lastMergeTargetCommit", description="Last target commit used in the merge."
    )
    merge_failure_message: Optional[str] = Field(
        default=None, alias="mergeFailureMessage", description="Message describing the reason for merge failure."
    )
    merge_failure_type: Optional[PullRequestMergeFailureType] = Field(
        default=None, alias="mergeFailureType", description="Type of failure encountered during merge."
    )
    merge_id: Optional[UUID] = Field(
        default=None, alias="mergeId", description="ID used to identify the merge operation."
    )
    merge_options: Optional[GitPullRequestMergeOptions] = Field(
        default=None, alias="mergeOptions", description="Options used during merge."
    )
    merge_status: Optional[PullRequestAsyncStatus] = Field(
        default=None, alias="mergeStatus", description="Status of the asynchronous merge operation."
    )
    remote_url: Optional[str] = Field(default=None, alias="remoteUrl", description="Remote URL of the pull request.")
    reviewers: Optional[List[IdentityRefWithVote]] = Field(
        default=None, description="List of reviewers for the pull request."
    )
    supports_iterations: Optional[bool] = Field(
        default=None, alias="supportsIterations", description="True if the pull request supports iterations."
    )
    url: Optional[str] = Field(default=None, description="URL to retrieve information about the pull request.")
    work_item_refs: Optional[List[ResourceRef]] = Field(
        default=None, alias="workItemRefs", description="List of work items linked to the pull request."
    )
    links: Optional[ReferenceLinks] = Field(
        default=None, alias="_links", description="Links to related REST resources."
    )

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )


class AzureDevOpsWebhookEvent(BaseModel):
    """Azure DevOps webhook event for pull request operations."""

    subscription_id: UUID = Field(alias="subscriptionId", description="ID of the webhook subscription.")
    notification_id: int = Field(alias="notificationId", description="ID of the notification event.")
    id: UUID = Field(description="Unique ID of the webhook event.")
    event_type: str = Field(alias="eventType", description="Type of event that triggered the webhook.")
    publisher_id: str = Field(alias="publisherId", description="ID of the publisher that generated the event.")
    message: dict = Field(description="Brief message describing the event.")
    detailed_message: dict = Field(alias="detailedMessage", description="Detailed message describing the event.")
    resource: GitPullRequest = Field(description="Pull request resource associated with the event.")
    resource_version: str = Field(alias="resourceVersion", description="Version of the pull request resource.")
    resource_containers: dict = Field(alias="resourceContainers", description="Containers that scope the resource.")
    created_date: datetime = Field(alias="createdDate", description="Date the event was created.")

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )
