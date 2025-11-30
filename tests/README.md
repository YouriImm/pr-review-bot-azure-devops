## Tests & Evals

---

The current implementation of both tests and evals is intended to be sufficient to catch any obvious issues with the
code, but I certainly will not pretend it is as thorough as it would be in a production scenario.

The unit tests cover the majority of the code and simply uses Pytest. Most of the code relating to the API itself is
covered.

For evals especially you will currently find an implementation for:
- _Python sub-agent review performance._ These evals are deterministic and validate certain rules are correctly marked as violated.
- _Python review comment accuracy and tone._ These evals use an LLMJudge and are non-deterministic.

Both have been implemented only for a subset of the currently available rules. There's a rather simple reason for this:
to save time and money. That said, it would be rather simple to implement additional evals. They use [Pydantic Evals](https://ai.pydantic.dev/evals/).

I wanted to ensure the evals are part of CI/CD automation like any other test. Evals are often subjective. We can not
realistically enforce that all evals must always return a boolean PASS or FAIL. What we can do however is let Pydantic-evals
assign a 0-1 score to each eval's assertion. We then wrap the evals in a Pytest invocation and expect a certain
average score to have been reached.

---

### Extending for production
To further protect the quality of the solution the following comes to mind:
- Comprehensive eval coverage of all the rules, not some of them.
- Assessing behavior of the agent when multiple rules are violated by the same script.
- Ensuring adherence of the agent to some nuances in the system prompt, like only allowing certain rules to be
  evaluated once per script.
