"""initial migration

Revision ID: adcb321513ca
Revises: 
Create Date: 2024-11-24 02:26:46.030387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adcb321513ca'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('domain')
    )
    op.create_index(op.f('ix_customers_id'), 'customers', ['id'], unique=False)
    op.create_table('ip_lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_address', sa.String(length=255), nullable=False),
    sa.Column('is_blocked', sa.Boolean(), nullable=True),
    sa.Column('domain', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['domain'], ['customers.domain'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ip_lists_id'), 'ip_lists', ['id'], unique=False)
    op.create_table('local_storage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.String(length=255), nullable=True),
    sa.Column('content', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('blocked_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('confidence_score', sa.Float(), nullable=True),
    sa.Column('is_malicious', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['domain'], ['customers.domain'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_local_storage_id'), 'local_storage', ['id'], unique=False)
    op.create_table('mouse_events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.String(length=255), nullable=True),
    sa.Column('ip_address', sa.String(length=255), nullable=False),
    sa.Column('x', sa.Integer(), nullable=False),
    sa.Column('y', sa.Integer(), nullable=False),
    sa.Column('viewport_x', sa.Integer(), nullable=False),
    sa.Column('viewport_y', sa.Integer(), nullable=False),
    sa.Column('is_malicious', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('blocked_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['domain'], ['customers.domain'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mouse_events_id'), 'mouse_events', ['id'], unique=False)
    op.create_table('network_events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.String(length=255), nullable=True),
    sa.Column('ip_address', sa.String(length=255), nullable=False),
    sa.Column('headers', sa.JSON(), nullable=False),
    sa.Column('method', sa.String(length=255), nullable=False),
    sa.Column('body', sa.JSON(), nullable=False),
    sa.Column('cookies', sa.JSON(), nullable=False),
    sa.Column('url', sa.String(length=2048), nullable=False),
    sa.Column('status_code', sa.Integer(), nullable=False),
    sa.Column('is_malicious', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('blocked_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['domain'], ['customers.domain'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_network_events_id'), 'network_events', ['id'], unique=False)
    op.create_table('text_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.String(length=255), nullable=True),
    sa.Column('ip_address', sa.String(length=255), nullable=False),
    sa.Column('message', sa.String(length=1000), nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('is_malicious', sa.Boolean(), nullable=True),
    sa.Column('caused_block', sa.Boolean(), nullable=True),
    sa.Column('confidence_score', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('blocked_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['domain'], ['customers.domain'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_text_messages_id'), 'text_messages', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_text_messages_id'), table_name='text_messages')
    op.drop_table('text_messages')
    op.drop_index(op.f('ix_network_events_id'), table_name='network_events')
    op.drop_table('network_events')
    op.drop_index(op.f('ix_mouse_events_id'), table_name='mouse_events')
    op.drop_table('mouse_events')
    op.drop_index(op.f('ix_local_storage_id'), table_name='local_storage')
    op.drop_table('local_storage')
    op.drop_index(op.f('ix_ip_lists_id'), table_name='ip_lists')
    op.drop_table('ip_lists')
    op.drop_index(op.f('ix_customers_id'), table_name='customers')
    op.drop_table('customers')
    # ### end Alembic commands ###