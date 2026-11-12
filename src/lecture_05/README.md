# Lecture 5: interfaces, model serving and the frontend

This folder holds the notebook of the lecture, the small backend from the slides, and two small Streamlit pages. It holds no page for your system and no templates. Your coding agent writes your page from the requirements you write.

| File | What it is for |
|---|---|
| `05_http_and_interfaces.ipynb` | Raw requests and responses, status codes, and what arrives when a value is left out, null, 0 or in the wrong unit. |
| `small_backend.py` | The backend from the slides, which the notebook starts by itself. An application has three fields. It has no model, approves everything and repeats what it received. |
| `rerun_demo.py` | A small Streamlit page that shows the rerun and session state. |
| `call_demo.py` | The page from the slide that calls the backend. It has a sentence for every kind of answer. |

## Run it

Run every command from this folder.

```bash
uv sync
uv run pytest
uv run streamlit run rerun_demo.py
```

To try the page that calls the backend, start the small backend in one terminal and the page in a second one.

```bash
uv run uvicorn small_backend:app --port 8000
BACKEND_URL=http://localhost:8000 uv run streamlit run call_demo.py
```

In PowerShell on Windows, set the variable first.

```powershell
$env:BACKEND_URL = "http://localhost:8000"
uv run streamlit run call_demo.py
```

Stop the backend while the page is open, and press Decide again.

Open the notebook with the kernel from `.venv` in this folder. If your editor picks another kernel, the first cell installs the two packages the notebook needs into it. The notebook starts the small backend by itself.

## Bring it into your repository

You do not need to copy anything from this folder. The notebook and the two pages are demos.
