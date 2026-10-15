# Lecture 3: training, tracking and versioning Model A

This folder holds the three notebooks of the lecture and the project code for this week. The notebooks are a reference. The project code is the training job for Model A, together with the change to the backend that loads the model the job registers.

By the end of the week the training job has trained a logistic regression and a random forest, tracked every run in Weights & Biases (W&B), and registered the best model of each kind. One of them carries the alias `production`, and your backend scores applicants with it.

## How the training job works

The job follows the order of the slide "The workflow in pseudo-code". Every step that learns from the data sees the training set only, and the test set is used once, at the very end.

| Step | File | What it does | Your task |
|---|---|---|---|
| 1 | `data.py` | Loads `data/credit_risk_dataset.csv`, drops duplicate rows and then the rows that carry the codes 96 or 98. Splits the rest into 70% training, 15% validation and 15% test, stratified and with a fixed seed. | |
| 2 | `preprocessing.py` | Builds every step that learns a number from the data. The models fit it on the training set and transform the validation set with it. | Task 2 |
| 3 | `metrics.py` | The metric every model is judged by. Every model refuses from the fixed threshold of 0.5 up. | Task 3 |
| 4 | `logistic_regression.py` | Trains one logistic regression, scores it on the validation set and logs the model to W&B. | Task 4 |
| 5 | `random_forest.py` | The same for a random forest. | Task 5 |
| 6 | `sweep.py` | Runs a W&B sweep over the settings of one model. Then it registers the best model of that kind found so far, under the alias `best-<kind>`. | Task 6 |
| 7 | `evaluate.py` | Compares your baseline with the best model of each kind, on the validation and on the test set. | Task 7 |
| 8 | `registry.py` | Registers the best model of a kind, and moves the alias `production` to the model you chose. | Task 7 |
| 9 | `tracking.py` | Opens a W&B run, and logs a trained model with what the backend needs to load it. | Task 1 |

The features are the fields of `FeatureVector` in your backend. The model is therefore trained on exactly the figures the backend builds for an applicant. `data.py` keeps them in their raw units, because that is what your baseline from lecture 2 expects. The preprocessing is part of the pipeline the job logs, so the backend applies the same fitted scaler to every applicant.

## Bring it into your repository

The folder runs on its own, so it carries a copy of the backend from lecture 2. Do not copy that part over yours. Copy the new files and merge the few changes instead.

1. Copy `src/credit_training` into the `src` folder of your repository. Copy the four test files `test_preprocessing.py`, `test_metrics.py`, `test_models.py` and `test_sweep.py` into `tests`, and `docs/model_card.md` into `docs`.
2. Copy `data/credit_risk_dataset.csv` from the root of this repository into a `data` folder at the root of yours. The training job looks for it there.
3. Add the new packages with `uv add joblib pandas scikit-learn wandb`. Then add the second package to `pyproject.toml`, as ours does under `[tool.uv.build-backend]`.
4. Merge the changes to three backend files. This command, run from the root of this repository, shows every line that changed since lecture 2.

   ```bash
   git diff --no-index src/lecture_02/src/credit_backend src/lecture_03/src/credit_backend
   ```

   - `scoring.py` gains `RegisteredScorer`. It downloads a registered model and scores an applicant with it, preprocessing included. `probability_of_default` may now return `None`, because a model cannot score a figure nobody could read. Your baseline stays where it is.
   - `dependencies.py` gains `build_baseline` and `build_scorer`. The backend scores with the registered model that the environment variable `MODEL_A` names, and with your baseline when `MODEL_A` is not set.
   - `rules.py` refuses an application from the threshold up. That is the fix from the boundary test of lecture 2, so your copy has it already.

5. Log in to W&B once on each machine with `uv run wandb login`.

In this folder `features.py` is still the placeholder from lecture 2, so the model here learns from `age` alone. In your repository it learns from the features you built.

## Run it

Run every command from the root of your repository.

```bash
uv run python -m credit_training.logistic_regression
uv run python -m credit_training.sweep logistic-regression --runs 20 --method bayes
uv run python -m credit_training.sweep random-forest --runs 20 --method random
uv run python -m credit_training.evaluate
uv run python -m credit_training.registry promote logistic-regression
```

The last command promotes the logistic regression. Promote whichever kind you chose in Task 7. Then start the backend with the model in production, and send the sample request through http://localhost:8000/docs.

```bash
MODEL_A=wandb-registry-model/model-a:production uv run uvicorn credit_backend.main:app
```

In PyCharm, set `MODEL_A` under Environment variables in your run configuration. A container has no W&B login, so it needs your API key as well. Pass both with `docker run -e MODEL_A=wandb-registry-model/model-a:production -e WANDB_API_KEY`, which hands the container the key from your shell. Never write the key into a file in your repository.

`uv run pytest` runs the checks. A check that is skipped names the task it is waiting for.

## Your tasks

**Bring in the training job**

1. Bring the training job into your repository, as described above, through a pull request. Return your team's baseline from `build_baseline` in `dependencies.py`. Set `ENTITY` in `tracking.py` to your W&B team, so that all of you log into one project. The registry belongs to an organisation, so the team has to belong to one too. If it does not, log into one person's account. Then run the logistic regression once and find its run in W&B.

**Data and metric**

2. Choose the scaler for Model A and handle the extreme values you found in the EDA, in `preprocessing.py`. Learn every limit on the training set only. Record your choices in the decision log.
3. Choose the metric you will be judged on, in `metrics.py`. Justify it in the decision log. The threshold is fixed at 0.5 for every team, so your metric judges every model at that threshold.

**Models and tracking**

4. Track the training of the logistic regression, so that a teammate can find a run again and repeat it. The slide "What to log" lists what belongs in a run.
5. Implement the random forest in `random_forest.py`, with its metric and its tracking, as the logistic regression does it.

**Sweeps, registry and the final comparison**

6. Choose the settings to search for each model in `SEARCH_SPACES` in `sweep.py`, and run a sweep for each. The best model of each kind lands in the registry as `best-logistic-regression` or `best-random-forest`.
7. Run `evaluate.py` once. Choose the model for production by its validation score, and report its test score. Then promote it with `registry.py`, and record the decision in your decision log.

**Backend and documentation**

8. Start your backend with `MODEL_A` set to the model in production, and send the sample request. The answer names the registered version that scored it.
9. Write the model card in `docs/model_card.md`. One page, with the intended use, the data, your metric, the results and the known limitations.
10. Update your decision log.
