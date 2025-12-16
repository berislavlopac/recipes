# List available recipes.
help:
    @just --list --unsorted

# Run unit tests without coverage.
test:
    uv run pytest --cov

# Run unit tests with coverage.
test-cov:
    uv run pytest

# Run linting and formating checks.
lint:
    uv run deptry .
    uv run ruff format --check .
    uv run ruff check .

# Run static typing analysis.
type:
    uv run mypy --install-types --non-interactive

# Run security and safety checks.
safety:
    uvx vulture  --exclude .venv --min-confidence 100 .
    uvx radon mi --show --multi --min B .
    uvx complexipy --quiet  --exclude recipes/presentation/streamlit.py .

# Run all checks.
check: lint safety type

# Run checks and tests.
ready: lint safety type test

# Reformat the code using isort and ruff.
[confirm]
reformat:
    uv run ruff format .
    uv run ruff check --select I --fix .

# Generate a new fernet encryption key.
[confirm]
fernet:
    uv run python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Extract current production requirements. Save to a file by appending `> requirements.txt`.
reqs:
    uv export --no-dev

# Run the local server.
run:
    uv run streamlit run main.py
