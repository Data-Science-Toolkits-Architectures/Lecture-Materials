"""One decision, from the confirmed application to the stored answer."""

from credit_backend.clients.extraction import Extractor
from credit_backend.clients.wording import WordingWriter
from credit_backend.contracts import (
    DecisionRecordRead,
    DecisionRequest,
    DecisionResponse,
    ExtractionResult,
)
from credit_backend.decisions.features import build_features
from credit_backend.decisions.records import DecisionRecords
from credit_backend.decisions.rules import Policy, RuleInputs, decide
from credit_backend.decisions.scoring import Scorer


class DecisionService:
    def __init__(
        self,
        scorer: Scorer,
        extraction: Extractor,
        wording: WordingWriter | None,
        records: DecisionRecords,
        policy: Policy,
    ) -> None:
        self._scorer = scorer
        self._extraction = extraction
        self._wording = wording
        self._records = records
        self._policy = policy

    def extract(self, payslip: bytes, debt_register: bytes) -> ExtractionResult:
        """What the documents say, before a case worker has confirmed any of it."""
        return self._extraction.extract(payslip, debt_register)

    def decide(self, request: DecisionRequest) -> DecisionResponse:
        """Decides on the figures the case worker confirmed. It reads no document itself."""
        entered = request.entered
        features = build_features(entered)
        probability = self._scorer.probability_of_default(features)
        decision = decide(
            RuleInputs(
                default_probability=probability,
                monthly_income=entered.monthly_income,
                has_loss_certificate=entered.has_loss_certificate,
            ),
            self._policy,
        )
        # Task 7d: connect the remaining steps. Have Model C word the decision, unless no
        # Model C is set. Store the decision with self._records. Then answer with the id of the
        # row it wrote, as record_id.
        raise NotImplementedError(f"Task 7d: {decision.outcome}, but neither worded nor stored")

    def recent(self, limit: int) -> list[DecisionRecordRead]:
        return self._records.recent(limit)

    def close(self) -> None:
        self._extraction.close()
        if self._wording is not None:
            self._wording.close()
