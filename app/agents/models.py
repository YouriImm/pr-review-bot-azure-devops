"""
Of course this would need to be different in a long term scenario, but for now it works

We can slot in any model that https://ai.pydantic.dev/models/overview/ supports.
For decisions like this I quite appreciate https://llm-stats.com/.

The coordinator agent can get away with using a 'weaker' model than the sub-agents.
Of course if we want models from different providers we'd change AGENT_API_KEY to a duo of variables instead.
"""

from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider

from app.auth import get_azure_devops_settings

# If I'd want gemini, I could do something like:
# provider = GoogleProvider(api_key=get_azure_devops_settings().AGENT_API_KEY)
# coordinator_agent_model = GoogleModel("gemini-2.0-flash", provider=provider)
# sub_agent_model = GoogleModel("gemini-2.5-flash", provider=provider)

coordinator_agent_model = AnthropicModel(
    "claude-haiku-4-5", provider=AnthropicProvider(api_key=get_azure_devops_settings().AGENT_API_KEY)
)
sub_agent_model = AnthropicModel(
    "claude-sonnet-4-5", provider=AnthropicProvider(api_key=get_azure_devops_settings().AGENT_API_KEY)
)
