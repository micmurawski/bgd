import datetime

import peewee

from .constants import DATABASE, DATABASE_HOST, DATABASE_PORT, DATABASE_USER


def get_db_password() -> str:
    return "postgres"


db = peewee.PostgresqlDatabase(
    DATABASE,
    user=DATABASE_USER,
    password=get_db_password(),
    host=DATABASE_HOST,
    port=DATABASE_PORT
)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = peewee.AutoField(primary_key=True)
    username = peewee.CharField(max_length=100, unique=True)
    email = peewee.CharField(max_length=100, unique=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'users'


class Item(BaseModel):
    item_id = peewee.AutoField(primary_key=True)
    name = peewee.CharField(max_length=200)
    description = peewee.TextField(null=True)
    price = peewee.DecimalField(max_digits=10, decimal_places=2)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    seller = peewee.ForeignKeyField(User, backref='items')

    class Meta:
        table_name = 'items'


class Transaction(BaseModel):
    transaction_id = peewee.AutoField(primary_key=True)
    date = peewee.DateTimeField(default=datetime.datetime.now)
    seller = peewee.ForeignKeyField(User, backref='sales')
    buyer = peewee.ForeignKeyField(User, backref='purchases')
    item = peewee.ForeignKeyField(Item, backref='transactions')
    price = peewee.DecimalField(max_digits=10, decimal_places=2)
    quantity = peewee.IntegerField(default=1)

    class Meta:
        table_name = 'transactions'


class Review(BaseModel):
    review_id = peewee.AutoField(primary_key=True)
    transaction = peewee.ForeignKeyField(
        Transaction, backref='reviews', unique=True)
    rating = peewee.IntegerField(
        constraints=[peewee.Check('rating >= 1 and rating <= 5')])
    comment = peewee.TextField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'reviews'


def create_tables():
    with db:
        db.create_tables([User, Item, Transaction, Review])
