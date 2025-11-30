from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ClientData(BaseModel):
    # Admittedly silly, but I do want to keep it in the body since it's a post request
    client_name: str


class WebhookRegistrationResponse(BaseModel):
    webhook_url: str
    token: str
    expires_at: datetime


class TokenValidationResponse(BaseModel):
    valid: bool
    expires_at: Optional[datetime]
    reason: Optional[str]
