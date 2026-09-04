# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Lecture 2. Interpreter, dependencies and the lockfile
#
# Everything taught tonight, in the order it was taught. Run it top to bottom.
#
# The Unicorn Adoption Bureau is imported from the package rather than copied in,
# so there is exactly one version of it. Short teaching fragments are written out
# in full, because you should be able to read them without opening another file.

# %%
# beat: 1630 which-python
import sys

print("interpreter:", sys.executable)
print("version:    ", sys.version.split()[0])
print("first three places import looks:")
for entry in sys.path[:3]:
    print("   ", entry or "(the current folder)")

# %%
# beat: 1643 stdlib-against-pypi
import json

print("json ships with Python:", json.__file__)

try:
    import pandas
except ModuleNotFoundError as missing:
    print("pandas does not:", missing)

# %%
# beat: 1647 where-did-it-go
from pathlib import Path

venv = Path(sys.prefix)
print("this environment lives at:", venv)
site_packages = next(venv.glob("lib/python*/site-packages"), None)
print("packages land in:         ", site_packages)
print("and that folder is on sys.path:", str(site_packages) in sys.path)

# %%
# beat: 1749 generated-decide
from unicorn_adoption_bureau.generated import decide_as_generated as generated
import inspect

source = inspect.getsource(generated.decide)
print(f"the assistant wrote {len(source.splitlines())} lines")
print("\n".join(source.splitlines()[:14]))

# %%
# beat: 1806 line-count
from unicorn_adoption_bureau import rules

after = inspect.getsource(rules.decide)
print("generated:  ", len(source.splitlines()), "lines")
print("after the three buckets:", len(after.splitlines()), "lines")

# %%
# beat: 1811 fail-fast
from unicorn_adoption_bureau.rules import Application, MissingAnswer, decide

unanswered = Application(
    garden_m2=80.0, glitter_tolerance=None, hours_at_home=30, floor=1, has_lift=False
)
try:
    decide(unanswered)
except MissingAnswer as stopped:
    print("stopped, rather than scoring it as perfect:", stopped)

# %% [markdown]
# ## Exercise 1. Make the failing check pass
#
# One character in the function below is wrong. The Bureau's rule is that a
# garden of **at least** fifty square metres is enough, and the third assertion
# says so. Run the cell, read the failure, then fix it.

# %%
MIN_GARDEN_M2 = 50.0


def garden_is_big_enough(garden_m2: float) -> bool:
    return garden_m2 > MIN_GARDEN_M2  # TODO one character is wrong


assert garden_is_big_enough(50.1)
assert not garden_is_big_enough(49.9)
assert garden_is_big_enough(50.0), "a garden of exactly the minimum is big enough"
print("all three pass")

# %% [markdown]
# <details>
#
# <summary>Show the solution</summary>
#
# {{solution:garden-boundary}}
#
# The applicant with exactly the required garden is the one the rule was written
# for, and the one a strict comparison silently refuses. Boundaries are where
# rules are wrong, which is why the tests you write tonight go there first.
#
# </details>

# %% [markdown]
# ## Exercise 2. Write the missing test
#
# The Bureau refuses a unicorn above the second floor when there is no lift,
# whatever the rest of the application says. No test covers that. Write one.
#
# You have `Application`, `decide` and `pytest` already imported above.

# %%
def test_the_floor_rule_overrides_a_perfect_score():
    ...  # TODO


test_the_floor_rule_overrides_a_perfect_score()
print("it passes")

# %% [markdown]
# <details>
#
# <summary>Show the solution</summary>
#
# {{solution:floor-rule-test}}
#
# A policy rule is one the score cannot outvote, so the test has to start from an
# application that would otherwise be approved. A test that starts from a bad
# application would pass whether the rule existed or not.
#
# </details>

# %%
# solution-source
# This cell never reaches the notebook students receive. The build lifts the
# solution out of it, folds it into the exercise above, and then removes the
# cell. Keeping it here means a solution is real code that runs, rather than
# text somebody typed into a markdown cell.

def garden_is_big_enough(garden_m2: float) -> bool:
    """At least the minimum means at least, so the comparison is inclusive."""
    return garden_m2 >= MIN_GARDEN_M2
