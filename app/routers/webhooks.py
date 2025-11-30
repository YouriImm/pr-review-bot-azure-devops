from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Request, HTTPException, Header, Depends, BackgroundTasks

from app.auth import get_azure_devops_settings
from app.dependencies import validate_authorization_header, limiter
from app.models.azure_devops.pull_request_models import AzureDevOpsWebhookEvent
from app.models.webhooks import ClientData, WebhookRegistrationResponse, TokenValidationResponse
from app.routers import pull_requests
from app.routers.pull_requests import review_created_pull_request

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
router.include_router(pull_requests.router, prefix="/pull-requests", tags=["pull_requests"])


@router.post("/register", response_model=WebhookRegistrationResponse)
async def register_webhook(data: ClientData, request: Request):
    """Acquire a new token to register a webhook to the app"""
    payload = {"sub": data.client_name, "iat": datetime.now(UTC), "exp": datetime.now(UTC) + timedelta(days=90)}

    secret_key = get_azure_devops_settings().JWT_SECRET_STRING
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return WebhookRegistrationResponse.model_validate(
        {"webhook_url": str(request.url), "token": token, "expires_at": payload["exp"]}
    )


@router.get("/validate", response_model=TokenValidationResponse, dependencies=[Depends(limiter)])
async def validate_token(authorization: Annotated[str, Header()]):
    """Confirm if your token is valid in terms of correctness and expiry date.
    Use Authorization: Bearer <token> as the header"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization bearer token required")
    try:
        secret_key = get_azure_devops_settings().JWT_SECRET_STRING
        print(f"secret key is {secret_key}")
        token = authorization.removeprefix("Bearer ").strip()
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return TokenValidationResponse(valid=True, expires_at=datetime.fromtimestamp(payload["exp"]), reason=None)
    except jwt.ExpiredSignatureError:
        return TokenValidationResponse(valid=False, expires_at=None, reason="Provided token was valid but is expired")
    except jwt.InvalidTokenError:
        return TokenValidationResponse(valid=False, expires_at=None, reason="Provided token was invalid")


# We don't really need the auth param functionally, this way we force its presence & validity in the route.
@router.post("/pull-request/created", dependencies=[Depends(limiter)])
async def create_pull_request(
    pr_body: AzureDevOpsWebhookEvent,
    request: Request,
    background_tasks: BackgroundTasks,
    authorization: Annotated[str, Depends(validate_authorization_header)],
):
    """Webhook trigger of the PR comment review process. Only works when a full Azure DevOps webhook event is provided."""
    if not pr_body.resource.pull_request_id:
        raise HTTPException(status_code=422, detail="Invalid pull request body")
    else:
        background_tasks.add_task(review_created_pull_request, pr_body.resource.pull_request_id, request)
        return {"status": "Accepted"}
        # return await review_created_pull_request(pull_request_id=pr_body.resource.pull_request_id, request=request)
