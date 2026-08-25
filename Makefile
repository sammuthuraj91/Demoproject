VENV=.venv

PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
PYTEST=$(VENV)/bin/pytest
RUFF=$(VENV)/bin/ruff
BANDIT=$(VENV)/bin/bandit

REPORTS=reports

.PHONY: setup test e2e lint security build all clean

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

reports:
	mkdir -p $(REPORTS)

test: reports
	APPNAME_ENV=test \
	$(PYTEST) tests \
		--cov=appname \
		--cov-report=term-missing \
		--cov-report=xml:$(REPORTS)/coverage.xml \
		--junitxml=$(REPORTS)/pytest.xml

e2e: reports
	BASE_URL=http://127.0.0.1:5000 \
	$(PYTEST) tests/e2e \
		--junitxml=$(REPORTS)/e2e.xml

lint:
	$(RUFF) check .

security: reports
	$(BANDIT) -r appname \
		-f json \
		-o $(REPORTS)/bandit.json

build:
	sudo docker build \
		-f docker/Dockerfile \
		-t mytemplate:latest \
		.

all: test e2e lint security build
