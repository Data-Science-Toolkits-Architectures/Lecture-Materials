# Explanation patterns

Use the smallest pattern that fits the question. Omit sections that do not add understanding, and use the language of the user's prompt.

## Small code fragment

1. **Direct answer:** Say what the fragment accomplishes in one sentence.
2. **Concrete trace:** Walk one realistic input through the statements in execution order.
3. **Key concept:** Define the one language feature the student must understand.
4. **Result or side effect:** Show the returned value and any changed state.
5. **Likely surprise:** Explain one non-obvious edge case only if it is relevant.

For example, explain `names[:3]` as “a new list containing at most the first three items,” then trace a short list. Introduce the term *slice* after stating the behavior. Mention that the original list is unchanged; discuss short lists only if that could affect the student's task.

## Function or class

Start with its contract:

- What responsibility does it have?
- What input does it expect, including important types or shapes?
- What does it return or change?
- Who calls it, and what does it rely on?

Then follow the normal path. Cover a branch, exception, mutation, or dependency only when it changes the answer. A compact flow such as `request -> validate -> transform -> save -> response` is often clearer than paraphrasing every line.

## Repository tour

Explain the repository from the outside in:

1. State what the project produces or enables.
2. Name only the few paths that reveal its structure and give each a one-line role.
3. Identify the entry point and trace one representative workflow across files.
4. Give the actual command used to run the project or its smallest useful example, if the repository provides one.
5. Point to the test that best demonstrates the expected behavior.
6. Suggest the next file to read and explain why it is the best next step.

Prefer a selective map over a directory dump. If the repository contains several applications or packages, first explain their boundaries and then focus on the one relevant to the question.

## Data science pipeline

Trace both the data and its meaning:

```text
source -> load -> validate -> transform -> split -> fit -> evaluate -> output
```

At each relevant transition, state:

- the unit represented by one row or sample;
- important columns, features, labels, array shapes, or units;
- what changes and what information may be lost;
- where randomness enters and whether it is controlled; and
- which operations learn from data, especially across training and test boundaries.

Distinguish a technical operation from its statistical purpose. For example, first say how values are standardized, then explain why comparable scales may help the model.

## Error or traceback

Use this causal order:

1. **Meaning:** Translate the final error into plain language.
2. **Location:** Identify the student's code that triggered it, not only the deepest library frame.
3. **Cause:** Connect the observed value or state to the failed expectation.
4. **Evidence:** Point to the relevant variable, call, configuration, or preceding message.
5. **Next check:** Offer the smallest diagnostic step that can confirm or reject the explanation.

Separate the root cause from later symptoms. If more than one cause fits the evidence, say what observation would distinguish them rather than presenting a guess as certain.
