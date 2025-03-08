import csv
from datetime import datetime

import peewee
from peewee import Model

from sysbiz.db import Item, Review, Transaction, User, create_tables, db

file_to_model = {
    'data/users.csv': User,
    'data/items.csv': Item,
    'data/transactions.csv': Transaction,
    'data/reviews.csv': Review,
}


def parse_datetime(dt_str:str) -> datetime:
    return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')


def parse_datetime_in_row(row:dict) -> dict:
    if "date" in row:
        row["date"] = parse_datetime(row["date"])
    if "created_at" in row:
        row["created_at"] = parse_datetime(row["created_at"])
    return row


def load_from_csv(filename: str, model:Model):
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
