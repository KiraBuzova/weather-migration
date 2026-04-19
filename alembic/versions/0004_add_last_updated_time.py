"""Add last_updated_time column
Revision ID: 0004
Revises: 0003
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('weather_records',
        sa.Column('last_updated_time', sa.Time(), nullable=True))

def downgrade():
    op.drop_column('weather_records', 'last_updated_time')