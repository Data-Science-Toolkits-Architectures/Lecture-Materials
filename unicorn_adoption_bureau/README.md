# The Unicorn Adoption Bureau

The teaching domain for L2. An application to adopt a unicorn is scored, a decision is
returned, and a reason is written that the applicant can be shown.

It has the same shape as the semester project and none of its judgement, so the structure
transfers and the credit decisions stay yours to make. See `decisions.md` in the lecturers'
repository, "The domain a deck teaches on".

| Path | What it is |
|---|---|
| `generated/decide_as_generated.py` | What a coding assistant produced from one sentence. Kept unedited. Every code quality example in L2 is read off this file |
| `rules_restructured.py` | The middle state. The database, the email, the HTML, the duplicate branches and the config class are gone, and an unanswered question raises. **The logic is untouched, so the boundary fault survives.** It exists so that a test can fail in the room |
| `rules.py` | The same decision, correct. Numbers in, a `Decision` out, no database, no email, no HTML |
| `tests/test_rules.py` | Boundaries, unanswered questions, and the policy rule that overrides a perfect score |
| `Dockerfile` | One container, the layer 4 example |
| `workflow-example.yml` | The continuous integration example. Not in `.github/` on purpose |
| `opening/staged-failure.md` | The two prepared terminals for 16:18, and the four layers they open onto |

## Three states of the same file

The block teaches that restructuring makes code testable and testing makes it correct, which
are two different activities that students reliably conflate.

| File | State | Same test file gives |
|---|---|---|
| `generated/decide_as_generated.py` | as an assistant wrote it | cannot be tested at all, it needs a database and an SMTP server |
| `rules_restructured.py` | after the three code quality buckets | 11 passed, **1 failed** on the garden boundary |
| `rules.py` | after the failure is narrowed and fixed | 12 passed |

The red test is deliberately left red at the end of the second input block and turns green in
the notebook block, so the second half of the evening breaks on a cliffhanger the way the first
half does.

## The two faults in the generated file

Both are real assistant output rather than planted, and both are voted on in the room.

An unanswered glitter question becomes `10`, the maximum, so an applicant who skipped it is
scored as maximally glitter tolerant and approved.

The garden test is `garden_m2 > 50` when the stated minimum is 50, so an applicant with exactly
the required garden is refused.

## Running it

```bash
uv sync
uv run pytest
uv run pytest --cov=rules
uv run ruff check .
uv run ty check .
docker build -t bureau . && docker run bureau
```
