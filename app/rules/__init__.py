import json
from pathlib import Path

from app.models.review_models import ReviewRuleLanguage, ReviewRule


async def get_review_rules(language: ReviewRuleLanguage) -> list[ReviewRule]:
    """
    Get code review rules for a specific language.

    Args:
        language: Programming language (e.g., "python", "sql", "javascript")

    Returns:
        list[ReviewRule]: Review rules for the specified language

    Raises:
        ValueError: Raised when the file with rules for that language can't be loaded or doesn't exist
    """
    language_str = language.value.lower()

    rules_file = Path(__file__).parent.joinpath(f"{language_str}_rules.json")

    if not rules_file.exists():
        raise ValueError(f"No review rules found for language: {language_str}")

    try:
        with open(rules_file, "r", encoding="utf-8") as f:
            rules_data = json.load(f)
            return [ReviewRule.model_validate(rule) for rule in rules_data]
    except Exception as e:
        raise ValueError(f"Error loading rules for {language_str}: {str(e)}")
