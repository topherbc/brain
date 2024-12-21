# Makefile for brain project

.PHONY: install test lint clean

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=src

lint:
	pylint src/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage
	rm -rf .pytest_cache
	rm -rf .pyc
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info