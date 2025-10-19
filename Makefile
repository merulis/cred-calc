SHELL := /bin/bash

APP_NAME = cred_calc
ENTRY = main.py
ICON = assets/icon.ico
REQ = req.txt

.PHONY: venv deps build rebuild clean run

venv:
	@if [ ! -d ".venv" ]; then python3 -m venv .venv; fi

deps: venv 
	@{ \
		source .venv/bin/activate; \
		pip install -r $(REQ); \
	}

build: deps
	@{ \
		source .venv/bin/activate; \
		pyinstaller --clean --onefile --windowed --icon=$(ICON) --name $(APP_NAME) $(ENTRY); \
	}

rebuild: clean build

run:
	./dist/$(APP_NAME)

clean:
	rm -rf build dist __pycache__ *.spec
