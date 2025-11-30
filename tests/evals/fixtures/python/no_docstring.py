from typing import List
from loguru import logger


def calculate_average(numbers: List[float]) -> float:
    if not numbers:
        logger.warning("Empty list provided")
        return 0.0
    return sum(numbers) / len(numbers)
