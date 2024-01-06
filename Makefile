# help
# make venv
# run local
# run test
# generate new migration
# apply migrations
# build usual
# build for arm-v7

test-local:
	.venv/bin/pytest ./tests

test-ci:
	.venv/bin/pytest ./test -v --cov=tracker_bot --cov-report=term-missing --disable-warnings --junitxml=report.xml
	.venv/bin/coverage xml

develop:
	rm -rf .venv
	python3.11 -m venv .venv
	.venv/bin/pip install -U pip poetry
	.venv/bin/poetry config virtualenvs.create false
	.venv/bin/poetry install

hooks:
	pre-commit install
