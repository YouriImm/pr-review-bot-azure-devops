## How to use

This bot should be deployed as a docker container on whatever VM capability that you see fit.

You can run the solution locally as well, though you'd need to simulate the webhook as Azure DevOps obviously can
not reach localhost.

### Prerequisites
- [UV](https://docs.astral.sh/uv/);
- [Docker](https://www.docker.com/get-started/);
- A [Logfire](https://pydantic.dev/logfire) account and access token. Not to worry, logfire has a very generous free tier.
- [Azure DevOps](https://azure.microsoft.com/en-us/products/devops/?nav=min), for obvious reasons.

<br>

### Local Setup
To set up the app locally:
- Clone the repository
- Run `make install`, or run `uv sync` followed by `uv run pre-commit install`
- Set up the environment variables that `app/auth.py` requires, either via a `.env` file or via environment variables.
- Run `uv run fastapi dev`

When running on `localhost` we can not react to live webhook events, but we can still test and use the app. To do
this:
- Create a pull request like normal. Copy the pull request ID.
- Make a POST call to API endpoint `/webhooks/register` with a simple body structured like like `{"client_name":
"<string>"}`. Copy the token you receive.
- Consider a GET call to `/webhooks/validate` with `Authorization: Bearer <token>` in your headers if you want to
  check the status of your token.
- Make a POST call to API endpoint `/pull-requests/<PR ID>/created`. Add `Authorization: Bearer <token>` to your
  headers. No body is needed.

This calls the same API route which the webhooks API would use in a real deployment and triggers the coordinator
agent like normal. You'll get all the core features of the system, so comments will be posted to your PR and the
observability dashboards will be populated automatically.

---
<br>

### Live Deployment
I set up my infrastructure according to the [architecture](architecture.md) documentation. If you've done the same you
can use the CI/CD pipeline in Azure DevOps from this repo, or you can just use the dockerfile and CLI commands directly.

Assuming a deployed app:
- Make a POST call to API endpoint `/webhooks/register` with a simple body structured like `{"client_name":
"<string>"}`. Copy the token you receive.
- Consider a GET call to `/webhooks/validate` with `Authorization: Bearer <token>` in your headers if you want to
  check the status of your token.
- Go to Azure DevOps and set up webhooks following the [instructions in the official docs](https://learn.microsoft.com/en-us/azure/devops/service-hooks/services/webhooks?view=azure-devops).
  - Set the event trigger type to `Pull request created`.
  - Set the filters as you see fit.
  - Set the URL and HTTP headers. The URL is your base URL with suffix `/webhooks/pull-request/created`, and the headers are
    `Authorization: Bearer <token>`.
    - Observe how azure devops offers **zero** security here: the auth token is a plain string and remains open for
      all to see, copy, and edit. No way around this, but at least we mitigate by strict API input
      validation on the webhooks API combined with per-token rate limiting.

When webhooks are set up, the system will respond to any created pull request that matches the filters you set up
for your webhook.
