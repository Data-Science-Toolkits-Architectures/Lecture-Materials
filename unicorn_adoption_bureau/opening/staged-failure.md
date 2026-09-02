# The opening failure, staged

For the twelve minutes at 16:18. Nothing runs live. Two prepared terminal recordings, played
one after the other, then the room is asked where the difference could come from.

Anna and Ben are in the same team. Same repository, same commit, same application.

## Terminal A, Anna

```
$ git log --oneline -1
a1f4c2e  Score an application

$ uv run bureau score application-114.json
Application 114
Score 70.5, rounded to 71
Threshold 71
APPROVED
```

## Terminal B, Ben

```
$ git log --oneline -1
a1f4c2e  Score an application

$ uv run bureau score application-114.json
Application 114
Score 70.5, rounded to 70
Threshold 71
REFUSED
```

Same commit. Same input. One applicant gets a unicorn and the other does not. No error, no
traceback, no warning.

## The question to the room

Two minutes, in pairs, on paper. Write down every place that difference could possibly be
hiding. Do not try to solve it, just list the places.

## The answer space, revealed

There are exactly four, and they stack.

| | Layer | How it could produce this | Pinned by |
|---|---|---|---|
| 4 | The operating system | a locale that formats or parses numbers differently, a package with no build for that platform so a fallback is used | the Docker image |
| 3 | The interpreter | a rounding or formatting behaviour that changed between two CPython versions | uv and `.python-version` |
| 2 | The dependencies | one machine has a package the other does not, or a different version of it | `pyproject.toml` and `uv.lock` |
| 1 | The source code | a change that was never committed | Git, done in L1 |

L1 pinned layer 1, and layer 1 is the one place this cannot be hiding, because both terminals
print the same commit.

## What it actually was

Layer 2. The scoring code rounds the score before comparing it to the threshold.

```python
try:
    from half_up import round_half_up as _round
except ImportError:
    _round = round
```

Anna's environment has the optional package. Ben's does not, so Python's built in `round` is
used instead, and Python rounds half to even rather than half up.

```
>>> round(70.5)
70
>>> Decimal("70.5").quantize(Decimal("1"), ROUND_HALF_UP)
Decimal('71')
```

Neither machine is broken. Neither student did anything wrong. Nobody wrote down which packages
this project needs, so the two machines answered that question differently.

## Why this failure and not another

It is silent. There is no traceback to read and no error to search for, which is the shape of
failure this whole module is about, and it is the shape they will meet again in the service we
provide.

It is decidable. Once the layer is named, the fix is obvious, so the twelve minutes end with an
answer rather than a mood.

And the fallback pattern is real. `try: import, except ImportError: use something else` is
everywhere in Python, and it is exactly how a missing dependency turns into a wrong number
instead of a crash.
