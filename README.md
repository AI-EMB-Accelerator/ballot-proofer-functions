# Ballot Proofer Functions

Azure Functions for Ballot Proofer

## 🚀 Quick Start

1. Install correct version of Python
2. Create `.env` file
3. Install uv
4. Run `uv sync --dev`
5. Run debug from VS Code

Alternative: `uv run file_name.py`

## 📦 Packages

**Add Package**

1. Run `uv add [PACKAGE NAME]`
2. Use `uv pip compile pyproject.toml -o requirements.txt`

**Remove Package**

1. Run `uv remove [PACKAGE NAME]`
2. Use `uv pip compile pyproject.toml -o requirements.txt`

## 🔧 Setup Virtual Environment

1. Run `uv venv`
2. Activate the environment
   - Mac/Linux - `source .venv/bin/activate`
   - Windows - `.venv\Scripts\activate`
3. Add pip for Azure Functions `python -m ensurepip --upgrade`
4. Update requirements (only required if out of date)
    - Use `uv pip compile pyproject.toml -o requirements.txt`

<!--References-->