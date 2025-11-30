This folder doesn't contain much more than large system prompt strings organized in a logical file separation. There
are no user prompts at all since this is an automated system.


While this works perfectly fine for now, in long-term enterprise usage you'd want to decouple prompts from the code
itself. You very likely would not want every change to your system prompts to mandate a full redeployment of your app.

If we decouple prompts from code, we can iterate on system prompts and code independently of one another.
Improvements to the system would be faster and easier to make that way. Another point is that while technically
speaking we could argue that there is version control on the prompts even now purely because we're in a git
repository, we lack dedicated prompt version management like the ability to compare prompt iterations and
promote/demote them.

No need to DIY this. One google search gets us a long list of (often paid) options. Some free options to consider:
- [Langfuse Prompt Management](https://langfuse.com/docs/prompt-management/overview)
- [MLFLow Prompt Registry](https://mlflow.org/docs/3.0.1/prompts)
