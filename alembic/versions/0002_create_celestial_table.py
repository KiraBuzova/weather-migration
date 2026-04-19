"""Create celestial_events table
Revision ID: 0002
Revises: 0001
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'celestial_events',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('weather_id', sa.Integer(),
                  sa.ForeignKey('weather_records.id'), nullable=False),
        sa.Column('sunrise', sa.Time()),
        sa.Column('sunset', sa.Time()),
        sa.Column('moonrise', sa.Time()),
        sa.Column('moonset', sa.Time()),
        sa.Column('moon_phase', sa.String(50)),
        sa.Column('moon_illumination', sa.Float()),
    )

def downgrade():
    op.drop_table('celestial_events')