"""Add initial seed data

Revision ID: 6e78535ca849
Revises: 737a3096074f
Create Date: 2024-11-23 15:42:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

revision = '6e78535ca849'
down_revision = '737a3096074f'

def upgrade():
    # Create reference tables
    customers = table('customers',
        column('id', sa.Integer),
        column('ip_address', sa.BigInteger),
        column('domain', sa.String),
        column('created_at', sa.DateTime)
    )

    blocked_ips = table('blocked_ips',
        column('id', sa.Integer),
        column('ip_address', sa.BigInteger),
        column('is_blocked', sa.Boolean),
        column('blocked_at', sa.DateTime)
    )

    text_messages = table('text_messages',
        column('id', sa.Integer),
        column('customer_id', sa.Integer),
        column('ip_address', sa.BigInteger),
        column('message', sa.String),
        column('is_malicious', sa.Boolean),
        column('created_at', sa.DateTime),
        column('updated_at', sa.DateTime)
    )

    mouse_events = table('mouse_events',
        column('id', sa.Integer),
        column('customer_id', sa.Integer),
        column('ip_address', sa.BigInteger),
        column('x', sa.Integer),
        column('y', sa.Integer),
        column('viewport_x', sa.Integer),
        column('viewport_y', sa.Integer),
        column('is_malicious', sa.Boolean),
        column('created_at', sa.DateTime),
        column('updated_at', sa.DateTime)
    )

    network_events = table('network_events',
        column('id', sa.Integer),
        column('customer_id', sa.Integer),
        column('ip_address', sa.BigInteger),
        column('x', sa.Integer),
        column('y', sa.Integer),
        column('viewport_x', sa.Integer),
        column('viewport_y', sa.Integer),
        column('is_malicious', sa.Boolean),
        column('created_at', sa.DateTime),
        column('updated_at', sa.DateTime)
    )

    # Insert seed data
    op.bulk_insert(customers,
        [
            {
                'ip_address': 3232235777,  # 192.168.1.1
                'domain': 'example.com'
            }
        ]
    )

    op.bulk_insert(blocked_ips,
        [
            {
                'ip_address': 3232235778,  # 192.168.1.2
                'is_blocked': True
            }
        ]
    )

    op.bulk_insert(text_messages,
        [
            {
                'customer_id': 1,
                'ip_address': 3232235777,
                'message': 'Hello, this is a test message',
                'is_malicious': False
            }
        ]
    )

    op.bulk_insert(mouse_events,
        [
            {
                'customer_id': 1,
                'ip_address': 3232235777,
                'x': 100,
                'y': 200,
                'viewport_x': 1920,
                'viewport_y': 1080,
                'is_malicious': False
            }
        ]
    )

    op.bulk_insert(network_events,
        [
            {
                'customer_id': 1,
                'ip_address': 3232235777,
                'x': 150,
                'y': 250,
                'viewport_x': 1920,
                'viewport_y': 1080,
                'is_malicious': False
            }
        ]
    )

def downgrade():
    # Remove all seeded data
    op.execute('DELETE FROM network_events')
    op.execute('DELETE FROM mouse_events')
    op.execute('DELETE FROM text_messages')
    op.execute('DELETE FROM blocked_ips')
    op.execute('DELETE FROM customers')