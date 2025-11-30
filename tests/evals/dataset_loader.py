from pathlib import Path
from typing import Any

from pydantic_evals import Dataset

from app.models.review_models import ReviewOutcomeItem
from tests.evals.evaluators import ReviewRulePresenceEvaluator


def load_dataset_from_yaml(yaml_path: Path) -> Dataset[dict, list[ReviewOutcomeItem], Any]:
    base_dir = Path(__file__).parent
    dataset = Dataset[dict, list[ReviewOutcomeItem], Any].from_file(
        base_dir.joinpath(yaml_path), custom_evaluator_types=[ReviewRulePresenceEvaluator]
    )

    for case in dataset.cases:
        if "file_content_path" in case.inputs:
            code_file = base_dir.joinpath(case.inputs["file_content_path"])
            with open(code_file, "r") as f:
                case.inputs["file_content"] = f.read()
            case.inputs.pop("file_content_path")  # Don't want this polluting the actual dataset!

    return dataset
