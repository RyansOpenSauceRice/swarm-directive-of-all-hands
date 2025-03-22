.PHONY: install test lint format clean

install:
	pip install -r requirements.txt

test:
	pytest tests/

lint:
	flake8 src/
	black --check src/

format:
	black src/

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache/ .coverage htmlcov/