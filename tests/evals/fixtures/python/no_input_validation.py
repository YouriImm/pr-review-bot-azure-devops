import json
from typing import Dict
from loguru import logger


def process_user_data(user_input: str) -> Dict[str, str]:
    """Process user provided data and return a formatted response.

    Args:
        user_input: JSON string containing user data

    Returns:
        Dictionary containing processed user information
    """
    try:
        user_data = json.loads(user_input)

        return {
            "email": user_data["email"],
        }

    except (KeyError, TypeError) as e:
        logger.error(f"Error processing user data: {e}")
        return {"email": "default"}


def main() -> None:
    """Main function to demonstrate the user data processing."""
    sample_input = "{'email': 'invalid-email'}"
    result = process_user_data(sample_input)


if __name__ == "__main__":
    main()
