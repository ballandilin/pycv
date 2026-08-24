# pyresume

*(v1, CLI only. The tool is still named `pycv` in the code; the rename will come with the TUI version currently in progress on the `wip/tui` branch.)*

Adapts a resume and generates a cover letter for a given job posting, via the Groq API.

Takes a resume (Markdown or PDF) and a job posting in text format as input, and writes the results to `results/<job_name>/`: `offre.txt` (a copy of the job posting), `cv.md` (the adapted resume) and `lettre.md`.

## Installation

```sh
uv sync
cp .env.example .env   # then fill in GROQ_API_KEY
```

## Usage

```sh
# a single job posting
uv run main.py my_resume.pdf -f job_posting.txt

# all .txt job postings in a folder
uv run main.py my_resume.pdf -b job_postings_folder/
```

Prompts, model, and temperature are configurable in `prompts.toml`.

## Known limitation

The cover letter is generated from the already-adapted resume: if the resume adaptation drifts from the original, the letter inherits the drift, and may even amplify it.
