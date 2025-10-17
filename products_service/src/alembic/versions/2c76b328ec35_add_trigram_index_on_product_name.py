"""Add trigram index on product name

Revision ID: 2c76b328ec35
Revises: d00e07956c55
Create Date: 2025-10-17 12:02:14.235577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c76b328ec35'
down_revision: Union[str, Sequence[str], None] = 'd00e07956c55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_products_name_trgm
        ON products
        USING gin (name gin_trgm_ops)
    """)

def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_products_name_trgm")
