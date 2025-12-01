"""initial migration: create users and memory tables

Revision ID: 0001_initial
Revises: 
Create Date: 2025-12-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    from jinx.db.session import Base
    Base.metadata.create_all(bind=bind)


def downgrade():
    bind = op.get_bind()
    from jinx.db.session import Base
    Base.metadata.drop_all(bind=bind)
