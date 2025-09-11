"""add content column to posts table

Revision ID: 07e09b772efc
Revises: 56ff080f1369
Create Date: 2025-08-30 23:30:17.852033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07e09b772efc'
down_revision: Union[str, Sequence[str], None] = '56ff080f1369'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))

    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
