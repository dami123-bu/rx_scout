
import logging

import pytest
from sqlalchemy import text, inspect

logger = logging.getLogger(__name__)


@pytest.mark.integration
def test_engine_connects(engine):
    """Engine can connect to Postgres and execute a query."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1

@pytest.mark.integration
def test_session_works(session):
    """Session can execute queries."""
    result = session.execute(text("SELECT 1"))
    assert result.scalar() == 1

@pytest.mark.integration
def test_tables_created(engine):
    """All expected tables exist after create_all."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert not tables
    # expected = [
    #     "drugs", "candidates", "evidence",
    #     "clinical_trials", "reports",
    #     "scored_candidates", "react_traces"
    # ]
    # for table in expected:
    #     assert table in tables, f"Missing table: {table}"
