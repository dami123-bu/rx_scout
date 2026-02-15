#!/bin/bash
set -e

# Create the databases
createdb rxscout 2>/dev/null || echo "rxscout already exists"
createdb rxscout_test 2>/dev/null || echo "rxscout_test already exists"

# Run migrations
alembic upgrade head

# Optionally seed reference data
# python scripts/seed_data.py

echo "Done. Databases ready."