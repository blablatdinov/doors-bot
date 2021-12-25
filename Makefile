run:
	./manage.py start

lint:
	isort . && flake8 .

test:
	pytest
