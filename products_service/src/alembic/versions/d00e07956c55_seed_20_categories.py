"""Seed 20 categories

Revision ID: d00e07956c55
Revises: 0747acdf2251
Create Date: 2025-10-17 11:58:41.986101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd00e07956c55'
down_revision: Union[str, Sequence[str], None] = '0747acdf2251'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

# Define a temporary table for bulk insert
category_table = table(
    "categories",
    column("id", Integer),
    column("name", String),
)

def upgrade() -> None:
    categories = [
        {"id": 1, "name": "Electronics"},
        {"id": 2, "name": "Books"},
        {"id": 3, "name": "Clothing"},
        {"id": 4, "name": "Home & Kitchen"},
        {"id": 5, "name": "Sports"},
        {"id": 6, "name": "Toys"},
        {"id": 7, "name": "Beauty"},
        {"id": 8, "name": "Automotive"},
        {"id": 9, "name": "Garden"},
        {"id": 10, "name": "Health"},
        {"id": 11, "name": "Music"},
        {"id": 12, "name": "Movies"},
        {"id": 13, "name": "Pet Supplies"},
        {"id": 14, "name": "Office Products"},
        {"id": 15, "name": "Baby"},
        {"id": 16, "name": "Grocery"},
        {"id": 17, "name": "Industrial"},
        {"id": 18, "name": "Jewelry"},
        {"id": 19, "name": "Shoes"},
        {"id": 20, "name": "Video Games"},
    ]

    op.bulk_insert(category_table, categories)

def downgrade() -> None:
    op.execute("DELETE FROM categories WHERE id BETWEEN 1 AND 20")
