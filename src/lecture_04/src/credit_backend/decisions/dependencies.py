"""Which concrete parts the decision service is built from."""

from typing import cast

from fastapi import Request

from credit_backend.clients.extraction import ExtractionClient
from credit_backend.clients.wording import WordingClient
from credit_backend.config import Settings
from credit_backend.decisions.records import DecisionRecords
from credit_backend.decisions.rules import Policy
from credit_backend.decisions.scoring import PlaceholderScorer, RegisteredScorer, Scorer
from credit_backend.decisions.service import DecisionService


def build_baseline() -> Scorer:
    # Your repository returns the baseline your team chose in lecture 2.
    return PlaceholderScorer()


def build_scorer(settings: Settings) -> Scorer:
    """The model that MODEL_A names, such as wandb-registry-model/model-a:production.

    Without MODEL_A, the baseline scores.
    """
    return (
        RegisteredScorer.from_registry(settings.model_a) if settings.model_a else build_baseline()
    )


def build_records(settings: Settings) -> DecisionRecords:
    # Task 7b: create the engine with SQLAlchemy's create_engine, from the database URL in
    # your settings. Then return DecisionRecords for that engine.
    raise SystemExit("Task 7b: connect the backend to PostgreSQL")


def build_wording(settings: Settings) -> WordingClient | None:
    # Task 6: return a WordingClient for the Model C your settings name. Return None when no
    # Model C is set, so that decisions go on without wording.
    return None


def build_service(settings: Settings) -> DecisionService:
    scorer = build_scorer(settings)
    records = build_records(settings)
    records.create_schema()
    return DecisionService(
        scorer=scorer,
        extraction=ExtractionClient(settings.extraction_url),
        wording=build_wording(settings),
        records=records,
        policy=Policy(
            threshold=scorer.threshold,
        ),
    )


def get_service(request: Request) -> DecisionService:
    return cast(DecisionService, request.app.state.service)
