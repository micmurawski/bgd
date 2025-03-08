"""
Database models and connection configuration for Sysbiz.

This module defines the ORM models using Peewee for the Sysbiz application,
including User, Item, Transaction, and Review models.
It handles database connections and provides model definitions with appropriate
relationships between entities.
"""

import datetime

import peewee

from .constants import DATABASE, DATABASE_HOST, DATABASE_PORT, DATABASE_USER


def get_db_password() -> str:
    """
    Retrieve the database password.
    
    Returns:
        str: The password for the PostgreSQL database connection.
    """
    return "postgres"


db = peewee.PostgresqlDatabase(
    DATABASE,
    user=DATABASE_USER,
    password=get_db_password(),
    host=DATABASE_HOST,
    port=DATABASE_PORT
)


class BaseModel(peewee.Model):
    """
    Base model class for all database models.
    
    All other models inherit from this class to ensure they use
    the same database connection.
    """
    class Meta:
        database = db


class User(BaseModel):
    """
    User model representing both buyers and sellers in the system.
    
    Attributes:
        user_id (AutoField): Primary key for user identification.
        username (CharField): Unique username for the user.
        email (CharField): Unique email address for the user.
        created_at (DateTimeField): Timestamp when the user was created.
    """
    user_id = peewee.AutoField(primary_key=True)
    username = peewee.CharField(max_length=100, unique=True)
    email = peewee.CharField(max_length=100, unique=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'users'


class Item(BaseModel):
    """
    Item model representing products listed for sale.
    
    Attributes:
        item_id (AutoField): Primary key for item identification.
        name (CharField): Name of the item.
        description (TextField): Detailed description of the item.
        price (DecimalField): Price of the item.
        created_at (DateTimeField): Timestamp when the item was listed.
        seller (ForeignKeyField): Foreign key linking to the User who sells this item.
    """
    item_id = peewee.AutoField(primary_key=True)
    name = peewee.CharField(max_length=200)
    description = peewee.TextField(null=True)
    price = peewee.DecimalField(max_digits=10, decimal_places=2)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    seller = peewee.ForeignKeyField(User, backref='items')

    class Meta:
        table_name = 'items'


class Transaction(BaseModel):
    """
    Transaction model representing purchases of items.
    
    Attributes:
        transaction_id (AutoField): Primary key for transaction identification.
        date (DateTimeField): Timestamp when the transaction occurred.
        seller (ForeignKeyField): Foreign key linking to the User who sold the item.
        buyer (ForeignKeyField): Foreign key linking to the User who purchased the item.
        item (ForeignKeyField): Foreign key linking to the Item that was purchased.
        price (DecimalField): Price at which the transaction occurred.
        quantity (IntegerField): Number of items purchased in this transaction.
    """
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
    """
    Review model representing feedback on transactions.
    
    Attributes:
        review_id (AutoField): Primary key for review identification.
        transaction (ForeignKeyField): Foreign key linking to the Transaction being reviewed.
        rating (IntegerField): Numerical rating from 1 to 5.
        comment (TextField): Text feedback about the transaction.
        created_at (DateTimeField): Timestamp when the review was created.
    """
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
    """
    Create all database tables for the defined models.
    
    This function should be called when setting up the database for the first time
    or when resetting the database schema.
    """
    with db:
        db.create_tables([User, Item, Transaction, Review])