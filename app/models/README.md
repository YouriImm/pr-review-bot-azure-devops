Just about everything in this app uses Pydantic models for validation and structure. There's a couple reasons for this:

- FastAPI all but mandates it (and rightly so);
- It helps the LLMs perform better;
- Input/output validation is important for writing decent software;
- I feel less confident in my code whenever I skip them.

You'll note that there are particularly many Azure DevOps models. This is one of the areas where an LLM proved
very helpful, though I did a fair bit of tweaking afterwards. They are created to mirror the Azure DevOps API and are
used primarily by the MCP tools in the system.
