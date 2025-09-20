APP_NAME = cred_calc
ENTRY = main.py
ICON = assets/icon.ico

.PHONY: build clean run

build:
	pyinstaller --clean --onefile --windowed --icon=$(ICON) --name $(APP_NAME) $(ENTRY)

run:
	./dist/$(APP_NAME)

clean:
	rm -rf build dist __pycache__ *.spec
