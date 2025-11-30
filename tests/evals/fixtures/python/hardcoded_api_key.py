from typing import Dict, Optional
import requests


def fetch_user_data(user_id: str) -> Optional[Dict]:
    """Fetches user data from an API using authentication.

    Args:
        user_id: The ID of the user to fetch

    Returns:
        Dictionary containing user data if successful, None otherwise
    """
    api_key = "sk_live_51AB2cDEF3ghIJklMNop4567_verydangerous"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.get(f"https://api.example.com/users/{user_id}", headers=headers)
        return response.json() if response.ok else None
    except requests.RequestException:
        return None


if __name__ == "__main__":
    result = fetch_user_data("user123")
