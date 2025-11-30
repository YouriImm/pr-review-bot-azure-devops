from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ReviewRuleLanguage(str, Enum):
    PYTHON = "python"
    SQL = "sql"
    MD = "markdown"


class ReviewRuleSeverity(str, Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    GENERIC = "generic"
    DECLINED = "declined"


class ReviewRule(BaseModel):
    # TODO: Consider adding categories. Useful when the number of rules grows.
    # TODO: Consider forced regex pattern matching for the id field on i.e. "SEC001" or "PERF002".
    id: str = Field(description="Unique identifier for this rule")
    title: str = Field(description="Title of the rule. Relevant for display purposes")
    description: str = Field(description="Description of the rule and its behavior")
    severity: ReviewRuleSeverity = Field(description="Relative importance of the rule. Critical > Error > Warning")
    code_smells: List[str] = Field(description="List of code smells to help recognize violations of this rule.")
    rule_instructions: Optional[str] = Field(
        default=None, description="Instructions that must be followed when evaluationg this rule."
    )


class ReviewComment(BaseModel):
    rule_level: ReviewRuleSeverity = Field(alias="ruleLevel", description="The severity level of the rule violation")
    rule_title: Optional[str] = Field(default=None, alias="ruleTitle", max_length=200, description="Title of the rule")
    rule_id: Optional[str] = Field(
        default=None,
        alias="ruleId",
        pattern=r"^[A-Z]{2,3}\d{3}$",
        description="Rule identifier in format XX### or XXX###",
    )
    problem_description: str = Field(
        alias="problemDescription", max_length=400, description="What is wrong with the code"
    )
    expected_fix: Optional[str] = Field(
        default=None, alias="expectedFix", max_length=400, description="What type of fix is expected"
    )


class ReviewOutcomeItem(BaseModel):
    file_path: Optional[str] = Field(alias="filePath", description="File path relative to the root of the repository.")
    start_line: Optional[int] = Field(ge=1, alias="startLine", description="Start line number of the violation.")
    start_offset: Optional[int] = Field(ge=1, alias="startOffset", description="Start offset of the violation.")
    end_line: Optional[int] = Field(ge=1, alias="endLine", description="End line number of the violation.")
    end_offset: Optional[int] = Field(ge=1, alias="endOffset", description="End offset of the violation.")
    review_comment: Optional[ReviewComment] = Field(default=None, alias="reviewComment", description="Review comment.")


class ReviewRequest(BaseModel):
    file_path: str = Field(alias="filePath", description="File path relative to the root of the repository.")
    file_content: str = Field(alias="fileContent", description="File content to be reviewed.")


class ReviewInput(BaseModel):
    review_rules: list[ReviewRule] = Field(
        alias="reviewRules", description="List of review rules to apply to the file_content"
    )
    file_path: str = Field(alias="filePath", description="File path relative to the root of the repository.")
    file_content: str = Field(alias="fileContent", description="File content to be reviewed.")
