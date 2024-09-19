install_dependencies:
	pip install -r requirements.txt

local_test:
	export DB_CONNECTION_STATUS=$$? && \
	python -Xfrozen_modules=off -m uvicorn src.app.main:app --port 8000 --log-level debug --reload

alembic_revision:
	@echo "Please enter a message for the review:"
	@read MESSAGE; \
	rev_id=$$(date -u +"%Y%m%d%H%M%S"); \
	alembic -c ./src/alembic.ini revision -m "$$MESSAGE" --rev-id="$$rev_id"

alembic_autogenerate_revision:
	@echo "Please enter a message for the review:"
	@read MESSAGE; \
	rev_id=$$(date -u +"%Y%m%d%H%M%S"); \
	alembic -c ./src/alembic.ini revision --autogenerate -m "$$MESSAGE" --rev-id="$$rev_id"

alembic_upgrade:
	alembic -c ./src/alembic.ini upgrade head

alembic_downgrade:
	alembic -c ./src/alembic.ini downgrade base

alembic_history:
	alembic -c ./src/alembic.ini history

reset_db:
	alembic -c ./src/alembic.ini downgrade base && alembic -c ./src/alembic.ini upgrade head &&  alembic -c ./src/alembic.seeders.ini -x env=seeders upgrade head
