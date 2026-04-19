"""Create weather_records table
Revision ID: 0001
Revises:
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'weather_records',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('country', sa.String(100), nullable=False),
        sa.Column('location_name', sa.String(150)),
        sa.Column('last_updated', sa.Date(), nullable=False),
        sa.Column('wind_kph', sa.Float()),
        sa.Column('wind_degree', sa.Integer()),
        sa.Column('wind_direction',
                  sa.Enum('N','NNE','NE','ENE','E','ESE','SE','SSE',
                          'S','SSW','SW','WSW','W','WNW','NW','NNW',
                          name='winddirectionenum')),
        sa.Column('temperature_c', sa.Float()),
        sa.Column('humidity', sa.Integer()),
        sa.Column('condition_text', sa.String(255)),
    )

def downgrade():
    op.drop_table('weather_records')
    op.execute("DROP TYPE IF EXISTS winddirectionenum")