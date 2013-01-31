unit:
	@nosetests -s --verbosity=2

deploy:
	@echo "Make sure you changed the version number if appropriate"
	python setup.py register sdist bdist_wininst upload