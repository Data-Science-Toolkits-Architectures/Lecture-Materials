"""Where the probability of default comes from."""

from typing import Protocol

from credit_backend.decisions.features import FeatureVector


class Scorer(Protocol):
    @property
    def model_version(self) -> str: ...

    @property
    def threshold(self) -> float: ...

    def probability_of_default(self, features: FeatureVector) -> float: ...


class PlaceholderScorer(Scorer):
    """The same probability for every applicant."""

    @property
    def model_version(self) -> str:
        return "placeholder"

    @property
    def threshold(self) -> int:
        return 0.30

    def probability_of_default(self, features: FeatureVector) -> float:
        return 0.10


# Task 6: your BaselineScorer(Scorer). A probability of default worked out by hand from
# the features, until Model A replaces it in lecture 3.
# Ask yourself: If I (with my human judgment) were to 
