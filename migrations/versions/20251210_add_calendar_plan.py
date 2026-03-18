"""add calendar plan table

Revision ID: 20251210_add_calendar_plan.py
Revises: 7c94a18a8094
Create Date: 2025-12-10

"""
revision = '20251210_add_calendar_plan.py'  # This is the key line that's missing
down_revision = '7c94a18a8094'  # Link to the previous migration's revision ID
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
def upgrade():
    op.create_table(
        'calendar_plan',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('educational_plan_id', sa.BigInteger, nullable=False),
        sa.Column('data', sa.JSON, nullable=False),
        sa.Column('file_path', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
def downgrade():
    op.drop_table('calendar_plan')
