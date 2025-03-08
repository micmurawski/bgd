# BGD

A PostgreSQL-based business transaction system that manages users, items, transactions, and reviews.

## Overview

Sysbiz is a data management system built with Python and PostgreSQL that handles e-commerce data relationships. It provides a framework for:

- User account management
- Item listings
- Transaction tracking
- Review management

## Project Structure

```
sysbiz/
├── data/                      # CSV data files
│   ├── items.csv              # Item listings data
│   ├── reviews.csv            # Customer reviews
│   ├── transactions.csv       # Transaction records
│   └── users.csv              # User account data
├── sysbiz/                    # Main package
│   ├── __init__.py            # Package initialization
│   ├── constants.py           # Database configuration constants
│   ├── db.py                  # Database models and connection
│   └── main.py                # Application entry point
├── Dockerfile                 # Docker container configuration
├── pyproject.toml             # Project dependencies and metadata
├── poetry.lock                # Pinned dependencies (Poetry)
└── README.md                  # This documentation
```

## Database Schema

The system uses the following data models (defined in `sysbiz/db.py`):

- **User**: Store user information (buyers and sellers)
- **Item**: Product listings with descriptions and pricing
- **Transaction**: Records of purchases between buyers and sellers
- **Review**: Feedback on transactions with ratings

### Model Relationships

```
User (1) ----< Item (1) ----< Transaction (1) ----< Review (1)
  ^              ^                ^
  |              |                |
  +---------- seller              |
  |                               |
  +------------------- buyer -----+
```

## Installation and Setup

### Prerequisites

- Python 3.12 or higher
- Docker and docker-compose
- Poetry (for dependency management)

### Running with Docker

1. Start the PostgreSQL database:

```bash
docker-compose up -d
```

2. Build and run the application container:

```bash
cd sysbiz
docker build -t sysbiz .
docker run sysbiz
```

### Development Setup

1. Install dependencies:

```bash
cd sysbiz
poetry install
```

2. Run the application:

```bash
poetry run python sysbiz/main.py
```