# Lecture 4: from one container to a system

This folder holds the project code for this week. Your backend stops being one container and becomes part of a system of four services. Two of them run models you did not train. Model B reads the payslip and the register extract, and Model C puts a decision into words.

By the end of the week one command starts the whole system. A case worker can have the two documents read, confirm the figures, and get a decision that is worded and stored.

## What the system looks like now

| Service | What it does | Port on your machine |
|---|---|---|
| `postgres` | Stores one row for every decision. The rows survive a restart, because they live in a volume. | 5432 |
| `extraction` | The Information Extraction Service. It runs Model B on the two documents and answers with the fields it read. A field it cannot read is `None`. | 8001 |
| `ollama` | Runs Model C. | 11434 |
| `backend` | Your backend. It forwards the documents to `extraction`, scores with Model A, applies the rules, asks `ollama` for the wording and stores the decision. | 8000 |

A decision takes two requests. `POST /extractions` sends the two documents and answers with what Model B read. It decides nothing. The case worker checks those figures and corrects them. Then `POST /decisions` sends the confirmed figures. The backend never reads a document while it decides, because a model's reading is not yet a fact. `GET /decisions/recent` shows the stored rows, newest first.

## How the parts work

| Step | File | What it does | Your task |
|---|---|---|---|
| 1 | `docker-compose.yaml` | Starts the four services with one command. `postgres` is complete, as the example for the other three. | Task 2 |
| 2 | `extraction_service/src/credit_extraction/config.py` | Reads the Model B you chose from the environment. A missing setting stops the service when it starts. | Task 3 |
| 3 | `extraction_service/src/credit_extraction/main.py` | Loads Model B once, when the service starts. | Task 3 |
| 4 | `extraction_service/src/credit_extraction/documents/` | Asks Model B questions about each document and turns the answers into typed values. | |
| 5 | `scripts/evaluate_extraction.py` | Sends the forty sample applicants to the service. It prints a metric for each field, in total and for each layout. | Task 5 |
| 6 | `src/credit_backend/clients/wording.py` | Has Model C put the outcome and the reasons into words. Model C decides nothing. | Task 6 |
| 7 | `src/credit_backend/decisions/rules.py` | Applies the rules. Every rule that fails adds its reason. | Task 7a |
| 8 | `src/credit_backend/config.py` and `decisions/dependencies.py` | Read the settings from the environment, and build the service from them. | Tasks 6 and 7b |
| 9 | `src/credit_backend/decisions/records.py` and `contracts.py` | The table with one row for every decision, and `DecisionRecordRead`, which shows a row through the API. | Task 7c |
| 10 | `src/credit_backend/decisions/service.py` | Connects the steps of one decision. | Task 7d |
| 11 | `src/credit_backend/clients/http.py`, `clients/extraction.py` and `main.py` | Calls the other services, and says what happens when one does not answer. | Task 7e |
| 12 | `src/credit_backend/decisions/router.py` | The four endpoints. | |

The extraction service is a project of its own, with its own `pyproject.toml`, `Dockerfile` and tests. It needs PyTorch, and your backend does not. Keeping them apart keeps several gigabytes out of the backend image.

## Bring it into your repository

The folder runs on its own, so it carries a copy of the backend from lecture 3. Do not copy that part over yours. Copy the new parts and merge the changes instead. Make every change through a pull request.

Start by removing the task markers of lectures 2 and 3 from your repository. Those tasks are done, and their numbers would clash with the tasks of this week. `git grep -n "Task [0-9]"` lists them, in the code and in the `pytest.skip` messages of your tests. Delete each comment, and turn each skip message into a plain sentence. Afterwards every task marker in your repository belongs to lecture 4.

1. Copy `extraction_service` to the root of your repository. Copy `scripts/evaluate_extraction.py` into a `scripts` folder at the root.
2. Copy the folder `data/sample-documents` from the root of this repository into the `data` folder of yours. It holds forty pairs of documents and `ground_truth.json`, the values the documents are known to carry.
3. Copy `docker-compose.yaml` and `.env.example` to the root of your repository. Add the line `.env` to your `.gitignore` and to your `.dockerignore`. Add `extraction_service` to your `.dockerignore` too, so that it stays out of the backend image.
4. Add the new packages with `uv add httpx ollama "psycopg[binary]" pydantic-settings sqlalchemy`. Then copy the block `[tool.pytest.ini_options]` from our `pyproject.toml` into yours. Without it, `uv run pytest` cannot import the evaluation script and the shared test helpers.
5. Merge the changes to the backend. This command, run from the root of this repository, shows every line that changed since lecture 3.

   ```bash
   git diff --no-index src/lecture_03/src/credit_backend src/lecture_04/src/credit_backend
   ```

   - `config.py`, the folder `clients` and `decisions/records.py` are new. Copy them.
   - `contracts.py` gains the fields the extraction service answers with. `CaseWorkerInput` gains `has_loss_certificate`. `DecisionResponse` gains `wording` and `record_id`.
   - `rules.py` gains two inputs in `RuleInputs`, the income and the loss certificate.
   - `service.py`, `dependencies.py`, `router.py` and `main.py` change to connect the new parts. Merge them into yours.
   - `scoring.py` and `features.py` are the ones from lecture 3. Keep yours.

