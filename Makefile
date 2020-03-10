API_USER?=""
API_KEY?=""

build:
	python3 setup.py sdist bdist_wheel

upload:
	@TWINE_PASSWORD=$(API_KEY) TWINE_USERNAME=$(API_USER);python3 -m twine upload dist/*

clean:
	rm -r build dist pythfinder.egg-info
