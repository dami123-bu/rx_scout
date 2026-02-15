.PHONY: db-up db-down db-reset db-shell ingest index run test test-unit lint typecheck

db-up:
	docker compose up -d

db-down:
	docker compose down

db-reset:
	docker compose down -v
	docker compose up -d

db-shell:
	docker exec -it rx_scout-db-1 psql -U rxscout -d rxscout

ingest:
	python -m rxscout.data.ingest

index:
	python -m rxscout.rag.indexer

run:
	streamlit run src/rxscout/ui/app.py

test:
	pytest

test-unit:
	pytest -m "not integration"

lint:
	ruff check src tests
	ruff format --check src tests

typecheck:
	mypy src
