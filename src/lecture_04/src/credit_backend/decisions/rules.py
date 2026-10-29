"""The decision rules, and the limits they are applied against."""

from dataclasses import dataclass

from credit_backend.contracts import Money, Outcome, Reason


@dataclass(frozen=True)
class Policy:
    threshold: float


@dataclass(frozen=True)
class RuleInputs:
    default_probability: float | None
    monthly_income: Money | None
    """The income as the case worker confirmed it, or None if nobody could establish it."""
    has_loss_certificate: bool | None
    """True when the register records an open loss certificate, None when nobody could read it."""


@dataclass(frozen=True)
class Decision:
    outcome: Outcome
    reasons: tuple[Reason, ...]


def decide(inputs: RuleInputs, policy: Policy) -> Decision:
    """Every rule that fails adds its reason. No reason means approved."""
    reasons: list[Reason] = []

    if inputs.default_probability is not None and inputs.default_probability >= policy.threshold:
        reasons.append(Reason.DEFAULT_PROBABILITY_ABOVE_THRESHOLD)

    # Task 7a: decide what an open loss certificate does to the outcome, and write that rule
    # here. A value nobody could read, such as a register that is None, is not a clean register.
    # Give it a reason of its own. Every reason refuses as the outcome below is worked out. If
    # one of yours should not, change how the outcome is worked out. Record why in your
    # decision log.

    outcome = Outcome.REFUSED if reasons else Outcome.APPROVED
    return Decision(outcome=outcome, reasons=tuple(reasons))
