"""Add go_outside column
Revision ID: 0003
Revises: 0002
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('celestial_events',
        sa.Column('go_outside', sa.Boolean(), server_default='false', nullable=False))

def downgrade():
    op.drop_column('celestial_events', 'go_outside')