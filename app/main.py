from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .mcp.azure_devops_server import azure_devops_mcp_app
from app.observability.observability import setup_logfire
from .routers import webhooks, pull_requests

# Good to extend later to include https://fastapi.tiangolo.com/tutorial/metadata/
app = FastAPI(
    title="Azure DevOps PRBot",
    description="A FastAPI application to process PR webhooks from Azure Devops.",
    version="0.0.1",  # Would need to make dynamic, but not important now
    lifespan=azure_devops_mcp_app.lifespan,
)

setup_logfire(app)

app.include_router(webhooks.router)
app.include_router(pull_requests.router)
app.mount("/mcp", app=azure_devops_mcp_app)
# In an enterprise setting, this needs to be much more restrictive.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # temp
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Does what it says on the cover."""
    return JSONResponse(status_code=200, content={"status": "ok"})
