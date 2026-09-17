---
name: explain-code
description: Explain code, notebooks, errors, data flows, or repository structure to students with limited programming experience. Use when the user asks what code does, how parts connect, why a construct exists, or how to approach an unfamiliar repository. Do not use when the primary request is only to write, fix, refactor, or review code.
---

# Explain code to students

Help the student build an accurate mental model and continue independently. Prefer the smallest complete explanation over a comprehensive lecture.

## Trigger

Use this workflow for questions about:

- what a code snippet, function, class, notebook cell, command, or error means;
- how data or control moves through a program;
- how a repository is organized and where to start reading it; or
- why a relevant implementation choice or programming concept exists.

If the request mixes explanation with implementation, explain the important reasoning and then perform only the changes the user requested.

## Procedure

1. **Identify the real question.** Determine the smallest code area or repository path needed to answer it. Infer the student's level from the prompt; ask a question only when ambiguity would materially change the answer.
2. **Inspect before explaining.** Read the referenced code and its immediate context. For a repository overview, inspect the README, top-level structure, dependency or build files, entry points, and representative tests. Follow imports or calls only as far as needed. Do not edit files unless the user asks for changes.
3. **Answer first.** Begin with one or two plain-language sentences that directly answer the question. Then add the evidence and detail needed to make the answer understandable.
4. **Build the explanation outside in.** State the purpose, place it in context, and walk through one concrete execution or data-flow example using the code's real names. Explain syntax only when it is necessary to understand the behavior.
5. **Make connections explicit.** Say what goes in, what comes out, what calls the code, what it calls, and which state or files it changes when these facts matter. For data science code, include relevant table columns, array shapes, units, missing-value behavior, and train/test boundaries.
6. **Anticipate the next confusion.** Briefly answer one or two likely follow-up questions when they prevent a common misunderstanding, such as “Where does this value come from?”, “Why is this step needed?”, or “What happens when the input is empty?” Do not append a generic FAQ.
7. **Verify the explanation.** Ground claims in inspected files, symbols, and observable behavior. Run a small, safe check only when reading is insufficient. Label an inferred design reason as an inference rather than a fact.

Choose the walkthrough shape that fits the request:

- **Snippet or notebook cell:** purpose, execution order, inputs, result, and one relevant gotcha. In notebooks, account for hidden state and out-of-order execution.
- **Function or class:** contract first, then the main path, important branches, side effects, and callers.
- **Repository:** purpose, a selective map of important paths, entry point, main flow, how to run it, and where behavior is tested. Do not inventory every file.
- **Error:** translate the message, identify where it originates, explain the causal chain, and give the smallest useful next diagnostic step.

## Explanation rules

- Answer in the language used in the user's prompt unless the user requests another language. Keep code identifiers, commands, paths, and error text unchanged.
- Match the student's demonstrated level. Define a technical term in plain language the first time it appears; do not replace it with an inaccurate simplification.
- Separate **what happens** from **why it matters**. State the literal behavior before using an analogy, and mention the limit of an analogy when it could mislead.
- Prefer a concrete example with actual values over an abstract description. Trace only the path needed to answer the question.
- Quote only the smallest useful code fragment. Refer to file paths and symbols; include line numbers only when they are stable and verified.
- Use short paragraphs or bullets and one idea per sentence. Add headings only when the response has multiple distinct parts.
- Do not assume that a familiar tool, acronym, language feature, or repository convention is obvious.
- Do not hide uncertainty, invent intent, or claim that code was executed when it was only read.
- Do not end with filler such as “Let me know if you have questions.” When helpful, end with one concrete next file, command, or check for understanding.

## Resources

Read only the relevant section of [references/explanation-patterns.md](references/explanation-patterns.md) when a consistent structure would make a snippet, repository, data pipeline, or error explanation clearer. The patterns are guides, not mandatory response templates.

## Definition of done

Before finishing, check that the response:

- directly answers the student's exact question near the beginning;
- uses the prompt's language and defines necessary jargon;
- distinguishes observed behavior from inferred rationale;
- explains the relevant inputs, output, flow, and context without unrelated detail;
- addresses the most likely misconception or next question when useful;
- points to evidence in the code or repository; and
- leaves the student with a usable mental model or a concrete next step.

## Portability

Base the explanation on the repository in front of you. Do not assume Python, a particular editor, Unix commands, or a fixed project layout. Adapt examples and commands to the actual language, build system, operating environment, and tools available. Keep links to this skill's resources relative so the whole folder can be copied into another repository or a personal skills directory.
