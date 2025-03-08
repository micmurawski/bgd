"""
Main entry point for the Sysbiz application.

This module handles data loading from CSV files into the database tables.
It maps CSV files to their corresponding models and provides utilities for
parsing date-time values from the CSV files.
"""

import csv
from datetime import datetime

import peewee
from peewee import Model

from sysbiz.db import Item, Review, Transaction, User, create_tables, db

# Map between CSV files and their corresponding database models
file_to_model = {
    'data/users.csv': User,
    'data/items.csv': Item,
    'data/transactions.csv': Transaction,
    'data/reviews.csv': Review,
}


def parse_datetime(dt_str: str) -> datetime:
    """
    Parse a datetime string into a datetime object.
    
    Args:
        dt_str (str): A string representing a datetime in format 'YYYY-MM-DD HH:MM:SS'
        
    Returns:
        datetime: A datetime object parsed from the input string
    """
    return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')


def parse_datetime_in_row(row: dict) -> dict:
    """
    Parse datetime strings in a CSV row into datetime objects.
    
    Checks for 'date' and 'created_at' fields and converts them
    from strings to datetime objects.
    
    Args:
        row (dict): A dictionary representing a row from a CSV file
        
    Returns:
        dict: The modified row with datetime strings converted to datetime objects
    """
    if "date" in row:
        row["date"] = parse_datetime(row["date"])
    if "created_at" in row:
        row["created_at"] = parse_datetime(row["created_at"])
    return row


def load_from_csv(filename: str, model: Model):
    """
    Load data from a CSV file into a database model.
    
    Args:
        filename (str): Path to the CSV file
        model (Model): Peewee model class to insert the data into
    """
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        items = []
        for row in reader:
            row = parse_datetime_in_row(row)
            items.append(row)
        with db.atomic():
            model.insert_many(items).execute()

        print(f"Loaded {len(items)} items from {filename}")


def main():
    """
    Main function to run the Sysbiz application.
    
    Connects to the database, creates tables if they don't exist,
    and loads sample data from CSV files.
    """
    db.connect()
    create_tables()

    try:
        for file_path, model in file_to_model.items():
            load_from_csv(file_path, model)
    except peewee.IntegrityError as e:
        print(f"Error inserting sample data: {e}")

    db.close()


if __name__ == '__main__':
    main()