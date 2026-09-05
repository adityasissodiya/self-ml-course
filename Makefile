.PHONY: check-links hours status lab-05

PYTHON ?= python

check-links:
	$(PYTHON) scripts/check_links.py

hours:
	$(PYTHON) scripts/hours.py

status:
	$(PYTHON) scripts/status.py

lab-05:
	docker compose -f labs/05-openfga-crossorg/docker-compose.yml up -d

