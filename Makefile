APP_NAME := texlooxup_parser

.venv-$(APP_NAME)/:
	bash -c 'python3 -m venv .venv-$(APP_NAME)/ && . .venv-$(APP_NAME)/bin/activate && pip install -r requirements.txt'

input/:
	mkdir input/;

output/: clean
	python3 src/texdict2/parser.py;
	rm output/*/*.{aux,idx};
	rm -r input/;
	echo "Please double-check the filenames.";

clean:
	rm -fr output/ input/;
