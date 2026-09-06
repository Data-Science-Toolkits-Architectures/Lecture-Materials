# Lecture 2, the code and the notebook

Everything for lecture 2 in one folder. The notebook, the code it imports, and
the tests. It is your own system, the credit decision, rather than an invented
one, so nothing has to be translated before you can use it.

**Every number here is an example, not a recommendation.** Which threshold you
use, which policy rules you add, which of the two mistakes you would rather
make, and what the applicant is told are yours to decide and to defend in your
decision log. Nothing in this folder answers any of them, and the places where
your judgement goes are marked.

| Path | What it is |
|---|---|
| `02_environments_containers_tests.ipynb` | the notebook for the session, with the exercises and their folded solutions |
| `generated/decide_as_generated.py` | what a coding assistant produced from one sentence, kept unedited. Every code quality example in L2 is read off this file |
| `rules_restructured.py` | the same decision after the three code quality buckets. Separated, readable, and still wrong |
| `rules.py` | the same again after the failing test is narrowed and fixed |
| `tests/test_rules.py` | boundaries, missing fields, and the policy rule that overrides the model |
| `Dockerfile` | one container, the layer 4 example |
| `workflow-example.yml` | the continuous integration example, deliberately not in `.github/` |

## Three states of the same file

Restructuring makes code testable. Testing makes it correct. They are different
activities and they are easy to confuse. The same test file gives a different
answer against each state.

| File | Result |
|---|---|
| `generated/decide_as_generated.py` | cannot be tested at all, it needs a database and a notification service |
| `rules_restructured.py` | 7 passed, 1 failed on the threshold boundary |
| `rules.py` | 8 passed |

## The two faults in the generated file

Both are ordinary assistant output rather than planted, and both are silent.

A missing `debt_ratio` becomes `0.0`, so an applicant who reported no debts and
an applicant who reported nothing at all are treated the same way.

The threshold test is `> 0.30` where the rule is at or above, so an applicant
sitting exactly on the threshold is approved.

## Running it

Run everything from the repository root.

```bash
uv sync
uv run pytest
uv run pytest --cov=src.lecture_02.rules
uv run ruff check .
uv run ty check .
docker build -f src/lecture_02/Dockerfile -t rules . && docker run rules
```
