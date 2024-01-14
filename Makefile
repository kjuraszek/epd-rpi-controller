-include .env  # not fail if .env not found

VENV = venv
CONTROLLER = controller
FRONT = front

PYTHON_VERSION = 3.11
SYSTEM_PYTHON = $(shell which python$(PYTHON_VERSION))

PYTHON_CONTROLLER = $(VENV)/bin/python$(PYTHON_VERSION)

PIP_CONTROLLER = $(VENV)/bin/pip$(PYTHON_VERSION)

venv:
ifneq ($(shell test -d $(VENV) && echo -n 1), 1)
	@echo 'Venv not exists. Proceeding with setting up virtual environment'
	$(SYSTEM_PYTHON) -m venv $(VENV)
else ifeq ($(shell test -d $(VENV) && test -f $(PYTHON_CONTROLLER) && echo -n 1), 1)
	@echo 'Venv exists with Python $(PYTHON_VERSION). Nothing to do in this step, moving forward.'
else
	@echo 'Venv exists without Python $(PYTHON_VERSION). Consider removing or renaming this directory to avoid conflicts and run command again.'
	@exit 1
endif

install: venv
	$(PIP_CONTROLLER) install -r $(CONTROLLER)/requirements.txt
	# W/A for issues with RPi.GPIO
	$(PIP_CONTROLLER) install --upgrade --force-reinstall RPi.GPIO
ifeq ($(shell test -f $(CONTROLLER)/custom_views/custom_requirements.txt && echo -n 0), 0)
	@echo 'Installing custom_requirements.'
	$(PIP_CONTROLLER) install -r $(CONTROLLER)/custom_views/custom_requirements.txt
else
	@echo 'No custom_requirements.txt file - skipping.'
endif

install-dev: install
	$(PIP_CONTROLLER) install -r $(CONTROLLER)/requirements_development.txt -r $(CONTROLLER)/custom_views/examplary_views/views_requirements.txt

install-ui:
	npm install --prefix $(FRONT)

create-config:
ifeq ($(shell test -s epd-rpi-controller.cfg && echo -n 0), 0)
	@echo 'Skipping this step - epd-rpi-controller.cfg file exists.'
else
	cp epd-rpi-controller.example.cfg epd-rpi-controller.cfg
endif

create-env:
ifeq ($(shell test -s .env && echo -n 0), 0)
	@echo 'Skipping this step - .env file exists.'
else
	cp .env.example .env
endif

create-docker-network:
	docker network create epd-rpi-network || true

prepare: install install-ui create-config create-env create-docker-network create-assets-folder

create-views-file:
ifeq ($(shell test -s controller/custom_views/views.py && echo -n 0), 0)
	@echo 'Skipping - controller/custom_views/views.py file exists.'
else
	cp controller/custom_views/example.py controller/custom_views/views.py
endif

create-assets-folder:
ifeq ($(shell test -s assets && echo -n 0), 0)
	@echo 'Skipping - assets dir exists.'
else
	mkdir assets
endif

run-controller:
	$(PYTHON_CONTROLLER) $(CONTROLLER)/main.py

run-ui:
	export VITE_UI_PORT=$(VITE_UI_PORT) &&\
	export VITE_API_PORT=$(VITE_API_PORT) &&\
	npm run --prefix $(FRONT) dev

build-docker:
	docker compose --profile all build

prepare-spotipy: install
	$(PYTHON_CONTROLLER) $(CONTROLLER)/spotipy_helper.py

run-docker:
	docker compose up -d

run-docker-kafka-full:
	docker compose --profile kafka-rest --profile kafdrop up -d

run-docker-ctrl:
	docker compose --profile controller up -d

run-docker-ctrl-ui:
	docker compose --profile controller --profile ui up -d

run-docker-ui:
	docker compose --profile ui up -d

run-docker-all:
	docker compose --profile all up -d

stop-docker:
	docker compose --profile all stop

clean-docker:
	docker compose down --rmi=all --volume

lint-pylint:
	$(VENV)/bin/pylint --rcfile=$(CONTROLLER)/.pylintrc $(CONTROLLER)/

lint-flake8:
	$(VENV)/bin/flake8 --config=$(CONTROLLER)/.flake8 $(CONTROLLER)/

lint-ui:
	npm run --prefix $(FRONT) lint

lint-controller: lint-pylint lint-flake8

typing-mypy:
	$(VENV)/bin/mypy $(CONTROLLER) --config-file $(CONTROLLER)/mypy.ini --strict

test-controller:
	$(VENV)/bin/pytest $(CONTROLLER)/tests/

test-ui:
	npm run --prefix $(FRONT) test

bandit-scan:
	$(VENV)/bin/bandit --ini $(CONTROLLER)/.bandit $(CONTROLLER) -r

black-format:
	$(VENV)/bin/black $(CONTROLLER)

check-controller: install-dev lint-controller typing-mypy test-controller bandit-scan

check-ui: lint-ui test-ui

check: check-controller check-ui

sphinx-md: install-dev
	export EPD_RPI_CONFIG_FILE=epd-rpi-controller.example.cfg && $(VENV)/bin/sphinx-build -M markdown docs/controller docs/controller/_build

sphinx-html: install-dev
	export EPD_RPI_CONFIG_FILE=epd-rpi-controller.example.cfg && $(VENV)/bin/sphinx-build -M html docs/controller docs/controller/_build

vue-docgen: install-ui
	npm run --prefix $(FRONT) docgen

docs: sphinx-md vue-docgen

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -rf $(CONTROLLER)/__pycache__
	rm -rf $(CONTROLLER)/api/__pycache__
	rm -rf $(CONTROLLER)/custom_views/views.py
	rm -rf $(CONTROLLER)/custom_views/custom_requirements.txt
	rm -rf $(CONTROLLER)/cov_html
	rm -rf $(FRONT)/node_modules
	rm -rf $(FRONT)/dist
	rm -rf docs/controller/_build
	rm -rf epd-rpi-controller.cfg
	rm -rf mocked_epd.png
	rm -rf assets
	
.PHONY: venv install install-ui create-env create-config create-assets-folder copy-config prepare run-controller run-ui build-docker run-docker stop-docker clean-docker clean
