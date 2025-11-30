from enum import Enum


class ProjectState(str, Enum):
    DELETING = "deleting"
    NEW = "new"
    WELL_FORMED = "wellFormed"
    CREATE_PENDING = "createPending"
    ALL = "all"
    UNCHANGED = "unchanged"
    DELETED = "deleted"


class ProjectVisibility(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    UNCHANGED = "unchanged"


class PullRequestStatus(str, Enum):
    NOT_SET = "notSet"
    ACTIVE = "active"
    ABANDONED = "abandoned"
    COMPLETED = "completed"
    ALL = "all"


class PullRequestAsyncStatus(str, Enum):
    NOT_SET = "notSet"
    QUEUED = "queued"
    CONFLICTS = "conflicts"
    SUCCEEDED = "succeeded"
    REJECTED_BY_POLICY = "rejectedByPolicy"
    FAILURE = "failure"


class PullRequestMergeFailureType(str, Enum):
    NONE = "none"
    UNKNOWN = "unknown"
    CASE_SENSITIVE = "caseSensitive"
    OBJECT_TOO_LARGE = "objectTooLarge"


class GitPullRequestMergeStrategy(str, Enum):
    NO_FAST_FORWARD = "noFastForward"
    SQUASH = "squash"
    REBASE = "rebase"
    REBASE_MERGE = "rebaseMerge"


class GitStatusState(str, Enum):
    NOT_SET = "notSet"
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ERROR = "error"
    NOT_APPLICABLE = "notApplicable"


class VersionControlChangeType(str, Enum):
    NONE = "none"
    ADD = "add"
    EDIT = "edit"
    ENCODING = "encoding"
    RENAME = "rename"
    DELETE = "delete"
    UNDELETE = "undelete"
    BRANCH = "branch"
    MERGE = "merge"
    LOCK = "lock"
    ROLLBACK = "rollback"
    SOURCE_RENAME = "sourceRename"
    TARGET_RENAME = "targetRename"
    PROPERTY = "property"
    ALL = "all"


class ItemContentType(str, Enum):
    RAW_TEXT = "rawText"
    BASE64_ENCODED = "base64Encoded"


class GitVersionType(str, Enum):
    BRANCH = "branch"
    TAG = "tag"
    COMMIT = "commit"


class CommentThreadStatus(str, Enum):
    UNKNOWN = "unknown"
    ACTIVE = "active"
    FIXED = "fixed"
    WONT_FIX = "wontFix"
    CLOSED = "closed"
    BY_DESIGN = "byDesign"
    PENDING = "pending"


class CommentType(str, Enum):
    UNKNOWN = "unknown"
    TEXT = "text"
    CODE_CHANGE = "codeChange"
    SYSTEM = "system"
