# init:
# 	pip install -r requirements.txt

test:
	python3 -m unittest midihub/**/test*.py

# .PHONY: init test
.PHONY: test
