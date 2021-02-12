# init:
# 	pip install -r requirements.txt

test:
	python3 -m unittest tests/*_test.py

# .PHONY: init test
.PHONY: test