6. Copy the test files from `tests` into your `tests` folder. `test_api.py` replaces yours, because the backend now needs a database to start, and the new test does not.

In this folder `features.py` is still the placeholder from lecture 2, and the backend scores with the placeholder baseline unless `MODEL_A` is set.

## Run it

Run every command from the root of your repository. Copy `.env.example` to `.env` first and fill in every value. `.env` holds the database password and your W&B key, so it never goes into Git.

```bash
docker compose up --build
```

The first start downloads Model B into a volume, which takes a few minutes. Model C is pulled once into the volume of `ollama`, with the tag you set in `.env`. Pull it before the first decision. Until it is pulled, Ollama is healthy but has no Model C, and every decision comes back with `wording: null`.

```bash
docker compose exec ollama ollama pull <your Model C tag>
```

`docker compose ps` shows whether each service is healthy. `docker compose logs -f backend` follows the log of one service. `docker compose down` stops the system and keeps the data. `docker compose down -v` deletes the volumes as well, and with them every stored decision.

The backend starts once Task 7b is done, because it connects to the database when it starts. Until then it stops with a message that names the task.

To try the extraction service on its own, start only that service with `docker compose up extraction` and open http://localhost:8001/docs. You can also run it outside Docker, from inside `extraction_service`.

```bash
uv run --env-file ../.env uvicorn credit_extraction.main:app --port 8001
```

To measure Model B, start the extraction service and run the evaluation.

```bash
uv run python scripts/evaluate_extraction.py
```

`uv run pytest` runs the checks. Run it at the root and, for Task 3, also inside `extraction_service`, which is a project of its own with its own tests. A check that is skipped names the task it is waiting for.

## Check that it works

1. `docker compose ps` lists four services, and each is healthy.
2. http://localhost:8000/health answers `{"status": "ok"}`.
3. In http://localhost:8000/docs, `POST /extractions` with `payslip_000_letterhead.pdf` and `register_000_office.pdf` answers with what Model B read.
4. `POST /decisions` with the sample request answers with the outcome, the reasons, the wording, the probability of default, the model version and a `record_id`.
5. `GET /decisions/recent` shows that decision.
6. After `docker compose down` and `docker compose up`, the decision is still there.
7. After `docker compose stop ollama`, a decision still comes back, with no wording.

`create_schema` creates the table when it is missing, and it never changes a table that exists. If you add a column after the table was created, nothing happens to the table. On your laptop, `docker compose down -v` deletes the table, and the next start creates it again.

## Your tasks

**Bring in the drop**

1. Bring the drop into your repository through a pull request, as described above. That covers the Information Extraction Service, the documents with known values and the evaluation script.

**The system**

2. Complete `docker-compose.yaml` so that one command starts the whole system. That is `postgres`, `extraction`, `ollama` and your backend. Give each service a health check. The backend starts only when the others are healthy. Every secret comes from `.env`, never from Git.

**Model B**

3. Choose Model B. On the Hugging Face Hub, filter by the task Document Question Answering. Choose a model below about one billion weights that runs on a CPU in Docker. Load it in the extraction service, pinned to one revision. The checkpoint and the revision come from the environment. Hint: search the Hub for `layoutlm` and pick one that answers questions about documents. Read `extraction_service/src/credit_extraction/documents/reader.py` first: your model must work with what the service gives it.
4. Try the extraction service on its own. Start it, open http://localhost:8001/docs, and send one payslip and one register extract to `POST /extractions`. A field it cannot read is `None`.
5. Evaluate Model B with `evaluate_extraction.py` on the documents with known values. Use the metric that fits each field. The date of birth is done as the example. Write the other metric functions marked `Task 5`.

**Model C**

6. Choose Model C for Ollama, and write its prompt in `clients/wording.py`. The file shows a borrowed example of a good input and a good output. Model C gets the outcome and the reasons, and nothing else. It decides nothing. Read its tag from `MODEL_C`. If the wording fails or no Model C is set, the decision goes on without wording.

**The backend**

7. Complete the backend so that every decision is complete and stored.
   - a) In `rules.py`, decide what an open loss certificate does to the outcome. A value nobody could read gets a reason of its own.
   - b) In `config.py` and `dependencies.py`, connect to PostgreSQL with the database URL from the environment.
   - c) In `records.py`, add the columns of the table, one row for every decision. An unknown value is stored as `NULL`, not as 0.
   - d) In `service.py`, connect the steps of a decision. The answer carries the `record_id` of the stored row.
   - e) In the clients, set the timeouts, and handle a service that does not answer. When the extraction service does not answer, `POST /extractions` answers with a clear 503. When Ollama does not answer, the decision goes on without wording.

**Documentation**

8. Update your decision log. Record the Model B and the Model C you chose and why, your metrics and what they showed, and every choice you made in Task 7.
