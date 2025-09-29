# Contributing Guidelines

## Branch Strategy
- Create feature branches from `main` using the pattern: `feat/<short-name>` or `fix/<short-name>`.
- Open a Pull Request (PR) to `main` and request a review before merging.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# OR
.\venv\Scripts\activate     # Windows

pip install -r requirements.txt
cp .env.example .env  # Set your environment variables
