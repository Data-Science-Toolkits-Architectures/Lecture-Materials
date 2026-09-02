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
