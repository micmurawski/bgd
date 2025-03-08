"""
Database configuration constants for Sysbiz.

This module defines the necessary constants for connecting to the PostgreSQL database.
These values can be modified to point to different database instances for
development, testing, or production environments.

Environment variables can override these defaults:
- DATABASE_HOST: The hostname of the PostgreSQL server
"""

import os

DATABASE = "postgres_db"
DATABASE_USER = "postgres"
# Get DATABASE_HOST from environment variable, or use "localhost" as default
DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
DATABASE_PORT = 5432