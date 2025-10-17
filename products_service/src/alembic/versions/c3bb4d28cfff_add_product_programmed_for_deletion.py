"""Add product programmed for deletion

Revision ID: c3bb4d28cfff
Revises: 2c76b328ec35
Create Date: 2025-10-17 14:00:28.635930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3bb4d28cfff'
down_revision: Union[str, Sequence[str], None] = '2c76b328ec35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
               ALTER TABLE products
               ADD COLUMN programmed_deletion BOOLEAN
               """)
    op.execute("UPDATE products SET programmed_deletion = FALSE WHERE 1=1")
    op.execute("""
        ALTER TABLE products
        ALTER COLUMN programmed_deletion SET NOT NULL
    """)
    pass


def downgrade() -> None:
    op.execute("""
        ALTER TABLE products
        DROP COLUMN programmed_deletion
    """)
