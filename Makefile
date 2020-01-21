upgrade-pip-tools-setuptools:
	pip install --upgrade pip-tools setuptools

update-main-deps: upgrade-pip-tools-setuptools
	pip-compile --upgrade --generate-hashes --quiet --output-file requirements/main.txt requirements/main.in

update-dev-deps: upgrade-pip-tools-setuptools
	pip-compile --upgrade --generate-hashes --quiet --output-file requirements/dev.txt requirements/dev.in

update-prod-deps: upgrade-pip-tools-setuptools
	pip-compile --upgrade --generate-hashes --quiet --output-file requirements/prod.txt requirements/prod.in

update-all-deps: update-main-deps update-dev-deps update-prod-deps

install-deps-dev:
	pip-sync requirements/dev.txt

install-deps-prod:
	pip-sync requirements/prod.txt
