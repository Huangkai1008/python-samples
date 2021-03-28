format:
	isort . && black . && flake8 .
test:
	pytest
