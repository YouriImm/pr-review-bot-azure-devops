from dataclasses import dataclass

from pydantic_evals.evaluators import Evaluator, EvaluatorContext

from app.models.review_models import ReviewOutcomeItem


@dataclass
class ReviewRulePresenceEvaluator(Evaluator):
    rule_id: str

    def evaluate(self, ctx: EvaluatorContext) -> bool:
        output: list[ReviewOutcomeItem] = ctx.output

        for review_outcome in output:
            if self.rule_id.lower() in review_outcome.review_comment.rule_id.lower():
                return True
        return False
