output/: clean
	python3 src/texdict2/parser.py;
	rm output/*/*.{aux,idx};
	rm -r input/;
	echo "Please double-check the filenames.";
clean:
	rm -fr output/ input/;
