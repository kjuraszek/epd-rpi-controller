VENV = venv
CONTROLLER = controller
FRONT = front

PYTHON_VERSION = 3.9
SYSTEM_PYTHON = $(shell which python$(PYTHON_VERSION))

VENV_ACTIVATE_CONTROLLER = . $(VENV)/bin/activate

PYTHON_CONTROLLER = $(VENV)/bin/python$(PYTHON_VERSION)

PIP_CONTROLLER = $(VENV)/bin/pip

venv:
	test -d $(VENV) || $(SYSTEM_PYTHON) -m venv $(VENV)

install: venv
	$(VENV_ACTIVATE_CONTROLLER) && $(PIP_CONTROLLER) install -r $(CONTROLLER)/requirements.txt
ifeq ($(shell test -f $(CONTROLLER)/custom_views/custom_requirements.txt && echo -n 0), 0)
	@echo 'Installing custom_requirements.'
	$(VENV_ACTIVATE_CONTROLLER) && $(PIP_CONTROLLER) install -r $(CONTROLLER)/custom_views/custom_requirements.txt
else
	@echo 'No custom_requirements.txt file - skipping.'
endif

create-config:
ifeq ($(shell test -s epd-rpi-controller.cfg && echo -n 0), 0)
	@echo 'Skipping this step - epd-rpi-controller.cfg file exists.'
else
	cp epd-rpi-controller.example.cfg epd-rpi-controller.cfg
endif

create-docker-network:
	docker network create epd-rpi-network || true

prepare: install create-config create-docker-network

create-views-file:
ifeq ($(shell test -s controller/custom_views/views.py && echo -n 0), 0)
	@echo 'Skipping - controller/custom_views/views.py file exists.'
else
	cp controller/custom_views/example.py controller/custom_views/views.py
endif

run-controller:
	$(VENV_ACTIVATE_CONTROLLER) && $(PYTHON_CONTROLLER) $(CONTROLLER)/main.py

run-ui:
	npm run --prefix $(FRONT) dev

build-docker:
	docker-compose --profile all build

run-docker:
	docker compose up -d

run-docker-ctrl:
	docker compose --profile controller up -d

run-docker-all:
	docker compose --profile all up -d

stop-docker:
	docker compose --profile all stop

clean-docker:
	docker compose down --rmi=all --volume

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -rf $(CONTROLLER)/__pycache__
	rm -rf $(CONTROLLER)/api/__pycache__
	rm -rf $(CONTROLLER)/custom_views/views.py
	rm -rf $(CONTROLLER)/custom_views/custom_requirements.txt
	rm -rf $(FRONT)/node_modules
	rm -rf $(FRONT)/dist
	rm -rf epd-rpi-controller.cfg
	rm -rf mocked_epd.png
	
.PHONY: venv install create-env create-config copy-config prepare run-controller run-ui build-docker run-docker stop-docker clean-docker clean
