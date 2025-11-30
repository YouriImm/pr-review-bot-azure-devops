The JSON files in this folder define code review rules. The system expects one JSON file per language sub-agent.

You can have as many rules as you like, but it's worth considering the tradeoff of potential rule coverage vs impact on
agent runtime, spend and performance.

The rule structure is fixed, but you can take liberties within certain fields:

| Field               | Description                                                                                                                        |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `id`                | Unique identifier for the rule. Used in review comments and in the evals setup.                                                    |
| `title`             | Short, descriptive name of the rule. Will be used in review comments.                                                              |
| `description`       | Detailed explanation of the rule’s intent and requirements.                                                                        |
| `severity`          | How bad do we consider a violation of this rule to be? Allowed values are `warning`, `error`, `critical`.                          |
| `code_smells`       | List of patterns that indicate a violation. Helps the agent identify violations.                                                   |                                                              |
| `rule_instructions` | Instructions for the agent on how to treat the rule, for example to not be too harsh or to only raise a violation once per script. |
