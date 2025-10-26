"""Add is_deleted column to Product

Revision ID: ba686050360d
Revises: c3bb4d28cfff
Create Date: 2025-10-25 17:52:33.676175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba686050360d'
down_revision: Union[str, Sequence[str], None] = 'c3bb4d28cfff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('products', sa.Column(
        'is_deleted',
        sa.Boolean(),
        nullable=False,
        server_default=sa.text('false')  # This sets default for existing rows
    ))
    # Optional: remove the default after setting values if you don't want it for future inserts
    op.alter_column('products', 'is_deleted', server_default=None)

def downgrade():
    op.drop_column('products', 'is_deleted')
